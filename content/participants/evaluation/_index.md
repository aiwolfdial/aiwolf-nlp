---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: '確認・評価'
---

## このセクションについて

**確認・評価** では、実行後の**データ確認と評価**をまとめています。  
サーバから届く JSON（Packet）の中身とゲームログ（`.log`）、**エージェントログ**の読み方、ゲームログをより見やすくするためのViewer の使いかた、勝率や会話品質の評価について詳しく説明していきます。

---

## 目次

1. **[ゲームサーバからのデータ](./server_data.md)**  
   サーバ→エージェントの **Packet(JSON)** を読み解くガイド。  
   どのキーが何を意味し、どのリクエストに何を返すべきかを整理。

2. **[ゲームログの見方](./game_log_guide.md)**  
   `log/game/*.log` の読み方。行種別（talk/whisper/divine/vote/…）の構造と、  
   番号→名前の対応、時系列追跡のコツを解説。

3. **[エージェントログの見方](./agent_log_guide.md)**  
   `aiwolf-nlp-agent-llm` 側のログ（DEBUG/INFO）の読み方。  
   受信Packet（DEBUG）、LLMの入出力・最終返答（INFO）の見分け方と活用法。

4. **[ビュアーの使いかた](./viewer_usage.md)**  
   Web ビューアでログを**可視化**。アーカイブログの読み込み、表示項目の切替、  
   過去大会ログの閲覧方法を説明。

5. **[winrate計算方法](./winrate_calculation.md)**  
   **Macro / Micro / Weighted Micro** の3指標で勝率を算出する手順とスクリプト。

6. **[LLM Judgeの使いかた](./llm_judge_usage.md)**  
   LLM を用いた**会話品質の自動評価**。入力データ配置、設定、実行、出力の読み方まで。

---

[参加者マニュアルトップへ](../_index.md)\
[前へ（実行）](../execution/_index.md)\
[次へ（改良・拡張）](../enhancement/_index.md)
