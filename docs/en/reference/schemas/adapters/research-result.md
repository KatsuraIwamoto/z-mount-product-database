# adapters/research-result.schema.json

Validates one research result stored at `research/results/adapters/<brand-id>/<result-id>.json`.
It records the current inclusion decision, the sources checked, and unresolved questions for one mount adapter candidate.

## Three inclusion decision states

Each research result has one decision.
The examples below use a different candidate product for each state and show only the structural differences imposed by the conditions.

=== "Included"

    Product: Mount Adapter FTZ II

    Source file: `research/results/adapters/nikon/mount-adapter-ftz-ii.json`

    Referenced field: `decision`

    ```json
    {
      "decision": {
        "status": "included",
        "recordId": "mount-adapter-ftz-ii"
      }
    }
    ```

    `recordId` is the product ID of the corresponding canonical record.

=== "Excluded"

    Product: Auto Focus Extension Tube Set for Nikon Z-Mount Lenses

    Source file: `research/results/adapters/vello/vello-ext-nz.json`

    Referenced field: `decision`

    ```json
    {
      "decision": {
        "status": "excluded",
        "reason": "This is a same-mount extension-tube set, not a product whose primary purpose is converting one interchangeable-lens mount to Nikon Z."
      }
    }
    ```

    This example is an extension-tube set installed between a Nikon Z-mount lens and camera.
    It is excluded because its primary purpose is not to adapt lenses from another interchangeable-lens mount to the Nikon Z mount.

=== "Needs review"

    Product: MonsterAdapter LA-FZ11

    Source file: `research/results/adapters/monsteradapter/monsteradapter-la-fz11.json`

    Referenced fields: `decision`, `unresolved`

    ```json
    {
      "decision": {
        "status": "needs-review"
      },
      "unresolved": [
        "Confirm an official release announcement or verified sale of LA-FZ11; development references alone do not qualify for a canonical record."
      ]
    }
    ```

    In this example, no information confirming a product release announcement or sale has been found.

## Requirements for each decision state

| `decision.status` | Additional required field | `sources` |
| --- | --- | --- |
| `included` | `decision.recordId` | At least one entry |
| `excluded` | `decision.reason` | At least one entry |
| `needs-review` | At least one entry in root `unresolved` | May be `[]` only when no recordable source has been found |

For `included`, `decision` contains `status` and `recordId`. For `excluded`, it contains `status` and `reason`. For `needs-review`, it contains only `status`.

## Common fields

`$schema`, `id`, `subject`, `reviewedOn`, `decision`, and `sources` are required.
Add `notes` and `unresolved` only when needed.

| Path | Type/value | Meaning |
| --- | --- | --- |
| `$schema` | `"../../../../schemas/adapters/research-result.schema.json"` | Fixed relative path to the JSON Schema that validates the research result |
| `id` | ID string | Result ID that uniquely identifies the subject of the investigation |
| `subject` | object | Name information known for the candidate product at the time of research |
| `subject.manufacturerId` | ID string or `null` | Known manufacturer ID |
| `subject.brandId` | ID string or `null` | Known brand ID |
| `subject.name` | string | Product name used for the investigation |
| `subject.aliases` | string[] with no duplicates | Other names that refer to the same candidate product. Omit when there are none |
| `reviewedOn` | date | Date on which the current decision and sources were last checked |
| `decision.status` | `included` / `excluded` / `needs-review` | Current inclusion decision |
| `decision.recordId` | ID string | Product ID of the corresponding canonical record for `included` |
| `decision.reason` | string | Reason the candidate was determined to be out of scope for `excluded` |
| `sources` | array of `source` objects | Sources checked when making the decision |
| `sources[].url` | HTTP(S) URL | URL of the page checked |
| `sources[].publisherRelationship` | enum | Relationship between the publisher and the manufacturer or brand |
| `sources[].sourceType` | enum | Type of page or medium |
| `sources[].checked` | unique enum[] | Product JSON Schema field paths checked at that URL |
| `sources[].decisionChecks` | unique enum[] | Inclusion checks that have no corresponding canonical-record field |
| `sources[].note` | string | Short qualification that cannot be expressed by the structured fields. Omit when unnecessary |
| `notes` | string[] with no duplicates | Supplementary information that does not change the decision. Omit when there is none |
| `unresolved` | string[] with no duplicates | Unresolved questions. At least one entry is required for `needs-review` |

Within `subject`, `manufacturerId`, `brandId`, and `name` are required.
If the manufacturer or brand cannot be identified, record `null` in the corresponding ID field.

## Relationship to canonical records

When `decision.status` is `included`, repository validation checks the following relationships.

| Check | Rule |
| --- | --- |
| ID | The result ID, `decision.recordId`, and product ID in the canonical record match |
| Identity | The manufacturer ID, brand ID, and product name in `subject` match those in the canonical record's `identity` |
| Review date | `reviewedOn` is not later than the date encoded by `dataVersion` |
| Product dates | `lifecycle.announcementDate` and `lifecycle.officialDesignations[].observedOn` are not later than `reviewedOn` |
| Source coverage | A `checked` entry in at least one source covers every major canonical field group that contains an established value |

Changing `checked` alone does not justify updating `reviewedOn`.
When an established canonical value or its `checked` coverage changes, recheck the affected sources and record the date on which the current decision and sources were actually checked.

`false` and an empty array count as established values; `null` does not.

## Source classifications and checked fields

The following values are available for `publisherRelationship`:

- `manufacturer-or-brand`, `authorized-distributor`, `authorized-retailer`
- `retailer`, `crowdfunding-platform`, `independent-publication`, `unknown`

The following values are available for `sourceType`:

- `announcement`, `catalog`, `collection`, `company-profile`
- `crowdfunding`, `distributor-page`, `faq`, `image`
- `manual`, `news-report`, `product-page`, `retailer-listing`
- `specification`, `support-page`, `technical-page`, `video`, `other`

Every `source` requires at least one of `checked` or `decisionChecks`.
Choose `checked` values from the following field paths:
When parent and child paths are listed separately, the parent path does not stand in for the child path.

- Basic information: `identity`, `identity.modelNumberOptions`, `identity.alternateNames`, `identity.variants`, `lifecycle`, `officialProductPages`
- Mounts and features: `mountConfigurations`, `electronics`, `electronicServices`, `conversionOptics`, `mechanisms`
- Physical properties: `physical.dimensionMeasurements`, `physical.weightMeasurements`, `physical.officialEnvironmentalProtectionClaims`, `physical.tripodSupport`

Use one of `availability`, `inclusion-criteria`, `licensing`, or `release-status` under `decisionChecks`.
Do not descend to individual numbers or array elements; store the values and facts themselves in the canonical record.
Do not store research conversations, prompts, or retrieval logs with a source.
See [Editing research results](../../../research.md) for details on handling sources and decisions.

## Related pages

- [adapter-record](adapter-record.md): Structure and placement rules for canonical mount adapter records
- [Data model](../../../data-model.md): Flow from a research result to a canonical record
- [Editing research results](../../../research.md): How to record decision states and sources

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/adapters/research-result.schema.json)
