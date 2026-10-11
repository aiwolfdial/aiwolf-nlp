---
date: '2025-10-04T09:40:00+09:00'
draft: false
title: '大きな変更をするとき'
category: organizer_guide
weight: 13
ShowToc: true
---

ふだんの運営はシートを書くだけで済みます。このページは、**シートの値を変えるだけでは足りない変更**をするときのためのものです。
どれも影響が大きいので、ブランチを切るか、ほかの運営メンバーに一声かけてから行ってください。

## シートで足りるもの（コードは触らない）

| やりたいこと | すること |
| --- | --- |
| 新しいトラックを足す（例: いつでも発話 × 9人村） | シートの「トラック」「トラック_en」タブに行を足す。大会の列の「開催トラック」にチェック欄が増えるのは、次の「シートの形を作り直す」の後 |
| ルールの値を変える、ルールセットを足す | シートの「ルール」タブの値を直す、列を足す |
| 新しい村の人数（役職構成） | aiwolf-nlp-contest-data の `roles/<人数>.yaml` を足す |

## シートに項目（行）を足す

サイトやフォームで新しい情報を使いたいときです。

1. 使う側を先に作ります（サイトのショートコード、organize-tool の処理など）。
1. aiwolf-nlp-contest-data の `schema/fields.yaml` に項目（キー、ラベル、型、必須かどうか、用途、説明）を足して push します。
1. organize-tool でシートの形を作り直します。値はそのまま残ります。

    ```bash
    uv run python -m ops contest layout
    ```

一時的な情報なら、シートの「追加項目（自由）」の行に書けば、項目を足さなくても大会データベースに入ります。

## 大会ページの雛形を直す

大会のページは前の大会のページを複製して作るので、**直近の国際大会のページが雛形**になります。
新しい文を足すときは、大会によって変わる部分を[ショートコード](./shortcodes.md)で書きます（大会名、学会、日程、回数や言語による出し分け）。
直したら、国内大会の設定でも崩れないか `new.py` で試しに作って確かめます。

## シートのボタンや道具を作り直す

| 状況 | すること |
| --- | --- |
| シートのメニュー「大会データ」が消えた、送り先のリポジトリが変わった | organize-tool で `uv run python -m ops contest button` |
| シートを新しく作り直したい | aiwolf-nlp-contest-data の `sheet.yaml` の `book_id` を空にして `uv run python -m ops contest layout --from-files`。新しいシートができ、`sheet.yaml` が書き換わるので push する |
| ボタンを押さずに手元で反映したい | `uv run python -m ops contest import --push`（ボタンと同じ処理。差分を見せて確認する） |

## サイトのテンプレートを変える

`layouts` の変更、`hugo.yaml` の設定の変更は、ブランチを切ってプルリクエストにします。
大会一覧の仕切りの判定は `layouts/_default/list.html`、大会データの読み込みは `layouts/partials/contest/` にあります。

## サイトの技術

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
