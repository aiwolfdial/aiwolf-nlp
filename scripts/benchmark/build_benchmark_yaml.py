#!/usr/bin/env python3
"""ベンチマークタブのデータ data/benchmark/{agents,judges}.yaml を、aiwolf-benchmark と aiwolf-judge-bench の集計から生成する。

使い方:
    python3 scripts/benchmark/build_benchmark_yaml.py

読む場所（既定。環境変数で変えられる）:
    AIWOLF_BENCHMARK  ~/pri/aiwolf-benchmark       runs/season1/report/by_model.csv（試合数・勝率）
    AIWOLF_JUDGE_BENCH ~/pri/aiwolf-judge-bench    results/season1/scores_ensemble.csv（相対評価の平均順位）
                                                   results/fair/summary.csv, results/fair/noninferiority.csv（judge と人手の一致）
                                                   results/count_final/summary.csv（件数 judge。あれば）
依存: pyyaml のみ。
"""
import csv, os
from pathlib import Path
import yaml

SITE = Path(__file__).resolve().parents[2]
BM = Path(os.environ.get("AIWOLF_BENCHMARK", Path.home() / "pri/aiwolf-benchmark"))
JB = Path(os.environ.get("AIWOLF_JUDGE_BENCH", Path.home() / "pri/aiwolf-judge-bench"))


def rows(p):
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def agents():
    by_model = {r["model"]: r for r in rows(BM / "runs/season1/report/by_model.csv")}
    out = []
    for r in rows(JB / "results/season1/scores_ensemble.csv"):
        m = r["model"]; b = by_model.get(m, {})
        out.append({
            "model": m, "rank": int(r["順位"]),
            "mean_rank": round(float(r["ens"]), 2), "se": round(float(r["ens_se"]), 2),
            "by_judge": {"gemma-4-31b": round(float(r["gemma-4-31b-nows"]), 2), "qwen3_8-27b": round(float(r["qwen3_8-27b"]), 2)},
            "games": int(b.get("games", 0) or 0), "win_rate": round(float(b.get("win_rate", 0) or 0), 2),
        })
    return {
        "season": "season1",
        "rules": "INLG 2026 国際大会と同じ 5 人村・英語・ターン式（発言 4 回/日、125 文字/発言）",
        "rules_en": "Same rules as the INLG 2026 international contest: 5-player village, English, turn-based (4 talks per day, 125 characters per talk)",
        "games": max((a["games"] for a in out), default=0),
        "n_models": len(out),
        "judges": ["gemma-4-31b", "qwen3_8-27b"],
        "models": out,
    }


def judges():
    summary = {r["model"]: r for r in rows(JB / "results/fair/summary.csv") if r["run"] == "en"}
    noninf = {r["model"]: r for r in rows(JB / "results/fair/noninferiority.csv") if r["run"] == "en"}
    rel = []
    for m, r in summary.items():
        n = noninf.get(m, {})
        rel.append({
            "model": m, "logs": int(r["logs"]),
            "judge_rho": round(float(r["judge_vs_others"]), 2), "human_rho": round(float(r["human_vs_others"]), 2),
            "diff": round(float(r["diff"]), 2),
            "ci_low": round(float(n["ci_low"]), 2) if n else None, "ci_high": round(float(n["ci_high"]), 2) if n else None,
            "verdict": n.get("verdict", ""),
        })
    rel.sort(key=lambda x: -x["judge_rho"])
    cnt = []
    p = JB / "results/count_final/summary.csv"
    if p.exists():
        for r in rows(p):
            cnt.append({k: (round(float(v), 2) if k not in ("model", "verdict") and v not in ("", None) else v) for k, v in r.items()})
    return {"bench": {"tracks": 7, "logs": 88, "contests": ["2026 春季国内大会（5 人村・9 人村・いつでも発話）", "INLG 2025（5 人村・13 人村）", "2025 春季国内大会（13 人村）", "2024 冬季国内大会"]},
            "relative": rel, "count": cnt}


if __name__ == "__main__":
    for name, data in (("agents", agents()), ("judges", judges())):
        p = SITE / "data/benchmark" / f"{name}.yaml"
        p.write_text("# 自動生成: scripts/benchmark/build_benchmark_yaml.py\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        print(p, "ok")
