# product-type-lens.schema.json

This schema validates the `lens` block of products with `productType: "lens"`.
Its structure combines general optical specifications with composable features such as cinema, anamorphic, and macro capabilities.

## Structure of the `lens` block

All top-level fields below except `imageCircleDiameters` and `zoom` are required.
Some required fields may be `null` when accepted published evidence is unavailable.
`zoom` is required when `focalLength.kind` is `zoom` and is prohibited when it is `prime`.

| Path | Contents |
| --- | --- |
| `lens.focalLength` | Focal length |
| `lens.aperture` | F-numbers, T-stops, diaphragm mechanism, and control mechanism |
| `lens.anglesOfView` | Angles of view by image format, orientation, and measurement conditions |
| `lens.coverage` | Largest image format covered |
| `lens.imageCircleDiameters` | Image circle diameters, added only when published |
| `lens.opticalConstruction` | Number of groups and elements in the complete lens |
| `lens.specialElements` | Special lens elements |
| `lens.coatings` | Coatings |
| `lens.focus` | Autofocus, manual focus, focusing system, focus distances, and reproduction ratios |
| `lens.zoom` | Zoom drive and optical zooming systems |
| `lens.stabilization` | In-lens image stabilization |
| `lens.specialized` | Composable features |

## Example of general lens specifications

The following example uses the NIKKOR Z 24-70mm f/2.8 S II to show how to record focal length, aperture, focus, and image stabilization.
The `specialized` section lists features permitted by the schema, including features not present in this product.

Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

=== "Focal length and aperture"

    Excerpt: `lens.focalLength`, `lens.aperture`

    ```json
    {
      "focalLength": {
        "kind": "zoom",
        "rangeMm": {
          "minimum": 24,
          "maximum": 70
        }
      },
      "aperture": {
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
    }
    ```

    In JSON, the officially stated f/2.8 is recorded as the number `2.8`.

=== "Focus, zoom, and image stabilization"

    Excerpt: `lens.focus.autofocus`, `lens.focus.manualFocus`, `lens.zoom`, `lens.stabilization`

    ```json
    {
      "focus": {
        "autofocus": {
          "present": true,
          "motors": [
            {
              "type": "voice-coil-motor",
              "quantity": null,
              "officialName": "Silky Swift VCM"
            }
          ]
        },
        "manualFocus": {
          "present": true,
          "mechanism": null
        }
      },
      "zoom": {
        "drive": null,
        "opticalZoomingSystems": null
      },
      "stabilization": {
        "present": false
      }
    }
    ```

    This product supports both autofocus and manual focus, and it does not have in-lens image stabilization.
    Accepted published evidence does not establish its zoom drive or optical zooming system, so both values are `null`.

## Optical specifications

| Path | Type/value | Description |
| --- | --- | --- |
| `lens.focalLength` | [focalLength](../shared/shared-definitions.md#focal-length-and-conditions) or `null` | Single focal length, zoom range, or focal-length configurations for interchangeable components |
| `lens.anglesOfView` | [angleOfView](../shared/shared-definitions.md#optical-values)[] or `null` | Official angles of view by image format, orientation, and focal-length condition. If known, the array contains at least one entry |
| `lens.coverage` | [coverage](../shared/shared-definitions.md#basic-values) | Largest image format covered by the lens |
| `lens.imageCircleDiameters` | measurement[] or `null` | Officially published image circle diameters. The field itself is optional; if known, the array contains at least one entry |
| `lens.imageCircleDiameters[].diameterMm` | positive number | Image circle diameter in millimeters |
| `lens.imageCircleDiameters[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | Measurement conditions such as focal length and focus distance |
| `lens.opticalConstruction` | [opticalConstruction](../shared/shared-definitions.md#opticalconstruction) or `null` | Number of groups and elements in the complete lens |
| `lens.specialElements` | [specialElement](../shared/shared-definitions.md#specialelement)[] or `null` | Special lens elements. Types and quantities may be recorded without a distinct official name. After checking the list, use `[]` if none apply |
| `lens.coatings` | [coating](../shared/shared-definitions.md#coating)[] or `null` | Coatings. Types and application may be recorded without a distinct official name. After checking the list, use `[]` if none apply |

## Aperture {#aperture}

`lens.aperture` records F-numbers, T-stops, the diaphragm mechanism, and the control mechanism separately.
`fNumber`, `diaphragm`, and `controlMechanism` are required. Only products with published T-stops contain `tNumber`.

### F-numbers and T-stops

`fNumber` is an object or `null`.
When it is an object, it contains `maximumAperture`, `minimumAperture`, and `effective`.
`tNumber` uses the same structure, but the field itself is optional.

| Path | Type/value | Description |
| --- | --- | --- |
| `lens.aperture.fNumber.maximumAperture` | f-number measurement[] or `null` | Nominal maximum aperture. If known, the array contains at least one entry |
| `lens.aperture.fNumber.minimumAperture` | f-number measurement[] or `null` | Nominal minimum aperture. If known, the array contains at least one entry |
| `lens.aperture.fNumber.effective` | object or `null` | Effective f-numbers published for close focus or other conditions |
| `lens.aperture.fNumber.effective.maximumAperture` | f-number measurement[] or `null` | Conditional effective maximum aperture |
| `lens.aperture.fNumber.effective.minimumAperture` | f-number measurement[] or `null` | Conditional effective minimum aperture |
| `lens.aperture.tNumber.maximumAperture` | T-stop measurement[] or `null` | Nominal maximum aperture expressed as a T-stop |
| `lens.aperture.tNumber.minimumAperture` | T-stop measurement[] or `null` | Nominal minimum aperture expressed as a T-stop |
| `lens.aperture.tNumber.effective` | object or `null` | Conditional effective T-stops. When it is an object, `maximumAperture` and `minimumAperture` are required |

For `value` and `conditions` in each measurement, see [F-number and T-stop measurements](../shared/shared-definitions.md#aperture-measurements).

### Diaphragm mechanism

| `lens.aperture.diaphragm` | Permitted structure |
| --- | --- |
| `null` | Accepted published evidence does not establish whether an adjustable diaphragm is present |
| `{ "present": false }` | The lens has no adjustable diaphragm |
| `{ "present": true, ... }` | `bladeCount` and `bladeShape` are required |

| Path | Type/value | Description |
| --- | --- | --- |
| `lens.aperture.diaphragm.present` | boolean | Whether an adjustable diaphragm is present |
| `lens.aperture.diaphragm.bladeCount` | integer of 1 or greater, or `null` | Number of diaphragm blades |
| `lens.aperture.diaphragm.bladeShape` | `rounded` / `straight` / `other` / `null` | Diaphragm blade shape |
| `lens.aperture.controlMechanism` | `mechanical` / `electronic` / `null` | Method used by the camera to actuate the aperture |

## Focus {#focus}

`autofocus`, `manualFocus`, `opticalFocusingSystems`, `minimumFocusDistances`, `reproductionMagnifications`, and `officialFocusBehaviorClaims` are all required.

### Autofocus and manual focus

| Path | Type/value | Description |
| --- | --- | --- |
| `lens.focus.autofocus` | object or `null` | Presence of autofocus and its drive motors |
| `lens.focus.autofocus.present` | boolean | Whether autofocus is supported |
| `lens.focus.autofocus.motors` | motor[] or `null` | Autofocus motors. Required when `present: true` |
| `lens.focus.autofocus.motors[].type` | `stepping-motor` / `voice-coil-motor` / `linear-motor` / `ultrasonic-motor` / `dc-motor` / `other` | Motor type |
| `lens.focus.autofocus.motors[].officialName` | string, optional | Stable manufacturer technical designation such as Stepping Motor (STM), Silky Swift VCM, or VXD. `type` provides cross-brand grouping, while `officialName` preserves the manufacturer's published terminology |
| `lens.focus.autofocus.motors[].quantity` | integer of 1 or greater, or `null` | Number of motors. Required in every entry |
| `lens.focus.manualFocus` | object or `null` | Presence of manual focus and its operating mechanism |
| `lens.focus.manualFocus.present` | boolean | Whether manual focus is supported |
| `lens.focus.manualFocus.mechanism` | `mechanical-coupled` / `electronic-by-wire` / `null` | Manual-focus mechanism. Required when `present: true` |

Autofocus and manual focus each use the following three states.

| State | Structure |
| --- | --- |
| Accepted published evidence is unavailable | `null` |
| Confirmed as unsupported | `{ "present": false }` |
| Confirmed as supported | `{ "present": true, ... }` |

### Focusing systems and focus specifications

| Path | Type/value | Description |
| --- | --- | --- |
| `lens.focus.opticalFocusingSystems` | system[] or `null` | Focusing systems used by the optical groups. After checking the list, use `[]` if none apply |
| `lens.focus.opticalFocusingSystems[].type` | `all-element-focusing` / `front-focusing` / `internal-focusing` / `rear-focusing` / `multiple-group-focusing` / `floating` / `other` | Focusing system |
| `lens.focus.opticalFocusingSystems[].officialName` | string, optional | Stable manufacturer technical designation such as Internal Focusing system, IF, or Multi-focusing system. `type` provides cross-brand grouping, while `officialName` preserves the manufacturer's published terminology |
| `lens.focus.minimumFocusDistances` | [minimumFocusDistance](../shared/shared-definitions.md#focus-measurements)[] or `null` | Minimum focus distances measured from the image plane. If known, the array contains at least one entry |
| `lens.focus.reproductionMagnifications` | [reproductionMagnification](../shared/shared-definitions.md#focus-measurements)[] or `null` | Nominal reproduction ratios. If known, the array contains at least one entry |
| `lens.focus.officialFocusBehaviorClaims` | claim[] or `null` | Manufacturer claims of suppressed focus breathing or parfocal performance. After checking the list, use `[]` if no wording applies |
| `lens.focus.officialFocusBehaviorClaims[].type` | `focus-breathing-suppressed` / `parfocal` | Type of official claim |
| `lens.focus.officialFocusBehaviorClaims[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | Conditions under which the claim applies |

## Zoom {#zoom}

Every zoom lens requires `lens.zoom`.
If accepted published evidence does not establish the drive or optical zooming system, retain the field and use `null`.

| Path | Type/value | Description |
| --- | --- | --- |
| `lens.zoom.drive` | `manual` / `motorized` / `manual-and-motorized` / `null` | Zoom drive |
| `lens.zoom.opticalZoomingSystems` | system[] or `null` | Published optical zooming systems; use `[]` when checked and none apply |
| `lens.zoom.opticalZoomingSystems[].type` | `internal-zooming` / `other` | Optical zooming-system classification |
| `lens.zoom.opticalZoomingSystems[].officialName` | string (optional) | Stable manufacturer technical designation |

Prime lenses omit `lens.zoom`.

## Image stabilization {#stabilization}

| `lens.stabilization` | Permitted structure |
| --- | --- |
| `null` | Accepted published evidence does not establish whether in-lens image stabilization is present |
| `{ "present": false }` | The lens is confirmed not to have in-lens image stabilization |
| `{ "present": true, "ratings": ... }` | In-lens image stabilization is confirmed. `ratings` is required |

| Path | Type/value | Description |
| --- | --- | --- |
| `lens.stabilization.present` | boolean | Whether in-lens image stabilization is present |
| `lens.stabilization.officialName` | string, optional | Stable manufacturer designation such as VR, OS, or VC |
| `lens.stabilization.ratings` | rating[] or `null` | Nominal stabilization rating in stops. Use `null` when accepted published evidence does not establish a value |
| `lens.stabilization.ratings[].stops` | nonnegative number | Nominal stabilization effectiveness in stops |
| `lens.stabilization.ratings[].conditions.focalLength` | [focalLengthCondition](../shared/shared-definitions.md#focallengthcondition) | Focal length used for the evaluation |
| `lens.stabilization.ratings[].conditions.imageFormat` | [imageFormat](../shared/shared-definitions.md#basic-values) | Image format used for the evaluation |
| `lens.stabilization.ratings[].conditions.cameraBodyModel` | string | Camera model used for the evaluation |
| `lens.stabilization.ratings[].conditions.configuration` | `lens-only` / `lens-and-body` / `unspecified` | Whether the rating is for the lens alone or for coordinated lens and body stabilization |
| `lens.stabilization.ratings[].conditions.standard` | string | Name of the evaluation standard, such as CIPA |
| `lens.stabilization.ratings[].conditions.standardVersion` | string | Version or year of the evaluation standard |
| `lens.stabilization.ratings[].conditions.mode` | string | Evaluation mode, such as Normal or Sport |
| `lens.stabilization.ratings[].conditions.measurementAxes` | integer of 1 or greater | Number of axes evaluated |
| `lens.stabilization.ratings[].conditions.evaluationPosition` | `center` / `center-and-peripheral` | Position in the frame used for the evaluation |

Every element of `ratings[]` requires `stops` and `conditions`.
Within `conditions`, record only the published conditions.

## Composable features {#specialized}

`lens.specialized` is required, but record `{}` when no feature applies.
A product may combine several features, such as cinema, anamorphic, and macro capabilities, without being limited to a single subtype.

| Path | Type/value | Description |
| --- | --- | --- |
| `lens.specialized.cinema` | `{}` | Product officially positioned for cinema use |
| `lens.specialized.reflex` | `{}` | Product with a reflex optical system |
| `lens.specialized.anamorphic` | object | Anamorphic specifications |
| `lens.specialized.fisheye` | object | Fisheye image specifications |
| `lens.specialized.macro` | object | Macro specifications |
| `lens.specialized.movements` | object | Tilt, shift, and rotation mechanisms |
| `lens.specialized.probe` | object | Viewing direction and integrated lighting for a probe lens |
| `lens.specialized.builtInTeleconverter` | object | Built-in teleconverter and specifications when engaged |

### Anamorphic, fisheye, and macro

| Path | Type/value | Description |
| --- | --- | --- |
| `lens.specialized.anamorphic.squeezeRatios` | measurement[] or `null` | Nominal squeeze ratios. If known, the array contains at least one entry |
| `lens.specialized.anamorphic.squeezeRatios[].value` | positive number | Squeeze ratio |
| `lens.specialized.anamorphic.squeezeRatios[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | Conditions under which the ratio applies |
| `lens.specialized.fisheye.imageTypes` | measurement[] or `null` | Nominal fisheye image types. If known, the array contains at least one entry |
| `lens.specialized.fisheye.imageTypes[].type` | `circular` / `diagonal` | Circular or diagonal fisheye |
| `lens.specialized.fisheye.imageTypes[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | Conditions such as image format and focal length |
| `lens.specialized.macro.workingDistances` | [workingDistance](../shared/shared-definitions.md#focus-measurements)[] or `null` | Distance from the front of the lens or another stated reference point to the subject. If known, the array contains at least one entry |

### Lens movements

`lens.specialized.movements` uses the [shared `movements` definition](../shared/shared-definitions.md#movements) and contains at least one of `tiltMeasurements`, `shiftMeasurements`, and `rotationMeasurements`.

| Path | Type/value | Description |
| --- | --- | --- |
| `lens.specialized.movements.tiltMeasurements` | measurement[] or `null` | Nominal tilt angles. If known, the array contains at least one entry |
| `lens.specialized.movements.tiltMeasurements[].maximumFromNeutralDegrees` | positive number or `null` | Maximum one-way tilt from neutral in degrees |
| `lens.specialized.movements.tiltMeasurements[].totalRangeDegrees` | positive number or `null` | Total end-to-end tilt range in degrees |
| `lens.specialized.movements.tiltMeasurements[].directionality` | `single-direction` / `bidirectional` / `null` | Published movement directionality |
| `lens.specialized.movements.tiltMeasurements[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | Conditions under which the value applies |
| `lens.specialized.movements.shiftMeasurements` | measurement[] or `null` | Nominal shift distances. If known, the array contains at least one entry |
| `lens.specialized.movements.shiftMeasurements[].maximumFromNeutralMm` | positive number or `null` | Maximum one-way shift from neutral in millimeters |
| `lens.specialized.movements.shiftMeasurements[].totalRangeMm` | positive number or `null` | Total end-to-end shift range in millimeters |
| `lens.specialized.movements.shiftMeasurements[].directionality` | `single-direction` / `bidirectional` / `null` | Published movement directionality |
| `lens.specialized.movements.shiftMeasurements[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | Conditions under which the value applies |
| `lens.specialized.movements.rotationMeasurements` | measurement[] or `null` | Nominal rotation of a movement mechanism or other scope |
| `lens.specialized.movements.rotationMeasurements[].scope` | `product` / `movement-assembly` / `mount-interface` / `other` | What rotates |
| `lens.specialized.movements.rotationMeasurements[].maximumFromNeutralDegrees` | number greater than 0 and at most 360, or `null` | Maximum one-way rotation from neutral in degrees |
| `lens.specialized.movements.rotationMeasurements[].totalRangeDegrees` | number greater than 0 and at most 360, or `null` | Total end-to-end rotation range in degrees |
| `lens.specialized.movements.rotationMeasurements[].directionality` | `single-direction` / `bidirectional` / `null` | Published rotation directionality |
| `lens.specialized.movements.rotationMeasurements[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | Conditions under which the value applies |

### Probe

The presence of the `lens.specialized.probe` key identifies a probe lens.
Use `{}` even when no viewing-direction or lighting information is available.

| Path | Type/value | Description |
| --- | --- | --- |
| `lens.specialized.probe.viewConfigurations` | configuration[] or `null` | Published viewing directions. If known, the array contains at least one entry |
| `lens.specialized.probe.viewConfigurations[].directionDegrees` | number from 0 through 360 | Viewing direction with straight ahead defined as 0 degrees |
| `lens.specialized.probe.viewConfigurations[].relationship` | `supplied` / `optional` / `integrated` / `null` | Relationship between the viewing-direction unit and the product |
| `lens.specialized.probe.viewConfigurations[].axialRotationDegrees` | nonnegative number | Axial rotation angle of the viewing-direction unit |
| `lens.specialized.probe.integratedLights` | light[] or `null` | Integrated lighting. After checking the list, use `[]` if no lights apply |
| `lens.specialized.probe.integratedLights[].type` | `led` / `other` | Type of light |
| `lens.specialized.probe.integratedLights[].location` | string | Location of the light |
| `lens.specialized.probe.integratedLights[].quantity` | integer of 1 or greater | Number of lights |

### Built-in teleconverter

`magnification`, `unitOpticalConstruction`, and `engagedSpecifications` are required within `lens.specialized.builtInTeleconverter`.
`engagedSpecifications` records only the specifications that change when the built-in teleconverter is engaged.

| Path | Type/value | Description |
| --- | --- | --- |
| `lens.specialized.builtInTeleconverter.magnification` | positive number | Nominal magnification of the built-in teleconverter |
| `lens.specialized.builtInTeleconverter.unitOpticalConstruction` | [opticalConstruction](../shared/shared-definitions.md#opticalconstruction) or `null` | Number of groups and elements in the teleconverter unit alone |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.focalLength` | [focalLength](../shared/shared-definitions.md#focal-length-and-conditions) or `null` | Focal length with the teleconverter engaged |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.aperture` | object or `null` | F-numbers and T-stops with the teleconverter engaged. Do not duplicate the diaphragm mechanism |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.aperture.fNumber` | object or `null` | F-numbers with the teleconverter engaged. When it is an object, it uses the same structure as the standard `fNumber` block |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.aperture.tNumber` | object | T-stops with the teleconverter engaged. Record only when applicable |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.anglesOfView` | [angleOfView](../shared/shared-definitions.md#optical-values)[] or `null` | Angles of view with the teleconverter engaged |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.minimumFocusDistances` | [minimumFocusDistance](../shared/shared-definitions.md#focus-measurements)[] or `null` | Minimum focus distances with the teleconverter engaged |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.reproductionMagnifications` | [reproductionMagnification](../shared/shared-definitions.md#focus-measurements)[] or `null` | Reproduction ratios with the teleconverter engaged |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.stabilizationRatings` | rating[] or `null` | Image-stabilization ratings in stops with the teleconverter engaged |

All six fields in `engagedSpecifications` are required.
Use `null` when a value has not been published. Arrays that can represent a checked list with no applicable entries may also use `[]`.

## Related pages

- [Shared definitions](../shared/shared-definitions.md): focal length, measurement conditions, optical construction, and focus specifications
- [product-components](product-components.md): identity, mount, and physical information shared with lenses
- [Lens and related optical product field reference](../../../lens-field-reference.md): examples of general lenses and `specialized` features

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/product-type-lens.schema.json)
