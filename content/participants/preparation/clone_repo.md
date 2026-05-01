---
date: '2026-04-20T14:00:00+09:00'
draft: false
title: 'リポジトリのクローン'
category: participants_guide
---

こちらのページでは、公式のサンプルエージェント [aiwolf-nlp-agent-llm](https://github.com/aiwolfdial/aiwolf-nlp-agent-llm) を手元に持ってきて、依存関係をインストールするまでの流れを説明します。

手順はおおまかに次の3段階です。

1. **Fork**：公式リポジトリを自分のGitHubアカウントにコピーする
2. **Clone**：自分のForkをローカルに取ってくる
3. **依存関係のインストール**：Pythonのライブラリを入れる

> GitHubの基礎知識があやしい方は、先に [GitとGitHub](../background/about_github.md) をご覧ください。

---

## 作業用のフォルダを作る

まずは関連ファイルをまとめる場所を作っておきます。

```bash
mkdir -p ~/aiwolfdial
cd ~/aiwolfdial
```

以降のコマンドは、基本的にこの `~/aiwolfdial` の中で実行してください。

---

## GitHub で Fork する

1. ブラウザで公式リポジトリを開きます：[aiwolfdial/aiwolf-nlp-agent-llm](https://github.com/aiwolfdial/aiwolf-nlp-agent-llm)
2. 右上の **Fork** ボタンを押します。
3. 自分のアカウント名の下にコピーが作成されれば成功です。

> Fork しておくと、自分が書いたコードを `git push` で気軽に保存できますし、大会終了後に他の参加者に公開することもできます。

---

## 自分の Fork をクローンする

GitHub の自分の Fork ページから、クローン用のURLをコピーして実行します（`<username>` は自分のGitHubユーザー名に置き換えてください）。

```bash
cd ~/aiwolfdial
git clone https://github.com/<username>/aiwolf-nlp-agent-llm.git
cd aiwolf-nlp-agent-llm
```

> SSH接続を設定している方は `git@github.com:<username>/aiwolf-nlp-agent-llm.git` を使ってください。

---

## 公式の更新を取り込めるようにする（任意）

大会期間中、公式リポジトリに修正が入ることがあります。
公式側の更新を後から取り込めるように、`upstream` という名前で公式を登録しておきましょう。

```bash
git remote add upstream https://github.com/aiwolfdial/aiwolf-nlp-agent-llm.git
git remote -v
```

出力に `origin`（自分のFork）と `upstream`（公式）の両方が並んでいればOKです。

公式の更新を取り込みたくなったら、以下のコマンドで取得できます。

```bash
git fetch upstream
git merge upstream/main
```

---

## 設定ファイルを準備する

エージェントは `config/config.yml` を読み込んで動きます。サンプル設定をコピーしてファイルを作りましょう。

```bash
# 日本語プロンプトを使う場合（おすすめ）
cp config/config.jp.yml.example config/config.yml

# 英語プロンプトを使いたい場合はこちら
# cp config/config.en.yml.example config/config.yml
```

APIキーを書き込むための `.env` ファイルも準備しておきます。

```bash
cp config/.env.example config/.env
```

> `.env` に書き込むキーの取得方法は次のページ [APIキーの取得と設定](./get_api_key.md) で説明します。

---

## 依存関係をインストールする

### uv を使う場合（おすすめ）

```bash
uv sync
```

これだけで必要なPythonのライブラリがすべて入ります。あとから `uv run python src/main.py` のように実行するだけでエージェントが動きます。

### uv を使わない場合

従来の `venv` + `pip` でもインストールできます。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

この場合、以降の作業では毎回 `source .venv/bin/activate` で仮想環境を有効化してから実行してください。

---

## ここまでで完了したこと

* 公式リポジトリを Fork してクローンできた
* `config/config.yml` と `config/.env` を用意した
* Pythonの依存関係をインストールできた

次はAPIキーを取得して `.env` に書き込みます。

---

[参加者マニュアルトップへ](../_index.md)\
[準備トップへ](./_index.md)\
[前へ（開発環境の準備）](./setup.md)\
[次へ（APIキーの取得と設定）](./get_api_key.md)
