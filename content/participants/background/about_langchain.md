---
date: '2026-04-20T14:00:00+09:00'
draft: false
title: 'LangChainとは'
category: participants_guide
ShowToc: true
---

こちらのページでは、サンプルエージェントが LLM とのやり取りに使っている **LangChain** の最低限の語彙と仕組みを説明します。

---

## LangChain って何？

**LangChain** は、LLM（大規模言語モデル）を使ったアプリケーションを書くための Python ライブラリです。
ざっくりと言うと、次の3つを **共通のインターフェース** で扱えるようにしてくれます。

| 機能 | LangChain の何が嬉しいか |
|---|---|
| **モデルを差し替えやすくする** | OpenAI / Google / Ollama などを、ほぼ同じコードで切り替えられる |
| **会話履歴を管理する** | 「役割つきメッセージ」のリストとして、過去のやり取りを保てる |
| **処理を組み合わせる** | 「LLM → 整形 → 別の LLM」のような流れを \| で繋げて書ける |

---

## LLM API を使う基本の流れ

LangChain で LLM を使うとき、処理の中心は次の3ステップです。どの LLM（GPT でも Claude でも）でも、この流れは変わりません。

1. **① モデル生成** … どの LLM を、どんな設定で使うか決めて、呼び出し用のオブジェクトを作る
2. **② 呼び出し** … プロンプトを渡して実行する
3. **③ 応答取得** … 返ってきた応答を文字列で受け取る

その手前に、APIキーや接続設定をそろえる「準備」が入ります。

```
 準備 ──▶  ① モデル生成  ──▶  ② 呼び出し  ──▶  ③ 応答取得
（鍵・設定） 呼び出し用の        プロンプトを渡して    返ってきた応答を
            オブジェクトを作る   実行する             文字列で受け取る
```

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

## はじめに：要素・invoke・チェーン

①②③ の説明に入る前に、このページで繰り返し登場する4つの言葉——**要素**（モデル・パーサ）と、**それを扱う言葉**（invoke・チェーン）——の意味を整理しておきます。

LangChain では、LLM を使った処理を、いくつかの **要素** を組み合わせて構成します。ここで登場する要素は2種類です。

* **モデル**（`ChatOpenAI` など）… LLM に入力を送り、応答を受け取る要素。
* **パーサ**（`StrOutputParser`）… モデルの応答を、扱いやすい形に変換する要素。モデルの応答は本文以外の情報も含んだ形（`AIMessage(content="こんにちは", ...)`）で返るため、本文だけを取り出したいときは少し手間がかかります。パーサを通すと、この本文部分だけが取り出され、ただの **文字列**（`"こんにちは"`）になります。

これらの要素を扱うための言葉が、次の2つです。

* **invoke（実行する）** … 要素に入力を渡して動作させるメソッドです。`要素.invoke(入力)` と書くと、その要素が実行され、結果が返されます。モデルもパーサも、実行する操作はいずれも `invoke` で共通しています。
* **チェーン（`|` でつなぐ）** … 要素どうしを `|`（縦棒）でつなぐと、「左の要素の出力を、右の要素の入力にする」という一続きの処理になります。これを **チェーン** と呼びます。チェーンもひとつの要素として扱え、同じく `invoke` で実行できます。

```python
# モデルとパーサを | でつなぎ（チェーン）、invoke で実行する
chain = model | StrOutputParser()   # 「モデルで応答を得る → 文字列に変換する」を一続きにする
answer = chain.invoke(messages)      # 実行すると、変換後の文字列が返る
```

以降の①②③では、この **「要素を `invoke` で実行する」「要素を `|` でつないでチェーンにする」** という考え方が繰り返し登場します。この2点を押さえれば、以降の説明はすべて読み解けます。
それでは、①から順に見ていきます。

---

## ① モデル生成：ChatModel と共通インターフェース

LangChain では、各社のチャット系 LLM のクラス（`ChatOpenAI` / `ChatGoogleGenerativeAI` / `ChatOllama`）が、**`BaseChatModel` という共通のおおもとの型をもとに作られています**。
`BaseChatModel` は「チャット系モデルはこういう操作ができる」という共通の取り決めです。各社のクラスはこの取り決めに従っているので、**どれも同じ書き方（`invoke` など）で扱えます**。
そのおかげで、サンプルでは `llm.type` の値で生成するクラスを切り替えるだけで、後段のコードはまったく同じものが使えます。

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

## ②③ 呼び出しと応答取得

①で作った `self.llm_model` に **プロンプトを渡して実行し（②）、応答を文字列で受け取る（③）** のがこのステップです。サンプルでは1行で書かれています。

```python
response = (self.llm_model | StrOutputParser()).invoke(messages)
```

この1行を、**②に渡すもの → ②実行 → ③受け取るもの** の順に分解します。

### ②に渡すもの：メッセージの型（HumanMessage / AIMessage）

`invoke` に渡す `messages` は、**ロール（役割）付きメッセージのリスト** です。
[LLMとのチャットはどうなっている？](./about_llm_chat.md) で見た「誰が何を言ったか」の1件1件を、LangChain では次の型で表します。

| クラス | 役割（OpenAI 用語） | 中身 |
|---|---|---|
| `SystemMessage` | system | LLM に与える役割設定や前提（サンプルでは未使用） |
| `HumanMessage` | user | ユーザーからの入力 |
| `AIMessage` | assistant | LLM の返答 |

たとえば最小の入力は `[HumanMessage(content=prompt)]` という1件のリストです。
（サンプルは会話を続けるため、ここに過去のやり取りも含めた履歴を渡しています。その仕組みは [サンプルの履歴管理](./about_history.md) で。）

### ② 呼び出し：invoke

`invoke(messages)` で①のモデルを実行します。これが「LLM にプロンプトを送って応答をもらう」本体です。
`invoke` の戻り値は、ロール付きの `AIMessage` です。

### ③ 応答取得：StrOutputParser で文字列にする

`invoke` の戻り値である `AIMessage` のままだと、`response.content` のように中身を取り出す手間がかかります。これを省くのが `StrOutputParser` で、はじめに見た `|` でモデルとつなぐと「モデルで応答を得る → 文字列に変換する」が一続きのチェーンになります。

```python
chain = self.llm_model | StrOutputParser()   # ② → ③ を1本に繋ぐ（チェーン）
response: str = chain.invoke(messages)        # 実行すると、ただの str が返る
```

このチェーンを `invoke` したときの流れは、

1. ①のモデルが実行され、`AIMessage` を返す（**② 呼び出し**）
2. その `AIMessage` が `StrOutputParser` に渡される
3. `StrOutputParser` が `.content`（文字列）を取り出す
4. 最終的に **ただの `str`** が `response` に入る（**③ 応答取得**）

> **ここが共通インターフェースの実利**：`invoke` も `|` も、`self.llm_model` の中身が OpenAI か Google かを問いません。
> **①でどのクラスを選んでも、②③ のコードは同じまま** です。

---

## ①〜③を繰り返して会話を続ける（履歴）

ここまでが LLM 呼び出し **1回分** の ① → ② → ③ です。
会話を続けるには、この ①〜③ を繰り返しながら、過去のやり取りを毎回 `messages` に積んで送ります（＝[マルチターン](./about_llm_chat.md)）。

サンプルエージェントがこれを実際にどう実装しているか——`llm_message_history` への積み方、ゲーム内発言の `talk_history` との違い、ゲーム間のリセット——は、別ページにまとめました。

> ☛ **[サンプルの履歴管理](./about_history.md)**\
> `HumanMessage` / `AIMessage` を使った履歴の積み方と、混同しやすい2つの「履歴」リストの違いを説明しています。

---

## システム全体：どこに何があり、モデル追加でどこを触るか

ここまでの語彙が、サンプルエージェントの実際のファイルにどう割り当てられているかをまとめます。
基本の流れ（① → ② → ③ ＋ 準備）に加え、フロー全体を障害・遅延から守る **横断的な備え**（例外処理・タイムアウト・レート制御）も、それぞれ次の場所に実装されています。

| 役割 | 実装の場所 | ひとことで言うと |
|---|---|---|
| 準備：APIキー | `config/.env` → `load_dotenv` → `os.environ` | 鍵をコードから分離して読み込む |
| 準備：接続設定 | `config/config.yml` の `llm:` と各プロバイダブロック | どのモデル・パラメータ・エンドポイントか |
| ① モデル生成 | `agent.py` `initialize()` の `match model_type` → `self.llm_model` | 種別に応じて `ChatOpenAI` などを作る |
| ② 呼び出し ＋ ③ 応答取得 | `agent.py` `_send_message_to_llm()` の `(self.llm_model \| StrOutputParser()).invoke(...)` | APIを叩いて文字列を受け取る |
| 文脈の管理 | `agent.py` `self.llm_message_history` | これまでの会話を記録する |
| 横断的な備え | `try/except`・`@timeout`・`llm.sleep_time` | 障害・遅延・レート制限からフローを守る |

### モデルを追加したいときに触るのは3か所

新しい LLM プロバイダを足すとき、書き換えるのは次の3か所だけです。

* **モデル生成の分岐**（`match model_type`）に1ケース追加 …… ①
* **接続設定**（`config.yml` にプロバイダ用のブロック）…… 準備
* **APIキー**（`config/.env`）…… 準備

② 呼び出し・③ 応答取得・履歴・横断的な備えは **触りません**。
理由は、これらが共通インターフェース（`BaseChatModel`）の上で書かれていて、どの LLM でも同じコードが使えるからです。
LLM ごとに違うのは「どれを、どんな設定で使うか」だけで、その違いは **① モデル生成の1か所** に収まります。だから残りを書き換えずに済みます。

もし LangChain がなければ、LLM を1つ足すたびに、呼び出し方も・履歴の積み方も・結果の受け取り方も LLM ごとに書き分けることになります。LangChain がその違いを ① の1か所にまとめてくれるので、触る場所と触らない場所がはっきり分かれます。

実際にこの3か所を書いて新プロバイダ（OpenRouter）を追加する手順は、実習ページで扱います。

> ☛ **【実習】[OpenRouter APIを追加する](./exercise_openrouter.md)**\
> `ChatOpenAI` の `base_url` を差し替えるだけで別の LLM プロバイダを叩ける、という頻出パターンを、手を動かして確認できます。

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

### なぜ `ChatPromptTemplate` ではなく Jinja2 なのか

このサンプルは、プロンプト本文を **`config.yml` 側に完全に追い出して、Python コードを触らずに編集できる** ことを重視しています。しかもその本文には、占い結果が「ある日／ない日」で行ごと出し分ける条件分岐や、トーク履歴を整形して並べる繰り返しが必要です。
LangChain の `ChatPromptTemplate` は基本が `{変数}` の差し込みで、こうした条件分岐・繰り返しは扱えません。一方 [Jinja2](./about_jinja2.md) は `{% if %}` / `{% for %}` をテンプレート側に書けるため、整形のロジックを Python に漏らさず設定ファイルだけで完結できます。この要件に合うのが Jinja2 です。
（Jinja2 はロール構造を直接は扱えないため、サンプルは「Jinja2 で文字列を整形 → それを `HumanMessage` に包む」と役割分担しています。）

---

## まとめ

* LangChain では処理を **要素**（モデル・パーサ）の組み合わせで構成する。要素を実行するのが `invoke`、`|` でつないだ一続きが **チェーン**
* LangChain で LLM を使う処理は **① モデル生成 → ② 呼び出し → ③ 応答取得** が中心で、その手前に準備（鍵・設定）が入る
* ① の各社クラス（`ChatOpenAI` など）は、共通のおおもとの型 `BaseChatModel` をもとに作られた同じ形のもの。だからモデルを差し替えても ②③ のコードは変わらない
* メッセージは `HumanMessage` / `AIMessage` などの **ロール付きオブジェクト** で表現
* ②③ は `|` でモデルとパーサをつないだチェーンを `invoke` で実行し、`StrOutputParser` で文字列にして受け取る
* ①〜③を繰り返して会話を続ける **履歴の実装**（`llm_message_history` の積み方、`talk_history` との違い）は [サンプルの履歴管理](./about_history.md) へ
* **モデルを追加するとき触るのは3か所**（モデル生成の分岐・接続設定・APIキー）。残りを触らずに済むのは共通インターフェースのおかげ

---

## 手を動かして学びたい方へ

ここまでの内容を **実際にコードを書いて確認する** ための実習ページを用意しています。
サンプルエージェントに新しい LLM プロバイダ（OpenRouter）を追加して、「触るのは3か所だけ／残りを触らなくていい理由」を体感できます。
発展課題として、**上限到達時の自動フォールバック**・**用途別のモデル切り分け**・**シングル/マルチターンの切り替え** も扱います。

☛ 【実習】[OpenRouter APIを追加する](./exercise_openrouter.md)

---

[参加者マニュアルトップへ](../_index.md)\
[背景知識トップへ](./_index.md)\
[前へ（LLMとのチャットはどうなっている？）](./about_llm_chat.md)\
[次へ（サンプルの履歴管理）](./about_history.md)
