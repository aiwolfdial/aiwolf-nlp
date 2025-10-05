---
date: '2025-10-04T10:00:00+09:00'
draft: false
title: '人狼知能大会ウェブサイト更新'
category: organizer_guide
ShowToc: true
---

## 新規ページ作成

主に以下のフォルダ内を編集・ページを追加

https://github.com/aiwolfdial/aiwolf-nlp/tree/main/content/menu

https://github.com/aiwolfdial/aiwolf-nlp/tree/main/content/page

- 方法
    <!-- ToDo: hugo newで作成する方法の説明を書く -->
    上記のリポジトリのフォルダに前回大会分のコピーを作成

    今回大会用に日時等修正する

- 注意点

    1. ~~開発はわざわざブランチは切らなくて良い~~ \
        ↑ 多少の文言修正などでは全然切らなくてもよいと思います。ただし、`layouts`などの変更で大幅に変わる場合や、新規大会向けにページを作る際など、大きく変わる際はブランチ切って作業した方が良いかなとも思います。
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