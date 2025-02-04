#!/bin/bash

# 開発環境のセットアップスクリプト

# Poetry のインストール
pip install poetry

# 仮想環境の作成 & 依存関係のインストール
poetry install

# pre-commit のインストール
poetry run pre-commit install

# Linter のインストール
poetry add --dev flake8 black isort

# テストフレームワークのインストール
poetry add --dev pytest

# 型チェックツールのインストール
poetry add --dev mypy

echo "開発環境のセットアップが完了しました。"
