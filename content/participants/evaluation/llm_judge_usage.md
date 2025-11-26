---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: 'LLM Judgeの使いかた'
category: participants_guide
---

**AIWolf NLP LLM Judge** は、ゲームの進行ログ（`.log`）を **生成AI（LLM）** で評価し、**項目別のランキング** や **チーム別の集計** を出力するバッチツールで、5人村、13人村の両方に対応しています。
こちらのページではこのLLM Judgeの使いかたについて解説していきます。

> 参考リポジトリ：`aiwolfdial/aiwolf-nlp-llm-judge`

---

## 事前準備（前提）

* **Python 3.11 以上**
* **OpenAI API キー**（環境変数または `.env` に `OPENAI_API_KEY` を設定）
* **評価したいゲームログ（`.log`）** と **同名のキャラクター情報（`.json`）**

  * 例：`2025-10-12_..._game.log` と `2025-10-12_..._game.json`（拡張子以外が同一名）

> `.log` は **サーバを起動したフォルダ** の `log/game/` に生成されます（詳しくは `evaluation/game_log_guide.md`）。
> `.json` は「キャラクター情報」用のファイルです。**ログと同じファイル名**にして `data/input/json/` に置きます。

---

## インストール

リポジトリを取得し、依存関係をインストールします。
本プロジェクトは **uv** の利用を前提としています。

```bash
# uv が未インストールなら
pip install uv

# リポジトリを取得
git clone https://github.com/aiwolfdial/aiwolf-nlp-llm-judge.git
cd aiwolf-nlp-llm-judge

# 依存関係のインストール
uv sync
```

> `uv` が使えない環境の場合は、プロジェクトのルートにある設定に従って `pip` を用いたインストールを試してください。
> ただし公式手順は `uv sync` 推奨です。

---

## データを配置する（最重要）

以下のディレクトリ構成で **入力** と **出力** を準備します。

```text
aiwolf-nlp-llm-judge/
└── data/
    ├── input/
    │   ├── log/     # ゲームログ (*.log)
    │   └── json/    # キャラクター情報 (*.json)  ← *.log とファイル名（拡張子除く）を合わせる
    └── output/      # 評価結果の出力先（自動生成）
```

### よくある配置例

```bash
# 例：サーバを ~/aiwolfdial/aiwolf-nlp-game-logs で起動した場合
#     生成された .log を Judge 側の data/input/log へコピー
mkdir -p data/input/log data/input/json
cp ~/aiwolfdial/aiwolf-nlp-game-logs/log/game/*.log data/input/log/

# キャラクター情報 .json を data/input/json/ へ
# （*.log と同じファイル名にして保存すること）
# 例：
#   data/input/log/  : 2025-10-12_..._game.log
#   data/input/json/ : 2025-10-12_..._game.json
```

> **重要**：`.log` と `.json` は **同じベース名**（拡張子だけ違う）である必要があります。
> これが一致しないと **評価できません**。

---

## 設定ファイルを確認する

### メイン設定（`config/settings.yaml`）

```yaml
llm:
  model: "gpt-4o"          # 使用するLLMモデル（OpenAI系）

game:
  format: "main_match"     # ゲーム形式（任意の文字列を運用で定義）
  player_count: 13         # プレイヤー数（5 または 13 など、ログに合わせる）

processing:
  max_workers: 4           # 並列処理数（I/Oや前処理）
  evaluation_workers: 8    # LLM評価の並列数（APIレートに注意）
```

* **player_count** は **ログの実態に合わせる**（5人戦のログなら `5`）。
* 並列数はマシン性能・API レートに応じて調整。最初は小さめ（例：`2` / `2`）から。

### 評価基準（`config/evaluation_criteria.yaml`）

```yaml
common_criteria:               # 全ゲーム共通
  - name: "natural_expression"
    description: "発話表現は自然か"
    ranking_type: "ordinal"    # 順位付け型（1 が最上位の想定）
    order: 1

game_specific_criteria:        # 形式固有（例：13人戦）
  13_player:
    - name: "team_play"
      description: "チームプレイができているか"
      ranking_type: "ordinal"
      applicable_games: [13]
      order: 6
```

* **common_criteria** と **game_specific_criteria** を組み合わせて評価します。
* `ranking_type: ordinal` は **順位** での評価（通常は **1 が最上位**）。
* `applicable_games` で該当するプレイヤー数にのみ適用できます。

---

## API キーの設定

**OpenAI API キー** が必要です。以下のどちらかで設定します。

### 方法 A：環境変数で設定（推奨）

```bash
# macOS / Linux
export OPENAI_API_KEY="sk-..."

# Windows PowerShell
setx OPENAI_API_KEY "sk-..."
```

### 方法 B：`.env` に記述

プロジェクトルートに `.env` を作成して、下記を記載します。

```dotenv
OPENAI_API_KEY=sk-...
```

> ※ `.env` の読み込みはプロジェクト側の実装に依存します。環境変数での設定が確実です。
> 既にエージェント側で `.env` をお使いでも、**Judge 用の `.env` は Judge リポジトリに**用意してください。

---

## 実行

### 基本実行

```bash
uv run python main.py -c config/settings.yaml
```

### デバッグモード

```bash
uv run python main.py -c config/settings.yaml --debug
```

### 集計のみ再生成（LLM呼び出しなし）

```bash
uv run python main.py -c config/settings.yaml --regenerate-aggregation
```

> 再集計は、`data/output/` に **既存の個別評価結果（`*_result.json`）** があるときのみ実行されます。
> 「チーム集計ファイルを消してしまった」「集計ロジックだけ変えた」場合に便利です。

---

## 出力結果の見方

出力は `data/output/` に生成されます。

### 個別ゲーム（JSON）

各ゲームの詳細評価。**項目ごとのランキングと理由**が含まれます。

```json
{
  "game_id": "01K3T3XN1SHBHSBHV1JWDDVS7W",
  "game_info": { "format": "main_match", "player_count": 13 },
  "evaluations": {
    "team_play": {
      "rankings": [
        {
          "player_name": "Takumi",
          "team": "sunamelli-b",
          "ranking": 1,
          "reasoning": "優れたチームプレイを実現..."
        }
      ]
    }
  }
}
```

* `ranking`: **順位**（通常 1 が最上位）
* `reasoning`: LLM が出した **根拠説明**（改善のヒントに）

### チーム集計（JSON / CSV）

複数ゲームの結果を **チーム平均** で集計します。

* `team_aggregation.json`

  ```json
  {
    "team_averages": {
      "kanolab": { "発話表現は自然か": 3.9, "文脈を踏まえた対話は自然か": 3.4 }
    },
    "team_sample_counts": {
      "kanolab": { "発話表現は自然か": 10, "文脈を踏まえた対話は自然か": 10 }
    }
  }
  ```text
* `team_aggregation.csv`

  ```csv
  Team,発話表現は自然か,文脈を踏まえた対話は自然か
  kanolab,3.900000,3.400000
  GPTaku,4.200000,3.800000
  ```

> **平均値の解釈**は評価基準に依存します。
> `ranking_type: ordinal` の場合は **順位の平均** になるため、**数値が小さいほど良い**（＝上位）解釈が一般的です。

---

## ワークフローのおすすめ

1. **ログを集める**：`log/game/*.log` をまとめる
2. **キャラ情報を用意**：それぞれに対応する **同名の `.json`** を作成
3. **設定を合わせる**：`player_count`、評価基準、並列数
4. **スモールデータで試走**：`--debug` で 1〜2本のログから確認
5. **本番評価**：全ログを `data/input/` に入れて実行
6. **集計・比較**：`team_aggregation.*` を基に改善ポイントを抽出

---

以上で **LLM Judge の基本的な使い方** は完了です。
まずは少数のログで動作を確認し、評価基準をチーム方針に合わせて調整しながら、
**`team_aggregation.*` を定点観測**して改善サイクルに活かしてください。

---

[参加者マニュアルトップへ](../_index.md)\
[確認・評価トップへ](./_index.md)\
[前へ（winrate計算方法）](./winrate_calculation.md)\
[次へ（人狼知能エージェントの課題点）](../enhancement/improvement_tips.md)
