# Website verification

Use when inspecting websites or verifying product names, model numbers, and source URLs.
Source eligibility and URL placement follow the repository's
[research rules](../../../../docs/en/research.md) and
[value rules](../../../../docs/en/value-rules.md#urls).

## Choose a sufficient way to inspect the page

Use search results to locate evidence, then open the source itself. A search snippet is
not confirmation of current page contents or the exact product configuration.
Extracted text is sufficient when it preserves the product identity, relevant facts,
and their conditions. Switch to a rendered browser view when text is missing, truncated,
contradictory, or dependent on interaction or images; do not require browser inspection
for every page. Follow official links to specifications, manuals, support, and downloads
rather than repeatedly searching for the same material.

On interactive sites, learn useful navigation from a representative product and reuse
it across the brand. Expand relevant specifications, inspect tabs and footnotes, and
allow the requested section to finish loading before checking it. After changing a
mount, model, region, or language selection, verify which headings, specifications,
images, and URLs actually changed. Shared images or tables may still describe another
configuration. Read numbers with their column headings, units, measurement conditions,
and footnotes; distinguish regional or language editions without silently choosing
between conflicting values.

Treat empty extraction, timeouts, access restrictions, and loading failures as access
problems, not evidence that information or a product is absent. Try a different retrieval
method or official route when it could resolve the problem. Stop equivalent retries
without a new lead and report the inaccessible source and affected fields.
For image evidence, use [Image inspection](image-review.md).

## Distinguish names from identifiers

Verify the product name from official product headings, manuals, or equivalent product
identification. Verify model numbers separately from an explicit manufacturer model
number or model-code designation. Do not infer a model number from a name's digits or
abbreviations, a URL slug, a retailer SKU, or a JAN/EAN/UPC code. A label such as SKU or
Model requires checking what that publisher uses it to identify.

Match each identifier to the product, generation, mount, and sales configuration. Use
accepted retailer evidence only within the corroboration limits of the research rules.
When a model number is unestablished, use `null` in the applicable model-number field;
do not copy the product name as a substitute. If an existing identifier is questionable,
recheck its recorded evidence and report the ambiguity rather than guessing a replacement.

## Verify the destination before recording a URL

Open the actual destination, including redirects, and verify its publisher, product,
generation, configuration, and page role. Do not construct a plausible URL from a slug
or use link text alone as proof. A redirect to a homepage or collection is not an exact
product landing page. Put eligible main product pages in `officialProductPages` and
specifications, manuals, announcements, and support evidence in research `sources`.

Remove tracking parameters and fragments under the URL rules, then reopen the normalized
URL to verify that the evidence remains accessible for the same product and configuration.
Preserve query parameters that select a product or configuration; not every parameter is
tracking. If a fragment-based selector or session state is essential, look for a stable
eligible URL or another accepted source and report any unresolved limitation. Do not
store a normalized URL as configuration-specific evidence when it loses that context.
Retain each material source under the research rules; an access failure alone is not a
reason to delete an existing fact or source or declare discontinuation.
