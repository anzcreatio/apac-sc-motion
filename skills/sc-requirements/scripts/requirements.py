"""Business requirements checklist for sc-requirements. Writes only new files.

  python requirements.py build --master requirements-master.json --customer NN-requirements-checklist.xlsx
                               --internal NN-requirements-internal.xlsx
      Customer workbook (Read me, Requirements, Scoring) with no internal columns, and the internal workbook with
      the source, fit and differentiator for every line. Refuses to build when a check fails (exit 1).

Checks (errors stop the build; warnings print):
  - customer-facing text has no Creatio product terms and no competitor names (master "competitors")
  - Must lines are tagged C (the customer said it) with a high-confidence fit
  - no line has a fit we'd fail (custom, partner, roadmap, no)
  - every line has a requirement, why, priority and how to verify
  - 40-80 lines, and lines that favour us ("favours") are 15-35% (warnings)
"""
import argparse
import collections
import json
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
try:
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:
    sys.exit("openpyxl missing: python -m pip install openpyxl")

OUR_TERMS = ["Creatio", "Freedom UI", "Business Studio", "AI Studio", "AI Twin", "Creatio.ai", "clio", "no-code platform",
             "DCM", "Marketplace app", "Copilot"]
FAIL_FITS = {"custom", "partner", "roadmap", "no"}
PRIORITIES = ["Must", "Should", "Could"]
RESPONSES = ["Standard (out of the box)", "Configuration without code", "Custom code", "Third-party product", "Not available"]
CUSTOMER_COLS = [("Ref", "ref", 8), ("Area", "area", 18), ("Requirement", "requirement", 60), ("Why it matters", "why", 42),
                 ("Priority", "priority", 10), ("How to verify", "verify", 42), ("Vendor response", None, 24),
                 ("Vendor explanation", None, 40)]
SC_CHECK = "DRAFT. SC check required before this is used with the customer. Delete this line once checked."


def check(m):
    E, W = [], []
    banned = OUR_TERMS + list(m.get("competitors", []))
    lines = m["lines"]
    seen = set()
    for q in lines:
        r = q.get("ref") or "?"
        if r in seen:
            E.append("%s: duplicate ref" % r)
        seen.add(r)
        for k in ("area", "requirement", "why", "priority", "verify"):
            if not str(q.get(k) or "").strip():
                E.append("%s: no %s" % (r, k))
        if q.get("priority") not in PRIORITIES:
            E.append("%s: priority must be Must, Should or Could" % r)
        text = " ".join(str(q.get(k) or "") for k in ("area", "requirement", "why", "verify"))
        for t in banned:
            if re.search(r"(?i)(?<![\w-])%s(?![\w-])" % re.escape(t), text):
                E.append("%s: customer text names '%s'" % (r, t))
        i = q.get("internal") or {}
        if i.get("fit") in FAIL_FITS:
            E.append("%s: fit is %s: never put a requirement we'd fail in the checklist" % (r, i["fit"]))
        if q.get("priority") == "Must" and (i.get("tag") != "C" or i.get("confidence") != "high"):
            E.append("%s: Must needs tag C and high confidence (has %s / %s): make it Should or confirm it" % (r, i.get("tag"), i.get("confidence")))
        if not i.get("source"):
            W.append("%s: no source (quote, minute, or scene)" % r)
    for t in banned:
        for k in ("intro", "title"):
            if re.search(r"(?i)(?<![\w-])%s(?![\w-])" % re.escape(t), str(m.get(k) or "")):
                E.append("%s names '%s'" % (k, t))
    n = len(lines)
    if not 40 <= n <= 80:
        W.append("%d lines: aim for 40-80" % n)
    fav = sum(1 for q in lines if (q.get("internal") or {}).get("favours"))
    if n and not 0.15 <= fav / n <= 0.35:
        W.append("%d of %d lines favour us (%.0f%%): aim for 15-35%%, or it reads as rigged" % (fav, n, 100.0 * fav / n))
    return E, W


def style_header(ws, fill="0A0A0A"):
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(wrap_text=True, vertical="top")


def customer(m, path):
    wb = openpyxl.Workbook()
    rm = wb.active
    rm.title = "Read me"
    rows = [(SC_CHECK,), (m.get("title") or "Business requirements",), ("",)]
    rows += [(p,) for p in m.get("intro", [])]
    rows += [("",), ("How to respond",), ("For each requirement, choose one response and explain how it's met:",)]
    rows += [("- " + r,) for r in RESPONSES]
    rows += [("",), ("Priority: Must = needed to go live · Should = expected · Could = welcome if available.",),
             ("How to verify: what the vendor shows during evaluation. Where it says live, it's shown in the session, not in slides.",)]
    for r in rows:
        rm.append(list(r))
    rm["A1"].font = Font(bold=True, color="C00000")
    rm["A2"].font = Font(bold=True, size=14)
    rm.column_dimensions["A"].width = 120
    for row in rm.iter_rows():
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")

    ws = wb.create_sheet("Requirements")
    ws.append([c[0] for c in CUSTOMER_COLS])
    style_header(ws)
    area = None
    for q in m["lines"]:
        ws.append([q.get(k) if k else None for _, k, _ in CUSTOMER_COLS])
    for i, (_, _, w) in enumerate(CUSTOMER_COLS, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    dv = DataValidation(type="list", formula1='"%s"' % ",".join(RESPONSES), allow_blank=True)
    ws.add_data_validation(dv)
    dv.add("G2:G%d" % (len(m["lines"]) + 1))
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = ws.dimensions

    sc = wb.create_sheet("Scoring")
    sc.append(["Criterion", "Suggested weight", "What it means"])
    style_header(sc)
    for s in m.get("scoring", []):
        sc.append([s["criterion"], s["weight"], s["what"]])
    sc.append(["Total", "=SUM(B2:B%d)" % (len(m.get("scoring", [])) + 1), ""])
    sc.column_dimensions["A"].width = 34
    sc.column_dimensions["B"].width = 16
    sc.column_dimensions["C"].width = 90
    for row in sc.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.active = 1
    wb.save(path)


def internal(m, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Internal (never send)"
    cols = ["Ref", "Area", "Requirement", "Priority", "Tag", "Source", "Demo scene", "Register ref", "Fit", "Confidence",
            "Differentiator", "Why it favours us"]
    ws.append(cols)
    style_header(ws, "FF4013")
    for q in m["lines"]:
        i = q.get("internal") or {}
        ws.append([q["ref"], q["area"], q["requirement"], q["priority"], i.get("tag"), i.get("source"), i.get("scene"),
                   i.get("register"), i.get("fit"), i.get("confidence"), i.get("diff"), i.get("favours")])
    for col, w in zip("ABCDEFGHIJKL", [8, 18, 60, 9, 6, 30, 30, 10, 12, 11, 12, 50]):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = ws.dimensions
    s = wb.create_sheet("Summary")
    lines = m["lines"]
    pr = collections.Counter(q["priority"] for q in lines)
    fits = collections.Counter((q.get("internal") or {}).get("fit") for q in lines)
    tags = collections.Counter((q.get("internal") or {}).get("tag") for q in lines)
    fav = sum(1 for q in lines if (q.get("internal") or {}).get("favours"))
    for k, v in [("Customer", m.get("customer")), ("Lines", len(lines)), ("Must / Should / Could", "%d / %d / %d" % (pr["Must"], pr["Should"], pr["Could"])),
                 ("Tags C / I / A", "%d / %d / %d" % (tags["C"], tags["I"], tags["A"])), ("Lines that favour us", "%d (%.0f%%)" % (fav, 100.0 * fav / max(1, len(lines))))] + \
            [("Fit: %s" % k, v) for k, v in fits.most_common()]:
        s.append([k, v])
    s.column_dimensions["A"].width = 30
    s.column_dimensions["B"].width = 30
    wb.save(path)


def build(a):
    m = json.load(open(a.master, encoding="utf-8"))
    E, W = check(m)
    for w in W:
        print("WARNING", w)
    if E:
        print("%d errors, nothing built:" % len(E))
        for e in E:
            print("  " + e)
        sys.exit(1)
    customer(m, a.customer)
    internal(m, a.internal)
    pr = collections.Counter(q["priority"] for q in m["lines"])
    print("Built %d requirements (Must %d, Should %d, Could %d) -> %s and %s" % (
        len(m["lines"]), pr["Must"], pr["Should"], pr["Could"], a.customer, a.internal))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("build")
    p.add_argument("--master", required=True)
    p.add_argument("--customer", required=True)
    p.add_argument("--internal", required=True)
    a = ap.parse_args()
    build(a)


if __name__ == "__main__":
    main()
