# shared-definitions.schema.json

このJSON Schemaは、複数のJSON Schemaから参照する定義を`$defs`にまとめています。
IDや数値のほか、焦点距離、測定条件、レンズ構成、電子情報、三脚支持、可動量なども定義します。

単独のJSONファイルを検証するJSON Schemaではありません。
必要な定義は、各JSON Schemaから`$ref`で参照します。

<div class="grid cards" markdown>

-   :material-file-tree:{ .lg .middle } **基本値**

    ---

    ID、文字列、数値、地域、言語、撮像フォーマット、測定時の付属部品を確認できます。

    [基本値を見る](#basic-values)

-   :material-swap-horizontal:{ .lg .middle } **焦点距離と条件**

    ---

    焦点距離の種類と、測定値が成立する条件を確認できます。

    [焦点距離と条件を見る](#focal-length-and-conditions)

-   :material-camera-iris:{ .lg .middle } **光学値**

    ---

    F値、T値、画角、レンズ構成、特殊レンズ、コーティングを確認できます。

    [光学値を見る](#optical-values)

-   :material-magnify:{ .lg .middle } **撮影距離と取付先**

    ---

    最短撮影距離、撮影倍率、ワーキングディスタンス、取付先を確認できます。

    [撮影距離と倍率を見る](#focus-measurements)

    [取付先を見る](#host)

-   :material-shield-outline:{ .lg .middle } **環境保護表現**

    ---

    防塵、防滴、耐候などの公式表現と、その適用範囲を確認できます。

    [環境保護表現を見る](#environmentalclaim)

-   :material-connection:{ .lg .middle } **電子情報と三脚支持**

    ---

    メタデータ伝達、電子サービス、三脚支持部品と取付インターフェースを確認できます。

    [電子情報を見る](#electronic-data)

    [三脚支持を見る](#tripod-support)

-   :material-axis-arrow:{ .lg .middle } **可動量**

    ---

    ティルト角、シフト量、可動部の回転範囲を確認できます。

    [可動量を見る](#movements)

</div>

## 共通定義の使用例

NIKKOR Z 24-70mm f/2.8 S IIを例に、共通定義が実際の値をどのように表すかを示します。

参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

=== "焦点距離"

    参照箇所：`lens.focalLength`

    ```json
    {
      "kind": "zoom",
      "rangeMm": {
        "minimum": 24,
        "maximum": 70
      }
    }
    ```

=== "画角と条件"

    参照箇所：`lens.anglesOfView[0]`

    ```json
    {
      "format": "full-frame",
      "orientation": "diagonal",
      "degrees": 84,
      "conditions": {
        "focalLength": {
          "kind": "point",
          "millimeters": 24
        }
      }
    }
    ```

=== "開放F値（追加条件なし）"

    参照箇所：`lens.aperture.fNumber.maximumAperture[0]`

    ```json
    {
      "value": 2.8,
      "conditions": {}
    }
    ```

`focalLength`は製品の公称焦点距離を表します。
測定値の`conditions.focalLength`は、その値が焦点距離上のどこで成立するかを表します。
`conditions`が空のオブジェクトの場合、焦点距離や撮影距離などの追加条件はありません。

## 基本値 {#basic-values}

| 定義 | 型・値 | 説明 |
| --- | --- | --- |
| `id` | `^[a-z0-9]+(?:-[a-z0-9]+)*$` | 小文字英数字をハイフンで区切るID |
| `nonEmptyString` | 1文字以上の文字列 | 空文字を許可しない文字列 |
| `positiveNumber` | 0より大きい数値 | 長さや倍率など、0にならない値 |
| `nonNegativeNumber` | 0以上の数値 | 段数や倍率範囲など、0を許す値 |
| `measurementComponent` | 列挙値 | `tripod-collar-assembly`、`tripod-foot`、`tripod-mount-cover`、`lens-hood`、`front-cap`、`rear-cap`、`drop-in-filter`、`other`のいずれか。寸法や重量を測定した際の付属部品 |
| `region` | 2文字の大文字コード | ISO 3166-1 alpha-2形式の地域コード |
| `language` | 言語タグ | `ja`、`en`、`en-US`などの言語表記 |
| `imageFormat` | `full-frame` / `aps-c` / `super-35` / `other` | 撮像フォーマットの分類 |
| `coverage` | `{ "format": imageFormat }`または`null` | 製品がカバーする最大撮像フォーマット。採用できる公開情報で確認できない場合は`null` |
| `modelNumberOptions` | 文字列[]または`null` | 公式資料で型番として確認できた識別子の一覧。重複は不可。採用できる公開情報で型番を確認できない場合は`null` |

JAN、EAN、UPC、バーコード、SKU、商品番号、カタログ番号、記事番号などは、メーカーまたはブランドが型番として明示していない限り、`modelNumberOptions`に記録しません。

## 焦点距離と条件 {#focal-length-and-conditions}

### `focalLengthCondition`

測定値が適用される焦点距離上の一点または範囲を表します。
レンズ自体の焦点距離仕様ではありません。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `focalLengthCondition.kind` | `point` / `range` | 一点指定か範囲指定か |
| `focalLengthCondition.millimeters` | 正数 | `point`で指定する焦点距離（mm） |
| `focalLengthCondition.minimumMm` | 正数 | `range`の下限（mm） |
| `focalLengthCondition.maximumMm` | 正数 | `range`の上限（mm） |

`point`では`kind`と`millimeters`、`range`では`kind`、`minimumMm`、`maximumMm`が必須です。
二つの構造は排他的で、選ばなかった構造のフィールドは含められません。

### `focalLength`

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `focalLength.kind` | `prime` / `zoom` / `interchangeable` | 単焦点、ズーム、交換構成のいずれか |
| `focalLength.millimeters` | 正数または`null` | 単焦点の公称焦点距離（mm）。値が未公表の場合は`null` |
| `focalLength.rangeMm.minimum` | 正数 | ズームの広角端（mm） |
| `focalLength.rangeMm.maximum` | 正数 | ズームの望遠端（mm） |
| `focalLength.configurations` | オブジェクト[] | 交換部品によって焦点距離が変わる製品の構成。2件以上 |
| `focalLength.configurations[].magnification` | 正数 | その構成の公称撮影倍率 |
| `focalLength.configurations[].millimeters` | 正数 | その構成の公称焦点距離（mm） |

`kind`に応じて、次のフィールドを記録します。

| `kind` | 記録するフィールド |
| --- | --- |
| `prime` | `millimeters` |
| `zoom` | `rangeMm` |
| `interchangeable` | `configurations` |

`prime`では`kind`と`millimeters`、`zoom`では`kind`と`rangeMm`、`interchangeable`では`kind`と`configurations`が必須です。
三つの構造は排他的で、選ばなかった構造のフィールドは含められません。
`configurations`には、`magnification`と`millimeters`を持つ重複のない要素が2件以上必要です。

### 条件オブジェクト

測定値に付けられる条件は、値の種類によって異なります。
各キーは任意で、空のオブジェクト`{}`は追加条件がないことを示します。

| 定義 | 記録できる条件 | 使用する値 |
| --- | --- | --- |
| `apertureConditions` | 焦点距離、撮影距離、撮影倍率、カメラ、バリエーション | F値、T値 |
| `angleConditions` | 焦点距離、カメラ、バリエーション | 画角 |
| `focusConditions` | 焦点距離、撮影倍率、カメラ、バリエーション | 最短撮影距離、撮影倍率 |
| `specializedConditions` | 焦点距離、撮影距離、撮影倍率、カメラ、バリエーション | ワーキングディスタンスなどの特殊仕様 |

条件オブジェクトには、次のキーを組み合わせて記録します。

| キー | 説明 | 使用できる条件定義 |
| --- | --- | --- |
| `focalLength` | 値が成立する焦点距離または焦点距離の範囲 | すべて |
| `focusDistanceM` | 値が成立する撮影距離（m） | `apertureConditions`、`specializedConditions` |
| `reproductionMagnification` | 値が成立する撮影倍率 | `apertureConditions`、`focusConditions`、`specializedConditions` |
| `cameraBodyModel` | 値が成立するカメラの機種名 | すべて |
| `variantId` | 値が成立する製品バリエーションのID | すべて |

## 光学値 {#optical-values}

### F値とT値 {#aperture-measurements}

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `fNumberMeasurement.value` | 正数 | F値。`2.8`はf/2.8を表す |
| `fNumberMeasurement.conditions` | `apertureConditions` | そのF値が成立する条件 |
| `tNumberMeasurement.value` | 正数 | T値。`2.9`はT2.9を表す |
| `tNumberMeasurement.conditions` | `apertureConditions` | そのT値が成立する条件 |

### `angleOfView`

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `angleOfView.format` | `full-frame` / `aps-c` / `super-35` / `other` | 画角を測定した撮像フォーマット |
| `angleOfView.orientation` | `diagonal` / `horizontal` / `vertical` / `null` | 対角、水平、垂直の別。公式表記で特定できない場合は`null` |
| `angleOfView.degrees` | 0超360以下の数値 | 画角（度） |
| `angleOfView.conditions` | `angleConditions` | 焦点距離、カメラ、バリエーションの条件 |

### `opticalConstruction`

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `opticalConstruction.groups` | 1以上の整数または`null` | 光学系の群数 |
| `opticalConstruction.elements` | 1以上の整数または`null` | 光学素子の枚数 |

群数と枚数の少なくとも一方には数値が必要です。
片方だけが公式に公表されている場合は、もう片方に`null`を記録できます。
両方が数値の場合は、`hatch run validate`が群数が枚数以下であることを確認します。

### `specialElement`

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `specialElement.types` | 列挙値[] | `low-dispersion`、`anomalous-partial-dispersion`、`aspherical`、`fluorite`、`high-refractive-index`、`diffractive-optical`、`other`の性質 |
| `specialElement.officialName` | 文字列（省略可） | ED、ED glass、FLD glass、PF lens、XGMなど、メーカーが安定して使う固有名称または技術名称 |
| `specialElement.quantity` | 1以上の整数または`null` | 使用枚数。採用できる公開情報で確認できない場合は`null` |

### `coating`

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `coating.types` | 列挙値[] | `anti-reflective`、`surface-protective`、`spectral-control`、`other`の目的 |
| `coating.officialName` | 文字列（省略可） | メーカーが安定して使う固有名称または技術名称。一般的な説明だけの場合は省略 |
| `coating.appliedTo` | 列挙値[]または`null` | `front-element`、`rear-element`、`all-elements`の適用先。特定できない場合は`null` |

`types`はブランド横断の分類を表し、`officialName`はメーカーの公式表記を保持します。両者が同じ一般的な性質を表していても、安定して使われる技術名称は`officialName`に記録します。`officialName`はブランドと項目の組み合わせごとに解釈し、同じ表記でも別ブランドの技術が同一であるとはみなしません。本文中の文頭・文中による大文字小文字の違い、空白、ハイフン、単複、一般的な接尾語だけの違いは別名として扱いません。公式の用語集、技術ページ、仕様表、見出し、バッジ、製品上の表示を優先します。公式英語ページに対応する名称がある場合は英語表記を使い、ない場合は公開されている表記を保持して独自に翻訳しません。`®`や`™`は名称に含めませんが、`T*`の`*`のように名称自体を構成する記号は残します。

## 環境保護表現 {#environmentalclaim}

`environmentalClaim`は、防塵、防滴、耐候などについてメーカーまたはブランドが明示した表現を、その対象範囲とともに記録します。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `environmentalClaim.types` | 列挙値[] | `dust-resistant`、`drip-resistant`、`splash-resistant`、`moisture-resistant`、`weather-resistant`、`waterproof`、`other`のうち1件以上 |
| `environmentalClaim.scope.kind` | `product` / `component` | 表現が製品全体に適用されるか、特定部品だけに適用されるか |
| `environmentalClaim.scope.component` | 文字列 | `scope.kind: "component"`の場合の対象部品。たとえばカメラ側のシール部 |
| `environmentalClaim.conditions` | [specializedConditions](#focal-length-and-conditions) | 表現が成立するバリエーションなどの条件。追加条件がなければ`{}` |

`scope.kind`が`product`の場合は`kind`だけを記録します。
`component`の場合は`component`も必須です。
この定義は公式表現を構造化するものであり、規格試験への適合や完全な防水性を推定するものではありません。

## 電子情報 {#electronic-data}

### `metadataTransmission`

`metadataTransmission`は、撮影メタデータを伝達するかどうかと、公表された伝達規格を記録します。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `metadataTransmission.present` | 真偽値 | メタデータ伝達の有無 |
| `metadataTransmission.standards` | `exif` / `cooke-i` / `other`の配列、または`null` | 伝達を確認できた場合の公表規格。規格を特定できない場合は`null` |

伝達しないことを確認した場合は`{ "present": false }`を記録します。
伝達を確認した場合は`present: true`と`standards`が必要です。
伝達の有無自体を確認できない場合は`null`を使います。

### `electronicServices`

`electronicServices`は、製品向けファームウェア更新の公開有無と、更新、設定、制御に使う接続方式を記録します。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `electronicServices.hasPublishedFirmwareUpdate` | 真偽値または`null` | 製品向けファームウェア更新が公開されているか |
| `electronicServices.connections` | connection[]または`null` | 公表された接続方式。確認済みで該当なしの場合は`[]` |
| `electronicServices.connections[].method` | `camera-body` / `direct-usb` / `dock` / `other` | 接続方法 |
| `electronicServices.connections[].connectorType` | `usb-c` / `micro-usb` / `other`（省略可） | 公表された端子種別 |
| `electronicServices.connections[].purposes` | `firmware-update` / `configuration` / `tethered-control`の配列 | その接続の用途 |
| `electronicServices.connections[].application` | 文字列（省略可） | 公表されたアプリケーション名 |

電子サービス全体を確認できない場合は`electronicServices: null`を使います。

## 三脚支持 {#tripod-support}

`tripodSupport`は、三脚支持部の有無と、確認できた構成部品を記録します。
レンズとマウントアダプターで同じ定義を使用します。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `tripodSupport.present` | 真偽値 | 三脚支持部の有無 |
| `tripodSupport.components` | tripodSupportComponent[]または`null` | 支持部品。存在は確認できても内訳を特定できない場合は`null` |
| `tripodSupport.components[].type` | `collar-assembly` / `foot` / `support-bridge` / `support-bracket` / `body-mounting-point` / `other` | 支持部品の種類 |
| `tripodSupport.components[].relationship` | `integrated` / `supplied` / `optional` / `null` | 製品との関係 |
| `tripodSupport.components[].removable` | 真偽値または`null` | 取り外し可否 |
| `tripodSupport.components[].interfaces` | tripodSupportInterface[]または`null` | 三脚側の取付方式 |
| `tripodSupport.components[].interfaces[].type` | `arca-compatible` / `mounting-thread` / `other` | 取付方式の分類 |
| `tripodSupport.components[].interfaces[].threadDesignation` | 文字列または`null` | 公表されたねじ規格。`mounting-thread`では必須 |
| `tripodSupport.components[].modelNumberOptions` | 文字列[]または`null` | 公表された型番 |
| `tripodSupport.components[].quantity` | 1以上の整数または`null` | 数量 |
| `tripodSupport.components[].conditions` | [specializedConditions](#focal-length-and-conditions) | バリエーションなどの適用条件 |

ねじ規格を確認できない`mounting-thread`では、`threadDesignation: null`を記録します。
三脚支持部がないことを確認した場合は`{ "present": false }`、有無を確認できない場合は`null`を使います。

## 可動量 {#movements}

`movements`は、ティルト、シフト、および可動部を光軸周りに回転できる範囲を記録します。
レンズとマウントアダプターで同じ定義を使用します。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `movements.tiltMeasurements` | tiltMeasurement[]または`null` | 公称ティルト量。判明している場合は1件以上 |
| `movements.tiltMeasurements[].maximumFromNeutralDegrees` | 正数または`null` | 中立位置から一方向への最大ティルト角（度） |
| `movements.tiltMeasurements[].totalRangeDegrees` | 正数または`null` | 端から端までの全ティルト範囲（度） |
| `movements.tiltMeasurements[].directionality` | `single-direction` / `bidirectional` / `null` | 公表された可動方向 |
| `movements.shiftMeasurements` | shiftMeasurement[]または`null` | 公称シフト量。判明している場合は1件以上 |
| `movements.shiftMeasurements[].maximumFromNeutralMm` | 正数または`null` | 中立位置から一方向への最大シフト量（mm） |
| `movements.shiftMeasurements[].totalRangeMm` | 正数または`null` | 端から端までの全シフト範囲（mm） |
| `movements.shiftMeasurements[].directionality` | `single-direction` / `bidirectional` / `null` | 公表された可動方向 |
| `movements.rotationMeasurements` | rotationMeasurement[]または`null` | 光軸周りの公称回転量。判明している場合は1件以上 |
| `movements.rotationMeasurements[].scope` | `product` / `movement-assembly` / `mount-interface` / `other` | 回転する範囲 |
| `movements.rotationMeasurements[].maximumFromNeutralDegrees` | 0超360以下の数値または`null` | 中立位置から一方向への最大回転角（度） |
| `movements.rotationMeasurements[].totalRangeDegrees` | 0超360以下の数値または`null` | 端から端までの全回転範囲（度） |
| `movements.rotationMeasurements[].directionality` | `single-direction` / `bidirectional` / `null` | 公表された回転方向 |
| `movements.*Measurements[].conditions` | [specializedConditions](#focal-length-and-conditions) | 値が成立するバリエーションなどの条件 |

`movements`は、`tiltMeasurements`、`shiftMeasurements`、`rotationMeasurements`のうち少なくとも一つを持ちます。
測定値の配列に同じ要素を重複して記録できません。
各測定値では中立位置からの最大値と全可動範囲の少なくとも一方に数値が必要で、もう一方を確認できない場合は`null`を記録します。
`directionality`と`conditions`も必須で、追加条件がなければ`conditions: {}`を記録します。
該当する可動機構は確認できるものの公称値を確認できない場合は、対応する値に`null`を記録できます。

## 撮影距離と倍率 {#focus-measurements}

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `minimumFocusDistance.distanceM` | 正数 | 撮像面から被写体までの最短撮影距離（m） |
| `minimumFocusDistance.conditions` | `focusConditions` | 焦点距離などの測定条件 |
| `reproductionMagnification.kind` | `maximum` / `fixed` / `range` / `discrete` | 最大値、固定値、連続範囲、離散値の表現方法 |
| `reproductionMagnification.value` | 0以上の数値 | `maximum`または`fixed`の倍率。等倍は`1` |
| `reproductionMagnification.minimum` | 0以上の数値 | `range`の下限倍率 |
| `reproductionMagnification.maximum` | 0以上の数値 | `range`の上限倍率 |
| `reproductionMagnification.values` | 0以上の数値[] | `discrete`で公表された倍率候補 |
| `reproductionMagnification.conditions` | `focusConditions` | 焦点距離などの測定条件 |
| `workingDistance.distanceM` | 正数 | レンズ先端などから被写体までのワーキングディスタンス（m） |
| `workingDistance.conditions` | `specializedConditions` | 倍率、焦点距離などの測定条件 |

`minimumFocusDistance`と`workingDistance`の各要素では、`distanceM`と`conditions`がどちらも必須です。
`reproductionMagnification`では、`maximum`または`fixed`に`value`、`range`に`minimum`と`maximum`、`discrete`に`values`を使用し、すべての構造で`kind`と`conditions`が必須です。
各構造は排他的で、`values`には重複のない値が1件以上必要です。

## 取付先 {#host}

`host`は、フィルターなどの取付先が製品本体か外付けアクセサリーかを表します。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `host.kind` | `product` / `accessory` | 製品本体か外付けアクセサリーか |
| `host.category` | `lens-hood` / `other` | `accessory`の場合の種類 |
| `host.modelNumberOptions` | 文字列[]または`null` | 取付先アクセサリーについて公式資料で確認できた型番の一覧 |

`kind`が`product`の場合は`kind`だけを記録します。
`accessory`の場合は、`category`と`modelNumberOptions`も必要です。

## リポジトリ検証

`hatch run validate`では、範囲の下限が上限を超えていないことも確認します。
対象には、焦点距離、撮影倍率などの`minimum`と`maximum`が含まれます。
光学構成では、`groups`が`elements`を超えていないことも確認します。

## 関連ページ

- [JSON Schemaリファレンス](../index.md)：JSON Schema全体の構成と読み方
- [値の読み方](../../../value-rules.md)：`null`、空配列、`false`の使い分け
- [レンズと関連光学製品のフィールドリファレンス](../../../lens-field-reference.md)：収録製品データ内での使われ方
- [マウントアダプターのフィールドリファレンス](../../../adapter-field-reference.md)：マウントアダプターで共通定義を使う項目
- [JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/shared/shared-definitions.schema.json)
