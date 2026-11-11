"""RFP / TOR fit-gap tools for sc-rfp. Read-only on the customer's file; writes only new files.

  python rfp.py scan     <rfp.xlsx> [--out scan.json]
      Every sheet: size, the likely header row, its columns and three sample rows. Claude reads this to write map.json.

  python rfp.py register <rfp.xlsx> --map map.json --out register.json
      Extract every requirement with the column map (see SKILL.md for the format).

  python rfp.py fitgap   --register register.json --verdicts verdicts.json --out fit-gap.xlsx [--summary summary.md]
                         [--codes codes.json] [--deal "<Customer>"]
      Fit-gap workbook (Fit-gap, Summary, Bid team, Questions sheets) and the bid / no-bid numbers.

  python rfp.py check    --register register.json --verdicts verdicts.json --out consistency.md [--xlsx consistency.xlsx]
      Compares the customer-facing answers already in the register (the bid team's) with our verdicts. Lists every
      line where their answer claims more than we found.

  python rfp.py poc      --register register.json --verdicts verdicts.json --out 05-poc-brief.md [--deal "<Customer>"]
      POC brief for sc-demo-plan proof mode (+ 05-poc-brief.json with the Build, Show and gap refs).

  python rfp.py coverage --brief 05-poc-brief.json <demo-plan.md> [<clickpath/cards.json> ...]
      Every Build ref and must-have gap must appear in each file. Exit 1 if any is missing.
"""
import argparse
import collections
import datetime
import json
import os
import re
import sys

try:
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import column_index_from_string, get_column_letter
except ImportError:
    sys.exit("openpyxl missing: python -m pip install openpyxl")

KEYS = re.compile(r"(?i)\b(no|id|requirement|kebutuhan|scope|mandatory|optional|compliance|response|respons|"
                  r"explanation|remark|priority|weight|bobot|module|category|section|fitur|deskripsi)\b")

# Our fit categories, strongest first. "fit" = can be met without a gap.
FITS = {
    "standard":    {"rank": 4, "fit": True,  "label": "Standard (out of the box)"},
    "configure":   {"rank": 4, "fit": True,  "label": "Configure, no code (Business Studio)"},
    "ai":          {"rank": 4, "fit": True,  "label": "Creatio.ai / AI Studio"},
    "marketplace": {"rank": 3, "fit": True,  "label": "Marketplace app"},
    "integration": {"rank": 3, "fit": True,  "label": "Integration (Creatio side supported; other system work)"},
    "custom":      {"rank": 2, "fit": False, "label": "Custom development"},
    "partner":     {"rank": 1, "fit": False, "label": "Third-party product or partner"},
    "roadmap":     {"rank": 1, "fit": False, "label": "Roadmap (not available today)"},
    "no":          {"rank": 0, "fit": False, "label": "Not supported"},
    "n/a":         {"rank": None, "fit": None, "label": "Not applicable / bid team"},
}
NO_BUILD = {"standard", "configure", "ai"}

# How strongly a customer-facing answer claims, by common wording (English, Bahasa, customer codes).
CLAIM = [
    (r"(?i)^(fully comply|comply|complied|yes|fs|fully supported|sesuai|memenuhi|ya|available)\b", 4),
    (r"(?i)^(mm|minor)", 3),
    (r"(?i)^(partial|partially|sebagian|lm|large|major|3rd party|third party|customi[sz])", 2),
    (r"(?i)^(roadmap|future|nv)", 1),
    (r"(?i)^(not comply|non comply|no|ns|not supported|tidak)\b", 0),
    (r"(?i)^n/?a$", None),
]
CUES = re.compile(r"(?i)(integrat|third[- ]party|3rd party|partner|custom(i[sz])?|develop|roadmap|future release|"
                  r"marketplace|add-?on|not (natively|out of the box)|can be (built|developed|configured)|requires?|"
                  r"via (api|cti)|integrasi|kustom|pengembangan)")


def cell(row, col):
    if not col:
        return None
    i = column_index_from_string(col) - 1
    v = row[i] if i < len(row) else None
    if isinstance(v, str):
        v = v.strip()
    return v if v not in ("", None) else None


def scan(a):
    wb = openpyxl.load_workbook(a.file, read_only=True, data_only=True)
    out = {"file": os.path.basename(a.file), "sheets": []}
    for ws in wb.worksheets:
        rows = [r for r in ws.iter_rows(values_only=True)]
        best, bi = -1, None
        for i, r in enumerate(rows[:40]):
            s = sum(1 for c in r if isinstance(c, str) and len(c) < 60 and KEYS.search(c))
            if s > best:
                best, bi = s, i
        info = {"sheet": ws.title, "rows": len(rows), "header_row": (bi + 1) if bi is not None else None}
        if bi is not None:
            info["columns"] = {get_column_letter(j + 1): str(c)[:60] for j, c in enumerate(rows[bi]) if c not in (None, "")}
            samples = [r for r in rows[bi + 1:] if sum(1 for c in r if c not in (None, "")) >= 2][:3]
            info["samples"] = [{get_column_letter(j + 1): str(c)[:120] for j, c in enumerate(r) if c not in (None, "")}
                               for r in samples]
        out["sheets"].append(info)
    js = json.dumps(out, ensure_ascii=False, indent=1)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(js)
    print(js[:20000])


def scope_of(sm, rid):
    """Sheet scope, unless the map lists row IDs: "ours_ids" (everything else is bid) or "bid_ids"."""
    if "ours_ids" in sm:
        return "ours" if rid in {str(x) for x in sm["ours_ids"]} else "bid"
    if "bid_ids" in sm:
        return "bid" if rid in {str(x) for x in sm["bid_ids"]} else sm.get("scope", "ours")
    return sm.get("scope", "ours")


def register(a):
    m = json.load(open(a.map, encoding="utf-8"))
    wb = openpyxl.load_workbook(a.file, read_only=True, data_only=True)
    reqs, seen = [], collections.Counter()
    for sm in m["sheets"]:
        ws = wb[sm["sheet"]]
        prefix = sm.get("prefix", "")
        sec_mode = sm.get("section", {}).get("mode")
        section = None
        for n, r in enumerate(ws.iter_rows(values_only=True), start=1):
            if n <= sm["header_row"]:
                continue
            rid, text = cell(r, sm["id_col"]), cell(r, sm["text_col"])
            mo = cell(r, sm.get("mo_col"))
            if sec_mode == "row":
                hc = cell(r, sm["section"].get("id_col", sm["id_col"]))
                ht = cell(r, sm["section"].get("text_col", sm["text_col"]))
                if hc is not None and re.fullmatch(r"\d+", str(hc).strip()) and ht and not rid:
                    section = str(ht)
                    continue
            if rid is None or not text:
                continue
            rid = str(rid).strip().rstrip(".")
            if isinstance(text, str) and text.lower() in ("requirements", "scope of software requirements", "scope of requirements",
                                                          "scope of work", "kebutuhan asli", "functional requirement",
                                                          "technical requirement"):
                continue
            text = str(text)
            if sec_mode == "prefix_colon":
                section = text.split(":", 1)[0].strip() if ":" in text[:80] else section
            elif sec_mode == "col":
                section = cell(r, sm["section"]["col"]) or section
            mand = None
            if mo:
                mand = bool(re.match(r"(?i)^(m|mandatory|wajib|must)", str(mo)))
            answer = {k: cell(r, c) for k, c in sm.get("answer_cols", {}).items()}
            extra = {k: cell(r, c) for k, c in sm.get("extra_cols", {}).items()}
            key = prefix + rid
            seen[key] += 1
            if seen[key] > 1:
                key = "%s#%d" % (key, seen[key])
            reqs.append({"rid": key, "sheet": sm["sheet"], "src_id": rid, "section": section or sm.get("default_section"),
                         "text": text, "mandatory": mand, "weight": extra.get("weight"), "scope": scope_of(sm, rid),
                         "answer": {k: v for k, v in answer.items() if v is not None}, "extra": extra})
    out = {"source": os.path.basename(a.file), "customer": m.get("customer"), "language": m.get("language"),
           "codes": m.get("codes"), "built": datetime.date.today().isoformat(), "requirements": reqs}
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    c = collections.Counter((q["sheet"], q["scope"]) for q in reqs)
    for (s, sc), k in c.items():
        print("%-40s %-5s %d" % (s[:40], sc, k))
    print("total", len(reqs), "ours", sum(1 for q in reqs if q["scope"] == "ours"), "->", a.out)


def load(a):
    reg = json.load(open(a.register, encoding="utf-8"))
    ver = {v["rid"]: v for v in json.load(open(a.verdicts, encoding="utf-8"))}
    return reg, ver


def metrics(reqs, ver):
    ours = [q for q in reqs if q["scope"] == "ours"]
    rated = [q for q in ours if ver.get(q["rid"], {}).get("fit") in FITS and FITS[ver[q["rid"]]["fit"]]["fit"] is not None]

    def share(qs, test):
        w = sum(float(q.get("weight") or 1) for q in qs)
        return round(100.0 * sum(float(q.get("weight") or 1) for q in qs if test(q)) / w, 1) if w else None

    fit = lambda q: FITS[ver[q["rid"]]["fit"]]["fit"]
    nob = lambda q: ver[q["rid"]]["fit"] in NO_BUILD
    must = [q for q in rated if q["mandatory"] is not False]
    gaps = [q for q in must if not fit(q)]
    hard = [q for q in gaps if ver[q["rid"]]["fit"] == "no" and not ver[q["rid"]].get("workaround")]
    soft = [q for q in gaps if ver[q["rid"]]["fit"] in ("custom", "partner")]
    mf = share(must, fit)
    if mf is None:
        rec = "Not enough rated"
    elif mf >= 90 and not hard and len(soft) <= 1 and not [q for q in gaps if ver[q["rid"]]["fit"] == "no"]:
        rec = "Bid"
    elif mf < 75 or hard:
        rec = "No-bid"
    else:
        rec = "Bid with conditions"
    return {
        "ours": len(ours), "rated": len(rated), "unrated": len(ours) - len(rated),
        "fit_pct": share(rated, fit), "no_build_pct": share(rated, nob),
        "must_n": len(must), "must_fit_pct": mf, "must_no_build_pct": share(must, nob),
        "by_fit": collections.Counter(ver[q["rid"]]["fit"] for q in rated),
        "must_gaps": gaps, "hard_gaps": hard, "low_conf": [q for q in rated if ver[q["rid"]].get("confidence") == "low"],
        "tiers": collections.Counter(ver[q["rid"]].get("tier") for q in rated),
        "build_hours": sum(float(ver[q["rid"]].get("hours") or 0) for q in rated if ver[q["rid"]].get("tier") == "Build"),
        "custom_days": sum(float(ver[q["rid"]].get("mandays") or 0) for q in rated),
        "recommendation": rec,
    }


def fitgap(a):
    reg, ver = load(a)
    reqs = reg["requirements"]
    codes = json.load(open(a.codes, encoding="utf-8")) if a.codes else (reg.get("codes") or {})
    mt = metrics(reqs, ver)
    wb = openpyxl.Workbook()
    hdr = Font(bold=True, color="FFFFFF")
    fill = PatternFill("solid", fgColor="0058EF")
    colors = {True: "E6F4EA", False: "FDE7E7"}
    ws = wb.active
    ws.title = "Fit-gap"
    cols = ["Ref", "Sheet", "Their ID", "Section", "Requirement (their words)", "English (if translated)", "Must?",
            "Fit", "How we meet it", "Confidence", "Evidence", "POC tier", "POC hours", "Custom man-days",
            "Their code (proposed)", "Workaround / note", "Question for the customer"]
    ws.append(cols)
    for c in ws[1]:
        c.font, c.fill = hdr, fill
    for q in reqs:
        if q["scope"] != "ours":
            continue
        v = ver.get(q["rid"], {})
        f = v.get("fit")
        ws.append([q["rid"], q["sheet"], q["src_id"], q["section"], q["text"], v.get("english"),
                   {True: "Must", False: "Optional", None: ""}[q["mandatory"]], FITS.get(f, {}).get("label", f or "NOT RATED"),
                   v.get("how"), v.get("confidence"), v.get("evidence"), v.get("tier"), v.get("hours"), v.get("mandays"),
                   codes.get(f, "") if f else "", v.get("workaround"), v.get("question")])
        ok = FITS.get(f, {}).get("fit")
        if ok is not None:
            ws.cell(ws.max_row, 8).fill = PatternFill("solid", fgColor=colors[ok])
    widths = [10, 14, 8, 22, 60, 40, 9, 26, 50, 11, 40, 10, 9, 10, 12, 30, 40]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "F2"
    ws.auto_filter.ref = ws.dimensions

    s = wb.create_sheet("Summary")
    lines = [("Deal", a.deal or reg.get("customer")), ("Source", reg.get("source")), ("Built", datetime.date.today().isoformat()),
             ("Requirements (ours)", mt["ours"]), ("Rated", mt["rated"]), ("Fit % (all rated)", mt["fit_pct"]),
             ("Fit without building anything %", mt["no_build_pct"]), ("Must-haves", mt["must_n"]),
             ("Must-have fit %", mt["must_fit_pct"]), ("Must-haves needing custom, partner, roadmap or no", len(mt["must_gaps"])),
             ("POC Build hours", mt["build_hours"]), ("Implementation man-days beyond standard (first estimate)", mt["custom_days"]),
             ("Low-confidence verdicts (check)", len(mt["low_conf"])), ("Recommendation", mt["recommendation"]), ("", "")]
    lines += [("Fit: " + FITS[k]["label"], n) for k, n in mt["by_fit"].most_common()]
    lines += [("", "")] + [("POC tier: %s" % k, n) for k, n in mt["tiers"].most_common()]
    for k, v in lines:
        s.append([k, v])
    s.column_dimensions["A"].width = 52
    s.column_dimensions["B"].width = 30

    b = wb.create_sheet("Bid team (not ours)")
    b.append(["Ref", "Sheet", "Their ID", "Requirement"])
    for q in reqs:
        if q["scope"] != "ours":
            b.append([q["rid"], q["sheet"], q["src_id"], q["text"]])
    b.column_dimensions["D"].width = 100

    qs = wb.create_sheet("Questions")
    qs.append(["Ref", "Requirement", "Question for the customer"])
    for q in reqs:
        v = ver.get(q["rid"], {})
        if v.get("question"):
            qs.append([q["rid"], q["text"][:300], v["question"]])
    qs.column_dimensions["B"].width = 70
    qs.column_dimensions["C"].width = 60
    wb.save(a.out)

    if a.summary:
        open(a.summary, "w", encoding="utf-8").write(summary_md(reg, ver, mt, a.deal, os.path.basename(a.out)))
    print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in mt.items()}, default=dict, indent=1))
    print("->", a.out)


def summary_md(reg, ver, mt, deal, xlsx="fit-gap.xlsx"):
    L = ["# Bid / no-bid: %s" % (deal or reg.get("customer") or reg["source"]), "",
         "> `sc-rfp` from `%s`, %s. Internal: for the SC, AE and bid team. Fit-gap: `%s`." % (reg["source"], datetime.date.today().isoformat(), xlsx),
         "", "## Recommendation: **%s**" % mt["recommendation"], "",
         "| Measure | Value |", "|---|---|",
         "| Requirements in our scope | %d (%d rated) |" % (mt["ours"], mt["rated"]),
         "| Must-have fit | **%s%%** (%d must-haves) |" % (mt["must_fit_pct"], mt["must_n"]),
         "| Fit, all rated | %s%% |" % mt["fit_pct"],
         "| Met without building anything (standard, configure, AI) | %s%% |" % mt["no_build_pct"],
         "| POC Build hours | %s |" % mt["build_hours"],
         "| Implementation man-days beyond standard (first estimate) | %s |" % mt["custom_days"],
         "| Low-confidence verdicts to check | %d |" % len(mt["low_conf"]), "",
         "Rule: Bid = must-have fit ≥ 90% and no must-have we can't do; Bid with conditions = 75–90% or a must-have needing "
         "custom or partner work; No-bid = under 75% or a must-have we can't do with no workaround.", "",
         "## Big gaps (must-haves)", "", "| Ref | Requirement | Fit | Workaround |", "|---|---|---|---|"]
    for q in mt["must_gaps"]:
        v = ver[q["rid"]]
        L.append("| %s | %s | %s | %s |" % (q["rid"], (v.get("english") or q["text"]).replace("|", "/").replace("\n", " ")[:160],
                                             FITS[v["fit"]]["label"], (v.get("workaround") or "").replace("|", "/")))
    if not mt["must_gaps"]:
        L.append("| | None | | |")
    L += ["", "## Fit by category", "", "| Fit | Count |", "|---|---|"] + \
         ["| %s | %d |" % (FITS[k]["label"], n) for k, n in mt["by_fit"].most_common()]
    L += ["", "SC check required before this is used with the customer or the bid team."]
    return "\n".join(L) + "\n"


def claim(text):
    if not text:
        return None, "blank"
    t = str(text).strip()
    for rx, r in CLAIM:
        if re.match(rx, t):
            return r, t
    return None, t


def check(a):
    reg, ver = load(a)
    rows = []
    for q in reg["requirements"]:
        if q["scope"] != "ours":
            continue
        v = ver.get(q["rid"])
        ans = q.get("answer", {})
        their_r, their_t = claim(ans.get("compliance"))
        if not v or v.get("fit") not in FITS or FITS[v["fit"]]["rank"] is None or their_r is None:
            continue
        ours = FITS[v["fit"]]["rank"]
        expl = ans.get("explanation") or ""
        cue = CUES.search(expl or "")
        issue = None
        if their_r == 4 and ours == 3:
            issue = "Says comply; it depends on an integration or Marketplace app"
        elif their_r > ours:
            issue = "Claims more than we found"
        elif their_r == 4 and cue and v["fit"] not in NO_BUILD:
            issue = "Says comply; their own explanation mentions '%s'" % cue.group(0)
        if issue:
            rows.append((q, v, their_t, issue, expl))
    sev = {"Claims more than we found": 0}
    rows.sort(key=lambda x: (sev.get(x[3], 1), x[0]["rid"]))
    total = sum(1 for q in reg["requirements"] if q["scope"] == "ours" and q["rid"] in ver)
    L = ["# Consistency check: %s" % (reg.get("customer") or reg["source"]), "",
         "> Our fit-gap vs the answers in `%s`. %s. Internal. Nothing here is sent to the bid team without the SC." % (reg["source"], datetime.date.today().isoformat()),
         "", "**%d of %d checked lines need a look**: %d claim more than we found (custom, partner, roadmap or no); %d say comply "
         "but depend on an integration or Marketplace app; %d say comply while their own explanation hints otherwise." %
         (len(rows), total, sum(1 for r in rows if r[3] == "Claims more than we found"),
          sum(1 for r in rows if r[3].startswith("Says comply; it depends")), sum(1 for r in rows if "explanation" in r[3])), "",
         "| Ref | Requirement | Their answer | Our fit | Issue | Their explanation (start) |", "|---|---|---|---|---|---|"]
    for q, v, t, issue, expl in rows:
        L.append("| %s | %s | %s | %s | %s | %s |" % (q["rid"], (v.get("english") or q["text"]).replace("|", "/").replace("\n", " ")[:120], t,
                                                     FITS[v["fit"]]["label"], issue, (expl or "").replace("|", "/").replace("\n", " ")[:160]))
    L += ["", "SC check required before this is used with the customer or the bid team."]
    open(a.out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    if a.xlsx:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Consistency"
        ws.append(["Ref", "Requirement", "Their answer", "Their explanation", "Our fit", "How we meet it", "Issue"])
        for q, v, t, issue, expl in rows:
            ws.append([q["rid"], q["text"], t, expl, FITS[v["fit"]]["label"], v.get("how"), issue])
        for col, w in zip("ABCDEFG", [10, 60, 14, 60, 26, 50, 40]):
            ws.column_dimensions[col].width = w
        wb.save(a.xlsx)
    print(len(rows), "of", total, "->", a.out)


def short(t, n=150):
    t = " ".join(str(t or "").split())
    return t if len(t) <= n else t[:n - 1] + "…"


def poc(a):
    """POC brief for sc-demo-plan (proof mode): Build lines to configure, gaps to handle, Show evidence, questions."""
    reg, ver = load(a)
    ours = [q for q in reg["requirements"] if q["scope"] == "ours" and q["rid"] in ver]
    tier = lambda t: [q for q in ours if ver[q["rid"]].get("tier") == t]
    build, show, tell = tier("Build"), tier("Show"), tier("Tell")
    mt = metrics(reg["requirements"], ver)
    eng = lambda q: ver[q["rid"]].get("english") or q["text"]
    L = ["# POC brief: %s" % (a.deal or reg.get("customer") or reg["source"]), "",
         "> From the fit-gap (`sc-rfp`), %s. Input for `sc-demo-plan` in **proof mode**: it maps every Build line to a "
         "scene and a test. Internal." % datetime.date.today().isoformat(), "",
         "| | |", "|---|---|",
         "| Build (live in the POC) | %d lines, about %s h |" % (len(build), sum(float(ver[q["rid"]].get("hours") or 0) for q in build)),
         "| Show (screenshot or clip) | %d |" % len(show), "| Tell (written answer; the bid team) | %d |" % len(tell),
         "| Must-have fit | %s%% (%s) |" % (mt["must_fit_pct"], mt["recommendation"]), "",
         "## 1. Build: every line needs a scene and a test", "",
         "Group these into 3–5 scenes around their journeys (and their named use cases, if the RFP has them). The plan's "
         "coverage table must list every ref below; `rfp.py coverage` checks it.", ""]
    by = collections.OrderedDict()
    for q in build:
        by.setdefault(q["section"] or "Other", []).append(q)
    for sec, qs in by.items():
        L += ["### %s" % sec, "", "| Ref | Requirement | How (fit) | Test (draft: the plan sharpens it) | Hours |", "|---|---|---|---|---|"]
        for q in qs:
            v = ver[q["rid"]]
            L.append("| %s | %s | %s (%s) | %s | %s |" % (q["rid"], short(eng(q)).replace("|", "/"), short(v.get("how"), 120).replace("|", "/"),
                                                     v.get("fit"), "they see it work live on their example data: " + short(v.get("how"), 80).replace("|", "/"),
                                                     v.get("hours") or ""))
        L.append("")
    L += ["## 2. Gaps to handle in the POC story", "",
          "Don't hide them: show the workaround or say how it's handled. These are the evaluator's likely questions.", "",
          "| Ref | Requirement | Fit | Workaround |", "|---|---|---|---|"]
    for q in mt["must_gaps"]:
        v = ver[q["rid"]]
        L.append("| %s | %s | %s | %s |" % (q["rid"], short(eng(q)).replace("|", "/"), FITS[v["fit"]]["label"], short(v.get("workaround"), 160).replace("|", "/")))
    if not mt["must_gaps"]:
        L.append("| | None | | |")
    L += ["", "## 3. Show: evidence to collect (library screenshots, clips, standard screens)", "",
          "| Ref | Requirement | Evidence |", "|---|---|---|"]
    for q in show:
        L.append("| %s | %s | %s |" % (q["rid"], short(eng(q), 110).replace("|", "/"), short(ver[q["rid"]].get("evidence"), 110).replace("|", "/")))
    qs = [q for q in ours if ver[q["rid"]].get("question")]
    L += ["", "## 4. Questions to settle before building", ""] + \
         ["- **%s**: %s" % (q["rid"], short(ver[q["rid"]]["question"], 220)) for q in qs] + \
         ["", "## 5. Low-confidence lines to confirm (product or SC)", ""] + \
         ["- **%s** (%s): %s" % (q["rid"], ver[q["rid"]]["fit"], short(eng(q), 140)) for q in mt["low_conf"]] + \
         ["", "SC check required before this is used with the customer or the bid team."]
    open(a.out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    json.dump({"deal": a.deal or reg.get("customer"), "build": [q["rid"] for q in build], "show": [q["rid"] for q in show],
               "gaps": [q["rid"] for q in mt["must_gaps"]]}, open(os.path.splitext(a.out)[0] + ".json", "w", encoding="utf-8"), indent=1)
    print("Build %d · Show %d · Tell %d · gaps %d -> %s" % (len(build), len(show), len(tell), len(mt["must_gaps"]), a.out))


def coverage(a):
    """Every Build ref must appear in the demo plan (and, once built, in the click path cards)."""
    brief = json.load(open(a.brief, encoding="utf-8"))
    texts = {}
    for f in a.files:
        texts[f] = open(f, encoding="utf-8", errors="replace").read()
    rows, missing = [], 0
    for rid in brief["build"] + brief["gaps"]:
        found = {os.path.basename(f): bool(re.search(r"(?<![\w-])%s(?![\w.])" % re.escape(rid), t)) for f, t in texts.items()}
        if not all(found.values()):
            missing += 1
        rows.append((rid, "gap" if rid in brief["gaps"] and rid not in brief["build"] else "build", found))
    print("%d of %d Build/gap refs missing from at least one file" % (missing, len(rows)))
    for rid, kind, found in rows:
        if not all(found.values()):
            print("  %-8s %-5s missing in: %s" % (rid, kind, ", ".join(k for k, v in found.items() if not v)))
    sys.exit(1 if missing else 0)


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("scan"); p.add_argument("file"); p.add_argument("--out")
    p = sp.add_parser("register"); p.add_argument("file"); p.add_argument("--map", required=True); p.add_argument("--out", required=True)
    p = sp.add_parser("fitgap"); p.add_argument("--register", required=True); p.add_argument("--verdicts", required=True)
    p.add_argument("--out", required=True); p.add_argument("--summary"); p.add_argument("--codes"); p.add_argument("--deal")
    p = sp.add_parser("check"); p.add_argument("--register", required=True); p.add_argument("--verdicts", required=True)
    p.add_argument("--out", required=True); p.add_argument("--xlsx")
    p = sp.add_parser("poc"); p.add_argument("--register", required=True); p.add_argument("--verdicts", required=True)
    p.add_argument("--out", required=True); p.add_argument("--deal")
    p = sp.add_parser("coverage"); p.add_argument("--brief", required=True); p.add_argument("files", nargs="+")
    a = ap.parse_args()
    {"scan": scan, "register": register, "fitgap": fitgap, "check": check, "poc": poc, "coverage": coverage}[a.cmd](a)


if __name__ == "__main__":
    main()
