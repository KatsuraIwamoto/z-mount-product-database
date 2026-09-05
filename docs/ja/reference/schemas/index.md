# JSON Schemaリファレンス

このリファレンスは、配布データを検証する利用者と、データ構造を変更する開発者向けの資料です。
許可される値と条件付き制約も、JSON Schemaごとに説明します。
各フィールドの役割や実際の値を先に理解したい場合は、[レンズと関連光学製品のフィールドリファレンス](../../lens-field-reference.md)または[マウントアダプターのフィールドリファレンス](../../adapter-field-reference.md)を参照してください。

このプロジェクトのJSON Schemaは、JSON Schema Draft 2020-12に準拠しています。
公開URLの名前空間は、レンズと関連光学製品、マウントアダプター、共通定義に分かれています。
JSON Schema一式には一つのスキーマバージョンを使い、配布データの`schemaVersion`に記録します。

## 目的からJSON Schemaを選ぶ {#choose-schema}

確認するデータの種類や単位によって、最初に開くページが異なります。

| 確認する対象 | 最初に開くページ |
| --- | --- |
| レンズFull版またはレンズLight版の配布データ全体 | [dataset-full](lenses/dataset-full.md)または[dataset-light](lenses/dataset-light.md) |
| レンズFull版またはレンズLight版に含まれる製品1件 | [product-full](lenses/product-full.md)または[product-light](lenses/product-light.md) |
| レンズと関連光学製品の収録製品データ | [product-record](lenses/product-record.md) |
| マウントアダプターFull版の配布データ全体 | [dataset-full](adapters/dataset-full.md) |
| マウントアダプターFull版に含まれる製品1件 | [adapter-full](adapters/adapter-full.md) |
| マウントアダプターの収録製品データ | [adapter-record](adapters/adapter-record.md) |
| 候補製品の調査結果データ | [レンズと関連光学製品](lenses/research-result.md)または[マウントアダプター](adapters/research-result.md) |
| 配布用JSONに埋め込むIDと表示情報 | [reference-data](shared/reference-data.md) |

## フィールド表と制約の読み方 {#field-tables}

各ページのフィールド表では、JSON内の位置を「パス」、許可されるデータ型や固定値を「型・値」、項目の役割を「説明」として示します。

- `[]`は配列を表します。
    たとえば`products[]`は、`products`配列に含まれる各要素を指します。
- 「Aまたは`null`」は、その項目にAで示した型の値か`null`を記録できることを表します。
- `{}`はプロパティを持たない空のオブジェクトを表します。
- `true`、`false`、`null`、列挙値、JSONのキーはコード表記で示します。

型表では、JSONの型名を次の日本語で表記します。

| 表記 | JSONまたはJSON Schema上の表現 |
| --- | --- |
| 文字列 | `string` |
| 数値 | `number` |
| 整数 | `integer` |
| オブジェクト | `object` |
| 真偽値 | `boolean` |
| 配列 | `array` |
| 列挙値 | JSON Schemaの`enum`で許可された値。JSON自体の型ではない |

型名の後ろに付けた`[]`は、その型の値を要素とする配列を表します。
すべての整数はI-JSONの安全整数範囲で扱い、上限を`9007199254740991`とします。
負の値を許す項目の下限は`-9007199254740991`です。
個別の表に、これより狭い範囲が記載されている場合は、その制約が優先されます。

リファレンスの各ページは、JSON Schemaの内容を本文と表で説明した資料です。
正確な型、必須項目、許可される値、条件付き制約はJSON Schemaファイルで確認してください。
リポジトリ内のソースを変更した場合、JSON Schemaだけでは表せない規則は`hatch run validate`で検証します。
リポジトリ検証の対象には、JSON Schema自体のDraft 2020-12適合性、`$id`と`$ref`、ファイル名と配置、IDとレジストリの参照、ファイル間の対応が含まれます。

## 公開URLとバージョン {#published-schema-urls}

各JSON Schemaの`$id`は、スキーマバージョンと名前空間を含む公開URLです。
現在のスキーマバージョンは`1.0.0`で、URLは次の形式です。

- レンズと関連光学製品：`https://cercidiphyllum.jp/schemas/1.0.0/lenses/<schema-file>`
- マウントアダプター：`https://cercidiphyllum.jp/schemas/1.0.0/adapters/<schema-file>`
- 共通定義：`https://cercidiphyllum.jp/schemas/1.0.0/shared/<schema-file>`

公開したバージョン付きURLとJSON Schemaの内容は変更しません。
データ構造や制約を変更する場合は`schemaVersion`を更新し、旧バージョンも引き続き公開します。
配布データを利用する側でのバージョン確認は、[配布データを使う](../../use-data.md)で説明しています。

## 共通 {#shared-schemas}

共通のJSON Schemaは、両方のデータセットで使う基本定義と、配布用JSONに埋め込む参照情報を検証します。

| JSON Schema | 検証する対象 |
| --- | --- |
| [shared-definitions](shared/shared-definitions.md) | ID、数値、測定条件など、複数のJSON Schemaから参照する定義 |
| [reference-data](shared/reference-data.md) | 配布用JSONのルートに埋め込む、参照IDと表示情報の対応表 |

## レンズと関連光学製品 {#lens-schemas}

レンズと関連光学製品では、配布データ、収録製品データ、調査結果データを別々のJSON Schemaで検証します。

| JSON Schema | 検証する対象 |
| --- | --- |
| [dataset-full](lenses/dataset-full.md) | レンズFull版の配布データ全体 |
| [dataset-light](lenses/dataset-light.md) | レンズLight版の配布データ全体 |
| [product-full](lenses/product-full.md) | レンズFull版の`products[]`に含まれる製品1件 |
| [product-light](lenses/product-light.md) | レンズLight版の`products[]`に含まれる製品1件 |
| [product-record](lenses/product-record.md) | `data/records/lenses/`に置く収録製品データ1件 |
| [product-components](lenses/product-components.md) | 複数の製品種別で使う識別情報、発売情報、マウント、外形などの共通ブロック |
| [product-type-lens](lenses/product-type-lens.md) | レンズの`lens`ブロック |
| [product-type-teleconverter](lenses/product-type-teleconverter.md) | テレコンバーターの`teleconverter`ブロック |
| [product-type-pinhole](lenses/product-type-pinhole.md) | ピンホールの`pinhole`ブロック |
| [research-result](lenses/research-result.md) | `research/results/lenses/`に置く調査結果データ1件 |

## マウントアダプター {#adapter-schemas}

マウントアダプターはレンズと関連光学製品とは異なるデータ構造を使い、Light版を設けません。

| JSON Schema | 検証する対象 |
| --- | --- |
| [dataset-full](adapters/dataset-full.md) | マウントアダプターFull版の配布データ全体 |
| [adapter-full](adapters/adapter-full.md) | マウントアダプターFull版の`adapters[]`に含まれる製品1件 |
| [adapter-record](adapters/adapter-record.md) | `data/records/adapters/`に置く収録製品データ1件 |
| [adapter-components](adapters/adapter-components.md) | マウント変換、電子機能、光学要素、外形などの共通ブロック |
| [research-result](adapters/research-result.md) | `research/results/adapters/`に置く調査結果データ1件 |

## JSON Schemaのライセンス {#schema-license}

`schemas/`配下のJSON SchemaファイルにはMIT Licenseを適用します。
各ファイルの`$comment`にある`SPDX-FileCopyrightText`と`SPDX-License-Identifier: MIT`も、JSON Schemaファイルだけを対象とします。
JSON Schemaで検証する調査結果データ、収録製品データ、レジストリ、配布データには[CC BY 4.0](../../license.md)を適用します。

## 関連ページ

- [データモデル](../../data-model.md)：調査結果データ、収録製品データ、配布データの関係
- [値の読み方](../../value-rules.md)：省略、`null`、空配列、`false`の使い分け
- [レンズと関連光学製品のフィールドリファレンス](../../lens-field-reference.md)：実際の収録製品データを使った項目の説明
- [マウントアダプターのフィールドリファレンス](../../adapter-field-reference.md)：実際の収録製品データを使った項目の説明
- [開発と検証](../../development.md)：生成、リポジトリ検証、ドキュメントのビルド手順
