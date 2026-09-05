# AGENTS.md

## Purpose and authority

This repository is the source of truth for two public Nikon Z-compatible datasets:
lenses and directly mountable related optical products, and mount adapters whose
primary purpose is converting another interchangeable-lens mount to Nikon Z.

- Schemas and executable validation define data contracts and cross-file rules.
- `docs/ja/` is the primary human documentation; `docs/en/` is its AI-translated mirror.
- `.agents/skills/z-mount-product-research/SKILL.md` is an operational aid subordinate
  to this file and the schemas.
- Narrative documentation never overrides validation.

## Sources of truth

- Canonical lens-dataset products: `data/records/lenses/<brand-id>/<id>.json`
- Canonical mount adapters: `data/records/adapters/<brand-id>/<id>.json`
- Manufacturer and brand spellings: `data/product-manufacturer-brand-registry.json`
- Mount-system identifiers: `data/mount-system-registry.json`
- Lens-dataset decisions and sources: `research/results/lenses/<brand-id>/<id>.json`
- Adapter decisions and sources: `research/results/adapters/<brand-id>/<id>.json`
- Schema and data release versions: `config/versions.json`
- Public data contracts: `schemas/{shared,lenses,adapters}/*.schema.json`
- Repository-only source-registry validation: `schemas/internal/*.schema.json`

Generated and committed files are:

```text
dist/z-mount-lenses.full.json
dist/z-mount-lenses.light.json
dist/z-mount-adapters.full.json
PRODUCTS.md
```

Never edit generated files manually.

## Public product identifiers

- A public product key is the pair `(namespace, id)`, where the namespace is
  `lenses` or `adapters`.
- Lens Full and Lens Light share the `lenses` namespace. Adapter Full uses the
  `adapters` namespace.
- A bare `id` is unique only within its namespace. The same bare `id` may exist
  in different namespaces, so consumers combining datasets must not use `id`
  alone as a primary key.
- Product IDs use human-readable slug strings. Their lexical format is defined
  by schema, but the relationship between slug text and product attributes is
  not part of the public data contract. Do not derive brand, manufacturer,
  product name, specifications, product type, or display text from an ID.
- A product key becomes fixed when it first appears in an official GitHub
  Release asset. Before that first release, working IDs may be corrected.
- After publication, never rename a product key, assign it to another product,
  or reuse it after removal. Reintroducing the same product uses its reserved ID.
- Stable IDs do not guarantee permanent inclusion in the latest release.
  Document merges, splits, removals, and namespace changes in the release notes,
  including the old key and the replacement key or the absence of one.
- Do not add a general ID-history schema or central ID registry until the first
  exceptional change or a concrete automation requirement makes one necessary.
- Manufacturer, brand, and mount-system IDs become public when they first appear
  in an official GitHub Release asset. After publication, never rename or reuse
  them. A display-name change updates registry metadata without changing its ID.
- Before the first public release, do not keep registry entries unused by canonical
  records or research subjects. Manufacturer and brand usage includes every research
  decision and canonical alternate-name brand; mount-system usage comes from canonical
  records. After publication, the stable-ID rules take precedence if a formerly used
  entry becomes unreferenced. Add an explicit retained-public-ID mechanism when that
  first occurs; do not delete or reuse the ID merely to satisfy the pre-release check.

## Lens-dataset product model

- Every record contains common product data and exactly one `lens`, `teleconverter`,
  or `pinhole` block selected by `productType`.
- Create a canonical record only after an official product release announcement or
  confirmed sale/availability. A development announcement alone remains a
  `needs-review` research result and does not qualify for `data/records/lenses/`.
- `lifecycle.announcementDate` is the official product release-announcement date;
  never substitute a development-announcement date.
- `mount.adapter` is present only for an official Nikon Z configuration whose adapter
  is supplied with the product or dedicated to that lens or named product series.
  Exclude FTZ, broad system adapters, generic mount adapters, and third-party adapters.
- Lens features under `lens.specialized` are composable. Do not invent exclusive
  lens subtypes.
- The filename must be `<id>.json`.
- `teleconverter.compatibleLensIds` references only canonical records in the
  `lenses` namespace whose `productType` is `lens`.
- The parent record directory is the registry ID for `identity.brandId`.
- `identity.manufacturerId`, `identity.brandId`, and any
  `identity.alternateNames[].brandId` must resolve in the manufacturer and brand
  registry.

## Mount-adapter model

- Adapter records are structurally independent of lens-dataset product records.
  Do not add `productType` or lens, teleconverter, or pinhole blocks to an adapter.
- Include only a marketed product whose primary purpose is converting another
  interchangeable-lens mount to Nikon Z. Exclude extension tubes, filter adapters,
  focal reducers without mount conversion, and accessories whose conversion role is
  incidental.
- Use one record for the same marketed product under the same rule used by the lens
  dataset. Put selectable mount or other officially named options in variants rather
  than duplicating a product without evidence that it is distinct.
- Record basic product, mount-pair, electronic, optical, mechanical, and physical
  facts first. Large compatible-lens, compatible-camera, and firmware matrices are
  outside the initial contract.
- Every `cameraSideMountSystemId` is `nikon-z`; both mount-system IDs must resolve in
  `data/mount-system-registry.json`.
- Adapter identity IDs use the same manufacturer and brand registry as lenses.
- Keep configuration-specific lens retention and rear-protrusion limits inside the
  matching `mountConfigurations` entry. Keep shift, tilt, and rotation measurements
  inside the matching typed mechanism.
- Use shared structures for metadata transmission, electronic services, tripod support,
  and movement measurements across the two datasets.
- Treat product-side electronic services as independent of mount contacts; a direct USB
  connection or dock may exist even when the mount has no electronic contacts.
- Create a canonical adapter record only after an official product release
  announcement or confirmed sale/availability. Development announcements remain
  `needs-review` results.

Use these value states consistently:

- omit a field only when structurally inapplicable;
- use `null` when applicable but not established by published evidence accepted under
  the source rules in this file;
- use `[]` when a checked collection contains no entries;
- use `false` only for a confirmed negative fact;
- never use sentinel strings such as `unknown`, `none`, or `not-applicable`.

## Lens Light compatibility

- Light keeps every full product in the same order with the same `id`,
  `productType`, common block names, and product-type block name.
- Every light product must be an ordered recursive subset of its full product.
  Objects may omit properties, and retained leaf values and value types must match.
- Arrays preserve source order. Except for the schema-defined focus selection,
  every retained array keeps its full length while object elements may omit fields.
  The existing website-compatible focus projection keeps only exact full entries
  tied for the shortest focus distance or greatest reproduction magnification.
- Never add light-only facts or calculate replacement minimum, maximum, range,
  representative, or summary leaf values.
- Keep identity, lifecycle, official page URLs, mount, dimension measurements,
  weight measurements, filter interfaces, and the schema-defined minimal
  `lens`, `teleconverter`, or `pinhole` facts.
- `lens.specialized` keeps category keys as empty marker objects. Presence facts
  such as autofocus, manual focus, and stabilization retain only `present`.
- Preserve the existing light projection unless a separately approved website
  migration changes its contract.

## Factual data

- Prefer manufacturer- or brand-official sources for canonical facts. When an exact
  product page is unavailable, manufacturer-run crowdfunding, corporate IR or press
  releases, and authorized-distributor product or announcement pages may support
  canonical facts. An exact authorized-retailer listing may corroborate a released
  mount configuration and manufacturer-published model number, but does not become an
  official product page. A directly linked photograph published by that authorized
  retailer may additionally support facts that are directly visible on the product,
  provided the exact product and configuration are established and the relevant area is
  shown clearly. Use multiple states or video for movement-dependent facts. Do not use
  appearance to infer hidden construction, materials, measurements, electronic functions,
  environmental protection, compatibility, or release status. The adapter schema's
  required negative electronic-function values may follow from a clearly visible absence
  of mount contacts.
- Preserve official product names and published numeric values.
- Use `officialName` only for a stable manufacturer- or brand-used designation. Prefer
  an official glossary, technology page, specification label, product heading, badge,
  or printed control label over capitalization inherited from a sentence. A sentence-only
  generic description is not an `officialName`. Preserve a stable published technical
  designation even when `type` or `types` already represents the same general class;
  normalized types provide cross-brand grouping, while `officialName` preserves the
  manufacturer's terminology. For controls, omit an ordinary component name that merely
  restates `type` unless an official label adds product-specific meaning. When equivalent
  local-language and official English pages exist, use the official English designation;
  otherwise preserve the published designation rather than inventing a translation.
- Treat an `officialName` as scoped to its brand and field. Do not assume that identical
  wording from different brands denotes the same technology. Within one brand and field,
  differences limited to case, spacing, punctuation, grammatical number, or a generic
  suffix do not create separate names. Use the most explicit stable official designation,
  and omit the name when official evidence does not establish one consistently.
- Do not include trademark registration symbols such as `®` or `™` in `officialName`;
  they describe legal status rather than the lexical name. Preserve symbols that are part
  of the designation itself, such as the asterisk in `T*`.
- Do not infer unpublished facts or silently choose between conflicting published values.
- `officialProductPages` contains only exact-product main landing pages.
- Use `officialProductPages: []` when no eligible exact landing page remains, and keep
  the alternative evidence in the matching research result's `sources`.
- Put specifications, manuals, announcements, support pages, and other evidence in
  the matching research result's `sources`.
- Store a canonical URL once; remove fragments and tracking parameters.
- A deleted page alone is not proof that a product was discontinued.

## Research results

- Keep one file per investigated lens-dataset product or mount adapter under its
  matching `research/results/lenses/` or `research/results/adapters/` directory.
- `included` requires `recordId`; the result ID, record ID, and canonical product ID
  must match, as must the subject and canonical identity.
- `excluded` requires a concise evidence-based `reason`.
- `needs-review` requires at least one concrete `unresolved` question.
- `reviewedOn` is the actual review date and must not be later than the date
  encoded by `dataVersion` in `config/versions.json`.
- Changing `checked` alone does not justify updating `reviewedOn`. When an established
  canonical value or its `checked` coverage changes, recheck the affected sources and
  set `reviewedOn` only to the actual date on which the current decision and those
  sources were rechecked.
- An included canonical record's `lifecycle.announcementDate` and each
  `lifecycle.officialDesignations[].observedOn` must not be later than its paired
  research result's `reviewedOn`.
- Keep every material source used for a decision or canonical fact in `sources`.
  Do not remove a source solely because another source checks the same element or
  publishes different information.
- For an included result, every major canonical field group containing an established
  value must be covered by `checked` in at least one source. An exact page retained in
  `officialProductPages` must also appear in research sources with that field checked.
- For lens and adapter research, classify every source with `publisherRelationship` and
  `sourceType`. Record checked canonical product areas as schema-aligned field paths in
  `checked`, using meaningful field groups rather than numeric leaves. A parent path does
  not cover a separately defined child path: for example, `physical` does not cover
  `physical.weightMeasurements`, and `mount` does not cover
  `mount.electronicContacts`. Record only
  non-canonical inclusion or release checks in `decisionChecks`. Use `note` only when
  those structured fields cannot preserve a
  source-specific fact needed to review the decision. Do not copy published values,
  compare sources, characterize differences as errors, justify a value choice, or
  narrate research workflow.
- Use `notes` only for factual context explicitly stated by a source and needed to
  interpret the evidence, such as a measurement basis or the scope of an officially
  named variant.
  Omit `notes` otherwise.
- When checked sources do not establish a single canonical value, do not choose one
  silently. Leave the affected fact unresolved under the normal value-state rules and
  use `unresolved` for a neutral, actionable question without comparing sources or
  alleging an error.
- Do not store AI conversations, prompts, model names, batch ledgers, duplicated
  retrieval logs, or guessed conclusions.

## Engineering and documentation

- Python 3.14 or later; Hatch; Ruff; strict mypy; pytest.
- JSON Schema Draft 2020-12.
- Generation must remain deterministic and transactional.
- Each Full dataset is its matching canonical records with only per-record `$schema`
  removed. Adapter Full has no Light counterpart unless separately approved.
- Do not publish the two source registry files as standalone release assets.
  Generate a root `referenceData` object in each JSON distribution containing only
  the manufacturer, brand, and mount-system entries referenced by that dataset.
  Lens Full and Lens Light use identical `referenceData`. Registry IDs are object
  keys, and each value is an extensible object whose current required field is `name`.
- Each dataset's `contentHash` covers its RFC 8785-canonicalized semantic payload:
  `referenceData` plus `products` for lenses, or `referenceData` plus `adapters`
  for adapters.
- Numbers included in a `contentHash` input must satisfy RFC 8785's I-JSON
  requirements. Integer values are limited to the inclusive range
  `-9007199254740991` through `9007199254740991`.
- Lens and adapter schemas are separate contracts. Share only deliberately generic
  public definitions under `schemas/shared/`. Keep schemas used only to validate
  repository source registries under `schemas/internal/`; they have no public `$id`.
- Both datasets use the single `schemaVersion` in `config/versions.json`, while their
  published schema URLs remain namespaced under `lenses/`, `adapters/`, or `shared/`.
- Published versioned schema URLs and contents are immutable. Contract changes use
  a new `schemaVersion` and keep prior version directories available.
- `dataVersion`, the Git tag, and the release date use the same `YYYY.MM.DD`
  value without a `v` prefix.
- Schema, JSON keys, and data narratives are English-first.
- `README.md` and `CONTRIBUTING.md` are the English primary editions;
  `README.ja.md` and `CONTRIBUTING.ja.md` are their Japanese mirrors.
- In bilingual notices such as `LICENSING.md` and directory `LICENSE` files,
  place every English heading and paragraph before its Japanese counterpart.
- Keep paired Markdown paths under `docs/ja/` and `docs/en/`; Japanese is primary.
- `hatch run clean` removes the generated `dist/` and `PRODUCTS.md` artifacts plus
  disposable build output and caches; it must never remove source data, research
  results, schemas, or configuration.

Before declaring work complete, run:

```bash
hatch run generate
hatch run check
hatch run docs:build
```

Before creating a release tag, publish both documentation editions and every public
versioned schema URL. The release workflow excludes repository-only schemas under
`schemas/internal/` when it verifies availability and exact schema contents.

## Completion criteria

A task is complete only when validation passes, generated files are current,
official facts were not guessed, and unresolved questions remain explicit.
