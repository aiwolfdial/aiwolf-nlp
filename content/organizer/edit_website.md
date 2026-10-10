---
date: '2025-10-04T10:00:00+09:00'
draft: false
title: 'サイトの更新'
category: organizer_guide
weight: 7
ShowToc: true
---

大会データ（aiwolf-nlp-contest-data）が更新されたら、このサイト（aiwolf-nlp）に取り込み、**localhost で確認してから自分で push** します。
大会データの更新は自動ですが、公開サイトへの反映は必ず人が確認します。

## 新しい大会のページを作る（初回）

```bash
cd aiwolf-nlp
git pull
bash scripts/contest/sync.sh                                            # 大会データの最新を取り込む
python3 scripts/contest/new.py <大会 id> --from <直近の国際大会 id>      # ページ一式を作る（例: --from inlg_2026）
python3 scripts/contest/check.py <大会 id> --from <直近の国際大会 id>    # 直すところを一覧にする
```

**国内大会も直近の国際大会から作ります。** 国際大会のページが最新のルールと説明を持っているためです。
回数・国内 / 国際・対戦言語・論文の有無で変わる文は雛形が出し分けるので、国内大会に複製しても書き直しは要りません。

`new.py` がすること:

- 前回大会のページ（`content/menu/<大会>/` とトップページ）を複製し、日付・リンク・大会メニュー（`hugo.yaml`）を今回の大会に直す
- 日本語・英語のどちらを作るかは、シートの「サイトの言語」で決まる。論文投稿の無い大会では論文提出のページを作らない
- 前回の大会名・学会名・季節・説明画像の言語を今回のものに置き換え、トップの更新情報を空にする（載せるときはコメントを外す）
- プログラムのページは「決定次第掲載します」にする

### 検査の結果の読み方

```text
aiwolfdial2026_winterjp: 直すところ 1 件（ファイル名:行番号 をクリックするとその行が開きます）

content/menu/aiwolfdial2026_winterjp/program.md
  content/menu/aiwolfdial2026_winterjp/program.md:9
      未記入 — placeholder '決定次第'
      > プログラムは決定次第掲載します。

プレビュー:
  http://localhost:1313/aiwolf-nlp/page/aiwolfdial2026_winterjp/
```

- `ファイル名:行番号` を VS Code のターミナルで Ctrl を押しながらクリックすると、その行が開きます。
- その下が直す理由、`>` の行が問題のある行の中身です。
- 前回大会の名残、シートと違う日付やフォームの URL、「決まり次第」「（仮）」などの未記入、回数や対戦言語と合わない記述、日英のページの対応、メニューのリンク切れを拾います。
- **プログラムの「決定次第」だけが残れば完了**です。それ以外は本文を直して、もう一度 `check.py` を流します。

## 確認して公開する

```bash
hugo server -D --poll 700ms --port 1313 --baseURL http://localhost:1313/aiwolf-nlp/ --appendPort=false
```

`sync.sh`・`new.py`・`check.py` の最後に、確認するページの URL が出ます。ファイルを直すと開いているページが自動で更新されます。
問題が無ければ commit して main に push します。GitHub Actions がビルドして、数分で公開サイトに反映されます。

```bash
git add -A && git commit -m "feat: 2027 春季国内大会のページを追加" && git push
```

大きな変更（`layouts` の変更など）はブランチを切ってプルリクエストにします。

## 以後の更新

シートを直したときは、**「大会データを更新」→ `bash scripts/contest/sync.sh` → localhost で確認 → push** です。
日付やフォームの URL はショートコードで出しているので、ページを作り直す必要はありません。`sync.sh` は変わった大会のページの URL を出します。

本文の文章を直すときは、Markdown を直接編集して同じように確認・push します。大会の事実は本文に直書きせず、[ショートコード](./shortcodes.md)で書いてください。

## 大会一覧の仕切り（自動）

トップページの「次回大会」「過去大会」の仕切りは、学会期間の終わり（無ければ日程の最終日）が今日以降かどうかで自動的に入ります。
判定はビルド時の日付なので、GitHub Actions が毎日 06:00（日本時間）にサイトを再ビルドします。会期が過ぎた翌朝に仕切りが移ります。

## 注意点

1. clone 直後はテーマと大会データ（submodule）を取得します（`git submodule update --init --recursive`）。無いと全ページが 404 になります。
1. ページは Markdown で書きます。次のルールを守ってください。
    - [公式ルール](https://raw.githubusercontent.com/DavidAnson/markdownlint/main/doc/Rules.md)
    - [カスタム](https://github.com/aiwolfdial/aiwolf-nlp/blob/main/config/custom.markdownlint.jsonc)
1. 結果・ログのページは[結果・ログのページ](./results_page.md)を参照してください。

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
