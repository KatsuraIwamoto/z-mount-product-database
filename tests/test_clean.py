"""Safety checks for the explicit clean command."""

from __future__ import annotations

from pathlib import Path

from tools.clean import clean


def test_clean_removes_only_disposable_paths(tmp_path: Path) -> None:
    disposable = [
        tmp_path / "site/index.html",
        tmp_path / "build/package.whl",
        tmp_path / "dist/z-mount-lenses.full.json",
        tmp_path / "dist/z-mount-lenses.light.json",
        tmp_path / "dist/z-mount-adapters.full.json",
        tmp_path / "PRODUCTS.md",
        tmp_path / ".pytest_cache/state",
        tmp_path / "src/package/__pycache__/module.pyc",
    ]
    preserved = [
        tmp_path / "data/records/lenses/example/example.json",
        tmp_path / "data/records/adapters/example/example.json",
        tmp_path / "research/results/lenses/example/example.json",
        tmp_path / "research/results/adapters/example/example.json",
        tmp_path / "schemas/lenses/example.schema.json",
        tmp_path / "schemas/adapters/example.schema.json",
        tmp_path / "schemas/shared/example.schema.json",
    ]
    for path in (*disposable, *preserved):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("test", encoding="utf-8")

    clean(tmp_path)

    assert all(not path.exists() for path in disposable)
    assert all(path.exists() for path in preserved)
