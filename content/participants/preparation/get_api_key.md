---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: 'API取得方法'
category: participants_guide
---

このページでは、**Google AI Studio で API キーを作成**し、**ローカルの `aiwolf-nlp-agent-llm` に設定**するまでを説明します。
基本は無料の **Gemini（Google）API** を前提にしていますが、`OPENAI_API_KEY` などの他ベンダー用キーも同様の手順で追加できます。

---

## Google AI Studio で API キーを作成する

1. ブラウザで **Google AI Studio** のキー管理ページを開く：
   `https://aistudio.google.com/api-keys`
2. **「APIキーを作成」** をクリック
3. **キー名** と **インポートするプロジェクト** を任意に設定

   * 例：キー名 **`aiwolf-nlp-agent-llm`**、プロジェクト名 **`aiwolfdial`**
4. **「キーを作成」** をクリック
5. **APIキー** 一覧の表から、今作成したキー名をクリック → **「キーをコピー」** を押してクリップボードにコピー

> セキュリティ：API キーは外部に公開しないでください。Git にコミットしないよう注意してください（`aiwolf-nlp-agent-llm` では`.env` は `.gitignore` 済みに設定済みです）。

---

## `.env` に API キーを設定する

`aiwolf-nlp-agent-llm` ディレクトリの `config/.env` に先ほど取得したAPIキーを貼り付けます。

1. aiwolf-nlp-agent-llmをコードエディタで開く

```bash
cd ~/aiwolfdial/aiwolf-nlp-agent-llm
code aiwolf-nlp-agent-llm
```

1. エディタで `config/.env` を開き、以下の **`YOUR_API_KEY`** を **先ほどコピーしたキー** に置き換えます。

```dotenv
# 例（必要に応じて使うものだけ設定）
OPENAI_API_KEY=YOUR_API_KEY
GOOGLE_API_KEY=YOUR_API_KEY
```

* **Gemini（Google）を使う場合**：最低でも `GOOGLE_API_KEY` を設定してください。
* **OpenAI を併用する場合**：`OPENAI_API_KEY` も設定します。

---

## `config.yml` で使用する LLM を選ぶ

どのベンダーの API を使うか、どのモデルを使うかを **`config/config.yml`（または `config/config.jp.yml`）** で指定します。

初期の `config/config.yml` では、以下のように設定してあります：

```yaml
llm:
  type: google   # ← まずは Google(Gemini) を使うなら 'google'
  sleep_time: 3  # API 呼び出し間隔の秒数（レート制限対策）

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

* **Gemini の無料枠で始める**なら、`llm.type: google` のままで OK（モデルもそのままで問題ありません）。
* **OpenAI を使う**場合は、`.env` に `OPENAI_API_KEY` を入れ、`llm.type: openai` に切り替え、`openai.model` を好みに合わせて調整します。
* **Ollama（ローカル LLM）** を使う場合は、`llm.type: ollama` にし、`base_url` と `model` を手元の環境に合わせてください。

> ⚙️ どの設定を使うかは **`llm.type`** が決め手です。`.env` に複数ベンダーのキーを入れておいても問題ありませんが、**実際に使うのは `llm.type` で指定したもの**になります。

---

## まとめ

* **Google AI Studio** で API キーを作成 → **`config/.env` に貼り付け**
* **`config.yml` の `llm.type`** で使用するベンダーを選択（まずは `google` 推奨）
* モデル名や `temperature` は後でチューニング可能。まずはデフォルトで OK

これで **API キーの取得と設定は完了** です。

---

[参加者マニュアルトップへ](../_index.md)\
[準備トップへ](./_index.md)\
[前へ（リポジトリのクローン）](./clone_repo.md)\
[次へ（サーバ起動方法）](../execution/server.md)
