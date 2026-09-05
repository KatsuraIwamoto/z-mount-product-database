# Glossary

This page defines the meanings and spelling of terms used in the English documentation for the Z Mount Product Database.
JSON keys, enum values, and filenames are shown as code.

## Project and scope

Z Mount Product Database
: The name of the project that publishes reusable datasets of product information related to the Nikon Z mount.

Z mount
: Nikon's Z mount system.
  In JSON, it is represented by the mount-system ID `nikon-z`.

Lenses and related optical products
: Photographic lenses, cinema lenses, teleconverters, pinholes, and similar products sold for the Nikon Z mount.

Mount adapter
: A product whose primary purpose is adapting another interchangeable-lens mount to the Nikon Z mount.

Camera
: A camera that uses the Nikon Z mount.
  Cameras are not included in the current distribution data.
  If camera data is added in the future, it will use a separate dataset.

Candidate product
: A product investigated to determine whether it belongs in the dataset.
  Its research result records one of three decisions: included, excluded, or needs review.

Included product
: A product determined to be in scope and represented by a corresponding canonical record.

## The two datasets

Lens and related optical product dataset
: The dataset containing lenses and related optical products.
  Its file paths and JSON Schema URLs use `lenses`.
  It contains three product types: lenses, teleconverters, and pinholes.

Mount adapter dataset
: The dataset containing mount adapters.
  Its file paths and JSON Schema URLs use `adapters`.
  It has a data structure independent of that of lenses and related optical products, and it does not have the `productType` field.

## Data from research to distribution

Research result
: JSON data that records the inclusion decision for one candidate product and the sources supporting that decision.
  Any open questions are recorded under `unresolved`.
  Research results are stored under `research/results/lenses/` or `research/results/adapters/`.

Canonical record
: Product information verified against supporting sources and recorded in one JSON file for each product determined to be in scope.
  Canonical records are stored under `data/records/lenses/` or `data/records/adapters/`.

Distribution data
: JSON data generated automatically from canonical records for searching, analysis, redistribution, web display, and other uses.
  This term refers to the three files under `dist/` and the files with the same names distributed through GitHub Releases.

Product list
: `PRODUCTS.md`, which presents included products and research status in a human-readable form.
  It is generated automatically from research results and canonical records.

Generated files
: The distribution data and `PRODUCTS.md` created by the generation process.
  These files are not edited directly.

[File layout and data structure](data-model.md)

## Inclusion decisions

Included (`included`)
: The state in which a candidate product has been determined to be in scope.
  The corresponding canonical record ID is recorded under `recordId`.

Excluded (`excluded`)
: The state in which supporting sources establish that a candidate product is outside the project scope.
  The reason for the decision is recorded under `reason`.

Needs review (`needs-review`)
: The state in which there is not enough information to decide whether a candidate product belongs in the dataset.
  Specific questions to investigate next are recorded under `unresolved`.

Open question (`unresolved`)
: A specific question that requires further investigation.
  A needs-review research result records at least one question under `unresolved`.

Last reviewed date (`reviewedOn`)
: The date on which the decision and sources recorded in a research result were last checked.

### Announcements and sale confirmation

Product release announcement
: An official announcement by the manufacturer or brand that a product will be released for sale.
  Its date is recorded as `announcementDate` in the canonical record.

Development announcement
: An announcement previewing a product that is still in development.
  A development announcement alone does not qualify a product for a canonical record; the candidate remains needs review until a product release announcement or sale is confirmed.

Sale confirmation
: Confirmation from a source acceptable for an inclusion decision that the product was actually sold or made available.
  Sale confirmation may qualify a product for inclusion even when no product release announcement page can be found.

[Inclusion decisions and sources](research.md)

## Product information and sources

Manufacturer
: The entity that manufactures a product.
  Canonical records store the manufacturer and brand separately.

Brand
: The name displayed on a product and used to identify it in the market.
  It may be the same as or different from the manufacturer.

Official product page
: The official main page dedicated to the exact product.
  It is recorded under `officialProductPages` in the canonical record.

Source
: A page used to verify an inclusion decision or product information.
  Specifications, manuals, announcements, support pages, and similar evidence are recorded under `sources` in the research result.

Registry
: Data that maintains the correspondence between IDs and names used in the datasets.
  The project has a manufacturer and brand registry and a mount-system registry.

ID
: A string that identifies a product, research result, or registry entry.
  Uniqueness and publication rules depend on the contract for the identified object.

Product ID
: The `id` in a canonical product record and distribution entry.
  It is unique within its namespace.
  It uses a human-readable slug based on the brand and product name, with lowercase letters and numbers separated by hyphens.
  The relationship between its text and product attributes is not part of the public data contract.
  Do not parse the manufacturer, brand, product name, specifications, or product type from `id`; use the dedicated fields instead.
  After this project first publishes the ID in a GitHub Release, it is not changed, assigned to another product, or reused after removal.

Composite key
: A key that combines multiple values to identify one record uniquely.
  In this project, it combines the dataset namespace and product ID.
  Lens Full and Light use `("lenses", id)`, while Mount adapter Full uses `("adapters", id)`.
  Because the same `id` may be used in different namespaces, do not use `id` alone as the primary key when combining multiple datasets.
  A stable composite key does not guarantee that the product will remain in the latest or every later release.

[Lens product fields](lens-field-reference.md)

[Mount adapter product fields](adapter-field-reference.md)

## Distribution files and retrieval methods

Lens Full
: `z-mount-lenses.full.json`, which combines the canonical records for lenses and related optical products and includes every recorded field.

Lens Light
: `z-mount-lenses.light.json`, which retains only the fields needed by the existing website display from Lens Full.
  It contains the same products in the same order as Lens Full and does not rewrite their IDs or retained values.

Mount adapter Full
: `z-mount-adapters.full.json`, which combines the canonical mount adapter records and includes every recorded field.
  There is no Light distribution for mount adapters.

Latest release
: A method for retrieving the most recent distribution data available from GitHub Releases at the time of access.
  Its URL uses `releases/latest/download/`.

Version-pinned release
: A method for continuing to retrieve the same distribution by including a specific `dataVersion` in the URL.

[Download methods and usage examples](use-data.md)

## Versions and validation

JSON Schema
: Validation rules defining JSON types, required fields, permitted values, and conditional constraints.
  This project uses JSON Schema Draft 2020-12.

Schema version (`schemaVersion`)
: The version of the JSON Schema bundle shared by all distribution data.
  It uses SemVer with three dot-separated integers, such as `1.0.0`.

Data version (`dataVersion`)
: An identifier for a published data release.
  The Git tag uses the same value in `YYYY.MM.DD` format.

Content hash (`contentHash`)
: A SHA-256 value used to compare the contents of distribution data.
  It is calculated separately for each distribution from a content object containing `referenceData` and `products` or `adapters` after RFC 8785 canonicalization.

Repository validation
: Checks for repository-wide consistency that JSON Schema alone cannot enforce.
  These checks cover filenames and placement, IDs, registry references, and correspondence across files.

[JSON Schema types and constraints](reference/schemas/index.md)

[Value states and numeric values](value-rules.md)
