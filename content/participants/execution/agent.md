---
date: '2026-04-26T14:00:00+09:00'
draft: false
title: 'エージェントの起動方法'
category: participants_guide
---

このページでは、サンプルエージェントを起動してサーバに接続する手順を説明します。
前のページで **サーバを起動したまま** にしておいてください。

---

## 1. エージェントのフォルダへ移動

```bash
cd ~/aiwolfdial/aiwolf-nlp-agent-llm
```

---

## 2. `config.yml` を確認する

起動前に、エージェント側の設定を軽く確認しておきましょう。`config/config.yml` を開くと、次のような項目があります。

```yaml
web_socket:
  url: ws://127.0.0.1:8080/ws   # 接続先のサーバURL
  token:                        # 大会参加時に配布されるトークン（通常は空）
  auto_reconnect: false         # 切断時に自動で再接続するかどうか

agent:
  num: 5                        # 同時に起動するエージェント数（サーバの人数設定に合わせる）
  team: kanolab                 # チーム名（接続時の名前の先頭に使われます）
  kill_on_timeout: true         # タイムアウト時に処理を強制停止するかどうか
```

**ここだけチェックしておけばOK**

* **`agent.num`**：起動したサーバが5人戦なら `5`、9人戦なら `9`、13人戦なら `13` に合わせます。
* **`agent.team`**：自分で好きなチーム名にしてください。ログや表示名の先頭に使われます。
* **`web_socket.url`**：ローカルで動かす場合はそのままでOKです。

---

## 3. エージェントを起動する

### uv を使っている場合

```bash
uv run python src/main.py
```

### 仮想環境（venv）を使っている場合

```bash
source .venv/bin/activate
python src/main.py
```

---

## 起動時のオプション

設定ファイルを明示したり、複数の設定ファイルを同時に起動することもできます。

```bash
# 特定の設定ファイルを指定
uv run python src/main.py -c config/config.yml

# 複数の設定ファイルを同時に起動（別々のチームで対戦させたいときなど）
uv run python src/main.py -c config/team_a.yml config/team_b.yml

# ワイルドカードで一括指定
uv run python src/main.py -c config/team_*.yml
```

停止するときは **`Ctrl + C`** を押します。

---

## うまく動かないときのチェックポイント

* **APIキーを設定したか？**：`config/.env` に `GOOGLE_API_KEY` または `OPENAI_API_KEY` が書かれているか確認してください。
* **サーバが起動しているか？**：別ターミナルで [サーバの起動方法](./server.md) が完了しているか確認してください。
* **人数が一致しているか？**：サーバの設定ファイル（`default_5.yml` など）とエージェントの `agent.num` を合わせてください。
* **接続エラーが出る**：`[Errno 61] Connection refused` が出る場合、サーバ側がまだ起動していないか、URLが違う可能性があります。

---

接続に成功すると、ターミナルに初期化ログや、LLMに送られたプロンプト・返答が次々と流れます。
ゲームが終わると、ログが `log/` フォルダに保存されます。ログの見方は次のセクションで説明します。

---

[参加者マニュアルトップへ](../_index.md)\
[実行トップへ](./_index.md)\
[前へ（サーバの起動方法）](./server.md)\
[次へ（ゲームログの見方）](../evaluation/game_log_guide.md)
