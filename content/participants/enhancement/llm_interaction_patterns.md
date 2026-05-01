---
date: '2026-04-20T14:00:00+09:00'
draft: false
title: 'LLMとのやり取りパターン'
category: participants_guide
ShowToc: true
---

こちらのページでは、サンプルエージェントが採用している **LLM とのやり取り方法** を整理し、それ以外にも検討に値する **設計パターン** を紹介します。

「マルチターンとシングルターンの違いって？」「リクエスト種別ごとに別の LLM 設定を使い分けたい」「履歴が肥大化してきた」といった、**LLM 呼び出しまわりを設計し直したくなったとき** の出発点として使ってください。

> LangChain そのものの基本（`HumanMessage` / `invoke` / `|` の意味）は [背景知識 ＞ LangChainとは](../background/about_langchain.md) を参照してください。
> 本ページでは、それらを使いこなして「どんな設計を選べるか」に踏み込みます。

---

## このページで扱うこと

1. 現状の実装：累積マルチターン
2. 主要な代替パターン（シングルターン／要約マルチターン／リクエスト別チェーン）
3. パターンを選ぶときの観点
4. 実装のとっかかり（コードスニペット）

---

## 1. 現状：累積マルチターン

サンプルエージェントは、**すべての過去メッセージを毎回まとめて LLM に渡す** 累積マルチターン方式です。

```python
# src/agent/agent.py（抜粋）
self.llm_message_history.append(HumanMessage(content=prompt))
response = (self.llm_model | StrOutputParser()).invoke(self.llm_message_history)
self.llm_message_history.append(AIMessage(content=response))
```

| 性質 | 内容 |
|---|---|
| **履歴の扱い** | `llm_message_history` に毎回追加。ゲーム終了（`INITIALIZE` 受信）まで保持 |
| **LLM への入力** | 過去のすべての `HumanMessage` / `AIMessage` を毎回送信 |
| **強み** | 「自分が前にどう発言したか」「前回の投票理由」を踏まえやすい |
| **弱み** | トークン消費・コスト・レイテンシが日数とともに増える／古い発言に引きずられることがある |

> このパターンが **常に最適とは限りません**。試合が長引くほど、増え続ける履歴がトークンも応答時間も食いつぶすので、後述のパターンに切り替える価値が出てきます。

---

## 2. 代替パターン

### 2.1 シングルターン（履歴を持たない）

毎回 **その回のプロンプトだけ** を LLM に渡し、過去のやり取りは保持しないパターンです。

```python
def _send_message_to_llm(self, request: Request | None) -> str | None:
    ...
    rendered = Template(prompt).render(**key).strip()
    # ▼ 履歴を積まずに、その回だけのメッセージで invoke
    response = (self.llm_model | StrOutputParser()).invoke(
        [HumanMessage(content=rendered)],
    )
    return response
```

| 性質 | 内容 |
|---|---|
| **履歴の扱い** | 持たない。毎回ゼロから |
| **強み** | トークン消費が一定／再現性が高い／古い発言に引きずられない／デバッグしやすい |
| **弱み** | 「前にこう言った」が伝わらない。**プロンプト側で必要な情報を全部渡す必要** がある |

このパターンに切り替えると、`talk_history` をプロンプトに明示的に埋め込まないと文脈が失われます。逆に言うと、「**何を見せて何を見せないか**」を完全にコントロールできます。

> **ポイント**：人狼のように「嘘の一貫性」が大切なゲームでも、シングルターンで戦える設計はあり得ます。
> その場合は **「自分の主張をプロンプトに毎回埋め込む」** ように内部状態（[エージェントの内部状態とデータの流れ §5](./agent_state.md#5-自分で内部状態を増やしたいとき)）で蓄積します。

### 2.2 要約マルチターン（古い履歴を要約に置き換える）

履歴の **古い部分を要約に圧縮** し、新しい部分だけ生で残すパターンです。マルチターンのコンテキスト性を保ちつつ、トークン肥大を抑えられます。

実装イメージ：

```python
def _maybe_compress_history(self) -> None:
    """履歴が長くなったら古い部分を要約に置き換える."""
    THRESHOLD = 20  # メッセージ数の目安
    if len(self.llm_message_history) <= THRESHOLD:
        return

    old_part = self.llm_message_history[:-10]   # 直近10件以外を要約対象に
    summary_prompt = [
        HumanMessage(content="次の会話を3行以内で要約してください:\n"
                     + "\n".join(m.content for m in old_part)),
    ]
    summary = (self.llm_model | StrOutputParser()).invoke(summary_prompt)
    # 要約済みの部分を1つの SystemMessage / AIMessage に置き換える
    from langchain_core.messages import SystemMessage
    self.llm_message_history = [
        SystemMessage(content=f"[これまでの要約] {summary}"),
        *self.llm_message_history[-10:],
    ]
```

| 性質 | 内容 |
|---|---|
| **履歴の扱い** | 古い部分を要約に置換。直近 N 件は生で保持 |
| **強み** | 文脈を保ちつつトークン量を抑えられる |
| **弱み** | 要約呼び出しのコスト／要約品質に依存／要約タイミングの設計が必要 |

### 2.3 リクエスト種別ごとに分離する

サンプルでは「talk も vote も同じ `llm_message_history` に積む」一本化された設計ですが、**リクエスト種別ごとに履歴を分ける** こともできます。

```python
# __init__
self.histories: dict[str, list[BaseMessage]] = {
    "talk": [],
    "vote": [],
    "divine": [],
    ...
}

# _send_message_to_llm 内
key = request.lower()
self.histories[key].append(HumanMessage(content=rendered))
response = (self.llm_model | StrOutputParser()).invoke(self.histories[key])
self.histories[key].append(AIMessage(content=response))
```

これによって、**「議論用の自分」と「投票判断用の自分」を分離** できます。
発言と投票の不一致は過去大会で繰り返し指摘されてきた課題（[改良のヒントと課題点 §1](./improvement_tips.md#1-発話と行動の食い違い)）なので、片方だけを分けて様子を見るのも有効です。

### 2.4 リクエスト別に system プロンプトを切り替える

履歴を分けるほどではないが、**LLM にかける役割設定** だけリクエストごとに変えたい、というパターンもあります。

```python
from langchain_core.messages import SystemMessage

SYSTEM_PROMPTS = {
    "talk":   "あなたは慎重に発言する人狼ゲームのプレイヤーです。",
    "vote":   "あなたは過去の発言から論理的に犯人を推定する分析官です。",
    "divine": "あなたは占い結果を最大限活用する占い師です。",
}

def _send_message_to_llm(self, request):
    ...
    key = request.lower()
    messages = [
        SystemMessage(content=SYSTEM_PROMPTS.get(key, "")),
        HumanMessage(content=rendered),
    ]
    return (self.llm_model | StrOutputParser()).invoke(messages)
```

履歴を持たないシングルターンの上に、リクエスト別の人格だけ被せるイメージです。

### 2.5 モデル自体をリクエスト別に変える

「投票判断は安価で高速なモデル、議論は精度重視のモデル」のように、**LLM そのものをリクエスト種別で使い分ける** こともできます。

```python
# initialize の中で複数モデルを保持
self.llm_models = {
    "fast":  ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3, ...),
    "smart": ChatGoogleGenerativeAI(model="gemini-2.5-pro",   temperature=0.7, ...),
}

# _send_message_to_llm の中で振り分け
fast_requests = {"vote", "divine", "guard", "attack"}
model = self.llm_models["fast"] if request.lower() in fast_requests else self.llm_models["smart"]
response = (model | StrOutputParser()).invoke(messages)
```

コスト最適化と応答速度の両面で効きます。ただし **`config.yml` 側の構造も拡張** する必要があるので、設定ファイルとセットで設計しましょう。

---

## 3. パターンを選ぶときの観点

ひとつの正解はありません。次の5つの観点でトレードオフを見ながら選んでください。

| 観点 | 累積マルチターン | シングルターン | 要約マルチターン | リクエスト別分離 |
|---|---|---|---|---|
| **トークン消費** | 多い（日数で増加） | 少ない（一定） | 中程度 | 種別ごとに最適化可 |
| **応答速度** | 遅くなりがち | 速い | 中 | 軽い種別を高速化可 |
| **文脈の保持** | 強い | 弱い（プロンプト依存） | 中 | 種別内では強い |
| **嘘・主張の一貫性** | 自然に保てる | 自前で蓄積が必要 | 要約品質次第 | 種別ごとに分離可能 |
| **デバッグしやすさ** | 履歴の影響が読みにくい | 入力が単純で読みやすい | 中 | 種別単位で追える |

> **ポイント**：「全部入りで強くしよう」とすると失敗しがちです。
> まずは **シングルターン化など影響が見えやすい変更を一つ** 試して、勝率や挙動の変化を確認するのがおすすめです。

---

## 4. 実装のとっかかり

どのパターンも、修正対象は基本的に `_send_message_to_llm` の **1〜数行** です。
本格的に書き換える前に、次の流れで小さく検証するとリスクを抑えられます。

1. 役職クラスのうち1つだけ（たとえば `villager.py`）で `_send_message_to_llm` をオーバーライド
2. ログを `level: debug` にして [config.ymlの説明 ＞ log](./config_explanation.md#log) のとおり LLM への入出力を確認
3. ローカル対戦（[応用編 ＞ ローカル対戦のセットアップ](../extras/local_battle_setup.md)）で挙動を比較
4. 良ければ基底クラスへ反映、悪ければ戻す

```python
# src/agent/villager.py の例：自分だけシングルターン化
class Villager(Agent):
    def _send_message_to_llm(self, request):
        if request is None or request.lower() not in self.config["prompt"]:
            return None
        prompt = self.config["prompt"][request.lower()]
        rendered = Template(prompt).render(
            info=self.info, setting=self.setting,
            talk_history=self.talk_history,
            whisper_history=self.whisper_history,
            role=self.role,
            sent_talk_count=self.sent_talk_count,
            sent_whisper_count=self.sent_whisper_count,
        ).strip()
        return (self.llm_model | StrOutputParser()).invoke(
            [HumanMessage(content=rendered)],
        )
```

> **注意**：`_send_message_to_llm` を完全に置き換える場合、**ログ出力やエラーハンドリング** を抜き落とさないようにしてください。
> 元のコード（[ソースコードの構成 ＞ agent.py](./nlp_agent_structure.md)）と差分で比べると安全です。

---

## まとめ

* サンプルは累積マルチターン。文脈を保ちやすいが、トークン肥大とノイズの影響を受けやすい
* シングルターンは制御性とコスト面で優れる。代わりに **必要な情報をすべてプロンプトに埋め込む設計** が必要
* 要約マルチターン・リクエスト別分離・モデル使い分けなど、中間的な選択肢も豊富
* まずは小さく試して、ログと勝率の両面で評価する

---

[参加者マニュアルトップへ](../_index.md)\
[改良・拡張トップへ](./_index.md)\
[前へ（エージェントのカスタマイズ方法）](./customize_agent.md)\
[次へ（大会の進め方）](../competition/competition.md)
