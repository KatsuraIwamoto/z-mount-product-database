# Field reference for lenses and related optical products

This page explains the canonical records for lenses and related optical products and the fields included in each product entry in the distribution data.
You do not need to read it from beginning to end; use the product type or field name to find the section you need.

To first review the relationship between canonical records, Lens Full, and Lens Light, see the [data model](data-model.md).

!!! info "Lens Full and Lens Light"

    The `products` array in Lens Full contains the contents of each canonical record with `$schema` removed.
    Lens Light contains the same products in the same order but retains only a subset of the fields.
    See [Lens Full and Lens Light](value-rules.md#lens-full-and-light) for how values are retained and the [Lens Light JSON Schema reference](reference/schemas/lenses/product-light.md) for the retained fields.

The JSON examples on this page contain only the portions needed for each explanation, taken from actual canonical records or distribution data.
Some examples show only part of an array.
See the [JSON Schema reference](reference/schemas/index.md) for field types, required fields, and permitted values.

Mount adapters use a different data structure and are documented in the [mount adapter field reference](adapter-field-reference.md).

## Product types and blocks

`productType` identifies the product type.
Product-specific information is stored in the block with the same name as `productType`.

| Product type | `productType` | Product-type block | Example on this page |
| --- | --- | --- | --- |
| Lens | `lens` | `lens` | NIKKOR Z 24-70mm f/2.8 S II |
| Teleconverter | `teleconverter` | `teleconverter` | Z TELECONVERTER TC-2.0x |
| Pinhole | `pinhole` | `pinhole` | Lensbaby Obscura 16 |

=== "Lens"

    The following example shows how the product type and product-type block are recorded for the NIKKOR Z 24-70mm f/2.8 S II.

    Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

    ```json
    {
      "id": "nikkor-z-24-to-70mm-f2p8-s-ii",
      "productType": "lens",
      "lens": {
        "focalLength": {
          "kind": "zoom",
          "rangeMm": {
            "minimum": 24,
            "maximum": 70
          }
        }
      }
    }
    ```

=== "Teleconverter"

    The following example shows how the product type and product-type block are recorded for the Z TELECONVERTER TC-2.0x.

    Source: `data/records/lenses/nikon/z-teleconverter-tc-2p0x.json`

    ```json
    {
      "id": "z-teleconverter-tc-2p0x",
      "productType": "teleconverter",
      "teleconverter": {
        "magnification": 2
      }
    }
    ```

=== "Pinhole"

    The following example shows how the product type and product-type block are recorded for the Lensbaby Obscura 16.

    Source: `data/records/lenses/lensbaby/lensbaby-obscura-16.json`

    ```json
    {
      "id": "lensbaby-obscura-16",
      "productType": "pinhole",
      "pinhole": {
        "focalLength": {
          "kind": "fixed",
          "millimeters": 16
        }
      }
    }
    ```

Each product contains only the `lens`, `teleconverter`, or `pinhole` block that corresponds to its `productType`.

## Common fields

Identity, publication information, mount, physical characteristics, controls, and accessories are recorded in the same locations for every product type.

| Field | Information recorded |
| --- | --- |
| `id` | ID used to identify the product |
| `productType` | Product type and the product-type block used |
| `identity` | Manufacturer ID, brand ID, official product name, official model numbers, official alternate names, and variants of the same product |
| `lifecycle` | Official product release announcement date and official status designations from the manufacturer or brand, such as legacy, sales ended, production ended, or discontinued |
| `officialProductPages` | Official main pages for the product, together with their region, language, and publisher |
| `mount` | Mount system, attachment method, electronic contacts, and a Z-mount adapter supplied with or officially designated for the product |
| `electronicServices` | Whether a firmware update has been published and connections used for updates, configuration, or control |
| `physical` | Dimensions, weight, official environmental-protection claims, filter attachment interfaces, tripod support, and external changes during zoom or focus |
| `controls` | Controls such as focus rings, buttons, and switches |
| `accessories` | Supplied or compatible accessories such as hoods, caps, and cases |

### Identity and publication information (`identity`, `lifecycle`, and `officialProductPages`)

The following example shows how identity, the product release announcement date, and official product pages are recorded for the NIKKOR Z 24-70mm f/2.8 S II.

Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "id": "nikkor-z-24-to-70mm-f2p8-s-ii",
  "productType": "lens",
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
  },
  "officialProductPages": [
    {
      "url": "https://nij.nikon.com/products/lineup/nikkor/zmount/nikkor_z_24-70mm_f28_s_2/",
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
In this example, `nikon` represents Nikon and `nikkor` represents NIKKOR.
In a distribution JSON, display names are available from the root `referenceData` object.
`identity.productName` preserves the official spelling of the product name.

`lifecycle.announcementDate` is the official product release announcement date.
A development-announcement date is not used in its place.
`lifecycle.officialDesignations: []` means that no official status designations were confirmed.
It does not mean that the product is currently sold, in stock, or available.
A deleted official product page alone is not treated as evidence that sales have ended.

The distinction between pages included in `officialProductPages` and other sources used for research is explained under [URLs and sources](value-rules.md#urls).

### Mount (`mount`)

The following example shows how the mount and electronic contacts are recorded for the NIKKOR Z 24-70mm f/2.8 S II.

Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "mount": {
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
}
```

`systemId` contains an ID defined in the mount-system registry.
In this example, `replaceability` and `electronicContacts` indicate that the product has a fixed Nikon Z mount and electronic contacts.
Here, `mount-owner` means that the product manufacturer also provides the Nikon Z mount system.

#### Adapters recorded under `mount.adapter`

`mount.adapter` records a Z-mount adapter supplied with the product.
It also covers a Z-mount adapter officially designated by the manufacturer for that lens or product series.
This is mounting information in a canonical record for a lens or related optical product, not a canonical mount adapter record.
Adapters intended for a broad range of lenses, such as FTZ, are not recorded under `mount.adapter`.

The following example shows how a Z-mount adapter supplied with the SZX SUPER TELE 400mm F8 Reflex MF is recorded.

Source: `data/records/lenses/tokina/tokina-szx-super-tele-400mm-f8-reflex-mf.json`

```json
{
  "mount": {
    "adapter": {
      "relationship": "supplied",
      "dedicatedToProduct": null,
      "nativeMountSystemId": "t-mount",
      "name": "Tokina Mount Adapter TA-016 for Nikon Z",
      "modelNumberOptions": [
        "TA-016",
        "TA-0016",
        "SZX-TA0016"
      ]
    }
  }
}
```

In this example, `relationship: "supplied"` indicates that the Tokina Mount Adapter TA-016 for Nikon Z is supplied with the product.

### Firmware updates and connections (`electronicServices`)

The following example shows how the availability of published firmware updates and connections used for updates, configuration, or control are recorded for the NIKKOR Z 24-70mm f/2.8 S II.

Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "electronicServices": {
    "hasPublishedFirmwareUpdate": null,
    "connections": null
  }
}
```

`hasPublishedFirmwareUpdate: null` means that accepted published evidence did not establish whether a product firmware update had been published.
`connections: null` means that the connection methods could not be confirmed from accepted published evidence.
`electronicServices` is independent of the mount contacts. A product without mount contacts may still record an officially published USB connection, dock, or other direct service.

### Physical characteristics (`physical`)

The following example shows how dimensions, weight, the filter interface, and changes in the barrel's external length are recorded for the NIKKOR Z 24-70mm f/2.8 S II.

Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "physical": {
    "dimensionMeasurements": [
      {
        "maximumDiameterMm": 84,
        "lengthMm": 142,
        "conditions": {}
      }
    ],
    "weightMeasurements": [
      {
        "grams": 675,
        "conditions": {
          "attachedComponents": []
        }
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
    "filterInterfaces": [
      {
        "type": "front-thread",
        "diameterMm": 77,
        "host": {
          "kind": "product"
        }
      }
    ],
    "tripodSupport": {
      "present": false
    },
    "externalLengthDuringZoom": "constant",
    "externalLengthDuringFocus": "constant",
    "isRetractableForStorage": false
  }
}
```

In this example, the maximum diameter is 84 mm and the length is 142 mm.
The weight is 675 g, and the front filter thread diameter is 77 mm.
`officialEnvironmentalProtectionClaims` records the officially stated dust- and drip-resistant performance of the product as a whole.
The `constant` values for `externalLengthDuringZoom` and `externalLengthDuringFocus` mean that the barrel's external length does not change during zoom or focus operation.
`tripodSupport.present: false` means that no tripod mounting hardware is present, and `isRetractableForStorage: false` means that the product has no storage mechanism that must be extended before use.
When tripod support is present, `tripodSupport.components` keeps its collar, foot, mounting interface, product relationship, and removability together.
Measurement conditions are explained under [Numbers and conditions](value-rules.md#numbers-and-conditions), and states such as `null` are explained under [Value states](value-rules.md#value-states).

### Controls and accessories (`controls` and `accessories`)

The following example shows how controls on the product and accessories are recorded for the NIKKOR Z 24-70mm f/2.8 S II.

Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "controls": [
    {
      "type": "focus-ring",
      "quantity": 1
    }
  ],
  "accessories": {
    "lensHoods": [
      {
        "relationship": "supplied",
        "modelNumberOptions": [
          "HB-117"
        ],
        "quantity": 1
      }
    ]
  }
}
```

## The `lens` block

The `lens` block records optical specifications, focus, stabilization, and specialized features.
Photographic and cinema lenses use the same `lens` block; their differences are represented by the values and combinations of fields they require.

| Field | Information recorded |
| --- | --- |
| `focalLength` | Prime focal length, zoom range, or multiple discrete focal lengths |
| `aperture` | F-number or T-stop, diaphragm, and aperture-control mechanism |
| `anglesOfView` | Angle of view by image format, orientation, and measurement conditions |
| `coverage` | Largest supported image format |
| `imageCircleDiameters` | Published image-circle diameters and their measurement conditions |
| `opticalConstruction` | Number of element groups and elements |
| `specialElements` | Types, official names, and quantities of special elements |
| `coatings` | Types, official names, and application locations of coatings |
| `focus` | Autofocus, manual focus, focusing systems, minimum focus distances, maximum reproduction ratios, and official focus-behavior claims |
| `zoom` | Zoom drive and optical zooming systems such as internal zooming; recorded only for zoom lenses |
| `stabilization` | Presence of stabilization, published stop ratings, and official name |
| `specialized` | Composable features such as macro, fisheye, cinema, and anamorphic |

The `conditions` attached to numeric values are explained under [Numbers and conditions](value-rules.md#numbers-and-conditions).
See [Lens Full and Lens Light](value-rules.md#lens-full-and-light) for the focus information retained in Lens Light.

!!! info "How to read the examples"

    Each JSON example is extracted from one canonical record.
    Values from multiple lenses are not combined into a single JSON example.
    The NIKKOR Z 24-70mm f/2.8 S II is used as the main example; other lenses are used only for fields that it cannot illustrate.

### Focal length and aperture (`focalLength` and `aperture`)

The following example shows how the focal length and aperture of the NIKKOR Z 24-70mm f/2.8 S II zoom lens are recorded.

Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "lens": {
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
}
```

In this example, the 24-70 mm focal-length range is recorded under `focalLength.rangeMm`.
The maximum aperture that Nikon denotes as f/2.8 is recorded numerically as `maximumAperture[].value: 2.8`.
Likewise, the minimum aperture of f/22 is recorded as `minimumAperture[].value: 22`.

### Largest image format and angle of view (`coverage` and `anglesOfView`)

The following example shows how the largest supported image format and the angle of view at each focal length are recorded for the NIKKOR Z 24-70mm f/2.8 S II.

Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "lens": {
    "coverage": {
      "format": "full-frame"
    },
    "anglesOfView": [
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
    ]
  }
}
```

In this example, `anglesOfView` records a diagonal angle of view of 84 degrees at the 24 mm wide-angle end.

### Optical construction (`opticalConstruction`, `specialElements`, and `coatings`)

The following example shows how element groups, elements, special elements, and coatings are recorded for the NIKKOR Z 24-70mm f/2.8 S II.

Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "lens": {
    "opticalConstruction": {
      "groups": 10,
      "elements": 14
    },
    "specialElements": [
      {
        "types": [
          "low-dispersion"
        ],
        "officialName": "ED glass",
        "quantity": 2
      }
    ],
    "coatings": [
      {
        "types": [
          "anti-reflective"
        ],
        "officialName": "Meso Amorphous Coat",
        "appliedTo": null
      }
    ]
  }
}
```

### Focus and zoom (`focus`, `zoom`)

The following example shows how autofocus (AF), manual focus (MF), focusing systems, minimum focus distances, and maximum reproduction ratios are recorded for the NIKKOR Z 24-70mm f/2.8 S II.

Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "lens": {
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
      },
      "opticalFocusingSystems": [
        {
          "type": "internal-focusing",
          "officialName": "Internal Focusing system"
        },
        {
          "type": "multiple-group-focusing",
          "officialName": "Multi-focusing system"
        }
      ],
      "minimumFocusDistances": [
        {
          "distanceM": 0.24,
          "conditions": {
            "focalLength": {
              "kind": "point",
              "millimeters": 24
            }
          }
        }
      ],
      "reproductionMagnifications": [
        {
          "kind": "maximum",
          "value": 0.32,
          "conditions": {
            "focalLength": {
              "kind": "point",
              "millimeters": 70
            }
          }
        }
      ],
      "officialFocusBehaviorClaims": [
        {
          "type": "focus-breathing-suppressed",
          "conditions": {}
        }
      ]
    },
    "zoom": {
      "drive": null,
      "opticalZoomingSystems": null
    }
  }
}
```

`opticalFocusingSystems` records the focusing systems published by the manufacturer.
The minimum focus distance and maximum reproduction ratio are associated with their respective focal lengths through `conditions`.
`officialFocusBehaviorClaims` records the official statement that focus breathing is suppressed.
Every zoom lens has a `zoom` object.
`drive` records manual, motorized, or combined operation, while `opticalZoomingSystems` records published systems such as internal zooming.
The `null` values in this example mean that accepted published evidence does not establish either property.
Prime lenses omit `zoom`.

### Stabilization (`stabilization`)

`stabilization` records whether in-lens stabilization is present, together with any published stop ratings and official name.
When its presence or absence can be confirmed, `present` is set to `true` or `false`.

=== "Present"

    The following example shows how confirmed in-lens stabilization is recorded for the NIKKOR Z 400mm f/2.8 TC VR S.

    Source: `data/records/lenses/nikkor/nikkor-z-400mm-f2p8-tc-vr-s.json`

    ```json
    {
      "lens": {
        "stabilization": {
          "present": true,
          "ratings": [
            {
              "stops": 5.5,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 400
                },
                "standard": "CIPA",
                "mode": "Normal",
                "imageFormat": "full-frame"
              }
            }
          ],
          "officialName": "Vibration Reduction"
        }
      }
    }
    ```

    `present: true` means that the presence of in-lens stabilization was confirmed.
    `ratings` records the published stop rating together with its focal-length, measurement-standard, stabilization-mode, and measurement-format conditions.

=== "Absent"

    When accepted published evidence confirms that a product has no in-lens stabilization, it is recorded as follows.

    ```json
    {
      "lens": {
        "stabilization": {
          "present": false
        }
      }
    }
    ```

    `present: false` means that accepted published evidence confirmed the absence of in-lens stabilization.

`stabilization` is `null` only when accepted published evidence does not establish whether stabilization is present.
See [Value states](value-rules.md#value-states) for how these states are used.

### Cinema-lens specifications

The following example shows how the T-stop, image-circle diameter, and cinema-lens feature are recorded for the LAOWA Argus 33mm T1 S35 Cine.

Source: `data/records/lenses/laowa/laowa-argus-33mm-t1-s35-cine.json`

```json
{
  "lens": {
    "aperture": {
      "fNumber": null,
      "tNumber": {
        "maximumAperture": [
          {
            "value": 1,
            "conditions": {}
          }
        ],
        "minimumAperture": [
          {
            "value": 11,
            "conditions": {}
          }
        ],
        "effective": null
      },
      "diaphragm": {
        "present": true,
        "bladeCount": 9,
        "bladeShape": null
      },
      "controlMechanism": "mechanical"
    },
    "coverage": {
      "format": "super-35"
    },
    "imageCircleDiameters": [
      {
        "diameterMm": 31.5,
        "conditions": {}
      }
    ],
    "specialized": {
      "cinema": {}
    }
  }
}
```

### Composable features (`specialized`)

`specialized` is a block whose keys identify the features that apply to the product.
A lens may combine multiple keys, so the block does not classify a lens into only one type.
For a product with none of these features, `specialized` is an empty object (`{}`).

| Key | Feature represented | Details recorded in Lens Full |
| --- | --- | --- |
| `cinema` | Product officially positioned as a cinema lens | Represented by the presence of the key alone |
| `anamorphic` | Anamorphic lens | Squeeze ratio |
| `fisheye` | Fisheye lens | Circular or diagonal fisheye image produced |
| `macro` | Macro lens | Working distance from the lens tip or another reference point to the subject |
| `reflex` | Lens using a reflex optical system | Represented by the presence of the key alone |
| `movements` | Lens that supports tilt, shift, or rotation | Movement range for each mechanism |
| `probe` | Probe lens | Viewing direction and integrated lighting |
| `builtInTeleconverter` | Lens with a built-in teleconverter | Magnification, optical construction, and specifications when engaged |

#### Differences between Lens Full and Lens Light

The LAOWA 24mm F14 2x Macro Probe illustrates how multiple features are recorded and what Lens Full and Lens Light retain.

=== "Lens Full"

    Source: `dist/z-mount-lenses.full.json`

    ```json
    {
      "id": "laowa-24mm-f14-2x-macro-probe",
      "lens": {
        "specialized": {
          "cinema": {},
          "macro": {
            "workingDistances": [
              {
                "distanceM": 0.02,
                "conditions": {}
              }
            ]
          },
          "probe": {
            "viewConfigurations": [
              {
                "directionDegrees": 0,
                "relationship": "integrated"
              }
            ],
            "integratedLights": [
              {
                "type": "led",
                "location": "lens tip",
                "quantity": 1
              }
            ]
          }
        }
      }
    }
    ```

    `cinema` is an empty object because the presence of the key identifies the feature.
    `macro` records a working distance of 0.02 m, while `probe` records the viewing direction and the integrated LED at the lens tip.

=== "Lens Light"

    Source: `dist/z-mount-lenses.light.json`

    ```json
    {
      "id": "laowa-24mm-f14-2x-macro-probe",
      "lens": {
        "specialized": {
          "cinema": {},
          "macro": {},
          "probe": {}
        }
      }
    }
    ```

    Lens Light retains only the presence of the three features.
    It does not include the details of working distance, viewing direction, or integrated lighting.

#### Specifications with the built-in teleconverter engaged

The following example shows where the NIKKOR Z 400mm f/2.8 TC VR S records its specifications with the built-in teleconverter disengaged and engaged.
The normal focal length and maximum aperture are placed directly under `lens`.
Values with the teleconverter engaged are recorded under `builtInTeleconverter.engagedSpecifications`.

Source: `data/records/lenses/nikkor/nikkor-z-400mm-f2p8-tc-vr-s.json`

```json
{
  "id": "nikkor-z-400mm-f2p8-tc-vr-s",
  "lens": {
    "focalLength": {
      "kind": "prime",
      "millimeters": 400
    },
    "aperture": {
      "fNumber": {
        "maximumAperture": [
          {
            "value": 2.8,
            "conditions": {}
          }
        ]
      }
    },
    "specialized": {
      "builtInTeleconverter": {
        "magnification": 1.4,
        "unitOpticalConstruction": {
          "groups": 4,
          "elements": 7
        },
        "engagedSpecifications": {
          "focalLength": {
            "kind": "prime",
            "millimeters": 560
          },
          "aperture": {
            "fNumber": {
              "maximumAperture": [
                {
                  "value": 4,
                  "conditions": {}
                }
              ]
            }
          }
        }
      }
    }
  }
}
```

In this example, the normal focal length and maximum aperture are 400 mm and f/2.8; with the built-in teleconverter engaged, they are 560 mm and f/4.
A teleconverter sold as a separate product is recorded with `productType: "teleconverter"`, not under `specialized`.
See the [`lens` JSON Schema reference](reference/schemas/lenses/product-type-lens.md#specialized) for the exact types and permitted values of each key.

## The `teleconverter` block

The `teleconverter` block records magnification, exposure impact, optical specifications, and compatible lenses.

| Field | Information recorded |
| --- | --- |
| `coverage` | Largest supported image format |
| `magnification` | Focal-length multiplier |
| `apertureLossStops` | Number of stops of light lost when attached |
| `supportsAutofocus` | Whether autofocus is supported with a compatible lens attached |
| `opticalConstruction` | Number of element groups and elements inside the teleconverter |
| `specialElements` | Types, official names, and quantities of special elements |
| `coatings` | Types, official names, and application locations of coatings |
| `compatibleLensIds` | IDs of compatible canonical products |

The following example shows how magnification, exposure impact, optical specifications, and compatible lenses are recorded for the Z TELECONVERTER TC-2.0x.

Source: `data/records/lenses/nikon/z-teleconverter-tc-2p0x.json`

```json
{
  "teleconverter": {
    "coverage": {
      "format": "full-frame"
    },
    "magnification": 2,
    "apertureLossStops": 2,
    "supportsAutofocus": true,
    "opticalConstruction": {
      "groups": 5,
      "elements": 8
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
      }
    ],
    "compatibleLensIds": [
      "nikkor-z-70-to-180mm-f2p8",
      "nikkor-z-70-to-200mm-f2p8-vr-s"
    ]
  }
}
```

The `compatibleLensIds` shown here contains only two entries extracted from the actual array.
Compatible lenses are referenced by their canonical-record `id` values.

## The `pinhole` block

The `pinhole` block records the largest supported image format, focal length, imaging modes, and angles of view.

| Field | Information recorded |
| --- | --- |
| `coverage` | Largest supported image format |
| `focalLength` | Focal length |
| `imagingModes` | Imaging modes provided by the product, together with their f-numbers and aperture diameters |
| `anglesOfView` | Published angles of view |

The following example uses the Lensbaby Obscura 16 to show how multiple imaging modes in one product are recorded.

Source: `data/records/lenses/lensbaby/lensbaby-obscura-16.json`

```json
{
  "pinhole": {
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
}
```

In this example, `zone-plate`, `pinhole-sieve`, and `pinhole` are the imaging modes provided by the Lensbaby Obscura 16.
The `null` values for `opening` and `anglesOfView` mean that the applicable information could not be confirmed from accepted published evidence.

## Related pages

- [Glossary](glossary.md): terms used by this project
- [Value-state rules](value-rules.md): meanings of `null`, empty arrays, `false`, and conditional numeric values
- [Data model](data-model.md): relationships among research results, canonical records, and distribution data
- [Mount adapter field reference](adapter-field-reference.md): fields for mount adapters
- [JSON Schema reference](reference/schemas/index.md): types, required fields, and permitted values
