#!/usr/bin/env python3
"""大会 1 つ分の data/results/<slug>.yaml を、設定ファイルと集計元ファイルから生成する。

使い方:
    python3 scripts/results/build_contest_yaml.py scripts/results/contests/<slug>.yaml

設定ファイルの書き方は scripts/results/contests/example.yaml と scripts/results/README.md を参照。
勝率は success ログから本スクリプト内で集計し (winrate.py)、ゲーム指標は calculate_meta の
team_summary.csv、LLM 相対評価は aiwolf-nlp-llm-judge の team_aggregation.csv、人手評価は
評価フォームの集計シート (totalling CSV) から読む。表彰は設定ファイルに直接書く。
依存: pyyaml のみ (calculate_meta 等は事前に実行してファイルを用意する)。
"""
import csv, json, re, statistics as st, subprocess, sys
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
SITE = HERE.parent.parent
CRIT6 = ["natural_expression", "contextual_dialogue", "logical_consistency", "action_consistency", "character_consistency", "team_play"]
META_COLS = [("追放されやすさ", "executed"), ("占われやすさ", "divined"), ("守られやすさ", "guarded"),
             ("占い精度", "divine_acc"), ("投票精度_村人陣営", "vote_acc"), ("人狼以外への投票率_狂人", "possessed_avoid")]

def norm_team(name):
    n = re.sub(r"[_-]?\d+[a-z]?$", "", name)
    return n.rstrip("_-") or name

def win_rates(log_dir, names_map):
    out = subprocess.run([sys.executable, str(HERE / "winrate.py"), str(log_dir)], check=True, capture_output=True, text=True).stdout
    wr = json.loads(out)
    rows = []
    for team, v in wr["teams"].items():
        rows.append({"team": names_map.get(team, team), "games": v["games"], "wins": v["wins"], "macro": v["macro"], "micro": v["micro"], "weighted": v["weighted"],
                     "by_role": {r: [x["games"], x["wins"]] for r, x in v["by_role"].items()}})
    return wr, rows

def game_metrics(team_summary_csv, names_map, order):
    by = {}
    for r in csv.DictReader(open(team_summary_csv, encoding="utf-8")):
        t = norm_team(r["team"]); by.setdefault(names_map.get(t, t), []).append(r)
    rows = []
    for team, rs in by.items():
        row = {"team": team}
        if len(rs) == 1:
            for col, key in META_COLS:
                v = rs[0].get(col, "")
                row[key] = round(float(v), 2) if v not in ("", None) else None
        rows.append(row)
    rows.sort(key=lambda r: order.get(r["team"], 999))
    return {"rows": rows}

def llm_judge(csv_paths, models, source, names_map):
    acc = {}
    for pth in csv_paths:
        for r in list(csv.reader(open(pth, encoding="utf-8-sig")))[1:]:
            if not r or not r[0]: continue
            vals = [float(x) for x in r[1:7] if x not in ("", None)]
            if len(vals) >= 5: acc.setdefault(r[0], []).append(vals)
    rows = []
    for team, lst in acc.items():
        n = min(len(v) for v in lst)
        m = [round(st.mean(col), 2) for col in zip(*[v[:n] for v in lst])]
        row = {"team": names_map.get(team, team), **dict(zip(CRIT6[:n], m)), "overall": round(st.mean(m), 2)}
        rows.append(row)
    crits = [c for c in CRIT6 if any(c in r for r in rows)]
    rows.sort(key=lambda r: r["overall"])
    return {"criteria": crits, "rows": rows, "models": models, "posthoc": False, "source": source}

def human_eval(totalling_csv, source, names_map):
    sys.path.insert(0, str(HERE)); import human_totalling
    data, games = human_totalling.parse(totalling_csv)
    crits = [c for c in CRIT6 if any(c in v for v in data.values())]
    rows = sorted(({"team": names_map.get(k, k), **{c: v.get(c) for c in crits}, "overall": v["overall"]} for k, v in data.items()), key=lambda r: r["overall"])
    return {"criteria": crits, "rows": rows, "games": games, "scale": "rank", "source": source}

def main(cfg_path):
    cfg = yaml.safe_load(open(cfg_path, encoding="utf-8"))
    names_map = cfg.get("team_names", {})
    d = {"contest": cfg["contest"], "contest_en": cfg["contest_en"],
         "awards": {"status": "published" if cfg.get("awards") else "pending", "note": cfg["announced"], "note_en": cfg["announced_en"], "items": cfg.get("awards", [])},
         "tracks": []}
    for tr in cfg["tracks"]:
        wr, rows = win_rates(Path(tr["log_dir"]).expanduser(), names_map)
        track = {"id": tr["id"], "name": tr["name"], "name_en": tr["name_en"], "logs": tr["logs_url"], "games": wr["games"], "village_size": wr["village_size"],
                 "win_rates": {"roles": wr["roles"], "rows": rows}}
        order = {r["team"]: i for i, r in enumerate(rows)}
        if tr.get("team_summary_csv"):
            track["game_metrics"] = game_metrics(Path(tr["team_summary_csv"]).expanduser(), names_map, order)
        track["human_eval"] = human_eval(Path(tr["human_totalling_csv"]).expanduser(), tr.get("human_source", ""), names_map) if tr.get("human_totalling_csv") else None
        if tr.get("judge_csvs"):
            track["llm_judge"] = llm_judge([Path(p).expanduser() for p in tr["judge_csvs"]], tr.get("judge_models", []), tr.get("judge_source", ""), names_map)
        d["tracks"].append(track)
    d["availability"] = cfg.get("availability", {})
    d["human_eval_short"], d["human_eval_short_en"] = cfg.get("human_eval_short"), cfg.get("human_eval_short_en")
    out = SITE / "external/aiwolf-nlp-contest-data/contests" / cfg["slug"] / "results.yaml"   # submodule（大会データ）に書く; out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# 生成: scripts/results/build_contest_yaml.py {Path(cfg_path).name}\n")
        yaml.safe_dump(d, f, allow_unicode=True, sort_keys=False, width=200)
    print("wrote", out, "| tracks:", len(d["tracks"]))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(1)
    main(sys.argv[1])
