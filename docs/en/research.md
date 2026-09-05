# Per-product research results

A research result records, in JSON, the current inclusion decision for one candidate product and the sources used as evidence.
It preserves the last-reviewed date, sources, and unresolved questions as well as the decision itself, so the decision can be checked again.

You do not need this page if you only use the distribution data.
Use it when you need to review an inclusion decision or edit a research result.

## Browse evidence from the product list {#browse-product-research}

To check product information, start with the [latest product list](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/PRODUCTS.md).
Search within the page for the product name to find its official product pages, the last-reviewed date for its research result, and a link to the full research result.
The "Needs attention" sections also list the last-reviewed date and links to the sources checked for candidates that need review and other results that require follow-up.

The last-reviewed date (`reviewedOn`) is the date on which the decision and sources were last checked.
It does not guarantee that the product information has remained unchanged since that date or that the product is currently available.

When no eligible official product page remains, the alternative evidence used for the inclusion decision or specifications is kept under `sources` in the research result.
Open the individual research result from the product list when you need the reason for the decision, alternative evidence, or unresolved questions.
In the JSON, `decision` records the inclusion decision, `sources` records the evidence, and `unresolved` records open questions.

## Three inclusion decisions

`decision.status` records one of three decisions: included, excluded, or needs review.

| Decision | Information required for the decision | Canonical record |
| --- | --- | --- |
| Included (`included`) | Canonical record ID under `recordId` | Create |
| Excluded (`excluded`) | Reason the candidate does not meet the inclusion criteria under `reason` | Do not create |
| Needs review (`needs-review`) | Specific questions for the next review under `unresolved` | Do not create |

Included and excluded results require at least one supporting entry in `sources`.
A needs-review result requires at least one specific question under `unresolved`.
When sources have been checked for a needs-review result, retain them under `sources`.
`sources` may be an empty array only when no source can be recorded.

## Research result examples

The following JSON examples contain only the fields and array entries needed for this explanation.
They are not complete files.
The included example uses the Mount Adapter FTZ II, and the excluded and needs-review examples use candidates for the lens and related optical product dataset.

=== "Included (`included`)"

    The Mount Adapter FTZ II research result records an included decision.

    Source: `research/results/adapters/nikon/mount-adapter-ftz-ii.json`

    ```json
    {
      "$schema": "../../../../schemas/adapters/research-result.schema.json",
      "id": "mount-adapter-ftz-ii",
      "subject": {
        "manufacturerId": "nikon",
        "brandId": "nikon",
        "name": "Mount Adapter FTZ II"
      },
      "reviewedOn": "2026-09-02",
      "decision": {
        "status": "included",
        "recordId": "mount-adapter-ftz-ii"
      },
      "sources": [
        {
          "url": "https://imaging.nikon.com/imaging/lineup/accessory/camera/ftz_2/",
          "publisherRelationship": "manufacturer-or-brand",
          "sourceType": "product-page",
          "checked": [
            "identity",
            "mountConfigurations",
            "electronics",
            "physical.dimensionMeasurements",
            "physical.weightMeasurements",
            "physical.officialEnvironmentalProtectionClaims",
            "physical.tripodSupport"
          ]
        },
        {
          "url": "https://downloadcenter.nikonimglib.com/en/products/590/FTZ_II.html",
          "publisherRelationship": "manufacturer-or-brand",
          "sourceType": "support-page",
          "checked": [
            "identity",
            "electronics"
          ],
          "decisionChecks": [
            "availability"
          ]
        }
      ]
    }
    ```

    `recordId` refers to the `id` of the corresponding canonical record.
    The research result `id`, `recordId`, and canonical record `id` must match.

=== "Excluded (`excluded`)"

    The 50mm F1.2 DG DN | Art research result records an excluded decision.

    Source: `research/results/lenses/sigma/sigma-50mm-f1p2-dg-dn-art.json`

    ```json
    {
      "$schema": "../../../../schemas/lenses/research-result.schema.json",
      "id": "sigma-50mm-f1p2-dg-dn-art",
      "subject": {
        "manufacturerId": "sigma",
        "brandId": "sigma",
        "name": "50mm F1.2 DG DN | Art"
      },
      "reviewedOn": "2026-09-02",
      "decision": {
        "status": "excluded",
        "reason": "The official product page offers the lens only in L-Mount and Sony E-mount configurations."
      },
      "sources": [
        {
          "url": "https://www.sigma-global.com/en/lenses/a024_50_12/",
          "publisherRelationship": "manufacturer-or-brand",
          "sourceType": "product-page",
          "checked": [
            "identity",
            "mount"
          ],
          "decisionChecks": [
            "release-status"
          ]
        }
      ]
    }
    ```

    `reason` states which inclusion criterion the candidate does not meet.
    Retaining an excluded candidate in a research result avoids repeated investigation of the same product.

=== "Needs review (`needs-review`)"

    The SIRUI Saturn V2 Full-Frame Anamorphic Lens Series research result records a needs-review decision.

    Source: `research/results/lenses/sirui/sirui-saturn-v2-full-frame-anamorphic-lens-series.json`

    ```json
    {
      "$schema": "../../../../schemas/lenses/research-result.schema.json",
      "id": "sirui-saturn-v2-full-frame-anamorphic-lens-series",
      "subject": {
        "manufacturerId": "sirui",
        "brandId": "sirui",
        "name": "SIRUI Saturn V2 Full-Frame Anamorphic Lens Series"
      },
      "reviewedOn": "2026-09-02",
      "decision": {
        "status": "needs-review"
      },
      "sources": [
        {
          "url": "https://store.sirui.com/collections/z-mount-nikon-1",
          "publisherRelationship": "manufacturer-or-brand",
          "sourceType": "collection",
          "checked": [
            "mount"
          ]
        }
      ],
      "unresolved": [
        "Has SIRUI published a product release announcement or confirmed sale or availability for the Saturn V2 series?",
        "Has SIRUI announced or offered a Nikon Z configuration for the Saturn V2 series?"
      ]
    }
    ```

    `unresolved` records specific questions for the next review.
    Do not create a canonical record until a product release announcement or sale has been confirmed and a Nikon Z configuration has also been established.

Write strings under `reason`, `notes`, `unresolved`, and `sources[].note` in English.

## Common fields

| Field | Information recorded |
| --- | --- |
| `$schema` | Reference to the JSON Schema used to validate the research result |
| `id` | ID that identifies the research result |
| `subject` | Manufacturer ID, brand ID, and product name of the candidate reviewed |
| `reviewedOn` | Date on which the decision and sources were last checked |
| `decision` | Included, excluded, or needs-review decision |
| `sources` | URLs used for the decision or product information, the publisher relationship, page type, and elements checked on each page |
| `notes` | Brief factual context explicitly stated by a source and needed to interpret the evidence |
| `unresolved` | Specific questions about the evidence needed for a decision or value |

`reviewedOn` records the date on which the decision and sources were actually checked, in `YYYY-MM-DD` format.
Changing `checked` alone does not justify updating `reviewedOn`.
When an established canonical value or its `checked` coverage changes, recheck the affected sources and record the date on which the current decision and sources were actually checked.
It must not be later than the date encoded by `dataVersion` in `config/versions.json`.

Use `notes` only for facts explicitly stated by a source, such as a measurement basis or the scope of an officially named variant.
Do not use `notes` for value-selection rationale, source comparison, human judgment, or follow-up questions.
Keep follow-up questions under `unresolved`.

## Record sources

Prefer official sources from the manufacturer or brand for inclusion decisions and product information.

Preferred sources
: The exact-product official product page, specifications, manual, and product release announcement.

Sources accepted as alternative evidence
: When no official product page remains, a crowdfunding page operated by the manufacturer or brand may provide evidence.
  Corporate investor-relations materials and press releases may also be used.
  Product and announcement pages from authorized distributors are also accepted as alternative evidence.

Sources used only for corroboration
: An authorized retailer's page for the exact product may corroborate that the product was released, that it is offered for the Nikon Z mount, and that the manufacturer published a model number.

Facts checked from product images
: An image published by an authorized retailer may support facts directly visible on the product when the exact product and configuration are established and the image clearly shows the relevant area.
  Record the direct image URL with `sourceType: image`, and retain the retailer page as a separate source when it establishes the product or configuration.
  Use images of multiple states or video for facts that depend on movement or a state change.
  Do not infer hidden construction, materials, dimensions, weight, electronic functions, environmental protection, compatibility, or release status from appearance.
  When an image of the complete mount face establishes that an adapter has no electronic contacts, record the related negative electronic-function values required by the adapter data structure.

Research leads
: Other retailers, reviews, news, and forums are leads for further research.
  Use only facts verified by an accepted source for an inclusion decision or product information.

Store a `sources[].url` without tracking parameters or fragments, and do not duplicate the same URL.
Keep every material source used for a decision or canonical value, even when another source checks the same element or publishes different information.

For a lens or mount-adapter source, use `publisherRelationship` for the publisher's relationship to the manufacturer or brand, `sourceType` for the kind of page, and `checked` for the canonical-record fields checked on that page.
Use medium-grained product JSON Schema field paths such as `lens.focus`, `mountConfigurations`, `electronics`, or `physical.dimensionMeasurements` under `checked`.
When the JSON Schema lists parent and child paths separately, record the path that matches the canonical destination actually checked.
For example, `physical` does not stand in for `physical.weightMeasurements`, and `mount` does not stand in for `mount.electronicContacts`.
Every major canonical field group containing an established value must be traceable to `checked` in at least one source.
Track `false` and an empty array as established values; do not require coverage for `null`, which remains unestablished.
For a source whose URL is retained as an official product page, also record `officialProductPages`.
Put release status, sale confirmation, licensing, and inclusion checks that have no canonical-record field under `decisionChecks`.
Use `sources[].note` only when a short qualification is necessary.

Record values such as dimensions, weight, dates, and identifiers in the canonical record rather than duplicating them in `checked` or `sources[].note`.
Under `checked`, do not descend to individual numeric leaves; choose a unit such as `lens.stabilization`, `electronics`, `physical.weightMeasurements`, or `controls` that still identifies the destination in the canonical record.
Do not compare sources, allege an error, justify a value choice, or narrate the research workflow under `sources`.

When the checked sources do not establish a single value, do not choose one without evidence.
Apply the normal [value states](value-rules.md#value-states) in the canonical record and state the evidence still needed as a neutral question under `unresolved`.
A deleted official product page alone does not establish that a product was discontinued.

The distinction between `officialProductPages` in a canonical record and `sources` in a research result is explained under [URLs and sources](value-rules.md#urls).

!!! warning "Do not retain research-process logs"

    Do not record AI conversations, prompts, model names, or duplicated retrieval logs in research results.
    Retain only the conclusions, sources, and unresolved questions needed to review the decision again.

## File placement and JSON Schema

The lens and related optical product dataset and the mount adapter dataset use separate research result structures and JSON Schemas.
Place one research result file for each candidate product in the directory for its dataset.

| Dataset | File placement | JSON Schema reference |
| --- | --- | --- |
| Lens and related optical product dataset | `research/results/lenses/<brand-directory>/<result-id>.json` | [lenses/research-result](reference/schemas/lenses/research-result.md) |
| Mount adapter dataset | `research/results/adapters/<brand-directory>/<result-id>.json` | [adapters/research-result](reference/schemas/adapters/research-result.md) |

Use the brand ID from the manufacturer and brand registry for `<brand-directory>`.
Place a candidate whose brand has not been identified under `unattributed/`.

For an included result, make its `id` and `recordId` match the `id` of the corresponding canonical record.
The manufacturer ID, brand ID, and product name in the research result must also match the corresponding canonical record.
The corresponding canonical record's `lifecycle.announcementDate` and `lifecycle.officialDesignations[].observedOn` cannot be later than the research result's `reviewedOn`.
Excluded and needs-review results do not have corresponding canonical records.

## Related pages

- [Report and edit product information](contribute.md): How to report an issue or edit data directly
- [Scope and inclusion criteria](overview.md): Criteria for included, excluded, and needs-review decisions
- [Data model](data-model.md): Relationship among research results, canonical records, and distribution data
- [Glossary](glossary.md): Terms for inclusion decisions and sources
- [JSON Schema reference](reference/schemas/index.md): Types, required fields, and conditional constraints
