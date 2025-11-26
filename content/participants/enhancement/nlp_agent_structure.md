---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: 'サンプルエージェントの構成と主要ファイル'
category: participants_guide
---

このページでは `aiwolf-nlp-agent-llm` の**フォルダ構成**と、**主要ファイル**を簡潔にまとめます。

---

## フォルダ構成

```text
├── LICENSE                         # ライセンス
├── README.en.md                    # 英語の概要・セットアップ
├── README.md                       # 日本語の概要・セットアップ
├── config/                         # 設定ファイル群
│   ├── config.en.yml.example       # 英語プロンプト用サンプル
│   ├── config.jp.yml.example       # 日本語プロンプト用サンプル
│   └── config.yml                  # 実際に読み込まれる設定（LLMやプロンプト等）
├── pyproject.toml                  # 依存関係管理（uv/PEP 621）
├── src/
│   ├── agent/                      # 役職エージェント実装
│   │   ├── __init__.py
│   │   ├── agent.py                # ★基底エージェント：共通処理・フック
│   │   ├── bodyguard.py            # 騎士（BODYGUARD）
│   │   ├── medium.py               # 霊媒師（MEDIUM）
│   │   ├── possessed.py            # 狂人（POSSESSED）
│   │   ├── seer.py                 # 占い師（SEER）
│   │   ├── villager.py             # 村人（VILLAGER）
│   │   └── werewolf.py             # 人狼（WEREWOLF）
│   ├── main.py                     # エージェント起動のエントリーポイント
│   ├── starter.py                  # 起動・初期化（複数体の立ち上げ等）
│   └── utils/                      # ★共通ユーティリティ
│       ├── __init__.py
│       ├── agent_logger.py         # ログ出力（DEBUG/INFO行など）
│       ├── agent_utils.py          # 設定・前処理・汎用関数
│       └── stoppable_thread.py     # タイムアウト制御用の停止可能スレッド
└── uv.lock                         # uv のロックファイル（固定依存）
```

---

## 実行のデータフロー

1. **`main.py`**：設定を読む → 設定ごとに親プロセス生成
2. **`main.py → starter.connect`**：`agent.num` 人分の子プロセス生成
3. **`starter.create_client / connect_to_server`**：クライアント作成 → 接続（失敗時リトライ）
4. **`starter.handle_game_session`**：パケット受信 → 初回に役職エージェント生成 → 毎回応答
5. **`agent.set_packet`**：リクエスト・情報・履歴を更新（初期化時はリセット）
6. **`agent.action`**：種別に応じて発話/行動を決定（必要なら LLM）
7. **`agent_logger`**：受信（DEBUG）・LLM I/O（INFO）・最終返答（INFO）を記録
8. **`FINISH → close`**：ゲーム終了 → `auto_reconnect` に応じて再接続/終了

---

## 主要ファイルの役割

### `src/starter.py`（接続と 1 ゲーム進行）

役割:

> サーバ接続、エージェント生成、パケット入出力のループを担当。

要点:

> `create_client(config)`：`web_socket.url`/`token` からクライアント生成。\
> `connect_to_server(client, name)`：**15 秒間隔で再試行**し、接続成功まで待つ。\
> `handle_game_session(client, config, name)`：
>> `NAME` → **チーム名+連番** を返す（例 `kanolab1`）。\
>> `INITIALIZE` → `utils.agent_utils.init_agent_from_packet()` で **役職クラス** を生成。\
>> 毎パケット：`agent.set_packet(packet)` → `agent.action()` → 返答があれば `client.send()`。\
>> `FINISH` でループ終了。
>
> `connect(config, idx)`：上記一連を実行。`auto_reconnect` が **true** のときだけ再接続。

---

### `src/agent/agent.py`（基底クラス：全役職の共通動作）

役割:

> 受信パケットに応じて **発話/行動** を決め、必要に応じて **LLM** を呼ぶ。

要点:

> `set_packet(packet)`：`request`/`info`/`setting` を更新。`talk/whisper` 履歴は**差分で蓄積**。`INITIALIZE` では **履歴と LLM メッセージ履歴をリセット**。この時点のパケット全体を **DEBUG** で記録。\
> `initialize()`：`.env` を読み、`llm.type` に応じて `ChatOpenAI` / `ChatGoogleGenerativeAI` / `ChatOllama` を初期化。\
> `_send_message_to_llm()`：`config["prompt"][request.lower()]`（Jinja2）に
  `info/setting/talk_history/whisper_history/role/sent_*_count` を埋めて送信。LLM I/O は **INFO** で `["LLM", プロンプト, 応答]` として記録。\
> `action()`：`Request` に応じてメソッドを呼び分け。
>> **発話系**：LLM 応答なしは **空文字**。\
>> **行動系**：LLM 応答なしは `get_alive_agents()` から **ランダム**。
>
> `@timeout`：`setting.timeout.action` 超過で警告。`agent.kill_on_timeout=true` なら実行停止。

---

### `src/utils/agent_logger.py`（エージェント単位のロギング）

役割:

> コンソール/ファイル出力を設定に従って行う。

要点:

> `log.level` / `console_output` / `file_output` を反映。\
> **ファイル出力先**：`log.output_dir/<ULIDタイムスタンプ>/＜エージェント名＞.log`（ゲーム ID の ULID からタイムスタンプを復元し、同一ゲームのログを同フォルダに集約）。\
> **出力内容**：
>> 受信パケット全文：**DEBUG**（`set_packet()` 内）\
>> LLM 入出力：**INFO**（`["LLM", prompt, response]`）\
>> 最終返答：**INFO**（`["Request.XXX", "本文"]`／返答なしは種別のみ）

---

以上でサンプルエージェントの構成と主要ファイルの解説は完了です。

---

[参加者マニュアルトップへ](../_index.md)\
[改良・拡張トップへ](./_index.md)\
[前へ（サンプルエージェントの構成と主要ファイル）](./improvement_tips.md)\
[次へ（config.ymlの説明）](./config_explanation.md)
