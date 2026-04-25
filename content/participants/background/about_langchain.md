---
date: '2026-04-26T14:00:00+09:00'
draft: false
title: 'LangChainとは'
category: participants_guide
ShowToc: true
---

このページでは、サンプルエージェントが LLM とのやり取りに使っている **LangChain** の最低限の語彙と仕組みを説明します。
「`llm_model.invoke(...)` とか `HumanMessage(...)` って何？」というところから押さえていきたい方向けのページです。

> LangChain を使った **設計の選択肢**（マルチターンとシングルターンの違いなど）は [改良・拡張 ＞ LLMとのやり取りパターン](../enhancement/llm_interaction_patterns.md) で扱います。
> このページは「LangChain そのものが何をするライブラリか」に絞って解説します。

---

## LangChain って何？

**LangChain** は、LLM（大規模言語モデル）を使ったアプリケーションを書くための Python ライブラリです。
ざっくりと言うと、次の3つを **共通のインターフェース** で扱えるようにしてくれます。

| 機能 | LangChain の何が嬉しいか |
|---|---|
| **モデルを差し替えやすくする** | OpenAI / Google / Ollama などを、ほぼ同じコードで切り替えられる |
| **会話履歴を管理する** | 「役割つきメッセージ」のリストとして、過去のやり取りを保てる |
| **処理を組み合わせる** | 「LLM → 整形 → 別の LLM」のような流れを `|` で繋げて書ける |

サンプルエージェントが LangChain を採用しているのは、主に **1つ目と2つ目** の理由です。

---

## サンプルでのインポート

`src/agent/agent.py` の冒頭を見ると、LangChain 関連で以下のものが使われています。

```python
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
```

| インポート | 役割 |
|---|---|
| `ChatOpenAI` / `ChatGoogleGenerativeAI` / `ChatOllama` | 各社のチャット系 LLM を呼び出すクラス。**共通の `invoke` インターフェース** を持つ |
| `HumanMessage` | 「ユーザーの発言」を表すメッセージ |
| `AIMessage` | 「LLM の返答」を表すメッセージ |
| `StrOutputParser` | LLM の返答を、メッセージ型から **ただの文字列** に変換するパーサ |

---

## ChatModel：モデルの共通インターフェース

LangChain では、チャット系の LLM は **`BaseChatModel` を継承した同じ形のオブジェクト** として扱われます。
そのおかげで、サンプルでは `llm.type` の値で実装を切り替えるだけで、後段のコードはまったく同じものが使えます。

```python
# src/agent/agent.py（抜粋）
match model_type:
    case "openai":
        self.llm_model = ChatOpenAI(model=..., temperature=..., api_key=...)
    case "google":
        self.llm_model = ChatGoogleGenerativeAI(model=..., temperature=..., api_key=...)
    case "ollama":
        self.llm_model = ChatOllama(model=..., temperature=..., base_url=...)
```

どの分岐に入っても、`self.llm_model.invoke(messages)` で呼び出せる、という構造です。

> **ポイント**：「OpenAI でも Google でも同じコードで動く」のは LangChain の抽象化のおかげです。
> 自前で `import openai` / `import google.generativeai` を書き分けると、ここがしんどくなります。

---

## メッセージの型：HumanMessage と AIMessage

ChatGPT 系の API では、会話は **ロール（役割）付きのメッセージのリスト** として表現されます。

| クラス | OpenAI 用語での役割 | 中身 |
|---|---|---|
| `SystemMessage` | system | LLM に与える役割設定や前提（サンプルでは未使用） |
| `HumanMessage` | user | ユーザーからの入力 |
| `AIMessage` | assistant | LLM の返答 |

サンプルエージェントでは、毎リクエスト時に **生成したプロンプトを `HumanMessage`** として履歴に積み、**LLM の返答を `AIMessage`** として履歴に積んでいます。

```python
# src/agent/agent.py（抜粋）
self.llm_message_history.append(HumanMessage(content=prompt))
response = (self.llm_model | StrOutputParser()).invoke(self.llm_message_history)
self.llm_message_history.append(AIMessage(content=response))
```

つまり `llm_message_history` は **「LLM との会話のログそのもの」** です。
これを丸ごと `invoke` に渡しているので、LLM 側からは「これまでの全やり取りを覚えた状態で次の発言を求められている」ように見えます。

---

## チェーンと `|` 演算子

LangChain には **LCEL (LangChain Expression Language)** という独自記法があり、`|`（パイプ）で処理を繋げます。

```python
chain = self.llm_model | StrOutputParser()
response: str = chain.invoke(self.llm_message_history)
```

ここで何が起きているかを分解すると、

1. `self.llm_model.invoke(messages)` が走り、`AIMessage` が返ってくる
2. その `AIMessage` が `StrOutputParser` に渡される
3. `StrOutputParser` が `AIMessage.content`（つまり文字列）を取り出す
4. 最終的に **ただの `str`** が `response` に入る

という流れです。
`StrOutputParser` を挟まないと、`response` は `AIMessage` オブジェクトになり、`response.content` のように属性アクセスが必要になります。サンプルではそのひと手間を省くために挟んでいる、というだけのことです。

> **ポイント**：チェーンは「左から右へ流れる」と読むのが基本です。
> 入力が左端に入って、各段で加工され、右端で結果が出てくる。Unix のパイプと同じ感覚です。

---

## 履歴を保持する仕組み（マルチターン）

サンプルの `_send_message_to_llm` を流れで追うと、次のことが起きています。

```text
リクエスト1（talk）
  ├ HumanMessage("[talk用プロンプト1]") を履歴に追加
  ├ 履歴 = [Human1] を LLM に送信
  └ AIMessage("...") を履歴に追加
リクエスト2（vote）
  ├ HumanMessage("[vote用プロンプト2]") を履歴に追加
  ├ 履歴 = [Human1, AI1, Human2] を LLM に送信
  └ AIMessage("...") を履歴に追加
リクエスト3（talk）
  ├ HumanMessage("[talk用プロンプト3]") を履歴に追加
  ├ 履歴 = [Human1, AI1, Human2, AI2, Human3] を LLM に送信
  ...
```

このように、毎回 **すべての過去メッセージを送り直している** のが現状の実装です。
LLM 側にはコンテキストが保たれるので、「自分が前にどう発言したか」「前回の投票理由は何だったか」を踏まえた応答が返ってきやすくなります。

### `llm_message_history` と `talk_history` は別物です

`agent.py` には **「履歴」と名のつくリストが2つ** あり、初見では混乱しやすいので明確に区別してください。

| 名前 | 中身 | 何を記録している？ | LLM への渡り方 |
|---|---|---|---|
| `talk_history` | `Talk` オブジェクトのリスト（aiwolf-nlp-common） | **ゲーム内の他プレイヤーの発言**。サーバから届いたものを蓄積 | プロンプトテンプレートの中で `{% for w in talk_history %}` のように **明示的に埋め込む** ことで LLM に渡る |
| `llm_message_history` | `BaseMessage` のリスト（LangChain） | **エージェントがLLMに送ったプロンプト** と **LLMが返した応答** のやり取りそのもの | `(self.llm_model \| StrOutputParser()).invoke(self.llm_message_history)` で **そのまま LLM の入力になる** |

つまり、

* `talk_history` は **「ゲーム世界で何が話されたか」のログ**（人狼ゲームの内容）
* `llm_message_history` は **「自分が LLM とどうやり取りしたか」のログ**（裏方の通信記録）

です。サーバ視点では `talk_history` だけが意味を持ち、LLM 視点では `llm_message_history` だけが見えています。両者が同じ情報を持つわけではありません。

> **ポイント**：プロンプト内に書ける変数（[エージェントの内部状態とデータの流れ §3](../enhancement/agent_state.md#3-エージェントが保持している属性) の `key` 辞書）に **`llm_message_history` は含まれていません**。
> これは「LLMへの送り物」であって、「LLMに見せる素材」ではないからです。

一方で、

* 履歴が長くなるほど **トークン消費・コスト・レイテンシが増える**
* 過去の不適切な発言に **引きずられる** こともある

という弱点もあり、これをどう設計するかは [LLMとのやり取りパターン](../enhancement/llm_interaction_patterns.md) で扱います。

---

## ゲーム間のリセット

`llm_message_history` は **エージェントインスタンスの寿命** で持続します。
サンプルでは `set_packet` で `Request.INITIALIZE` を受け取ったときに、`talk_history` などと一緒にクリアされます。

```python
# src/agent/agent.py（抜粋）
if self.request == Request.INITIALIZE:
    self.talk_history: list[Talk] = []
    self.whisper_history: list[Talk] = []
    self.llm_message_history: list[BaseMessage] = []
```

これにより、**1ゲーム単位で会話履歴がリセット** されます。

---

## サンプルが使っていない LangChain の機能

LangChain には他にも多彩な機能がありますが、サンプルでは使われていません。参考までに名前だけ挙げておきます。

| 機能 | 何ができる？ |
|---|---|
| `ChatPromptTemplate` | LangChain ネイティブのプロンプトテンプレート（本プロジェクトでは Jinja2 を直接使用） |
| `RunnableBranch` | 条件によって分岐するチェーンを書ける |
| `RunnableParallel` | 複数の処理を並列で動かす |
| `MessagesPlaceholder` | プロンプトの中に「履歴を差し込む場所」を作る |
| Memory（`ConversationBufferMemory` など） | 履歴管理を専用クラスに任せる |
| Retrieval（`VectorStoreRetriever` など） | 外部知識を検索して LLM に渡す |

これらをどう取り入れるかは、エージェント改造の発展トピックです。

---

## まとめ

* LangChain は LLM 呼び出しを **共通インターフェース化** するライブラリ
* `ChatOpenAI` / `ChatGoogleGenerativeAI` / `ChatOllama` は `BaseChatModel` を継承した同形のクラス
* メッセージは `HumanMessage` / `AIMessage` などの **ロール付きオブジェクト** で表現
* `|` で処理を繋ぐ LCEL 記法。サンプルでは `llm_model | StrOutputParser()` を使用
* `llm_message_history` に積み続けることで **マルチターン** の文脈を維持している

---

[参加者マニュアルトップへ](../_index.md)\
[背景知識トップへ](./_index.md)\
[前へ（YAMLとは）](./about_yaml.md)\
[次へ（環境変数と.envファイル）](./about_env_vars.md)
