"""Compare the deck we generated with the deck the SC actually presented, slide by slide.

Usage:
    python deck_diff.py --generated <built.pptx> [--spec <deck.json>] --presented <presented.pptx>
                        [--deal <name>] [--out <dir>]
    python deck_diff.py --deal-dir <deal folder>          (finds both decks itself; see find_decks)

For every presented slide: kept (as generated), edited (same slide, words changed), library (from the Slide-library),
hand-made (new), plus the generated slides that were dropped and any change of order. For edited slides, the words
removed and added. Writes <out>/deck-review-<deal>-<date>.md and .json (default out: <team root>/Lessons/deck-edits),
so the weekly lessons run can count patterns across deals. Changes nothing else.
"""
import argparse
import datetime
import difflib
import json
import os
import re
import sys

from pptx import Presentation

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "sc-inbox", "scripts"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "sc-deck", "scripts"))
from inbox_scan import slides_of, words  # noqa: E402
from build_deck import team_root  # noqa: E402

KEPT, EDITED = 0.92, 0.45  # word-set similarity thresholds


def sim(a, b):
    wa, wb = words(a), words(b)
    if not wa and not wb:
        return 1.0
    return len(wa & wb) / len(wa | wb) if wa | wb else 0.0


def spec_types(spec_path, n_slides):
    """Slide type per built slide, from deck.json (a library entry expands to its slide count)."""
    if not spec_path or not os.path.isfile(spec_path):
        return ["?"] * n_slides
    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    types = []
    for d in spec["slides"]:
        if d.get("skip"):
            continue
        if d["type"] == "library":
            types += ["library"] * len(d["slides"])
        else:
            types.append(d["type"])
    return types[:n_slides] + ["?"] * max(0, n_slides - len(types))


NOISE = re.compile(r"^(\d{1,3}|shown today|not yet shown|you'll see this today|next time|confidential)$", re.I)


def lines(t):
    """Text lines that carry meaning: no page numbers, part numbers or status chips."""
    return [x.strip() for x in t.split("\n") if x.strip() and not NOISE.match(x.strip())]


def text_changes(gen, pres):
    """Lines removed from the generated slide and lines added on the presented one (fuzzy-paired)."""
    g, p = lines(gen), lines(pres)
    removed, added = [], []
    sm = difflib.SequenceMatcher(a=g, b=p, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op in ("replace", "delete"):
            removed += g[i1:i2]
        if op in ("replace", "insert"):
            added += p[j1:j2]
    return removed, added


def library_index():
    try:
        lib_dir = os.path.join(team_root(), "Slide-library")
    except SystemExit:
        return []
    out = []
    for root, _, files in os.walk(lib_dir):
        for f in files:
            if f.lower().endswith(".pptx") and not f.startswith("~$"):
                rel = os.path.relpath(os.path.join(root, f), lib_dir)
                for s in slides_of(os.path.join(root, f))[0]:
                    out.append((rel, s["slide"], s["text"]))
    return out


def compare(generated, presented, spec=None):
    gen, _ = slides_of(generated)
    pres, _ = slides_of(presented)
    types = spec_types(spec, len(gen))
    for g, t in zip(gen, types):
        g["type"] = t
    lib = library_index()
    used = set()
    rows = []
    for p in pres:
        best, score = None, 0.0
        for g in gen:
            if g["slide"] in used:
                continue
            s = sim(g["text"], p["text"])
            if s > score:
                best, score = g, s
        row = {"presented": p["slide"], "title": (lines(p["text"]) or ["(picture or video only)"])[0][:80]}
        if best and score >= EDITED and p["text"].strip():
            used.add(best["slide"])
            row.update(generated=best["slide"], type=best["type"], similarity=round(score, 2))
            if score >= KEPT:
                row["status"] = "kept"
            else:
                removed, added = text_changes(best["text"], p["text"])
                row.update(status="edited", removed=removed, added=added)
                gt, pt = (lines(best["text"]) or [""])[0], (lines(p["text"]) or [""])[0]
                if gt != pt:
                    row["title_change"] = [gt, pt]
        else:
            lbest, lscore = None, 0.0
            for rel, n, t in lib:
                s = sim(t, p["text"]) if p["text"].strip() else 0.0
                if s > lscore:
                    lbest, lscore = (rel, n), s
            if lbest and lscore >= 0.8:
                row.update(status="library", library="%s #%d" % lbest, similarity=round(lscore, 2))
            else:
                row.update(status="hand-made", text=p["text"][:600])
        rows.append(row)
    dropped = [{"generated": g["slide"], "type": g["type"], "title": (lines(g["text"]) or [""])[0][:80]}
               for g in gen if g["slide"] not in used]
    order = [r["generated"] for r in rows if "generated" in r]
    reordered = order != sorted(order)
    counts = {k: sum(1 for r in rows if r["status"] == k) for k in ("kept", "edited", "library", "hand-made")}
    total = len(rows) or 1
    metrics = {
        "presented_slides": len(rows), "generated_slides": len(gen), **counts, "dropped": len(dropped),
        "reordered": reordered,
        "kit_share": round((counts["kept"] + counts["edited"] + counts["library"]) / total, 2),
        "kept_as_is_share": round(counts["kept"] / total, 2),
    }
    return {"generated": generated, "presented": presented, "spec": spec, "metrics": metrics,
            "slides": rows, "dropped": dropped}


def find_decks(deal_dir):
    """Generated = the 'out' of deal_dir/deck.json. Presented = the newest other .pptx in the deal folder."""
    spec = os.path.join(deal_dir, "deck.json")
    with open(spec, encoding="utf-8") as fh:
        out = json.load(fh).get("out", "deck.pptx")
    gen = os.path.join(deal_dir, out)
    cands = [os.path.join(deal_dir, f) for f in os.listdir(deal_dir)
             if f.lower().endswith(".pptx") and not f.startswith("~$") and f != out]
    if not os.path.isfile(gen) or not cands:
        sys.exit("Need the built deck (%s) and at least one other .pptx in %s" % (out, deal_dir))
    return gen, max(cands, key=os.path.getmtime), spec


def report_md(r, deal):
    m = r["metrics"]
    L = ["# Deck review: %s (%s)" % (deal, datetime.date.today().isoformat()), "",
         "Generated: `%s` · Presented: `%s`" % (os.path.basename(r["generated"]), os.path.basename(r["presented"])), "",
         "| Presented | From the kit | Kept as is | Edited | Library | Hand-made | Generated but dropped | Order changed |",
         "|---|---|---|---|---|---|---|---|",
         "| %d | %d%% | %d | %d | %d | %d | %d | %s |" % (m["presented_slides"], m["kit_share"] * 100, m["kept"], m["edited"],
                                                        m["library"], m["hand-made"], m["dropped"], "yes" if m["reordered"] else "no"),
         "", "## Slide by slide", "", "| # | Status | Type | Title | Detail |", "|---|---|---|---|---|"]
    for s in r["slides"]:
        detail = ""
        if s["status"] == "edited":
            detail = "title: %s → %s; " % tuple(s["title_change"]) if s.get("title_change") else ""
            detail += "%d lines removed, %d added" % (len(s["removed"]), len(s["added"]))
        elif s["status"] == "library":
            detail = s["library"]
        elif s["status"] == "kept":
            detail = "from generated #%d" % s["generated"]
        L.append("| %d | %s | %s | %s | %s |" % (s["presented"], s["status"], s.get("type", "-"),
                                                 s["title"].replace("|", "/"), detail.replace("|", "/")))
    if r["dropped"]:
        L += ["", "## Generated but not presented", ""] + ["- #%d %s: %s" % (d["generated"], d["type"], d["title"]) for d in r["dropped"]]
    edits = [s for s in r["slides"] if s["status"] == "edited"]
    if edits:
        L += ["", "## What changed in edited slides", ""]
        for s in edits:
            L.append("**#%d %s**" % (s["presented"], s["title"]))
            for x in s["removed"][:8]:
                L.append("- removed: %s" % x[:160])
            for x in s["added"][:8]:
                L.append("- added: %s" % x[:160])
            L.append("")
    hand = [s for s in r["slides"] if s["status"] == "hand-made"]
    if hand:
        L += ["", "## Hand-made slides (candidates for new slide types or library)", ""]
        for s in hand:
            L.append("- #%d %s" % (s["presented"], s["title"]))
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--generated")
    ap.add_argument("--presented")
    ap.add_argument("--spec")
    ap.add_argument("--deal-dir")
    ap.add_argument("--deal")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.deal_dir:
        gen, pres, spec = find_decks(a.deal_dir)
        deal = a.deal or os.path.basename(os.path.normpath(a.deal_dir))
    else:
        gen, pres, spec = a.generated, a.presented, a.spec
        deal = a.deal or "deal"
    r = compare(gen, pres, spec)
    out = a.out or os.path.join(team_root(), "Lessons", "deck-edits")
    os.makedirs(out, exist_ok=True)
    stamp = "%s-%s" % (deal, datetime.date.today().isoformat())
    with open(os.path.join(out, "deck-review-%s.json" % stamp), "w", encoding="utf-8") as fh:
        json.dump(dict(r, deal=deal), fh, ensure_ascii=False, indent=1)
    md = os.path.join(out, "deck-review-%s.md" % stamp)
    with open(md, "w", encoding="utf-8") as fh:
        fh.write(report_md(r, deal))
    m = r["metrics"]
    print("%s: %d presented, %d%% from the kit, %d kept as is, %d edited, %d library, %d hand-made, %d dropped"
          % (deal, m["presented_slides"], m["kit_share"] * 100, m["kept"], m["edited"], m["library"], m["hand-made"], m["dropped"]))
    print(md)


if __name__ == "__main__":
    main()
