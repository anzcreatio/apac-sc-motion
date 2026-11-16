"""Checks for sc-bom on a fictional deal (no customer data). Run after any change to bom.py or the catalogue:

  python tests/bom/test_bom.py

Builds into a temp folder; prints PASS or the failures.
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SCRIPT = os.path.join(ROOT, "skills", "sc-bom", "scripts", "bom.py")
sys.path.insert(0, os.path.dirname(SCRIPT))
import bom  # noqa: E402

fails = []


def ok(cond, what):
    if not cond:
        fails.append(what)


cat = bom.catalogue()

# catalogue matches the template rows the script fills
import openpyxl  # noqa: E402
wb = openpyxl.load_workbook(bom.TEMPLATE)
ok({c.value for c in wb["SKUs"]["A"] if c.value} >= {s["id"] for s in cat["skus"]}, "every catalogue SKU has a template row")
ok({c.value for c in wb["Gotchas"]["A"] if c.value} >= {g["id"] for g in cat["gotchas"]}, "every gotcha has a template row")
ok(len(cat["sizing_questions"]) == 13, "13 sizing questions (template rows 5-17)")
labels = {c.value for c in wb["Deal"]["A"] if c.value}
ok(all(lbl in labels for _, lbl, _ in bom.FACTS), "every deal fact label is in the template")

# tier: same rule as the template (upper bounds inclusive, highest of the three)
ok(bom.tier_of(cat, revenue=100)[0] == 1, "revenue 100 -> tier 1")
ok(bom.tier_of(cat, revenue=101)[0] == 2, "revenue 101 -> tier 2")
ok(bom.tier_of(cat, revenue=50, employees=2600)[0] == 4, "employees 2600 wins -> tier 4")
ok(bom.tier_of(cat, aum=60000)[0] == 7, "AUM 60bn -> tier 7")
ok(bom.tier_of(cat)[0] is None, "no facts -> no tier")

# prices and user counts are refused; sizes are not
for t, want in {"A$7.8bn AUM": False, "USD 5,070 million": False, "$4,300 per block": True, "AUD 120k a year": True,
                "costs $500": True}.items():
    ok(bool(bom.PRICE_RX.search(t)) == want, "price rule: %r" % t)
for t, want in {"about 300 users": True, "50 seats": True, "3 businesses": False, "50 roles": False}.items():
    ok(bool(bom.USERS_RX.search(t)) == want, "user rule: %r" % t)

# a fictional deal
tmp = tempfile.mkdtemp(prefix="bomtest-")
try:
    deal = os.path.join(tmp, "kestrel-finance-xx")
    os.makedirs(deal)
    bom.new_bom(cat, deal)
    p = os.path.join(deal, "bom.json")
    b = bom.load_json(p)
    b["deal_facts"]["customer"] = {"value": "Kestrel Finance (fictional)", "tag": "C", "source": "test"}
    b["deal_facts"]["employees"] = {"value": 900, "tag": "C", "source": "test"}
    b["deal_facts"]["revenue_musd"] = {"value": 80, "tag": "C", "source": "test"}
    for sid in [s["id"] for s in cat["skus"]]:
        b["lines"][sid].update({"needed": "No"})
    b["lines"]["P1"].update({"needed": "Yes", "why": "Default", "tag": "A"})
    b["lines"]["C1"].update({"needed": "Yes", "why": "Dealer pipeline", "tag": "C"})
    b["lines"]["I3"].update({"needed": "TBC", "why": "Two loan books", "tag": "I"})

    err, _ = bom.check(cat, b)
    ok(any("P1 is Yes, so A1" in e for e in err), "Unlimited without an AI Package is an error")
    b["lines"]["A1"].update({"needed": "Yes", "why": "Document reading scene", "tag": "C"})
    err, _ = bom.check(cat, b)
    ok(not err, "clean BOM has no errors: %s" % err)

    bad = copy.deepcopy(b)
    bad["lines"]["C1"]["why"] = "about 40 users at $12 per user"
    err, _ = bom.check(cat, bad)
    ok(sum(("Price" in e or "User count" in e) for e in err) == 2, "price and user count both caught")
    bad = copy.deepcopy(b)
    bad["deal_facts"]["commercial_model"]["value"] = "Per seat"
    bad["lines"]["P1"]["needed"] = "No"
    bad["lines"]["P2"].update({"needed": "Yes", "why": "x", "tag": "C"})
    err, _ = bom.check(cat, bad)
    ok(any("per_seat_reason" in e for e in err), "per seat needs a reason")
    ok(any("so P3" in e for e in err), "Studio needs AI Platform")
    ok(any("S1/S2" in e for e in err), "per seat needs support")
    bad = copy.deepcopy(b)
    bad["lines"]["C1"]["qty"] = 40
    err, _ = bom.check(cat, bad)
    ok(any("qty only" in e for e in err), "qty on a user line is an error")

    err, _ = bom.check(cat, b, final=True)
    ok(any("G01" in e for e in err), "--final needs a status on every applicable gotcha")

    qs = [q["id"] for q in bom.open_questions(cat, b)]
    ok("SQ02" not in qs and "SQ01" not in qs, "size facts tagged C are not asked again")
    ok("SQ04" in qs, "a TBC storage line asks for record volumes")

    bom.save_json(p, b)
    r = subprocess.run([sys.executable, "-I", SCRIPT, "build", p, "--nn", "09"], capture_output=True, text=True)
    ok(r.returncode == 0, "build runs: %s" % r.stderr[-300:])
    md = open(os.path.join(deal, "09-bom.md"), encoding="utf-8").read()
    ok("INTERNAL ONLY" in md and "Tier 2" in md, "md has the internal banner and tier 2 (900 employees)")
    ok("Additional database storage" in md.split("## 3.")[1].split("## 4.")[0], "storage shows under Extra to quote")
    s = openpyxl.load_workbook(os.path.join(deal, "09-bom.xlsx"))["Summary for the AE"]
    col = [str(c.value) for c in s["B"] if c.value]
    ok(any("Additional database storage" in v for v in col), "AE summary lists storage as extra")
    ok(any(v.startswith("7. Open with Deal Desk") for v in col), "AE summary lists the OPEN items")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("PASS (%s)" % os.path.basename(SCRIPT) if not fails else "FAIL\n- " + "\n- ".join(fails))
sys.exit(1 if fails else 0)
