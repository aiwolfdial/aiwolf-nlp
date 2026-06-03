---
date: '2026-04-20T14:00:00+09:00'
draft: false
title: '背景知識'
---

## このセクションについて

エージェント開発をするうえで **あると便利な基礎知識** をまとめています。
「コマンドラインって何？」「Gitってどう使うの？」といった、開発の土台になるところを解説しています。

すでにご存じの方は読み飛ばして構いません。辞書的に、必要なときだけ戻ってきてください。

---

## 目次

1. **[WSLとLinux](./about_wsl.md)**\
   Windows で開発する方向けに、WSL（Windows Subsystem for Linux）と Linux とは何か、その導入方法を説明します。

2. **[ターミナル操作とコマンド](./about_terminal.md)**\
   ターミナルの読み方から、よく使う Linux コマンド・オプション・隠しファイル・リダイレクトまで、実際の操作を辞書的にまとめます。

3. **[GitとGitHub](./about_github.md)**\
   バージョン管理ツール Git と、コードを共有する GitHub の基礎を説明します。Fork・Clone・Push・README など、本マニュアルで出てくる用語がここに書かれています。

4. **[仮想環境とは](./virtual_env.md)**\
   Pythonの仮想環境の必要性と、よく使われるツール（venv・uv・poetry など）の違いを説明します。

5. **[WebSocketとは](./about_websocket.md)**\
   サーバとエージェントの通信に使われている WebSocket について、HTTPとの違いも交えて説明します。

6. **[Jinja2テンプレートとは](./about_jinja2.md)**\
   `config.yml` の `prompt` で使われているテンプレートエンジン Jinja2 の基本文法（`{{ }}` ・`{% %}`・ハイフンによる空白制御など）を解説します。

7. **[YAMLとは](./about_yaml.md)**\
   `config.yml` の文法であるYAMLの基本（辞書・リスト・複数行文字列・インデントの罠）を解説します。

8. **[LLMとのチャットはどうなっている？](./about_llm_chat.md)**\
   ライブラリに依らない前提知識として、「LLM は記憶を持たず、会話を続けるには過去のやり取りを毎回まとめて送り直す（＝マルチターン）」という仕組みを解説します。

9. **[LangChainとは](./about_langchain.md)**\
   サンプルエージェントが LLM 呼び出しに使っている LangChain の最低限の語彙（`ChatModel` / `HumanMessage` / `\|` チェーン）を解説します。
   * ☛ 【実習】**[OpenRouter APIを追加する](./exercise_openrouter.md)**\
     LangChain で実際にAPIを使う流れを、サンプルエージェントに新しいLLMプロバイダを追加することで手を動かして学びます。

10. **[サンプルの履歴管理](./about_history.md)**\
    上記のマルチターンを、サンプルエージェントが実際のコードでどう実装しているか（`llm_message_history` への積み方、ゲーム内発言の `talk_history` との違い、ゲーム間のリセット）を解説します。

11. **[環境変数と.envファイル](./about_env_vars.md)**\
    APIキーの管理に使われている環境変数の概念、`.env` ファイルの書き方、隠しファイル慣習、`python-dotenv`、`.gitignore` での除外などをまとめます。

---

[参加者マニュアルトップへ](../_index.md)\
[前へ（応用編）](../extras/_index.md)
