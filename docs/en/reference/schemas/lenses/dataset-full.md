# lenses/dataset-full.schema.json

This schema validates the complete Lens Full distribution generated at `dist/z-mount-lenses.full.json`.
It connects the distribution metadata at the root with the `products` array, whose entries follow [product-full](product-full.md).

## Root fields

All of the following fields are required.

| Path | Type/value | Description |
| --- | --- | --- |
| `$schema` | fixed URI | Versioned public URL of this schema |
| `datasetName` | `"Z Mount Lens Database"` | Fixed name of the lens distribution |
| `datasetVariant` | `"full"` | Fixed value identifying the Full distribution |
| `schemaVersion` | `"1.0.0"` | Version shared by the complete JSON Schema set |
| `dataVersion` | string in `YYYY.MM.DD` format | Data release identifier. The Git tag uses the same value |
| `creator` | string | Creator of the distribution |
| `license` | `"CC-BY-4.0"` | SPDX license identifier applied to the distribution |
| `licenseUrl` | HTTP(S) URL | Canonical URL for CC BY 4.0 |
| `repositoryUrl` | HTTP(S) URL | Public repository containing the canonical records, JSON Schemas, licensing information, issues, and release history |
| `recordCount` | nonnegative integer | Number of products in `products` |
| `contentHash` | `sha256:<64 lowercase hexadecimal digits>` | SHA-256 of a content object containing `referenceData` and `products` |
| `referenceData` | [reference-data](../shared/reference-data.md) | IDs referenced by this distribution and their display metadata |
| `products` | [product-full](product-full.md)[] | Product array generated from all canonical records. Individual entries do not contain `$schema` |

`datasetName` is a fixed value in the distribution and differs from the project name, "Z Mount Product Database."

!!! info "Validation outside JSON Schema"

    The generation process sets `recordCount` from the number of entries in `products`.
    `hatch run validate` confirms that the generated file matches the result of rebuilding the distribution.
    The JSON Schema also rejects `$schema` within an individual `products[]` entry.
    `contentHash` is calculated from the UTF-8 bytes of an object containing `referenceData` and `products` after RFC 8785 canonicalization.

!!! warning "Do not edit generated files directly"

    To change the contents, edit the corresponding canonical record or the generation process.

## Related pages

- [product-full](product-full.md): one product in `products[]`
- [Using the distribution data](../../../use-data.md): how to obtain the Full distribution and check its metadata
- [Data model](../../../data-model.md): how distribution data is generated from canonical records

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/dataset-full.schema.json)
