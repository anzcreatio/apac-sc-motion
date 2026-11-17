"""Turn Lessons/TEAM-LESSONS.md into an easy-read page: top 5 before every call, a filter per stage, search, one
card per lesson (do / avoid / why). The markdown stays the only source; never edit the HTML by hand.

  python team_lessons_page.py [--root <team root>] [--md <file>] [--out <file>] [--fragment]

Defaults: <team root>/Lessons/TEAM-LESSONS.md -> <team root>/Lessons/TEAM-LESSONS.html (a full page that opens in
any browser). --fragment writes the page without <!doctype>/<head>, for publishing as a claude.ai Artifact.
"""
import argparse
import html
import json
import os
import re
import sys


def team_root(arg):
    if arg:
        return arg
    try:
        with open(os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json"), encoding="utf-8") as fh:
            return json.load(fh)["sharepoint_root"]
    except (OSError, KeyError, ValueError):
        sys.exit("No team root: run sc-setup, or pass --root <SharePoint folder>")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


def parse(md):
    meta = {"status": "", "top": [], "how": ""}
    sections, cur, header = [], None, None
    for line in md.splitlines():
        if line.startswith("Status:"):
            meta["status"] = line[len("Status:"):].strip()
        elif line.startswith("**Top 5 before every call:**"):
            meta["top"] = [x.strip() for x in line.split(":**", 1)[1].split(",") if x.strip()]
        elif line.startswith("**How it grows:**"):
            meta["how"] = line.split(":**", 1)[1].strip()
        m = re.match(r"^## (\d+)\. (.+)$", line)
        if m:
            cur = {"n": m.group(1), "title": m.group(2).strip(), "lessons": [], "note": ""}
            sections.append(cur)
            header = None
            continue
        if line.startswith("## "):
            cur = None
            continue
        if cur is None:
            continue
        if line.startswith("|"):
            row = cells(line)
            if header is None:
                header = [h.lower() for h in row]
                continue
            if set("".join(row)) <= set("-: "):
                continue
            rec = dict(zip(header, row))
            lesson = {"id": rec.get("#", ""), "title": re.sub(r"\*\*", "", rec.get("lesson", "")),
                      "do": rec.get("do", ""), "avoid": rec.get("avoid", ""), "why": rec.get("why", ""),
                      "line": rec.get("in one line", "")}
            cur["lessons"].append(lesson)
        elif line.strip() and not cur["lessons"]:
            cur["note"] = (cur["note"] + " " + line.strip()).strip()
    return meta, sections


CSS = """
:root{
  /* Layout: a field card deck. Sticky stage filter, one column of lesson cards, do/avoid side by side. */
  --bg:#f4f6f8; --surface:#ffffff; --ink:#14212e; --muted:#566676; --line:#d9e0e7;
  --accent:#0b5cad; --accent-ink:#ffffff; --do:#17784a; --do-bg:#e6f4ec; --avoid:#b4232c; --avoid-bg:#fbeaea;
  --top-bg:#0f2a44; --top-ink:#eaf2fa; --chip:#e8eef5;
  --f-head:"Space Grotesk","Segoe UI",system-ui,sans-serif; --f-body:"Inter","Segoe UI",system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0e151c; --surface:#16202a; --ink:#e4ebf2; --muted:#9aa9b8; --line:#26333f;
  --accent:#5aa7f0; --accent-ink:#081521; --do:#5fd096; --do-bg:#13301f; --avoid:#f2828a; --avoid-bg:#3a1a1d;
  --top-bg:#0b1f33; --top-ink:#dbe8f5; --chip:#1d2a36; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0e151c; --surface:#16202a; --ink:#e4ebf2; --muted:#9aa9b8; --line:#26333f;
  --accent:#5aa7f0; --accent-ink:#081521; --do:#5fd096; --do-bg:#13301f; --avoid:#f2828a; --avoid-bg:#3a1a1d;
  --top-bg:#0b1f33; --top-ink:#dbe8f5; --chip:#1d2a36; color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 var(--f-body)}
.wrap{max-width:880px;margin:0 auto;padding-block:28px 64px;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
header h1{font:700 30px/1.15 var(--f-head);margin:0 0 6px;text-wrap:balance}
header p{margin:0;color:var(--muted);max-width:65ch}
.status{display:inline-block;margin-top:10px;font-size:12px;letter-spacing:.04em;text-transform:uppercase;
  color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:2px 10px}
.top{margin-top:22px;background:var(--top-bg);color:var(--top-ink);border-radius:14px;padding:18px 18px 8px}
.top h2{font:600 13px/1 var(--f-body);letter-spacing:.08em;text-transform:uppercase;margin:0 0 12px;opacity:.85}
.top ol{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.top li{display:flex;gap:12px;align-items:baseline;padding-bottom:10px;border-bottom:1px solid rgba(255,255,255,.12)}
.top li:last-child{border-bottom:0}
.top .id{font:600 12px/1 var(--f-head);opacity:.7;min-width:28px}
.top b{font-weight:600}
.top span.do{opacity:.85;display:block;font-size:14px}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);padding-block:14px 10px;
  display:flex;flex-wrap:wrap;gap:8px;align-items:center;border-bottom:1px solid var(--line);margin-top:22px}
.bar button{font:500 13px/1 var(--f-body);border:1px solid var(--line);background:var(--chip);color:var(--ink);
  border-radius:999px;padding:8px 12px;cursor:pointer}
.bar button[aria-pressed="true"]{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.bar button:focus-visible,.bar input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.bar input{flex:1 1 180px;min-width:0;font:14px var(--f-body);padding:8px 12px;border-radius:999px;
  border:1px solid var(--line);background:var(--surface);color:var(--ink)}
section.stage{margin-top:26px}
section.stage h2{font:600 20px/1.2 var(--f-head);margin:0 0 4px}
section.stage .note{color:var(--muted);margin:0 0 10px;font-size:14px}
.cards{display:grid;gap:12px;margin-top:10px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px}
.card h3{margin:0 0 10px;font:600 16px/1.3 var(--f-head);display:flex;gap:10px;align-items:baseline}
.card h3 .id{font:600 12px/1 var(--f-head);color:var(--muted);min-width:26px}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.pair div{border-radius:8px;padding:10px 12px;min-width:0;font-size:14px}
.pair .do{background:var(--do-bg)} .pair .avoid{background:var(--avoid-bg)}
.pair .lab{display:block;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;margin-bottom:3px}
.pair .do .lab{color:var(--do)} .pair .avoid .lab{color:var(--avoid)}
.why{margin:10px 0 0;color:var(--muted);font-size:14px}
.why b{color:var(--ink);font-weight:600}
.one{margin:0;font-size:14px}
code{font-size:.92em;background:var(--chip);padding:1px 5px;border-radius:4px}
.empty{color:var(--muted);margin-top:24px}
footer{margin-top:40px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:14px}
@media (max-width:560px){.pair{grid-template-columns:1fr} header h1{font-size:25px}}
"""

JS = """
(function(){
  var btns=[].slice.call(document.querySelectorAll('.bar button'));
  var q=document.getElementById('q'); var stage='all';
  function apply(){
    var term=(q.value||'').toLowerCase(), any=false;
    document.querySelectorAll('section.stage').forEach(function(s){
      var show=stage==='all'||s.dataset.stage===stage, n=0;
      s.querySelectorAll('.card').forEach(function(c){
        var ok=show&&(!term||c.textContent.toLowerCase().indexOf(term)>-1); c.hidden=!ok; if(ok)n++;});
      s.hidden=n===0; if(n)any=true;});
    document.getElementById('empty').hidden=any;
  }
  btns.forEach(function(b){b.addEventListener('click',function(){
    stage=b.dataset.stage; btns.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')}); apply();});});
  q.addEventListener('input',apply);
})();
"""


def render(meta, sections, fragment):
    index = {l["id"]: l for s in sections for l in s["lessons"]}
    out = []
    if not fragment:
        out.append('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
                   '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">')
    out.append('<title>APAC SC Team Lessons</title>')
    out.append('<meta name="claude:viewport-fit-sides" content="cover">')
    out.append('<link rel="preconnect" href="https://fonts.googleapis.com">'
               '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
               '&family=Space+Grotesk:wght@600;700&display=swap">')
    out.append("<style>%s</style>" % CSS)
    if not fragment:
        out.append("</head><body>")
    total = sum(len(s["lessons"]) for s in sections)
    out.append('<div class="wrap"><header><h1>Team lessons</h1>'
               '<p>What the APAC SC team has learnt on real deals: what to do, what to avoid, and why. '
               'No names, no deals.</p>')
    if meta["status"]:
        out.append('<span class="status">%s · %d lessons</span>' % (html.escape(meta["status"]), total))
    out.append("</header>")
    top = [index[i] for i in meta["top"] if i in index]
    if top:
        out.append('<div class="top"><h2>Before every call: the top %d</h2><ol>' % len(top))
        for l in top:
            out.append('<li><span class="id">%s</span><div><b>%s</b><span class="do">%s</span></div></li>' % (
                html.escape(l["id"]), inline(l["title"]), inline(l["do"] or l["line"])))
        out.append("</ol></div>")
    out.append('<nav class="bar" aria-label="Filter lessons"><button type="button" data-stage="all" '
               'aria-pressed="true">All</button>')
    for s in sections:
        short = re.sub(r"^(In the meeting: )", "", s["title"])
        out.append('<button type="button" data-stage="%s" aria-pressed="false">%s</button>' % (
            s["n"], html.escape(short.split(",")[0])))
    out.append('<input id="q" type="search" placeholder="Search, e.g. AI, stand, closing" aria-label="Search lessons">'
               "</nav>")
    for s in sections:
        out.append('<section class="stage" data-stage="%s"><h2>%s. %s</h2>' % (s["n"], s["n"], inline(s["title"])))
        if s["note"]:
            out.append('<p class="note">%s</p>' % inline(s["note"]))
        out.append('<div class="cards">')
        for l in s["lessons"]:
            out.append('<article class="card"><h3><span class="id">%s</span>%s</h3>' % (
                html.escape(l["id"]), inline(l["title"])))
            if l["do"] or l["avoid"]:
                out.append('<div class="pair"><div class="do"><span class="lab">Do</span>%s</div>'
                           '<div class="avoid"><span class="lab">Avoid</span>%s</div></div>' % (
                               inline(l["do"]), inline(l["avoid"])))
            if l["line"]:
                out.append('<p class="one">%s</p>' % inline(l["line"]))
            if l["why"]:
                out.append('<p class="why"><b>Why:</b> %s</p>' % inline(l["why"]))
            out.append("</article>")
        out.append("</div></section>")
    out.append('<p class="empty" id="empty" hidden>No lesson matches that search.</p>')
    out.append("<footer>%s<br>Built from <code>Lessons/TEAM-LESSONS.md</code>: change the lessons there, then re-run "
               "<code>team_lessons_page.py</code>.</footer></div>" % inline(meta["how"]))
    out.append("<script>%s</script>" % JS)
    if not fragment:
        out.append("</body></html>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--md")
    ap.add_argument("--out")
    ap.add_argument("--fragment", action="store_true")
    x = ap.parse_args()
    if x.md and x.out:
        md_path, out_path = x.md, x.out
    else:
        lessons = os.path.join(team_root(x.root), "Lessons")
        md_path = x.md or os.path.join(lessons, "TEAM-LESSONS.md")
        out_path = x.out or os.path.join(lessons, "TEAM-LESSONS.html")
    with open(md_path, encoding="utf-8") as fh:
        meta, sections = parse(fh.read())
    if not sections:
        sys.exit("No '## N. Stage' sections found in %s" % md_path)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(render(meta, sections, x.fragment))
    print("wrote %s (%d stages, %d lessons, top %d)" % (
        out_path, len(sections), sum(len(s["lessons"]) for s in sections), len(meta["top"])))


if __name__ == "__main__":
    main()
