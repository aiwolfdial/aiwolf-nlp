---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: '概要'
---

## このセクションについて

**概要** では、参加者が最初に押さえるべき4つのトピックをまとめています。
ゲームの基本, 大会の進み方 → エージェントの仕組み → 関連リポジトリ、の順で読むと全体像がつかめます。

---

## 目次

1. **[人狼知ゲームとは](./werewolf_overview.md)**
   人狼ゲームの概要・基本ルール・役職（村人／占い師／霊媒師／騎士／人狼／狂人）、
   村人／人狼それぞれの基本戦略、1日の流れ、主要用語を解説。

2. **[人狼知能大会のゲームロジックの実装](./aiwolf_logic.md)**
   大会サーバ側の進行（昼・夜・投票・占い・護衛・襲撃）や設定項目の全体像。
   5人戦／13人戦の配役、各フェーズの扱い、ログ出力の考え方など。

3. **[エージェントとサーバの仕組み（データの流れ）](./system_mechanism.md)**
   `aiwolf-nlp-agent-llm`（エージェント）／`aiwolf-nlp-server`（サーバ）／`aiwolf-nlp-common`（共通型）の役割と、
   JSONリクエスト → 文字列レスポンスの往復、LLM応答生成、差分履歴の扱いを図解で説明。

4. **[AIWolfDialリポジトリの説明](./aiwolfdial_repo.md)**
   開発で見るべき主要リポジトリの要点を整理。
   `aiwolf-nlp-agent-llm`／`aiwolf-nlp-common`／`aiwolf-nlp-server` は必読、
   ログ可視化・評価には `aiwolf-nlp-viewer`／`aiwolf-nlp-llm-judge` を紹介。

---

[参加者マニュアルトップへ](../_index.md)\
[次へ（準備）](../preparation/_index.md)
