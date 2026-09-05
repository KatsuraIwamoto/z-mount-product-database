# product-light.schema.json

レンズLight版の`products[]`に含まれる製品1件を検証します。
Full版と同じトップレベルのブロック名を使い、既存のWeb表示に必要なフィールドだけを保持します。

## Full版からの生成規則

| 確認項目 | Light版の規則 |
| --- | --- |
| 製品 | Full版の全製品を同じ順序で保持する |
| トップレベルのフィールド | `lenses`名前空間の`id`、`productType`と製品種別ブロック名を変えない |
| オブジェクト | 不要なプロパティを省略できる |
| 値 | 保持した値と型をFull版から変更しない |
| 配列 | 元の順序と要素数を保つ。最短撮影距離と最大撮影倍率だけは、後述の規則でFull版の要素を値を変えずに選ぶ |

Light版だけの値は追加せず、範囲や代表値も新たに計算しません。
JSON Schemaは、Light版で許可する構造を検証します。
Full版との対応は、`hatch run validate`でも検証します。

!!! warning "Light版は生成ファイルです"

    `dist/z-mount-lenses.light.json`は直接編集しません。
    保持フィールドを変更する場合は、既存のWeb表示との互換性も確認します。

## Full版とLight版の実例

NIKKOR Z 24-70mm f/2.8 S IIの`lens.aperture`を例に、同じ値を保ったまま構造を小さくする方法を示します。
各コードは、対応する製品から`lens.aperture`だけを取り出した実データです。

=== "Full版"

    参照元：`dist/z-mount-lenses.full.json`

    参照箇所：製品ID `nikkor-z-24-to-70mm-f2p8-s-ii`の`lens.aperture`

    ```json
    {
      "fNumber": {
        "maximumAperture": [
          {
            "value": 2.8,
            "conditions": {}
          }
        ],
        "minimumAperture": [
          {
            "value": 22,
            "conditions": {}
          }
        ],
        "effective": null
      },
      "diaphragm": {
        "present": true,
        "bladeCount": 11,
        "bladeShape": "rounded"
      },
      "controlMechanism": "electronic"
    }
    ```

=== "Light版"

    参照元：`dist/z-mount-lenses.light.json`

    参照箇所：製品ID `nikkor-z-24-to-70mm-f2p8-s-ii`の`lens.aperture`

    ```json
    {
      "fNumber": {
        "maximumAperture": [
          {
            "value": 2.8,
            "conditions": {}
          }
        ]
      }
    }
    ```

Light版は開放F値の`2.8`と測定条件をそのまま保持し、最小絞り、絞り機構、制御方式を省略します。

## トップレベルのフィールド

`id`から`physical`までの共通7フィールドは、すべて必須です。
加えて、`productType`に対応する`lens`、`teleconverter`、`pinhole`のいずれか一つだけを持ち、ほかの二つは含めません。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `id` | ID文字列 | `lenses`名前空間でFull版と共有するスラッグ形式のID。文字列から製品情報を解析しない |
| `productType` | `lens` / `teleconverter` / `pinhole` | Full版と同じ製品種別 |
| `identity` | オブジェクト | メーカーID、ブランドID、製品名 |
| `lifecycle` | [lifecycle](product-components.md#lifecycle) | Full版と同じ発売発表日と公式の状態表記 |
| `officialProductPages` | オブジェクト[] | 各公式製品ページのURLだけを保持した配列 |
| `mount` | [mount](product-components.md#mount) | 公式アダプターの情報を含む、Full版と同じマウント構造 |
| `physical` | オブジェクト | 寸法、重量、フィルター取付方式 |
| `lens` | オブジェクト | `productType: "lens"`のときに持つLight版のレンズ仕様 |
| `teleconverter` | オブジェクト | `productType: "teleconverter"`のときに持つLight版のテレコンバーター仕様 |
| `pinhole` | オブジェクト | `productType: "pinhole"`のときに持つLight版のピンホール仕様 |

## 共通の保持フィールド

`identity`直下の3フィールドと、`officialProductPages[]`各要素の`url`は必須です。
`physical`直下の3フィールドも必須で、`dimensionMeasurements`と`weightMeasurements`を配列で記録する場合は1件以上必要です。
フィルター取付方式は`type`に対応する寸法フィールドだけを持ち、`rear-gelatin`の`sheetDimensionsMm`をオブジェクトで記録する場合は`width`と`height`がどちらも必須です。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `identity.manufacturerId` | ID文字列 | Full版と同じメーカーID |
| `identity.brandId` | ID文字列 | Full版と同じブランドID |
| `identity.productName` | 文字列 | Full版と同じ公式製品名 |
| `officialProductPages[].url` | HTTP(S) URL | Full版の各公式製品ページURL。配列順と要素数を保つ |
| `physical.dimensionMeasurements` | measurement[]または`null` | Full版の寸法と測定条件 |
| `physical.weightMeasurements` | measurement[]または`null` | Full版の重量と測定条件 |
| `physical.filterInterfaces` | interface[]または`null` | フィルター取付方式と寸法。Full版の`host`は省略する |
| `physical.filterInterfaces[].type` | `front-thread` / `rear-thread` / `drop-in` / `rear-gelatin` | フィルター取付方式 |
| `physical.filterInterfaces[].diameterMm` | 正数 | 前面または後部のねじ径mm |
| `physical.filterInterfaces[].filterDiameterMm` | 正数 | ドロップインフィルター径mm |
| `physical.filterInterfaces[].sheetDimensionsMm` | オブジェクトまたは`null` | 後部ゼラチンフィルターの寸法 |
| `physical.filterInterfaces[].sheetDimensionsMm.width` | 正数 | 後部ゼラチンフィルターの幅mm |
| `physical.filterInterfaces[].sheetDimensionsMm.height` | 正数 | 後部ゼラチンフィルターの高さmm |

## レンズ

`lens`では、光学系の概要とWeb表示に使う存在情報を保持します。
`lens`直下では、`focalLength`、`aperture`、`coverage`、`focus`、`stabilization`、`specialized`が必須です。
`aperture`では`fNumber`が必須で、`fNumber`がオブジェクトの場合と`tNumber`を記録する場合は`maximumAperture`が必要です。
`maximumAperture`、`minimumFocusDistances`、`reproductionMagnifications`を配列で記録する場合は、それぞれ1件以上必要です。
`focus`では`autofocus`、`manualFocus`、`minimumFocusDistances`、`reproductionMagnifications`が必須で、AF、MF、手ぶれ補正をオブジェクトで記録する場合は`present`が必須です。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `lens.focalLength` | [focalLength](../shared/shared-definitions.md#focal-length-and-conditions)または`null` | Full版の単焦点、ズーム範囲、交換構成 |
| `lens.aperture.fNumber` | オブジェクトまたは`null` | F値で公表された開放値 |
| `lens.aperture.fNumber.maximumAperture` | F値測定[]または`null` | Full版の公称開放F値 |
| `lens.aperture.tNumber` | オブジェクト | T値が適用できる製品の公称開放T値 |
| `lens.aperture.tNumber.maximumAperture` | T値測定[]または`null` | Full版の公称開放T値 |
| `lens.coverage` | [coverage](../shared/shared-definitions.md#basic-values) | Full版と同じ最大撮像フォーマット |
| `lens.focus.autofocus` | オブジェクトまたは`null` | AFの確認状態 |
| `lens.focus.autofocus.present` | 真偽値 | Full版で確認したAFの有無 |
| `lens.focus.manualFocus` | オブジェクトまたは`null` | MFの確認状態 |
| `lens.focus.manualFocus.present` | 真偽値 | Full版で確認したMFの有無 |
| `lens.focus.minimumFocusDistances` | 撮影距離[]または`null` | Full版で`distanceM`が最小の要素。値を変えず、同値は元の順序ですべて保持する |
| `lens.focus.reproductionMagnifications` | 撮影倍率[]または`null` | Full版で撮影倍率が最大の要素。値を変えず、同値は元の順序ですべて保持する |
| `lens.stabilization` | オブジェクトまたは`null` | レンズ内手ぶれ補正の確認状態 |
| `lens.stabilization.present` | 真偽値 | Full版で確認したレンズ内手ぶれ補正の有無 |
| `lens.specialized.<category>` | `{}` | Full版に存在する`cinema`、`anamorphic`、`fisheye`、`macro`、`reflex`、`movements`、`probe`、`builtInTeleconverter`の存在マーカー |

## テレコンバーター

`teleconverter`の5フィールドはすべて必須です。
`compatibleLensIds`を配列で記録する場合は、重複のないIDが1件以上必要です。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `teleconverter.coverage` | [coverage](../shared/shared-definitions.md#basic-values) | Full版と同じ最大撮像フォーマット |
| `teleconverter.magnification` | 正数 | Full版と同じ公称倍率 |
| `teleconverter.apertureLossStops` | 0以上の数値 | Full版と同じ露出低下段数 |
| `teleconverter.supportsAutofocus` | 真偽値または`null` | Full版と同じ対応レンズ装着時のAF対応 |
| `teleconverter.compatibleLensIds` | ID[]または`null` | Full版と同じ対応レンズID |

## ピンホール

`pinhole`の3フィールドはすべて必須です。
`imagingModes`を配列で記録する場合は1件以上必要です。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `pinhole.coverage` | [coverage](../shared/shared-definitions.md#basic-values) | Full版と同じ最大撮像フォーマット |
| `pinhole.focalLength` | オブジェクトまたは`null` | Full版と同じ固定焦点距離または可変範囲 |
| `pinhole.imagingModes` | mode[]または`null` | Full版と同じ撮像方式、F値、開口情報 |

Light版のピンホール仕様には、Full版の`pinhole.anglesOfView`を保持しません。

## 関連ページ

- [product-full](product-full.md)：対応するFull版の製品構造
- [dataset-light](dataset-light.md)：Light版の配布メタデータ
- [レンズと関連光学製品のフィールドリファレンス](../../../lens-field-reference.md)：Full版とLight版の実データ比較

[JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/product-light.schema.json)
