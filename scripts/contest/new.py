#!/usr/bin/env python3
"""新しい大会のページ一式を、前回大会のページをコピーして作る。

    python3 scripts/contest/new.py <id> --from <前回の id>

    <id> は aiwolf-nlp-contest-data の contests/<id>/contest.yaml が存在すること。
    やること:
      - 作る言語は contest.yaml の site_language（ja / en / both）。英語の雛形が前回大会に無ければ --from-en で指定
      - content/menu/<id>/（と <id>_en/）を前回のディレクトリから複製し、front matter の date を今日に、
        translationKey と内部リンクを新 id に、contest: <id> を追加
      - content/page/<id>.md（と .en.md）を前回のトップページから複製（menu_id: <id>）
      - result.md を生成（results_data: <id>、contest: contest.yaml の name）
      - hugo.yaml の大会メニューを前回のブロックから複製（URL を新 id に）
    本文の文章は書き換えない。続きは scripts/contest/check.py <id> で確認する。
"""
import argparse, datetime, re, sys
from pathlib import Path
import yaml

SITE = Path(__file__).resolve().parents[2]
CONTESTS = SITE / "external/aiwolf-nlp-contest-data/contests"

def menu_dir(cid, en=False):
    """content/menu の中から id に対応するディレクトリ名を返す（大文字小文字の揺れを吸収）"""
    want = cid + ("_en" if en else "")
    for d in (SITE / "content/menu").iterdir():
        if d.is_dir() and d.name.lower() == want:
            return d
    return None

def page_file(cid, en=False):
    """content/page から menu_id が id のトップページを探す"""
    for f in (SITE / "content/page").glob("*.en.md" if en else "*.md"):
        if not en and f.name.endswith(".en.md"):
            continue
        fm = front_matter(f.read_text(encoding="utf-8"))
        if fm.get("menu_id") == cid:
            return f
    return None

def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return yaml.safe_load(m.group(1)) or {} if m else {}

def rewrite(text, old_id, new_id, old_dirs, new_dirs, old_pages, new_pages, today, is_page):
    # front matter
    text = re.sub(r"^date: .*$", f"date: '{today}'", text, count=1, flags=re.M)
    text = text.replace(f"translationKey: menu-{old_id}-", f"translationKey: menu-{new_id}-")
    text = text.replace(f"translationKey: page-{old_id}", f"translationKey: page-{new_id}")
    if is_page:
        text = re.sub(r"^menu_id: .*$", f"menu_id: {new_id}", text, count=1, flags=re.M)
        # 前回大会の公開 URL の固定（url / aliases）は引き継がない。新しいページは /page/<id>/ になる
        text = re.sub(r"^url: .*\n", "", text, count=1, flags=re.M)
        text = re.sub(r"^aliases:\n(?:\s+- .*\n)+|^aliases: .*\n", "", text, count=1, flags=re.M)
    if re.search(r"^contest: ", text, re.M):
        text = re.sub(r"^contest: .*$", f"contest: {new_id}", text, count=1, flags=re.M)
    else:
        text = re.sub(r"^(---\n.*?)\n---\n", lambda m: m.group(1) + f"\ncontest: {new_id}\n---\n", text, count=1, flags=re.S)
    # 内部リンク
    for od, nd in zip(old_dirs, new_dirs):
        if od and nd:
            text = re.sub(rf"/menu/{re.escape(od.name)}(?=[/#)\s])", f"/menu/{nd}", text, flags=re.I)
    for op, np_ in zip(old_pages, new_pages):
        if op and np_:
            text = re.sub(rf"/page/{re.escape(op)}(?=[/#)\s])", f"/page/{np_}", text, flags=re.I)
    return text

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("id"); ap.add_argument("--from", dest="prev", required=True)
    ap.add_argument("--from-en", dest="prev_en", help="英語ページの雛形にする大会（前回大会に英語ページが無いとき。例: inlg_2026）")
    ap.add_argument("--date", help="front matter の date（YYYY-MM-DD。既定は今日）")
    a = ap.parse_args()
    cid, prev = a.id, a.prev
    cy = CONTESTS / cid / "contest.yaml"
    if not cy.exists():
        sys.exit(f"contest.yaml がありません: {cy}\n先に aiwolf-nlp-contest-data に contests/{cid}/contest.yaml を書いてください。")
    contest = yaml.safe_load(cy.read_text(encoding="utf-8"))
    today = (a.date or datetime.date.today().isoformat()) + "T10:00:00+09:00"
    # どの言語のページを作るか: contest.yaml の site_language（ja / en / both）。無ければ前回大会に英語ページがあるかで決める
    lang = contest.get("site_language") or ("both" if menu_dir(prev, en=True) else "ja")
    want = {"ja": lang in ("ja", "both"), "en": lang in ("en", "both")}
    src_id = {"ja": prev, "en": a.prev_en or prev}          # 雛形にする大会（言語ごと）
    if want["en"] and not (menu_dir(src_id["en"], en=True) and page_file(src_id["en"], en=True)):
        sys.exit(f"英語ページの雛形がありません（{src_id['en']} に英語ページが無い）。--from-en <英語ページのある大会 id>（例: inlg_2026）を付けてください")
    if want["ja"] and not (menu_dir(prev) and page_file(prev)):
        sys.exit(f"前回大会 {prev} の日本語ページが見つかりません")
    old_dirs = [menu_dir(src_id["ja"]) if want["ja"] else None, menu_dir(src_id["en"], en=True) if want["en"] else None]
    new_dirs = [cid if want["ja"] else None, cid + "_en" if want["en"] else None]
    old_pages = [page_file(src_id["ja"]) if want["ja"] else None, page_file(src_id["en"], en=True) if want["en"] else None]
    old_page_stems = [p.name.replace(".en.md", "").replace(".md", "") if p else None for p in old_pages]
    new_page_stems = [cid, cid]
    made = []
    # menu ディレクトリ
    for od, nd, L in zip(old_dirs, new_dirs, ("ja", "en")):
        if not od: continue
        dst = SITE / "content/menu" / nd
        if dst.exists():
            sys.exit(f"既にあります: {dst}")
        dst.mkdir(parents=True)
        for f in sorted(od.glob("*.md")):
            text = f.read_text(encoding="utf-8")
            if f.name.startswith("result."):
                fm = front_matter(text)
                en = f.name.endswith(".en.md")
                text = ("---\n" f"date: '{today}'\ndraft: false\ntitle: '{fm.get('title', 'Results & Logs' if en else '結果・ログ')}'\n"
                        f"layout: result\nresult_page: true\nresults_data: {cid}\ncontest: {cid}\n"
                        f"translationKey: menu-{cid}-result\n---\n")
            else:
                text = rewrite(text, src_id[L], cid, old_dirs, new_dirs, old_page_stems, new_page_stems, today, is_page=False)
            (dst / f.name).write_text(text, encoding="utf-8"); made.append(dst / f.name)
    # トップページ
    for op, en, L in zip(old_pages, (False, True), ("ja", "en")):
        if not op: continue
        dst = SITE / "content/page" / (f"{cid}.en.md" if en else f"{cid}.md")
        if dst.exists():
            sys.exit(f"既にあります: {dst}")
        text = rewrite(op.read_text(encoding="utf-8"), src_id[L], cid, old_dirs, new_dirs, old_page_stems, new_page_stems, today, is_page=True)
        dst.write_text(text, encoding="utf-8"); made.append(dst)
    # hugo.yaml のメニュー: 言語ごとに、雛形の大会のブロックを複製して直前に挿入
    hy = SITE / "hugo.yaml"; lines = hy.read_text(encoding="utf-8").split("\n"); out = []; i = 0; inserted = 0; cur_lang = None
    while i < len(lines):
        line = lines[i]
        m_lang = re.match(r"^  (ja|en):\s*$", line)
        if m_lang: cur_lang = m_lang.group(1)
        if cur_lang and want[cur_lang] and re.match(rf"^      {re.escape(src_id[cur_lang])}:\s*$", line):
            j = i + 1
            while j < len(lines) and (lines[j].startswith("        ") or lines[j].strip() == "" or lines[j].lstrip().startswith("#")):
                if lines[j].strip() == "" or (lines[j].startswith("      ") and not lines[j].startswith("        ") and not lines[j].lstrip().startswith("#")):
                    break
                j += 1
            block = lines[i:j]
            new_block = [f"      {cid}:"]
            for b in block[1:]:
                b2 = b
                for od, nd in zip(old_dirs, new_dirs):
                    if od and nd: b2 = re.sub(rf"/menu/{re.escape(od.name)}(?=[/\s]|$)", f"/menu/{nd}", b2, flags=re.I)
                for ops, nps in zip(old_page_stems, new_page_stems):
                    if ops: b2 = re.sub(rf"/page/{re.escape(ops)}\b", f"/page/{nps}", b2, flags=re.I)
                new_block.append(b2)
            out.extend(new_block); out.extend(block); i = j; inserted += 1; continue
        out.append(line); i += 1
    hy.write_text("\n".join(out), encoding="utf-8")
    print(f"作成: {len(made)} ファイル、hugo.yaml のメニュー {inserted} ブロック")
    for m in made: print("  ", m.relative_to(SITE))
    print("\n次にやること:")
    print(f"  1. 本文を今回の内容に書き直す（日程・フォーム・役職・試合数・会場はショートコードに置き換える）")
    print(f"  2. python3 scripts/contest/check.py {cid} --from {prev} で直し忘れを確認する")
    print(f"  3. hugo server -D で /page/{cid} と /menu/{cid}/ を確認する")

if __name__ == "__main__":
    main()
