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
    - フロントマターの `date` を今回大会の日付に更新する
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

### content/page/ の仕切りページ

以下のファイルを編集し、大会一覧の表示を整えます。

- `next.md` / `next.en.md`
- `past.md` / `past.en.md`
- `coming_soon.md` / `coming_soon.en.md`

サイトのトップページで大会一覧が表示される際に、過去大会と次回大会の仕切りとして機能しています。
フロントマターの `date` の値を調整し、一覧上で適切な位置に表示されるようにしてください。
`coming_soon` は次大会の予定がない場合のみ、フロントマターの `draft` を `false` に変更します。

### hugo.yaml

- 次回大会のリンクに修正する
- 論文提出のページを使わない場合はコメントアウトする
- `ja` では国内大会のページを扱い、`en` では国際大会のページを扱う

## 注意点

1. 軽微な文言修正などではブランチを切らなくてもOKです。ただし、`layouts` の変更や新規大会向けのページ作成など、大きな変更を行う場合はブランチを切って作業してください。

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
