# adapter-full.schema.json

マウントアダプターFull版の`adapters[]`に含まれる製品1件を検証します。
すべての製品が同じトップレベルの構造を使います。
変換するマウントの組み合わせと、製品の機能や外形を記録します。

レンズと関連光学製品のJSON Schemaとは独立しているため、`productType`や製品種別ブロックは使用しません。

## トップレベルのフィールド {#top-level-fields}

`id`、`identity`、`lifecycle`、`officialProductPages`、`mountConfigurations`、`electronics`、`electronicServices`、`conversionOptics`、`mechanisms`、`physical`の10フィールドは必須です。
`$schema`は、収録製品データでは[adapter-record](adapter-record.md)が必須化し、配布データの生成時に除去します。

| パス | 型・値 | 説明 |
| --- | --- | --- |
| `$schema` | 文字列 | JSON Schemaへの参照。収録製品データだけが使用する |
| `id` | ID文字列 | `adapters`名前空間内で一意のID。小文字英数字をハイフンで区切った、人が読めるスラッグ形式を使う。文字列から製品情報を解析しない。ファイル名と調査結果データの対応に使う |
| `identity` | [identity](adapter-components.md#identity) | メーカーID、ブランドID、製品名、型番、別名、バリエーション |
| `lifecycle` | [lifecycle](adapter-components.md#lifecycle) | 発売発表日とメーカーまたはブランドによる状態表記 |
| `officialProductPages` | [officialProductPage](adapter-components.md#officialproductpage)[] | 製品そのものの公式メインページ。該当ページが残っていない場合は`[]` |
| `mountConfigurations` | [mountConfiguration](adapter-components.md#mountconfiguration)[] | 変換元となるレンズ側マウントとZマウントの組み合わせ。1件以上 |
| `electronics` | [electronics](adapter-components.md#electronics)または`null` | アダプターを介して利用できる電子機能 |
| `electronicServices` | [electronicServices](../shared/shared-definitions.md#electronic-data)または`null` | ファームウェア更新の公開有無と、更新、設定、制御に使う接続方式 |
| `conversionOptics` | [conversionOptics](adapter-components.md#conversionoptics)または`null` | 変換光学系の有無と、焦点距離や開放値への影響 |
| `mechanisms` | [mechanisms](adapter-components.md#mechanisms)または`null` | 確認済みの付加機構 |
| `physical` | [physical](adapter-components.md#physical) | 寸法、重量、環境保護表現、三脚取付部 |

`electronics`、`electronicServices`、`conversionOptics`、`mechanisms`は、確認できた内容がなくてもフィールド自体を省略しません。
`electronicServices.connections[].method`が`camera-body`の場合は、`electronics.electronicContacts`が`true`でなければなりません。
独立した`direct-usb`または`dock`接続には、この条件を適用しません。
シフト、ティルト、回転の可動量は、対応する`mechanisms[]`要素の`movements`に記録します。
これにより、機構の種類、適用条件、可動量を同じ要素として追跡できます。
採用できる公開情報で値を確認できない場合の`null`、一覧を確認して該当する要素がない場合の`[]`、確認済みの否定を表す`false`は、それぞれ意味が異なります。
詳しい使い分けは、[値の読み方](../../../value-rules.md)を参照してください。

!!! info "マウントアダプターはFull版のみ"

    マウントアダプターにはLight版を設けていません。
    配布データでは、すべての収録製品データから`$schema`だけを除去します。

## 関連ページ

- [adapter-record](adapter-record.md)：収録製品データに追加する`$schema`と配置規則
- [adapter-components](adapter-components.md)：各トップレベルのフィールドから参照する定義
- [マウントアダプターのフィールドリファレンス](../../../adapter-field-reference.md)：実データを使った各フィールドの説明

[JSON Schemaファイル](https://github.com/KatsuraIwamoto/z-mount-product-database/blob/main/schemas/adapters/adapter-full.schema.json)
