---
date: '2025-10-05T09:00:00+09:00'
draft: false
title: '運営の全体像'
category: organizer_guide
weight: 1
ShowToc: true
---

## 運営の進め方

運営の作業は、すべて次の 5 段階で進めます。

1. **大会の情報はシートに書く**（[大会定義シート](https://docs.google.com/spreadsheets/d/1NzFe2zl2lPqE9MQSbj_PVA4LMDwuje9Uez7GmGDdORg/edit)）
1. **書いたら大会データベースに反映する**（シートのメニュー「大会データ → 大会データを更新」。aiwolf-nlp-contest-data に push される）
1. **データベースの情報から、大会の成果物をコマンドで作る**（参加フォーム、サイトのページ、登録の通知）
1. **目で確認する**
1. **公開する**

大会の事実（名前、日程、学会、トラック、ルール、フォームの URL）はシートだけに書き、フォームやサイトの本文には直接書きません。
データベースの更新はボタンで自動ですが、公開は必ず人が確認してから行います。

```text
大会定義シート ──「大会データを更新」──▶ aiwolf-nlp-contest-data（大会データベース）
                                             ├─▶ 参加フォーム  … aiwolf-nlp-organize-tool
                                             ├─▶ 登録の通知    … aiwolf-nlp-organize-tool
                                             └─▶ サイト        … aiwolf-nlp（確認して push）
```

## 大会前の手順

上から順に進めます。

1. [準備](./preparing.md) … 最初の 1 回だけ
1. [フォームの作成と登録](./registration_form.md)
1. [サイト更新](./edit_website.md)
1. [参加登録が届いたら（Slack への招待）](./slack_invitation.md) … 登録期間中、届くたびに

## 必要なときに見るページ

- [秘密情報（サービスアカウントの鍵・Slack のトークン）](./secrets.md)
- [担当者（Slack の通知先）の追加](./owners.md)
- [大会定義シートの決まり](./sheet.md) … 日付の書き方、色の意味、更新の結果の見方
- [大きな変更をするとき](./advanced.md) … シートの項目やトラックを足す、ページの雛形を直す
- [ショートコード一覧](./shortcodes.md)
- [大会サーバへの接続](./server_access.md)
- [結果・ログのページ](./results_page.md) … 大会が終わったら

大会サーバの運用、勝率の集計、人手評価などの大会後半の作業は、それぞれのページ（[予選・本戦実行のコマンド一覧](./server_command.md)、[ゲームスコアの配信と集計](./win_rates.md)、[人狼知能人手評価手順](./subjective_evaluation.md)）を参照してください。
