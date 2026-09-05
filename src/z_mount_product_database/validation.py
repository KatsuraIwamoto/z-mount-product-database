"""Validation for canonical records, research results, and generated datasets."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, cast
from urllib.parse import parse_qsl, urlsplit

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
from referencing import Registry, Resource
from referencing.exceptions import Unresolvable

from z_mount_product_database.generation import (
    ADAPTER_FULL_PATH,
    FULL_PATH,
    LIGHT_PATH,
    SCHEMA_BASE_URL,
    build_artifacts,
)
from z_mount_product_database.repository import (
    JsonObject,
    RepositoryError,
    adapter_record_paths,
    load_json,
    record_paths,
)

PUBLIC_SCHEMA_PATHS = (
    "shared/reference-data.schema.json",
    "shared/shared-definitions.schema.json",
    "lenses/dataset-full.schema.json",
    "lenses/dataset-light.schema.json",
    "lenses/product-components.schema.json",
    "lenses/product-full.schema.json",
    "lenses/product-light.schema.json",
    "lenses/product-record.schema.json",
    "lenses/product-type-lens.schema.json",
    "lenses/product-type-pinhole.schema.json",
    "lenses/product-type-teleconverter.schema.json",
    "lenses/research-result.schema.json",
    "adapters/adapter-components.schema.json",
    "adapters/adapter-full.schema.json",
    "adapters/adapter-record.schema.json",
    "adapters/dataset-full.schema.json",
    "adapters/research-result.schema.json",
)
INTERNAL_SCHEMA_PATHS = (
    "internal/mount-system-registry.schema.json",
    "internal/product-manufacturer-brand-registry.schema.json",
)
SCHEMA_PATHS = (*PUBLIC_SCHEMA_PATHS, *INTERNAL_SCHEMA_PATHS)
DRAFT202012_SCHEMA = "https://json-schema.org/draft/2020-12/schema"

TRACKING_QUERY_PARAMETERS = {
    "_ga",
    "_gl",
    "dclid",
    "fbclid",
    "gad_campaignid",
    "gad_source",
    "gbraid",
    "gclid",
    "msclkid",
    "srsltid",
    "wbraid",
    "yclid",
}

NIKON_PAGE_FAMILIES = ("global", "nikon-imaging-japan", "usa")
OTHER_PAGE_FAMILIES = ("home-country", "global", "japan", "usa")
SEMVER_PATTERN = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)")
CALVER_PATTERN = re.compile(r"\d{4}\.\d{2}\.\d{2}")
PRODUCT_TYPE_FIELD_PREFIXES = ("lens.", "teleconverter.", "pinhole.")
SPECIALIZED_PRODUCT_NAME_PATTERNS = (
    (re.compile(r"\b(?:cine|cinema)\b", re.IGNORECASE), "cinema"),
    (re.compile(r"\banamorphic\b", re.IGNORECASE), "anamorphic"),
    (re.compile(r"\bfisheye\b", re.IGNORECASE), "fisheye"),
    (re.compile(r"\bmacro\b", re.IGNORECASE), "macro"),
    (re.compile(r"\b(?:reflex|mirror lens)\b", re.IGNORECASE), "reflex"),
    (re.compile(r"\bprobe\b", re.IGNORECASE), "probe"),
)
LENS_RESEARCH_COVERAGE_PATHS = (
    "productType",
    "identity",
    "identity.modelNumberOptions",
    "identity.alternateNames",
    "identity.variants",
    "lifecycle",
    "officialProductPages",
    "mount",
    "mount.electronicContacts",
    "mount.adapter",
    "physical.dimensionMeasurements",
    "physical.weightMeasurements",
    "physical.officialEnvironmentalProtectionClaims",
    "physical.filterInterfaces",
    "physical.tripodSupport",
    "physical.externalLengthDuringZoom",
    "physical.externalLengthDuringFocus",
    "physical.isRetractableForStorage",
    "physical.frontAccessoryInterface",
    "controls",
    "accessories",
    "electronicServices",
    "lens.focalLength",
    "lens.aperture",
    "lens.anglesOfView",
    "lens.coverage",
    "lens.imageCircleDiameters",
    "lens.opticalConstruction",
    "lens.specialElements",
    "lens.coatings",
    "lens.focus",
    "lens.zoom",
    "lens.stabilization",
    "lens.specialized",
    "teleconverter.coverage",
    "teleconverter.magnification",
    "teleconverter.apertureLossStops",
    "teleconverter.supportsAutofocus",
    "teleconverter.opticalConstruction",
    "teleconverter.specialElements",
    "teleconverter.coatings",
    "teleconverter.compatibleLensIds",
    "pinhole.coverage",
    "pinhole.focalLength",
    "pinhole.imagingModes",
    "pinhole.anglesOfView",
)
ADAPTER_RESEARCH_COVERAGE_PATHS = (
    "identity",
    "identity.modelNumberOptions",
    "identity.alternateNames",
    "identity.variants",
    "lifecycle",
    "officialProductPages",
    "mountConfigurations",
    "electronics",
    "electronicServices",
    "conversionOptics",
    "mechanisms",
    "physical.dimensionMeasurements",
    "physical.weightMeasurements",
    "physical.officialEnvironmentalProtectionClaims",
    "physical.tripodSupport",
)
AUTHORIZED_RETAILER_COVERAGE_PATHS = frozenset(
    {
        "identity.modelNumberOptions",
        "mount",
        "mount.adapter",
        "mountConfigurations",
    }
)
AUTHORIZED_RETAILER_IMAGE_COVERAGE_PATHS = frozenset(
    {
        "accessories",
        "controls",
        "conversionOptics",
        "electronics",
        "identity",
        "identity.alternateNames",
        "identity.variants",
        "lens.aperture",
        "lens.focalLength",
        "lens.focus",
        "lens.specialized",
        "lens.stabilization",
        "lens.zoom",
        "mechanisms",
        "mount.electronicContacts",
        "physical.externalLengthDuringFocus",
        "physical.externalLengthDuringZoom",
        "physical.filterInterfaces",
        "physical.frontAccessoryInterface",
        "physical.isRetractableForStorage",
        "physical.tripodSupport",
        "pinhole.focalLength",
        "pinhole.imagingModes",
        "productType",
        "teleconverter.apertureLossStops",
        "teleconverter.magnification",
    }
)


@dataclass(frozen=True, order=True)
class Diagnostic:
    """One deterministic, CI-friendly validation error."""

    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _json_object(value: Any, path: str) -> JsonObject:
    if not isinstance(value, dict):
        message = f"{path} must contain a JSON object"
        raise RepositoryError(message)
    return cast("JsonObject", value)


def _schema_refs(value: Any) -> list[str]:
    if isinstance(value, dict):
        own = [value["$ref"]] if isinstance(value.get("$ref"), str) else []
        return own + [ref for child in value.values() for ref in _schema_refs(child)]
    if isinstance(value, list):
        return [ref for child in value for ref in _schema_refs(child)]
    return []


def _schema_registry(root: Path) -> tuple[dict[str, JsonObject], Registry[Any]]:
    schemas: dict[str, JsonObject] = {}
    resources: list[tuple[str, Resource[Any]]] = []
    for relative_path in SCHEMA_PATHS:
        display_path = f"schemas/{relative_path}"
        schema = _json_object(load_json(root / display_path), display_path)
        schemas[relative_path] = schema
        schema_id = schema.get("$id")
        resource_uri = (
            schema_id if isinstance(schema_id, str) else (root / display_path).resolve().as_uri()
        )
        resource_contents = {**schema, "$schema": DRAFT202012_SCHEMA}
        resources.append((resource_uri, Resource.from_contents(resource_contents)))
    return schemas, Registry().with_resources(resources)


def _schema_set_diagnostics(
    root: Path,
    schemas: dict[str, JsonObject],
    registry: Registry[Any],
    schema_version: str | None,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for name in SCHEMA_PATHS:
        display_path = f"schemas/{name}"
        schema = schemas[name]
        if schema.get("$schema") != DRAFT202012_SCHEMA:
            diagnostics.append(
                Diagnostic(f"{display_path}/$schema", f"must be {DRAFT202012_SCHEMA!r}")
            )
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as error:
            diagnostics.append(
                Diagnostic(display_path, f"invalid Draft 2020-12 schema: {error.message}")
            )

        schema_id = schema.get("$id")
        base_uri = (
            schema_id if isinstance(schema_id, str) else (root / display_path).resolve().as_uri()
        )
        resolver = registry.resolver(base_uri=base_uri)
        for ref in sorted(set(_schema_refs(schema))):
            try:
                resolver.lookup(ref)
            except Unresolvable as error:
                diagnostics.append(Diagnostic(display_path, f"unresolvable $ref {ref!r}: {error}"))

    if schema_version is not None:
        for name in PUBLIC_SCHEMA_PATHS:
            expected_id = f"{SCHEMA_BASE_URL}/{schema_version}/{name}"
            if schemas[name].get("$id") != expected_id:
                diagnostics.append(Diagnostic(f"schemas/{name}/$id", f"must be {expected_id!r}"))
    return diagnostics


def _schema_diagnostics(
    instance: Any,
    schema: JsonObject,
    registry: Registry[Any],
    display_path: str,
) -> list[Diagnostic]:
    validator = Draft202012Validator(
        schema,
        registry=registry,
        format_checker=FormatChecker(),
    )
    diagnostics: list[Diagnostic] = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
        location = display_path
        if error.absolute_path:
            location += "/" + "/".join(str(part) for part in error.absolute_path)
        diagnostics.append(Diagnostic(location, error.message))
    return diagnostics


def _walk_ranges(value: Any, path: str) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if isinstance(value, dict):
        for minimum_key, maximum_key in (
            ("minimum", "maximum"),
            ("minimumMm", "maximumMm"),
            ("minimumDiameterMm", "maximumDiameterMm"),
            ("groups", "elements"),
        ):
            minimum = value.get(minimum_key)
            maximum = value.get(maximum_key)
            if (
                isinstance(minimum, int | float)
                and not isinstance(minimum, bool)
                and isinstance(maximum, int | float)
                and not isinstance(maximum, bool)
                and minimum > maximum
            ):
                diagnostics.append(Diagnostic(path, f"{minimum_key} must not exceed {maximum_key}"))
        for key, child in value.items():
            diagnostics.extend(_walk_ranges(child, f"{path}/{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            diagnostics.extend(_walk_ranges(child, f"{path}/{index}"))
    return diagnostics


def _official_name_key(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    lexical_symbols = {"*", "+", "/", "&"}
    return "".join(
        character
        for character in normalized
        if not character.isspace()
        and (not unicodedata.category(character).startswith("P") or character in lexical_symbols)
        and character not in {"®", "™", "℠"}
    )


def _walk_official_names(value: Any, path: str) -> list[tuple[str, str]]:
    names: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "officialName" and isinstance(child, str):
                names.append((path, child))
            else:
                names.extend(_walk_official_names(child, f"{path}.{key}" if path else key))
    elif isinstance(value, list):
        for child in value:
            names.extend(_walk_official_names(child, path))
    return names


def _official_name_diagnostics(
    root: Path,
    records: dict[str, tuple[Path, JsonObject]],
) -> list[Diagnostic]:
    variants: dict[tuple[str, str, str], dict[str, set[str]]] = {}
    diagnostics: list[Diagnostic] = []
    for record_path, record in records.values():
        identity = record.get("identity")
        brand = identity.get("brandId") if isinstance(identity, dict) else None
        if not isinstance(brand, str):
            continue
        display_path = _relative(root, record_path)
        for field_path, name in _walk_official_names(record, ""):
            normalized_name = _official_name_key(name)
            if any(symbol in name for symbol in ("®", "™", "℠")):
                diagnostics.append(
                    Diagnostic(
                        display_path,
                        f"{field_path} must omit trademark registration symbols: {name!r}",
                    )
                )
            key = (brand, field_path, normalized_name)
            entry = variants.setdefault(key, {})
            entry.setdefault(name, set()).add(display_path)

    for (brand, field_path, _key), spellings in sorted(variants.items()):
        if len(spellings) < 2:
            continue
        paths = sorted(path for spelling_paths in spellings.values() for path in spelling_paths)
        diagnostics.append(
            Diagnostic(
                paths[0],
                f"{brand} {field_path} has equivalent officialName spellings: "
                + ", ".join(repr(spelling) for spelling in sorted(spellings)),
            )
        )
    return sorted(diagnostics, key=lambda diagnostic: (diagnostic.path, diagnostic.message))


def _url_diagnostics(url: str, path: str) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    try:
        parsed = urlsplit(url)
    except ValueError:
        return diagnostics
    if parsed.fragment:
        diagnostics.append(Diagnostic(path, "URLs must not contain fragments"))
    tracking = sorted(
        {
            name
            for name, _value in parse_qsl(parsed.query, keep_blank_values=True)
            if name.casefold().startswith("utm_") or name.casefold() in TRACKING_QUERY_PARAMETERS
        }
    )
    if tracking:
        diagnostics.append(
            Diagnostic(path, "URLs must not contain tracking parameters: " + ", ".join(tracking))
        )
    return diagnostics


def _official_url_diagnostics(record: JsonObject, display_path: str) -> list[Diagnostic]:
    pages = record.get("officialProductPages")
    if not isinstance(pages, list):
        return []
    diagnostics: list[Diagnostic] = []
    urls: set[str] = set()
    families: set[str] = set()
    family_positions: list[int] = []
    identity = record.get("identity")
    manufacturer = identity.get("manufacturerId") if isinstance(identity, dict) else None
    family_order = NIKON_PAGE_FAMILIES if manufacturer == "nikon" else OTHER_PAGE_FAMILIES
    for index, page in enumerate(pages):
        if not isinstance(page, dict):
            continue
        url = page.get("url")
        if isinstance(url, str):
            url_path = f"{display_path}/officialProductPages/{index}/url"
            if url in urls:
                diagnostics.append(
                    Diagnostic(url_path, "official product page URLs must be unique")
                )
            urls.add(url)
            diagnostics.extend(_url_diagnostics(url, url_path))
        page_families = page.get("pageFamilies")
        if not isinstance(page_families, list):
            continue
        positions: list[int] = []
        for family in page_families:
            if not isinstance(family, str):
                continue
            if family in families:
                diagnostics.append(
                    Diagnostic(
                        f"{display_path}/officialProductPages/{index}/pageFamilies",
                        f"page family {family!r} must be represented once",
                    )
                )
            families.add(family)
            if family not in family_order:
                diagnostics.append(
                    Diagnostic(
                        f"{display_path}/officialProductPages/{index}/pageFamilies",
                        f"page family {family!r} is not valid for {manufacturer!r}",
                    )
                )
            else:
                positions.append(family_order.index(family))
        if positions:
            family_positions.append(min(positions))
    if family_positions != sorted(family_positions):
        diagnostics.append(
            Diagnostic(
                f"{display_path}/officialProductPages",
                "official product pages are not in the required family order",
            )
        )
    return diagnostics


def _walk_variant_references(
    value: Any,
    path: str,
    known_variant_ids: set[str],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}/{key}"
            if key == "variantId" and isinstance(child, str):
                if child not in known_variant_ids:
                    diagnostics.append(
                        Diagnostic(child_path, f"variantId {child!r} does not resolve")
                    )
            else:
                diagnostics.extend(_walk_variant_references(child, child_path, known_variant_ids))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            diagnostics.extend(
                _walk_variant_references(child, f"{path}/{index}", known_variant_ids)
            )
    return diagnostics


def _variant_diagnostics(record: JsonObject, display_path: str) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    identity = record.get("identity")
    variants = identity.get("variants") if isinstance(identity, dict) else None
    known_variant_ids: set[str] = set()
    if isinstance(variants, list):
        for index, variant in enumerate(variants):
            variant_id = variant.get("variantId") if isinstance(variant, dict) else None
            if not isinstance(variant_id, str):
                continue
            if variant_id in known_variant_ids:
                diagnostics.append(
                    Diagnostic(
                        f"{display_path}/identity/variants/{index}/variantId",
                        f"duplicate variantId {variant_id!r}",
                    )
                )
            known_variant_ids.add(variant_id)
    for key, value in record.items():
        if key != "identity":
            diagnostics.extend(
                _walk_variant_references(value, f"{display_path}/{key}", known_variant_ids)
            )
    return diagnostics


def _record_semantics(
    root: Path,
    path: Path,
    record: JsonObject,
    known_lens_ids: set[str],
) -> list[Diagnostic]:
    display_path = _relative(root, path)
    diagnostics = _walk_ranges(record, display_path)
    diagnostics.extend(_official_url_diagnostics(record, display_path))
    diagnostics.extend(_variant_diagnostics(record, display_path))
    if record.get("id") != path.stem:
        diagnostics.append(Diagnostic(display_path, "id must equal the filename stem"))
    lens = record.get("lens")
    physical = record.get("physical")
    if isinstance(lens, dict):
        identity = record.get("identity")
        product_name = identity.get("productName") if isinstance(identity, dict) else None
        specialized = lens.get("specialized")
        if isinstance(product_name, str) and isinstance(specialized, dict):
            for pattern, feature in SPECIALIZED_PRODUCT_NAME_PATTERNS:
                if pattern.search(product_name) is not None and feature not in specialized:
                    diagnostics.append(
                        Diagnostic(
                            f"{display_path}/lens/specialized",
                            f"productName identifies {feature!r}, but lens.specialized.{feature} "
                            "is absent",
                        )
                    )
        aperture = lens.get("aperture")
        focus = lens.get("focus")
        autofocus = focus.get("autofocus") if isinstance(focus, dict) else None
        requires_contacts = (isinstance(autofocus, dict) and autofocus.get("present") is True) or (
            isinstance(aperture, dict) and aperture.get("controlMechanism") == "electronic"
        )
        mount = record.get("mount")
        electronic_contacts = mount.get("electronicContacts") if isinstance(mount, dict) else None
        if requires_contacts and not (
            isinstance(electronic_contacts, dict) and electronic_contacts.get("present") is True
        ):
            diagnostics.append(
                Diagnostic(
                    f"{display_path}/mount/electronicContacts",
                    "autofocus or electronic aperture requires confirmed electronic contacts",
                )
            )
        focal_length = lens.get("focalLength")
        if (
            isinstance(focal_length, dict)
            and focal_length.get("kind") == "prime"
            and isinstance(physical, dict)
            and "externalLengthDuringZoom" in physical
        ):
            diagnostics.append(
                Diagnostic(
                    f"{display_path}/physical/externalLengthDuringZoom",
                    "a prime lens must omit externalLengthDuringZoom",
                )
            )
    teleconverter = record.get("teleconverter")
    if isinstance(teleconverter, dict):
        compatible_ids = teleconverter.get("compatibleLensIds")
        if isinstance(compatible_ids, list):
            for compatible_id in compatible_ids:
                if isinstance(compatible_id, str) and compatible_id not in known_lens_ids:
                    diagnostics.append(
                        Diagnostic(display_path, f"unresolved compatibleLensId {compatible_id!r}")
                    )
    if isinstance(physical, dict):
        filters = physical.get("filterInterfaces")
        accessories = record.get("accessories")
        hood_models: set[str] = set()
        if isinstance(accessories, dict):
            hoods = accessories.get("lensHoods")
            if isinstance(hoods, list):
                for hood in hoods:
                    options = hood.get("modelNumberOptions") if isinstance(hood, dict) else None
                    if isinstance(options, list):
                        hood_models.update(item for item in options if isinstance(item, str))
        if isinstance(filters, list):
            for index, item in enumerate(filters):
                host = item.get("host") if isinstance(item, dict) else None
                if not isinstance(host, dict) or host.get("kind") != "accessory":
                    continue
                if host.get("category") != "lens-hood":
                    continue
                options = host.get("modelNumberOptions")
                if isinstance(options, list) and not set(options).issubset(hood_models):
                    diagnostics.append(
                        Diagnostic(
                            f"{display_path}/physical/filterInterfaces/{index}/host",
                            "lens-hood model numbers must resolve in accessories.lensHoods",
                        )
                    )
    return diagnostics


def _lens_mount_system_diagnostics(
    root: Path,
    path: Path,
    record: JsonObject,
    mount_system_ids: set[str] | dict[str, str],
) -> list[Diagnostic]:
    mount = record.get("mount")
    adapter = mount.get("adapter") if isinstance(mount, dict) else None
    native_mount = adapter.get("nativeMountSystemId") if isinstance(adapter, dict) else None
    if not isinstance(native_mount, str) or native_mount in mount_system_ids:
        return []
    return [
        Diagnostic(
            f"{_relative(root, path)}/mount/adapter/nativeMountSystemId",
            f"mount system {native_mount!r} is not registered",
        )
    ]


def _adapter_record_semantics(
    root: Path,
    path: Path,
    record: JsonObject,
    mount_system_ids: set[str] | dict[str, str],
) -> list[Diagnostic]:
    display_path = _relative(root, path)
    diagnostics = _walk_ranges(record, display_path)
    diagnostics.extend(_official_url_diagnostics(record, display_path))
    diagnostics.extend(_variant_diagnostics(record, display_path))
    if record.get("id") != path.stem:
        diagnostics.append(Diagnostic(display_path, "id must equal the filename stem"))
    configurations = record.get("mountConfigurations")
    if isinstance(configurations, list):
        for index, configuration in enumerate(configurations):
            if not isinstance(configuration, dict):
                continue
            for field in ("lensSideMountSystemId", "cameraSideMountSystemId"):
                mount_system = configuration.get(field)
                if isinstance(mount_system, str) and mount_system not in mount_system_ids:
                    diagnostics.append(
                        Diagnostic(
                            f"{display_path}/mountConfigurations/{index}/{field}",
                            f"mount system {mount_system!r} is not registered",
                        )
                    )
    return diagnostics


def _load_record_set(
    root: Path,
    relative_directory: Path,
    schema: JsonObject,
    registry: Registry[Any],
    noun: str,
) -> tuple[dict[str, tuple[Path, JsonObject]], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    supported_paths = set((root / relative_directory).glob("*/*.json"))
    records: dict[str, tuple[Path, JsonObject]] = {}
    duplicate_ids: set[str] = set()
    for path in sorted(supported_paths):
        display_path = _relative(root, path)
        record = _json_object(load_json(path), display_path)
        diagnostics.extend(_schema_diagnostics(record, schema, registry, display_path))
        record_id = record.get("id")
        if isinstance(record_id, str):
            if record_id in records:
                duplicate_ids.add(record_id)
            else:
                records[record_id] = (path, record)
    for record_id in sorted(duplicate_ids):
        diagnostics.append(
            Diagnostic(relative_directory.as_posix(), f"duplicate {noun} id {record_id!r}")
        )
    return records, diagnostics


def _load_mount_registry(
    root: Path,
    schema: JsonObject,
    registry: Registry[Any],
) -> tuple[dict[str, str], list[Diagnostic]]:
    display_path = "data/mount-system-registry.json"
    document = _json_object(load_json(root / display_path), display_path)
    diagnostics = _schema_diagnostics(document, schema, registry, display_path)
    mount_systems: dict[str, str] = {}
    names: set[str] = set()
    entries = document.get("mountSystems")
    if isinstance(entries, list):
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                continue
            entry_id = entry.get("id")
            name = entry.get("name")
            if isinstance(entry_id, str):
                if entry_id in mount_systems:
                    diagnostics.append(
                        Diagnostic(f"{display_path}/mountSystems/{index}/id", "id must be unique")
                    )
                mount_systems[entry_id] = name if isinstance(name, str) else ""
            if isinstance(name, str):
                if name in names:
                    diagnostics.append(
                        Diagnostic(
                            f"{display_path}/mountSystems/{index}/name",
                            "name must be unique",
                        )
                    )
                names.add(name)
    if "nikon-z" not in mount_systems:
        diagnostics.append(Diagnostic(display_path, "mount system 'nikon-z' is required"))
    return mount_systems, diagnostics


def _load_registry(
    root: Path,
    schema: JsonObject,
    registry: Registry[Any],
) -> tuple[dict[str, str], dict[str, str], list[Diagnostic]]:
    display_path = "data/product-manufacturer-brand-registry.json"
    document = _json_object(load_json(root / display_path), display_path)
    diagnostics = _schema_diagnostics(document, schema, registry, display_path)
    indexes: list[dict[str, str]] = []
    for field in ("manufacturers", "brands"):
        entries = document.get(field)
        by_id: dict[str, str] = {}
        names: set[str] = set()
        ids: set[str] = set()
        if isinstance(entries, list):
            for index, entry in enumerate(entries):
                if not isinstance(entry, dict):
                    continue
                entry_id = entry.get("id")
                name = entry.get("name")
                if isinstance(entry_id, str):
                    if entry_id in ids:
                        diagnostics.append(
                            Diagnostic(f"{display_path}/{field}/{index}/id", "id must be unique")
                        )
                    ids.add(entry_id)
                if isinstance(name, str):
                    if name in names:
                        diagnostics.append(
                            Diagnostic(
                                f"{display_path}/{field}/{index}/name",
                                "name must be unique",
                            )
                        )
                    names.add(name)
                if isinstance(name, str) and isinstance(entry_id, str):
                    by_id[entry_id] = name
        indexes.append(by_id)
    return indexes[0], indexes[1], diagnostics


def _registry_record_diagnostics(
    root: Path,
    records: dict[str, tuple[Path, JsonObject]],
    manufacturers: dict[str, str],
    brands: dict[str, str],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for path, record in records.values():
        display_path = _relative(root, path)
        identity = record.get("identity")
        if not isinstance(identity, dict):
            continue
        manufacturer_id = identity.get("manufacturerId")
        brand_id = identity.get("brandId")
        if isinstance(manufacturer_id, str) and manufacturer_id not in manufacturers:
            diagnostics.append(
                Diagnostic(
                    f"{display_path}/identity/manufacturerId",
                    f"manufacturer ID {manufacturer_id!r} is not registered",
                )
            )
        if isinstance(brand_id, str):
            if brand_id not in brands:
                diagnostics.append(
                    Diagnostic(
                        f"{display_path}/identity/brandId",
                        f"brand ID {brand_id!r} is not registered",
                    )
                )
            elif path.parent.name != brand_id:
                diagnostics.append(
                    Diagnostic(display_path, f"brand directory must be {brand_id!r}")
                )
        alternate_names = identity.get("alternateNames")
        if isinstance(alternate_names, list):
            for index, alternate_name in enumerate(alternate_names):
                alternate_brand_id = (
                    alternate_name.get("brandId") if isinstance(alternate_name, dict) else None
                )
                if isinstance(alternate_brand_id, str) and alternate_brand_id not in brands:
                    diagnostics.append(
                        Diagnostic(
                            f"{display_path}/identity/alternateNames/{index}/brandId",
                            f"brand ID {alternate_brand_id!r} is not registered",
                        )
                    )
    return diagnostics


def _research_diagnostics(
    root: Path,
    relative_directory: Path,
    schema: JsonObject,
    registry: Registry[Any],
    records: dict[str, tuple[Path, JsonObject]],
    manufacturers: dict[str, str],
    brands: dict[str, str],
    data_version_date: date | None,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    result_directory = root / relative_directory
    supported_paths = set(result_directory.glob("*/*.json"))
    for path in sorted(result_directory.rglob("*.json")):
        if path not in supported_paths:
            diagnostics.append(
                Diagnostic(
                    _relative(root, path),
                    f"research results must be {relative_directory.as_posix()}/"
                    "<brand-id>/<result-id>.json",
                )
            )
    result_ids: set[str] = set()
    included_by_record: dict[str, str] = {}
    for path in sorted(supported_paths):
        display_path = _relative(root, path)
        result = _json_object(load_json(path), display_path)
        diagnostics.extend(_schema_diagnostics(result, schema, registry, display_path))
        reviewed_on = result.get("reviewedOn")
        reviewed_date: date | None = None
        if isinstance(reviewed_on, str):
            try:
                reviewed_date = date.fromisoformat(reviewed_on)
            except ValueError:
                pass
            else:
                if data_version_date is not None and reviewed_date > data_version_date:
                    diagnostics.append(
                        Diagnostic(
                            f"{display_path}/reviewedOn",
                            "must not be later than config/versions.json dataVersion",
                        )
                    )
        result_id = result.get("id")
        if isinstance(result_id, str):
            if result_id in result_ids:
                diagnostics.append(Diagnostic(display_path, f"duplicate result id {result_id!r}"))
            result_ids.add(result_id)
            if path.stem != result_id:
                diagnostics.append(Diagnostic(display_path, "id must equal the filename stem"))
        subject = result.get("subject")
        if isinstance(subject, dict):
            manufacturer_id = subject.get("manufacturerId")
            brand_id = subject.get("brandId")
            if isinstance(manufacturer_id, str) and manufacturer_id not in manufacturers:
                diagnostics.append(
                    Diagnostic(
                        f"{display_path}/subject/manufacturerId",
                        f"manufacturer ID {manufacturer_id!r} is not registered",
                    )
                )
            expected_directory = "unattributed" if brand_id is None else brand_id
            if isinstance(brand_id, str) and brand_id not in brands:
                diagnostics.append(
                    Diagnostic(
                        f"{display_path}/subject/brandId",
                        f"brand ID {brand_id!r} is not registered",
                    )
                )
            elif path.parent.name != expected_directory:
                diagnostics.append(
                    Diagnostic(display_path, f"brand directory must be {expected_directory!r}")
                )
        sources = result.get("sources")
        if isinstance(sources, list):
            seen_urls: set[str] = set()
            for index, source in enumerate(sources):
                url = source.get("url") if isinstance(source, dict) else None
                if not isinstance(url, str):
                    continue
                url_path = f"{display_path}/sources/{index}/url"
                if url in seen_urls:
                    diagnostics.append(Diagnostic(url_path, "source URLs must be unique"))
                seen_urls.add(url)
                diagnostics.extend(_url_diagnostics(url, url_path))
        decision = result.get("decision")
        if not isinstance(decision, dict) or decision.get("status") != "included":
            continue
        record_id = decision.get("recordId")
        if not isinstance(record_id, str):
            continue
        if result_id != record_id:
            diagnostics.append(Diagnostic(display_path, "included result id must equal recordId"))
        if record_id in included_by_record:
            diagnostics.append(
                Diagnostic(display_path, f"record {record_id!r} has multiple included results")
            )
        included_by_record[record_id] = display_path
        record_entry = records.get(record_id)
        if record_entry is None:
            diagnostics.append(Diagnostic(display_path, f"recordId {record_id!r} does not resolve"))
            continue
        if reviewed_date is not None:
            diagnostics.extend(
                _lifecycle_review_diagnostics(
                    root,
                    record_entry[0],
                    record_entry[1],
                    reviewed_date,
                )
            )
        product_type = record_entry[1].get("productType")
        if isinstance(product_type, str) and isinstance(sources, list):
            expected_prefix = f"{product_type}."
            for source_index, source in enumerate(sources):
                checked = source.get("checked") if isinstance(source, dict) else None
                if not isinstance(checked, list):
                    continue
                for checked_index, field_path in enumerate(checked):
                    if (
                        isinstance(field_path, str)
                        and field_path.startswith(PRODUCT_TYPE_FIELD_PREFIXES)
                        and not field_path.startswith(expected_prefix)
                    ):
                        diagnostics.append(
                            Diagnostic(
                                f"{display_path}/sources/{source_index}/checked/{checked_index}",
                                f"field path {field_path!r} does not apply to {product_type!r}",
                            )
                        )
        canonical_identity = record_entry[1].get("identity")
        if isinstance(subject, dict) and isinstance(canonical_identity, dict):
            for research_key, canonical_key in (
                ("manufacturerId", "manufacturerId"),
                ("brandId", "brandId"),
                ("name", "productName"),
            ):
                if subject.get(research_key) != canonical_identity.get(canonical_key):
                    diagnostics.append(
                        Diagnostic(
                            f"{display_path}/subject/{research_key}",
                            f"must match canonical identity.{canonical_key}",
                        )
                    )
        coverage_paths = (
            ADAPTER_RESEARCH_COVERAGE_PATHS
            if relative_directory.name == "adapters"
            else LENS_RESEARCH_COVERAGE_PATHS
        )
        diagnostics.extend(
            _research_coverage_diagnostics(
                display_path,
                record_entry[1],
                sources,
                coverage_paths,
            )
        )
    for record_id in sorted(set(records) - set(included_by_record)):
        diagnostics.append(
            Diagnostic(
                relative_directory.as_posix(),
                f"record {record_id!r} has no included research result",
            )
        )
    return diagnostics


def _research_source_metadata_diagnostics(root: Path) -> list[Diagnostic]:
    sources_by_url: dict[str, dict[tuple[str, str], set[str]]] = {}
    for path in sorted((root / "research" / "results").glob("*/*/*.json")):
        display_path = _relative(root, path)
        result = _json_object(load_json(path), display_path)
        sources = result.get("sources")
        if not isinstance(sources, list):
            continue
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                continue
            url = source.get("url")
            relationship = source.get("publisherRelationship")
            source_type = source.get("sourceType")
            if not all(isinstance(value, str) for value in (url, relationship, source_type)):
                continue
            source_path = f"{display_path}/sources/{index}"
            metadata = sources_by_url.setdefault(cast("str", url), {})
            metadata.setdefault((cast("str", relationship), cast("str", source_type)), set()).add(
                source_path
            )

    diagnostics: list[Diagnostic] = []
    for url, metadata in sorted(sources_by_url.items()):
        if len(metadata) < 2:
            continue
        paths = sorted(path for metadata_paths in metadata.values() for path in metadata_paths)
        values = ", ".join(
            f"{relationship}/{source_type}" for relationship, source_type in sorted(metadata)
        )
        diagnostics.append(
            Diagnostic(
                paths[0],
                f"source URL {url!r} has inconsistent metadata: {values}",
            )
        )
    return diagnostics


def _field_value(value: Any, field_path: str) -> Any:
    current = value
    for part in field_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _contains_canonical_fact(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, dict):
        return any(_contains_canonical_fact(child) for child in value.values())
    if isinstance(value, list):
        return not value or any(_contains_canonical_fact(child) for child in value)
    return True


def _accepted_checked_paths(source: Any) -> set[str]:
    if not isinstance(source, dict):
        return set()
    checked = source.get("checked")
    if not isinstance(checked, list):
        return set()
    paths = {field_path for field_path in checked if isinstance(field_path, str)}
    relationship = source.get("publisherRelationship")
    if relationship in {"manufacturer-or-brand", "authorized-distributor"}:
        return paths
    if relationship == "crowdfunding-platform":
        return paths - {"officialProductPages"}
    if relationship == "authorized-retailer":
        allowed_paths = AUTHORIZED_RETAILER_COVERAGE_PATHS
        if source.get("sourceType") == "image":
            allowed_paths |= AUTHORIZED_RETAILER_IMAGE_COVERAGE_PATHS
        return paths & allowed_paths
    return set()


def _lifecycle_review_diagnostics(
    root: Path,
    record_path: Path,
    record: JsonObject,
    reviewed_date: date,
) -> list[Diagnostic]:
    lifecycle = record.get("lifecycle")
    if not isinstance(lifecycle, dict):
        return []

    dated_fields: list[tuple[str, Any]] = [
        ("announcementDate", lifecycle.get("announcementDate")),
    ]
    official_designations = lifecycle.get("officialDesignations")
    if isinstance(official_designations, list):
        dated_fields.extend(
            (f"officialDesignations/{index}/observedOn", designation.get("observedOn"))
            for index, designation in enumerate(official_designations)
            if isinstance(designation, dict)
        )

    display_path = _relative(root, record_path)
    diagnostics: list[Diagnostic] = []
    for field_path, value in dated_fields:
        if not isinstance(value, str):
            continue
        try:
            value_date = date.fromisoformat(value)
        except ValueError:
            continue
        if value_date > reviewed_date:
            diagnostics.append(
                Diagnostic(
                    f"{display_path}/lifecycle/{field_path}",
                    "must not be later than paired research reviewedOn",
                )
            )
    return diagnostics


def _research_coverage_diagnostics(
    display_path: str,
    record: JsonObject,
    sources: Any,
    coverage_paths: tuple[str, ...],
) -> list[Diagnostic]:
    source_list = sources if isinstance(sources, list) else []
    checked_paths = {
        field_path for source in source_list for field_path in _accepted_checked_paths(source)
    }
    diagnostics: list[Diagnostic] = []
    for field_path in coverage_paths:
        field_value = _field_value(record, field_path)
        if field_path == "officialProductPages":
            for page in field_value if isinstance(field_value, list) else []:
                url = page.get("url") if isinstance(page, dict) else None
                if not isinstance(url, str):
                    continue
                if any(
                    isinstance(source, dict)
                    and source.get("url") == url
                    and "officialProductPages" in _accepted_checked_paths(source)
                    for source in source_list
                ):
                    continue
                diagnostics.append(
                    Diagnostic(
                        f"{display_path}/sources",
                        f"official product page {url!r} has no matching checked source",
                    )
                )
            continue
        presence_is_fact = (
            field_path == "lens.specialized" and isinstance(field_value, dict) and bool(field_value)
        )
        if not presence_is_fact and not _contains_canonical_fact(field_value):
            continue
        if field_path in checked_paths:
            continue
        diagnostics.append(
            Diagnostic(
                f"{display_path}/sources",
                f"canonical field group {field_path!r} has no checked source coverage",
            )
        )
    return diagnostics


def _registry_usage_diagnostics(
    root: Path,
    lens_records: dict[str, tuple[Path, JsonObject]],
    adapter_records: dict[str, tuple[Path, JsonObject]],
    manufacturers: dict[str, str],
    brands: dict[str, str],
    mount_systems: dict[str, str],
) -> list[Diagnostic]:
    used_manufacturers: set[str] = set()
    used_brands: set[str] = set()
    used_mount_systems: set[str] = set()

    for _path, record in (*lens_records.values(), *adapter_records.values()):
        identity = record.get("identity")
        if isinstance(identity, dict):
            manufacturer_id = identity.get("manufacturerId")
            brand_id = identity.get("brandId")
            if isinstance(manufacturer_id, str):
                used_manufacturers.add(manufacturer_id)
            if isinstance(brand_id, str):
                used_brands.add(brand_id)
            alternate_names = identity.get("alternateNames")
            if isinstance(alternate_names, list):
                for alternate_name in alternate_names:
                    alternate_brand_id = (
                        alternate_name.get("brandId") if isinstance(alternate_name, dict) else None
                    )
                    if isinstance(alternate_brand_id, str):
                        used_brands.add(alternate_brand_id)

        mount = record.get("mount")
        if isinstance(mount, dict):
            system_id = mount.get("systemId")
            if isinstance(system_id, str):
                used_mount_systems.add(system_id)
            adapter = mount.get("adapter")
            native_mount_system_id = (
                adapter.get("nativeMountSystemId") if isinstance(adapter, dict) else None
            )
            if isinstance(native_mount_system_id, str):
                used_mount_systems.add(native_mount_system_id)

        mount_configurations = record.get("mountConfigurations")
        if isinstance(mount_configurations, list):
            for configuration in mount_configurations:
                if not isinstance(configuration, dict):
                    continue
                for field in ("lensSideMountSystemId", "cameraSideMountSystemId"):
                    mount_system_id = configuration.get(field)
                    if isinstance(mount_system_id, str):
                        used_mount_systems.add(mount_system_id)

    for path in sorted((root / "research" / "results").glob("*/*/*.json")):
        result = _json_object(load_json(path), _relative(root, path))
        subject = result.get("subject")
        if not isinstance(subject, dict):
            continue
        manufacturer_id = subject.get("manufacturerId")
        brand_id = subject.get("brandId")
        if isinstance(manufacturer_id, str):
            used_manufacturers.add(manufacturer_id)
        if isinstance(brand_id, str):
            used_brands.add(brand_id)

    diagnostics = [
        Diagnostic(
            "data/product-manufacturer-brand-registry.json/manufacturers",
            f"unused manufacturer ID {entry_id!r}",
        )
        for entry_id in sorted(set(manufacturers) - used_manufacturers)
    ]
    diagnostics.extend(
        Diagnostic(
            "data/product-manufacturer-brand-registry.json/brands",
            f"unused brand ID {entry_id!r}",
        )
        for entry_id in sorted(set(brands) - used_brands)
    )
    diagnostics.extend(
        Diagnostic(
            "data/mount-system-registry.json/mountSystems",
            f"unused mount-system ID {entry_id!r}",
        )
        for entry_id in sorted(set(mount_systems) - used_mount_systems)
    )
    return diagnostics


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
        for subset_item in subset:
            while source_index < len(source) and not _is_ordered_recursive_subset(
                subset_item, source[source_index]
            ):
                source_index += 1
            if source_index == len(source):
                return False
            source_index += 1
        return True
    return type(subset) is type(source) and subset == source


def _generated_diagnostics(
    root: Path,
    schemas: dict[str, JsonObject],
    registry: Registry[Any],
    manufacturers: dict[str, str],
    brands: dict[str, str],
    mount_systems: dict[str, str],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    expected = build_artifacts(root)
    for relative_path, expected_bytes in expected.items():
        path = root / relative_path
        if not path.is_file():
            diagnostics.append(Diagnostic(relative_path.as_posix(), "generated file is missing"))
        elif path.read_bytes() != expected_bytes:
            diagnostics.append(Diagnostic(relative_path.as_posix(), "generated file is stale"))
    if not all((root / path).is_file() for path in (FULL_PATH, LIGHT_PATH, ADAPTER_FULL_PATH)):
        return diagnostics
    full = _json_object(load_json(root / FULL_PATH), FULL_PATH.as_posix())
    light = _json_object(load_json(root / LIGHT_PATH), LIGHT_PATH.as_posix())
    adapter_full = _json_object(load_json(root / ADAPTER_FULL_PATH), ADAPTER_FULL_PATH.as_posix())
    diagnostics.extend(
        _schema_diagnostics(
            full,
            schemas["lenses/dataset-full.schema.json"],
            registry,
            FULL_PATH.as_posix(),
        )
    )
    for document, record_field, display_path in (
        (full, "products", FULL_PATH.as_posix()),
        (light, "products", LIGHT_PATH.as_posix()),
        (adapter_full, "adapters", ADAPTER_FULL_PATH.as_posix()),
    ):
        records = full.get("products") if document is light else document.get(record_field)
        reference_data = document.get("referenceData")
        if not isinstance(records, list) or not isinstance(reference_data, dict):
            continue
        manufacturer_ids: set[str] = set()
        brand_ids: set[str] = set()
        mount_ids: set[str] = set()
        for record in records:
            if not isinstance(record, dict):
                continue
            identity = record.get("identity")
            if isinstance(identity, dict):
                manufacturer_id = identity.get("manufacturerId")
                brand_id = identity.get("brandId")
                if isinstance(manufacturer_id, str):
                    manufacturer_ids.add(manufacturer_id)
                if isinstance(brand_id, str):
                    brand_ids.add(brand_id)
                alternate_names = identity.get("alternateNames")
                if isinstance(alternate_names, list):
                    for alternate_name in alternate_names:
                        alternate_brand_id = (
                            alternate_name.get("brandId")
                            if isinstance(alternate_name, dict)
                            else None
                        )
                        if isinstance(alternate_brand_id, str):
                            brand_ids.add(alternate_brand_id)
            mount = record.get("mount")
            system_id = mount.get("systemId") if isinstance(mount, dict) else None
            if isinstance(system_id, str):
                mount_ids.add(system_id)
            embedded_adapter = mount.get("adapter") if isinstance(mount, dict) else None
            native_mount_id = (
                embedded_adapter.get("nativeMountSystemId")
                if isinstance(embedded_adapter, dict)
                else None
            )
            if isinstance(native_mount_id, str):
                mount_ids.add(native_mount_id)
            configurations = record.get("mountConfigurations")
            if isinstance(configurations, list):
                for configuration in configurations:
                    if not isinstance(configuration, dict):
                        continue
                    for field in ("lensSideMountSystemId", "cameraSideMountSystemId"):
                        configuration_system_id = configuration.get(field)
                        if isinstance(configuration_system_id, str):
                            mount_ids.add(configuration_system_id)
        expected_reference_data = {
            "manufacturers": {
                entry_id: {"name": manufacturers[entry_id]}
                for entry_id in sorted(manufacturer_ids)
                if entry_id in manufacturers
            },
            "brands": {
                entry_id: {"name": brands[entry_id]}
                for entry_id in sorted(brand_ids)
                if entry_id in brands
            },
            "mountSystems": {
                entry_id: {"name": mount_systems[entry_id]}
                for entry_id in sorted(mount_ids)
                if entry_id in mount_systems
            },
        }
        if reference_data != expected_reference_data:
            diagnostics.append(
                Diagnostic(
                    f"{display_path}/referenceData",
                    "must contain exactly the registry entries referenced by this dataset",
                )
            )
    if full.get("referenceData") != light.get("referenceData"):
        diagnostics.append(
            Diagnostic(
                f"{LIGHT_PATH.as_posix()}/referenceData",
                "must equal the Lens Full referenceData",
            )
        )
    diagnostics.extend(
        _schema_diagnostics(
            light,
            schemas["lenses/dataset-light.schema.json"],
            registry,
            LIGHT_PATH.as_posix(),
        )
    )
    diagnostics.extend(
        _schema_diagnostics(
            adapter_full,
            schemas["adapters/dataset-full.schema.json"],
            registry,
            ADAPTER_FULL_PATH.as_posix(),
        )
    )
    full_products = full.get("products")
    light_products = light.get("products")
    if isinstance(full_products, list) and isinstance(light_products, list):
        if len(full_products) != len(light_products):
            diagnostics.append(Diagnostic(LIGHT_PATH.as_posix(), "product count differs from full"))
        for index, light_product in enumerate(light_products):
            if index >= len(full_products) or not _is_ordered_recursive_subset(
                light_product, full_products[index]
            ):
                diagnostics.append(
                    Diagnostic(
                        f"{LIGHT_PATH.as_posix()}/products/{index}",
                        "light product must be an ordered recursive subset of the matching full product",
                    )
                )
    return diagnostics


def _configuration_diagnostics(
    root: Path,
    schemas: dict[str, JsonObject],
    registry: Registry[Any],
) -> tuple[list[Diagnostic], date | None]:
    path = "config/versions.json"
    config = _json_object(load_json(root / path), path)
    diagnostics: list[Diagnostic] = []
    if set(config) != {"schemaVersion", "dataVersion"}:
        diagnostics.append(Diagnostic(path, "version configuration has unexpected fields"))
    schema_version = config.get("schemaVersion")
    if not isinstance(schema_version, str) or SEMVER_PATTERN.fullmatch(schema_version) is None:
        diagnostics.append(Diagnostic(f"{path}/schemaVersion", "must be major.minor.patch SemVer"))
    valid_schema_version = (
        schema_version
        if isinstance(schema_version, str) and SEMVER_PATTERN.fullmatch(schema_version)
        else None
    )
    diagnostics.extend(_schema_set_diagnostics(root, schemas, registry, valid_schema_version))
    for name in INTERNAL_SCHEMA_PATHS:
        if "$id" in schemas[name]:
            diagnostics.append(
                Diagnostic(
                    f"schemas/{name}/$id",
                    "repository-only schema must not declare a public identifier",
                )
            )
    data_version = config.get("dataVersion")
    data_version_date: date | None = None
    if not isinstance(data_version, str) or CALVER_PATTERN.fullmatch(data_version) is None:
        diagnostics.append(Diagnostic(f"{path}/dataVersion", "must be a YYYY.MM.DD date"))
    else:
        try:
            data_version_date = date.fromisoformat(data_version.replace(".", "-"))
        except ValueError:
            diagnostics.append(Diagnostic(f"{path}/dataVersion", "must be a valid calendar date"))
    return diagnostics, data_version_date


def validate_repository(root: Path, *, include_generated: bool = True) -> list[Diagnostic]:
    """Return every repository diagnostic in deterministic order."""
    schemas, registry = _schema_registry(root)
    diagnostics, data_version_date = _configuration_diagnostics(root, schemas, registry)
    expected_schema_paths = {root / "schemas" / path for path in SCHEMA_PATHS}
    actual_schema_paths = set((root / "schemas").rglob("*.schema.json"))
    for path in sorted(actual_schema_paths - expected_schema_paths):
        diagnostics.append(Diagnostic(_relative(root, path), "obsolete or unsupported schema"))

    supported_record_paths = {*record_paths(root), *adapter_record_paths(root)}
    for path in sorted((root / "data" / "records").rglob("*.json")):
        if path not in supported_record_paths:
            diagnostics.append(
                Diagnostic(
                    _relative(root, path),
                    "records must be data/records/<lenses|adapters>/<brand-id>/<record-id>.json",
                )
            )
    lens_records, lens_record_diagnostics = _load_record_set(
        root,
        Path("data/records/lenses"),
        schemas["lenses/product-record.schema.json"],
        registry,
        "lens-dataset product",
    )
    diagnostics.extend(lens_record_diagnostics)
    diagnostics.extend(_official_name_diagnostics(root, lens_records))
    lens_ids = {
        record_id
        for record_id, (_path, record) in lens_records.items()
        if record.get("productType") == "lens"
    }
    for path, record in lens_records.values():
        diagnostics.extend(_record_semantics(root, path, record, lens_ids))

    adapter_records, adapter_record_diagnostics = _load_record_set(
        root,
        Path("data/records/adapters"),
        schemas["adapters/adapter-record.schema.json"],
        registry,
        "mount adapter",
    )
    diagnostics.extend(adapter_record_diagnostics)
    diagnostics.extend(_official_name_diagnostics(root, adapter_records))

    manufacturers, brands, registry_diagnostics = _load_registry(
        root,
        schemas["internal/product-manufacturer-brand-registry.schema.json"],
        registry,
    )
    diagnostics.extend(registry_diagnostics)
    diagnostics.extend(_registry_record_diagnostics(root, lens_records, manufacturers, brands))
    diagnostics.extend(_registry_record_diagnostics(root, adapter_records, manufacturers, brands))

    mount_system_ids, mount_registry_diagnostics = _load_mount_registry(
        root,
        schemas["internal/mount-system-registry.schema.json"],
        registry,
    )
    diagnostics.extend(mount_registry_diagnostics)
    for path, record in lens_records.values():
        diagnostics.extend(_lens_mount_system_diagnostics(root, path, record, mount_system_ids))
    for path, record in adapter_records.values():
        diagnostics.extend(_adapter_record_semantics(root, path, record, mount_system_ids))

    lens_research_directory = Path("research/results/lenses")
    adapter_research_directory = Path("research/results/adapters")
    supported_research_paths = {
        *(root / lens_research_directory).glob("*/*.json"),
        *(root / adapter_research_directory).glob("*/*.json"),
    }
    for path in sorted((root / "research" / "results").rglob("*.json")):
        if path not in supported_research_paths:
            diagnostics.append(
                Diagnostic(
                    _relative(root, path),
                    "research results must be research/results/<lenses|adapters>/"
                    "<brand-id>/<result-id>.json",
                )
            )
    diagnostics.extend(
        _research_diagnostics(
            root,
            lens_research_directory,
            schemas["lenses/research-result.schema.json"],
            registry,
            lens_records,
            manufacturers,
            brands,
            data_version_date,
        )
    )
    diagnostics.extend(
        _research_diagnostics(
            root,
            adapter_research_directory,
            schemas["adapters/research-result.schema.json"],
            registry,
            adapter_records,
            manufacturers,
            brands,
            data_version_date,
        )
    )
    diagnostics.extend(_research_source_metadata_diagnostics(root))
    diagnostics.extend(
        _registry_usage_diagnostics(
            root,
            lens_records,
            adapter_records,
            manufacturers,
            brands,
            mount_system_ids,
        )
    )
    if include_generated and not diagnostics:
        diagnostics.extend(
            _generated_diagnostics(root, schemas, registry, manufacturers, brands, mount_system_ids)
        )
    return sorted(set(diagnostics))
