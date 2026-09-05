"""Checks for source JSON formatting."""

from __future__ import annotations

import json
from pathlib import Path

from tools.format_json import format_repository_json


def test_format_repository_json_includes_schemas_and_excludes_generated_files(
    tmp_path: Path,
) -> None:
    source_paths = [
        tmp_path / "data/record.json",
        tmp_path / "schemas/example.schema.json",
        tmp_path / "tools/example.json",
    ]
    generated_path = tmp_path / "dist/generated.json"
    unformatted = '{"label":"日本語","items":[1,2]}\n'
    for path in (*source_paths, generated_path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(unformatted, encoding="utf-8")

    expected_changes = [path.relative_to(tmp_path) for path in source_paths]
    assert format_repository_json(tmp_path, check=True) == expected_changes
    assert all(path.read_text(encoding="utf-8") == unformatted for path in source_paths)

    assert format_repository_json(tmp_path) == expected_changes
    formatted = json.dumps(json.loads(unformatted), ensure_ascii=False, indent=2) + "\n"
    assert all(path.read_text(encoding="utf-8") == formatted for path in source_paths)
    assert generated_path.read_text(encoding="utf-8") == unformatted
    assert format_repository_json(tmp_path, check=True) == []
