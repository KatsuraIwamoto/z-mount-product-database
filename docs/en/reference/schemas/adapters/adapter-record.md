# adapter-record.schema.json

Validates one canonical mount adapter record stored at `data/records/adapters/<brand-id>/<adapter-id>.json`.
The product structure follows [adapter-full](adapter-full.md) and adds only the required `$schema` declaration for the editable JSON file.

## Addition to adapter-full

| Path | Type/value | Meaning |
| --- | --- | --- |
| `$schema` | `"../../../../schemas/adapters/adapter-record.schema.json"` | Fixed relative path to the JSON Schema that validates the canonical record |

All remaining fields are defined in the [top-level fields of adapter-full](adapter-full.md#top-level-fields) and the [adapter-components](adapter-components.md) definitions referenced from them.

## File placement and ID

Repository validation checks the following rules, which cannot be expressed by JSON Schema alone.

| Check | Rule |
| --- | --- |
| File name | `<id>.json` |
| Parent directory | Same brand ID as `identity.brandId` |
| Research result | For an included product, the result ID, `decision.recordId`, and product ID match |

When the distribution data is generated, only `$schema` is removed from each canonical record.

Source file: `data/records/adapters/nikon/mount-adapter-ftz-ii.json`

Referenced field: `$schema`

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/adapters/adapter-record.schema.json)
