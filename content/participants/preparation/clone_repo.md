---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: 'リポジトリのクローン'
category: participants_guide
---

このページでは、公式リポジトリ aiwolfdial/aiwolf-nlp-agent-llm を 自分の GitHub アカウントへ Fork し、その Fork をローカルへクローン、さらに 配布元を upstream として登録 するまでを説明します。

---

## 作業用ディレクトリを作る

今後の管理を楽にするため、まずは上位フォルダを用意しておきます。

```bash
mkdir -p ~/aiwolfdial
cd ~/aiwolfdial
```

> 以降のクローンは、基本的にこの `~/aiwolfdial` の直下で行います。

---

## GitHub 上で Fork を作成する

1. ブラウザで公式リポジトリにアクセス：
   `https://github.com/aiwolfdial/aiwolf-nlp-agent-llm`
2. 右上の **Fork** ボタンを押して、自分のアカウントに Fork を作成します。
   （リポジトリ名はデフォルトのままで OK）

> Fork を使うと、`origin` が最初から **自分のリポジトリ** になるため、push 先の変更作業が不要で分かりやすいです。

---

## 自分の Fork をローカルへクローン

GitHub で自分のアカウント側にできた Fork のページを開き、**自分のリポジトリ URL** を使ってクローンします（`username` は自分のユーザー名に置き換え）。

```bash
cd ~/aiwolfdial

# HTTPS 例（推奨）
git clone https://github.com/<username>/aiwolf-nlp-agent-llm.git

# プロジェクトフォルダへ移動
cd aiwolf-nlp-agent-llm
```

> SSH を使う場合は `git@github.com:<username>/aiwolf-nlp-agent-llm.git` を利用します。

---

## 配布元を upstream として登録（更新の取り込み用）

配布元（公式）からの更新を取り込めるよう、`upstream` を追加します。

```bash
git remote add upstream https://github.com/aiwolfdial/aiwolf-nlp-agent-llm.git
git remote -v
```

出力例（`origin` が自分、`upstream` が公式になっていればOK）:

```bash
origin    https://github.com/<username>/aiwolf-nlp-agent-llm.git (fetch)
origin    https://github.com/<username>/aiwolf-nlp-agent-llm.git (push)
upstream  https://github.com/aiwolfdial/aiwolf-nlp-agent-llm.git (fetch)
upstream  https://github.com/aiwolfdial/aiwolf-nlp-agent-llm.git (push)
```

---

## 公式の更新を取り込むとき

Fork で作業していると、公式リポジトリに更新が入ることがあります。
定期的に取り込んで差分を解消しましょう。

```bash
# 公式から取得
git fetch upstream

# 例：main ブランチに取り込む
git checkout main
git merge upstream/main    # あるいは git rebase upstream/main
```

> コンフリクト（衝突）が出た場合は、該当ファイルを手で解消してコミットします。

---

## 環境構築

以下のコマンドで環境を構築します。

```bash
# 日本語のプロンプトを使用したい場合
cp config/config.jp.yml.example config/config.yml
# 英語のプロンプトを使用したい場合
# cp config/config.en.yml.example config/config.yml
cp config/.env.example config/.env
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## フォルダ構成の目安（推奨セットアップ）

将来的に「実行」「評価」「強化」の各ドキュメントと行き来しやすいよう、**同じ親ディレクトリ（`~/aiwolfdial`）に関連ツールを並べる**構成を推奨します。
まずは、ログ置き場と、ローカル対戦サーバ／評価ツールをこのタイミングで用意しておくとスムーズです。

```bash
# 作業用ルートへ
cd ~/aiwolfdial

# 1) ログ置き場（execution/server.md で詳説）
mkdir -p aiwolf-nlp-game-logs

# 2) ローカル対戦サーバ（extras/local_battle_setup.md で詳説）
git clone https://github.com/<username>/aiwolf-nlp-server.git

# 3) LLM Judge（evaluation/llm_judge_usage.md で詳説）
git clone https://github.com/<username>/aiwolf-nlp-llm-judge.git
```

フォルダ構成イメージは以下の通りです。

```text
~/aiwolfdial/
├── aiwolf-nlp-agent-llm/   # ← 本ページの手順で Fork & Clone したメイン開発用
├── aiwolf-nlp-game-logs/   # ゲームログファイルの置き場（Git管理外 推奨）
├── aiwolf-nlp-server/      # ローカル対戦・検証用サーバ
└── aiwolf-nlp-llm-judge/   # 主観評価用ツール
```

---

[参加者マニュアルトップへ](../_index.md)\
[準備トップへ](./_index.md)\
[前へ（事前準備）](./setup.md)\
[次へ（API取得方法）](./get_api_key.md)
