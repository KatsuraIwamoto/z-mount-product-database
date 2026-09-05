# Mount-adapter research

Use this reference only for independently marketed mount-conversion products stored under
the adapter dataset.

## Paths and schemas

- Research result: `research/results/adapters/<brand-id>/<adapter-id>.json`
- Canonical record: `data/records/adapters/<brand-id>/<adapter-id>.json`
- Research schema: `schemas/adapters/research-result.schema.json`
- Canonical schema: `schemas/adapters/adapter-record.schema.json`
- Mount identifiers: `data/mount-system-registry.json`

## Inclusion

Include a marketed product whose primary purpose is converting another interchangeable-
lens mount to Nikon Z after an official release announcement or confirmed sale. Keep a
development-only announcement as `needs-review`.

Exclude extension tubes, filter-only adapters, focal reducers without mount conversion,
and accessories whose mount-conversion role is incidental. A lens-supplied or
product-dedicated adapter configuration may instead belong in the lens record.

Use one record for the same marketed product. Put selectable mount combinations or other
officially named options in `identity.variants` and resolve every `variantId`.

## Canonical record

- Adapter records are independent from lens records. Do not add `productType`, `lens`,
  `teleconverter`, or `pinhole` blocks.
- Every `cameraSideMountSystemId` is `nikon-z`. Every `lensSideMountSystemId` is a different,
  registered mount ID.
- Keep lens retention and rear-protrusion limits in the applicable mount configuration.
  Use `null` when the product supports multiple configurations and accepted published
  evidence does not establish which configuration a published property covers.
- If `electronicContacts` is `false`, autofocus, camera-controlled aperture, metadata
  transmission, lens-stabilization communication, manual-focus assistance, lens-power
  transmission, and recording-trigger transmission are confirmed negative values.
  Record firmware updates and their connection methods separately in `electronicServices`.
- An accepted photograph may establish visible mount faces, contacts, labels, external
  mechanisms, tripod support, and an unobstructed optical path when the exact adapter
  configuration and the relevant area are shown clearly. Absence claims require enough
  views to show the complete relevant exterior. Do not infer materials, measurements,
  movement ranges, hidden construction, or electronic capabilities from appearance.
- Use `conversionOptics` for optics built into the adapter for mount conversion. When
  `present` is `true`, keep all seven applicable specification fields and use `null` for
  values not established by accepted published evidence.
- Record mechanisms as typed objects. Keep shift, tilt, and rotation measurements inside
  the matching mechanism so its type, conditions, and movement data remain coupled.
- Use the shared tripod-support structure for collars, feet, brackets, body mounting
  points, and their tripod-side interfaces.
- Record basic identity, mount-pair, electronic, optical, mechanical, and physical facts.
  Do not add large lens, camera, or firmware compatibility matrices to the initial model.
- Adapter Full has no Light counterpart; generated distributions are not source data.
