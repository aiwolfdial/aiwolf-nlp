#!/usr/bin/env python3
"""大会ページの直し忘れを機械的に拾う。

    python3 scripts/contest/check.py <id> [--from <前回の id>]

確認すること:
  A. 前回大会の名残: 前回 id・前回ディレクトリ名・大会の年以外の西暦が本文に残っていないか
  B. フォーム URL: 本文中の forms.gle / docs.google.com/forms が contest.yaml の form_url と一致するか
  C. 手書きの日付: 本文中の日付らしい文字列が contest.yaml の日程（milestones / venue）に含まれているか
  D. 未記入: 「決まり次第」「未定」「TBD」「TODO」「XX」などの placeholder と、ショートコードが出す【未定】
  E. 日英の対応: _en ディレクトリがある大会で、ja と en のファイルが揃い translationKey が対になっているか
  F. メニュー: hugo.yaml の大会メニュー（ja/en）があり、URL 先のページが存在するか
  G. front matter: 各ページに contest: <id> があるか
終了コード: 問題があれば 1。
"""
import argparse, re, sys
from pathlib import Path
import yaml

SITE = Path(__file__).resolve().parents[2]
CONTESTS = SITE / "external/aiwolf-nlp-contest-data/contests"
PLACEHOLDERS = ["決まり次第", "決定次第", "未定", "TBA", "TBD", "TODO", "XX", "xx/xx", "（仮）"]

def fm_and_body(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m: return {}, text
    return (yaml.safe_load(m.group(1)) or {}), m.group(2)

def strip_comments(body):
    return re.sub(r"<!--.*?-->", "", body, flags=re.S)

def find_menu_dir(cid, en):
    want = cid + ("_en" if en else "")
    for d in (SITE / "content/menu").iterdir():
        if d.is_dir() and d.name.lower() == want: return d
    return None

def find_pages(cid):
    out = []
    for f in (SITE / "content/page").glob("*.md"):
        fm, _ = fm_and_body(f.read_text(encoding="utf-8"))
        if fm.get("menu_id") == cid or fm.get("contest") == cid: out.append(f)
    return out

def contest_dates(c):
    ds = set()
    def add(v):
        if v is None: return
        s = str(v)[:10]; ds.add(s)
    for r in c.get("rounds", []):
        for m in r.get("milestones", []): add(m.get("date")); add(m.get("end"))
    v = c.get("venue", {}) or {}
    add(v.get("start")); add(v.get("end"))
    return ds

def parse_dates(line):
    out = []
    for m in re.finditer(r"(20\d\d)[/年]\s*(\d{1,2})[/月]\s*(\d{1,2})", line):
        out.append(f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}")
    return out

def print_preview(cid):
    """プレビューの URL を出す（動いている hugo server の番号で）"""
    import importlib.util
    sp = importlib.util.spec_from_file_location("preview_links", Path(__file__).with_name("preview_links.py"))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    base = m.running_base() or "http://localhost:1313/aiwolf-nlp/"
    print("\nプレビュー:")
    for p in m.page_paths(cid): print(f"  {base}{p}")
    if not m.running_base():
        print("  （プレビューのサーバが動いていません: hugo server -D --port 1313 --baseURL http://localhost:1313/aiwolf-nlp/ --appendPort=false --poll 700ms）")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("id"); ap.add_argument("--from", dest="prev")
    a = ap.parse_args(); cid = a.id
    cy = CONTESTS / cid / "contest.yaml"
    if not cy.exists(): sys.exit(f"contest.yaml がありません: {cy}")
    c = yaml.safe_load(cy.read_text(encoding="utf-8"))
    years = {d[:4] for d in contest_dates(c) if re.match(r"^20\d\d", d)}
    year = "・".join(sorted(years)) if years else None
    issues = []
    def issue(kind, where, msg): issues.append((kind, where, msg))

    files = []
    for en in (False, True):
        d = find_menu_dir(cid, en)
        if d: files += sorted(d.glob("*.md"))
    files += find_pages(cid)
    if not files: sys.exit(f"{cid} のページが見つかりません")

    prev_tokens = []
    if a.prev:
        prev_tokens.append(a.prev)
        for en in (False, True):
            d = find_menu_dir(a.prev, en)
            if d: prev_tokens.append(d.name)
        for p in find_pages(a.prev): prev_tokens.append(p.name.replace(".en.md", "").replace(".md", ""))
        py = CONTESTS / a.prev / "contest.yaml"
        if py.exists():
            pc = yaml.safe_load(py.read_text(encoding="utf-8"))
            pname, name = str(pc.get("name", "")), str(c.get("name", ""))
            for w in ("春季", "夏季", "秋季", "冬季"):
                if w in pname and w not in name: prev_tokens += [w, w[0] + "に", "年" + w[0], w[0] + "の"]
            pv, v = str((pc.get("venue") or {}).get("name", "")), str((c.get("venue") or {}).get("name", ""))
            for w in re.findall(r"[^\s\d()（）_\-]{2,}", re.sub(r"20\d\d", " ", pv)):
                if w not in v: prev_tokens.append(w)
        if py.exists():
            cur_sp = {s.get("name") for s in c.get("sponsors") or []}
            for s_ in pc.get("sponsors") or []:
                n_ = str(s_.get("name", ""))
                if n_ and n_ not in cur_sp: prev_tokens += [n_, re.sub(r"株式会社|社$", "", n_).strip()]
    prev_tokens = sorted({t for t in prev_tokens if t and len(t) >= 2}, key=len, reverse=True)
    one_round = len(c.get("rounds") or []) <= 1
    lang_words = ["英語で", "(英語)", "（英語）", "English", "/images/en/"] if c.get("language") == "ja" else ["日本語で", "(日本語)", "（日本語）"]
    known = contest_dates(c)
    form = c.get("form_url")

    for f in files:
        rel = f.relative_to(SITE); text = f.read_text(encoding="utf-8")
        fm, body = fm_and_body(text); body = strip_comments(body)
        if fm.get("contest") != cid and fm.get("menu_id") != cid:
            issue("G", rel, f"front matter に contest: {cid} がない")
        created = str(fm.get("date", ""))[:10]
        lines = [f"title: {fm.get('title', '')}"] + body.split("\n")
        for n, line in enumerate(lines):
            where = f"{rel}:{'title' if n == 0 else n}"
            hit = next((t for t in prev_tokens if t.lower() in line.lower()), None)
            if hit: issue("A", where, f"前回の名残 '{hit}': {line.strip()[:80]}")
            if one_round and re.search(r"[12]次", line): issue("A", where, f"回は 1 つなのに 1次・2次 の記述: {line.strip()[:80]}")
            w_ = next((w for w in lang_words if w in line), None)
            if w_: issue("A", where, f"対戦言語（{c.get('language')}）と違う言語の記述 '{w_}': {line.strip()[:80]}")
            m_news = re.match(r"^\s*[-*]\s*\*\*(20\d\d)/(\d\d)/(\d\d)\*\*", line)
            if m_news and created and f"{m_news.group(1)}-{m_news.group(2)}-{m_news.group(3)}" < created:
                issue("A", where, f"ページを作る前の日付の更新情報（前回大会のもの？）: {line.strip()[:60]}")
            if year:
                for y in set(re.findall(r"20\d\d", line)):
                    if y not in years and not re.search(r"20\d\d/\d\d/\d\d|^\s*[-*]\s*\*\*20\d\d", line):
                        issue("A", where, f"大会の年 {year} 以外の西暦 {y}: {line.strip()[:80]}")
            for u in re.findall(r"https?://(?:forms\.gle|docs\.google\.com/forms)[^\s)]*", line):
                if form and u.rstrip("/") != form.rstrip("/"): issue("B", where, f"フォーム URL が contest.yaml と違う: {u}")
            if not re.match(r"^\s*[-*]\s*\*\*20\d\d/\d\d/\d\d\*\*", line):   # 更新情報の日付は対象外
                for d in parse_dates(line):
                    if d not in known: issue("C", where, f"contest.yaml に無い日付 {d}: {line.strip()[:80]}")
            for ph in PLACEHOLDERS:
                if ph in line: issue("D", where, f"placeholder '{ph}': {line.strip()[:80]}")

    # E. 日英の対応
    dja, den = find_menu_dir(cid, False), find_menu_dir(cid, True)
    if dja and den:
        ja = {f.name: f for f in dja.glob("*.md")}; en = {f.name.replace(".en.md", ".md"): f for f in den.glob("*.en.md")}
        for k in sorted(set(ja) | set(en)):
            if k not in en: issue("E", dja / k, "英語版がない")
            elif k not in ja: issue("E", en[k], "日本語版がない")
            else:
                tj = fm_and_body(ja[k].read_text(encoding="utf-8"))[0].get("translationKey")
                te = fm_and_body(en[k].read_text(encoding="utf-8"))[0].get("translationKey")
                if tj != te: issue("E", ja[k], f"translationKey が対になっていない: ja={tj} en={te}")
    # F. メニュー
    hy = yaml.safe_load((SITE / "hugo.yaml").read_text(encoding="utf-8"))
    for lang in ("ja", "en"):
        menus = (hy.get("languages", {}).get(lang, {}) or {}).get("menu", {}) or {}
        block = menus.get(cid)
        if not block:
            if lang == "ja" or den: issue("F", f"hugo.yaml[{lang}]", f"大会メニュー {cid} がない")
            continue
        for item in block:
            url = item.get("url", "").strip("/")
            parts = url.split("/")
            ok = False
            if parts[0] == "page":
                ok = any(p.name.replace(".en.md", "").replace(".md", "").lower() == parts[1].lower() for p in (SITE / "content/page").glob("*.md"))
            elif parts[0] == "menu" and len(parts) >= 3:
                d = next((d for d in (SITE / "content/menu").iterdir() if d.name.lower() == parts[1].lower()), None)
                ok = bool(d) and any(p.name.split(".")[0] == parts[2] for p in d.glob("*.md"))
            if not ok: issue("F", f"hugo.yaml[{lang}]", f"メニュー '{item.get('name')}' の URL 先が無い: /{url}")

    if not issues:
        print(f"{cid}: 問題なし（{len(files)} ファイル）"); print_preview(cid); return 0
    print(f"{cid}: {len(issues)} 件")
    for kind, where, msg in issues: print(f"  [{kind}] {where}: {msg}")
    print_preview(cid)
    return 1

if __name__ == "__main__":
    sys.exit(main())
