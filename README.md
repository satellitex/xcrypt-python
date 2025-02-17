# Xcrypt Transformer

## 概要
Xcrypt Transformer は Python の AST (Abstract Syntax Tree) を解析し、
対応する Perl (Xcrypt) コードに変換するツールです。

## 環境構築
本プロジェクトでは `poetry` を使用して依存関係を管理します。

### 1. Poetry のインストール
Poetry がインストールされていない場合は、以下のコマンドを実行してください。

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

または、pip を使用してインストールできます。

```sh
pip install poetry
```

### 2. プロジェクトのセットアップ
Poetry を使用してプロジェクトの環境をセットアップします。

```sh
poetry install
```

### 3. 仮想環境の有効化

```sh
poetry shell
```

## `perltidy` のインストール
本プロジェクトでは、Xcrypt で生成された Perl コードを整形するために `perltidy` を使用します。
`perltidy` をインストールするには、以下のコマンドを実行してください。

```sh
cpan install Perl::Tidy
```

または、以下の方法でもインストールできます。

```sh
sudo apt-get install perltidy  # Ubuntu/Debian
brew install perltidy          # macOS
```

## 使い方
Xcrypt Transformer を使用して Python コードを Xcrypt に変換するには、
関数に `@Xcrypt` デコレータを付けて実行してください。

### 1. 変換対象の関数を作成
```python
@Xcrypt
def sample():
    from qw import bulk, core
    bulk.initialize(max_time=16384)
    
    template = {
        'RANGE0': [30, 40],
        'RANGE1': list(range(5)),
        'id': 'jobbulktime',
        'exe0': 'bin/fib',
        'arg0_0@': lambda VALUE: VALUE[0] + VALUE[1],
        'time@': lambda VALUE: 2 ** (VALUE[0] + VALUE[1] - 30),
    }

    jobs = core.prepare(template)
    print("ID              \testimated time")
    for j in jobs:
        print(f"{j['id']}\t{j['time']}")

    bulkedjobs = bulk.bulk('bulktim', jobs)
    core.submit(bulkedjobs)
    core.sync(bulkedjobs)
```

### 2. 実行

```sh
poetry run python script.py
```

変換された Xcrypt コードが出力されます。

## ライセンス
本プロジェクトは MIT ライセンスの下で提供されます。

