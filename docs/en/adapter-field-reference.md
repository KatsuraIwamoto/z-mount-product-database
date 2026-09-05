# Mount adapter field reference

This page is a reference for the fields in canonical mount adapter records and in each product entry in the distribution data.
You do not need to read it from beginning to end; use the field names to find the sections you need.

Every canonical mount adapter record uses the same structure.
Because the structure does not branch by product type, these records have neither a `productType` field nor a product-type block.

!!! info "Mount adapters have only a Full distribution"

    In the mount adapter Full distribution, the `adapters` array contains each canonical record with only `$schema` removed.
    The file is named `z-mount-adapters.full.json`.
    There is no Light version.

The JSON shown on this page contains only the parts of actual canonical records needed for each explanation.
The examples are not complete records.
Some examples also show only part of an array.
See the [JSON Schema reference](reference/schemas/adapters/adapter-full.md) for each field's type, whether it is required, and its allowed values.

The main examples use the Mount Adapter FTZ II.
The Magic Shift Converter (MSC) provides examples of multiple mount configurations, conversion optics, and additional mechanisms.
Fields for lenses and related optical products are documented in the [field reference for lenses and related optical products](lens-field-reference.md).

## Identity and publication information (`identity`, `lifecycle`, and `officialProductPages`)

| Field | Information recorded |
| --- | --- |
| `id` | ID that identifies the product |
| `identity` | Manufacturer ID, brand ID, official product name, official model numbers, official alternate names, and variants within the same product |
| `lifecycle` | Official product release announcement date and official status designations from the manufacturer or brand, such as legacy, sales ended, production ended, or discontinued |
| `officialProductPages` | Official main pages for the product, together with their region, language, and publisher |

The Mount Adapter FTZ II demonstrates how identity information, the product release announcement date, and official product pages are recorded.

Source: `data/records/adapters/nikon/mount-adapter-ftz-ii.json`

```json
{
  "id": "mount-adapter-ftz-ii",
  "identity": {
    "manufacturerId": "nikon",
    "brandId": "nikon",
    "productName": "Mount Adapter FTZ II",
    "modelNumberOptions": null,
    "alternateNames": [
      {
        "name": "マウントアダプター FTZ II",
        "region": "JP",
        "language": "ja"
      }
    ],
    "variants": null
  },
  "lifecycle": {
    "announcementDate": "2021-10-28",
    "officialDesignations": []
  },
  "officialProductPages": [
    {
      "url": "https://nij.nikon.com/products/lineup/accessory/body/ftz_2/index.html",
      "pageFamilies": [
        "nikon-imaging-japan"
      ],
      "region": "JP",
      "language": "ja",
      "publisher": {
        "type": "manufacturer-or-brand",
        "name": "Nikon"
      }
    }
  ]
}
```

`identity.manufacturerId` records the manufacturing entity ID, while `identity.brandId` records the ID of the brand displayed on the product.
In this example, both IDs are `nikon`, whose display name is Nikon.
In a distribution JSON, display names are available from the root `referenceData` object.
The English official product name is stored in `identity.productName`, and the official Japanese name is stored in `identity.alternateNames`.

`lifecycle.announcementDate` is the official product release announcement date.
A development-announcement date is not used as a substitute.
An empty `lifecycle.officialDesignations` array means that no official designation was confirmed; it does not mean that the product is currently sold, in stock, or available.
The removal of an official product page alone is not treated as proof that sales have ended.
See [URLs and sources](value-rules.md#urls) for the distinction between official product pages and other sources used in research.

## Mount configurations (`mountConfigurations`)

`mountConfigurations` records pairs of the lens-side source mount and the camera-side destination mount.

| Field | Information recorded |
| --- | --- |
| `lensSideMountSystemId` | Mount-system ID for the source interchangeable-lens mount |
| `cameraSideMountSystemId` | Mount-system ID for the destination camera mount; the value is `nikon-z` |
| `lensRetention` | Lens-side retention method and official name; `null` when not established |
| `lensRearProtrusionLimits` | Permitted rear-lens protrusion, reference plane, and applicable conditions; `null` when not established |
| `variantId` | ID of the product variant corresponding to the mount pair |

=== "One mount configuration"

    The Mount Adapter FTZ II demonstrates how a single mount configuration is recorded.

    Source: `data/records/adapters/nikon/mount-adapter-ftz-ii.json`

    ```json
    {
      "mountConfigurations": [
        {
          "lensSideMountSystemId": "nikon-f",
          "cameraSideMountSystemId": "nikon-z",
          "lensRetention": null,
          "lensRearProtrusionLimits": null
        }
      ]
    }
    ```

    In this example, the source Nikon F mount is stored in `lensSideMountSystemId`, and the destination Nikon Z mount is stored in `cameraSideMountSystemId`.

=== "Multiple mount configurations"

    The Magic Shift Converter (MSC) demonstrates how multiple mount configurations are recorded.
    Each `mountConfigurations[].variantId` refers to the corresponding `identity.variants[].variantId`.

    Source: `data/records/adapters/laowa/laowa-magic-shift-converter-z.json`

    ```json
    {
      "identity": {
        "variants": [
          {
            "variantId": "canon-ef-nikon-z",
            "name": "Canon EF to Nikon Z",
            "modelNumberOptions": null
          },
          {
            "variantId": "nikon-f-nikon-z",
            "name": "Nikon F to Nikon Z",
            "modelNumberOptions": null
          }
        ]
      },
      "mountConfigurations": [
        {
          "lensSideMountSystemId": "canon-ef",
          "cameraSideMountSystemId": "nikon-z",
          "variantId": "canon-ef-nikon-z",
          "lensRetention": null,
          "lensRearProtrusionLimits": null
        },
        {
          "lensSideMountSystemId": "nikon-f",
          "cameraSideMountSystemId": "nikon-z",
          "variantId": "nikon-f-nikon-z",
          "lensRetention": null,
          "lensRearProtrusionLimits": null
        }
      ]
    }
    ```

    This example records the Canon EF and Nikon F variants in a single canonical product record.

See the [data model](data-model.md#shared-registries) for the relationship between mount-system IDs and the registry.

## Electronic functions and connection services (`electronics`, `electronicServices`)

`electronics` records whether electronic contacts are present and which electronic functions are available through the adapter.

!!! warning "Individual combinations are not guaranteed"
    These values describe functions confirmed for the adapter product by accepted published evidence.
    They do not guarantee operation with every lens, camera body, or firmware version.
    Check the official compatibility information and manuals from the manufacturer or brand for a specific combination.

| Field | Information recorded |
| --- | --- |
| `electronicContacts` | Whether electronic contacts are present |
| `autofocus` | Whether autofocus is supported |
| `cameraControlledAperture` | Whether camera-controlled aperture is supported |
| `metadataTransmission` | Whether shooting metadata is transmitted and, when published, whether it uses Exif, Cooke /i, or another standard |
| `lensStabilizationCommunication` | Whether the adapter communicates with in-lens stabilization |
| `manualFocusAssistance` | Whether the adapter integrates with manual-focus assistance |
| `lensPowerTransmission` | Whether the camera supplies power to the lens |
| `recordingTriggerTransmission` | Whether a lens-side recording command is transmitted to the camera |
| `electronicServices` | Published firmware-update status and connection methods used for updates, configuration, or control |

The Mount Adapter FTZ II demonstrates how electronic functions are recorded.

Source: `data/records/adapters/nikon/mount-adapter-ftz-ii.json`

```json
{
  "electronics": {
    "electronicContacts": true,
    "autofocus": true,
    "cameraControlledAperture": true,
    "lensStabilizationCommunication": true,
    "manualFocusAssistance": true,
    "metadataTransmission": {
      "present": true,
      "standards": [
        "exif"
      ]
    },
    "lensPowerTransmission": null,
    "recordingTriggerTransmission": null
  },
  "electronicServices": null
}
```

`true` means that support was confirmed, while `false` means that lack of support was confirmed.
`metadataTransmission.standards` is `null` when transmission is confirmed but its standard is not identified.
A field-level `null`, such as `lensPowerTransmission: null`, means that accepted published evidence does not establish support for that function.
When the entire `electronics` value is `null`, no electronic-function information could be confirmed.
`electronicServices` is separate from functions carried through lens contacts, so it can describe firmware updates through USB or a dock.
See [value states](value-rules.md#value-states) for how these states differ.

## Conversion optics and additional mechanisms (`conversionOptics`, `mechanisms`)

`conversionOptics` records whether conversion optics are present, their effect on focal length and maximum aperture, their optical construction, and properties such as the supported image circle.
`mechanisms` records each additional mechanism as a typed object.
Nominal shift, tilt, and rotation amounts are nested in the corresponding mechanism's `movements` field.

| Field | Information recorded |
| --- | --- |
| `conversionOptics.present` | Whether the adapter contains optics used for mount conversion |
| `conversionOptics.focalLengthMultiplier` | Focal-length multiplier introduced by the conversion optics |
| `conversionOptics.apertureChange` | Whether the aperture becomes brighter or darker, the number of stops, and whether the published value is exact, approximate, or a less-than limit |
| `conversionOptics.opticalConstruction` | Number of groups and elements in the conversion optics |
| `conversionOptics.specialElements` | Types, official names, and quantities of special optical elements |
| `conversionOptics.coatings` | Coating types, official names, and application locations |
| `conversionOptics.supportedImageCircleDiameterMm` | Supported image-circle diameter or range in millimeters |
| `conversionOptics.maximumSupportedAperture` | Fastest published f-number or T-number supported for an attached lens |
| `mechanisms[].type` | Aperture ring, drop-in filter, flange-focal-distance adjustment, helicoid, shift, tilt, rotation, or another mechanism |
| `mechanisms[].officialName` | Stable manufacturer name for the mechanism, when established |
| `mechanisms[].movements` | Shift, tilt, or rotation measurements; omitted for non-movement mechanisms |
| `mechanisms[].conditions` | Variant or other conditions under which the mechanism applies |

=== "No optics or additional mechanisms"

    The Mount Adapter FTZ II demonstrates how the absence of conversion optics and additional mechanisms is recorded.

    Source: `data/records/adapters/nikon/mount-adapter-ftz-ii.json`

    ```json
    {
      "conversionOptics": {
        "present": false
      },
      "mechanisms": []
    }
    ```

=== "Optics and an additional mechanism"

    The Magic Shift Converter (MSC) demonstrates how conversion optics and an additional mechanism are recorded.

    Source: `data/records/adapters/laowa/laowa-magic-shift-converter-z.json`

    ```json
    {
      "conversionOptics": {
        "present": true,
        "focalLengthMultiplier": 1.4,
        "apertureChange": {
          "direction": "darker",
          "stops": 1,
          "relation": "exact"
        },
        "opticalConstruction": {
          "groups": 4,
          "elements": 5
        },
        "specialElements": null,
        "coatings": null,
        "supportedImageCircleDiameterMm": null,
        "maximumSupportedAperture": null
      },
      "mechanisms": [
        {
          "type": "shift",
          "conditions": {},
          "movements": {
            "shiftMeasurements": [
              {
                "maximumFromNeutralMm": 10,
                "totalRangeMm": null,
                "directionality": null,
                "conditions": {}
              }
            ]
          }
        },
        {
          "type": "rotation",
          "movements": {
            "rotationMeasurements": [
              {
                "scope": "movement-assembly",
                "maximumFromNeutralDegrees": null,
                "totalRangeDegrees": 360,
                "directionality": null,
                "conditions": {}
              }
            ]
          },
          "conditions": {}
        }
      ]
    }
    ```

    This example records a 4-group, 5-element optical system that applies a 1.4× focal-length multiplier and makes the maximum aperture exactly one stop slower, together with a shift mechanism.
    The one-way shift from the neutral position is 10 mm, and the movable assembly has a 360° rotation range.
    The `null` values for special elements and similar fields mean that the optics themselves are confirmed but accepted published evidence does not establish those properties.

`apertureChange.direction` uses `brighter`, `darker`, or `unchanged`.
`relation` uses `exact`, `approximately`, or `less-than`, preserving wording such as "approximately one stop" and "less than one stop" separately from the numeric value.
When `conversionOptics.present` is `false`, no optical specification other than `present` is recorded.
`conversionOptics: null` means that accepted published evidence does not establish whether conversion optics are present.
When `conversionOptics.present` is `true`, all seven specification fields are present and any value not established by accepted published evidence is `null`.
`mechanisms: []` means that the product was checked and confirmed to have no applicable additional mechanisms.
`mechanisms: null` means that the presence of additional mechanisms could not be established.
Shift, tilt, and rotation mechanisms require `movements`; use `null` when the nominal amount cannot be confirmed.
Other mechanism types omit `movements`.
Measurements distinguish the maximum from a neutral position from the total end-to-end range, while preserving published directionality and conditions.
See [value states](value-rules.md#value-states) for how these states differ.

## Dimensions, weight, environmental-protection claims, and tripod support (`physical`)

`physical` records dimensions, weight, official environmental-protection claims, and tripod support established by accepted published evidence.

| Field | Information recorded |
| --- | --- |
| `dimensionMeasurements` | Maximum diameter, width, height, length, dimensions whose axes are not published, and their measurement conditions |
| `weightMeasurements` | Weight in grams, whether it is approximate, and its measurement conditions |
| `officialEnvironmentalProtectionClaims` | Official dust-, drip-, or weather-protection wording and its scope |
| `tripodSupport` | Presence of tripod support, component type, product relationship, removability, tripod-side interface, model number, quantity, and conditions |

The Mount Adapter FTZ II demonstrates how dimensions, weight, environmental-protection claims, and tripod support are recorded.

Source: `data/records/adapters/nikon/mount-adapter-ftz-ii.json`

```json
{
  "physical": {
    "dimensionMeasurements": [
      {
        "widthMm": 70,
        "heightMm": 70,
        "lengthMm": 36,
        "approximate": true,
        "conditions": {
          "excludesProjections": true
        }
      }
    ],
    "weightMeasurements": [
      {
        "grams": 125,
        "approximate": true,
        "conditions": {}
      }
    ],
    "officialEnvironmentalProtectionClaims": [
      {
        "types": [
          "dust-resistant",
          "drip-resistant"
        ],
        "scope": {
          "kind": "product"
        },
        "conditions": {}
      }
    ],
    "tripodSupport": {
      "present": false
    }
  }
}
```

In this example, the width and height are approximately 70 mm, the length is approximately 36 mm, and the weight is approximately 125 g.
`conditions.excludesProjections: true` means that the dimensions exclude projections, while an empty `conditions` object means that the weight has no additional conditions.
The environmental claim applies to the product and records both dust and drip resistance.
`tripodSupport.present: false` means that the absence of a tripod support mechanism was confirmed.
When tripod support is present, a collar assembly and its foot can be recorded as separate components.
Use `components: null` when support is confirmed but its component breakdown is not established.
See the [shared definition](reference/schemas/shared/shared-definitions.md#tripod-support) for component fields.

## Related pages

- [Glossary](glossary.md): terms used by this project
- [Value-state rules](value-rules.md): meanings of omitted fields, `null`, empty arrays, and `false`
- [Data model](data-model.md): relationships among research results, canonical records, and distributions
- [Field reference for lenses and related optical products](lens-field-reference.md): fields for lenses, teleconverters, and pinholes
- [JSON Schema reference](reference/schemas/adapters/adapter-full.md): types, required fields, and allowed values
