# Reporting and editing product information

Use the GitHub forms to report incorrect product information or missing products.
If you can edit JSON, you may also update the research result and canonical record directly and open a pull request.

<div class="grid cards" markdown>

-   :material-message-alert-outline:{ .lg .middle } **Report product information**

    ---

    Report the product name and what you noticed, with whatever details you have.
    You do not need to write JSON or JSON Schema.

    [Open the product correction and addition form](https://github.com/KatsuraIwamoto/z-mount-product-database/issues/new?template=data-correction.yml){ .md-button .md-button--primary }

-   :material-file-edit-outline:{ .lg .middle } **Edit files directly**

    ---

    Check sources published by the manufacturer or brand, then update the applicable research result or canonical record.

    [View the direct editing guide](#direct-edit)

</div>

## Report product information

The [product correction and addition form](https://github.com/KatsuraIwamoto/z-mount-product-database/issues/new?template=data-correction.yml) asks for:

1. Report type
2. Whether the report concerns a lens or related optical product, or a mount adapter
3. Product name
4. The current information and the error or omission you noticed
5. An official product page, specification, manual, or similar URL from the manufacturer or brand, if known
6. Additional context such as the relevant place on the page, regional differences, or images

For the report type, choose "Correction", "Missing product", "Possible exclusion", "Official URL change", or "Other".
If you do not know which dataset applies, choose "Unsure".

!!! info "You can report even if you are unsure"

    You can report a product that may be missing or a value that appears to differ from an official product page.
    If you cannot find an official product page or another source, the product name and what you noticed are enough.
    When the inclusion decision remains uncertain, the project continues the research with a `needs-review` result.

You may use AI to edit the wording of your report.
Do not ask it to invent facts such as URLs, product names, or numeric values; submit only information you could verify.

## Report a bug

Use the [bug report form](https://github.com/KatsuraIwamoto/z-mount-product-database/issues/new?template=bug-report.yml) for problems with repository validation, distribution generation, or JSON Schema.
The same form covers documentation site and CI problems.
Use the product form in the previous section for incorrect product information or missing products.

## Edit files directly { #direct-edit }

Choose the source file that matches the change.
Distribution data and the product list are generated, so do not edit them directly.

| Change | File to edit |
| --- | --- |
| Lens or related optical product decision, sources, or unresolved questions | `research/results/lenses/<brand-directory>/<result-id>.json` |
| Lens or related optical product information | `data/records/lenses/<brand-id>/<product-id>.json` |
| Mount adapter decision, sources, or unresolved questions | `research/results/adapters/<brand-directory>/<result-id>.json` |
| Mount adapter product information | `data/records/adapters/<brand-id>/<adapter-id>.json` |
| Manufacturer and brand IDs and their display names | `data/product-manufacturer-brand-registry.json` |
| Mount-system IDs and display names | `data/mount-system-registry.json` |

!!! warning "Do not edit generated files"

    The distribution data under `dist/` and `PRODUCTS.md` are generated.
    Update the required source files, then run `hatch run generate`.

!!! tip "Use Z Product Compare for research"

    The `Z Product Compare` extension for Chrome and Edge keeps a source open in the browser while displaying the research result and canonical record in a side panel.

    [View the installation and usage guide](development.md#z-product-compare)

### Research results and canonical records

Record the investigation of each candidate product in one research result.
An `included` decision requires a corresponding canonical record.
Do not create a canonical record for an `excluded` or `needs-review` decision.

See [Research results](research.md) for how to record the decision, sources, `reviewedOn`, and `unresolved`, and see [Scope and principles](overview.md) for the inclusion rules.

### Record product information

Preserve the official product name and the values confirmed by supporting sources.
Do not guess unpublished values or arbitrarily choose one of several conflicting values.

Follow [Value-state rules](value-rules.md) to distinguish field omission, `null`, empty arrays, and `false`.
Use the [field reference for lenses and related optical products](lens-field-reference.md) or [mount adapter field reference](adapter-field-reference.md) for field meanings, and the [JSON Schema reference](reference/schemas/index.md) for exact types, required fields, and permitted values.

### Last-reviewed date and data version

Set the research result's last-reviewed date, `reviewedOn`, to the date on which you actually checked the decision and its sources.
Changing `checked` alone does not justify updating `reviewedOn`.
When an established canonical value or its `checked` coverage changes, recheck the affected sources and record the date on which the current decision and sources were actually checked.
If `reviewedOn` is later than the current `dataVersion`, temporarily set `dataVersion` in `config/versions.json` to the same date as the latest `reviewedOn` so the pull request can pass validation.
The published `dataVersion` is the release date in Asia/Tokyo.

## Validate changes

Python 3.14 or later and Hatch are required.
See [Development and validation](development.md) for environment setup.

Run JSON formatting, distribution generation, repository validation, and the documentation build in this order:

```bash
hatch run format-json
hatch run generate
git diff -- dist PRODUCTS.md
hatch run check
hatch run docs:build
```

After generation, confirm that the generated files contain only the intended changes.
A research-only change may update `PRODUCTS.md`; a canonical lens record change may update Lens Full, Lens Light, and `PRODUCTS.md`; and a canonical mount adapter record change may update Mount adapter Full and `PRODUCTS.md`.
Include only the generated files that actually differ in the same pull request as the research result, canonical record, or registry that caused the change.

When changing documentation, update the corresponding Japanese and English files in the same pull request.
See [Documentation maintenance](development.md#documentation-maintenance) for the primary edition and validation method for each document pair.

## Open a pull request

Describe:

1. What changed and why
2. The source URLs used for verification
3. Any unresolved questions
4. The checks you ran

Contributions to research results, canonical records, and registries are provided under CC BY 4.0.
Contributions to code, JSON Schema, tests, tools, configuration, and documentation are provided under the MIT License.
Submit only material that you have the right to provide under the applicable project license.
If you include third-party text, images, logos, or similar material, identify the rights holder, source, terms of use, and any portions not covered by the permission in the pull request or issue.
Images and other material attached to an issue as research evidence are not copied directly into public documentation.
See [Licensing](license.md) for the exact scope.

## Related pages

- [Research results](research.md): how to record decisions, sources, and unresolved questions
- [Scope and principles](overview.md): inclusion rules for lenses, related optical products, and mount adapters
- [Value-state rules](value-rules.md): the meanings of omission, `null`, empty arrays, and `false`
- [Data model](data-model.md): relationships among research results, canonical records, and distribution data
- [Development and validation](development.md): development environment, generation, and validation
