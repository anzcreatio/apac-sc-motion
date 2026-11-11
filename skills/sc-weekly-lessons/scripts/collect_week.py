"""Collect a week's evidence for the weekly lessons digest. Read-only.

Usage: python collect_week.py [--days 7] [--root <team root>] [--repo <plugin repo>] [--out <file.json>]

Gathers, for files changed in the window:
  - deck reviews        SharePoint Lessons/deck-edits/*.json  (kit share, kept / edited / library / hand-made)
  - meeting reviews     Deals/*/NN-meeting-review-*.md
  - first-meeting preps Deals/*/01-fm-prep.md  (six-question coverage score)
  - demo plans          Deals/*/NN-demo-plan*.md
  - lessons files       <repo>/lessons/*.md
  - inbox               _inbox files waiting, latest scan; Patterns/_inbox items waiting
  - library             deals with a demo build but no library module (harvest overdue)
  - click paths         customer recaps still DRAFT (approved false)
Prints a short summary and writes the full JSON for Claude to read and judge.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "sc-deck", "scripts"))
from build_deck import team_root  # noqa: E402

REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))


def recent(paths, since):
    out = []
    for p in paths:
        try:
            if datetime.datetime.fromtimestamp(os.path.getmtime(p)) >= since:
                out.append(p)
        except OSError:
            pass
    return sorted(out)


def coverage(text):
    m = re.search(r"[Cc]overage[^0-9]{0,30}(\d+(?:\.\d)?)\s*(?:/|of)\s*6", text)
    if m:
        return float(m.group(1))
    m = re.search(r"(\d)\s*answered,\s*(\d)\s*partly", text)
    if m:
        return int(m.group(1)) + 0.5 * int(m.group(2))
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--root")
    ap.add_argument("--repo", default=REPO)
    ap.add_argument("--out")
    a = ap.parse_args()
    root = a.root or team_root()
    since = datetime.datetime.now() - datetime.timedelta(days=a.days)
    deals = os.path.join(root, "Deals")
    week = datetime.date.today().isocalendar()
    rep = {"week": "%d-W%02d" % (week[0], week[1]), "since": since.date().isoformat(), "root": root}

    rep["deck_reviews"] = []
    for p in recent(glob.glob(os.path.join(root, "Lessons", "deck-edits", "*.json")), since):
        d = json.load(open(p, encoding="utf-8"))
        rep["deck_reviews"].append({"file": os.path.basename(p), "deal": d.get("deal"), "metrics": d.get("metrics"),
                                    "hand_made": [s["title"] for s in d.get("slides", []) if s.get("status") == "hand-made"],
                                    "edited_titles": [s.get("title_change") for s in d.get("slides", []) if s.get("title_change")]})

    rep["meeting_reviews"] = [os.path.relpath(p, deals) for p in recent(glob.glob(os.path.join(deals, "*", "*meeting-review*.md")), since)]
    rep["demo_plans"] = [os.path.relpath(p, deals) for p in recent(glob.glob(os.path.join(deals, "*", "*demo-plan*.md")), since)]
    rep["transcripts"] = [os.path.relpath(p, deals) for p in recent(glob.glob(os.path.join(deals, "*", "*transcript*.md")), since)]

    rep["coverage"] = []
    for p in recent(glob.glob(os.path.join(deals, "*", "*fm-prep*.md")), since):
        rep["coverage"].append({"deal": os.path.basename(os.path.dirname(p)), "file": os.path.basename(p),
                                "score": coverage(open(p, encoding="utf-8", errors="replace").read())})

    rep["lessons_files"] = [os.path.basename(p) for p in recent(glob.glob(os.path.join(a.repo, "lessons", "*.md")), since)]

    inbox = os.path.join(root, "_inbox")
    rep["inbox_waiting"] = [f for f in os.listdir(inbox) if not f.startswith(("_", "~$")) and os.path.isfile(os.path.join(inbox, f))] if os.path.isdir(inbox) else []
    pin = os.path.join(root, "Patterns", "_inbox")
    rep["patterns_waiting"] = [f for f in os.listdir(pin) if not f.startswith(("_", "~$"))] if os.path.isdir(pin) else []

    cat = os.path.join(a.repo, "library", "catalogue.json")
    harvested = {m.get("source_deal") for m in json.load(open(cat, encoding="utf-8")).get("modules", [])} if os.path.isfile(cat) else set()
    built = set()
    for d in glob.glob(os.path.join(deals, "*")):
        if glob.glob(os.path.join(d, "click*", "cards.json")) or glob.glob(os.path.join(d, "build", "*")):
            built.add(os.path.basename(d))
    rep["harvest_missing"] = sorted(built - harvested)

    rep["recaps_draft"] = []
    for p in glob.glob(os.path.join(deals, "*", "click*", "clickpath-customer.json")):
        o = json.load(open(p, encoding="utf-8"))
        if not o.get("approved"):
            rep["recaps_draft"].append(os.path.relpath(p, deals))

    out = a.out or os.path.join(root, "Lessons", "weekly", "%s-evidence.json" % rep["week"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(rep, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Week %s (since %s)" % (rep["week"], rep["since"]))
    for k in ("deck_reviews", "meeting_reviews", "demo_plans", "transcripts", "coverage", "lessons_files",
              "inbox_waiting", "patterns_waiting", "harvest_missing", "recaps_draft"):
        print("  %-17s %d" % (k, len(rep[k])))
    print(out)


if __name__ == "__main__":
    main()
