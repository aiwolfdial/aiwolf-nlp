---
date: '2026-04-20T14:00:00+09:00'
draft: false
title: '勝率の計算方法'
category: participants_guide
---

このページでは、大会で使われている勝率の計算方法を紹介します。

「勝った試合の数 ÷ 全試合数」というシンプルな勝率だけでは、**担当した役職の偏り** を反映できません。
そこで大会では、次の3つの指標を組み合わせて評価します。

| 指標 | 考え方 |
|---|---|
| **Macro** | 全試合を通した総勝率（担当試合数で重み付け） |
| **Micro** | 役職ごとの勝率を、単純に平均した値 |
| **Weighted Micro** | 役職ごとの勝率を、役職配分（例：13人戦の比率）で加重平均した値 |

---

## それぞれの指標の意味

### Macro（総勝率）

「勝った試合 ÷ 全試合」に近い、もっとも素直な勝率です。
担当した役職が多ければ、それだけ分母も大きくなります。

### Micro（役職平均）

村人・人狼・占い師などの役職ごとの勝率をそれぞれ計算し、それらの **単純平均** を取ります。
村人ばかり当たって勝率が高くなっている人と、すべての役職をバランスよく担当している人を比較しやすくなります。

### Weighted Micro（加重平均）

Micro と同じ考え方ですが、**役職配分による加重** をかけます。下のスクリプト例では、すべての役職が登場する **13人戦の配分**（`村人6 / 人狼3 / 狂人1 / 占い師1 / 霊媒師1 / 騎士1`）を採用していますが、評価したい大会のトラック構成に合わせて重みを変えても構いません。
これにより、「実際の大会でよく当たる役職」を重く見た評価ができます。

---

## 入力データの形

役職別の担当回数と勝率（%）を、次のようなCSVにまとめます。

```csv
Team,BODYGUARD,MEDIUM,POSSESSED,SEER,VILLAGER,WEREWOLF,BODYGUARD (%),MEDIUM (%),POSSESSED (%),SEER (%),VILLAGER (%),WEREWOLF (%),TOTAL
kanolab,12,10,15,15,90,45,50.0,40.0,46.7,53.3,55.6,44.4,187
```

* **各役職の列**：その役職を担当した **回数**
* **各役職（%）の列**：その役職のときの **勝率（%）**
* **TOTAL**：そのチームが参加した総ゲーム数

---

## 計算用のPythonスクリプト

以下のスクリプトを使うと、入力CSVに3つの指標を追記した出力CSVが作れます。
`pandas` が必要なので、あらかじめ `pip install pandas`（または `uv pip install pandas`）しておいてください。

```python
import pandas as pd
from pathlib import Path
import argparse

ROLES = ["BODYGUARD", "MEDIUM", "POSSESSED", "SEER", "VILLAGER", "WEREWOLF"]
WEIGHTS = {"BODYGUARD": 1, "MEDIUM": 1, "POSSESSED": 1, "SEER": 1, "VILLAGER": 6, "WEREWOLF": 3}


def compute_metrics(row):
    counts = [row[r] for r in ROLES]
    ps = [row[f"{r} (%)"] / 100.0 for r in ROLES]
    observed = [c > 0 for c in counts]

    total = sum(counts)
    macro = sum(c * p for c, p in zip(counts, ps)) / total if total else 0.0

    ps_obs = [p for p, o in zip(ps, observed) if o]
    micro = sum(ps_obs) / len(ps_obs) if ps_obs else 0.0

    denom = sum(WEIGHTS[r] for r, o in zip(ROLES, observed) if o)
    numer = sum(WEIGHTS[r] * p for r, p, o in zip(ROLES, ps, observed) if o)
    wmicro = numer / denom if denom else 0.0

    return pd.Series({
        "Macro (%)": round(macro * 100, 2),
        "Micro (%)": round(micro * 100, 2),
        "Weighted Micro (%)": round(wmicro * 100, 2),
    })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", default="input.csv")
    ap.add_argument("--out", dest="out_path", default="metrics_out.csv")
    args = ap.parse_args()

    df = pd.read_csv(args.in_path)
    metrics = df.apply(compute_metrics, axis=1)
    pd.concat([df, metrics], axis=1).to_csv(args.out_path, index=False, encoding="utf-8-sig")
    print(f"Wrote: {args.out_path}")


if __name__ == "__main__":
    main()
```

---

## 使い方

```bash
# 同じフォルダに input.csv を置いた場合
python result.py

# パスを指定する場合
python result.py --in path/to/input.csv --out path/to/output.csv
```

出力CSVの末尾に、`Macro (%)` / `Micro (%)` / `Weighted Micro (%)` の列が追加されます。

---

## 実際の集計フロー（参考）

1. ローカルサーバでたくさん対戦してログを集める
2. `.json` ログや自分の集計ツールで、役職ごとの担当回数・勝率を算出する
3. それをCSVにまとめて、このスクリプトに通す
4. 3つの指標を見比べて、得意・苦手な役職を把握する

---

[参加者マニュアルトップへ](../_index.md)\
[確認・評価トップへ](./_index.md)\
[前へ（ビュアーの使い方）](./viewer_usage.md)\
[次へ（LLM Judgeの使い方）](./llm_judge_usage.md)
