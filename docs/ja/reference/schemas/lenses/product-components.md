# product-components.schema.json

レンズ、テレコンバーター、ピンホールで共通する製品情報のブロックを定義します。
[product-full](product-full.md)から参照する定義集であり、単独のJSONファイルを検証するスキーマではありません。

## 定義グループ

| 定義 | 内容 |
| --- | --- |
| [`identity`](#identity) | メーカー、ブランド、製品名、型番、別名、バリエーション |
| [`lifecycle`](#lifecycle) | 発売発表日とメーカーまたはブランドによる状態表記 |
| [`officialProductPage`](#officialproductpage) | 公式製品ページのURL、地域、言語、公開元 |
| [`mount`](#mount) | Zマウントとの接続、電子接点、製品に付属または専用のマウントアダプター |
| [`physical`](#physical) | 寸法、重量、保護表記、フィルター、三脚取付部、外形変化 |
| [`control`](#control) | リング、スイッチ、ボタン、表示などの操作部 |
| [`accessories`](#accessories) | フード、キャップ、ケースなど |

ID、数値、測定条件、レンズ構成などの小さな定義は、[共通定義](../shared/shared-definitions.md)を参照します。

## 共通ブロックの実例

NIKKOR Z 24-70mm f/2.8 S IIを例に、収録製品データでの配置を示します。
各コードは、記載したブロックだけを取り出した実データです。

=== "識別情報と発売情報"

    参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

    参照箇所：`identity`、`lifecycle`

    ```json
    {
      "identity": {
        "manufacturerId": "nikon",
        "brandId": "nikkor",
        "productName": "NIKKOR Z 24-70mm f/2.8 S II",
        "modelNumberOptions": null,
        "alternateNames": null,
        "variants": null
      },
      "lifecycle": {
        "announcementDate": "2025-08-22",
        "officialDesignations": []
      }
    }
    ```

=== "マウント"

    参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

    参照箇所：`mount`

    ```json
    {
      "systemId": "nikon-z",
      "replaceability": "fixed",
      "mountOwnerRelationship": "mount-owner",
      "electronicContacts": {
        "present": true,
        "metadataTransmission": {
          "present": true,
          "standards": [
            "exif"
          ]
        }
      }
    }
    ```

## 識別情報 {#identity}

`identity`直下の6フィールドはすべて必須です。
型番、別名、バリエーションを採用できる公開情報で確認できない場合も、フィールドを省略せず`null`を記録します。
型番として扱う識別子の範囲は、[共通定義の`modelNumberOptions`](../shared/shared-definitions.md#basic-values)に従います。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `identity.manufacturerId` | ID文字列 | メーカー・ブランドレジストリに登録された、製品を製造する主体のID |
| `identity.brandId` | ID文字列 | メーカー・ブランドレジストリに登録された、製品に表示され販売上の識別に使われるブランドのID |
| `identity.productName` | 文字列 | 大文字小文字や記号を含む公式製品名 |
| `identity.modelNumberOptions` | 文字列[]または`null` | 公式資料で確認できた型番の一覧 |
| `identity.alternateNames` | alternateName[]または`null` | 地域名、旧名など、公式に確認できる別名 |
| `identity.alternateNames[].name` | 文字列 | 別名。各要素で必須 |
| `identity.alternateNames[].brandId` | ID文字列 | `identity.brandId`と異なるブランドを使う別名のブランドID |
| `identity.alternateNames[].region` | 2文字地域コード | 別名を使用する地域 |
| `identity.alternateNames[].language` | 言語タグ | 別名の言語 |
| `identity.variants` | variant[]または`null` | 一つの製品として扱う色や販売仕様のバリエーション |
| `identity.variants[].variantId` | ID文字列 | 測定条件から参照するバリエーションID。各要素で必須 |
| `identity.variants[].name` | 文字列 | バリエーションの公式名または識別名。各要素で必須 |
| `identity.variants[].modelNumberOptions` | 文字列[]または`null` | バリエーション固有の公式型番。各要素で必須 |
| `identity.variants[].color` | 文字列 | 公式な色名 |
| `identity.variants[].focusScaleUnit` | `meters` / `feet` | 距離目盛の単位 |

## 発売情報 {#lifecycle}

`announcementDate`と`officialDesignations`は必須です。
開発発表日は`announcementDate`に使用しません。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `lifecycle.announcementDate` | 日付または`null` | メーカーまたはブランドが製品の発売を公式発表した日 |
| `lifecycle.officialDesignations` | designation[]または`null` | メーカーまたはブランドが公式に示す旧製品、販売終了、生産終了などの状態表記。一覧を確認し、該当する表記がない場合は`[]` |
| `lifecycle.officialDesignations[].type` | `legacy-product` / `sales-ended` / `production-ended` / `discontinued` | 公式表現を正規化した状態。各要素で必須 |
| `lifecycle.officialDesignations[].region` | 2文字地域コード | 状態表記が適用される地域 |
| `lifecycle.officialDesignations[].observedOn` | 日付 | 状態表記を確認した日 |

`officialDesignations: []`は、現在販売中、在庫あり、入手可能であることを意味しません。

## 公式製品ページ {#officialproductpage}

`officialProductPages[]`の各要素は、`url`、`pageFamilies`、`region`、`language`、`publisher`の5フィールドを直下に持ちます。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `officialProductPages[].url` | HTTP(S) URL | 製品そのものの公式メインページ |
| `officialProductPages[].pageFamilies` | 列挙値[] | `home-country`、`global`、`japan`、`nikon-imaging-japan`、`usa`から選ぶページ系統。1件以上 |
| `officialProductPages[].region` | 2文字地域コードまたは`null` | 対象地域。グローバルページなど地域を限定できない場合は`null` |
| `officialProductPages[].language` | 言語タグまたは`null` | ページの主言語 |
| `officialProductPages[].publisher` | オブジェクト | 公開元の種別と名称 |
| `officialProductPages[].publisher.type` | `manufacturer-or-brand` / `authorized-distributor` | メーカーまたはブランド自身のページか、正規代理店のページか |
| `officialProductPages[].publisher.name` | 文字列 | 公開元の名称 |

`publisher.type`と`publisher.name`は、`publisher`内でどちらも必須です。

## Zマウントとの接続 {#mount}

`mount`直下の`systemId`、`replaceability`、`mountOwnerRelationship`、`electronicContacts`は必須です。
`adapter`は、Zマウント用アダプターを同梱する製品、または対象製品や公式に示された製品シリーズ専用のアダプターを使う製品だけが持ちます。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `mount.systemId` | `"nikon-z"` | 対象となるマウントシステムの固定値 |
| `mount.replaceability` | `fixed` / `user-interchangeable` / `service-interchangeable` / `null` | 製品側マウントの交換可否と交換主体 |
| `mount.mountOwnerRelationship` | `mount-owner` / `officially-licensed` / `null` | Nikon自身または公式ライセンスとの関係 |
| `mount.electronicContacts` | オブジェクトまたは`null` | 電子接点の有無とメタデータ伝達。採用できる公開情報で確認できない場合は`null` |
| `mount.electronicContacts.present` | 真偽値 | 電子接点の有無 |
| `mount.electronicContacts.metadataTransmission` | [metadataTransmission](../shared/shared-definitions.md#electronic-data) | 電子接点がある場合の撮影メタデータ伝達と公表規格 |
| `mount.adapter` | officialMountAdapter | 収録条件を満たすZマウント用アダプター |
| `mount.adapter.relationship` | `supplied` / `optional` | 製品への同梱または別売 |
| `mount.adapter.dedicatedToProduct` | 真偽値または`null` | 対象製品または公式に示された製品シリーズ専用か |
| `mount.adapter.nativeMountSystemId` | マウントシステムIDまたは`null` | アダプター装着前のレンズ側マウントシステム |
| `mount.adapter.name` | 文字列または`null` | アダプターの公式名称 |
| `mount.adapter.modelNumberOptions` | 文字列[]または`null` | アダプターについて公式資料で確認できた型番の一覧 |

### 電子接点の条件

| `mount.electronicContacts` | 許可される構造 |
| --- | --- |
| `null` | 電子接点の有無を採用できる公開情報で確認できない |
| `{ "present": false }` | `metadataTransmission`は指定できない |
| `{ "present": true, "metadataTransmission": ... }` | `metadataTransmission`が必須。伝達の有無を確認できない場合は`null` |

### マウントアダプターの条件

`mount.adapter`直下の5フィールドはすべて必須です。
`relationship`が`optional`の場合、`dedicatedToProduct`は`true`でなければなりません。

詳しい収録条件と実例は、[レンズと関連光学製品のフィールドリファレンス](../../../lens-field-reference.md)を参照してください。

## 外形と取付部 {#physical}

`physical`直下の`dimensionMeasurements`、`weightMeasurements`、`officialEnvironmentalProtectionClaims`、`filterInterfaces`、`tripodSupport`は必須です。
その他のフィールドは、構造的に適用できる製品だけが持ちます。

### 寸法と重量

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `physical.dimensionMeasurements` | measurement[]または`null` | 公式寸法。判明している場合は1件以上 |
| `physical.dimensionMeasurements[].maximumDiameterMm` | 正数または`null` | 最大径mm |
| `physical.dimensionMeasurements[].lengthMm` | 正数または`null` | メーカー基準による長さmm |
| `physical.dimensionMeasurements[].approximate` | 真偽値 | 情報源が測定値全体を概算と明示した場合だけ記録する |
| `physical.dimensionMeasurements[].conditions.state` | `operational` / `storage` / `at-infinity` | 寸法を測定した製品の状態 |
| `physical.dimensionMeasurements[].conditions.variantId` | ID文字列 | 寸法が特定のバリエーションにだけ適用される場合のID |
| `physical.dimensionMeasurements[].conditions.attachedComponents` | 列挙値[] | 測定時に装着していた部品 |
| `physical.weightMeasurements` | measurement[]または`null` | 公式重量。判明している場合は1件以上 |
| `physical.weightMeasurements[].grams` | 正数 | 重量g |
| `physical.weightMeasurements[].approximate` | 真偽値 | 情報源が重量を概算と明示した場合だけ記録する |
| `physical.weightMeasurements[].conditions.attachedComponents` | 列挙値[] | 重量に含まれる部品。装着部品を確認し、該当する部品がない場合は`[]` |
| `physical.weightMeasurements[].conditions.variantId` | ID文字列 | 重量が特定のバリエーションにだけ適用される場合のID |

寸法の各要素では、`maximumDiameterMm`と`lengthMm`の少なくとも一方に正数が必要です。
両フィールドは必須であるため、公表されていない側には`null`を記録します。
寸法の`conditions`と、重量の`conditions.attachedComponents`も必須です。

`attachedComponents`には、次の値を使用できます。

- 三脚取付部：`tripod-collar-assembly`、`tripod-foot`、`tripod-mount-cover`
- レンズ付属品：`lens-hood`、`front-cap`、`rear-cap`
- フィルター：`drop-in-filter`
- その他：`other`

### 保護表記

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `physical.officialEnvironmentalProtectionClaims` | claim[]または`null` | 防塵や防滴などの公式表現。一覧を確認し、該当する表現がない場合は`[]` |
| `physical.officialEnvironmentalProtectionClaims[].types` | 列挙値[] | `dust-resistant`、`drip-resistant`、`splash-resistant`、`moisture-resistant`、`weather-resistant`、`waterproof`、`other`。1件以上 |
| `physical.officialEnvironmentalProtectionClaims[].scope.kind` | `product` / `component` | 製品全体の表記か、特定部品だけの表記か |
| `physical.officialEnvironmentalProtectionClaims[].scope.component` | 文字列 | `scope.kind: "component"`の場合の対象部品名 |
| `physical.officialEnvironmentalProtectionClaims[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | 表記が成立する焦点距離、ボディ、バリエーションなどの条件 |

`scope.kind`が`product`の場合、`scope.component`は使用しません。
`component`の場合は、`scope.component`が必須です。

### フィルター取付方式

`physical.filterInterfaces`は、取付方式を確認し、該当する方式がない場合を`[]`、採用できる公開情報で確認できない場合を`null`で表します。
各要素では、`type`に応じて寸法フィールドが変わります。

| `type` | 必須の寸法 | 取付先 |
| --- | --- | --- |
| `front-thread` | `diameterMm` | `host` |
| `rear-thread` | `diameterMm` | `host` |
| `drop-in` | `filterDiameterMm` | `host` |
| `rear-gelatin` | `sheetDimensionsMm` | `host` |

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `physical.filterInterfaces[].diameterMm` | 正数 | 前面または後部のねじ径mm |
| `physical.filterInterfaces[].filterDiameterMm` | 正数 | ドロップインフィルター径mm |
| `physical.filterInterfaces[].sheetDimensionsMm` | オブジェクトまたは`null` | 後部ゼラチンフィルターの幅と高さ |
| `physical.filterInterfaces[].sheetDimensionsMm.width` | 正数 | 幅mm |
| `physical.filterInterfaces[].sheetDimensionsMm.height` | 正数 | 高さmm |
| `physical.filterInterfaces[].host` | [host](../shared/shared-definitions.md#host) | フィルターを取り付ける製品本体またはアクセサリー |

### 三脚取付部と外形変化

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `physical.tripodSupport` | [tripodSupport](../shared/shared-definitions.md#tripod-support) | 三脚支持部の有無、構成部品、製品との関係、取付方式 |
| `physical.externalLengthDuringZoom` | `constant` / `variable` / `null` | ズーム操作による外形長の変化 |
| `physical.externalLengthDuringFocus` | `constant` / `variable` / `null` | フォーカス操作による外形長の変化 |
| `physical.isRetractableForStorage` | 真偽値または`null` | 使用前に繰り出す収納機構の有無 |
| `physical.frontAccessoryInterface.outsideDiameterMm` | 正数 | クランプ式の前面アクセサリーを取り付ける外径mm |

`tripodSupport.present`が`false`の場合は`present`だけを持ちます。
`true`の場合は`components`も必須で、存在は確認できても内訳を特定できない場合は`null`を記録します。

## 操作部 {#control}

`controls[]`の各要素は、`type`と`quantity`を必ず持ちます。
`officialName`は、製品上の表示や公式仕様で安定して使われる名称がある場合に、どの操作部にも追加できます。`Focus ring`など`type`と同義の一般名称は省略します。公式英語ページに対応する名称がある場合はその英語表記を使い、公式な英語表記がない名称を独自に翻訳しません。

リングとして扱う`type`は、`aperture-ring`、`control-ring`、`function-ring`、`focus-ring`、`zoom-ring`です。
これらの操作部だけが、`clickBehavior`、`rotationDegrees`、`geared`、`response`を使用できます。

その他の`type`には、次の値があります。

- ズーム操作：`power-zoom-control`、`zoom-lever`、`zoom-lock`
- ボタン：`function-button`、`memory-set-button`
- フォーカス操作：`focus-mode-switch`、`focus-limiter`
- 絞りとコントロールリング：`aperture-ring-click-switch`、`control-ring-click-switch`、`aperture-ring-lock`
- 表示：`information-display`、`focus-distance-scale`、`depth-of-field-scale`
- その他：`other`

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `controls[].type` | 列挙値 | 操作部の種類 |
| `controls[].quantity` | 1以上の整数 | 同じ種類の操作部の個数 |
| `controls[].officialName` | 文字列（省略可） | 製品上の表示や公式仕様でメーカーが安定して使い、`type`だけでは保持できない操作部の名称 |
| `controls[].clickBehavior` | `clicked` / `declicked` / `switchable` | リングのクリック感 |
| `controls[].rotationDegrees` | 正数 | リングの公称回転角 |
| `controls[].geared` | 真偽値 | シネギアなどの歯があるか |
| `controls[].response` | `linear` / `nonlinear` / `switchable` | 電子リングの回転量に対する応答方式 |

## アクセサリー {#accessories}

`accessories`はオブジェクトまたは`null`です。
オブジェクトの場合、直下の6フィールドをすべて持ち、各フィールドには配列または`null`を記録します。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `accessories.lensHoods` | relationship[]または`null` | レンズフード |
| `accessories.frontCaps` | relationship[]または`null` | 前キャップ |
| `accessories.rearCaps` | relationship[]または`null` | 後キャップ |
| `accessories.lensCases` | caseAccessory[]または`null` | ソフトケースまたはハードケース |
| `accessories.lensStraps` | relationship[]または`null` | レンズストラップ |
| `accessories.protectiveWraps` | relationship[]または`null` | 保護用ラップ |
| `accessories.*[].modelNumberOptions` | 文字列[]または`null` | アクセサリーについて公式資料で確認できた型番の一覧。各要素で必須 |
| `accessories.*[].quantity` | 1以上の整数 | 個数。各要素で必須 |
| `accessories.lensHoods[]`などの`relationship` | `supplied` / `optional` / `integrated` / `null` | フード、キャップ、ストラップ、ラップと製品の関係 |
| `accessories.lensCases[].relationship` | `supplied` / `optional` / `null` | ケースと製品の関係 |
| `accessories.lensCases[].construction` | `soft-case` / `hard-case` | ケースの構造 |

## 関連ページ

- [共通定義](../shared/shared-definitions.md)：ID、数値、測定条件、電子サービス、三脚支持、取付先などの定義
- [product-full](product-full.md)：共通ブロックと製品種別ブロックの組み合わせ
- [レンズと関連光学製品のフィールドリファレンス](../../../lens-field-reference.md)：実データを使った各ブロックの説明

[JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/product-components.schema.json)
