# Licensing

Data is available under CC BY 4.0, while source code and documentation are available under the MIT License.
The applicable license depends on the material you use.
This page is a summary of the main points and is not exhaustive.
For the exact scope, see [`LICENSING.md`](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/LICENSING.md).
For the formal terms, see the [CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en) and the [MIT License text](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/LICENSES/MIT.txt).

## License by material

| Material | License |
| --- | --- |
| Canonical product data and registries | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Research-result data | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Three distribution JSON files and `PRODUCTS.md` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Source code, JSON Schema, tests, tools, configuration, and documentation | [MIT License](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/LICENSES/MIT.txt) |

## Using the data

Data covered by CC BY 4.0 may be copied, shared, and adapted, including for commercial purposes.
The main attribution items when sharing the data are:

- The project name and creator name
- A CC BY 4.0 notice and a link to the license
- The URL of the data used, when reasonably practicable
- An indication of changes, if any

See the [CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en) for all applicable terms.

### Attribution examples

When sharing the data, attribution is required, but its presentation may be adapted to the medium.
The following examples can be copied as written.

=== "Share unchanged data"

    ```text
    Z Mount Product Database, Katsura Iwamoto, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), https://github.com/KatsuraIwamoto/z-mount-product-database
    ```

=== "Share modified data"

    ```text
    Z Mount Product Database, Katsura Iwamoto, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), https://github.com/KatsuraIwamoto/z-mount-product-database
    Changes: [describe the changes]
    ```

## Using the code and documentation

Material covered by the MIT License may be copied, modified, redistributed, and used commercially.
When copying or redistributing all or substantial portions, retain the copyright notice and the MIT License text.

## No warranty

The CC BY 4.0 and MIT License texts include disclaimers of warranties and limitations of liability.
This project's verification process does not guarantee the accuracy or completeness of the data.
For uses involving important decisions, also check the recorded sources or official information from the manufacturer.

## Third-party rights

!!! important "Trademarks, patents, and official pages are outside the license grant"
    CC BY 4.0 applies only to copyright and similar rights that this project can license.
    The project does not claim new rights in factual product specifications.
    This license does not grant rights in third-party trademarks, patents, official pages, or other third-party material.

## Relationship with manufacturers

Manufacturer, brand, and product names are used to identify products and information sources.
Z Mount Product Database is not affiliated with, authorized by, sponsored by, or endorsed by Nikon Corporation or any other manufacturer or rights holder.

## File-level licensing

File-level licenses are defined in the repository's [`REUSE.toml`](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/REUSE.toml).
See [`LICENSING.md`](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/LICENSING.md) for the license texts and exact scope.
Each distribution also identifies its data license through the root `license` and `licenseUrl` fields.
If you obtain only a distribution JSON file, open the public repository through its root `repositoryUrl`, then use `LICENSING.md` to check the scope and third-party-rights notice.

!!! note "JSON Schema and data licenses"
    The `SPDX-FileCopyrightText` and `SPDX-License-Identifier: MIT` lines in a JSON Schema file's `$comment` apply to that JSON Schema file.
    Canonical product data and distributions validated by the JSON Schema remain under CC BY 4.0.
