"""Checks for the local canonical-record review tool."""

from __future__ import annotations

import subprocess
from collections import Counter
from importlib.resources import files
from pathlib import Path
from typing import Any, cast
from unittest.mock import MagicMock, patch

from z_mount_product_database.repository import (
    JsonObject,
    adapter_record_paths,
    load_json,
    record_paths,
)
from z_mount_product_database.review import build_catalog, main, open_in_vscode

ROOT = Path(__file__).resolve().parents[1]
AURORA_ID = "sirui-aurora-85mm-f1-4-full-frame-autofocus-lens"


def test_review_catalog_contains_every_research_result_and_optional_record() -> None:
    catalog = build_catalog(ROOT)
    products = cast("list[JsonObject]", catalog["products"])
    lens_research_paths = sorted((ROOT / "research/results/lenses").glob("*/*.json"))
    adapter_research_paths = sorted((ROOT / "research/results/adapters").glob("*/*.json"))
    assert len(products) == len(lens_research_paths) + len(adapter_research_paths)
    assert catalog["validation"] == []
    for dataset, record_count in (
        ("lenses", len(record_paths(ROOT))),
        ("adapters", len(adapter_record_paths(ROOT))),
    ):
        dataset_products = [product for product in products if product["dataset"] == dataset]
        statuses = Counter(cast("str", product["status"]) for product in dataset_products)
        assert statuses["included"] == record_count
        assert statuses["needs-review"] > 0
        assert statuses["excluded"] > 0

    product = next(item for item in products if item["id"] == AURORA_ID)
    record_path = ROOT / cast("str", product["recordPath"])
    research_path = ROOT / cast("str", product["researchPath"])
    assert product["dataset"] == "lenses"
    assert product["status"] == "included"
    assert product["record"] == load_json(record_path)
    assert product["research"] == load_json(research_path)
    sources = cast("list[JsonObject]", product["sources"])
    assert [source["url"] for source in sources] == [
        "https://store.sirui.com/products/sirui-aurora-series-85mm-full-frame-autofocus-lens",
        "https://store.sirui.com/collections/z-mount-nikon-1",
    ]
    assert sources[0]["kind"] == "officialProductPage"
    assert sources[0]["description"] == (
        "manufacturer-or-brand · product-page · fields: productType, identity, lifecycle, "
        "officialProductPages, mount, mount.electronicContacts, physical, "
        "physical.filterInterfaces, physical.tripodSupport, controls, accessories, "
        "lens.focalLength, lens.aperture, lens.anglesOfView, lens.coverage, "
        "lens.opticalConstruction, lens.focus, lens.stabilization"
    )
    assert sources[1]["kind"] == "researchSource"

    excluded = next(item for item in products if item["id"] == "7artisans-50mm-f1-4-tilt-shift")
    assert excluded["status"] == "excluded"
    assert excluded["record"] is None
    assert excluded["recordPath"] is None
    decision = cast("JsonObject", cast("JsonObject", excluded["research"])["decision"])
    assert decision["status"] == "excluded"
    assert isinstance(decision["reason"], str)
    assert len(cast("list[JsonObject]", excluded["sources"])) == 1

    needs_review = next(item for item in products if item["id"] == "caye-135mm-f2-5-iii")
    assert needs_review["status"] == "needs-review"
    assert needs_review["sources"] == []

    adapter = next(
        item
        for item in products
        if item["dataset"] == "adapters" and item["id"] == "mount-adapter-ftz"
    )
    assert adapter["status"] == "included"
    assert adapter["recordPath"] == "data/records/adapters/nikon/mount-adapter-ftz.json"
    assert adapter["researchPath"] == "research/results/adapters/nikon/mount-adapter-ftz.json"
    assert adapter["record"] == load_json(ROOT / cast("str", adapter["recordPath"]))
    assert adapter["research"] == load_json(ROOT / cast("str", adapter["researchPath"]))
    adapter_sources = cast("list[JsonObject]", adapter["sources"])
    assert adapter_sources[0]["description"] == (
        "manufacturer-or-brand · product-page · fields: identity, identity.alternateNames, "
        "officialProductPages, mountConfigurations, electronics, electronicServices, "
        "mechanisms, physical.dimensionMeasurements, physical.weightMeasurements, "
        "physical.officialEnvironmentalProtectionClaims"
    )


def test_review_html_has_the_primary_controls() -> None:
    html = files("z_mount_product_database").joinpath("review.html").read_text(encoding="utf-8")
    for expected in (
        "Z Product Compare",
        '<html lang="en" data-theme="system">',
        'data-theme="system"',
        'id="datasetSelect"',
        'id="themeSelect"',
        'id="languageSelect"',
        'id="scopeSelect"',
        'id="decisionStatus"',
        'id="decisionSummary"',
        'id="reviewedOn"',
        'id="previousSource"',
        'id="sourcePosition"',
        'id="sourceUrl"',
        'id="copyProductName"',
        'id="openVSCode"',
        'id="dataKindSelect"',
        'id="toggleEmpty"',
        'id="recordTable"',
        'id="jsonView"',
        'type: "zproduct:navigate"',
        'localStorage.setItem("zproduct-review-theme"',
        'language: localStorage.getItem("zproduct-review-language") || "en"',
        "kind: state.dataKind",
        "dataset: state.product.dataset",
        'dataset: ["lenses", "adapters"].includes(savedDataset) ? savedDataset : "lenses"',
        'scope: "included"',
        "light-dark(",
        "--canvas: light-dark(#ffffff, #202124)",
    ):
        assert expected in html
    assert 'id="productSearch"' not in html
    assert 'id="sourceFrame"' not in html
    assert 'class="divider"' not in html
    assert "<iframe" not in html

    empty_value_function = html.split("const isEmptyValue", 1)[1].split("const flatten", 1)[0]
    assert "value === false" not in empty_value_function
    assert html.index('type: "zproduct:loaded"') > html.index(
        "state.catalog = await response.json()"
    )


def test_browser_extension_uses_the_native_side_panel_without_extra_permissions() -> None:
    extension = ROOT / "tools/z-product-compare-extension"
    manifest = cast("JsonObject", load_json(extension / "manifest.json"))
    assert manifest["manifest_version"] == 3
    assert manifest["name"] == "Z Product Compare"
    assert manifest["version"] == "1.0.0"
    assert manifest["permissions"] == ["sidePanel"]
    assert manifest["side_panel"] == {"default_path": "sidepanel.html"}

    for name in ("service-worker.js", "sidepanel.css", "sidepanel.html", "sidepanel.js"):
        assert (extension / name).is_file()

    sidepanel = (extension / "sidepanel.html").read_text(encoding="utf-8")
    script = (extension / "sidepanel.js").read_text(encoding="utf-8")
    assert "hatch run review" in sidepanel
    assert "Z Product Compare" in sidepanel
    assert "--no-open" not in sidepanel
    assert '<html lang="en">' in sidepanel
    assert "local server" in sidepanel
    assert '<meta name="color-scheme" content="light dark">' in sidepanel
    assert "background: light-dark(#ffffff, #202124)" in (extension / "sidepanel.css").read_text(
        encoding="utf-8"
    )
    assert 'allow="clipboard-write"' in sidepanel
    assert "chrome.tabs.update" in script
    assert "event.origin !== REVIEW_ORIGIN" in script
    assert "ローカルサーバーに接続できませんでした" in script
    assert 'new Error("unsupportedUrl")' in script
    assert 'new Error("activeTabNotFound")' in script


def test_review_opens_the_standalone_ui_only_when_requested() -> None:
    server = MagicMock(server_port=8765)
    patches = (
        patch("z_mount_product_database.review.find_repository_root", return_value=ROOT),
        patch("z_mount_product_database.review.build_catalog", return_value={"products": []}),
        patch("z_mount_product_database.review.ReviewHTTPServer", return_value=server),
        patch("z_mount_product_database.review.webbrowser.open"),
    )

    with (
        patches[0],
        patches[1],
        patches[2],
        patches[3] as open_browser,
        patch("sys.argv", ["zproduct-review"]),
    ):
        main()
    open_browser.assert_not_called()

    server.reset_mock()
    with (
        patches[0],
        patches[1],
        patches[2],
        patches[3] as open_browser,
        patch("sys.argv", ["zproduct-review", "--open"]),
    ):
        main()
    open_browser.assert_called_once_with("http://127.0.0.1:8765/")


def test_open_in_vscode_reuses_the_active_window_and_targets_a_line() -> None:
    record = (
        ROOT / "data/records/lenses/sirui/sirui-aurora-85mm-f1-4-full-frame-autofocus-lens.json"
    )
    completed = subprocess.CompletedProcess[Any]([], 0)
    with (
        patch("z_mount_product_database.review.shutil.which", return_value="/usr/local/bin/code"),
        patch("z_mount_product_database.review.subprocess.run", return_value=completed) as run,
    ):
        open_in_vscode(ROOT, record, 8)

    assert run.call_args.args[0] == [
        "/usr/local/bin/code",
        "--reuse-window",
        "--goto",
        f"{record}:8:1",
    ]
    assert run.call_args.kwargs["cwd"] == ROOT
