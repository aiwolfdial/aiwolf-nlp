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

各エージェント（自動プレイヤー）は、運営の提供するゲームサーバに接続することでゲームの実行をすることができます。本戦においては運営が実行するゲームサーバに接続し、他のチームと対戦することで、予選においては参加者各自が参加トラックに応じて5体または9体のエージェントを運営が実行するゲームサーバに接続することで、自己対戦を行います。

## サンプルエージェントとゲームサーバのソースコード

環境構築や実行方法についてはREADMEを参照してください。お問い合わせは、リポジトリのIssueによる報告もしくはメール、Slackに参加している場合はSlackでお願いいたします。

- [aiwolf-nlp-agent](https://github.com/aiwolfdial/aiwolf-nlp-agent)
    JSAI 2026 のサンプルエージェントです。
- [aiwolf-nlp-server](https://github.com/aiwolfdial/aiwolf-nlp-server)
    JSAI 2026 のゲームサーバです。

## エージェントへの要求事項

エージェントを実装するにあたり必要な注意事項や要求事項に関しては下記ページをご確認ください。\
[大会レギュレーション](/menu/AIWolfDial2026_SpringJP/regulation)

## エージェント実装の詳細とゲームサーバについて

エージェントの実装にあたっては、下記ドキュメントをお読みの上、詳細必要であればソースコードを参照して下さい。

- プロトコルの実装について
    [aiwolf-nlp-server/doc/protocol.md](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/develop/doc/ja/protocol.md)
- 役職やゲームの流れ、ゲームロジックの実装について
    [aiwolf-nlp-server/doc/logic.md](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/develop/doc/ja/logic.md)

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

## いつでも発話トラックへの対応

### ターンベースとの違い

従来方式ではサーバが各エージェントに順番に `TALK` リクエストを送信し応答を待機しますが、いつでも発話トラックではエージェントが能動的に発話を送信する方式に変わります。

- `TALK_PHASE_START` 受信後、サーバの要求を待たず自発的に発話を送信する
- 他エージェントの発話は `TALK_BROADCAST` でリアルタイム配信される（`new_talk` フィールドを参照）
- `TALK_PHASE_END` 受信後は送信禁止（以降の送信は無視される）
- 発話を終了する場合は `Over` を送信する（全員が送信すると早期終了）
- `WHISPER` フェーズも同様に `WHISPER_PHASE_START` / `WHISPER_BROADCAST` / `WHISPER_PHASE_END` を使用

### パケット構造

`TALK_BROADCAST` には `new_talk` フィールドが追加されており、1件の新規発話が格納されています。
```json
{
  "request": "TALK_BROADCAST",
  "info": { ... },
  "new_talk": { "idx": 0, "day": 1, "turn": 0, "agent": {...}, "text": "..." }
}
```

### サンプルエージェントでの実装

公開している[サンプルエージェント](https://github.com/aiwolfdial/aiwolf-nlp-agent-llm)では、`TALK_PHASE_START` を受け取ると発話フェーズに入り、一定間隔で `talk()` の結果を自発的に送信します。必要に応じて、発話タイミングや受信時の処理を行うメソッドを書き換え、戦略に応じた挙動を実装してください。`TALK_BROADCAST` で受け取った他エージェントの発話は `on_talk_received` で扱えます。基底クラスにはこのための `handle_talk_phase` や履歴管理の仕組みが用意されています。
