# FastAPIとAmazon Aurora Serverless V2を使った外形監視アプリ

## 概要

このアプリケーションは、FastAPIとAmazon Aurora Serverless V2を使った外形監視アプリです。

## 使用方法

### 事前準備

cfnディレクトリ配下のCloudFormationテンプレートを使って、AWSリソースを作成します。

1. vpc.yml
2. db.yml

本プログラムは、AWS App Runnerで稼働させることを想定しています。
App Runnerと本リポジトリを接続することでデプロイします。

## 開発

### 依存ライブラリのインストール

```
pipenv install --dev
```
Pipfile.lock が作成されるので、Gitの管理対象としてCommitする必要有り。

### ユニットテストの実行
tests/unit/test_handler.pyに定義されたテストの実行
（以下コマンド実行前に$ pipenv shellで仮想環境に入る必要あり）

```
pipenv run pytest -v -s
```

### コードフォーマットの実行（コードの自動整形）
isortとblackを使用。isortはblackが対応していないimport文の並び替えなどを行う。
（以下コマンド実行前に$ pipenv shellで仮想環境に入る必要あり）

```
pipenv run format
```

### Lintの実行(PEP8にもとづくコードの静的解析)
（以下コマンド実行前に$ pipenv shellで仮想環境に入る必要あり）

```
pipenv run lint
```

## メモ

CFnでRDSを作る時のEngineVersionの選択肢を確認するコマンド

```bash
aws rds describe-db-engine-versions --engine aurora-mysql --query 'DBEngineVersions[].EngineVersion'
```

AWS Secrets Managerからシークレットを取得するコマンド

```
aws secretsmanager get-secret-value --secret-id '{シークレットIDまたはシークレット名}'
```