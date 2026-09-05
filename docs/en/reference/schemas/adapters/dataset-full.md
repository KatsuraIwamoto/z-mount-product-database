# adapters/dataset-full.schema.json

Validates the complete Full distribution for mount adapters generated at `dist/z-mount-adapters.full.json`.
This schema combines distribution metadata at the root with an `adapters` array whose entries follow [adapter-full](adapter-full.md).

## Root fields

All fields below are required.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `$schema` | fixed URI | Published versioned URL of this schema |
| `datasetName` | `"Z Mount Adapter Database"` | Fixed name of the mount adapter distribution data |
| `datasetVariant` | `"full"` | Fixed value identifying the Full edition |
| `schemaVersion` | `"1.0.0"` | Version shared by the JSON Schema bundle |
| `dataVersion` | string in `YYYY.MM.DD` format | Data release identifier. The Git tag uses the same value |
| `creator` | string | Creator of the distribution data |
| `license` | `"CC-BY-4.0"` | SPDX license identifier applied to the distribution data |
| `licenseUrl` | HTTP(S) URL | Canonical URL for CC BY 4.0 |
| `repositoryUrl` | HTTP(S) URL | Public repository containing canonical records, JSON Schemas, licensing information, issues, and release history |
| `recordCount` | non-negative integer | Number of products in `adapters` |
| `contentHash` | `sha256:<64 lowercase hexadecimal digits>` | SHA-256 of a content object containing `referenceData` and `adapters` |
| `referenceData` | [reference-data](../shared/reference-data.md) | IDs referenced by this distribution and their display metadata |
| `adapters` | [adapter-full](adapter-full.md)[] | Product array generated from all canonical mount adapter records. Individual entries do not contain `$schema` |

`datasetName` is a fixed value within the distribution data and differs from the project name Z Mount Product Database.

!!! info "Validation beyond JSON Schema"

    The generation process sets `recordCount` from the number of elements in `adapters`.
    `hatch run validate` verifies that the generated file matches the result of rebuilding the distribution data.
    The JSON Schema also rejects `$schema` within an individual `adapters[]` entry.
    `contentHash` is calculated from the UTF-8 bytes of an object containing `referenceData` and `adapters` after RFC 8785 canonicalization.
    The generation process sorts `adapters` in ascending lexicographic order by each element's `id` string.
    Adding or removing a product can change the array positions of existing products between data versions.

!!! warning "Do not edit generated files directly"

    To change the contents, edit the corresponding canonical records or the generation process.

## Related pages

- [adapter-full](adapter-full.md): One product in `adapters[]`
- [Using the distribution data](../../../use-data.md): How to obtain the Full edition and inspect its metadata
- [Data model](../../../data-model.md): How distribution data is generated from canonical records

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/adapters/dataset-full.schema.json)
