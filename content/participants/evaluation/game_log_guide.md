---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: 'ゲームログの見方'
category: participants_guide
---

このページでは、**ゲームの進行を記録した生ログ（`.log` ファイル）**の読み方を解説します。
サーバを起動した **ディレクトリ直下の `log/` フォルダ**に保存され、**`.log` 形式**と**`.json` 形式**の2種類が出力されます。

* **game_logger（.log）** … ゲームの進行を人が読みやすい形で記録（このページで解説）
* **json_logger（.json）** … サーバと各エージェントの通信（Packet）を JSON で記録（機械処理・集計向け）

> 実際に流れを追うときは、次セクションで紹介する **aiwolf-nlp-viewer** を使うと直観的に理解できます。

---

## 出力場所とファイル

* 既定では **サーバを起動した場所に `log/` ディレクトリが作成** されます。
* ファイル名や出力有無はサーバ設定（`game_logger` / `json_logger`）で調整できます。

> 設定の詳細は「設定ファイルについて」を参照（`json_logger` は通信ログ、`game_logger` は進行ログ）。

---

## 行の基本フォーマット

**各行はカンマ区切り**で、**第1項がゲームの日付（day）**、**第2項が行の種類（種別）**です。
以降の項目は、行の種類によって構成が変わります。

```text
<日付>,<行の種類>,<項目3>,<項目4>,...
```

例：

```text
0,talk,3,1,2,こんにちは
^ ^    ^ ^ ^ └ 発話内容
| |    | | └── 発話エージェント番号
| |    | └──── ターン番号
| |    └────── 発話ID（その日のn番目）
| └────────── 行の種類
└────────────── ゲーム日付（0日目）
```

---

## 行の種類ごとの構造

以下に、**代表的な行種別**と**各項目の意味**をまとめます。
（「実装参照」は、詳細実装の読みどころです）

### 3.5 `status` 行（各プレイヤーの状態）

| 項目名      | 変数名                                                   | 型       | 説明                  |
| -------- | ----------------------------------------------------- | ------- | ------------------- |
| 日付       | `g.currentDay`                                        | 整数（%d）  | ゲームの日付              |
| 行の種類     | `"status"`（固定）                                        | 文字列     | この行がエージェントの状態を表す           |
| 番号 | `agent.Idx`                                           | 整数（%d）  | エージェントの番号            |
| 役職      | `agent.Role.Name`                                     | 文字列（%s） | エージェントの役職        |
| 生死     | `g.getCurrentGameStatus().StatusMap[*agent].String()` | 文字列（%s） | エージェントの生死 |
| 元の名前     | `agent.OriginalName`                                  | 文字列（%s） | ゲーム開始前の名前           |
| ゲーム内名    | `agent.GameName`                                      | 文字列（%s） | ゲーム内の表示名            |

実装参照：[`aiwolf-nlp-server/logic/game.go L198`](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/logic/game.go#L198)

---

### `talk` 行（発話）

| 項目名        | 変数名              | 型       | 説明                |
| ---------- | ---------------- | ------- | ----------------- |
| 日付         | `g.currentDay`   | 整数（%d）  | ゲームの日付            |
| 行の種類       | `"talk"`（固定）     | 文字列     | この行が発話を表す         |
| 発話ID       | `talk.Idx`       | 整数（%d）  | この日の何番目の発話か |
| ターン番号      | `talk.Turn`      | 整数（%d）  | 何順（ターン）目の発話か |
| 発話エージェント番号 | `talk.Agent.Idx` | 整数（%d）  | 発話したエージェントの番号     |
| 発話内容       | `talk.Text`      | 文字列（%s） | 発話の内容             |

実装参照：[`aiwolf-nlp-server/logic/communication.go L208`](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/logic/communication.go#L208)

---

### `whisper` 行（人狼の囁き）

| 項目名        | 変数名              | 型       | 説明                                            |
| ---------- | ---------------- | ------- | --------------------------------------------- |
| 日付         | `g.currentDay`   | 整数（%d）  | ゲームの日付                                        |
| 行の種類       | `"whisper"`（固定）     | 文字列     | この行が囁きを表す |
| 囁きID       | `talk.Idx`       | 整数（%d）  | この日の何番目の囁きか                             |
| ターン番号      | `talk.Turn`      | 整数（%d）  | 何順（ターン）目の囁きか                             |
| 囁きエージェント番号 | `talk.Agent.Idx` | 整数（%d）  | 囁きを発話したエージェントの番号                                  |
| 囁き内容       | `talk.Text`      | 文字列（%s） | 囁きの内容                                         |

実装参照：[`aiwolf-nlp-server/logic/communication.go L210`](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/logic/communication.go#L210)

> **注意**：囁きは **生存人狼2名以上** が条件です。行種別の表記は実装変更の影響を受けることがあります。

---

### `divine` 行（占い先指定）

| 項目名          | 変数名                   | 型       | 説明                      |
| ------------ | --------------------- | ------- | ----------------------- |
| 日付           | `g.currentDay`        | 整数（%d）  | ゲームの日付                  |
| 行の種類         | `"divine"`（固定）        | 文字列     | この行が占い先指定を表す                    |
| 占い師エージェント番号   | `agent.Idx`           | 整数（%d）  | 占い師エージェントの番号            |
| 被占いエージェント番号 | `target.Idx`          | 整数（%d）  | 被占いいエージェントの種族（HUMAN / WEREWOLF）              |
| 占い結果         | `target.Role.Species` | 文字列（%s） | `HUMAN` / `WEREWOLF` など |

実装参照：[`aiwolf-nlp-server/logic/divine.go L43`](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/logic/divine.go#L43)

---

### `vote` 行（追放先の投票）

| 項目名          | 変数名            | 型      | 説明           |
| ------------ | -------------- | ------ | ------------ |
| 日付           | `g.currentDay` | 整数（%d） | ゲームの日付       |
| 行の種類         | `"vote"`（固定）   | 文字列    | この行が追放先の投票を表す           |
| 投票エージェント番号   | `agent.Idx`    | 整数（%d） | 投票を行ったエージェントの番号 |
| 被投票エージェント番号 | `target.Idx`   | 整数（%d） | 投票されるエージェントの番号  |

実装参照：[`aiwolf-nlp-server/logic/vote.go L47`](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/logic/vote.go#L47)

---

### `execute` 行（追放結果）

| 項目名          | 変数名                  | 型       | 説明             |
| ------------ | -------------------- | ------- | -------------- |
| 日付           | `g.currentDay`       | 整数（%d）  | ゲームの日付         |
| 行の種類         | `"execute"`（固定）      | 文字列     | この行が追放結果を表す           |
| 被追放エージェント番号 | `executed.Idx`       | 整数（%d）  | 被追放エージェントの番号    |
| 被追放エージェントの役職          | `executed.Role.Name` | 文字列（%s） | 被追放エージェントの役職 |

実装参照：[`aiwolf-nlp-server/logic/execution.go L37`](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/logic/execution.go#L37)

---

### `guard` 行（護衛先指定）

| 項目名          | 変数名                | 型       | 説明       |
| ------------ | ------------------ | ------- | -------- |
| 日付           | `g.currentDay`     | 整数（%d）  | ゲームの日付   |
| 行の種類         | `"guard"`（固定）      | 文字列     | この行が護衛先指定を表す       |
| 騎士エージェント番号   | `agent.Idx`        | 整数（%d）  | 騎士エージェントの番号   |
| 被護衛エージェント番号 | `target.Idx`       | 整数（%d）  | 騎士に護衛されるエージェントの番号     |
| 被護衛エージェントの役職     | `target.Role.Name` | 文字列（%s） | 護衛されるエージェントの役職 |

実装参照：[`aiwolf-nlp-server/logic/guard.go L41`](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/logic/guard.go#L41)

---

### `attackVote` 行（襲撃先投票）

| 項目名          | 変数名                | 型      | 説明              |
| ------------ | ------------------ | ------ | --------------- |
| 日付           | `g.currentDay`     | 整数（%d） | ゲームの日付          |
| 行の種類         | `"attackVote"`（固定） | 文字列    | この行が襲撃先投票を表す            |
| 投票エージェント番号   | `agent.Idx`        | 整数（%d） | 襲撃投票を行ったエージェントの番号      |
| 被投票エージェント番号 | `target.Idx`       | 整数（%d） | 襲撃投票をされるエージェントの番号 |

実装参照：[`aiwolf-nlp-server/logic/vote.go L49`](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/logic/vote.go#L49)

---

### 3.9 `attack` 行（襲撃結果）※3パターン

#### :one: 襲撃成功（護衛なし）

| 項目名          | 変数名            | 型      | 説明          |
| ------------ | -------------- | ------ | ----------- |
| 日付           | `g.currentDay` | 整数（%d） | ゲームの日付      |
| 行の種類         | `"attack"`（固定） | 文字列    | 襲撃結果        |
| 被襲撃エージェント番号 | `attacked.Idx` | 整数（%d） | 襲撃投票の結果襲撃されたエージェントの番号 |
| 襲撃の成否        | `"true"`（固定）   | 文字列    | 成功を示す   |

実装参照：[`aiwolf-nlp-server/logic/attack.go L40`](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/logic/attack.go#L40)

#### :two: 護衛されて失敗

| 項目名          | 変数名            | 型      | 説明             |
| ------------ | -------------- | ------ | -------------- |
| 日付           | `g.currentDay` | 整数（%d） | ゲームの日付         |
| 行の種類         | `"attack"`（固定） | 文字列    | 襲撃結果           |
| 被襲撃エージェント番号 | `attacked.Idx` | 整数（%d） | 襲撃投票の結果襲撃されたエージェントの番号 |
| 襲撃の成否        | `"false"`（固定）  | 文字列    | 護衛で失敗を示す   |

実装参照：[`aiwolf-nlp-server/logic/attack.go L51`](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/logic/attack.go#L51)

#### :three: 襲撃対象なし

| 項目名          | 変数名            | 型      | 説明                 |
| ------------ | -------------- | ------ | ------------------ |
| 日付           | `g.currentDay` | 整数（%d） | ゲームの日付             |
| 行の種類         | `"attack"`（固定） | 文字列    | 襲撃結果               |
| 襲撃対象エージェント番号 | `-1`（固定）       | 整数（%d） | 対象なしを示す        |
| 襲撃の成否        | `"true"`（固定）   | 文字列    | フェーズが完了したことを示す |

実装参照：[`aiwolf-nlp-server/logic/attack.go 64`](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/logic/attack.go#L64)

---

以上で、**ゲームログ（`.log`）の読み方**の基本は完了です。

---

[参加者マニュアルトップへ](../_index.md)\
[確認・評価トップへ](./_index.md)\
[前へ（ゲームサーバからのデータ）](./server_data.md)\
[次へ（エージェントログの見方）](./agent_log_guide.md)
