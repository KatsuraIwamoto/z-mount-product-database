# Lens research

Use for lenses, teleconverters, pinhole products, and their eligible adapter
configurations under the policy routes in `SKILL.md`.

## Paths and schemas

- Research result: `research/results/lenses/<brand-id>/<product-id>.json`
- Canonical record: `data/records/lenses/<brand-id>/<product-id>.json`
- Research schema: `schemas/lenses/research-result.schema.json`
- Canonical schema: `schemas/lenses/product-record.schema.json`

## Configuration and field mapping

- A manufacturer's interchangeable rear mount can establish a directly attachable
  Nikon Z configuration. Apply the inclusion rules to supplied or dedicated
  adapters; broad system and third-party adapters do not establish lens eligibility.
- Specifications from another mount may support optical facts only when official
  evidence establishes the same marketed lens and optical design. Dimensions, weight,
  controls, connections, firmware, accessories, and variants need Nikon Z evidence.
- Use `metadataTransmission` for data carried through mount contacts and the separate
  `electronicServices` block for product-side connections and firmware services.
  Confirmed absence of contacts does not rule out direct USB or dock services.
- Keep applicable zoom, external-length, and retractable-storage fields even when
  their values are unknown. Use the current schema to distinguish applicability from
  missing evidence; prime lenses omit `lens.zoom`.
- Put tripod components in the shared tripod-support structure, not `accessories`.

## Measurements and visual evidence

- Preserve officially approximate dimensions and weights with `approximate: true`.
- When degrees-and-minutes or a `1:n` ratio must become a decimal number, round to six
  decimal places and omit trailing zeroes. Retain enough precision to recover the
  source notation at its published precision.
- Accepted photographs can establish visible controls, interfaces, variants, supplied
  or integrated external components, and printed markings. Absence of tripod support
  requires the relevant exterior to be fully shown. Focus or zoom movement needs an
  explicit mechanism description, a manual, multiple accepted states, or accepted video;
  one static image is insufficient.
- Distinguish a normal diaphragm and aperture range from fixed openings, removable
  aperture disks, texture apertures, and effect inserts. Use fields that preserve
  their published roles.
- If a format, variant, or measurement condition cannot be represented faithfully,
  leave the fact unresolved and report the schema limitation. Do not force it into
  a broader value such as `other` merely to retain a number.
- A distance from the product front to the sensor plane, film plane, or flange is
  not automatically physical lens length. Use `lengthMm` only for published lens
  length or when its measurement basis can be preserved faithfully.
- Preserve the scope and strength of protection claims: component coatings do not
  establish product-wide protection, and water resistance does not mean waterproofing.
