---
date: '2026-04-20T14:00:00+09:00'
draft: false
title: 'ソースコードの構成'
category: participants_guide
---

こちらのページでは、サンプルエージェント `aiwolf-nlp-agent-llm` の **どこに何があるか** を説明します。
「コードを読む前の地図」として使ってください。

---

## フォルダ構成

```text
aiwolf-nlp-agent-llm/
├── README.md                   # 日本語の概要とセットアップ手順
├── README.en.md                # 英語版
├── pyproject.toml              # 依存関係の管理（uv / pip）
├── uv.lock                     # 依存バージョンのロック
├── config/
│   ├── config.jp.yml.example   # 日本語プロンプト版の設定サンプル
│   ├── config.en.yml.example   # 英語プロンプト版の設定サンプル
│   ├── config.yml              # 実際に読み込まれる設定（自分で作成）
│   └── .env.example            # APIキーの例（.env にコピーして使う）
└── src/
    ├── main.py                 # エントリーポイント
    ├── starter.py              # サーバ接続・ゲームセッション管理
    ├── agent/
    │   ├── agent.py            # 基底クラス（★改造の中心）
    │   ├── villager.py         # 村人
    │   ├── seer.py             # 占い師
    │   ├── medium.py           # 霊媒師
    │   ├── bodyguard.py        # 騎士
    │   ├── werewolf.py         # 人狼
    │   └── possessed.py        # 狂人
    └── utils/
        ├── agent_logger.py     # ログ出力
        ├── agent_utils.py      # 役職ごとのエージェント生成など
        └── stoppable_thread.py # タイムアウト制御
```

---

## 実行の流れ

コードを順に追うと、次のような流れになっています。

1. **`main.py`**：`config.yml` を読み込み、指定された人数分のエージェントプロセスを立ち上げます。
2. **`starter.connect`**：各プロセスでクライアントを作り、サーバに接続します（失敗すると15秒ごとにリトライ）。
3. **`starter.handle_game_session`**：サーバから届くパケットを1つずつ受け取り、それぞれに応じて処理を行います。
4. **`agent_utils.init_agent_from_packet`**：ゲーム開始時に、自分の役職に応じた **役職クラス** を生成します。
5. **`agent.set_packet`** → **`agent.action`**：パケットを読み取り、必要に応じてLLMを呼んで返答を作ります。
6. **`agent_logger`**：受信したパケット・LLMの入出力・最終返答をログに記録します。
7. **ゲーム終了**：`FINISH` を受け取ったら切断します。`auto_reconnect` が有効なら再接続します。

---

## 主要ファイルの役割

### `src/starter.py`

**役割**：サーバとの接続、1ゲーム分の進行を司るループを担当します。

* `create_client(config)`：`web_socket.url` / `token` からWebSocketクライアントを作成
* `connect_to_server`：接続に失敗したら15秒待って再試行
* `handle_game_session_async`：パケットを1つずつ受信 → 必要に応じてエージェントに処理させる
* `connect`：1ゲーム分の流れを実行。`auto_reconnect` が有効なら繰り返す

### `src/agent/agent.py`

**役割**：すべての役職の共通処理を書いた **基底クラス** です。改造の中心になります。

* `set_packet(packet)`：受信したパケットを内部状態に反映。履歴は差分で蓄積し、`INITIALIZE` ではリセット
* `initialize()`：`.env` からAPIキーを読み、`llm.type` に応じてLLMを初期化
* `_send_message_to_llm()`：`config.prompt[request]` のJinja2テンプレートにゲーム状態を埋めてLLMを呼ぶ
* `talk()` / `vote()` / `divine()` / `guard()` / `attack()` / `whisper()`：各リクエストへの応答を生成
* `action()`：届いたリクエスト種別に応じて、上記メソッドを呼び分ける
* `@timeout`：タイムアウト超過時に警告を出し、`kill_on_timeout: true` なら強制停止

> `set_packet` がどの属性に何を保存しているか、`self.info` などの中身を詳しく追いかけたい場合は [エージェントの内部状態とデータの流れ](./agent_state.md) を参照してください。

> **ポイント**：LLMが応答を返せなかった場合、**発話系**は空文字を返し、**行動系**（投票・占いなど）は生存者からランダムに選ばれます。

#### グループチャット方式（フリーフォーム）に関わるメソッド

サーバが **フリーフォーム方式**（[エージェントとサーバの仕組み ＞ 会話の方式](../overview/system_mechanism.md#会話の方式ターン制とフリーフォーム)）で動いているときだけ呼ばれる、非同期処理用のメソッドが基底クラスに用意されています。

* `handle_talk_phase(send)`：`TALK_PHASE_START` を受け取ったあと、**自分のターンが終わるまで数秒おきにLLMへ問い合わせて発言を送信** する非同期ループ
* `handle_whisper_phase(send)`：同上の囁き版
* `on_talk_received(talk)` / `on_whisper_received(whisper)`：他プレイヤーの発言が `TALK_BROADCAST` / `WHISPER_BROADCAST` で届いたときに呼ばれる **フックメソッド**。デフォルトは何もしない

ターン制で動かしている限り、これらは触らなくて大丈夫です。
フリーフォーム方式向けに発言タイミングや反応方法を作り込みたい場合は、これらをオーバーライドする形になります。

### `src/agent/*.py`（役職クラス）

役職ごとに `agent.py` を継承した専用クラスがあります。
デフォルトでは基底クラスのメソッドをそのまま呼び出すだけなので、「ここを改造すると特定の役職だけ動作を変えられる」という位置づけです。

### `src/utils/agent_logger.py`

**役割**：コンソールとファイルへのログ出力を担当します。

* 出力先：`log.output_dir/<ULIDタイムスタンプ>/<エージェント名>.log`
* 出力内容：
  * **DEBUG**：受信パケット全体
  * **INFO**：LLMへの入出力と、サーバへの最終返答
* 何を出力するかは `config.yml` の `log` セクションで調整できます。

### `src/utils/agent_utils.py`

役職ごとのクラスを管理しています。`INITIALIZE` 時に、サーバから届いた役職情報をもとに適切なクラスを生成します。

---

## 改造するときの優先順位

1. **プロンプトを変える**：`config.yml` の `prompt.*` を変えるのがいちばん手軽
2. **基底クラスの挙動を変える**：`agent.py` の `talk()` / `vote()` などを上書きする
3. **役職ごとに特別な処理を入れる**：`seer.py` / `werewolf.py` などを編集する
4. **共通処理を追加する**：`utils/` に新しいファイルを作り、`agent.py` から呼び出す

詳しくは次のページ [エージェントのカスタマイズ方法](./customize_agent.md) をご覧ください。

---

[参加者マニュアルトップへ](../_index.md)\
[改良・拡張トップへ](./_index.md)\
[前へ（改良のヒントと課題点）](./improvement_tips.md)\
[次へ（config.ymlの説明）](./config_explanation.md)
