"""Command-line entry points for repository generation and validation."""

from __future__ import annotations

import sys

from z_mount_product_database.generation import GenerationError, generate
from z_mount_product_database.repository import RepositoryError, find_repository_root
from z_mount_product_database.validation import validate_repository


def generate_main() -> None:
    """Validate sources and generate all public artifacts."""
    try:
        root = find_repository_root()
        diagnostics = validate_repository(root, include_generated=False)
        if diagnostics:
            raise GenerationError("\n".join(str(diagnostic) for diagnostic in diagnostics))
        outputs = generate(root)
    except (GenerationError, RepositoryError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from None
    print(f"Generated {len(outputs)} artifact(s).")


def validate_main() -> None:
    """Run repository validation and exit nonzero on errors."""
    try:
        root = find_repository_root()
        diagnostics = validate_repository(root)
    except RepositoryError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from None
    if diagnostics:
        for diagnostic in diagnostics:
            print(f"error: {diagnostic}", file=sys.stderr)
        print(f"{len(diagnostics)} validation error(s)", file=sys.stderr)
        raise SystemExit(1)
    print("Validation passed.")
