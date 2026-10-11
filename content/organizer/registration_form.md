---
date: '2025-10-04T12:00:00+09:00'
draft: false
title: 'フォームの作成と登録'
category: organizer_guide
weight: 3
ShowToc: true
---

参加登録の Google フォームと回答シートを作り、フォームの URL を大会データベースに登録します。

## 大会情報入力

1. **自分の Google アカウントで**[大会定義シート](https://docs.google.com/spreadsheets/d/1NzFe2zl2lPqE9MQSbj_PVA4LMDwuje9Uez7GmGDdORg/edit)の「大会」タブを開きます。
1. 新しい大会なら、空いている列の **1 行目に大会 id** を書きます（例: `aiwolfdial2027_springjp`。半角の英小文字・数字・`_` だけ）。
1. **D1 のドロップダウンで「フォーム」を選びます。** フォームに必要な行がハイライトされます。
    - **濃い黄色**: フォームに必須の項目（空なら赤）。大会名、国内 / 国際、対戦言語、開催トラック、回 1 の識別子
    - **薄い黄色**: 使うけれど任意の項目（論文投稿の有無、回の名前など）
1. 濃い黄色の行を全部埋めます。英語の大会は「大会_en」タブの大会名（英語）も埋めます。

日付の書き方などは[大会定義シートの決まり](./sheet.md)を見てください。

## 大会データベース更新

シートのメニュー「**大会データ → 大会データを更新**」を押します。aiwolf-nlp-contest-data に push されます（30 秒〜1 分）。
終わるとダイアログに結果が出ます。「注意」が出たらシートを直して、もう一度押します。

## フォーム作成

aiwolf-nlp-organize-tool のターミナルで実行します。

```bash
cd aiwolf-nlp-organize-tool
git pull
uv run python -m ops form init <大会 id> --from <直近の大会 id>    # 初回だけ。質問の並びを前回から複製
uv run python -m ops form create <大会 id> --dry-run                # 質問の一覧を見るだけ（Google には触らない）
uv run python -m ops form create <大会 id>                          # フォームと回答シートを作る
```

- 大会データベースの最新を自動で取り込んでから作ります。
- タイトルは大会名から「人狼知能コンテスト ＜大会名＞（自然言語部門） 参加登録フォーム」になります。
- 回の質問（「1次＋2次」など）は、回が 2 つある大会だけに入ります。
- 「ログインしてください」と止まったら、[準備](./preparing.md#google-のスクリプトをターミナルから実行できるように登録)の clasp のログインをやり直します。

作り終わったら、organize-tool の `contests/<大会 id>/`（フォームの定義と回答シートの場所）を commit して push します。ほかの運営メンバーが登録の通知や名前の付け直しをするのに使います。

```bash
git add contests/<大会 id> && git commit -m "feat: <大会 id> の参加フォームを作成" && git push
```

## 大会データベース更新（フォームの URL）

フォームの URL は**シートの「参加フォーム URL」に自動で入ります**。シートに URL が載ったのを確かめてから、もう一度「大会データ → 大会データを更新」を押します。

## 確認

公開（告知）の前に、フォームを開いて確かめます。

- タイトル、質問の文言、トラックや回の選択肢が今回の大会のものか
- 送信できるか（必要なら自分でテスト回答し、回答シートから消す）

フォームをサイトに載せるのは、次の[サイト更新](./edit_website.md)です。

## 作ったあとに直すとき

| やりたいこと | すること |
| --- | --- |
| 大会名を変えた | シートを直して更新 → `uv run python -m ops form rename <大会 id>` |
| 質問を少し変えたい | Google フォームの編集画面で直す（URL は変わらない） |
| 質問の並びを毎回変えたい | `contests/<大会 id>/form.yaml` を直す（定番の質問は `ops/form/questions_common.yaml`） |
| 作り直したい | `uv run python -m ops form create <大会 id> --again`。古いフォームは Google ドライブで手で消す |

同じ大会でもう一度 `form create` を実行すると、二重に作らないように止まります。
