#!/usr/bin/env python3
"""指定ディレクトリ内の .log のうち「正常終了したゲーム」だけを <dir>/success/ にコピーする。

判定は copy_success_logs.py と同じく最終行の最終カラムが NONE でないこと。加えて
最終行が result 行であることと、ファイル名に _err_/_ERROR を含まないことを要求する
(2024 形式ではエラーが別ファイルに出るため)。
使い方: python3 make_success_dir.py [--recursive] [--dry-run] DIR...
  --recursive : DIR 直下のサブディレクトリ (success 以外) も走査し、DIR/success に集約
  --out PATH  : 出力先を DIR/success の代わりに PATH にする (DIR が書き込めない場合など)
  --prune     : 出力先にある、条件を満たさなくなったファイルを削除する
"""
import shutil, sys
from pathlib import Path

def last_non_empty_line(p: Path):
    try:
        for l in reversed(p.read_text(encoding="utf-8", errors="replace").splitlines()):
            if l.strip():
                return l.strip()
    except Exception as e:
        print(f"[ERROR] {p}: {e}")
    return None

def is_success(p: Path) -> bool:
    n = p.name.lower()
    if "_err_" in n or "_error" in n:
        return False
    l = last_non_empty_line(p)
    if not l:
        return False
    c = l.split(",")
    # 勝者が WEREWOLF / VILLAGER のものだけ (NONE, null, 空 は未決着)
    return len(c) >= 2 and c[1] == "result" and c[-1].strip().upper() in ("WEREWOLF", "VILLAGER")

def main():
    args = sys.argv[1:]
    recursive = "--recursive" in args
    dry = "--dry-run" in args
    prune = "--prune" in args
    out_override = None
    if "--out" in args:
        i = args.index("--out"); out_override = Path(args[i+1]); del args[i:i+2]
    dirs = [Path(a) for a in args if not a.startswith("--")]
    for d in dirs:
        if not d.is_dir():
            print(f"[ERROR] not a dir: {d}"); continue
        out = out_override if out_override else d / "success"
        srcs = []
        for p in sorted(d.rglob("*.log") if recursive else d.glob("*.log")):
            if out in p.parents or out == p.parent:
                continue
            srcs.append(p)
        good = [p for p in srcs if is_success(p)]
        if not dry:
            out.mkdir(exist_ok=True)
            for p in good:
                dst = out / p.name
                if dst.exists() and dst.stat().st_size == p.stat().st_size:
                    continue
                shutil.copy2(p, dst)
        removed = 0
        if prune and out.exists():
            keep = {p.name for p in good}
            for q in out.glob("*.log"):
                if q.name not in keep:
                    removed += 1
                    if not dry: q.unlink()
        have = len(list(out.glob("*.log"))) if out.exists() else 0
        print(f"{d}: logs={len(srcs)} success={len(good)} skipped={len(srcs)-len(good)} -> {out} (now {have} files, pruned {removed}){' [dry-run]' if dry else ''}")

if __name__ == "__main__":
    main()
