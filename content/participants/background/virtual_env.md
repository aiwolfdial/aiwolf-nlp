---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: '仮想環境とは'
category: participants_guide
ShowToc: true
---

## 仮想環境って何？

Pythonの **仮想環境** は、プロジェクトごとに **独立したPython環境** を作る仕組みです。
ライブラリを入れたり消したりするときの影響を、そのプロジェクトの中だけに閉じ込められるのが最大のメリットです。

たとえば、次のような状況を防げます。

* プロジェクトAでは `langchain` 0.3 が必要、プロジェクトBでは 0.2 が必要
* システム全体のPythonに色々入れすぎて、壊れたときに戻せない

---

## 本プロジェクトで使うもの

`aiwolf-nlp-agent-llm` では **[uv](https://docs.astral.sh/uv/)** というツールを使うのが標準です。
`uv` は仮想環境の作成と依存関係のインストールをまとめて行ってくれるので、仮想環境の作成・有効化・パッケージ管理を自分で意識する必要がほぼありません。

詳しい導入は [開発環境の準備](../preparation/setup.md) と [リポジトリのクローン](../preparation/clone_repo.md) をご覧ください。

---

## Pythonの仮想環境ツール比較

参考までに、主な仮想環境ツールの特徴を表にまとめます。本大会では `uv` が推奨ですが、他のツールでも開発できます。

| ツール | 特徴 | ロック/再現性 | 速度 | 向いている場面 |
|---|---|---|---|---|
| **uv** | Rust製の高速ツール。`pyproject.toml` をベースに依存解決 | `uv.lock` | **速い** | 本プロジェクト推奨。素早い環境構築 |
| **venv（標準）** | Python標準の軽量仮想環境 | `requirements.txt` | 普通 | シンプルに使いたいとき |
| **poetry** | 依存解決と配布まで統合 | `poetry.lock` | 中 | ライブラリ開発・厳密な管理 |
| **conda** | Python以外も含めた環境管理 | `environment.yml` | 中 | GPU・科学計算系 |
| **pipenv** | pipとvenvを統合 | `Pipfile.lock` | 中 | Webアプリ開発 |

---

## venv を使うときの最低限の操作

何らかの理由で `uv` ではなく `venv` を使う場合、以下の操作だけ覚えておけば困りません。

### 作成

```bash
python3 -m venv .venv
```

### 有効化

```bash
source .venv/bin/activate
```

有効化に成功すると、プロンプトの先頭に `(.venv)` と表示されます。

### 無効化

```bash
deactivate
```

### `.gitignore` に追加

```text
.venv/
```

仮想環境のフォルダは **コミットしない** のが原則です。

---

## まとめ

* 仮想環境はプロジェクトごとにPython環境を独立させる仕組み
* 本プロジェクトでは **`uv`** を使うのが推奨
* どうしても `uv` が使えない環境では `venv` でもOK

---

[参加者マニュアルトップへ](../_index.md)\
[背景知識トップへ](./_index.md)\
[前へ（GitとGitHub）](./about_github.md)\
[次へ（WebSocketとは）](./about_websocket.md)
