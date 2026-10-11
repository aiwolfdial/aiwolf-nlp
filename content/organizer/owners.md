---
date: '2025-10-04T11:00:00+09:00'
draft: false
title: '担当者（Slack の通知先）の追加'
category: organizer_guide
weight: 11
ShowToc: true
---

参加登録があると、その大会の**担当者**に Slack の DM で知らせが届きます（[参加登録が届いたら](./slack_invitation.md)）。
運営メンバーが替わったときや、担当者を増やすときの手順です。この作業には organize-tool への push 権限が要ります。

## 1. Slack のメンバー ID を調べる

1. Slack で追加する人のプロフィールを開きます。
1. 「⋮」（その他）→「**メンバー ID をコピー**」を押します。`U` で始まる文字列（例: `U08XXXXXXXX`）です。

## 2. 運営の道具に登録する

aiwolf-nlp-organize-tool の `ops/config.yaml` の `people` に、短い名前（キー）と ID を足します。

```yaml
people:
  suzuki:              # 既にいる担当者
    name: 鈴木花子
    slack_user: U01AAAAAAAA
  tanaka:              # ← 追加。シートの「担当者」にはこのキーを書く
    name: 田中太郎
    slack_user: U08XXXXXXXX
```

```bash
git add ops/config.yaml && git commit -m "chore: 担当者に tanaka を追加" && git push
```

ほかの運営メンバーは `git pull` すると使えるようになります。

## 3. 大会の担当者にする

[大会定義シート](https://docs.google.com/spreadsheets/d/1NzFe2zl2lPqE9MQSbj_PVA4LMDwuje9Uez7GmGDdORg/edit)の「担当者」の行に、2 で付けたキーを書きます。
複数ならカンマかスペースで区切ります（`suzuki, tanaka`）。書いたら「大会データを更新」を押します。

## 届かないとき

- 通知は Bot（aiwolf-ops）から届きます。その人が同じ Slack ワークスペースにいる必要があります。
- キーの綴りがシートと `config.yaml` で一致しているか確かめてください。一致しないと「送り先なし」と表示されます。
