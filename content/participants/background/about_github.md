---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: 'GitとGitHub'
category: participants_guide
ShowToc: true
---

## なぜ Git が必要なのか？（目的）

* どのファイルが最新か分からない
* 古い版で上書きしてしまう
* 複数人の変更が衝突して混乱
* いつ・誰が・何を変えたか追えない

**Git** は、こうした課題を解決する **バージョン管理システム** です。

---

## Git の役割と仕組み

**Git** は「ファイルの**変更履歴を記録・管理**する仕組み」（**分散型VCS**）。

* 変更の「**いつ・誰が・何を**」を記録
* いつでも**差し戻し**可能
* 複数人が**並行作業**してからマージできる

---

## GitHub とは？（Git との関係）

* **Git**：ローカルで履歴管理するツール
* **GitHub**：その履歴（リポジトリ）をクラウドで**共有・レビュー・バックアップ**できるサービス

> Git が **仕組み**、GitHub は **場所**。チーム開発にはリモート（GitHub等）がほぼ必須。

---

## Git と GitHub の関係まとめ

| 項目         | 役割   | 置き場所          | できること                             |
| ---------- | ---- | ------------- | --------------------------------- |
| **Git**    | 履歴管理 | 自分のPC（ローカル）   | 変更の記録、ブランチ運用、差し戻し                 |
| **GitHub** | 共有基盤 | インターネット（リモート） | コラボ、PRレビュー、Issue、Actions、自動バックアップ |

---

## 基本用語の解説

**リポジトリ（Repository）**：履歴つきプロジェクト本体。ローカル／リモートの2種
**ブランチ（Branch）**：履歴の分岐（`main` / `feature/*` / `fix/*` など）
**コミット（Commit）**：変更のスナップショットを記録
**ステージ（Stage）**：次のコミットに含める変更の仮置き（`git add`）
**プッシュ（Push）**：ローカル変更をリモートへ送信（`git push`）
**プル（Pull）**：リモートの変更を取得して反映（`git pull`）
**リモート（Remote）**：接続先URLの別名。自分のリポジトリは通常 `origin`、元リポジトリは `upstream`
**クローン（Clone）**：リモートを丸ごと手元に複製（`git clone`）

---

## GitHub でリポジトリを作成する（最初の準備）

1. GitHub にログイン
2. 右上 **「＋」→「New repository」**
3. リポジトリ名（例：`my-project`）を入力
4. Public/Private を選択
5. **Create repository** をクリック
6. 表示された **リポジトリURL** を控える（例：`https://github.com/<you>/my-project.git`）

---

## プロジェクトを管理する2つの始め方

### パターンA：自分の新規プロジェクトから始める

```bash
mkdir my-project
cd my-project
git init
git remote add origin https://github.com/<you>/my-project.git
git remote -v   # 接続確認
```

### パターンB：**Fork中心で始める（推奨）**

オープンソースや大会の**公式リポジトリをベースに開発する**標準的な流れです。

#### **1) GitHubでForkする（UI操作）**

* 元のリポジトリ（例：`aiwolfdial/aiwolf-nlp-agent-llm`）のページで **「Fork」** をクリック
* 自分のアカウント配下に **自分用のリポジトリ（Fork）** が作成されます

  * 以後、**自分のFork = `origin`**、**元リポジトリ = `upstream`** として扱います

#### **2) 自分のForkをクローンする**

```bash
git clone https://github.com/<you>/<repo>.git
cd <repo>
git remote -v    # origin は自分のForkを指しているはず
```

#### **3) 元リポジトリを upstream に登録**

```bash
git remote add upstream https://github.com/<owner>/<repo>.git
git remote -v
# origin  -> https://github.com/<you>/<repo>.git   (自分のFork)
# upstream-> https://github.com/<owner>/<repo>.git (公式/元)
```

#### **4) 作業用ブランチを切る**

```bash
git switch -c feature/add-new-logic   # or: git checkout -b feature/add-new-logic
```

#### **5) 変更 → コミット → 自分のForkへプッシュ**

```bash
# 変更する
git add .
git commit -m "feat: add new logic"

# 自分のFork（origin）へ送る
git push -u origin feature/add-new-logic
```

#### **6) Pull Request（PR）を作成**

* GitHub上で自分のForkの `feature/*` ブランチから、**upstream の `main`** へ PR を作成
* レビューを受けてマージされると、公式に取り込まれます

#### **7) 公式の更新を取り込む（定期的な同期）**

```bash
git fetch upstream
git switch main
git merge upstream/main   # もしくは: git rebase upstream/main
git push origin main
```

> **ポイント**
>
> * 直接 `upstream` に push はできません（権限なし）。**常に Fork → PR** で貢献します。
> * `origin` は **自分のFork**、`upstream` は **公式**。この二段構えで「開発」と「同期」を分担できます。

---

## 作業の基本フロー（共通）

1. 変更状況を確認

   ```bash
   git status
   ```

2. 変更をステージ

   ```bash
   git add .
   ```

   > `.env` など秘密情報を誤って含めないように。後述の `.gitignore` で除外設定を。

3. 変更を記録（コミット）

   ```bash
   git commit -m "fix: バグ修正"
   ```

4. リモートへ反映

   ```bash
   git push origin <branch>
   ```

**基本サイクル**：`編集 → git add → git commit → git push`（※ `.gitignore` で除外管理）

---

## .gitignore

**定義**：Git に「**追跡しないファイル**」を指示する設定ファイル。
**目的**：個人設定・秘密情報・ビルド成果物・一時ファイル等を履歴から除外する。

よく入れる例：

| 種類       | 例                                  | 理由              |
| -------- | ---------------------------------- | --------------- |
| 環境変数・秘密鍵 | `.env`                             | セキュリティリスク（公開NG） |
| ローカル設定   | `.vscode/`, `.idea/`               | 個人環境依存で共有不要     |
| 生成物      | `dist/`, `build/`, `node_modules/` | 自動生成で履歴不要       |
| OSごみ     | `.DS_Store`, `Thumbs.db`           | キャッシュ不要         |
| ログ       | `*.log`                            | デバッグ用で履歴に不要     |

---

以上で **Git / GitHub** の説明を完了します。

---

[参加者マニュアルトップへ](../_index.md)\
[背景知識トップへ](./_index.md)\
[前へ（WSLとは）](./about_wsl.md)\
[次へ（仮想環境とは）](./virtual_env.md)
