---
date: '2025-10-05T22:34:38+09:00'
draft: false
title: '準備'
---

## このセクションについて

**準備** では、エージェント開発を始めるための**必須準備**をまとめています。

---

## 目次

1. **[事前準備](./setup.md)**
   必須バージョンの確認、仮想環境（venv）の作成までを手順化。

2. **[リポジトリのクローン](./clone_repo.md)**
   `aiwolf-nlp-agent-llm` を **自分のGitHubにFork → ローカルへClone → upstream登録**。
   併せてログ置き場・評価ツールのフォルダ構成も提案。

3. **[API取得方法](./get_api_key.md)**
   Google AI Studio で **APIキー作成 → `config/.env` 設定**。
   使うLLMは `config.yml` の `llm.type`（`google` / `openai` / `ollama`）で切替。

---

[参加者マニュアルトップへ](../_index.md)\
[前へ（概要）](../overview/_index.md)\
[次へ（実行）](../execution/_index.md)
