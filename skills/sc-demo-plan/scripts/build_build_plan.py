"""Build plan page the SC reviews BEFORE anything is built (sc-demo-plan step 12a, sc-first-meeting step 6b).

    python build_build_plan.py <build-plan.json> --out <deal>/NN-build-plan.html          (Mac: python3)

Writes one self-contained HTML page (works offline; or publish it as a private artifact and send the SC the link).
Each demo step gets a wireframe drawn from a few standard Creatio layouts, so a deal only writes content, not HTML.
Format of build-plan.json: see ../SKILL.md "Build plan".
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "templates", "build-plan.html")
SCREEN_TYPES = {"record", "list", "table", "dashboard", "panel", "beforeafter", "custom"}
CUSTOM_LAYOUTS = {"journey": "steps", "matrix": "items", "scorer": "criteria", "trace": "rows"}
CHIPS = {"built", "simulated", "existing", "parked"}
TAGS = {"C", "P", "I", "A"}
DIFFS = {"D1", "D2", "D3", "D4", "D5", "D6", "D7"}
COVERAGE = {"covered", "partly", "not shown"}


def check_screen(s, where, E):
    t = s.get("type")
    if t not in SCREEN_TYPES:
        E.append("%s: screen type '%s' is not one of %s" % (where, t, sorted(SCREEN_TYPES)))
        return
    if t == "beforeafter":
        for k in ("before", "after"):
            if k not in s:
                E.append("%s: beforeafter needs '%s'" % (where, k))
            else:
                check_screen(s[k], "%s.%s" % (where, k), E)
        return
    if not s.get("page"):
        E.append("%s: screen has no 'page' name" % where)
    for c, w in ([(s, where)] if t == "custom" else []) + ([(s["custom"], where + ".custom")] if s.get("custom") else []):
        lay = c.get("layout")
        if lay not in CUSTOM_LAYOUTS:
            E.append("%s: custom layout '%s' is not one of %s" % (w, lay, sorted(CUSTOM_LAYOUTS)))
        elif not c.get(CUSTOM_LAYOUTS[lay]):
            E.append("%s: custom %s needs '%s'" % (w, lay, CUSTOM_LAYOUTS[lay]))
        if not c.get("component"):
            E.append("%s: custom component needs a 'component' name (it's marked custom in the plan)" % w)
    if t == "record" and "stages" in s and not 0 <= s.get("stage", -1) < len(s["stages"]):
        E.append("%s: 'stage' must index into 'stages'" % where)
    for tbl in [s] + ([s["list"]] if s.get("list") else []):
        cols = tbl.get("columns")
        for r in tbl.get("rows", []) if cols else []:
            if len(r) != len(cols):
                E.append("%s: a row has %d cells for %d columns" % (where, len(r), len(cols)))
                break


def norm(s):
    """Lower case, straight quotes, one space: so a quote matches the transcript however it was typed."""
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip().lower()


def load_sources(d, base):
    text = []
    for f in d.get("sources", []):
        p = os.path.join(base, f)
        if not os.path.exists(p):
            sys.exit("Not built: source file not found: %s" % p)
        text.append(open(p, encoding="utf-8").read())
    return norm("\n".join(text))


def check(d, sources=""):
    E, W = [], []
    if not d.get("sources"):
        W.append("no 'sources': customer quotes can't be checked against the transcript or email")
    for k in ("deal", "title", "one_line", "decision", "steps", "build", "data", "not_built", "decisions"):
        if not d.get(k):
            E.append("missing %s" % k)
    if E:
        return E, W
    for i, st in enumerate(d["steps"], 1):
        w = "step %d" % i
        for k in ("title", "screen", "click", "say"):
            if not st.get(k):
                E.append("%s: missing %s" % (w, k))
        if st.get("screen"):
            check_screen(st["screen"], w, E)
        for c in st.get("chips", []):
            if c not in CHIPS:
                W.append("%s: chip '%s' isn't one of %s" % (w, c, sorted(CHIPS)))
        idea = st.get("our_idea")
        if idea:
            for k in ("why", "source", "ask"):
                if not idea.get(k):
                    E.append("%s: our_idea needs '%s' (a blind spot must be sourced and asked as a question)" % (w, k))
        elif not st.get("triggers"):
            E.append("%s: no trigger. Quote what the customer said, or mark it our_idea with a source" % w)
        for t in st.get("triggers", []):
            if t.get("tag", "C") not in TAGS:
                E.append("%s: trigger tag must be C, P, I or A" % w)
            if t.get("tag", "C") in ("C", "P") and sources:
                missing = [part for part in re.split(r"\s*(?:\.\.\.|…)\s*", t.get("quote", "")) if part.strip()
                           and norm(part) not in sources]
                if missing:
                    E.append("%s: quote not found word for word in the sources: '%s'" % (w, missing[0][:70]))
        dif = st.get("differentiator")
        if not dif:
            W.append("%s: no differentiator (D1-D7): which point do we win here?" % w)
        elif dif.get("id") not in DIFFS:
            E.append("%s: differentiator id must be one of D1-D7" % w)
        if not st.get("minutes"):
            W.append("%s: no minutes" % w)
    ideas = sum(1 for s in d["steps"] if s.get("our_idea"))
    if ideas > 2:
        E.append("%d 'our idea' steps: at most 2, their own pains come first" % ideas)
    elif ideas == 0:
        W.append("no 'our idea' step: is there a blind spot worth one question? (industry pack, research, pattern book)")
    first_idea = next((i for i, s in enumerate(d["steps"]) if s.get("our_idea")), None)
    if first_idea is not None and any(not s.get("our_idea") and s.get("triggers") and i > first_idea
                                      and not s.get("screen", {}).get("type") == "beforeafter"
                                      for i, s in enumerate(d["steps"])):
        W.append("an 'our idea' step comes before customer steps: earn it first, show their pains first")
    mins = sum(float(s.get("minutes", 0)) for s in d["steps"])
    if d.get("demo_minutes") and mins > d["demo_minutes"]:
        W.append("scenes add up to %g min in a %g min demo slot: cut or shorten" % (mins, d["demo_minutes"]))
    for c in d.get("criteria", []):
        if c.get("coverage") not in COVERAGE:
            E.append("criterion '%s': coverage must be one of %s" % (c.get("criterion"), sorted(COVERAGE)))
        elif c["coverage"] != "covered" and not c.get("say"):
            E.append("criterion '%s' is %s: add what we say about the gap" % (c.get("criterion"), c["coverage"]))
    if not d.get("criteria"):
        W.append("no criteria table: if they gave us criteria (RFP, email), map every one")
    if not any(s.get("screen", {}).get("type") == "beforeafter" for s in d["steps"]):
        W.append("no before/after step: show the live change as its own card")
    total = sum(float(b.get("hours", 0)) for b in d["build"] if b.get("status") != "parked")
    budget = d.get("budget_hours")
    if budget and total > budget:
        W.append("build is %.2g h against a %.2g h budget: say why in build_note, or cut" % (total, budget))
        if not d.get("build_note"):
            E.append("over budget with no build_note")
    if len(d["steps"]) > 8:
        W.append("%d steps: a 60-minute demo carries 3-4 scenes; check the cut" % len(d["steps"]))
    return E, W


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan_json")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = json.load(open(a.plan_json, encoding="utf-8"))
    sources = load_sources(d, os.path.dirname(os.path.abspath(a.plan_json)))
    E, W = check(d, sources)
    for w in W:
        print("WARNING", w)
    if E:
        sys.exit("Not built: " + "; ".join(E))
    html = open(TEMPLATE, encoding="utf-8").read()
    data = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("/*BUILD_PLAN_DATA*/{}", data, 1)
    html = html.replace("<title>Build Plan</title>", "<title>%s Build Plan</title>" % d["deal"].replace("<", ""), 1)
    open(a.out, "w", encoding="utf-8").write(html)
    total = sum(float(b.get("hours", 0)) for b in d["build"] if b.get("status") != "parked")
    mins = sum(float(s.get("minutes", 0)) for s in d["steps"])
    ideas = sum(1 for s in d["steps"] if s.get("our_idea"))
    print("Build plan -> %s (%d steps, %g min, %d our idea, %.2g h)" % (a.out, len(d["steps"]), mins, ideas, total))


if __name__ == "__main__":
    main()
