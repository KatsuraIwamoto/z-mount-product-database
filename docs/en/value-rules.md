# Value-state rules

Canonical records and distribution data distinguish field omission, `null`, an empty array, and `false` according to why a value is absent.
Separate rules also apply to condition-dependent numbers, values retained from Lens Full in Lens Light, and the location used to record a URL.

The JSON examples contain only the parts needed for each explanation.
Examples with arrays may show only some of their entries.

## Value states {#value-states}

Field omission, `null`, an empty array, and `false` have different meanings.

| Representation | Meaning | Example |
| --- | --- | --- |
| Field omitted | Structurally inapplicable to the product | A product whose `productType` is `lens` has no `teleconverter` block |
| `null` | Applicable, but no value can be confirmed from accepted published evidence | `modelNumberOptions` is `null` because no model number can be confirmed from accepted published evidence |
| `[]` | The collection was checked and contains no matching entries | `mechanisms` is an empty array because the adapter was confirmed to have none |
| `false` | A negative fact has been confirmed | `conversionOptics.present` is `false` because the adapter has no conversion optics |

!!! note "`officialDesignations: []` does not mean currently sold"
    `lifecycle.officialDesignations: []` means that no official status designation was confirmed in the sources checked.
    It does not mean that the product is currently sold, in stock, or available.

=== "Field omission and `null`"

    The NIKKOR Z 24-70mm f/2.8 S II has `lens` as its `productType`.
    Its record contains a `lens` block and omits the structurally inapplicable `teleconverter` and `pinhole` blocks.
    The `null` value for `identity.modelNumberOptions` means that no model number can be confirmed from accepted published evidence.

    Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

    ```json
    {
      "productType": "lens",
      "identity": {
        "modelNumberOptions": null
      },
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

=== "Empty array and `false`"

    `mechanisms` for the Mount Adapter FTZ II is an empty array because the adapter was confirmed to have no applicable mechanisms.
    The `false` value for `conversionOptics.present` means that it has no conversion optics.

    Source: `data/records/adapters/nikon/mount-adapter-ftz-ii.json`

    ```json
    {
      "conversionOptics": {
        "present": false
      },
      "mechanisms": []
    }
    ```

!!! warning "Do not use sentinel strings for value states"

    Do not use strings such as `"unknown"`, `"none"`, or `"not-applicable"` as sentinel values for unknown, inapplicable, or empty states.
    The four distinct states let consumers distinguish an unconfirmed value from a confirmed empty collection or negative fact.

## Numbers and conditions {#numbers-and-conditions}

A number may apply only under specific conditions, such as a minimum focus distance that varies with focal length.
For the NIKKOR Z 24-70mm f/2.8 S II, each `distanceM` value is stored in the same entry as the focal length to which it applies.

Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "lens": {
    "focus": {
      "minimumFocusDistances": [
        {
          "distanceM": 0.24,
          "conditions": {
            "focalLength": {
              "kind": "point",
              "millimeters": 24
            }
          }
        },
        {
          "distanceM": 0.33,
          "conditions": {
            "focalLength": {
              "kind": "point",
              "millimeters": 70
            }
          }
        }
      ]
    }
  }
}
```

In this example, the minimum focus distance is 0.24 m at a focal length of 24 mm and 0.33 m at 70 mm.
Preserve published values with their conditions without rounding or averaging.
Do not derive a new representative value or range from multiple published values.

When a degrees-and-minutes value or a `1:n` ratio must be normalized to a single decimal number in the schema, round the converted result to six decimal places.
Omit trailing zeroes from JSON numbers while preserving enough precision to recover the original notation at its published precision.

## Recording official names {#official-names}

Use `officialName` for a stable manufacturer- or brand-used designation.
Prefer an official glossary, technology page, specification label, product heading, badge, or printed control label; sentence capitalization alone does not establish a name.
Do not record sentence-only generic descriptions as names.
Preserve stable published technical designations even when `type` or `types` represents the same class: normalized types support cross-brand grouping, while `officialName` preserves manufacturer terminology.
For controls, omit ordinary component names that merely restate `type`; retain official labels that add product-specific meaning.

Use the official English designation when an equivalent official English page exists; otherwise preserve the published designation without inventing a translation.
Scope names to their brand and field; identical wording across brands does not establish the same technology.
Within one brand and field, differences limited to case, spacing, punctuation, grammatical number, or a generic suffix do not create separate names. Use the most explicit stable official designation.
Omit the name when official evidence does not establish one consistently.
Remove `®` and `™`, which are not part of the lexical name, but retain symbols belonging to the designation itself, such as the asterisk in `T*`.

## Lens Full and Lens Light {#lens-full-and-light}

Lens Light retains a subset of the values in Lens Full.
It does not add Light-only values or calculate new values from multiple Full values.

In the `focus` data for the NIKKOR Z 24-70mm f/2.8 S II, Lens Full contains every measurement for each focal length.
Lens Light retains only the entries tied for the shortest focus distance and the entries tied for the greatest reproduction ratio.

=== "Lens Full"

    Source: `dist/z-mount-lenses.full.json`

    ```json
    {
      "id": "nikkor-z-24-to-70mm-f2p8-s-ii",
      "lens": {
        "focus": {
          "minimumFocusDistances": [
            {
              "distanceM": 0.24,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 24
                }
              }
            },
            {
              "distanceM": 0.24,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 28
                }
              }
            },
            {
              "distanceM": 0.27,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 35
                }
              }
            },
            {
              "distanceM": 0.3,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 50
                }
              }
            },
            {
              "distanceM": 0.33,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 70
                }
              }
            }
          ],
          "reproductionMagnifications": [
            {
              "kind": "maximum",
              "value": 0.21,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 24
                }
              }
            },
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
          ]
        }
      }
    }
    ```

=== "Lens Light"

    Source: `dist/z-mount-lenses.light.json`

    ```json
    {
      "id": "nikkor-z-24-to-70mm-f2p8-s-ii",
      "lens": {
        "focus": {
          "minimumFocusDistances": [
            {
              "distanceM": 0.24,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 24
                }
              }
            },
            {
              "distanceM": 0.24,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 28
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
          ]
        }
      }
    }
    ```

The same shortest focus distance, 0.24 m, applies at both 24 mm and 28 mm, so both entries remain in Lens Light.
For maximum reproduction ratio, the entry with the highest value, 0.32, remains.
This filtering applies only to `minimumFocusDistances` and `reproductionMagnifications`.
Any other array retained in Lens Light preserves the order and number of entries from Lens Full.
Some fields within each array entry may still be omitted.

## URLs and sources {#urls}

Official product pages and other materials used to verify specifications are recorded in different locations.

=== "Product pages"

    `officialProductPages` contains official main pages dedicated to the exact product.
    The following example retains an official product page for Japan together with its region, language, and publisher.

    Source: `data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

    ```json
    {
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

=== "Research sources"

    In addition to product pages, `sources` in a research result records manuals, specifications, announcements, support pages, and other sources used for a decision or specification.

    Source: `research/results/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

    ```json
    {
      "sources": [
        {
          "url": "https://nij.nikon.com/products/lineup/nikkor/zmount/nikkor_z_24-70mm_f28_s_2/",
          "publisherRelationship": "manufacturer-or-brand",
          "sourceType": "product-page",
          "checked": [
            "identity",
            "mount",
            "physical.dimensionMeasurements",
            "physical.weightMeasurements",
            "physical.filterInterfaces",
            "lens.focalLength",
            "lens.aperture",
            "lens.coverage",
            "lens.opticalConstruction",
            "lens.focus"
          ]
        },
        {
          "url": "https://download.nikonimglib.com/archive7/NpSBN00JyCGA07ITCA437TDmBL05/Z24-70_2.8SIIRG_(En)01.pdf",
          "publisherRelationship": "manufacturer-or-brand",
          "sourceType": "manual",
          "checked": [
            "controls",
            "accessories",
            "lens.focus",
            "lens.stabilization"
          ]
        }
      ]
    }
    ```

When no eligible official product page remains, use an empty array for `officialProductPages` and retain the alternative evidence under `sources` in the research result.
Remove tracking parameters and fragments from URLs, and do not record the same URL more than once.

## Related pages

- [Data model](data-model.md): Relationship among research results, canonical records, and distribution data
- [Field reference for lenses and related optical products](lens-field-reference.md): Where to record product information for the lens and related optical product dataset
- [Mount adapter field reference](adapter-field-reference.md): Where to record mount adapter information
- [Per-product research results](research.md): How to record inclusion decisions and sources
- [JSON Schema reference](reference/schemas/index.md): Types, required fields, and permitted values
