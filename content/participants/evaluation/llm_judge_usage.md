---
date: '2026-04-26T14:00:00+09:00'
draft: false
title: 'LLM Judgeの使い方'
category: participants_guide
---

**AIWolf NLP LLM Judge** は、ゲームログをLLMに読ませて、発話の質やチームワークなどを **項目別にランキング** してくれるツールです。
大会の主観評価で実際に使われているリポジトリで、参加者も同じツールを **手元で動かして自分のエージェントを評価できます**。

* リポジトリ：[aiwolfdial/aiwolf-nlp-llm-judge](https://github.com/aiwolfdial/aiwolf-nlp-llm-judge)

> **対応形式と使い方の方針**：本リポジトリは大会で評価対象となるトラックに合わせて、評価基準・プロンプト・対応人数の設定が随時更新されます。
> 自分のエージェント評価に使いたい場合は、**リポジトリを clone か fork** して、評価したいログのトラック・人数・評価項目に合わせて `config/settings.yaml` や `config/evaluation_criteria.yaml` を **適宜書き換えてからご利用ください**。
> 本ページでは、リポジトリで現在公開されている標準的なフローを説明します。

このページでは、LLM Judge の導入から実行・結果確認までを順番に説明します。

---

## 事前に必要なもの

* **Python 3.11 以上**
* **OpenAI API キー**（`OPENAI_API_KEY` を環境変数か `.env` に設定）
* **評価したいゲームログ（`.log`）** と **同名のキャラクター情報（`.json`）**

> `.log` は、サーバを起動したフォルダの `log/game/` に生成されたものをそのまま使えます。
> `.json` はキャラクター情報用のファイルで、`.log` と **同じベース名**（拡張子だけ違う）にそろえます。

---

## インストール

本プロジェクトは `uv` を前提としています。

```bash
# uv をまだ入れていなければ
pip install uv

# リポジトリを取得
git clone https://github.com/aiwolfdial/aiwolf-nlp-llm-judge.git
cd aiwolf-nlp-llm-judge

# 依存関係のインストール
uv sync
```

`uv` が使えない環境では、代わりに `pip` で `pyproject.toml` の依存関係をインストールしてください。

---

## データを配置する

次のような構成で入力ファイルを置きます。

```text
aiwolf-nlp-llm-judge/
└── data/
    ├── input/
    │   ├── log/     # .log ファイルをここに置く
    │   └── json/    # .log と同じベース名の .json をここに置く
    └── output/      # 評価結果が自動で書き出される
```

たとえば次のように配置します。

```bash
mkdir -p data/input/log data/input/json
cp ~/aiwolfdial/aiwolf-nlp-game-logs/log/game/*.log data/input/log/
# .json も data/input/json/ に同名で配置する
```

> **重要**：`.log` と `.json` のベース名（拡張子を除いた部分）が一致していないと評価できません。

---

## 設定ファイル

### メイン設定：`config/settings.yaml`

```yaml
path:
  env: config/.env                              # .envファイルのパス
  evaluation_criteria: config/evaluation_criteria.yaml

llm:
  prompt_yml: config/prompts.yaml               # プロンプト定義ファイル
  model: "gpt-4o"                               # 使うLLMモデル

game:
  format: "main_match"                          # main_match または self_match
  player_count: 13                              # ログの人数に合わせる（リポジトリの対応状況に依存）

processing:
  input_dir: "data/input"                       # 入力ディレクトリ
  output_dir: "data/output"                     # 出力ディレクトリ
  encoding: "utf-8"
  max_workers: 4                                # ゲーム間並列処理数（プロセス）
  evaluation_workers: 8                         # 評価基準並列処理数（スレッド）
  max_retries: 5                                # LLMバリデーション失敗時の再試行回数
```

* **`player_count` はログの人数に合わせてください**（5人戦のログなら `5`）。**ただしリポジトリ側で対応設定が用意されているトラックに限られます**。未対応のトラックを評価したい場合は、評価基準ファイルやコードに自分で項目を追加する必要があります。
* 並列数はAPIのレート制限に注意して、最初は小さめから始めましょう。

### 評価基準：`config/evaluation_criteria.yaml`

評価項目はこのファイルで定義されています。
共通項目（全ゲーム共通で評価）と、ゲーム形式別の項目（例：人数によるチームプレイ評価の有無）を組み合わせて指定できます。

> **fork して使う想定**：自分のエージェントの強みを別の観点で評価したい／公式リポジトリにまだ無いトラックの評価をしたい、という場合は、このファイルに評価項目を追加してください。
> プロンプトファイル（`config/prompts.yaml`）と組み合わせて、独自の評価軸を作れます。

---

## APIキーの設定

OpenAI APIキーを環境変数または `.env` に設定します。

```bash
# Linux / macOS / WSL
export OPENAI_API_KEY="sk-..."

# Windows PowerShell
setx OPENAI_API_KEY "sk-..."
```

`.env` を使う場合は、LLM Judge のプロジェクトルートに `.env` を作成してください。

---

## 実行する

### 通常の実行

```bash
uv run python main.py -c config/settings.yaml
```

### デバッグモード（少数のログで動作確認）

```bash
uv run python main.py -c config/settings.yaml --debug
```

### 集計だけ再生成（LLM呼び出しなし）

```bash
uv run python main.py -c config/settings.yaml --regenerate-aggregation
```

> 再集計は、`data/output/` に過去の評価結果が残っているときだけ動きます。
> 集計ロジックを変えたい、チーム集計ファイルだけ作り直したいときに便利です。

---

## 結果の見方

結果は `data/output/` に書き出されます。

### 個別ゲームの評価（JSON）

各ゲームについて、**項目ごとのランキングと理由** が記録されます。

```json
{
  "game_id": "01K3T3XN...",
  "evaluations": {
    "team_play": {
      "rankings": [
        {
          "player_name": "タクミ",
          "team": "kanolab",
          "ranking": 1,
          "reasoning": "仲間との役割分担を明確にしており…"
        }
      ]
    }
  }
}
```

### チーム集計（JSON / CSV）

複数ゲームをまとめた **チームごとの平均値** が出力されます。

> `ranking_type: ordinal` の項目は **順位の平均** なので、**数値が小さいほど良い** という点に注意してください。

---

## おすすめのワークフロー

1. **ログを集める**：`log/game/*.log` を集める
2. **同名の `.json` を用意する**
3. **`player_count` をログに合わせる**
4. **`--debug` で小さく試す**
5. **本番実行して `data/output/` を確認する**
6. **チーム集計を比較して改善ポイントを探す**

---

[参加者マニュアルトップへ](../_index.md)\
[確認・評価トップへ](./_index.md)\
[前へ（勝率の計算方法）](./winrate_calculation.md)\
[次へ（改良・拡張）](../enhancement/_index.md)
