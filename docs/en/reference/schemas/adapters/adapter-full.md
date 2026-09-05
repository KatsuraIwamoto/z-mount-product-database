# adapter-full.schema.json

Validates one product in the `adapters[]` array of the Full mount adapter distribution.
Every product uses the same top-level structure.
It records the source and destination mount pair, together with the product's functions and physical characteristics.

This schema is independent of the JSON Schemas for lenses and related optical products, so it does not use `productType` or a product-type block.

## Top-level fields {#top-level-fields}

The ten fields `id`, `identity`, `lifecycle`, `officialProductPages`, `mountConfigurations`, `electronics`, `electronicServices`, `conversionOptics`, `mechanisms`, and `physical` are required.
For canonical records, [adapter-record](adapter-record.md) makes `$schema` required. The field is removed when the distribution data is generated.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `$schema` | string | Reference to the JSON Schema. Used only in canonical records |
| `id` | ID string | ID unique within the `adapters` namespace. Uses a human-readable slug of lowercase ASCII letters and digits separated by hyphens. Do not derive product information from the string. Used to match the file name and research result |
| `identity` | [identity](adapter-components.md#identity) | Manufacturer ID, brand ID, product name, model numbers, alternate names, and variants |
| `lifecycle` | [lifecycle](adapter-components.md#lifecycle) | Product release announcement date and official designations from the manufacturer or brand |
| `officialProductPages` | [officialProductPage](adapter-components.md#officialproductpage)[] | Main official landing pages for the exact product. Use `[]` when no eligible page remains |
| `mountConfigurations` | [mountConfiguration](adapter-components.md#mountconfiguration)[] | Combinations of the source lens-side mount and the Nikon Z mount. At least one entry |
| `electronics` | [electronics](adapter-components.md#electronics) or `null` | Electronic functions available through the adapter |
| `electronicServices` | [electronicServices](../shared/shared-definitions.md#electronic-data) or `null` | Published firmware-update status and connections used for updates, configuration, or control |
| `conversionOptics` | [conversionOptics](adapter-components.md#conversionoptics) or `null` | Presence of conversion optics and their effects on focal length and maximum aperture |
| `mechanisms` | [mechanisms](adapter-components.md#mechanisms) or `null` | Confirmed additional mechanisms |
| `physical` | [physical](adapter-components.md#physical) | Dimensions, weight, environmental-protection claims, and tripod support |

Do not omit `electronics`, `electronicServices`, `conversionOptics`, or `mechanisms` when no details have been confirmed.
When `electronicServices.connections[].method` is `camera-body`, `electronics.electronicContacts` must be `true`.
This condition does not apply to an independent `direct-usb` or `dock` connection.
Shift, tilt, and rotation measurements are nested in the `movements` field of the corresponding `mechanisms[]` item.
This keeps the mechanism type, its conditions, and its measurements in one object.
`null` for an applicable value that cannot be confirmed from accepted published evidence, `[]` for a checked collection with no applicable entries, and `false` for a confirmed negative each have a different meaning.
See [Value-state rules](../../../value-rules.md) for details.

!!! info "Mount adapters have only a Full edition"

    There is no Light edition for mount adapters.
    In the distribution data, only `$schema` is removed from each canonical record.

## Related pages

- [adapter-record](adapter-record.md): The `$schema` declaration and file-placement rules added to canonical records
- [adapter-components](adapter-components.md): Definitions referenced by each top-level field
- [Mount adapter field reference](../../../adapter-field-reference.md): Field descriptions using actual data

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/adapters/adapter-full.schema.json)
