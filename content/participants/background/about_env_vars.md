---
date: '2026-04-26T14:00:00+09:00'
draft: false
title: '環境変数と.envファイル'
category: participants_guide
ShowToc: true
---

このページでは、本プロジェクトで **APIキーの管理** に使われている **環境変数** と、その実体である **`.env` ファイル** について説明します。
「`.env` って何？」「なんで API キーをコードに直接書いちゃダメなの？」というところから押さえていきたい方向けのページです。

> セットアップ手順としての `.env` の **書き方** は [準備 ＞ APIキーの取得と設定](../preparation/get_api_key.md) を参照してください。
> このページは「環境変数の概念と仕組み」に絞って解説します。

---

## 環境変数とは

**環境変数**（environment variable）は、**OSがプロセスに渡す「外から差し込む設定値」** です。
プログラムは実行時に `os.environ["GOOGLE_API_KEY"]` のような形で読み出せて、コードを書き換えなくても挙動を変えられます。

例えば次のように、シェルから一時的に設定して Python を起動できます。

```bash
export GOOGLE_API_KEY=AIza...   # シェルに環境変数を設定
python my_script.py             # この python から os.environ で読める
```

シェルを閉じると消える「**そのセッション限定の設定**」なので、毎回入力するのは面倒です。
そのため実用上は、**`.env` ファイル** にまとめて書いておき、起動時に読み込ませる方法が広く使われています。

---

## なぜコードに直接書かないのか

API キーやパスワードのような **秘密情報** をコードにベタ書きすると、次のような問題が起きます。

| 問題 | 起きること |
|---|---|
| **GitHub に公開してしまう** | 一度 push すると履歴から完全に消すのは難しく、即座にキーが流出する |
| **チームで共有しづらい** | 各自のキーを書いた状態で push し合うと、毎回コンフリクト |
| **環境ごとに切り替えづらい** | 本番・開発・ローカルで別のキーを使いたいのに、コード書き換えが必要に |
| **不正利用されやすい** | 公開リポジトリに混入したキーは、自動スキャンで数分以内に発見・悪用されることがある |

これらをまとめて避けるために、

* **コード**：`os.environ["GOOGLE_API_KEY"]` のように **読むだけ**
* **値**：`.env` のような **Git 管理外** のファイルに書く

という分離が定着しています。

---

## `.env` ファイル

`.env` は **環境変数を定義したテキストファイル** です。書き方はシンプルで、`KEY=VALUE` を1行ずつ並べるだけです。

```dotenv
# config/.env の例
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

* `=` の **前後にスペースは入れない**（`KEY = VALUE` は意図しない解釈になり得ます）
* **クォートは基本不要**。値に空白や `#` を含めたいときだけ `KEY="value with space"` のように囲む
* `#` で始まる行は **コメント**

---

## ファイル名が `.` で始まるのは「隠しファイル」だから

`.env` の **先頭の `.`** は、Unix/Linux/macOS の慣習で **「隠しファイル」** を表します。

* `ls` コマンドでは表示されない（`ls -a` で初めて見える）
* GUI のファイルマネージャでも、デフォルトでは表示されないことが多い

これは **「日常の操作では邪魔にならず、必要なときだけ意識する設定ファイル」** を表現するための慣習です。
`.env` 以外にも、`.gitignore` / `.git/` / `.bashrc` / `.vscode/` など、開発まわりの設定はだいたい `.` で始まります。

> **Windows ユーザーへの注意**：エクスプローラーでは「**隠しファイルを表示**」を有効にしないと `.env` が見えません。
> WSL を使っているなら、ターミナルから `ls -a config/` で確認するのが確実です。

> **空ファイルにしか見えないとき**：エディタで `.env` を作成したのに保存できない、開けないという場合、Windows のメモ帳が拡張子 `.txt` を勝手に付けていることがあります（`env.txt` になっていないか確認）。

---

## `python-dotenv`：`.env` を読み込む仕組み

Python では、`.env` ファイルの内容を `os.environ` に読み込む機能は **標準では提供されていません**。
代わりに、`python-dotenv` というライブラリの `load_dotenv()` 関数を使うのが定番です。

サンプルエージェント（`aiwolf-nlp-agent-llm`）では、`agent.py` の `__init__` で次のように呼び出されています。

```python
# src/agent/agent.py（抜粋）
from dotenv import load_dotenv

class Agent:
    def __init__(self, ...):
        ...
        load_dotenv(Path(__file__).parent.joinpath("./../../config/.env"))
```

これによって `config/.env` の中身が `os.environ` に流し込まれ、後段のコードから `os.environ["GOOGLE_API_KEY"]` として参照できるようになります。

```python
# src/agent/agent.py（initialize 内、抜粋）
self.llm_model = ChatGoogleGenerativeAI(
    model=...,
    temperature=...,
    api_key=SecretStr(os.environ["GOOGLE_API_KEY"]),  # ← .env から来た値
)
```

つまり **「コードはキーの値を知らない」**「**`.env` だけが値を知っている**」という構造が保たれています。

---

## `.gitignore` で必ず除外する

`.env` には秘密情報が入るので、**Git の追跡対象から外す** 必要があります。これを担当するのが `.gitignore` ファイルです。

サンプルエージェントの `.gitignore` には、最初から `.env` が登録されています。

```gitignore
# aiwolf-nlp-agent-llm/.gitignore（抜粋）
config/.env
```

> **重要**：自分でファイル名を変えたり、別の場所に `.env` を置いたりすると、`.gitignore` のパターンから外れて **誤ってコミットされる危険** があります。
> 既存の `.gitignore` の指定通りの場所に置くのが安全です。

`.gitignore` の書き方そのものは、[GitとGitHub ＞ .gitignore](./about_github.md#gitignore) を参照してください。

---

## `.env.example`：テンプレートとしての公開ファイル

`.env` は **個人ごとに値が違う** ため、リポジトリには直接コミットできません。
その代わり、**「キー名だけを書いた空のテンプレート」** を `.env.example` として共有するのが定番です。

サンプルエージェントにも `config/.env.example` が用意されています。

```dotenv
# config/.env.example
OPENAI_API_KEY=YOUR_API_KEY
GOOGLE_API_KEY=YOUR_API_KEY
```

これは `.gitignore` の対象外なので **公開リポジトリに含まれます**。
新しい開発者は `.env.example` をコピーして `.env` にリネームし、自分のキーを書き込む、という流れで使います。

```bash
cp config/.env.example config/.env
# 続けて config/.env を編集
```

---

## もし誤ってキーを公開してしまったら

GitHub に push してしまった場合、**履歴から消すだけでは不十分** です。GitHub のキャッシュやフォークに残ることがあるので、次の手順を踏んでください。

1. **すぐに該当キーを失効させる**（Google AI Studio・OpenAI などのコンソールから）
2. 新しいキーを発行して `.env` を書き換える
3. 必要であれば、過去のコミットから秘密情報を削除（`git filter-repo` などのツール）

> 一度漏れたキーは「もう使わない」と割り切るのが鉄則です。延命を考えるよりも、新しいキーを発行する方が安全で速いです。

---

## まとめ

* 環境変数は OS がプロセスに渡す「外から差し込む設定値」
* `.env` ファイルは環境変数をまとめて定義するテキスト。`KEY=VALUE` を並べるだけ
* `.` で始まるファイルは Unix の **隠しファイル** 慣習
* `.env` は **必ず `.gitignore` で除外** する。サンプルは最初から登録済み
* `.env.example` をテンプレートとして共有する流儀がある
* キーを誤公開したら即座に失効・再発行が鉄則

---

[参加者マニュアルトップへ](../_index.md)\
[背景知識トップへ](./_index.md)\
[前へ（LangChainとは）](./about_langchain.md)
