---
date: '2025-10-04T10:00:00+09:00'
draft: false
title: '人狼知能大会ウェブサイト更新'
category: organizer_guide
ShowToc: true
---

## 大会データ（aiwolf-nlp-contest-data）

大会の事実（日程、参加フォームの URL、トラックと役職構成、試合数、併催の学会、文字数などのルール値、スポンサー）と結果は、
別リポジトリ [aiwolf-nlp-contest-data](https://github.com/aiwolfdial/aiwolf-nlp-contest-data) に置きます。
本サイトはそれを `external/aiwolf-nlp-contest-data` に submodule として取り込み、`hugo.yaml` のマウント設定で `data/contests/` と `data/roles/` に見せています。

```text
contests/<大会 id>/contest.yaml   大会の定義（人が書く）
contests/<大会 id>/results.yaml   結果（scripts/results/build_contest_yaml.py が生成する）
roles/<人数>.yaml                  村の人数ごとの役職表
```

大会 id は `inlg_2026`、`aiwolfdial2026_springjp` のように小文字で付け、サイト側のディレクトリ名・ファイル名もこれに合わせます。

- clone 直後は `git submodule update --init --recursive` で取得します（PaperMod と同じ）。
- contests 側が更新されたら、サイト側で `bash scripts/contest/sync.sh` を実行すると submodule の参照を進めてコミットします（push はしません）。localhost で確認してから自分で push すると反映されます。
- 連絡先など公開できない情報は contests には書きません（登録フォームの回答シートが台帳です）。

## 新規ページ作成

1. **contests に大会を登録する。** 大会定義シート（Google スプレッドシート 1 枚。行が項目、列が大会）の「大会」タブで、空いている列の 1 行目に大会 id を書き、値を埋めます。
   ドロップダウンやチェックボックスは最初から付いていて、項目名の頭の「＊」が必須、会期前の大会で必須なのに空のセルは赤く表示されます。
   英語ページも作る大会は「サイトの言語」を「両方」（英語だけなら「英語」）にし、「大会_en」タブの同じ列を埋めます。
   トラックの一覧と文字数などのルールは大会横断の「トラック」「ルール」タブにあり、大会の列では使うトラックにチェックを入れ、ルールセット名を選ぶだけです。
   埋めたらメニュー「大会データ → 大会データを更新」を押します。contests の `contests/<大会 id>/contest.yaml` が書かれ、push まで自動で行われます（ボタンの準備は運営ツールの README）。
   YAML を直接書く必要はなく、未定の値は空欄のままで構いません（ページには「決定次第」と出て、検査で拾えます）。参加フォームは運営ツールの `ops form create <大会 id>` で作り、URL はシートに自動で入ります（もう一度「更新」を押す）。
1. **サイトでページ一式を生成する。**

    ```bash
    bash scripts/contest/sync.sh                                   # contests の最新を取り込む
    python3 scripts/contest/new.py <大会 id> --from <前回の大会 id>   # 英語の雛形が前回に無ければ --from-en inlg_2026 も
    ```

    前回大会の `content/menu/<前回>/` とトップページを複製し、front matter（`date`、`translationKey`、`contest: <大会 id>`）、内部リンク、`hugo.yaml` の大会メニュー、`result.md` を整えます。本文は書き換えません。
    日本語・英語のどちらを作るかは「サイトの言語」で決まります。
1. **本文を今回の内容に書き直す。** 日程・フォーム・役職・試合数・会場などの事実は下のショートコードで書き、文章だけを直します。
   国内大会は前回の国内大会ではなく**直近の国際大会**を元にし、国内固有の部分（言語、学会セッション、スポンサー）だけ戻すと、改善点を引き継げます。
1. **検査する。**

    ```bash
    python3 scripts/contest/check.py <大会 id> --from <前回の大会 id>
    ```

    前回大会の名残、contest.yaml と違うフォーム URL や日付、「決まり次第」「（仮）」などの未記入、日英の対応、メニューの URL 切れを一覧にします。0 件になるまで直します。
1. `hugo server -D` で `/page/<大会 id>` と `/menu/<大会 id>/` を確認してから push します。
1. 以後、シートを直したときは「大会データを更新」→ `bash scripts/contest/sync.sh` → localhost で確認 → push です。日付やフォーム URL はショートコードで出しているので、ページを作り直す必要はありません。

### ショートコード（事実は contests から出す）

ページの front matter に `contest: <大会 id>` があれば、どのページでも使えます。英語ページでは自動で英語になります。

| 書き方 | 出るもの |
|---|---|
| `{{%/* contest-dates format="ja" bold="true" */%}}` | 日程の箇条書き。回が 2 つ以上なら回ごとの見出し付き。`format` は `ja`（2026年7月4日）/ `slash`（2026/05/01）/ `en` |
| `{{%/* contest-date key="venue" */%}}` | 日付を 1 つだけ文中に（`key` は `venue`＝会期、または日程の `key`）。`format` / `sep` / `pad="false"` で書式を合わせる |
| `{{%/* contest-form */%}}` | 参加登録フォームへのリンク |
| `{{%/* contest-tracks indent="  " */%}}` | トラック名の箇条書き |
| `{{%/* contest-roles size="9" */%}}` | 役職の表。`format="x"` で「村人×3, 占い師, …」、`format="plus"` で「村人3 + 占い師1 + …」の 1 行 |
| `{{%/* contest-games */%}}` | トラックごとのチーム当たり試合数の表 |
| `{{%/* contest-venue */%}}` | 併催の学会・会議「名前 [host](url)」。`part="session"` でセッション名、`part="place"` で開催地だけ |
| `{{%/* contest-rule key="talk_chars" */%}}` | ルールの値 1 つ（`talk_chars` / `mention_chars` / `response_timeout_sec` / `anytime_talks_per_day` / `anytime_phase_min`）。`as="min"` で秒を分に |
| `{{%/* contest-sponsors */%}}` | スポンサーの箇条書き |
| `{{%/* contest-name */%}}` | 大会名（英語ページは `name_en`）。「〇〇のサンプルエージェント」のように大会名を書く所に使う |
| `{{%/* contest-text key="character_prompt" */%}}` | `contest.yaml` の `texts.<key>` の自由文（Markdown 可）。英語ページは `<key>_en` |

値が無いときはどのショートコードも決まり文句を出します（文中は「【未定】」、段落は「決定次第掲載します。」、英語は `[TBA]` / `To be announced.`）。検査がこの文言を未記入として拾います。

### content/menu/{{contest_name}}/ と content/page/{{contest_name}}.md

`new.py` が作るファイルの構成は従来どおりです（`agent.md`、`organizer.md`、`program.md`、`regulation.md`、`participation.md` または `schedule_participation.md`、`result.md`、論文投稿があれば `paper_submission.md`）。
各ページで直すべき箇所の目安は次のとおりです。

- **全ファイル共通**: 本文の大会名・年を今回のものに。日付や URL は本文に直書きせずショートコードにする
- **organizer.md**: スポンサーは確定するまで `contest.yaml` の `sponsors` を空にしておく（確定したら書く）
- **program.md**: 基本的に全て入れ替える。確定するたびに更新する
- **regulation.md**: 文章は前回を引き継いで変更点を直す。役職表と文字数などの数値はショートコードから出る

### content/menu/{{contest_name}}/result.md（結果・ログ）

`new.py` が生成します（`layout: result`、`result_page: true`、`results_data: <大会 id>`、`contest: <大会 id>`）。
表はすべて contests の `results.yaml` から描画され、結果・ログタブの `/results/<大会 id>/` と「大会横断の比較」の 4 ページも自動で作られます。

#### 大会が終わったらやること

1. **success ディレクトリを確認する**（aiwolf サーバ）。本戦中にゲームスコアの配信（[ゲームスコアの配信と集計](./win_rates.md)）を動かしていれば、決着したゲームのログは `<トラック>/log/success/` に揃っています。動かしていなかった場合だけ、次で作ります。

    ```bash
    ssh aiwolf
    cd /var/www/html/aiwolf
    python3 ~/bin/make_success_dir.py 2027/INLG/MainTruck5/log 2027/INLG/MainTruck9/log   # <トラック>/log/success ができる
    ```

1. **success ログを手元に取得**し、`scripts/results/contests/<大会 id>.yaml` を書く（`example.yaml` をコピー）。
1. **ゲーム指標と LLM 相対評価の元ファイルを用意する**（任意。無ければその節は「準備中」と表示される）。
    - ゲーム指標: [aiwolf-nlp-calculate-score](https://github.com/aiwolfdial/aiwolf-nlp-calculate-score) の `run` が出す `data/output/<大会>_<トラック>/team_summary.csv`
    - LLM 相対評価: aiwolf-nlp-llm-judge の出力 `team_aggregation.csv`（モデルごとに 1 つ。複数指定すると平均される）
    - 人手評価: 評価フォームの集計シート（totalling CSV）
1. **results.yaml を生成して contests に push する。**

    ```bash
    python3 scripts/results/build_contest_yaml.py scripts/results/contests/<大会 id>.yaml   # external/aiwolf-nlp-contest-data/contests/<大会 id>/results.yaml に書く
    git -C external/aiwolf-nlp-contest-data add -A && git -C external/aiwolf-nlp-contest-data commit -m "結果: <大会 id>" && git -C external/aiwolf-nlp-contest-data push
    ```

1. **表彰を書く。** 発表後に `results.yaml` の `awards.items` へ追加し、`awards.status` を `published` にします（設定ファイルの `awards:` に書いて再生成しても同じ）。
1. サイト側で submodule の参照を進めてコミットし、`hugo server -D` で確認してからデプロイします。

#### results.yaml の項目（抜粋）

| 項目 | 内容 |
|---|---|
| `awards.items[]` | `title` / `title_en` / `team` / `note` / `note_en`（受賞理由や審査員名など任意。チーム名の後ろに括弧書きで出る） |
| `awards.remark` / `remark_en` | 表彰についての補足説明（任意、Markdown 可）。表彰の表の下に段落として出ます。集計の訂正など、受賞そのものは変えずに事情を書くときに使います |
| `availability.human_eval` | `ok` / `none`（未実施）/ `pending`（準備中）。節の文言が切り替わる |
| `availability.llm_judge` | 同上。`posthoc` は「大会後に事後実施」の注記が付く |
| `human_eval_short` | 評価方法ページの表に出す短い表記（例: 学生評価者 3 名） |
| `tracks[].win_rates` | `winrate.py` の出力。`macro`（総合）/ `micro` / `weighted`（構成加重）/ `by_role` |
| `tracks[].game_metrics` | aiwolf-nlp-calculate-score の team_summary.csv から転記した 6 指標 |
| `tracks[].human_eval` | `scale` は `rank`（順位平均）か `rating5`（5 点評点）。`source` は表の上に出る注記 |
| `tracks[].llm_judge` | `models`（評価方法ページの表に出る）/ `source`（表の上に出る注記）/ `posthoc` |
| `tracks[].logs` | ログ一覧の URL（対戦ログ節と対戦ログ一覧ページに出る） |

LLM-as-a-Judge の定量カウントは現在ページから外しています。データは `data/results_archive/quantitative/`（git 管理外）に退避してあり、
復帰させる場合はテンプレートの節を戻す必要があります。

### 大会一覧の仕切り（自動）

トップページの「次回大会」「過去大会」の仕切りは、contests の会期（`venue.end`、無ければ日程の最終日）が今日以降かどうかで自動的に入ります。
終わっていない大会が 1 つも無いときは「近日追加予定」が出ます。`next.md` や `past.md` の日付を手で動かす作業は要りません。

判定はビルド時の日付で行うため、GitHub Actions が毎日 06:00（日本時間）にサイトを再ビルドします（`.github/workflows/hugo.yaml` の `schedule`）。
会期が過ぎた翌朝に仕切りが移ります。

### hugo.yaml

ヘッダーのメニューは 2 階層になっています。

- `main` … サイト全体のメニュー（「大会情報」「結果・ログ」「リンク」）。ヘッダーの上段に常に表示される。新大会のたびに書き換える必要はない
- 大会ごとのメニュー … `content/menu/` のディレクトリ名を小文字にし、末尾の `_en` を除いた名前（例: `inlg_2026`）。その大会のページを開いているときだけ、ヘッダーの下段に大会名とともに表示される

新大会では、前回大会のメニューをコピーして名前と URL を今回のものに直し、大会トップページ `content/page/{{contest_name}}.md` の front matter に `menu_id: <メニュー名>` を書きます（`content/menu/<大会>/` 配下のページはディレクトリ名から自動で判定されます）。

- 「結果・ログ」の項目は本戦が終わってから追加してもよい
- 論文提出のページを使わない場合はその項目を削除する
- `ja` では国内大会および国際大会の日本語用のページを扱い、`en` では国際大会のページを扱う

## 注意点

1. 軽微な文言修正などではブランチを切らなくてもOKです。ただし、`layouts` の変更や新規大会向けのページ作成など、大きな変更を行う場合はブランチを切って作業してください。

1. リポジトリをクローンした直後は、テーマ（PaperMod）を取得する \
    本サイトのテーマ PaperMod は git submodule として管理されているため、クローン直後は `themes/PaperMod` が空です。この状態で `hugo server` を実行してもテーマが読み込まれず、全ページが404になります。以下のコマンドでサブモジュールを取得してください（一度実行すればOKです）。
     ```bash
    git submodule update --init --recursive
    ```

1. 必ずローカルホストで確認してからデプロイ
     ```bash
    hugo server -D
    ```

1. ページはmd形式で作成。作成の際には以下のルールを守ること。
    - [公式ルール](https://raw.githubusercontent.com/DavidAnson/markdownlint/main/doc/Rules.md)
    - [カスタム](https://github.com/aiwolfdial/aiwolf-nlp/blob/main/config/custom.markdownlint.jsonc)

## Webサイトの技術について
<!-- ざっくり説明してチャッピーに書いてもらいました。 -->
<!-- ToDo: 設定項目についての説明を書く -->

### それぞれの概要

本ウェブサイトは、GitHub Pages上にホスティングされており、静的サイトジェネレーターとして [**Hugo**](https://gohugo.io) を利用しています。
Hugoでは、テーマとして [**PaperMod**](https://adityatelange.github.io/hugo-PaperMod) を使用しており、シンプルかつ高速でレスポンシブなデザインを提供しています。

- **Hugo**

    高速な静的サイトジェネレーターで、Markdownファイルから簡単にHTMLを生成できます。
    ローカル環境でプレビューを確認しながら作業できるため、コンテンツ更新やページ追加が容易です。

- **PaperMod**

    Hugo向けの人気テーマの一つで、モダンでシンプルなデザインを提供します。
    記事やページの見やすさに優れており、カスタマイズもしやすい構造になっています。

- **GitHub Pages**

    GitHub上で管理されているリポジトリから自動でデプロイされ、ウェブサイトを公開できます。
    デプロイ作業はGitのプッシュ操作だけで完了し、サーバー管理の手間がほとんどありません。

### テーマのカスタムについて

PaperMod テーマのテンプレートは `themes/PaperMod/layouts` 以下に配置されています。\
Hugo では、同じパスで自サイトの `layouts` フォルダにファイルを置くことで、テーマのテンプレートを上書き（オーバーライド）することが可能です。\
これを利用して、一部テンプレートをカスタマイズしています。

参考: [override-theme-template](https://adityatelange.github.io/hugo-PaperMod/posts/papermod/papermod-faq/#override-theme-template)

- カスタムした内容

    1. 英語用リンクの修正 \
        英語用のサイトへのリンクが何故が正常に作成されなかったため、`header.html`を修正して英語用のサイトのリンクが正しく作られる様にしました。\
        修正内容: [aiwolf-nlp/commit](https://github.com/aiwolfdial/aiwolf-nlp/commit/2a192007eb1a70265dd562c48b42392fae9361d3)
    1. 大会一覧を見やすくするための区切りを追加\
        [aiwolf-nlp](https://aiwolfdial.github.io/aiwolf-nlp/)にアクセスすると過去大会の一覧が出てくると思うのですが、初見だとどれを見たら良いか絶対に分からないと思ったので、区別する文字が欲しいなと思って`----- 次回大会-----`などの文字を追加しました。(より良い方法があればそちらにしてください。)\
        [aiwolf-nlp/commit/](https://github.com/aiwolfdial/aiwolf-nlp/commit/eb0145ae0752977fc004b5d0c0f45d1816f9edde#diff-d1e7544294c58d71d0a3493b08bc1552015d5e88dfcfefac92cf48c42011a1f1R93)

[outlineへ戻る](./outline.md)
[前: 運営を始める前に](./preparing.md)
[次: 参加登録フォームの作成](./registration_form.md)
