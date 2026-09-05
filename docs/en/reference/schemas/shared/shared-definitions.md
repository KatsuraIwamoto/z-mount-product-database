# shared-definitions.schema.json

This JSON Schema collects definitions referenced by multiple JSON Schemas under `$defs`.
In addition to IDs and numbers, it defines focal lengths, measurement conditions, optical construction, electronic data, tripod support, movements, and related values.

It does not validate a standalone JSON file.
Each JSON Schema uses `$ref` to reference the definitions it needs.

<div class="grid cards" markdown>

-   :material-file-tree:{ .lg .middle } **Basic values**

    ---

    Find definitions for IDs, strings, numbers, regions, languages, image formats, and components present during measurement.

    [View basic values](#basic-values)

-   :material-swap-horizontal:{ .lg .middle } **Focal lengths and conditions**

    ---

    Find focal-length forms and the conditions under which a measurement applies.

    [View focal lengths and conditions](#focal-length-and-conditions)

-   :material-camera-iris:{ .lg .middle } **Optical values**

    ---

    Find definitions for f-numbers, T-stops, angles of view, optical construction, special elements, and coatings.

    [View optical values](#optical-values)

-   :material-magnify:{ .lg .middle } **Focus measurements and hosts**

    ---

    Find definitions for minimum focus distance, reproduction ratio, working distance, and attachment hosts.

    [View focus distances and reproduction ratios](#focus-measurements)

    [View hosts](#host)

-   :material-shield-outline:{ .lg .middle } **Environmental-protection claims**

    ---

    Find definitions for official dust-, drip-, weather-, and similar protection wording and its scope.

    [View environmental-protection claims](#environmentalclaim)

-   :material-connection:{ .lg .middle } **Electronic data and tripod support**

    ---

    Find definitions for metadata transmission, electronic services, tripod-support components, and mounting interfaces.

    [View electronic data](#electronic-data)

    [View tripod support](#tripod-support)

-   :material-axis-arrow:{ .lg .middle } **Movements**

    ---

    Find definitions for tilt angle, shift amount, and movable-assembly rotation range.

    [View movements](#movements)

</div>

## Example using shared definitions

The NIKKOR Z 24-70mm f/2.8 S II example below shows how shared definitions represent actual values.

Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

=== "Focal length"

    Location: `lens.focalLength`

    ```json
    {
      "kind": "zoom",
      "rangeMm": {
        "minimum": 24,
        "maximum": 70
      }
    }
    ```

=== "Angle of view and conditions"

    Location: `lens.anglesOfView[0]`

    ```json
    {
      "format": "full-frame",
      "orientation": "diagonal",
      "degrees": 84,
      "conditions": {
        "focalLength": {
          "kind": "point",
          "millimeters": 24
        }
      }
    }
    ```

=== "Maximum-aperture f-number with no additional conditions"

    Location: `lens.aperture.fNumber.maximumAperture[0]`

    ```json
    {
      "value": 2.8,
      "conditions": {}
    }
    ```

`focalLength` represents the product's nominal focal length.
The `conditions.focalLength` of a measurement indicates where on the focal-length range that value applies.
An empty `conditions` object means that there are no additional focal-length, focus-distance, or other conditions.

## Basic values {#basic-values}

| Definition | Type/value | Meaning |
| --- | --- | --- |
| `id` | `^[a-z0-9]+(?:-[a-z0-9]+)*$` | Lowercase alphanumeric ID with segments separated by hyphens |
| `nonEmptyString` | string of at least one character | String that cannot be empty |
| `positiveNumber` | number greater than 0 | Length, magnification, or another value that cannot be zero |
| `nonNegativeNumber` | number at least 0 | Number of stops, a magnification range, or another value that may be zero |
| `measurementComponent` | enum | One of `tripod-collar-assembly`, `tripod-foot`, `tripod-mount-cover`, `lens-hood`, `front-cap`, `rear-cap`, `drop-in-filter`, or `other`; a component present during a dimension or weight measurement |
| `region` | two-character uppercase code | Region code in ISO 3166-1 alpha-2 form |
| `language` | language tag | Language notation such as `ja`, `en`, or `en-US` |
| `imageFormat` | `full-frame` / `aps-c` / `super-35` / `other` | Image-format category |
| `coverage` | `{ "format": imageFormat }` or `null` | Largest image format covered by the product; `null` when accepted published evidence is unavailable |
| `modelNumberOptions` | string[] or `null` | Identifiers confirmed as model numbers in official sources; values cannot be duplicated. Use `null` when no model number can be confirmed from accepted published evidence |

Do not record JAN, EAN, or UPC codes, barcodes, SKUs, product numbers, catalog numbers, article numbers, or similar identifiers in `modelNumberOptions` unless the manufacturer or brand explicitly identifies them as model numbers.

## Focal lengths and conditions {#focal-length-and-conditions}

### `focalLengthCondition`

Represents a point or range on the focal-length scale to which a measurement applies.
It is not the focal-length specification of the lens itself.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `focalLengthCondition.kind` | `point` / `range` | Selects a single point or a range |
| `focalLengthCondition.millimeters` | positive number | Focal length in millimeters for `point` |
| `focalLengthCondition.minimumMm` | positive number | Lower bound of a `range` in millimeters |
| `focalLengthCondition.maximumMm` | positive number | Upper bound of a `range` in millimeters |

`point` requires `kind` and `millimeters`; `range` requires `kind`, `minimumMm`, and `maximumMm`.
The two shapes are mutually exclusive, so fields from the unselected shape are not permitted.

### `focalLength`

| Path | Type/value | Meaning |
| --- | --- | --- |
| `focalLength.kind` | `prime` / `zoom` / `interchangeable` | Prime, zoom, or interchangeable-component configuration |
| `focalLength.millimeters` | positive number or `null` | Nominal focal length of a prime lens in millimeters; `null` when the value is unpublished |
| `focalLength.rangeMm.minimum` | positive number | Wide-angle end of a zoom in millimeters |
| `focalLength.rangeMm.maximum` | positive number | Telephoto end of a zoom in millimeters |
| `focalLength.configurations` | object[] | Configurations for a product whose focal length changes with interchangeable components; at least two |
| `focalLength.configurations[].magnification` | positive number | Nominal reproduction ratio for the configuration |
| `focalLength.configurations[].millimeters` | positive number | Nominal focal length for the configuration in millimeters |

Record the following fields according to `kind`.

| `kind` | Fields to record |
| --- | --- |
| `prime` | `millimeters` |
| `zoom` | `rangeMm` |
| `interchangeable` | `configurations` |

`prime` requires `kind` and `millimeters`; `zoom` requires `kind` and `rangeMm`; `interchangeable` requires `kind` and `configurations`.
The three shapes are mutually exclusive, so fields from the unselected shapes are not permitted.
`configurations` must contain at least two distinct entries, each with `magnification` and `millimeters`.

### Condition objects

The conditions that can be attached to a measurement depend on the type of value.
Each key is optional, and an empty object `{}` means that there are no additional conditions.

| Definition | Conditions that can be recorded | Values that use it |
| --- | --- | --- |
| `apertureConditions` | Focal length, focus distance, reproduction ratio, camera, variant | F-numbers, T-stops |
| `angleConditions` | Focal length, camera, variant | Angles of view |
| `focusConditions` | Focal length, reproduction ratio, camera, variant | Minimum focus distances, reproduction ratios |
| `specializedConditions` | Focal length, focus distance, reproduction ratio, camera, variant | Working distances and other specialized specifications |

Condition objects combine the following keys.

| Key | Meaning | Condition definitions that permit it |
| --- | --- | --- |
| `focalLength` | Focal-length point or range at which the value applies | All |
| `focusDistanceM` | Focus distance in meters at which the value applies | `apertureConditions`, `specializedConditions` |
| `reproductionMagnification` | Reproduction ratio at which the value applies | `apertureConditions`, `focusConditions`, `specializedConditions` |
| `cameraBodyModel` | Camera body model for which the value applies | All |
| `variantId` | Product variant ID for which the value applies | All |

## Optical values {#optical-values}

### F-number and T-stop measurements {#aperture-measurements}

| Path | Type/value | Meaning |
| --- | --- | --- |
| `fNumberMeasurement.value` | positive number | F-number; `2.8` represents f/2.8 |
| `fNumberMeasurement.conditions` | `apertureConditions` | Conditions under which the f-number applies |
| `tNumberMeasurement.value` | positive number | T-stop; `2.9` represents T2.9 |
| `tNumberMeasurement.conditions` | `apertureConditions` | Conditions under which the T-stop applies |

### `angleOfView`

| Path | Type/value | Meaning |
| --- | --- | --- |
| `angleOfView.format` | `full-frame` / `aps-c` / `super-35` / `other` | Image format used to measure the angle of view |
| `angleOfView.orientation` | `diagonal` / `horizontal` / `vertical` / `null` | Diagonal, horizontal, or vertical; `null` when the official notation does not identify it |
| `angleOfView.degrees` | number greater than 0 and at most 360 | Angle of view in degrees |
| `angleOfView.conditions` | `angleConditions` | Focal-length, camera, and variant conditions |

### `opticalConstruction`

| Path | Type/value | Meaning |
| --- | --- | --- |
| `opticalConstruction.groups` | integer at least 1 or `null` | Number of optical groups |
| `opticalConstruction.elements` | integer at least 1 or `null` | Number of optical elements |

At least one of the group and element counts must be numeric.
If only one is officially published, record `null` for the other.
When both are numeric, `hatch run validate` checks that the group count does not exceed the element count.

### `specialElement`

| Path | Type/value | Meaning |
| --- | --- | --- |
| `specialElement.types` | enum[] | `low-dispersion`, `anomalous-partial-dispersion`, `aspherical`, `fluorite`, `high-refractive-index`, `diffractive-optical`, or `other` properties |
| `specialElement.officialName` | string, optional | Stable manufacturer designation such as ED, ED glass, FLD glass, PF lens, or XGM |
| `specialElement.quantity` | integer at least 1 or `null` | Number of special optical elements used; `null` when accepted published evidence does not establish the quantity |

### `coating`

| Path | Type/value | Meaning |
| --- | --- | --- |
| `coating.types` | enum[] | `anti-reflective`, `surface-protective`, `spectral-control`, or `other` purposes |
| `coating.officialName` | string, optional | Stable manufacturer designation for the coating; omit when the source provides only a generic description |
| `coating.appliedTo` | enum[] or `null` | `front-element`, `rear-element`, or `all-elements` application; `null` when it cannot be determined |

`types` provides cross-brand grouping, while `officialName` preserves the manufacturer's published terminology. Retain a stable technical designation in `officialName` even when both fields express the same general property. Interpret `officialName` within its brand and field; identical wording does not establish that technologies from different brands are the same. Differences limited to sentence capitalization, spacing, hyphenation, grammatical number, or generic suffixes do not create separate names. Prefer an official glossary, technology page, specification label, heading, badge, or marking on the product. Use an official English designation when an equivalent official English page exists; otherwise preserve the published designation rather than inventing a translation. Omit `®` and `™`, but preserve a symbol that is part of the designation itself, such as the asterisk in `T*`.

## Environmental-protection claims {#environmentalclaim}

`environmentalClaim` records dust-, drip-, weather-, and similar protection wording explicitly published by the manufacturer or brand, together with the scope to which it applies.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `environmentalClaim.types` | enum[] | One or more of `dust-resistant`, `drip-resistant`, `splash-resistant`, `moisture-resistant`, `weather-resistant`, `waterproof`, or `other` |
| `environmentalClaim.scope.kind` | `product` / `component` | Whether the wording applies to the whole product or only to a specific component |
| `environmentalClaim.scope.component` | string | Component to which the wording applies when `scope.kind: "component"`, such as a camera-side seal |
| `environmentalClaim.conditions` | [specializedConditions](#focal-length-and-conditions) | Variant or other conditions under which the wording applies; `{}` when there are no additional conditions |

When `scope.kind` is `product`, record only `kind` in `scope`.
When it is `component`, `component` is also required.
This definition structures official wording; it does not infer compliance with a test standard or complete waterproofing.

## Electronic data {#electronic-data}

### `metadataTransmission`

`metadataTransmission` records whether shooting metadata is transmitted and which published standards are used.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `metadataTransmission.present` | Boolean | Whether metadata transmission is present |
| `metadataTransmission.standards` | Array of `exif`, `cooke-i`, or `other`, or `null` | Published standards when transmission is present; `null` when no standard is established |

Use `{ "present": false }` when the absence of transmission is confirmed.
When transmission is present, both `present: true` and `standards` are required.
Use `null` when accepted published evidence does not establish whether transmission is present.

### `electronicServices`

`electronicServices` records published product firmware-update status and connection methods used for updates, configuration, or control.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `electronicServices.hasPublishedFirmwareUpdate` | Boolean or `null` | Whether a product firmware update has been published |
| `electronicServices.connections` | connection[] or `null` | Published connection methods; `[]` when checked and none apply |
| `electronicServices.connections[].method` | `camera-body` / `direct-usb` / `dock` / `other` | Connection method |
| `electronicServices.connections[].connectorType` | `usb-c` / `micro-usb` / `other` (optional) | Published connector type |
| `electronicServices.connections[].purposes` | Array of `firmware-update`, `configuration`, or `tethered-control` | Purposes of that connection |
| `electronicServices.connections[].application` | String (optional) | Published application name |

Use `electronicServices: null` when electronic services as a whole are not established.

## Tripod support {#tripod-support}

`tripodSupport` records whether tripod support is present and the components that have been established.
Lenses and mount adapters use the same definition.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `tripodSupport.present` | Boolean | Whether tripod support is present |
| `tripodSupport.components` | tripodSupportComponent[] or `null` | Support components; `null` when support is present but its component breakdown is not established |
| `tripodSupport.components[].type` | `collar-assembly` / `foot` / `support-bridge` / `support-bracket` / `body-mounting-point` / `other` | Component type |
| `tripodSupport.components[].relationship` | `integrated` / `supplied` / `optional` / `null` | Relationship to the product |
| `tripodSupport.components[].removable` | Boolean or `null` | Whether the component is removable |
| `tripodSupport.components[].interfaces` | tripodSupportInterface[] or `null` | Tripod-side mounting interfaces |
| `tripodSupport.components[].interfaces[].type` | `arca-compatible` / `mounting-thread` / `other` | Interface classification |
| `tripodSupport.components[].interfaces[].threadDesignation` | String or `null` | Published thread designation; required for `mounting-thread` |
| `tripodSupport.components[].modelNumberOptions` | string[] or `null` | Published model numbers |
| `tripodSupport.components[].quantity` | Integer of at least 1 or `null` | Quantity |
| `tripodSupport.components[].conditions` | [specializedConditions](#focal-length-and-conditions) | Variant or other applicable conditions |

Use `threadDesignation: null` for a `mounting-thread` whose thread specification is not established.
Use `{ "present": false }` when the absence of support is confirmed, and `null` when its presence is not established.

## Movements {#movements}

`movements` records tilt, shift, and the range through which a movable assembly can rotate around the optical axis.
The same definition is used for lenses and mount adapters.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `movements.tiltMeasurements` | tiltMeasurement[] or `null` | Nominal tilt amounts. At least one entry when known |
| `movements.tiltMeasurements[].maximumFromNeutralDegrees` | positive number or `null` | Maximum one-way tilt from neutral in degrees |
| `movements.tiltMeasurements[].totalRangeDegrees` | positive number or `null` | Total end-to-end tilt range in degrees |
| `movements.tiltMeasurements[].directionality` | `single-direction` / `bidirectional` / `null` | Published movement directionality |
| `movements.shiftMeasurements` | shiftMeasurement[] or `null` | Nominal shift amounts. At least one entry when known |
| `movements.shiftMeasurements[].maximumFromNeutralMm` | positive number or `null` | Maximum one-way shift from neutral in millimeters |
| `movements.shiftMeasurements[].totalRangeMm` | positive number or `null` | Total end-to-end shift range in millimeters |
| `movements.shiftMeasurements[].directionality` | `single-direction` / `bidirectional` / `null` | Published movement directionality |
| `movements.rotationMeasurements` | rotationMeasurement[] or `null` | Nominal rotation values around the optical axis. At least one entry when known |
| `movements.rotationMeasurements[].scope` | `product` / `movement-assembly` / `mount-interface` / `other` | What rotates |
| `movements.rotationMeasurements[].maximumFromNeutralDegrees` | number greater than 0 and at most 360, or `null` | Maximum one-way rotation from neutral in degrees |
| `movements.rotationMeasurements[].totalRangeDegrees` | number greater than 0 and at most 360, or `null` | Total end-to-end rotation range in degrees |
| `movements.rotationMeasurements[].directionality` | `single-direction` / `bidirectional` / `null` | Published rotation directionality |
| `movements.*Measurements[].conditions` | [specializedConditions](#focal-length-and-conditions) | Variant or other conditions under which the value applies |

`movements` contains at least one of `tiltMeasurements`, `shiftMeasurements`, and `rotationMeasurements`.
Measurement arrays cannot contain duplicate entries.
Every measurement requires either a numeric maximum from neutral or a numeric total range; use `null` for the other when it is not established.
`directionality` and `conditions` are also required; use `conditions: {}` when there are no additional conditions.
When the applicable movement mechanism is confirmed but its nominal amount is not, the corresponding value may be `null`.

## Focus distances and reproduction ratios {#focus-measurements}

| Path | Type/value | Meaning |
| --- | --- | --- |
| `minimumFocusDistance.distanceM` | positive number | Minimum focus distance from the image plane to the subject in meters |
| `minimumFocusDistance.conditions` | `focusConditions` | Focal-length and other measurement conditions |
| `reproductionMagnification.kind` | `maximum` / `fixed` / `range` / `discrete` | Maximum, fixed, continuous-range, or discrete representation |
| `reproductionMagnification.value` | non-negative number | Reproduction ratio for `maximum` or `fixed`; `1` represents 1:1 |
| `reproductionMagnification.minimum` | non-negative number | Lower reproduction-ratio bound for `range` |
| `reproductionMagnification.maximum` | non-negative number | Upper reproduction-ratio bound for `range` |
| `reproductionMagnification.values` | non-negative number[] | Published reproduction-ratio options for `discrete` |
| `reproductionMagnification.conditions` | `focusConditions` | Focal-length and other measurement conditions |
| `workingDistance.distanceM` | positive number | Working distance from the front of the lens or another stated reference point to the subject in meters |
| `workingDistance.conditions` | `specializedConditions` | Reproduction-ratio, focal-length, and other measurement conditions |

Each `minimumFocusDistance` and `workingDistance` entry requires both `distanceM` and `conditions`.
A `reproductionMagnification` uses `value` for `maximum` or `fixed`, `minimum` and `maximum` for `range`, or `values` for `discrete`; every shape also requires `kind` and `conditions`.
These shapes are mutually exclusive, and `values` must contain at least one value with no duplicates.

## Host {#host}

`host` indicates whether a filter or similar interface is attached to the product itself or to an external accessory.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `host.kind` | `product` / `accessory` | Product itself or an external accessory |
| `host.category` | `lens-hood` / `other` | Type of host when `kind` is `accessory` |
| `host.modelNumberOptions` | string[] or `null` | Model numbers confirmed in official material for the host accessory |

When `kind` is `product`, record only `kind`.
When it is `accessory`, `category` and `modelNumberOptions` are also required.

## Repository validation

`hatch run validate` also checks that the lower bound of a range does not exceed its upper bound.
This applies to `minimum` and `maximum` values for focal lengths, reproduction ratios, and similar ranges.
For optical construction, it also checks that `groups` does not exceed `elements`.

## Related pages

- [JSON Schema reference](../index.md): Overall JSON Schema structure and how to read the reference
- [How to interpret values](../../../value-rules.md): When to use `null`, an empty array, or `false`
- [Field reference for lenses and related optical products](../../../lens-field-reference.md): How these definitions appear in canonical records
- [Mount adapter field reference](../../../adapter-field-reference.md): Mount adapter fields that use shared definitions
- [JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/shared/shared-definitions.schema.json)
