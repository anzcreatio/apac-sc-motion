"""Scan the SharePoint _inbox for new corporate decks and compare every slide with the Slide-library.

Usage: python inbox_scan.py [--root <team root>] [--out <dir>]

For each .pptx in <team root>/_inbox (not in _inbox/_done): the text of every slide, a fingerprint, and the closest
match in the Slide-library (same / changed / new). Writes <out>/inbox-scan-<date>.json and .md for Claude to read and
judge. It changes nothing: adding slides to the library and moving files to _done happen only after the SC approves.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

from pptx import Presentation

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "sc-deck", "scripts"))
from build_deck import team_root  # noqa: E402


def slide_text(slide):
    parts = []
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            parts.append(sh.text_frame.text.strip())
        if getattr(sh, "has_table", False) and sh.has_table:
            parts.extend(c.text for r in sh.table.rows for c in r.cells if c.text.strip())
    return "\n".join(parts)


def words(text):
    return set(re.findall(r"[a-z0-9]{3,}", text.lower()))


def fingerprint(text):
    return hashlib.sha1(" ".join(sorted(words(text))).encode()).hexdigest()[:12]


def slides_of(path):
    prs = Presentation(path)
    out = []
    for i, s in enumerate(prs.slides, 1):
        t = slide_text(s)
        notes = s.notes_slide.notes_text_frame.text if s.has_notes_slide and s.notes_slide.notes_text_frame is not None else ""
        pics = sum(1 for sh in s.shapes if sh.shape_type == 13)
        media = sum(1 for r in s.part.rels.values() if r.reltype.endswith(("/video", "/media")))
        out.append({"slide": i, "layout": s.slide_layout.name, "text": t, "notes": notes, "pictures": pics,
                    "video": media > 0, "fp": fingerprint(t), "words": sorted(words(t))})
    return out, [l.name for m in prs.slide_masters for l in m.slide_layouts]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--out")
    a = ap.parse_args()
    root = a.root or team_root()
    inbox, lib_dir = os.path.join(root, "_inbox"), os.path.join(root, "Slide-library")
    out_dir = a.out or os.path.join(inbox, "_scans")
    os.makedirs(out_dir, exist_ok=True)

    library = []
    for f in sorted(os.listdir(lib_dir)):
        if f.lower().endswith(".pptx") and not f.startswith("~$"):
            for s in slides_of(os.path.join(lib_dir, f))[0]:
                library.append(dict(s, file=f))

    files = [f for f in sorted(os.listdir(inbox)) if not f.startswith(("~$", "_")) and os.path.isfile(os.path.join(inbox, f))]
    report = {"date": datetime.date.today().isoformat(), "root": root, "files": []}
    for f in files:
        entry = {"file": f, "size_mb": round(os.path.getsize(os.path.join(inbox, f)) / 1e6, 1)}
        if not f.lower().endswith(".pptx"):
            entry["note"] = "not a .pptx: read it directly (PDF/Word) and judge by hand"
            report["files"].append(entry)
            continue
        slides, layouts = slides_of(os.path.join(inbox, f))
        entry["layouts"] = layouts
        for s in slides:
            best, score = None, 0.0
            for l in library:
                if l["fp"] == s["fp"]:
                    best, score = l, 1.0
                    break
                ws, wl = set(s["words"]), set(l["words"])
                j = len(ws & wl) / len(ws | wl) if ws | wl else 0
                if j > score:
                    best, score = l, j
            s["match"] = None if not best else {"file": best["file"], "slide": best["slide"], "similarity": round(score, 2)}
            s["status"] = "same" if score >= 0.95 else "changed" if score >= 0.6 else "new"
            del s["words"]
        entry["slides"] = slides
        report["files"].append(entry)

    stamp = report["date"]
    jpath = os.path.join(out_dir, "inbox-scan-%s.json" % stamp)
    with open(jpath, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)
    lines = ["# Inbox scan %s" % stamp, "", "Library: %d slides in %s" % (len(library), lib_dir), ""]
    for e in report["files"]:
        lines.append("## %s (%s MB)" % (e["file"], e["size_mb"]))
        if "slides" not in e:
            lines.append(e["note"])
            continue
        lines.append("| # | Status | Closest library slide | First line |")
        lines.append("|---|---|---|---|")
        for s in e["slides"]:
            m = s["match"]
            first = (s["text"].split("\n")[0] if s["text"] else "(no text: picture or video)")[:70]
            lines.append("| %d | %s | %s | %s |" % (s["slide"], s["status"],
                         "%s #%d (%.2f)" % (m["file"], m["slide"], m["similarity"]) if m else "-", first.replace("|", "/")))
        lines.append("")
    mpath = os.path.join(out_dir, "inbox-scan-%s.md" % stamp)
    with open(mpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("scanned %d file(s); %d library slides compared" % (len(files), len(library)))
    print(mpath)


if __name__ == "__main__":
    main()
