---
title: null
---

# Z Mount Product Database

This project publishes Nikon Z-mount product information as datasets for searching, comparison, and analysis.
The current datasets cover lenses and related optical products as well as mount adapters.

This documentation explains the project scope, how to use the distribution data, how the data is structured, and how to report errors or missing products.

[Download the product list](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/PRODUCTS.md){ .md-button .md-button--primary }
[Use the distribution data](use-data.md){ .md-button .md-button--primary }

!!! warning "Included does not mean currently available"
    Inclusion means that a product release announcement or sale was confirmed.
    It does not mean that the product is currently sold, in stock, or available.
    Check current official information from the manufacturer or brand before purchase or use.

## Available datasets {#datasets}

<div class="grid cards" markdown>

-   :material-camera-iris:{ .lg .middle } **Lenses and related optical products**

    ---

    Photographic lenses, cinema lenses, teleconverters, pinholes, and similar products sold for the Nikon Z mount.

-   :material-swap-horizontal:{ .lg .middle } **Mount adapters**

    ---

    Products whose primary purpose is adapting another interchangeable-lens mount to the Nikon Z mount.

</div>

See [Scope and principles](overview.md) for the inclusion and exclusion rules.

!!! info "Cameras are outside the current scope"
    If camera data is added in the future, it will use a separate dataset.

## Find what you need {#find-by-purpose}

<div class="grid cards" markdown>

-   :material-format-list-bulleted:{ .lg .middle } **Browse included products**

    ---

    The product list attached to each GitHub Release shows included products and research status across both datasets.
    It also includes official product pages, last-reviewed dates, and links to detailed research results.

    [Download the product list](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/PRODUCTS.md)
    [How to read the evidence and last-reviewed dates](research.md#browse-product-research)

-   :material-download-outline:{ .lg .middle } **Use the distribution data**

    ---

    Choose a distribution file, download it, and follow the usage examples.

    [View the usage guide](use-data.md)

-   :material-file-tree:{ .lg .middle } **Understand the data**

    ---

    Review the data structure and the fields in each dataset.

    [Data model](data-model.md) · [Lenses and related optical products](lens-field-reference.md) · [Mount adapters](adapter-field-reference.md)

-   :material-message-alert-outline:{ .lg .middle } **Report an error or missing product**

    ---

    Report incorrect product information or a missing product without editing JSON.

    [View the reporting guide](contribute.md)

</div>

!!! tip "Compare sources and recorded data side by side"
    When researching product information, use the `Z Product Compare` extension for Chrome or Edge.
    It keeps the source open in the browser while displaying the research result and canonical record in a side panel.

    [How to use Z Product Compare](development.md#z-product-compare)

## References {#references}

- [Glossary](glossary.md): terms and spelling used in this documentation
- [JSON Schema reference](reference/schemas/index.md): data types, required fields, and constraints
- [Development and validation](development.md): generation, validation, documentation builds, and Z Product Compare
- [Licensing](license.md): usage terms and attribution
