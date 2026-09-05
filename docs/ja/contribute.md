# 製品情報の報告と編集

製品情報の誤りや未収録製品は、GitHubのフォームから報告できます。
JSONを編集できる場合は、調査結果データと収録製品データを直接修正し、Pull Requestを送ることもできます。

<div class="grid cards" markdown>

-   :material-message-alert-outline:{ .lg .middle } **製品情報を報告する**

    ---

    製品名と気づいた内容を、分かる範囲で報告できます。
    JSONやJSON Schemaを書く必要はありません。

    [製品の追加と修正フォームを開く](https://github.com/KatsuraIwamoto/z-mount-product-database/issues/new?template=data-correction.yml){ .md-button .md-button--primary }

-   :material-file-edit-outline:{ .lg .middle } **ファイルを直接編集する**

    ---

    メーカーまたはブランドが公開した情報源を確認し、対応する調査結果データや収録製品データを修正します。

    [直接編集の手順を見る](#direct-edit)

</div>

## 製品情報を報告する

[製品の追加と修正フォーム](https://github.com/KatsuraIwamoto/z-mount-product-database/issues/new?template=data-correction.yml)では、次の内容を入力します。

1. 報告の種類
2. レンズと関連光学製品、マウントアダプターのどちらに関する報告か
3. 製品名
4. 現在の情報と、気づいた誤りや不足
5. 分かれば、メーカーまたはブランドの公式製品ページ、仕様書、マニュアルなどのURL
6. ページ内の確認箇所、地域差、画像などの補足

フォームでは、「誤りの修正」「未収録製品」「収録対象外かもしれない」「公式URLの変更」「その他」から報告の種類を選びます。
どのデータセットに該当するか分からない場合は、フォームで「不明」を選択できます。

!!! info "確信がなくても報告できます"

    「製品が抜けているかもしれない」「公式製品ページと値が違うように見える」という段階でも報告できます。
    公式製品ページなどの情報源が見つからない場合は、製品名と気づいた内容だけでも構いません。
    収録判断を確定できない候補製品は、要確認（`needs-review`）として調査を続けます。

AIを使って報告文を整えても構いません。
ただし、URL、製品名、数値などの事実は推測させず、確認できた内容だけを投稿してください。

## 不具合を報告する

リポジトリ検証、配布データの生成、JSON Schemaに関する不具合は、[不具合報告フォーム](https://github.com/KatsuraIwamoto/z-mount-product-database/issues/new?template=bug-report.yml)を使用してください。
ドキュメントサイトやCIの不具合も、同じフォームから報告できます。
製品情報の誤りや未収録製品は、前節の製品情報用フォームから報告します。

## ファイルを直接編集する { #direct-edit }

直接編集する場合は、次の表から変更内容に対応するファイルを選んで修正します。
配布データと製品一覧は自動生成されるため、直接編集しません。

| 変更する内容 | 編集するファイル |
| --- | --- |
| レンズと関連光学製品の収録判断、情報源、未解決事項 | `research/results/lenses/<brand-directory>/<result-id>.json` |
| レンズと関連光学製品の製品情報 | `data/records/lenses/<brand-id>/<product-id>.json` |
| マウントアダプターの収録判断、情報源、未解決事項 | `research/results/adapters/<brand-directory>/<result-id>.json` |
| マウントアダプターの製品情報 | `data/records/adapters/<brand-id>/<adapter-id>.json` |
| メーカーID、ブランドID、対応する表示名 | `data/product-manufacturer-brand-registry.json` |
| マウントシステムIDと表示名 | `data/mount-system-registry.json` |

!!! warning "生成ファイルは直接編集しません"

    `dist/`の配布データと`PRODUCTS.md`は、生成処理で作られます。
    必要なファイルを修正してから`hatch run generate`を実行してください。

!!! tip "調査にはZ Product Compareを利用できます"

    ChromeとEdgeの拡張機能`Z Product Compare`を使うと、情報源をブラウザで開いたまま、調査結果データと収録製品データをサイドパネルで確認できます。

    [導入と操作方法を見る](development.md#z-product-compare)

### 調査結果データと収録製品データ

候補製品を調べた結果は、製品ごとに一つの調査結果データへ記録します。
収録（`included`）と判断した製品には、対応する収録製品データが必要です。
除外（`excluded`）または要確認（`needs-review`）では、収録製品データを作成しません。

収録判断、情報源、`reviewedOn`、`unresolved`の記録方法は[調査結果データ](research.md)で説明しています。
収録範囲は[収録範囲と考え方](overview.md)を確認してください。

### 製品情報を記録する

正式な製品名と、根拠となる情報源で確認できた値をそのまま記録します。
情報源で確認できない値を推測したり、矛盾する複数の値から一つを独断で選んだりしません。

項目の省略、`null`、空配列、`false`の使い分けは[値の読み方](value-rules.md)に従います。
各項目の意味は、[レンズと関連光学製品のフィールドリファレンス](lens-field-reference.md)または[マウントアダプターのフィールドリファレンス](adapter-field-reference.md)で確認できます。
正確な型、必須項目、許可される値は[JSON Schemaリファレンス](reference/schemas/index.md)を参照してください。

### 最終確認日とデータバージョン

調査結果データの最終確認日（`reviewedOn`）には、判断と情報源を実際に確認した日を記録します。
`checked`を変更しただけでは、`reviewedOn`を更新しません。
収録製品データの確定値または`checked`の対象を変更する場合は、関係する情報源を再確認し、現在の判断と情報源を実際に確認した日を記録します。
`reviewedOn`が現在の`dataVersion`より後になる場合は、Pull Requestでの検証のため、`config/versions.json`の`dataVersion`を最新の`reviewedOn`と同じ日付へ暫定的に更新します。
公開版の`dataVersion`には、リリース日（Asia/Tokyo）を使用します。

## 変更を検証する

Python 3.14以降とHatchが必要です。
環境の準備は[開発と検証](development.md)を参照してください。

次の順序で、JSONの整形、配布データの生成、リポジトリ検証、ドキュメントのビルドを実行します。

```bash
hatch run format-json
hatch run generate
git diff -- dist PRODUCTS.md
hatch run check
hatch run docs:build
```

生成後は、意図した変更が生成ファイルへ反映されていることを確認します。
調査結果データだけの変更では`PRODUCTS.md`、レンズの収録製品データ変更ではレンズFull版、Light版、`PRODUCTS.md`、マウントアダプターの収録製品データ変更ではマウントアダプターFull版と`PRODUCTS.md`に差分が生じる場合があります。
実際に差分がある生成ファイルだけを、その変更元となった調査結果データ、収録製品データ、またはレジストリと同じPull Requestへ含めます。

ドキュメントを変更する場合は、対応する日本語版と英語版を同じPull Requestで更新します。
各文書の基準版と検証方法は、[ドキュメントの保守](development.md#documentation-maintenance)を参照してください。

## Pull Requestを送る

Pull Requestには、次の内容を記載します。

1. 変更した内容と理由
2. 確認に使った情報源のURL
3. 残っている未解決事項
4. 実行した検証

調査結果データ、収録製品データ、レジストリへの貢献にはCC BY 4.0が適用されます。
コード、JSON Schema、テスト、ツール、設定、ドキュメントへの貢献にはMIT Licenseが適用されます。
貢献者自身が、該当するプロジェクトのライセンスで提供する権限を持つ内容だけを提出してください。
第三者の文章、画像、ロゴなどを含める場合は、権利者、出典、利用条件、許諾の対象外となる部分をPull RequestまたはIssueに明記してください。
Issueに調査資料として添付した画像などは、そのまま公開文書へ転載しません。
詳しい適用範囲は[ライセンス](license.md)を確認してください。

## 関連ページ

- [調査結果データ](research.md)：収録判断、情報源、未解決事項の記録方法
- [収録範囲と考え方](overview.md)：レンズと関連光学製品、マウントアダプターの収録基準
- [値の読み方](value-rules.md)：項目の省略、`null`、空配列、`false`の意味
- [データモデル](data-model.md)：調査結果データ、収録製品データ、配布データの関係
- [開発と検証](development.md)：開発環境、生成、検証の詳細
