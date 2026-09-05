# マウントアダプターのフィールドリファレンス

このページは、マウントアダプターの収録製品データと、配布データ内の製品1件に含まれる項目を確認するための参照ページです。
初めから通読する必要はなく、項目名から必要な節を参照できます。

マウントアダプターの収録製品データは、すべての製品で同じ構造を使います。
製品種別による分岐がないため、`productType`や製品種別ブロックは持ちません。

!!! info "マウントアダプターはFull版のみ"

    マウントアダプターFull版の`adapters`には、各収録製品データから`$schema`を除いた内容が入ります。
    ファイル名は`z-mount-adapters.full.json`です。
    Light版は設けません。

掲載しているJSONは、実際の収録製品データから説明に必要な部分を抜き出したものです。
配列の一部だけを掲載している例もあります。
各項目の型、必須性、許可される値は[JSON Schemaリファレンス](reference/schemas/adapters/adapter-full.md)で確認してください。

基本例にはマウントアダプター FTZ IIを使います。
複数のマウント構成、内蔵光学系、付加機構は、Magic Shift Converter (MSC)で補います。
レンズと関連光学製品の項目は、[レンズと関連光学製品のフィールドリファレンス](lens-field-reference.md)で説明しています。

## 識別情報と公開情報（`identity`、`lifecycle`、`officialProductPages`）

| 項目 | 記録する情報 |
| --- | --- |
| `id` | 製品を識別するためのID |
| `identity` | メーカーID、ブランドID、公式製品名、公式型番、公式な別名、同一製品内のバリエーション |
| `lifecycle` | 公式な発売発表日と、メーカーまたはブランドが公式に示す旧製品、販売終了、生産終了などの状態表記 |
| `officialProductPages` | 製品自体を紹介する公式のメインページと、その地域、言語、公開元 |

マウントアダプター FTZ IIを例に、識別情報、発売発表日、公式製品ページの記録方法を説明します。

参照元：`data/records/adapters/nikon/mount-adapter-ftz-ii.json`

```json
{
  "id": "mount-adapter-ftz-ii",
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
  },
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

`identity.manufacturerId`には製造主体のID、`identity.brandId`には製品に表示されるブランドのIDを記録します。
この例では、メーカーとブランドがどちらも`nikon`で、表示名はNikonです。
配布用JSONでは、表示名をルートの`referenceData`から取得できます。
英語の公式製品名は`identity.productName`、日本向けの公式名称は`identity.alternateNames`に入っています。

`lifecycle.announcementDate`は公式な発売発表日です。
開発発表日で代用しません。
`lifecycle.officialDesignations: []`は、確認した公式な状態表記が0件であることを示します。
現在販売中、在庫あり、入手可能であることは意味しません。
公式製品ページが削除されたことだけを理由に、販売終了とは判断しません。
公式製品ページと調査に使った情報源の違いは[値の読み方](value-rules.md#urls)で説明しています。

## マウント構成（`mountConfigurations`）

`mountConfigurations`では、変換元となるレンズ側マウントと、変換先となるカメラ側マウントを組み合わせて記録します。

| 項目 | 記録する情報 |
| --- | --- |
| `lensSideMountSystemId` | 変換元となる交換レンズマウントのマウントシステムID |
| `cameraSideMountSystemId` | 変換先となるカメラ側のマウントシステムID。値は`nikon-z` |
| `lensRetention` | レンズ側マウントの固定方式と公式名称。確認できない場合は`null` |
| `lensRearProtrusionLimits` | レンズ後端の許容突出量、基準面、適用条件。確認できない場合は`null` |
| `variantId` | マウントの組み合わせに対応する製品バリエーションのID |

=== "一つのマウント構成"

    マウントアダプター FTZ IIを例に、一つのマウント構成を持つ場合の記録方法を説明します。

    参照元：`data/records/adapters/nikon/mount-adapter-ftz-ii.json`

    ```json
    {
      "mountConfigurations": [
        {
          "lensSideMountSystemId": "nikon-f",
          "cameraSideMountSystemId": "nikon-z",
          "lensRetention": null,
          "lensRearProtrusionLimits": null
        }
      ]
    }
    ```

    この例では、変換元のNikon Fを`lensSideMountSystemId`、変換先のNikon Zを`cameraSideMountSystemId`に記録しています。

=== "複数のマウント構成"

    Magic Shift Converter (MSC)を例に、複数のマウント構成を持つ場合の記録方法を説明します。
    `mountConfigurations[].variantId`は、対応する`identity.variants[].variantId`を指します。

    参照元：`data/records/adapters/laowa/laowa-magic-shift-converter-z.json`

    ```json
    {
      "identity": {
        "variants": [
          {
            "variantId": "canon-ef-nikon-z",
            "name": "Canon EF to Nikon Z",
            "modelNumberOptions": null
          },
          {
            "variantId": "nikon-f-nikon-z",
            "name": "Nikon F to Nikon Z",
            "modelNumberOptions": null
          }
        ]
      },
      "mountConfigurations": [
        {
          "lensSideMountSystemId": "canon-ef",
          "cameraSideMountSystemId": "nikon-z",
          "variantId": "canon-ef-nikon-z",
          "lensRetention": null,
          "lensRearProtrusionLimits": null
        },
        {
          "lensSideMountSystemId": "nikon-f",
          "cameraSideMountSystemId": "nikon-z",
          "variantId": "nikon-f-nikon-z",
          "lensRetention": null,
          "lensRearProtrusionLimits": null
        }
      ]
    }
    ```

    この例では、Canon EF用とNikon F用のバリエーションを一件の収録製品データに記録しています。

マウントシステムIDとレジストリの関係は[データモデル](data-model.md#shared-registries)で説明しています。

## 電子機能と接続サービス（`electronics`、`electronicServices`）

`electronics`には、電子接点の有無と、アダプターを介して利用できる電子機能を記録します。

!!! warning "個別の組み合わせは保証しません"
    ここで記録する値は、アダプター製品として採用できる公開情報から確認できた機能です。
    すべてのレンズ、カメラ、ファームウェアの組み合わせで動作することは保証しません。
    個別の互換性は、メーカーまたはブランドの対応表やマニュアルで確認してください。

| 項目 | 記録する情報 |
| --- | --- |
| `electronicContacts` | 電子接点の有無 |
| `autofocus` | オートフォーカス対応の有無 |
| `cameraControlledAperture` | カメラからの絞り制御に対応するか |
| `metadataTransmission` | 撮影メタデータを伝達するか。伝達する場合はExif、Cooke /iなどの公表規格も記録 |
| `lensStabilizationCommunication` | レンズ内手ぶれ補正と通信するか |
| `manualFocusAssistance` | マニュアルフォーカス補助と連携するか |
| `lensPowerTransmission` | カメラ側からレンズへ電力を供給するか |
| `recordingTriggerTransmission` | レンズ側の録画操作をカメラへ伝達するか |
| `electronicServices` | 公開済みファームウェア更新の有無と、更新、設定、制御に使う接続方式 |

マウントアダプター FTZ IIを例に、電子機能の記録方法を説明します。

参照元：`data/records/adapters/nikon/mount-adapter-ftz-ii.json`

```json
{
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
  "electronicServices": null
}
```

`true`は対応を確認できた状態、`false`は対応しないことを確認できた状態です。
`metadataTransmission.standards`は、伝達を確認できても規格を特定できない場合に`null`になります。
`lensPowerTransmission: null`のような項目内の`null`は、その機能への対応を採用できる公開情報で確認できない状態です。
`electronics`全体が`null`の場合は、電子機能に関する情報をまとめて確認できない状態です。
`electronicServices`は電子接点を介する機能と分けており、USB端子やドックなどを使うファームウェア更新も記録できます。
値の状態の使い分けは[値の読み方](value-rules.md#value-states)を参照してください。

## 変換光学系と付加機構（`conversionOptics`、`mechanisms`）

`conversionOptics`には、変換に使う内蔵光学系の有無と、焦点距離や開放値への影響、光学構成、対応できる像円などを記録します。
`mechanisms`には、アダプターが備える付加機構を種類ごとのオブジェクトとして記録します。
シフト、ティルト、回転の可動量は、対応する機構の`movements`にまとめます。

| 項目 | 記録する情報 |
| --- | --- |
| `conversionOptics.present` | マウント変換に関わる内蔵光学系の有無 |
| `conversionOptics.focalLengthMultiplier` | 内蔵光学系による焦点距離の倍率 |
| `conversionOptics.apertureChange` | 明るくなるか暗くなるか、変化する段数、公表された段数が正確値、概算値、指定値未満のどれか |
| `conversionOptics.opticalConstruction` | 内蔵光学系の群数と枚数 |
| `conversionOptics.specialElements` | 特殊光学素子の種類、公式名称、枚数 |
| `conversionOptics.coatings` | コーティングの種類、公式名称、適用先 |
| `conversionOptics.supportedImageCircleDiameterMm` | 対応する像円径の値または範囲（mm） |
| `conversionOptics.maximumSupportedAperture` | 対応レンズについて公表された最も明るいF値またはT値 |
| `mechanisms[].type` | 絞りリング、ドロップインフィルター、フランジバック調整、ヘリコイド、シフト、ティルト、回転などの種類 |
| `mechanisms[].officialName` | メーカーが安定して使う機構名。確認できる場合だけ記録 |
| `mechanisms[].movements` | シフト量、ティルト角、回転範囲。可動機構以外では省略 |
| `mechanisms[].conditions` | 機構が成立するバリエーションなどの条件 |

=== "光学系と付加機構なし"

    マウントアダプター FTZ IIを例に、内蔵光学系と付加機構がない場合の記録方法を説明します。

    参照元：`data/records/adapters/nikon/mount-adapter-ftz-ii.json`

    ```json
    {
      "conversionOptics": {
        "present": false
      },
      "mechanisms": []
    }
    ```

=== "光学系と付加機構あり"

    Magic Shift Converter (MSC)を例に、内蔵光学系と付加機構がある場合の記録方法を説明します。

    参照元：`data/records/adapters/laowa/laowa-magic-shift-converter-z.json`

    ```json
    {
      "conversionOptics": {
        "present": true,
        "focalLengthMultiplier": 1.4,
        "apertureChange": {
          "direction": "darker",
          "stops": 1,
          "relation": "exact"
        },
        "opticalConstruction": {
          "groups": 4,
          "elements": 5
        },
        "specialElements": null,
        "coatings": null,
        "supportedImageCircleDiameterMm": null,
        "maximumSupportedAperture": null
      },
      "mechanisms": [
        {
          "type": "shift",
          "conditions": {},
          "movements": {
            "shiftMeasurements": [
              {
                "maximumFromNeutralMm": 10,
                "totalRangeMm": null,
                "directionality": null,
                "conditions": {}
              }
            ]
          }
        },
        {
          "type": "rotation",
          "movements": {
            "rotationMeasurements": [
              {
                "scope": "movement-assembly",
                "maximumFromNeutralDegrees": null,
                "totalRangeDegrees": 360,
                "directionality": null,
                "conditions": {}
              }
            ]
          },
          "conditions": {}
        }
      ]
    }
    ```

    この例では、焦点距離を1.4倍にし、開放値を正確に1段暗くする4群5枚の光学系と、シフト機構を記録しています。
    シフト量は中立位置から片側へ10 mm、可動部の回転範囲は360°です。
    特殊光学素子などの`null`は、内蔵光学系自体は確認できたものの、その項目を採用できる公開情報で確認できない状態です。

`apertureChange.direction`には`brighter`、`darker`、`unchanged`を使います。
`relation`には`exact`、`approximately`、`less-than`を使い、「約1段」や「1段未満」を数値と分けて保持します。
`conversionOptics.present: false`の場合は、`present`以外の光学仕様を記録しません。
`conversionOptics: null`は、内蔵光学系の有無を確認できない状態です。
`conversionOptics.present: true`の場合は、7項目すべてを記録し、採用できる公開情報で確認できない値を`null`にします。
`mechanisms: []`は、確認した結果、該当する付加機構がない状態です。
`mechanisms: null`は、付加機構の有無を確認できない状態です。
シフト、ティルト、回転の機構では`movements`が必須で、公称可動量を確認できない場合は`null`を記録します。
可動機構以外の要素には`movements`を記録しません。
可動量は中立位置からの最大値と全可動範囲を区別し、公表された方向性と適用条件も同じ測定値に保持します。
値の状態の使い分けは[値の読み方](value-rules.md#value-states)を参照してください。

## 外形、重量、環境保護表現、三脚取付部（`physical`）

`physical`には、採用できる公開情報で確認した寸法、重量、環境保護に関する公式表現、三脚取付部を記録します。

| 項目 | 記録する情報 |
| --- | --- |
| `dimensionMeasurements` | 最大径、幅、高さ、長さ、軸名が公表されていない寸法と、その測定条件 |
| `weightMeasurements` | グラム単位の重量、概算値かどうか、その測定条件 |
| `officialEnvironmentalProtectionClaims` | 防塵、防滴、耐候などの公式表現と適用範囲 |
| `tripodSupport` | 三脚支持部の有無、部品の種類、製品との関係、取り外し可否、三脚側の取付方式、型番、数量、適用条件 |

マウントアダプター FTZ IIを例に、寸法、重量、環境保護表現、三脚取付部の記録方法を説明します。

参照元：`data/records/adapters/nikon/mount-adapter-ftz-ii.json`

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

この例では、幅と高さが約70 mm、長さが約36 mm、重量が約125 gです。
`conditions.excludesProjections: true`は寸法が突起部を除いた値であること、空の`conditions`は重量に追加条件がないことを表します。
環境保護表現は製品全体を対象とし、防塵と防滴の2種類を記録しています。
`tripodSupport.present: false`は、三脚取付部を持たないと確認できた状態です。
三脚支持部がある場合は、三脚座と脚を別の構成部品として記録できます。
部品の存在は確認できても内訳を特定できない場合は`components: null`を使います。
構成部品の詳しいフィールドは[共通定義](reference/schemas/shared/shared-definitions.md#tripod-support)を参照してください。

## 関連ページ

- [用語集](glossary.md)：このプロジェクトで使用する用語
- [値の読み方](value-rules.md)：項目の省略、`null`、空配列、`false`の意味
- [データモデル](data-model.md)：調査結果データ、収録製品データ、配布データの関係
- [レンズと関連光学製品のフィールドリファレンス](lens-field-reference.md)：レンズ、テレコンバーター、ピンホールの項目
- [JSON Schemaリファレンス](reference/schemas/adapters/adapter-full.md)：型、必須項目、許可される値
