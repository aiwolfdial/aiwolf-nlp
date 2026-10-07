---
date: '2025-10-04T10:00:00+09:00'
draft: false
title: '人狼知能大会ウェブサイト更新'
category: organizer_guide
ShowToc: true
---

## 新規ページ作成

主に以下のフォルダ内を編集・ページを追加します。

### content/menu/{{contest_name}}/

<https://github.com/aiwolfdial/aiwolf-nlp/tree/main/content/menu>

大会の参加者に向けた詳細情報をまとめたページ群です。
前回大会のフォルダをコピーし、以下のファイルを作成します（論文投稿がある場合は `paper_submission.md` も追加）。

- `agent.md`
- `organizer.md`
- `program.md`
- `regulation.md`
- `schedule_participation.md`

各ファイルの修正箇所は以下の通りです。

- **全ファイル共通**
    - フロントマターの `date` を現在の日付に更新する
    - コピー元の大会名称・年度でファイル内検索をかけ、今回大会のものに修正する
- **organizer.md**
    - スポンサー情報は確定するまではコメントアウトしておく（先生に確認をとり、確定したらコメントアウトを外す）
- **program.md**
    - 基本的に全て入れ替える。確定するたびに更新する
- **schedule_participation.md**
    - 日程セクションを修正する
    - Googleフォームのリンクを新しいものに置き換える
    - スポンサー情報は確定するまではコメントアウトしておく

### content/page/{{contest_name}}.md

<https://github.com/aiwolfdial/aiwolf-nlp/tree/main/content/page>

大会のトップページです。前回大会のファイルをコピーして作成します。

- 前回からサーバやエージェントおよび大会ルール等で更新した箇所があれば、更新情報セクションに追記する
- Googleフォームのリンクを新しいものに置き換える
- コピー元の大会名称・年度でファイル内検索をかけ、今回大会のものに修正する

### content/menu/{{contest_name}}/result.md（結果・ログ）

各大会のメニューにある「結果・ログ」のページです。中身の表はすべて `data/results/<slug>.yaml` から描画されるので、
`result.md` 自体は front matter だけです（既存大会のものをコピーして `date` と `contest`、`results_data`、`translationKey` を直す）。

- `layout: result` … 表と「ログの見方」を描画するレイアウト
- `result_page: true` … 結果・ログタブの収集対象にする印
- `results_data: <slug>` … 読み込む YAML 名。`<slug>` は `content/menu/` のディレクトリ名を小文字にして末尾の `_en` を除いたもの
- `contest: '2026 国際大会（INLG 2026）'` … タブのカードと横断ページに出る大会名
- `date` … 大会トップページと同じ日付（並び順に使う）

同じ YAML から、結果・ログタブの `/results/<slug>/`（サイト全体メニューの下で開く複製ページ）と、
「大会横断の比較」の 4 ページ（表彰一覧・評価方法・人手評価との一致度・対戦ログ一覧）が自動で作られます。
**タブ側や横断ページに手で書き足すものはありません。**

#### 大会が終わったらやること

1. **success ディレクトリを作る**（aiwolf サーバ）。決着したゲームのログだけを集めます。既にあるトラックは再実行しても差分だけ更新されます。

    ```bash
    ssh aiwolf
    cd /var/www/html/aiwolf
    python3 ~/bin/make_success_dir.py 2027/INLG/MainTruck5/log 2027/INLG/MainTruck9/log   # <トラック>/log/success ができる
    ```

1. **success ログを手元に取得**し、`scripts/results/contests/<slug>.yaml` を書く（`example.yaml` をコピー）。トラックごとにログの URL、取得先ディレクトリ、集計元ファイルを指定します。

1. **ゲーム指標と LLM 相対評価の元ファイルを用意する**（任意。無ければその節は「準備中」と表示される）。
    - ゲーム指標: calculate_meta の `./analyze.py` を実行した `data/output/<データセット>/team_summary.csv`
    - LLM 相対評価: aiwolf-nlp-llm-judge の出力 `team_aggregation.csv`（モデルごとに 1 つ。複数指定すると平均される）
    - 人手評価: 評価フォームの集計シート（ログ × チーム × 評価項目の平均順位が入った totalling CSV）

1. **YAML を生成する。**

    ```bash
    python3 scripts/results/build_contest_yaml.py scripts/results/contests/<slug>.yaml
    ```

1. **表彰を書く。** 発表後に `data/results/<slug>.yaml` の `awards.items` へ「賞名 / 英語名 / チーム / 注記」を追加し、`awards.status` を `published` にします。設定ファイルの `awards:` に書いて再生成しても同じです。

1. `hugo server -D` で `/menu/<大会>/result/` と `/results/` を確認してからデプロイします。

#### YAML の項目（抜粋）

| 項目 | 内容 |
|---|---|
| `awards.items[]` | `title` / `title_en` / `team` / `note` / `note_en`（受賞理由や審査員名など任意。チーム名の後ろに括弧書きで出る） |
| `awards.remark` / `remark_en` | 表彰についての補足説明（任意、Markdown 可）。表彰の表の下に段落として出ます。集計の訂正など、受賞そのものは変えずに事情を書くときに使います |
| `availability.human_eval` | `ok` / `none`（未実施）/ `pending`（準備中）。節の文言が切り替わる |
| `availability.llm_judge` | 同上。`posthoc` は「大会後に事後実施」の注記が付く |
| `human_eval_short` | 評価方法ページの表に出す短い表記（例: 学生評価者 3 名） |
| `tracks[].win_rates` | `winrate.py` の出力。`macro`（総合）/ `micro` / `weighted`（構成加重）/ `by_role` |
| `tracks[].game_metrics` | calculate_meta の team_summary.csv から転記した 6 指標 |
| `tracks[].human_eval` | `scale` は `rank`（順位平均）か `rating5`（5 点評点）。`source` は表の上に出る注記 |
| `tracks[].llm_judge` | `models`（評価方法ページの表に出る）/ `source`（表の上に出る注記）/ `posthoc` |
| `tracks[].logs` | ログ一覧の URL（対戦ログ節と対戦ログ一覧ページに出る） |

LLM-as-a-Judge の定量カウントは現在ページから外しています。データは `data/results_archive/quantitative/`（git 管理外）に退避してあり、
復帰させる場合はテンプレートの節を戻す必要があります。

### content/page/ の仕切りページ

以下のファイルを編集し、大会一覧の表示を整えます。

- `next.md` / `next.en.md`
- `past.md` / `past.en.md`
- `coming_soon.md` / `coming_soon.en.md`

サイトのトップページで大会一覧が表示される際に、過去大会と次回大会の仕切りとして機能しています。
フロントマターの `date` の値を調整し、一覧上で適切な位置に表示されるようにしてください。
`coming_soon` ファイルは次大会の予定がない場合のみ、フロントマターの `draft` を `false` に変更します。

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
