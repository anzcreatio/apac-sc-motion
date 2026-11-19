"""Clarification questions for sc-rfp: one JSON -> a working sheet for the SC and a customer sheet.

  python clarify.py build --questions rfp/clarifications.json --working rfp/NN-questions-working-<date>.xlsx
                          --customer rfp/NN-<Vendor>-clarification-questions-<Customer>-<date>.xlsx
  python clarify.py read  <customer-or-working.xlsx> [--out edited.json]
      Read a sheet back (after the SC edited it) as JSON, so the changes can be merged into clarifications.json.

clarifications.json:
  {"title": "Navalo RFP: clarification questions from Creatio",
   "subtitle": "RFP: ..., issued 18 November 2026. Sent 20 November 2026.",
   "answer_label": "Navalo's answer", "first": "1 to 4",
   "questions": [{"group": 1, "topic": "How you'll assess responses", "criteria": "Parts A, B, C",
                  "question": "Customer wording, with the one-sentence reason inline where it helps.",
                  "need": "internal: what would help us", "why": "internal: why we ask",
                  "dropped": false, "drop_reason": ""}]}

Numbers (1a, 1b, 2a...) are worked out from group order every build, so cuts and additions never leave gaps.
Rules for the wording: standards/CUSTOMER-QUESTIONS-v0.1.md.
"""
import argparse
import json
import string
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
try:
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:
    sys.exit("openpyxl missing: python -m pip install openpyxl")

NAVY, BAND, YELLOW = "1F2A44", "F2F4F8", "FFF2CC"
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def number(qs):
    """Give live questions 1a, 1b, 2a... in group order; dropped ones get no number."""
    order, seen = [], {}
    for q in qs:
        if q.get("dropped"):
            continue
        g = q["group"]
        if g not in seen:
            seen[g] = len(order) + 1
            order.append(g)
    count = {}
    for q in qs:
        if q.get("dropped"):
            q["no"] = ""
            continue
        n = seen[q["group"]]
        k = count.get(n, 0)
        count[n] = k + 1
        q["no"] = "%d%s" % (n, string.ascii_lowercase[k])
    return qs


def sheet(ws, data, cols, widths, rows, how):
    f = lambda **k: Font(name="Arial", size=10, **k)
    last = openpyxl.utils.get_column_letter(len(cols))
    ws["A1"] = data["title"]
    ws["A1"].font = Font(name="Montserrat", bold=True, size=14, color=NAVY)
    ws["A2"] = data.get("subtitle", "")
    ws["A2"].font = f(italic=True)
    ws["A3"] = how
    ws["A3"].font = f()
    for r in (1, 2, 3):
        ws.merge_cells("A%d:%s%d" % (r, last, r))
        ws["A%d" % r].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[3].height = 44
    ws.append(cols)
    for i in range(1, len(cols) + 1):
        c = ws.cell(row=4, column=i)
        c.fill = PatternFill("solid", fgColor=NAVY)
        c.font = f(bold=True, color="FFFFFF")
        c.border = BOX
        c.alignment = Alignment(vertical="center", wrap_text=True)
    ans = cols.index(data.get("answer_label", "Answer")) + 1
    prev, shade = None, False
    for g, vals in rows:
        if g != prev:
            shade, prev = not shade, g
        ws.append(vals)
        r = ws.max_row
        longest = max(sum(len(p) // 60 + 1 for p in str(v or "").split("\n")) for v in vals)
        ws.row_dimensions[r].height = max(26, 13.5 * longest + 4)
        for i, c in enumerate(ws[r], 1):
            c.alignment = Alignment(vertical="top", wrap_text=True)
            c.border = BOX
            c.font = f(bold=(i == 1))
            if i == ans:
                c.fill = PatternFill("solid", fgColor=YELLOW)
            elif shade:
                c.fill = PatternFill("solid", fgColor=BAND)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    ws.freeze_panes = "C5"
    ws.auto_filter.ref = "A4:%s%d" % (last, ws.max_row)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.print_title_rows = "4:4"


def build(a):
    data = json.load(open(a.questions, encoding="utf-8"))
    qs = number(data["questions"])
    label = data.get("answer_label", "Answer")
    first = data.get("first")
    tail = (" Questions %s affect how we put the whole response together, so those help most if answered first." % first) if first else ""
    live = [q for q in qs if not q.get("dropped")]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Questions"
    sheet(ws, data, ["#", "Criterion IDs", "Our question", label], [6, 18, 70, 46],
          [(q["group"], [q["no"], q.get("criteria", ""), q["question"], ""]) for q in live],
          "How to use this sheet: each row is one question, and a short answer is fine. Please add your answer in the "
          "\"%s\" column. If a question doesn't apply, or you'd rather talk it through, just say so there.%s" % (label, tail))
    wb.save(a.customer)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Working"
    cols = ["#", "Topic", "Criterion IDs", "Our question (customer wording)", "What would help us", "Why we're asking (internal)",
            "Status", label, "Dropped?"]
    sheet(ws, data, cols, [6, 18, 16, 60, 40, 34, 13, 40, 22],
          [(q["group"], [q["no"], q.get("topic", ""), q.get("criteria", ""), q["question"], q.get("need", ""), q.get("why", ""),
                         q.get("status", "Open"), q.get("answer", ""),
                         ("Dropped: " + q.get("drop_reason", "")) if q.get("dropped") else ""]) for q in qs],
          "Internal working sheet: never send. The customer sheet is built from the same JSON (clarify.py build).")
    dv = DataValidation(type="list", formula1='"Open,Answered,Partly answered"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add("G5:G%d" % ws.max_row)
    wb.save(a.working)
    print("%d questions in %d groups (%d dropped) -> %s, %s" % (len(live), len({q["group"] for q in live}), len(qs) - len(live),
                                                                 a.customer, a.working))


def read(a):
    ws = openpyxl.load_workbook(a.file, data_only=True).active
    head = [c.value for c in ws[4]]
    out = []
    for r in ws.iter_rows(min_row=5, values_only=True):
        if any(v not in (None, "") for v in r):
            out.append({str(h): v for h, v in zip(head, r) if h})
    js = json.dumps(out, indent=1, ensure_ascii=False)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(js)
    print(js if not a.out else "%d rows -> %s" % (len(out), a.out))


def main():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="cmd", required=True)
    b = s.add_parser("build")
    b.add_argument("--questions", required=True)
    b.add_argument("--working", required=True)
    b.add_argument("--customer", required=True)
    r = s.add_parser("read")
    r.add_argument("file")
    r.add_argument("--out")
    a = p.parse_args()
    {"build": build, "read": read}[a.cmd](a)


if __name__ == "__main__":
    main()
