---
date: '2025-10-04T14:00:00+09:00'
draft: false
title: '人狼知能デモ手順'
category: organizer_guide
---

## 全体の仕組み

```
【あなたのPC (WSL)】                     【ブラウザ (Viewer)】
ゲームサーバ :8080  ←─────────────────── リアルタイムログ接続
      ↑                                  (http://localhost:8080)
      │ ngrokトンネル
      ↓
pug-square-toucan.ngrok-free.app  ←───── 他エージェント接続
(wss://〜/ws)
```

**なぜ ngrok が必要か？**
Viewer は `https://aiwolfdial.github.io/` という HTTPS ページとして動いています。ブラウザのセキュリティポリシー上、HTTPS ページからローカルの `ws://`（暗号化なし WebSocket）には直接接続できません。ngrok を使うことで `wss://`（暗号化 WebSocket）のトンネルを作り、外部エージェントからの接続を可能にします。

---

## 事前準備

### 1. ngrok のインストールと Authtoken の設定（初回のみ）

ngrok は、ローカル PC 上のサーバをインターネット経由で一時的に公開するトンネルツールです。

[ngrokインストール参考リンク](https://qiita.com/miriwo/items/8c1e6550a5ab279d60b5)

インストール後、以下のコマンドで Authtoken を設定します。

```bash
ngrok config add-authtoken <YOUR_NGROK_AUTHTOKEN>
```

> **⚠️ セキュリティ注意：** Authtoken は認証情報です。公開リポジトリや共有ドキュメントには絶対に記載しないでください。PC 内だけで管理してください。

固定 URL を使う場合は ngrok の管理画面でドメインを取得しておいてください。

---

## 起動手順

### Step 1：ゲームサーバを起動する（WSL）

初回のみ、以下のコマンドでサーバ本体と設定ファイルをダウンロードします。

```bash
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/aiwolf-nlp-server-linux-amd64
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_5.yml
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_9.yml
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_13.yml
curl -Lo .env https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/example.env
chmod u+x ./aiwolf-nlp-server-linux-amd64
```

サーバを起動します。

```bash
./aiwolf-nlp-server-linux-amd64 -c ./default_13.yml  # 13人ゲームの場合
# ./aiwolf-nlp-server-linux-amd64 -c ./default_9.yml  # 9人ゲームの場合
# ./aiwolf-nlp-server-linux-amd64 -c ./default_5.yml  # 5人ゲームの場合
```

起動すると `ws://127.0.0.1:8080/ws` でエージェントの接続待ち受けを開始します。

> **補足：** デフォルト設定では「同じチーム名のエージェントのみ対戦させる自己対戦モード」が有効です。異なるチームのエージェントと対戦させたい場合は設定ファイルを編集してください。

---

### Step 2：ngrok を起動する

**別のターミナルを開き**、以下のコマンドを実行します。

```bash
ngrok http --url=pug-square-toucan.ngrok-free.app 8080
```

ターミナルに `Forwarding: https://pug-square-toucan.ngrok-free.app -> http://localhost:8080` と表示されれば成功です。**ゲーム中はこのターミナルを閉じないでください。**

---

### Step 3：Viewer でリアルタイムログに接続する

ブラウザで Viewer を開きます。

👉 `https://aiwolfdial.github.io/aiwolf-nlp-viewer/`

「リアルタイムログ」を選択し、接続先 URL に以下を入力して接続します。

​```
http://localhost:8080
​```

サーバへの接続が確立されれば OK です。ログはエージェントが接続してゲームが始まると流れ始めます。

---

### Step 4：外部エージェントを接続する

他チームや自分の別エージェントを起動し、接続先に ngrok の WebSocket URL を指定します。

```
wss://pug-square-toucan.ngrok-free.app/ws
```

`ws://` ではなく **`wss://`**（暗号化あり）を使う点に注意してください。設定した人数（5人・9人・13人）が揃い次第、ゲームが自動で開始され、Viewer にログが流れ始めます。

---

## URL まとめ

| 用途 | URL |
|------|-----|
| Viewer → サーバ（リアルタイムログ） | `http://localhost:8080` |
| 他エージェント → サーバ | `wss://pug-square-toucan.ngrok-free.app/ws` |
