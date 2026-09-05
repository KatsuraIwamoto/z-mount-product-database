# ライセンス

データはCC BY 4.0、ソースコードやドキュメントはMIT Licenseで利用できます。
適用されるライセンスは、利用する対象によって異なります。
このページは主な内容の概要であり、すべての条件を網羅するものではありません。
正確な適用範囲は[`LICENSING.md`](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/LICENSING.md)を確認してください。
正式な条件は[CC BY 4.0の日本語リーガル・コード](https://creativecommons.org/licenses/by/4.0/legalcode.ja)と[MIT License本文](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/LICENSES/MIT.txt)を確認してください。

## 対象ごとのライセンス

| 対象 | ライセンス |
| --- | --- |
| 収録製品データとレジストリ | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja) |
| 調査結果データ | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja) |
| 3つの配布用JSONと`PRODUCTS.md` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja) |
| ソースコード、JSON Schema、テスト、ツール、設定、ドキュメント | [MIT License](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/LICENSES/MIT.txt) |

## データの利用条件

CC BY 4.0が適用されるデータは、営利目的を含め、複製、共有、改変できます。
データを共有する場合の主な表示項目は、次のとおりです。

- プロジェクト名と作成者名
- CC BY 4.0の表記とライセンスへのリンク
- 利用したデータのURL（合理的に可能な場合）
- 変更した場合は、その旨

適用されるすべての条件は、[CC BY 4.0の日本語リーガル・コード](https://creativecommons.org/licenses/by/4.0/legalcode.ja)を確認してください。

### クレジットの表記例

データを共有する場合はクレジットの表示が必要ですが、文面は利用する媒体に合わせて調整できます。
次の例は、そのままコピーして使えます。

=== "変更せず共有する"

    ```text
    Z Mount Product Database, Katsura Iwamoto, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), https://github.com/KatsuraIwamoto/z-mount-product-database
    ```

=== "変更して共有する"

    ```text
    Z Mount Product Database, Katsura Iwamoto, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), https://github.com/KatsuraIwamoto/z-mount-product-database
    変更内容：［変更した内容］
    ```

## コードとドキュメントの利用条件

MIT Licenseが適用されるものは、複製、変更、再配布、商用利用ができます。
これらの全部または重要な一部を複製、再配布する場合は、著作権表示とMIT Licenseの本文を残してください。

## 無保証

CC BY 4.0とMIT Licenseの本文には、無保証と責任制限が定められています。
本プロジェクトの確認手順は、データの正確性や完全性を保証するものではありません。
判断に重要な用途では、記録された情報源またはメーカーの公式情報も確認してください。

## 第三者の権利

!!! important "商標、特許、公式ページは許諾の対象外です"
    CC BY 4.0が適用されるのは、本プロジェクトが許諾できる著作権その他これに類する権利だけです。
    製品仕様などの事実に、本プロジェクトが新たな権利を主張するものではありません。
    第三者の商標、特許、公式ページなどに関する権利は、このライセンスでは許諾しません。

## メーカーとの関係

メーカー名、ブランド名、製品名は、製品と情報源を識別するために使用しています。
Z Mount Product Databaseは、Nikon Corporationを含むメーカーや権利者と提携しておらず、公認、後援、推奨も受けていません。

## ファイルごとのライセンス

ファイルごとのライセンスは、リポジトリの [`REUSE.toml`](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/REUSE.toml) で定義しています。
ライセンス本文と詳しい適用範囲は、[`LICENSING.md`](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/LICENSING.md)を参照してください。
各配布データのライセンスは、ルートにある `license` と `licenseUrl` でも確認できます。
配布用JSONだけを取得した場合は、ルートの`repositoryUrl`から公開リポジトリを開き、`LICENSING.md`で適用範囲と第三者の権利を確認できます。

!!! note "JSON Schemaとデータのライセンス"
    JSON Schemaの `$comment` にある `SPDX-FileCopyrightText` と `SPDX-License-Identifier: MIT` は、そのJSON Schemaファイルに適用されます。
    JSON Schemaで検証する収録製品データや配布データには、CC BY 4.0が適用されます。
