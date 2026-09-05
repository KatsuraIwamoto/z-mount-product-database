# 貢献ガイド

[English](CONTRIBUTING.md)

製品情報の報告とファイルの編集は、日本語と英語のどちらでも受け付けています。
JSONを編集できない場合は、GitHubのフォームから製品名と気づいた内容を報告するだけで構いません。

## 製品情報を報告する

[製品の追加と修正フォーム](https://github.com/KatsuraIwamoto/z-mount-product-database/issues/new?template=data-correction.yml)には、次の内容を分かる範囲で記載してください。

1. 製品名とブランド
2. レンズと関連光学製品、マウントアダプターのどちらに関する報告か
3. 気づいた誤りや不足、または未収録だと思った内容
4. メーカーまたはブランドの公式製品ページ、仕様書、マニュアルなどのURL
5. ページ内の確認箇所、地域差、未確定な点などの補足

収録対象か判断できない場合や、情報源を見つけられない場合も報告できます。
収録判断を確定できない候補製品は、要確認（`needs-review`）の調査結果データとして残し、確認を続けます。

正式な製品ページが残っていない場合は、メーカーが運営するクラウドファンディング、企業のIR資料やプレスリリース、正規代理店のページを代替根拠にできます。
正規販売店の対象製品ページは、発売済みのマウント構成とメーカーが公表した型番の裏付けに限って使用します。
その他の販売店、レビュー、ニュース、掲示板は、追加調査の手掛かりとして扱います。

AIを使って報告文を整えても構いません。
ただし、URL、製品名、数値などの事実は推測させず、確認できた内容だけを投稿してください。

配布データの生成、リポジトリ検証、JSON Schema、ドキュメントサイトに関する不具合は、[不具合報告フォーム](https://github.com/KatsuraIwamoto/z-mount-product-database/issues/new?template=bug-report.yml)から報告してください。

## ファイルを直接編集する

変更内容に応じて、次の表から編集するファイルを選びます。

| 変更する内容 | 編集するファイル |
| --- | --- |
| レンズと関連光学製品の収録判断、情報源、未解決事項 | `research/results/lenses/<brand-directory>/<result-id>.json` |
| レンズと関連光学製品の製品情報 | `data/records/lenses/<brand-id>/<product-id>.json` |
| マウントアダプターの収録判断、情報源、未解決事項 | `research/results/adapters/<brand-directory>/<result-id>.json` |
| マウントアダプターの製品情報 | `data/records/adapters/<brand-id>/<adapter-id>.json` |
| メーカーID、ブランドID、対応する表示名 | `data/product-manufacturer-brand-registry.json` |
| マウントシステムIDと表示名 | `data/mount-system-registry.json` |

`reviewedOn`は、現在の判断と対象の情報源を再確認した後に限って更新します。
`checked`を変更しただけでは、再確認したことにはなりません。

候補製品の調査内容は、製品ごとに一つの調査結果データへ記録します。
収録（`included`）と判断した製品には、対応する収録製品データが必要です。
除外（`excluded`）または要確認（`needs-review`）では、収録製品データを作成しません。

正式な製品名と、根拠となる情報源で確認できた値を記録してください。
情報源で確認できない値を推測したり、矛盾する複数の値から一つを独断で選んだりせず、未解決事項を`unresolved`に記録します。
項目の省略、`null`、空配列、`false`は、それぞれ異なる状態を表します。

`dist/`の配布データと`PRODUCTS.md`は生成ファイルです。
直接編集せず、変更内容に対応する調査結果データ、収録製品データ、またはレジストリを修正してから再生成してください。

詳しい手順は、次のページを参照してください。

- [製品情報の報告と編集](https://katsuraiwamoto.github.io/z-mount-product-database/ja/contribute/)
- [調査結果データ](https://katsuraiwamoto.github.io/z-mount-product-database/ja/research/)
- [値の読み方](https://katsuraiwamoto.github.io/z-mount-product-database/ja/value-rules/)
- [JSON Schemaリファレンス](https://katsuraiwamoto.github.io/z-mount-product-database/ja/reference/schemas/)

本プロジェクトがGitHub Releasesで初めて正式公開した製品の`id`は、製品名、ブランド、仕様、製品種別を訂正する場合も変更しません。
公開済みの製品IDを別の製品に割り当てたり、削除後に再利用したりしないでください。
GitHub Releasesでの初回正式公開より前は、作業中のIDをレビューで訂正できます。

製品調査には、ChromeとEdgeの拡張機能`Z Product Compare`も利用できます。
[導入と操作方法](https://katsuraiwamoto.github.io/z-mount-product-database/ja/development/#z-product-compare)は、開発と検証のページで説明しています。

## 初めてのPull Request

1. リポジトリをフォークし、そのフォークをローカルへクローンします。
2. 作業用ブランチを作成します。
3. Python 3.14以降とHatchを利用できることを確認し、編集前に`hatch run check`と`hatch run docs:build`を実行して、変更前の状態に問題がないことを確認します。
4. 必要なファイルを編集し、後述の検証を実行して、意図したソースと生成ファイルの差分だけをコミットします。
5. ブランチをプッシュしてPull Requestを作成し、変更内容、根拠として使った情報源のURL、未解決事項、実行した検証を記載します。

## 収録範囲を確認する

現在の収録対象は、レンズと関連光学製品、およびマウントアダプターです。
カメラは現在の収録対象外です。将来カメラのデータを追加する場合は、独立したデータセットとします。

レンズと関連光学製品では、Zマウントへ直接装着する製品と、Zマウント用アダプターを同梱した製品、そのレンズまたは製品シリーズ専用のZマウント用アダプターを使用する製品を収録します。
マウントアダプターでは、他の交換レンズマウントからZマウントへの変換を主目的とする製品を収録します。
初期のアダプターデータは、基本情報、変換するマウント、電子機能、光学系、機構、寸法と重量を対象とします。
レンズ、カメラ、ファームウェアの組み合わせごとの大規模な互換性一覧は含めず、レンズデータとは別のJSON Schemaを使います。

収録製品データを作成するには、製品の発売発表または販売確認が必要です。
開発発表だけの場合は、要確認の調査結果データとして残します。

詳しい条件は、[収録範囲と考え方](https://katsuraiwamoto.github.io/z-mount-product-database/ja/overview/)を参照してください。
情報源の優先順位と記録方法は、[調査結果データ](https://katsuraiwamoto.github.io/z-mount-product-database/ja/research/)で説明しています。

## 変更を検証する

Python 3.14以降とHatchが必要です。
環境の準備は、[開発と検証](https://katsuraiwamoto.github.io/z-mount-product-database/ja/development/)を参照してください。

次の順序で、JSONの整形、配布データの生成、リポジトリ検証、ドキュメントのビルドを実行します。

```bash
hatch run format-json
hatch run generate
git diff -- dist PRODUCTS.md
hatch run check
hatch run docs:build
```

生成後は、意図した変更が生成ファイルへ反映されていることを確認してください。
調査結果データだけの変更では`PRODUCTS.md`、レンズの収録製品データ変更ではレンズFull版、Light版、`PRODUCTS.md`、マウントアダプターの収録製品データ変更ではマウントアダプターFull版と`PRODUCTS.md`に差分が生じる場合があります。
実際に差分がある生成ファイルだけを、その変更元となった調査結果データ、収録製品データ、またはレジストリと同じPull Requestへ含めます。

ドキュメントを変更する場合は、対応する日本語版と英語版を同じPull Requestで更新します。
各文書の基準版と検証方法は、[ドキュメントの保守](https://katsuraiwamoto.github.io/z-mount-product-database/ja/development/#documentation-maintenance)を参照してください。

## Pull Requestを送る

Pull Requestには、次の内容を記載してください。

1. 変更した内容と理由
2. 確認に使った情報源のURL
3. 残っている未解決事項
4. 実行した検証

## ライセンス

調査結果データ、収録製品データ、レジストリへの貢献にはCC BY 4.0が適用されます。
コード、JSON Schema、テスト、ツール、設定、ドキュメントへの貢献にはMIT Licenseが適用されます。
貢献者自身が、該当するプロジェクトのライセンスで提供する権限を持つ内容だけを提出してください。
第三者の文章、画像、ロゴなどを含める場合は、権利者、出典、利用条件、許諾の対象外となる部分を明記してください。
Issueに調査資料として添付した画像などは、そのまま公開文書へ転載しません。
詳しい適用範囲は、[ライセンス](https://katsuraiwamoto.github.io/z-mount-product-database/ja/license/)と[LICENSING.md](LICENSING.md)を参照してください。
