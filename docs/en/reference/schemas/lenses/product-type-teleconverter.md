# product-type-teleconverter.schema.json

This schema validates the `teleconverter` block of products with `productType: "teleconverter"`.
It covers teleconverters sold as standalone products that mount directly on the Nikon Z mount.

## Example `teleconverter` block

The following example uses the Z TELECONVERTER TC-1.4x to show the basic specifications and compatible lens IDs separately.

=== "Basic specifications"

    Source: `data/records/lenses/nikon/z-teleconverter-tc-1p4x.json`

    Excerpt: `teleconverter` (excluding `compatibleLensIds`)

    ```json
    {
      "coverage": {
        "format": "full-frame"
      },
      "magnification": 1.4,
      "apertureLossStops": 1,
      "supportsAutofocus": true,
      "opticalConstruction": {
        "groups": 4,
        "elements": 6
      },
      "specialElements": [
        {
          "types": [
            "aspherical"
          ],
          "officialName": "Aspherical lens",
          "quantity": 1
        }
      ],
      "coatings": [
        {
          "types": [
            "anti-reflective"
          ],
          "officialName": "Nikon Super Integrated Coating",
          "appliedTo": null
        },
        {
          "types": [
            "surface-protective"
          ],
          "officialName": "Fluorine coat",
          "appliedTo": [
            "front-element",
            "rear-element"
          ]
        }
      ]
    }
    ```

=== "Compatible lens IDs"

    Source: `data/records/lenses/nikon/z-teleconverter-tc-1p4x.json`

    Excerpt: `teleconverter.compatibleLensIds`

    ```json
    {
      "compatibleLensIds": [
        "nikkor-z-70-to-180mm-f2p8",
        "nikkor-z-70-to-200mm-f2p8-vr-s",
        "nikkor-z-70-to-200mm-f2p8-vr-s-ii",
        "nikkor-z-100-to-400mm-f4p5-to-5p6-vr-s",
        "nikkor-z-180-to-600mm-f5p6-to-6p3-vr",
        "nikkor-z-400mm-f2p8-tc-vr-s",
        "nikkor-z-400mm-f4p5-vr-s",
        "nikkor-z-600mm-f4-tc-vr-s",
        "nikkor-z-600mm-f6p3-vr-s",
        "nikkor-z-800mm-f6p3-vr-s"
      ]
    }
    ```

## Fields in the `teleconverter` block

All eight fields below are required.

| Path | Type/value | Description |
| --- | --- | --- |
| `teleconverter.coverage` | [coverage](../shared/shared-definitions.md#basic-values) | Largest supported image format |
| `teleconverter.magnification` | positive number | Nominal factor applied to focal length |
| `teleconverter.apertureLossStops` | nonnegative number | Loss of light in stops when the teleconverter is attached |
| `teleconverter.supportsAutofocus` | boolean or `null` | Autofocus support when a compatible lens is attached. This does not describe the teleconverter's own drive mechanism |
| `teleconverter.opticalConstruction` | [opticalConstruction](../shared/shared-definitions.md#opticalconstruction) or `null` | Number of groups and elements in the teleconverter itself |
| `teleconverter.specialElements` | [specialElement](../shared/shared-definitions.md#specialelement)[] or `null` | Special lens elements. Types and quantities may be recorded without a distinct official name. After checking the list, use `[]` if none apply |
| `teleconverter.coatings` | [coating](../shared/shared-definitions.md#coating)[] or `null` | Coatings. Types and application may be recorded without a distinct official name. After checking the list, use `[]` if none apply |
| `teleconverter.compatibleLensIds` | ID[] or `null` | IDs of canonical products in the `lenses` namespace with `productType: "lens"` that the manufacturer identifies as compatible. If known, the array contains at least one entry, with no duplicates |

`coverage` may be `null` when the largest supported image format is unknown.
Record the magnification and aperture loss as unitless numbers, such as `1.4` and `1`.

## Validating compatible lens IDs

Repository validation checks that every value in `compatibleLensIds` corresponds to a canonical product in the `lenses` namespace with `productType: "lens"`.
Using product IDs instead of free-text product names links each entry to the compatible lens in the distribution data.

## Related pages

- [product-full](product-full.md): how to combine the block with common fields
- [Shared definitions](../shared/shared-definitions.md): image formats, optical construction, special lens elements, and coatings
- [Lens and related optical product field reference](../../../lens-field-reference.md): how to read teleconverter data from an actual record

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/product-type-teleconverter.schema.json)
