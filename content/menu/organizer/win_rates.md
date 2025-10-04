---
date: '2025-10-04T14:00:00+09:00'
draft: false
title: 'win_ratesまとめ手順'
category: organizer_guide
---

## win_ratesまとめ手順

<details>
<summary>サーバーからゲームの結果を取得</summary>

```bash
./aiwolf-nlp-server-linux-amd64 -c ./default5.yml -a
./aiwolf-nlp-server-linux-amd64 -c ./default13.yml -a
```

</details>

<details>
<summary>役職ごと、トータルの勝率を計算</summary>

役職ごとの勝率とすべてのゲームでの勝率を計算。csv形式でまとめる。

```csv
Team,BODYGUARD,MEDIUM,POSSESSED,SEER,VILLAGER,WEREWOLF,BODYGUARD (%),MEDIUM (%),POSSESSED (%),SEER (%),VILLAGER (%),WEREWOLF (%),TOTAL
```

の形式でまとめる
</details>

<details>
<summary>Macro, Micro, Weighted Microを計算</summary>

以下のコードを参考。

```python
import pandas as pd
from pathlib import Path
import argparse

計算ルール:
# Macro = 総勝率
# Micro = 役職勝率の単純平均（担当0の役職は除外）
# Weighted Micro = 13人配分(1,1,1,1,6,3)で加重（未観測役職の重みは除外し再正規化）

ROLES = ["BODYGUARD", "MEDIUM", "POSSESSED", "SEER", "VILLAGER", "WEREWOLF"]
WEIGHTS = {"BODYGUARD": 1, "MEDIUM": 1, "POSSESSED": 1, "SEER": 1, "VILLAGER": 6, "WEREWOLF": 3}

def compute_metrics_row(row):
    counts = [row[r] for r in ROLES]
    ps = [row[f"{r} (%)"] / 100.0 for r in ROLES]  # 0〜1 に変換
    observed = [c > 0 for c in counts]

    # Macro: 総勝率 = sum(cnt * p) / sum(cnt)
    total_counts = sum(counts)
    macro = (sum(c * p for c, p in zip(counts, ps)) / total_counts) if total_counts > 0 else 0.0

    # Micro: 観測あり役職の平均
    ps_obs = [p for p, o in zip(ps, observed) if o]
    micro = (sum(ps_obs) / len(ps_obs)) if ps_obs else 0.0

    # Weighted Micro: 観測あり役職だけで重み再正規化
    denom_w = sum(WEIGHTS[r] for r, o in zip(ROLES, observed) if o)
    numer_w = sum(WEIGHTS[r] * p for r, p, o in zip(ROLES, ps, observed) if o)
    wmicro = (numer_w / denom_w) if denom_w > 0 else 0.0

    return pd.Series({
        "Macro (%)": round(macro * 100, 2),
        "Micro (%)": round(micro * 100, 2),
        "Weighted Micro (%)": round(wmicro * 100, 2),
    })

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", default="input.csv", help="入力CSVパス")
    ap.add_argument("--out", dest="out_path", default="metrics_out.csv", help="出力CSVパス")
    args = ap.parse_args()

    script_dir = Path(__file__).resolve().parent

    in_path = Path(args.in_path)
    if not in_path.is_absolute():
        in_path = script_dir / in_path
    if not in_path.exists():
        print(f"ERROR: 入力CSVが見つかりません: {in_path}")
        print("対処: 1) CSVを result.py と同じフォルダに置き 'input.csv' にリネーム")
        print("      2) パスを明示指定: python result.py --in \"C:\\full\\path\\to\\your.csv\"")
        raise SystemExit(1)

    df = pd.read_csv(in_path)

    # 必要列の存在チェック（あると安心）
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

</details>

<details>
<summary>csvデータのアップロード</summary>

[aiwolf-nlp-viewer/static/assets/](https://github.com/aiwolfdial/aiwolf-nlp-viewer/tree/main/static/assets)直下に今大会分の勝率csvファイルを追加する。
</details>
