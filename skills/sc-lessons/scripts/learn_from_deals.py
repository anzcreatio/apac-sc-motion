"""Learn from past deals: what applies to the deal in front of us, from every SC's deals. Read-only, except `applied`.

  python learn_from_deals.py brief   --stage first-meeting|demo-plan|deck|rfp|workshop --deal <deal folder>
                                     [--industry bfsi|manufacturing|...] [--pains "single view, approvals"] [--out file.md] [--json file]
  python learn_from_deals.py applied --deal <deal folder> --stage <stage> --item "<id>: <what we did>" [--item ...]
  python learn_from_deals.py stats   [--days 7]

`brief` gathers, for the stage and this deal's industry and pains:
  - team lessons     Lessons/TEAM-LESSONS.md, the sections for this stage (ids like TL-2.2)
  - registers        Lessons/registers/: open product limits (L-), questions we should ask (Q-), approved answers (E-)
  - similar deals    other deals (any SC) by industry and pain words, and from each one only its LEARNINGS:
                     repo lessons/<date>-<deal>.md (keep / change / stop, without the evidence quotes),
                     meeting reviews' "What landed" (patterns and reactions), deck reviews (kit share, what got edited),
                     library modules harvested from it
Learnings, not people: never coaching, ratings, "Explaining it" sections or quotes of our own people.
`applied` appends what the SC used to <deal>/lessons-applied.json; `stats` counts it for the Friday digest.
Team root from ~/.apac-sc-motion.json.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TODAY = dt.date.today()

# Which team-lessons sections each stage reads (TEAM-LESSONS.md: 1 before, 2 deck, 3 build, 4 explaining, 5 claims, 6 after)
STAGE_SECTIONS = {"first-meeting": ["1", "2", "4", "5"], "deck": ["2", "4", "5"], "demo-plan": ["3", "5", "1"],
                  "rfp": ["5", "1"], "workshop": ["1", "6", "4"]}
# What to pull from similar deals for each stage
STAGE_FOCUS = {"first-meeting": ("lessons", "landed", "deck"), "deck": ("deck", "lessons", "landed"),
               "demo-plan": ("landed", "library", "lessons"), "rfp": ("lessons", "library"), "workshop": ("lessons", "landed")}
INDUSTRY = {
    "bfsi": r"\b(bank|banking|lend|lender|loan|credit|insur|securities|multi-?finance|pawn|wealth|broker)",
    "manufacturing": r"\b(manufactur|fmcg|distributor|wholesale|factory|plant|supply chain|field sales|dealer)",
    "education": r"\b(universit|college|student|enrol|academy|higher education)",
    "healthcare": r"\b(clinic|hospital|patient|radiolog|health)",
    "telco": r"\b(telco|telecom|mobile operator|subscriber)",
    "retail": r"\b(retail|store|shopper|e-?commerce)",
}
STOP = set("the a an and or of to in on for with our their your we they is are be it this that from by as at not no "
           "can will how what who when which more less one all any each new demo creatio customer customers team".split())
PRIVATE_HEADINGS = re.compile(r"explaining it|coaching|sc's own rating|how it felt", re.I)


def team_root(arg=None):
    if arg:
        return arg
    try:
        return json.load(open(os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json"), encoding="utf-8"))["sharepoint_root"]
    except Exception:
        sys.exit("No team root: run sc-setup first, or pass --root")


def rtext(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def rjson(p, default=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return default


def words(s):
    return [w for w in re.findall(r"[a-z][a-z\-]{2,}", (s or "").lower()) if w not in STOP]


def strip_md(s):
    return re.sub(r"\*\*|`", "", s or "").strip()


def deal_name(p):
    return re.sub(r"-(rh|wn|fa)$", "", os.path.basename(os.path.normpath(p)))


def deal_text(d, limit=400000):
    """The deal's own words: prep, transcripts, reviews, plans (enough to judge industry and pains)."""
    out, n = [], 0
    for pat in ("*fm-prep*.md", "*W1*.md", "*transcript*.md", "*meeting-review*.md", "*demo-plan*.md", "*discovery*.md",
                "*customer-email*.md", "rfp/*.md", "bank-ai.json", "deck.json", "build-plan.json"):
        for p in glob.glob(os.path.join(d, pat)):
            t = rtext(p)
            out.append(t)
            n += len(t)
            if n > limit:
                return "\n".join(out)
    return "\n".join(out)


def industries(text):
    t = text.lower()
    hits = {k: len(re.findall(v, t)) for k, v in INDUSTRY.items()}
    top = max(hits.values() or [0])
    return {k for k, v in hits.items() if v >= 3 and v >= 0.3 * top}


def table_rows(text, heading_re):
    m = re.search(heading_re, text, re.I | re.M)
    if not m:
        return [], None
    rows, header = [], None
    for line in text[m.end():].splitlines():
        s = line.strip()
        if s.startswith("#"):
            break
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            if header is None:
                header = [c.lower() for c in cells]
                continue
            rows.append(cells)
        elif rows and s and not s.startswith("|"):
            break
    return rows, header


# ---------- sources ----------

def team_lessons(root, stage):
    t = rtext(os.path.join(root, "Lessons", "TEAM-LESSONS.md"))
    out = []
    for sec in STAGE_SECTIONS.get(stage, []):
        m = re.search(r"^##\s*%s\.\s*(.+)$" % re.escape(sec), t, re.M)
        if not m:
            continue
        rows, header = table_rows(t, r"^##\s*%s\.\s*.+$" % re.escape(sec))
        for r in rows:
            if len(r) >= 3 and re.match(r"\d+\.\d+", r[0]):
                rec = dict(zip(header or [], r))
                out.append({"id": "TL-%s" % r[0], "section": m.group(1).strip(), "lesson": strip_md(r[1]),
                            "do": strip_md(rec.get("do", "")), "avoid": strip_md(rec.get("avoid", "")),
                            "source": "Lessons/TEAM-LESSONS.md"})
    return out


def registers(root, pain_words, ind):
    d = os.path.join(root, "Lessons", "registers")
    out = {"limits": [], "questions": [], "answers": [], "missing": []}
    for key, f in (("limits", "product-limits.json"), ("questions", "discovery-questions.json"), ("answers", "explanations.json")):
        j = rjson(os.path.join(d, f))
        if j is None:
            out["missing"].append(f)
            continue
        for e in j.get("entries", []):
            text = " ".join(str(e.get(k, "")) for k in ("area", "topic", "limit", "question", "signal", "one_liner", "workaround"))
            rel = len(set(words(text)) & pain_words)
            if key == "answers":
                if e.get("status") != "approved" or (pain_words and not rel):
                    continue
                out[key].append({"id": e["id"], "question": e.get("question"), "one_liner": e.get("one_liner"), "rel": rel})
            elif key == "limits":
                if e.get("status") != "open":
                    continue
                out[key].append({"id": e["id"], "area": e.get("area"), "limit": e.get("limit"), "workaround": e.get("workaround"),
                                 "confidence": e.get("confidence"), "rel": rel})
            else:
                if e.get("status") not in ("open", "approved", None):
                    continue
                out[key].append({"id": e["id"], "topic": e.get("topic"), "question": e.get("question"), "signal": e.get("signal"), "rel": rel})
    for k in ("limits", "questions", "answers"):
        out[k].sort(key=lambda e: -e["rel"])
    return out


def deal_lessons(d):
    """Repo lessons/<date>-<deal>.md: keep / change / stop rows, What + the note or proposed change. No evidence column."""
    out = []
    name = deal_name(d)
    for p in sorted(glob.glob(os.path.join(PLUGIN, "lessons", "*%s*.md" % name))):
        t = rtext(p)
        for kind in ("Keep", "Change", "Stop"):
            rows, header = table_rows(t, r"^##\s*%s\b.*$" % kind)
            for r in rows:
                rec = dict(zip(header or [], r))
                what = strip_md(rec.get("what") or r[0])
                how = strip_md(rec.get("proposed change") or rec.get("note") or "")
                if what:
                    out.append({"kind": kind.lower(), "what": what, "how": how, "source": "lessons/%s" % os.path.basename(p)})
        # one combined table: | Keep / change / stop | What | Evidence | Proposed change |
        for m in re.finditer(r"^\|\s*Keep\s*/\s*change.*$", t, re.I | re.M):
            for line in t[m.end():].lstrip("\r\n").splitlines():
                c = [x.strip() for x in line.strip().strip("|").split("|")]
                if not line.strip().startswith("|"):
                    break
                if len(c) < 2 or all(re.fullmatch(r":?-{2,}:?", x) for x in c if x):
                    continue
                how = strip_md(c[3]) if len(c) > 3 and c[3].lower() not in ("none", "-") else ""
                out.append({"kind": c[0].lower(), "what": strip_md(c[1]), "how": how, "source": "lessons/%s" % os.path.basename(p)})
    return out


def deal_landed(d):
    out = []
    for p in sorted(glob.glob(os.path.join(d, "*meeting-review*.md"))):
        t = rtext(p)
        rows, header = table_rows(t, r"^##\s*\d*\.?\s*What landed.*$")
        for r in rows:
            if len(r) >= 2 and r[0]:
                react = re.sub(r"\s*\((?:[A-Z][a-z]+ )?~?\d{1,2}:\d{2}\)", "", strip_md(r[1]))  # drop who-said-it timestamps
                out.append({"pattern": strip_md(r[0]), "reaction": react, "source": os.path.basename(p)})
    return out


def deal_deck(root, d):
    out = []
    name = os.path.basename(os.path.normpath(d))
    for p in sorted(glob.glob(os.path.join(root, "Lessons", "deck-edits", "deck-review-%s-*.json" % name)) +
                    glob.glob(os.path.join(root, "Lessons", "deck-edits", "deck-review-%s-*.json" % deal_name(d)))):
        j = rjson(p) or {}
        md = rtext(p[:-5] + ".md")
        rows, _ = table_rows(md, r"^##\s*Slide by slide.*$")
        edited = [strip_md(r[3]) for r in rows if len(r) > 4 and r[1] in ("edited", "hand-made")]
        dropped = [strip_md(r[3]) for r in rows if len(r) > 4 and r[1].startswith("generated but dropped")]
        m = re.search(r"\|\s*(\d+)\s*\|\s*(\d+)%\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", md)
        summary = ("%s slides, %s%% from the kit, %s kept, %s edited, %s corporate added, %s hand-made" % m.groups()) if m else ""
        out.append({"summary": summary, "edited": edited[:6], "dropped": dropped[:6], "source": "Lessons/deck-edits/%s" % os.path.basename(p)[:-5] + ".md"})
        if j:
            pass
    seen, uniq = set(), []
    for o in out:
        if o["source"] not in seen:
            seen.add(o["source"])
            uniq.append(o)
    return uniq


def deal_library(d):
    cat = rjson(os.path.join(PLUGIN, "library", "catalogue.json")) or {}
    out = []
    for m in cat.get("modules", []):
        if m.get("source_deal") in (os.path.basename(os.path.normpath(d)), deal_name(d)):
            out.append({"id": m.get("id"), "title": m.get("name") or m.get("id"),
                        "what": "%s%s" % (m.get("name") or "", ": %s" % m["what"] if m.get("what") else ""),
                        "reuse_h": m.get("reuse_estimate_h"), "source": "library/catalogue.json"})
    return out


def similar_deals(root, here, ind, pain_words, n=4):
    here_n = os.path.normpath(here) if here else None
    scored = []
    for d in sorted(glob.glob(os.path.join(root, "Deals", "*"))):
        b = os.path.basename(d)
        if not os.path.isdir(d) or b.startswith(("_", ".")) or (here_n and os.path.normpath(d) == here_n):
            continue
        t = deal_text(d)
        if not t.strip():
            continue
        di = industries(t)
        tw = set(words(t))
        hits = sorted(pain_words & tw)
        score = 3 * len(di & ind) + len(hits)
        has = bool(deal_lessons(d) or deal_landed(d) or deal_deck(root, d) or deal_library(d))
        if score and has:
            scored.append((score, b, sorted(di & ind), hits))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return scored[:n]


# ---------- commands ----------

def c_brief(a):
    root = team_root(a.root)
    deal = a.deal if a.deal and os.path.isdir(a.deal) else (os.path.join(root, "Deals", a.deal) if a.deal else None)
    here_text = deal_text(deal) if deal and os.path.isdir(deal) else ""
    ind = set(a.industry.lower().split(",")) if a.industry else industries(here_text)
    pain_words = set(words(a.pains)) if a.pains else set()
    if not pain_words and here_text:
        freq = {}
        lower = set(re.findall(r"\b[a-z][a-z\-]{2,}\b", here_text))  # words used in lower case; names are skipped
        for w in words(here_text):
            if w in lower:
                freq[w] = freq.get(w, 0) + 1
        pain_words = {w for w, _ in sorted(freq.items(), key=lambda kv: -kv[1])[:40]}
    res = {"stage": a.stage, "deal": deal and os.path.basename(deal), "industry": sorted(ind), "pains": sorted(pain_words)[:20],
           "team_lessons": team_lessons(root, a.stage), "registers": registers(root, pain_words, ind), "deals": []}
    focus = STAGE_FOCUS[a.stage]
    for score, b, di, hits in similar_deals(root, deal, ind, pain_words):
        d = os.path.join(root, "Deals", b)
        item = {"deal": b, "why": "same industry (%s)" % ", ".join(di) if di else "", "shared_words": hits[:8]}
        for f in focus:
            item[f] = {"lessons": deal_lessons, "landed": deal_landed, "library": deal_library}.get(f, lambda x: deal_deck(root, x))(d)
        res["deals"].append(item)
    L = ["# Learn from past deals: %s%s" % (a.stage, " for %s" % res["deal"] if res["deal"] else ""), "",
         "Industry: %s · Matched on: %s" % (", ".join(res["industry"]) or "not clear (pass --industry)", ", ".join(res["pains"][:10]) or "-"), "",
         "Use what fits, say which in the output's **Applied from past deals** section, then log it with `applied`.", ""]
    L += ["## Team lessons for this stage", ""]
    for t in res["team_lessons"]:
        L.append("- **%s %s** · Do: %s · Avoid: %s" % (t["id"], t["lesson"], t["do"], t["avoid"]))
    if not res["team_lessons"]:
        L.append("- (no team lessons page found)")
    R = res["registers"]
    L += ["", "## Ask, check and say (shared registers; live straight away)", ""]
    for q in R["questions"][:6]:
        L.append("- **%s** ask: %s%s" % (q["id"], q["question"], " (when: %s)" % q["signal"] if q.get("signal") else ""))
    for l in R["limits"][:6]:
        L.append("- **%s** limit (%s): %s%s" % (l["id"], l.get("confidence") or "reported", l["limit"], "; workaround: %s" % l["workaround"] if l.get("workaround") else ""))
    for e in R["answers"][:4]:
        L.append("- **%s** approved answer to \"%s\": %s" % (e["id"], e["question"], e["one_liner"]))
    if R["missing"]:
        L.append("- Not started yet: %s (`sc-lessons` creates them)" % ", ".join(R["missing"]))
    L += ["", "## From similar deals (any SC: learnings only)", ""]
    if not res["deals"]:
        L.append("No similar deal with lessons yet.")
    for it in res["deals"]:
        L += ["### %s%s" % (it["deal"], " · %s" % it["why"] if it["why"] else ""), ""]
        for x in it.get("lessons", [])[:8]:
            L.append("- %s: %s%s (`%s`)" % (x["kind"].capitalize(), x["what"], " → %s" % x["how"] if x["how"] else "", x["source"]))
        for x in it.get("landed", [])[:6]:
            L.append("- Landed? %s: %s (`%s`)" % (x["pattern"], x["reaction"], x["source"]))
        for x in it.get("deck", [])[:2]:
            L.append("- Deck: %s%s%s (`%s`)" % (x["summary"], "; edited before presenting: %s" % ", ".join(x["edited"]) if x["edited"] else "",
                                                 "; dropped: %s" % ", ".join(x["dropped"]) if x["dropped"] else "", x["source"]))
        for x in it.get("library", [])[:4]:
            L.append("- Reusable: library module `%s` (%s%s)" % (x["id"], x["what"][:140], ", reuse about %s h" % x["reuse_h"] if x.get("reuse_h") else ""))
        L.append("")
    md = "\n".join(L)
    print(md)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(md)
    if a.json:
        json.dump(res, open(a.json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def c_applied(a):
    root = team_root(a.root)
    deal = a.deal if os.path.isdir(a.deal) else os.path.join(root, "Deals", a.deal)
    if not os.path.isdir(deal):
        sys.exit("Deal folder not found: %s" % a.deal)
    if os.path.basename(os.path.dirname(os.path.normpath(deal))) == "_practice" or "_practice" in deal:
        sys.exit("Practice folder: nothing logged.")
    p = os.path.join(deal, "lessons-applied.json")
    j = rjson(p) or {"deal": os.path.basename(deal), "runs": []}
    items = []
    for s in a.item:
        m = re.match(r"\s*([A-Za-z0-9.\-:_]+?)\s*:\s*(.+)", s)
        items.append({"id": m.group(1), "what": m.group(2)} if m else {"id": None, "what": s})
    j["runs"].append({"date": TODAY.isoformat(), "stage": a.stage, "items": items})
    json.dump(j, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("%s: %d lessons applied at %s" % (j["deal"], len(items), a.stage))


def c_stats(a):
    root = team_root(a.root)
    since = TODAY - dt.timedelta(days=a.days)
    runs = items = 0
    by = {}
    for p in glob.glob(os.path.join(root, "Deals", "*", "lessons-applied.json")):
        for r in (rjson(p) or {}).get("runs", []):
            try:
                if dt.date.fromisoformat(r["date"]) < since:
                    continue
            except Exception:
                continue
            runs += 1
            for it in r.get("items", []):
                items += 1
                k = (it.get("id") or "other").split(":")[0]
                k = re.sub(r"^(TL-\d+)\.\d+$", r"\1", k) if k.startswith("TL-") else (k.split("-")[0] + "-" if re.match(r"^[LQE]-", k) else "past deal")
                by[k] = by.get(k, 0) + 1
    print("Last %d days: %d deal-start runs applied %d lessons · by source: %s" % (a.days, runs, items,
          ", ".join("%s %d" % kv for kv in sorted(by.items(), key=lambda kv: -kv[1])) or "none"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("brief"); p.add_argument("--stage", required=True, choices=list(STAGE_SECTIONS)); p.add_argument("--deal")
    p.add_argument("--industry"); p.add_argument("--pains"); p.add_argument("--out"); p.add_argument("--json")
    p = sp.add_parser("applied"); p.add_argument("--deal", required=True); p.add_argument("--stage", required=True, choices=list(STAGE_SECTIONS))
    p.add_argument("--item", action="append", required=True)
    p = sp.add_parser("stats"); p.add_argument("--days", type=int, default=7)
    a = ap.parse_args()
    {"brief": c_brief, "applied": c_applied, "stats": c_stats}[a.cmd](a)


if __name__ == "__main__":
    main()
