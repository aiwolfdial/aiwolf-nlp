---
date: '2026-04-26T14:00:00+09:00'
draft: false
title: 'エージェントの内部状態とデータの流れ'
category: participants_guide
ShowToc: true
---

このページでは、サーバから届いた情報が **エージェント内部のどこに、いつ保存されているか** を整理します。

「`info` や `talk_history` の中身は知っているけど、それがどう保たれているのかピンと来ない」「自分で履歴を貯めたいけど、どこに書けばいいのか分からない」という段階の方に向けたページです。
プロンプトから参照できる変数の正体や、コード側で情報を加工・蓄積するときの取っ掛かりとして使ってください。

---

## このページで扱うこと

1. サーバから届くパケットの構造
2. `set_packet` でパケットがどう内部状態に保存されるか
3. エージェントが保持している属性の一覧（出どころは common 由来か agent 内部か）
4. `Info` / `Setting` / `Talk` などの中身（属性リファレンス）
5. 自分で内部状態を増やすときの手順
6. 増やした状態をプロンプトから参照できるようにする

---

## 1. データの流れ：サーバ → packet → エージェント

サーバから届く JSON は、`aiwolf-nlp-common` の `Packet` オブジェクトに変換されてから、エージェントに渡されます。

```text
サーバ ──(JSON)──▶ Packet.from_dict()        # aiwolf-nlp-common 側
                       │
                       ├─ Info.from_dict()        # 現状態
                       ├─ Setting.from_dict()     # ゲーム設定
                       ├─ Talk.from_dict() × N    # 会話・囁き履歴
                       │
                       ▼
                   agent.set_packet(packet)     # ★ここで内部状態に保存
                       │
                       ▼
                   agent.action()               # 保存済みの状態を使って応答
```

`Packet` は次の構造を持っています（`aiwolf_nlp_common.packet.Packet`）。

| フィールド | 型 | 中身 |
|---|---|---|
| `request` | `Request` | リクエスト種別（`TALK` / `VOTE` など） |
| `info` | `Info \| None` | 現状態。多くのリクエストで届く |
| `setting` | `Setting \| None` | ゲーム設定。基本は `INITIALIZE` のみ |
| `talk_history` | `list[Talk] \| None` | 前回の通信以降に追加された会話の差分 |
| `whisper_history` | `list[Talk] \| None` | 同上（人狼の囁き） |
| `new_talk` | `Talk \| None` | グループチャット方式での新着発言 |
| `new_whisper` | `Talk \| None` | グループチャット方式での新着囁き |

> **ポイント**：`talk_history` / `whisper_history` は **その時点までの差分** であって、ゲーム全体の履歴ではありません。「全体の履歴」を保つのはエージェント側の責任です（次の節で見ます）。

---

## 2. `set_packet` での保存処理

サーバから `Packet` を受け取ると、エージェントは **`set_packet()` の中で内部状態を更新** します（`src/agent/agent.py`）。

```python
# src/agent/agent.py（要点を抜粋）
def set_packet(self, packet: Packet) -> None:
    self.request = packet.request
    if packet.info:
        self.info = packet.info               # ① 上書き
    if packet.setting:
        self.setting = packet.setting         # ① 上書き
    if packet.talk_history:
        self.talk_history.extend(packet.talk_history)        # ② 追加蓄積
    if packet.whisper_history:
        self.whisper_history.extend(packet.whisper_history)  # ② 追加蓄積

    if packet.new_talk:                       # グループチャット方式
        self.talk_history.append(packet.new_talk)
    if packet.new_whisper:
        self.whisper_history.append(packet.new_whisper)

    if self.request == Request.INITIALIZE:    # ③ 新ゲームでリセット
        self.talk_history = []
        self.whisper_history = []
        self.llm_message_history = []
```

3つのパターンが混ざっていることに注目してください。

| パターン | 対象 | 挙動 |
|---|---|---|
| ① **上書き** | `info` / `setting` / `request` | 受信のたびに丸ごと差し替え |
| ② **追加蓄積** | `talk_history` / `whisper_history` | 差分を `extend` してリストに足す |
| ③ **リセット** | `INITIALIZE` 受信時 | 履歴をクリアして次ゲームに備える |

> 「自分で履歴を貯めたい」ときの設計は、基本的にこの3パターンを真似することになります。後ほど「投票履歴を蓄積する」例を扱います。

---

## 3. エージェントが保持している属性

`__init__` と `set_packet` を経て、エージェントインスタンスは次の属性を持ちます。これらは **`_send_message_to_llm` の `key` 辞書からプロンプトに渡される候補** でもあります。

| 属性 | 型 | 出どころ | プロンプトで使える？ |
|---|---|---|---|
| `self.request` | `Request` | common（最後に届いたリクエスト） | ❌ 直接は渡されない |
| `self.info` | `Info` | common（packet.info を上書き保存） | ✅ `info` |
| `self.setting` | `Setting` | common（packet.setting を上書き保存） | ✅ `setting` |
| `self.talk_history` | `list[Talk]` | common 由来を agent 側で蓄積 | ✅ `talk_history` |
| `self.whisper_history` | `list[Talk]` | 同上 | ✅ `whisper_history` |
| `self.role` | `Role` | common（`__init__` で受け取り） | ✅ `role` |
| `self.sent_talk_count` | `int` | **agent 内部**（履歴の送信済み位置） | ✅ `sent_talk_count` |
| `self.sent_whisper_count` | `int` | **agent 内部**（同上） | ✅ `sent_whisper_count` |
| `self.llm_message_history` | `list[BaseMessage]` | agent 内部（LangChain 用） | ❌ 直接は渡されない |
| `self.agent_name` | `str` | agent 内部（接続名） | ❌ 直接は渡されない（`info.agent` で代替できる） |

> **ポイント**：プロンプトで参照できる7変数のうち、5つは common から受け取ったオブジェクトを **そのまま** 渡し、2つ（`sent_talk_count` / `sent_whisper_count`）は **agent 側で計算したカウンタ** を渡しています。
> つまりサンプルの時点で、すでに「common 由来」と「agent 由来」をミックスしてプロンプトに供給する設計になっています。

> **注意**：`talk_history` と `llm_message_history` は **名前が似ていますが別物** です。
> `talk_history` は「ゲーム内で他プレイヤーが何を話したか」のログ（`Talk` のリスト）で、プロンプトに埋め込んで LLM に見せる素材です。
> 一方の `llm_message_history` は「自分が LLM とどうやり取りしたか」の記録（LangChain の `BaseMessage` のリスト）で、`invoke()` にそのまま渡されるものです。
> 詳しくは [背景知識 ＞ LangChainとは ＞ `llm_message_history` と `talk_history` は別物です](../background/about_langchain.md#llm_message_history-と-talk_history-は別物です) を参照してください。

---

## 4. 各属性の中身（リファレンス）

### 4.1 `info`：現状態（`aiwolf_nlp_common.packet.Info`）

サーバから届く JSON をそのままマッピングした dataclass です。プロンプトでよく使う属性を抜粋します。

| 属性 | 中身 | None になる条件 |
|---|---|---|
| `info.day` | 現在の日数（0 始まり） | なし |
| `info.agent` | 自分の名前（例：`ミナト`） | なし |
| `info.game_id` | ゲームの識別子（ログ用途） | なし |
| `info.profile` | 自分のキャラクタープロフィール | `INITIALIZE` 以外では None |
| `info.status_map` | `{"ミナト": Status.ALIVE, ...}` の辞書 | なし |
| `info.role_map` | 各エージェントの役職（**自分以外は見えない**） | なし |
| `info.medium_result` | 霊媒結果（`Judge` オブジェクト） | 霊媒師でない／結果未到着時は None |
| `info.divine_result` | 占い結果（`Judge` オブジェクト） | 占い師でない／結果未到着時は None |
| `info.executed_agent` | 前日追放されたエージェント名 | 初日や追放なしの場合は None |
| `info.attacked_agent` | 前夜襲撃されたエージェント名 | 初日や襲撃なしの場合は None |
| `info.vote_list` | 投票結果のリスト（`Vote` のリスト） | `setting.vote_visibility` が false の場合は None |
| `info.attack_vote_list` | 襲撃投票の結果（`Vote` のリスト） | 人狼でない／非公開の場合は None |
| `info.remain_count` | 残りトーク／囁き回数 | `TALK` / `WHISPER` 以外では None |
| `info.remain_length` | 残り文字数（最低文字数を除く） | `TALK` / `WHISPER` 以外、または文字数制限がない場合は None |
| `info.remain_skip` | 残りスキップ回数 | `TALK` / `WHISPER` 以外では None |

`Judge`（占い／霊媒結果）と `Vote`（投票結果）の中身は次の通りです。

| オブジェクト | 属性 | 中身 |
|---|---|---|
| `Judge` | `.day` / `.agent` / `.target` / `.result` | 判定日 / 判定を出したエージェント / 対象 / 結果（`'HUMAN'` または `'WEREWOLF'`） |
| `Vote` | `.day` / `.agent` / `.target` | 投票日 / 投票したエージェント / 投票先 |

> **重要**：`None` になりうる属性は、テンプレートで参照する前に `{% if ... is not none %}` で囲むのが鉄則です。`None.target` のような参照は描画エラーになります。

### 4.2 `talk_history` / `whisper_history`：会話履歴（`Talk` のリスト）

要素は `Talk` オブジェクトで、次の属性を持ちます。

| 属性 | 中身 |
|---|---|
| `talk.agent` | 発言者の名前 |
| `talk.text` | 発言の本文 |
| `talk.day` | その発言が行われた日数 |
| `talk.turn` | ターン番号（1日の中での順序） |
| `talk.idx` | 発言のインデックス（連番） |
| `talk.skip` | スキップ発言かどうか（`True` / `False`） |
| `talk.over` | 発言を打ち切った（`"Over"`）かどうか |

> プロンプトで履歴を見せるときは、`{% if not w.skip and not w.over %}` で空発言を弾くと読みやすくなります。

### 4.3 `setting`：ゲーム設定（`aiwolf_nlp_common.packet.Setting`）

設定系の属性です。「試合の制約に応じた指示」をプロンプトに入れたいときに使います。

| 属性 | 例 |
|---|---|
| `setting.agent_count` | 「今回は5人戦です」「9人戦です」と明示してプロンプトの方針を切り替える |
| `setting.max_day` | 「最長〇日で決着させる必要があります」（None の場合は制限なし） |
| `setting.role_num_map` | 役職構成をプロンプトに埋め込む（例：`{Role.WEREWOLF: 3, ...}`） |
| `setting.vote_visibility` | 投票結果が公開されるかどうかで指示を切り替える |
| `setting.talk.max_count.per_day` | 「本日の発言は最大〇回です」 |
| `setting.talk.max_length.per_talk` | 「1発言あたり〇〇文字以内にしてください」 |
| `setting.talk.max_skip` | 1日あたりのスキップ上限回数 |
| `setting.vote.allow_self_vote` | 自己投票を許可するか |
| `setting.attack_vote.allow_no_target` | 襲撃なしの夜を許可するか |
| `setting.timeout.action` | アクションのタイムアウト（ミリ秒） |

`setting.whisper.*` は `setting.talk.*` と同じ構造で、囁き用の値が入ります。

### 4.4 `role`：自分の役職（`Role` enum）

`'WEREWOLF' / 'POSSESSED' / 'SEER' / 'BODYGUARD' / 'VILLAGER' / 'MEDIUM'` のいずれか。
プロンプトでは `role.value` で文字列として取り出せます（例：`{% if role.value == 'SEER' %}`）。

### 4.5 `sent_talk_count` / `sent_whisper_count`：履歴の切り出し位置

これは agent 内部のカウンタで、`talk()` / `whisper()` の **末尾** で `len(self.talk_history)` などを保存しています。次のリクエスト時に「まだLLMに渡していない発言だけ」を取り出すための目印として使います。

```jinja
{% for w in talk_history[sent_talk_count:] -%}
{{ w.agent }}: {{ w.text }}
{% endfor %}
```

> 改造する際にも、このパターン（差分だけ渡す）はそのまま踏襲するのがおすすめです。

---

## 5. 自分で内部状態を増やしたいとき

「投票履歴を全日ぶん持ちたい」「占い済みのエージェントを覚えておきたい」のように、`info` には載らない情報を蓄積したくなることがあります。
そのときに触る場所は、基本的に次の2か所です。

### 5.1 `__init__` で属性を初期化する

`src/agent/agent.py` の `__init__` 末尾あたりに、空のリストや辞書を用意します。

```python
def __init__(self, config, name, game_id, role):
    ...
    # 既存の属性
    self.talk_history: list[Talk] = []
    ...
    # ▼ 自分で追加する例
    self.my_vote_history: list[dict] = []
    self.divined: set[str] = set()
```

> **注意**：基底クラス（`agent.py`）に追加すると **すべての役職** に共通になります。占い師だけに必要なものは `seer.py` の `__init__` に書く方が影響範囲を絞れます。

### 5.2 `set_packet` で内容を更新する

サーバから情報が届くタイミングで、`set_packet` の最後に追加処理を書きます。

```python
def set_packet(self, packet):
    super().set_packet(packet)   # 既存処理を必ず先に呼ぶ
    # ▼ 自分の投票分だけ蓄積する例
    if self.info and self.info.vote_list:
        for v in self.info.vote_list:
            if v.agent == self.info.agent:
                self.my_vote_history.append({"day": self.info.day, "target": v.target})
```

> **ポイント**：`set_packet` を上書きするときは、必ず最初に `super().set_packet(packet)` を呼んでください。これを忘れると `self.info` などが更新されなくなり、エージェントが動かなくなります。

### 5.3 `daily_initialize` などで蓄積するパターン

「占い済みのエージェントを覚える」のような、特定のリクエストにだけ反応したい蓄積は、`set_packet` ではなく `daily_initialize` などのフェーズメソッドで書く方が読みやすくなります（[エージェントのカスタマイズ方法 ＞ 改造に慣れてきたら](./customize_agent.md#改造に慣れてきたら) の占い師の例を参照）。

---

## 6. 増やした状態をプロンプトから参照できるようにする

`__init__` に属性を足しただけでは、プロンプト側からは見えません。**`_send_message_to_llm` の `key` 辞書** にエントリを追加して、初めてテンプレート変数として使えるようになります。

```python
# src/agent/agent.py  _send_message_to_llm 内
key = {
    "info": self.info,
    "setting": self.setting,
    "talk_history": self.talk_history,
    "whisper_history": self.whisper_history,
    "role": self.role,
    "sent_talk_count": self.sent_talk_count,
    "sent_whisper_count": self.sent_whisper_count,
    # ▼ 追加するエントリ
    "alive_agents": self.get_alive_agents(),
    "my_vote_history": self.my_vote_history,
}
```

これで `config.yml` のプロンプトから次のように書けるようになります。

```yaml
prompt:
  vote: |-
    生存者: {{ alive_agents | join(", ") }}
    これまでの自分の投票: {{ my_vote_history }}
```

> **ポイント**：テンプレート内で `{% for %}` や `{% if %}` を駆使して情報を切り出すよりも、**Python 側で前処理した結果を `key` に詰める** 方が読みやすく、保守も楽になります。
> たとえば「生存者一覧」は `info.status_map` から `{% for %}` でフィルタしても作れますが、`get_alive_agents()` のヘルパーを `key` に登録する方がプロンプトはスッキリします。

---

## 7. よくある追加例

### 例1：生存者一覧をプロンプトで使う

`agent.py` には既に `get_alive_agents()` メソッドが定義されているので、`key` に1行足すだけで使えるようになります。

```python
key = {
    ...
    "alive_agents": self.get_alive_agents(),   # ← 追加
}
```

```yaml
prompt:
  vote: |-
    生存者: {{ alive_agents | join(", ") }}
    最も人狼の可能性が高いエージェントの名前だけを出力してください。
```

### 例2：自分の投票履歴を全日ぶん貯める

`info.vote_list` には **今日の** 結果しか入りません。過去分も使いたいなら、5.1 と 5.2 のパターンで蓄積します。

```python
# __init__
self.my_vote_history: list[dict] = []

# set_packet（または daily_initialize）
if self.info and self.info.vote_list:
    for v in self.info.vote_list:
        if v.agent == self.info.agent:
            self.my_vote_history.append({"day": self.info.day, "target": v.target})

# _send_message_to_llm
key = {..., "my_vote_history": self.my_vote_history}
```

### 例3：会話履歴を要約してプロンプトに載せる

履歴がトークン数を圧迫してきたら、Python 側で要約して短い文字列に変換しておく方法があります。

```python
def _summarize_talk_history(self) -> str:
    # 自前のロジックや LLM 呼び出しで要約する
    ...

key = {..., "talk_summary": self._summarize_talk_history()}
```

```yaml
prompt:
  talk: |-
    これまでの議論の要約:
    {{ talk_summary }}
    ...
```

---

## まとめ

* サーバから届いた `Packet` は、`set_packet` で `self.info` / `self.setting` / `self.talk_history` などに保存される
* プロンプトから参照できる変数は、`_send_message_to_llm` の `key` 辞書に入っているもの（既定では7つ）
* 既定の7つは、common 由来のオブジェクトをそのまま渡しているもの（5つ）と、agent が計算したカウンタ（2つ）の混合
* 新しい情報を渡したいときは、**`__init__` で属性を作り → `set_packet` で更新 → `key` 辞書に登録** の3ステップ
* 詳しい使い方は [プロンプトエンジニアリング](./prompt_engineering.md) と [エージェントのカスタマイズ方法](./customize_agent.md) を参照

---

[参加者マニュアルトップへ](../_index.md)\
[改良・拡張トップへ](./_index.md)\
[前へ（config.ymlの説明）](./config_explanation.md)\
[次へ（プロンプトエンジニアリング）](./prompt_engineering.md)
