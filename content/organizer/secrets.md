---
date: '2025-10-04T09:50:00+09:00'
draft: false
title: '秘密情報（サービスアカウントの鍵・Slack のトークン）'
category: organizer_guide
weight: 10
ShowToc: true
---

運営の道具（aiwolf-nlp-organize-tool）が Google と Slack を使うための鍵です。**管理者から直接受け取り**、自分のマシンの `~/.ops/` に置きます。

**チャット、メール、リポジトリには貼らないでください。** 受け取ったら権限を自分だけにします（`chmod 600`）。

## 置くもの

| ファイル | 中身 | 使うコマンド |
| --- | --- | --- |
| `~/.ops/clasp_client_secret.json` | Google の OAuth クライアント | clasp のログイン（[準備](./preparing.md#google-のスクリプトをターミナルから実行できるように登録)）。フォームの作成など |
| `~/.ops/service_account.json` | Google のサービスアカウントの鍵 | 回答シートと大会定義シートの読み取り（`ops sync`、`ops contest import`、`ops contest layout`） |
| `~/.ops/secrets.env` | 上の鍵の場所と Slack Bot のトークン | `ops sync`（登録の通知） |

`~/.ops/secrets.env` の書き方（見本は organize-tool の `secrets.env.example`）:

```text
GOOGLE_SERVICE_ACCOUNT_JSON=/home/<自分>/.ops/service_account.json
SLACK_BOT_TOKEN=xoxb-…
```

```bash
mkdir -p ~/.ops && chmod 700 ~/.ops
chmod 600 ~/.ops/*
```

## どの作業に要るか

| 作業 | 要るもの |
| --- | --- |
| フォームの作成 | OAuth クライアント（clasp のログイン） |
| 参加登録の通知（`ops sync`） | サービスアカウントの鍵、Slack Bot のトークン |
| シートの形の作り直し（[大きな変更をするとき](./advanced.md)） | OAuth クライアント、サービスアカウントの鍵 |
| シートの「大会データを更新」 | 要らない（GitHub のトークンをシートに登録する。[準備](./preparing.md#シートから-githubaiwolf-nlp-contest-dataへ-push-できるように登録)） |

鍵を作り直すとき（漏れたかもしれないときなど）は、Google Cloud と Slack の管理画面で古い鍵を無効にしてから、新しい鍵を配ります。手順は organize-tool の `docs/setup_google.md` にあります。
