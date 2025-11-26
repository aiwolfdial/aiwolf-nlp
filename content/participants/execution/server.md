---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: 'サーバ起動方法'
category: participants_guide
---

このページでは、**AIWolf NLP サーバ** をローカルで起動する手順を説明します。
サーバを起動した **ディレクトリ直下にゲームログが保存** されるため、専用の作業フォルダで起動するのが便利です。

---

## （推奨）ログ用ディレクトリで起動する

任意の場所で構いませんが、ここでは次のフォルダを使います。

```bash
mkdir -p ~/aiwolfdial/aiwolf-nlp-game-logs
cd ~/aiwolfdial/aiwolf-nlp-game-logs
```

> サーバを **このフォルダから起動** すると、生成されるログがすべてここに貯まります（管理が楽）。

---

## ドキュメント

* [設定ファイルについて](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/doc/ja/config.md)
* [ゲームロジックの実装について](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/doc/ja/logic.md)
* [プロトコルの実装について](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/doc/ja/protocol.md)

---

## 実行の考え方

* 既定のサーバアドレス：`ws://127.0.0.1:8080/ws`
  → **エージェントの接続先**（`config/config.yml` の `web_socket.url`）もこのURLに合わせます。
  → マニュアル通りの手順なら **デフォルトのまま動作** します。
* **自己対戦モード（同一チーム名のマッチング）** はデフォルト有効。
  → 異なるチーム名でマッチさせるには **設定ファイルを編集** してください（詳細は [設定ファイルについて](/doc/ja/config.md)）。

---

## Linux

```bash
# バイナリ／設定／環境テンプレートを取得
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/aiwolf-nlp-server-linux-amd64
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_5.yml
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_13.yml
curl -Lo .env https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/example.env

# 実行権限を付与
chmod u+x ./aiwolf-nlp-server-linux-amd64

# 起動（どちらか片方だけ有効にして実行）
./aiwolf-nlp-server-linux-amd64 -c ./default_5.yml   # 5人ゲームの場合
# ./aiwolf-nlp-server-linux-amd64 -c ./default_13.yml # 13人ゲームの場合
```

---

## Windows

```bash
# バイナリ／設定／環境テンプレートを取得（PowerShell）
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/aiwolf-nlp-server-windows-amd64.exe
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_5.yml
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_13.yml
curl -Lo .env https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/example.env

# 起動（どちらか片方だけ有効にして実行）
.\aiwolf-nlp-server-windows-amd64.exe -c .\default_5.yml   # 5人ゲームの場合
# .\aiwolf-nlp-server-windows-amd64.exe -c .\default_13.yml # 13人ゲームの場合
```

---

## macOS (Intel)

> [!NOTE]
> 「開発元が未確認のため開けません」と表示された場合は、以下を参考に実行許可を与えてください：
> [https://support.apple.com/ja-jp/guide/mac-help/mh40616/mac](https://support.apple.com/ja-jp/guide/mac-help/mh40616/mac)

```bash
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/aiwolf-nlp-server-darwin-amd64
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_5.yml
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_13.yml
curl -Lo .env https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/example.env
chmod u+x ./aiwolf-nlp-server-darwin-amd64

# 起動（どちらか片方だけ有効にして実行）
./aiwolf-nlp-server-darwin-amd64 -c ./default_5.yml   # 5人ゲームの場合
# ./aiwolf-nlp-server-darwin-amd64 -c ./default_13.yml # 13人ゲームの場合
```

---

## macOS (Apple Silicon)

> [!NOTE]
> 「開発元が未確認のため開けません」と表示された場合は、以下を参考に実行許可を与えてください：
> [https://support.apple.com/ja-jp/guide/mac-help/mh40616/mac](https://support.apple.com/ja-jp/guide/mac-help/mh40616/mac)

```bash
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/aiwolf-nlp-server-darwin-arm64
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_5.yml
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/default_13.yml
curl -Lo .env https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/example.env
chmod u+x ./aiwolf-nlp-server-darwin-arm64

# 起動（どちらか片方だけ有効にして実行）
./aiwolf-nlp-server-darwin-arm64 -c ./default_5.yml   # 5人ゲームの場合
# ./aiwolf-nlp-server-darwin-arm64 -c ./default_13.yml # 13人ゲームの場合
```

---

## 起動後の確認

* “`#`” はコメントです。
* コンソールに **`INFO サーバを起動しました host=127.0.0.1 port=8080`** が出力されます。
* フォルダ直下にゲームログが生成される
* エージェント接続先（`config/config.yml` の `web_socket.url`）が
  `ws://127.0.0.1:8080/ws` になっている（変更した場合は合わせる）

---

これでローカルサーバの起動は完了です。

---

[参加者マニュアルトップへ](../_index.md)\
[実行トップへ](./_index.md)\
[前へ（API取得方法）](../preparation/get_api_key.md)\
[次へ（エージェント起動方法）](./agent.md)
