# Image inspection and uncertain findings

Use this reference when inspecting product images or deciding how to handle ambiguous
findings. Apply the source and value rules in [Research results](../../../../docs/en/research.md).

## Inspect what the claim requires

Establish the product, generation, mount, and sales configuration before combining views.
A mount selector or shared gallery is not proof that every image shows the selected mount.
Inspect the actual images at sufficient resolution; captions, search snippets, and OCR
alone do not establish visual facts. Check uncertain markings against the image and
accepted text sources rather than guessing digits, units, or symbols.

For exterior component inspection, follow the four-sided coverage rule in the research
policy. Keep track of top, bottom, left, and right views relative to the product, not the
image orientation. Add front, rear, or covered-area views as needed. Repeated angles,
crops, reflections, and occlusions do not resolve missing coverage. Report missing views
when they prevent a conclusion; do not create a separate inspection ledger in the data.

Separate a visible part from its movement and function. A grooved ring may be decorative;
a seam need not be a movable or detachable joint. Seek official control diagrams or
operating instructions, or accepted views showing the relevant action and its result.
Rotation alone does not establish aperture or focus control. Apply the same distinction
to removable hoods, rotating tripod collars, switches, connectors, and fixed covers.
A photograph of an accessory attached to the product does not establish package contents.

## Escalate the uncertain finding, not the whole task

Flag a finding for human review when accepted evidence still permits materially different
interpretations after a focused check. Typical cases include:

- Conflicting product, generation, mount, or sales-configuration identification.
- Uncertain control function, movement, detachability, or absence due to blind spots.
- Illegible markings or unclear measurement conditions, units, or included components.
- Conflicting published specifications or an unclear product-versus-variant boundary.
- Proposed removal of an established fact, source, or official URL, or replacement with
  `null`, when the underlying evidence is still ambiguous.

In the user-facing report, identify the product and field, link the relevant evidence,
explain what remains uncertain, and state the specific question to resolve. Keep source
comparisons and review rationale out of canonical notes and source notes; use neutral,
actionable `unresolved` questions in research results. Continue independent research and
validation rather than blocking the whole batch for a single uncertain fact.

Use `needs-review` for an unresolved inclusion decision, not as a generic flag for every
unknown specification. If inclusion is established, retain `included` and represent the
unknown field using the schema's value states, with an `unresolved` question. Do not
invent a control type to fill an array, use `[]` for an unchecked collection, or delete
supported facts merely because new photographs omit them. If the schema cannot express
a partially known finding, leave the affected value unestablished and report the limit.
Human judgment does not replace accepted evidence; unresolved facts may remain unresolved.
