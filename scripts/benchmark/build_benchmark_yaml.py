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
    return {"bench": {"tracks": 7, "logs": 88, "contests": ["2026 春季国内大会（5 人村・9 人村・いつでも発話）", "INLG 2025（5 人村・13 人村）", "2025 春季国内大会（13 人村）", "2024 冬季国内大会"]},
            "relative": rel}


def count():
    """カウントジャッジ: 人手評価との一致（judge-bench の results/count_final/summary.csv。無ければ空）と、season1 への適用結果。"""
    bench = []
    p = JB / "results/count_final/summary.csv"
    if p.exists():
        for r in rows(p):
            bench.append({k: (round(float(v), 2) if k not in ("model", "verdict") and _isnum(v) else v) for k, v in r.items()})
    by_track = []
    p = JB / "results/count_final/by_track.csv"
    if p.exists():
        for r in rows(p):
            by_track.append({"model": r["model"], "track": r["track"], "ded": round(float(r["ded"]), 2), "add": round(float(r["add"]), 2), "net": round(float(r["net"]), 2)})
    ens = {r["model"]: float(r["ens"]) for r in rows(JB / "results/season1/scores_ensemble.csv")}
    seasons = []
    for p in sorted((BM / "runs/season1/report").glob("count_judge_*.csv")):
        judge = p.stem[len("count_judge_"):]
        ms = []
        for r in rows(p):
            ms.append({"model": r["model"], "rank": int(r["rank"]), "games": int(r["games"]), "deduction": round(float(r["deduction"]), 2), "addition": round(float(r["addition"]), 2), "net": round(float(r["net"]), 2),
                       **{f"net_{a}": round(float(r.get(f"net_{a}", 0) or 0), 2) for a in "ABCDE"}})
        ms.sort(key=lambda x: x["rank"])
        rho = _spearman([-m["net"] for m in ms], [ens.get(m["model"]) for m in ms])
        seasons.append({"judge": judge, "models": ms, "rho_vs_relative": rho})
    return {"season": "season1", "bench": bench, "by_track": by_track, "seasons": seasons}


def _spearman(a, b):
    """同順位は平均順位。n < 3 なら None。"""
    def ranks(x):
        order = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0] * len(x); i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and x[order[j + 1]] == x[order[i]]: j += 1
            for k in range(i, j + 1): r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if len(pairs) < 3: return None
    ra, rb = ranks([x for x, _ in pairs]), ranks([y for _, y in pairs]); n = len(pairs); ma = mb = (n + 1) / 2
    cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb)); va = sum((x - ma) ** 2 for x in ra); vb = sum((y - mb) ** 2 for y in rb)
    return round(cov / (va * vb) ** 0.5, 2) if va and vb else None


def game():
    """ゲームスコア（scores.yaml）とレビュー（review.yaml）: calculate_meta の陣営別集計（期待値比）と scripts/interaction.py の相互関係。"""
    meta = BM / "runs/season1/report/meta"; inter = BM / "runs/season1/report/interaction"
    camp = rows(meta / "team_by_camp.csv"); summ = {r["team"]: r for r in rows(meta / "team_summary.csv")}
    ens = {r["model"]: r for r in rows(JB / "results/season1/scores_ensemble.csv")}
    by = {}
    for r in camp:
        t = r["team"]; d = by.setdefault(t, {})
        f = lambda a, b: round(float(r[a]) / float(r[b]), 2) if float(r[b] or 0) > 0 else None
        if r["camp"] == "VILLAGER":
            d["suspected"] = f("voted_recv", "voted_exp"); d["vote_accuracy"] = f("vote_to_wolf", "vote_to_wolf_exp")
    models = []
    for m, e in ens.items():
        d = by.get(m, {})
        models.append({"model": m, "rank": int(e["順位"]), "mean_rank": round(float(e["ens"]), 2),
                       "vote_accuracy": d.get("vote_accuracy"), "suspected": d.get("suspected"),
                       "win_rate": round(float(summ.get(m, {}).get("勝率_macro", 0) or 0), 2)})
    models.sort(key=lambda x: x["rank"])
    def table(name):
        out = []
        with open(inter / name, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                out.append({k: (round(float(v), 2) if v not in ("", None) and k not in ("ファミリー",) and _isnum(v) else v) for k, v in r.items()})
        return out
    tiers = ["上位", "中位", "下位"]
    fam = [r for r in table("family_bias.csv") if r["期待票数"] and float(r["期待票数"]) >= 10]
    comp = table("top_suspected_by_table.csv")
    scores = {"season": "season1", "models": models}
    nz = lambda v: v if _isnum(v) else None
    review = {"season": "season1", "tiers": tiers,
            "family_bias": [{"family": r["ファミリー"], "models": r["モデル数"], "vote_ratio": r["誤投票で同ファミリーを選ぶ比"], "vote_expected": r["期待票数"], "attack_ratio": r["襲撃で同ファミリーを選ぶ比"], "attack_expected": r["期待襲撃数"]} for r in fam],
            "by_table": [{"n_bottom": int(r["卓の下位層の人数"]), "games": int(r["試合数"]), "votes": int(r["村人陣営の票数"]), "wrong_rate": nz(r["誤投票率"])} for r in comp]}
    return scores, review


def _isnum(v):
    try: float(v); return True
    except (TypeError, ValueError): return False


if __name__ == "__main__":
    scores, review = game()
    for name, data in (("agents", agents()), ("judges", judges()), ("count", count()), ("scores", scores), ("review", review)):
        p = SITE / "data/benchmark" / f"{name}.yaml"
        p.write_text("# 自動生成: scripts/benchmark/build_benchmark_yaml.py\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        print(p, "ok")
