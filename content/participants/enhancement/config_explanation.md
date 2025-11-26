---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: 'config.ymlの説明'
category: participants_guide
---

このページでは、`config.yml` の各セクションを説明します。

---

## 重要5項目

* **web_socket.url**：`ws://127.0.0.1:8080/ws`（ローカルサーバならそのまま）
* **web_socket.token**：大会運営から配布された **接続トークン**（必要な場合のみ）
* **agent.team / agent.num**：チーム名と起動数（自己対戦はデフォルトで可）
* **APIキー**：`config/.env` に `GOOGLE_API_KEY` / `OPENAI_API_KEY`（使うLLMに合わせて）
* **log.output_dir / level**：ログ保存先とレベル（不具合調査は `DEBUG` 推奨）

---

## セクション別の設定

### 1. `web_socket`（ゲームサーバ接続）

| キー               | 説明                  | 典型値 / メモ                       |
| ---------------- | ------------------- | ------------------------------ |
| `url`            | サーバの WebSocket URL。 | ローカル: `ws://127.0.0.1:8080/ws` |
| `token`          | 接続トークン（必要な大会時のみ）。   | 未使用なら空でOK                      |
| `auto_reconnect` | 対戦終了後に自動再接続するか。     | 練習: `true` / 単発実行: `false`     |

> `auto_reconnect=true` のときは、試合終了後に同設定で**すぐ再接続**します。

---

### 2. `agent`（エージェント起動）

| キー                | 説明                            | 典型値 / メモ                               |
| ----------------- | ----------------------------- | -------------------------------------- |
| `num`             | 起動するエージェント数。                  | 5人または13人（起動したサーバに合わせて）                           |
| `team`            | チーム名（`NAME` 応答の接頭に使用）。        | 例: `kanolab` → `kanolab1`, `kanolab2`… |
| `kill_on_timeout` | アクションのタイムアウト時に**処理を強制停止**するか。 | 本番は `true` 推奨                          |

---

### 3. `llm` / `openai` / `google` / `ollama`（モデル設定）

| セクション    | 主なキー                               | 説明                                        |
| -------- | ---------------------------------- | ----------------------------------------- |
| `llm`    | `type`                             | 使用するプロバイダ（`google` / `openai` / `ollama`） |
| 〃        | `sleep_time`                       | LLM呼び出し前の**待ち時間（秒）**。レート制御に便利             |
| `openai` | `model`, `temperature`             | 例: `gpt-4o-mini`, `0.7`                   |
| `google` | `model`, `temperature`             | 例: `gemini-2.0-flash-lite`, `0.7`         |
| `ollama` | `model`, `temperature`, `base_url` | 例: `llama3.1`, `http://localhost:11434`   |

> APIキーは **`config/.env`** に保存：
>
> * OpenAI → `OPENAI_API_KEY`
> * Google → `GOOGLE_API_KEY`

---

### 4. `prompt`（プロンプト一括管理）

* 各リクエスト種別に対応する **Jinja2 テンプレート** を定義します。
  キー名は **小文字** の `initialize`, `daily_initialize`, `talk`, `whisper`, `daily_finish`, `vote`, `divine`, `guard`, `attack`。
* よく使う埋め込み変数（抜粋）：

  * `info.*`：ゲーム状態（例：`info.agent`, `info.day`, `info.status_map`）
  * `setting.*`：ゲーム設定
  * `talk_history` / `whisper_history`：履歴（差分提供）
  * `role.value`：自分の役職名
  * `sent_talk_count` / `sent_whisper_count`：**自分がすでに発話/囁きした回数**（履歴の差分取得に使用）

#### ポイント

* `talk_history[sent_talk_count:]` や `whisper_history[sent_whisper_count:]` のように、**未読分だけ**を LLM に渡すテンプレが用意されています。
* `name` / `finish` はサーバへ**文字列を返さない**ため、プロンプトは不要です（定義しても使われません）。
* プロンプトに **余計な説明文** を入れるとそのまま送信されるため、**ゲームに必要な最小限**に保つのがおすすめです。

---

### 5) `log`（ロギング）

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

* **出力先**

  * コンソール：`console_output`
  * ファイル：`file_output`（`./log/<ULIDタイムスタンプ>/<エージェント名>.log` に保存）
* **レベル**

  * `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`（小文字でもOK）
* **`log.request`**（重要）

  * リクエストごとの**最終返答ログ**を出す/出さないの切り替えです（キーは**小文字**）。
  * `whisper` / `talk` など、必要なものだけ `true` に。
  * **LLM 入出力ログ**はこのフラグでは消せません（レベル/出力先で制御）。

---

最初はデフォルトのconfig.ymlをしようすれば問題ありません。
必要に応じてプロンプトとログ出力の粒度を調整し、挙動を確認してください。
以上でconfig.ymlの解説は完了です。

---

[参加者マニュアルトップへ](../_index.md)\
[改良・拡張トップへ](./_index.md)\
[前へ（サンプルエージェントの構成と主要ファイル）](./nlp_agent_structure.md)\
[次へ（エージェントのカスタマイズ方法）](./customize_agent.md)
