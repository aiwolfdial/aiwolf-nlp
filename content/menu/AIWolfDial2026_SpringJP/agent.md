---
date: '2026-02-19T13:29:24+09:00'
draft: false
title: 'エージェントの作成と対戦方法'
category: agent
---

人狼知能コンテストでは、参加者が作成したエージェント（自動プレイヤー）を運営側が用意するゲームサーバにリモート接続することで、自動対戦を行います。ゲームサーバは下記の通り公開していますので、ご自分でゲームサーバを立ち上げてテストすることもできます。

## エージェントの実装

エージェントの作成にあたっては、運営側が定義する仕様を満たした通信をするネットワーク接続の対戦エージェントを実装いただきます。人狼知能大会には別にプロトコル部門があり、基本的に仕様は同一ですがネットワーク対戦であること、プロトコル（人狼言語）ではなく自然言語（日本語または英語）を用いる点など（詳細は下記）が異なります。エージェント作成に当たってはライブラリ非互換性の問題を避けるため、プロトコル部門の提供するライブラリではなく下記の公開リポジトリのコードをベースに実装してください。

## ゲームの実行

各エージェント（自動プレイヤー）は、運営の提供するゲームサーバに接続することでゲームの実行をすることができます。本戦においては運営が実行するゲームサーバに接続し、他のチームと対戦することで、予選においては参加者各自が参加トラックに応じて5体または13体のエージェントを運営が実行するゲームサーバに接続することで、自己対戦を行います。

## サンプルエージェントとゲームサーバのソースコード

環境構築や実行方法についてはREADMEを参照してください。お問い合わせは、リポジトリのIssueによる報告もしくはメール、Slackに参加している場合はSlackでお願いいたします。

- [aiwolf-nlp-agent](https://github.com/aiwolfdial/aiwolf-nlp-agent)
    JSAI 2026 のサンプルエージェントです。
- [aiwolf-nlp-server](https://github.com/aiwolfdial/aiwolf-nlp-server)
    JSAI 2026 のゲームサーバです。

## エージェントへの要求事項

エージェントを実装するにあたり必要な注意事項や要求事項に関しては下記ページをご確認ください。\
[大会レギュレーション](/menu/JSAI_2026/regulation)

## エージェント実装の詳細とゲームサーバについて

エージェントの実装にあたっては、下記ドキュメントをお読みの上、詳細必要であればソースコードを参照して下さい。

- プロトコルの実装について
    [aiwolf-nlp-server/doc/protocol.md](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/doc/protocol.md)
- 役職やゲームの流れ、ゲームロジックの実装について
    [aiwolf-nlp-server/doc/logic.md](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/doc/logic.md)

## 対戦のビューア

エージェント同士の対戦をブラウザ上で観戦できるプログラムです。エージェントの実装には必須ではありませんが、観戦用途やログビューアとして必要に応じてご活用いただけます。

[aiwolf-nlp-viewer](https://aiwolfdial.github.io/aiwolf-nlp-viewer/)

## 投票結果の参照について

ゲームサーバの設定で `vote_visibility: true` が有効になっている場合、各エージェントは `daily_initialize` のタイミングで他のエージェントの投票結果（`info.vote_list`）および襲撃投票結果（`info.attack_vote_list`）を受け取ることができます。

サンプルエージェント（aiwolf-nlp-agent-llm）では、プロンプトテンプレート内の `daily_initialize` で以下のように参照しています。
```yaml
{% if info.vote_list is not none -%}
投票結果: {{ info.vote_list }}
{%- endif %}
{% if info.attack_vote_list is not none -%}
襲撃投票結果: {{ info.attack_vote_list }}
{%- endif %}
```

各 `Vote` オブジェクトは `day`（日数）、`agent`（投票者）、`target`（投票先）のフィールドを持ちます。投票や襲撃の判断材料として活用してください。