---
date: '2026-04-26T14:00:00+09:00'
draft: false
title: 'APIキーの取得と設定'
category: participants_guide
---

このページでは、LLM（大規模言語モデル）を呼び出すためのAPIキーを取得して、エージェントに設定する方法を説明します。

サンプルエージェントは次の3つのLLMに対応しています。

* **Google Gemini**（無料枠あり・初心者におすすめ）
* **OpenAI（GPT系）**
* **Ollama**（ローカルで動くLLM）

ここではいちばん始めやすい **Google Gemini** の取得方法を説明します。他のLLMを使う場合も、最後の `config.yml` の切り替え方は同じです。

---

## Google AI Studio でAPIキーを作る

1. ブラウザで [Google AI Studio のAPIキーページ](https://aistudio.google.com/api-keys) を開きます。
2. **「APIキーを作成」** をクリックします。
3. キー名（例：`aiwolf-nlp-agent-llm`）とプロジェクト名を入力します。
4. 作成後に表示された APIキー を **コピー** しておきましょう。

> **重要**：APIキーは絶対に他人に見せたり、GitHubに公開したりしないでください。
> `aiwolf-nlp-agent-llm` の `config/.env` は最初から `.gitignore` に入っているので、そこに書き込めば安全です。
>
> 「`.env` って何？」「なぜコードに直接書かないの？」という背景は [背景知識 ＞ 環境変数と.envファイル](../background/about_env_vars.md) に体系的にまとめてあります。

---

## `.env` に書き込む

`aiwolf-nlp-agent-llm` のフォルダに移動して、`config/.env` を開きます。

```bash
cd ~/aiwolfdial/aiwolf-nlp-agent-llm
```

エディタで `config/.env` を開くと、次のようになっているはずです。

```dotenv
OPENAI_API_KEY=YOUR_API_KEY
GOOGLE_API_KEY=YOUR_API_KEY
```

`GOOGLE_API_KEY=` の右側を、先ほどコピーしたAPIキーに置き換えて保存してください。
OpenAI を使うときは `OPENAI_API_KEY` の方を書き換えます。両方設定しても問題ありません。

---

## どのLLMを使うかを選ぶ

`config/config.yml` の `llm.type` で、実際に使うLLMを指定します。

```yaml
llm:
  type: google   # google / openai / ollama のどれか
  sleep_time: 3  # APIを呼ぶ前の待機秒数（レート制限対策）

openai:
  model: gpt-4o-mini
  temperature: 0.7

google:
  model: gemini-2.0-flash-lite
  temperature: 0.7

ollama:
  model: llama3.1
  temperature: 0.7
  base_url: http://localhost:11434
```

* **Gemini を使う**：`type: google` のまま、GeminiのAPIキーを `.env` に書いておけばOKです。
* **OpenAI を使う**：`type: openai` に変更し、`.env` の `OPENAI_API_KEY` を設定します。
* **Ollama を使う**：ローカルでOllamaを起動した上で、`type: ollama` に変更し、`base_url` と `model` を環境に合わせます。

モデルの名前（`gemini-2.0-flash-lite` など）は自由に変更できます。利用可能なモデルは各サービスの公式ドキュメントを確認してください。

---

## これで準備は完了です

* `.env` にAPIキーを書き込んだ
* `config.yml` で使うLLMを選んだ

次はいよいよエージェントを動かしてみましょう。

---

[参加者マニュアルトップへ](../_index.md)\
[準備トップへ](./_index.md)\
[前へ（リポジトリのクローン）](./clone_repo.md)\
[次へ（サーバの起動方法）](../execution/server.md)
