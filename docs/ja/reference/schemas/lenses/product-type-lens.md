# product-type-lens.schema.json

`productType: "lens"`の製品が持つ`lens`ブロックを検証します。
一般的な光学仕様に、シネマ、アナモルフィック、マクロなどの組み合わせ可能な特徴を追加できる構造です。

## lensブロックの構成

`imageCircleDiameters`と`zoom`を除く次のトップレベルのフィールドは、すべて必須です。
必須フィールドでも、採用できる公開情報で確認できない場合に`null`を使用できるものがあります。
`zoom`は`focalLength.kind`が`zoom`の場合に必須で、`prime`の場合は記録できません。

| パス | 内容 |
| --- | --- |
| `lens.focalLength` | 焦点距離 |
| `lens.aperture` | F値、T値、絞り機構、制御方式 |
| `lens.anglesOfView` | 撮像フォーマット、方向、測定条件ごとの画角 |
| `lens.coverage` | 最大撮像フォーマット |
| `lens.imageCircleDiameters` | 公表されている場合だけ追加するイメージサークル径 |
| `lens.opticalConstruction` | レンズ全体の群数と枚数 |
| `lens.specialElements` | 特殊レンズ |
| `lens.coatings` | コーティング |
| `lens.focus` | AF、MF、フォーカシング方式、撮影距離、撮影倍率 |
| `lens.zoom` | ズームの駆動方式と光学ズーム方式 |
| `lens.stabilization` | レンズ内手ぶれ補正 |
| `lens.specialized` | 組み合わせ可能な特徴 |

## 一般的なレンズ仕様の実例

NIKKOR Z 24-70mm f/2.8 S IIを例に、焦点距離、絞り、フォーカス、手ぶれ補正の記録方法を示します。
`specialized`の節は、この製品に含まれないものも含め、スキーマが許可する特徴を一覧にしたものです。

参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

=== "焦点距離と絞り"

    参照箇所：`lens.focalLength`、`lens.aperture`

    ```json
    {
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
    ```

    JSONでは、公式表記のf/2.8を数値`2.8`として記録します。

=== "フォーカス、ズーム、手ぶれ補正"

    参照箇所：`lens.focus.autofocus`、`lens.focus.manualFocus`、`lens.zoom`、`lens.stabilization`

    ```json
    {
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
        }
      },
      "zoom": {
        "drive": null,
        "opticalZoomingSystems": null
      },
      "stabilization": {
        "present": false
      }
    }
    ```

    この製品はAFとMFに対応し、レンズ内手ぶれ補正は搭載していません。
    ズームの駆動方式と光学ズーム方式は、採用できる公開情報で確認できないため`null`です。

## 光学仕様

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `lens.focalLength` | [focalLength](../shared/shared-definitions.md#focal-length-and-conditions)または`null` | 単焦点、ズーム範囲、交換部品ごとの焦点距離構成 |
| `lens.anglesOfView` | [angleOfView](../shared/shared-definitions.md#optical-values)[]または`null` | 撮像フォーマット、方向、焦点距離条件ごとの公式画角。判明している場合は1件以上 |
| `lens.coverage` | [coverage](../shared/shared-definitions.md#basic-values) | レンズがカバーする最大撮像フォーマット |
| `lens.imageCircleDiameters` | measurement[]または`null` | 公式に公表されたイメージサークル径。フィールド自体は任意で、判明している場合は1件以上 |
| `lens.imageCircleDiameters[].diameterMm` | 正数 | イメージサークル径mm |
| `lens.imageCircleDiameters[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | 焦点距離、撮影距離などの測定条件 |
| `lens.opticalConstruction` | [opticalConstruction](../shared/shared-definitions.md#opticalconstruction)または`null` | レンズ全体の群数と枚数 |
| `lens.specialElements` | [specialElement](../shared/shared-definitions.md#specialelement)[]または`null` | 特殊レンズ。固有名称がなくても`types`と枚数を記録できる。一覧を確認し、該当する要素がない場合は`[]` |
| `lens.coatings` | [coating](../shared/shared-definitions.md#coating)[]または`null` | コーティング。固有名称がなくても`types`と適用先を記録できる。一覧を確認し、該当するコーティングがない場合は`[]` |

## 絞り {#aperture}

`lens.aperture`は、F値、T値、絞り機構、制御方式を分けて記録します。
`fNumber`、`diaphragm`、`controlMechanism`は必須で、T値を公表する製品だけが`tNumber`を持ちます。

### F値とT値

`fNumber`はオブジェクトまたは`null`です。
オブジェクトの場合は`maximumAperture`、`minimumAperture`、`effective`をすべて持ちます。
`tNumber`も同じ構造を使いますが、フィールド自体は任意です。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `lens.aperture.fNumber.maximumAperture` | F値測定[]または`null` | 公称開放F値。判明している場合は1件以上 |
| `lens.aperture.fNumber.minimumAperture` | F値測定[]または`null` | 公称最小絞りF値。判明している場合は1件以上 |
| `lens.aperture.fNumber.effective` | オブジェクトまたは`null` | 近接撮影などで公表される実効F値 |
| `lens.aperture.fNumber.effective.maximumAperture` | F値測定[]または`null` | 条件付きの実効開放F値 |
| `lens.aperture.fNumber.effective.minimumAperture` | F値測定[]または`null` | 条件付きの実効最小絞りF値 |
| `lens.aperture.tNumber.maximumAperture` | T値測定[]または`null` | 公称開放T値 |
| `lens.aperture.tNumber.minimumAperture` | T値測定[]または`null` | 公称最小絞りT値 |
| `lens.aperture.tNumber.effective` | オブジェクトまたは`null` | 条件付きの実効T値。オブジェクトの場合は`maximumAperture`と`minimumAperture`が必須 |

各測定要素の`value`と`conditions`は、[F値とT値](../shared/shared-definitions.md#aperture-measurements)を参照してください。

### 絞り機構

| `lens.aperture.diaphragm` | 許可される構造 |
| --- | --- |
| `null` | 可動絞りの有無を採用できる公開情報で確認できない |
| `{ "present": false }` | 可動絞りを持たない |
| `{ "present": true, ... }` | `bladeCount`と`bladeShape`が必須 |

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `lens.aperture.diaphragm.present` | 真偽値 | 可動絞りの有無 |
| `lens.aperture.diaphragm.bladeCount` | 1以上の整数または`null` | 絞り羽根枚数 |
| `lens.aperture.diaphragm.bladeShape` | `rounded` / `straight` / `other` / `null` | 絞り羽根形状 |
| `lens.aperture.controlMechanism` | `mechanical` / `electronic` / `null` | カメラから絞りを駆動する方式 |

## フォーカス {#focus}

`autofocus`、`manualFocus`、`opticalFocusingSystems`、`minimumFocusDistances`、`reproductionMagnifications`、`officialFocusBehaviorClaims`は、すべて必須です。

### AFとMF

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `lens.focus.autofocus` | オブジェクトまたは`null` | AFの有無と駆動モーター |
| `lens.focus.autofocus.present` | 真偽値 | AF対応の有無 |
| `lens.focus.autofocus.motors` | motor[]または`null` | AFモーター。`present: true`の場合に必須 |
| `lens.focus.autofocus.motors[].type` | `stepping-motor` / `voice-coil-motor` / `linear-motor` / `ultrasonic-motor` / `dc-motor` / `other` | モーター方式 |
| `lens.focus.autofocus.motors[].officialName` | 文字列（省略可） | Stepping Motor (STM)、Silky Swift VCM、VXDなど、メーカーが安定して使う技術名称。`type`はブランド横断の分類、`officialName`はメーカーの公式表記を保持する |
| `lens.focus.autofocus.motors[].quantity` | 1以上の整数または`null` | モーター数。各要素で必須 |
| `lens.focus.manualFocus` | オブジェクトまたは`null` | MFの有無と操作方式 |
| `lens.focus.manualFocus.present` | 真偽値 | MF対応の有無 |
| `lens.focus.manualFocus.mechanism` | `mechanical-coupled` / `electronic-by-wire` / `null` | MF機構。`present: true`の場合に必須 |

AFとMFは、それぞれ次の3状態を使います。

| 状態 | 構造 |
| --- | --- |
| 採用できる公開情報で確認できない | `null` |
| 非対応を確認 | `{ "present": false }` |
| 対応を確認 | `{ "present": true, ... }` |

### フォーカシング方式と撮影値

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `lens.focus.opticalFocusingSystems` | system[]または`null` | 光学群のフォーカシング方式。一覧を確認し、該当する方式がない場合は`[]` |
| `lens.focus.opticalFocusingSystems[].type` | `all-element-focusing` / `front-focusing` / `internal-focusing` / `rear-focusing` / `multiple-group-focusing` / `floating` / `other` | フォーカシング方式 |
| `lens.focus.opticalFocusingSystems[].officialName` | 文字列（省略可） | Internal Focusing system、IF、Multi-focusing systemなど、メーカーが安定して使う技術名称。`type`はブランド横断の分類、`officialName`はメーカーの公式表記を保持する |
| `lens.focus.minimumFocusDistances` | [minimumFocusDistance](../shared/shared-definitions.md#focus-measurements)[]または`null` | 撮像面を基準とする最短撮影距離。判明している場合は1件以上 |
| `lens.focus.reproductionMagnifications` | [reproductionMagnification](../shared/shared-definitions.md#focus-measurements)[]または`null` | 公称撮影倍率。判明している場合は1件以上 |
| `lens.focus.officialFocusBehaviorClaims` | claim[]または`null` | メーカーが明示するフォーカスブリージング抑制やパーフォーカル性。一覧を確認し、該当する表記がない場合は`[]` |
| `lens.focus.officialFocusBehaviorClaims[].type` | `focus-breathing-suppressed` / `parfocal` | 公式表記の種類 |
| `lens.focus.officialFocusBehaviorClaims[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | 表記が成立する条件 |

## ズーム {#zoom}

ズームレンズでは`lens.zoom`が必須です。
駆動方式と光学ズーム方式を採用できる公開情報で確認できない場合も、フィールドを省略せず`null`を記録します。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `lens.zoom.drive` | `manual` / `motorized` / `manual-and-motorized` / `null` | ズームの駆動方式 |
| `lens.zoom.opticalZoomingSystems` | system[]または`null` | 公表された光学ズーム方式。確認済みで該当なしの場合は`[]` |
| `lens.zoom.opticalZoomingSystems[].type` | `internal-zooming` / `other` | 光学ズーム方式の分類 |
| `lens.zoom.opticalZoomingSystems[].officialName` | 文字列（省略可） | メーカーが安定して使う技術名称 |

単焦点レンズでは`lens.zoom`を記録しません。

## 手ぶれ補正 {#stabilization}

| `lens.stabilization` | 許可される構造 |
| --- | --- |
| `null` | レンズ内手ぶれ補正の有無を採用できる公開情報で確認できない |
| `{ "present": false }` | レンズ内手ぶれ補正を搭載していないことを確認した |
| `{ "present": true, "ratings": ... }` | 搭載を確認した。`ratings`が必須 |

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `lens.stabilization.present` | 真偽値 | レンズ内手ぶれ補正の有無 |
| `lens.stabilization.officialName` | 文字列（省略可） | VR、OS、VCなど、メーカーが安定して使う名称 |
| `lens.stabilization.ratings` | rating[]または`null` | 公称補正段数。採用できる公開情報で確認できない場合は`null` |
| `lens.stabilization.ratings[].stops` | 0以上の数値 | 公称補正効果の段数 |
| `lens.stabilization.ratings[].conditions.focalLength` | [focalLengthCondition](../shared/shared-definitions.md#focallengthcondition) | 評価した焦点距離 |
| `lens.stabilization.ratings[].conditions.imageFormat` | [imageFormat](../shared/shared-definitions.md#basic-values) | 評価に使用した撮像範囲 |
| `lens.stabilization.ratings[].conditions.cameraBodyModel` | 文字列 | 組み合わせたカメラ機種 |
| `lens.stabilization.ratings[].conditions.configuration` | `lens-only` / `lens-and-body` / `unspecified` | レンズ単体評価か、ボディとの協調評価か |
| `lens.stabilization.ratings[].conditions.standard` | 文字列 | CIPAなどの評価規格名 |
| `lens.stabilization.ratings[].conditions.standardVersion` | 文字列 | 評価規格の版または年 |
| `lens.stabilization.ratings[].conditions.mode` | 文字列 | Normal、Sportなどの評価モード |
| `lens.stabilization.ratings[].conditions.measurementAxes` | 1以上の整数 | 評価軸数 |
| `lens.stabilization.ratings[].conditions.evaluationPosition` | `center` / `center-and-peripheral` | 画面上の評価位置 |

`ratings[]`の各要素では、`stops`と`conditions`が必須です。
`conditions`内のフィールドは、公表された条件だけを記録します。

## 組み合わせ可能な特徴 {#specialized}

`lens.specialized`は必須ですが、該当する特徴がない場合は`{}`を記録します。
シネマ、アナモルフィック、マクロなど、複数の特徴を併せ持つ製品も、一つの細分類へ限定せず表現できます。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `lens.specialized.cinema` | `{}` | シネマ用途として公式に位置付けられた製品 |
| `lens.specialized.reflex` | `{}` | 反射光学系を使う製品 |
| `lens.specialized.anamorphic` | オブジェクト | アナモルフィック仕様 |
| `lens.specialized.fisheye` | オブジェクト | 魚眼像の仕様 |
| `lens.specialized.macro` | オブジェクト | マクロ仕様 |
| `lens.specialized.movements` | オブジェクト | ティルト、シフト、回転機構 |
| `lens.specialized.probe` | オブジェクト | プローブレンズの視方向と内蔵照明 |
| `lens.specialized.builtInTeleconverter` | オブジェクト | 内蔵テレコンバーターと使用時の仕様 |

### アナモルフィック、魚眼、マクロ

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `lens.specialized.anamorphic.squeezeRatios` | measurement[]または`null` | 公称スクイーズ倍率。判明している場合は1件以上 |
| `lens.specialized.anamorphic.squeezeRatios[].value` | 正数 | スクイーズ倍率 |
| `lens.specialized.anamorphic.squeezeRatios[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | 倍率が成立する条件 |
| `lens.specialized.fisheye.imageTypes` | measurement[]または`null` | 公称の魚眼像形式。判明している場合は1件以上 |
| `lens.specialized.fisheye.imageTypes[].type` | `circular` / `diagonal` | 円周魚眼または対角魚眼 |
| `lens.specialized.fisheye.imageTypes[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | 撮像フォーマットや焦点距離などの条件 |
| `lens.specialized.macro.workingDistances` | [workingDistance](../shared/shared-definitions.md#focus-measurements)[]または`null` | レンズ先端などから被写体までの距離。判明している場合は1件以上 |

### アオリ機構

`lens.specialized.movements`は[共通の`movements`定義](../shared/shared-definitions.md#movements)を使用し、`tiltMeasurements`、`shiftMeasurements`、`rotationMeasurements`のうち少なくとも一つを持ちます。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `lens.specialized.movements.tiltMeasurements` | measurement[]または`null` | 公称ティルト角。判明している場合は1件以上 |
| `lens.specialized.movements.tiltMeasurements[].maximumFromNeutralDegrees` | 正数または`null` | 中立位置から一方向への最大ティルト角（度） |
| `lens.specialized.movements.tiltMeasurements[].totalRangeDegrees` | 正数または`null` | 端から端までの全ティルト範囲（度） |
| `lens.specialized.movements.tiltMeasurements[].directionality` | `single-direction` / `bidirectional` / `null` | 公表された可動方向 |
| `lens.specialized.movements.tiltMeasurements[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | 適用条件 |
| `lens.specialized.movements.shiftMeasurements` | measurement[]または`null` | 公称シフト量。判明している場合は1件以上 |
| `lens.specialized.movements.shiftMeasurements[].maximumFromNeutralMm` | 正数または`null` | 中立位置から一方向への最大シフト量（mm） |
| `lens.specialized.movements.shiftMeasurements[].totalRangeMm` | 正数または`null` | 端から端までの全シフト範囲（mm） |
| `lens.specialized.movements.shiftMeasurements[].directionality` | `single-direction` / `bidirectional` / `null` | 公表された可動方向 |
| `lens.specialized.movements.shiftMeasurements[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | 適用条件 |
| `lens.specialized.movements.rotationMeasurements` | measurement[]または`null` | アオリ機構などの公称回転量 |
| `lens.specialized.movements.rotationMeasurements[].scope` | `product` / `movement-assembly` / `mount-interface` / `other` | 回転する範囲 |
| `lens.specialized.movements.rotationMeasurements[].maximumFromNeutralDegrees` | 0超360以下の数値または`null` | 中立位置から一方向への最大回転角（度） |
| `lens.specialized.movements.rotationMeasurements[].totalRangeDegrees` | 0超360以下の数値または`null` | 端から端までの全回転範囲（度） |
| `lens.specialized.movements.rotationMeasurements[].directionality` | `single-direction` / `bidirectional` / `null` | 公表された回転方向 |
| `lens.specialized.movements.rotationMeasurements[].conditions` | [specializedConditions](../shared/shared-definitions.md#focal-length-and-conditions) | 適用条件 |

### プローブ

`lens.specialized.probe`は、キーが存在することでプローブレンズを表します。
視方向や照明の情報がなくても`{}`を使用できます。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `lens.specialized.probe.viewConfigurations` | configuration[]または`null` | 公表された視方向。判明している場合は1件以上 |
| `lens.specialized.probe.viewConfigurations[].directionDegrees` | 0以上360以下の数値 | 正面を0度とした視方向 |
| `lens.specialized.probe.viewConfigurations[].relationship` | `supplied` / `optional` / `integrated` / `null` | 視方向ユニットと製品の関係 |
| `lens.specialized.probe.viewConfigurations[].axialRotationDegrees` | 0以上の数値 | 視方向ユニットの軸回転角 |
| `lens.specialized.probe.integratedLights` | light[]または`null` | 内蔵照明。一覧を確認し、該当する照明がない場合は`[]` |
| `lens.specialized.probe.integratedLights[].type` | `led` / `other` | 照明の種類 |
| `lens.specialized.probe.integratedLights[].location` | 文字列 | 照明の配置 |
| `lens.specialized.probe.integratedLights[].quantity` | 1以上の整数 | 灯数 |

### 内蔵テレコンバーター

`magnification`、`unitOpticalConstruction`、`engagedSpecifications`は、`lens.specialized.builtInTeleconverter`内で必須です。
`engagedSpecifications`は、内蔵テレコンバーターを入れた状態で変化する仕様だけを分けて記録します。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `lens.specialized.builtInTeleconverter.magnification` | 正数 | 内蔵テレコンバーターの公称倍率 |
| `lens.specialized.builtInTeleconverter.unitOpticalConstruction` | [opticalConstruction](../shared/shared-definitions.md#opticalconstruction)または`null` | テレコンバーターユニット単体の群数と枚数 |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.focalLength` | [focalLength](../shared/shared-definitions.md#focal-length-and-conditions)または`null` | 使用時の焦点距離 |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.aperture` | オブジェクトまたは`null` | 使用時のF値とT値。絞り機構は重複して記録しない |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.aperture.fNumber` | オブジェクトまたは`null` | 使用時のF値。オブジェクトの場合は通常の`fNumber`と同じ構造 |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.aperture.tNumber` | オブジェクト | 使用時のT値。適用できる場合だけ記録する |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.anglesOfView` | [angleOfView](../shared/shared-definitions.md#optical-values)[]または`null` | 使用時の画角 |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.minimumFocusDistances` | [minimumFocusDistance](../shared/shared-definitions.md#focus-measurements)[]または`null` | 使用時の最短撮影距離 |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.reproductionMagnifications` | [reproductionMagnification](../shared/shared-definitions.md#focus-measurements)[]または`null` | 使用時の撮影倍率 |
| `lens.specialized.builtInTeleconverter.engagedSpecifications.stabilizationRatings` | rating[]または`null` | 使用時の手ぶれ補正段数 |

`engagedSpecifications`の6フィールドはすべて必須です。
各値が公表されていない場合は`null`を使い、一覧を確認して該当する要素がない場合を表せる配列では`[]`も使用できます。

## 関連ページ

- [共通定義](../shared/shared-definitions.md)：焦点距離、測定条件、レンズ構成、撮影値
- [product-components](product-components.md)：レンズにも共通する識別情報、マウント、外形
- [レンズと関連光学製品のフィールドリファレンス](../../../lens-field-reference.md)：一般的なレンズと`specialized`の実例

[JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/product-type-lens.schema.json)
