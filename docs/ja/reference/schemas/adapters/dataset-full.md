# adapters/dataset-full.schema.json

`dist/z-mount-adapters.full.json`に生成する、マウントアダプターFull版の配布データ全体を検証します。
ルートの配布メタデータと、[adapter-full](adapter-full.md)に従う`adapters`配列を結び付けるスキーマです。

## ルートフィールド

次のフィールドはすべて必須です。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `$schema` | 固定URI | このスキーマのバージョン付き公開URL |
| `datasetName` | `"Z Mount Adapter Database"` | マウントアダプター配布データの固定名称 |
| `datasetVariant` | `"full"` | Full版を表す固定値 |
| `schemaVersion` | `"1.0.0"` | JSON Schema一式で共有するバージョン |
| `dataVersion` | `YYYY.MM.DD`形式の文字列 | データのリリース識別子。Gitタグにも同じ値を使う |
| `creator` | 文字列 | 配布データの作成者 |
| `license` | `"CC-BY-4.0"` | 配布データに適用するSPDXライセンス識別子 |
| `licenseUrl` | HTTP(S) URL | CC BY 4.0のカノニカルURL |
| `repositoryUrl` | HTTP(S) URL | 収録製品データ、JSON Schema、ライセンス案内、Issue、リリース履歴を管理する公開リポジトリ |
| `recordCount` | 0以上の整数 | `adapters`に含まれる製品数 |
| `contentHash` | `sha256:<64桁の小文字16進数>` | `referenceData`と`adapters`を含む内容オブジェクトのSHA-256 |
| `referenceData` | [reference-data](../shared/reference-data.md) | この配布データから参照するIDと表示情報 |
| `adapters` | [adapter-full](adapter-full.md)[] | すべてのマウントアダプターの収録製品データから生成した製品配列。各要素に`$schema`は含めない |

`datasetName`は配布データ内の固定値であり、プロジェクト名「Z Mount Product Database」とは異なります。

!!! info "JSON Schema以外の検証"

    `recordCount`は、生成処理が`adapters`の要素数から設定します。
    `hatch run validate`では、配布データを再構築した結果と生成ファイルが一致することを確認します。
    JSON Schemaも、`adapters[]`内の`$schema`を拒否します。
    `contentHash`は、`referenceData`と`adapters`を持つオブジェクトをRFC 8785に従って正規化し、そのUTF-8バイト列から計算します。
    生成処理は、`adapters`を各要素の`id`文字列による辞書順（昇順）に並べます。
    製品を追加または削除すると、`dataVersion`間で既存製品の配列位置が変わる場合があります。

!!! warning "生成ファイルは直接編集しません"

    内容を変更する場合は、対応する収録製品データまたは生成処理を修正します。

## 関連ページ

- [adapter-full](adapter-full.md)：`adapters[]`に含まれる製品1件
- [配布データを使う](../../../use-data.md)：Full版の取得方法とメタデータの確認
- [データモデル](../../../data-model.md)：収録製品データから配布データを生成する流れ

[JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/adapters/dataset-full.schema.json)
