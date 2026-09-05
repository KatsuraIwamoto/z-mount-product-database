# product-type-pinhole.schema.json

This schema validates the `pinhole` block of products with `productType: "pinhole"`.
A single product can record imaging methods that do not rely on conventional lens-focusing mechanisms, including pinholes, pinhole sieves, and zone plates.

## Example `pinhole` block

The following example uses the Lensbaby Obscura 16 to show how to record a product with three imaging modes.

Source: `data/records/lenses/lensbaby/lensbaby-obscura-16.json`

Excerpt: `pinhole`

```json
{
  "coverage": {
    "format": "full-frame"
  },
  "focalLength": {
    "kind": "fixed",
    "millimeters": 16
  },
  "imagingModes": [
    {
      "type": "zone-plate",
      "fNumber": 22,
      "opening": null
    },
    {
      "type": "pinhole-sieve",
      "fNumber": 45,
      "opening": null
    },
    {
      "type": "pinhole",
      "fNumber": 90,
      "opening": null
    }
  ],
  "anglesOfView": null
}
```

## Top-level fields

All four fields below are required.

| Path | Type/value | Description |
| --- | --- | --- |
| `pinhole.coverage` | [coverage](../shared/shared-definitions.md#basic-values) | Largest image format covered by the product |
| `pinhole.focalLength` | object or `null` | Nominal focal length from the pinhole plane to the image plane |
| `pinhole.imagingModes` | mode[] or `null` | Imaging modes provided by the product. If known, the array contains at least one entry |
| `pinhole.anglesOfView` | [angleOfView](../shared/shared-definitions.md#optical-values)[] or `null` | Officially published angles of view. If known, the array contains at least one entry |

Record dimensions, weight, mount information, and filter attachment methods in the [common product blocks](product-components.md).

## Focal length

Use `null` for `pinhole.focalLength` when accepted published evidence does not establish a value.
When it is an object, the required fields depend on `kind`.

| `kind` | Required fields | Description |
| --- | --- | --- |
| `fixed` | `millimeters` | Fixed focal length in millimeters |
| `variable` | `rangeMm.minimum`, `rangeMm.maximum` | Minimum and maximum values of the variable range in millimeters |

The two focal-length shapes are mutually exclusive; fields that do not correspond to `kind` are not permitted.

| Path | Type/value | Description |
| --- | --- | --- |
| `pinhole.focalLength.kind` | `fixed` / `variable` | Selects whether the focal length is fixed or variable |
| `pinhole.focalLength.millimeters` | positive number | Focal length in millimeters when `kind` is `fixed` |
| `pinhole.focalLength.rangeMm.minimum` | positive number | Minimum focal length in millimeters when `kind` is `variable` |
| `pinhole.focalLength.rangeMm.maximum` | positive number | Maximum focal length in millimeters when `kind` is `variable` |

## Imaging modes and apertures

Every element of `imagingModes[]` contains `type`, `fNumber`, and `opening`.

| Path | Type/value | Description |
| --- | --- | --- |
| `pinhole.imagingModes[].type` | `pinhole` / `pinhole-sieve` / `zone-plate` | Imaging mode |
| `pinhole.imagingModes[].fNumber` | positive number or `null` | Nominal f-number for the imaging mode |
| `pinhole.imagingModes[].opening` | object or `null` | Aperture diameter specification |

Record `opening: null` when the aperture diameter has not been published.
When it is an object, the required fields depend on `kind`.

| `opening.kind` | Required fields | Description |
| --- | --- | --- |
| `fixed` | `diameterMm` | Fixed aperture diameter in millimeters |
| `discrete` | `diametersMm` | One or more distinct selectable aperture diameters in millimeters |
| `continuous-range` | `minimumDiameterMm`, `maximumDiameterMm` | Minimum and maximum aperture diameters of the continuous range in millimeters |

The three `opening` shapes are mutually exclusive; fields that do not correspond to `opening.kind` are not permitted.

| Path | Type/value | Description |
| --- | --- | --- |
| `pinhole.imagingModes[].opening.kind` | `fixed` / `discrete` / `continuous-range` | Selects whether the aperture diameter is fixed, discrete, or continuously variable |
| `pinhole.imagingModes[].opening.diameterMm` | positive number | Fixed aperture diameter in millimeters |
| `pinhole.imagingModes[].opening.diametersMm` | positive number[] | Selectable aperture diameters in millimeters |
| `pinhole.imagingModes[].opening.minimumDiameterMm` | positive number | Minimum aperture diameter of the continuous range in millimeters |
| `pinhole.imagingModes[].opening.maximumDiameterMm` | positive number | Maximum aperture diameter of the continuous range in millimeters |

## Related pages

- [product-full](product-full.md): how to combine the block with common fields
- [product-components](product-components.md): dimensions, weight, mount information, and filter attachment methods
- [Lens and related optical product field reference](../../../lens-field-reference.md): an explanation using the Lensbaby Obscura 16

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/product-type-pinhole.schema.json)
