---
date: '2025-10-04T12:00:00+09:00'
draft: false
title: '参加フォームの作成'
category: organizer_guide
weight: 4
ShowToc: true
---

参加登録の Google フォームと回答シートを、コマンド 1 つで作ります。フォームの中身（大会名、トラックの選択肢、回の選択肢）は大会定義シートから入ります。

## 1. シートでフォームに必要な項目を埋める

1. [大会定義シート](https://docs.google.com/spreadsheets/d/1NzFe2zl2lPqE9MQSbj_PVA4LMDwuje9Uez7GmGDdORg/edit)の「大会」タブを開きます。
1. **D1 のドロップダウンで「フォーム」を選びます。** フォームに必須の行が濃い黄色、使うだけの行が薄い黄色になります。
1. 自分の大会の列で、**濃い黄色の行を全部埋めます**（空だと赤く表示されます）。今は次の項目です。
    - 大会名、国内 / 国際、対戦言語
    - 開催トラック（チェックボックス）
    - 回 1 の識別子（2 回ある大会は回 2 も）
1. 英語の大会では「大会_en」タブの大会名（英語）も埋めます。フォームが英語と日本語の併記になります。
1. メニュー「大会データ → 大会データを更新」を押します。

## 2. フォームを作る

```bash
cd aiwolf-nlp-organize-tool
uv run python -m ops form init <大会 id> --from <直近の大会 id>   # 初回だけ。質問の並びを前回から複製
uv run python -m ops form create <大会 id> --dry-run               # 質問の一覧を見るだけ（Google には触らない）
uv run python -m ops form create <大会 id>                         # フォームと回答シートを作る
```

- `form create` は最初に aiwolf-nlp-contest-data を最新にしてから、シートの値でフォームを作ります。
- タイトルは大会名から「人狼知能コンテスト ＜大会名＞（自然言語部門） 参加登録フォーム」になります。
- 回の質問（「1次＋2次」など）は、回が 2 つある大会だけに入ります。
- 質問を足したり並べ替えたりするときは、`contests/<大会 id>/form.yaml` を直してから `form create` します。定番の質問は `ops/form/questions_common.yaml` にあります。

終わると、フォームの URL が**シートの「参加フォーム URL」に自動で入ります**。回答シートの場所は `contests/<大会 id>/ops.yaml` に書かれます（非公開）。
`contests/<大会 id>/` を commit して push してください。

## 3. もう一度データを更新する

シートのメニュー「大会データ → 大会データを更新」を押します。フォームの URL が大会データに入り、サイトの「参加申請フォーム」のリンクに使われます。
サイトに出すには[サイトの更新](./edit_website.md)を行います。

## 作ったあとに直すとき

| やりたいこと | すること |
| --- | --- |
| 大会名を変えた | シートを直して更新 → `uv run python -m ops form rename <大会 id>`（フォームと回答シートの名前を付け直す） |
| 質問を変えたい | Google フォームの編集画面で直す（URL はそのまま） |
| 作り直したい | `uv run python -m ops form create <大会 id> --again`。古いフォームは残るので、Google ドライブで手で消す |

同じ大会でもう一度 `form create` を実行すると、二重に作らないように止まります。
