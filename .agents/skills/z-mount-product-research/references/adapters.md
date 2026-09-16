# Adapter research

Use for independently marketed mount-conversion products under the policy routes
in `SKILL.md`.

## Paths and schemas

- Research result: `research/results/adapters/<brand-id>/<adapter-id>.json`
- Canonical record: `data/records/adapters/<brand-id>/<adapter-id>.json`
- Research schema: `schemas/adapters/research-result.schema.json`
- Canonical schema: `schemas/adapters/adapter-record.schema.json`

## Evidence and field mapping

- Selectable mount combinations belong in `identity.variants` when they are options
  of the same marketed product. Resolve each configuration's `variantId`.
- If a published retention or rear-protrusion property cannot be tied to a specific
  mount configuration, keep that configuration's value unresolved.
- An accepted photograph can establish visible mount faces, contacts, labels,
  external mechanisms, tripod support, and an unobstructed optical path for the exact
  configuration. Absence claims require views showing the complete relevant exterior.
  Appearance does not establish materials, measurements, movement ranges, hidden
  construction, or electronic capabilities.
- When absence of mount contacts is established, apply the schema's required negative
  values for mount-mediated electronic functions. Check product-side firmware and
  connection services independently in `electronicServices`.
- Use `conversionOptics` for optics built into the adapter for mount conversion.
  When present, retain all applicable specification fields required by the schema,
  using the repository's unknown-value state for unestablished facts.
- Use the shared tripod-support structure for collars, feet, brackets, body mounting
  points, and their tripod-side interfaces.
