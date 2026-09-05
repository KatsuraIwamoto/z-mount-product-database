# JSON Schema reference

This reference is for data consumers who validate the distribution data and developers who modify the data structures.
It explains permitted values and conditional constraints for each JSON Schema.
If you first want to understand what each field represents and how it appears in actual data, see the [field reference for lenses and related optical products](../../lens-field-reference.md) or the [mount adapter field reference](../../adapter-field-reference.md).

This project's JSON Schemas conform to JSON Schema Draft 2020-12.
The published URL namespace is divided into lenses and related optical products, mount adapters, and shared definitions.
The complete set of JSON Schemas uses one schema version, recorded in the distribution data as `schemaVersion`.

## Choose a JSON Schema for your purpose {#choose-schema}

The first page to open depends on the type and scope of the data you want to inspect.

| What you want to inspect | Start with |
| --- | --- |
| The complete Lens Full or Lens Light distribution | [dataset-full](lenses/dataset-full.md) or [dataset-light](lenses/dataset-light.md) |
| One product in Lens Full or Lens Light | [product-full](lenses/product-full.md) or [product-light](lenses/product-light.md) |
| One canonical record for a lens or related optical product | [product-record](lenses/product-record.md) |
| The complete Full distribution for mount adapters | [dataset-full](adapters/dataset-full.md) |
| One product in the Full mount adapter distribution | [adapter-full](adapters/adapter-full.md) |
| One canonical mount adapter record | [adapter-record](adapters/adapter-record.md) |
| A research result for a product candidate | [Lenses and related optical products](lenses/research-result.md) or [mount adapters](adapters/research-result.md) |
| IDs and display metadata embedded in distributions | [reference-data](shared/reference-data.md) |

## How to read field tables and constraints {#field-tables}

On each page, field tables use "Path" for the location in the JSON document, "Type/value" for permitted data types and fixed values, and "Meaning" for the role of the field.

- `[]` denotes an array.
    For example, `products[]` refers to each element in the `products` array.
- "A or `null`" means that a field may contain either a value of type A or `null`.
- `{}` denotes an empty object with no properties.
- Literal `true`, `false`, and `null` values, enumerated values, and JSON keys are shown as code.

The type tables use the following names for JSON types.

| Term | JSON or JSON Schema representation |
| --- | --- |
| String | `string` |
| Number | `number` |
| Integer | `integer` |
| Object | `object` |
| Boolean | `boolean` |
| Array | `array` |
| Enumerated value | A value permitted by a JSON Schema `enum`; not a separate JSON type |

When `[]` follows a type name, it denotes an array whose elements have that type.
All integers use the I-JSON safe integer range, with an upper bound of `9007199254740991`.
Fields that permit negative values have a lower bound of `-9007199254740991`.
If an individual table specifies a narrower range, that constraint takes precedence.

Each reference page explains the corresponding JSON Schema in prose and tables.
Consult the JSON Schema file for the exact types, required fields, permitted values, and conditional constraints.
When modifying repository source files, use `hatch run validate` to check rules that JSON Schema alone cannot express.
Repository validation covers each schema's Draft 2020-12 validity, `$id` and `$ref` values, file names and locations, ID and registry references, and relationships between files.

## Published URLs and versions {#published-schema-urls}

Each JSON Schema `$id` is a published URL that includes the schema version and namespace.
The current schema version is `1.0.0`, and the URLs use the following forms.

- Lenses and related optical products: `https://cercidiphyllum.jp/schemas/1.0.0/lenses/<schema-file>`
- Mount adapters: `https://cercidiphyllum.jp/schemas/1.0.0/adapters/<schema-file>`
- Shared definitions: `https://cercidiphyllum.jp/schemas/1.0.0/shared/<schema-file>`

The contents of a published versioned URL and its JSON Schema never change.
When the data structure or its constraints change, `schemaVersion` is updated and previous versions remain published.
See [Use the distribution data](../../use-data.md) for version checks performed by data consumers.

## Shared {#shared-schemas}

The shared JSON Schemas validate definitions used by both datasets and reference information embedded in distribution JSON.

| JSON Schema | What it validates |
| --- | --- |
| [shared-definitions](shared/shared-definitions.md) | IDs, numbers, measurement conditions, and other definitions referenced by multiple JSON Schemas |
| [reference-data](shared/reference-data.md) | ID-to-display-metadata maps embedded at the root of each distribution JSON |

## Lenses and related optical products {#lens-schemas}

For lenses and related optical products, separate JSON Schemas validate distribution data, canonical records, and research results.

| JSON Schema | What it validates |
| --- | --- |
| [dataset-full](lenses/dataset-full.md) | The complete Lens Full distribution |
| [dataset-light](lenses/dataset-light.md) | The complete Lens Light distribution |
| [product-full](lenses/product-full.md) | One product in the Lens Full `products[]` array |
| [product-light](lenses/product-light.md) | One product in the Lens Light `products[]` array |
| [product-record](lenses/product-record.md) | One canonical record under `data/records/lenses/` |
| [product-components](lenses/product-components.md) | Shared blocks for identity, lifecycle, mount, physical details, and other information used by multiple product types |
| [product-type-lens](lenses/product-type-lens.md) | The `lens` block for a lens |
| [product-type-teleconverter](lenses/product-type-teleconverter.md) | The `teleconverter` block for a teleconverter |
| [product-type-pinhole](lenses/product-type-pinhole.md) | The `pinhole` block for a pinhole product |
| [research-result](lenses/research-result.md) | One research result under `research/results/lenses/` |

## Mount adapters {#adapter-schemas}

Mount adapters use a data structure separate from lenses and related optical products, and there is no Light edition.

| JSON Schema | What it validates |
| --- | --- |
| [dataset-full](adapters/dataset-full.md) | The complete Full distribution for mount adapters |
| [adapter-full](adapters/adapter-full.md) | One product in the Full mount adapter distribution's `adapters[]` array |
| [adapter-record](adapters/adapter-record.md) | One canonical record under `data/records/adapters/` |
| [adapter-components](adapters/adapter-components.md) | Shared blocks for mount conversion, electronics, optics, physical details, and other information |
| [research-result](adapters/research-result.md) | One research result under `research/results/adapters/` |

## JSON Schema license {#schema-license}

The JSON Schema files under `schemas/` are licensed under the MIT License.
The `SPDX-FileCopyrightText` and `SPDX-License-Identifier: MIT` lines in each file's `$comment` also apply only to the JSON Schema file.
Research results, canonical records, registries, and distribution data validated by those JSON Schemas are licensed under [CC BY 4.0](../../license.md).

## Related pages

- [Data model](../../data-model.md): How research results, canonical records, and distribution data relate to one another
- [How to interpret values](../../value-rules.md): When to use omission, `null`, an empty array, or `false`
- [Field reference for lenses and related optical products](../../lens-field-reference.md): Field descriptions based on actual canonical records
- [Mount adapter field reference](../../adapter-field-reference.md): Field descriptions based on actual canonical records
- [Development and validation](../../development.md): Generation, repository validation, and documentation build procedures
