"""人手評価 totalling CSV → {team: {criterion: mean_rank, 'overall': mean}}
ブロック見出し ('A 発話表現は自然か' など) をグリッド上で探し、その下のログ行 (先頭が 10 桁の数字) を集計する。
見出しと同じ行にチーム名があればそれを、無ければ次行 ('ファイル名' 行)、それも無ければ同じ列範囲の直近ヘッダを使う。"""
import csv, re, statistics as st
CRIT6 = ["natural_expression","contextual_dialogue","logical_consistency","action_consistency","character_consistency","team_play"]

def parse(path):
    rows = [list(r) for r in csv.reader(open(path, encoding="utf-8-sig"))]
    W = max(len(r) for r in rows)
    rows = [r + [""] * (W - len(r)) for r in rows]
    def names_right(r, c):
        out = []
        for x in rows[r][c + 1:]:
            x = x.strip()
            if not x: break
            out.append(x)
        return out
    last_header = {}   # col -> teams
    acc = {}           # team -> crit -> [values]
    logs = set()
    for r in range(len(rows)):
        for c in range(W):
            cell = rows[r][c].strip()
            m = re.match(r"^([A-F])\s", cell)
            if not m: continue
            crit = CRIT6["ABCDEF".index(m.group(1))]
            teams = names_right(r, c)
            if not teams and r + 1 < len(rows) and "ファイル名" in rows[r + 1][c]:
                teams = names_right(r + 1, c)
            if not teams: teams = last_header.get(c, [])
            if not teams: continue
            last_header[c] = teams
            for rr in range(r + 1, len(rows)):
                c0 = rows[rr][c].strip()
                if "ファイル名" in c0: continue
                if re.match(r"^\d{10}", c0): logs.add(c0)
                if not re.match(r"^\d{10}", c0):
                    if c0 == "" and rr > r + 2: break
                    if c0 == "": continue
                    break
                for t, v in zip(teams, rows[rr][c + 1:]):
                    v = v.strip()
                    if v:
                        try: acc.setdefault(t, {}).setdefault(crit, []).append(float(v))
                        except ValueError: pass
    out = {}
    for t, d in acc.items():
        m = {k: round(st.mean(v), 2) for k, v in d.items()}
        m["overall"] = round(st.mean(m.values()), 2); m["n_logs"] = max(len(v) for v in d.values())
        out[t] = m
    return out, len(logs)

if __name__ == "__main__":
    import sys, json
    for p in sys.argv[1:]:
        d, n = parse(p); print("=", p.split("/")[-1], "teams:", len(d), "games:", n)
        for t, v in sorted(d.items(), key=lambda kv: kv[1]["overall"])[:4]: print("  ", t, v)
