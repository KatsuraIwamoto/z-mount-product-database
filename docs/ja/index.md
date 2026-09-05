---
title: null
---

# Z Mount Product Database

ニコンZマウントに関わる製品情報を、検索、比較、分析に使えるデータセットとして公開しています。
現在は、レンズと関連光学製品、およびマウントアダプターを収録しています。

このドキュメントでは、収録範囲、配布データの使い方、データの構成、誤りや未収録製品の報告方法を案内します。

[製品一覧をダウンロード](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/PRODUCTS.md){ .md-button .md-button--primary }
[配布データを使う](use-data.md){ .md-button .md-button--primary }

!!! warning "収録済みは現在の販売状況を示しません"
    収録済みは、発売発表または販売を確認できたことを示します。
    現在販売中、在庫あり、入手可能であることは意味しません。
    購入や利用の前に、メーカーまたはブランドの公式情報を確認してください。

## 収録しているデータ {#datasets}

<div class="grid cards" markdown>

-   :material-camera-iris:{ .lg .middle } **レンズと関連光学製品**

    ---

    Zマウント用として販売された写真用レンズ、シネマ用レンズ、テレコンバーター、ピンホールなどを収録しています。

-   :material-swap-horizontal:{ .lg .middle } **マウントアダプター**

    ---

    他の交換レンズマウントからZマウントへの変換を主目的とする製品を収録しています。

</div>

収録・除外の判断基準は、[収録範囲と考え方](overview.md)で確認できます。

!!! info "カメラは現在の収録対象外です"
    将来カメラのデータを追加する場合は、独立したデータセットとします。

## 目的から探す {#find-by-purpose}

<div class="grid cards" markdown>

-   :material-format-list-bulleted:{ .lg .middle } **収録製品を一覧で確認する**

    ---

    GitHub Releaseの製品一覧で、収録済みの製品と調査状況をデータセットをまたいで確認できます。
    公式製品ページ、調査結果の最終確認日、詳しい調査結果へのリンクも掲載しています。

    [製品一覧をダウンロード](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/PRODUCTS.md)
    [根拠と最終確認日の読み方](research.md#browse-product-research)

-   :material-download-outline:{ .lg .middle } **配布データを使う**

    ---

    配布ファイルの選び方、ダウンロード方法、利用例を確認できます。

    [利用方法を見る](use-data.md)

-   :material-file-tree:{ .lg .middle } **データを理解する**

    ---

    データの構成と、二つのデータセットの各項目を確認できます。

    [データモデル](data-model.md) · [レンズと関連光学製品](lens-field-reference.md) · [マウントアダプター](adapter-field-reference.md)

-   :material-message-alert-outline:{ .lg .middle } **誤りや不足を知らせる**

    ---

    製品情報の誤りや未収録製品を、JSONを編集せずに報告できます。

    [報告方法を見る](contribute.md)

</div>

!!! tip "情報源とデータを並べて確認できます"

    製品情報を調査する場合は、ChromeとEdgeの拡張機能`Z Product Compare`を利用できます。
    情報源をブラウザで開いたまま、調査結果データと収録製品データをサイドパネルで確認できます。

    [Z Product Compareの使い方](development.md#z-product-compare)

## 参考資料 {#references}

- [用語集](glossary.md)：ドキュメントで使う用語と表記
- [JSON Schemaリファレンス](reference/schemas/index.md)：データの型、必須項目、制約
- [開発と検証](development.md)：生成、検証、ドキュメントのビルド、Z Product Compare
- [ライセンス](license.md)：利用条件とクレジット
