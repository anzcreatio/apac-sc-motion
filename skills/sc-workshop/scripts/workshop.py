"""Workshop tools for sc-workshop. Writes only new files. Run from the deal folder (paths are relative to it).

  python workshop.py check --model workshop/solution-model.json [--register workshop/register.json]
                           [--md workshop/solution-model.md] [--followup workshop/wN-03-follow-up-email.md] [--deal "<Customer>"]
      Render the solution model, list every gap the Creatio build would trip on, and draft the follow-up email from
      the gaps, the model's "open" list and what they promised to send. Exit 1 while there are gaps.

  python workshop.py playback --model workshop/solution-model.json --register workshop/register.json --out workshop/playback-<date>.docx
                              [--deal "<Customer>"]
      Customer playback for sign-off: outcomes, each journey, requirements by priority in their words, open questions.
"""
import argparse
import collections
import datetime
import json
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SECTIONS = ["outcomes", "objects", "stages", "roles", "rules", "systems", "channels", "ai_moments", "example_data"]
TITLES = {"outcomes": "Outcomes", "objects": "Things they track (objects)", "stages": "Stages", "roles": "Roles",
          "rules": "Rules", "systems": "Systems", "channels": "Channels and devices", "ai_moments": "AI moments",
          "example_data": "Example data"}
COLS = {"outcomes": ["id", "measure", "baseline", "target", "owner"],
        "objects": ["id", "their_word", "kind", "creatio", "schema", "fields", "volume"],
        "stages": ["id", "object", "stages", "end_states", "who_moves", "branches", "note"],
        "roles": ["id", "name", "does", "approves", "count"],
        "rules": ["id", "rule", "value", "disputed"],
        "systems": ["id", "name", "owns", "direction", "frequency"],
        "channels": ["id", "step", "channel", "where"],
        "ai_moments": ["id", "task", "today", "who_confirms", "data"],
        "example_data": ["id", "what", "status"]}


def empty(v):
    if v is None or v == [] or v == {}:
        return True
    return isinstance(v, str) and v.strip().lower() in ("", "?", "tbc", "unknown", "to confirm")


def fmt(v):
    if isinstance(v, list):
        return " → ".join(map(str, v)) if v and all(isinstance(x, str) for x in v) else json.dumps(v, ensure_ascii=False)
    if isinstance(v, dict):
        return "; ".join("%s: %s" % (k, x) for k, x in v.items())
    if isinstance(v, bool):
        return "yes" if v else "no"
    return "" if v is None else str(v)


def plural(w):
    w = str(w).strip()
    if not w:
        return w
    low = w[0].lower() + w[1:] if not w[:2].isupper() else w
    return low if low.endswith("s") else (low[:-1] + "ies" if low.endswith("y") and low[-2:-1] not in "aeiou" else low + "s")


def word(model, oid):
    for o in model.get("objects", []):
        if o.get("id") == oid:
            w = o.get("their_word") or oid
            return w[0].lower() + w[1:] if not w[:2].isupper() else w
    return str(oid).replace("obj:", "")


def gaps(model, reg):
    """List of (where, what is missing, question for the customer or None when it's ours to fix)."""
    G = []
    opened = {o.get("about") for o in model.get("open", [])}

    def add(w, m, q=None):
        G.append((w, m, None if w in opened else q))  # an open item already asks about it: don't ask twice

    objs = {o.get("id") for o in model.get("objects", [])}
    for o in model.get("outcomes", []):
        for k, q in (("baseline", "What's the figure for %s today?"), ("target", "What would good look like for %s?"),
                     ("owner", "Who owns %s?")):
            if empty(o.get(k)):
                add(o["id"], "no " + k, q % (o.get("measure") or o["id"]))
    for o in model.get("objects", []):
        w = word(model, o["id"])
        if empty(o.get("creatio")):
            add(o["id"], "not mapped to a Creatio object (check the object model)")
        elif o["creatio"] == "new" and empty(o.get("schema")):
            add(o["id"], "new object with no neutral schema name (demo bar §6b)")
        if empty(o.get("fields")):
            add(o["id"], "no fields", "Could you send the spreadsheet or form you use for %s, so we use your own fields?" % plural(w))
        if empty(o.get("volume")):
            add(o["id"], "no volume", ("Roughly how many %s do you have?" if o.get("kind") == "master"
                                       else "Roughly how many %s a month?") % plural(w))
    for s in model.get("stages", []):
        if s.get("object") not in objs:
            add(s["id"], "object %s isn't in objects" % s.get("object"))
        st = s.get("stages") or []
        if len(st) < 2:
            add(s["id"], "fewer than 2 stages", "What are the statuses a %s goes through?" % word(model, s.get("object")))
        ends = set(s.get("end_states") or st[-1:])
        wm = s.get("who_moves") or {}
        missing = [x for x in st if x not in ends and empty(wm.get(x))]
        if missing:
            add(s["id"], "nobody moves it on from: " + ", ".join(missing),
                "Who moves a %s on from %s?" % (word(model, s.get("object")), " / ".join("“%s”" % x for x in missing)))
        if s.get("branches") and empty(s.get("note")):
            add(s["id"], "branches = true: say in a note which process carries the parallel path (stages can't)")
    for r in model.get("roles", []):
        if empty(r.get("count")):
            add(r["id"], "no head count", "Roughly how many %s are there?" % plural(r.get("name") or r["id"]))
    for r in model.get("rules", []):
        if empty(r.get("value")):
            add(r["id"], "no value", "What's the actual limit or number for this rule: %s?" % (r.get("rule") or r["id"]))
    for s in model.get("systems", []):
        miss = [k for k in ("owns", "direction", "frequency") if empty(s.get(k))]
        if miss:
            add(s["id"], "no " + ", ".join(miss),
                "For %s: %s?" % (s.get("name") or s["id"], "; ".join({"owns": "what information does it hold",
                                                                      "direction": "does it send to the new system, receive from it, or both",
                                                                      "frequency": "how often does information need to move (as it happens, hourly, daily)"}[k] for k in miss)))
    if not model.get("channels"):
        add("channels", "none captured", "Where does each step happen: at a desk, on site, on a phone?")
    for a in model.get("ai_moments", []):
        if empty(a.get("who_confirms")):
            add(a["id"], "nobody confirms the AI's work", "If the system drafted “%s” for your team, who would check it first?" % (a.get("task") or a["id"]))
    if not model.get("outcomes"):
        add("outcomes", "none captured", "Which two or three numbers would tell you this is working?")
    ex = model.get("example_data", [])
    if not [e for e in ex if e.get("status") in ("received", "asked")]:
        add("example_data", "no example data received or promised",
            "Could you send a typical record and an awkward one, with the names and details changed?")
    ids = {x.get("id") for sec in SECTIONS for x in model.get(sec, [])}
    rids = {q["rid"] for q in reg["requirements"]} if reg else set()
    if reg:
        for q in reg["requirements"]:
            e = q.get("extra") or {}
            if empty(q.get("src_id")) or e.get("tag") not in ("C", "I", "A"):
                add(q["rid"], "no source minute or C/I/A tag")
            for m in e.get("model_refs") or []:
                if m not in ids:
                    add(q["rid"], "points at %s, which isn't in the model" % m)
    for o in model.get("open", []):
        ab = o.get("about")
        if ab and ab not in ids and ab not in rids and ab not in SECTIONS:
            G.append((ab, "open item points at something not in the model or register", None))
        if (o.get("to") or "").lower() == "us":
            G.append((ab or "open", "our action: " + (o.get("ask") or ""), None))
        else:
            G.append((ab or "open", "open question", o.get("ask")))
    return G


def render(model, reg, G, deal):
    L = ["# Solution model: %s" % (deal or model.get("customer", "")), "",
         "> `sc-workshop`, %s. Their world in Creatio terms, for `sc-demo-plan` (Part 1, Part 2, example data, home page) "
         "and the toolkit runbook. Internal. Tags: C confirmed in the room · I inferred · A assumed." % datetime.date.today().isoformat(), ""]
    for sec in SECTIONS:
        rows = model.get(sec, [])
        cols = [c for c in COLS[sec] if c == "id" or any(not empty(r.get(c)) for r in rows)] + ["tag", "src"]
        L += ["## %s" % TITLES[sec], ""]
        if not rows:
            L += ["*None captured.*", ""]
            continue
        L += ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        for r in rows:
            L.append("| " + " | ".join(fmt(r.get(c)).replace("|", "/").replace("\n", " ") for c in cols) + " |")
        L.append("")
    if reg:
        rq = [q for q in reg["requirements"] if q["scope"] == "ours"]
        pr = collections.Counter((q.get("extra") or {}).get("priority") for q in rq)
        L += ["## Requirements in the register", "", "%d ours: %d must, %d should, %d could, %d not ranked; %d tagged C." % (
            len(rq), pr["must"], pr["should"], pr["could"], pr["unconfirmed"], sum(1 for q in rq if (q.get("extra") or {}).get("tag") == "C")), ""]
    L += ["## Gaps (%d)" % len(G), ""] + (["| Where | Missing | Follow-up question |", "|---|---|---|"] +
                                           ["| %s | %s | %s |" % (w, m, q or "*ours to fix*") for w, m, q in G] if G else ["None."])
    return "\n".join(L) + "\n"


def followup(model, G):
    meta = model.get("meta", {})
    nxt = meta.get("next") or {}
    who = {}
    for o in model.get("open", []):
        if o.get("ask") and (o.get("to") or "").lower() != "us":
            who[o["ask"]] = o.get("to") or ""
    groups, seen = collections.OrderedDict(), set()
    for w, m, q in G:
        if q and q not in seen:
            seen.add(q)
            groups.setdefault(who.get(q, ""), []).append(q)
    promised = [e for e in model.get("example_data", []) if e.get("status") == "asked"]
    L = ["**Subject:** Thanks for %s: a few things to close off" % (("the workshop on " + meta["date_text"]) if meta.get("date_text") else "the workshop"), "",
         "Hi %s," % (meta.get("contact") or "<name>"), "",
         "Thanks for your time on %s. We came away with a clear picture of %s%s." % (
             meta.get("date_text") or meta.get("date") or "<date>", meta.get("journey") or "<journey>",
             (", and we'll open the next session on %s by showing it running in Creatio" % (nxt.get("date_text") or nxt.get("date"))) if nxt.get("date") else ""), ""]
    if promised:
        L += ["**What you said you'd send** (no rush, but it lets us build with your real fields and numbers):", ""] + \
             ["- %s" % e.get("what") for e in promised] + [""]
    if groups:
        L += ["**A few questions we didn't get to, or need a number for.** Short answers are fine, and anything you're "
              "not sure of can wait for the next session.", ""]
        n = 0
        for to, qs in groups.items():
            if to:
                L += ["*For %s:*" % to, ""]
            elif len(groups) > 1:
                L += ["*For anyone who knows:*", ""]
            for q in qs:
                n += 1
                L.append("%d. %s" % (n, q))
            L.append("")
        if n > 12:
            L.insert(0, "<!-- %d questions: trim to the ones that block the next build; the rest can wait for workshop %s -->" % (n, (meta.get("workshop") or 1) + 1))
    L += ["Thanks,", meta.get("from") or "<AE / SC>", "", "---"]
    return "\n".join(L) + "\n"


def check(a):
    model = json.load(open(a.model, encoding="utf-8"))
    reg = json.load(open(a.register, encoding="utf-8")) if a.register else None
    G = gaps(model, reg)
    if a.md:
        open(a.md, "w", encoding="utf-8").write(render(model, reg, G, a.deal))
    if a.followup:
        open(a.followup, "w", encoding="utf-8").write(followup(model, G))
    n = {s: len(model.get(s, [])) for s in SECTIONS}
    print("Model: " + " · ".join("%s %d" % (k, v) for k, v in n.items()))
    print("%d gaps (%d for the follow-up email, %d ours to fix)" % (len(G), sum(1 for g in G if g[2]), sum(1 for g in G if not g[2])))
    for w, m, q in G:
        print("  %-24s %s" % (w, m))
    sys.exit(1 if G else 0)


def playback(a):
    try:
        from docx import Document
        from docx.shared import Pt, RGBColor
    except ImportError:
        sys.exit("python-docx missing: python -m pip install python-docx")
    model = json.load(open(a.model, encoding="utf-8"))
    reg = json.load(open(a.register, encoding="utf-8"))
    meta = model.get("meta", {})
    deal = a.deal or model.get("customer", "")
    d = Document()
    st = d.styles["Normal"]
    st.font.name, st.font.size = "Calibri", Pt(10.5)
    d.add_heading("%s: what we heard" % deal, 0)
    when = meta.get("date_text") or meta.get("date") or datetime.date.today().isoformat()
    d.add_paragraph("Workshop playback (%s). This is our understanding of how things work today and what matters most, "
                    "in your words. Please correct anything we've got wrong. Once you're happy with it, it's the list "
                    "we'll show working in Creatio." % when)

    def table(head, rows):
        t = d.add_table(rows=1, cols=len(head))
        t.style = "Light Grid Accent 1"
        for i, h in enumerate(head):
            t.rows[0].cells[i].text = h
        for r in rows:
            cells = t.add_row().cells
            for i, v in enumerate(r):
                cells[i].text = fmt(v)
        d.add_paragraph()

    if model.get("outcomes"):
        d.add_heading("What success looks like", 1)
        table(["Measure", "Today", "Target", "Owner"],
              [[o.get("measure"), o.get("baseline") or "to confirm", o.get("target") or "to confirm", o.get("owner") or "to confirm"]
               for o in model["outcomes"]])
    rq = [q for q in reg["requirements"] if q["scope"] == "ours"]
    journeys = list(collections.OrderedDict.fromkeys(q["sheet"] for q in rq))
    steps_by = meta.get("journeys") or {}
    clean = lambda t: re.sub(r"^~\s*", "", str(t or ""))
    for j in journeys:
        d.add_heading(re.sub(r"^Workshop \d+:\s*", "", j), 1)
        steps = steps_by.get(j) or [s for s in collections.OrderedDict.fromkeys(q["section"] for q in rq if q["sheet"] == j)
                                    if s and not re.match(r"(?i)across|general|overall", s)]
        d.add_paragraph("The journey as you described it: " + " → ".join(re.sub(r"^\d+\.\s*", "", s) for s in steps))
        for label, pr in (("Must have", "must"), ("Should have", "should"), ("Could have", "could"), ("Not ranked yet", "unconfirmed")):
            rows = [[q["rid"], re.sub(r"^\d+\.\s*", "", q["section"] or ""), clean(q["text"]), (q.get("extra") or {}).get("pain")]
                    for q in rq if q["sheet"] == j and (q.get("extra") or {}).get("priority") == pr]
            if rows:
                d.add_heading(label, 2)
                table(["Ref", "Step", "What you need", "Why (what goes wrong today)"], rows)
    opens = [o.get("ask") for o in model.get("open", []) if o.get("ask") and (o.get("to") or "").lower() != "us"]
    if opens:
        d.add_heading("Still to confirm", 1)
        for o in opens:
            d.add_paragraph(o, style="List Number")
    d.add_heading("Sign-off", 1)
    d.add_paragraph("Confirmed as an accurate record of our needs for %s." % ("these journeys" if len(journeys) > 1 else "this journey"))
    d.add_paragraph("Name: ______________________   Role: ______________________   Date: ____________")
    d.save(a.out)
    pr = collections.Counter((q.get("extra") or {}).get("priority") for q in rq)
    print("Playback: %d journeys, %d requirements (%s) -> %s" % (len(journeys), len(rq), dict(pr), a.out))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("check"); p.add_argument("--model", required=True); p.add_argument("--register")
    p.add_argument("--md"); p.add_argument("--followup"); p.add_argument("--deal")
    p = sp.add_parser("playback"); p.add_argument("--model", required=True); p.add_argument("--register", required=True)
    p.add_argument("--out", required=True); p.add_argument("--deal")
    a = ap.parse_args()
    {"check": check, "playback": playback}[a.cmd](a)


if __name__ == "__main__":
    main()
