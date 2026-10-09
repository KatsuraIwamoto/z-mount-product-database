# Using the distribution data

This page explains how to choose the right public file, download it from GitHub Releases, and read it with JavaScript or Python.
If this is your first time using the data, follow steps 1 through 3 in order.
Refer to the metadata and schema compatibility sections when you need them.

## 1. Choose a distribution file {#distribution-files}

The official distribution consists of three JSON files and one product list.

| Distribution | Choose it when |
| --- | --- |
| **Lens Full**<br>`z-mount-lenses.full.json` | You need every recorded field for lenses and related optical products. Use this file as the default for search, analysis, validation, and redistribution. |
| **Lens Light**<br>`z-mount-lenses.light.json` | You want a smaller file while retaining compatibility with this project's existing website. |
| **Mount adapter Full**<br>`z-mount-adapters.full.json` | You need every recorded field for mount adapters. There is no Light version for mount adapters. |
| **Product list**<br>`PRODUCTS.md` | You want to review included products, research status, and statistics without using JSON. |

Lens Light includes basic information such as product names, release information, official product page URLs, mounts, dimensions, weights, and filter attachment methods.
For lenses, it includes focal length, maximum-aperture f-numbers and T-stops, image format, whether AF, MF, and in-lens stabilization are present, minimum focus distance, and maximum reproduction ratio.
It omits details such as controls, accessories, optical construction, and coatings.
See the [Lens Light JSON Schema reference](reference/schemas/lenses/product-light.md) for the complete field list.

!!! tip "Choose Full when unsure"
    Lens Full and Lens Light contain the same products in the same order, with matching `id` values.
    Lens Light removes fields from Lens Full and does not add Light-only or summary values.
    If you have not decided which fields a search or analysis needs, choose Lens Full.

The ordering guarantee applies to Lens Full and Light with the same `dataVersion`. Across releases, do not use an array index as a product identifier. Before combining Full and Light, confirm that their `dataVersion` values match and join products by `id`.

!!! note "Browse products without JSON"
    `PRODUCTS.md` lists included products, official product pages, the last review date for each research result, and research status in a readable format.
    Like the three distribution JSON files, it is an official file attached to each GitHub Release.
    See [Browse evidence from the product list](research.md#browse-product-research) for how to read each entry.

## 2. Download from GitHub Releases {#download}

These links point to the latest distribution available at the time you use them.

- [Download Lens Full](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/z-mount-lenses.full.json)
- [Download Lens Light](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/z-mount-lenses.light.json)
- [Download Mount adapter Full](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/z-mount-adapters.full.json)
- [Download the product list](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/PRODUCTS.md)

The latest URLs return different content after a new release is published.
To keep using the same version, replace `YYYY.MM.DD` in these URLs with the required data version.

```text
https://github.com/KatsuraIwamoto/z-mount-product-database/releases/download/YYYY.MM.DD/z-mount-lenses.full.json
https://github.com/KatsuraIwamoto/z-mount-product-database/releases/download/YYYY.MM.DD/z-mount-lenses.light.json
https://github.com/KatsuraIwamoto/z-mount-product-database/releases/download/YYYY.MM.DD/z-mount-adapters.full.json
https://github.com/KatsuraIwamoto/z-mount-product-database/releases/download/YYYY.MM.DD/PRODUCTS.md
```

Use a version-pinned URL for reproducible analysis and production workflows.
Do not use `dist/` or the repository-root `PRODUCTS.md` on a Git branch as a distribution source.
Published Release attachments are not replaced.
Corrections and updates are published in a new `dataVersion` GitHub Release, and earlier GitHub Releases remain available.

## 3. Read with JavaScript or Python {#read-data}

!!! warning "Serve web-app data from your own origin"
    Use GitHub Releases as the source for obtaining distribution data, not as the origin that serves a web app.
    In a production web app, fetch a version-pinned distribution at build or update time and place it on the same origin as the app or on your CDN.
    Avoid designs that access GitHub Releases directly from the browser on every page view.

The following examples read a downloaded or deployed Lens Full file and print the data version, number of included products, and key identity fields for the first product.

=== "JavaScript"

    This example places the distribution under `/data/` at the website root and reads it from a `<script type="module">` element or an equivalent JavaScript module.
    If you place the file elsewhere, change the path passed to `fetch()`.

    ```javascript
    const response = await fetch("/data/z-mount-lenses.full.json");

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const dataset = await response.json();
    const firstProduct = dataset.products[0];
    const manufacturerId = firstProduct.identity.manufacturerId;
    const brandId = firstProduct.identity.brandId;
    const output = {
      dataVersion: dataset.dataVersion,
      recordCount: dataset.recordCount,
      firstProduct: {
        id: firstProduct.id,
        productType: firstProduct.productType,
        identity: {
          manufacturerId,
          manufacturerName: dataset.referenceData.manufacturers[manufacturerId].name,
          brandId,
          brandName: dataset.referenceData.brands[brandId].name,
          productName: firstProduct.identity.productName,
        },
      },
    };

    console.log(JSON.stringify(output, null, 2));
    ```

=== "Python"

    This example reads a downloaded distribution using the Python standard library.

    ```python
    import json
    from pathlib import Path

    path = Path("z-mount-lenses.full.json")
    with path.open(encoding="utf-8") as file:
        dataset = json.load(file)

    first_product = dataset["products"][0]
    manufacturer_id = first_product["identity"]["manufacturerId"]
    brand_id = first_product["identity"]["brandId"]
    output = {
        "dataVersion": dataset["dataVersion"],
        "recordCount": dataset["recordCount"],
        "firstProduct": {
            "id": first_product["id"],
            "productType": first_product["productType"],
            "identity": {
                "manufacturerId": manufacturer_id,
                "manufacturerName": dataset["referenceData"]["manufacturers"][manufacturer_id]["name"],
                "brandId": brand_id,
                "brandName": dataset["referenceData"]["brands"][brand_id]["name"],
                "productName": first_product["identity"]["productName"],
            },
        },
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    ```

### Actual output

For Lens Full data version `2026.10.09`, both examples print:

```json
{
  "dataVersion": "2026.10.09",
  "recordCount": 611,
  "firstProduct": {
    "id": "7artisans-24mm-f1-4",
    "productType": "lens",
    "identity": {
      "manufacturerId": "7artisans",
      "manufacturerName": "7Artisans",
      "brandId": "7artisans",
      "brandName": "7Artisans",
      "productName": "7Artisans 24mm F1.4"
    }
  }
}
```

`dataVersion` and `recordCount` are root metadata fields in the distribution.
`firstProduct` collects the fields used in this example from `products[0]`, the first included product.
The examples read manufacturer and brand IDs from the product and resolve their display names through `referenceData` in the same distribution JSON.

### Root product arrays

| Distribution | Root array containing included products |
| --- | --- |
| Lens Full | `products` |
| Lens Light | `products` |
| Mount adapter Full | `adapters` |

To read Mount adapter Full, change the file to `z-mount-adapters.full.json` and read `adapters` instead of `products`.
The root product-array names differ, but the metadata fields described below are shared by all three distributions.

### Search for matching lenses

This Python example searches the Lens Full data loaded above for autofocus lenses whose maximum image format is `full-frame`, then prints their product IDs and names.

```python
matches = {
    product["id"]: product["identity"]["productName"]
    for product in dataset["products"]
    if product["productType"] == "lens"
    and (coverage := product["lens"]["coverage"]) is not None
    and coverage["format"] == "full-frame"
    and (autofocus := product["lens"]["focus"]["autofocus"]) is not None
    and autofocus["present"] is True
}

print(json.dumps(matches, ensure_ascii=False, indent=2))
```

A `null` `coverage` or `autofocus` value means that accepted published evidence did not establish the value, so the example does not treat it as a match.
An `autofocus.present` value of `false` is also excluded because it confirms that autofocus is not supported.
An omitted field, `null`, an empty array, and `false` have different meanings.
Before testing or displaying values, see [Reading value states](value-rules.md#value-states).

!!! info "This is enough for basic use"
    Refer to the remaining sections when you need to check for distribution updates or validate data with JSON Schema.

## Include the namespace when storing product IDs {#product-keys}

Use a composite key made from the distribution namespace and `id` to identify a product uniquely.

| Distribution file | Namespace | Composite key |
| --- | --- | --- |
| `z-mount-lenses.full.json` | `lenses` | `("lenses", id)` |
| `z-mount-lenses.light.json` | `lenses` | `("lenses", id)` |
| `z-mount-adapters.full.json` | `adapters` | `("adapters", id)` |

Lens Full and Light share the `lenses` namespace.
An `id` is unique within a namespace.
The same `id` may be used in the `lenses` and `adapters` namespaces.
When importing multiple distributions into one database, do not use `id` alone as the primary key.
Store the namespace as well.

There is no new JSON field for the namespace.
Determine it from the distribution file type.

An `id` is a human-readable slug based on the brand and product name, using lowercase letters and numbers separated by hyphens.
However, the relationship between words in the slug and product information is not part of the public data contract.
Do not parse the brand, manufacturer, product name, focal length, f-number, generation, product type, or other facts from `id`.
Use `identity` and the applicable dedicated fields for display, search, and classification.

After this project first publishes a composite key in a GitHub Release, that key does not change.
A published `id` is not assigned to another product or reused after removal.
If the same product is included again, it uses its previous `id`.
This does not guarantee that the product will remain in the latest or every later release.
If products are merged, split, removed, or reclassified between datasets, check the release notes for the previous composite key and its replacement, or confirmation that there is no replacement.

`manufacturerId`, `brandId`, and mount-system IDs also remain fixed after first publication.
When a name changes, the `name` in `referenceData` changes without renaming or reusing the published ID.

## Check root metadata {#root-metadata}

Each distribution root includes metadata such as versions, record count, content hash, and license.
The project as a whole is named "Z Mount Product Database," while `datasetName` contains the name of the individual dataset.
The following examples omit `referenceData` and `products` or `adapters` and show the other root fields from each distribution at data version `2026.10.09`.

=== "Lens Full"

    ```json
    {
      "$schema": "https://cercidiphyllum.jp/schemas/1.0.0/lenses/dataset-full.schema.json",
      "datasetName": "Z Mount Lens Database",
      "datasetVariant": "full",
      "schemaVersion": "1.0.0",
      "dataVersion": "2026.10.09",
      "creator": "Katsura Iwamoto",
      "license": "CC-BY-4.0",
      "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
      "repositoryUrl": "https://github.com/KatsuraIwamoto/z-mount-product-database",
      "recordCount": 611,
      "contentHash": "sha256:484f0751db150132ce33d3aae7c31f75e5b7a2386c21211432c1051a3f8a50fd"
    }
    ```

=== "Lens Light"

    ```json
    {
      "$schema": "https://cercidiphyllum.jp/schemas/1.0.0/lenses/dataset-light.schema.json",
      "datasetName": "Z Mount Lens Database",
      "datasetVariant": "light",
      "schemaVersion": "1.0.0",
      "dataVersion": "2026.10.09",
      "creator": "Katsura Iwamoto",
      "license": "CC-BY-4.0",
      "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
      "repositoryUrl": "https://github.com/KatsuraIwamoto/z-mount-product-database",
      "recordCount": 611,
      "contentHash": "sha256:d8acf1c6a99bdeb312cafd14ab2bf55add586e044dd9418a6c1806bc0a2f3c06"
    }
    ```

=== "Mount adapter Full"

    ```json
    {
      "$schema": "https://cercidiphyllum.jp/schemas/1.0.0/adapters/dataset-full.schema.json",
      "datasetName": "Z Mount Adapter Database",
      "datasetVariant": "full",
      "schemaVersion": "1.0.0",
      "dataVersion": "2026.10.09",
      "creator": "Katsura Iwamoto",
      "license": "CC-BY-4.0",
      "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
      "repositoryUrl": "https://github.com/KatsuraIwamoto/z-mount-product-database",
      "recordCount": 447,
      "contentHash": "sha256:84a64958d2fc3aa73642e7a907bba516c8b94883768166de7c5e874c7fda1a32"
    }
    ```

`dataVersion`, `recordCount`, and `contentHash` are the values at the time these examples were created.
Check the distribution you obtain for the values you should use.

| Field | What it tells you |
| --- | --- |
| `$schema` | URL of the JSON Schema used to validate this distribution. |
| `datasetName` | Name of the dataset contained in the distribution. |
| `datasetVariant` | Whether this is Full or Light. The value is `full` or `light`. |
| `schemaVersion` | Version of the corresponding JSON Schema set, in SemVer format. |
| `dataVersion` | This project's data release identifier, in `YYYY.MM.DD` form. The Git tag uses the same value. |
| `creator` | Creator of the distribution. |
| `license`, `licenseUrl` | SPDX identifier and URL for the license applied to the distribution. |
| `repositoryUrl` | URL of the repository that maintains the distribution. |
| `recordCount` | Number of included products in `products` or `adapters`. |
| `referenceData` | Maps manufacturer, brand, and mount-system IDs referenced by products to display metadata. |
| `contentHash` | SHA-256 hash used to compare distribution contents. It is calculated by canonicalizing a content object containing `referenceData` and `products` or `adapters` according to [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785). |

`contentHash` is calculated from the UTF-8 bytes produced by RFC 8785 canonicalization and is written as `sha256:` followed by 64 lowercase hexadecimal digits.
Root metadata such as `$schema`, `schemaVersion`, `dataVersion`, and `recordCount`, along with whitespace and line endings in the complete distribution JSON, are outside the hash input.
Numbers included in the hash input must satisfy the I-JSON requirements assumed by RFC 8785.
This value compares the contents of the reference data and product array.
It does not authenticate the publisher or guarantee that the complete GitHub Release attachment has remained unchanged since publication.

Compare `dataVersion` to check for an update, and compare `contentHash` to check whether the contents are identical.

## Check compatibility when schemas change {#schema-versioning}

The three distributions share the same `schemaVersion`, but the lens dataset and mount adapter dataset use different JSON Schemas.
For validation, use the URL given in the distribution's `$schema`.

Published versioned JSON Schema URLs and their contents do not change.
When schema structure or constraints change, `schemaVersion` is updated and earlier versions remain available.
When only the included content changes, `dataVersion` is updated without changing `schemaVersion`.

| Type of change | `schemaVersion` increment |
| --- | --- |
| A JSON Schema correction that does not change validation results, distribution output, or value meanings | `patch` |
| An independent JSON Schema or distribution format that does not change an existing format, or a deprecation that keeps an existing field valid | `minor` |
| A change to an existing JSON Schema's validation results, distribution-output guarantees, or value meanings, including field or enum additions and weaker or stronger constraints | `major` |

Compatibility is determined by whether an existing program can process data from the new GitHub Release.
A known distribution format remains acceptable within the same `major` version.
However, always validate a distribution with the version specified by its own `$schema`, not an older JSON Schema.
Even when `schemaVersion` stays the same, a `dataVersion` update may add, remove, or correct products, change array positions, or use an already permitted value for the first time.

When the schema version changes, check the release notes before migrating.
See the [field reference for lenses and related optical products](lens-field-reference.md) or [mount adapter field reference](adapter-field-reference.md) for field meanings.
See the [JSON Schema reference](reference/schemas/index.md) for exact types and constraints.

## Validate with JSON Schema before updating {#validate-data}

In a production workflow, do not overwrite the current file with a newly obtained file.
Validate the new file separately, then switch to it.
The following Lens Full example replaces the current file only after validation against the JSON Schema named by the distribution's `$schema` and successful checks of `recordCount` and `contentHash`.
If download, JSON parsing, validation, or comparison fails, it leaves the previous file in place.

First, choose one GitHub Release to validate.
Replace every `YYYY.MM.DD` below with that Release's `dataVersion`, and run the commands in an empty working directory.
These commands obtain the complete JSON Schema set from the Git tag that matches the distribution.

```shell
git clone --depth 1 --branch YYYY.MM.DD --single-branch \
  https://github.com/KatsuraIwamoto/z-mount-product-database.git \
  schema-source-YYYY.MM.DD
git -C schema-source-YYYY.MM.DD describe --tags --exact-match
cp -R schema-source-YYYY.MM.DD/schemas ./schemas
```

Use the copied `schemas/` only if the `git describe` output matches the selected `YYYY.MM.DD`.
This tag matches the distribution's `dataVersion` and is not moved after publication.
`schemas/` contains the JSON Schemas used to validate the distribution and every dependency they reference through `$ref`, preserving the required directory structure.
When moving to another version, use a fresh working directory or replace the complete `schemas/` directory with the matching tag's contents.
Do not mix files from different tags.

Install the validation libraries first.

```shell
python -m pip install "jsonschema>=4.23,<5" "referencing>=0.28.4,<1" "rfc3986-validator>=0.1.1,<1" "rfc8785>=0.1.4,<1"
```

After storing the complete matching JSON Schema set under `schemas/`, run this code.
It stops the update when it finds an unknown `$schema` instead of retrieving that schema automatically.
It also rejects duplicate object keys and the values `NaN`, `Infinity`, and `-Infinity` while parsing JSON.
The example installs `rfc3986-validator` and passes an explicit `FormatChecker` so that Draft 2020-12 `format` values are checked as URIs.

```python
import json
from hashlib import sha256
from pathlib import Path
from urllib.request import urlopen

import rfc8785
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


def object_without_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def reject_nonfinite_number(value):
    raise ValueError(f"non-finite JSON number: {value}")


expected_data_version = "YYYY.MM.DD"
data_url = (
    "https://github.com/KatsuraIwamoto/z-mount-product-database/"
    f"releases/download/{expected_data_version}/z-mount-lenses.full.json"
)
current_path = Path("current/z-mount-lenses.full.json")

schemas = {}
resources = []
for path in Path("schemas").rglob("*.schema.json"):
    schema = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=object_without_duplicate_keys,
        parse_constant=reject_nonfinite_number,
    )
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError(f"unsupported schema dialect: {path}")
    Draft202012Validator.check_schema(schema)
    if isinstance(schema.get("$id"), str):
        schemas[schema["$id"]] = schema
        resources.append((schema["$id"], Resource.from_contents(schema)))

with urlopen(data_url, timeout=30) as response:
    raw = response.read()
candidate = json.loads(
    raw,
    object_pairs_hook=object_without_duplicate_keys,
    parse_constant=reject_nonfinite_number,
)

if not isinstance(candidate, dict):
    raise ValueError("distribution root must be an object")
if candidate.get("dataVersion") != expected_data_version:
    raise ValueError("unexpected dataVersion")
if (candidate.get("datasetName"), candidate.get("datasetVariant")) != (
    "Z Mount Lens Database",
    "full",
):
    raise ValueError("unexpected distribution")

schema_url = candidate.get("$schema")
if not isinstance(schema_url, str) or schema_url not in schemas:
    raise ValueError(f"unsupported schema: {schema_url}")

Draft202012Validator(
    schemas[schema_url],
    registry=Registry().with_resources(resources),
    format_checker=FormatChecker(),
).validate(candidate)

products = candidate["products"]
if candidate["recordCount"] != len(products):
    raise ValueError("recordCount does not match products")
hash_payload = {
    "referenceData": candidate["referenceData"],
    "products": products,
}
actual_hash = "sha256:" + sha256(rfc8785.dumps(hash_payload)).hexdigest()
if candidate["contentHash"] != actual_hash:
    raise ValueError("contentHash does not match products")

current_path.parent.mkdir(parents=True, exist_ok=True)
staged_path = current_path.with_name(f".{current_path.name}.tmp")
staged_path.write_bytes(raw)
staged_path.replace(current_path)
```

The temporary file is created in the same directory as the current file, and only the final `replace()` switches the files.
Set `expected_data_version` to the same value as the Git tag used for the JSON Schema set.
When updating to a new Release, change the version-pinned distribution URL and the JSON Schema tag together.
This `contentHash` check tests the internal consistency of the reference data and product array.
It does not authenticate the publisher.

## Show attribution when sharing data {#attribution}

Canonical product data, research results, the three distribution JSON files, and `PRODUCTS.md` are available under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The recommended attribution is:

> Z Mount Product Database, Katsura Iwamoto, CC BY 4.0, https://github.com/KatsuraIwamoto/z-mount-product-database

If you share modified data, also state that you made changes.
This section summarizes the main points and does not cover every condition.
See [Licensing](license.md) for the exact scope, warranty disclaimer, third-party rights notice, and links to the formal license texts.

## Report an error or missing product {#report-data-issues}

Use the [product correction and addition form](https://github.com/KatsuraIwamoto/z-mount-product-database/issues/new?template=data-correction.yml) to report the product name, what you noticed, and an official URL from the manufacturer or brand if available.
You do not need to write JSON or JSON Schema.
