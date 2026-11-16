"""Bill of materials (BOM) for a Creatio APAC deal: which products (SKUs) the solution needs, and the gotchas.

INTERNAL ONLY. No prices, no users per module (log item 74). The AE and Deal Desk own price and user counts.

  python bom.py new       <deal folder>                      # writes <deal>/bom.json from the catalogue
  python bom.py check     <deal>/bom.json [--final]          # rules; exit 1 on errors (--final: every line decided)
  python bom.py tier      [--revenue 120] [--aum 900] [--employees 650]   # USD millions; prints the candidate tier
  python bom.py questions <deal>/bom.json [--max 6]          # open sizing questions as ae-brief.json "licence" entries
  python bom.py build     <deal>/bom.json --nn 20 [--draft]  # <deal>/NN-bom.md + NN-bom.xlsx (runs check first)

Catalogue: ../../knowledge/BOM-CATALOGUE-v0.1.json. Template: ../templates/BOM-TEMPLATE-v0.2.xlsx.
Team gotchas (from /sc-lessons): SharePoint Lessons/registers/bom-gotchas.json, read when ~/.apac-sc-motion.json
has "sharepoint_root" (or --root).
"""
import argparse
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
CATALOGUE = os.path.join(PLUGIN, "knowledge", "BOM-CATALOGUE-v0.1.json")
TEMPLATE = os.path.join(HERE, "..", "templates", "BOM-TEMPLATE-v0.2.xlsx")

NEEDED = ("Yes", "No", "TBC")
TAGS = ("C", "P", "I", "A")
GOTCHA_STATUS = ("Covered", "Needs quote", "Ask customer", "N/A")
FACTS = [  # key, label in the template's Deal sheet (column A), allowed values
    ("customer", "Customer", None),
    ("legal_entity", "Legal entity that will use the platform", None),
    ("group", "Group / holding company", None),
    ("country", "Country", None),
    ("hosting_region", "Hosting region required", None),
    ("commercial_model", "Commercial model", ("Unlimited", "Per seat")),
    ("per_seat_reason", "If per seat: why Unlimited can't be accepted", None),
    ("studio_edition", "Studio edition (per seat only)", ("Growth", "Enterprise")),
    ("revenue_musd", "Annual revenue (USD millions)", None),
    ("aum_musd", "AUM (USD millions, BFSI only)", None),
    ("employees", "Total employees", None),
    ("existing_customer", "Existing Creatio customer?", ("Yes", "No")),
    ("deployment", "Deployment", ("Cloud", "On-premise")),
]
NUMERIC = ("revenue_musd", "aum_musd", "employees")
# A currency amount is a price unless it's a size (bn / m / million / billion: AUM, a loan book, revenue)
PRICE_RX = re.compile(r"(\$|\bAUD\b|\bUSD\b|\bIDR\b|\bRp\b|\bSGD\b)\s?(\d[\d,]*(\.\d+)?)(?!\s?(bn|b|m|mn|million|billion|trillion|t)\b)(?![\d,]|\.\d)", re.I)
EXTRA = ("NOT", "Beyond", "TO CONFIRM")  # in_unlimited values that mean "quote it on top"
USERS_RX = re.compile(r"\b\d[\d,]*\s*(named\s+)?(users?|seats?|licen[cs]es?)\b", re.I)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def load_json(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def save_json(p, data):
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, p)


def catalogue():
    return load_json(CATALOGUE)


def team_gotchas(root_arg):
    root = root_arg
    if not root:
        try:
            root = load_json(os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json")).get("sharepoint_root")
        except (OSError, ValueError):
            root = None
    if not root:
        return []
    p = os.path.join(root, "Lessons", "registers", "bom-gotchas.json")
    if not os.path.exists(p):
        return []
    return [e for e in load_json(p).get("entries", []) if e.get("status") == "open"]


# ---------- tier ----------

def tier_of(cat, revenue=None, aum=None, employees=None):
    """Same as the template: tier = count of tier upper bounds below the value, plus one; highest of the three."""
    t = [r for r in cat["tiers"] if r["tier"] <= 6]
    parts = {}
    if revenue not in (None, ""):
        parts["revenue"] = sum(1 for r in t if r["revenue_upper_musd"] < float(revenue)) + 1
    if aum not in (None, ""):
        parts["aum"] = sum(1 for r in t if r["aum_upper_musd"] < float(aum)) + 1
    if employees not in (None, ""):
        parts["employees"] = sum(1 for r in t if r["max_employees"] < float(employees)) + 1
    if not parts:
        return None, parts, {}
    tier = max(parts.values())
    row = next(r for r in cat["tiers"] if r["tier"] == tier)
    emp = row["max_employees"]
    incl = {"dedicated_blocks": row["dedicated_blocks"],
            "db_storage_gb": 2 * emp if isinstance(emp, (int, float)) else "Custom",
            "file_storage_gb": 2 * emp if isinstance(emp, (int, float)) else "Custom"}
    return tier, parts, incl


# ---------- bom.json ----------

def fact(bom, key):
    v = bom.get("deal_facts", {}).get(key) or {}
    return v.get("value") if isinstance(v, dict) else v


def line(bom, sid):
    return bom.get("lines", {}).get(sid) or {}


def wanted(bom, sid):
    return line(bom, sid).get("needed") in ("Yes", "TBC")


def flags(bom):
    model = fact(bom, "commercial_model") or "Unlimited"
    return {
        "all": True,
        "unlimited": model == "Unlimited",
        "per_seat": model == "Per seat",
        "growth": model == "Per seat" and fact(bom, "studio_edition") == "Growth",
        "group": bool(fact(bom, "group")),
        "existing": fact(bom, "existing_customer") == "Yes",
        "ai": any(wanted(bom, s) for s in ("A1", "A2", "A3")),
        "byo_ai": wanted(bom, "A3"),
        "large_volume": wanted(bom, "I3") or wanted(bom, "I4") or wanted(bom, "I2"),
        "onprem_systems": wanted(bom, "I7"),
        "connector": any(wanted(bom, s) for s in ("M1", "M2", "M3")),
    }


def applicable(gotcha, fl):
    return any(fl.get(a) for a in gotcha.get("applies", ["all"]))


def new_bom(cat, deal_dir):
    p = os.path.join(deal_dir, "bom.json")
    if os.path.exists(p):
        sys.exit("%s already exists: edit it, don't recreate it" % p)
    bom = {
        "bom": "sc-bom", "catalogue_version": cat["version"], "deal": os.path.basename(os.path.normpath(deal_dir)),
        "updated": datetime.date.today().isoformat(), "sc": "", "ae": "",
        "inputs": [],
        "deal_facts": {k: {"value": "Unlimited" if k == "commercial_model" else "", "tag": "A" if k == "commercial_model" else "", "source": ""}
                       for k, _, _ in FACTS},
        "deal_desk_validated": {"value": "No", "who_when": ""},
        "lines": {s["id"]: {"needed": "", "why": "", "tag": "", "qty": None} for s in cat["skus"]},
        "gotchas": {g["id"]: {"status": "", "answer": ""} for g in cat["gotchas"]},
        "team_gotchas": {},
        "sizing": {q["id"]: {"answer": "", "tag": ""} for q in cat["sizing_questions"]},
        "notes": [],
    }
    for m in ("M1", "M2", "M3"):
        bom["lines"][m]["name"] = ""
    save_json(p, bom)
    return p


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def check(cat, bom, final=False, team=None):
    err, warn = [], []
    skus = {s["id"]: s for s in cat["skus"]}
    for t in strings({k: v for k, v in bom.items() if k != "deal_facts"}):
        if PRICE_RX.search(t):
            err.append("Price found (never in a BOM): %r" % t[:80])
        if USERS_RX.search(t):
            err.append("User count found (AE and Deal Desk own user numbers; say 'sizing: ask'): %r" % t[:80])
    for k, label, allowed in FACTS:
        v = fact(bom, k)
        if allowed and v and v not in allowed:
            err.append("Deal fact %s = %r, expected one of %s" % (k, v, "/".join(allowed)))
        if k in NUMERIC and v not in (None, ""):
            try:
                float(v)
            except (TypeError, ValueError):
                err.append("Deal fact %s must be a number in USD millions (or a head count), got %r" % (k, v))
        tg = (bom.get("deal_facts", {}).get(k) or {}).get("tag") if isinstance(bom.get("deal_facts", {}).get(k), dict) else None
        if v not in (None, "") and tg not in TAGS:
            warn.append("Deal fact %s has no evidence tag (C/P/I/A)" % k)
    if fact(bom, "commercial_model") == "Per seat" and not fact(bom, "per_seat_reason"):
        err.append("Per seat needs the reason Unlimited can't be accepted (per_seat_reason)")
    if fact(bom, "deployment") == "On-premise" and fact(bom, "studio_edition") == "Growth":
        err.append("Growth is cloud only: on-premise needs Enterprise or Unlimited (G14)")
    for sid, ln in bom.get("lines", {}).items():
        if sid not in skus:
            err.append("Unknown SKU id %s (not in the catalogue)" % sid)
            continue
        n = ln.get("needed", "")
        if n and n not in NEEDED:
            err.append("%s needed = %r, expected Yes/No/TBC" % (sid, n))
        if final and not n:
            err.append("%s %s: not decided (Yes/No/TBC)" % (sid, skus[sid]["name"]))
        if n in ("Yes", "TBC"):
            if not (ln.get("why") or "").strip():
                err.append("%s %s is %s with no reason (a requirement, pain or demo scene)" % (sid, skus[sid]["name"], n))
            if ln.get("tag") not in TAGS:
                err.append("%s %s is %s with no evidence tag C/P/I/A" % (sid, skus[sid]["name"], n))
            if n == "Yes" and ln.get("tag") == "A" and sid != "P1":  # P1 Yes is the default model
                warn.append("%s is Yes on an assumption (A): make it TBC or ask" % sid)
            if sid.startswith("M") and not (ln.get("name") or "").strip():
                err.append("%s: name the Marketplace app or connector" % sid)
        if ln.get("qty") not in (None, "") and not skus[sid].get("qty_unit"):
            err.append("%s: qty only for non-user items (blocks, GB, environments); this line has none" % sid)
    for r in cat["requires"]:
        if line(bom, r["if"]).get("needed") != "Yes":
            continue
        for t in r.get("then", []):
            if not wanted(bom, t):
                err.append("%s is Yes, so %s must be Yes or TBC: %s" % (r["if"], t, r["why"]))
        if r.get("then_any") and not any(wanted(bom, t) for t in r["then_any"]):
            err.append("%s is Yes, so one of %s must be Yes or TBC: %s" % (r["if"], "/".join(r["then_any"]), r["why"]))
        for t in r.get("then_not", []):
            if line(bom, t).get("needed") == "Yes":
                err.append("%s and %s are both Yes: %s" % (r["if"], t, r["why"]))
    fl = flags(bom)
    for g in cat["gotchas"]:
        st = (bom.get("gotchas", {}).get(g["id"]) or {}).get("status", "")
        if st and st not in GOTCHA_STATUS:
            err.append("Gotcha %s status %r, expected %s" % (g["id"], st, " / ".join(GOTCHA_STATUS)))
        if applicable(g, fl) and not st:
            (err if final else warn).append("Gotcha %s applies (%s) and has no status" % (g["id"], g["area"]))
    for e in team or []:
        st = (bom.get("team_gotchas", {}).get(e["id"]) or {}).get("status", "")
        if not st:
            warn.append("Team gotcha %s (%s): check it and set a status" % (e["id"], e.get("area")))
    return err, warn


def open_questions(cat, bom):
    """Open sizing questions worth asking, most useful first: tier and entity; then lines that cost extra (not in
    Unlimited, beyond the tier); then TBC scope lines; last, lines already covered. Within each, by evidence C, P, I, A.
    An answer counts only when the customer or a partner gave it (C or P); research (I) or a guess (A) is confirmed.
    The hint quotes the customer only for C or P lines."""
    rank_tag = {"C": 0, "P": 1, "I": 2, "A": 3}
    skus = {s["id"]: s for s in cat["skus"]}
    fl = flags(bom)
    out = []
    for q in cat["sizing_questions"]:
        a = bom.get("sizing", {}).get(q["id"]) or {}
        if a.get("answer") and a.get("tag") in ("C", "P"):
            continue
        linked = [s for s in q["skus"] if wanted(bom, s)]
        def firm(k):  # a size fact the customer or a partner gave us
            d = bom.get("deal_facts", {}).get(k) or {}
            return d.get("value") not in (None, "") and d.get("tag") in ("C", "P")
        if q["id"] == "SQ01":
            need = not (firm("revenue_musd") or firm("aum_musd"))
            size = fact(bom, "aum_musd") or fact(bom, "revenue_musd")
            if size and not a.get("answer"):
                a = {"answer": "USD %sm from research" % size, "tag": "I"}
        elif q["id"] == "SQ02":
            need = not firm("employees")  # tier = highest of size and employees: always ask both
        elif q["id"] == "SQ03":
            need = fl["group"]
        else:
            need = bool(linked)
        if not need:
            continue
        def weight(s):
            ln, extra = line(bom, s), str(skus[s]["in_unlimited"]).startswith(EXTRA) or not fl["unlimited"]
            band = 1 if extra else (5 if ln.get("needed") == "TBC" else 10)
            return band + rank_tag.get(ln.get("tag"), 3)
        score = 0 if q["id"] in ("SQ01", "SQ02", "SQ03") else min(weight(s) for s in linked)
        hint = ""
        if a.get("answer"):
            hint = "We have %s (%s): confirm" % (a["answer"], a.get("tag") or "A")
        for s in sorted(linked, key=lambda s: rank_tag.get(line(bom, s).get("tag"), 3)):
            ln = line(bom, s)
            if not hint and ln.get("why") and ln.get("tag") in ("C", "P"):
                hint = "We heard: " + ln["why"]
                break
        out.append((score, {"id": q["id"], "q": q["ae_wording"], "hint": hint or q["why"]}))
    return [o for _, o in sorted(out, key=lambda t: t[0])]


# ---------- outputs ----------

def md(cat, bom, team):
    skus = {s["id"]: s for s in cat["skus"]}
    tier, parts, incl = tier_of(cat, fact(bom, "revenue_musd"), fact(bom, "aum_musd"), fact(bom, "employees"))
    fl = flags(bom)
    L = ["# Bill of materials: %s" % (fact(bom, "customer") or bom.get("deal")), "",
         "> **INTERNAL ONLY.** Never send to a customer or partner. No prices and no users per module: the AE and Deal Desk own the quote.",
         "", "Updated %s · catalogue v%s · SC %s · AE %s" % (bom.get("updated"), cat["version"], bom.get("sc") or "?", bom.get("ae") or "?"), ""]
    L += ["## 1. The deal", "", "| | | Tag |", "|---|---|---|"]
    for k, label, _ in FACTS:
        v = fact(bom, k)
        if v in (None, ""):
            continue
        tg = (bom["deal_facts"].get(k) or {}).get("tag", "")
        L.append("| %s | %s | %s |" % (label, v, tg))
    if tier:
        why = ", ".join("%s → tier %d" % (k, v) for k, v in parts.items())
        L.append("| **Candidate tier** | **Tier %d** (highest of: %s). Includes %s dedicated blocks, %s GB database + %s GB file storage (OPEN-2) | |"
                 % (tier, why, incl["dedicated_blocks"], incl["db_storage_gb"], incl["file_storage_gb"]))
    else:
        L.append("| **Candidate tier** | Unknown: we need revenue (or AUM) or employees | |")
    dd = bom.get("deal_desk_validated", {})
    L.append("| Deal Desk validated the tier? | %s %s | |" % (dd.get("value", "No"), dd.get("who_when", "")))
    L.append("")

    def rows(pred):
        r = []
        for s in cat["skus"]:
            ln = line(bom, s["id"])
            if pred(s, ln):
                name = ln.get("name") and "%s: %s" % (s["name"].split(" (")[0], ln["name"]) or s["name"]
                q = ("%s %s" % (ln["qty"], s.get("qty_unit") or "")) if ln.get("qty") not in (None, "") else ""
                r.append("| %s | %s | %s | %s | %s | %s |" % (s["id"], name, s["in_unlimited"] if fl["unlimited"] else s["model"],
                                                         ln.get("why", ""), ln.get("tag", ""), q))
        return r
    hdr = ["| ID | Product (SKU) | %s | Why | Tag | Qty |" % ("In Unlimited?" if fl["unlimited"] else "Model"), "|---|---|---|---|---|---|"]
    yes = rows(lambda s, ln: ln.get("needed") == "Yes")
    L += ["## 2. Products they need", ""] + (hdr + yes if yes else ["Nothing marked Yes yet."]) + [""]
    is_extra = lambda s: fl["unlimited"] and str(s["in_unlimited"]).startswith(EXTRA)
    extra = rows(lambda s, ln: ln.get("needed") in ("Yes", "TBC") and is_extra(s))
    L += ["## 3. Extra to quote (not in Unlimited, or beyond the tier; Yes and TBC)", ""] + (hdr + extra if extra else ["Nothing extra so far."]) + [""]
    tbc = rows(lambda s, ln: ln.get("needed") == "TBC" and not is_extra(s))
    L += ["## 4. Not decided yet (TBC, other than the extras above)", ""] + (hdr + tbc if tbc else ["Nothing open."]) + [""]
    L += ["## 5. Gotchas that apply", "", "| ID | Area | Gotcha | Status | Answer / what we did |", "|---|---|---|---|---|"]
    for g in cat["gotchas"]:
        if applicable(g, fl):
            st = bom.get("gotchas", {}).get(g["id"], {})
            L.append("| %s | %s | %s | %s | %s |" % (g["id"], g["area"], g["text"], st.get("status") or "**no status**", st.get("answer", "")))
    for e in team:
        st = bom.get("team_gotchas", {}).get(e["id"], {})
        L.append("| %s (team) | %s | %s | %s | %s |" % (e["id"], e.get("area", ""), e.get("gotcha", ""), st.get("status") or "**no status**", st.get("answer", "")))
    L += ["", "## 6. Open with Deal Desk", ""] + ["- **%s** %s" % (o["id"], o["text"]) for o in cat["open_items"]] + [""]
    qs = open_questions(cat, bom)
    L += ["## 7. Ask the customer next time (the AE brief takes these)", ""]
    L += ["%d. %s  _(%s)_" % (i, q["q"], q["hint"]) for i, q in enumerate(qs, 1)] if qs else ["Nothing open."]
    answered = [(q, bom["sizing"][q["id"]]) for q in cat["sizing_questions"] if (bom.get("sizing", {}).get(q["id"]) or {}).get("answer")]
    if answered:
        L += ["", "Noted so far (only C or P answers count as answered):", ""] + ["- %s: %s (%s)" % (q["question"], a["answer"], a.get("tag", "")) for q, a in answered]
    L += ["", "## 8. What the AE does next", "",
          "1. Send this BOM (the .xlsx) to Deal Desk: they validate the tier and build the quote with the user numbers.",
          "2. Never give the customer a number before the quote is approved (the CEO approves every Unlimited quote).",
          "3. AI always needs an AI Package on top, also on Unlimited.",
          "4. Questions about a product line: ask the SC, not the customer.", ""]
    if bom.get("inputs"):
        L += ["## Sources used", ""] + ["- %s" % i for i in bom["inputs"]] + [""]
    L += ["SC check required before this is used with the customer."]
    return "\n".join(L) + "\n"


def xlsx(cat, bom, team, out):
    try:
        import openpyxl
    except ImportError:
        sys.exit("openpyxl missing: python -m pip install --user openpyxl (sc-setup)")
    wb = openpyxl.load_workbook(TEMPLATE)
    ws = wb["Deal"]
    rows = {c.value: c.row for c in ws["A"] if c.value}
    for k, label, _ in FACTS:
        d = bom.get("deal_facts", {}).get(k) or {}
        v = d.get("value")
        if v not in (None, ""):
            ws.cell(rows[label], 2).value = float(v) if k in NUMERIC else v
            ws.cell(rows[label], 3).value = d.get("tag") or None
            if d.get("source"):
                ws.cell(rows[label], 4).value = d["source"]
    dd = bom.get("deal_desk_validated", {})
    ws.cell(rows["Deal Desk validated the tier?"], 2).value = dd.get("value", "No")
    if dd.get("who_when"):
        ws.cell(rows["Deal Desk validated the tier?"], 4).value = dd["who_when"]
    ws = wb["SKUs"]
    rows = {c.value: c.row for c in ws["A"] if c.value}
    for sid, ln in bom.get("lines", {}).items():
        r = rows[sid]
        if ln.get("name"):
            ws.cell(r, 3).value = "Marketplace: %s" % ln["name"]
        for col, key in ((7, "needed"), (8, "qty"), (10, "why"), (11, "tag")):
            if ln.get(key) not in (None, ""):
                ws.cell(r, col).value = ln[key]
    ws = wb["Gotchas"]
    rows = {c.value: c.row for c in ws["A"] if c.value}
    for gid, st in bom.get("gotchas", {}).items():
        if st.get("status"):
            ws.cell(rows[gid], 6).value = st["status"]
        if st.get("answer"):
            ws.cell(rows[gid], 7).value = st["answer"]
    if team:
        r = ws.max_row + 2
        ws.cell(r, 1).value = "Team gotchas (from /sc-lessons, SharePoint Lessons/registers/bom-gotchas.json)"
        for e in team:
            r += 1
            st = bom.get("team_gotchas", {}).get(e["id"], {})
            for col, v in enumerate((e["id"], e.get("area"), e.get("gotcha"), e.get("applies_when"), e.get("question"),
                                     st.get("status"), st.get("answer"), e.get("source_ref")), 1):
                ws.cell(r, col).value = v
    ws = wb["Sizing questions"]
    for i, q in enumerate(cat["sizing_questions"]):
        a = bom.get("sizing", {}).get(q["id"]) or {}
        if a.get("answer"):
            ws.cell(5 + i, 4).value = a["answer"]
            ws.cell(5 + i, 5).value = a.get("tag") or None
    summary(cat, bom, wb["Summary for the AE"])
    wb.save(out)


def summary(cat, bom, ws):
    """Rewrite the AE's Summary from section 2 down. The v0.2 template's formulas had fixed slots (10/6/8/8) and
    counted only "NOT included" as extra, so storage, VPN, region and blocks fell off (found on Navalo, 16 Nov 2026).
    Section 1 keeps its formulas (customer, entity, model, tier)."""
    from copy import copy
    from openpyxl.styles import Border, Font, PatternFill, Side
    thin = Side(style="thin", color="BFBFBF")
    head_font, head_fill = copy(ws.cell(4, 2).font), copy(ws.cell(4, 2).fill)
    item_font = Font(size=10)
    border = Border(top=thin, bottom=thin, left=thin, right=thin)
    for rng in [r for r in ws.merged_cells.ranges if r.min_row >= 11]:
        ws.unmerge_cells(str(rng))
    for r in range(11, ws.max_row + 1):
        for c in (2, 3):
            cell = ws.cell(r, c)
            cell.value, cell.font, cell.fill, cell.border = None, Font(size=10), PatternFill(), Border()
    ws.cell(2, 2).value = ("INTERNAL ONLY. Generated by sc-bom from bom.json on %s: don't edit, ask the SC to rebuild. "
                           "No prices here: Deal Desk quotes." % bom.get("updated", ""))
    skus = {s["id"]: s for s in cat["skus"]}
    fl = flags(bom)
    is_extra = lambda s: fl["unlimited"] and str(skus[s]["in_unlimited"]).startswith(EXTRA)

    def name(sid):
        ln = line(bom, sid)
        return "Marketplace: %s" % ln["name"] if ln.get("name") else skus[sid]["name"]

    order = [s["id"] for s in cat["skus"]]
    yes = [name(s) for s in order if line(bom, s).get("needed") == "Yes"]
    extra = [name(s) + ("" if line(bom, s).get("needed") == "Yes" else "  (TBC)") for s in order
             if line(bom, s).get("needed") in ("Yes", "TBC") and is_extra(s)]
    tbc = [name(s) for s in order if line(bom, s).get("needed") == "TBC" and not is_extra(s)]
    asks = ["%s  (%s)" % (q["q"], q["hint"]) for q in open_questions(cat, bom)]
    nxt = ["1. Send this file to Deal Desk with the user numbers by role: they check the tier and build the quote.",
           "2. Never give the customer a number before the quote is approved (the CEO approves every Unlimited quote).",
           "3. AI always needs an AI Package on top, also with Unlimited.",
           "4. Questions about a product line? Ask the SC, not the customer."]
    opens = ["%s: %s" % (o["id"], o["text"]) for o in cat["open_items"]]
    sections = [("2. Products they need (Yes)", yes or ["None marked Yes yet"]),
                ("3. Extra to quote: not in Unlimited, or beyond the tier", extra or ["Nothing extra so far"]),
                ("4. Not decided yet (TBC)", tbc or ["Nothing open"]),
                ("5. Ask the customer next time", asks or ["Nothing open"]),
                ("6. What you do next", nxt),
                ("7. Open with Deal Desk (don't answer these yourself)", opens)]
    r = 11
    for title, items in sections:
        for c in (2, 3):
            h = ws.cell(r, c)
            h.font, h.fill, h.border = copy(head_font), copy(head_fill), border
        ws.cell(r, 2).value = title
        r += 1
        for it in items:
            ws.cell(r, 2).value = it
            for c in (2, 3):
                ws.cell(r, c).font, ws.cell(r, c).border = item_font, border
            ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
            r += 1
        r += 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", help="SharePoint team root (default from ~/.apac-sc-motion.json)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new"); n.add_argument("deal")
    c = sub.add_parser("check"); c.add_argument("bom"); c.add_argument("--final", action="store_true")
    t = sub.add_parser("tier")
    for k in ("--revenue", "--aum", "--employees"):
        t.add_argument(k, type=float)
    q = sub.add_parser("questions"); q.add_argument("bom"); q.add_argument("--max", type=int, default=6)
    b = sub.add_parser("build"); b.add_argument("bom"); b.add_argument("--nn", required=True)
    b.add_argument("--draft", action="store_true", help="build even with errors (marked DRAFT)")
    x = ap.parse_args()
    cat = catalogue()

    if x.cmd == "new":
        print("wrote", new_bom(cat, x.deal))
        return
    if x.cmd == "tier":
        tier, parts, incl = tier_of(cat, x.revenue, x.aum, x.employees)
        print(json.dumps({"candidate_tier": tier, "by": parts, "included": incl}, indent=1))
        return
    bom = load_json(x.bom)
    team = team_gotchas(x.root)
    if x.cmd == "questions":
        print(json.dumps([{"q": i["q"], "hint": i["hint"]} for i in open_questions(cat, bom)[:x.max]], ensure_ascii=False, indent=1))
        return
    err, warn = check(cat, bom, final=(x.cmd == "check" and x.final), team=team)
    for w in warn:
        print("WARN ", w)
    for e in err:
        print("ERROR", e)
    if x.cmd == "check":
        print("%d errors, %d warnings" % (len(err), len(warn)))
        sys.exit(1 if err else 0)
    if err and not x.draft:
        sys.exit("Fix the errors above, or build with --draft")
    deal = os.path.dirname(os.path.abspath(x.bom))
    base = os.path.join(deal, "%s-bom" % x.nn)
    text = md(cat, bom, team)
    if err:
        text = "> **DRAFT: %d rule errors still open** (run `bom.py check`).\n\n" % len(err) + text
    with open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write(text)
    xlsx(cat, bom, team, base + ".xlsx")
    print("wrote", base + ".md")
    print("wrote", base + ".xlsx")


if __name__ == "__main__":
    main()
