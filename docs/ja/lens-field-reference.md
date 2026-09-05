# レンズと関連光学製品のフィールドリファレンス

このページは、レンズと関連光学製品の収録製品データと、配布データ内の製品1件に含まれる項目を確認するための参照ページです。
初めから通読する必要はなく、製品種別や項目名から必要な節を参照できます。

収録製品データ、レンズFull版、レンズLight版の関係を先に確認する場合は、[データモデル](data-model.md)を参照してください。

!!! info "レンズFull版とレンズLight版"

    レンズFull版の`products`には、各収録製品データから`$schema`を除いた内容が入ります。
    レンズLight版は、同じ製品を同じ順序で収録しながら、項目を一部に絞っています。
    値の残し方は[値の読み方](value-rules.md#lens-full-and-light)、残る項目は[レンズLight版のJSON Schemaリファレンス](reference/schemas/lenses/product-light.md)で確認できます。

掲載しているJSONは、実際の収録製品データまたは配布データから説明に必要な部分を抜き出したものです。
配列の一部だけを掲載している例もあります。
各項目の型、必須性、許可される値は[JSON Schemaリファレンス](reference/schemas/index.md)で確認してください。

マウントアダプターはデータ構造が異なるため、[マウントアダプターのフィールドリファレンス](adapter-field-reference.md)で説明しています。

## 製品種別とブロック

`productType`は製品種別を表します。
製品固有の情報は、`productType`と同じ名前のブロックに記録します。

| 製品種別 | `productType` | 製品種別ブロック | このページの例 |
| --- | --- | --- | --- |
| レンズ | `lens` | `lens` | NIKKOR Z 24-70mm f/2.8 S II |
| テレコンバーター | `teleconverter` | `teleconverter` | Z TELECONVERTER TC-2.0x |
| ピンホール | `pinhole` | `pinhole` | Lensbaby Obscura 16 |

=== "レンズ"

    NIKKOR Z 24-70mm f/2.8 S IIを例に、レンズの製品種別と製品種別ブロックの記録方法を説明します。

    参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

    ```json
    {
      "id": "nikkor-z-24-to-70mm-f2p8-s-ii",
      "productType": "lens",
      "lens": {
        "focalLength": {
          "kind": "zoom",
          "rangeMm": {
            "minimum": 24,
            "maximum": 70
          }
        }
      }
    }
    ```

=== "テレコンバーター"

    Z TELECONVERTER TC-2.0xを例に、テレコンバーターの製品種別と製品種別ブロックの記録方法を説明します。

    参照元：`data/records/lenses/nikon/z-teleconverter-tc-2p0x.json`

    ```json
    {
      "id": "z-teleconverter-tc-2p0x",
      "productType": "teleconverter",
      "teleconverter": {
        "magnification": 2
      }
    }
    ```

=== "ピンホール"

    Lensbaby Obscura 16を例に、ピンホールの製品種別と製品種別ブロックの記録方法を説明します。

    参照元：`data/records/lenses/lensbaby/lensbaby-obscura-16.json`

    ```json
    {
      "id": "lensbaby-obscura-16",
      "productType": "pinhole",
      "pinhole": {
        "focalLength": {
          "kind": "fixed",
          "millimeters": 16
        }
      }
    }
    ```

各製品には、`lens`、`teleconverter`、`pinhole`のうち、`productType`に対応するブロックだけが入ります。

## 共通項目

製品種別にかかわらず、識別情報、公開情報、マウント、外形、操作部、付属品などは同じ位置に記録します。

| 項目 | 記録する情報 |
| --- | --- |
| `id` | 製品を識別するためのID |
| `productType` | 製品種別と、使用する製品種別ブロック |
| `identity` | メーカーID、ブランドID、公式製品名、公式型番、公式な別名、同一製品内のバリエーション |
| `lifecycle` | 公式な発売発表日と、メーカーまたはブランドが公式に示す旧製品、販売終了、生産終了などの状態表記 |
| `officialProductPages` | 製品自体を紹介する公式のメインページと、その地域、言語、公開元 |
| `mount` | マウントシステム、取付方式、電子接点、製品に付属するか専用として示されたZマウント用アダプター |
| `electronicServices` | ファームウェア更新の公開有無と、更新、設定、制御に使う接続方式 |
| `physical` | 寸法、重量、防塵・防滴などに関する公式表現、フィルター取付部、三脚取付部、ズームやフォーカスによる外形変化 |
| `controls` | フォーカスリング、ボタン、スイッチなどの操作部 |
| `accessories` | フード、キャップ、ケースなどの付属品や対応品 |

### 識別情報と公開情報（`identity`、`lifecycle`、`officialProductPages`）

NIKKOR Z 24-70mm f/2.8 S IIを例に、識別情報、発売発表日、公式製品ページの記録方法を説明します。

参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "id": "nikkor-z-24-to-70mm-f2p8-s-ii",
  "productType": "lens",
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
  },
  "officialProductPages": [
    {
      "url": "https://nij.nikon.com/products/lineup/nikkor/zmount/nikkor_z_24-70mm_f28_s_2/",
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
この例では、`nikon`がNikon、`nikkor`がNIKKORを表します。
配布用JSONでは、表示名をルートの`referenceData`から取得できます。
`identity.productName`は、公式表記の製品名を保持します。

`lifecycle.announcementDate`は、製品の公式な発売発表日です。
開発発表日で代用しません。
`lifecycle.officialDesignations: []`は、確認した公式な状態表記が0件であることを示します。
現在販売中、在庫あり、入手可能であることは意味しません。
公式製品ページが削除されたことだけを理由に、販売終了とは判断しません。

`officialProductPages`に含めるページと、調査に使った情報源の違いは[値の読み方](value-rules.md#urls)で説明しています。

### マウント（`mount`）

NIKKOR Z 24-70mm f/2.8 S IIを例に、製品のマウントと電子接点の記録方法を説明します。

参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "mount": {
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
}
```

`systemId`には、マウントシステムレジストリで定義されたIDを記録します。
この例では、固定式のNikon Zマウントと電子接点を備えることを`replaceability`と`electronicContacts`で表します。
この例の`mount-owner`は、製品のメーカーがNikon Zマウントの提供者でもあることを表します。

#### `mount.adapter`に記録するアダプター

`mount.adapter`には、製品に同梱されるZマウント用アダプターを記録します。
そのレンズ、またはメーカーが公式に示した製品シリーズ専用のZマウント用アダプターも対象です。
これはレンズと関連光学製品の収録製品データに含まれる装着情報であり、マウントアダプターの収録製品データではありません。
FTZのような幅広いレンズに対応するアダプターは、`mount.adapter`には記録しません。

SZX SUPER TELE 400mm F8 Reflex MFを例に、製品に同梱されるZマウント用アダプターの記録方法を説明します。

参照元：`data/records/lenses/tokina/tokina-szx-super-tele-400mm-f8-reflex-mf.json`

```json
{
  "mount": {
    "adapter": {
      "relationship": "supplied",
      "dedicatedToProduct": null,
      "nativeMountSystemId": "t-mount",
      "name": "Tokina Mount Adapter TA-016 for Nikon Z",
      "modelNumberOptions": [
        "TA-016",
        "TA-0016",
        "SZX-TA0016"
      ]
    }
  }
}
```

この例では、Tokina Mount Adapter TA-016 for Nikon Zが同梱されることを`relationship: "supplied"`で表します。

### ファームウェア更新と接続（`electronicServices`）

NIKKOR Z 24-70mm f/2.8 S IIを例に、製品向けファームウェア更新の公開有無と、更新、設定、制御に使う接続方式の記録方法を説明します。

参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "electronicServices": {
    "hasPublishedFirmwareUpdate": null,
    "connections": null
  }
}
```

`hasPublishedFirmwareUpdate: null`は、製品向けファームウェア更新の公開有無を採用できる公開情報で確認できない状態です。
`connections: null`は、接続方式を採用できる公開情報で確認できない状態です。
`electronicServices`はマウントの電子接点とは別の項目です。電子接点がない製品でも、独立したUSB接続やドックなどが公式に公表されている場合は記録できます。

### 外形（`physical`）

NIKKOR Z 24-70mm f/2.8 S IIを例に、寸法、重量、フィルター取付部、鏡筒の全長変化の記録方法を説明します。

参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "physical": {
    "dimensionMeasurements": [
      {
        "maximumDiameterMm": 84,
        "lengthMm": 142,
        "conditions": {}
      }
    ],
    "weightMeasurements": [
      {
        "grams": 675,
        "conditions": {
          "attachedComponents": []
        }
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
    "filterInterfaces": [
      {
        "type": "front-thread",
        "diameterMm": 77,
        "host": {
          "kind": "product"
        }
      }
    ],
    "tripodSupport": {
      "present": false
    },
    "externalLengthDuringZoom": "constant",
    "externalLengthDuringFocus": "constant",
    "isRetractableForStorage": false
  }
}
```

この例では、最大径84 mm、長さ142 mmです。
重量は675 g、前面フィルター径は77 mmです。
`officialEnvironmentalProtectionClaims`には、公式に示された製品全体の防塵・防滴性能を記録しています。
`externalLengthDuringZoom`と`externalLengthDuringFocus`の`constant`は、ズーム操作やフォーカス操作で鏡筒の全長が変わらないことを表します。
`tripodSupport.present: false`は三脚取付部がなく、`isRetractableForStorage: false`は使用前に繰り出す収納機構がないことを表します。
三脚支持部がある場合は、三脚座、脚、取付ねじなどの構成部品と、製品との関係、取り外し可否、取付方式を`tripodSupport.components`にまとめます。
測定条件は[数値と条件](value-rules.md#numbers-and-conditions)、`null`などの値の状態は[値の状態](value-rules.md#value-states)で説明しています。

### 操作部と付属品（`controls`、`accessories`）

NIKKOR Z 24-70mm f/2.8 S IIを例に、製品本体の操作部と付属品の記録方法を説明します。

参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "controls": [
    {
      "type": "focus-ring",
      "quantity": 1
    }
  ],
  "accessories": {
    "lensHoods": [
      {
        "relationship": "supplied",
        "modelNumberOptions": [
          "HB-117"
        ],
        "quantity": 1
      }
    ]
  }
}
```

## `lens`ブロック

`lens`ブロックには、レンズの光学仕様、フォーカス、手ぶれ補正、用途別の特徴を記録します。
写真用レンズとシネマ用レンズは同じ`lens`ブロックを使い、必要な項目の値や組み合わせで違いを表します。

| 項目 | 記録する情報 |
| --- | --- |
| `focalLength` | 単焦点、ズーム範囲、複数の離散的な焦点距離 |
| `aperture` | F値またはT値、絞り羽根、絞りの制御方式 |
| `anglesOfView` | 撮像フォーマット、方向、測定条件ごとの画角 |
| `coverage` | 対応する最大撮像フォーマット |
| `imageCircleDiameters` | 公開されているイメージサークル径と測定条件 |
| `opticalConstruction` | レンズの群数と枚数 |
| `specialElements` | 特殊レンズの種類、公式名称、枚数 |
| `coatings` | コーティングの種類、公式名称、適用箇所 |
| `focus` | オートフォーカス、マニュアルフォーカス、フォーカス方式、最短撮影距離、最大撮影倍率、フォーカス挙動に関する公式説明 |
| `zoom` | ズームの駆動方式と、インターナルズームなどの光学ズーム方式。ズームレンズだけに記録 |
| `stabilization` | 手ぶれ補正の有無、公開されている補正段数、公式名称 |
| `specialized` | マクロ、魚眼、シネマ、アナモルフィックなど、組み合わせ可能な特徴 |

数値に付随する`conditions`は[値の読み方](value-rules.md#numbers-and-conditions)で説明しています。
レンズLight版に残すフォーカス情報は[レンズFull版とレンズLight版](value-rules.md#lens-full-and-light)で確認できます。

!!! info "例の読み方"

    各JSONは、一つの収録製品データから個別に抜き出しています。
    複数のレンズの値を一つのJSONに組み合わせたものではありません。
    NIKKOR Z 24-70mm f/2.8 S IIを基本例とし、その例だけでは示せない項目に限って別のレンズを使います。

### 焦点距離と絞り（`focalLength`、`aperture`）

NIKKOR Z 24-70mm f/2.8 S IIを例に、ズームレンズの焦点距離と絞りの記録方法を説明します。

参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "lens": {
    "focalLength": {
      "kind": "zoom",
      "rangeMm": {
        "minimum": 24,
        "maximum": 70
      }
    },
    "aperture": {
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
  }
}
```

この例では、焦点距離24–70 mmの範囲を`focalLength.rangeMm`に記録します。
ニコンがf/2.8と表記する開放F値は、`maximumAperture[].value: 2.8`として数値で記録します。
同じように、最小絞りのf/22は`minimumAperture[].value: 22`です。

### 最大撮像フォーマットと画角（`coverage`、`anglesOfView`）

NIKKOR Z 24-70mm f/2.8 S IIを例に、対応する最大撮像フォーマットと焦点距離ごとの画角の記録方法を説明します。

参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "lens": {
    "coverage": {
      "format": "full-frame"
    },
    "anglesOfView": [
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
    ]
  }
}
```

この例では、広角端24 mmにおける対角線画角84度を`anglesOfView`に記録しています。

### レンズ構成（`opticalConstruction`、`specialElements`、`coatings`）

NIKKOR Z 24-70mm f/2.8 S IIを例に、レンズの群数・枚数、特殊レンズ、コーティングの記録方法を説明します。

参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "lens": {
    "opticalConstruction": {
      "groups": 10,
      "elements": 14
    },
    "specialElements": [
      {
        "types": [
          "low-dispersion"
        ],
        "officialName": "ED glass",
        "quantity": 2
      }
    ],
    "coatings": [
      {
        "types": [
          "anti-reflective"
        ],
        "officialName": "Meso Amorphous Coat",
        "appliedTo": null
      }
    ]
  }
}
```

### フォーカスとズーム（`focus`、`zoom`）

NIKKOR Z 24-70mm f/2.8 S IIを例に、オートフォーカス（AF）、マニュアルフォーカス（MF）、フォーカス方式、最短撮影距離、最大撮影倍率の記録方法を説明します。

参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "lens": {
    "focus": {
      "autofocus": {
        "present": true,
        "motors": [
          {
            "type": "voice-coil-motor",
            "quantity": null,
            "officialName": "Silky Swift VCM"
          }
        ]
      },
      "manualFocus": {
        "present": true,
        "mechanism": null
      },
      "opticalFocusingSystems": [
        {
          "type": "internal-focusing",
          "officialName": "Internal Focusing system"
        },
        {
          "type": "multiple-group-focusing",
          "officialName": "Multi-focusing system"
        }
      ],
      "minimumFocusDistances": [
        {
          "distanceM": 0.24,
          "conditions": {
            "focalLength": {
              "kind": "point",
              "millimeters": 24
            }
          }
        }
      ],
      "reproductionMagnifications": [
        {
          "kind": "maximum",
          "value": 0.32,
          "conditions": {
            "focalLength": {
              "kind": "point",
              "millimeters": 70
            }
          }
        }
      ],
      "officialFocusBehaviorClaims": [
        {
          "type": "focus-breathing-suppressed",
          "conditions": {}
        }
      ]
    },
    "zoom": {
      "drive": null,
      "opticalZoomingSystems": null
    }
  }
}
```

`opticalFocusingSystems`には、メーカーが公表しているフォーカス方式を記録します。
最短撮影距離と最大撮影倍率は、`conditions`でそれぞれの焦点距離に対応付けます。
`officialFocusBehaviorClaims`には、フォーカスブリージングを抑えるという公式説明を記録しています。
ズームレンズでは`zoom`を必ず記録し、`drive`には手動、電動、または両対応の駆動方式を記録します。
`opticalZoomingSystems`には、メーカーが公表したインターナルズーム方式などを記録します。
この例の`null`は、どちらも採用できる公開情報で確認できない状態です。
単焦点レンズには`zoom`を記録しません。

### 手ぶれ補正（`stabilization`）

`stabilization`では、レンズ内手ぶれ補正の有無と、公開されている補正段数や公式名称を記録します。
搭載の有無を確認できる場合は、`present`に`true`または`false`を記録します。

=== "搭載あり"

    NIKKOR Z 400mm f/2.8 TC VR Sを例に、レンズ内手ぶれ補正の搭載を確認できた場合の記録方法を説明します。

    参照元：`data/records/lenses/nikkor/nikkor-z-400mm-f2p8-tc-vr-s.json`

    ```json
    {
      "lens": {
        "stabilization": {
          "present": true,
          "ratings": [
            {
              "stops": 5.5,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 400
                },
                "standard": "CIPA",
                "mode": "Normal",
                "imageFormat": "full-frame"
              }
            }
          ],
          "officialName": "Vibration Reduction"
        }
      }
    }
    ```

    `present: true`は、レンズ内手ぶれ補正の搭載を確認できた状態です。
    `ratings`には、焦点距離、測定規格、補正モード、測定時の撮像範囲を条件として公称補正段数を記録します。

=== "搭載なし"

    採用できる公開情報からレンズ内手ぶれ補正を搭載しないことを確認できた場合は、次のように記録します。

    ```json
    {
      "lens": {
        "stabilization": {
          "present": false
        }
      }
    }
    ```

    `present: false`は、採用できる公開情報からレンズ内手ぶれ補正を搭載しないと確認できた状態です。

採用できる公開情報から搭載の有無を確認できない場合に限り、`stabilization`を`null`にします。
値の状態の使い分けは[値の読み方](value-rules.md#value-states)を参照してください。

### シネマ用レンズの仕様

LAOWA Argus 33mm T1 S35 Cineを例に、T値、イメージサークル径、シネマ用レンズとしての特徴の記録方法を説明します。

参照元：`data/records/lenses/laowa/laowa-argus-33mm-t1-s35-cine.json`

```json
{
  "lens": {
    "aperture": {
      "fNumber": null,
      "tNumber": {
        "maximumAperture": [
          {
            "value": 1,
            "conditions": {}
          }
        ],
        "minimumAperture": [
          {
            "value": 11,
            "conditions": {}
          }
        ],
        "effective": null
      },
      "diaphragm": {
        "present": true,
        "bladeCount": 9,
        "bladeShape": null
      },
      "controlMechanism": "mechanical"
    },
    "coverage": {
      "format": "super-35"
    },
    "imageCircleDiameters": [
      {
        "diameterMm": 31.5,
        "conditions": {}
      }
    ],
    "specialized": {
      "cinema": {}
    }
  }
}
```

### 組み合わせ可能な特徴（`specialized`）

`specialized`は、製品に該当する特徴をキーとして並べるブロックです。
一つのレンズに複数のキーを組み合わせられるため、レンズを一種類だけに分類するものではありません。
該当する特徴がない製品では、`specialized`を空のオブジェクト（`{}`）にします。

| キー | 表す特徴 | レンズFull版に記録する詳細 |
| --- | --- | --- |
| `cinema` | シネマ用レンズとして公式に位置付けられた製品 | キーの存在だけで表す |
| `anamorphic` | アナモルフィックレンズ | スクイーズ倍率 |
| `fisheye` | 魚眼レンズ | 円周魚眼または対角魚眼として得られる像 |
| `macro` | マクロレンズ | レンズ先端などから被写体までのワーキングディスタンス |
| `reflex` | 反射光学系を使うレンズ | キーの存在だけで表す |
| `movements` | ティルト、シフト、回転が可能なレンズ | 各機構の可動範囲 |
| `probe` | プローブレンズ | 視方向と内蔵照明 |
| `builtInTeleconverter` | テレコンバーターを内蔵するレンズ | 倍率、レンズ構成、使用時の仕様 |

#### レンズFull版とレンズLight版の違い

LAOWA 24mm F14 2x Macro Probeを例に、複数の特徴と、レンズFull版およびレンズLight版での残し方を説明します。

=== "レンズFull版"

    参照元：`dist/z-mount-lenses.full.json`

    ```json
    {
      "id": "laowa-24mm-f14-2x-macro-probe",
      "lens": {
        "specialized": {
          "cinema": {},
          "macro": {
            "workingDistances": [
              {
                "distanceM": 0.02,
                "conditions": {}
              }
            ]
          },
          "probe": {
            "viewConfigurations": [
              {
                "directionDegrees": 0,
                "relationship": "integrated"
              }
            ],
            "integratedLights": [
              {
                "type": "led",
                "location": "lens tip",
                "quantity": 1
              }
            ]
          }
        }
      }
    }
    ```

    `cinema`は、キーの存在自体が特徴を表すため空のオブジェクトです。
    `macro`には0.02 mのワーキングディスタンス、`probe`には視方向とレンズ先端の内蔵LEDを記録しています。

=== "レンズLight版"

    参照元：`dist/z-mount-lenses.light.json`

    ```json
    {
      "id": "laowa-24mm-f14-2x-macro-probe",
      "lens": {
        "specialized": {
          "cinema": {},
          "macro": {},
          "probe": {}
        }
      }
    }
    ```

    レンズLight版では、三つの特徴があることだけを残します。
    ワーキングディスタンス、視方向、内蔵照明の詳細は含みません。

#### 内蔵テレコンバーターの使用時仕様

NIKKOR Z 400mm f/2.8 TC VR Sを例に、内蔵テレコンバーターの通常時と使用時の仕様をどこに記録するか説明します。
通常時の焦点距離と開放F値は`lens`直下に置きます。
テレコンバーター使用時の値は`builtInTeleconverter.engagedSpecifications`に記録します。

参照元：`data/records/lenses/nikkor/nikkor-z-400mm-f2p8-tc-vr-s.json`

```json
{
  "id": "nikkor-z-400mm-f2p8-tc-vr-s",
  "lens": {
    "focalLength": {
      "kind": "prime",
      "millimeters": 400
    },
    "aperture": {
      "fNumber": {
        "maximumAperture": [
          {
            "value": 2.8,
            "conditions": {}
          }
        ]
      }
    },
    "specialized": {
      "builtInTeleconverter": {
        "magnification": 1.4,
        "unitOpticalConstruction": {
          "groups": 4,
          "elements": 7
        },
        "engagedSpecifications": {
          "focalLength": {
            "kind": "prime",
            "millimeters": 560
          },
          "aperture": {
            "fNumber": {
              "maximumAperture": [
                {
                  "value": 4,
                  "conditions": {}
                }
              ]
            }
          }
        }
      }
    }
  }
}
```

この例では、通常時は焦点距離400 mm、開放F値f/2.8で、内蔵テレコンバーター使用時は焦点距離560 mm、開放F値f/4です。
独立した製品として販売されるテレコンバーターは、`specialized`ではなく`productType: "teleconverter"`で記録します。
各キーの詳細な型と許可される値は、[レンズのJSON Schemaリファレンス](reference/schemas/lenses/product-type-lens.md#specialized)を参照してください。

## `teleconverter`ブロック

`teleconverter`ブロックには、倍率、露出への影響、光学仕様、対応レンズを記録します。

| 項目 | 記録する情報 |
| --- | --- |
| `coverage` | 対応する最大撮像フォーマット |
| `magnification` | 焦点距離の倍率 |
| `apertureLossStops` | 取り付けによって暗くなる段数 |
| `supportsAutofocus` | 対応レンズ装着時のオートフォーカス対応の有無 |
| `opticalConstruction` | テレコンバーター内部の群数と枚数 |
| `specialElements` | 特殊レンズの種類、公式名称、枚数 |
| `coatings` | コーティングの種類、公式名称、適用箇所 |
| `compatibleLensIds` | 対応する収録製品のID |

Z TELECONVERTER TC-2.0xを例に、倍率、露出への影響、光学仕様、対応レンズの記録方法を説明します。

参照元：`data/records/lenses/nikon/z-teleconverter-tc-2p0x.json`

```json
{
  "teleconverter": {
    "coverage": {
      "format": "full-frame"
    },
    "magnification": 2,
    "apertureLossStops": 2,
    "supportsAutofocus": true,
    "opticalConstruction": {
      "groups": 5,
      "elements": 8
    },
    "specialElements": [
      {
        "types": [
          "aspherical"
        ],
        "officialName": "Aspherical lens",
        "quantity": 1
      }
    ],
    "coatings": [
      {
        "types": [
          "anti-reflective"
        ],
        "officialName": "Nikon Super Integrated Coating",
        "appliedTo": null
      }
    ],
    "compatibleLensIds": [
      "nikkor-z-70-to-180mm-f2p8",
      "nikkor-z-70-to-200mm-f2p8-vr-s"
    ]
  }
}
```

掲載した`compatibleLensIds`は、実際の配列から2件だけを抜き出しています。
対応レンズは、収録製品データの`id`で参照します。

## `pinhole`ブロック

`pinhole`ブロックには、対応する最大撮像フォーマット、焦点距離、撮像方式、画角を記録します。

| 項目 | 記録する情報 |
| --- | --- |
| `coverage` | 対応する最大撮像フォーマット |
| `focalLength` | 焦点距離 |
| `imagingModes` | 製品が備える撮像方式と、そのF値や開口径 |
| `anglesOfView` | 公開されている画角 |

Lensbaby Obscura 16を例に、一つの製品が複数の撮像方式を備える場合の記録方法を説明します。

参照元：`data/records/lenses/lensbaby/lensbaby-obscura-16.json`

```json
{
  "pinhole": {
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
}
```

この例の`zone-plate`（ゾーンプレート）、`pinhole-sieve`（ピンホールシーブ）、`pinhole`（ピンホール）は、それぞれLensbaby Obscura 16が備える撮像方式です。
`opening`と`anglesOfView`の`null`は、該当する情報を採用できる公開情報で確認できないことを表します。

## 関連ページ

- [用語集](glossary.md)：このプロジェクトで使用する用語
- [値の読み方](value-rules.md)：`null`、空配列、`false`、条件付き数値の意味
- [データモデル](data-model.md)：調査結果データ、収録製品データ、配布データの関係
- [マウントアダプターのフィールドリファレンス](adapter-field-reference.md)：マウントアダプターの項目
- [JSON Schemaリファレンス](reference/schemas/index.md)：型、必須項目、許可される値
