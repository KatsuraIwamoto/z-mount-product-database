# lenses/research-result.schema.json

This schema validates one research result stored at `research/results/lenses/<brand-id>/<result-id>.json`.
It records the current inclusion decision, sources checked, and unresolved questions for one candidate product.

## Three inclusion-decision states

Each research-result record has one decision.
The examples below use a different candidate product for each state and show only the structural differences imposed by the conditions.

=== "Included"

    Product: NIKKOR Z 24-70mm f/2.8 S II

    Source: `research/results/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

    Excerpt: `decision`

    ```json
    {
      "decision": {
        "status": "included",
        "recordId": "nikkor-z-24-to-70mm-f2p8-s-ii"
      }
    }
    ```

    `recordId` is the product ID of the corresponding canonical record.

=== "Excluded"

    Product: Lightdow 900mm F8 Mirror Lens

    Source: `research/results/lenses/lightdow/lightdow-900mm-f8-mirror-lens.json`

    Excerpt: `decision`

    ```json
    {
      "decision": {
        "status": "excluded",
        "reason": "The product is a generic T2-mount mirror lens sold with camera-side adapter rings. It is not a direct, supplied lens-specific, or dedicated-series Nikon Z configuration."
      }
    }
    ```

    In this example, the product combines a general-purpose T2-mount lens with a camera-side adapter and therefore does not meet the inclusion criteria.

=== "Needs review"

    Product: SIRUI Saturn V2 Full-Frame Anamorphic Lens Series

    Source: `research/results/lenses/sirui/sirui-saturn-v2-full-frame-anamorphic-lens-series.json`

    Excerpt: `decision`, `unresolved`

    ```json
    {
      "decision": {
        "status": "needs-review"
      },
      "unresolved": [
        "Has SIRUI published a product release announcement or confirmed sale or availability for the Saturn V2 series?",
        "Has SIRUI announced or offered a Nikon Z configuration for the Saturn V2 series?"
      ]
    }
    ```

    In this example, a product release announcement or confirmed sale remains unverified, as does the existence of a Nikon Z-mount product.

## Requirements for each decision state

| `decision.status` | Additional required fields | `sources` |
| --- | --- | --- |
| `included` | `decision.recordId` | At least one entry |
| `excluded` | `decision.reason` | At least one entry |
| `needs-review` | At least one entry in the root-level `unresolved` field | May be `[]` only when no recordable source can be found |

`decision` contains only the fields for its state.
Do not use `reason` with `included` or `recordId` with `needs-review`.

## Common fields

`$schema`, `id`, `subject`, `reviewedOn`, `decision`, and `sources` are required.
Add `notes` and `unresolved` only when needed.

| Path | Type/value | Description |
| --- | --- | --- |
| `$schema` | `"../../../../schemas/lenses/research-result.schema.json"` | Fixed relative path to the JSON Schema that validates research-result records |
| `id` | ID string | Result ID that uniquely identifies the research subject |
| `subject` | object | Name information known for the candidate product at the time of research |
| `subject.manufacturerId` | ID string or `null` | Known manufacturer ID |
| `subject.brandId` | ID string or `null` | Known brand ID |
| `subject.name` | string | Name of the product under investigation |
| `subject.aliases` | unique string[] | Other names for the same candidate product. Omit when there are none |
| `reviewedOn` | date | Date on which the current decision and sources were last checked |
| `decision.status` | `included` / `excluded` / `needs-review` | Current inclusion decision |
| `decision.recordId` | ID string | Product ID of the corresponding canonical record when the status is `included` |
| `decision.reason` | string | Basis for excluding the product when the status is `excluded` |
| `sources` | array of `source` objects | Sources checked to make the decision |
| `sources[].url` | HTTP(S) URL | URL of the page checked |
| `sources[].publisherRelationship` | enum | Relationship between the publisher and the manufacturer or brand |
| `sources[].sourceType` | enum | Type of page or medium |
| `sources[].checked` | unique enum[] | Product JSON Schema field paths checked at that URL |
| `sources[].decisionChecks` | unique enum[] | Inclusion checks that have no corresponding canonical-record field |
| `sources[].note` | string | Short qualification that cannot be expressed by the structured fields. Omit when unnecessary |
| `notes` | unique string[] | Supplemental information that does not change the decision. Omit when there is none |
| `unresolved` | unique string[] | Unresolved questions. At least one entry is required for `needs-review` |

Within `subject`, `manufacturerId`, `brandId`, and `name` are required.
If the manufacturer or brand cannot be identified, record `null` in the corresponding ID field.

## Relationship to canonical records

When `decision.status` is `included`, repository validation checks the following relationships.

| Item checked | Rule |
| --- | --- |
| ID | The result ID, `decision.recordId`, and product ID in the canonical record match |
| Identity | The manufacturer ID, brand ID, and product name in `subject` match the `identity` block in the canonical record |
| Review date | `reviewedOn` is not later than the date in `dataVersion` |
| Product dates | `lifecycle.announcementDate` and `lifecycle.officialDesignations[].observedOn` are not later than `reviewedOn` |
| Source coverage | A `checked` entry in at least one source covers every major canonical field group that contains an established value |

Changing `checked` alone does not justify updating `reviewedOn`.
When an established canonical value or its `checked` coverage changes, recheck the affected sources and record the date on which the current decision and sources were actually checked.

`false` and an empty array count as established values; `null` does not.
Under `lens.specialized`, an empty marker object such as `cinema: {}` is still an established fact.
When a canonical record has a nonempty `specialized` object, a corresponding source must include `lens.specialized` in `checked`.

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
Entries under `checked` correspond to canonical-record field names without descending to individual numbers or array elements.
When parent and child paths are listed separately, the parent path does not stand in for the child path.

- Common fields
    - Basic information: `productType`, `identity`, `identity.modelNumberOptions`, `identity.alternateNames`, `identity.variants`, `lifecycle`, `officialProductPages`
    - Mount: `mount`, `mount.electronicContacts`, `mount.adapter`
    - Physical properties: `physical`, `physical.dimensionMeasurements`, `physical.weightMeasurements`, `physical.officialEnvironmentalProtectionClaims`, `physical.filterInterfaces`, `physical.tripodSupport`
    - External length and storage: `physical.externalLengthDuringZoom`, `physical.externalLengthDuringFocus`, `physical.isRetractableForStorage`, `physical.frontAccessoryInterface`
    - Other: `controls`, `accessories`, `electronicServices`
- Lens
    - Basic specifications: `lens.focalLength`, `lens.aperture`, `lens.anglesOfView`, `lens.coverage`, `lens.imageCircleDiameters`, `lens.opticalConstruction`
    - Optical elements: `lens.specialElements`, `lens.coatings`
    - Features: `lens.focus`, `lens.zoom`, `lens.stabilization`, `lens.specialized`
- Teleconverter
    - Basic specifications: `teleconverter.coverage`, `teleconverter.magnification`, `teleconverter.apertureLossStops`, `teleconverter.supportsAutofocus`
    - Optical elements: `teleconverter.opticalConstruction`, `teleconverter.specialElements`, `teleconverter.coatings`
    - Compatible lenses: `teleconverter.compatibleLensIds`
- Pinhole: `pinhole.coverage`, `pinhole.focalLength`, `pinhole.imagingModes`, `pinhole.anglesOfView`

Use one of `availability`, `inclusion-criteria`, `licensing`, or `release-status` under `decisionChecks`.
Store the values and facts themselves in the canonical record rather than in the research result.
Do not store research conversations, prompts, or retrieval logs with a source.
For details about sources and decisions, see [Editing research-result records](../../../research.md).

## Related pages

- [product-record](product-record.md): canonical record structure and placement rules
- [Data model](../../../data-model.md): the path from a research result to a canonical record
- [Editing research-result records](../../../research.md): how to record decision states and sources

[JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/research-result.schema.json)
