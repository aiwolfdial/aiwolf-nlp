---
date: '2025-10-05T22:34:38+09:00'
draft: false
title: '参加者向けマニュアル'
---

このマニュアルでは、人狼知能大会（自然言語部門）に参加するうえで必要なことを、はじめての方でも進められるようにまとめています。
大会のルールや仕組みから、サンプルエージェント [aiwolf-nlp-agent-llm](https://github.com/aiwolfdial/aiwolf-nlp-agent-llm) の動かし方、設定の変更方法、結果の確認、エージェントの改良までを扱います。

「順に読んで進める」「困ったときに辞書的に開く」のどちらの使い方でも問題ありません。各章は独立していますが、上から順に読むと実際の作業順になるのでスムーズです。

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
| | | [エージェントのカスタマイズ方法](./enhancement/customize_agent.md) |
| [**大会**](./competition/_index.md) | 本番のサーバに接続する | [大会での対戦方法](./competition/competition.md) |
| [**応用編**](./extras/_index.md) | サーバを自分で編集する／別用途に使う | [サーバ設定の編集方法](./extras/local_battle_setup.md) |
| | | [playground：人狼以外の議論にも使える環境](./extras/playground.md) |
| [**背景知識**](./background/_index.md) | 開発の基礎知識（任意） | [WSLとターミナル](./background/about_wsl.md) |
| | | [GitとGitHub](./background/about_github.md) |
| | | [仮想環境とは](./background/virtual_env.md) |
| | | [WebSocketとは](./background/about_websocket.md) |

---

> **GitHub公式**：[AIWolfDial Organization](https://github.com/aiwolfdial)\
> **最新大会情報**：[人狼知能大会 自然言語部門](https://aiwolfdial.github.io/aiwolf-nlp/)
