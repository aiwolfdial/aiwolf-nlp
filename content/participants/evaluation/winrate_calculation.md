---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: 'winrate計算方法'
category: participants_guide
---

このページでは、チームの実際の人狼大会で勝率の計算に用いられている計算方法を３つ紹介・解説します。扱う指標は次の 3 つです。

* **Macro**：総勝率（ゲーム**件数で重み付け**した勝率）
* **Micro**：役職勝率の**単純平均**（そのチームが**一度でも担当した役職のみ**平均化）
* **Weighted Micro**：**13人戦の役職配分**（`1,1,1,1,6,3`）で**加重平均**（未観測役職は重みを除外して再正規化）

> この勝率計算はあらかじめ自身のディレクトリにaiwolf-nlp-serverを落として、自身で設定・起動できることを前提としています。

---

## 入力 CSV の仕様

```bash
./aiwolf-nlp-server-linux-amd64 -c ./default5.yml -a
./aiwolf-nlp-server-linux-amd64 -c ./default13.yml -a
```

でサーバからゲームの結果を取得します。

次に上で取得した結果からチームごとの **担当回数** と **役職別勝率（%）** をcsv形式にまとめなおします。列は以下の並びを厳守してください。

```csv
Team,BODYGUARD,MEDIUM,POSSESSED,SEER,VILLAGER,WEREWOLF,
BODYGUARD (%),MEDIUM (%),POSSESSED (%),SEER (%),VILLAGER (%),WEREWOLF (%),TOTAL
```

* `Team`：チーム名
* 各役職列（整数）：そのチームが**その役職を担当した回数**
* 各役職（%）列（小数/百分率）：その役職担当時の**勝率（%）**
* `TOTAL`：そのチームが参加した**総ゲーム数**

### サンプル行

```csv
Team,BODYGUARD,MEDIUM,POSSESSED,SEER,VILLAGER,WEREWOLF,BODYGUARD (%),MEDIUM (%),POSSESSED (%),SEER (%),VILLAGER (%),WEREWOLF (%),TOTAL
kanolab,12,10,15,15,90,45,50.0,40.0,46.7,53.3,55.6,44.4,187
```

> 役職の勝率（%）は、たとえば「村人を 90 回担当して 50 回勝利」なら **55.6%** のように事前集計しておきます。

---

## 出力イメージ

入力 CSV に 3 指標を付け足して、次のような形で出力します。

```csv
Team, ... ,TOTAL,Macro (%),Micro (%),Weighted Micro (%)
kanolab, ... ,187,52.31,49.38,50.72
```

> パーセント表記（小数点 2 桁、例：`52.31`）で追記します。

---

## 実際に3種の勝率の計算使用できるPythonコード

> 依存関係：**Python 3.11+**, **pandas**
> インストール例：`pip install pandas`

```python
import pandas as pd
from pathlib import Path
import argparse

# 対象役職と、Weighted Micro 用の 13人戦重み
ROLES = ["BODYGUARD", "MEDIUM", "POSSESSED", "SEER", "VILLAGER", "WEREWOLF"]
WEIGHTS = {"BODYGUARD": 1, "MEDIUM": 1, "POSSESSED": 1, "SEER": 1, "VILLAGER": 6, "WEREWOLF": 3}

def compute_metrics_row(row):
    """1 チーム分の行に対して、Macro / Micro / Weighted Micro を返す"""
    counts = [row[r] for r in ROLES]
    ps = [row[f"{r} (%)"] / 100.0 for r in ROLES]  # 0〜1 に正規化
    observed = [c > 0 for c in counts]

    # Macro = 総勝率（担当回数で重み付け）
    total_counts = sum(counts)
    macro = (sum(c * p for c, p in zip(counts, ps)) / total_counts) if total_counts > 0 else 0.0

    # Micro = 観測あり役職の単純平均
    ps_obs = [p for p, o in zip(ps, observed) if o]
    micro = (sum(ps_obs) / len(ps_obs)) if ps_obs else 0.0

    # Weighted Micro = 13人配分で重み付け（未観測役職は除外し再正規化）
    denom_w = sum(WEIGHTS[r] for r, o in zip(ROLES, observed) if o)
    numer_w = sum(WEIGHTS[r] * p for r, p, o in zip(ROLES, ps, observed) if o)
    wmicro = (numer_w / denom_w) if denom_w > 0 else 0.0

    return pd.Series({
        "Macro (%)": round(macro * 100, 2),
        "Micro (%)": round(micro * 100, 2),
        "Weighted Micro (%)": round(wmicro * 100, 2),
    })

def main():
    ap = argparse.ArgumentParser(description="役職別勝率CSVから Macro / Micro / Weighted Micro を付与して出力します。")
    ap.add_argument("--in", dest="in_path", default="input.csv", help="入力CSVパス（既定: input.csv）")
    ap.add_argument("--out", dest="out_path", default="metrics_out.csv", help="出力CSVパス（既定: metrics_out.csv）")
    args = ap.parse_args()

    script_dir = Path(__file__).resolve().parent

    in_path = Path(args.in_path)
    if not in_path.is_absolute():
        in_path = script_dir / in_path
    if not in_path.exists():
        print(f"ERROR: 入力CSVが見つかりません: {in_path}")
        print("対処: 1) CSVを result.py と同じフォルダに置き 'input.csv' にリネーム")
        print('      2) パスを明示指定: python result.py --in "C:\\full\\path\\to\\your.csv"')
        raise SystemExit(1)

    df = pd.read_csv(in_path)

    # 必要列の存在チェック
    required_cols = (ROLES + [f"{r} (%)" for r in ROLES] + ["TOTAL"])
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print("ERROR: 必要な列が入力CSVにありません:", missing)
        raise SystemExit(1)

    metrics = df.apply(compute_metrics_row, axis=1)
    out = pd.concat([df, metrics], axis=1)

    out_path = Path(args.out_path)
    if not out_path.is_absolute():
        out_path = script_dir / out_path
    out.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"Wrote: {out_path}")

if __name__ == "__main__":
    main()
```

---

## 使い方

### もっとも簡単な実行

```bash
# result.py と同じフォルダに input.csv を置く
python result.py
# => 同じフォルダに metrics_out.csv が出力されます
```

### 入出力パスを指定

```bash
python result.py --in "/absolute/or/relative/path/to/input.csv" --out "./out/metrics.csv"
```

---

以上で勝率の計算方法の解説が完了しました。

---

[参加者マニュアルトップへ](../_index.md)\
[確認・評価トップへ](./_index.md)\
[前へ（ビュアーの使いかた）](./viewer_usage.md)\
[次へ（LLM Judgeの使いかた）](./llm_judge_usage.md)
