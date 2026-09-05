# Contributing

[日本語](CONTRIBUTING.ja.md)

Reports about product information and direct file edits are welcome in Japanese or English.
If you do not work with JSON, you can simply report the product name and what you noticed through the GitHub form.

## Reporting product information

Provide as much of the following information as you know in the [product addition and correction form](https://github.com/KatsuraIwamoto/z-mount-product-database/issues/new?template=data-correction.yml):

1. Product name and brand
2. Whether the report concerns a lens or related optical product, or a mount adapter
3. The error, missing information, or unlisted product you noticed
4. The URL of an official product page, specification, manual, or similar source from the manufacturer or brand
5. Any useful details, such as where to find the information on the page, regional differences, or points that remain uncertain

You can submit a report even if you cannot determine whether the product is in scope or cannot find a source.
A candidate whose inclusion cannot yet be decided remains a `needs-review` research result for further investigation.

If the official product page is no longer available, manufacturer-run crowdfunding, corporate investor-relations materials and press releases, and authorized-distributor pages may serve as alternative evidence.
Use an exact authorized-retailer product page only to corroborate a released mount configuration and a manufacturer-published model number.
Treat other retailers, reviews, news reports, and forum posts only as leads for further research.

You may use AI to help format your report.
Do not ask it to guess facts such as URLs, product names, or numbers. Submit only information you have verified.

Report problems with distribution generation, repository validation, JSON Schemas, or the documentation site through the [bug report form](https://github.com/KatsuraIwamoto/z-mount-product-database/issues/new?template=bug-report.yml).

## Editing files directly

Choose the file to edit based on the type of change:

| Change | File to edit |
| --- | --- |
| Inclusion decision, sources, or unresolved questions for a lens or related optical product | `research/results/lenses/<brand-directory>/<result-id>.json` |
| Product information for a lens or related optical product | `data/records/lenses/<brand-id>/<product-id>.json` |
| Inclusion decision, sources, or unresolved questions for a mount adapter | `research/results/adapters/<brand-directory>/<result-id>.json` |
| Product information for a mount adapter | `data/records/adapters/<brand-id>/<adapter-id>.json` |
| Manufacturer and brand IDs and their display names | `data/product-manufacturer-brand-registry.json` |
| Mount-system IDs and display names | `data/mount-system-registry.json` |

Set `reviewedOn` only after rechecking the current decision and the affected sources.
Changing `checked` alone does not count as a recheck.

Record the research for each candidate product in one research result.
Every product with an `included` decision requires a corresponding canonical record.
Do not create a canonical record for an `excluded` or `needs-review` result.

Record the official product name and values confirmed by the supporting sources.
Do not guess values that the sources do not confirm or silently choose among conflicting values. Record the question under `unresolved` instead.
Omitted fields, `null`, empty arrays, and `false` each represent a different state.

The distribution files under `dist/` and the root `PRODUCTS.md` are generated files.
Do not edit them directly. Update the corresponding research result, canonical record, or registry, then regenerate the files.

See the following pages for detailed instructions:

- [Reporting and editing product information](https://katsuraiwamoto.github.io/z-mount-product-database/contribute/)
- [Research results](https://katsuraiwamoto.github.io/z-mount-product-database/research/)
- [Value-state rules](https://katsuraiwamoto.github.io/z-mount-product-database/value-rules/)
- [JSON Schema reference](https://katsuraiwamoto.github.io/z-mount-product-database/reference/schemas/)

Do not change the `id` of a product after it first appears in an official GitHub Release, even when correcting its name, brand, specifications, or product type.
Do not assign a published product ID to another product or reuse it after removal.
Before the first official GitHub Release containing the product, a working ID may be corrected during review.

You can also use the `Z Product Compare` Chrome and Edge extension for product research.
The [development and validation guide](https://katsuraiwamoto.github.io/z-mount-product-database/development/#z-product-compare) explains how to install and use it.

## Your first pull request

1. Fork the repository and clone your fork.
2. Create a working branch.
3. Confirm that Python 3.14 or later and Hatch are available. Before editing, run `hatch run check` and `hatch run docs:build` to verify a clean baseline.
4. Edit the required files, run the checks below, and commit only the intended source and generated changes.
5. Push the branch and open a pull request. Describe the changes, provide the source URLs used as evidence, list unresolved questions, and state which checks you ran.

## Checking the inclusion scope

The current scope covers lenses and related optical products, and mount adapters.
Cameras are outside the current scope. If camera data is added in the future, it will use a separate dataset.

The lens and related optical product dataset includes products that attach directly to the Z mount, products supplied with a Z-mount adapter, and products that use a Z-mount adapter dedicated to that lens or product series.
The mount adapter dataset includes products whose primary purpose is adapting another interchangeable-lens mount to the Nikon Z mount.
The initial adapter data covers basic product information, mount pairs, electronic functions, optical and mechanical features, dimensions, and weight.
It does not include large compatibility matrices for combinations of lenses, cameras, and firmware, and it uses a separate JSON Schema from the lens data.

A canonical record requires a confirmed product release announcement or sale.
A development announcement alone remains a `needs-review` research result.

See [Scope and principles](https://katsuraiwamoto.github.io/z-mount-product-database/overview/) for the full criteria.
The [research results guide](https://katsuraiwamoto.github.io/z-mount-product-database/research/) explains source priorities and how to record them.

## Validating changes

Python 3.14 or later and Hatch are required.
See [Development and validation](https://katsuraiwamoto.github.io/z-mount-product-database/development/) to prepare the environment.

Run JSON formatting, distribution generation, repository checks, and the documentation build in this order:

```bash
hatch run format-json
hatch run generate
git diff -- dist PRODUCTS.md
hatch run check
hatch run docs:build
```

After generation, confirm that the intended changes appear in the generated files.
A research-only change may update `PRODUCTS.md`; a canonical lens record change may update Lens Full, Lens Light, and `PRODUCTS.md`; and a canonical mount adapter record change may update Mount adapter Full and `PRODUCTS.md`.
Include only changed generated files in the same pull request as the research result, canonical record, or registry that caused the changes.

When changing documentation, update the corresponding Japanese and English editions in the same pull request.
See [Documentation maintenance](https://katsuraiwamoto.github.io/z-mount-product-database/development/#documentation-maintenance) for the primary edition of each document and how to validate both editions.

## Submitting a pull request

Include the following information in the pull request:

1. What you changed and why
2. The source URLs used as evidence
3. Any unresolved questions
4. The checks you ran

## License

Contributions to research results, canonical records, and registries are provided under CC BY 4.0.
Contributions to code, JSON Schemas, tests, tools, configuration, and documentation are provided under the MIT License.
Submit only material that you have the right to provide under the applicable project license.
If you include third-party text, images, logos, or similar material, identify the rights holder, source, terms of use, and any parts not covered by the permission.
Images and other material attached to an issue as research evidence are not copied directly into public documentation.
See [Licensing](https://katsuraiwamoto.github.io/z-mount-product-database/license/) and [LICENSING.md](LICENSING.md) for the exact scope.
