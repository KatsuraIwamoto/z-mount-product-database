# product-record.schema.json

This schema validates one canonical record stored at `data/records/lenses/<brand-id>/<product-id>.json`.
It uses [product-full](product-full.md) for the product structure and adds only the `$schema` field required by the editable JSON file.

## Addition to product-full

| Path | Type/value | Description |
| --- | --- | --- |
| `$schema` | `"../../../../schemas/lenses/product-record.schema.json"` | Fixed relative path to the JSON Schema that validates a canonical record |

The remaining fields are defined by the [top-level fields in product-full](product-full.md#top-level-fields) and by the common and product-type schemas referenced from that page.

## File placement and ID

Repository validation checks the following rules that JSON Schema alone cannot express.

| Check | Rule |
| --- | --- |
| Filename | `<id>.json` |
| Parent directory | Same brand ID as `identity.brandId` |
| Research result | For an included product, the result ID, `decision.recordId`, and product ID match |

When generating distribution data, the process removes only `$schema` from each canonical record.

Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

Referenced field: `$schema`

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/product-record.schema.json)
