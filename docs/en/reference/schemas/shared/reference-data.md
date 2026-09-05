# reference-data.schema.json

This JSON Schema validates the root `referenceData` object in a distribution JSON.
`referenceData` maps manufacturer, brand, and mount-system IDs used by product records to human-readable display names.

## Example

```json
{
  "manufacturers": {
    "nikon": {
      "name": "Nikon"
    }
  },
  "brands": {
    "nikkor": {
      "name": "NIKKOR"
    }
  },
  "mountSystems": {
    "nikon-z": {
      "name": "Nikon Z"
    }
  }
}
```

IDs are object keys, so consumers can retrieve display metadata without searching an array.
For example, when `product.identity.brandId` is `nikkor`, its display name is `referenceData.brands.nikkor.name`.

## Fields

| Path | Type/value | Meaning |
| --- | --- | --- |
| `manufacturers` | reference map | Object keyed by manufacturer ID with manufacturer display metadata as values |
| `brands` | reference map | Object keyed by brand ID with brand display metadata as values |
| `mountSystems` | reference map | Object keyed by mount-system ID with mount-system display metadata as values |
| `manufacturers.<id>.name` | string | Manufacturer display name |
| `brands.<id>.name` | string | Brand display name |
| `mountSystems.<id>.name` | string | Mount-system display name |

`manufacturers`, `brands`, and `mountSystems` are required.
Every key follows the shared ID format, and every value is an object requiring `name`.
The current schema allows no other fields in an entry.
If more display metadata becomes necessary later, the entry objects can be extended without migrating string values to objects.

## Generation and validation

`referenceData` is generated from two source registries.

- `data/product-manufacturer-brand-registry.json`
- `data/mount-system-registry.json`

Each distribution contains only entries referenced by that dataset.
Lens Full and Lens Light have identical `referenceData`.
Repository validation checks that every referenced ID resolves, no unused entry is included, and every display name matches the source registry.

`contentHash` includes `referenceData`, so a display-name update changes the content hash.

## Related pages

- [Data model](../../../data-model.md): Relationship between source registries and distribution JSON
- [JSON Schema file](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/shared/reference-data.schema.json)
