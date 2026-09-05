# Z Mount Product Database

This project publishes information about Nikon Z-mount products as reusable datasets.

It currently covers lenses and related optical products sold for the Z mount, as well as mount adapters whose primary purpose is adapting another interchangeable-lens mount to the Nikon Z mount.

Inclusion means that a product release announcement or sale has been confirmed.
It does not mean that the product is currently sold, in stock, or otherwise available.

[日本語](README.ja.md)

## Why this project exists

Official information about Z-mount products is spread across manufacturer and brand websites.
Separate pages may be published for different regions, with different content or terminology.
Earlier information may also become difficult to find after a website is updated.

Using this information directly for searches, comparisons, and aggregation across manufacturers takes considerable work.
This project prioritizes official information, records accepted evidence in a common format, and preserves it as reusable data.

## Design principles

- The lens and mount adapter datasets use separate distributions and JSON Schemas, sharing only generic registries and definitions.
- Products store stable manufacturer, brand, and mount-system IDs, with display names available from `referenceData` in each distribution JSON.
- The data distinguishes a field that does not apply, a value that applies but is not established by accepted published evidence, a confirmed empty collection, and a confirmed negative.
- JSON Schema validation and deterministic generation detect differences between editable files and the distribution data.

## Included data

| Dataset | Scope |
| --- | --- |
| Lenses and related optical products | Photographic lenses, cinema lenses, teleconverters, pinholes, and similar products sold for the Z mount |
| Mount adapters | Products whose primary purpose is adapting another interchangeable-lens mount to the Nikon Z mount |

Lenses and related optical products are collected in one dataset, while mount adapters are collected in a separate dataset.

Cameras are outside the scope of the current distributions.
If camera data is added in the future, it will use a separate dataset.

See [Scope and principles](https://katsuraiwamoto.github.io/z-mount-product-database/overview/) for the full inclusion criteria.

### Main public files

| File | Contents |
| --- | --- |
| [PRODUCTS.md](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/PRODUCTS.md) | List of included products and research status |
| [z-mount-lenses.full.json](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/z-mount-lenses.full.json) | All recorded fields for lenses and related optical products |
| [z-mount-lenses.light.json](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/z-mount-lenses.light.json) | Only the fields needed to display lenses and related optical products on the web |
| [z-mount-adapters.full.json](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/z-mount-adapters.full.json) | All recorded fields for mount adapters |

These four files are distributed as GitHub Release assets.

`z-mount-lenses.light.json` contains the same products in the same order as `z-mount-lenses.full.json`.
It retains only the fields needed for web display and does not rewrite their values.

See the [distribution data guide](https://katsuraiwamoto.github.io/z-mount-product-database/use-data/) for the latest and version-specific downloads and for JavaScript and Python examples.

## Example uses

The distribution data can be used to:

- Find products that meet specified criteria
- Compare product information
- Aggregate and visualize data by brand, product type, specification, or other attributes
- Integrate product data into websites and applications
- Provide source data for research and analysis

### Search and visualization on a website

The [Nikon page on cercidiphyllum.jp](https://cercidiphyllum.jp/en/nikon/) uses this project's distribution data for product search and aggregate visualizations.

## From research to distribution

The distribution data and `PRODUCTS.md` are produced through the following process:

1. **Research results:** Record the findings for each candidate product in one JSON file.
   Each file preserves the inclusion, exclusion, or needs-review decision, its sources, and any unresolved questions.
2. **Canonical records:** Record each included product in one JSON file.
   Do not guess values that cannot be confirmed from accepted published evidence.
3. **Distribution data:** Generate the distribution JSON files automatically from the canonical records.

`PRODUCTS.md` is also generated automatically from the research results and canonical records.

## Documentation

The [documentation site](https://katsuraiwamoto.github.io/z-mount-product-database/) explains the inclusion criteria, data structure, and meaning of each field.
It also covers how to use the distributions and how to research and edit product information.

JSON Schemas, JSON keys, and descriptive text stored in the data are written in English.
README and CONTRIBUTING are available in both English and Japanese.
The documentation site's English edition is translated from the Japanese edition using AI.

## Contributing

If you find incorrect or missing product information or a product that has not been included, report it through the [product addition and correction form](https://github.com/KatsuraIwamoto/z-mount-product-database/issues/new?template=data-correction.yml).
Reports are welcome in Japanese or English.
You do not need to edit JSON.

Provide the product name and describe what caught your attention.
Include the manufacturer's official page if you know its URL.
You can report an uncertain concern, such as a product that may be missing or a value that appears to differ from an official page.

See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to edit the data directly.
The [development and validation guide](https://katsuraiwamoto.github.io/z-mount-product-database/development/) explains how to prepare the development environment and run the checks.

### Z Product Compare for product research

The repository includes `Z Product Compare`, a Chrome and Edge extension for researching product information.
It lets you keep a source open in the browser while viewing the research result and canonical record in a side panel.
The same panel also shows the current repository validation results.

<a href="docs/en/assets/images/z-product-compare.webp">
  <img src="docs/en/assets/images/z-product-compare.webp" alt="Example of Z Product Compare, with an area for the official product page on the left and a canonical record on the right" width="840">
</a>

*Example of Z Product Compare. During use, the corresponding official product page appears on the left.*

Run `hatch run review` to start the local server used by `Z Product Compare`.
See [Using Z Product Compare](https://katsuraiwamoto.github.io/z-mount-product-database/development/#z-product-compare) for installation and operating instructions.

## License

- JSON files containing product information and research results, the three distribution JSON files, and `PRODUCTS.md`: [CC BY 4.0](LICENSES/CC-BY-4.0.txt)
- Code, JSON Schemas, documentation, and configuration: [MIT License](LICENSES/MIT.txt)

This is a summary.
See [LICENSING.md](LICENSING.md) for the exact scope and recommended attribution.
The license texts linked above contain the formal terms, including warranty disclaimers and limitations of liability.

> [!IMPORTANT]
> CC BY 4.0 applies only to copyright and similar rights that this project can license.
> The project does not claim ownership of factual product specifications, third-party names, or trademarks.
> This independent project is not affiliated with any manufacturer, including Nikon Corporation, and is neither authorized nor endorsed by any manufacturer.
