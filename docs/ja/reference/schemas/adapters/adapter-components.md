# adapter-components.schema.json

マウントアダプターで共通する製品情報のブロックを定義します。
[adapter-full](adapter-full.md)から参照する定義集であり、単独のJSONファイルを検証するスキーマではありません。

## 定義グループ

| 定義 | 内容 |
| --- | --- |
| [`identity`](#identity) | メーカー、ブランド、製品名、型番、別名、バリエーション |
| [`lifecycle`](#lifecycle) | 発売発表日とメーカーまたはブランドによる状態表記 |
| [`officialProductPage`](#officialproductpage) | 公式製品ページのURL、地域、言語、公開元 |
| [`mountConfiguration`](#mountconfiguration) | 変換元となるレンズ側マウントとZマウントの組み合わせ |
| [`electronics`](#electronics) | 電子接点と、アダプターを介して利用できる電子機能 |
| [`conversionOptics`](#conversionoptics) | 変換光学系の有無と、焦点距離や開放値への影響 |
| [`mechanisms`](#mechanisms) | 絞りリング、ヘリコイド、シフトなどの付加機構 |
| [`physical`](#physical) | 寸法、重量、環境保護に関する公式表現、三脚取付部 |

ID、文字列、地域コード、言語タグなどの小さな定義は、[共通定義](../shared/shared-definitions.md)を参照します。

## 共通ブロックの実例

マウントアダプター FTZ IIを例に、収録製品データでの配置を示します。
各コードは、実際の収録製品データから、説明に必要なブロックや配列要素を抜粋しています。

=== "識別情報と発売情報"

    参照元：`data/records/adapters/nikon/mount-adapter-ftz-ii.json`

    参照箇所：`identity`、`lifecycle`

    ```json
    {
      "identity": {
        "manufacturerId": "nikon",
        "brandId": "nikon",
        "productName": "Mount Adapter FTZ II",
        "modelNumberOptions": null,
        "alternateNames": [
          {
            "name": "マウントアダプター FTZ II",
            "region": "JP",
            "language": "ja"
          }
        ],
        "variants": null
      },
      "lifecycle": {
        "announcementDate": "2021-10-28",
        "officialDesignations": []
      }
    }
    ```

=== "公式製品ページ"

    参照元：`data/records/adapters/nikon/mount-adapter-ftz-ii.json`

    参照箇所：`officialProductPages[1]`

    ```json
    {
      "officialProductPages": [
        {
          "url": "https://nij.nikon.com/products/lineup/accessory/body/ftz_2/index.html",
          "pageFamilies": [
            "nikon-imaging-japan"
          ],
          "region": "JP",
          "language": "ja",
          "publisher": {
            "type": "manufacturer-or-brand",
            "name": "Nikon"
          }
        }
      ]
    }
    ```

=== "接続と機能"

    参照元：`data/records/adapters/nikon/mount-adapter-ftz-ii.json`

    参照箇所：`mountConfigurations`、`electronics`、`electronicServices`、`conversionOptics`、`mechanisms`

    ```json
    {
      "mountConfigurations": [
        {
          "lensSideMountSystemId": "nikon-f",
          "cameraSideMountSystemId": "nikon-z",
          "lensRetention": null,
          "lensRearProtrusionLimits": null
        }
      ],
      "electronics": {
        "electronicContacts": true,
        "autofocus": true,
        "cameraControlledAperture": true,
        "lensStabilizationCommunication": true,
        "manualFocusAssistance": true,
        "metadataTransmission": {
          "present": true,
          "standards": [
            "exif"
          ]
        },
        "lensPowerTransmission": null,
        "recordingTriggerTransmission": null
      },
      "electronicServices": null,
      "conversionOptics": {
        "present": false
      },
      "mechanisms": []
    }
    ```

=== "外形"

    参照元：`data/records/adapters/nikon/mount-adapter-ftz-ii.json`

    参照箇所：`physical`

    ```json
    {
      "physical": {
        "dimensionMeasurements": [
          {
            "widthMm": 70,
            "heightMm": 70,
            "lengthMm": 36,
            "approximate": true,
            "conditions": {
              "excludesProjections": true
            }
          }
        ],
        "weightMeasurements": [
          {
            "grams": 125,
            "approximate": true,
            "conditions": {}
          }
        ],
        "officialEnvironmentalProtectionClaims": [
          {
            "types": [
              "dust-resistant",
              "drip-resistant"
            ],
            "scope": {
              "kind": "product"
            },
            "conditions": {}
          }
        ],
        "tripodSupport": {
          "present": false
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
| `identity.variants` | variant[]または`null` | 一つの製品として扱う色やマウントのバリエーション |
| `identity.variants[].variantId` | ID文字列 | `mountConfigurations[]`から参照するバリエーションID。各要素で必須 |
| `identity.variants[].name` | 文字列 | バリエーションの公式名または識別名。各要素で必須 |
| `identity.variants[].modelNumberOptions` | 文字列[]または`null` | バリエーション固有の公式型番。各要素で必須 |
| `identity.variants[].color` | 文字列 | 公式な色名 |

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

## マウントの組み合わせ {#mountconfiguration}

`mountConfigurations`は1件以上必要です。
同一内容の要素は重複できません。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `mountConfigurations[].lensSideMountSystemId` | マウントシステムID | 変換元となるレンズ側マウント。各要素で必須 |
| `mountConfigurations[].cameraSideMountSystemId` | `"nikon-z"` | 変換先となるカメラ側マウント。各要素で必須 |
| `mountConfigurations[].lensRetention` | lensRetentionまたは`null` | レンズ側マウントの固定方式。各要素で必須 |
| `mountConfigurations[].lensRetention.type` | `mount-defined` / `positive-lock` / `locking-ring` / `other` | 固定方式の分類 |
| `mountConfigurations[].lensRetention.officialName` | 文字列（省略可） | メーカーが安定して使う固定方式の名称 |
| `mountConfigurations[].lensRearProtrusionLimits` | lensRearProtrusionLimit[]または`null` | 許容されるレンズ後端の突出量。各要素で必須 |
| `mountConfigurations[].lensRearProtrusionLimits[].maximumMm` | 0以上の数値 | 基準面からの最大突出量（mm） |
| `mountConfigurations[].lensRearProtrusionLimits[].referencePlane` | `mount-flange` / `mount-face` / `other` / `null` | 測定の基準面 |
| `mountConfigurations[].lensRearProtrusionLimits[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | 適用条件 |
| `mountConfigurations[].variantId` | ID文字列 | 対応する`identity.variants[].variantId` |

`lensSideMountSystemId`には`nikon-z`を指定できません。
両側のマウントシステムIDがレジストリに登録され、`variantId`が`identity.variants`内のIDを参照することは、リポジトリ検証で確認します。

## 電子機能 {#electronics}

`electronics`はオブジェクトまたは`null`です。
オブジェクトの場合、直下の8フィールドをすべて持ちます。
各値はアダプター製品として確認できた機能を示し、すべてのレンズ、カメラ、ファームウェアの組み合わせでの動作は保証しません。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `electronics.electronicContacts` | 真偽値または`null` | 電子接点の有無 |
| `electronics.autofocus` | 真偽値または`null` | オートフォーカス対応 |
| `electronics.cameraControlledAperture` | 真偽値または`null` | カメラからの絞り制御 |
| `electronics.metadataTransmission` | [metadataTransmission](../shared/shared-definitions.md#electronic-data) | 撮影メタデータの伝達と公表規格 |
| `electronics.lensStabilizationCommunication` | 真偽値または`null` | レンズ内手ぶれ補正との通信 |
| `electronics.manualFocusAssistance` | 真偽値または`null` | マニュアルフォーカス補助との連携 |
| `electronics.lensPowerTransmission` | 真偽値または`null` | カメラ側からレンズへの電力供給 |
| `electronics.recordingTriggerTransmission` | 真偽値または`null` | レンズ側からカメラへの録画操作の伝達 |

`electronicContacts`が`false`の場合、ほかの7項目も確認済みの否定値でなければなりません。
ファームウェア更新や設定用の接続は、共通定義の`electronicServices`に記録します。
この分離により、電子接点を使わないUSB接続やドックも表現できます。

## 変換光学系 {#conversionoptics}

`conversionOptics`の構造は、変換光学系の確認状態によって変わります。

| 状態 | 記録する構造 |
| --- | --- |
| 有無を採用できる公開情報で確認できない | `null` |
| 光学系がないことを確認した | `{ "present": false }` |
| 光学系があることを確認した | `present`と、下表に示す7個の光学仕様フィールドを持つオブジェクト |

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `conversionOptics.present` | 真偽値 | マウント変換に関わる内蔵光学系の有無 |
| `conversionOptics.focalLengthMultiplier` | 正数または`null` | 内蔵光学系による焦点距離の倍率 |
| `conversionOptics.apertureChange` | apertureChangeまたは`null` | 内蔵光学系による開放値の変化 |
| `conversionOptics.apertureChange.direction` | `brighter` / `darker` / `unchanged` | 開放値が明るくなる、暗くなる、変わらないのいずれか |
| `conversionOptics.apertureChange.stops` | 0以上の数値 | 変化量の絶対値（段）。`unchanged`では`0`、それ以外では正数 |
| `conversionOptics.apertureChange.relation` | `exact` / `approximately` / `less-than` | 公表値が正確値、概算値、指定段数未満のいずれか。`unchanged`では`exact` |
| `conversionOptics.opticalConstruction` | [opticalConstruction](../shared/shared-definitions.md#opticalconstruction)または`null` | 内蔵光学系の群数と枚数 |
| `conversionOptics.specialElements` | [specialElement](../shared/shared-definitions.md#specialelement)[]または`null` | 特殊光学素子。確認済みで該当なしの場合は`[]` |
| `conversionOptics.coatings` | [coating](../shared/shared-definitions.md#coating)[]または`null` | 内蔵光学系のコーティング。確認済みで該当なしの場合は`[]` |
| `conversionOptics.supportedImageCircleDiameterMm` | imageCircleDiameterまたは`null` | 対応する像円径（mm） |
| `conversionOptics.supportedImageCircleDiameterMm.kind` | `value` / `range` | 単一値か範囲か |
| `conversionOptics.supportedImageCircleDiameterMm.diameterMm` | 正数 | `value`の像円径（mm） |
| `conversionOptics.supportedImageCircleDiameterMm.minimumDiameterMm` | 正数 | `range`の下限（mm） |
| `conversionOptics.supportedImageCircleDiameterMm.maximumDiameterMm` | 正数 | `range`の上限（mm） |
| `conversionOptics.maximumSupportedAperture` | maximumSupportedApertureまたは`null` | 対応レンズについて公表された最も明るい開放値 |
| `conversionOptics.maximumSupportedAperture.scale` | `f-number` / `t-number` | F値かT値か |
| `conversionOptics.maximumSupportedAperture.value` | 正数 | 開放値。たとえば`scale: "t-number"`と`value: 2.8`はT2.8を表す |

`present`が`false`の場合、`present`以外の光学仕様は記録しません。
`true`の場合は7フィールドが必須で、採用できる公開情報から個別の値を確認できないフィールドに`null`を記録します。
像円径が範囲の場合は`minimumDiameterMm`が`maximumDiameterMm`以下であることもリポジトリ検証で確認します。

## 付加機構 {#mechanisms}

`mechanisms`は、確認できた付加機構をオブジェクトとして重複なく並べる配列または`null`です。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `mechanisms[].type` | `aperture-ring` / `drop-in-filter` / `flange-focal-distance-adjustment` / `helicoid` / `shift` / `tilt` / `rotation` / `other` | 付加機構の分類 |
| `mechanisms[].officialName` | 文字列（省略可） | メーカーが安定して使う機構名 |
| `mechanisms[].movements` | [movements](../shared/shared-definitions.md#movements)または`null` | シフト、ティルト、回転の公称可動量 |
| `mechanisms[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | 機構が成立する条件 |

付加機構の一覧を確認し、該当する機構がない場合は`[]`、採用できる公開情報で確認できない場合は`null`を記録します。
シフト、ティルト、回転では`movements`が必須で、対応する種類の測定値だけを記録できます。
`shift`は`movements.shiftMeasurements`、`tilt`は`movements.tiltMeasurements`、`rotation`は`movements.rotationMeasurements`を使用します。
機構は確認できても可動量を確認できない場合は`movements: null`を使います。
`movements`をオブジェクトにして、対応する測定値だけを`null`にする表現は使用できません。
それ以外の機構には`movements`を記録しません。
レンズの固定方式は付加機構に混ぜず、該当する`mountConfigurations[].lensRetention`に記録します。

## 寸法、重量、環境保護表現、三脚取付部 {#physical}

`physical`直下の`dimensionMeasurements`、`weightMeasurements`、`officialEnvironmentalProtectionClaims`、`tripodSupport`はすべて必須です。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `physical.dimensionMeasurements` | dimensionMeasurement[]または`null` | 公式寸法。判明している場合は1件以上 |
| `physical.dimensionMeasurements[].maximumDiameterMm` | 正数 | 最大径mm |
| `physical.dimensionMeasurements[].lengthMm` | 正数 | メーカー基準による長さmm |
| `physical.dimensionMeasurements[].widthMm` | 正数 | 幅mm |
| `physical.dimensionMeasurements[].heightMm` | 正数 | 高さmm |
| `physical.dimensionMeasurements[].unclassifiedDimensionsMm` | 正数[] | 公開情報源が軸名を示していない寸法値。公表順を維持し、1件以上 |
| `physical.dimensionMeasurements[].approximate` | 真偽値 | 公表値が概算表記か。省略時は、情報源に概算表記がない |
| `physical.dimensionMeasurements[].conditions` | dimensionMeasurementConditions | 寸法の測定条件。各要素で必須 |
| `physical.dimensionMeasurements[].conditions.variantId` | ID文字列 | 寸法が適用される製品バリエーション |
| `physical.dimensionMeasurements[].conditions.componentStates` | measurementComponentStates | 測定時に各部品が取り付けられていたか |
| `physical.dimensionMeasurements[].conditions.excludesProjections` | 真偽値 | 寸法が突起部を除くか |
| `physical.dimensionMeasurements[].note` | 文字列 | 構造化フィールドで表せない、情報源が明示した測定条件や定義 |
| `physical.weightMeasurements` | weightMeasurement[]または`null` | 公式重量。判明している場合は1件以上 |
| `physical.weightMeasurements[].grams` | 正数 | 重量g。各要素で必須 |
| `physical.weightMeasurements[].approximate` | 真偽値 | 公表値が概算表記か。省略時は、情報源に概算表記がない |
| `physical.weightMeasurements[].conditions` | weightMeasurementConditions | 重量の測定条件。各要素で必須 |
| `physical.weightMeasurements[].conditions.variantId` | ID文字列 | 重量が適用される製品バリエーション |
| `physical.weightMeasurements[].conditions.componentStates` | measurementComponentStates | 測定時に各部品が取り付けられていたか |
| `physical.weightMeasurements[].note` | 文字列 | 構造化フィールドで表せない、情報源が明示した測定条件 |
| `physical.officialEnvironmentalProtectionClaims` | [environmentalClaim](../shared/shared-definitions.md#environmentalclaim)[]または`null` | 防塵、防滴、耐候などの公式表現。確認済みで該当なしの場合は`[]` |
| `physical.tripodSupport` | [tripodSupport](../shared/shared-definitions.md#tripod-support) | 三脚支持部の有無と構成部品 |

`measurementComponentStates`には、`tripodCollarAssembly`、`tripodFoot`、`tripodMountCover`、`lensHood`、`frontCap`、`rearCap`、`dropInFilter`のうち、情報源が明示する部品だけを真偽値で記録します。
寸法の各要素には、`maximumDiameterMm`、`lengthMm`、`widthMm`、`heightMm`、`unclassifiedDimensionsMm`のうち少なくとも一つが必要です。
`tripodSupport.present`が`false`の場合は`present`だけを持ちます。

## 関連ページ

- [共通定義](../shared/shared-definitions.md)：ID、文字列、地域コード、言語タグなどの小さな定義
- [adapter-full](adapter-full.md)：各定義を組み合わせた製品1件の構造
- [マウントアダプターのフィールドリファレンス](../../../adapter-field-reference.md)：実データを使った各ブロックの説明

[JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/adapters/adapter-components.schema.json)
