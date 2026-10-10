---
date: '2025-10-04T14:00:00+09:00'
draft: false
title: '準備（リポジトリと初回設定）'
category: organizer_guide
weight: 2
ShowToc: true
---

運営に参加したら、最初に 1 回だけ行う準備です。

## 運営で使うリポジトリ

運営の作業に使うのは次の 3 つです。同じフォルダに並べて置きます（道具が隣のフォルダを探すため）。

| リポジトリ | 公開 | 役割 |
| --- | --- | --- |
| [aiwolf-nlp](https://github.com/aiwolfdial/aiwolf-nlp) | 公開 | このウェブサイト。大会ページの作成と更新 |
| [aiwolf-nlp-contest-data](https://github.com/aiwolfdial/aiwolf-nlp-contest-data) | 公開 | 大会データ（大会の定義、参加チーム一覧、結果）。シートのボタンで自動更新されるので、手で編集しない |
| [aiwolf-nlp-organize-tool](https://github.com/aiwolfdial/aiwolf-nlp-organize-tool) | 非公開 | 運営の道具（`ops` コマンド）。フォームの作成、登録の通知、大会サーバの設定、結果の集計 |

```bash
mkdir aiwolfdial && cd aiwolfdial
git clone --recursive https://github.com/aiwolfdial/aiwolf-nlp.git
git clone https://github.com/aiwolfdial/aiwolf-nlp-contest-data.git
git clone git@github.com:aiwolfdial/aiwolf-nlp-organize-tool.git
```

`aiwolf-nlp` は `--recursive` で、テーマと大会データ（submodule）も一緒に取得します。
付け忘れたら `git submodule update --init --recursive` を実行してください。テーマが無いと全ページが 404 になります。

### そのほかのリポジトリ

| リポジトリ | 概要 |
| --- | --- |
| aiwolf-nlp-server | 大会のゲームサーバ |
| aiwolf-nlp-agent-llm | LLM で発話するサンプルエージェント。参加者向けの基準 |
| aiwolf-nlp-agent | テンプレートから発話するサンプルエージェント。サーバの動作確認に使える |
| aiwolf-nlp-common | サーバが送る JSON をオブジェクトに変換するパッケージ |
| aiwolf-nlp-viewer | 対戦ログのビューア |
| aiwolf-nlp-calculate-score | 勝率とゲームスコアの計算。本戦中の配信にも使う |
| aiwolf-nlp-llm-judge | 主観評価と同じ項目を LLM で順位付けする |
| aiwolf-nlp-log-picker / aiwolf-nlp-log-translator | 評価用ログの抽出、ログの翻訳 |

必要になったときに同じフォルダへ clone してください。

## 運営の道具（aiwolf-nlp-organize-tool）の初回設定

```bash
cd aiwolf-nlp-organize-tool
uv sync          # 依存の導入（uv が無ければ https://docs.astral.sh/uv/ で入れる）
uv run python -m ops --help
```

Google（フォームの作成、シートの読み書き）と Slack（通知）を使うために、次を用意します。手順の詳細はリポジトリ内の `docs/setup_google.md` にあります。

- **Google へのログイン**: `clasp login` で運営の共有アカウントにログインします。フォームの作成で使います。
  ログインの有効期限は 7 日です。切れたらコマンドが案内を出すので、もう一度ログインします。
- **秘密情報**: サービスアカウントの鍵と Slack Bot のトークンを管理者から受け取り、`~/.ops/` に置きます（`secrets.env.example` を参照）。
  **チャットやリポジトリには貼らないでください。**

## 大会定義シートを使う準備

- 管理者にシートの**編集権限**をもらいます。
- シートのメニュー「大会データ → 大会データを更新」を使う人は、GitHub のトークンを 1 回設定します（[大会定義シートの使い方](./sheet.md#更新ボタンの準備初回だけ)）。

## GitHub Organization への参加

aiwolfdial の Organization に参加し、上の 3 つのリポジトリに書き込めるようにしてもらいます。

## 大会サーバへの接続（後半の作業で使う）

予選・本戦を動かす人は、大会サーバに SSH で入れるようにします。

1. 自分の PC で鍵のペアを作り、公開鍵を運営の人に渡します（参考: [SSH鍵を生成するコマンドと全手順解説](https://qiita.com/to3izo/items/9b5b80430e43cd3c4e3c)）。
1. 運営の人が公開鍵をサーバの `~/.ssh/authorized_keys` に追記します。
1. `~/.ssh/config` に次を書きます。IP アドレスは運営の人に聞いてください。

    ```text
    Host aiwolf
    HostName [人狼サーバの IP アドレス]
    User aiwolf
    IdentityFile ~/.ssh/[秘密鍵のファイル名]
    ```

1. `ssh aiwolf` で接続できることを確かめます。
