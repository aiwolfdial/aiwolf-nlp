---
date: '2025-10-05T22:34:38+09:00'
draft: false
title: '参加者向けマニュアル'
---
こちらのページでは人狼知能大会の概要や人狼知能大会サンプルエージェント[aiwolf-nlp-agent-llm](https://github.com/aiwolfdial/aiwolf-nlp-agent-llm)の動かし方や設定について詳細に示しています。
本大会に興味のある方はぜひこちらを活用して、大会へ出場してみてください！

> 上から順に閲覧していただいても構いませんし、辞書的にご利用いただいても大丈夫です。各章は独立して読めますが、実際の作業順に沿って読むとよりスムーズに理解できます。

---

## ページ名一覧

| セクション | 説明 | ページ一覧 |
|---|---|---|
| [**概要**](./overview/_index.md) | 人狼ゲームと大会の仕組みを理解する導入セクション | [人狼ゲームとは](./overview/werewolf_overview.md) |
|  |  | [人狼知能大会のロジック](./overview/aiwolf_logic.md) |
|  |  | [エージェントとサーバの仕組み](./overview/system_mechanism.md) |
|  |  | [AIWolfDialリポジトリの説明](./overview/aiwolfdial_repo.md) |
| [**準備**](./preparation/_index.md) | Python環境の準備からリポジトリ設定、APIキー取得まで | [事前準備](./preparation/setup.md) |
|  |  | [リポジトリのクローン](./preparation/clone_repo.md) |
|  |  | [API取得方法](./preparation/get_api_key.md) |
| [**実行**](./execution/_index.md) | サーバとエージェントをローカルで実行し、動作を確認 | [サーバ起動方法](./execution/server.md) |
|  |  | [エージェント起動方法](./execution/agent.md) |
| [**確認・評価**](./evaluation/_index.md) | ゲームログ・エージェントログ・Viewer・勝率・Judgeを使った評価 | [サーバデータの見方](./evaluation/server_data.md) |
|  |  | [ゲームログの見方](./evaluation/game_log_guide.md) |
|  |  | [エージェントログの見方](./evaluation/agent_log_guide.md) |
|  |  | [Viewerの使い方](./evaluation/viewer_usage.md) |
|  |  | [Winrate計算方法](./evaluation/winrate_calculation.md) |
|  |  | [LLM Judgeの使い方](./evaluation/llm_judge_usage.md) |
| [**改良・拡張**](./enhancement/_index.md) | 構成理解・設定編集・カスタマイズによるエージェント強化 | [エージェントの課題点](./enhancement/improvement_tips.md) |
|  |  | [構成と主要ファイル](./enhancement/nlp_agent_structure.md) |
|  |  | [config.ymlの説明](./enhancement/config_explanation.md) |
|  |  | [カスタマイズ方法](./enhancement/customize_agent.md) |
| [**大会**](./competition/_index.md) | 実際の大会（予選・本戦）での接続・実行方法 | [大会での対戦方法](./competition/competition.md) |
| [**応用編**](./extras/_index.md) | サーバをローカルで編集して実験・研究に活用 | [サーバ編集・ローカル対戦環境構築](./extras/local_battle_setup.md) |
| [**背景知識**](./background/_index.md) | WSL・GitHub・仮想環境などの開発基礎知識 | [WSLとは](./background/about_wsl.md) |
|  |  | [GitHubとは](./background/about_github.md) |
|  |  | [仮想環境とは](./background/virtual_env.md) |

---

> **GitHub公式**：[AIWolfDial Organization](https://github.com/aiwolfdial)\
> **最新大会情報**：[人狼知能大会 自然言語部門](https://aiwolfdial.github.io/aiwolf-nlp/)
