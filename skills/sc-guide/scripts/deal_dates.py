"""Deal timing: when the first call happened, when the SC got the transcript, when the demo is. Every deal keeps
<deal>/deal-dates.json; stats across all deals go to <team root>/Lessons/stats/deal-timing.md.

  python deal_dates.py show  --deal <deal folder>
  python deal_dates.py set   --deal <deal folder> --field first_call --date 2026-11-04 [--type BDR|AE|discovery] [--source "..."]
  python deal_dates.py set   --deal <deal folder> --field sc_notified --date 2026-11-05 [--source "Teams message from Andrew"]
  python deal_dates.py set   --deal <deal folder> --field demo --date 2026-11-11 [--status planned|done|moved|cancelled]
  python deal_dates.py stats [--root <team root>]

`show` lists what's missing, so the skill knows which question to ask. Dates are yyyy-mm-dd. Writes only deal-dates.json
and the stats page.
"""
import argparse
import datetime
import json
import os
import statistics
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

FIELDS = {
    "first_call": "When did the first call with the customer happen (BDR, AE or discovery call)?",
    "sc_notified": "When did you (the SC) first get the transcript or hear about this deal?",
    "demo": "When is the demo (or when did it happen)?",
}


def path(deal):
    return os.path.join(deal, "deal-dates.json")


def load(deal):
    p = path(deal)
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8"))
    return {"deal": os.path.basename(os.path.normpath(deal))}


def days(a, b):
    try:
        return (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days
    except Exception:
        return None


def show(a):
    d = load(a.deal)
    for k, q in FIELDS.items():
        v = d.get(k) or {}
        print("%-12s %s" % (k, ("%s %s" % (v.get("date"), v.get("type") or v.get("status") or "")).strip() if v.get("date") else "MISSING: ask \"%s\"" % q))
    f, s, m = (d.get(k, {}).get("date") for k in ("first_call", "sc_notified", "demo"))
    print("first call -> SC notified: %s days · SC notified -> demo: %s days · first call -> demo: %s days" % (days(f, s), days(s, m), days(f, m)))


def set_(a):
    try:
        datetime.date.fromisoformat(a.date)
    except ValueError:
        sys.exit("Date must be yyyy-mm-dd, e.g. 2026-11-14 (got %s)" % a.date)
    d = load(a.deal)
    old = (d.get(a.field) or {}).get("date")
    v = dict(d.get(a.field) or {}, date=a.date)
    for k in ("type", "source", "status"):
        if getattr(a, k):
            v[k] = getattr(a, k)
    d[a.field] = v
    d.setdefault("history", []).append({"field": a.field, "date": a.date, "was": old, "recorded": datetime.date.today().isoformat()})
    json.dump(d, open(path(a.deal), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("%s: %s = %s%s" % (d["deal"], a.field, a.date, " (was %s)" % old if old and old != a.date else ""))


def team_root():
    try:
        return json.load(open(os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json"), encoding="utf-8"))["sharepoint_root"]
    except Exception:
        sys.exit("No team root: run sc-setup first")


def stats(a):
    root = a.root or team_root()
    deals_dir = os.path.join(root, "Deals")
    rows = []
    for name in sorted(os.listdir(deals_dir)):
        p = os.path.join(deals_dir, name, "deal-dates.json")
        if name.startswith("_") or not os.path.isfile(p):
            continue
        d = json.load(open(p, encoding="utf-8"))
        f, s, m = (d.get(k, {}).get("date") for k in ("first_call", "sc_notified", "demo"))
        sc = name.rsplit("-", 1)[-1] if name.rsplit("-", 1)[-1] in ("rh", "wn", "fa") else ""
        rows.append({"deal": name, "sc": sc, "first_call": f, "sc_notified": s, "demo": m,
                     "demo_status": d.get("demo", {}).get("status", ""), "a": days(f, s), "b": days(s, m), "c": days(f, m)})

    def med(k):
        v = [r[k] for r in rows if r[k] is not None]
        return ("%g (n=%d)" % (statistics.median(v), len(v))) if v else "n/a"
    L = ["# Deal timing", "", "From each deal's `deal-dates.json` (kept by sc-guide, sc-first-meeting, sc-demo-plan, "
         "sc-meeting-review). Updated %s. Days are calendar days." % datetime.date.today().isoformat(), "",
         "| Median | Days |", "|---|---|",
         "| First call → SC notified | %s |" % med("a"), "| SC notified → demo | %s |" % med("b"),
         "| First call → demo | %s |" % med("c"), "",
         "| Deal | SC | First call | SC notified | Demo | Call → SC | SC → demo | Call → demo |",
         "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append("| %s | %s | %s | %s | %s %s | %s | %s | %s |" % (r["deal"], r["sc"], r["first_call"] or "?", r["sc_notified"] or "?",
                                                               r["demo"] or "?", "(%s)" % r["demo_status"] if r["demo_status"] else "",
                                                               "" if r["a"] is None else r["a"], "" if r["b"] is None else r["b"], "" if r["c"] is None else r["c"]))
    missing = [r["deal"] for r in rows if None in (r["first_call"], r["sc_notified"], r["demo"])]
    no_file = [n for n in sorted(os.listdir(deals_dir)) if not n.startswith("_") and os.path.isdir(os.path.join(deals_dir, n))
               and not os.path.isfile(os.path.join(deals_dir, n, "deal-dates.json"))]
    L += ["", "Missing a date: %s" % (", ".join(missing) or "none"), "", "No dates file yet: %s" % (", ".join(no_file) or "none")]
    out = os.path.join(root, "Lessons", "stats")
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "deal-timing.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("%d deals with dates · medians: call→SC %s, SC→demo %s, call→demo %s -> %s" % (len(rows), med("a"), med("b"), med("c"), out))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("show"); p.add_argument("--deal", required=True)
    p = sp.add_parser("set"); p.add_argument("--deal", required=True); p.add_argument("--field", required=True, choices=list(FIELDS))
    p.add_argument("--date", required=True); p.add_argument("--type", choices=["BDR", "AE", "discovery"]); p.add_argument("--source")
    p.add_argument("--status", choices=["planned", "done", "moved", "cancelled"])
    p = sp.add_parser("stats"); p.add_argument("--root")
    a = ap.parse_args()
    {"show": show, "set": set_, "stats": stats}[a.cmd](a)


if __name__ == "__main__":
    main()
