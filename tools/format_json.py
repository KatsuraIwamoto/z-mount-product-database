"""Format repository-owned source JSON files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from z_mount_product_database.generation import GenerationError, _json_bytes, _write_transaction
from z_mount_product_database.repository import RepositoryError, load_json

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORIES = ("config", "data", "research", "schemas", "tools")


def source_json_paths(root: Path) -> list[Path]:
    """Return source JSON paths while excluding generated distributions."""
    root = root.resolve()
    return sorted(
        path
        for directory in SOURCE_DIRECTORIES
        for path in (root / directory).rglob("*.json")
        if path.is_file() and not path.is_symlink()
    )


def format_repository_json(root: Path, *, check: bool = False) -> list[Path]:
    """Format source JSON and return relative paths that differed."""
    root = root.resolve()
    changes: dict[Path, bytes] = {}
    for path in source_json_paths(root):
        formatted = _json_bytes(load_json(path))
        if path.read_bytes() != formatted:
            changes[path.relative_to(root)] = formatted
    if changes and not check:
        _write_transaction(root, changes)
    return list(changes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report differences without writing")
    arguments = parser.parse_args()
    try:
        changed = format_repository_json(ROOT, check=arguments.check)
    except (GenerationError, RepositoryError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from None

    if not changed:
        print("JSON formatting is current.")
        return

    output = sys.stderr if arguments.check else sys.stdout
    action = "would reformat" if arguments.check else "formatted"
    for path in changed:
        print(f"{action}: {path}", file=output)
    if arguments.check:
        print(f"{len(changed)} JSON file(s) require formatting.", file=sys.stderr)
        raise SystemExit(1)
    print(f"Formatted {len(changed)} JSON file(s).")


if __name__ == "__main__":
    main()
