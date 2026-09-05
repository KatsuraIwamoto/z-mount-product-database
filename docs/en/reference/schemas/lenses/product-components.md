# product-components.schema.json

This schema defines the product-information blocks shared by lenses, teleconverters, and pinhole products.
It is a collection of definitions referenced by [product-full](product-full.md), not a schema that validates a standalone JSON file.

## Definition groups

| Definition | Contents |
| --- | --- |
| [`identity`](#identity) | Manufacturer, brand, product name, model numbers, alternate names, and variants |
| [`lifecycle`](#lifecycle) | Product release announcement date and status wording from the manufacturer or brand |
| [`officialProductPage`](#officialproductpage) | Official product page URL, region, language, and publisher |
| [`mount`](#mount) | Connection to the Nikon Z mount, electronic contacts, and a mount adapter supplied with or dedicated to the product |
| [`physical`](#physical) | Dimensions, weight, protection claims, filters, tripod mounting hardware, and external shape changes |
| [`control`](#control) | Controls such as rings, switches, buttons, and displays |
| [`accessories`](#accessories) | Hoods, caps, cases, and similar items |

For smaller definitions such as IDs, numbers, measurement conditions, and optical construction, see [Shared definitions](../shared/shared-definitions.md).

## Examples of common blocks

The following examples use the NIKKOR Z 24-70mm f/2.8 S II to show where these blocks appear in a canonical record.
Each code block contains actual data limited to the blocks identified below.

=== "Identity and product release information"

    Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

    Excerpt: `identity`, `lifecycle`

    ```json
    {
      "identity": {
        "manufacturerId": "nikon",
        "brandId": "nikkor",
        "productName": "NIKKOR Z 24-70mm f/2.8 S II",
        "modelNumberOptions": null,
        "alternateNames": null,
        "variants": null
      },
      "lifecycle": {
        "announcementDate": "2025-08-22",
        "officialDesignations": []
      }
    }
    ```

=== "Mount"

    Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

    Excerpt: `mount`

    ```json
    {
      "systemId": "nikon-z",
      "replaceability": "fixed",
      "mountOwnerRelationship": "mount-owner",
      "electronicContacts": {
        "present": true,
        "metadataTransmission": {
          "present": true,
          "standards": [
            "exif"
          ]
        }
      }
    }
    ```

## Identity {#identity}

All six fields directly under `identity` are required.
Even when model numbers, alternate names, or variants cannot be confirmed from accepted published evidence, do not omit the fields. Record `null` instead.
See the [shared definition of `modelNumberOptions`](../shared/shared-definitions.md#basic-values) for which identifiers are treated as model numbers.

| Path | Type/value | Description |
| --- | --- | --- |
| `identity.manufacturerId` | ID string | ID of the entity that manufactures the product, registered in the manufacturer and brand registry |
| `identity.brandId` | ID string | ID of the brand shown on the product and used to identify it commercially, registered in the manufacturer and brand registry |
| `identity.productName` | string | Official product name, including its capitalization and symbols |
| `identity.modelNumberOptions` | string[] or `null` | Model numbers confirmed in official materials |
| `identity.alternateNames` | alternateName[] or `null` | Officially confirmed alternate names, such as regional or former names |
| `identity.alternateNames[].name` | string | Alternate name. Required in every entry |
| `identity.alternateNames[].brandId` | ID string | Brand ID used with the alternate name when it differs from `identity.brandId` |
| `identity.alternateNames[].region` | two-letter region code | Region in which the alternate name is used |
| `identity.alternateNames[].language` | language tag | Language of the alternate name |
| `identity.variants` | variant[] or `null` | Color or sales-configuration variants treated as one product |
| `identity.variants[].variantId` | ID string | Variant ID referenced by measurement conditions. Required in every entry |
| `identity.variants[].name` | string | Official or identifying name of the variant. Required in every entry |
| `identity.variants[].modelNumberOptions` | string[] or `null` | Official model numbers specific to the variant. Required in every entry |
| `identity.variants[].color` | string | Official color name |
| `identity.variants[].focusScaleUnit` | `meters` / `feet` | Unit used on the distance scale |

## Product release information {#lifecycle}

`announcementDate` and `officialDesignations` are required.
Do not use a development-announcement date for `announcementDate`.

| Path | Type/value | Description |
| --- | --- | --- |
| `lifecycle.announcementDate` | date or `null` | Date on which the manufacturer or brand officially announced the product's release |
| `lifecycle.officialDesignations` | designation[] or `null` | Official status wording from the manufacturer or brand, such as legacy product, end of sales, end of production, or discontinued. After checking the list, use `[]` if no designation applies |
| `lifecycle.officialDesignations[].type` | `legacy-product` / `sales-ended` / `production-ended` / `discontinued` | Normalized status for the official wording. Required in every entry |
| `lifecycle.officialDesignations[].region` | two-letter region code | Region to which the status wording applies |
| `lifecycle.officialDesignations[].observedOn` | date | Date on which the status wording was observed |

`officialDesignations: []` does not mean that the product is currently sold, in stock, or available.

## Official product pages {#officialproductpage}

Every element of `officialProductPages[]` contains five fields directly under it: `url`, `pageFamilies`, `region`, `language`, and `publisher`.

| Path | Type/value | Description |
| --- | --- | --- |
| `officialProductPages[].url` | HTTP(S) URL | Official main page for the exact product |
| `officialProductPages[].pageFamilies` | enum[] | At least one page family selected from `home-country`, `global`, `japan`, `nikon-imaging-japan`, and `usa` |
| `officialProductPages[].region` | two-letter region code or `null` | Target region. Use `null` when no single region applies, as with a global page |
| `officialProductPages[].language` | language tag or `null` | Primary language of the page |
| `officialProductPages[].publisher` | object | Publisher type and name |
| `officialProductPages[].publisher.type` | `manufacturer-or-brand` / `authorized-distributor` | Whether the page is published by the manufacturer or brand itself, or by an authorized distributor |
| `officialProductPages[].publisher.name` | string | Name of the publisher |

Both `publisher.type` and `publisher.name` are required within `publisher`.

## Connection to the Nikon Z mount {#mount}

`systemId`, `replaceability`, `mountOwnerRelationship`, and `electronicContacts` are required directly under `mount`.
`adapter` is present only for a product supplied with a Nikon Z-mount adapter or used with an adapter dedicated to that product or an officially identified product series.

| Path | Type/value | Description |
| --- | --- | --- |
| `mount.systemId` | `"nikon-z"` | Fixed value for the target mount system |
| `mount.replaceability` | `fixed` / `user-interchangeable` / `service-interchangeable` / `null` | Whether the product-side mount is replaceable and who can replace it |
| `mount.mountOwnerRelationship` | `mount-owner` / `officially-licensed` / `null` | Whether the product is made by Nikon as the mount owner or is officially licensed |
| `mount.electronicContacts` | object or `null` | Presence of electronic contacts and metadata transmission. Use `null` when accepted published evidence is unavailable |
| `mount.electronicContacts.present` | boolean | Whether electronic contacts are present |
| `mount.electronicContacts.metadataTransmission` | [metadataTransmission](../shared/shared-definitions.md#electronic-data) | Shooting-metadata transmission and published standards when contacts are present |
| `mount.adapter` | officialMountAdapter | Nikon Z-mount adapter that meets the inclusion criteria |
| `mount.adapter.relationship` | `supplied` / `optional` | Whether the adapter is supplied with the product or sold separately |
| `mount.adapter.dedicatedToProduct` | boolean or `null` | Whether the adapter is dedicated to the product or an officially identified product series |
| `mount.adapter.nativeMountSystemId` | mount-system ID or `null` | Lens-side mount system before the adapter is attached |
| `mount.adapter.name` | string or `null` | Official name of the adapter |
| `mount.adapter.modelNumberOptions` | string[] or `null` | Model numbers for the adapter confirmed in official materials |

### Electronic-contact conditions

| `mount.electronicContacts` | Permitted structure |
| --- | --- |
| `null` | Accepted published evidence does not establish whether electronic contacts are present |
| `{ "present": false }` | `metadataTransmission` must not be specified |
| `{ "present": true, "metadataTransmission": ... }` | `metadataTransmission` is required. Use `null` if transmission cannot be confirmed |

### Mount-adapter conditions

All five fields directly under `mount.adapter` are required.
When `relationship` is `optional`, `dedicatedToProduct` must be `true`.

For detailed inclusion criteria and examples, see the [Lens and related optical product field reference](../../../lens-field-reference.md).

## Physical form and attachment interfaces {#physical}

`dimensionMeasurements`, `weightMeasurements`, `officialEnvironmentalProtectionClaims`, `filterInterfaces`, and `tripodSupport` are required directly under `physical`.
Other fields are present only for products to which they structurally apply.

### Dimensions and weight

| Path | Type/value | Description |
| --- | --- | --- |
| `physical.dimensionMeasurements` | measurement[] or `null` | Official dimensions. If known, the array contains at least one entry |
| `physical.dimensionMeasurements[].maximumDiameterMm` | positive number or `null` | Maximum diameter in millimeters |
| `physical.dimensionMeasurements[].lengthMm` | positive number or `null` | Length in millimeters under the manufacturer's measurement convention |
| `physical.dimensionMeasurements[].approximate` | boolean | Record only when the source explicitly states that the entire measurement is approximate |
| `physical.dimensionMeasurements[].conditions.state` | `operational` / `storage` / `at-infinity` | Product state in which the dimensions were measured |
| `physical.dimensionMeasurements[].conditions.variantId` | ID string | ID used when the dimensions apply only to a specific variant |
| `physical.dimensionMeasurements[].conditions.attachedComponents` | enum[] | Components attached during measurement |
| `physical.weightMeasurements` | measurement[] or `null` | Official weights. If known, the array contains at least one entry |
| `physical.weightMeasurements[].grams` | positive number | Weight in grams |
| `physical.weightMeasurements[].approximate` | boolean | Record only when the source explicitly states that the weight is approximate |
| `physical.weightMeasurements[].conditions.attachedComponents` | enum[] | Components included in the weight. After checking the attached components, use `[]` if none apply |
| `physical.weightMeasurements[].conditions.variantId` | ID string | ID used when the weight applies only to a specific variant |

Every dimension entry requires a positive number in at least one of `maximumDiameterMm` and `lengthMm`.
Both fields are required, so record `null` for the unpublished value.
`conditions` for dimensions and `conditions.attachedComponents` for weight are also required.

The following values are available for `attachedComponents`:

- Tripod mounting hardware: `tripod-collar-assembly`, `tripod-foot`, `tripod-mount-cover`
- Lens accessories: `lens-hood`, `front-cap`, `rear-cap`
- Filter: `drop-in-filter`
- Other: `other`

### Environmental protection claims

| Path | Type/value | Description |
| --- | --- | --- |
| `physical.officialEnvironmentalProtectionClaims` | claim[] or `null` | Official wording for dust resistance, drip resistance, and similar protection. After checking the list, use `[]` if no wording applies |
| `physical.officialEnvironmentalProtectionClaims[].types` | enum[] | One or more of `dust-resistant`, `drip-resistant`, `splash-resistant`, `moisture-resistant`, `weather-resistant`, `waterproof`, and `other` |
| `physical.officialEnvironmentalProtectionClaims[].scope.kind` | `product` / `component` | Whether the wording applies to the entire product or only to a specific component |
| `physical.officialEnvironmentalProtectionClaims[].scope.component` | string | Name of the applicable component when `scope.kind: "component"` |
| `physical.officialEnvironmentalProtectionClaims[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | Conditions under which the wording applies, such as focal length, camera body, or variant |

Do not use `scope.component` when `scope.kind` is `product`.
When it is `component`, `scope.component` is required.

### Filter attachment methods

For `physical.filterInterfaces`, use `[]` after checking the attachment methods and finding that none apply, or `null` when accepted published evidence is unavailable.
The dimension field in each entry depends on `type`.

| `type` | Required dimensions | Attachment host |
| --- | --- | --- |
| `front-thread` | `diameterMm` | `host` |
| `rear-thread` | `diameterMm` | `host` |
| `drop-in` | `filterDiameterMm` | `host` |
| `rear-gelatin` | `sheetDimensionsMm` | `host` |

| Path | Type/value | Description |
| --- | --- | --- |
| `physical.filterInterfaces[].diameterMm` | positive number | Front or rear thread diameter in millimeters |
| `physical.filterInterfaces[].filterDiameterMm` | positive number | Drop-in filter diameter in millimeters |
| `physical.filterInterfaces[].sheetDimensionsMm` | object or `null` | Width and height of a rear gelatin filter |
| `physical.filterInterfaces[].sheetDimensionsMm.width` | positive number | Width in millimeters |
| `physical.filterInterfaces[].sheetDimensionsMm.height` | positive number | Height in millimeters |
| `physical.filterInterfaces[].host` | [host](../shared/shared-definitions.md#host) | Product body or accessory to which the filter is attached |

### Tripod mounting hardware and external shape changes

| Path | Type/value | Description |
| --- | --- | --- |
| `physical.tripodSupport` | [tripodSupport](../shared/shared-definitions.md#tripod-support) | Presence of tripod support, its components, product relationship, and mounting interfaces |
| `physical.externalLengthDuringZoom` | `constant` / `variable` / `null` | Change in external length during zooming |
| `physical.externalLengthDuringFocus` | `constant` / `variable` / `null` | Change in external length during focusing |
| `physical.isRetractableForStorage` | boolean or `null` | Whether the product has a storage mechanism that must be extended before use |
| `physical.frontAccessoryInterface.outsideDiameterMm` | positive number | Outside diameter in millimeters for attaching clamp-on front accessories |

When `tripodSupport.present` is `false`, the object contains only `present`.
When it is `true`, `components` is also required; use `null` when support is present but its component breakdown is not established.

## Controls {#control}

Every element of `controls[]` contains `type` and `quantity`.
`officialName` may be added to any control when a stable name appears on the product or in an official specification. Omit a generic name such as `Focus ring` when it merely repeats `type`. Use the manufacturer's official English designation when an equivalent English page exists, but do not invent a translation.

The values of `type` treated as rings are `aperture-ring`, `control-ring`, `function-ring`, `focus-ring`, and `zoom-ring`.
Only these controls may use `clickBehavior`, `rotationDegrees`, `geared`, and `response`.

The other `type` values are grouped below.

- Zoom controls: `power-zoom-control`, `zoom-lever`, `zoom-lock`
- Buttons: `function-button`, `memory-set-button`
- Focus controls: `focus-mode-switch`, `focus-limiter`
- Aperture and control rings: `aperture-ring-click-switch`, `control-ring-click-switch`, `aperture-ring-lock`
- Displays: `information-display`, `focus-distance-scale`, `depth-of-field-scale`
- Other: `other`

| Path | Type/value | Description |
| --- | --- | --- |
| `controls[].type` | enum | Type of control |
| `controls[].quantity` | integer of 1 or greater | Number of controls of the same type |
| `controls[].officialName` | string, optional | Stable manufacturer name shown on the product or in an official specification when `type` alone does not preserve it |
| `controls[].clickBehavior` | `clicked` / `declicked` / `switchable` | Click behavior of the ring |
| `controls[].rotationDegrees` | positive number | Nominal rotation angle of the ring |
| `controls[].geared` | boolean | Whether the ring has teeth, such as cinema gearing |
| `controls[].response` | `linear` / `nonlinear` / `switchable` | How an electronic ring responds to the amount of rotation |

## Accessories {#accessories}

`accessories` is an object or `null`.
When it is an object, it contains all six fields directly under it, and every field contains an array or `null`.

| Path | Type/value | Description |
| --- | --- | --- |
| `accessories.lensHoods` | relationship[] or `null` | Lens hoods |
| `accessories.frontCaps` | relationship[] or `null` | Front caps |
| `accessories.rearCaps` | relationship[] or `null` | Rear caps |
| `accessories.lensCases` | caseAccessory[] or `null` | Soft or hard cases |
| `accessories.lensStraps` | relationship[] or `null` | Lens straps |
| `accessories.protectiveWraps` | relationship[] or `null` | Protective wraps |
| `accessories.*[].modelNumberOptions` | string[] or `null` | Model numbers for the accessory confirmed in official materials. Required in every entry |
| `accessories.*[].quantity` | integer of 1 or greater | Quantity. Required in every entry |
| `relationship` for `accessories.lensHoods[]` and similar arrays | `supplied` / `optional` / `integrated` / `null` | Relationship between the product and its hood, cap, strap, or wrap |
| `accessories.lensCases[].relationship` | `supplied` / `optional` / `null` | Relationship between the product and the case |
| `accessories.lensCases[].construction` | `soft-case` / `hard-case` | Case construction |

## Related pages

- [Shared definitions](../shared/shared-definitions.md): definitions for IDs, numbers, measurement conditions, electronic services, tripod support, and attachment hosts
- [product-full](product-full.md): combination of common and product-type blocks
- [Lens and related optical product field reference](../../../lens-field-reference.md): explanations of each block using actual data

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/product-components.schema.json)
