# dataset-light.schema.json

This schema validates the complete Lens Light distribution generated at `dist/z-mount-lenses.light.json`.
The distribution metadata at the root uses the same structure as Lens Full, and each entry in `products` follows [product-light](product-light.md).

## Relationship to Lens Full

| Check | Lens Light rule |
| --- | --- |
| Product count, order, and IDs | Match Lens Full |
| Product structure | Fields may be omitted from the corresponding Lens Full product, including from nested objects, but array order is preserved |
| Retained values | Values and their types are unchanged from Lens Full |
| Arrays | Preserve their original order. The projection retains only the exact Lens Full entries selected by the schema for minimum focus distance and maximum reproduction ratio, without changing their values |
| Reference data | Identical to Lens Full `referenceData` |
| Content hash | Calculated from `referenceData` and the Lens Light `products` array |

JSON Schema validates the structures permitted in Lens Light.
The generation process creates Lens Light from the same input as Lens Full.
`hatch run validate` also checks that values, product count, and product order correspond to Lens Full.

## Root fields

All of the following fields are required.

| Path | Type/value | Description |
| --- | --- | --- |
| `$schema` | fixed URI | Versioned public URL of this schema |
| `datasetName` | `"Z Mount Lens Database"` | Fixed name of the lens distribution |
| `datasetVariant` | `"light"` | Fixed value identifying the Light distribution |
| `schemaVersion` | `"1.0.0"` | Version shared by the complete JSON Schema set |
| `dataVersion` | string in `YYYY.MM.DD` format | Data release identifier shared with Lens Full. The Git tag uses the same value |
| `creator` | string | Creator of the distribution |
| `license` | `"CC-BY-4.0"` | SPDX license identifier applied to the distribution |
| `licenseUrl` | HTTP(S) URL | Canonical URL for CC BY 4.0 |
| `repositoryUrl` | HTTP(S) URL | Public repository containing the canonical records, JSON Schemas, licensing information, issues, and release history |
| `recordCount` | nonnegative integer | Number of products in `products`. Matches Lens Full |
| `contentHash` | `sha256:<64 lowercase hexadecimal digits>` | SHA-256 of a content object containing `referenceData` and the Lens Light `products` array |
| `referenceData` | [reference-data](../shared/reference-data.md) | Same IDs and display metadata as Lens Full |
| `products` | [product-light](product-light.md)[] | Lightweight product array that preserves the product order from Lens Full |

`datasetName` is a fixed value shared with Lens Full in the distribution and differs from the project name, "Z Mount Product Database."

!!! warning "Do not edit generated files directly"

    Lens Light is generated from canonical records and the generation rules.
    When changing the retained fields, also confirm compatibility with the existing website display.

## Related pages

- [product-light](product-light.md): one product in `products[]`
- [dataset-full](dataset-full.md): corresponding root structure of Lens Full
- [Reading data values](../../../value-rules.md): how values are handled in Lens Full and Lens Light

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/dataset-light.schema.json)
