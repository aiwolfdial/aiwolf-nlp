---
date: '2025-10-04T14:00:00+09:00'
draft: false
title: '人狼知能人手評価手順'
category: organizer_guide
---

## ゴール（何ができればOK？）

* ローカルで **ゲームサーバ** を起動
* **Viewer** から `http://localhost:8080` に接続してログが見える
* 外部（他PC/他拠点）から **ngrok経由のWebSocket** に接続できる

  * 他エージェント: `wss://<あなたのngrokドメイン>/ws`
  * Viewer単独エージェント: `https://<あなたのngrokドメイン>/ws`

---

## ngrok の準備

1. ngrok をインストール（任意の方法）
2. **Authtoken を設定**（※セキュリティ注意：認証情報はPC内に保管、公開リポジトリ等に絶対に載せない）

```bash
ngrok config add-authtoken <YOUR_NGROK_AUTHTOKEN>
```

---

## サーバの起動（WSL）

```bash
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/aiwolf-nlp-server-linux-amd64
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_5.yml
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_13.yml
curl -Lo .env https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/example.env
chmod u+x ./aiwolf-nlp-server-linux-amd64
./aiwolf-nlp-server-linux-amd64 -c ./default_13.yml # 13人ゲームの場合
```

（5人なら `-c ./default_5.yml`）

---

## Viewer から接続

1. ブラウザで Viewer を開く：
   `https://aiwolfdial.github.io/aiwolf-nlp-viewer/`
2. 「リアルタイムログ」等の入力欄に **`http://localhost:8080`** を指定して接続
3. ログ（発言や進行）が流れればOK

---

## ngrok 起動

```bash
ngrok http --url=pug-square-toucan.ngrok-free.app 8080
```

---

## 外部向け接続先

* 他エージェント: `wss://pug-square-toucan.ngrok-free.app/ws`
* Viewer単独: `https://pug-square-toucan.ngrok-free.app/ws`
