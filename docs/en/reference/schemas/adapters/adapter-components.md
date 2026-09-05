# adapter-components.schema.json

Defines the product-information blocks shared by mount adapters.
It is a collection of definitions referenced by [adapter-full](adapter-full.md), not a schema that validates a standalone JSON file.

## Definition groups

| Definition | Contents |
| --- | --- |
| [`identity`](#identity) | Manufacturer, brand, product name, model numbers, alternate names, and variants |
| [`lifecycle`](#lifecycle) | Product release announcement date and official designations from the manufacturer or brand |
| [`officialProductPage`](#officialproductpage) | Official product page URL, region, language, and publisher |
| [`mountConfiguration`](#mountconfiguration) | Combination of the source lens-side mount and the Nikon Z mount |
| [`electronics`](#electronics) | Electronic contacts and electronic functions available through the adapter |
| [`conversionOptics`](#conversionoptics) | Presence of conversion optics and their effects on focal length and maximum aperture |
| [`mechanisms`](#mechanisms) | Additional mechanisms such as aperture rings, helicoids, and shift functionality |
| [`physical`](#physical) | Dimensions, weight, official environmental-protection claims, and tripod support |

See [Shared definitions](../shared/shared-definitions.md) for smaller definitions such as IDs, strings, region codes, and language tags.

## Examples of shared blocks

The following examples show where the blocks appear in the canonical record for the Mount Adapter FTZ II.
Each code sample extracts only the blocks or array elements needed for the explanation from the actual canonical record.

=== "Identity and release information"

    Source file: `data/records/adapters/nikon/mount-adapter-ftz-ii.json`

    Referenced fields: `identity`, `lifecycle`

    ```json
    {
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
      }
    }
    ```

=== "Official product page"

    Source file: `data/records/adapters/nikon/mount-adapter-ftz-ii.json`

    Referenced element: `officialProductPages[1]`

    ```json
    {
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

=== "Mounts and functions"

    Source file: `data/records/adapters/nikon/mount-adapter-ftz-ii.json`

    Referenced fields: `mountConfigurations`, `electronics`, `electronicServices`, `conversionOptics`, `mechanisms`

    ```json
    {
      "mountConfigurations": [
        {
          "lensSideMountSystemId": "nikon-f",
          "cameraSideMountSystemId": "nikon-z",
          "lensRetention": null,
          "lensRearProtrusionLimits": null
        }
      ],
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
      "electronicServices": null,
      "conversionOptics": {
        "present": false
      },
      "mechanisms": []
    }
    ```

=== "Physical characteristics"

    Source file: `data/records/adapters/nikon/mount-adapter-ftz-ii.json`

    Referenced field: `physical`

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

## Identity {#identity}

All six fields directly under `identity` are required.
Even when model numbers, alternate names, or variants cannot be confirmed from accepted published evidence, do not omit their fields. Record `null` instead.
See the [shared definition of `modelNumberOptions`](../shared/shared-definitions.md#basic-values) for which identifiers are treated as model numbers.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `identity.manufacturerId` | ID string | ID of the entity that manufactures the product, registered in the manufacturer and brand registry |
| `identity.brandId` | ID string | ID of the brand displayed on the product and used to identify it commercially, registered in the manufacturer and brand registry |
| `identity.productName` | string | Official product name, including its capitalization and punctuation |
| `identity.modelNumberOptions` | string[] or `null` | Model numbers confirmed in official sources |
| `identity.alternateNames` | alternateName[] or `null` | Officially confirmed alternate names, such as regional or former names |
| `identity.alternateNames[].name` | string | Alternate name. Required in every entry |
| `identity.alternateNames[].brandId` | ID string | Brand ID used with the alternate name when it differs from `identity.brandId` |
| `identity.alternateNames[].region` | two-letter region code | Region in which the alternate name is used |
| `identity.alternateNames[].language` | language tag | Language of the alternate name |
| `identity.variants` | variant[] or `null` | Color or mount variants treated as one product |
| `identity.variants[].variantId` | ID string | Variant ID referenced from `mountConfigurations[]`. Required in every entry |
| `identity.variants[].name` | string | Official or identifying name of the variant. Required in every entry |
| `identity.variants[].modelNumberOptions` | string[] or `null` | Official model numbers specific to the variant. Required in every entry |
| `identity.variants[].color` | string | Official color name |

## Release information {#lifecycle}

`announcementDate` and `officialDesignations` are required.
Do not use a development-announcement date for `announcementDate`.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `lifecycle.announcementDate` | date or `null` | Date on which the manufacturer or brand officially announced the product's release |
| `lifecycle.officialDesignations` | designation[] or `null` | Official manufacturer or brand designations such as legacy product, sales ended, production ended, or discontinued. After checking the collection, use `[]` when there is no applicable designation |
| `lifecycle.officialDesignations[].type` | `legacy-product` / `sales-ended` / `production-ended` / `discontinued` | Normalized form of the official designation. Required in every entry |
| `lifecycle.officialDesignations[].region` | two-letter region code | Region to which the designation applies |
| `lifecycle.officialDesignations[].observedOn` | date | Date on which the designation was observed |

`officialDesignations: []` does not mean that the product is currently sold, in stock, or available.

## Official product page {#officialproductpage}

Every entry in `officialProductPages[]` has five fields directly under it: `url`, `pageFamilies`, `region`, `language`, and `publisher`.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `officialProductPages[].url` | HTTP(S) URL | Main official landing page for the exact product |
| `officialProductPages[].pageFamilies` | enum[] | One or more page families selected from `home-country`, `global`, `japan`, `nikon-imaging-japan`, or `usa` |
| `officialProductPages[].region` | two-letter region code or `null` | Target region. Use `null` for a global page or another page that cannot be limited to one region |
| `officialProductPages[].language` | language tag or `null` | Primary language of the page |
| `officialProductPages[].publisher` | object | Publisher type and name |
| `officialProductPages[].publisher.type` | `manufacturer-or-brand` / `authorized-distributor` | Whether the page is published by the manufacturer or brand itself, or by an authorized distributor |
| `officialProductPages[].publisher.name` | string | Publisher name |

Both `publisher.type` and `publisher.name` are required within `publisher`.

## Mount configurations {#mountconfiguration}

`mountConfigurations` must contain at least one entry.
Duplicate entries are not allowed.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `mountConfigurations[].lensSideMountSystemId` | mount system ID | Source lens-side mount. Required in every entry |
| `mountConfigurations[].cameraSideMountSystemId` | `"nikon-z"` | Target camera-side mount. Required in every entry |
| `mountConfigurations[].lensRetention` | lensRetention or `null` | Lens-side retention method. Required in every entry |
| `mountConfigurations[].lensRetention.type` | `mount-defined` / `positive-lock` / `locking-ring` / `other` | Retention classification |
| `mountConfigurations[].lensRetention.officialName` | string (optional) | Stable manufacturer name for the retention method |
| `mountConfigurations[].lensRearProtrusionLimits` | lensRearProtrusionLimit[] or `null` | Permitted rear-lens protrusion. Required in every entry |
| `mountConfigurations[].lensRearProtrusionLimits[].maximumMm` | non-negative number | Maximum protrusion from the reference plane in millimeters |
| `mountConfigurations[].lensRearProtrusionLimits[].referencePlane` | `mount-flange` / `mount-face` / `other` / `null` | Measurement reference plane |
| `mountConfigurations[].lensRearProtrusionLimits[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | Applicable conditions |
| `mountConfigurations[].variantId` | ID string | Corresponding `identity.variants[].variantId` |

`lensSideMountSystemId` cannot be `nikon-z`.
Repository validation checks that both mount system IDs are registered and that `variantId` references an ID in `identity.variants`.

## Electronic functions {#electronics}

`electronics` is an object or `null`.
When it is an object, all eight fields directly under it are required.
Each value describes a function confirmed for the adapter product. It does not guarantee operation with every combination of lens, camera, and firmware.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `electronics.electronicContacts` | boolean or `null` | Presence of electronic contacts |
| `electronics.autofocus` | boolean or `null` | Autofocus support |
| `electronics.cameraControlledAperture` | boolean or `null` | Camera-controlled aperture |
| `electronics.metadataTransmission` | [metadataTransmission](../shared/shared-definitions.md#electronic-data) | Shooting-metadata transmission and published standards |
| `electronics.lensStabilizationCommunication` | boolean or `null` | Communication with in-lens image stabilization |
| `electronics.manualFocusAssistance` | boolean or `null` | Integration with manual-focus assistance |
| `electronics.lensPowerTransmission` | boolean or `null` | Camera-to-lens power transmission |
| `electronics.recordingTriggerTransmission` | boolean or `null` | Lens-to-camera recording-trigger transmission |

When `electronicContacts` is `false`, the other seven fields must also contain confirmed negative values.
Firmware updates and configuration connections are recorded in the shared `electronicServices` definition.
This separation also represents USB or dock services that do not use lens contacts.

## Conversion optics {#conversionoptics}

The structure of `conversionOptics` depends on what has been confirmed about the presence of conversion optics.

| State | Structure to record |
| --- | --- |
| Accepted published evidence does not establish whether optics are present | `null` |
| Confirmed that no optics are present | `{ "present": false }` |
| Confirmed that optics are present | Object containing `present` and the seven optical-specification fields in the table below |

| Path | Type/value | Meaning |
| --- | --- | --- |
| `conversionOptics.present` | boolean | Whether the adapter contains optics used for mount conversion |
| `conversionOptics.focalLengthMultiplier` | positive number or `null` | Focal-length multiplier produced by the conversion optics |
| `conversionOptics.apertureChange` | apertureChange or `null` | Change in maximum aperture produced by the conversion optics |
| `conversionOptics.apertureChange.direction` | `brighter` / `darker` / `unchanged` | Whether the maximum aperture becomes brighter, darker, or remains unchanged |
| `conversionOptics.apertureChange.stops` | non-negative number | Absolute change in stops; `0` for `unchanged` and positive otherwise |
| `conversionOptics.apertureChange.relation` | `exact` / `approximately` / `less-than` | Whether the published value is exact, approximate, or less than the stated number of stops; `exact` for `unchanged` |
| `conversionOptics.opticalConstruction` | [opticalConstruction](../shared/shared-definitions.md#opticalconstruction) or `null` | Group and element counts for the conversion optics |
| `conversionOptics.specialElements` | [specialElement](../shared/shared-definitions.md#specialelement)[] or `null` | Special optical elements; use `[]` when checked and none apply |
| `conversionOptics.coatings` | [coating](../shared/shared-definitions.md#coating)[] or `null` | Coatings on the conversion optics; use `[]` when checked and none apply |
| `conversionOptics.supportedImageCircleDiameterMm` | imageCircleDiameter or `null` | Supported image-circle diameter in millimeters |
| `conversionOptics.supportedImageCircleDiameterMm.kind` | `value` / `range` | Selects a single value or a range |
| `conversionOptics.supportedImageCircleDiameterMm.diameterMm` | positive number | Image-circle diameter in millimeters for `value` |
| `conversionOptics.supportedImageCircleDiameterMm.minimumDiameterMm` | positive number | Lower bound of a `range` in millimeters |
| `conversionOptics.supportedImageCircleDiameterMm.maximumDiameterMm` | positive number | Upper bound of a `range` in millimeters |
| `conversionOptics.maximumSupportedAperture` | maximumSupportedAperture or `null` | Fastest published maximum aperture supported for an attached lens |
| `conversionOptics.maximumSupportedAperture.scale` | `f-number` / `t-number` | Selects the f-number or T-number scale |
| `conversionOptics.maximumSupportedAperture.value` | positive number | Aperture value; for example, `scale: "t-number"` with `value: 2.8` represents T2.8 |

When `present` is `false`, do not record optical specifications other than `present`.
When it is `true`, all seven fields are required. Record `null` for an individual field not established by accepted published evidence.
For an image-circle range, repository validation also checks that `minimumDiameterMm` does not exceed `maximumDiameterMm`.

## Additional mechanisms {#mechanisms}

`mechanisms` is an array of objects describing the confirmed additional mechanisms without duplicates, or `null`.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `mechanisms[].type` | `aperture-ring` / `drop-in-filter` / `flange-focal-distance-adjustment` / `helicoid` / `shift` / `tilt` / `rotation` / `other` | Mechanism classification |
| `mechanisms[].officialName` | string (optional) | Stable manufacturer name for the mechanism |
| `mechanisms[].movements` | [movements](../shared/shared-definitions.md#movements) or `null` | Nominal shift, tilt, or rotation measurements |
| `mechanisms[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | Conditions under which the mechanism applies |

After checking the collection of additional mechanisms, use `[]` when there are no applicable mechanisms and `null` when they cannot be confirmed from accepted published evidence.
Shift, tilt, and rotation mechanisms require `movements`, which can contain only the corresponding measurement type.
Use `movements.shiftMeasurements` for `shift`, `movements.tiltMeasurements` for `tilt`, and `movements.rotationMeasurements` for `rotation`.
Use `movements: null` when the mechanism is established but its nominal range is not.
Do not use a `movements` object whose corresponding measurement field is `null`.
Other mechanism types omit `movements`.
Record lens retention under the applicable `mountConfigurations[].lensRetention` instead of mixing it with additional mechanisms.

## Dimensions, weight, environmental-protection claims, and tripod support {#physical}

`dimensionMeasurements`, `weightMeasurements`, `officialEnvironmentalProtectionClaims`, and `tripodSupport` are all required directly under `physical`.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `physical.dimensionMeasurements` | dimensionMeasurement[] or `null` | Official dimensions. At least one entry when known |
| `physical.dimensionMeasurements[].maximumDiameterMm` | positive number | Maximum diameter in millimeters |
| `physical.dimensionMeasurements[].lengthMm` | positive number | Length in millimeters under the manufacturer's measurement convention |
| `physical.dimensionMeasurements[].widthMm` | positive number | Width in millimeters |
| `physical.dimensionMeasurements[].heightMm` | positive number | Height in millimeters |
| `physical.dimensionMeasurements[].unclassifiedDimensionsMm` | positive number[] | Dimensions whose axes are not identified by the published source, in published order; at least one value |
| `physical.dimensionMeasurements[].approximate` | boolean | Whether the source qualifies the value as approximate; omission means that it does not |
| `physical.dimensionMeasurements[].conditions` | dimensionMeasurementConditions | Measurement conditions; required in every entry |
| `physical.dimensionMeasurements[].conditions.variantId` | ID string | Product variant to which the dimensions apply |
| `physical.dimensionMeasurements[].conditions.componentStates` | measurementComponentStates | Whether each stated component was attached during measurement |
| `physical.dimensionMeasurements[].conditions.excludesProjections` | boolean | Whether the dimensions exclude projections |
| `physical.dimensionMeasurements[].note` | string | Source-explicit measurement condition or definition that structured fields cannot represent |
| `physical.weightMeasurements` | weightMeasurement[] or `null` | Official weight. At least one entry when known |
| `physical.weightMeasurements[].grams` | positive number | Weight in grams. Required in every entry |
| `physical.weightMeasurements[].approximate` | boolean | Whether the source qualifies the value as approximate; omission means that it does not |
| `physical.weightMeasurements[].conditions` | weightMeasurementConditions | Weight conditions; required in every entry |
| `physical.weightMeasurements[].conditions.variantId` | ID string | Product variant to which the weight applies |
| `physical.weightMeasurements[].conditions.componentStates` | measurementComponentStates | Whether each stated component was attached during measurement |
| `physical.weightMeasurements[].note` | string | Source-explicit measurement condition that structured fields cannot represent |
| `physical.officialEnvironmentalProtectionClaims` | [environmentalClaim](../shared/shared-definitions.md#environmentalclaim)[] or `null` | Official dust-, drip-, weather-, or similar protection claims; use `[]` when checked and none apply |
| `physical.tripodSupport` | [tripodSupport](../shared/shared-definitions.md#tripod-support) | Presence of tripod support and its components |

`measurementComponentStates` records only components explicitly addressed by the source, using boolean values under `tripodCollarAssembly`, `tripodFoot`, `tripodMountCover`, `lensHood`, `frontCap`, `rearCap`, or `dropInFilter`.
Each dimension entry must contain at least one of `maximumDiameterMm`, `lengthMm`, `widthMm`, `heightMm`, or `unclassifiedDimensionsMm`.
When `tripodSupport.present` is `false`, the object contains only `present`.

## Related pages

- [Shared definitions](../shared/shared-definitions.md): Smaller definitions such as IDs, strings, region codes, and language tags
- [adapter-full](adapter-full.md): Structure of one product assembled from these definitions
- [Mount adapter field reference](../../../adapter-field-reference.md): Descriptions of each block using actual data

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/adapters/adapter-components.schema.json)
