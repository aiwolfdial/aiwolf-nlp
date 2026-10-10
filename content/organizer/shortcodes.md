---
date: '2025-10-04T09:30:00+09:00'
draft: false
title: 'ショートコード一覧'
category: organizer_guide
weight: 8
ShowToc: true
---

大会ページの本文では、大会の事実（日程、フォームの URL、役職、学会など）を直接書かずに**ショートコード**で書きます。
値は大会定義シート（大会データ）から入るので、シートを直すだけでページも変わります。
ふだんの大会ページの作成では雛形が使っているので意識しなくて構いません。雛形に新しい文を足すときに使います。

## 大会の事実を出す

ページの front matter に `contest: <大会 id>` があれば、どのページでも使えます。英語ページでは自動で英語になります。

| 書き方 | 出るもの |
|---|---|
| `{{%/* contest-dates format="ja" bold="true" */%}}` | 日程の箇条書き。回が 2 つ以上なら回ごとの見出し付き。`format` は `ja`（2026年7月4日）/ `slash`（2026/05/01）/ `en` |
| `{{%/* contest-date key="venue" */%}}` | 日付を 1 つだけ文中に（`key` は `venue`＝会期、または日程の `key`）。`format` / `sep` / `pad="false"` で書式を合わせる |
| `{{%/* contest-form */%}}` | 参加登録フォームへのリンク |
| `{{%/* contest-tracks indent="  " */%}}` | トラック名の箇条書き |
| `{{%/* contest-roles size="9" */%}}` | 役職の表。`format="x"` で「村人×3, 占い師, …」、`format="plus"` で「村人3 + 占い師1 + …」の 1 行 |
| `{{%/* contest-games */%}}` | トラックごとのチーム当たり試合数の表 |
| `{{%/* contest-venue */%}}` | 併催の学会・会議「名前 [host](url)」。`part="name"` で名前だけ、`part="namelink"` でリンク付きの名前、`part="session"` でセッション名、`part="place"` で開催地だけ |
| `{{%/* contest-rule key="talk_chars" */%}}` | ルールの値 1 つ（`talk_chars` / `mention_chars` / `response_timeout_sec` / `anytime_talks_per_day` / `anytime_phase_min`）。`as="min"` で秒を分に |
| `{{%/* contest-sponsors */%}}` | スポンサーの箇条書き |
| `{{%/* contest-lang */%}}` | 対戦言語（「日本語」「英語」）。`as="code"` で `ja` / `en`（画像のパスなど） |
| `{{%/* contest-if rounds="2+" */%}}…{{%/* /contest-if */%}}` | 大会の設定に合うときだけ中身を出す。条件は `rounds="1"`/`"2+"`、`kind="domestic"`/`"international"`、`language`、`paper`、`sponsors`、`results`（`"true"`/`"false"`）、`has="venue.place"`（項目が埋まっているとき）。行ごと出し分けるときは前の行の末尾に開始タグを置き、中身を `- ` で始める |
| `{{%/* contest-results-note */%}}` | 結果・ログの案内。結果（results.yaml）が入る前は「掲載予定です」、入ったら「掲載しています」に自動で切り替わる |
| `{{%/* contest-name */%}}` | 大会名（英語ページは `name_en`）。「〇〇のサンプルエージェント」のように大会名を書く所に使う |
| `{{%/* contest-text key="character_prompt" */%}}` | `contest.yaml` の `texts.<key>` の自由文（Markdown 可）。英語ページは `<key>_en` |

値が無いときはどのショートコードも決まり文句を出します（文中は「【未定】」、段落は「決定次第掲載します。」、英語は `[TBA]` / `To be announced.`）。検査がこの文言を未記入として拾います。

## 大会によって文を出し分ける

回数、国内 / 国際、対戦言語、論文の有無によって変わる文は `contest-if` で書きます。雛形（直近の国際大会）にこう書いておくと、国内大会に複製しても書き直しが要りません。

```text
文の一部:   接続確認は{{%/* contest-if rounds="2+" */%}}各回（1次・2次）の{{%/* /contest-if */%}}締切までに提出してください。

行ごと:     前の行の末尾に開始タグを置き、中身を「- 」で始める（空行を残さないため）
            - 前の行{{%/* contest-if rounds="2+" */%}}
            - 2 回制のときだけ出る行{{%/* /contest-if */%}}

段落ごと:   空行で囲む
            {{%/* contest-if kind="international" */%}}
            国際大会だけの段落
            {{%/* /contest-if */%}}
```

対戦言語は `{{%/* contest-lang */%}}`（「日本語」「英語」）、大会名は `{{%/* contest-name */%}}` で書きます。
検査（`check.py`）は `contest-if` の条件を読むので、その大会で表示されない部分は指摘しません。
