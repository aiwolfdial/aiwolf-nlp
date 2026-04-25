---
date: '2026-04-26T14:00:00+09:00'
draft: false
title: 'Jinja2テンプレートとは'
category: participants_guide
ShowToc: true
---

このページでは、本プロジェクトの `config.yml` の `prompt` セクションで使われている **Jinja2** の基本を説明します。
「`{% for %}` とか `{{ ... }}` ってそもそも何？」というところから押さえていきたい方向けのページです。

> Jinja2 をどう使ってプロンプトを組み立てているかは [改良・拡張 ＞ プロンプトエンジニアリング](../enhancement/prompt_engineering.md) 側で扱います。
> このページは「Jinja2 の文法そのもの」に絞って解説します。

---

## Jinja2 って何？

**Jinja2** は Python で広く使われているテンプレートエンジンです。
一言でいうと、**「穴あきの文字列」に、後から値を差し込んで完成形の文字列を作る仕組み** です。

たとえば、次のようなテンプレート

```jinja
こんにちは、{{ name }}さん。今日は{{ day }}日目です。
```

に対して、`name="ミナト"`, `day=3` を渡すと、

```text
こんにちは、ミナトさん。今日は3日目です。
```

という完成形の文字列が得られます。本プロジェクトでは、これを **LLMへの指示文** に使っています。

---

## 3種類の記号

Jinja2 で覚えるべき記号は、基本的に3種類だけです。

| 記号 | 用途 | 例 |
|---|---|---|
| `{{ ... }}` | **値の差し込み**（変数や式の結果を出力） | `{{ info.day }}` |
| `{% ... %}` | **制御構文**（if・for など、出力しない処理） | `{% if x %}` / `{% endif %}` |
| `{# ... #}` | **コメント**（出力に残らない） | `{# ここはメモ #}` |

---

## 変数の差し込み `{{ ... }}`

もっとも基本的な使い方です。

```jinja
自分の名前: {{ info.agent }}
役職: {{ role.value }}
```

* `info.agent` のように、**Python のオブジェクトの属性** にそのままアクセスできます。
* 辞書は `dict["key"]` でも `dict.key` でも書けます（どちらも動きます）。
* リストは `list[0]` のようにインデックスでも取り出せます。

### フィルタ（`|`）で加工する

値に `|` でフィルタをつなぐと、出力前に加工できます。

```jinja
{{ name | upper }}              {# 大文字に #}
{{ agents | join(", ") }}        {# リストをカンマ区切りに #}
{{ text | default("（なし）") }} {# None や空のときの代替表示 #}
{{ items | length }}             {# 件数を取得 #}
```

よく使うのは `join` / `length` / `default` あたりです。

---

## 条件分岐 `{% if %}`

```jinja
{% if info.divine_result is not none %}
占い結果: {{ info.divine_result.target }} は {{ info.divine_result.result }}
{% elif info.day == 0 %}
まだ占っていません。
{% else %}
結果は届いていません。
{% endif %}
```

ポイント：

* `is not none` で **None チェック** ができます（Python と少し違って `is not None` ではなく小文字の `none`）。
* `==` / `!=` / `>` / `<` などの比較もそのまま使えます。
* `and` / `or` / `not` も使えます。
* **`{% endif %}` を忘れない** のが一番よくある間違いです。

---

## 繰り返し `{% for %}`

```jinja
{% for talk in talk_history %}
{{ talk.agent }}: {{ talk.text }}
{% endfor %}
```

* リスト・タプル・辞書を回せます。
* `{% endfor %}` が必要です。
* 辞書を回すときは `items()` を使います。

```jinja
{% for agent, status in info.status_map.items() %}
{{ agent }}: {{ status }}
{% endfor %}
```

### スライスで部分だけを回す

Python と同じくスライスが使えます。本プロジェクトで頻出のパターンです。

```jinja
{% for w in talk_history[sent_talk_count:] %}
{{ w.agent }}: {{ w.text }}
{% endfor %}
```

これで「インデックス `sent_talk_count` 以降だけ」を取り出せます。

### ループ内で使える特別変数

`loop.index`（1 始まり）・`loop.index0`（0 始まり）・`loop.first` / `loop.last` などが使えます。

```jinja
{% for talk in talk_history %}
{{ loop.index }}. {{ talk.agent }}: {{ talk.text }}
{% endfor %}
```

---

## 空白と改行の制御（ハイフン `-`）

Jinja2 を書いていて **一番つまずきやすいのが空白制御** です。

`{% for %}` や `{% if %}` の前後には、自動的に改行や空白が残ってしまうことがあります。そのままだと、LLMに渡るプロンプトが妙にスカスカだったり、インデントが揃わなかったりします。

これを抑えるのが **ハイフン `-`** です。

| 記法 | 効果 |
|---|---|
| `{%- ... %}` | **直前** の空白・改行を削除 |
| `{% ... -%}` | **直後** の空白・改行を削除 |
| `{%- ... -%}` | 前後どちらも削除 |

例：

```jinja
{% for w in talk_history -%}
{{ w.agent }}: {{ w.text }}
{% endfor %}
```

こう書くと、各行の間の余計な空行が消えて、以下のようにきれいに並びます。

```text
ミナト: おはようございます。
サクラ: おはよう。
```

### 「何も出ないとき」は `{% if ... %}` ごと消す

条件を満たさないときに空行だけが残るのを防ぎたい場合は、**開始タグと終了タグの両方にハイフン** を入れます。

```jinja
{%- if info.divine_result is not none -%}
占い結果: {{ info.divine_result }}
{%- endif %}
```

---

## コメント `{# ... #}`

Jinja2 のコメントは、**最終出力に残りません**。

```jinja
{# このブロックは 'talk' のときだけ使う #}
{% for w in talk_history %}
{{ w.agent }}: {{ w.text }}
{% endfor %}
```

プロンプトの意図をメモしておきたいけれど LLM には見せたくない、というときに便利です。

---

## 変数に値を入れる `{% set %}`

同じ値を何度も書きたいときや、ちょっと加工した値を使い回したいときに便利です。

```jinja
{% set alive = info.status_map.items() | selectattr("1", "equalto", "ALIVE") | list %}
生存者数: {{ alive | length }}
```

本プロジェクトの標準プロンプトでは使われていませんが、**中〜上級** のプロンプトを書きたくなったときに思い出してください。

---

## よくあるエラーと対処

| 症状 | 主な原因 |
|---|---|
| `jinja2.exceptions.UndefinedError: 'xxx' is undefined` | 渡していない変数を参照している。`_send_message_to_llm` の `key` 辞書にその名前があるか確認 |
| `AttributeError: 'NoneType' object has no attribute ...` | `None` 属性に裸でアクセスしている。`{% if ... is not none %}` で囲む |
| `TemplateSyntaxError: Unexpected end of template` | `{% endif %}` / `{% endfor %}` の書き忘れ |
| 出力に変な空行が混じる | ハイフン `-` で空白制御する |

---

## 本プロジェクトでの使われ方

本プロジェクトでは、`config.yml` の `prompt.*` に Jinja2 テンプレートを書き、`src/agent/agent.py` の `_send_message_to_llm` メソッドが以下の流れで処理しています。

1. `config["prompt"][request]` からテンプレート文字列を取り出す
2. `info` / `setting` / `talk_history` / `role` などを含む辞書 `key` を作る
3. `Template(prompt).render(**key)` で値を差し込み、最終文字列を得る
4. それを LLM に投げる

つまり、**「テンプレートから参照できる変数は `key` に入れてある値だけ」** です。新しい値を参照したくなったら `key` に足す必要があります（詳しくは [プロンプトエンジニアリング](../enhancement/prompt_engineering.md) のコード改造の節へ）。

---

## まとめ

* `{{ }}` が値の差し込み、`{% %}` が制御構文、`{# #}` がコメント
* `is not none` と `{% endif %}` / `{% endfor %}` 忘れに注意
* 空白が気になったら `-` を使う
* スライス（`list[n:]`）は Python と同じ感覚で使える
* 参照できる変数は、コード側（`_send_message_to_llm` の `key`）で決まる

---

[参加者マニュアルトップへ](../_index.md)\
[背景知識トップへ](./_index.md)\
[前へ（WebSocketとは）](./about_websocket.md)\
[次へ（YAMLとは）](./about_yaml.md)
