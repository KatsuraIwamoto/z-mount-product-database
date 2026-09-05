# adapter-record.schema.json

`data/records/adapters/<brand-id>/<adapter-id>.json`に置く、マウントアダプターの収録製品データ1件を検証します。
製品の構造には[adapter-full](adapter-full.md)を使い、編集するJSONファイルに必要な`$schema`だけを追加します。

## adapter-fullへの追加

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `$schema` | `"../../../../schemas/adapters/adapter-record.schema.json"` | 収録製品データを検証するJSON Schemaへの固定相対パス |

残りのフィールドは、[adapter-fullのトップレベルのフィールド](adapter-full.md#top-level-fields)と、そこから参照される[adapter-components](adapter-components.md)で定義します。

## ファイル配置とID

JSON Schemaだけでは表せない次の規則は、リポジトリ検証で確認します。

| 確認項目 | 規則 |
| --- | --- |
| ファイル名 | `<id>.json` |
| 親ディレクトリ | `identity.brandId`と同じブランドID |
| 調査結果データ | 収録済みの場合は結果ID、`decision.recordId`、製品IDが一致する |

配布データを生成するときは、各収録製品データから`$schema`だけを除去します。

参照元：`data/records/adapters/nikon/mount-adapter-ftz-ii.json`

参照箇所：`$schema`

[JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/adapters/adapter-record.schema.json)
