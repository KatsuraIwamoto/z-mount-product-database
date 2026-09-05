# product-type-pinhole.schema.json

`productType: "pinhole"`の製品が持つ`pinhole`ブロックを検証します。
ピンホール、ピンホールシーブ、ゾーンプレートなど、レンズと同じフォーカス機構を前提としない撮像方式を一つの製品内に記録できます。

## pinholeブロックの実例

Lensbaby Obscura 16を例に、三つの撮像方式を持つ製品の記録方法を示します。

参照元：`data/records/lenses/lensbaby/lensbaby-obscura-16.json`

参照箇所：`pinhole`

```json
{
  "coverage": {
    "format": "full-frame"
  },
  "focalLength": {
    "kind": "fixed",
    "millimeters": 16
  },
  "imagingModes": [
    {
      "type": "zone-plate",
      "fNumber": 22,
      "opening": null
    },
    {
      "type": "pinhole-sieve",
      "fNumber": 45,
      "opening": null
    },
    {
      "type": "pinhole",
      "fNumber": 90,
      "opening": null
    }
  ],
  "anglesOfView": null
}
```

## トップレベルのフィールド

次の4フィールドはすべて必須です。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `pinhole.coverage` | [coverage](../shared/shared-definitions.md#basic-values) | 製品がカバーする最大撮像フォーマット |
| `pinhole.focalLength` | オブジェクトまたは`null` | ピンホール面から撮像面までの公称焦点距離 |
| `pinhole.imagingModes` | mode[]または`null` | 製品が提供する撮像方式。判明している場合は1件以上 |
| `pinhole.anglesOfView` | [angleOfView](../shared/shared-definitions.md#optical-values)[]または`null` | 公式に公表された画角。判明している場合は1件以上 |

寸法、重量、マウント、フィルター取付方式は、[製品共通ブロック](product-components.md)に記録します。

## 焦点距離

`pinhole.focalLength`は、採用できる公開情報で確認できない場合に`null`を使用します。
オブジェクトの場合は、`kind`に応じて必要なフィールドが変わります。

| `kind` | 必須フィールド | 説明 |
| --- | --- | --- |
| `fixed` | `millimeters` | 固定焦点距離mm |
| `variable` | `rangeMm.minimum`、`rangeMm.maximum` | 可変範囲の最小値と最大値mm |

二つの焦点距離構造は排他的で、`kind`に対応しないフィールドは含められません。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `pinhole.focalLength.kind` | `fixed` / `variable` | 焦点距離の構造を選ぶ値 |
| `pinhole.focalLength.millimeters` | 正数 | `fixed`の場合の焦点距離mm |
| `pinhole.focalLength.rangeMm.minimum` | 正数 | `variable`の場合の最小焦点距離mm |
| `pinhole.focalLength.rangeMm.maximum` | 正数 | `variable`の場合の最大焦点距離mm |

## 撮像方式と開口

`imagingModes[]`の各要素は、`type`、`fNumber`、`opening`をすべて持ちます。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `pinhole.imagingModes[].type` | `pinhole` / `pinhole-sieve` / `zone-plate` | 撮像方式 |
| `pinhole.imagingModes[].fNumber` | 正数または`null` | その撮像方式の公称F値 |
| `pinhole.imagingModes[].opening` | オブジェクトまたは`null` | 開口径の仕様 |

開口径が公表されていない場合は、`opening: null`を記録します。
オブジェクトの場合は、`kind`に応じて必要なフィールドが変わります。

| `opening.kind` | 必須フィールド | 説明 |
| --- | --- | --- |
| `fixed` | `diameterMm` | 固定された開口径mm |
| `discrete` | `diametersMm` | 選択できる重複のない開口径mm。1件以上 |
| `continuous-range` | `minimumDiameterMm`、`maximumDiameterMm` | 連続可変範囲の最小値と最大値mm |

三つの開口構造は排他的で、`opening.kind`に対応しないフィールドは含められません。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `pinhole.imagingModes[].opening.kind` | `fixed` / `discrete` / `continuous-range` | 開口径の構造を選ぶ値 |
| `pinhole.imagingModes[].opening.diameterMm` | 正数 | 固定開口径mm |
| `pinhole.imagingModes[].opening.diametersMm` | 正数[] | 選択式の開口径mm |
| `pinhole.imagingModes[].opening.minimumDiameterMm` | 正数 | 連続可変範囲の最小開口径mm |
| `pinhole.imagingModes[].opening.maximumDiameterMm` | 正数 | 連続可変範囲の最大開口径mm |

## 関連ページ

- [product-full](product-full.md)：共通フィールドとの組み合わせ
- [product-components](product-components.md)：寸法、重量、マウント、フィルター取付方式
- [レンズと関連光学製品のフィールドリファレンス](../../../lens-field-reference.md)：Lensbaby Obscura 16を使った説明

[JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/product-type-pinhole.schema.json)
