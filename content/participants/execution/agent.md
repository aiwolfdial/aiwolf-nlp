---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: 'エージェント起動方法'
category: participants_guide
---

このページでは、仮想環境を有効化し、`aiwolf-nlp-agent-llm` のエージェントを起動する手順を説明します。

---

## 1. リポジトリへ移動

```bash
cd ~/aiwolfdial/aiwolf-nlp-agent-llm
```

---

## 2. 仮想環境を有効化する

仮想環境が有効化されると、プロンプトの先頭に `(.venv)` のように**環境名**が表示されます。表示がない場合は仮想環境の外です。

```bash
# 環境の外の場合は有効化（bash / zsh）
user@host:~/aiwolfdial/aiwolf-nlp-agent-llm$ source .venv/bin/activate

# 環境が有効化
(.venv) user@host:~/aiwolfdial/aiwolf-nlp-agent-llm$
```

---

## 5. 起動前チェック（サーバ接続先・エージェント数）

起動前に、**サーバ接続設定** と **エージェント起動数** を `config/config.yml`（または指定する設定ファイル）で確認してください。

```yaml
web_socket:
  url: ws://127.0.0.1:8080/ws   # サーバの WebSocket URL
  token:                        # 認証が必要な場合に設定
  auto_reconnect: false         # 切断時の自動再接続

agent:
  num: 5                        # 起動するエージェント数（5または13）
  team: kanolab                 # チーム名（ログや表示で利用）
  kill_on_timeout: true         # タイムアウト時にプロセスを落とすか
```

* **`web_socket.url`**：`execution/server.md` の手順で起動した **サーバの URL** を設定します。
  マニュアル通りであれば **デフォルトのままで動く**ように設定済みですが、将来的に変更する可能性があるため項目の存在と役割を把握しておいてください。
* **`agent.num`**：同時に起動するエージェント数（ローカル対戦の規模に合わせて調整）。
* **`team` / `kill_on_timeout` / `auto_reconnect`**：運用ポリシーに応じて調整。

> 例：サーバの URL を変更した場合や起動したサーバの人数設定を変更した場合は、上記を**必ず**合わせて更新してください。トークンが必要な構成にした場合は `token` を設定します。

---

## 6. エージェントを起動する

```bash
python src/main.py
```

デフォルトでは **`config/config.yml`** の設定を参照して起動します。
指定して起動する方法や、複数の設定ファイルを同時に実行する方法は以下のとおりです。

```bash
# 単一の設定ファイルを指定
python src/main.py -c config/config_1.yml

# 複数の設定ファイルを同時指定
python src/main.py -c config/config_1.yml config/config_2.yml

# ワイルドカード指定
python src/main.py -c config/config_*.yml
```

* 成功すると、ターミナルに初期化ログやサーバ接続の試行が表示されます。
* 停止は **`Ctrl + C`**。

---

[参加者マニュアルトップへ](../_index.md)\
[実行トップへ](./_index.md)\
[前へ（サーバ起動方法）](./server.md)\
[次へ（ゲームサーバからのデータ）](../evaluation/server_data.md)
