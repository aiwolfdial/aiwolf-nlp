---
date: '2026-04-26T14:00:00+09:00'
draft: false
title: '参加者向けマニュアル'
cascade:
  ShowLastMod: true
---

このマニュアルでは、人狼知能大会（自然言語部門）に参加するうえで必要なことを、はじめての方でも進められるようにまとめています。
大会のルールや仕組みから、サンプルエージェント [aiwolf-nlp-agent-llm](https://github.com/aiwolfdial/aiwolf-nlp-agent-llm) の動かし方、設定の変更方法、結果の確認、エージェントの改良までを扱います。

「順に読んで進める」「困ったときに辞書的に開く」のどちらの使い方でも問題ありません。各章は独立していますが、上から順に読むと実際の作業順になるのでスムーズです。

> **マニュアルの鮮度について**：本マニュアルは可能な限り最新の状態を保つよう努めていますが、サンプルエージェントや大会サーバが更新されてから本マニュアルへ反映されるまでにタイムラグが生じる場合があります。
> **各ページの最終更新日** はページ本文の上部または下部に表示されます。動作確認時は、最新のサンプルコードや運営の最新告知もあわせてご確認ください。

---

## ページ一覧

| セクション | 内容 | ページ |
|---|---|---|
| [**概要**](./overview/_index.md) | ゲームと大会の全体像を知る | [人狼ゲームとは](./overview/werewolf_overview.md) |
| | | [大会のルールとゲームの流れ](./overview/aiwolf_logic.md) |
| | | [エージェントとサーバの仕組み](./overview/system_mechanism.md) |
| | | [サーバから届くデータ](./overview/server_data.md) |
| | | [関連リポジトリの紹介](./overview/aiwolfdial_repo.md) |
| [**準備**](./preparation/_index.md) | 開発環境を整える | [開発環境の準備](./preparation/setup.md) |
| | | [リポジトリのクローン](./preparation/clone_repo.md) |
| | | [APIキーの取得と設定](./preparation/get_api_key.md) |
| [**実行**](./execution/_index.md) | ローカルで動かしてみる | [サーバの起動方法](./execution/server.md) |
| | | [エージェントの起動方法](./execution/agent.md) |
| [**確認・評価**](./evaluation/_index.md) | 結果を見て強さを測る | [ゲームログの見方](./evaluation/game_log_guide.md) |
| | | [エージェントログの見方](./evaluation/agent_log_guide.md) |
| | | [ビュアーの使い方](./evaluation/viewer_usage.md) |
| | | [勝率の計算方法](./evaluation/winrate_calculation.md) |
| | | [LLM Judgeの使い方](./evaluation/llm_judge_usage.md) |
| [**改良・拡張**](./enhancement/_index.md) | エージェントを強くする | [改良のヒントと課題点](./enhancement/improvement_tips.md) |
| | | [ソースコードの構成](./enhancement/nlp_agent_structure.md) |
| | | [config.ymlの説明](./enhancement/config_explanation.md) |
| | | [エージェントの内部状態とデータの流れ](./enhancement/agent_state.md) |
| | | [プロンプトエンジニアリング](./enhancement/prompt_engineering.md) |
| | | [エージェントのカスタマイズ方法](./enhancement/customize_agent.md) |
| | | [LLMとのやり取りパターン](./enhancement/llm_interaction_patterns.md) |
| [**大会**](./competition/_index.md) | 本番のサーバに接続する | [大会の進め方（全体像）](./competition/competition.md) |
| | | [予選編](./competition/qualifying.md) |
| | | [本戦編](./competition/main_round.md) |
| [**応用編**](./extras/_index.md) | サーバを自分で編集する／別用途に使う | [サーバ設定の編集方法](./extras/local_battle_setup.md) |
| | | [playground：人狼以外の議論にも使える環境](./extras/playground.md) |
| [**背景知識**](./background/_index.md) | 開発の基礎知識（任意） | [WSLとターミナル](./background/about_wsl.md) |
| | | [GitとGitHub](./background/about_github.md) |
| | | [仮想環境とは](./background/virtual_env.md) |
| | | [WebSocketとは](./background/about_websocket.md) |
| | | [Jinja2テンプレートとは](./background/about_jinja2.md) |
| | | [YAMLとは](./background/about_yaml.md) |
| | | [LangChainとは](./background/about_langchain.md) |
| | | [環境変数と.envファイル](./background/about_env_vars.md) |

---

> **GitHub公式**：[AIWolfDial Organization](https://github.com/aiwolfdial)\
> **最新大会情報**：[人狼知能大会 自然言語部門](https://aiwolfdial.github.io/aiwolf-nlp/)
