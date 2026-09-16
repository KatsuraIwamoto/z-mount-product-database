# 調査結果データ

調査結果データは、候補製品ごとに、現在の収録判断とその根拠として使った情報源を記録するJSONデータです。
収録するかどうかを再確認できるように、判断結果だけでなく、最終確認日、情報源、未解決事項も残します。

配布データだけを利用する場合は、このページを読む必要はありません。
製品の収録判断を確認する場合や、調査結果データを編集する場合に参照してください。

## 製品一覧から根拠を確認する {#browse-product-research}

製品情報を確認するだけなら、まず[最新の製品一覧](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/PRODUCTS.md)を利用してください。
製品名をページ内検索すると、収録製品の公式製品ページ、調査結果の最終確認日、詳しい調査結果へのリンクを確認できます。
「対応が必要な調査結果」には、要確認の候補製品などについて、最終確認日と確認に使った情報源へのリンクも掲載しています。

最終確認日（`reviewedOn`）は、判断と情報源を最後に確認した日です。
製品情報がその日以降変わっていないことや、現在の販売状況を保証する日付ではありません。

公式製品ページが残っていない製品では、収録判断や仕様確認に使った代替根拠を調査結果データの`sources`に記録しています。
判断理由、代替根拠、未解決事項まで確認する必要がある場合は、製品一覧の「調査結果」から個別の調査結果を開いてください。
説明文は英語ですが、`decision`が収録判断、`sources`が根拠、`unresolved`が未解決事項を表します。

## 三つの収録判断

調査結果データの`decision.status`には、収録、除外、要確認のいずれかを記録します。

| 収録判断 | `decision`に記録する内容 | 収録製品データ |
| --- | --- | --- |
| 収録（`included`） | 収録製品データのIDを`recordId`に記録 | 作成する |
| 除外（`excluded`） | 収録基準を満たさない理由を`reason`に記録 | 作成しない |
| 要確認（`needs-review`） | 次に確認する具体的な問いを`unresolved`に記録 | 作成しない |

収録と除外には、判断を裏付ける`sources`が1件以上必要です。
要確認では、次に確認する具体的な問いを`unresolved`に1件以上記録します。
要確認でも、確認に使った情報源があれば`sources`に残します。
記録できる情報源が見つからない場合に限り、`sources`を空配列にできます。

## 実際の調査結果データ

次のJSONは、実際の調査結果データから説明に必要な項目と配列の要素を抜き出したものです。
掲載例は完全なファイルではありません。
収録の例にはマウントアダプターのMount Adapter FTZ IIを、除外と要確認の例にはレンズの候補製品を使います。

=== "収録（included）"

    Mount Adapter FTZ IIを例に、収録と判断した調査結果データを説明します。

    参照元：`research/results/adapters/nikon/mount-adapter-ftz-ii.json`

    ```json
    {
      "$schema": "../../../../schemas/adapters/research-result.schema.json",
      "id": "mount-adapter-ftz-ii",
      "subject": {
        "manufacturerId": "nikon",
        "brandId": "nikon",
        "name": "Mount Adapter FTZ II"
      },
      "reviewedOn": "2026-09-02",
      "decision": {
        "status": "included",
        "recordId": "mount-adapter-ftz-ii"
      },
      "sources": [
        {
          "url": "https://imaging.nikon.com/imaging/lineup/accessory/camera/ftz_2/",
          "publisherRelationship": "manufacturer-or-brand",
          "sourceType": "product-page",
          "checked": [
            "identity",
            "mountConfigurations",
            "electronics",
            "physical.dimensionMeasurements",
            "physical.weightMeasurements",
            "physical.officialEnvironmentalProtectionClaims",
            "physical.tripodSupport"
          ]
        },
        {
          "url": "https://downloadcenter.nikonimglib.com/en/products/590/FTZ_II.html",
          "publisherRelationship": "manufacturer-or-brand",
          "sourceType": "support-page",
          "checked": [
            "identity",
            "electronics"
          ],
          "decisionChecks": [
            "availability"
          ]
        }
      ]
    }
    ```

    `recordId`は、対応する収録製品データの`id`を指します。
    調査結果データの`id`、`recordId`、収録製品データの`id`は一致します。

=== "除外（excluded）"

    50mm F1.2 DG DN | Artを例に、除外と判断した調査結果データを説明します。

    参照元：`research/results/lenses/sigma/sigma-50mm-f1p2-dg-dn-art.json`

    ```json
    {
      "$schema": "../../../../schemas/lenses/research-result.schema.json",
      "id": "sigma-50mm-f1p2-dg-dn-art",
      "subject": {
        "manufacturerId": "sigma",
        "brandId": "sigma",
        "name": "50mm F1.2 DG DN | Art"
      },
      "reviewedOn": "2026-09-02",
      "decision": {
        "status": "excluded",
        "reason": "The official product page offers the lens only in L-Mount and Sony E-mount configurations."
      },
      "sources": [
        {
          "url": "https://www.sigma-global.com/en/lenses/a024_50_12/",
          "publisherRelationship": "manufacturer-or-brand",
          "sourceType": "product-page",
          "checked": [
            "identity",
            "mount"
          ],
          "decisionChecks": [
            "release-status"
          ]
        }
      ]
    }
    ```

    `reason`には、どの収録基準を満たさないかが分かる理由を記録します。
    除外した候補製品も調査結果データに残すことで、同じ候補製品を繰り返し調査せずに済みます。

=== "要確認（needs-review）"

    SIRUI Saturn V2 Full-Frame Anamorphic Lens Seriesを例に、要確認とした調査結果データを説明します。

    参照元：`research/results/lenses/sirui/sirui-saturn-v2-full-frame-anamorphic-lens-series.json`

    ```json
    {
      "$schema": "../../../../schemas/lenses/research-result.schema.json",
      "id": "sirui-saturn-v2-full-frame-anamorphic-lens-series",
      "subject": {
        "manufacturerId": "sirui",
        "brandId": "sirui",
        "name": "SIRUI Saturn V2 Full-Frame Anamorphic Lens Series"
      },
      "reviewedOn": "2026-09-02",
      "decision": {
        "status": "needs-review"
      },
      "sources": [
        {
          "url": "https://store.sirui.com/collections/z-mount-nikon-1",
          "publisherRelationship": "manufacturer-or-brand",
          "sourceType": "collection",
          "checked": [
            "mount"
          ]
        }
      ],
      "unresolved": [
        "Has SIRUI published a product release announcement or confirmed sale or availability for the Saturn V2 series?",
        "Has SIRUI announced or offered a Nikon Z configuration for the Saturn V2 series?"
      ]
    }
    ```

    `unresolved`には、次の調査で確認する具体的な問いを記録します。
    発売発表または販売確認に加え、Zマウント用製品であることも確認できるまで、収録製品データは作成しません。

`reason`、`notes`、`unresolved`、`sources[].note`の文字列は英語で記述します。

## 共通項目

| 項目 | 記録する情報 |
| --- | --- |
| `$schema` | 調査結果データの検証に使うJSON Schemaへの参照 |
| `id` | 調査結果データを識別するID |
| `subject` | 調査した候補製品のメーカーID、ブランドID、製品名 |
| `reviewedOn` | 判断と情報源の最終確認日 |
| `decision` | 収録、除外、要確認のいずれかの判断 |
| `sources` | 判断や製品情報の確認に使ったURL、発行者との関係、ページ種別、そのページで確認した要素 |
| `notes` | 情報源に明記された、根拠の解釈に必要な短い補足 |
| `unresolved` | 収録判断または値の確定に必要な根拠を問う、具体的な質問 |

最終確認日（`reviewedOn`）には、判断と情報源を実際に確認した日を`YYYY-MM-DD`形式で記録します。
`checked`を変更しただけでは、`reviewedOn`を更新しません。
収録製品データの確定値または`checked`の対象を変更する場合は、関係する情報源を再確認し、現在の判断と情報源を実際に確認した日を記録します。
この日付は、`config/versions.json`の`dataVersion`が表す日付より後にはできません。

`notes`は、測定基準や公式に命名されたバリエーションの適用範囲など、情報源に明記された事実を補足する項目です。
値を選んだ理由、情報源の比較、人間による判断、次に確認する問いは`notes`へ記録しません。
次に確認する問いは`unresolved`に記録します。

## 情報源を記録する

収録判断と製品情報の確認には、メーカーまたはブランドの情報源を優先します。

優先する情報源
: 対象製品の公式製品ページ、仕様書、マニュアル、発売発表です。

代替根拠として使う情報源
: 公式製品ページが残っていない場合は、メーカーまたはブランドが運営するクラウドファンディングのページを根拠にできます。
  企業のIR資料やプレスリリースも利用できます。
  正規代理店の製品ページや発表ページも代替根拠に含まれます。

裏付けに限って使う情報源
: 対象製品を扱う正規販売店のページは、発売済みであること、Zマウント用製品であること、メーカーが公式に公表した型番の裏付けに限って使用します。

外観画像から確認する情報
: 正規販売店が掲載した画像でも、対象製品と構成を特定でき、確認対象を明瞭に写していれば、製品上の表示、マウント、電子接点、操作部、外部機構、外部インターフェース、三脚支持など、外観から直接確認できる事実に使用できます。
  画像そのもののURLを`sourceType: image`として記録し、製品や構成の特定に使った販売ページも別の情報源として残します。
  動作や状態変化に依存する事実は、複数の状態を写した画像または動画で確認します。
  外観から内部構造、材質、寸法、重量、電子機能、耐候性能、互換性、発売状況を推測しません。
  マウント面全体を写した画像で電子接点がないことを確認した場合は、アダプターのデータ構造が必須とする関連電子機能の否定値も記録できます。

追加調査の手掛かり
: その他の販売店、レビュー、ニュース、掲示板は、追加調査の手掛かりとして扱います。
  収録判断や製品情報には、根拠となる情報源で確認できた事実だけを使います。

`sources[].url`には追跡用パラメーターやページ内の位置を示すフラグメントを除いたURLを記録し、同じURLを重複させません。
判断や収録値の根拠として使った情報源は、別の情報源と同じ要素を扱っている場合や、掲載内容が異なる場合も削除しません。

レンズとマウントアダプターの情報源では、`publisherRelationship`に発行者とメーカー・ブランドとの関係、`sourceType`にページ種別、`checked`にそのページで確認した収録製品データの項目を記録します。
`checked`は`lens.focus`、`mountConfigurations`、`electronics`、`physical.dimensionMeasurements`のように、製品用JSON Schemaのフィールドへ対応する中粒度のパスを使用します。
JSON Schemaに親と子のパスが別々に定義されている場合は、実際に確認した格納先と同じパスを記録します。
たとえば、`physical`は`physical.weightMeasurements`を、`mount`は`mount.electronicContacts`を確認した記録の代わりにはなりません。
収録製品データに確認済みの値がある主要フィールド群は、少なくとも一つの情報源の`checked`で追跡できなければなりません。
`false`と空配列も確認済みの値として追跡し、`null`は未確定なので追跡対象にしません。
収録した公式製品ページと同じURLの情報源には、`officialProductPages`も記録します。
収録製品データに対応するフィールドがない発売状況、販売確認、ライセンス、収録基準は`decisionChecks`へ分けます。
判断の再確認に必要なその情報源についての事実を構造化された項目で表せない場合だけ、`sources[].note`を使用します。

寸法、重量、日付、識別子などの値は収録製品データに記録し、`checked`や`sources[].note`へ重複させません。
`checked`では、個々の数値まで細分化せず、`lens.stabilization`、`electronics`、`physical.weightMeasurements`、`controls`など、収録製品データの格納先を追跡できる単位を選びます。
他の情報源との比較、誤記の断定、値を選んだ理由、調査手順は`sources`へ記録しません。

確認した情報源から一つの値を確定できない場合は、根拠なく値を選びません。
収録製品データでは[値の状態](value-rules.md#value-states)に従い、`unresolved`には必要な根拠を中立的な質問として記録します。
公式製品ページが削除されたことだけを理由に、製品が販売終了したとは判断しません。

収録製品データの`officialProductPages`と、調査結果データの`sources`の違いは[値の読み方](value-rules.md#urls)で説明しています。

!!! warning "調査過程のログは保存しません"

    AIとの会話、プロンプト、モデル名、一括調査の作業管理記録、重複した取得ログ、推測による結論は調査結果データへ記録しません。
    判断を再確認するために必要な結論、情報源、未解決事項だけを残します。

## ファイル配置とJSON Schema

レンズと関連光学製品のデータセットと、マウントアダプターのデータセットでは、調査結果データの構造とJSON Schemaを分けています。
各候補製品の調査結果データは、対応するデータセットのディレクトリに1ファイルずつ置きます。

| データセット | ファイル配置 | JSON Schemaリファレンス |
| --- | --- | --- |
| レンズと関連光学製品のデータセット | `research/results/lenses/<brand-directory>/<result-id>.json` | [lenses/research-result](reference/schemas/lenses/research-result.md) |
| マウントアダプターのデータセット | `research/results/adapters/<brand-directory>/<result-id>.json` | [adapters/research-result](reference/schemas/adapters/research-result.md) |

`<brand-directory>`には、メーカーとブランドのレジストリで定義されたブランドIDを使います。
ブランドをまだ確認できない候補製品は、`unattributed/`に置きます。

収録と判断した場合は、調査結果データの`id`と`recordId`を、対応する収録製品データの`id`と一致させます。
調査結果データに記録したメーカーID、ブランドID、製品名も、対応する収録製品データと一致させます。
対応する収録製品データの`lifecycle.announcementDate`と`lifecycle.officialDesignations[].observedOn`は、調査結果データの`reviewedOn`より後の日付にはできません。
除外と要確認の調査結果データは、対応する収録製品データを持ちません。

## 関連ページ

- [製品情報の報告と編集](contribute.md)：Issueでの報告と直接編集の手順
- [収録範囲と考え方](overview.md)：収録、除外、要確認を判断する基準
- [データモデル](data-model.md)：調査結果データ、収録製品データ、配布データの関係
- [用語集](glossary.md)：収録判断と情報源に関する用語
- [JSON Schemaリファレンス](reference/schemas/index.md)：型、必須項目、条件付き制約
