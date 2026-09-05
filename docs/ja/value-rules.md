# 値の読み方

収録製品データと配布データでは、値がない理由に応じて、項目の省略、`null`、空配列、`false`を使い分けます。
条件によって変わる数値、レンズFull版からレンズLight版へ残す値、URLの記録先にも、それぞれ規則があります。

掲載しているJSONは実際のファイルから説明に必要な部分を抜き出したものです。
配列を含む例では、一部の要素だけを掲載している場合があります。

## 値の状態 {#value-states}

項目の省略、`null`、空配列、`false`には、それぞれ異なる意味があります。

| 表現 | 意味 | 例 |
| --- | --- | --- |
| 項目を省略 | その製品の構造には適用されない | `productType`が`lens`の製品には`teleconverter`ブロックを記録しない |
| `null` | 項目は適用されるが、採用できる公開情報では値を確認できない | 根拠となる公開情報で型番を確認できないため`modelNumberOptions`が`null` |
| `[]` | 一覧を確認し、該当する要素がない | 機構を持たないことを確認したため`mechanisms`が空配列 |
| `false` | 否定の事実を確認済み | 変換光学系を持たないため`conversionOptics.present`が`false` |

!!! note "`officialDesignations: []`は販売中を意味しません"
    `lifecycle.officialDesignations: []`は、確認した公式な状態表記が0件であることを示します。
    現在販売中、在庫あり、入手可能であることは意味しません。

=== "項目の省略と`null`"

    NIKKOR Z 24-70mm f/2.8 S IIの`productType`は`lens`です。
    この製品には`lens`ブロックを記録し、対象外となる`teleconverter`と`pinhole`ブロックは記録しません。
    `identity.modelNumberOptions`の`null`は、根拠となる公開情報で型番を確認できないことを表します。

    参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

    ```json
    {
      "productType": "lens",
      "identity": {
        "modelNumberOptions": null
      },
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

=== "空配列と`false`"

    マウントアダプター FTZ IIの`mechanisms`は、該当する機構がないことを確認済みなので空配列です。
    `conversionOptics.present`の`false`は、変換光学系を持たないことを表します。

    参照元：`data/records/adapters/nikon/mount-adapter-ftz-ii.json`

    ```json
    {
      "conversionOptics": {
        "present": false
      },
      "mechanisms": []
    }
    ```

!!! warning "状態を表す特別な文字列は使いません"

    不明、該当なし、要素なしを表すセンチネル値として、`"unknown"`、`"none"`、`"not-applicable"`などの文字列は使いません。
    四つの状態を分けることで、値を確認できない場合と、確認した結果が空または否定だった場合を判別できます。

## 数値と条件 {#numbers-and-conditions}

焦点距離によって変わる最短撮影距離のように、数値が特定の条件と結び付く場合があります。
NIKKOR Z 24-70mm f/2.8 S IIでは、`distanceM`と、その値が当てはまる焦点距離を同じ要素に記録しています。

参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

```json
{
  "lens": {
    "focus": {
      "minimumFocusDistances": [
        {
          "distanceM": 0.24,
          "conditions": {
            "focalLength": {
              "kind": "point",
              "millimeters": 24
            }
          }
        },
        {
          "distanceM": 0.33,
          "conditions": {
            "focalLength": {
              "kind": "point",
              "millimeters": 70
            }
          }
        }
      ]
    }
  }
}
```

この例では、0.24 mは焦点距離24 mm、0.33 mは焦点距離70 mmでの最短撮影距離です。
公開された値は、丸めたり平均したりせず、条件と組み合わせたまま保持します。
複数の値から代表値や範囲を新たに作ることもありません。

ただし、度分表記や`1:n`の比率表記をスキーマの単一の10進数へ正規化する場合は、変換結果を小数第6位に丸めます。
JSON数値の末尾の0は省略し、元の表記を公表時の精度で復元できるようにします。

## レンズFull版とレンズLight版 {#lens-full-and-light}

レンズLight版は、レンズFull版にある値の一部を残した配布データです。
レンズLight版だけの値を追加したり、複数の値から新しい値を計算したりしません。

NIKKOR Z 24-70mm f/2.8 S IIの`focus`を比較すると、レンズFull版には焦点距離ごとの測定値がすべて含まれています。
レンズLight版には、最短撮影距離が最小になる要素と、最大撮影倍率が最大になる要素だけを残しています。

=== "レンズFull版"

    参照元：`dist/z-mount-lenses.full.json`

    ```json
    {
      "id": "nikkor-z-24-to-70mm-f2p8-s-ii",
      "lens": {
        "focus": {
          "minimumFocusDistances": [
            {
              "distanceM": 0.24,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 24
                }
              }
            },
            {
              "distanceM": 0.24,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 28
                }
              }
            },
            {
              "distanceM": 0.27,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 35
                }
              }
            },
            {
              "distanceM": 0.3,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 50
                }
              }
            },
            {
              "distanceM": 0.33,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 70
                }
              }
            }
          ],
          "reproductionMagnifications": [
            {
              "kind": "maximum",
              "value": 0.21,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 24
                }
              }
            },
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
          ]
        }
      }
    }
    ```

=== "レンズLight版"

    参照元：`dist/z-mount-lenses.light.json`

    ```json
    {
      "id": "nikkor-z-24-to-70mm-f2p8-s-ii",
      "lens": {
        "focus": {
          "minimumFocusDistances": [
            {
              "distanceM": 0.24,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 24
                }
              }
            },
            {
              "distanceM": 0.24,
              "conditions": {
                "focalLength": {
                  "kind": "point",
                  "millimeters": 28
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
          ]
        }
      }
    }
    ```

最短撮影距離の0.24 mは、焦点距離24 mmと28 mmの二つの条件で同じため、どちらの要素もレンズLight版に残ります。
最大撮影倍率は、最も大きい0.32の要素が残ります。
この絞り込みは`minimumFocusDistances`と`reproductionMagnifications`に限られます。
この二つ以外の配列をレンズLight版に残す場合は、レンズFull版と同じ順序と要素数を保ちます。
ただし、配列内の各要素から一部の項目を省略する場合があります。

## URLと情報源 {#urls}

製品ページと、仕様確認に使った資料では、記録する場所が異なります。

=== "製品ページ"

    `officialProductPages`には、その製品自体を紹介する公式のメインページを記録します。
    次の例では、日本向けの公式製品ページと、地域、言語、公開元を一緒に保持しています。

    参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

    ```json
    {
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

=== "調査に使った情報源"

    調査結果データの`sources`には、製品ページに加え、マニュアル、仕様書、発表、サポートページなど、判断や仕様確認に使った情報源を記録します。

    参照元：`research/results/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

    ```json
    {
      "sources": [
        {
          "url": "https://nij.nikon.com/products/lineup/nikkor/zmount/nikkor_z_24-70mm_f28_s_2/",
          "publisherRelationship": "manufacturer-or-brand",
          "sourceType": "product-page",
          "checked": [
            "identity",
            "mount",
            "physical.dimensionMeasurements",
            "physical.weightMeasurements",
            "physical.filterInterfaces",
            "lens.focalLength",
            "lens.aperture",
            "lens.coverage",
            "lens.opticalConstruction",
            "lens.focus"
          ]
        },
        {
          "url": "https://download.nikonimglib.com/archive7/NpSBN00JyCGA07ITCA437TDmBL05/Z24-70_2.8SIIRG_(En)01.pdf",
          "publisherRelationship": "manufacturer-or-brand",
          "sourceType": "manual",
          "checked": [
            "controls",
            "accessories",
            "lens.focus",
            "lens.stabilization"
          ]
        }
      ]
    }
    ```

該当する公式製品ページが残っていない場合は、`officialProductPages`を空配列にし、代わりに使った根拠を調査結果データの`sources`に残します。
URLからは追跡用のパラメーターとページ内位置を示すフラグメントを除き、同じURLを重複して記録しません。

## 関連ページ

- [データモデル](data-model.md)：調査結果データ、収録製品データ、配布データの関係
- [レンズと関連光学製品のフィールドリファレンス](lens-field-reference.md)：製品情報を記録する場所
- [マウントアダプターのフィールドリファレンス](adapter-field-reference.md)：マウントアダプターの製品情報を記録する場所
- [製品ごとの調査結果](research.md)：収録判断と情報源の記録方法
- [JSON Schemaリファレンス](reference/schemas/index.md)：型、必須項目、許可される値
