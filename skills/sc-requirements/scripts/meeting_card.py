"""Build the one-page meeting card: what to say when the customer asks "tell us what we need".

  python meeting_card.py --industry multifinance [--journey "Loan origination" ...] [--deal <deal folder>]
                         [--out <file.html>] [--draft]

Reads ../../../knowledge/requirements-library.json (approved lines only; --draft shows unapproved seed lines under a
DRAFT banner) and the shared product-limits register on SharePoint (lines linked to an open limit are left out and
the limit is listed as "check first"). Writes one self-contained HTML page, readable on a phone. INTERNAL: for the SC.
"""
import argparse
import datetime
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(HERE, "..", "..", "..", "knowledge", "requirements-library.json"))
INDUSTRY_NAMES = {"banking": "Banking", "multifinance": "Multifinance lending", "service": "Omnichannel customer service"}


def team_root():
    try:
        with open(os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json"), encoding="utf-8") as fh:
            return json.load(fh).get("sharepoint_root")
    except (OSError, ValueError):
        return None


def open_limits(root):
    if not root:
        return []
    p = os.path.join(root, "Lessons", "registers", "product-limits.json")
    try:
        with open(p, encoding="utf-8") as fh:
            return [e for e in json.load(fh).get("entries", []) if e.get("status") == "open"]
    except (OSError, ValueError):
        return []


def esc(s):
    return html.escape(str(s or ""))


CSS = """
:root{--ink:#1d2433;--body:#3b4252;--grey:#6b7280;--acc:#ff4013;--teal:#0b7a75;--soft:#f6f7f9;--line:#e5e7eb;--draft:#7a5300;--draft-bg:#fff6e0}
*{box-sizing:border-box}body{margin:0;font:15px/1.45 -apple-system,Segoe UI,Roboto,Arial,sans-serif;color:var(--body);background:#fff}
.wrap{max-width:860px;margin:0 auto;padding:16px}
h1{font-size:22px;color:var(--ink);margin:4px 0 2px}.sub{color:var(--grey);font-size:13px;margin-bottom:12px}
.draft{background:var(--draft-bg);color:var(--draft);border-radius:8px;padding:8px 12px;font-weight:600;margin:8px 0}
.moves{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:12px 0 16px}
.move{background:var(--soft);border-radius:10px;padding:10px 12px}.move b{display:block;color:var(--acc);font-size:12px;letter-spacing:.04em;text-transform:uppercase;margin-bottom:4px}
.move span{color:var(--ink);font-weight:600}
.top3{border:2px solid var(--acc);border-radius:12px;padding:10px 14px;margin:0 0 18px}
.top3 h2{font-size:15px;color:var(--acc);margin:2px 0 8px;text-transform:uppercase;letter-spacing:.04em}
.top3 li{margin:4px 0;color:var(--ink)}
details{border:1px solid var(--line);border-radius:10px;margin:0 0 10px;background:#fff}
summary{cursor:pointer;padding:10px 14px;font-weight:700;color:var(--ink);list-style:none}
summary::-webkit-details-marker{display:none}summary small{color:var(--grey);font-weight:400}
.stage{padding:0 14px 6px}.stage h3{font-size:13px;color:var(--teal);text-transform:uppercase;letter-spacing:.05em;margin:10px 0 4px}
.line{border-top:1px solid var(--line);padding:8px 0}.line:first-of-type{border-top:0}
.req{color:var(--ink);font-weight:600}.why{font-size:14px}.meta{font-size:12px;color:var(--grey);margin-top:2px}
.chip{display:inline-block;font-size:11px;font-weight:700;border-radius:999px;padding:1px 8px;margin-right:4px;vertical-align:1px}
.proven{background:#e6f4f1;color:var(--teal)}.standard{background:#eef2ff;color:#3949ab}.first{background:#ffe9e2;color:var(--acc)}
.check{background:var(--draft-bg);border-radius:10px;padding:10px 14px;margin:14px 0}.check h2{font-size:14px;margin:0 0 6px;color:var(--draft)}
.foot{color:var(--grey);font-size:12px;margin:18px 0 8px}
@media (max-width:600px){.moves{grid-template-columns:1fr}}
"""


def card(industry, lines, limits, deal, draft):
    name = INDUSTRY_NAMES.get(industry, industry)
    journeys = []
    for ln in lines:
        if ln["journey"] not in journeys:
            journeys.append(ln["journey"])
    top = [ln for ln in lines if ln.get("recommend_first")]
    top.sort(key=lambda l: (l.get("proof") != "proven", l["id"]))
    out = ["<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>",
           "<title>%s meeting card</title><style>%s</style></head><body><div class='wrap'>" % (esc(name), CSS)]
    out.append("<h1>If they ask what they need: %s</h1>" % esc(name))
    out.append("<div class='sub'>%sInternal, for the SC only · built %s from the requirements library</div>"
               % ("%s · " % esc(deal) if deal else "", datetime.date.today().isoformat()))
    if draft:
        out.append("<div class='draft'>DRAFT: includes lines Renzo hasn't approved yet. Don't rely on unapproved lines in a meeting.</div>")
    out.append("<div class='moves'><div class='move'><b>1 · Peers</b><span>\"What we see at organisations like yours is…\"</span> 2-3 lines from their stage</div>"
               "<div class='move'><b>2 · Recommend</b><span>\"For you, I'd start with…\"</span> the top 3 below</div>"
               "<div class='move'><b>3 · Ask</b><span>\"Which of these matter most to you?\"</span> their ranking goes in the review as C</div></div>")
    out.append("<div class='top3'><h2>I'd start with</h2><ol>")
    for ln in top[:3]:
        out.append("<li>%s <span class='chip %s'>%s</span></li>" % (esc(ln["requirement"]), ln.get("proof"), "we can show you" if ln.get("proof") == "proven" else "standard"))
    out.append("</ol></div>")
    for j in journeys:
        jl = [ln for ln in lines if ln["journey"] == j]
        out.append("<details%s><summary>%s <small>· %d lines</small></summary>" % (" open" if j == journeys[0] else "", esc(j), len(jl)))
        stages = []
        for ln in jl:
            if ln["stage"] not in stages:
                stages.append(ln["stage"])
        for st in stages:
            out.append("<div class='stage'><h3>%s</h3>" % esc(st))
            for ln in [l for l in jl if l["stage"] == st][:8]:
                chips = "<span class='chip %s'>%s</span>" % (ln.get("proof"), "we can show you" if ln.get("proof") == "proven" else "standard")
                if ln.get("recommend_first"):
                    chips += "<span class='chip first'>start here</span>"
                meta = " · ".join(x for x in [ln.get("kpi") or "", ("Show: " + ln["how_we_show"]) if ln.get("how_we_show") else "", ln.get("diff") or ""] if x)
                out.append("<div class='line'>%s<div class='req'>%s</div><div class='why'>%s</div><div class='meta'>%s</div></div>"
                           % (chips, esc(ln["requirement"]), esc(ln.get("why")), esc(meta)))
            out.append("</div>")
        out.append("</details>")
    if limits:
        out.append("<div class='check'><h2>Check first: known limits</h2><ul>")
        for e in limits:
            out.append("<li><b>%s:</b> %s%s <small>(%s, %s)</small></li>" % (esc(e.get("area")), esc(e.get("limit")),
                       (" Workaround: " + esc(e["workaround"])) if e.get("workaround") else "", esc(e.get("id")), esc(e.get("source"))))
        out.append("</ul></div>")
    out.append("<div class='foot'>\"Start here\" and \"we can show you\" lines are proven on a demo or standard in the product. Anything not on this card: \"we'll confirm in writing\". Claims only from the differentiator catalogue.</div>")
    out.append("</div></body></html>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--industry", required=True, choices=sorted(INDUSTRY_NAMES))
    ap.add_argument("--journey", action="append", help="limit to these journeys (repeatable)")
    ap.add_argument("--deal", help="deal folder; the card is written there by default")
    ap.add_argument("--out")
    ap.add_argument("--draft", action="store_true", help="include lines not yet approved, under a DRAFT banner")
    ap.add_argument("--library", default=LIB)
    a = ap.parse_args()
    with open(a.library, encoding="utf-8") as fh:
        lib = json.load(fh)
    lines = [l for l in lib["lines"] if l["industry"] == a.industry and (a.draft or l.get("approved"))
             and l.get("fit") in ("standard", "configure")]
    if a.journey:
        lines = [l for l in lines if l["journey"] in a.journey]
    limits = open_limits(team_root())
    blocked = {lid for e in limits for lid in [e.get("id")]}
    lines = [l for l in lines if not set(l.get("limits") or []) & blocked]
    if not lines:
        sys.exit("No %slines for %s%s. Approve the seed, or use --draft." % ("" if a.draft else "approved ", a.industry,
                 " / " + ", ".join(a.journey) if a.journey else ""))
    deal_name = os.path.basename(os.path.normpath(a.deal)) if a.deal else None
    out = a.out or os.path.join(a.deal or ".", "meeting-card-%s.html" % a.industry)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(card(a.industry, lines, limits, deal_name, a.draft or not all(l.get("approved") for l in lines)))
    print("meeting card -> %s (%d lines, %d journeys, %d known limits)" % (out, len(lines), len({l['journey'] for l in lines}), len(limits)))


if __name__ == "__main__":
    main()
