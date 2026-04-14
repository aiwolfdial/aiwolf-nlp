---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: 'playground：人狼以外の議論にも使える環境'
category: participants_guide
---

## このページについて（おまけセクション）

このページでは、人狼知能大会のサーバを **人狼ゲーム以外の用途** に活用できる仕組み、**playground** を紹介します。
人狼のルールを一切使わず、**複数のAIエージェントが同じ話題について議論するだけの環境** を簡単に立ち上げられます。

対応するエージェントは、サンプルとは別リポジトリで公開されている **[playground-agent-llm](https://github.com/nharu-0630/playground-agent-llm)** です。

---

## 何ができる？

playground は、人狼ゲームの「追放・占い・襲撃」といった要素をすべて取り払い、**昼の会話だけ** を残した環境です。

そのため、次のような用途に応用できます。

* **一般的な議題についての集団議論**（例：新製品のアイデア出し、街づくりの話し合い、倫理ジレンマの討論など）
* **異なる性格のエージェント同士の会話実験**
* **マルチエージェント対話の研究・プロトタイピング**
* **LLMのロールプレイ能力の検証**

人狼ゲームに限らず、「複数のLLMエージェントに何かのトピックを議論させたい」という場面で、手軽に使える対話プラットフォームになります。

---

## サーバ側の設定（playground.yml）

[サーバの起動方法](../execution/server.md) と同じ手順で、サーババイナリと `playground.yml` をダウンロードして起動します。

```bash
curl -LO https://github.com/aiwolfdial/aiwolf-nlp-server/releases/latest/download/playground.yml
./aiwolf-nlp-server-linux-amd64 -c ./playground.yml
```

`playground.yml` の特徴は以下のとおりです。

* **役職がすべて村人**（人狼・占い師・狂人などは0人）
* **夜のフェーズが存在しない**（昼の会話だけを繰り返す）
* **最大5日間、毎日会話する**
* **カスタムプロフィール（日本語名・性格設定）が有効**

役職ではなく性格・プロフィールを指針に各エージェントが議論するため、ロールプレイ色の強い会話が観察できます。

---

## エージェント側：playground-agent-llm

playground 用のエージェントは、サンプルと同じく `aiwolf-nlp-common` をベースにした Python 実装です。
人狼に特化した要素（投票・占い・囁きなど）が削ぎ落とされ、**トークだけを扱うシンプルな構成** になっています。

### クローンと環境構築

```bash
cd ~/aiwolfdial
git clone https://github.com/nharu-0630/playground-agent-llm.git
cd playground-agent-llm

# 設定ファイルを準備
cp config/config.yml.example config/config.yml
cp config/.env.example config/.env

# 依存関係をインストール（uv 推奨）
uv sync
```

### 起動

```bash
uv run python src/main.py
```

サーバ（`playground.yml` で起動済み）に自動で接続し、議論が始まります。

---

## config.yml の中身

`playground-agent-llm` の `config.yml` は、基本的に `aiwolf-nlp-agent-llm` と同じ構造ですが、**`prompt` セクションに残っているのは `initialize` / `daily_initialize` / `talk` / `daily_finish` の4つだけ** です。人狼ゲーム特有のプロンプト（投票・占い・襲撃など）はありません。

例：`prompt.talk` はシンプルに次のようになっています。

```yaml
prompt:
  talk: |-
    トークリクエスト
    履歴:
    {% for w in talk_history[sent_talk_count:] -%}
    {{ w.agent }}: {{ w.text }}
    {% endfor %}
```

これを自分の議論テーマに合わせて書き換えるだけで、エージェントに **任意のトピックで議論** させられます。
例えば次のように書き換えれば、環境問題についての議論を始められます。

```yaml
prompt:
  initialize: |-
    あなたは議論ゲームのエージェントです。
    名前は{{ info.agent }}です。

    今日は「家庭でできる環境への取り組み」について話し合います。
    あなたの性格やプロフィールをもとに、自然に意見を述べてください。

    {% if info.profile is not none -%}
    あなたのプロフィール: {{ info.profile }}
    {%- endif %}

    発言のみを出力してください。話すことがなければ「Over」と出力してください。
```

---

## どう使うと面白い？

次のようなアイデアがあります。

1. **ペルソナ別の意見分布を観察する**\
   `custom_profile` でキャラクターの性格を変えておき、LLMが性格に沿った発言をするか検証できます。
2. **同じLLMで思考パターンを比較する**\
   `config.yml` の `llm.type` を切り替えて、OpenAI・Gemini・Ollama の差を観察できます。
3. **会話データの自動収集**\
   ゲームログ（`.log` / `.json`）がそのまま使えるので、対話コーパスを手軽に作れます。
4. **人狼以外の研究題材**\
   意思決定・説得・誤情報の拡散・集団極性化など、マルチエージェント研究のお試し環境として活用できます。

---

## 注意点

* playground は **非公式のおまけ機能** です。公式大会のルールには含まれません。
* `playground-agent-llm` は `aiwolfdial` 公式ではなく、**個人リポジトリ（`nharu-0630`）** で公開されています。将来仕様が変わる可能性があります。
* 研究や教育目的で自由に使って構いませんが、結果を公開する際は「人狼知能大会のサーバ基盤を流用している」旨を明記するのが望ましいです。

---

## まとめ

* `playground.yml` ＋ `playground-agent-llm` で、**人狼のルールなしのピュアな議論環境** を手元に持てる
* プロンプトを書き換えるだけで、**任意のトピックの集団議論** を実験できる
* 研究・教育・プロトタイピングの出発点として、とても扱いやすい

人狼に飽きたら、あるいは「人狼じゃなくてもこの基盤を使ってみたい」と思ったら、ぜひ試してみてください。

---

[参加者マニュアルトップへ](../_index.md)\
[応用編トップへ](./_index.md)\
[前へ（サーバ設定の編集方法）](./local_battle_setup.md)\
[次へ（背景知識）](../background/_index.md)
