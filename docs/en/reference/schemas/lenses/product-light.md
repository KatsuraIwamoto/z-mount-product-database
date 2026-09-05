# product-light.schema.json

This schema validates one product in `products[]` in the Lens Light dataset.
It uses the same top-level block names as the Full dataset and retains only the fields needed by the existing web display.

## Generation rules from Full

| Item checked | Rule for Light |
| --- | --- |
| Products | Retains every product from Full in the same order |
| Top-level fields | Does not change `id` in the `lenses` namespace, `productType`, or the product-type block name |
| Objects | May omit properties that are not needed |
| Values | Does not change any retained value or its type from Full |
| Arrays | Preserves source order and element count. Only the minimum-focus-distance and maximum-reproduction-ratio arrays may be reduced; the projection keeps the selected Full entries unchanged according to the rules below |

Light does not add values of its own or calculate new ranges or representative values.
The JSON Schema validates the structures permitted in Light.
`hatch run validate` also checks the relationship to Full.

!!! warning "Light is generated"

    Do not edit `dist/z-mount-lenses.light.json` directly.
    If you change the retained fields, also check compatibility with the existing web display.

## Full and Light examples

The following example uses `lens.aperture` from the NIKKOR Z 24-70mm f/2.8 S II to show how Light reduces the structure while preserving the same values.
Each code block is actual data containing only `lens.aperture` from the corresponding product.

=== "Full"

    Source: `dist/z-mount-lenses.full.json`

    Excerpt: `lens.aperture` from product ID `nikkor-z-24-to-70mm-f2p8-s-ii`

    ```json
    {
      "fNumber": {
        "maximumAperture": [
          {
            "value": 2.8,
            "conditions": {}
          }
        ],
        "minimumAperture": [
          {
            "value": 22,
            "conditions": {}
          }
        ],
        "effective": null
      },
      "diaphragm": {
        "present": true,
        "bladeCount": 11,
        "bladeShape": "rounded"
      },
      "controlMechanism": "electronic"
    }
    ```

=== "Light"

    Source: `dist/z-mount-lenses.light.json`

    Excerpt: `lens.aperture` from product ID `nikkor-z-24-to-70mm-f2p8-s-ii`

    ```json
    {
      "fNumber": {
        "maximumAperture": [
          {
            "value": 2.8,
            "conditions": {}
          }
        ]
      }
    }
    ```

Light retains the maximum aperture of `2.8` and its measurement conditions unchanged, while omitting the minimum aperture, diaphragm mechanism, and control mechanism.

## Top-level fields

All seven common fields from `id` through `physical` are required.
In addition, the product contains exactly one `lens`, `teleconverter`, or `pinhole` block matching `productType`; the other two blocks are not permitted.

| Path | Type/value | Description |
| --- | --- | --- |
| `id` | ID string | Slug-format ID shared with Full in the `lenses` namespace. Do not parse product information from this string |
| `productType` | `lens` / `teleconverter` / `pinhole` | Same product type as Full |
| `identity` | object | Manufacturer ID, brand ID, and product name |
| `lifecycle` | [lifecycle](product-components.md#lifecycle) | Same product release announcement date and official status wording as Full |
| `officialProductPages` | object[] | Array retaining only the URL of each official product page |
| `mount` | [mount](product-components.md#mount) | Same mount structure as Full, including official adapter information |
| `physical` | object | Dimensions, weight, and filter attachment methods |
| `lens` | object | Light lens specifications present when `productType: "lens"` |
| `teleconverter` | object | Light teleconverter specifications present when `productType: "teleconverter"` |
| `pinhole` | object | Light pinhole specifications present when `productType: "pinhole"` |

## Retained common fields

All three fields directly under `identity` are required, and every `officialProductPages[]` entry requires `url`.
All three fields directly under `physical` are also required. When `dimensionMeasurements` or `weightMeasurements` is an array, it must contain at least one entry.
A filter interface contains only the size field selected by `type`. When `sheetDimensionsMm` for `rear-gelatin` is an object, both `width` and `height` are required.

| Path | Type/value | Description |
| --- | --- | --- |
| `identity.manufacturerId` | ID string | Same manufacturer ID as Full |
| `identity.brandId` | ID string | Same brand ID as Full |
| `identity.productName` | string | Same official product name as Full |
| `officialProductPages[].url` | HTTP(S) URL | Each official product page URL from Full. Preserves array order and element count |
| `physical.dimensionMeasurements` | measurement[] or `null` | Dimensions and measurement conditions from Full |
| `physical.weightMeasurements` | measurement[] or `null` | Weights and measurement conditions from Full |
| `physical.filterInterfaces` | interface[] or `null` | Filter attachment methods and dimensions. Omits `host` from Full |
| `physical.filterInterfaces[].type` | `front-thread` / `rear-thread` / `drop-in` / `rear-gelatin` | Filter attachment method |
| `physical.filterInterfaces[].diameterMm` | positive number | Front or rear thread diameter in millimeters |
| `physical.filterInterfaces[].filterDiameterMm` | positive number | Drop-in filter diameter in millimeters |
| `physical.filterInterfaces[].sheetDimensionsMm` | object or `null` | Rear gelatin filter dimensions |
| `physical.filterInterfaces[].sheetDimensionsMm.width` | positive number | Rear gelatin filter width in millimeters |
| `physical.filterInterfaces[].sheetDimensionsMm.height` | positive number | Rear gelatin filter height in millimeters |

## Lens

The `lens` block retains an overview of the optical system and the presence information used by the web display.
The `lens` block requires `focalLength`, `aperture`, `coverage`, `focus`, `stabilization`, and `specialized`.
Within `aperture`, `fNumber` is required. An object-valued `fNumber` and any present `tNumber` require `maximumAperture`.
Each array-valued `maximumAperture`, `minimumFocusDistances`, or `reproductionMagnifications` must contain at least one entry.
The `focus` block requires `autofocus`, `manualFocus`, `minimumFocusDistances`, and `reproductionMagnifications`. When `autofocus`, `manualFocus`, or `stabilization` is an object, `present` is required.

| Path | Type/value | Description |
| --- | --- | --- |
| `lens.focalLength` | [focalLength](../shared/shared-definitions.md#focal-length-and-conditions) or `null` | Single focal length, zoom range, or interchangeable-component configuration from Full |
| `lens.aperture.fNumber` | object or `null` | Published maximum aperture expressed as an f-number |
| `lens.aperture.fNumber.maximumAperture` | f-number measurement[] or `null` | Nominal maximum-aperture f-number from Full |
| `lens.aperture.tNumber` | object | Nominal maximum aperture expressed as a T-stop for products to which T-stops apply |
| `lens.aperture.tNumber.maximumAperture` | T-stop measurement[] or `null` | Nominal maximum-aperture T-stop from Full |
| `lens.coverage` | [coverage](../shared/shared-definitions.md#basic-values) | Same largest image format as Full |
| `lens.focus.autofocus` | object or `null` | Confirmed autofocus status |
| `lens.focus.autofocus.present` | boolean | Presence or absence of autofocus confirmed in Full |
| `lens.focus.manualFocus` | object or `null` | Confirmed manual-focus status |
| `lens.focus.manualFocus.present` | boolean | Presence or absence of manual focus confirmed in Full |
| `lens.focus.minimumFocusDistances` | focus distance[] or `null` | Elements with the shortest `distanceM` in Full. Values remain unchanged, and all ties are retained in their original order |
| `lens.focus.reproductionMagnifications` | reproduction ratio[] or `null` | Elements with the highest reproduction ratio in Full. Values remain unchanged, and all ties are retained in their original order |
| `lens.stabilization` | object or `null` | Confirmed in-lens stabilization status |
| `lens.stabilization.present` | boolean | Presence or absence of in-lens stabilization confirmed in Full |
| `lens.specialized.<category>` | `{}` | Presence marker for any `cinema`, `anamorphic`, `fisheye`, `macro`, `reflex`, `movements`, `probe`, or `builtInTeleconverter` category present in Full |

## Teleconverter

All five fields in `teleconverter` are required.
When `compatibleLensIds` is an array, it must contain at least one ID and cannot contain duplicates.

| Path | Type/value | Description |
| --- | --- | --- |
| `teleconverter.coverage` | [coverage](../shared/shared-definitions.md#basic-values) | Same largest image format as Full |
| `teleconverter.magnification` | positive number | Same nominal magnification as Full |
| `teleconverter.apertureLossStops` | nonnegative number | Same aperture loss in stops as Full |
| `teleconverter.supportsAutofocus` | boolean or `null` | Same autofocus support with a compatible lens as Full |
| `teleconverter.compatibleLensIds` | ID[] or `null` | Same compatible lens IDs as Full |

## Pinhole

All three fields in `pinhole` are required.
When `imagingModes` is an array, it must contain at least one entry.

| Path | Type/value | Description |
| --- | --- | --- |
| `pinhole.coverage` | [coverage](../shared/shared-definitions.md#basic-values) | Same largest image format as Full |
| `pinhole.focalLength` | object or `null` | Same fixed focal length or variable range as Full |
| `pinhole.imagingModes` | mode[] or `null` | Same imaging modes, f-numbers, and aperture information as Full |

The Light pinhole specifications do not retain `pinhole.anglesOfView` from Full.

## Related pages

- [product-full](product-full.md): corresponding product structure in Full
- [dataset-light](dataset-light.md): Light distribution metadata
- [Lens and related optical product field reference](../../../lens-field-reference.md): comparison of actual Full and Light data

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/product-light.schema.json)
