---
date: '2026-04-26T14:00:00+09:00'
draft: false
title: 'エージェントのカスタマイズ方法'
category: participants_guide
---

このページでは、サンプルエージェントを **実際に改造する** ための方針を説明します。
「どのファイルの、どのメソッドを変えれば、どんな挙動が変わるのか」を把握しておくと、改良作業がスムーズになります。

---

## 改造する場所の考え方

改造する場所は、大きく3つに分けられます。

1. **プロンプト**（`config.yml` の `prompt.*`）\
   もっとも手軽で効果も大きい。LLMへの指示文を書き換えるだけ。
2. **基底クラス**（`src/agent/agent.py`）\
   すべての役職に共通する動作を変えたいときに編集する。
3. **役職クラス**（`src/agent/villager.py` など）\
   特定の役職だけ動作を変えたいときに編集する。

まずはプロンプトを触ってみて、それでも足りない部分をコードで補うのが基本です。

---

## 段階的に強くしていく道のり

いきなり全部いじらなくて大丈夫です。下記のような段階で少しずつ強化していくと、原因と効果が見えやすく、手戻りが少なくなります。

| ステップ | 改造する場所 | 難しさ |
|---|---|---|
| ① プロンプトを書き換える | `config.yml` の `prompt.*` | 低 |
| ② LLMの設定を変える | `config.yml` の `llm.*` / モデル名・温度 | 低 |
| ③ 役職クラスに独自ロジックを入れる | `src/agent/*.py` | 中 |
| ④ 基底クラスを拡張する | `src/agent/agent.py` / `src/utils/` 新ファイル | 中〜高 |
| ⑤ 会話・投票パターンの分析など新機能を追加する | 新規ユーティリティ | 高 |

最初は **①だけで十分に強くなります**。実際、過去の大会でもプロンプト改善だけで上位に入った例があります。

---

## 返り値のルール

エージェントのメソッドが返す値には、種類ごとにルールがあります。

| メソッドの種類 | 何を返すか | 例 |
|---|---|---|
| 会話系（`talk` / `whisper`） | 発言の本文（テキスト） | `"こんにちは、村人です"` |
| 行動系（`vote` / `divine` / `guard` / `attack`） | 対象の **プレイヤー名** | `"ミナト"` |
| 初期化系（`initialize` / `daily_initialize` / `daily_finish` / `finish`） | 返さない（内部処理のみ） | — |

**注意点**：

* 行動系の返り値は、サーバから届いた生存者の名前と **完全一致** させる必要があります。`self.get_alive_agents()` を使うと生存者のリストが取れるので便利です。
* 会話系で `"Over"` を返すと、自分のターンを早めに終了できます。
* アクションには制限時間があります。LLMを呼ぶときは、長考しすぎないように注意しましょう。

---

## 役職ごとのカスタマイズポイント

以下では、それぞれの役職クラスで上書きできるメソッドを示します。
**変更推奨度** は「改造する価値がどれくらい高いか」の目安です。

### 基底クラス（`src/agent/agent.py`）

すべての役職に共通する動作はここで定義されています。特定の役職でなく、**エージェント全体の挙動** を変えたいときに編集します。

| メソッド | 変更推奨度 | 役割 |
|---|---|---|
| `name` | 低 | 接続時の名前を返す（通常は変更不要） |
| `initialize` | 中 | ゲーム開始時の準備処理 |
| `daily_initialize` | 中 | 昼の始まりの処理 |
| `talk` | **高** | 昼の発言を生成 |
| `whisper` | **高** | 人狼同士の囁きを生成 |
| `daily_finish` | 中 | 昼の終わりの処理 |
| `vote` | **高** | 追放投票の対象を決める |
| `divine` | **高** | 占い対象を決める（占い師のみ呼ばれる） |
| `guard` | **高** | 護衛対象を決める（騎士のみ呼ばれる） |
| `attack` | **高** | 襲撃対象を決める（人狼のみ呼ばれる） |
| `finish` | 低 | ゲーム終了時の後処理 |

### 人狼（`src/agent/werewolf.py`）

人狼固有のメソッドとして、`whisper`（囁き）と `attack`（襲撃投票）が重要です。
人狼同士での連携や、襲撃先の選び方を工夫しましょう。

### 占い師（`src/agent/seer.py`）

占い対象の選び方を `divine` メソッドで定義します。
占い結果は、占いフェーズの翌朝に届く `info.divine_result` から取得できます。

### 騎士（`src/agent/bodyguard.py`）

護衛対象の選び方を `guard` メソッドで定義します。自分自身は護衛対象に指定できません。

### 霊媒師（`src/agent/medium.py`）

霊媒結果は、追放フェーズの翌朝に届く `info.medium_result` から取得できます。
基本的には `talk` や `vote` でこの情報をどう活用するかが腕の見せどころです。

### 村人（`src/agent/villager.py`）・狂人（`src/agent/possessed.py`）

これらは特別なアクションを持ちません。
基本的には `talk` や `vote` のプロンプトを中心に改良していきます。

---

## 小さなカスタマイズの例

### 例1：投票先を「いちばん怪しいと言った人」に固定する

`vote()` メソッドをオーバーライドして、独自のロジックを組み込みます。

```python
def vote(self) -> str:
    # まずはLLMに聞いてみる
    response = super().vote()
    # 生存者の中から、LLMの応答に一番近い名前を選ぶなどの処理を追加…
    return response
```

### 例2：発言内容に定型の締め言葉を付ける

```python
def talk(self) -> str:
    text = super().talk()
    if text and text != "Over":
        text = f"{text}（ケンジより）"
    return text
```

---

## 共通処理を追加したいときは

複数の役職で使うヘルパー関数は、`src/utils/` に新しいファイルを作って置くのがおすすめです。
たとえば「会話履歴から怪しい人物を抽出する」といった関数をそこに書き、`agent.py` や各役職クラスから呼び出します。

---

## 独自キーのプロンプトを追加する

`config.yml` の `prompt.*` は、サーバから届くリクエスト種別（`talk` / `vote` / `divine` …）と **1 対 1 で固定的に結び付いて** います（詳しくは [プロンプトエンジニアリング §2.1](./prompt_engineering.md#21-configpromptキー-の名前はどうやって決まっているか) を参照）。
そのため、「昼の発言を作る前にもう一度 LLM に戦略を整理させたい」「自分用のふりかえりプロンプトを差し込みたい」のように、**リクエスト名と無関係なプロンプト** を使いたいときは、`config.yml` に独自キーを書くだけでは動かず、`agent.py` にも手を入れる必要があります。

手順はシンプルに2ステップです。

### 手順1：`config.yml` に独自キーを追加する

`prompt` セクションに、好きな名前でキーを作ります。使える変数（`info` / `talk_history` など）は既存のプロンプトと同じです。

```yaml
prompt:
  talk: |-
    ...
  my_strategy: |-                         # ← 独自キー
    あなたは{{ info.agent }}です。{{ info.day }}日目の議論中です。
    これまでの会話:
    {% for w in talk_history[sent_talk_count:] -%}
    {{ w.agent }}: {{ w.text }}
    {% endfor %}
    誰を疑うべきか、3行以内で整理してください。
```

### 手順2：`agent.py` にヘルパーを追加する

まず、テンプレートを描画するヘルパー `_render_prompt` を基底クラスに追加します。**既存の `_send_message_to_llm` には手を加えず、新しいメソッドを1つ足すだけ** にしておくと、既存のリクエスト処理を壊さずに済みます。

```python
# src/agent/agent.py
# 既存の import に以下が入っていることを確認（無ければ追加）
from jinja2 import Template
from langchain_core.messages import HumanMessage


class Agent:
    # ... 既存の __init__ / set_packet / _send_message_to_llm などはそのまま ...

    # ▼▼▼ ここから新規メソッドを追加（クラス内ならどこでもOK）
    def _render_prompt(self, key_name: str) -> str:
        """任意のキー名のプロンプトを描画して返す."""
        prompt = self.config["prompt"][key_name]
        key = {
            "info": self.info,
            "setting": self.setting,
            "talk_history": self.talk_history,
            "whisper_history": self.whisper_history,
            "role": self.role,
            "sent_talk_count": self.sent_talk_count,
            "sent_whisper_count": self.sent_whisper_count,
        }
        return Template(prompt).render(**key).strip()
    # ▲▲▲ 新規メソッドここまで
```

### 手順3：使いたいメソッドから呼び出す

次に、独自プロンプトを挟みたいメソッドで `self._render_prompt("my_strategy")` を呼びます。
ここでは「昼の発言前に戦略整理を挟む」例として、**既存の `talk()` をオーバーライド** するパターンを示します（基底クラス側を直接編集するより、役職クラスで拡張する方が影響範囲を絞れます）。

```python
# src/agent/villager.py  （他の役職クラスでも同じ要領）
class Villager(Agent):
    # ... 既存の __init__ などはそのまま ...

    # ▼▼▼ talk() をオーバーライドして独自プロンプトを差し込む
    def talk(self) -> str:
        # --- 追加：発言を作る前に戦略整理プロンプトをLLM履歴に積む ---
        strategy = self._render_prompt("my_strategy")
        self.llm_message_history.append(HumanMessage(content=strategy))
        # --- 追加ここまで ---

        # 既存の talk 処理（基底クラスの _send_message_to_llm 経由）に委譲
        return super().talk()
    # ▲▲▲ オーバーライドここまで
```

ポイントは、**新規追加**（`_render_prompt`）と **既存メソッドの拡張**（`talk` のオーバーライド）を分けて書くことです。こうしておくと、動かなくなったときに「どの変更が原因か」を切り分けやすくなります。

### 補足：注意点

* 独自キーのプロンプトは **サーバからのリクエストに自動では紐付きません**。「いつ・どのメソッドで呼ぶか」は自分で設計する必要があります。
* 既存の `_send_message_to_llm` を書き換えて「`Request` の代わりに文字列キーを受け取れる」ようにする手もありますが、まずは **別メソッドを足す** 方が既存処理を壊さずに安全です。
* 追加したキーで参照できる変数を増やしたい場合は、[エージェントの内部状態とデータの流れ §6](./agent_state.md#6-増やした状態をプロンプトから参照できるようにする) と同じ要領で `key` 辞書にエントリを足してください。

---

## プロンプト改善の具体例

コードを触らずに `config.yml` の `prompt.*` を書き換えるだけでも、エージェントの振る舞いは大きく変わります。
ここではよく効く改善例を3つ紹介します。

### 例A：役職ごとの戦略方針を明示する

`talk` プロンプトの中で役職ごとに条件分岐を入れると、役職に応じた方針でLLMが発言してくれます。

```yaml
prompt:
  talk: |-
    あなたは{{ info.agent }}（役職: {{ role.value }}）です。{{ info.day }}日目です。

    {% if role.value == 'SEER' %}
    あなたは占い師です。占った結果を適切なタイミングで共有してください。
    ただし、いきなり初日に名乗り出る必要はありません。
    {% elif role.value == 'WEREWOLF' %}
    あなたは人狼です。村人のふりをしつつ、仲間と連携してください。
    占い師を騙ることも選択肢に入れてください。
    {% elif role.value == 'POSSESSED' %}
    あなたは狂人です。人狼陣営が勝つように、村側を混乱させてください。
    偽の占い師を演じると効果的なことがあります。
    {% endif %}

    最新の会話:
    {% for talk in talk_history[sent_talk_count:] -%}
    {{ talk.agent }}: {{ talk.text }}
    {% endfor %}

    自然な日本語で1発言してください。発言のみを出力してください。
```

### 例B：投票の判断材料を明示する

`vote` プロンプトで、**今日の会話** と **前日までの投票結果** を一緒にLLMへ渡すと、根拠のある投票が返ってきやすくなります。

```yaml
prompt:
  vote: |-
    {{ info.day }}日目の投票です。以下の情報をもとに投票先を決めてください。

    【本日の議論】
    {% for talk in talk_history -%}
    {% if talk.day == info.day -%}
    {{ talk.agent }}: {{ talk.text }}
    {% endif -%}
    {% endfor %}

    {% if info.vote_list -%}
    【前回の投票結果】
    {% for vote in info.vote_list -%}
    {{ vote.agent }} → {{ vote.target }}
    {% endfor %}
    {% endif %}

    【生存中のエージェント】
    {% for agent, status in info.status_map.items() -%}
    {% if status == 'ALIVE' and agent != info.agent -%}
    - {{ agent }}
    {% endif -%}
    {% endfor %}

    最も人狼の可能性が高いエージェントの名前だけを出力してください。
```

### 例C：昼の開始時に前夜の出来事を整理する

`daily_initialize` に「前日に何が起きたか」をまとめておくと、LLMが状況を把握しやすくなります。

```yaml
prompt:
  daily_initialize: |-
    {{ info.day }}日目が始まりました。

    {% if info.executed_agent -%}
    【追放】{{ info.executed_agent }}が追放されました。
    {% endif %}
    {% if info.attacked_agent -%}
    【襲撃】{{ info.attacked_agent }}が襲撃されました。
    {% endif %}
    {% if info.divine_result -%}
    【占い結果】{{ info.divine_result.target }} は {{ info.divine_result.result }} でした。
    {% endif %}
    {% if info.medium_result -%}
    【霊媒結果】{{ info.medium_result.target }} の正体は {{ info.medium_result.result }} でした。
    {% endif %}

    これらの情報を踏まえて、今日の議論に臨んでください。
```

---

## 改造に慣れてきたら

### アイデア1：占い師の「未占い者優先」ロジック

占い済みの対象を記憶しておき、未占いの人物から優先的に選ぶようにします。

```python
# src/agent/seer.py
class Seer(Agent):
    def __init__(self, config, name, game_id, role):
        super().__init__(config, name, game_id, Role.SEER)
        self.divined = set()

    def daily_initialize(self):
        super().daily_initialize()
        if self.info and self.info.divine_result:
            self.divined.add(self.info.divine_result.target)

    def divine(self) -> str:
        alive = self.get_alive_agents()
        candidates = [a for a in alive if a != self.info.agent and a not in self.divined]
        if candidates:
            response = super().divine()
            if response in candidates:
                return response
            return candidates[0]
        return super().divine()
```

### アイデア2：投票履歴をプロンプトに埋め込む

`agent.py` 側で投票履歴を蓄積しておき、プロンプトで参照できるようにします。`_send_message_to_llm` のテンプレート変数を増やすイメージです。これにより、「誰が誰に投票したか」の時系列をLLMに見せられるようになります。

> 具体的な手順（`__init__` で属性を作る → `set_packet` で更新 → `key` 辞書に登録）は [エージェントの内部状態とデータの流れ §5〜§6](./agent_state.md#5-自分で内部状態を増やしたいとき) にコード例つきで示しています。

---

## 最初の一歩として

いきなりコードを書き換えるより、まずは **プロンプトを変えるだけ** で十分な改善が得られることも多いです。
`config.yml` の `prompt.initialize` に方針を書き加えたり、`prompt.talk` に「人狼の可能性が高い人を優先的に疑う」などの指示を追加したりするところから始めてみてください。

---

[参加者マニュアルトップへ](../_index.md)\
[改良・拡張トップへ](./_index.md)\
[前へ（プロンプトエンジニアリング）](./prompt_engineering.md)\
[次へ（LLMとのやり取りパターン）](./llm_interaction_patterns.md)
