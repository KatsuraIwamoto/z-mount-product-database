# product-type-teleconverter.schema.json

`productType: "teleconverter"`の製品が持つ`teleconverter`ブロックを検証します。
対象は、独立した製品として販売され、Zマウントへ直接装着できるテレコンバーターです。

## teleconverterブロックの実例

Z TELECONVERTER TC-1.4xを例に、基本仕様と対応レンズIDを分けて示します。

=== "基本仕様"

    参照元：`data/records/lenses/nikon/z-teleconverter-tc-1p4x.json`

    参照箇所：`teleconverter`（`compatibleLensIds`を除く）

    ```json
    {
      "coverage": {
        "format": "full-frame"
      },
      "magnification": 1.4,
      "apertureLossStops": 1,
      "supportsAutofocus": true,
      "opticalConstruction": {
        "groups": 4,
        "elements": 6
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
        },
        {
          "types": [
            "surface-protective"
          ],
          "officialName": "Fluorine coat",
          "appliedTo": [
            "front-element",
            "rear-element"
          ]
        }
      ]
    }
    ```

=== "対応レンズID"

    参照元：`data/records/lenses/nikon/z-teleconverter-tc-1p4x.json`

    参照箇所：`teleconverter.compatibleLensIds`

    ```json
    {
      "compatibleLensIds": [
        "nikkor-z-70-to-180mm-f2p8",
        "nikkor-z-70-to-200mm-f2p8-vr-s",
        "nikkor-z-70-to-200mm-f2p8-vr-s-ii",
        "nikkor-z-100-to-400mm-f4p5-to-5p6-vr-s",
        "nikkor-z-180-to-600mm-f5p6-to-6p3-vr",
        "nikkor-z-400mm-f2p8-tc-vr-s",
        "nikkor-z-400mm-f4p5-vr-s",
        "nikkor-z-600mm-f4-tc-vr-s",
        "nikkor-z-600mm-f6p3-vr-s",
        "nikkor-z-800mm-f6p3-vr-s"
      ]
    }
    ```

## teleconverterブロックのフィールド

次の8フィールドはすべて必須です。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `teleconverter.coverage` | [coverage](../shared/shared-definitions.md#basic-values) | 対応する最大撮像フォーマット |
| `teleconverter.magnification` | 正数 | 焦点距離に掛ける公称倍率 |
| `teleconverter.apertureLossStops` | 0以上の数値 | 装着時に暗くなる露出段数 |
| `teleconverter.supportsAutofocus` | 真偽値または`null` | 対応レンズを装着したときのAF対応。テレコンバーター自身の駆動方式は表さない |
| `teleconverter.opticalConstruction` | [opticalConstruction](../shared/shared-definitions.md#opticalconstruction)または`null` | テレコンバーター単体の群数と枚数 |
| `teleconverter.specialElements` | [specialElement](../shared/shared-definitions.md#specialelement)[]または`null` | 特殊レンズ。固有名称がなくても`types`と枚数を記録できる。一覧を確認し、該当する要素がない場合は`[]` |
| `teleconverter.coatings` | [coating](../shared/shared-definitions.md#coating)[]または`null` | コーティング。固有名称がなくても`types`と適用先を記録できる。一覧を確認し、該当するコーティングがない場合は`[]` |
| `teleconverter.compatibleLensIds` | ID[]または`null` | メーカーが対応を示す、`lenses`名前空間内の`productType: "lens"`である収録製品のID。判明している場合は重複のない1件以上 |

`coverage`は、最大撮像フォーマットが不明な場合に`null`を使用できます。
倍率と露出低下段数は数値で表し、`1.4`や`1`のように単位を付けず記録します。

## 対応レンズIDの検証

`compatibleLensIds`の各値に対応し、`lenses`名前空間内で`productType: "lens"`である収録製品データが存在することは、リポジトリ検証で確認します。
自由記述の製品名ではなく製品IDを使うため、配布データ内の対応レンズと結び付けられます。

## 関連ページ

- [product-full](product-full.md)：共通フィールドとの組み合わせ
- [共通定義](../shared/shared-definitions.md)：撮像フォーマット、レンズ構成、特殊レンズ、コーティング
- [レンズと関連光学製品のフィールドリファレンス](../../../lens-field-reference.md)：テレコンバーターの実データの読み方

[JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/product-type-teleconverter.schema.json)
