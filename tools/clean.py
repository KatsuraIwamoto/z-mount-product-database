"""Remove repository-generated files and local tool caches."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = (
    "site",
    "build",
    "dist",
    "PRODUCTS.md",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
)


def _inside(root: Path, path: Path) -> bool:
    return path == root or root in path.parents


def clean(root: Path = ROOT) -> list[Path]:
    """Delete known disposable paths below *root* and return what was removed."""
    root = root.resolve()
    removed: list[Path] = []

    targets = [root / name for name in PATHS]
    targets.extend(path for path in root.rglob("__pycache__") if path.is_dir())
    targets.extend(path for suffix in ("*.pyc", "*.pyo") for path in root.rglob(suffix))

    for target in sorted(set(targets), key=lambda path: len(path.parts), reverse=True):
        resolved = target.resolve()
        if not _inside(root, resolved):
            raise RuntimeError(f"Refusing to remove a path outside the repository: {target}")
        if target.is_dir():
            shutil.rmtree(target)
            removed.append(target)
        elif target.exists():
            target.unlink()
            removed.append(target)

    return removed


def main() -> None:
    removed = clean()
    if removed:
        print(f"Removed {len(removed)} disposable path(s).")
    else:
        print("Nothing to clean.")


if __name__ == "__main__":
    main()
