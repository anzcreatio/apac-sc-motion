"""Customer enablement: teach a customer's team to build on Creatio with Claude and Creatio's public toolkit.

Everything for one customer lives in the deal folder: <deal>/enablement/ (plan, people, feedback, customer pack).
The course itself (course.json, modules/) is in the plugin; upkeep (refresh, stamp) reuses the sc-academy engine:
  python ../sc-academy/scripts/academy.py --course ../sc-customer-academy/course.json refresh | stamp ...

  python customer_academy.py prep    --deal <deal folder> --product "Sales Creatio" --format 1h|3h|full [--tracks T1,T2]
                                     --env-name <their clio env> --env-url <url> [--scenario own|practice]
                                     [--non-prod-confirmed-by "<customer name, role>"] [--customer-name "Harbourline Credit Union"]
        enablement/plan.json. Refuses an environment that looks like production unless the customer confirmed it isn't.
  python customer_academy.py person  --deal <deal> --name "..." --role "..." --track T1
  python customer_academy.py at      --deal <deal> --person "..." --module B2 --step 3
  python customer_academy.py result  --deal <deal> --person "..." --module B2 --result pass|fail [--note "..."]
  python customer_academy.py feedback --deal <deal> --person "..." --module B2 --hardest "..." --lab "..." --useful 4 [--change "..."]
        Full answers -> <deal>/enablement/feedback/. A copy without the person's name -> Lessons/feedback/ (Source: customer-training).
  python customer_academy.py status  --deal <deal>
  python customer_academy.py pack    --deal <deal> [--approved-by "<SC name>"]
        The customer pack: workbook pages (facilitator notes removed) + the creatio-build-coach skill they keep.
        DRAFT until the SC approves it.
  python customer_academy.py tips    [--days 7]   -> Lessons/customer-training/weekly/<yyyy-Www>.md (for Renzo)
"""
import argparse
import datetime
import glob
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(SKILL_DIR, "..", "sc-academy", "scripts"))
import academy  # noqa: E402  (shared engine: json helpers, md_to_html, fingerprints)

academy.COURSE = os.path.join(SKILL_DIR, "course.json")
academy.SKILL_DIR = SKILL_DIR
load_json, save_json, kebab, today = academy.load_json, academy.save_json, academy.kebab, academy.today

PROD_HINT = re.compile(r"(^|[-_.])(prod|production|live|prd)([-_.]|$)", re.I)
NONPROD_HINT = re.compile(r"(dev|test|sandbox|uat|trial|demo|staging|stage|qa|training|sbx|preprod)", re.I)
SC_CHECK = "SC check required before this is used with the customer."


def course():
    return academy.course()


def modules(c):
    return academy.modules(c)


def person_modules(c, p, track=None):
    """The modules one participant works through: the format's list (1h, 3h) or their track in the full course."""
    fmt = (c.get("formats") or {}).get(p.get("format") or "full", {})
    if fmt.get("modules"):
        ids = fmt["modules"]
        return [m for i in ids for m in modules(c) if m["id"] == i]
    return [m for m in modules(c) if m["path"] == (track or "").upper()] if track else         [m for m in modules(c) if m["path"] in p.get("tracks", [])]


def edir(deal, *parts):
    p = os.path.join(deal, "enablement", *parts)
    os.makedirs(p if not os.path.splitext(p)[1] else os.path.dirname(p), exist_ok=True)
    return p


def plan(deal, must=True):
    p = load_json(os.path.join(deal, "enablement", "plan.json"))
    if p is None and must:
        sys.exit("No enablement plan yet: run `customer_academy.py prep --deal ...` first")
    return p


def put_plan(deal, p):
    p["updated"] = today()
    return save_json(os.path.join(edir(deal), "plan.json"), p)


def person(p, name):
    for x in p["people"]:
        if x["name"].lower() == name.lower():
            return x
    sys.exit("No participant %s in the plan: add them with `person`" % name)


def sc_initials():
    return (load_json(academy.CONFIG, {}) or {}).get("sc", "")


# ---------------------------------------------------------------- commands

def cmd_prep(a):
    deal = os.path.abspath(a.deal)
    if not os.path.isdir(deal):
        sys.exit("Deal folder not found: %s" % deal)
    host = (a.env_url or "").split("//")[-1].split("/")[0]
    text = "%s %s" % (a.env_name, host)
    looks_prod = bool(PROD_HINT.search(text)) or not NONPROD_HINT.search(text)
    if looks_prod and not a.non_prod_confirmed_by:
        print("STOP: '%s' (%s) doesn't look like a development or sandbox environment." % (a.env_name, host or "no URL"))
        print("The course only runs in the customer's own dev or sandbox, never production. Ask the customer; if they")
        print("confirm it isn't production, re-run with --non-prod-confirmed-by \"<name, role>\" (recorded in the plan).")
        sys.exit(2)
    c = course()
    fmt = (c.get("formats") or {}).get(a.format)
    if not fmt:
        sys.exit("Unknown format %s; formats: %s" % (a.format, ", ".join(c.get("formats", {}))))
    tracks = [t.strip().upper() for t in (a.tracks or ",".join(fmt.get("tracks", ["F"]))).split(",")]
    valid = {p["id"] for p in c["paths"] if p.get("status") == "live"}
    bad = [t for t in tracks if t not in valid]
    if bad:
        sys.exit("Unknown track(s) %s; live tracks: %s" % (bad, sorted(valid)))
    old = plan(deal, must=False) or {}
    slug = os.path.basename(deal)
    display = a.customer_name or old.get("customer") or " ".join(
        w.capitalize() for w in re.sub(r"-(rh|wn|fa)$", "", slug).split("-"))
    p = {"account": slug, "customer": display, "product": a.product, "format": a.format, "tracks": tracks, "scenario": a.scenario,
         "course_version": c["version"], "sc": sc_initials(),
         "environment": {"name": a.env_name, "url": a.env_url, "looks_prod": looks_prod,
                         "non_prod_confirmed_by": a.non_prod_confirmed_by, "checked": today()},
         "people": old.get("people", []), "sessions": old.get("sessions", []), "pack": old.get("pack"),
         "created": old.get("created", today())}
    print(put_plan(deal, p))
    mods = person_modules(c, p)
    print("%s: %s (%s), about %.1f hours in the room plus pre-work." % (a.format, fmt["title"], ", ".join(m["id"] for m in mods),
          sum(m.get("minutes", 0) for m in mods if m["id"] != "F0") / 60.0))


def cmd_person(a):
    deal = os.path.abspath(a.deal)
    p = plan(deal)
    if any(x["name"].lower() == a.name.lower() for x in p["people"]):
        print("%s is already in the plan." % a.name)
        return
    track = (a.track or p.get("format") or "").upper()
    mine = person_modules(course(), p, a.track if p.get("format") == "full" else None)
    if not mine:
        sys.exit("No modules for %s in this plan (format %s): pass --track T1 or T2 for the full course" % (a.name, p.get("format")))
    first = mine[0]["id"]
    p["people"].append({"name": a.name, "role": a.role, "track": track, "module": first, "step": 1,
                        "started": {first: today()}, "done": {}, "results": []})
    print(put_plan(deal, p))


def cmd_at(a):
    deal = os.path.abspath(a.deal)
    p = plan(deal)
    x = person(p, a.person)
    m = academy.module_by_id(course(), a.module)
    x["module"], x["step"] = m["id"], a.step
    x.setdefault("started", {}).setdefault(m["id"], today())
    print(put_plan(deal, p))


def cmd_result(a):
    deal = os.path.abspath(a.deal)
    c = course()
    p = plan(deal)
    x = person(p, a.person)
    m = academy.module_by_id(c, a.module)
    x["results"].append({"module": m["id"], "result": a.result, "date": today(), "note": a.note or ""})
    if a.result == "pass":
        x["done"][m["id"]] = today()
        mine = person_modules(c, p, x["track"] if p.get("format") == "full" else None)
        nxt = next((n for n in mine if n["id"] not in x["done"]), None)
        x["module"], x["step"] = (nxt["id"], 1) if nxt else (None, None)
        if nxt:
            x["started"].setdefault(nxt["id"], today())
    print(put_plan(deal, p))
    if a.result == "fail" and sum(1 for r in x["results"] if r["module"] == m["id"] and r["result"] == "fail") >= 2:
        print("Second fail on %s: slow down, pair with them on it, and note what the module should explain better." % m["id"])


def cmd_feedback(a):
    deal = os.path.abspath(a.deal)
    p = plan(deal)
    x = person(p, a.person)
    m = academy.module_by_id(course(), a.module)
    body = [
        "- What happened: hardest or unclear: %s" % (a.hardest or "-"),
        "- What happened: did the lab work as written: %s" % (a.lab or "-"),
        "- What they'd change: %s" % (a.change or "-"),
        "- How it felt (1-5): %s (useful for their own work)" % (a.useful if a.useful is not None else "-"),
        "- Severity: %s" % ("blocker" if a.blocker else ("annoying" if (a.useful or 5) <= 2 else "idea")), ""]
    full = os.path.join(edir(deal, "feedback"), "%s-%s-%s.md" % (today(), kebab(x["name"]), m["id"].lower()))
    with open(full, "w", encoding="utf-8") as fh:
        fh.write("\n".join(["# %s, module %s %s" % (x["name"], m["id"], m["title"]),
                            "- Participant: %s (%s, track %s) · Date: %s" % (x["name"], x["role"], x["track"], today())] + body))
    root = academy.team_root(None)
    d = os.path.join(root, "Lessons", "feedback")  # about the course, role only, so shared (FEEDBACK-LOOP v0.2 section 5)
    os.makedirs(d, exist_ok=True)
    team = os.path.join(d, "%s-%s-customer-%s-%s-%s.md" % (today(), p.get("sc") or "sc", kebab(p["account"]),
                                                            m["id"].lower(), kebab(x["role"])[:20]))
    with open(team, "w", encoding="utf-8") as fh:
        fh.write("\n".join([
            "# Customer academy %s %s: %s" % (m["id"], m["title"], (a.hardest or "no notes")[:80]),
            "- SC: %s · Deal: %s · Skill + step: sc-customer-academy, module %s · Source: customer-training · Module: %s · Role: %s · Kind: process · Date: %s"
            % (p.get("sc") or "-", p["account"], m["id"], m["id"], x["role"], today())] + body))
    print(full)
    print(team)


def cmd_status(a):
    deal = os.path.abspath(a.deal)
    c = course()
    p = plan(deal)
    env = p["environment"]
    print("%s · %s · %s · environment %s%s" % (p["account"], p["product"], p.get("format", "full"), env["name"],
          " (customer confirmed non-production: %s)" % env["non_prod_confirmed_by"] if env.get("non_prod_confirmed_by") else ""))
    stale = (load_json(os.path.join(academy.team_root(None), *academy.state_dir(), "_state", "stale.json"), {}) or {}).get("stale", {})
    for x in p["people"]:
        done = len(x["done"])
        total = len(person_modules(c, p, x["track"] if p.get("format") == "full" else None))
        print("  %-24s %-22s %s  %d/%d done, now %s step %s%s" % (x["name"], x["role"][:22], x["track"], done, total,
              x["module"] or "-", x["step"] or "-", "  [module being updated]" if x["module"] in stale else ""))
    print("Customer pack: %s" % ((p.get("pack") or {}).get("status") or "not built"))


def strip_facilitator(md):
    """Customer copies never carry the facilitator section."""
    return re.split(r"\n## For the facilitator\b", md)[0].rstrip() + "\n"


def cmd_pack(a):
    deal = os.path.abspath(a.deal)
    c = course()
    p = plan(deal)
    out = edir(deal, "customer-pack")
    for sub in ("pages", "creatio-build-coach"):
        shutil.rmtree(os.path.join(out, sub), ignore_errors=True)
    approved = bool(a.approved_by)
    mods = person_modules(c, p)
    # 1. the skill the customer keeps
    sk = os.path.join(out, "creatio-build-coach")
    os.makedirs(os.path.join(sk, "modules"), exist_ok=True)
    with open(os.path.join(SKILL_DIR, "pack", "creatio-build-coach", "SKILL.md"), encoding="utf-8") as fh:
        skill = fh.read().replace("{{CUSTOMER}}", p.get("customer") or p["account"]).replace("{{PRODUCT}}", p["product"])
    with open(os.path.join(sk, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(skill)
    for m in mods:
        with open(os.path.join(SKILL_DIR, m["file"]), encoding="utf-8") as fh:
            body = strip_facilitator(fh.read())
        with open(os.path.join(sk, m["file"]), "w", encoding="utf-8") as fh:
            fh.write(body)
    for fx in ("practice-scenario.md", "glossary.md"):
        shutil.copy(os.path.join(SKILL_DIR, "fixtures", fx), os.path.join(sk, fx))
    save_json(os.path.join(sk, "course.json"), {"title": c["title"], "version": c["version"], "customer": p.get("customer") or p["account"],
              "product": p["product"], "references": c.get("references", {}),
              "modules": [{k: m[k] for k in ("id", "title", "file", "minutes", "path")} for m in mods]})
    # 2. the workbook pages
    pg = os.path.join(out, "pages")
    os.makedirs(pg, exist_ok=True)
    banner = "" if approved else "<p style='background:#fde68a;color:#111;padding:8px 12px;border-radius:6px'><strong>DRAFT</strong>: %s</p>" % SC_CHECK
    ftitle = ((c.get("formats") or {}).get(p.get("format") or "full") or {}).get("title") or c["title"]
    idx = ["# %s" % (ftitle if p.get("format") in ("1h", "3h") else c["title"]), "", "For **%s** (%s)." % (p.get("customer") or p["account"], p["product"]), "", c["about"], "",
           "| Part | Module | Minutes |", "|---|---|---|"]
    head = ("<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
            "<title>%s</title><style>%s</style>")
    for m in mods:
        with open(os.path.join(SKILL_DIR, m["file"]), encoding="utf-8") as fh:
            body = strip_facilitator(fh.read())
        name = os.path.basename(m["file"]).replace(".md", ".html")
        with open(os.path.join(pg, name), "w", encoding="utf-8") as fh:
            fh.write(head % ("%s %s" % (m["id"], m["title"]), academy.CSS) + banner +
                     "<p><a href='index.html'>Course index</a></p>" + academy.md_to_html(body))
        idx.append("| %s | [%s](%s) | %s |" % ({"F": "Session"}.get(m["path"], m["path"]), m["title"], name, m.get("minutes", "")))
    with open(os.path.join(SKILL_DIR, "fixtures", "glossary.md"), encoding="utf-8") as fh:
        gl = fh.read()
    with open(os.path.join(pg, "glossary.html"), "w", encoding="utf-8") as fh:
        fh.write(head % ("Words you'll hear", academy.CSS) + banner + "<p><a href='index.html'>Course index</a></p>" + academy.md_to_html(gl))
    idx.append("| | [Words you'll hear](glossary.html) | |")
    idx += ["", "## Keep learning", "",
            "- Toolkit setup guide (Creatio Academy): %s" % c["references"]["toolkit_setup"],
            "- The toolkit on GitHub: %s" % c["references"]["toolkit_repo"],
            "- To keep using the coach after the course: copy the `creatio-build-coach` folder into `~/.claude/skills/` and say \"coach me\" in Claude Code."]
    with open(os.path.join(pg, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(head % (c["title"], academy.CSS) + banner + academy.md_to_html("\n".join(idx)))
    with open(os.path.join(out, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("# Customer pack: %s\n\n- pages/index.html: the workbook\n- creatio-build-coach/: the Claude skill they keep\n\n%s\n"
                 % (p["account"], "Approved by %s on %s." % (a.approved_by, today()) if approved else "**DRAFT.** " + SC_CHECK))
    p["pack"] = {"status": "approved" if approved else "draft", "by": a.approved_by, "date": today(),
                 "modules": [m["id"] for m in mods], "course_version": c["version"]}
    put_plan(deal, p)
    print(out)
    print("Pack is %s" % ("APPROVED by %s." % a.approved_by if approved else "a DRAFT: " + SC_CHECK))


def cmd_tips(a):
    root = academy.team_root(None)
    c = course()
    mods = {m["id"]: m for m in modules(c)}
    since = (datetime.date.today() - datetime.timedelta(days=a.days)).isoformat()
    plans = []
    for f in glob.glob(os.path.join(root, "Deals", "*", "enablement", "plan.json")):
        pl = load_json(f)
        if pl:
            plans.append(pl)
    fails, ratings, notes, active = {}, {}, {}, 0
    for pl in plans:
        for x in pl["people"]:
            if any(d >= since for d in x["done"].values()) or any(r["date"] >= since for r in x["results"]):
                active += 1
            for r in x["results"]:
                if r["result"] == "fail" and r["date"] >= since:
                    fails.setdefault(r["module"], []).append(r["note"])
    for f in glob.glob(os.path.join(root, "Lessons", "feedback", "*.md")) + glob.glob(os.path.join(root, "Lessons", "feedback", "*", "*.md")):
        try:
            t = open(f, encoding="utf-8").read()
        except OSError:
            continue
        if "Source: customer-training" not in t:
            continue
        dm = re.search(r"Date: (\d{4}-\d\d-\d\d)", t)
        if dm and dm.group(1) < since:
            continue
        mm = re.search(r"Module: (\w+)", t)
        rm = re.search(r"How it felt \(1-5\): (\d)", t)
        hm = re.search(r"hardest or unclear: (.*)", t)
        if mm:
            if rm:
                ratings.setdefault(mm.group(1), []).append(int(rm.group(1)))
            if hm and hm.group(1).strip() not in ("-", ""):
                notes.setdefault(mm.group(1), []).append(hm.group(1).strip())
    st = load_json(os.path.join(root, *academy.state_dir(), "_state", "stale.json"), {}) or {}
    pend = [m["id"] for m in modules(c) if (m.get("stamped") or {}).get("status") != "approved"]
    wk = "%d-W%02d" % datetime.date.today().isocalendar()[:2]
    L = ["# Customer academy: tips for Renzo, %s" % wk, "",
         "> `customer_academy.py tips`, %s, last %d days. Accounts named; participants never." % (today(), a.days), "",
         "## Decisions for you", ""]
    n = 0
    for mid, s in (st.get("stale") or {}).items():
        n += 1
        L.append("%d. Module %s %s is stale (%s): approve the drafted update?" % (n, mid, s["title"], "; ".join(
            "%s %s" % (w["skill"], w["change"]) for w in s["why"])))
    if pend:
        n += 1
        L.append("%d. Not approved by you yet: %s. Approve with `academy.py --course ../sc-customer-academy/course.json stamp --module <id> --by \"Renzo Huruiti\"`?" % (n, ", ".join(pend)))
    if st.get("uncovered"):
        n += 1
        L.append("%d. Toolkit skills no module teaches: %s." % (n, ", ".join(st["uncovered"])))
    if not n:
        L.append("None this week.")
    L += ["", "## Where customers get stuck", "", "| Module | Signal | Detail |", "|---|---|---|"]
    rows = 0
    for mid in sorted(set(fails) | set(ratings)):
        r = ratings.get(mid, [])
        L.append("| %s %s | %s%s | %s |" % (mid, mods.get(mid, {}).get("title", ""),
                 "%d failed check(s) " % len(fails.get(mid, [])) if fails.get(mid) else "",
                 "usefulness %.1f / 5 (%d)" % (sum(r) / len(r), len(r)) if r else "",
                 "; ".join((fails.get(mid, []) + notes.get(mid, []))[:4])[:300]))
        rows += 1
    if not rows:
        L.append("| - | nothing this week | |")
    L += ["", "## Activity", "", "| Measure | Value |", "|---|---|",
          "| Customers with an enablement plan | %d |" % len(plans),
          "| Participants active this week | %d |" % active,
          "| Customer packs approved | %d |" % sum(1 for pl in plans if (pl.get("pack") or {}).get("status") == "approved"), ""]
    out = os.path.join(academy.tdir(root, "weekly"), "%s.md" % wk)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))
    print(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("prep"); s.add_argument("--deal", required=True); s.add_argument("--product", required=True)
    s.add_argument("--format", choices=["1h", "3h", "full"], required=True); s.add_argument("--tracks")
    s.add_argument("--env-name", required=True); s.add_argument("--env-url")
    s.add_argument("--scenario", choices=["own", "practice"], default="practice"); s.add_argument("--non-prod-confirmed-by")
    s.add_argument("--customer-name", help="as the customer writes it, for the pack (default: from the folder name)")
    s = sub.add_parser("person"); s.add_argument("--deal", required=True); s.add_argument("--name", required=True)
    s.add_argument("--role", required=True); s.add_argument("--track", help="T1 or T2, full course only")
    s = sub.add_parser("at"); s.add_argument("--deal", required=True); s.add_argument("--person", required=True)
    s.add_argument("--module", required=True); s.add_argument("--step", type=int, required=True)
    s = sub.add_parser("result"); s.add_argument("--deal", required=True); s.add_argument("--person", required=True)
    s.add_argument("--module", required=True); s.add_argument("--result", choices=["pass", "fail"], required=True)
    s.add_argument("--note")
    s = sub.add_parser("feedback"); s.add_argument("--deal", required=True); s.add_argument("--person", required=True)
    s.add_argument("--module", required=True); s.add_argument("--hardest"); s.add_argument("--lab")
    s.add_argument("--useful", type=int, choices=range(1, 6)); s.add_argument("--change"); s.add_argument("--blocker", action="store_true")
    s = sub.add_parser("status"); s.add_argument("--deal", required=True)
    s = sub.add_parser("pack"); s.add_argument("--deal", required=True); s.add_argument("--approved-by")
    s = sub.add_parser("tips"); s.add_argument("--days", type=int, default=7)
    a = ap.parse_args()
    {"prep": cmd_prep, "person": cmd_person, "at": cmd_at, "result": cmd_result, "feedback": cmd_feedback,
     "status": cmd_status, "pack": cmd_pack, "tips": cmd_tips}[a.cmd](a)


if __name__ == "__main__":
    main()
