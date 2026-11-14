"""Shared lessons registers on SharePoint (Lessons/registers/): product limits, discovery questions, explanations.

The only way to change them, so the JSON stays valid and IDs stay unique. Nothing is ever deleted.

  python registers.py list   [--register limits|questions] [--status open]
  python registers.py add-limit    --area "Field sales" --limit "..." [--workaround "..."] --source R&D
                                   [--source-ref "email 12 Nov, J. Smith"] [--version 8.3.1] --by "Renzo Huruiti"
                                   [--supersedes L-003]
  python registers.py add-question --topic sizing --question "..." --signal "..." --lesson "..." --by "..."
                                   [--source-ref "..."] [--supersedes Q-002]
  python registers.py close-limit  --id L-004 --fixed-in 8.3.2 --by "..." [--note "release notes 8.3.2"]
  python registers.py add-explanation --topic "no-code" --question "What does no-code mean for us?"
                                   --one-liner "..." --thirty "..." [--deeper "..."] [--analogy "..."]
                                   [--dont-say "..."] [--follow-up "..."] [--follow-up-answer "..."]
                                   [--claims D1,D4] [--audience business|it|exec] [--source-ref "EWB 12 Nov 20:59"]
                                   --by "..." [--supersedes E-002]
  python registers.py approve-explanation --id E-004 --by "Renzo Huruiti" [--note "..."]
  python registers.py retire-explanation  --id E-004 --by "..." --note "why"

Explanations expand what the team says, so (FEEDBACK-LOOP 3, the asymmetric rule) a new one is always `proposed`
and only `approved` ones are used as the team answer. Only Renzo approves, at the Friday digest.

Team root comes from ~/.apac-sc-motion.json ("sharepoint_root"), or --root.
"""
import argparse
import datetime
import json
import os
import sys

FILES = {"limits": "product-limits.json", "questions": "discovery-questions.json", "explanations": "explanations.json"}
PREFIX = {"limits": "L", "questions": "Q", "explanations": "E"}


def team_root(arg):
    if arg:
        return arg
    cfg = os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json")
    try:
        with open(cfg, encoding="utf-8") as fh:
            return json.load(fh)["sharepoint_root"]
    except (OSError, KeyError, ValueError):
        sys.exit("No team root: run sc-setup, or pass --root <SharePoint folder>")


def path_of(root, reg):
    d = os.path.join(root, "Lessons", "registers")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, FILES[reg])


def load(root, reg):
    p = path_of(root, reg)
    if not os.path.exists(p):
        return {"register": reg, "updated": None, "entries": []}
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def save(root, reg, data):
    data["updated"] = datetime.date.today().isoformat()
    p = path_of(root, reg)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, p)
    return p


def next_id(data, reg):
    nums = [int(e["id"].split("-")[1]) for e in data["entries"] if e.get("id", "").startswith(PREFIX[reg] + "-")]
    return "%s-%03d" % (PREFIX[reg], max(nums or [0]) + 1)


def mark_superseded(data, old, new):
    if not old:
        return
    for e in data["entries"]:
        if e["id"] == old:
            e["status"] = "superseded"
            e["superseded_by"] = new
            return
    sys.exit("No entry %s to supersede" % old)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list"); l.add_argument("--register", choices=FILES, default=None); l.add_argument("--status")
    a = sub.add_parser("add-limit")
    for k in ("--area", "--limit", "--source", "--by"):
        a.add_argument(k, required=True)
    for k in ("--workaround", "--source-ref", "--version", "--supersedes", "--deal"):
        a.add_argument(k)
    q = sub.add_parser("add-question")
    for k in ("--topic", "--question", "--signal", "--lesson", "--by"):
        q.add_argument(k, required=True)
    for k in ("--source-ref", "--supersedes", "--deal"):
        q.add_argument(k)
    c = sub.add_parser("close-limit")
    for k in ("--id", "--fixed-in", "--by"):
        c.add_argument(k, required=True)
    c.add_argument("--note")
    e = sub.add_parser("add-explanation")
    for k in ("--topic", "--question", "--one-liner", "--thirty", "--by"):
        e.add_argument(k, required=True)
    for k in ("--deeper", "--analogy", "--dont-say", "--follow-up", "--follow-up-answer", "--claims", "--audience",
              "--source-ref", "--supersedes", "--deal"):
        e.add_argument(k)
    for name in ("approve-explanation", "retire-explanation"):
        r = sub.add_parser(name)
        r.add_argument("--id", required=True); r.add_argument("--by", required=True)
        r.add_argument("--note", required=(name == "retire-explanation"))
    x = ap.parse_args()
    root = team_root(x.root)
    today = datetime.date.today().isoformat()

    if x.cmd == "list":
        for reg in ([x.register] if x.register else list(FILES)):
            data = load(root, reg)
            print("== %s (%d entries, updated %s)" % (FILES[reg], len(data["entries"]), data["updated"]))
            for e in data["entries"]:
                if x.status and e.get("status") != x.status:
                    continue
                text = e.get("limit") or e.get("one_liner") or e.get("question")
                print("%s [%s] %s: %s" % (e["id"], e.get("status"), e.get("area") or e.get("topic"), text))
        return

    if x.cmd == "add-limit":
        data = load(root, "limits")
        eid = next_id(data, "limits")
        mark_superseded(data, x.supersedes, eid)
        confirmed = x.source.strip().lower() in ("r&d", "rd", "support", "docs", "release notes")
        data["entries"].append({
            "id": eid, "area": x.area, "limit": x.limit, "workaround": x.workaround, "source": x.source,
            "source_ref": x.source_ref, "version": x.version, "deal": x.deal, "date": today, "reported_by": x.by,
            "confidence": "confirmed" if confirmed else "reported", "status": "open", "fixed_in": None,
            "supersedes": x.supersedes})
        print("added", eid, "->", save(root, "limits", data))
    elif x.cmd == "add-question":
        data = load(root, "questions")
        eid = next_id(data, "questions")
        mark_superseded(data, x.supersedes, eid)
        data["entries"].append({
            "id": eid, "topic": x.topic, "question": x.question, "signal": x.signal, "lesson": x.lesson,
            "source_ref": x.source_ref, "deal": x.deal, "date": today, "reported_by": x.by, "status": "open",
            "supersedes": x.supersedes})
        print("added", eid, "->", save(root, "questions", data))
    elif x.cmd == "add-explanation":
        data = load(root, "explanations")
        eid = next_id(data, "explanations")
        claims = [c.strip().upper() for c in (x.claims or "").split(",") if c.strip()]
        bad = [c for c in claims if not (c.startswith("D") and c[1:].isdigit())]
        if bad:
            sys.exit("--claims takes catalogue IDs only (D1-D7), got: %s" % ", ".join(bad))
        data["entries"].append({
            "id": eid, "topic": x.topic, "question": x.question, "one_liner": x.one_liner, "thirty_seconds": x.thirty,
            "deeper": x.deeper, "analogy": x.analogy, "dont_say": x.dont_say, "follow_up": x.follow_up,
            "follow_up_answer": x.follow_up_answer, "claims": claims, "audience": x.audience,
            "source_ref": x.source_ref, "deal": x.deal, "date": today, "reported_by": x.by, "status": "proposed",
            "approved_by": None, "approved_on": None, "supersedes": x.supersedes})
        print("proposed", eid, "(waits for Renzo's Friday approval) ->", save(root, "explanations", data))
    elif x.cmd in ("approve-explanation", "retire-explanation"):
        data = load(root, "explanations")
        for e in data["entries"]:
            if e["id"] == x.id:
                if x.cmd == "approve-explanation":
                    if e.get("status") != "proposed":
                        sys.exit("%s is %s, not proposed" % (x.id, e.get("status")))
                    e["status"] = "approved"; e["approved_by"] = x.by; e["approved_on"] = today
                    # the older answer it replaces stops being the team answer only once this one is approved
                    if e.get("supersedes"):
                        mark_superseded(data, e["supersedes"], x.id)
                else:
                    e["status"] = "retired"; e["retired_by"] = x.by; e["retired_on"] = today
                if x.note:
                    e["status_note"] = x.note
                print(e["status"], x.id, "->", save(root, "explanations", data))
                return
        sys.exit("No entry %s" % x.id)
    elif x.cmd == "close-limit":
        data = load(root, "limits")
        for e in data["entries"]:
            if e["id"] == x.id:
                e["status"] = "fixed"; e["fixed_in"] = x.fixed_in; e["closed_by"] = x.by; e["closed_on"] = today
                if x.note:
                    e["close_note"] = x.note
                print("closed", x.id, "->", save(root, "limits", data))
                return
        sys.exit("No entry %s" % x.id)


if __name__ == "__main__":
    main()
