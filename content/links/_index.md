---
date: '2026-09-26T00:00:00+09:00'
draft: false
title: 'リンク'
description: '公式アカウント、ログ閲覧ツール、公式リポジトリ、過去大会の結果とログの見方。'
---

## 公式アカウント

- 公式 X: [@aiwolfdial_nlp](https://x.com/aiwolfdial_nlp) \
    大会情報やサイトの更新情報を発信しています。
- 公式 GitHub: [github.com/aiwolfdial](https://github.com/aiwolfdial) \
    自然言語部門のリポジトリをまとめている organization です。
- 人狼知能プロジェクト: [aiwolf.org](https://aiwolf.org/) \
    人狼知能プロジェクト全体の公式ウェブサイトです。

## ログ閲覧ツール（aiwolf-nlp-viewer）

対戦ログをブラウザ上で観戦・再生できるビューアです。インストール不要で、ホスティング版をそのまま使えます。

- ホスティング版: [aiwolfdial.github.io/aiwolf-nlp-viewer](https://aiwolfdial.github.io/aiwolf-nlp-viewer/)
- ソースコード: [aiwolf-nlp-viewer](https://github.com/aiwolfdial/aiwolf-nlp-viewer)

使い方は次のとおりです。

1. **公開ログをそのまま開く**: [対戦ログ一覧](/results/logs)（全大会・全トラックのリンク集）か各大会の結果ページから「ログ一覧」を開き、見たいログの行の「▶ 開く」を押します。viewer がそのログを読み込んで開きます。
1. **同梱ログから選ぶ**: viewer の [archive ページ](https://aiwolfdial.github.io/aiwolf-nlp-viewer/archive)で、Select Folder（大会名）→ Select Log（ファイル名）の順に選ぶと、過去大会の主観評価に使ったログをすぐに見られます。
1. **手元のファイルを開く**: 同じ archive ページで、ファイルを選択するか、ログの本文をコピーして「クリップボードから貼り付け」を押します。自分で動かしたサーバのログもこの方法で見られます。
1. **URL で開く**: `https://aiwolfdial.github.io/aiwolf-nlp-viewer/archive?url=<ログの URL>` の形でリンクを共有できます（公開ログサーバ上のログのみ）。

## 公式リポジトリ

エージェント開発に使うリポジトリです。環境構築や実行方法は各リポジトリの README を参照してください。

| リポジトリ | 内容 |
|---|---|
| [aiwolf-nlp-agent](https://github.com/aiwolfdial/aiwolf-nlp-agent) | サンプルエージェント |
| [aiwolf-nlp-agent-llm](https://github.com/aiwolfdial/aiwolf-nlp-agent-llm) | LLM を用いたサンプルエージェント |
| [aiwolf-nlp-common](https://github.com/aiwolfdial/aiwolf-nlp-common) | エージェント向けの共通パッケージ |
| [aiwolf-nlp-server](https://github.com/aiwolfdial/aiwolf-nlp-server) | ゲームサーバ |
| [aiwolf-nlp-viewer](https://github.com/aiwolfdial/aiwolf-nlp-viewer) | ログ閲覧ツール（上記） |
| [aiwolf-nlp-llm-judge](https://github.com/aiwolfdial/aiwolf-nlp-llm-judge) | ゲームログを LLM で相対評価するシステム（LLM-as-a-Judge） |

## 過去大会の結果とログの見方

2024 年以降の大会の結果とログは、本サイトの[結果・ログ](/results)にまとめています。

- **大会を選ぶ**: 結果・ログのページで大会のカードを開くと、その大会の結果ページに移ります。各大会のページのメニューにある「結果・ログ」からも同じ内容を見られます。
- **結果ページの構成**: 公式結果（表彰）、勝率、ゲーム指標、人手評価、LLM-as-a-Judge（相対評価）、対戦ログの順に並び、冒頭の目次から各節へ飛べます。指標の意味は各節の冒頭に書いてあります。
- **大会をまたいで見る**: 結果・ログのページ上段「大会横断の比較」に、表彰一覧、評価方法（評価者・モデル）、人手評価との一致度、[対戦ログ一覧](/results/logs)の 4 ページがあります。
- **ログを見る・保存する**: [対戦ログ一覧](/results/logs)または各結果ページ末尾の「対戦ログ」からログ一覧（公開ログサーバ）を開きます。一覧では、行の「▶ 開く」で viewer 表示、「⬇ 保存」で 1 ファイル保存、フォルダ行の「⬇ zip」でフォルダごとの一括保存ができます。
