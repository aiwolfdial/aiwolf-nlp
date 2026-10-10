---
date: '2025-10-05T09:00:00+09:00'
draft: false
title: '運営の全体像'
category: organizer_guide
weight: 1
ShowToc: true
---

大会の運営は、**大会定義シート**に大会の情報を書くところから始まります。
シートの値が大会データ（aiwolf-nlp-contest-data）になり、参加フォーム・ウェブサイト・通知がそこから作られます。
YAML や HTML を手で書く場面はほとんどありません。

## 情報の流れ

```text
大会定義シート（Google スプレッドシート）
   │  シートのメニュー「大会データ → 大会データを更新」
   ▼
aiwolf-nlp-contest-data（大会データ。GitHub 上で自動更新）
   ├─▶ 参加フォーム          … aiwolf-nlp-organize-tool の ops form create
   ├─▶ 登録の通知（Slack）   … aiwolf-nlp-organize-tool の ops sync
   └─▶ ウェブサイト          … aiwolf-nlp で取り込み → localhost で確認 → push
```

- 大会の事実（名前、日程、学会、トラック、ルール、フォームの URL）は**シートだけ**に書きます。サイトの本文やフォームには、シートの値が自動で入ります。
- 大会データの更新はシートのボタンで自動ですが、**公開サイトへの反映は必ず人が確認してから**行います。

## 手順（上から順に）

1. [準備（リポジトリと初回設定）](./preparing.md) … 最初の 1 回だけ
1. [大会定義シートの使い方](./sheet.md) … 新しい大会を始める
1. [参加フォームの作成](./registration_form.md)
1. [サイトの更新](./edit_website.md) … 大会ページの作成と、以後の更新
1. [参加登録が届いたら（Slack への招待）](./slack_invitation.md) … 登録期間中、届くたびに

必要になったときに見るページ:

- [担当者（Slack の通知先）の追加](./owners.md) … 運営メンバーが替わったとき
- [ショートコード一覧](./shortcodes.md) … 大会ページの雛形を直すとき
- [結果・ログのページ](./results_page.md) … 大会が終わったら

大会サーバの運用、勝率の集計、人手評価などの後半の作業は、それぞれのページ（[予選・本戦実行のコマンド一覧](./server_command.md)、[ゲームスコアの配信と集計](./win_rates.md)、[人狼知能人手評価手順](./subjective_evaluation.md)）を参照してください。
