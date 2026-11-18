"""ready.py: the learning loop's private log (standards/LEARNING-LOOP-v0.1.md).

Everything here stays on the SC's own PC: ~/.apac-sc-motion/learn/ (never the deal folder, never SharePoint).

  python ready.py pilot [--feature call-it-first|ready]   is the pilot on for me? (exit 0 on, 3 off) + skip streak
  python ready.py call   --deal <deal> --stage fm|demo-plan --text "<3 lines>"   save my call before Claude's
  python ready.py call   --deal <deal> --stage fm|demo-plan --skip               I skipped it (logged)
  python ready.py call   --deal <deal> --stage fm|demo-plan --match 0-3          how many lines matched Claude's
  python ready.py learn  --deal <deal> --rule "..." --evidence "..." --next "..." [--risk high|normal]
  python ready.py pick   [--deal <deal>]          one past Learn point that is due again (spaced: 2, 7, 21, 60 days)
  python ready.py recall --id L-... --ok|--miss   how the re-ask went (moves it along the schedule or back)
  python ready.py quiz   --deal <deal> --score N --of M [--misses "q1|q2"] [--verdict ready|not-ready]
  python ready.py misses --deal <deal>            the last quiz's misses (morning recheck)
  python ready.py stats                           pilot numbers
"""
import argparse
import datetime as dt
import json
import os
import sys

HOME = os.path.expanduser("~")
CFG = os.path.join(HOME, ".apac-sc-motion.json")
DIR = os.path.join(HOME, ".apac-sc-motion", "learn")
STEPS = [2, 7, 21, 60]  # days until a Learn point is asked again, per correct recall
FEATURES = ("call-it-first", "ready")
NOW = dt.datetime.now()
TODAY = NOW.date()


def cfg():
    try:
        return json.load(open(CFG, encoding="utf-8"))
    except Exception:
        return {}


def path(name):
    os.makedirs(DIR, exist_ok=True)
    return os.path.join(DIR, name)


def rows(name):
    p = path(name)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def add(name, row):
    row = dict(row, at=NOW.isoformat(timespec="seconds"))
    with open(path(name), "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def save_all(name, items):
    with open(path(name), "w", encoding="utf-8") as f:
        for r in items:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def deal_id(d):
    return os.path.basename(os.path.normpath(d)) if d else ""


def on(feature=None):
    p = cfg().get("pilot") or []
    return bool(p) if feature is None else feature in p


def skip_streak():
    n = 0
    for r in reversed([r for r in rows("calls.jsonl") if "match" not in r]):
        if r.get("skip"):
            n += 1
        else:
            break
    return n


def c_pilot(a):
    feats = [f for f in FEATURES if on(f)]
    if a.feature:
        ok = on(a.feature)
        print("%s: %s" % (a.feature, "on" if ok else "off (skip the learning-loop steps)"))
    else:
        print("Pilot features on: %s" % (", ".join(feats) or "none (skip the learning-loop steps)"))
        ok = bool(feats)
    s = skip_streak()
    if ok and s >= 3:
        print("Note: the last %d 'call it first' steps were skipped. Mention it once, plainly, no lecture." % s)
    sys.exit(0 if ok else 3)


def c_call(a):
    base = {"deal": deal_id(a.deal), "stage": a.stage}
    if a.match is not None:
        if not 0 <= a.match <= 3:
            sys.exit("--match is 0 to 3")
        add("calls.jsonl", dict(base, match=a.match))
        print("Saved: %d/3 of your call matched." % a.match)
    elif a.skip:
        add("calls.jsonl", dict(base, skip=True))
        print("Skipped (logged).")
    elif a.text:
        add("calls.jsonl", dict(base, text=a.text))
        print("Your call is saved. Claude's comes next.")
    else:
        sys.exit("Give --text, --skip or --match")


def c_learn(a):
    items = rows("learn.jsonl")
    n = 1 + len([i for i in items if i["id"].startswith("L-%s" % TODAY.strftime("%Y%m%d"))])
    lid = "L-%s-%d" % (TODAY.strftime("%Y%m%d"), n)
    add("learn.jsonl", {"id": lid, "deal": deal_id(a.deal), "rule": a.rule, "evidence": a.evidence, "next": a.next,
                        "risk": a.risk, "box": 0, "due": (TODAY + dt.timedelta(days=STEPS[0])).isoformat(), "asked": 0, "right": 0})
    print("Logged %s (asked again from %s)." % (lid, (TODAY + dt.timedelta(days=STEPS[0])).isoformat()))


def c_pick(a):
    items = [i for i in rows("learn.jsonl") if i.get("due") and i["due"] <= TODAY.isoformat() and i.get("box", 0) < len(STEPS)]
    if not items:
        print("No past Learn point is due. Skip the recall question.")
        return
    # high-risk first, then most overdue; prefer another deal's point (it's the transfer that counts)
    items.sort(key=lambda i: (i.get("risk") != "high", i.get("deal") == deal_id(a.deal), i["due"]))
    i = items[0]
    print(json.dumps({k: i[k] for k in ("id", "deal", "rule", "evidence", "next", "risk")}, ensure_ascii=False, indent=1))
    print("Ask it as a scenario (\"on a deal where ..., what do you look for?\"), not by reading the rule out.")


def c_recall(a):
    items = rows("learn.jsonl")
    hit = [i for i in items if i["id"] == a.id]
    if not hit:
        sys.exit("No Learn point %s" % a.id)
    i = hit[0]
    i["asked"] = i.get("asked", 0) + 1
    if a.ok:
        i["right"] = i.get("right", 0) + 1
        i["box"] = i.get("box", 0) + 1
    else:
        i["box"] = 0
    i["due"] = (TODAY + dt.timedelta(days=STEPS[min(i["box"], len(STEPS) - 1)])).isoformat() if i["box"] < len(STEPS) else None
    save_all("learn.jsonl", items)
    print("%s: %s. %s" % (a.id, "right" if a.ok else "missed", "Next ask %s." % i["due"] if i["due"] else "Retired: you've got this one."))


def c_quiz(a):
    misses = [m.strip() for m in (a.misses or "").split("|") if m.strip()]
    add("quiz.jsonl", {"deal": deal_id(a.deal), "score": a.score, "of": a.of, "misses": misses, "verdict": a.verdict,
                       "recheck": a.recheck})
    print("Saved: %d/%d%s." % (a.score, a.of, ", verdict %s" % a.verdict if a.verdict else ""))


def c_misses(a):
    q = [r for r in rows("quiz.jsonl") if r["deal"] == deal_id(a.deal) and not r.get("recheck")]
    if not q:
        print("No readiness quiz on record for this deal.")
        return
    last = q[-1]
    print("Last quiz %s: %d/%d." % (last["at"][:10], last["score"], last["of"]))
    print("\n".join("- " + m for m in last["misses"]) or "No misses: nothing to recheck.")


def c_stats(a):
    calls = rows("calls.jsonl")
    made = [c for c in calls if c.get("text")]
    skipped = [c for c in calls if c.get("skip")]
    matches = [c["match"] for c in calls if "match" in c]
    quiz = rows("quiz.jsonl")
    first = [q for q in quiz if not q.get("recheck")]
    re_ = [q for q in quiz if q.get("recheck")]
    learn = rows("learn.jsonl")
    asked = sum(i.get("asked", 0) for i in learn)
    right = sum(i.get("right", 0) for i in learn)
    pct = lambda x, y: "%d%%" % round(100.0 * x / y) if y else "n/a"
    print("| Measure | Value |\n|---|---|")
    print("| Pilot features on | %s |" % (", ".join(f for f in FEATURES if on(f)) or "none"))
    print("| Calls made / skipped | %d / %d |" % (len(made), len(skipped)))
    print("| Your call matched Claude's (avg of 3) | %s |" % ("%.1f (n=%d); first half %s, second half %s" % (
        sum(matches) / len(matches), len(matches),
        "%.1f" % (sum(matches[:len(matches) // 2]) / max(1, len(matches) // 2)) if len(matches) > 1 else "n/a",
        "%.1f" % (sum(matches[len(matches) // 2:]) / max(1, len(matches) - len(matches) // 2))) if matches else "n/a"))
    print("| Readiness quiz, first try | %s (n=%d) |" % (pct(sum(q["score"] for q in first), sum(q["of"] for q in first)), len(first)))
    print("| Morning recheck | %s (n=%d) |" % (pct(sum(q["score"] for q in re_), sum(q["of"] for q in re_)), len(re_)))
    print("| Learn points logged / high-risk | %d / %d |" % (len(learn), len([i for i in learn if i.get("risk") == "high"])))
    print("| Learn points re-asked, right | %s (%d asked) |" % (pct(right, asked), asked))


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("pilot"); x.add_argument("--feature", choices=FEATURES); x.set_defaults(f=c_pilot)
    x = s.add_parser("call"); x.add_argument("--deal", required=True); x.add_argument("--stage", required=True, choices=["fm", "demo-plan"])
    x.add_argument("--text"); x.add_argument("--skip", action="store_true"); x.add_argument("--match", type=int); x.set_defaults(f=c_call)
    x = s.add_parser("learn"); x.add_argument("--deal", required=True); x.add_argument("--rule", required=True)
    x.add_argument("--evidence", required=True); x.add_argument("--next", required=True)
    x.add_argument("--risk", choices=["high", "normal"], default="normal"); x.set_defaults(f=c_learn)
    x = s.add_parser("pick"); x.add_argument("--deal"); x.set_defaults(f=c_pick)
    x = s.add_parser("recall"); x.add_argument("--id", required=True); g = x.add_mutually_exclusive_group(required=True)
    g.add_argument("--ok", action="store_true"); g.add_argument("--miss", action="store_true"); x.set_defaults(f=c_recall)
    x = s.add_parser("quiz"); x.add_argument("--deal", required=True); x.add_argument("--score", type=int, required=True)
    x.add_argument("--of", type=int, required=True); x.add_argument("--misses"); x.add_argument("--verdict", choices=["ready", "not-ready"])
    x.add_argument("--recheck", action="store_true", help="morning recheck of the misses"); x.set_defaults(f=c_quiz)
    x = s.add_parser("misses"); x.add_argument("--deal", required=True); x.set_defaults(f=c_misses)
    x = s.add_parser("stats"); x.set_defaults(f=c_stats)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
