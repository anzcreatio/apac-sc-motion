"""AE brief page for a demo session (sc-demo-plan output). Writes only the new HTML file.

    python build_ae_brief.py <ae-brief.json> --out <deal>/NN-ae-brief.html          (Mac: python3)

The page works offline in any browser (double-click it), or the SC publishes it as an artifact and sends the AE the
link. The AE's ticks and notes stay in their own browser. Format of ae-brief.json: see ../SKILL.md "AE brief".
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "templates", "ae-brief.html")
OUR_TERMS = ["Freedom UI", "Business Studio", "clio", "DCM"]


def check(d):
    E, W = [], []
    for k in ("deal", "title", "when", "ae", "sc", "them", "recap", "question", "next_step", "dont"):
        if not d.get(k):
            E.append("missing %s" % k)
    if E:
        return E, W
    if not 2 <= len(d["recap"]) <= 4:
        W.append("recap has %d points: 3 is best (2-4)" % len(d["recap"]))
    if not d["next_step"].get("suggestion"):
        E.append("next_step.suggestion is empty: say what next step we want booked")
    if len(d["question"]) > 120:
        W.append("the question is long: the AE reads it word for word")
    if re.search(r"(?i)success", " ".join(d["recap"])):
        W.append("recap mentions success criteria: get those before the meeting, not live")
    text = json.dumps(d, ensure_ascii=False)
    for t in OUR_TERMS:
        if t.lower() in text.lower():
            W.append("uses '%s': the AE brief is plain English" % t)
    return E, W


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brief_json")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = json.load(open(a.brief_json, encoding="utf-8"))
    E, W = check(d)
    for w in W:
        print("WARNING", w)
    if E:
        sys.exit("Not built: " + "; ".join(E))
    html = open(TEMPLATE, encoding="utf-8").read()
    data = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("/*AE_BRIEF_DATA*/{}", data, 1)
    html = html.replace("<title>AE Brief</title>", "<title>%s AE Brief</title>" % d["deal"].replace("<", ""), 1)
    open(a.out, "w", encoding="utf-8").write(html)
    print("AE brief -> %s (%d recap points, %d licence questions)" % (a.out, len(d["recap"]), len(d.get("licence", []))))


if __name__ == "__main__":
    main()
