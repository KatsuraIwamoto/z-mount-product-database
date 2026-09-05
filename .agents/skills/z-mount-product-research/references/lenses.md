# Lens-dataset research

Use this reference only for products stored under the lens dataset.

## Paths and schemas

- Research result: `research/results/lenses/<brand-id>/<product-id>.json`
- Canonical record: `data/records/lenses/<brand-id>/<product-id>.json`
- Research schema: `schemas/lenses/research-result.schema.json`
- Canonical schema: `schemas/lenses/product-record.schema.json`

## Inclusion

Include an independently sold or officially release-announced optical product when the
manufacturer offers a Nikon Z configuration that attaches directly, including the
manufacturer's own interchangeable rear mount. A development announcement alone remains
`needs-review` until an official product release announcement or confirmed sale is found.

An adapter configuration belongs in this dataset only when the official Nikon Z product
kit supplies the adapter, or when a separately sold adapter is dedicated to that lens or
an explicitly named product series. Record it under `mount.adapter`.

Exclude broad system adapters such as FTZ, generic or third-party adapters, unofficial
conversions, rumors, unreleased prototypes, and products offered officially only for
another mount. Independently marketed mount-conversion products belong in the adapter
dataset instead.

## Canonical record

- Select exactly one `lens`, `teleconverter`, or `pinhole` block with `productType`.
- Use the official product release-announcement date for `lifecycle.announcementDate`,
  never a development-announcement date.
- For an optional `mount.adapter`, `dedicatedToProduct` must be `true`.
- Record `mount.adapter.nativeMountSystemId` as a registered mount-system ID rather than
  free text.
- Use structured `metadataTransmission` for data carried through electronic mount contacts.
  Keep firmware-update and product-side connection facts in the independent shared
  `electronicServices` block.
- Every zoom lens has `lens.zoom`; use `null` for its drive or optical zooming systems when
  accepted published evidence does not establish them. Prime lenses omit the block.
- Keep applicable external-length and retractable-storage fields present for lenses, using
  `null` for behavior not established by accepted published evidence.
- Use the shared tripod-support structure and keep tripod components out of `accessories`.
- Treat `lens.specialized` features as composable rather than exclusive subtypes.
- Preserve published IDs and the existing Lens Light projection; generated Full and Light
  files are not source data.

## Efficient brand re-research

Before browsing a manufacturer's site, summarize missing or `null` canonical facts for
its included lenses. Prioritize factual coverage in this order:

1. focal length, maximum and minimum aperture, coverage, minimum focus distance,
   reproduction magnification, angle of view, and optical construction;
2. dimensions, weight, and filter interfaces;
3. focusing systems and external-length behavior, stabilization, tripod support,
   controls, protection claims, accessories, variants, and electronic services.

Use one representative current product to learn the manufacturer's interactive product,
support, download, and official-store navigation. Then reuse those routes across the
brand, reserving manuals, images, and videos for facts still unresolved after the common
pages are checked. Finish with a missing-field summary so facts not established by
accepted published evidence remain explicit and low-value searches are not repeated.

Before finishing, compare the investigated records and research results with their
pre-review state. Report newly established facts separately from fields changed to
`null`, removed canonical facts, removed `officialProductPages` entries, and added or
removed research notes. Do not let a net increase in populated fields conceal a
regression or deletion.

## Field evidence boundaries

- A specification from another mount configuration may support optical facts when
  official evidence establishes the same marketed lens and optical design. Do not carry
  over dimensions, weight, controls, connections, firmware, accessories, or variants
  without evidence for the Nikon Z configuration.
- When an official dimension or weight is explicitly approximate, preserve the value
  with the schema's `approximate: true` qualifier instead of leaving it unresolved.
- When a degrees-and-minutes value or a `1:n` ratio must be normalized to a single
  decimal number, round the converted result to six decimal places and omit trailing
  zeroes. The stored value must retain enough precision to recover the source notation
  at its published precision.
- Accepted product photographs may establish clearly visible controls, interfaces,
  variants, supplied or integrated external components, printed markings, and the absence
  of tripod support when the relevant exterior is fully shown. This includes a directly
  linked image from an exact authorized-retailer listing under the shared evidence rules.
  Do not use a single static image to decide movement during focus or zoom; use an explicit
  mechanism description, a manual, multiple accepted states, or accepted video.
- Before treating a product photograph as evidence for a mount-specific fact, verify that
  the displayed mount selection and the photograph refer to the same configuration.
  A selectable Nikon Z option does not make a default or shared photograph Nikon Z-specific.
- Distinguish a normal diaphragm and its aperture range from a fixed opening, removable
  aperture disk, texture aperture, or other effect insert. Record each only when the
  schema field preserves its published role without changing its meaning.
- When a published value depends on a named format, variant, or condition that the schema
  cannot preserve, do not force it into a broader value such as `other` merely to retain
  the number. Leave it unrecorded until the condition can be represented faithfully.
- Do not map a distance measured from the product front to the sensor plane, film plane,
  or flange directly to the product's physical length. Record `lengthMm` only when the
  official measurement is lens length or its published basis can be preserved faithfully.
- When official specifications and mount-specific photographs establish that electronic
  contacts are absent, set `mount.electronicContacts.present` to `false`. This does not
  rule out a separately published direct USB, dock, configuration, or control service;
  record such product-side facts in `electronicServices` when applicable.
- Preserve the scope and strength of protection wording. Component coating claims do not
  become product-wide environmental protection, and water-resistant wording does not
  become waterproof wording.
