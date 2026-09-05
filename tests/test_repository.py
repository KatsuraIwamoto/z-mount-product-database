"""High-value checks for the repository data contracts."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlsplit

import pytest
import rfc8785
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from z_mount_product_database import validation as validation_module
from z_mount_product_database.generation import (
    ADAPTER_FULL_PATH,
    FULL_PATH,
    LIGHT_PATH,
    PRODUCTS_PATH,
    GenerationError,
    _content_hash,
    _write_transaction,
    build_artifacts,
)
from z_mount_product_database.repository import (
    RepositoryError,
    adapter_record_paths,
    load_json,
    record_paths,
)
from z_mount_product_database.validation import (
    ADAPTER_RESEARCH_COVERAGE_PATHS,
    INTERNAL_SCHEMA_PATHS,
    LENS_RESEARCH_COVERAGE_PATHS,
    PUBLIC_SCHEMA_PATHS,
    SCHEMA_PATHS,
    Diagnostic,
    _lifecycle_review_diagnostics,
    _load_record_set,
    _official_name_diagnostics,
    _record_semantics,
    _registry_usage_diagnostics,
    _research_coverage_diagnostics,
    _research_source_metadata_diagnostics,
    _schema_registry,
    _schema_set_diagnostics,
    validate_repository,
)

ROOT = Path(__file__).resolve().parents[1]


def _object(path: Path) -> dict[str, Any]:
    value = load_json(path)
    assert isinstance(value, dict)
    return cast("dict[str, Any]", value)


def _json_object_code_blocks(document: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    for section in document.split("```json")[1:]:
        payload = section.split("```", 1)[0].strip()
        try:
            value = json.loads(payload)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            blocks.append(value)
    return blocks


def _payload_hash(value: Any) -> str:
    payload = rfc8785.dumps(value)
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _is_ordered_recursive_subset(subset: Any, source: Any) -> bool:
    if isinstance(subset, dict):
        return isinstance(source, dict) and all(
            key in source and _is_ordered_recursive_subset(value, source[key])
            for key, value in subset.items()
        )
    if isinstance(subset, list):
        if not isinstance(source, list):
            return False
        source_index = 0
        for item in subset:
            while source_index < len(source) and not _is_ordered_recursive_subset(
                item, source[source_index]
            ):
                source_index += 1
            if source_index == len(source):
                return False
            source_index += 1
        return True
    return type(subset) is type(source) and subset == source


def _magnification_upper_bound(measurement: dict[str, Any]) -> int | float:
    if "value" in measurement:
        return cast("int | float", measurement["value"])
    if "maximum" in measurement:
        return cast("int | float", measurement["maximum"])
    return max(cast("list[int | float]", measurement["values"]))


def _schema_refs(value: Any) -> list[str]:
    if isinstance(value, dict):
        own = [value["$ref"]] if isinstance(value.get("$ref"), str) else []
        return own + [ref for child in value.values() for ref in _schema_refs(child)]
    if isinstance(value, list):
        return [ref for child in value for ref in _schema_refs(child)]
    return []


def _schema_property_names(value: Any) -> set[str]:
    if isinstance(value, dict):
        properties = value.get("properties")
        own = set(properties) if isinstance(properties, dict) else set()
        return own | {name for child in value.values() for name in _schema_property_names(child)}
    if isinstance(value, list):
        return {name for child in value for name in _schema_property_names(child)}
    return set()


def _schema_objects(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        return [value, *(item for child in value.values() for item in _schema_objects(child))]
    if isinstance(value, list):
        return [item for child in value for item in _schema_objects(child)]
    return []


def _public_validator(name: str) -> Draft202012Validator:
    resources: list[tuple[str, Resource[Any]]] = []
    schemas: dict[str, dict[str, Any]] = {}
    for schema_name in PUBLIC_SCHEMA_PATHS:
        schema = _object(ROOT / "schemas" / schema_name)
        schemas[schema_name] = schema
        resources.append((cast("str", schema["$id"]), Resource.from_contents(schema)))
    return Draft202012Validator(
        schemas[name],
        registry=Registry[Any]().with_resources(resources),
        format_checker=FormatChecker(),
    )


def test_repository_is_valid() -> None:
    assert validate_repository(ROOT) == []


def test_product_ids_must_be_unique_within_each_namespace(tmp_path: Path) -> None:
    for namespace, noun in (
        ("lenses", "lens-dataset product"),
        ("adapters", "mount adapter"),
    ):
        relative_directory = Path("data/records") / namespace
        for brand in ("brand-a", "brand-b"):
            path = tmp_path / relative_directory / brand / f"{brand}.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({"id": "shared-id"}))

        _records, diagnostics = _load_record_set(
            tmp_path,
            relative_directory,
            {},
            Registry[Any](),
            noun,
        )

        assert diagnostics == [
            Diagnostic(relative_directory.as_posix(), f"duplicate {noun} id 'shared-id'")
        ]


def test_product_ids_may_match_across_namespaces(tmp_path: Path) -> None:
    records_by_namespace: dict[str, dict[str, tuple[Path, dict[str, Any]]]] = {}
    for namespace, noun in (
        ("lenses", "lens-dataset product"),
        ("adapters", "mount adapter"),
    ):
        relative_directory = Path("data/records") / namespace
        path = tmp_path / relative_directory / "example" / "shared-id.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({"id": "shared-id"}))

        records, diagnostics = _load_record_set(
            tmp_path,
            relative_directory,
            {},
            Registry[Any](),
            noun,
        )
        records_by_namespace[namespace] = records
        assert diagnostics == []

    assert set(records_by_namespace["lenses"]) == {"shared-id"}
    assert set(records_by_namespace["adapters"]) == {"shared-id"}


def test_equivalent_official_name_spellings_are_rejected_within_brand_and_field(
    tmp_path: Path,
) -> None:
    records: dict[str, tuple[Path, dict[str, Any]]] = {}
    for record_id, name in (("lens-a", "HD Nano Coating"), ("lens-b", "HD nano-coating")):
        path = tmp_path / "data/records/lenses/example" / f"{record_id}.json"
        records[record_id] = (
            path,
            {
                "identity": {"brandId": "example"},
                "lens": {"coatings": [{"officialName": name}]},
            },
        )

    assert _official_name_diagnostics(tmp_path, records) == [
        Diagnostic(
            "data/records/lenses/example/lens-a.json",
            "example lens.coatings has equivalent officialName spellings: "
            "'HD Nano Coating', 'HD nano-coating'",
        )
    ]


def test_official_names_are_scoped_to_brand_and_field(tmp_path: Path) -> None:
    records = {
        "lens-a": (
            tmp_path / "data/records/lenses/a/lens-a.json",
            {
                "identity": {"brandId": "brand-a"},
                "lens": {"coatings": [{"officialName": "HD Nano Coating"}]},
            },
        ),
        "lens-b": (
            tmp_path / "data/records/lenses/b/lens-b.json",
            {
                "identity": {"brandId": "brand-b"},
                "lens": {"specialElements": [{"officialName": "HD nano-coating"}]},
            },
        ),
    }

    assert _official_name_diagnostics(tmp_path, records) == []


def test_official_name_preserves_lexical_symbols_and_omits_trademark_symbols(
    tmp_path: Path,
) -> None:
    records = {
        "lens-a": (
            tmp_path / "data/records/lenses/example/lens-a.json",
            {
                "identity": {"brandId": "example"},
                "lens": {"coatings": [{"officialName": "T* Coating"}]},
            },
        ),
        "lens-b": (
            tmp_path / "data/records/lenses/example/lens-b.json",
            {
                "identity": {"brandId": "example"},
                "lens": {"coatings": [{"officialName": "T Coating"}]},
            },
        ),
        "lens-c": (
            tmp_path / "data/records/lenses/example/lens-c.json",
            {
                "identity": {"brandId": "example"},
                "lens": {"coatings": [{"officialName": "T*® Coating"}]},
            },
        ),
    }

    assert _official_name_diagnostics(tmp_path, records) == [
        Diagnostic(
            "data/records/lenses/example/lens-a.json",
            "example lens.coatings has equivalent officialName spellings: "
            "'T* Coating', 'T*® Coating'",
        ),
        Diagnostic(
            "data/records/lenses/example/lens-c.json",
            "lens.coatings must omit trademark registration symbols: 'T*® Coating'",
        ),
    ]


def test_compatible_lens_ids_reject_non_lens_product_ids(tmp_path: Path) -> None:
    path = tmp_path / "data/records/lenses/example/teleconverter-a.json"
    path.parent.mkdir(parents=True)
    known_products = {
        "lens-a": {"productType": "lens"},
        "teleconverter-b": {"productType": "teleconverter"},
    }
    known_lens_ids = {
        product_id
        for product_id, product in known_products.items()
        if product["productType"] == "lens"
    }
    record: dict[str, Any] = {
        "id": "teleconverter-a",
        "productType": "teleconverter",
        "teleconverter": {"compatibleLensIds": ["lens-a", "teleconverter-b"]},
    }

    assert _record_semantics(tmp_path, path, record, known_lens_ids) == [
        Diagnostic(
            "data/records/lenses/example/teleconverter-a.json",
            "unresolved compatibleLensId 'teleconverter-b'",
        )
    ]


def test_lens_semantics_require_specialized_names_and_electronic_contacts(
    tmp_path: Path,
) -> None:
    path = tmp_path / "data/records/lenses/example/example.json"
    record: dict[str, Any] = {
        "id": "example",
        "identity": {"productName": "Example AF Macro Lens"},
        "mount": {"electronicContacts": None},
        "lens": {
            "aperture": {"controlMechanism": "electronic"},
            "focus": {"autofocus": {"present": True}},
            "specialized": {},
        },
    }

    assert _record_semantics(tmp_path, path, record, set()) == [
        Diagnostic(
            "data/records/lenses/example/example.json/lens/specialized",
            "productName identifies 'macro', but lens.specialized.macro is absent",
        ),
        Diagnostic(
            "data/records/lenses/example/example.json/mount/electronicContacts",
            "autofocus or electronic aperture requires confirmed electronic contacts",
        ),
    ]


@pytest.mark.parametrize(
    ("product_name", "feature"),
    [
        ("Example Cine Lens", "cinema"),
        ("Example Cinema Lens", "cinema"),
        ("Example Anamorphic Lens", "anamorphic"),
        ("Example Fisheye Lens", "fisheye"),
        ("Example Macro Lens", "macro"),
        ("Example Reflex Lens", "reflex"),
        ("Example Mirror Lens", "reflex"),
        ("Example Probe Lens", "probe"),
    ],
)
def test_lens_semantics_recognize_every_specialized_product_name_pattern(
    tmp_path: Path,
    product_name: str,
    feature: str,
) -> None:
    path = tmp_path / "data/records/lenses/example/example.json"
    record: dict[str, Any] = {
        "id": "example",
        "identity": {"productName": product_name},
        "lens": {"specialized": {}},
    }

    assert _record_semantics(tmp_path, path, record, set()) == [
        Diagnostic(
            "data/records/lenses/example/example.json/lens/specialized",
            f"productName identifies {feature!r}, but lens.specialized.{feature} is absent",
        )
    ]


def test_lens_semantics_do_not_match_specialized_name_substrings(tmp_path: Path) -> None:
    path = tmp_path / "data/records/lenses/example/example.json"
    record: dict[str, Any] = {
        "id": "example",
        "identity": {"productName": "Example Macron Lens"},
        "lens": {"specialized": {}},
    }

    assert _record_semantics(tmp_path, path, record, set()) == []


def test_research_source_metadata_must_be_consistent_for_the_same_url(tmp_path: Path) -> None:
    for namespace, source_type in (("lenses", "catalog"), ("adapters", "collection")):
        path = tmp_path / "research/results" / namespace / "example" / f"{namespace}.json"
        path.parent.mkdir(parents=True)
        path.write_text(
            json.dumps(
                {
                    "sources": [
                        {
                            "url": "https://example.com/products",
                            "publisherRelationship": "manufacturer-or-brand",
                            "sourceType": source_type,
                        }
                    ]
                }
            )
        )

    assert _research_source_metadata_diagnostics(tmp_path) == [
        Diagnostic(
            "research/results/adapters/example/adapters.json/sources/0",
            "source URL 'https://example.com/products' has inconsistent metadata: "
            "manufacturer-or-brand/catalog, manufacturer-or-brand/collection",
        )
    ]


def test_uri_format_validation_is_active() -> None:
    checker = FormatChecker()
    assert checker.conforms("https://example.com/product", "uri")
    assert not checker.conforms("not a URI", "uri")


def test_uri_fields_accept_only_http_urls() -> None:
    for name in PUBLIC_SCHEMA_PATHS:
        for schema in _schema_objects(_object(ROOT / "schemas" / name)):
            if schema.get("format") != "uri":
                continue
            validator = Draft202012Validator(schema, format_checker=FormatChecker())
            assert validator.is_valid("https://example.com/product")
            assert validator.is_valid("http://example.com/product")
            for value in ("javascript:alert(1)", "file:///etc/passwd", "mailto:a@example.com"):
                assert not validator.is_valid(value)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ('{"value": 1, "value": 2}', "duplicate JSON object key 'value'"),
        ('{"value": NaN}', "non-finite JSON number 'NaN'"),
        ('{"value": Infinity}', "non-finite JSON number 'Infinity'"),
        ('{"value": -Infinity}', "non-finite JSON number '-Infinity'"),
    ],
)
def test_json_loader_rejects_ambiguous_values(
    tmp_path: Path,
    content: str,
    message: str,
) -> None:
    path = tmp_path / "invalid.json"
    path.write_text(content)
    with pytest.raises(RepositoryError, match=message):
        load_json(path)


def test_generated_files_are_exact_and_deterministic() -> None:
    outputs = build_artifacts(ROOT)
    assert set(outputs) == {FULL_PATH, LIGHT_PATH, ADAPTER_FULL_PATH, PRODUCTS_PATH}
    for path, content in outputs.items():
        assert (ROOT / path).read_bytes() == content
    assert outputs == build_artifacts(ROOT)


def test_content_hash_uses_rfc8785_reference_vector() -> None:
    products: list[Any] = [
        {
            "z": ["line\nbreak", 9007199254740991],
            "nested": {"雪": 1e-7, "a": -0.0},
            "one": 1.0,
        }
    ]
    canonical = (
        b'[{"nested":{"a":0,"\xe9\x9b\xaa":1e-7},"one":1,"z":["line\\nbreak",9007199254740991]}]'
    )
    expected_hash = "sha256:7ebf6770e78df4de82d8b19aa6b038a568a682bd2e0b80ef18fe1426b7d5bccc"

    assert rfc8785.dumps(products) == canonical
    assert _content_hash(products) == expected_hash
    assert (
        _content_hash(
            [
                {
                    "one": 1.0,
                    "nested": {"a": -0.0, "雪": 1e-7},
                    "z": ["line\nbreak", 9007199254740991],
                }
            ]
        )
        == expected_hash
    )
    assert _content_hash([{**products[0], "z": list(reversed(products[0]["z"]))}]) != expected_hash

    first_root: dict[str, Any] = {"schemaVersion": "1.0.0", "products": products}
    second_root: dict[str, Any] = {"schemaVersion": "9.0.0", "products": products}
    assert _content_hash(first_root["products"]) == _content_hash(second_root["products"])


@pytest.mark.parametrize("value", [9007199254740992, float("nan"), float("inf")])
def test_content_hash_rejects_values_outside_rfc8785_domain(value: int | float) -> None:
    with pytest.raises(GenerationError, match="Cannot canonicalize contentHash payload"):
        _content_hash([value])


def test_generated_files_are_world_readable(tmp_path: Path) -> None:
    path = Path("dist/example.json")
    _write_transaction(tmp_path, {path: b"{}\n"})
    assert stat.S_IMODE((tmp_path / path).stat().st_mode) == 0o644


def test_generated_files_are_restored_when_replacement_is_interrupted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    outputs = {Path("one.json"): b"new one", Path("two.json"): b"new two"}
    for path in outputs:
        (tmp_path / path).write_bytes(f"old {path.stem}".encode())

    real_replace = os.replace
    replacement_count = 0

    def interrupt_second_replace(source: Any, destination: Any) -> None:
        nonlocal replacement_count
        replacement_count += 1
        real_replace(source, destination)
        if replacement_count == 2:
            raise KeyboardInterrupt

    monkeypatch.setattr(os, "replace", interrupt_second_replace)
    with pytest.raises(KeyboardInterrupt):
        _write_transaction(tmp_path, outputs)

    assert (tmp_path / "one.json").read_bytes() == b"old one"
    assert (tmp_path / "two.json").read_bytes() == b"old two"


def test_generated_comparison_waits_for_source_validation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_configuration_diagnostics = validation_module._configuration_diagnostics
    expected = Diagnostic("config/versions.json", "example source error")

    def configuration_with_error(*args: Any, **kwargs: Any) -> tuple[list[Diagnostic], date | None]:
        diagnostics, data_version = original_configuration_diagnostics(*args, **kwargs)
        return [*diagnostics, expected], data_version

    def unexpected_generated_comparison(*args: Any, **kwargs: Any) -> list[Diagnostic]:
        raise AssertionError("generated comparison ran before source validation passed")

    monkeypatch.setattr(validation_module, "_configuration_diagnostics", configuration_with_error)
    monkeypatch.setattr(
        validation_module, "_generated_diagnostics", unexpected_generated_comparison
    )

    assert expected in validate_repository(ROOT)


def test_products_markdown_is_a_linked_brand_inventory() -> None:
    markdown = (ROOT / PRODUCTS_PATH).read_text()
    records = [_object(path) for path in record_paths(ROOT)]
    adapters = [_object(path) for path in adapter_record_paths(ROOT)]
    brands = {record["identity"]["brandId"] for record in records}
    adapter_brands = {record["identity"]["brandId"] for record in adapters}
    lens_research_results = [
        _object(path)
        for path in sorted((ROOT / "research" / "results" / "lenses").glob("*/*.json"))
    ]
    adapter_research_results = [
        _object(path)
        for path in sorted((ROOT / "research" / "results" / "adapters").glob("*/*.json"))
    ]
    lens_status_counts = Counter(result["decision"]["status"] for result in lens_research_results)
    adapter_status_counts = Counter(
        result["decision"]["status"] for result in adapter_research_results
    )
    lens_attention = [result for result in lens_research_results if result.get("unresolved")]
    adapter_attention = [result for result in adapter_research_results if result.get("unresolved")]
    lens_included_with_unresolved = sum(
        result["decision"]["status"] == "included" for result in lens_attention
    )
    adapter_included_with_unresolved = sum(
        result["decision"]["status"] == "included" for result in adapter_attention
    )
    product_type_counts = Counter(record["productType"] for record in records)
    published_announcement_dates = sum(
        record["lifecycle"]["announcementDate"] is not None for record in records
    )
    designation_counts = Counter(
        designation["type"]
        for record in records
        for designation in record["lifecycle"]["officialDesignations"] or []
    )
    data_version = _object(ROOT / "config" / "versions.json")["dataVersion"]
    blob_url = f"https://github.com/KatsuraIwamoto/z-mount-product-database/blob/{data_version}"
    lens_heading = (
        "## Lens and related optical product dataset / レンズと関連光学製品のデータセット"
    )
    adapter_heading = "## Mount adapter dataset / マウントアダプターのデータセット"
    lens_section, adapter_section = markdown.split(lens_heading, maxsplit=1)[1].split(
        adapter_heading, maxsplit=1
    )

    assert markdown.startswith("# Products / 製品一覧\n")
    assert "> [!NOTE]" in markdown
    assert markdown.index("> Generated from") < markdown.index("> レンズと関連光学製品")
    assert "It does not mean the product is currently sold, in stock, or available." in markdown
    assert "現在販売中、在庫あり、入手可能であることを意味しません。" in markdown
    assert markdown.index("> [!NOTE]") < markdown.index("> [!WARNING]")
    assert markdown.index("> [!WARNING]") < markdown.index("**Included:**")
    assert markdown.index("**Included:**") < markdown.index("**収録:**")
    assert markdown.index("**収録:**") < markdown.index("[Report a correction or addition")
    assert (
        '"Source mount" identifies the lens-side mount in the marketed adapter configuration.'
        in adapter_section
    )
    assert (
        "すべてのレンズ、カメラ、ファームウェアの組み合わせで動作することは保証しません。"
        in adapter_section
    )
    assert (
        f"**Included:** Lens and related optical product dataset: {len(records)} products "
        f"across {len(brands)} brands; mount adapter dataset: {len(adapters)} products "
        f"across {len(adapter_brands)} brands.\n"
        "\n"
        f"**収録:** レンズと関連光学製品のデータセット：{len(records)}製品、"
        f"{len(brands)}ブランド。マウントアダプターのデータセット："
        f"{len(adapters)}製品、{len(adapter_brands)}ブランド。"
    ) in markdown
    h2_headings = [line for line in markdown.splitlines() if line.startswith("## ")]
    assert h2_headings == [
        "## Contents / 目次",
        "## Dataset overview / データセット概要",
        lens_heading,
        adapter_heading,
    ]
    for anchor in (
        "statistics",
        "lens-dataset",
        "lens-statistics",
        "lens-needs-attention",
        "lens-products-by-brand",
        "adapter-dataset",
        "adapter-statistics",
        "adapter-needs-attention",
        "adapter-products-by-brand",
    ):
        assert f"](#{anchor})" in markdown
    assert markdown.count("\n### ") == 6
    assert markdown.count("\n#### ") == len(brands) + len(adapter_brands) + 4
    assert markdown.count("\n| [") == len(records) + len(adapters)
    assert markdown.count("| [Research result: lenses/") == len(records)
    assert markdown.count("| [Research result: adapters/") == len(adapters)
    assert "](data/" not in markdown
    assert "](research/" not in markdown
    for product_type in ("lens", "teleconverter", "pinhole"):
        assert (
            f"| `productType: {product_type}` | {product_type_counts[product_type]} |"
            in lens_section
        )
    assert (
        f"| Published `announcementDate` / 発売発表日あり | {published_announcement_dates} |"
        in lens_section
    )
    assert (
        f"| `announcementDate: null` | {len(records) - published_announcement_dates} |" in markdown
    )
    for designation in ("legacy-product", "sales-ended", "production-ended", "discontinued"):
        assert (
            f"| `officialDesignations: {designation}` | {designation_counts[designation]} |"
            in lens_section
        )
    assert f"| Research results / 調査結果データ | {len(lens_research_results)} |" in lens_section
    assert (
        f"| Research results / 調査結果データ | {len(adapter_research_results)} |"
        in adapter_section
    )
    for status in ("included", "excluded", "needs-review"):
        assert f"| `{status}` | {lens_status_counts[status]} |" in lens_section
        assert f"| `{status}` | {adapter_status_counts[status]} |" in adapter_section
    assert f"| Results with `unresolved` / 未解決事項あり | {len(lens_attention)} |" in lens_section
    assert (
        f"| Results with `unresolved` / 未解決事項あり | {len(adapter_attention)} |"
        in adapter_section
    )
    assert lens_section.count("\n| `needs-review` | [") == lens_status_counts["needs-review"]
    assert adapter_section.count("\n| `needs-review` | [") == adapter_status_counts["needs-review"]
    assert lens_section.count("\n| `included` | [") == lens_included_with_unresolved
    assert adapter_section.count("\n| `included` | [") == adapter_included_with_unresolved
    assert markdown.count("> [!WARNING]") == 3
    zeiss_count = sum(record["identity"]["brandId"] == "zeiss" for record in records)
    assert f"\n#### ZEISS ({zeiss_count})\n" in lens_section
    assert "\n#### Carl Zeiss AG " not in lens_section
    assert (
        "| [ZEISS Otus ML 1.4/35]"
        f"({blob_url}/data/records/lenses/zeiss/zeiss-otus-ml-35mm-f1p4.json)"
    ) in markdown
    assert (
        "[Research result: lenses/zeiss-otus-ml-35mm-f1p4 / 調査結果]"
        f"({blob_url}/research/results/lenses/zeiss/zeiss-otus-ml-35mm-f1p4.json)"
    ) in markdown
    assert "16mm F1.4 DC DN \\| Contemporary" in markdown
    assert (
        f"| [Mount Adapter FTZ]({blob_url}/data/records/adapters/nikon/mount-adapter-ftz.json) "
        "| `mount-adapter-ftz` | Nikon F"
    ) in adapter_section
    assert (
        "[Research result: adapters/mount-adapter-ftz / 調査結果]"
        f"({blob_url}/research/results/adapters/nikon/mount-adapter-ftz.json)"
    ) in adapter_section
    for record in records + adapters:
        for page in record["officialProductPages"]:
            region = page["region"] or "global"
            label = f"{page['publisher']['name']} ({region}/{page['language']})"
            assert f"[{label}](<{page['url']}>)" in markdown
    record_without_page = next(record for record in records if not record["officialProductPages"])
    result_without_page = next(
        result for result in lens_research_results if result["id"] == record_without_page["id"]
    )
    assert (
        f"| `{record_without_page['id']}` | {result_without_page['reviewedOn']} | — | "
        f"[Research result: lenses/{record_without_page['id']} / 調査結果]"
    ) in lens_section
    for result in lens_attention + adapter_attention:
        assert f"| {result['reviewedOn']} |" in markdown
        for index, source in enumerate(result["sources"], 1):
            assert f"[{index}](<{source['url']}>)" in markdown
    assert (
        "https://github.com/KatsuraIwamoto/z-mount-product-database/"
        "issues/new?template=data-correction.yml"
    ) in markdown
    english_license = f"This list is available under [CC BY 4.0]({blob_url}/LICENSES/CC-BY-4.0.txt)"
    japanese_license = f"この一覧は [CC BY 4.0]({blob_url}/LICENSES/CC-BY-4.0.txt)"
    assert markdown.index(english_license) < markdown.index(japanese_license)


def test_license_notices_exclude_third_party_rights_and_affiliation() -> None:
    licensing = (ROOT / "LICENSING.md").read_text()

    assert "> [!IMPORTANT]" in licensing
    assert "Patent and trademark rights are not licensed under CC BY 4.0." in licensing
    assert "does not claim copyright in factual product specifications" in licensing
    assert "is not affiliated with, authorized by, sponsored by, or endorsed by" in licensing
    assert "特許権と商標権は許諾されません" in licensing
    assert "提携関係になく、公認、後援、推奨を受けたものでもありません" in licensing

    for path in (ROOT / "README.md", ROOT / "README.ja.md"):
        readme = path.read_text()
        assert "> [!IMPORTANT]" in readme
        assert "LICENSING.md" in readme


def test_full_and_light_contracts() -> None:
    versions = _object(ROOT / "config" / "versions.json")
    full = _object(ROOT / FULL_PATH)
    light = _object(ROOT / LIGHT_PATH)
    full_products = cast("list[Any]", full["products"])
    light_products = cast("list[Any]", light["products"])

    assert set(versions) == {"schemaVersion", "dataVersion"}
    assert full["schemaVersion"] == light["schemaVersion"] == versions["schemaVersion"]
    assert full["dataVersion"] == light["dataVersion"] == versions["dataVersion"]
    assert "releasedOn" not in full and "releasedOn" not in light
    assert "generator" not in full and "generator" not in light
    assert full["license"] == light["license"] == "CC-BY-4.0"
    assert (
        full["licenseUrl"] == light["licenseUrl"] == "https://creativecommons.org/licenses/by/4.0/"
    )
    assert full["referenceData"] == light["referenceData"]
    assert full["contentHash"] == _payload_hash(
        {"referenceData": full["referenceData"], "products": full_products}
    )
    assert light["contentHash"] == _payload_hash(
        {"referenceData": light["referenceData"], "products": light_products}
    )
    assert [item["id"] for item in full_products] == [item["id"] for item in light_products]
    assert all(
        _is_ordered_recursive_subset(light_product, full_product)
        for full_product, light_product in zip(full_products, light_products, strict=True)
    )


def test_adapter_full_contract() -> None:
    versions = _object(ROOT / "config" / "versions.json")
    full = _object(ROOT / ADAPTER_FULL_PATH)
    adapters = cast("list[Any]", full["adapters"])

    assert full["datasetName"] == "Z Mount Adapter Database"
    assert full["datasetVariant"] == "full"
    assert full["schemaVersion"] == versions["schemaVersion"]
    assert full["dataVersion"] == versions["dataVersion"]
    assert full["recordCount"] == len(adapters) == len(adapter_record_paths(ROOT))
    assert full["contentHash"] == _payload_hash(
        {"referenceData": full["referenceData"], "adapters": adapters}
    )
    adapter_ids = [cast("str", adapter["id"]) for adapter in adapters]
    assert adapter_ids == sorted(adapter_ids)
    assert all("$schema" not in adapter for adapter in adapters)


def test_full_datasets_reject_record_schema_markers() -> None:
    for path, collection_name, schema_name in (
        (FULL_PATH, "products", "lenses/dataset-full.schema.json"),
        (ADAPTER_FULL_PATH, "adapters", "adapters/dataset-full.schema.json"),
    ):
        dataset = _object(ROOT / path)
        records = cast("list[dict[str, Any]]", dataset[collection_name])
        records[0]["$schema"] = "https://example.com/unexpected.schema.json"
        assert not _public_validator(schema_name).is_valid(dataset)


def test_light_focus_arrays_follow_the_existing_website_contract() -> None:
    full_products = cast("list[dict[str, Any]]", _object(ROOT / FULL_PATH)["products"])
    light_products = cast("list[dict[str, Any]]", _object(ROOT / LIGHT_PATH)["products"])
    for full, light in zip(full_products, light_products, strict=True):
        if full["productType"] != "lens":
            continue
        full_focus = cast("dict[str, Any]", cast("dict[str, Any]", full["lens"])["focus"])
        light_focus = cast("dict[str, Any]", cast("dict[str, Any]", light["lens"])["focus"])

        distances = cast("list[dict[str, Any]] | None", full_focus["minimumFocusDistances"])
        expected_distances = (
            [
                entry
                for entry in distances
                if entry["distanceM"] == min(x["distanceM"] for x in distances)
            ]
            if distances
            else distances
        )
        assert light_focus["minimumFocusDistances"] == expected_distances

        magnifications = cast(
            "list[dict[str, Any]] | None", full_focus["reproductionMagnifications"]
        )
        expected_magnifications = (
            [
                entry
                for entry in magnifications
                if _magnification_upper_bound(entry)
                == max(_magnification_upper_bound(x) for x in magnifications)
            ]
            if magnifications
            else magnifications
        )
        assert light_focus["reproductionMagnifications"] == expected_magnifications


def test_data_version_date_covers_every_research_review() -> None:
    data_version_date = date.fromisoformat(
        cast("str", _object(ROOT / "config/versions.json")["dataVersion"]).replace(".", "-")
    )
    reviewed_on = [
        date.fromisoformat(cast("str", _object(path)["reviewedOn"]))
        for path in sorted((ROOT / "research" / "results").rglob("*.json"))
    ]
    assert max(reviewed_on) <= data_version_date


def test_every_record_has_one_paired_included_research_result() -> None:
    records = {_object(path)["id"]: path for path in record_paths(ROOT)}
    included: list[str] = []
    for path in sorted((ROOT / "research" / "results" / "lenses").glob("*/*.json")):
        result = _object(path)
        assert "schemaVersion" not in result
        decision = cast("dict[str, Any]", result["decision"])
        if decision["status"] == "included":
            record_id = cast("str", decision["recordId"])
            included.append(record_id)
            assert record_id in records
            assert path.parent.name == records[record_id].parent.name
    assert len(included) == len(set(included))
    assert set(included) == set(records)


def test_decided_research_results_have_sources() -> None:
    for path in sorted((ROOT / "research" / "results").rglob("*.json")):
        result = _object(path)
        decision = cast("dict[str, Any]", result["decision"])
        sources = cast("list[Any]", result["sources"])
        if decision["status"] in {"included", "excluded"}:
            assert sources, path


def test_schema_set_is_small_and_explicit() -> None:
    schema_version = cast("str", _object(ROOT / "config/versions.json")["schemaVersion"])
    actual = {
        path.relative_to(ROOT / "schemas").as_posix()
        for path in (ROOT / "schemas").rglob("*.schema.json")
    }
    assert actual == set(SCHEMA_PATHS)
    for name in SCHEMA_PATHS:
        schema = _object(ROOT / "schemas" / name)
        assert schema["$comment"] == (
            "SPDX-FileCopyrightText: 2026 Katsura Iwamoto\nSPDX-License-Identifier: MIT"
        )
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        Draft202012Validator.check_schema(schema)
        assert "x-schemaVersion" not in schema
        assert all(not urlsplit(ref).scheme for ref in _schema_refs(schema))
    for name in PUBLIC_SCHEMA_PATHS:
        assert _object(ROOT / "schemas" / name)["$id"] == (
            f"https://cercidiphyllum.jp/schemas/{schema_version}/{name}"
        )
    for name in INTERNAL_SCHEMA_PATHS:
        assert "$id" not in _object(ROOT / "schemas" / name)

    registry = _object(ROOT / "data" / "product-manufacturer-brand-registry.json")
    assert "schemaVersion" not in registry
    mount_registry = _object(ROOT / "data" / "mount-system-registry.json")
    assert "schemaVersion" not in mount_registry


def test_schema_reference_validation_finds_unresolvable_targets() -> None:
    schemas, registry = _schema_registry(ROOT)
    broken = {**schemas}
    name = "lenses/product-full.schema.json"
    broken_schema = deepcopy(schemas[name])
    cast("dict[str, Any]", broken_schema["properties"])["broken"] = {"$ref": "missing.schema.json"}
    broken[name] = broken_schema

    schema_version = cast("str", _object(ROOT / "config/versions.json")["schemaVersion"])
    diagnostics = _schema_set_diagnostics(ROOT, broken, registry, schema_version)
    assert any("unresolvable $ref 'missing.schema.json'" in item.message for item in diagnostics)


def test_probe_details_are_optional_without_removing_their_definitions() -> None:
    lens_schema = _object(ROOT / "schemas" / "lenses" / "product-type-lens.schema.json")
    specialized = cast(
        "dict[str, Any]", cast("dict[str, Any]", lens_schema["$defs"])["specialized"]
    )
    probe = cast("dict[str, Any]", cast("dict[str, Any]", specialized["properties"])["probe"])
    validator = Draft202012Validator(probe)
    assert validator.is_valid({})
    assert validator.is_valid({"viewConfigurations": None, "integratedLights": None})


def test_optional_mount_adapter_must_be_product_dedicated() -> None:
    resources: list[tuple[str, Resource[Any]]] = []
    schemas: dict[str, dict[str, Any]] = {}
    for name in PUBLIC_SCHEMA_PATHS:
        schema = _object(ROOT / "schemas" / name)
        schemas[name] = schema
        resources.append((cast("str", schema["$id"]), Resource.from_contents(schema)))
    components = schemas["lenses/product-components.schema.json"]
    validator = Draft202012Validator(
        {"$ref": f"{components['$id']}#/$defs/officialMountAdapter"},
        registry=Registry[Any]().with_resources(resources),
    )
    supplied = {
        "relationship": "supplied",
        "dedicatedToProduct": None,
        "nativeMountSystemId": "leica-m39",
        "name": "Lens mount adapter",
        "modelNumberOptions": None,
    }
    assert validator.is_valid(supplied)
    assert validator.is_valid({**supplied, "relationship": "optional", "dedicatedToProduct": True})
    assert not validator.is_valid(
        {**supplied, "relationship": "optional", "dedicatedToProduct": False}
    )


def test_adapter_schema_is_independent_and_rejects_contradictions() -> None:
    resources: list[tuple[str, Resource[Any]]] = []
    schemas: dict[str, dict[str, Any]] = {}
    for name in PUBLIC_SCHEMA_PATHS:
        schema = _object(ROOT / "schemas" / name)
        schemas[name] = schema
        resources.append((cast("str", schema["$id"]), Resource.from_contents(schema)))
    validator = Draft202012Validator(
        schemas["adapters/adapter-record.schema.json"],
        registry=Registry[Any]().with_resources(resources),
        format_checker=FormatChecker(),
    )
    adapter: dict[str, Any] = {
        "$schema": "../../../../schemas/adapters/adapter-record.schema.json",
        "id": "example-adapter",
        "identity": {
            "manufacturerId": "example-manufacturer",
            "brandId": "example-brand",
            "productName": "Example Adapter",
            "modelNumberOptions": None,
            "alternateNames": [],
            "variants": None,
        },
        "lifecycle": {"announcementDate": None, "officialDesignations": []},
        "officialProductPages": [],
        "mountConfigurations": [
            {
                "lensSideMountSystemId": "example-mount",
                "cameraSideMountSystemId": "nikon-z",
                "lensRetention": None,
                "lensRearProtrusionLimits": None,
            }
        ],
        "electronics": None,
        "electronicServices": None,
        "conversionOptics": {"present": False},
        "mechanisms": [],
        "physical": {
            "dimensionMeasurements": None,
            "weightMeasurements": None,
            "officialEnvironmentalProtectionClaims": None,
            "tripodSupport": None,
        },
    }
    assert validator.is_valid(adapter)
    assert "productType" not in adapter

    adapter["mountConfigurations"][0]["lensSideMountSystemId"] = "nikon-z"
    assert not validator.is_valid(adapter)
    adapter["mountConfigurations"][0]["lensSideMountSystemId"] = "example-mount"

    adapter["electronics"] = {
        "electronicContacts": False,
        "autofocus": False,
        "cameraControlledAperture": False,
        "metadataTransmission": {"present": False},
        "lensStabilizationCommunication": False,
        "manualFocusAssistance": False,
        "lensPowerTransmission": False,
        "recordingTriggerTransmission": False,
    }
    assert validator.is_valid(adapter)
    for field in (
        "autofocus",
        "cameraControlledAperture",
        "lensStabilizationCommunication",
        "manualFocusAssistance",
        "lensPowerTransmission",
        "recordingTriggerTransmission",
    ):
        adapter["electronics"][field] = True
        assert not validator.is_valid(adapter)
        adapter["electronics"][field] = False

    adapter["electronics"]["metadataTransmission"] = {"present": True, "standards": None}
    assert not validator.is_valid(adapter)
    adapter["electronics"]["metadataTransmission"] = {"present": False}

    adapter["electronicServices"] = {
        "hasPublishedFirmwareUpdate": True,
        "connections": [{"method": "camera-body", "purposes": ["firmware-update"]}],
    }
    assert not validator.is_valid(adapter)
    adapter["electronics"]["electronicContacts"] = True
    assert validator.is_valid(adapter)
    adapter["electronicServices"] = None
    adapter["electronics"]["electronicContacts"] = False

    adapter["conversionOptics"] = {
        "present": True,
        "focalLengthMultiplier": 1.4,
        "apertureChange": {
            "direction": "darker",
            "stops": 1,
            "relation": "less-than",
        },
        "opticalConstruction": {"groups": 4, "elements": 6},
        "specialElements": [{"types": ["aspherical"], "quantity": None}],
        "coatings": None,
        "supportedImageCircleDiameterMm": {
            "kind": "range",
            "minimumDiameterMm": 31,
            "maximumDiameterMm": 43.27,
        },
        "maximumSupportedAperture": {"scale": "t-number", "value": 2.8},
    }
    assert validator.is_valid(adapter)
    adapter["conversionOptics"]["apertureChange"]["direction"] = "unchanged"
    assert not validator.is_valid(adapter)
    adapter["conversionOptics"]["apertureChange"]["direction"] = "darker"

    adapter["mechanisms"] = [{"type": "shift", "conditions": {}}]
    assert not validator.is_valid(adapter)
    adapter["mechanisms"][0]["movements"] = None
    assert validator.is_valid(adapter)
    adapter["mechanisms"][0]["movements"] = {"shiftMeasurements": None}
    assert not validator.is_valid(adapter)
    adapter["mechanisms"] = [
        {
            "type": "shift",
            "conditions": {},
            "movements": {
                "shiftMeasurements": [
                    {
                        "maximumFromNeutralMm": 10,
                        "totalRangeMm": None,
                        "directionality": None,
                        "conditions": {},
                    }
                ]
            },
        },
        {
            "type": "rotation",
            "conditions": {},
            "movements": {
                "rotationMeasurements": [
                    {
                        "scope": "movement-assembly",
                        "maximumFromNeutralDegrees": None,
                        "totalRangeDegrees": 360,
                        "directionality": None,
                        "conditions": {},
                    }
                ]
            },
        },
    ]
    assert validator.is_valid(adapter)
    shift = adapter["mechanisms"][0]["movements"]["shiftMeasurements"][0]
    shift["maximumFromNeutralMm"] = 0
    assert not validator.is_valid(adapter)
    shift["maximumFromNeutralMm"] = 10
    rotation = adapter["mechanisms"][1]["movements"]["rotationMeasurements"][0]
    rotation["totalRangeDegrees"] = 361
    assert not validator.is_valid(adapter)
    rotation["totalRangeDegrees"] = 360

    adapter["mechanisms"][0]["movements"]["tiltMeasurements"] = [
        {
            "maximumFromNeutralDegrees": 10,
            "totalRangeDegrees": None,
            "directionality": None,
            "conditions": {},
        }
    ]
    assert not validator.is_valid(adapter)
    del adapter["mechanisms"][0]["movements"]["tiltMeasurements"]

    adapter["mechanisms"] = [
        {
            "type": "drop-in-filter",
            "conditions": {},
            "movements": None,
        }
    ]
    assert not validator.is_valid(adapter)
    del adapter["mechanisms"][0]["movements"]
    assert validator.is_valid(adapter)

    adapter["physical"]["tripodSupport"] = {
        "present": True,
        "components": [
            {
                "type": "body-mounting-point",
                "relationship": "integrated",
                "removable": False,
                "interfaces": [{"type": "mounting-thread"}],
                "modelNumberOptions": None,
                "quantity": 1,
                "conditions": {},
            }
        ],
    }
    assert not validator.is_valid(adapter)
    interface = adapter["physical"]["tripodSupport"]["components"][0]["interfaces"][0]
    interface["threadDesignation"] = None
    assert validator.is_valid(adapter)


def test_lens_zoom_and_physical_behavior_are_structurally_coupled() -> None:
    resources: list[tuple[str, Resource[Any]]] = []
    schemas: dict[str, dict[str, Any]] = {}
    for name in PUBLIC_SCHEMA_PATHS:
        schema = _object(ROOT / "schemas" / name)
        schemas[name] = schema
        resources.append((cast("str", schema["$id"]), Resource.from_contents(schema)))
    validator = Draft202012Validator(
        schemas["lenses/product-record.schema.json"],
        registry=Registry[Any]().with_resources(resources),
        format_checker=FormatChecker(),
    )

    zoom = _object(ROOT / "data/records/lenses/nikkor/nikkor-z-24-to-50mm-f4-to-6p3.json")
    assert validator.is_valid(zoom)
    zoom_block = cast("dict[str, Any]", cast("dict[str, Any]", zoom["lens"])["zoom"])
    del cast("dict[str, Any]", zoom["lens"])["zoom"]
    assert not validator.is_valid(zoom)
    cast("dict[str, Any]", zoom["lens"])["zoom"] = zoom_block

    zoom_physical = cast("dict[str, Any]", zoom["physical"])
    for field in (
        "isRetractableForStorage",
        "externalLengthDuringFocus",
        "externalLengthDuringZoom",
    ):
        value = zoom_physical.pop(field)
        assert not validator.is_valid(zoom)
        zoom_physical[field] = value

    prime = _object(ROOT / "data/records/lenses/nikkor/nikkor-z-35mm-f1p8-s.json")
    assert validator.is_valid(prime)
    electronic_services = prime.pop("electronicServices")
    assert not validator.is_valid(prime)
    prime["electronicServices"] = electronic_services
    cast("dict[str, Any]", prime["lens"])["zoom"] = {
        "drive": None,
        "opticalZoomingSystems": None,
    }
    assert not validator.is_valid(prime)
    del cast("dict[str, Any]", prime["lens"])["zoom"]
    cast("dict[str, Any]", prime["physical"])["externalLengthDuringZoom"] = None
    assert not validator.is_valid(prime)

    prime_physical = cast("dict[str, Any]", prime["physical"])
    prime_physical.pop("externalLengthDuringZoom")
    prime_physical["externalLengthDuringFocus"] = "variable"
    assert not validator.is_valid(prime)
    prime_physical["externalLengthDuringFocus"] = "constant"
    cast("dict[str, Any]", cast("dict[str, Any]", prime["mount"])["electronicContacts"])[
        "present"
    ] = False
    cast("dict[str, Any]", prime["mount"])["electronicContacts"].pop("metadataTransmission")
    assert not validator.is_valid(prime)

    zoom_block["opticalZoomingSystems"] = [{"type": "internal-zooming"}]
    assert not validator.is_valid(zoom)
    zoom_physical["externalLengthDuringZoom"] = "constant"
    assert validator.is_valid(zoom)

    manual = _object(
        ROOT / "data/records/lenses/artra-lab/artralab-nonikkor-mc-35mm-f1p4-1960s.json"
    )
    assert validator.is_valid(manual)
    manual["electronicServices"] = {
        "hasPublishedFirmwareUpdate": None,
        "connections": [
            {
                "method": "direct-usb",
                "connectorType": "usb-c",
                "purposes": ["configuration"],
            }
        ],
    }
    assert validator.is_valid(manual)


def test_optical_construction_groups_must_not_exceed_elements(tmp_path: Path) -> None:
    path = tmp_path / "data/records/lenses/example/example.json"
    record: dict[str, Any] = {
        "id": "example",
        "lens": {"opticalConstruction": {"groups": 7, "elements": 6}},
    }
    assert _record_semantics(tmp_path, path, record, set()) == [
        Diagnostic(
            "data/records/lenses/example/example.json/lens/opticalConstruction",
            "groups must not exceed elements",
        )
    ]


def test_research_checked_coverage_tracks_canonical_field_groups() -> None:
    record: dict[str, Any] = {
        "identity": {"productName": "Example"},
        "officialProductPages": [
            {
                "url": "https://example.com/product",
            }
        ],
        "electronics": {
            "electronicContacts": False,
            "autofocus": False,
        },
        "conversionOptics": {"present": False},
    }
    diagnostics = _research_coverage_diagnostics(
        "research/results/adapters/example.json",
        record,
        [
            {
                "url": "https://example.com/other-page",
                "publisherRelationship": "manufacturer-or-brand",
                "checked": ["identity", "officialProductPages", "conversionOptics"],
            }
        ],
        ("identity", "officialProductPages", "electronics", "conversionOptics"),
    )
    assert diagnostics == [
        Diagnostic(
            "research/results/adapters/example.json/sources",
            "official product page 'https://example.com/product' has no matching checked source",
        ),
        Diagnostic(
            "research/results/adapters/example.json/sources",
            "canonical field group 'electronics' has no checked source coverage",
        ),
    ]
    assert (
        _research_coverage_diagnostics(
            "research/results/adapters/example.json",
            record,
            [
                {
                    "url": "https://example.com/product",
                    "publisherRelationship": "manufacturer-or-brand",
                    "checked": ["identity", "officialProductPages"],
                }
            ],
            ("identity", "officialProductPages"),
        )
        == []
    )
    assert (
        _research_coverage_diagnostics(
            "research/results/adapters/example.json",
            record,
            None,
            ("identity",),
        )[0].message
        == "canonical field group 'identity' has no checked source coverage"
    )

    specialized_record: dict[str, Any] = {"lens": {"specialized": {"cinema": {}}}}
    assert _research_coverage_diagnostics(
        "research/results/lenses/example.json",
        specialized_record,
        [{"publisherRelationship": "manufacturer-or-brand", "checked": []}],
        ("lens.specialized",),
    ) == [
        Diagnostic(
            "research/results/lenses/example.json/sources",
            "canonical field group 'lens.specialized' has no checked source coverage",
        )
    ]


def test_research_checked_coverage_uses_exact_paths_and_value_states() -> None:
    record: dict[str, Any] = {
        "physical": {
            "weightMeasurements": [],
            "officialEnvironmentalProtectionClaims": None,
        },
        "mount": {"electronicContacts": {"present": False}},
    }

    assert _research_coverage_diagnostics(
        "research/results/lenses/example.json",
        record,
        [
            {
                "publisherRelationship": "manufacturer-or-brand",
                "checked": ["physical", "mount"],
            }
        ],
        (
            "physical.weightMeasurements",
            "physical.officialEnvironmentalProtectionClaims",
            "mount.electronicContacts",
        ),
    ) == [
        Diagnostic(
            "research/results/lenses/example.json/sources",
            "canonical field group 'physical.weightMeasurements' has no checked source coverage",
        ),
        Diagnostic(
            "research/results/lenses/example.json/sources",
            "canonical field group 'mount.electronicContacts' has no checked source coverage",
        ),
    ]


def test_research_checked_coverage_respects_source_relationships() -> None:
    record: dict[str, Any] = {
        "identity": {
            "productName": "Example",
            "modelNumberOptions": ["EXAMPLE-1"],
        },
        "mountConfigurations": [
            {
                "lensSideMountSystemId": "example",
                "cameraSideMountSystemId": "nikon-z",
            }
        ],
        "electronics": {"electronicContacts": False},
        "physical": {"weightMeasurements": []},
    }
    coverage_paths = (
        "identity",
        "identity.modelNumberOptions",
        "mountConfigurations",
        "electronics",
        "physical.weightMeasurements",
    )

    assert _research_coverage_diagnostics(
        "research/results/adapters/example.json",
        record,
        [
            {
                "publisherRelationship": "authorized-retailer",
                "checked": list(coverage_paths),
            }
        ],
        coverage_paths,
    ) == [
        Diagnostic(
            "research/results/adapters/example.json/sources",
            "canonical field group 'identity' has no checked source coverage",
        ),
        Diagnostic(
            "research/results/adapters/example.json/sources",
            "canonical field group 'electronics' has no checked source coverage",
        ),
        Diagnostic(
            "research/results/adapters/example.json/sources",
            "canonical field group 'physical.weightMeasurements' has no checked source coverage",
        ),
    ]

    assert validation_module._accepted_checked_paths(
        {
            "publisherRelationship": "authorized-retailer",
            "sourceType": "image",
            "checked": [
                "identity",
                "electronics",
                "mechanisms",
                "physical.tripodSupport",
                "physical.weightMeasurements",
            ],
        }
    ) == {"identity", "electronics", "mechanisms", "physical.tripodSupport"}
    assert (
        validation_module._accepted_checked_paths(
            {
                "publisherRelationship": "retailer",
                "sourceType": "image",
                "checked": ["electronics"],
            }
        )
        == set()
    )

    assert len(
        _research_coverage_diagnostics(
            "research/results/adapters/example.json",
            record,
            [
                {
                    "publisherRelationship": "retailer",
                    "checked": list(coverage_paths),
                }
            ],
            coverage_paths,
        )
    ) == len(coverage_paths)


def test_lifecycle_dates_must_not_postdate_the_paired_research_review(tmp_path: Path) -> None:
    path = tmp_path / "data/records/lenses/example/example.json"
    record: dict[str, Any] = {
        "lifecycle": {
            "announcementDate": "2026-09-03",
            "officialDesignations": [
                {"observedOn": "2026-09-01"},
                {"observedOn": "2026-09-04"},
            ],
        }
    }

    assert _lifecycle_review_diagnostics(tmp_path, path, record, date(2026, 9, 2)) == [
        Diagnostic(
            "data/records/lenses/example/example.json/lifecycle/announcementDate",
            "must not be later than paired research reviewedOn",
        ),
        Diagnostic(
            "data/records/lenses/example/example.json/lifecycle/officialDesignations/1/observedOn",
            "must not be later than paired research reviewedOn",
        ),
    ]


def test_source_registries_reject_entries_unused_by_records_or_research(tmp_path: Path) -> None:
    research_path = tmp_path / "research/results/lenses/research-brand/candidate.json"
    research_path.parent.mkdir(parents=True)
    research_path.write_text(
        json.dumps(
            {
                "subject": {
                    "manufacturerId": "research-manufacturer",
                    "brandId": "research-brand",
                }
            }
        )
    )
    lens_records = {
        "example": (
            tmp_path / "data/records/lenses/record-brand/example.json",
            {
                "identity": {
                    "manufacturerId": "record-manufacturer",
                    "brandId": "record-brand",
                    "alternateNames": [{"brandId": "alternate-brand"}],
                },
                "mount": {
                    "systemId": "nikon-z",
                    "adapter": {"nativeMountSystemId": "t-mount"},
                },
            },
        )
    }
    adapter_records = {
        "adapter": (
            tmp_path / "data/records/adapters/record-brand/adapter.json",
            {
                "mountConfigurations": [
                    {
                        "lensSideMountSystemId": "leica-m",
                        "cameraSideMountSystemId": "nikon-z",
                    }
                ]
            },
        )
    }

    assert _registry_usage_diagnostics(
        tmp_path,
        lens_records,
        adapter_records,
        {
            "record-manufacturer": "Record Manufacturer",
            "research-manufacturer": "Research Manufacturer",
            "unused-manufacturer": "Unused Manufacturer",
        },
        {
            "record-brand": "Record Brand",
            "alternate-brand": "Alternate Brand",
            "research-brand": "Research Brand",
            "unused-brand": "Unused Brand",
        },
        {
            "nikon-z": "Nikon Z",
            "t-mount": "T-mount",
            "leica-m": "Leica M",
            "unused-mount": "Unused Mount",
        },
    ) == [
        Diagnostic(
            "data/product-manufacturer-brand-registry.json/manufacturers",
            "unused manufacturer ID 'unused-manufacturer'",
        ),
        Diagnostic(
            "data/product-manufacturer-brand-registry.json/brands",
            "unused brand ID 'unused-brand'",
        ),
        Diagnostic(
            "data/mount-system-registry.json/mountSystems",
            "unused mount-system ID 'unused-mount'",
        ),
    ]


def test_research_coverage_paths_follow_checked_schema_paths() -> None:
    lens_schema = _object(ROOT / "schemas/lenses/research-result.schema.json")
    adapter_schema = _object(ROOT / "schemas/adapters/research-result.schema.json")
    lens_paths = set(lens_schema["$defs"]["productFieldPath"]["enum"])
    adapter_paths = set(adapter_schema["$defs"]["productFieldPath"]["enum"])

    assert set(LENS_RESEARCH_COVERAGE_PATHS) == lens_paths - {"physical"}
    assert set(ADAPTER_RESEARCH_COVERAGE_PATHS) == adapter_paths


def test_documentation_has_matching_japanese_and_english_pages() -> None:
    japanese = {
        path.relative_to(ROOT / "docs" / "ja") for path in (ROOT / "docs" / "ja").rglob("*.md")
    }
    english = {
        path.relative_to(ROOT / "docs" / "en") for path in (ROOT / "docs" / "en").rglob("*.md")
    }
    assert japanese == english
    assert {
        Path("reference/schemas") / name.replace(".schema.json", ".md")
        for name in PUBLIC_SCHEMA_PATHS
    } <= japanese


def test_japanese_entry_documents_link_to_japanese_site() -> None:
    site_root = "https://katsuraiwamoto.github.io/z-mount-product-database/"
    japanese_site_root = f"{site_root}ja/"

    for path in (ROOT / "README.ja.md", ROOT / "CONTRIBUTING.ja.md"):
        document = path.read_text()
        assert site_root in document
        assert document.count(site_root) == document.count(japanese_site_root)


def test_distribution_metadata_examples_are_current() -> None:
    distributions = {
        ("products", "full"): _object(ROOT / FULL_PATH),
        ("products", "light"): _object(ROOT / LIGHT_PATH),
        ("adapters", "full"): _object(ROOT / ADAPTER_FULL_PATH),
    }
    metadata_fields = (
        "$schema",
        "datasetName",
        "datasetVariant",
        "schemaVersion",
        "dataVersion",
        "creator",
        "license",
        "licenseUrl",
        "repositoryUrl",
        "recordCount",
        "contentHash",
    )
    expected_metadata = {
        key: {field: distribution[field] for field in metadata_fields}
        for key, distribution in distributions.items()
    }
    expected_model_metadata = {
        key: {
            field: distribution[field] for field in ("dataVersion", "datasetVariant", "recordCount")
        }
        for key, distribution in distributions.items()
        if key != ("products", "light")
    }

    for language in ("ja", "en"):
        use_data = _json_object_code_blocks((ROOT / "docs" / language / "use-data.md").read_text())
        documented_metadata = {
            (
                "adapters" if block["datasetName"] == "Z Mount Adapter Database" else "products",
                block["datasetVariant"],
            ): block
            for block in use_data
            if all(field in block for field in metadata_fields)
        }
        assert documented_metadata == expected_metadata

        data_model = _json_object_code_blocks(
            (ROOT / "docs" / language / "data-model.md").read_text()
        )
        documented_model_metadata = {
            (array_name, block["datasetVariant"]): {
                field: block[field] for field in ("dataVersion", "datasetVariant", "recordCount")
            }
            for block in data_model
            for array_name in ("products", "adapters")
            if array_name in block and "dataVersion" in block
        }
        assert documented_model_metadata == expected_model_metadata


def test_schema_fields_are_documented_in_both_languages() -> None:
    for name in PUBLIC_SCHEMA_PATHS:
        schema = _object(ROOT / "schemas" / name)
        reference_name = name.replace(".schema.json", ".md")
        japanese = (ROOT / "docs" / "ja" / "reference" / "schemas" / reference_name).read_text()
        english = (ROOT / "docs" / "en" / "reference" / "schemas" / reference_name).read_text()
        for field in _schema_property_names(schema):
            assert field in japanese, f"{name}: {field} is missing from Japanese reference"
            assert field in english, f"{name}: {field} is missing from English reference"
