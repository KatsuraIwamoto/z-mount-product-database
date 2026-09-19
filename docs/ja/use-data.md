# 配布データを使う

目的に合う公開ファイルを選び、GitHub Releasesから取得し、JavaScriptまたはPythonで読み込むまでの手順を説明します。
初めて利用する場合は、手順1から3までを順に読み、メタデータとスキーマ互換性の説明は必要なときに参照してください。

## 1. 目的に合う配布ファイルを選ぶ {#distribution-files}

正式な配布ファイルは、配布用JSON 3件と製品一覧1件の計4件です。

| 配布データ | 選ぶ場面 |
| --- | --- |
| **レンズFull版**<br>`z-mount-lenses.full.json` | レンズと関連光学製品について、記録されたすべての項目を使う場合。検索、分析、検証、再配布では、このファイルを基本とします。 |
| **レンズLight版**<br>`z-mount-lenses.light.json` | 本プロジェクトの既存Webサイトとの互換性を保ちながら、読み込むデータを小さくしたい場合。 |
| **マウントアダプターFull版**<br>`z-mount-adapters.full.json` | マウントアダプターについて、記録されたすべての項目を使う場合。マウントアダプターにLight版はありません。 |
| **製品一覧**<br>`PRODUCTS.md` | JSONを使わずに、収録製品、調査状況、統計を確認する場合。 |

レンズLight版には、製品名、発売情報、公式製品ページのURL、マウント、寸法、重量、フィルター取付部などの基本情報が含まれます。
レンズの仕様では、焦点距離、開放F値・T値、撮像フォーマット、AF・MFとレンズ内手ぶれ補正の有無、最短撮影距離、最大撮影倍率が含まれます。
操作部、付属品、レンズ構成、コーティングなどの詳細は含みません。
Light版に含まれる項目の一覧は、[レンズLight版のJSON Schemaリファレンス](reference/schemas/lenses/product-light.md)を参照してください。

!!! tip "迷った場合はFull版"
    レンズFull版とレンズLight版には同じ製品が同じ順序で収録され、各製品の `id` も一致します。
    レンズLight版はレンズFull版から項目を減らしたデータであり、Light版だけの値や要約値は追加しません。
    検索や分析で必要な項目が決まっていない場合は、レンズFull版を選んでください。

製品順の一致を保証するのは、`dataVersion`が同じレンズFull版とLight版の間だけです。
リリースをまたいで配列位置を製品の識別に使わず、Full版とLight版を照合する前に`dataVersion`の一致を確認し、`id`で対応付けてください。

!!! note "JSONを使わずに製品を確認する"
    `PRODUCTS.md`では、収録製品、公式製品ページ、調査結果の最終確認日、調査状況を人が読みやすい形式で確認できます。
    3つの配布用JSONと同様に、GitHub Releaseへ添付する正式な配布ファイルです。
    各項目の読み方は、[製品一覧から根拠を確認する](research.md#browse-product-research)で説明しています。

## 2. GitHub Releasesから取得する {#download}

次のリンクは、その時点で最新の配布データを参照します。

- [レンズFull版をダウンロード](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/z-mount-lenses.full.json)
- [レンズLight版をダウンロード](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/z-mount-lenses.light.json)
- [マウントアダプターFull版をダウンロード](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/z-mount-adapters.full.json)
- [製品一覧をダウンロード](https://github.com/KatsuraIwamoto/z-mount-product-database/releases/latest/download/PRODUCTS.md)

最新版のURLは、新しいリリースが公開されると取得内容が変わります。
同じ版を継続して使う場合は、`YYYY.MM.DD` を取得するデータバージョンに置き換えたURLを使います。

```text
https://github.com/KatsuraIwamoto/z-mount-product-database/releases/download/YYYY.MM.DD/z-mount-lenses.full.json
https://github.com/KatsuraIwamoto/z-mount-product-database/releases/download/YYYY.MM.DD/z-mount-lenses.light.json
https://github.com/KatsuraIwamoto/z-mount-product-database/releases/download/YYYY.MM.DD/z-mount-adapters.full.json
https://github.com/KatsuraIwamoto/z-mount-product-database/releases/download/YYYY.MM.DD/PRODUCTS.md
```

分析結果を再現する処理や継続運用する処理では、バージョンを指定したURLを使ってください。
Gitブランチ上の`dist/`とリポジトリ直下の`PRODUCTS.md`は、配布元として使用しません。
公開済みのRelease添付ファイルは置き換えません。
訂正や更新は新しい`dataVersion`のGitHub Releaseで公開し、以前のGitHub Releaseも残します。

## 3. JavaScriptまたはPythonで読み込む {#read-data}

!!! warning "Webアプリでは配布データを自分の配信元に置く"
    GitHub Releasesは配布データの取得元として使い、Webアプリの配信元には使いません。
    本番のWebアプリでは、特定バージョンの配布データをビルド時または更新時に取得し、アプリと同じオリジンまたは利用中のCDNに配置してください。
    ページを表示するたびに、ブラウザからGitHub Releasesへ直接アクセスする構成は避けてください。

次の例は、ダウンロードまたは配置したレンズFull版を読み込み、データバージョン、収録製品数、最初の製品の主な識別情報を表示します。

=== "JavaScript"

    Webサイトのルートにある `/data/` に配布データを配置し、`<script type="module">` または同等のJavaScriptモジュールから読み込む例です。
    配置先が異なる場合は、`fetch()` に指定するパスも変更してください。

    ```javascript
    const response = await fetch("/data/z-mount-lenses.full.json");

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const dataset = await response.json();
    const firstProduct = dataset.products[0];
    const manufacturerId = firstProduct.identity.manufacturerId;
    const brandId = firstProduct.identity.brandId;
    const output = {
      dataVersion: dataset.dataVersion,
      recordCount: dataset.recordCount,
      firstProduct: {
        id: firstProduct.id,
        productType: firstProduct.productType,
        identity: {
          manufacturerId,
          manufacturerName: dataset.referenceData.manufacturers[manufacturerId].name,
          brandId,
          brandName: dataset.referenceData.brands[brandId].name,
          productName: firstProduct.identity.productName,
        },
      },
    };

    console.log(JSON.stringify(output, null, 2));
    ```

=== "Python"

    ダウンロードした配布データを、Pythonの標準ライブラリで読み込む例です。

    ```python
    import json
    from pathlib import Path

    path = Path("z-mount-lenses.full.json")
    with path.open(encoding="utf-8") as file:
        dataset = json.load(file)

    first_product = dataset["products"][0]
    manufacturer_id = first_product["identity"]["manufacturerId"]
    brand_id = first_product["identity"]["brandId"]
    output = {
        "dataVersion": dataset["dataVersion"],
        "recordCount": dataset["recordCount"],
        "firstProduct": {
            "id": first_product["id"],
            "productType": first_product["productType"],
            "identity": {
                "manufacturerId": manufacturer_id,
                "manufacturerName": dataset["referenceData"]["manufacturers"][manufacturer_id]["name"],
                "brandId": brand_id,
                "brandName": dataset["referenceData"]["brands"][brand_id]["name"],
                "productName": first_product["identity"]["productName"],
            },
        },
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    ```

### 実際の出力

データバージョン `2026.09.19` のレンズFull版では、どちらのコードも次の内容を表示します。

```json
{
  "dataVersion": "2026.09.19",
  "recordCount": 606,
  "firstProduct": {
    "id": "7artisans-24mm-f1-4",
    "productType": "lens",
    "identity": {
      "manufacturerId": "7artisans",
      "manufacturerName": "7Artisans",
      "brandId": "7artisans",
      "brandName": "7Artisans",
      "productName": "7Artisans 24mm F1.4"
    }
  }
}
```

`dataVersion` と `recordCount` は配布データのルートにあるメタデータです。
`firstProduct` は、最初の収録製品である `products[0]` から、例で使う項目をまとめた出力です。
メーカーとブランドのIDは製品から取得し、表示名は同じ配布用JSONの`referenceData`から参照しています。

### ルート直下の製品配列の違い

| 配布データ | 収録製品が入るルート直下の配列 |
| --- | --- |
| レンズFull版 | `products` |
| レンズLight版 | `products` |
| マウントアダプターFull版 | `adapters` |

マウントアダプターFull版を読む場合は、読み込むファイルを `z-mount-adapters.full.json` に変更し、`products` の代わりに `adapters` を読みます。
ルート直下の製品配列の名前は異なりますが、次に示すメタデータ項目は3つの配布データに共通します。

### 条件に合うレンズを検索する

次のPythonコードは、先ほど読み込んだレンズFull版から、最大撮像フォーマットが`full-frame`で、AFに対応するレンズを検索し、製品IDと製品名を表示します。

```python
matches = {
    product["id"]: product["identity"]["productName"]
    for product in dataset["products"]
    if product["productType"] == "lens"
    and (coverage := product["lens"]["coverage"]) is not None
    and coverage["format"] == "full-frame"
    and (autofocus := product["lens"]["focus"]["autofocus"]) is not None
    and autofocus["present"] is True
}

print(json.dumps(matches, ensure_ascii=False, indent=2))
```

`coverage`や`autofocus`が`null`の場合は採用できる公開情報で確認できないため、条件に合うとは判定しません。
`autofocus.present`が`false`の場合も、AFに対応しないことを確認しているため除外します。
項目の省略、`null`、空配列、`false`は意味が異なるため、判定や表示の前に[値の読み方](value-rules.md#value-states)を確認してください。

!!! info "基本的な利用はここまでです"
    以降は、配布データの更新確認やJSON Schemaによる検証が必要なときに参照してください。

## 製品IDを保存するときは名前空間を含める {#product-keys}

製品を一意に識別するには、配布データの名前空間（namespace）と`id`の複合キーを使います。

| 配布ファイル | 名前空間 | 複合キー |
| --- | --- | --- |
| `z-mount-lenses.full.json` | `lenses` | `("lenses", id)` |
| `z-mount-lenses.light.json` | `lenses` | `("lenses", id)` |
| `z-mount-adapters.full.json` | `adapters` | `("adapters", id)` |

レンズFull版とLight版は同じ`lenses`名前空間を共有します。
`id`は名前空間内で一意です。
`lenses`と`adapters`では同じ`id`を使用できます。
複数の配布データを一つのデータベースへ取り込む場合は、`id`単体を主キーにせず、名前空間も保存してください。

名前空間を表す新しいJSONフィールドはありません。
取得した配布ファイルの種類から判定します。

`id`は、ブランド名や製品名をもとに、小文字英数字をハイフンで区切った、人が読めるスラッグ形式のIDです。
ただし、スラッグ内の語と製品情報との対応関係は、公開データの仕様に含まれません。
ブランド、メーカー、製品名、焦点距離、F値、世代、製品種別などは`id`から解析せず、表示、検索、分類には`identity`と各専用フィールドを使用してください。

本プロジェクトがGitHub Releasesで初めて正式公開した後は、この複合キーを変更しません。
公開済みの`id`を別の製品に割り当てたり、削除後に再利用したりもしません。
同じ製品を再び収録する場合は、以前と同じ`id`を使用します。
ただし、その製品が最新版や以後のすべてのリリースに収録され続けるとは限りません。
統合、分割、削除、データセット間の再分類が発生した場合は、リリースノートで以前の複合キーと移行先、または移行先がないことを確認してください。

`manufacturerId`、`brandId`、各マウントシステムIDも、最初の公開後は固定します。
名称が変わった場合は`referenceData`内の`name`を更新し、公開済みIDの改名や再利用は行いません。

## ルートのメタデータを確認する {#root-metadata}

各配布データのルートには、版、件数、ハッシュ値、ライセンスなどのメタデータがあります。
プロジェクト全体の名称は「Z Mount Product Database」ですが、`datasetName` にはデータセットごとの名称が入ります。
次の例は、データバージョン `2026.09.19` の各配布データから、`referenceData`と`products`または`adapters`を除いて抜き出したものです。

=== "レンズFull版"

    ```json
    {
      "$schema": "https://cercidiphyllum.jp/schemas/1.0.0/lenses/dataset-full.schema.json",
      "datasetName": "Z Mount Lens Database",
      "datasetVariant": "full",
      "schemaVersion": "1.0.0",
      "dataVersion": "2026.09.19",
      "creator": "Katsura Iwamoto",
      "license": "CC-BY-4.0",
      "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
      "repositoryUrl": "https://github.com/KatsuraIwamoto/z-mount-product-database",
      "recordCount": 606,
      "contentHash": "sha256:3c5acd5353ff4d81b1eddffbc21fdc7b19fcdf9ebf6e92895b7a620c13e86275"
    }
    ```

=== "レンズLight版"

    ```json
    {
      "$schema": "https://cercidiphyllum.jp/schemas/1.0.0/lenses/dataset-light.schema.json",
      "datasetName": "Z Mount Lens Database",
      "datasetVariant": "light",
      "schemaVersion": "1.0.0",
      "dataVersion": "2026.09.19",
      "creator": "Katsura Iwamoto",
      "license": "CC-BY-4.0",
      "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
      "repositoryUrl": "https://github.com/KatsuraIwamoto/z-mount-product-database",
      "recordCount": 606,
      "contentHash": "sha256:1a8e417780758c75f790884e471b9a43fbf3a9ce746596a91bf91b9b4cf48d8d"
    }
    ```

=== "アダプターFull版"

    ```json
    {
      "$schema": "https://cercidiphyllum.jp/schemas/1.0.0/adapters/dataset-full.schema.json",
      "datasetName": "Z Mount Adapter Database",
      "datasetVariant": "full",
      "schemaVersion": "1.0.0",
      "dataVersion": "2026.09.19",
      "creator": "Katsura Iwamoto",
      "license": "CC-BY-4.0",
      "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
      "repositoryUrl": "https://github.com/KatsuraIwamoto/z-mount-product-database",
      "recordCount": 445,
      "contentHash": "sha256:7459f1ac4108d9772bd6628e1d57d8f802f74f0145351cccf82e8d2d41faf55c"
    }
    ```

`dataVersion`、`recordCount`、`contentHash` は、この例を作成した時点の値です。
実際に利用する値は、取得した配布データで確認してください。

| 項目 | 確認できること |
| --- | --- |
| `$schema` | この配布データの検証に使うJSON SchemaのURL。 |
| `datasetName` | 配布データに収録されているデータセットの名称。 |
| `datasetVariant` | Full版かLight版か。値は `full` または `light` です。 |
| `schemaVersion` | 対応するJSON Schema一式のバージョン。SemVer形式です。 |
| `dataVersion` | 本プロジェクトのデータリリース識別子。`YYYY.MM.DD`形式で、Gitタグにも同じ値を使います。 |
| `creator` | 配布データの作成者。 |
| `license`、`licenseUrl` | 配布データに適用されるライセンスのSPDX識別子とURL。 |
| `repositoryUrl` | 配布データを管理するリポジトリのURL。 |
| `recordCount` | `products` または `adapters` に含まれる収録製品数。 |
| `referenceData` | 製品が参照するメーカーID、ブランドID、マウントシステムIDと表示情報の対応表。 |
| `contentHash` | 配布データの内容を照合するためのSHA-256ハッシュ値。`referenceData`と`products`または`adapters`を含む内容オブジェクトを[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785)に従って正規化して計算します。 |

`contentHash`は、RFC 8785による正規化結果のUTF-8バイト列から計算し、`sha256:`と小文字16進数64桁で表します。
`$schema`、`schemaVersion`、`dataVersion`、`recordCount`などのルートメタデータと、配布JSON全体の空白や改行は計算対象に含めません。
数値はRFC 8785が前提とするI-JSONの範囲で扱います。
この値は参照データと製品配列の内容照合に使うものであり、配布元の真正性やGitHub Releaseの添付ファイル全体が公開後に変更されていないことは保証しません。

更新の有無を確認する場合は `dataVersion` を比較し、内容が同一かを照合する場合は `contentHash` を比較します。

## スキーマ変更では互換性を確認する {#schema-versioning}

3つの配布データは同じ `schemaVersion` を共有しますが、レンズデータセットとマウントアダプターのデータセットでは異なるJSON Schemaを使います。
検証には、配布データの `$schema` に記載されたURLを使ってください。

公開済みのバージョン付きJSON Schemaは、URLと内容を変更しません。
スキーマの構造や制約を変更するときは `schemaVersion` を更新し、旧版も引き続き公開します。
収録内容だけを更新する場合は、`schemaVersion` を変えずに `dataVersion` を更新します。

| 変更の種類 | `schemaVersion` の上げ方 |
| --- | --- |
| 検証結果、配布データの出力、値の意味を変えないJSON Schema上の訂正 | `patch` |
| 既存形式を変えない独立したJSON Schemaや配布形式の追加、既存フィールドを有効なまま非推奨化する変更 | `minor` |
| 既存JSON Schemaの検証結果、配布データの出力保証、値の意味を変える変更（フィールドや列挙値の追加、制約の緩和や強化を含む） | `major` |

互換性は、新しいGitHub Releaseの配布データを既存のプログラムで扱えるかどうかを基準に判定します。
同じ`major`の既知の配布形式は受け入れられますが、検証には必ず配布データ自身の`$schema`が示す版を使い、旧版のJSON Schemaを代用しないでください。
`schemaVersion`が同じでも、`dataVersion`の更新では製品の追加、削除、訂正、配列位置の変更や、既存の仕様ですでに許可されている値が初めて現れることがあります。

スキーマバージョンが変わった場合は、移行前にリリースノートを確認してください。
レンズと関連光学製品の項目は[レンズと関連光学製品のフィールドリファレンス](lens-field-reference.md)、マウントアダプターの項目は[マウントアダプターのフィールドリファレンス](adapter-field-reference.md)で確認できます。
正確な型と制約は[JSON Schemaリファレンス](reference/schemas/index.md)を参照してください。

## JSON Schemaで検証してから更新する {#validate-data}

継続運用では、新しく取得したファイルをそのまま現在使用中のファイルへ上書きせず、別の場所で検証してから切り替えます。
次の例はレンズFull版を対象に、配布データの`$schema`が示すJSON Schemaによる検証、`recordCount`と`contentHash`の照合がすべて成功した場合だけ、現在使用中のファイルを置き換えます。
取得、JSONの解析、検証、照合のいずれかに失敗した場合は、以前のファイルを残します。

最初に、検証するGitHub Releaseを一つ選びます。
次の`YYYY.MM.DD`を、そのReleaseの`dataVersion`にすべて置き換え、空の作業ディレクトリで実行してください。
配布データと同じGitタグからJSON Schema一式を取得します。

```shell
git clone --depth 1 --branch YYYY.MM.DD --single-branch \
  https://github.com/KatsuraIwamoto/z-mount-product-database.git \
  schema-source-YYYY.MM.DD
git -C schema-source-YYYY.MM.DD describe --tags --exact-match
cp -R schema-source-YYYY.MM.DD/schemas ./schemas
```

`git describe`の出力が選んだ`YYYY.MM.DD`と一致した場合だけ、取得した`schemas/`を使用します。
このタグは配布データの`dataVersion`と一致し、公開後は移動しません。
`schemas/`には、配布データの検証に使うJSON Schemaと、それらが`$ref`で参照する依存先が、必要なディレクトリ構造のまま含まれます。
別の版へ更新するときは新しい作業ディレクトリを使うか、`schemas/`全体を対応するタグの内容へ入れ替え、異なるタグのファイルを混在させないでください。

まず、検証に使うライブラリをインストールします。

```shell
python -m pip install "jsonschema>=4.23,<5" "referencing>=0.28.4,<1" "rfc3986-validator>=0.1.1,<1" "rfc8785>=0.1.4,<1"
```

対応する版のJSON Schema一式を`schemas/`に保存してから、次のコードを実行します。
未知の`$schema`は自動取得せず、更新を停止します。
重複したオブジェクトキーと`NaN`、`Infinity`、`-Infinity`もJSONの解析時に拒否します。
Draft 2020-12の`format`をURI検査に使うため、`rfc3986-validator`をインストールし、検証時に`FormatChecker`を明示します。

```python
import json
from hashlib import sha256
from pathlib import Path
from urllib.request import urlopen

import rfc8785
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


def object_without_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def reject_nonfinite_number(value):
    raise ValueError(f"non-finite JSON number: {value}")


expected_data_version = "YYYY.MM.DD"
data_url = (
    "https://github.com/KatsuraIwamoto/z-mount-product-database/"
    f"releases/download/{expected_data_version}/z-mount-lenses.full.json"
)
current_path = Path("current/z-mount-lenses.full.json")

schemas = {}
resources = []
for path in Path("schemas").rglob("*.schema.json"):
    schema = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=object_without_duplicate_keys,
        parse_constant=reject_nonfinite_number,
    )
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError(f"unsupported schema dialect: {path}")
    Draft202012Validator.check_schema(schema)
    if isinstance(schema.get("$id"), str):
        schemas[schema["$id"]] = schema
        resources.append((schema["$id"], Resource.from_contents(schema)))

with urlopen(data_url, timeout=30) as response:
    raw = response.read()
candidate = json.loads(
    raw,
    object_pairs_hook=object_without_duplicate_keys,
    parse_constant=reject_nonfinite_number,
)

if not isinstance(candidate, dict):
    raise ValueError("distribution root must be an object")
if candidate.get("dataVersion") != expected_data_version:
    raise ValueError("unexpected dataVersion")
if (candidate.get("datasetName"), candidate.get("datasetVariant")) != (
    "Z Mount Lens Database",
    "full",
):
    raise ValueError("unexpected distribution")

schema_url = candidate.get("$schema")
if not isinstance(schema_url, str) or schema_url not in schemas:
    raise ValueError(f"unsupported schema: {schema_url}")

Draft202012Validator(
    schemas[schema_url],
    registry=Registry().with_resources(resources),
    format_checker=FormatChecker(),
).validate(candidate)

products = candidate["products"]
if candidate["recordCount"] != len(products):
    raise ValueError("recordCount does not match products")
hash_payload = {
    "referenceData": candidate["referenceData"],
    "products": products,
}
actual_hash = "sha256:" + sha256(rfc8785.dumps(hash_payload)).hexdigest()
if candidate["contentHash"] != actual_hash:
    raise ValueError("contentHash does not match products")

current_path.parent.mkdir(parents=True, exist_ok=True)
staged_path = current_path.with_name(f".{current_path.name}.tmp")
staged_path.write_bytes(raw)
staged_path.replace(current_path)
```

一時ファイルを現行ファイルと同じディレクトリに作り、最後の`replace()`だけで切り替えます。
`expected_data_version`には、JSON Schema一式を取得したGitタグと同じ値を指定します。
新しいReleaseへ更新するときは、配布データの固定版URLとJSON Schema一式のタグを一緒に変更してください。
この例の`contentHash`照合は参照データと製品配列の内部整合性を確認するもので、配布元の真正性を証明するものではありません。

## データを共有するときはクレジットを表示する {#attribution}

収録製品データ、調査結果データ、3つの配布用JSON、`PRODUCTS.md`は、[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)で利用できます。
推奨するクレジット表記は次のとおりです。

> Z Mount Product Database, Katsura Iwamoto, CC BY 4.0, https://github.com/KatsuraIwamoto/z-mount-product-database

変更したデータを共有する場合は、変更したことも明記してください。
この節は主な内容の概要であり、すべての条件を網羅するものではありません。
正確な適用範囲、無保証、第三者の権利、正式なライセンス本文への導線は、[ライセンス](license.md)を参照してください。

## 誤りや未収録製品を報告する {#report-data-issues}

[製品の追加・修正フォーム](https://github.com/KatsuraIwamoto/z-mount-product-database/issues/new?template=data-correction.yml)から、製品名、気になった内容、分かればメーカーまたはブランドの公式URLを報告してください。
JSONやJSON Schemaを書く必要はありません。
