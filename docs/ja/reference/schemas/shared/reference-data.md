# reference-data.schema.json

このJSON Schemaは、配布用JSONのルートにある`referenceData`を検証します。
`referenceData`は、製品に記録されたメーカーID、ブランドID、マウントシステムIDを、人が読む表示名へ変換するための対応表です。

## 例

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

IDをオブジェクトのキーにするため、配列を検索せずに表示情報を取得できます。
たとえば、`product.identity.brandId`が`nikkor`なら、表示名は`referenceData.brands.nikkor.name`です。

## フィールド

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `manufacturers` | 参照マップ | メーカーIDをキー、メーカーの表示情報を値とするオブジェクト |
| `brands` | 参照マップ | ブランドIDをキー、ブランドの表示情報を値とするオブジェクト |
| `mountSystems` | 参照マップ | マウントシステムIDをキー、マウントシステムの表示情報を値とするオブジェクト |
| `manufacturers.<id>.name` | 文字列 | メーカーの表示名 |
| `brands.<id>.name` | 文字列 | ブランドの表示名 |
| `mountSystems.<id>.name` | 文字列 | マウントシステムの表示名 |

`manufacturers`、`brands`、`mountSystems`は必須です。
各キーは共通のID形式に従い、各値は`name`を必須とするオブジェクトです。
現行Schemaでは、各値に`name`以外のフィールドを追加できません。
将来表示用の属性が必要になった場合は、文字列をオブジェクトへ置き換える移行をせず、各値のオブジェクトを拡張できます。

## 生成と検証

`referenceData`は、二つの基準レジストリから自動生成します。

- `data/product-manufacturer-brand-registry.json`
- `data/mount-system-registry.json`

各配布用JSONには、そのデータセットで参照する項目だけを収録します。
レンズFull版とLight版の`referenceData`は同一です。
リポジトリ検証では、参照するすべてのIDが存在すること、未使用の項目がないこと、表示名が基準レジストリと一致することを確認します。

`contentHash`は`referenceData`も対象に含めます。
表示名が変わった場合も、内容の変更として検出できます。

## 関連ページ

- [データモデル](../../../data-model.md)：基準レジストリと配布用JSONの関係
- [JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/shared/reference-data.schema.json)
