# product-full.schema.json

レンズFull版の`products[]`に含まれる製品1件を検証します。
識別情報や外形などの共通フィールドに、製品種別に対応する仕様ブロックを一つだけ組み合わせます。

## トップレベルのフィールド {#top-level-fields}

`id`、`productType`、`identity`、`lifecycle`、`officialProductPages`、`mount`、`physical`、`controls`、`accessories`は、すべての製品で必須です。
`$schema`、`electronicServices`、製品種別ごとの仕様ブロックには、次節で説明する追加条件があります。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `$schema` | 文字列 | JSON Schemaへの参照。収録製品データでは[product-record](product-record.md)が必須化し、配布データの生成時に除去する |
| `id` | ID文字列 | `lenses`名前空間内で一意のID。小文字英数字をハイフンで区切った、人が読めるスラッグ形式を使う。文字列から製品情報を解析しない。ファイル名、調査結果データ、製品間参照に使う |
| `productType` | `lens` / `teleconverter` / `pinhole` | 使用する製品種別ブロックを選ぶ値 |
| `identity` | [identity](product-components.md#identity) | メーカーID、ブランドID、製品名、型番、別名、バリエーション |
| `lifecycle` | [lifecycle](product-components.md#lifecycle) | 発売発表日とメーカーまたはブランドによる状態表記 |
| `officialProductPages` | [officialProductPage](product-components.md#officialproductpage)[] | 製品そのものの公式メインページ。該当ページが残っていない場合は`[]` |
| `mount` | [mount](product-components.md#mount) | Zマウントとの接続方法と電子接点 |
| `physical` | [physical](product-components.md#physical) | 寸法、重量、保護表記、フィルター、三脚取付部 |
| `controls` | [control](product-components.md#control)[]または`null` | リング、スイッチ、ボタンなどの操作部 |
| `accessories` | [accessories](product-components.md#accessories)または`null` | 付属または別売のアクセサリー |
| `electronicServices` | [electronicServices](../shared/shared-definitions.md#electronic-data)または`null` | ファームウェア更新、設定、制御に使う接続方式 |
| `lens` | [lens](product-type-lens.md) | レンズの仕様ブロック |
| `teleconverter` | [teleconverter](product-type-teleconverter.md) | テレコンバーターの仕様ブロック |
| `pinhole` | [pinhole](product-type-pinhole.md) | ピンホールと関連する撮像方式の仕様ブロック |

## 製品種別と仕様ブロック

`productType`に対応するブロックだけが必須かつ許可されます。

| `productType` | 必須ブロック | 含められないブロック |
| --- | --- | --- |
| `lens` | `lens` | `teleconverter`、`pinhole` |
| `teleconverter` | `teleconverter` | `lens`、`pinhole` |
| `pinhole` | `pinhole` | `lens`、`teleconverter` |

## 電子接点と製品側の接続サービス {#electronic-services-condition}

`electronicServices`は、マウント接点を介する機能ではなく、製品のファームウェア更新、設定、制御に使う接続を記録します。

| `mount.electronicContacts` | `electronicServices` |
| --- | --- |
| `{ "present": true, ... }` | 必須。採用できる公開情報で確認できない場合は`null`も使用できる |
| `{ "present": false }` | 省略できる。独立したUSB接続やドックなどが公表されている場合は記録できる |
| `null` | 省略できる。接続サービスを確認できる場合は記録できる |

電子接点がないことだけを理由に、独立した接続サービスまで否定しません。
ただし、`electronicServices.connections[].method`が`camera-body`の場合は、カメラとの通信にマウント接点を使うため、`mount.electronicContacts.present`が`true`でなければなりません。
`direct-usb`と`dock`には、この条件を適用しません。

## レンズの外形変化

`productType: "lens"`では、適用できる外形変化フィールドを省略せず、採用できる公開情報で確認できない値を`null`にします。

| 条件 | `physical`の規則 |
| --- | --- |
| すべてのレンズ | `externalLengthDuringFocus`と`isRetractableForStorage`が必須 |
| `lens.focalLength.kind: "zoom"` | `externalLengthDuringZoom`が必須 |
| `lens.focalLength.kind: "prime"` | `externalLengthDuringZoom`を含められない |
| `lens.focus.opticalFocusingSystems[].type: "internal-focusing"`または`"rear-focusing"` | `externalLengthDuringFocus`は`"constant"` |
| `lens.zoom.opticalZoomingSystems[].type: "internal-zooming"` | `externalLengthDuringZoom`は必須かつ`"constant"` |

`constant`は操作しても全長が変わらないこと、`variable`は全長が変わることを表します。
`null`は、その挙動を採用できる公開情報で確認できない状態です。

値の省略、`null`、空配列、`false`の意味は、[値の読み方](../../../value-rules.md)を参照してください。

## 関連ページ

- [product-record](product-record.md)：収録製品データに追加する`$schema`と配置規則
- [product-components](product-components.md)：製品種別に共通するブロック
- [レンズと関連光学製品のフィールドリファレンス](../../../lens-field-reference.md)：実データを使った各フィールドの説明

[JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/product-full.schema.json)
