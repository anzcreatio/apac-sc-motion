"""Approval pack and build log for a non-stop demo build (BUILD-RULES section 4). Writes only <deal>/build/.

  python approval_pack.py new    --deal <deal> --plan <deal>/build-plan.json --approved-by "Renzo" [--shared] [--max-restarts 3] [--max-attempts 2]
      Write build/approval-pack.json from the build plan (items B1.., stand, hours budget = plan hours x 1.5, plan hash)
      and print the one-message checklist the SC confirms.
  python approval_pack.py check  --deal <deal>
      Before the build and between items: the plan hasn't changed, the time budget isn't spent. Exit 3 = hard stop.
  python approval_pack.py log    --deal <deal> --kind <kind> [--item B3] [--note "..."] [--reversible yes|no]
      kinds: preflight-ok, restore-point, start, attempt, done, failed, rollback, compile, restart, decision, hardstop, end
      Enforces the caps. Exit 0 = carry on · 3 = HARD STOP (tell the SC) · 4 = give up this item (roll it back, skip it,
      carry on with items that don't depend on it).
  python approval_pack.py report --deal <deal>
      build/build-report.md: every item's status, compiles, restarts, rollbacks, decisions to check, time used.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HARD, GIVE_UP = 3, 4


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def paths(deal):
    b = os.path.join(deal, "build")
    return b, os.path.join(b, "approval-pack.json"), os.path.join(b, "build-log.jsonl")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]


def load_pack(deal):
    _, pp, _ = paths(deal)
    if not os.path.exists(pp):
        print("HARD STOP: no approval pack. Ask the SC to approve the build plan and the pack first.")
        sys.exit(HARD)
    return json.load(open(pp, encoding="utf-8"))


def entries(deal):
    _, _, lp = paths(deal)
    return [json.loads(l) for l in open(lp, encoding="utf-8")] if os.path.exists(lp) else []


def new(a):
    plan = json.load(open(a.plan, encoding="utf-8"))
    items = [{"id": "B%d" % i, "element": b.get("element"), "part": b.get("part"), "hours": b.get("hours", 0),
              "custom": bool(re.search(r"\bcustom(?!er)\b|\busr\.[A-Za-z]", (b.get("how") or "") + " " + (b.get("element") or ""), re.I))}
             for i, b in enumerate([b for b in plan.get("build", []) if b.get("status") != "parked"], 1)]
    hours = sum(float(i["hours"] or 0) for i in items) or float(plan.get("budget_hours") or 0)
    pack = {"approved_by": a.approved_by, "date": now(), "deal": plan.get("deal"), "plan": os.path.basename(a.plan),
            "plan_sha": sha(a.plan), "plan_path": os.path.abspath(a.plan), "stand": plan.get("stand"),
            "stand_shared": a.shared, "items": items, "budget_hours": round(hours * 1.5, 1),
            "compiles": "listed schema and code items only, after a refresh didn't do it",
            "max_restarts": 0 if a.shared else a.max_restarts, "max_attempts": a.max_attempts,
            "custom_code": "allowed once its rollback plan is written in the build log",
            "auto_rollback": True, "data": "create and replace demo data in our packages; run the reset",
            "decisions": "reversible only: take the default and log it; irreversible = hard stop",
            "restore_point_required": True}
    b, pp, _ = paths(a.deal)
    os.makedirs(b, exist_ok=True)
    json.dump(pack, open(pp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    custom = [i["id"] for i in items if i["custom"]]
    print("Approval pack -> %s\n" % pp)
    print("Please confirm in one reply, and the build runs without stopping to ask:")
    print("1. Scope: the %d items in %s (about %.1f h; budget %.1f h). Nothing else." % (len(items), pack["plan"], hours, pack["budget_hours"]))
    print("2. Stand: %s, %s." % (pack["stand"], "SHARED, so no restarts" if a.shared else "ours alone"))
    print("3. Compiles for the listed schema and code items, only when a refresh doesn't do it.")
    print("4. Restarts: %s." % ("none (shared stand)" if a.shared else "up to %d, on this stand only" % a.max_restarts))
    print("5. Custom components and code%s, each once its rollback plan is written." % (" (%s)" % ", ".join(custom) if custom else ""))
    print("6. If something breaks: roll it back, log it, carry on. Each item gets %d tries, then it's skipped and reported." % a.max_attempts)
    print("7. Demo data and the reset script, in our packages.")
    print("8. Small choices the plan doesn't settle: the default, logged. Anything that can't be undone stops the build.")
    print("Before you leave: the pre-flight check (about 5 minutes) and a restore point.")


def check(a):
    p = load_pack(a.deal)
    problems = []
    if not os.path.exists(p["plan_path"]) or sha(p["plan_path"]) != p["plan_sha"]:
        problems.append("the build plan changed after it was approved: show the change and get it approved again")
    e = entries(a.deal)
    starts = [x for x in e if x["kind"] == "start"]
    if starts:
        used = (datetime.datetime.now() - datetime.datetime.fromisoformat(starts[0]["at"])).total_seconds() / 3600
        if used > p["budget_hours"]:
            problems.append("time budget spent (%.1f h of %.1f h)" % (used, p["budget_hours"]))
    if p.get("restore_point_required") and starts and not [x for x in e if x["kind"] == "restore-point"]:
        problems.append("no restore point was taken before the build started")
    if problems:
        print("HARD STOP: " + "; ".join(problems))
        sys.exit(HARD)
    print("OK: plan unchanged, %s" % ("budget fine" if starts else "not started"))


def log(a):
    p = load_pack(a.deal)
    e = entries(a.deal)
    ids = {i["id"] for i in p["items"]}
    rec = {"at": now(), "kind": a.kind, "item": a.item, "note": a.note, "reversible": a.reversible}
    code, msg = 0, "logged"
    if a.kind == "start" and not [x for x in e if x["kind"] == "preflight-ok"]:
        code, msg = HARD, "HARD STOP: run the pre-flight check with the SC before starting"
    elif a.kind == "start" and not [x for x in e if x["kind"] == "restore-point"]:
        code, msg = HARD, "HARD STOP: take the restore point before the first change"
    elif a.item and a.item not in ids and a.kind in ("attempt", "done", "compile"):
        code, msg = HARD, "HARD STOP: %s isn't in the approved scope" % a.item
    elif a.kind == "restart":
        n = sum(1 for x in e if x["kind"] == "restart") + 1
        if p["stand_shared"] or n > p["max_restarts"]:
            code, msg = HARD, "HARD STOP: restart %d not pre-approved (%s)" % (n, "shared stand" if p["stand_shared"] else "max %d" % p["max_restarts"])
    elif a.kind == "attempt":
        n = sum(1 for x in e if x["kind"] == "attempt" and x["item"] == a.item) + 1
        if n > p["max_attempts"]:
            code, msg = GIVE_UP, "GIVE UP %s after %d tries: roll it back, skip it, carry on with what doesn't depend on it" % (a.item, n - 1)
    elif a.kind == "decision" and a.reversible != "yes":
        code, msg = HARD, "HARD STOP: a decision that can't be undone needs the SC"
    elif a.kind == "hardstop":
        code, msg = HARD, "HARD STOP logged"
    rec["result"] = msg
    _, _, lp = paths(a.deal)
    with open(lp, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(msg)
    sys.exit(code)


def report(a):
    p = load_pack(a.deal)
    e = entries(a.deal)
    status = {}
    for x in e:
        if x.get("item") and x["kind"] in ("attempt", "done", "failed", "rollback"):
            status[x["item"]] = {"attempt": "started", "done": "done", "failed": "failed", "rollback": "rolled back"}[x["kind"]]
        if x.get("item") and x["result"].startswith("GIVE UP"):
            status[x["item"]] = "skipped after %d tries" % p["max_attempts"]
    count = lambda k: [x for x in e if x["kind"] == k]
    starts = count("start")
    used = ((datetime.datetime.fromisoformat(e[-1]["at"]) - datetime.datetime.fromisoformat(starts[0]["at"])).total_seconds() / 3600) if starts else 0
    L = ["# Build report: %s" % (p.get("deal") or ""), "",
         "Stand **%s** · plan `%s` · %.1f h used of %.1f h budget · built %s" % (p["stand"], p["plan"], used, p["budget_hours"], now()[:16]), "",
         "## Items", "", "| Item | Element | Status |", "|---|---|---|"]
    L += ["| %s | %s | %s |" % (i["id"], (i["element"] or "")[:90], status.get(i["id"], "not started")) for i in p["items"]]
    for title, k in (("Compiles", "compile"), ("Restarts", "restart"), ("Rollbacks", "rollback")):
        ok = [x for x in count(k) if not x["result"].startswith("HARD STOP")]
        L += ["", "## %s (%d)" % (title, len(ok)), ""] + ["- %s %s: %s" % (x["at"][11:16], x.get("item") or "", x.get("note") or "") for x in ok]
    L += ["", "## Decisions taken on a default: check before the demo", ""] + \
         ["- %s: %s" % (x.get("item") or "general", x.get("note") or "") for x in count("decision")]
    hs = [x for x in e if x["result"].startswith("HARD STOP")]
    L += ["", "## Needs the SC", ""] + (["- %s" % x["result"] for x in hs] or ["- Nothing."])
    L += ["", "## Scope check", "", "Compare what's on the stand in our packages with the items above; list anything extra here."]
    b, _, _ = paths(a.deal)
    out = os.path.join(b, "build-report.md")
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("Report -> %s" % out)


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("new"); p.add_argument("--deal", required=True); p.add_argument("--plan", required=True)
    p.add_argument("--approved-by", required=True); p.add_argument("--shared", action="store_true")
    p.add_argument("--max-restarts", type=int, default=3); p.add_argument("--max-attempts", type=int, default=2)
    p = sp.add_parser("check"); p.add_argument("--deal", required=True)
    p = sp.add_parser("log"); p.add_argument("--deal", required=True); p.add_argument("--kind", required=True,
        choices=["preflight-ok", "restore-point", "start", "attempt", "done", "failed", "rollback", "compile", "restart", "decision", "hardstop", "end"])
    p.add_argument("--item"); p.add_argument("--note"); p.add_argument("--reversible", choices=["yes", "no"])
    p = sp.add_parser("report"); p.add_argument("--deal", required=True)
    a = ap.parse_args()
    {"new": new, "check": check, "log": log, "report": report}[a.cmd](a)


if __name__ == "__main__":
    main()
