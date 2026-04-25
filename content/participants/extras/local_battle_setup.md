---
date: '2026-04-26T14:00:00+09:00'
draft: false
title: 'サーバ設定の編集方法'
category: participants_guide
---

このページでは、**サーバの設定ファイルを自分で編集** して、対戦のルールや環境を変更する方法を紹介します。
サーバ本体はクローンしなくても配布バイナリで動きますが、設定ファイル（`default_5.yml` など）を書き換えるだけで、**役職の人数・発言制限・タイムアウト・キャラクター情報** などを自由に調整できます。

---

## 何ができる？

設定ファイルを編集すると、例えば以下のようなことができます。

* 村人の人数を増やしたり、騎士を減らしたりする
* 1日あたりの発言回数・文字数の上限を変える
* タイムアウトの時間を延ばす（デバッグ時に便利）
* プレイヤーのキャラクター名・性格をオリジナルのものに差し替える
* 投票の可視化（誰が誰に投票したか）をON/OFFする

---

## 設定ファイルの入手

[サーバの起動方法](../execution/server.md) の手順通りにダウンロードしていれば、手元に `default_5.yml` / `default_9.yml` / `default_13.yml` があるはずです。

元のファイルを残しておきたい場合は、コピーして編集しましょう。

```bash
cp default_5.yml my_custom_5.yml
```

起動時に `-c` オプションで新しいファイルを指定すれば、そちらが使われます。

```bash
./aiwolf-nlp-server-linux-amd64 -c ./my_custom_5.yml
```

---

## よく編集する項目

### 役職の人数を変える

`logic.roles` のブロックで、役職ごとの人数を指定しています。

```yaml
logic:
  roles:
    5:
      WEREWOLF: 1
      POSSESSED: 1
      SEER: 1
      BODYGUARD: 0
      VILLAGER: 2
      MEDIUM: 0
```

合計が `game.agent_count` と一致している必要があります。

### 発言の制限を変える

`game.talk` で発言の回数・文字数の上限を設定できます。

```yaml
game:
  talk:
    max_count:
      per_agent: 4    # 1人あたり1日に話せる回数
      per_day: 20     # 1日の総発言回数の上限
    max_length:
      base_length: 50 # 1発言の基本文字数
      mention_length: 50
      per_talk: -1
      per_agent: -1
```

`-1` を指定すると「制限なし」になります。

### タイムアウトを延ばす

開発中、LLMの応答が遅いためにタイムアウトしてしまうときは、`server.timeout` を調整します。

```yaml
server:
  timeout:
    action: 60s      # エージェントのアクション1回あたりの制限時間
    response: 120s   # 接続全体の応答制限
    acceptable: 5s
```

### 投票の可視化

`game.vote_visibility` を `true` にすると、昼の投票結果が `info.vote_list` としてエージェントに届きます。
`false` にすると届かなくなり、より本物の人狼ゲームに近い状況を再現できます。

---

## キャラクター名を自分好みにする

サーバには **カスタムプロフィール** という仕組みがあります。
`custom_profile.enable: true` にすると、あらかじめ登録されたキャラクター名・性格・年齢などがプレイヤー名の代わりに割り当てられます。

```yaml
custom_profile:
  enable: true
  profile_encoding:
    age: 年齢
    gender: 性別
    personality: 性格
  profiles:
    - name: カスタム太郎
      avatar_url: https://example.com/avatar.png
      voice_id: 3
      age: 20
      gender: 男性
      personality: 冷静で論理的なタイプ。
    # 必要な人数分だけ追加する
```

キャラクター情報は、`INITIALIZE` 時にエージェント側の `info.profile` として受け取れます。
プロンプトでこの情報をLLMに伝えれば、**各プレイヤーの人格を反映した会話** を生成できます。

---

## 自己対戦ではなく自由マッチングにしたい

デフォルトでは「同じチーム名のエージェント同士しかマッチングしない」自己対戦モードになっています。
異なるチーム同士で対戦させたい場合は、`matching.self_match` を `false` にします。

```yaml
matching:
  self_match: false
  team_count: 5
  game_count: 5
```

---

## ログの保存先を変える

`json_logger` と `game_logger` の `output_dir` を変えると、ログの保存場所を指定できます。

```yaml
json_logger:
  enable: true
  output_dir: ./log/json

game_logger:
  enable: true
  output_dir: ./log/game
```

---

## より詳しい項目一覧

すべての設定項目は、公式ドキュメントで公開されています。

* [aiwolf-nlp-server / 設定ファイルについて](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/doc/ja/config.md)

---

## 編集するときのコツ

* **元のファイルは残しておく**：何か壊しても戻せるように、コピーしてから編集するのがおすすめです。
* **1つずつ変えて確認する**：複数の項目を同時に変えると、挙動の原因が分からなくなります。
* **ゲームログで結果を確認する**：変更が効いているかは、ゲーム終了後のログで確認しましょう。

---

[参加者マニュアルトップへ](../_index.md)\
[応用編トップへ](./_index.md)\
[前へ（本戦編）](../competition/main_round.md)\
[次へ（playground：人狼以外の議論にも使える環境）](./playground.md)
