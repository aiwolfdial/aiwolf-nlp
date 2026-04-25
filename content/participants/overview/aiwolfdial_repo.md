---
date: '2026-04-20T14:00:00+09:00'
draft: false
title: '関連リポジトリの紹介'
category: participants_guide
---

このページでは、人狼知能大会の開発・運営に使われている主要なリポジトリを紹介します。
最初からすべてを把握する必要はありません。**まずは必須の3つ** を覚えて、必要になったら他のリポジトリも使ってみてください。

---

## 最初に押さえておきたい3つ

この3つが本大会の中心です。どれも [AIWolfDial の GitHub](https://github.com/aiwolfdial) 上にあります。

| リポジトリ | 役割 |
|---|---|
| **[aiwolf-nlp-agent-llm](https://github.com/aiwolfdial/aiwolf-nlp-agent-llm)** | LLMを使うサンプルエージェント。**これを改造して大会に参加します** |
| **[aiwolf-nlp-server](https://github.com/aiwolfdial/aiwolf-nlp-server)** | ゲームサーバ。ローカル対戦・自己対戦・本戦の接続先になる |
| **[aiwolf-nlp-common](https://github.com/aiwolfdial/aiwolf-nlp-common)** | サーバとのやり取りで使う型定義（Python）。`pip` で導入できます |

> `aiwolf-nlp-common` は通常 `pip` でインストールするだけで十分です。改造したい場合だけクローンしてください。

---

## 確認・評価で使うツール

対戦が終わったあと、結果を見るための便利なツールです。

| リポジトリ | 役割 |
|---|---|
| **[aiwolf-nlp-viewer](https://aiwolfdial.github.io/aiwolf-nlp-viewer/)** | ゲームログをブラウザで可視化できます。**クローン不要、Webから直接使えます** |
| **[aiwolf-nlp-llm-judge](https://github.com/aiwolfdial/aiwolf-nlp-llm-judge)** | ログをLLMに評価させて、項目ごとのランキングを出力します |

---

## 運営向け・研究向けのツール

大会運営や研究目的で使われるリポジトリです。通常の参加では触らなくて構いません。

| リポジトリ | 役割 |
|---|---|
| **aiwolf-nlp-log-picker** | 評価用にログをバランスよく抽出する |
| **aiwolf-nlp-log-translator** | ログを多言語翻訳する |
| **aiwolf-nlp** | 大会公式サイト（このマニュアルを公開しているサイト） |

---

## 開発の流れ（最短ルート）

1. **開発する**：`aiwolf-nlp-agent-llm` を改造する
2. **動かす**：`aiwolf-nlp-server` をローカルで起動してエージェントを接続する
3. **見る**：`aiwolf-nlp-viewer` でゲームログを確認する
4. **評価する**：必要に応じて `aiwolf-nlp-llm-judge` で自動評価する

---

## おすすめのフォルダ構成

後々のドキュメントを読みやすくするため、次のようにまとめておくことをおすすめします。

```text
~/aiwolfdial/
├── aiwolf-nlp-agent-llm/   # 開発のメイン（必須）
├── aiwolf-nlp-server/      # ゲームサーバ（あると便利）
└── aiwolf-nlp-game-logs/   # ログ置き場（サーバをここで起動するとログがたまる）
```

> まずは `aiwolf-nlp-agent-llm` だけあれば動き始められます。他のリポジトリは必要になったタイミングで追加しましょう。

---

[参加者マニュアルトップへ](../_index.md)\
[概要トップへ](./_index.md)\
[前へ（サーバから届くデータ）](./server_data.md)\
[次へ（準備）](../preparation/_index.md)
