"""Z Mount product database path and JSON helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

JsonObject = dict[str, Any]


class RepositoryError(Exception):
    """Raised when the repository cannot be read."""


def _object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> JsonObject:
    result: JsonObject = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def _reject_nonfinite_number(value: str) -> Any:
    raise ValueError(f"non-finite JSON number {value!r}")


def find_repository_root(start: Path | None = None) -> Path:
    """Find the repository root from a path at or below it."""
    current = (start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "config" / "versions.json").is_file():
            return candidate
    message = "could not find config/versions.json in this directory or its parents"
    raise RepositoryError(message)


def load_json(path: Path) -> Any:
    """Load one UTF-8 JSON file."""
    try:
        with path.open(encoding="utf-8") as stream:
            return json.load(
                stream,
                object_pairs_hook=_object_without_duplicate_keys,
                parse_constant=_reject_nonfinite_number,
            )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        message = f"{path}: {error}"
        raise RepositoryError(message) from error


def record_paths(root: Path) -> list[Path]:
    """Return canonical lens-dataset record paths in stable order."""
    return sorted((root / "data" / "records" / "lenses").glob("*/*.json"))


def adapter_record_paths(root: Path) -> list[Path]:
    """Return canonical mount-adapter record paths in stable order."""
    return sorted((root / "data" / "records" / "adapters").glob("*/*.json"))
