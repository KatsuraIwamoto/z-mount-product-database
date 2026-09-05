---
name: z-mount-product-research
description: Research Nikon Z-compatible lens-dataset products or mount adapters using accepted published evidence, prioritizing official sources; decide inclusion, exclusion, or needs-review; and update matching canonical data and research results. Use for product additions, corrections, official specification checks, inclusion decisions, duplicate review, or bounded re-research. Do not use for generated distribution editing, retailer-only research, compatibility-matrix expansion, general camera advice, or release publication.
---

# Z-mount product research

Follow `AGENTS.md`, current schemas, and executable validation. They remain authoritative.
Read only the relevant pages under `docs/ja/` or `docs/en/` when a field needs explanation.

## Route by dataset

Before changing product data, read the one dataset reference that applies:

- For a lens, teleconverter, pinhole product, or its supplied or product-dedicated
  adapter configuration, read [Lens-dataset research](references/lenses.md).
- For an independently marketed product whose primary purpose is converting another
  interchangeable-lens mount to Nikon Z, read
  [Mount-adapter research](references/adapters.md).

If a request spans both datasets, handle each candidate under its matching reference.

## Shared workflow

1. Locate the matching research result and any canonical record, or choose a stable ID.
2. Check the manufacturer and brand registry before settling canonical spellings.
3. Research exact manufacturer- or brand-official pages and primary documents first.
4. Decide `included`, `excluded`, or `needs-review` without guessing.
5. Update the research result. Add or edit a canonical record only when `included`.
6. Add registry entries only for newly required canonical spellings or identifiers.

## Evidence handling

- Prefer exact official product pages, specifications, manuals, and announcements.
- On manufacturer sites with interactive content, inspect a representative rendered
  product page and support page for accordions, tabs, mount selectors, expanded sections,
  download areas, and image-based specifications. Apply the discovered official routes
  across the investigated products instead of relying only on initially visible text.
- When a specification section exposes only a teaser, activate its expansion control and
  inspect the rendered content again. Do not assume an initial page or accessibility
  snapshot contains rows that remain collapsed.
- Treat firmware-update capability, a USB connection, and an actually published firmware
  update as separate facts. Set a publication fact to `true` only when an official update
  file or release entry exists; absence of one does not establish `false` without an
  explicit official negative statement.
- If an exact page is unavailable, manufacturer-run crowdfunding, corporate IR or
  press releases, and authorized-distributor product or announcement pages may support
  facts.
- An exact authorized-retailer listing may corroborate a released mount configuration
  and a manufacturer-published model number. A directly linked image published by that
  authorized retailer may also support facts directly visible on the product when the
  exact product and configuration are established and the relevant area is shown clearly.
  Store the direct image URL with `sourceType: image`; keep the containing listing as a
  separate source when it establishes identity or configuration. Use multiple states or
  video for movement-dependent facts. Do not infer hidden construction, materials,
  measurements, electronic functions, protection claims, compatibility, or release status
  from appearance. Treat other retailer, review, news, marketplace, and forum pages only
  as leads for further research; do not use them as canonical or inclusion evidence unless
  an accepted source verifies the fact.
- Put only exact-product main landing pages in `officialProductPages`. Use `[]` when no
  eligible landing page remains, and keep other evidence in the research result. An
  unavailable landing page does not by itself establish discontinuation.
- Before applying a manual, support file, or similarly named product page, establish that
  it covers the same marketed product, generation, and mount configuration. A shared
  short name is insufficient when generation labels or known specifications differ.
- Store each canonical URL once without fragments or tracking parameters. Keep every
  material source; do not remove one solely because another checks the same element or
  publishes different information.
- For lens and adapter research, classify each source with `publisherRelationship` and `sourceType`,
  list checked canonical product areas as schema-aligned field paths in `checked`, and
  put only non-canonical inclusion or release checks in `decisionChecks`. Use meaningful
  field groups such as `lens.focus`, not individual numeric leaves. Use the exact
  schema-listed path for a separately listed child group; a parent such as `physical` or
  `mount` does not cover `physical.weightMeasurements` or `mount.electronicContacts`.
  Use `note` only when those structured fields cannot preserve a source-specific fact
  needed to review the decision. Under `sources`, do not copy published values, compare
  sources, characterize differences as errors, justify a value choice, or narrate the
  research workflow.
- Use notes only for source-explicit factual context needed to interpret the evidence,
  such as a measurement basis or the scope of an officially named variant. Omit notes
  otherwise.
- Preserve published names and numbers in canonical data. When checked sources do not
  establish a single value, leave the fact unresolved under the normal value-state rules
  and add a neutral, actionable question under `unresolved` rather than choosing silently.
- For `officialName`, identify the stable manufacturer designation rather than copying a
  sentence fragment. Prefer an official glossary, technology page, specification label,
  heading, badge, or printed control label. Ignore sentence capitalization and trademark
  registration symbols; preserve lexical symbols such as the asterisk in `T*`. Preserve a
  stable published technical designation even when the normalized `type` represents the
  same general class: `type` is for cross-brand grouping and `officialName` is for the
  manufacturer's terminology. Omit sentence-only descriptions and ordinary control names
  that merely restate `type` without adding a product-specific label. Prefer the official
  English designation when an equivalent English page exists; otherwise preserve the
  published designation rather than inventing a translation. Apply one spelling within
  the same brand and field, but do not merge identically worded technologies across brands.

## Decisions and canonical facts

- `included` requires `recordId`; the result ID, record ID, file stem, and canonical ID
  match, as do the research subject and canonical identity.
- `excluded` requires a concise evidence-based `reason`.
- `needs-review` requires at least one actionable question under `unresolved`.
- Use the actual review date for `reviewedOn`. Changing `checked` alone does not justify
  a new date. When an established canonical value or its `checked` coverage changes,
  recheck the affected sources and use only the date on which the current decision and
  those sources were rechecked. Keep narratives in English while preserving official
  product names in their published script.
- For an included result, ensure that `checked` collectively covers every major canonical
  field group containing an established value. A URL retained in `officialProductPages`
  must also appear in `sources` with that field checked.
- Do not retain prompts, chat logs, model names, batch metadata, or retrieval telemetry.
- Use the brand registry ID as the canonical parent directory and resolve both identity
  names in the registry.
- Omit structurally inapplicable fields; use `null` for applicable values not established
  by accepted published evidence, `[]` for a confirmed empty collection, and `false` only
  for a confirmed negative fact.

## Completion

Ensure `dataVersion` is on or after the actual `reviewedOn` date. For an included result,
also ensure that canonical lifecycle dates are no later than `reviewedOn`. Never edit `dist/` or
`PRODUCTS.md` directly. After changing product data or research, run `hatch run generate`,
then complete the checks required by `AGENTS.md`.
