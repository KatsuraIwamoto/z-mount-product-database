# product-record.schema.json

`data/records/lenses/<brand-id>/<product-id>.json`に置く、収録製品データ1件を検証します。
製品の構造には[product-full](product-full.md)を使い、編集するJSONファイルに必要な`$schema`だけを追加します。

## product-fullへの追加

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `$schema` | `"../../../../schemas/lenses/product-record.schema.json"` | 収録製品データを検証するJSON Schemaへの固定相対パス |

残りのフィールドは、[product-fullのトップレベルのフィールド](product-full.md#top-level-fields)と、そこから参照される共通スキーマおよび製品種別スキーマで定義します。

## ファイル配置とID

JSON Schemaだけでは表せない次の規則は、リポジトリ検証で確認します。

| 確認項目 | 規則 |
| --- | --- |
| ファイル名 | `<id>.json` |
| 親ディレクトリ | `identity.brandId`と同じブランドID |
| 調査結果データ | 収録済みの場合は結果ID、`decision.recordId`、製品IDが一致する |

配布データを生成するときは、各収録製品データから`$schema`だけを除去します。

参照元：`data/records/lenses/nikkor/nikkor-z-24-to-70mm-f2p8-s-ii.json`

参照箇所：`$schema`

[JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/lenses/product-record.schema.json)
