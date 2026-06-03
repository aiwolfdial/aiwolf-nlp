---
date: '2026-04-20T14:00:00+09:00'
draft: false
title: '【実習】LLM APIの実装手順を理解する（OpenRouter追加）'
category: participants_guide
ShowToc: true
---

こちらは [LangChainとは](./about_langchain.md) の **実習編** です。
解説ページで見た **基本の流れ（① モデル生成 → ② 呼び出し → ③ 応答取得）** と、**モデル追加で触るのは3か所だけ** という話を前提に、公式サンプルエージェント `aiwolf-nlp-agent-llm` に新しいLLMプロバイダ **OpenRouter** を **実際に書いて追加** します。

このページは実装が中心です。「なぜ3か所で済むのか」という仕組みの説明は [LangChainとは ＞ システム全体：どこに何があり、モデル追加でどこを触るか](./about_langchain.md#システム全体どこに何がありモデル追加でどこを触るか) にまとめてあるので、必要に応じて参照してください。
ゴールは「OpenRouterを足せること」そのものよりも、**この一周を終えたら、別の言語・別のフレームワークでも、LLM APIを使うシステムを自力で一から組み立てられるイメージが持てる** ことです。

> **想定読了時間**：30〜60分（OpenRouterの登録時間を除く）

---

## おさらい：今回触るのは3か所

[LangChainとは](./about_langchain.md) で見たとおり、LLM を使う処理は **① モデル生成 → ② 呼び出し → ③ 応答取得** の3ステップで、手前に準備（鍵・設定）、全体に横断的な備え（例外処理・タイムアウト・レート制御）が付きます。

新しいプロバイダを足すとき **書き換えるのは3か所だけ** です。

* **APIキー**（`config/.env`）…… 準備（→ Step A）
* **モデル生成の分岐**（`match model_type`）に1ケース追加 …… ①（→ Step B）
* **接続設定**（`config.yml` にプロバイダ用ブロック）…… 準備（→ Step C）

② 呼び出し・③ 応答取得・履歴・横断的な備えは **触りません**。どの LLM でも同じコードが使えるからで、その理由は [LangChainとは ＞ モデルを追加したいときに触るのは3か所](./about_langchain.md#モデルを追加したいときに触るのは3か所) を参照してください。
このページでは、その3か所を **Step A（鍵）→ Step B（モデル生成）→ Step C（設定）** の順に実際に書いていきます。

---

## なぜ OpenRouter を題材にするのか

[OpenRouter](https://openrouter.ai/) は、**1つのAPIキーで複数社のLLM（OpenAI / Anthropic / Google / Mistral / Meta など）を呼べる** ゲートウェイサービスです。教材として優れている点は次のとおりです。

| 観点 | 理由 |
|---|---|
| **APIがOpenAI互換** | 既存の `ChatOpenAI` の `base_url` を差し替えるだけで動く。「OpenAIっぽいけど別物」を1つ足す練習に最適 |
| **無料枠つきモデルがある** | `:free` サフィックス付きモデル（例：`openai/gpt-oss-20b:free`）はクレジット消費なしで試せる |
| **1キーで複数モデル試せる** | 各社にアカウントを作らずに、いろいろなモデルを比較できる |

サンプルエージェントは `openai` / `google` / `ollama` の3種にしか対応していません。**4つ目を自分で追加する** のが今回の作業です。

### 前提

* [準備](../preparation/_index.md) が完了している（`aiwolf-nlp-agent-llm` がクローン済み、Python仮想環境が動く）
* [LangChainとは](./about_langchain.md) を読み、`ChatOpenAI` / `match model_type` / `invoke` の構造をなんとなく把握している
* [環境変数と.envファイル](./about_env_vars.md) を読み、`.env` の役割を理解している

---

## 実装する：触る3か所

ここから実装です。書き換えるのは次の3ファイルだけで、順に進めます。

| Step | ファイル | 役割 |
|---|---|---|
| **Step A** | `config/.env` | APIキーを置く（準備） |
| **Step B** | `src/agent/agent.py` の `match model_type` | モデル生成に1ケース追加（①） |
| **Step C** | `config/config.yml` | 接続設定のブロック追加（準備） |

各ファイルが流れ全体（①〜③＋準備＋横断的な備え）のどこに位置するかは、[LangChainとは ＞ システム全体](./about_langchain.md#システム全体どこに何がありモデル追加でどこを触るか) の対応表を参照してください。② 呼び出し・③ 応答取得・履歴・横断的な備えは **触りません**。

### Step A：APIキーを発行して `.env` に保管する（準備）

#### A-1. OpenRouterでキーを発行する（認証）

LLM APIはほぼ例外なく、リクエストに **APIキー** を添えて「正規の利用者か」を判定します。

1. [https://openrouter.ai/](https://openrouter.ai/) を開き、右上の **Sign in** から Google や GitHub でログインします。
2. 右上のアバター → **Keys**（または [https://openrouter.ai/keys](https://openrouter.ai/keys)）を開きます。
3. **Create Key** をクリックします。
   * Name：`aiwolf-nlp-agent-llm` など分かる名前
   * Credit limit：空欄でOK（無料モデルしか使わないなら課金されません）
4. 表示されたキー（`sk-or-v1-...` で始まる文字列）を **コピー** します。

> **重要**：このキーは一度しか表示されません。忘れたら再発行してください。
> 公開しないこと、コードにベタ書きしないことについては [環境変数と.envファイル](./about_env_vars.md#なぜコードに直接書かないのか) を参照。

#### A-2. キーを `.env` に置く（コードから分離）

APIキーは **ソースコードに直接書いてはいけません**（Gitに乗せると即漏洩します）。
サンプルは起動時に `.env` を読み込み、環境変数として参照しています。

```python
# src/agent/agent.py（抜粋）
load_dotenv(Path(__file__).parent.joinpath("./../../config/.env"))  # __init__ 内で .env を環境変数に展開
...
api_key=SecretStr(os.environ["OPENAI_API_KEY"])  # 実際の参照は os.environ 経由
```

**コードにはキー名（文字列）しか現れず、値は環境側にある** のがポイント。だから `.env` に書き足すだけで使えます（この `load_dotenv` 自体は触りません）。

編集するのは2ファイルです。

**`config/.env.example`（テンプレート、Git管理対象）** の最終行に1行追加：

```dotenv
OPENAI_API_KEY=YOUR_API_KEY
GOOGLE_API_KEY=YOUR_API_KEY
OPENROUTER_API_KEY=YOUR_API_KEY
```

**`config/.env`（実際のキー、Git管理外）** に、A-1でコピーしたキーを貼り付け：

```dotenv
OPENAI_API_KEY=（既存のまま）
GOOGLE_API_KEY=（既存のまま）
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

`=` の前後にスペースを入れない、行末に余計な文字を入れないこと（[環境変数と.envファイル §`.env`ファイル](./about_env_vars.md#env-ファイル)）。

> **チェック**：`config/.env` は `.gitignore` で除外されているので `git status` に出ないはずです。

### Step B：`match model_type` に `openrouter` のケースを足す（① モデル生成）

設定とキーがそろったら、それらから **呼び出し可能なモデルオブジェクト** を作ります。
サンプルは `initialize()` で `llm.type` を見て、対応するクライアントを生成します。

```python
# src/agent/agent.py（抜粋）
model_type = str(self.config["llm"]["type"])
match model_type:
    case "openai":
        self.llm_model = ChatOpenAI(
            model=str(self.config["openai"]["model"]),
            temperature=float(self.config["openai"]["temperature"]),
            api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
        )
    case "google":
        self.llm_model = ChatGoogleGenerativeAI(...)
    case "ollama":
        self.llm_model = ChatOllama(
            model=str(self.config["ollama"]["model"]),
            temperature=float(self.config["ollama"]["temperature"]),
            base_url=str(self.config["ollama"]["base_url"]),
        )
    case _:
        raise ValueError(model_type, "Unknown LLM type")
```

各 `case` がやっているのは **「設定値（config.yml）」と「環境変数（.env）」を引数として渡す** だけです。
`case "ollama":` と `case _:` の **間** に、次を追加します。

```python
    case "openrouter":
        self.llm_model = ChatOpenAI(
            model=str(self.config["openrouter"]["model"]),
            temperature=float(self.config["openrouter"]["temperature"]),
            api_key=SecretStr(os.environ["OPENROUTER_API_KEY"]),
            base_url=str(self.config["openrouter"]["base_url"]),
        )
```

#### なぜこれで動くのか（重要）

* **新しいインポートは不要**：OpenRouter専用パッケージは要りません。既存の `ChatOpenAI` を使い回します。
* **OpenRouterはOpenAI互換**：`/chat/completions` の入出力スキーマがOpenAIと同じなので、`base_url` を差し替えるだけで別サービスを叩けます。
* **戻り値はどの `case` でも `BaseChatModel`**：だから後段の `(self.llm_model | StrOutputParser()).invoke(...)` は**まったく同じコード**で動きます（＝後の「答え合わせ」で確認する性質そのもの）。

この **「`ChatOpenAI` + `base_url`」パターン** は、vLLM・LM Studio・FastChat など多くのOSS推論サーバでも同じように使えます。

### Step C：`config.yml` に `openrouter:` を足して切り替える（準備：接続設定）

「どのモデルを、どんなパラメータで、どのエンドポイントに使うか」は、**コードに埋め込まず設定ファイルに出す** のが定石です。
サンプルの `config/config.yml`（日本語版は `config.jp.yml`）は `llm.type` で使うプロバイダを選び、プロバイダごとに設定ブロックを持ちます。

`ollama:` ブロックの直下に `openrouter:` を追加し、`llm.type` を切り替えます。

```yaml
llm:
  type: openrouter   # ← この実習では openrouter に切り替える
  sleep_time: 3       # ← 連続呼び出しの間隔（横断的な備え＝レート制御）

# ...（openai / google / ollama は既存のまま）...

openrouter:
  model: openai/gpt-oss-20b:free      # 最初は :free 付きが安全
  temperature: 0.7
  base_url: https://openrouter.ai/api/v1
```

ポイント：

* **`llm.type` を `openrouter` に** → Step B の `case "openrouter":` に入ります。
* **`model`** は [OpenRouter Models](https://openrouter.ai/models) から選べます。
* **`base_url`** は Step B でクライアントに渡す**接続先**。YAMLに出しておくと、後で別のOpenAI互換サーバ（vLLM等）にも転用できます。

> **モデルslugは時期で入れ替わります**。`:free` 系は予告なく終了することがあり、`openai/gpt-oss-20b:free` も将来 `404 No endpoints found` になり得ます。自分のキーから到達可能な `:free` モデルを一覧するワンライナー：
>
> ```bash
> curl -s -H "Authorization: Bearer $OPENROUTER_API_KEY" \
>   https://openrouter.ai/api/v1/models \
>   | python -c "import json,sys; [print(m['id']) for m in json.load(sys.stdin)['data'] if m['id'].endswith(':free')]"
> ```

> **YAMLでハマったら** [YAMLとは](./about_yaml.md) を。インデント（半角スペース2つ）と `: ` の後ろの半角スペースが要点です。
> プロンプト本文（`prompt:`）に `{{ info.agent }}` などを埋め込む仕組みは [Jinja2とは](./about_jinja2.md) を参照（今回は触りません）。

---

## 答え合わせ：触らなかった側を確かめる

Step A〜Cで触ったのは「鍵・設定・モデル生成」だけでした。
ここで、**あなたは ② 呼び出しも ③ 応答取得も履歴も、1行も書いていない** ことを確かめます。これらは `_send_message_to_llm()` の中で1本につながっています。

```python
# src/agent/agent.py（抜粋・簡略）
prompt = self.config["prompt"][request.lower()]          # 設定からテンプレート取得
prompt = Template(prompt).render(**key).strip()          # Jinja2でゲーム状態を埋め込む
self.llm_message_history.append(HumanMessage(content=prompt))                    # 文脈：user発言を履歴に
response = (self.llm_model | StrOutputParser()).invoke(self.llm_message_history) # ② 呼び出し → ③ 文字列で取得
self.llm_message_history.append(AIMessage(content=response))                     # 文脈：応答を履歴に追加
```

注目してほしいのは、この `(self.llm_model | StrOutputParser()).invoke(...)` が、`self.llm_model` の中身を **OpenAIだろうがOpenRouterだろうが気にしていない** こと。Step B で作ったのが `BaseChatModel`（LangChainの共通の型）である限り、呼び出しも応答取得も履歴も**無修正で動きます**。`invoke` / `|` / `StrOutputParser` が何をしているかは [LangChainとは ＞ チェーンと `|` 演算子](./about_langchain.md#②③-呼び出しと応答取得) を参照してください。

その外側を包む **横断的な備え** も、一切触っていません。

* **例外処理**：呼び出しフロー全体を `try/except` で囲み、失敗時は `None` を返して落とさない。投票などは `None` のとき生存者からランダム選択にフォールバック（`vote()` など）。
* **タイムアウト**：`@timeout` デコレータが別スレッドで実行し、`setting.timeout.action` を超えたら警告／強制終了。
* **レート制御**：`config.yml` の `llm.sleep_time` ぶん、呼び出し前に `sleep()`。

> Step B で `self.llm_model` が `BaseChatModel` になっている限り、② 呼び出し・③ 応答取得・履歴・横断的な備えは、**OpenRouterに対して無修正で動く**。「変える部分を1か所にまとめ、残りは共通のコードで動かす」——これを実際のコードで確認できました。
> （履歴設計のコスト・要約・打ち切りなどは [LLMとのやり取りパターン](../enhancement/llm_interaction_patterns.md) で扱います。）

---

## 起動して動作確認する

ターミナルで `aiwolf-nlp-agent-llm` に移動し、いつもどおり起動します。

```bash
cd ~/aiwolfdial/aiwolf-nlp-agent-llm
source .venv/bin/activate   # 仮想環境を有効化（プロジェクトの流儀に合わせて）
python src/main.py
```

正常に起動し、サーバ側のゲームでエージェントが発話していれば成功です。
**OpenRouterに実際にリクエストが飛んでいるか** は [OpenRouter Activity](https://openrouter.ai/activity) で履歴・トークン数・料金を確認できます。

### トラブルシューティング

どのStepでつまずいたかと対応づけて読むと、原因に辿り着きやすいです。

| 症状 | つまずいたStep | 対処 |
|---|---|---|
| `ValueError: openrouter Unknown LLM type` | Step B：`case "openrouter":` 追加忘れ | Step B を再確認 |
| `KeyError: 'OPENROUTER_API_KEY'` | Step A：`.env` にキーが無い／キー名のスペルミス | Step A を再確認（`.env` の保存も） |
| `KeyError: 'openrouter'`（configから） | Step C：`config.yml` に `openrouter:` セクションが無い | Step C を再確認（インデントも） |
| `AuthenticationError` / `401 Unauthorized` | Step A：キーが間違い／失効 | OpenRouterのKeysページで再発行 |
| `openai.NotFoundError: 404 - No endpoints found` | Step C：`model` slug が現時点で未提供（`:free` 停止／改名／タイポ） | Step C 末尾のワンライナーで到達可能な `:free` を一覧し差し替え |
| `RateLimitError: 429 ... rate-limited upstream` | レート制御：無料モデルは上流でレート制限されやすい | 少し待つ、`sleep_time` を増やす、別の `:free` へ（発展1も参照） |
| クレジット残高エラー | Step C：有料モデルを指定している | `:free` 付きに変更、またはクレジット入金 |

---

## 「発展」：余裕があれば

ここからは「OpenRouterを足せた」前提で、実用的な機能を作ります。
注目してほしいのは、**どれも ② 呼び出し本体（`invoke`）を書き換えずに実現できる** こと。
どのAIも同じ書き方で呼べるので、拡張は呼び出しのコードに手を入れず、その外側で足せます（「答え合わせ」で見た性質の応用です）。

### 発展1：上限が来たら自動で別モデルに切り替える（フォールバック連鎖）

無料モデルは混雑やレート上限（429）で失敗しがちです。**失敗したら自動で次のモデルへ切り替える** ようにしましょう。
LangChain には、まさにこのための `runnable.with_fallbacks([...])` があります（例外が起きたら控えへ順に切り替える）。

**Step B の `case "openrouter":` を、フォールバック対応に拡張：**

```python
    case "openrouter":
        def _make(model_name: str) -> ChatOpenAI:
            return ChatOpenAI(
                model=model_name,
                temperature=float(self.config["openrouter"]["temperature"]),
                api_key=SecretStr(os.environ["OPENROUTER_API_KEY"]),
                base_url=str(self.config["openrouter"]["base_url"]),
            )

        primary = _make(str(self.config["openrouter"]["model"]))
        fallback_models = self.config["openrouter"].get("fallback_models", [])
        if fallback_models:
            # primary が失敗したら、リストの順に切り替える
            self.llm_model = primary.with_fallbacks([_make(m) for m in fallback_models])
        else:
            self.llm_model = primary
```

**`config.yml` 側：本命＋控えを並べる**

```yaml
openrouter:
  model: openai/gpt-oss-20b:free        # 本命
  temperature: 0.7
  base_url: https://openrouter.ai/api/v1
  fallback_models:                       # 上から順に切り替わる控え
    - z-ai/glm-4.5-air:free
    - meta-llama/llama-3.3-70b-instruct:free
```

ポイント：

* `with_fallbacks` が返すのも「`.invoke` で呼べる・`|` でつなげる」**同じ顔の部品**なので、**`_send_message_to_llm` は1行も変えなくてよい**。
* 既定では「あらゆる例外」で切り替わります。レート上限だけに絞りたいなら `with_fallbacks([...], exceptions_to_handle=(...))` で対象例外を指定します。
* ねらいは「本命が混んでいる／上限でも、ゲームを止めずに発話を出し続ける」こと。

### 発展2：行動系（vote等）と発話系（talk等）でモデルを切り分ける

サンプルは **1つの `self.llm_model` をすべてのリクエストで使い回し** ています。
ですが用途を考えると、

* **発話系**（`talk`/`whisper`）… 多様で自然な発言がほしい → 温度高め・賢いモデル
* **行動系**（`vote`/`divine`/`guard`/`attack`）… 対象の名前だけを確実に返したい → 温度0・軽いモデル

と分けたくなります。これは「モデルを2つ持つ」改造で、サンプルの1モデル構成から一歩進んだ設計練習になります。

**考え方（スケッチ）**：

1. `config.yml` に発話用・行動用の2ブロックを用意（例：`openrouter_talk:` と `openrouter_action:`）。
2. `initialize()` で両方を生成して持つ（例：`self.llm_model` と `self.llm_model_action`）。
3. `_send_message_to_llm()`（またはリクエスト種別ごとのメソッド）で、リクエストが行動系なら `self.llm_model_action` を、発話系なら `self.llm_model` を使うよう **行き先を選ぶ**。

```python
# イメージ：リクエスト種別で使うモデルを選ぶ
action_requests = {"vote", "divine", "guard", "attack"}
model = self.llm_model_action if request.lower() in action_requests else self.llm_model
response = (model | StrOutputParser()).invoke(self.llm_message_history)
```

ここでも変わるのは「**どのモデルを選ぶか**」だけで、`invoke` の作法は同じです。
（賢いモデルを発話に、安いモデルを行動に振ってコスト最適化、という使い方もできます。改造の足がかりは [サンプルエージェントの改造](../enhancement/customize_agent.md) も参照。）

### 発展3：シングルターンとマルチターンを切り替えられるようにする

サンプルは毎回 **過去の全メッセージ** を送る **マルチターン**（[サンプルの履歴管理](./about_history.md#llm_message_history-に積んで毎回まとめて送る)）です。

* **マルチターン**：文脈を踏まえられるが、毎回トークンが増え、コストも上がり、過去に引きずられることもある。
* **シングルターン**：履歴を渡さず、その回の質問だけを単発で送る。独立・安価・安定だが、前の話は覚えない。

`_send_message_to_llm()` に **`stateless` スイッチ**を足して選べるようにします。

```python
    def _send_message_to_llm(self, request, ..., stateless: bool = False):
        ...
        if stateless:
            # シングルターン：履歴を渡さず、その回の質問だけ送る
            messages = [HumanMessage(content=prompt)]
        else:
            # マルチターン：これまでの履歴 ＋ 今回の質問
            self.llm_message_history.append(HumanMessage(content=prompt))
            messages = self.llm_message_history

        response = (self.llm_model | StrOutputParser()).invoke(messages)

        if not stateless:                 # シングルターンのときは履歴に積まない（独立させる）
            self.llm_message_history.append(AIMessage(content=response))
        return response
```

使い分けの例：「毎回独立に判定したい処理」はシングルターン、「会話の発言」はマルチターン。
設計上の比較は [LLMとのやり取りパターン](../enhancement/llm_interaction_patterns.md) に詳しくあります。

> 3つの発展に共通するのは、**② 呼び出し本体（`invoke`）を触らずに外側で拡張できている** こと。
> どのAIも同じ書き方で呼べるので、機能追加は呼び出しのコードの外側で完結します。これは「答え合わせ」で見た性質そのものです。

---

## まとめ

* OpenRouter追加で **書き換えたのは3か所だけ**：`config/.env` のキー・`config.yml` の `openrouter:` ブロック・`match model_type` の1ケース。OpenRouterは **OpenAI互換** なので `ChatOpenAI` の `base_url` 差し替えで足りた。
* **呼び出し・応答取得・履歴・横断的な備えは無修正** で動いた。LangChainがどのAIも同じ書き方に揃えているので、プロバイダの違いを `match` の1か所にまとめれば残りは共通のまま使える（仕組みの詳細は [LangChainとは](./about_langchain.md) を参照）。
* 発展（自動フォールバック・用途別モデル・シングル/マルチターン）も、**呼び出しのコードを触らず外側で足せる**。

この見方を持っておけば、フレームワークや言語が変わっても、LLM APIを使うシステムの全体像を自分で描けるはずです。
ここで身につけた手順は、[改良・拡張 ＞ サンプルエージェントの改造](../enhancement/customize_agent.md) でも繰り返し出てきます。

---

[参加者マニュアルトップへ](../_index.md)\
[背景知識トップへ](./_index.md)\
[戻る（LangChainとは）](./about_langchain.md)
