# Z Mount Product Database

ニコンZマウントに関わる製品情報を、再利用できるデータセットとして公開するプロジェクトです。

現在は、Zマウント用として販売されたレンズと関連光学製品、および他の交換レンズマウントからZマウントへ変換するマウントアダプターを収録しています。

収録済みは、発売発表または販売を確認できたことを示します。
現在販売中、在庫あり、入手可能であることは意味しません。

[English](README.md)

## プロジェクトを始めた理由

Zマウント製品の公式情報は、メーカーやブランドごとのWebサイトに分散しています。
地域ごとに別のページが用意され、掲載内容や表記が異なる場合もあります。
Webサイトの更新後に、以前の情報を確認しづらくなることもあります。

こうした情報を、そのままメーカーをまたいだ検索、比較、集計に利用するには手間がかかります。
そのため、このプロジェクトでは公式情報を優先し、採用した根拠を共通の形式で整理して、再利用しやすいデータとして残します。

## 設計方針

- レンズとマウントアダプターでは、配布データとJSON Schemaを分け、汎用的なレジストリと定義だけを共有します。
- 製品にはメーカー、ブランド、マウントシステムの固定IDを記録し、表示名は各配布用JSONの`referenceData`から参照できます。
- 項目が適用されない場合、適用されるが採用できる公開情報では確認できない場合、確認済みの空集合、確認済みの否定を区別します。
- JSON Schemaによる検証と、同じ入力から同じ結果を得られる生成処理により、編集するファイルと配布データのずれを検出します。

## 収録しているデータ

| データセット | 収録対象 |
| --- | --- |
| レンズと関連光学製品 | Zマウント用として販売された写真用レンズ、シネマ用レンズ、テレコンバーター、ピンホールなど |
| マウントアダプター | 他の交換レンズマウントからZマウントへの変換を主目的とする製品 |

レンズと関連光学製品は一つのデータセットに、マウントアダプターは別のデータセットに収録しています。

カメラは、現在の配布データの収録対象外です。
将来カメラのデータを追加する場合は、独立したデータセットとします。

詳しい収録基準は[収録範囲と考え方](https://katsuraiwamoto.github.io/z-mount-product-database/ja/overview/)を参照してください。

### 主な公開ファイル

| ファイル名 | 内容 |
| --- | --- |
| [PRODUCTS.md](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/PRODUCTS.md) | 収録製品と調査状況をまとめた一覧 |
| [z-mount-lenses.full.json](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/z-mount-lenses.full.json) | レンズと関連光学製品について、収録した項目をすべて含むJSONファイル |
| [z-mount-lenses.light.json](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/z-mount-lenses.light.json) | レンズと関連光学製品について、Web表示に必要な項目だけを残したJSONファイル |
| [z-mount-adapters.full.json](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/z-mount-adapters.full.json) | マウントアダプターについて、収録した項目をすべて含むJSONファイル |

この4ファイルは、GitHub Releaseの添付ファイルとして配布します。

`z-mount-lenses.light.json`には、`z-mount-lenses.full.json`と同じ製品を同じ順序で収録しています。
Web表示に必要な項目だけを残し、値は書き換えていません。

最新版と特定バージョンの取得方法、JavaScriptとPythonの利用例については、[配布データの利用ガイド](https://katsuraiwamoto.github.io/z-mount-product-database/ja/use-data/)を参照してください。

## データの活用例

配布データは、次のように利用できます。

- 条件に合う製品の検索
- 製品情報の比較
- ブランド、製品種別、仕様などによる集計と可視化
- Webサイトやアプリケーションへの組み込み
- 調査や分析のための基礎データ

### Webサイトでの検索と可視化

[cercidiphyllum.jpのNikonページ](https://cercidiphyllum.jp/nikon/)では、このプロジェクトの配布データを使って、製品検索と集計結果の可視化を行っています。

## 調査から配布まで

配布データと`PRODUCTS.md`は、次の流れで作成します。

1. **調査結果データ**：候補製品について、1製品につき1つのJSONファイルで調査結果を記録します。
   収録、除外、要確認の判断に加え、情報源と未解決の点を残します。
2. **収録製品データ**：収録対象と判断した製品について、1製品につき1つのJSONファイルで情報を記録します。
   採用できる公開情報で確認できない値は、推測で補いません。
3. **配布データ**：収録製品データから、JSONファイルを自動生成します。

調査結果データと収録製品データから、`PRODUCTS.md`も自動生成します。

## 詳しいドキュメント

収録基準、データの構成、各項目の意味は、[ドキュメントサイト](https://katsuraiwamoto.github.io/z-mount-product-database/ja/)で説明しています。
配布データの利用方法や調査と編集の手順も確認できます。

JSON Schema、JSONキー、データ内の説明は英語で記録しています。
READMEとCONTRIBUTINGには、日本語版と英語版があります。
ドキュメントサイトの英語版は、日本語版を基にAIで翻訳しています。

## プロジェクトへの貢献

製品情報の誤りや不足、収録されていない製品に気づいた場合は、[製品の追加と修正フォーム](https://github.com/KatsuraIwamoto/z-mount-product-database/issues/new?template=data-correction.yml)から報告できます。
報告は日本語と英語のどちらでも構いません。
JSONの編集は不要です。

製品名と気になった内容を記入してください。
メーカー公式ページのURLも、分かれば添えてください。
確信がなくても、「製品が抜けているかもしれない」「公式ページと値が違うように見える」という報告で構いません。

データを直接編集する場合は[貢献ガイド](CONTRIBUTING.ja.md)を参照してください。
開発環境の準備や検証方法は[開発と検証](https://katsuraiwamoto.github.io/z-mount-product-database/ja/development/)で説明しています。

### 製品調査用のZ Product Compare

製品情報の調査には、リポジトリに含まれるChromeとEdgeの拡張機能`Z Product Compare`を利用できます。
情報源をブラウザで開いたまま、調査結果データと収録製品データをサイドパネルで確認できます。
現在のリポジトリ検証の結果も同じ画面に表示されます。

<a href="docs/ja/assets/images/z-product-compare.webp">
  <img src="docs/ja/assets/images/z-product-compare.webp" alt="Z Product Compareの画面例。左側は公式製品ページの表示領域、右側は収録製品データ" width="840">
</a>

*Z Product Compareの画面例。実際の利用時は、左側に対応する公式製品ページが表示されます。*

`Z Product Compare`を使用するには、`hatch run review`でローカルサーバーを起動します。
拡張機能の追加方法と操作方法は、[Z Product Compareの使い方](https://katsuraiwamoto.github.io/z-mount-product-database/ja/development/#z-product-compare)を参照してください。

## ライセンス

- 製品情報と調査結果を記録したJSONファイル、3つの配布用JSON、`PRODUCTS.md`：[CC BY 4.0](LICENSES/CC-BY-4.0.txt)
- コード、JSON Schema、文書、設定：[MIT License](LICENSES/MIT.txt)

ここで示すのは概要です。
正確な適用範囲と推奨クレジット表記は[LICENSING.md](LICENSING.md)、無保証と責任制限を含む正式な条件は上記の各ライセンス本文を参照してください。

> [!IMPORTANT]
> CC BY 4.0が適用されるのは、本プロジェクトが許諾できる著作権その他これに類する権利だけです。
> 製品仕様などの事実や第三者の名称、商標を本プロジェクト固有の権利として主張するものではありません。
> 本プロジェクトは独立したプロジェクトであり、Nikon Corporationを含むいずれのメーカーとも提携していません。
> いずれのメーカーからも公認や推奨を受けていません。
