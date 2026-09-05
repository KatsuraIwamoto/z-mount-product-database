"""Deterministic generation of the public datasets and product list."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Literal, cast

import rfc8785
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from z_mount_product_database.repository import (
    JsonObject,
    adapter_record_paths,
    load_json,
    record_paths,
)

FULL_PATH = Path("dist/z-mount-lenses.full.json")
LIGHT_PATH = Path("dist/z-mount-lenses.light.json")
ADAPTER_FULL_PATH = Path("dist/z-mount-adapters.full.json")
PRODUCTS_PATH = Path("PRODUCTS.md")
REPOSITORY_URL = "https://github.com/KatsuraIwamoto/z-mount-product-database"
ISSUE_REPORT_URL = f"{REPOSITORY_URL}/issues/new?template=data-correction.yml"
SCHEMA_BASE_URL = "https://cercidiphyllum.jp/schemas"


class GenerationError(Exception):
    """Raised when generated files cannot be built safely."""


def _metadata(
    *,
    variant: Literal["full", "light"],
    schema_group: Literal["lenses", "adapters"],
    dataset_name: str,
    schema_version: str,
    data_version: str,
    count: int,
) -> JsonObject:
    return {
        "$schema": (
            f"{SCHEMA_BASE_URL}/{schema_version}/{schema_group}/dataset-{variant}.schema.json"
        ),
        "datasetName": dataset_name,
        "datasetVariant": variant,
        "schemaVersion": schema_version,
        "dataVersion": data_version,
        "creator": "Katsura Iwamoto",
        "license": "CC-BY-4.0",
        "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
        "repositoryUrl": REPOSITORY_URL,
        "recordCount": count,
    }


def _shortest_focus_distances(
    measurements: list[JsonObject] | None,
) -> list[JsonObject] | None:
    if not measurements:
        return measurements
    shortest_distance = min(cast("int | float", item["distanceM"]) for item in measurements)
    return [
        measurement for measurement in measurements if measurement["distanceM"] == shortest_distance
    ]


def _reproduction_magnification_upper_bound(measurement: JsonObject) -> int | float:
    if "value" in measurement:
        return cast("int | float", measurement["value"])
    if "maximum" in measurement:
        return cast("int | float", measurement["maximum"])
    return max(cast("list[int | float]", measurement["values"]))


def _greatest_reproduction_magnifications(
    measurements: list[JsonObject] | None,
) -> list[JsonObject] | None:
    if not measurements:
        return measurements
    greatest_magnification = max(
        _reproduction_magnification_upper_bound(measurement) for measurement in measurements
    )
    return [
        measurement
        for measurement in measurements
        if _reproduction_magnification_upper_bound(measurement) == greatest_magnification
    ]


def _light_product(record: JsonObject) -> JsonObject:
    """Return the existing website-compatible light projection."""
    identity = cast("JsonObject", record["identity"])
    official_product_pages = cast("list[JsonObject]", record["officialProductPages"])
    physical = cast("JsonObject", record["physical"])
    filter_interfaces = physical["filterInterfaces"]
    selected_filter_interfaces = (
        [
            {
                key: interface[key]
                for key in ("type", "diameterMm", "filterDiameterMm", "sheetDimensionsMm")
                if key in interface
            }
            for interface in cast("list[JsonObject]", filter_interfaces)
        ]
        if isinstance(filter_interfaces, list)
        else filter_interfaces
    )
    light: JsonObject = {
        "id": record["id"],
        "productType": record["productType"],
        "identity": {
            field: identity[field] for field in ("manufacturerId", "brandId", "productName")
        },
        "lifecycle": record["lifecycle"],
        "officialProductPages": [{"url": page["url"]} for page in official_product_pages],
        "mount": record["mount"],
        "physical": {
            "dimensionMeasurements": physical["dimensionMeasurements"],
            "weightMeasurements": physical["weightMeasurements"],
            "filterInterfaces": selected_filter_interfaces,
        },
    }
    product_type = cast("str", record["productType"])
    if product_type == "lens":
        lens = cast("JsonObject", record["lens"])
        aperture = cast("JsonObject", lens["aperture"])
        selected_aperture: JsonObject = {}
        for aperture_type in ("fNumber", "tNumber"):
            if aperture_type not in aperture:
                continue
            aperture_values = aperture[aperture_type]
            selected_aperture[aperture_type] = (
                {"maximumAperture": aperture_values["maximumAperture"]}
                if isinstance(aperture_values, dict)
                else aperture_values
            )
        focus = cast("JsonObject", lens["focus"])
        selected_focus = {
            focus_type: (
                {"present": focus_value["present"]}
                if isinstance((focus_value := focus[focus_type]), dict)
                else focus_value
            )
            for focus_type in ("autofocus", "manualFocus")
        }
        selected_focus["minimumFocusDistances"] = _shortest_focus_distances(
            cast("list[JsonObject] | None", focus["minimumFocusDistances"])
        )
        selected_focus["reproductionMagnifications"] = _greatest_reproduction_magnifications(
            cast("list[JsonObject] | None", focus["reproductionMagnifications"])
        )
        stabilization = lens["stabilization"]
        selected_stabilization = (
            {"present": stabilization["present"]}
            if isinstance(stabilization, dict)
            else stabilization
        )
        specialized = cast("JsonObject", lens["specialized"])
        light["lens"] = {
            "focalLength": lens["focalLength"],
            "aperture": selected_aperture,
            "coverage": lens["coverage"],
            "focus": selected_focus,
            "stabilization": selected_stabilization,
            "specialized": {key: {} for key in specialized},
        }
    elif product_type == "teleconverter":
        teleconverter = cast("JsonObject", record["teleconverter"])
        light["teleconverter"] = {
            field: teleconverter[field]
            for field in (
                "coverage",
                "magnification",
                "apertureLossStops",
                "supportsAutofocus",
                "compatibleLensIds",
            )
        }
    else:
        pinhole = cast("JsonObject", record["pinhole"])
        light["pinhole"] = {
            field: pinhole[field] for field in ("coverage", "focalLength", "imagingModes")
        }
    return light


def _content_hash(value: Any) -> str:
    try:
        payload = rfc8785.dumps(value)
    except rfc8785.CanonicalizationError as error:
        raise GenerationError(f"Cannot canonicalize contentHash payload: {error}") from error
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _markdown_link_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]").replace("|", "\\|")


type InventoryEntry = tuple[str, str, str, str, str, list[JsonObject]]
type AttentionEntry = tuple[int, str, str, str, list[str], str, list[JsonObject]]
type ResearchSummary = tuple[Counter[str], list[AttentionEntry], int, int, int]


def _brand_inventory(
    root: Path,
    records: list[JsonObject],
    brand_names: dict[str, str],
    dataset: Literal["lenses", "adapters"],
    data_version: str,
) -> dict[str, list[InventoryEntry]]:
    brands: dict[str, list[InventoryEntry]] = {}
    for record in records:
        identity = cast("JsonObject", record["identity"])
        brand_id = cast("str", identity["brandId"])
        brand = brand_names[brand_id]
        product_name = cast("str", identity["productName"])
        product_id = cast("str", record["id"])
        canonical_path = f"data/records/{dataset}/{brand_id}/{product_id}.json"
        research_path = f"research/results/{dataset}/{brand_id}/{product_id}.json"
        research = cast("JsonObject", load_json(root / research_path))
        blob_url = f"{REPOSITORY_URL}/blob/{data_version}"
        brands.setdefault(brand, []).append(
            (
                product_name,
                product_id,
                f"{blob_url}/{canonical_path}",
                f"{blob_url}/{research_path}",
                cast("str", research["reviewedOn"]),
                cast("list[JsonObject]", record["officialProductPages"]),
            )
        )
    return brands


def _official_page_links(pages: list[JsonObject]) -> str:
    if not pages:
        return "—"
    links = []
    for page in pages:
        publisher = cast("JsonObject", page["publisher"])
        region = cast("str | None", page["region"]) or "global"
        label = f"{cast('str', publisher['name'])} ({region}/{cast('str', page['language'])})"
        links.append(f"[{_markdown_link_text(label)}](<{cast('str', page['url'])}>)")
    return "<br>".join(links)


def _lifecycle_statistics(
    records: list[JsonObject],
) -> tuple[int, int, int, Counter[str]]:
    published_announcement_dates = 0
    empty_designations = 0
    unknown_designations = 0
    designation_counts: Counter[str] = Counter()
    for record in records:
        lifecycle = cast("JsonObject", record["lifecycle"])
        if lifecycle["announcementDate"] is not None:
            published_announcement_dates += 1
        designations = cast("list[JsonObject] | None", lifecycle["officialDesignations"])
        if designations is None:
            unknown_designations += 1
        elif not designations:
            empty_designations += 1
        else:
            designation_counts.update(
                {cast("str", designation["type"]) for designation in designations}
            )
    return (
        published_announcement_dates,
        empty_designations,
        unknown_designations,
        designation_counts,
    )


def _research_summary(
    root: Path,
    dataset: Literal["lenses", "adapters"],
    data_version: str,
) -> ResearchSummary:
    status_counts: Counter[str] = Counter()
    attention: list[AttentionEntry] = []
    unresolved_question_count = 0
    included_with_unresolved = 0
    needs_review_without_sources = 0
    for path in sorted((root / "research" / "results" / dataset).glob("*/*.json")):
        result = cast("JsonObject", load_json(path))
        decision = cast("JsonObject", result["decision"])
        status = cast("str", decision["status"])
        status_counts[status] += 1
        sources = cast("list[JsonObject]", result["sources"])
        if status == "needs-review" and not sources:
            needs_review_without_sources += 1
        unresolved = cast("list[str]", result.get("unresolved", []))
        if not unresolved:
            continue
        unresolved_question_count += len(unresolved)
        if status == "included":
            included_with_unresolved += 1
        subject = cast("JsonObject", result["subject"])
        attention.append(
            (
                0 if status == "needs-review" else 1,
                status,
                cast("str", subject["name"]),
                f"{REPOSITORY_URL}/blob/{data_version}/{path.relative_to(root).as_posix()}",
                unresolved,
                cast("str", result["reviewedOn"]),
                sources,
            )
        )
    attention.sort(key=lambda entry: (entry[0], entry[2].casefold(), entry[3]))
    return (
        status_counts,
        attention,
        unresolved_question_count,
        included_with_unresolved,
        needs_review_without_sources,
    )


def _research_markdown_lines(
    dataset: Literal["lenses", "adapters"],
    summary: ResearchSummary,
    *,
    legacy_attention_anchor: bool = False,
) -> list[str]:
    (
        status_counts,
        attention,
        unresolved_question_count,
        included_with_unresolved,
        needs_review_without_sources,
    ) = summary
    lines = [
        f"#### Research results / 調査結果データ (`research/results/{dataset}/`)",
        "",
        "| Metric / 項目 | Count / 件数 |",
        "| --- | ---: |",
        f"| Research results / 調査結果データ | {sum(status_counts.values())} |",
        f"| `included` | {status_counts['included']} |",
        f"| `excluded` | {status_counts['excluded']} |",
        f"| `needs-review` | {status_counts['needs-review']} |",
        f"| Results with `unresolved` / 未解決事項あり | {len(attention)} |",
        f"| Unresolved questions / 未解決事項 | {unresolved_question_count} |",
        f"| `needs-review` with no sources / 情報源なし | {needs_review_without_sources} |",
        "",
    ]
    if legacy_attention_anchor:
        lines.extend(('<a id="needs-attention"></a>', ""))
    attention_anchor = "lens-needs-attention" if dataset == "lenses" else "adapter-needs-attention"
    lines.extend(
        (
            f'<a id="{attention_anchor}"></a>',
            "",
            "### Needs attention / 対応が必要な調査結果",
            "",
            "> [!WARNING]",
            f"> **Needs attention:** {status_counts['needs-review']} `needs-review` results and "
            f"{included_with_unresolved} included results still have unresolved questions.",
            ">",
            f"> **対応が必要:** `needs-review` が {status_counts['needs-review']}件、"
            f"未解決事項が残る `included` が {included_with_unresolved}件あります。",
            "",
            "| Decision / 判断 | Product or candidate / 製品・候補 | "
            "Reviewed on / 最終確認日 | Unresolved / 未解決事項 | Sources / 情報源 |",
            "| --- | --- | --- | --- | --- |",
        )
    )
    for _, status, name, research_url, unresolved, reviewed_on, sources in attention:
        questions = "<br>".join(
            _markdown_link_text(question).replace("\n", " ") for question in unresolved
        )
        source_links = (
            " ".join(
                f"[{index}](<{cast('str', source['url'])}>)"
                for index, source in enumerate(sources, 1)
            )
            or "—"
        )
        lines.append(
            f"| `{status}` | [{_markdown_link_text(name)}]({research_url}) "
            f"| {reviewed_on} | {questions} | {source_links} |"
        )
    return lines


def _products_markdown(
    root: Path,
    products: list[JsonObject],
    adapters: list[JsonObject],
    data_version: str,
) -> str:
    registry = cast(
        "JsonObject", load_json(root / "data" / "product-manufacturer-brand-registry.json")
    )
    brand_names = {
        cast("str", entry["id"]): cast("str", entry["name"])
        for entry in cast("list[JsonObject]", registry["brands"])
    }
    lens_brands = _brand_inventory(root, products, brand_names, "lenses", data_version)
    adapter_brands = _brand_inventory(root, adapters, brand_names, "adapters", data_version)
    blob_url = f"{REPOSITORY_URL}/blob/{data_version}"

    mount_registry = cast("JsonObject", load_json(root / "data" / "mount-system-registry.json"))
    mount_names = {
        cast("str", entry["id"]): cast("str", entry["name"])
        for entry in cast("list[JsonObject]", mount_registry["mountSystems"])
    }
    adapter_source_mounts: dict[str, str] = {}
    for adapter in adapters:
        configurations = cast("list[JsonObject]", adapter["mountConfigurations"])
        adapter_source_mounts[cast("str", adapter["id"])] = "<br>".join(
            _markdown_link_text(mount_names[cast("str", configuration["lensSideMountSystemId"])])
            for configuration in configurations
        )

    product_type_counts = Counter(cast("str", product["productType"]) for product in products)
    (
        lens_announcement_dates,
        lens_empty_designations,
        lens_unknown_designations,
        lens_designation_counts,
    ) = _lifecycle_statistics(products)
    (
        adapter_announcement_dates,
        adapter_empty_designations,
        adapter_unknown_designations,
        adapter_designation_counts,
    ) = _lifecycle_statistics(adapters)
    lens_research = _research_summary(root, "lenses", data_version)
    adapter_research = _research_summary(root, "adapters", data_version)
    lens_status_counts = lens_research[0]
    adapter_status_counts = adapter_research[0]
    mount_configuration_count = sum(
        len(cast("list[JsonObject]", adapter["mountConfigurations"])) for adapter in adapters
    )
    electronic_contact_adapters = sum(
        isinstance(adapter["electronics"], dict)
        and adapter["electronics"].get("electronicContacts") is True
        for adapter in adapters
    )
    optical_adapters = sum(
        isinstance(adapter["conversionOptics"], dict)
        and adapter["conversionOptics"].get("present") is True
        for adapter in adapters
    )

    lines = [
        "# Products / 製品一覧",
        "",
        "> [!NOTE]",
        "> Generated from the canonical records and research results for the lens and related "
        "optical product dataset and the mount adapter dataset.",
        "> Do not edit this file manually.",
        ">",
        "> レンズと関連光学製品のデータセット、およびマウントアダプターのデータセットの"
        "収録製品データと調査結果データから自動生成しています。",
        "> 直接編集しないでください。",
        "",
        "> [!WARNING]",
        "> Inclusion means a product release announcement or sale was confirmed. It does not "
        "mean the product is currently sold, in stock, or available.",
        ">",
        "> 収録済みは、発売発表または販売を確認できたことを示します。現在販売中、在庫あり、"
        "入手可能であることを意味しません。",
        "",
        f"**Included:** Lens and related optical product dataset: {len(products)} products "
        f"across {len(lens_brands)} brands; mount adapter dataset: {len(adapters)} products "
        f"across {len(adapter_brands)} brands.",
        "",
        f"**収録:** レンズと関連光学製品のデータセット：{len(products)}製品、"
        f"{len(lens_brands)}ブランド。マウントアダプターのデータセット："
        f"{len(adapters)}製品、{len(adapter_brands)}ブランド。",
        "",
        f"[Report a correction or addition / 修正・追加を報告]({ISSUE_REPORT_URL})",
        "",
        "## Contents / 目次",
        "",
        "- [Dataset overview / データセット概要](#statistics)",
        "- [Lens and related optical product dataset / レンズと関連光学製品のデータセット]"
        "(#lens-dataset)",
        "  - [Statistics / 統計](#lens-statistics)",
        "  - [Needs attention / 対応が必要な調査結果](#lens-needs-attention)",
        "  - [Products by brand / ブランド別製品](#lens-products-by-brand)",
        "- [Mount adapter dataset / マウントアダプターのデータセット](#adapter-dataset)",
        "  - [Statistics / 統計](#adapter-statistics)",
        "  - [Needs attention / 対応が必要な調査結果](#adapter-needs-attention)",
        "  - [Products by brand / ブランド別製品](#adapter-products-by-brand)",
        "",
        '<a id="statistics"></a>',
        "",
        "## Dataset overview / データセット概要",
        "",
        "| Dataset / データセット | Included products / 収録製品 | Brands / ブランド | "
        "Research results / 調査結果データ | `needs-review` |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| Lens and related optical product dataset / レンズと関連光学製品のデータセット "
        f"| {len(products)} | {len(lens_brands)} | "
        f"{sum(lens_status_counts.values())} | {lens_status_counts['needs-review']} |",
        f"| Mount adapter dataset / マウントアダプターのデータセット | {len(adapters)} | "
        f"{len(adapter_brands)} | {sum(adapter_status_counts.values())} | "
        f"{adapter_status_counts['needs-review']} |",
        "",
        '<a id="lens-dataset"></a>',
        "",
        "## Lens and related optical product dataset / レンズと関連光学製品のデータセット",
        "",
        '<a id="lens-statistics"></a>',
        "",
        "### Statistics / 統計",
        "",
        "#### Canonical records / 収録製品データ (`data/records/lenses/`)",
        "",
        "| Metric / 項目 | Count / 件数 |",
        "| --- | ---: |",
        f"| Included products / 収録製品 | {len(products)} |",
        f"| Brands / ブランド | {len(lens_brands)} |",
        f"| `productType: lens` | {product_type_counts['lens']} |",
        f"| `productType: teleconverter` | {product_type_counts['teleconverter']} |",
        f"| `productType: pinhole` | {product_type_counts['pinhole']} |",
        f"| Published `announcementDate` / 発売発表日あり | {lens_announcement_dates} |",
        f"| `announcementDate: null` | {len(products) - lens_announcement_dates} |",
        f"| `officialDesignations: []` | {lens_empty_designations} |",
        f"| `officialDesignations: null` | {lens_unknown_designations} |",
        *(
            f"| `officialDesignations: {designation}` | {lens_designation_counts[designation]} |"
            for designation in (
                "legacy-product",
                "sales-ended",
                "production-ended",
                "discontinued",
            )
        ),
        "",
    ]
    lines.extend(_research_markdown_lines("lenses", lens_research, legacy_attention_anchor=True))
    lines.extend(
        (
            "",
            '<a id="lens-products-by-brand"></a>',
            "",
            "### Products by brand / ブランド別製品",
            "",
            '"Reviewed on" is the date when the research result was last checked. If no '
            "official page is listed, follow the research result link to review the alternative "
            "evidence.",
            "",
            "「最終確認日」は、調査結果データを最後に確認した日です。公式ページがない場合は、"
            "調査結果データへのリンクから代替の根拠を確認してください。",
        )
    )
    for brand in sorted(lens_brands, key=str.casefold):
        entries = sorted(lens_brands[brand], key=lambda entry: (entry[0].casefold(), entry[1]))
        lines.extend(
            (
                "",
                f"#### {brand} ({len(entries)})",
                "",
                "| Product / 製品 | Product ID / 製品ID | Reviewed on / 最終確認日 | "
                "Official pages / 公式ページ | Research result / 調査結果 |",
                "| --- | --- | --- | --- | --- |",
            )
        )
        for product_name, product_id, canonical_url, research_url, reviewed_on, pages in entries:
            lines.append(
                f"| [{_markdown_link_text(product_name)}]({canonical_url}) "
                f"| `{product_id}` | {reviewed_on} | {_official_page_links(pages)} "
                f"| [Research result: lenses/{product_id} / 調査結果]({research_url}) |"
            )
    lines.extend(
        (
            "",
            '<a id="adapter-dataset"></a>',
            "",
            "## Mount adapter dataset / マウントアダプターのデータセット",
            "",
            '<a id="adapter-statistics"></a>',
            "",
            "### Statistics / 統計",
            "",
            "#### Canonical records / 収録製品データ (`data/records/adapters/`)",
            "",
            "| Metric / 項目 | Count / 件数 |",
            "| --- | ---: |",
            f"| Included mount adapters / 収録マウントアダプター | {len(adapters)} |",
            f"| Brands / ブランド | {len(adapter_brands)} |",
            f"| Mount configurations / マウント構成 | {mount_configuration_count} |",
            f"| `electronics.electronicContacts: true` | {electronic_contact_adapters} |",
            f"| `conversionOptics.present: true` | {optical_adapters} |",
            f"| Published `announcementDate` / 発売発表日あり | {adapter_announcement_dates} |",
            f"| `announcementDate: null` | {len(adapters) - adapter_announcement_dates} |",
            f"| `officialDesignations: []` | {adapter_empty_designations} |",
            f"| `officialDesignations: null` | {adapter_unknown_designations} |",
            *(
                f"| `officialDesignations: {designation}` | "
                f"{adapter_designation_counts[designation]} |"
                for designation in (
                    "legacy-product",
                    "sales-ended",
                    "production-ended",
                    "discontinued",
                )
            ),
            "",
        )
    )
    lines.extend(_research_markdown_lines("adapters", adapter_research))
    lines.extend(
        (
            "",
            '<a id="adapter-products-by-brand"></a>',
            "",
            "### Products by brand / ブランド別製品",
            "",
            '"Reviewed on" is the date when the research result was last checked. If no '
            "official page is listed, follow the research result link to review the alternative "
            "evidence.",
            "",
            '"Source mount" identifies the lens-side mount in the marketed adapter '
            "configuration. It does not guarantee operation with every lens, camera, or firmware "
            "version. Check manufacturer- or brand-official compatibility information and manuals "
            "for a specific combination.",
            "",
            "「最終確認日」は、調査結果データを最後に確認した日です。公式ページがない場合は、"
            "調査結果データへのリンクから代替の根拠を確認してください。",
            "",
            "「変換元マウント」は、製品として販売されたアダプター構成のレンズ側マウントを"
            "示します。すべてのレンズ、カメラ、ファームウェアの組み合わせで動作することは"
            "保証しません。個別の互換性は、メーカーまたはブランドの対応表やマニュアルで"
            "確認してください。",
        )
    )
    for brand in sorted(adapter_brands, key=str.casefold):
        entries = sorted(adapter_brands[brand], key=lambda entry: (entry[0].casefold(), entry[1]))
        lines.extend(
            (
                "",
                f"#### {brand} ({len(entries)})",
                "",
                "| Product / 製品 | Product ID / 製品ID | "
                "Source mount / 変換元マウント | Reviewed on / 最終確認日 | "
                "Official pages / 公式ページ | Research result / 調査結果 |",
                "| --- | --- | --- | --- | --- | --- |",
            )
        )
        for product_name, product_id, canonical_url, research_url, reviewed_on, pages in entries:
            lines.append(
                f"| [{_markdown_link_text(product_name)}]({canonical_url}) "
                f"| `{product_id}` | {adapter_source_mounts[product_id]} "
                f"| {reviewed_on} | {_official_page_links(pages)} "
                f"| [Research result: adapters/{product_id} / 調査結果]({research_url}) |"
            )
    lines.extend(
        (
            "",
            "---",
            "",
            f"This list is available under [CC BY 4.0]({blob_url}/LICENSES/CC-BY-4.0.txt). "
            f"[Scope and attribution]({blob_url}/LICENSING.md)",
            "",
            f"この一覧は [CC BY 4.0]({blob_url}/LICENSES/CC-BY-4.0.txt) で提供します。"
            f"[適用範囲とクレジット]({blob_url}/LICENSING.md)",
        )
    )
    return "\n".join(lines) + "\n"


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _registry_names(document: JsonObject, field: str) -> dict[str, str]:
    return {
        cast("str", entry["id"]): cast("str", entry["name"])
        for entry in cast("list[JsonObject]", document[field])
    }


def _identity_reference_ids(records: list[JsonObject]) -> tuple[set[str], set[str]]:
    manufacturer_ids: set[str] = set()
    brand_ids: set[str] = set()
    for record in records:
        identity = cast("JsonObject", record["identity"])
        manufacturer_ids.add(cast("str", identity["manufacturerId"]))
        brand_ids.add(cast("str", identity["brandId"]))
        alternate_names = identity["alternateNames"]
        if isinstance(alternate_names, list):
            brand_ids.update(
                cast("str", alternate_name["brandId"])
                for alternate_name in alternate_names
                if "brandId" in alternate_name
            )
    return manufacturer_ids, brand_ids


def _reference_map(ids: set[str], names: dict[str, str]) -> JsonObject:
    return {entry_id: {"name": names[entry_id]} for entry_id in sorted(ids)}


def _reference_data(
    records: list[JsonObject],
    manufacturer_names: dict[str, str],
    brand_names: dict[str, str],
    mount_names: dict[str, str],
    *,
    adapter_dataset: bool,
) -> JsonObject:
    manufacturer_ids, brand_ids = _identity_reference_ids(records)
    if adapter_dataset:
        mount_ids = {
            cast("str", configuration[field])
            for record in records
            for configuration in cast("list[JsonObject]", record["mountConfigurations"])
            for field in ("lensSideMountSystemId", "cameraSideMountSystemId")
        }
    else:
        mount_ids = set()
        for record in records:
            mount = cast("JsonObject", record["mount"])
            mount_ids.add(cast("str", mount["systemId"]))
            adapter = mount.get("adapter")
            if isinstance(adapter, dict) and isinstance(adapter.get("nativeMountSystemId"), str):
                mount_ids.add(adapter["nativeMountSystemId"])
    return {
        "manufacturers": _reference_map(manufacturer_ids, manufacturer_names),
        "brands": _reference_map(brand_ids, brand_names),
        "mountSystems": _reference_map(mount_ids, mount_names),
    }


def build_artifacts(root: Path) -> dict[Path, bytes]:
    """Build public artifact bytes without reading their current committed copies."""
    versions = cast("JsonObject", load_json(root / "config" / "versions.json"))
    schema_version = cast("str", versions["schemaVersion"])
    data_version = cast("str", versions["dataVersion"])
    products: list[JsonObject] = []
    for path in record_paths(root):
        record = cast("JsonObject", load_json(path))
        products.append({key: value for key, value in record.items() if key != "$schema"})
    products.sort(key=lambda product: cast("str", product["id"]))
    product_registry = cast(
        "JsonObject", load_json(root / "data" / "product-manufacturer-brand-registry.json")
    )
    mount_registry = cast("JsonObject", load_json(root / "data" / "mount-system-registry.json"))
    manufacturer_names = _registry_names(product_registry, "manufacturers")
    brand_names = _registry_names(product_registry, "brands")
    mount_names = _registry_names(mount_registry, "mountSystems")
    lens_reference_data = _reference_data(
        products,
        manufacturer_names,
        brand_names,
        mount_names,
        adapter_dataset=False,
    )

    full = _metadata(
        variant="full",
        schema_group="lenses",
        dataset_name="Z Mount Lens Database",
        schema_version=schema_version,
        data_version=data_version,
        count=len(products),
    )
    full["contentHash"] = _content_hash(
        {"referenceData": lens_reference_data, "products": products}
    )
    full["referenceData"] = lens_reference_data
    full["products"] = products

    light_products = [_light_product(product) for product in products]
    light = _metadata(
        variant="light",
        schema_group="lenses",
        dataset_name="Z Mount Lens Database",
        schema_version=schema_version,
        data_version=data_version,
        count=len(light_products),
    )
    light["contentHash"] = _content_hash(
        {"referenceData": lens_reference_data, "products": light_products}
    )
    light["referenceData"] = lens_reference_data
    light["products"] = light_products

    adapters: list[JsonObject] = []
    for path in adapter_record_paths(root):
        record = cast("JsonObject", load_json(path))
        adapters.append({key: value for key, value in record.items() if key != "$schema"})
    adapters.sort(key=lambda adapter: cast("str", adapter["id"]))
    adapter_reference_data = _reference_data(
        adapters,
        manufacturer_names,
        brand_names,
        mount_names,
        adapter_dataset=True,
    )
    adapter_full = _metadata(
        variant="full",
        schema_group="adapters",
        dataset_name="Z Mount Adapter Database",
        schema_version=schema_version,
        data_version=data_version,
        count=len(adapters),
    )
    adapter_full["contentHash"] = _content_hash(
        {"referenceData": adapter_reference_data, "adapters": adapters}
    )
    adapter_full["referenceData"] = adapter_reference_data
    adapter_full["adapters"] = adapters

    return {
        FULL_PATH: _json_bytes(full),
        LIGHT_PATH: _json_bytes(light),
        ADAPTER_FULL_PATH: _json_bytes(adapter_full),
        PRODUCTS_PATH: _products_markdown(root, products, adapters, data_version).encode("utf-8"),
    }


def _validate_dataset_documents(root: Path, outputs: dict[Path, bytes]) -> None:
    resources: list[tuple[str, Resource[Any]]] = []
    schemas: dict[str, JsonObject] = {}
    for path in sorted((root / "schemas").rglob("*.schema.json")):
        schema = cast("JsonObject", load_json(path))
        schemas[path.relative_to(root / "schemas").as_posix()] = schema
        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            resources.append((schema_id, Resource.from_contents(schema)))
    registry: Registry[Any] = Registry().with_resources(resources)
    for path, schema_path in (
        (FULL_PATH, "lenses/dataset-full.schema.json"),
        (LIGHT_PATH, "lenses/dataset-light.schema.json"),
        (ADAPTER_FULL_PATH, "adapters/dataset-full.schema.json"),
    ):
        instance = json.loads(outputs[path])
        errors = sorted(
            Draft202012Validator(
                schemas[schema_path],
                registry=registry,
                format_checker=FormatChecker(),
            ).iter_errors(instance),
            key=lambda error: list(error.absolute_path),
        )
        if errors:
            raise GenerationError(f"{path}: {errors[0].message}")


def _write_transaction(root: Path, outputs: dict[Path, bytes]) -> None:
    staged: dict[Path, Path] = {}
    previous: dict[Path, bytes | None] = {}
    replaced: list[Path] = []
    try:
        for relative_path, content in outputs.items():
            destination = root / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            previous[relative_path] = destination.read_bytes() if destination.exists() else None
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{destination.name}.",
                suffix=".tmp",
                dir=destination.parent,
            )
            temporary_path = Path(temporary_name)
            staged[relative_path] = temporary_path
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            temporary_path.chmod(0o644)
        for relative_path in outputs:
            replaced.append(relative_path)
            os.replace(staged[relative_path], root / relative_path)
    except BaseException as error:
        for relative_path in reversed(replaced):
            destination = root / relative_path
            old_content = previous[relative_path]
            if old_content is None:
                destination.unlink(missing_ok=True)
            else:
                destination.write_bytes(old_content)
        if isinstance(error, OSError):
            raise GenerationError(
                f"could not atomically replace generated files: {error}"
            ) from error
        raise
    finally:
        for temporary_path in staged.values():
            temporary_path.unlink(missing_ok=True)


def generate(root: Path) -> dict[Path, bytes]:
    """Atomically regenerate all public files from validated sources."""
    outputs = build_artifacts(root)
    _validate_dataset_documents(root, outputs)
    _write_transaction(root, outputs)
    return outputs
