---
date: '2026-04-26T14:00:00+09:00'
draft: false
title: 'プロンプトエンジニアリング'
category: participants_guide
ShowToc: true
---

このページでは、`config.yml` の `prompt` セクションを編集するために必要な知識をまとめます。

最初に `config.yml` の `prompt.*` を見ると、波カッコ・パーセント・ハイフンといった記号を用いてプロンプトが作成されています。これらは **Jinja2 テンプレート** の文法です。そして、そこに埋め込まれている `info` や `talk_history` などの変数は、すべて `agent.py` のコードから渡されています。

「何がどこから来ていて、どう書き換えれば何が変わるのか」についてこちらのページでは解説していきます。

> Jinja2 の書き方そのものに不安のある方は、先に [背景知識 ＞ Jinja2テンプレートとは](../background/about_jinja2.md) に目を通しておくと読み進めやすくなります。
>
> 各変数の **詳しい中身**（`info` のどんな属性が使えるか、`Talk` の構造など）は、姉妹ページの [エージェントの内部状態とデータの流れ](./agent_state.md) にまとめてあります。本ページは「テンプレートをどう書くか」に集中して説明します。

---

## このページで扱うこと

1. プロンプト設計
2. プロンプトが使われるまでの流れ
3. プロンプトから参照できる変数と、その出どころ
4. リクエスト種別ごとのプロンプトキー
5. プロンプトを編集するときの具体的な手順
6. 新しい変数を追加したい・参照情報を増やしたいときのコード改造
7. よくあるつまずき

---

## 1. プロンプト設計

`config.yml` の `prompt` セクションには、リクエスト種別（`talk` / `vote` / `divine` など）ごとに **LLMへの指示文のひな形** が書かれています。

```yaml
prompt:
  talk: |-
    トークリクエスト
    履歴:
    {% for w in talk_history[sent_talk_count:] -%}
    {{ w.agent }}: {{ w.text }}
    {% endfor %}
```

この文字列は **ただの定型文ではなく、Jinja2 というテンプレートエンジンで処理されるテンプレート** です。
`{{ ... }}` の部分には変数の値が、`{% ... %}` の部分には制御構文（if・for など）の結果が埋め込まれ、最終的にただの文字列となって LLM に渡されます。

> Jinja2 を採用している理由は、**Pythonの値をそのまま差し込みやすい** からです。`info` のような複雑なオブジェクトも、`info.day` のように属性アクセスでそのまま使えます。

---

## 2. プロンプトが使われるまでの流れ

プロンプトが実際に LLM に届くまでの流れは、次のようになっています。

```text
サーバ ── リクエスト（JSON） ──▶ starter.py
                                 │
                                 ▼
                          agent.set_packet()        # packet.request を self.request に保存
                                 │                   # info / talk_history などもここで内部に保存
                                 ▼
                          agent.action()            # self.request で分岐（match 文）
                                 │
                                 ▼
                 agent.talk() / vote() / divine()…  # それぞれが…
                                 │
                                 ▼
                 agent._send_message_to_llm(self.request)
                   │
                   ├─ key = self.request.lower()              # 例: Request.TALK → "talk"
                   ├─ config["prompt"][key] を読み込む         # ← ここで config の該当プロンプトが決まる
                   ├─ Jinja2 テンプレートを描画（変数を差し込む）
                   └─ LLM に送信 → 返答を取得
                                 │
                                 ▼
                          サーバへ返答（そのまま送信）
```

鍵になるのは `_send_message_to_llm` です。`src/agent/agent.py` の中で、次のようなことをしています（要点を抜粋）。

```python
# src/agent/agent.py
def _send_message_to_llm(self, request):
    prompt = self.config["prompt"][request.lower()]   # ①テンプレート文字列を取得
    key = {                                           # ②テンプレートに渡す値をまとめる
        "info": self.info,
        "setting": self.setting,
        "talk_history": self.talk_history,
        "whisper_history": self.whisper_history,
        "role": self.role,
        "sent_talk_count": self.sent_talk_count,
        "sent_whisper_count": self.sent_whisper_count,
    }
    template = Template(prompt)
    prompt = template.render(**key).strip()           # ③Jinja2で描画
    ...
    response = self.llm_model.invoke(...).content     # ④LLMに投げる
    return response
```

つまり、**プロンプトに書ける変数は、`key` 辞書に入っているものがすべて** です。逆に言うと、ここに入っていない値は直接は使えません（＝足したいときは `key` にキーを追加する必要がある、という話は後ほど出てきます）。

`key` 辞書に並んでいる7つの値は、**サーバから届いた情報をそのまま渡しているもの** と、**agent 側で計算した値を渡しているもの** の2種類が混ざっています。

| キー | 中身 | 出どころ |
|---|---|---|
| `info` | `Info` オブジェクト | **common 由来**：サーバから届いた `packet.info` を `self.info` に保存したもの |
| `setting` | `Setting` オブジェクト | **common 由来**：`packet.setting` を保存したもの |
| `talk_history` | `Talk` のリスト | **common 由来**：`packet.talk_history` を `extend` で蓄積したもの |
| `whisper_history` | `Talk` のリスト | **common 由来**：同上 |
| `role` | `Role` enum | **common 由来**：`__init__` で受け取った自分の役職 |
| `sent_talk_count` | `int` | **agent 内部**：「ここまでLLMに渡した」位置のカウンタ |
| `sent_whisper_count` | `int` | **agent 内部**：同上（囁き用） |

> **ポイント**：サンプルの時点ですでに「common 由来をそのまま渡す」「agent 側で計算した値を渡す」の **両方のパターンが混在** しています。
> つまり、§6 で扱う「`key` 辞書に新しいエントリを足す」というのは、この混在を **自分の用途に合わせて広げる** 作業にあたります。
>
> 各属性が `set_packet` でどう保存されるかは [エージェントの内部状態とデータの流れ §2](./agent_state.md#2-set_packet-での保存処理) を参照してください。

### 2.1 `config.prompt.<キー>` の名前はどうやって決まっているか

上のコード①で `self.config["prompt"][request.lower()]` としているのがポイントです。ここでの `request` は、`set_packet` のときにサーバから受け取って `self.request` に保存された **`Request` enum の値**（例：`Request.TALK`、`Request.VOTE` など）で、これを `.lower()` で小文字の文字列に変換した結果が、そのまま `config.prompt` の **キー名** として使われます。

| サーバから届く `Request` | `config.prompt` のキー名 |
|---|---|
| `Request.INITIALIZE` | `initialize` |
| `Request.DAILY_INITIALIZE` | `daily_initialize` |
| `Request.TALK` | `talk` |
| `Request.WHISPER` | `whisper` |
| `Request.DAILY_FINISH` | `daily_finish` |
| `Request.VOTE` | `vote` |
| `Request.DIVINE` | `divine` |
| `Request.GUARD` | `guard` |
| `Request.ATTACK` | `attack` |

つまり、**リクエスト種別とプロンプトのキーは 1 対 1 で固定的に結び付いています**。`config.yml` に `my_strategy:` のような独自キーを書いても、対応する `Request` が存在しないため **そのままでは呼び出されません**（コード側で `if request.lower() not in self.config["prompt"]` を見て、未定義のキーは黙って `None` を返しています）。

独自のキーを追加したい／特定のタイミングで別のプロンプトに差し替えたい場合は、`agent.py` にメソッドを足してプロンプトを自分で呼び出す必要があります。コード側の具体的な手順は、姉妹ページの [エージェントのカスタマイズ方法 ＞ 独自キーのプロンプトを追加する](./customize_agent.md#独自キーのプロンプトを追加する) を参照してください（このページでは、既存リクエストに対してプロンプトがどう使われるかに絞って説明します）。

---

## 3. プロンプトから参照できる変数

### 3.1 変数一覧

`_send_message_to_llm` がテンプレートに渡すのは、以下の7つです。

| 変数 | 型 | 中身の概要 |
|---|---|---|
| `info` | `Info` | 現在の日数・自分の名前・生死マップ・前日までの結果など。**最もよく使う** |
| `setting` | `Setting` | ゲーム設定（人数・発言回数上限・タイムアウトなど） |
| `talk_history` | `list[Talk]` | その日の会話履歴（`agent` / `text` / `day` などを持つ） |
| `whisper_history` | `list[Talk]` | 人狼同士の囁き履歴 |
| `role` | `Role` | 自分の役職（`role.value` で `'SEER'` などの文字列） |
| `sent_talk_count` | `int` | 前回までにLLMへ渡した `talk_history` の末尾位置 |
| `sent_whisper_count` | `int` | 前回までにLLMへ渡した `whisper_history` の末尾位置 |

> 各変数の **属性レベルの詳細**（`info.day` / `info.status_map` / `Talk.agent` などの中身、None になる条件など）は、[エージェントの内部状態とデータの流れ §4](./agent_state.md#4-各属性の中身リファレンス) にまとめてあります。
> プロンプトを書きながら「この情報、属性で言うとどれだっけ？」となったら、そちらを開いて辞書代わりに参照してください。

### 3.2 よく使うパターン

ここでは、**テンプレート上での書き方** に絞って代表的なパターンを示します。

#### 3.2.1 None になる属性は守る

`info.medium_result` のように、役職や進行状況によって `None` になる属性を裸で参照すると、テンプレート描画が落ちます。

```jinja
{% if info.medium_result is not none -%}
霊媒結果: {{ info.medium_result.target }} は {{ info.medium_result.result }}
{%- endif %}
```

> どの属性が `None` になりうるかは [エージェントの内部状態とデータの流れ §4.1](./agent_state.md#41-info現状態aiwolf_nlp_commonpacketinfo) の「None になる条件」列を参照してください。

#### 3.2.2 履歴は差分だけ渡す（`sent_talk_count` の使い方）

`talk_history` は **そのゲーム全体** の会話が蓄積され続けるリストです。
毎回すべてを LLM に渡すと、トークン数が肥大化し、応答も遅く・高コストになります。

そのため、サンプルプロンプトでは

```jinja
{% for w in talk_history[sent_talk_count:] -%}
{{ w.agent }}: {{ w.text }}
{% endfor %}
```

のように「まだ渡していない新しい発言だけ」を切り出して渡すパターンを採用しています。
LangChain 側で会話履歴を保持しているため、**差分だけ追加** する形でも文脈は維持されます。

> 改造する際にも、このパターン（「差分だけ渡す」）はそのまま踏襲するのがおすすめです。囁き側は `whisper_history[sent_whisper_count:]` と書きます。

#### 3.2.3 スキップ発言を弾く

`talk.skip` や `talk.over` が `True` の要素は中身の `text` に意味がないことが多いので、履歴を見せるときは弾いておくと読みやすくなります。

```jinja
{% for w in talk_history[sent_talk_count:] -%}
{% if not w.skip and not w.over -%}
{{ w.agent }}: {{ w.text }}
{% endif -%}
{% endfor %}
```

---

## 4. リクエスト種別ごとのプロンプトキー

プロンプトは、 **リクエスト種別ごとに別のテンプレート** を使います。キー名はすべて小文字です。以下はサンプルエージェントにおける各キーの説明をまとめた表です。

| キー | 呼び出されるタイミング | 代表的に使う変数 | 返答の扱い |
|---|---|---|---|
| `initialize` | ゲーム開始時 | `info.agent` / `role.value` / `info.profile` | **返答は送信されない**（指示文としてのみ使う） |
| `daily_initialize` | 各日の朝 | `info.day` / `info.*_result` / `info.executed_agent` | 同上 |
| `talk` | 発言ターン | `talk_history[sent_talk_count:]` | 発言としてそのまま送信 |
| `whisper` | 人狼の囁きターン | `whisper_history[sent_whisper_count:]` | 囁きとしてそのまま送信 |
| `daily_finish` | 各日の終わり | `info.*_result` / `info.vote_list` | 送信されない |
| `vote` | 追放投票 | `info.status_map` | **対象の名前** として送信 |
| `divine` | 占い | `info.status_map` | 対象の名前として送信 |
| `guard` | 護衛 | `info.status_map` | 対象の名前として送信 |
| `attack` | 襲撃 | `info.status_map` | 対象の名前として送信 |

> **注意**：`vote` / `divine` / `guard` / `attack` では、LLMの出力がそのまま投票先として扱われます。
> 不要な前置きや説明文が混じらないよう、「名前のみを出力してください」と **明示** するのが安全です。

---

## 5. プロンプトを編集するときの手順

基本的なやり方はシンプルで、次の3ステップです。

1. `config/config.yml` を開く
2. `prompt.<キー>` の `|-` 以下の本文を書き換える
3. エージェントを再起動する（実行中のプロセスは設定を再読み込みしません）

コードには一切触らなくて構いません。まずは `talk` や `vote` など、影響の見えやすいキーから調整するのがおすすめです。

### 編集するときの小さなチェックリスト

* ✅ YAML のインデントを崩していないか（`|-` のブロック内は元のインデントを保つ）
* ✅ `None` になりうる属性を `{% if ... is not none %}` で守っているか
* ✅ 最後に LLM への指示（「名前のみ」「〇〇文字以内」など）を入れているか
* ✅ 別のキーにコピペしたとき、そこで使える変数だけを使っているか（例：`talk_history` は `divine` でも参照可能だが、`remain_count` は `TALK` / `WHISPER` 以外では `None`）

---

## 6. 新しい変数を追加したい／参照情報を増やしたいとき

「プロンプトに渡したい情報が、`info` や `talk_history` には入っていない」という場面が出てきたら、**コード側の改造** が必要です。
変更すべき場所は、基本的に次の2か所です。

> 「内部状態をどう増やすか」「どこに保存するか」の踏み込んだ説明は [エージェントの内部状態とデータの流れ §5](./agent_state.md#5-自分で内部状態を増やしたいとき) と [§6](./agent_state.md#6-増やした状態をプロンプトから参照できるようにする) にまとめてあります。本節では「プロンプト編集の延長として最低限おさえる手順」を示します。

### 6.1 テンプレートに渡す変数を増やす

`src/agent/agent.py` の `_send_message_to_llm` 内にある `key` 辞書にキーを追加します。

```python
# src/agent/agent.py  （追加箇所のイメージ）
key = {
    "info": self.info,
    "setting": self.setting,
    "talk_history": self.talk_history,
    "whisper_history": self.whisper_history,
    "role": self.role,
    "sent_talk_count": self.sent_talk_count,
    "sent_whisper_count": self.sent_whisper_count,
    "alive_agents": self.get_alive_agents(),   # ← 追加
    "my_vote_history": self.my_vote_history,   # ← 追加（要：属性を別途定義）
}
```

こうするとテンプレート側で次のように書けるようになります。

```yaml
prompt:
  vote: |-
    生存者: {{ alive_agents | join(", ") }}
    これまでの自分の投票: {{ my_vote_history }}
```

### 6.2 蓄積が必要なデータは `set_packet` などで貯める

たとえば「自分の投票履歴をプロンプトに見せたい」という場合、`info.vote_list` には **今日の** 結果しか入りません。
過去分も使いたいなら、`agent.py` 側で属性を作って蓄積しておきます。

```python
# src/agent/agent.py  （__init__ と set_packet に追加）
def __init__(self, ...):
    ...
    self.my_vote_history: list[dict] = []

def set_packet(self, packet):
    super_result = super().set_packet(packet) if hasattr(super(), "set_packet") else None
    if self.info and self.info.vote_list:
        for v in self.info.vote_list:
            if v.agent == self.info.agent:
                self.my_vote_history.append({"day": self.info.day, "target": v.target})
    return super_result
```

### 6.3 フィルタや関数を追加したくなったら

Jinja2 には独自のフィルタ（`|` で繋ぐ関数）を追加することもできますが、**初学者のうちは不要** です。
同等のことは、Python 側で事前に整形した値を `key` に渡すだけで達成できます（例：`alive_agents_str = ", ".join(self.get_alive_agents())` のように加工して渡す）。

> リクエスト名とは別のキー（例：`prompt.my_strategy`）を追加して、自分で書いたタイミングで呼び出したい場合は、**コード側にもメソッドを追加する必要** があります。これはプロンプト編集というより「エージェント本体の改造」になるので、[エージェントのカスタマイズ方法 ＞ 独自キーのプロンプトを追加する](./customize_agent.md#独自キーのプロンプトを追加する) で扱います。

---

## 7. よくあるつまずき

### 7.1 出力に前置きや装飾が混じる

LLM の返答はそのままサーバへ送られます。`vote` などで `「投票先はミナトです」` と返ってしまうと、そのままでは無効な投票になります。
プロンプトの最後に「**名前のみを出力してください。説明は不要です。**」と明示しましょう。

### 7.2 `info.xxx` が `None` で落ちる

`info.medium_result` など、**役職や進行状況によって `None` になる属性** を裸で参照すると、`None.target` のような形でテンプレート描画が落ちます。
必ず次のように囲みます。

```jinja
{% if info.medium_result is not none -%}
霊媒結果: {{ info.medium_result.target }} は {{ info.medium_result.result }}
{%- endif %}
```

### 7.3 履歴が全部渡って遅い／トークン超過

`{% for w in talk_history %}` と書くと、**ゲーム全体** の履歴が毎回渡ります。
差分だけでよい場面では、`talk_history[sent_talk_count:]` のようにスライスするのが基本です。

### 7.4 空行や余計なインデントが入る

Jinja2 の `{%- ... -%}` のハイフンは、**前後の空白や改行を消す** 役割があります。
出力のレイアウトが気になるときは、[Jinja2テンプレートとは](../background/about_jinja2.md) のハイフン制御の節を参照してください。

### 7.5 YAML としてパースできない

`|-` の下で、**行頭のインデントを揃える** のを忘れると YAML エラーになります。既存のサンプルに合わせて半角スペースを維持してください。

### 7.6 「どの変数が使えるのか思い出せない」

思い出せないときは、このページの [§3 プロンプトから参照できる変数](#3-プロンプトから参照できる変数) か、`agent.py` の `_send_message_to_llm` にある `key` 辞書を直接見てください。**渡されているものが答え** です。
属性レベルの中身（`info.day` など）が思い出せないときは [エージェントの内部状態とデータの流れ §4](./agent_state.md#4-各属性の中身リファレンス) を辞書代わりに使ってください。

---

## まとめ

* プロンプトは Jinja2 テンプレート。変数は `agent.py` の `_send_message_to_llm` から渡されている
* まず触るべきは `config.yml` の `prompt.*`。コード変更なしで挙動を大きく変えられる
* `None` になりうる属性は `{% if ... is not none %}` で守る
* 新しい情報を渡したくなったら、`_send_message_to_llm` の `key` 辞書に追加すればよい
* 文法そのものに不安があれば [Jinja2テンプレートとは](../background/about_jinja2.md) を参照

---

[参加者マニュアルトップへ](../_index.md)\
[改良・拡張トップへ](./_index.md)\
[前へ（エージェントの内部状態とデータの流れ）](./agent_state.md)\
[次へ（エージェントのカスタマイズ方法）](./customize_agent.md)
