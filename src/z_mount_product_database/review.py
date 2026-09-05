"""Local browser UI for reviewing investigated products against evidence sources."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlsplit

from z_mount_product_database.repository import (
    JsonObject,
    RepositoryError,
    find_repository_root,
    load_json,
)
from z_mount_product_database.validation import validate_repository

HOST = "127.0.0.1"
DEFAULT_PORT = 8765


class ReviewError(Exception):
    """Raised when the local review tool cannot start or complete an action."""


def _object(path: Path) -> JsonObject:
    value = load_json(path)
    if not isinstance(value, dict):
        raise ReviewError(f"{path}: expected a JSON object")
    return cast("JsonObject", value)


def _source_description(source: JsonObject) -> str:
    parts = [
        value
        for key in ("publisherRelationship", "sourceType")
        if isinstance(value := source.get(key), str)
    ]
    checked = source.get("checked")
    if isinstance(checked, list):
        parts.append("fields: " + ", ".join(str(value) for value in checked))
    decision_checks = source.get("decisionChecks")
    if isinstance(decision_checks, list):
        parts.append("decision: " + ", ".join(str(value) for value in decision_checks))
    note = source.get("note")
    if isinstance(note, str):
        parts.append(note)
    return " · ".join(parts)


def _sources(record: JsonObject, research: JsonObject) -> list[JsonObject]:
    sources: list[JsonObject] = []
    by_url: dict[str, JsonObject] = {}

    pages = record.get("officialProductPages")
    if isinstance(pages, list):
        for page in pages:
            if not isinstance(page, dict) or not isinstance(page.get("url"), str):
                continue
            url = cast("str", page["url"])
            source: JsonObject = {
                "url": url,
                "kind": "officialProductPage",
                "description": "",
                "pageFamilies": page.get("pageFamilies"),
                "region": page.get("region"),
                "language": page.get("language"),
            }
            sources.append(source)
            by_url[url] = source

    research_sources = research.get("sources")
    if isinstance(research_sources, list):
        for item in research_sources:
            if not isinstance(item, dict) or not isinstance(item.get("url"), str):
                continue
            url = cast("str", item["url"])
            description = _source_description(item)
            existing = by_url.get(url)
            if existing is not None:
                existing["description"] = description
                continue
            source = {
                "url": url,
                "kind": "researchSource",
                "description": description,
                "pageFamilies": None,
                "region": None,
                "language": None,
            }
            sources.append(source)
            by_url[url] = source

    return sources


def build_catalog(root: Path) -> JsonObject:
    """Load every research result and its optional canonical record."""
    registry = _object(root / "data/product-manufacturer-brand-registry.json")
    manufacturer_names = {
        cast("str", entry["id"]): cast("str", entry["name"])
        for entry in cast("list[JsonObject]", registry["manufacturers"])
    }
    brand_names = {
        cast("str", entry["id"]): cast("str", entry["name"])
        for entry in cast("list[JsonObject]", registry["brands"])
    }
    products: list[JsonObject] = []
    for dataset in ("lenses", "adapters"):
        research_root = root / "research" / "results" / dataset
        for research_path in sorted(research_root.glob("*/*.json")):
            research = _object(research_path)
            subject = research.get("subject")
            decision = research.get("decision")
            if not isinstance(subject, dict) or not isinstance(decision, dict):
                raise ReviewError(f"{research_path}: subject and decision must be objects")

            product_id = research.get("id")
            brand_id = subject.get("brandId")
            manufacturer_id = subject.get("manufacturerId")
            product_name = subject.get("name")
            status = decision.get("status")
            reviewed_on = research.get("reviewedOn")
            if not all(
                value is None or isinstance(value, str) for value in (brand_id, manufacturer_id)
            ):
                raise ReviewError(
                    f"{research_path}: subject brandId/manufacturerId must be strings or null"
                )
            if not all(
                isinstance(value, str) for value in (product_id, product_name, status, reviewed_on)
            ):
                raise ReviewError(
                    f"{research_path}: id, subject name, decision status, and reviewedOn "
                    "must be strings"
                )
            brand = (
                brand_names.get(brand_id)
                if isinstance(brand_id, str)
                else manufacturer_names.get(manufacturer_id)
                if isinstance(manufacturer_id, str)
                else None
            ) or "—"

            record: JsonObject | None = None
            record_path: Path | None = None
            if status == "included":
                record_id = decision.get("recordId")
                if not isinstance(record_id, str):
                    raise ReviewError(f"{research_path}: included result requires recordId")
                record_path = (
                    root
                    / "data"
                    / "records"
                    / dataset
                    / research_path.parent.name
                    / f"{record_id}.json"
                )
                record = _object(record_path)

            products.append(
                {
                    "dataset": dataset,
                    "id": product_id,
                    "brand": brand,
                    "productName": product_name,
                    "status": status,
                    "reviewedOn": reviewed_on,
                    "recordPath": (
                        record_path.relative_to(root).as_posix()
                        if record_path is not None
                        else None
                    ),
                    "researchPath": research_path.relative_to(root).as_posix(),
                    "record": record,
                    "research": research,
                    "sources": _sources(record or {}, research),
                }
            )

    products.sort(
        key=lambda item: (
            0 if item["dataset"] == "lenses" else 1,
            str(item["brand"]).casefold(),
            str(item["productName"]).casefold(),
        )
    )
    diagnostics = [str(diagnostic) for diagnostic in validate_repository(root)]
    return {
        "products": products,
        "validation": diagnostics,
    }


def _code_executable() -> str:
    command = shutil.which("code")
    if command is not None:
        return command
    if sys.platform == "darwin":
        app_command = Path("/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code")
        if app_command.is_file():
            return str(app_command)
    raise ReviewError(
        "VS Code command was not found. Run \"Shell Command: Install 'code' command in PATH\" "
        "from the VS Code Command Palette."
    )


def open_in_vscode(root: Path, json_path: Path, line: int = 1) -> None:
    """Open one review JSON file in the last active VS Code window."""
    target = f"{json_path}:{max(1, line)}:1"
    try:
        result = subprocess.run(
            [_code_executable(), "--reuse-window", "--goto", target],
            cwd=root,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ReviewError(f"could not open VS Code: {error}") from error
    if result.returncode != 0:
        raise ReviewError(f"VS Code command exited with status {result.returncode}")


class ReviewHTTPServer(ThreadingHTTPServer):
    """HTTP server carrying immutable review assets and repository paths."""

    def __init__(self, root: Path, port: int, catalog: JsonObject) -> None:
        super().__init__((HOST, port), ReviewRequestHandler)
        self.root = root
        self.html = files("z_mount_product_database").joinpath("review.html").read_bytes()
        self.catalog = json.dumps(catalog, ensure_ascii=False, separators=(",", ":")).encode()
        self.review_files: dict[tuple[str, str, str], Path] = {}
        for product in cast("list[JsonObject]", catalog["products"]):
            dataset = cast("str", product["dataset"])
            product_id = cast("str", product["id"])
            self.review_files[(dataset, product_id, "research")] = root / cast(
                "str", product["researchPath"]
            )
            record_path = product.get("recordPath")
            if isinstance(record_path, str):
                self.review_files[(dataset, product_id, "record")] = root / record_path


class ReviewRequestHandler(BaseHTTPRequestHandler):
    """Serve the review UI and its two local API endpoints."""

    server: ReviewHTTPServer

    def _send(self, content: bytes, content_type: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self' https: data:; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src https://fonts.gstatic.com; frame-src 'none'; connect-src 'self'",
        )
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, value: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        content = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode()
        self._send(content, "application/json; charset=utf-8", status)

    def _same_origin(self) -> bool:
        origin = self.headers.get("Origin")
        if origin is None:
            return True
        parsed = urlsplit(origin)
        return (
            parsed.scheme == "http"
            and parsed.hostname in {HOST, "localhost"}
            and (parsed.port == self.server.server_port)
        )

    def do_GET(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        if path in {"/", "/index.html"}:
            self._send(self.server.html, "text/html; charset=utf-8")
            return
        if path == "/api/catalog":
            self._send(self.server.catalog, "application/json; charset=utf-8")
            return
        self._send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path != "/api/open-vscode":
            self._send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            return
        if not self._same_origin():
            self._send_json({"error": "forbidden origin"}, HTTPStatus.FORBIDDEN)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 4096:
                raise ValueError("invalid request size")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict) or not isinstance(payload.get("id"), str):
                raise ValueError("id is required")
            dataset = payload.get("dataset")
            if not isinstance(dataset, str) or dataset not in {"lenses", "adapters"}:
                raise ValueError("dataset must be lenses or adapters")
            kind = payload.get("kind")
            if not isinstance(kind, str) or kind not in {"record", "research"}:
                raise ValueError("kind must be record or research")
            json_path = self.server.review_files.get((dataset, payload["id"], kind))
            if json_path is None:
                raise ValueError("unknown review file")
            line_value = payload.get("line", 1)
            if not isinstance(line_value, int) or isinstance(line_value, bool):
                raise ValueError("line must be an integer")
            if not 1 <= line_value <= 1_000_000:
                raise ValueError("line is out of range")
            open_in_vscode(self.server.root, json_path, line_value)
        except (json.JSONDecodeError, ValueError) as error:
            self._send_json({"error": str(error)}, HTTPStatus.BAD_REQUEST)
            return
        except ReviewError as error:
            self._send_json({"error": str(error)}, HTTPStatus.SERVICE_UNAVAILABLE)
            return
        self._send_json({"ok": True})

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    """Start the local review server and optionally open its standalone UI."""
    parser = argparse.ArgumentParser(
        description="Review investigated products against evidence sources"
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--open", action="store_true", help="open the standalone browser UI")
    args = parser.parse_args()

    try:
        root = find_repository_root()
        catalog = build_catalog(root)
        server = ReviewHTTPServer(root, args.port, catalog)
    except (OSError, RepositoryError, ReviewError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from None

    url = f"http://{HOST}:{server.server_port}/"
    print(f"Z Product Compare: {url}")
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
