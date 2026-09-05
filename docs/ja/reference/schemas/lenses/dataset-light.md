# dataset-light.schema.json

`dist/z-mount-lenses.light.json`に生成する、レンズLight版の配布データ全体を検証します。
ルートの配布メタデータはFull版と同じ構成を使い、`products`の各要素は[product-light](product-light.md)に従います。

## Full版との関係

| 確認項目 | Light版の規則 |
| --- | --- |
| 製品数、順序、ID | Full版と一致する |
| 製品の構造 | 対応するFull版製品から、入れ子のオブジェクト内も含めて項目を省略できる。ただし、配列の順序は保つ |
| 保持する値 | Full版の値と型を変更しない |
| 配列 | 元の順序を保つ。最短撮影距離と最大撮影倍率だけは、スキーマで定めたFull版の要素を値を変えずに選ぶ |
| 参照データ | Full版の`referenceData`と一致する |
| 内容ハッシュ | `referenceData`とLight版自身の`products`から計算する |

JSON SchemaはLight版で許可する構造を検証します。
生成処理は、Full版と同じ入力からLight版を作ります。
Full版との値、製品数、順序の対応は、`hatch run validate`でも検証します。

## ルートフィールド

次のフィールドはすべて必須です。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `$schema` | 固定URI | このスキーマのバージョン付き公開URL |
| `datasetName` | `"Z Mount Lens Database"` | レンズ配布データの固定名称 |
| `datasetVariant` | `"light"` | Light版を表す固定値 |
| `schemaVersion` | `"1.0.0"` | JSON Schema一式で共有するバージョン |
| `dataVersion` | `YYYY.MM.DD`形式の文字列 | Full版と共有するデータのリリース識別子。Gitタグにも同じ値を使う |
| `creator` | 文字列 | 配布データの作成者 |
| `license` | `"CC-BY-4.0"` | 配布データに適用するSPDXライセンス識別子 |
| `licenseUrl` | HTTP(S) URL | CC BY 4.0のカノニカルURL |
| `repositoryUrl` | HTTP(S) URL | 収録製品データ、JSON Schema、ライセンス案内、Issue、リリース履歴を管理する公開リポジトリ |
| `recordCount` | 0以上の整数 | `products`に含まれる製品数。Full版と一致する |
| `contentHash` | `sha256:<64桁の小文字16進数>` | `referenceData`とLight版の`products`を含む内容オブジェクトのSHA-256 |
| `referenceData` | [reference-data](../shared/reference-data.md) | Full版と同じIDと表示情報 |
| `products` | [product-light](product-light.md)[] | Full版と同じ製品順を保つ軽量な製品配列 |

`datasetName`はFull版と共通する配布データ内の固定値であり、プロジェクト名「Z Mount Product Database」とは異なります。

!!! warning "生成ファイルは直接編集しません"

    Light版は収録製品データと生成規則から作成します。
    保持項目を変更する場合は、既存のWeb表示との互換性も確認します。

## 関連ページ

- [product-light](product-light.md)：`products[]`に含まれる製品1件
- [dataset-full](dataset-full.md)：対応するFull版のルート構造
- [値の読み方](../../../value-rules.md)：Full版とLight版の値の扱い

[JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/dataset-light.schema.json)
