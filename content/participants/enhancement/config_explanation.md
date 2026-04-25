---
date: '2026-04-26T14:00:00+09:00'
draft: false
title: 'config.ymlの説明'
category: participants_guide
---

このページでは、エージェントの設定ファイル `config/config.yml` の各項目を説明します。
まずはデフォルトのままで問題なく動きますが、**プロンプトとログ** を調整するだけでも、エージェントの挙動はかなり変わります。

---

## まず押さえておきたい5つ

最初はこれだけ覚えておけばOKです。

1. **`web_socket.url`**：接続先のサーバURL。ローカルなら `ws://127.0.0.1:8080/ws`
2. **`web_socket.token`**：大会運営から配布されたトークン（ローカル対戦では空でOK）
3. **`agent.num` / `agent.team`**：起動するエージェント数と、チーム名
4. **`config/.env`**：APIキーを書く場所（`GOOGLE_API_KEY` / `OPENAI_API_KEY`）
5. **`log.level`**：不具合調査をするときは `debug` にしておく

---

## セクション別の説明

### `web_socket`：サーバ接続設定

```yaml
web_socket:
  url: ws://127.0.0.1:8080/ws
  token:
  auto_reconnect: false
```

| キー | 説明 |
|---|---|
| `url` | サーバのWebSocket URL |
| `token` | 接続トークン（必要な場合のみ） |
| `auto_reconnect` | 対戦終了後に自動で再接続するか |

> 練習時や大会本戦では `auto_reconnect: true` にしておくと、一度設定しておけば試合終了後も自動で次に繋がります。

---

### `agent`：エージェントの起動設定

```yaml
agent:
  num: 5
  team: kanolab
  kill_on_timeout: true
```

| キー | 説明 |
|---|---|
| `num` | 同時に起動するエージェント数（5 / 9 / 13）。サーバの人数に合わせる |
| `team` | チーム名。接続時の名前の先頭として使われる（例：`kanolab1`） |
| `kill_on_timeout` | アクションがタイムアウトしたときに処理を強制停止するかどうか |

---

### `llm` ／ `openai` ／ `google` ／ `ollama`：LLMの設定

```yaml
llm:
  type: google   # google / openai / ollama のいずれか
  sleep_time: 3  # LLMを呼ぶ前の待機秒数
```

| セクション | 設定項目 | 説明 |
|---|---|---|
| `llm` | `type` | 使うLLMのプロバイダ |
| `llm` | `sleep_time` | LLMを呼ぶ前に待つ秒数（レート制限対策） |
| `openai` | `model` / `temperature` | OpenAIのモデル設定 |
| `google` | `model` / `temperature` | Geminiのモデル設定 |
| `ollama` | `model` / `temperature` / `base_url` | Ollama（ローカルLLM）の設定 |

APIキーは `config/.env` に置きます。

```dotenv
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
```

---

### `prompt`：LLMへの指示文（★いちばん触りがいのある場所）

`prompt` セクションには、リクエストごとにLLMに渡す **指示文（Jinja2テンプレート）** が書かれています。

使えるキー名はすべて小文字で、以下の通りです。

```text
initialize / daily_initialize / talk / whisper / daily_finish /
vote / divine / guard / attack
```

テンプレート内では、次のような変数が使えます。

| 変数 | 内容 |
|---|---|
| `info.agent` | 自分の名前 |
| `info.day` | 今が何日目か |
| `info.status_map` | 各プレイヤーの生死 |
| `info.profile` | 自分のキャラクタープロフィール |
| `role.value` | 自分の役職名 |
| `talk_history` / `whisper_history` | これまでの会話履歴 |
| `sent_talk_count` / `sent_whisper_count` | 自分がすでに読み込んだ履歴の位置 |

> **ポイント**：`talk_history[sent_talk_count:]` のように書くと、「まだLLMに渡していない新しい発言だけ」を取り出せます。
> サンプルはそのように書かれているので、改造する際もこのパターンを踏襲するのがおすすめです。

LLMの応答は **そのままサーバに送られる** ので、不要な前置きやコードブロック装飾が出力されないようにプロンプトで明示しておきましょう。

---

### `log`：ログの出力設定

```yaml
log:
  console_output: true
  file_output: true
  output_dir: ./log
  level: debug
  request:
    name: false
    initialize: false
    daily_initialize: false
    whisper: true
    talk: true
    daily_finish: false
    divine: true
    guard: true
    vote: true
    attack: true
    finish: false
```

| キー | 説明 |
|---|---|
| `console_output` | ターミナルに出力するかどうか |
| `file_output` | ファイルに出力するかどうか |
| `output_dir` | ログの保存先フォルダ |
| `level` | ログレベル（`debug` / `info` / `warning` / `error` / `critical`） |
| `request.*` | リクエストごとに「最終返答」をログに残すかどうか |

> **補足**：`log.request.*` は「サーバに送った最終返答」のログだけを制御するフラグです。
> LLMへの入出力ログは `level` と `console_output` / `file_output` で制御されます。

---

## キャラクター名について

大会標準のサーバ設定では、プレイヤーに **日本語のキャラクター名**（例：ミナト・サクラ・ケンジ）と性格・年齢などのプロフィールが自動で割り当てられます。
プロンプト内で `info.profile` を使うと、このキャラクター情報をLLMに伝えられます。

---

## まずはデフォルト、そして少しずつ

最初はサンプル通りの `config.yml` で動かして、ゲームの流れを確認しましょう。
その後、改良するときは次の順番がおすすめです。

1. `prompt` を調整する（いちばん効果が出やすい）
2. `log` を `info` → `debug` に切り替えて詳細を確認する
3. `llm.type` や `model` を変えて、モデルによる違いを比べる

---

[参加者マニュアルトップへ](../_index.md)\
[改良・拡張トップへ](./_index.md)\
[前へ（ソースコードの構成）](./nlp_agent_structure.md)\
[次へ（エージェントの内部状態とデータの流れ）](./agent_state.md)
