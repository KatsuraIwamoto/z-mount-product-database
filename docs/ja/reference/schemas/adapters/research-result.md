# adapters/research-result.schema.json

`research/results/adapters/<brand-id>/<result-id>.json`に置く、調査結果データ1件を検証します。
一つのマウントアダプター候補について、現在の収録判断、確認した情報源、未解決の確認事項を記録します。

## 収録判断の3状態

一つの調査結果データが持つ判断は一つです。
次の実例では状態ごとに異なる候補製品を使い、条件による構造の違いだけを示します。

=== "収録（included）"

    製品：マウントアダプター FTZ II

    参照元：`research/results/adapters/nikon/mount-adapter-ftz-ii.json`

    参照箇所：`decision`

    ```json
    {
      "decision": {
        "status": "included",
        "recordId": "mount-adapter-ftz-ii"
      }
    }
    ```

    `recordId`は、対応する収録製品データの製品IDです。

=== "除外（excluded）"

    製品：Auto Focus Extension Tube Set for Nikon Z-Mount Lenses

    参照元：`research/results/adapters/vello/vello-ext-nz.json`

    参照箇所：`decision`

    ```json
    {
      "decision": {
        "status": "excluded",
        "reason": "This is a same-mount extension-tube set, not a product whose primary purpose is converting one interchangeable-lens mount to Nikon Z."
      }
    }
    ```

    この例は、Zマウントのレンズとカメラの間に装着する接写リングです。
    別の交換レンズマウントからZマウントへの変換を主目的とする製品ではないため、収録対象外と判断しています。

=== "要確認（needs-review）"

    製品：MonsterAdapter LA-FZ11

    参照元：`research/results/adapters/monsteradapter/monsteradapter-la-fz11.json`

    参照箇所：`decision`、`unresolved`

    ```json
    {
      "decision": {
        "status": "needs-review"
      },
      "unresolved": [
        "Confirm an official release announcement or verified sale of LA-FZ11; development references alone do not qualify for a canonical record."
      ]
    }
    ```

    この例では、製品の発売発表または販売の事実を確認できる情報が見つかっていません。

## 判断状態ごとの条件

| `decision.status` | 追加必須フィールド | `sources` |
| --- | --- | --- |
| `included` | `decision.recordId` | 1件以上 |
| `excluded` | `decision.reason` | 1件以上 |
| `needs-review` | ルートの`unresolved`を1件以上 | 記録できる情報源が見つからない場合に限り`[]`を使用できる |

`decision`は、`included`の場合は`status`と`recordId`、`excluded`の場合は`status`と`reason`、`needs-review`の場合は`status`だけを持ちます。

## 共通フィールド

`$schema`、`id`、`subject`、`reviewedOn`、`decision`、`sources`は必須です。
`notes`と`unresolved`は、必要な場合だけ追加します。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `$schema` | `"../../../../schemas/adapters/research-result.schema.json"` | 調査結果データを検証するJSON Schemaへの固定相対パス |
| `id` | ID文字列 | 調査対象を一意に表す結果ID |
| `subject` | オブジェクト | 調査時点で把握している候補製品の名称情報 |
| `subject.manufacturerId` | ID文字列または`null` | 判明しているメーカーID |
| `subject.brandId` | ID文字列または`null` | 判明しているブランドID |
| `subject.name` | 文字列 | 調査対象とした製品名 |
| `subject.aliases` | 重複のない文字列[] | 同じ候補製品を指す別名。ない場合は省略する |
| `reviewedOn` | 日付 | 現在の判断と情報源を最後に確認した日 |
| `decision.status` | `included` / `excluded` / `needs-review` | 現在の収録判断 |
| `decision.recordId` | ID文字列 | `included`の場合に対応する収録製品データの製品ID |
| `decision.reason` | 文字列 | `excluded`の場合に対象外と判断した根拠 |
| `sources` | `source`の配列 | 判断のために確認した情報源 |
| `sources[].url` | HTTP(S) URL | 確認したページのURL |
| `sources[].publisherRelationship` | 列挙値 | 発行者とメーカー・ブランドとの関係 |
| `sources[].sourceType` | 列挙値 | ページまたは媒体の種別 |
| `sources[].checked` | 重複のない列挙値[] | そのURLで確認した製品用JSON Schemaのフィールドパス |
| `sources[].decisionChecks` | 重複のない列挙値[] | 収録製品データに対応するフィールドがない収録判断用の確認事項 |
| `sources[].note` | 文字列 | 構造化フィールドだけでは表せない短い補足。不要な場合は省略する |
| `notes` | 重複のない文字列[] | 判断を変えない補足。ない場合は省略する |
| `unresolved` | 重複のない文字列[] | 未解決の確認事項。`needs-review`では1件以上必須 |

`subject`では、`manufacturerId`、`brandId`、`name`が必須です。
メーカーまたはブランドを特定できない場合は、対応するIDフィールドに`null`を記録します。

## 収録製品データとの対応

`decision.status`が`included`の場合、次の対応をリポジトリ検証で確認します。

| 確認項目 | 規則 |
| --- | --- |
| ID | 結果ID、`decision.recordId`、収録製品データの製品IDが一致する |
| 識別情報 | `subject`のメーカーID、ブランドID、製品名が収録製品データの`identity`と一致する |
| 確認日 | `reviewedOn`が`dataVersion`の日付より後にならない |
| 製品の日付 | `lifecycle.announcementDate`と`lifecycle.officialDesignations[].observedOn`が`reviewedOn`より後にならない |
| 情報源の範囲 | 収録製品データに確認済みの値がある主要フィールド群を、いずれかの情報源の`checked`が覆う |

`checked`を変更しただけでは、`reviewedOn`を更新しません。
収録製品データの確定値または`checked`の対象を変更する場合は、関係する情報源を再確認し、現在の判断と情報源を実際に確認した日を記録します。

`false`と空配列も確認済みの値として扱い、`null`は対象外です。

## 情報源の分類と確認項目

`publisherRelationship`には、次の値を使用できます。

- `manufacturer-or-brand`、`authorized-distributor`、`authorized-retailer`
- `retailer`、`crowdfunding-platform`、`independent-publication`、`unknown`

`sourceType`には、次の値を使用できます。

- `announcement`、`catalog`、`collection`、`company-profile`
- `crowdfunding`、`distributor-page`、`faq`、`image`
- `manual`、`news-report`、`product-page`、`retailer-listing`
- `specification`、`support-page`、`technical-page`、`video`、`other`

各`source`には`checked`または`decisionChecks`の少なくとも一方が必要です。
`checked`は、次のフィールドパスから選びます。
親と子が個別に列挙されている場合、親パスは子パスの代わりになりません。

- 基本情報：`identity`、`identity.modelNumberOptions`、`identity.alternateNames`、`identity.variants`、`lifecycle`、`officialProductPages`
- マウントと機能：`mountConfigurations`、`electronics`、`electronicServices`、`conversionOptics`、`mechanisms`
- 外形：`physical.dimensionMeasurements`、`physical.weightMeasurements`、`physical.officialEnvironmentalProtectionClaims`、`physical.tripodSupport`

`decisionChecks`には、`availability`、`inclusion-criteria`、`licensing`、`release-status`のいずれかを使用します。
個々の数値や配列要素までは細分化せず、値と事実そのものは収録製品データに記録します。
情報源には調査時の会話、プロンプト、取得ログを保存しません。
情報源と判断の詳しい扱いは、[調査結果データを編集する](../../../research.md)を参照してください。

## 関連ページ

- [adapter-record](adapter-record.md)：マウントアダプターの収録製品データの構造と配置規則
- [データモデル](../../../data-model.md)：調査結果データから収録製品データへ進む流れ
- [調査結果データを編集する](../../../research.md)：判断状態と情報源の記録方法

[JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/adapters/research-result.schema.json)
