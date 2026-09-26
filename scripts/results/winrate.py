#!/usr/bin/env python3
"""success ログからチーム別勝率を集計する (2024 形式 / 2025 以降形式の両対応)。
使い方: winrate.py LOGDIR [LOGDIR...]  → 標準出力に JSON
出力: {"games": N, "roles": [...], "teams": {team: {"games":..,"wins":..,"macro":..,"micro":..,"weighted":..,
        "by_role": {ROLE: {"games":g,"wins":w,"rate":r}}}}}
定義 (運営マニュアル win_rates.md と同じ):
  macro    = 総勝数 / 総試合数
  micro    = 役職別勝率の単純平均 (担当 0 の役職は除外)
  weighted = 役職別勝率を村の役職構成で加重平均 (未観測役職は重みから除外して再正規化)
"""
import json, re, sys
from collections import defaultdict
from pathlib import Path

COMP = {  # 村サイズ -> 役職構成
    5:  {"VILLAGER": 2, "SEER": 1, "POSSESSED": 1, "WEREWOLF": 1},
    9:  {"VILLAGER": 3, "SEER": 1, "BODYGUARD": 1, "MEDIUM": 1, "POSSESSED": 1, "WEREWOLF": 2},
    13: {"VILLAGER": 6, "SEER": 1, "BODYGUARD": 1, "MEDIUM": 1, "POSSESSED": 1, "WEREWOLF": 3},
}
WOLF_SIDE = {"WEREWOLF", "POSSESSED"}

def team_of(name: str) -> str:
    # kanolab1 / sUper_IL_1 / UECIL_1 / CamelliaDragons1 / agent1h / GPTaku_2 -> チーム名
    n = re.sub(r"[_-]?\d+[a-z]?$", "", name)
    return n.rstrip("_-") or name

def parse(path: Path):
    """(winner, {idx: (role, name)}) を返す。異常なら None"""
    winner = None; roles = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        c = line.rstrip("\n").split(",")
        if len(c) < 2: continue
        if c[1] == "status" and len(c) >= 6:
            roles[c[2]] = (c[3], c[5])   # 最終日の status で上書きされる
        elif c[1] == "result":
            winner = c[-1].strip().upper()
    if winner not in ("WEREWOLF", "VILLAGER") or not roles:
        return None
    return winner, roles

def main(dirs):
    stat = defaultdict(lambda: defaultdict(lambda: [0, 0]))  # team -> role -> [games, wins]
    n_games = 0; sizes = defaultdict(int); skipped = 0
    for d in dirs:
        for f in sorted(Path(d).glob("*.log")):
            r = parse(f)
            if r is None: skipped += 1; continue
            winner, roles = r
            n_games += 1; sizes[len(roles)] += 1
            for idx, (role, name) in roles.items():
                won = (winner == "WEREWOLF") == (role in WOLF_SIDE)
                s = stat[team_of(name)][role]; s[0] += 1; s[1] += int(won)
    size = max(sizes, key=sizes.get)
    comp = COMP.get(size, {})
    teams = {}
    for team, by_role in stat.items():
        g = sum(v[0] for v in by_role.values()); w = sum(v[1] for v in by_role.values())
        rates = {r: v[1] / v[0] for r, v in by_role.items() if v[0]}
        micro = sum(rates.values()) / len(rates) if rates else 0.0
        wsum = sum(comp.get(r, 0) for r in rates)
        weighted = sum(rates[r] * comp.get(r, 0) for r in rates) / wsum if wsum else micro
        teams[team] = {"games": g, "wins": w, "macro": round(w / g, 4), "micro": round(micro, 4), "weighted": round(weighted, 4),
                       "by_role": {r: {"games": v[0], "wins": v[1], "rate": round(v[1] / v[0], 4)} for r, v in sorted(by_role.items())}}
    roles_order = [r for r in ("VILLAGER", "SEER", "BODYGUARD", "MEDIUM", "POSSESSED", "WEREWOLF") if any(r in t["by_role"] for t in teams.values())]
    out = {"games": n_games, "village_size": size, "skipped": skipped, "roles": roles_order,
           "teams": dict(sorted(teams.items(), key=lambda kv: -kv[1]["macro"]))}
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main(sys.argv[1:])
