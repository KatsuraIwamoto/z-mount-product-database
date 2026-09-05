# product-full.schema.json

This schema validates one product in the Lens Full `products[]` array.
It combines common fields such as identity and physical characteristics with exactly one specification block corresponding to the product type.

## Top-level fields {#top-level-fields}

`id`, `productType`, `identity`, `lifecycle`, `officialProductPages`, `mount`, `physical`, `controls`, and `accessories` are required for every product.
`$schema`, `electronicServices`, and the specification blocks for each product type have the additional conditions described in the next section.

| Path | Type/value | Description |
| --- | --- | --- |
| `$schema` | string | Reference to a JSON Schema. [product-record](product-record.md) requires it in canonical records, and generation removes it from distribution data |
| `id` | ID string | ID unique within the `lenses` namespace. Uses a human-readable slug format with lowercase letters and digits separated by hyphens. Do not parse product information from the string. Used in filenames, research results, and cross-product references |
| `productType` | `lens` / `teleconverter` / `pinhole` | Value that selects the product-type block to use |
| `identity` | [identity](product-components.md#identity) | Manufacturer ID, brand ID, product name, model numbers, alternate names, and variants |
| `lifecycle` | [lifecycle](product-components.md#lifecycle) | Product release announcement date and status designations from the manufacturer or brand |
| `officialProductPages` | [officialProductPage](product-components.md#officialproductpage)[] | Official main pages for the product itself. Use `[]` when no eligible page remains |
| `mount` | [mount](product-components.md#mount) | Connection to Nikon Z mount and electronic contacts |
| `physical` | [physical](product-components.md#physical) | Dimensions, weight, protection claims, filters, and tripod support |
| `controls` | [control](product-components.md#control)[] or `null` | Controls such as rings, switches, and buttons |
| `accessories` | [accessories](product-components.md#accessories) or `null` | Supplied or separately sold accessories |
| `electronicServices` | [electronicServices](../shared/shared-definitions.md#electronic-data) or `null` | Connections used for firmware updates, configuration, and control |
| `lens` | [lens](product-type-lens.md) | Lens specification block |
| `teleconverter` | [teleconverter](product-type-teleconverter.md) | Teleconverter specification block |
| `pinhole` | [pinhole](product-type-pinhole.md) | Specification block for pinholes and related imaging modes |

## Product types and specification blocks

Only the block corresponding to `productType` is required and permitted.

| `productType` | Required block | Prohibited blocks |
| --- | --- | --- |
| `lens` | `lens` | `teleconverter`, `pinhole` |
| `teleconverter` | `teleconverter` | `lens`, `pinhole` |
| `pinhole` | `pinhole` | `lens`, `teleconverter` |

## Electronic contacts and product-side connection services {#electronic-services-condition}

`electronicServices` records product connections used for firmware updates, configuration, or control, rather than functions carried through the mount contacts.

| `mount.electronicContacts` | `electronicServices` |
| --- | --- |
| `{ "present": true, ... }` | Required. `null` is also permitted when accepted published evidence is unavailable |
| `{ "present": false }` | May be omitted; may be recorded when an independent USB connection, dock, or similar service is published |
| `null` | May be omitted; may be recorded when a connection service is established |

The absence of mount contacts does not by itself establish the absence of an independent connection service.
However, when `electronicServices.connections[].method` is `camera-body`, communication uses the camera mount contacts, so `mount.electronicContacts.present` must be `true`.
This condition does not apply to `direct-usb` or `dock`.

## External-length behavior for lenses

For `productType: "lens"`, applicable external-behavior fields are not omitted; use `null` when accepted published evidence does not establish a value.

| Condition | Rule under `physical` |
| --- | --- |
| Every lens | `externalLengthDuringFocus` and `isRetractableForStorage` are required |
| `lens.focalLength.kind: "zoom"` | `externalLengthDuringZoom` is required |
| `lens.focalLength.kind: "prime"` | `externalLengthDuringZoom` is prohibited |
| `lens.focus.opticalFocusingSystems[].type: "internal-focusing"` or `"rear-focusing"` | `externalLengthDuringFocus` is `"constant"` |
| `lens.zoom.opticalZoomingSystems[].type: "internal-zooming"` | `externalLengthDuringZoom` is required and is `"constant"` |

`constant` means that operation does not change external length, while `variable` means that it does.
`null` means that accepted published evidence does not establish the behavior.

See [Reading data values](../../../value-rules.md) for the meanings of omission, `null`, an empty array, and `false`.

## Related pages

- [product-record](product-record.md): the `$schema` field and placement rules added to canonical records
- [product-components](product-components.md): blocks shared by all product types
- [Field reference for lenses and related optical products](../../../lens-field-reference.md): field explanations based on actual data

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/product-full.schema.json)
