---
date: '2026-04-20T14:00:00+09:00'
draft: false
title: 'サンプルの履歴管理'
category: participants_guide
ShowToc: true
---

このページは、サンプルエージェントが **会話の履歴をどう実装しているか** の解説です。

* 「LLM は記憶を持たず、会話を続けるには過去のやり取りを毎回まとめて送り直す（＝マルチターン）」という **概念** は [LLMとのチャットはどうなっている？](./about_llm_chat.md) を、
* `HumanMessage` / `AIMessage` / `invoke` といった **LangChain の語彙** は [LangChainとは](./about_langchain.md) を、

先に読んでいる前提で進めます。ここでは「その仕組みを、サンプルが実際のコードでどう回しているか」に絞ります。

---

## `llm_message_history` に積んで、毎回まとめて送る

サンプルは、ユーザーの発言を `HumanMessage`、LLM の応答を `AIMessage` として `llm_message_history` というリストに積み、**毎回そのリストごと** `invoke` に渡します。

```python
# src/agent/agent.py（抜粋）
self.llm_message_history.append(HumanMessage(content=prompt))                    # 今回の質問を積む
response = (self.llm_model | StrOutputParser()).invoke(self.llm_message_history) # 履歴ごと送って実行
self.llm_message_history.append(AIMessage(content=response))                     # 応答も積む
```

`_send_message_to_llm` を複数リクエストにわたって追うと、送る中身が毎回増えていくのが分かります。

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

このように、毎回 **`llm_message_history` のすべてを送り直す** ことで、「自分が前にどう発言したか」「前回の投票理由は何だったか」を踏まえた応答が返ってきやすくなります。
これが、[LLMとのチャットはどうなっている？](./about_llm_chat.md) で見たマルチターンの、サンプルでの実装です。

---

## `llm_message_history` と `talk_history` は別物です

`agent.py` には **「履歴」と名のつくリストが2つ** あり、初見では混乱しやすいので明確に区別してください。

| 名前 | 中身 | 何を記録している？ | LLM への渡り方 |
|---|---|---|---|
| `talk_history` | `Talk` オブジェクトのリスト（aiwolf-nlp-common） | **ゲーム内の他プレイヤーの発言**。サーバから届いたものを蓄積 | プロンプトテンプレートの中で `{% for w in talk_history %}` のように **明示的に埋め込む** ことで LLM に渡る |
| `llm_message_history` | `BaseMessage` のリスト（LangChain） | **エージェントが LLM に送ったプロンプト** と **LLM が返した応答** のやり取りそのもの | `(self.llm_model \| StrOutputParser()).invoke(self.llm_message_history)` で **そのまま LLM の入力になる** |

つまり、

* `talk_history` は **「ゲーム世界で何が話されたか」のログ**（人狼ゲームの内容）
* `llm_message_history` は **「自分が LLM とどうやり取りしたか」のログ**（裏方の通信記録）

です。サーバ視点では `talk_history` だけが意味を持ち、LLM 視点では `llm_message_history` だけが見えています。両者が同じ情報を持つわけではありません。

> **ポイント**：プロンプト内に書ける変数（[エージェントの内部状態とデータの流れ §3](../enhancement/agent_state.md#3-エージェントが保持している属性) の `key` 辞書）に **`llm_message_history` は含まれていません**。
> これは「LLM への送り物」であって、「LLM に見せる素材」ではないからです。

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

## この実装の弱点と、設計の選択肢

毎回すべてを送り直すこの方式には、次の弱点もあります。

* 履歴が長くなるほど **トークン消費・コスト・レイテンシが増える**
* 過去の不適切な発言に **引きずられる** こともある

そのため、履歴を要約する・古い分を打ち切る・そもそも履歴を渡さない（シングルターン）といった選択肢があります。
これらをどう設計するかは [改良・拡張 ＞ LLMとのやり取りパターン](../enhancement/llm_interaction_patterns.md) で扱います。

---

## まとめ

* サンプルは `HumanMessage` / `AIMessage` を `llm_message_history` に積み、**毎回そのリストごと送る**（マルチターンの実装）
* `talk_history`（ゲーム内の発言ログ）と `llm_message_history`（LLM との通信ログ）は **別物**。前者はプロンプトに埋め込んで渡し、後者はそのまま `invoke` の入力になる
* `llm_message_history` は `Request.INITIALIZE` で **1ゲームごとにリセット** される
* 「毎回全部送る」ことの弱点（コスト・引きずられ）への対処は [LLMとのやり取りパターン](../enhancement/llm_interaction_patterns.md) へ

---

[参加者マニュアルトップへ](../_index.md)\
[背景知識トップへ](./_index.md)\
[前へ（LangChainとは）](./about_langchain.md)\
[次へ（環境変数と.envファイル）](./about_env_vars.md)
