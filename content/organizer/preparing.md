---
date: '2025-10-04T14:00:00+09:00'
draft: false
title: '準備'
category: organizer_guide
weight: 2
ShowToc: true
---

運営に参加したら、最初に 1 回だけ行います。aiwolfdial の GitHub Organization に入れてもらい、[大会定義シート](https://docs.google.com/spreadsheets/d/1NzFe2zl2lPqE9MQSbj_PVA4LMDwuje9Uez7GmGDdORg/edit)の編集権限をもらっておいてください。

## リポジトリのクローン

運営で使うのは次の 3 つです。**同じフォルダに並べて**置きます（道具が隣のフォルダを探すため）。

| リポジトリ | 役割 |
| --- | --- |
| [aiwolf-nlp-organize-tool](https://github.com/aiwolfdial/aiwolf-nlp-organize-tool) | 運営で使うスクリプト（`ops` コマンド）。フォームの作成、登録の通知など。非公開 |
| [aiwolf-nlp-contest-data](https://github.com/aiwolfdial/aiwolf-nlp-contest-data) | 大会データベース。シートと連携していて、シートのボタンで自動更新される。手で編集しない |
| [aiwolf-nlp](https://github.com/aiwolfdial/aiwolf-nlp) | このウェブサイト |

```bash
mkdir aiwolfdial && cd aiwolfdial
git clone git@github.com:aiwolfdial/aiwolf-nlp-organize-tool.git
git clone https://github.com/aiwolfdial/aiwolf-nlp-contest-data.git
git clone --recursive https://github.com/aiwolfdial/aiwolf-nlp.git     # テーマと大会データ（submodule）も取得する

cd aiwolf-nlp-organize-tool
uv sync                                  # 依存を入れる（uv が無ければ https://docs.astral.sh/uv/ ）
npm install -g @google/clasp             # Google のスクリプトを扱う道具（Node.js が要る）
```

## Google のスクリプトをターミナルから実行できるように登録

フォームの作成などは、Google のスクリプトをターミナルから呼び出して行います。そのために clasp でログインします。
**ログインは 7 日で切れます。** 切れるとコマンドが案内を出すので、そのときにもう一度ログインします。

先に、管理者から OAuth クライアントのファイルを受け取り、`~/.ops/clasp_client_secret.json` に置きます（[秘密情報](./secrets.md)）。
ログインはブラウザで運営の共有 Google アカウントに入った状態で行います。次の 2 つのどちらかです。

### A. VS Code から（おすすめ）

VS Code の Remote-SSH で作業用のマシンに入っている場合です。organize-tool のターミナルで実行します。

```bash
clasp login --creds ~/.ops/clasp_client_secret.json
```

1. 表示された URL を Ctrl を押しながらクリックし、ブラウザで「許可」を押します。
1. VS Code が 8888 番を自動で転送するので、そのまま「ログインしました」と出て終わります。

自動で転送されないときは、実行する前に VS Code の「ポート」タブで 8888 を足しておきます。手元の PC で 8888 番が使われているとこの方法は使えないので、B にします。

### B. 自分で URL を貼る

```bash
clasp login --no-localhost --creds ~/.ops/clasp_client_secret.json
```

1. 表示された URL をブラウザで開き、「許可」を押します。
1. ブラウザが `http://localhost:8888/?…&code=…` に移って「アクセスできません」と表示されます。**これで正常です。**
1. アドレスバーの URL 全体をコピーして、ターミナルの `paste it here:` に貼り、Enter を押します。
1. 画面が固まったように見えてアドレスバーが変わらないときは、ブラウザで **F12** を押して開発者ツールを開き、「ネットワーク」タブで `localhost:8888` で始まる行を探します。その行を右クリック →「コピー」→「URL をコピー」し、ターミナルに貼ります。

## シートから GitHub（aiwolf-nlp-contest-data）へ push できるように登録

シートのメニュー「大会データ → 大会データを更新」は、押した人の GitHub トークンで aiwolf-nlp-contest-data を更新します。**押す人ごとに 1 回**登録します。

### GitHub トークンの取得

1. GitHub の右上のアイコン → Settings → 左下の Developer settings → Personal access tokens → **Fine-grained tokens** → Generate new token を開きます。
1. 次のように設定します。
    - Token name: 「大会定義シート」など
    - Resource owner: **aiwolfdial**
    - Expiration: 1 年程度（切れたら作り直して貼り直す）
    - Repository access: Only select repositories → **aiwolf-nlp-contest-data** だけ
    - Permissions → Repository permissions → **Actions を Read and write**（ほかは触らない）
1. Generate token を押し、表示された `github_pat_...` をコピーします（この画面を閉じると二度と表示されません）。

Organization の設定によっては、トークンが管理者の承認待ちになります。その場合は管理者に承認してもらいます。

### シートに登録

1. **自分の Google アカウントで**[大会定義シート](https://docs.google.com/spreadsheets/d/1NzFe2zl2lPqE9MQSbj_PVA4LMDwuje9Uez7GmGDdORg/edit)を開きます（開いているなら再読み込み）。
1. 数秒待つと、メニューバーの「ヘルプ」の右に「**大会データ**」が出ます。
1. 「大会データ → GitHub のトークンを設定」を押し、コピーしたトークンを貼って OK を押します。
1. 初回は Google の承認画面が出ます。「このアプリは Google で確認されていません」と出たら「詳細」→「（安全ではないページ）に移動」→「許可」で進めます。

トークンは自分の Google アカウント専用の領域に保存され、ほかの人には見えません。ほかの人が貼っても上書きされません。
