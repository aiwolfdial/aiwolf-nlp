---
date: '2026-04-20T14:00:00+09:00'
draft: false
title: 'サーバの起動方法'
category: participants_guide
---

このページでは、ゲームサーバ（`aiwolf-nlp-server`）をローカルで起動する手順を説明します。
サーバは **配布されているバイナリ** を使えば、ビルドなしですぐに動かせます。

> サーバは、起動したフォルダの直下に `log/` ディレクトリを作ってログを書き出します。
> 専用のログ用フォルダを用意しておくと、後から整理が楽になります。

---

## ログ用フォルダの用意（おすすめ）

次のようにログ用のディレクトリを用意し、その中でサーバを起動すると便利です。

```bash
mkdir -p ~/aiwolfdial/aiwolf-nlp-game-logs
cd ~/aiwolfdial/aiwolf-nlp-game-logs
```

以降のコマンドはこのフォルダの中で実行するものとして書いています。

---

## 人数設定について

サーバには、ターン制の5人戦・9人戦・13人戦と、フリーフォーム方式の5人戦、人狼なしの議論環境（playground）など、複数の設定ファイルが用意されています。
実行するときに `-c` オプションで指定して使い分けます。

| 設定ファイル | 人数 | 特徴 |
|---|---|---|
| `default_5.yml` | 5人 | 役職は人狼1・占い師1・狂人1・村人2。ゲームが短く、お試しに最適 |
| `default_9.yml` | 9人 | 騎士・霊媒師も含む標準構成 |
| `default_13.yml` | 13人 | すべての役職がそろう大規模戦 |
| `freeform_5.yml` | 5人 | **フリーフォーム（グループチャット方式）** の5人戦。自由なタイミングで会話するモードを試したいとき |
| `playground.yml` | 5人 | **人狼なしの一般的な議論環境**（詳しくは [playground](../extras/playground.md) を参照） |

> まずは **5人戦** から動作確認するのがおすすめです。会話方式の違いについては [エージェントとサーバの仕組み](../overview/system_mechanism.md) の「会話の方式」を参照してください。

---

## Linux

```bash
# サーバ本体と設定ファイルをダウンロード
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/aiwolf-nlp-server-linux-amd64
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_5.yml
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_9.yml
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_13.yml
curl -Lo .env https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/example.env

# 実行できるようにする
chmod u+x ./aiwolf-nlp-server-linux-amd64

# 起動（使いたい人数のコメントを外す）
./aiwolf-nlp-server-linux-amd64 -c ./default_5.yml
# ./aiwolf-nlp-server-linux-amd64 -c ./default_9.yml
# ./aiwolf-nlp-server-linux-amd64 -c ./default_13.yml
```

---

## Windows (PowerShell)

```powershell
curl.exe -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/aiwolf-nlp-server-windows-amd64.exe
curl.exe -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_5.yml
curl.exe -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_9.yml
curl.exe -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_13.yml
curl.exe -Lo .env https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/example.env

.\aiwolf-nlp-server-windows-amd64.exe -c .\default_5.yml
```

---

## macOS

Intel Mac は `aiwolf-nlp-server-darwin-amd64`、Apple Silicon は `aiwolf-nlp-server-darwin-arm64` を使います。

```bash
# Apple Silicon (M1/M2/M3) の例
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/aiwolf-nlp-server-darwin-arm64
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_5.yml
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_9.yml
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_13.yml
curl -Lo .env https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/example.env

chmod u+x ./aiwolf-nlp-server-darwin-arm64
./aiwolf-nlp-server-darwin-arm64 -c ./default_5.yml
```

> **注意**：macOSでは「開発元が未確認」として実行がブロックされることがあります。その場合は [Appleのヘルプページ](https://support.apple.com/ja-jp/guide/mac-help/mh40616/mac) を参考に実行許可を与えてください。

---

## 起動できたことの確認

起動に成功すると、ターミナルに次のようなメッセージが表示されます。

```text
INFO サーバを起動しました host=127.0.0.1 port=8080
```

このメッセージが出ていれば、エージェントからの接続を待ち受けている状態です。

* **接続先URL**：`ws://127.0.0.1:8080/ws`
* **既定の動作モード**：自己対戦（同じチーム名のエージェント同士でマッチング）

次のページに進んで、エージェントを起動しましょう。

---

[参加者マニュアルトップへ](../_index.md)\
[実行トップへ](./_index.md)\
[前へ（APIキーの取得と設定）](../preparation/get_api_key.md)\
[次へ（エージェントの起動方法）](./agent.md)
