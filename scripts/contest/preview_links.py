#!/usr/bin/env python3
"""変わった大会のプレビューの URL を出す（sync.sh から呼ぶ）。

    python3 scripts/contest/preview_links.py <前の contest-data のコミット> <今のコミット>

このリポジトリで動いている hugo server を探して、その baseURL で URL を作る。動いていなければ起動コマンドを出す。
"""
import re, subprocess, sys
from pathlib import Path
import yaml

SITE = Path(__file__).resolve().parents[2]
DATA = SITE / "external/aiwolf-nlp-contest-data"

def changed_contests(old, new):
    out = subprocess.run(["git", "-C", str(DATA), "diff", "--name-only", old, new, "--", "contests"], capture_output=True, text=True).stdout.split()
    return sorted({p.split("/")[1] for p in out if p.count("/") >= 2 and not p.split("/")[1].startswith("_")})

def running_base():
    """このサイトのディレクトリで動いている hugo server の baseURL"""
    for pid in subprocess.run(["pgrep", "-u", str(Path.home().owner()), "-x", "hugo"], capture_output=True, text=True).stdout.split():
        try:
            cwd = Path(f"/proc/{pid}/cwd").resolve()
            args = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
        except OSError:
            continue
        if cwd != SITE or b"server" not in args: continue
        args = [a.decode() for a in args]
        for i, a in enumerate(args):
            if a in ("--baseURL", "-b") and i + 1 < len(args): return args[i + 1].rstrip("/") + "/"
            if a.startswith("--baseURL="): return a.split("=", 1)[1].rstrip("/") + "/"
        port = next((args[i + 1] for i, a in enumerate(args) if a in ("--port", "-p") and i + 1 < len(args)), "1313")
        return f"http://localhost:{port}/aiwolf-nlp/"
    return None

def page_paths(cid):
    """トップページの URL のパス（ja / en）。front matter の url があればそれ"""
    out = []
    for f in sorted((SITE / "content/page").glob("*.md")):
        m = re.match(r"^---\n(.*?)\n---\n", f.read_text(encoding="utf-8"), re.S)
        fm = yaml.safe_load(m.group(1)) if m else {}
        if fm.get("contest") != cid and fm.get("menu_id") != cid: continue
        en = f.name.endswith(".en.md")
        path = (fm.get("url") or f"/page/{f.name.replace('.en.md', '').replace('.md', '')}/").lstrip("/")
        out.append(("en/" if en else "") + path)
    return out

def main():
    old, new = sys.argv[1], sys.argv[2]
    ids = changed_contests(old, new)
    if not ids: return
    base = running_base()
    print("\n変わった大会:")
    for cid in ids:
        paths = page_paths(cid)
        if not paths:
            print(f"  {cid}: サイトにページがまだありません（python3 scripts/contest/new.py {cid} --from <前回の id>）"); continue
        for p in paths: print(f"  {cid}: {(base or 'http://localhost:1313/aiwolf-nlp/') + p}")
    if not base:
        print("\nプレビューのサーバが動いていません。起動してから上の URL を開いてください:\n"
              "  hugo server -D --port 1313 --baseURL http://localhost:1313/aiwolf-nlp/ --appendPort=false --poll 700ms")

if __name__ == "__main__":
    main()
