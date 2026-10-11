---
date: '2025-10-04T10:30:00+09:00'
draft: false
title: '参加登録が届いたら（Slack への招待）'
category: organizer_guide
weight: 5
ShowToc: true
---

登録期間中は、参加登録が届くたびに担当者へ Slack の DM が届きます。DM を見たら、参加者を大会の Slack チャンネルに招待します。

## 登録の通知を動かす

担当者への DM は、aiwolf-nlp-organize-tool の `ops sync` が送ります。登録期間の始まりに、常に動いているマシンで起動しておきます。
回答シートの読み取りと Slack への送信に、[秘密情報](./secrets.md)（サービスアカウントの鍵と Slack Bot のトークン）が要ります。

```bash
cd aiwolf-nlp-organize-tool
tmux new -s sync                                   # ログアウトしても止まらないように
uv run python -m ops sync <大会 id>                 # 5 分おきに回答シートを見て、新しい登録を DM で知らせる
```

| オプション | 意味 |
| --- | --- |
| `--once` | 1 回だけ見て終わる |
| `--no-notify` | DM を送らずに、公開用のチーム一覧だけ更新する |
| `--interval 600` | 見に行く間隔（秒）。既定は 300 |

DM の送り先は、大会定義シートの「担当者」の人です（追加は[担当者（Slack の通知先）の追加](./owners.md)）。
あわせて、公開用のチーム一覧（チーム名と公開可の氏名・所属だけ。連絡先は含めない）が aiwolf-nlp-contest-data に自動で push されます。

DM にはこう書かれています。

```text
[2026 国際大会（INLG 2026）] 新規登録: *kanolab*
代表: 山田太郎（〇〇大学） taro@example.com
トラック: ターン式 × 5人村, いつでも発話 × 5人村 / 回: 1次＋2次
Slack 招待: taro@example.com, hanako@example.com
公開表記: 山田太郎（〇〇大学）
```

「Slack 招待」の行のメールアドレスを、次の手順で招待します。

## Slack に招待する

- 歯車マークの「管理者」
![管理者](https://aiwolfdial.github.io/aiwolf-nlp/images/organizer/slack_invitation/image.png)

- 「メンバーを管理する」
![メンバーを管理する](https://aiwolfdial.github.io/aiwolf-nlp/images/organizer/slack_invitation/image%201.png)

- 「名前またはメールアドレスで」
![名前またはメールアドレスで](https://aiwolfdial.github.io/aiwolf-nlp/images/organizer/slack_invitation/image%202.png)

    1. 参加登録GoogleFormに入力されたメールアドレスを入力

    2. 参加者が過去に出場したことがあった場合は検索結果にユーザが表示される
    </details>

- 「･･･」→「アカウントを有効かする」
![アカウントを有効化する](https://aiwolfdial.github.io/aiwolf-nlp/images/organizer/slack_invitation/image%203.png)

- 「シングルチャンネルゲスト」→「次へ」
![シングルチャンネルゲスト](https://aiwolfdial.github.io/aiwolf-nlp/images/organizer/slack_invitation/image%204.png)

- 「チャンネルを選択する」→「該当大会のチャンネル」→「シングルチャンネルゲストにする」
![チャンネルを選択する](https://aiwolfdial.github.io/aiwolf-nlp/images/organizer/slack_invitation/image%205.png)

- 「メンバーを招待する」
![メンバーを招待する](https://aiwolfdial.github.io/aiwolf-nlp/images/organizer/slack_invitation/image%206.png)

- 「送信」
![送信](https://aiwolfdial.github.io/aiwolf-nlp/images/organizer/slack_invitation/image%207.png)

    1. 送信先に参加登録GoogleFormに入力されたメールアドレスを入力

    2. 招待の種類は「ゲスト」

    3. チームのチャンネルに追加する「該当大会のチャンネル」

    4. 「送信」
    </details>

DM が届くたびに、この作業を行います。
