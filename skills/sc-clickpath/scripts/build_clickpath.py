"""Build the two click-path pages for a demo from the toolkit's click-path cards.

Usage:
    python build_clickpath.py <cards.json> [--customer <clickpath-customer.json>] [--sc <clickpath-sc.json>]
                              [--credentials <file>] [--shots <dir>] [--out <dir>] [--slug <name>] [--fragment]
                              [--approved]

Inputs
  cards.json        the creatio-demo-clickpass cards (title, persona, before_start, reset, sections, cards[...]).
  --sc              SC teaching overlay (default: clickpath-sc.json beside cards.json). Per step: open {record, find,
                    state}, clicks [...], type [[field, value]], see, they_said [{quote, who, at, tag, partner}],
                    land {point, why, kpi, d_id, d_line}, say, if_they_ask [{q, a, source}], watch, signed_in.
                    Per use case (use_cases.UC1): value_story, pain [{quote, who, at, tag}], bridge.
                    Top level: logins [{role, username, url, steps}], faq [{q, a, source}], notes [...].
                    Rules the builder enforces: "they said" keeps tag C only (I/A dropped and reported); an answer
                    without a source becomes "We'll confirm that in writing."; d_id must be in the catalogue.
  --credentials     the demo passwords. Default: the team's one file <SharePoint root>/Stand-logins/stand-logins.json,
                    {"<stand>": {"<username>": "<password>"}}, matched on cards.json "instance". Also accepts (JSON {username: password} or
                    [{username, password}], or text lines "username: password" / "username = password" /
                    "| username | password |"). Read by this script only; Claude never opens it. Passwords go
                    into the SC page in plain view (also the --fragment copy), never into the customer page.
  --customer        overlay with the customer-facing words (default: clickpath-customer.json beside cards.json):
                    {customer, page_name, title, eyebrow, date, intro, simulated, contact, approved,
                     sections: {UC1: "heading"}, titles: {"UC1-2": "..."}, cards: {"UC1-2": "what it means for them"},
                     hide: [...], crop: {"UC1-3": [l, t, r, b] fractions}, screens_reviewed: [...]}
  --shots           screenshot folder (default: shots/ beside cards.json)

Outputs (default: the folder of cards.json)
  <slug>-click-path-sc.html        for the SC: per step open / click / you'll see / they said / land this / say /
                                   if they ask / watch out / signed in as; per use case the value story, pain and
                                   bridge; before you start with logins; practice mode hides say, land this and
                                   if they ask until you click; rehearsal ticks
  <slug>-click-path-customer.html  for the customer: screenshots and plain words only. DRAFT banner until approved
                                   ("approved": true or --approved), refused while a check fails or a shown screenshot
                                   is not in screens_reviewed. Any login, username or password in its text stops the
                                   build (exit 2, no customer file written).
Layout: the Creatio explorer shell (masthead + stat strip, clickable flow strip, tabs, sticky filter rail, collapsible
use cases with step rows). One light brand theme (Creatio brand: no dark backgrounds). Both files are self-contained
(screenshots and logo embedded) and work offline. --fragment writes them without the <!doctype>/<html>/<body>
wrapper, for publishing as a Claude artifact.
"""
import argparse
import base64
import html
import io
import json
import os
import re
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "sc-deck", "scripts"))
try:
    from build_deck import VENDOR_WORDS, AI_TELLS  # same style rules as the deck
except Exception:  # pragma: no cover
    VENDOR_WORDS, AI_TELLS = re.compile(r"$^"), []

LOGO_FILE = os.path.join(HERE, "creatio-logo.txt")
LOGO = open(LOGO_FILE).read().strip() if os.path.isfile(LOGO_FILE) else ""

# Anything that must never reach a customer.
INTERNAL = [
    (re.compile(r"\b\d{8}-demo\b|\.creatio\.com", re.I), "stand name or URL"),
    (re.compile(r"\b(Usr|Rsw|lab)[A-Z]\w+"), "schema or package name"),
    (re.compile(r"\b(Supervisor|Administrator ?\d?|SysAdmin|clio|runbook|rehears\w*|reset|snapshot|seeded|seed data)\b", re.I), "internal demo wording"),
    (re.compile(r"\[(C|I|A|P)\b[^\]]*\]|\b(SC check|SC h)\b"), "evidence tag or SC note"),
    (re.compile(r"\b(caution|careful|warning|TODO|TBC|workaround|bug|hack|fake|faked|don't press|do not press|don't say|do not say)\b", re.I), "presenter caution"),
    (re.compile(r"\b(price|pricing|discount|licen[cs]e cost|\$\s?\d+k? per)\b", re.I), "pricing"),
]
# Logins and passwords never reach a customer: any hit stops the build.
LOGIN_RX = re.compile(r"\b(passwords?|passwd|pwd|log-?ins?|usernames?|user names?|sign(ed)?[- ]in as|credentials?)\b", re.I)

PLUGIN_ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
CONFIRM = "We'll confirm that in writing."


def catalogue_ids():
    """D-IDs and titles from knowledge/DIFFERENTIATOR-CATALOGUE-*.md (claims come only from there)."""
    kdir = os.path.join(PLUGIN_ROOT, "knowledge")
    ids = {}
    for f in sorted(os.listdir(kdir)) if os.path.isdir(kdir) else []:
        if f.startswith("DIFFERENTIATOR-CATALOGUE"):
            for m in re.finditer(r"^### (D\d+) · (.+?)(?: \(|$)", open(os.path.join(kdir, f), encoding="utf-8").read(), re.M):
                ids[m.group(1)] = m.group(2).strip()
    return ids


def team_logins_file():
    """The team's one logins file: <SharePoint root>/Stand-logins/stand-logins.json (root from ~/.apac-sc-motion.json)."""
    try:
        root = json.load(open(os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json"), encoding="utf-8"))["sharepoint_root"]
    except Exception:
        return None
    for name in ("stand-logins.json", "stand-logins.json.txt"):  # Notepad often adds .txt
        p = os.path.join(root, "Stand-logins", name)
        if os.path.isfile(p):
            if os.path.getsize(p) == 0:
                print("Logins file %s is empty: add the stand's logins and save it." % name)
                return None
            return p
    return None


def read_credentials(path, usernames, stand=None):
    """Passwords for the given usernames. The team file is {"<stand>": {"<username>": "<password>"}}; a flat
    {username: password} file also works. Values are never printed."""
    found = {}
    if not path:
        return found
    raw = open(path, encoding="utf-8-sig").read()
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and any(isinstance(v, dict) for v in data.values()):
            data = data.get(stand) or {}
        if isinstance(data, dict):
            found = {k: str(v.get("password") if isinstance(v, dict) else v) for k, v in data.items()
                     if isinstance(v, (str, int)) or (isinstance(v, dict) and v.get("password"))}
        elif isinstance(data, list):
            found = {str(d.get("username") or d.get("login")): str(d.get("password")) for d in data
                     if isinstance(d, dict) and d.get("password")}
    except ValueError:
        for line in raw.splitlines():
            cells = [c.strip().strip("`*") for c in line.strip().strip("|").split("|")] if "|" in line else None
            for u in usernames:
                if cells and len(cells) >= 2 and u in cells[:-1]:
                    i = cells.index(u)
                    if i + 1 < len(cells) and cells[i + 1]:
                        found.setdefault(u, cells[i + 1])
                m = re.match(r"^\s*[-*]?\s*`?%s`?\s*[:=]\s*`?(.+?)`?\s*$" % re.escape(u), line)
                if m:
                    found.setdefault(u, m.group(1))
    return {u: found[u] for u in usernames if u in found}


def stand_logins(path, stand):
    """Every login the team file holds for this stand, as clickpath logins (no passwords): [{role, username, ...}].
    A value may be a plain password or {"password": ..., "role": ..., "steps": ...}."""
    try:
        data = json.load(open(path, encoding="utf-8-sig"))
    except Exception:
        return []
    entries = data.get(stand) if isinstance(data, dict) else None
    out = []
    for u, v in (entries or {}).items() if isinstance(entries, dict) else []:
        v = v if isinstance(v, dict) else {}
        out.append({"username": u, "role": v.get("role") or "Demo login", "steps": v.get("steps") or "",
                    "url": "https://%s.creatio.com" % stand if re.match(r"^\d{8}-demo$", stand or "") else ""})
    return out


def esc(s):
    return html.escape(str(s or ""), quote=True)


def card_key(c):
    return "%s-%s" % (c.get("uc", ""), c.get("step", ""))


def img_data(path, max_w=1400, crop=None):
    """crop = [left, top, right, bottom] as fractions of the image (0-1), to cut out what a customer mustn't see."""
    im = Image.open(path)
    if crop:
        w, h = im.size
        im = im.crop((round(crop[0] * w), round(crop[1] * h), round(crop[2] * w), round(crop[3] * h)))
    if im.mode not in ("RGB", "L"):
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.split()[-1] if im.mode in ("RGBA", "LA") else None)
        im = bg
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=84, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.width, im.height


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600'
         '&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">')

STYLE = """
<style>
/* Layout: the Creatio explorer shell (masthead + stat strip, demo-flow strip, tabs, sticky filter rail,
   use case > step rows). Creatio brand forbids dark backgrounds, so the page commits to one light theme
   and paints every colour explicitly. */
:root{
  --bg:#FFFFFF; --bg-alt:#F0F0F0; --bg-alt2:#E7E7E7;
  --text-primary:#0A0A0A; --text-body:#5C5C5C; --text-caption:#888888;
  --accent:#FF4013; --accent-deep:#C6350F; --accent-tint:#FFF1EC;
  --say-bg:#FFF1EC; --said-bg:#EEF3FA; --said-text:#1B3354; --land-bg:#EAF5EC; --land-text:#1E4D29; --watch-bg:#FFF6E0; --watch-text:#7A5300; --draft-bg:#FFF6E0; --draft-text:#7A5300;
  --font-head:'Montserrat',system-ui,-apple-system,'Segoe UI',sans-serif;
  --font-body:'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif;
  --font-mono:'IBM Plex Mono',ui-monospace,'SFMono-Regular',Menlo,monospace;
  color-scheme:light;
}
*{box-sizing:border-box}
html{background:var(--bg)}
body{background:var(--bg); color:var(--text-body); font-family:var(--font-body); font-size:15px; line-height:1.55; margin:0;
  -webkit-font-smoothing:antialiased; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px))}
h1,h2,h3,h4{font-family:var(--font-head); color:var(--text-primary); font-weight:500; margin:0; text-wrap:balance}
a{color:var(--accent-deep)}
:focus-visible{outline:2px solid var(--accent); outline-offset:2px; border-radius:4px}
button,input{font-family:inherit; font-size:inherit; color:inherit}
.accent{color:var(--accent)}
.accent-tab{width:48px; height:3px; background:var(--accent); border-radius:2px}
.shell{max-width:1400px; margin:0 auto; padding-block:36px 96px; display:flex; flex-direction:column; gap:26px}
.masthead{display:flex; flex-direction:column; gap:14px}
.eyebrow{font-family:var(--font-head); font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:var(--accent); font-weight:600}
h1.title{font-size:clamp(24px,3vw,34px); letter-spacing:-.01em}
.lede{margin:0; max-width:80ch; color:var(--text-body)}
.draft{background:var(--draft-bg); color:var(--draft-text); border-radius:10px; padding:10px 14px; font-weight:600; font-size:13.5px}
.stat-strip{display:grid; grid-template-columns:repeat(auto-fit,minmax(130px,1fr)); gap:10px}
.stat-tile{background:var(--bg-alt); border-radius:10px; padding:14px; display:flex; flex-direction:column; gap:4px; min-width:0}
.stat-num{font-family:var(--font-head); font-weight:500; font-size:24px; color:var(--accent); font-variant-numeric:tabular-nums; overflow-wrap:anywhere}
.stat-label{font-size:11px; letter-spacing:.06em; text-transform:uppercase; color:var(--text-caption)}
.flow-wrap{display:flex; flex-direction:column; gap:8px}
.flow-head{display:flex; align-items:baseline; justify-content:space-between; gap:10px; flex-wrap:wrap}
.flow-strip{display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:6px}
.flow-step{appearance:none; border:none; text-align:left; cursor:pointer; background:var(--bg-alt); border-radius:10px; padding:12px 14px;
  display:flex; flex-direction:column; gap:4px; position:relative; min-width:0}
.flow-step:hover{background:var(--bg-alt2)}
.flow-step[aria-pressed="true"]{background:var(--accent-tint)}
.flow-step[aria-pressed="true"] .flow-name{color:var(--accent-deep)}
.flow-strip.filtered .flow-step[aria-pressed="false"]{opacity:.55}
.flow-top{display:flex; align-items:center; justify-content:space-between; gap:6px}
.num-badge{font-family:var(--font-mono); font-size:11px; color:var(--accent-deep); border:1.5px solid var(--accent); border-radius:6px; min-width:22px; height:22px;
  padding:0 4px; display:flex; align-items:center; justify-content:center; flex:none}
.flow-count{font-family:var(--font-mono); font-size:11.5px; color:var(--text-caption)}
.flow-name{font-family:var(--font-head); font-weight:600; font-size:13.5px; color:var(--text-primary)}
.flow-arrow{position:absolute; right:-9px; top:50%; transform:translateY(-50%); width:12px; height:12px; z-index:1; color:var(--accent)}
.flow-strip .flow-step:last-child .flow-arrow{display:none}
.hint{font-size:12px; color:var(--text-caption)}
.tabbar{display:flex; gap:6px; background:var(--bg-alt); padding:4px; border-radius:10px; width:fit-content; max-width:100%; flex-wrap:wrap}
.tab-btn{appearance:none; border:none; background:transparent; padding:9px 18px; border-radius:7px; font-family:var(--font-head); font-weight:600; font-size:13px;
  color:var(--text-body); cursor:pointer}
.tab-btn[aria-selected="true"]{background:var(--bg); color:var(--text-primary); box-shadow:0 1px 3px rgba(10,10,10,.08)}
.tab-panel{display:none}
.tab-panel.active{display:block}
.layout{display:grid; grid-template-columns:270px minmax(0,1fr); gap:28px; align-items:start}
@media (max-width:860px){.layout{grid-template-columns:minmax(0,1fr)}}
.rail{background:var(--bg-alt); border-radius:14px; padding:20px; display:flex; flex-direction:column; gap:22px; position:sticky;
  top:calc(20px + env(safe-area-inset-top, 0px)); max-height:calc(100vh - 40px); overflow-y:auto}
@media (max-width:860px){.rail{position:static; max-height:none}}
.rail-block{display:flex; flex-direction:column; gap:10px}
.rail-title{font-family:var(--font-head); font-weight:600; font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:var(--text-primary)}
.search{width:100%; border:none; border-radius:8px; padding:10px 12px; background:var(--bg); color:var(--text-primary)}
.search::placeholder{color:var(--text-caption)}
.chip-row{display:flex; flex-wrap:wrap; gap:6px}
.chip{appearance:none; border:none; background:var(--bg); color:var(--text-body); padding:7px 11px; border-radius:8px; font-size:12.5px; font-weight:500;
  cursor:pointer; text-align:left; display:flex; align-items:center; gap:7px}
.chip .sq{width:9px; height:9px; border-radius:2px; background:var(--text-caption); flex:none}
.chip[aria-pressed="true"]{background:var(--accent-tint); color:var(--accent-deep); font-weight:600}
.chip[aria-pressed="true"] .sq{background:var(--accent)}
.toggle-list{display:flex; flex-direction:column; gap:6px}
.progress-bar{background:var(--bg); border-radius:999px; height:8px; overflow:hidden}
.progress-fill{height:100%; width:0; background:var(--accent); border-radius:999px}
.text-btn{appearance:none; border:none; background:none; font-size:12.5px; font-weight:600; color:var(--accent-deep); cursor:pointer; padding:6px 2px; text-align:left}
.text-btn:hover{color:var(--accent)}
.results-head{display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:16px}
.results-count{font-size:13.5px}
.results-count b{color:var(--text-primary); font-weight:600}
.empty{background:var(--bg-alt); border-radius:12px; padding:36px 20px; text-align:center; font-size:14px}
details.uc-block{margin-bottom:14px; border-radius:14px; background:var(--bg-alt); overflow:hidden}
details.uc-block > summary{list-style:none; cursor:pointer; padding:16px 18px; display:flex; align-items:center; justify-content:space-between; gap:12px}
details.uc-block > summary::-webkit-details-marker{display:none}
.uc-title-wrap{display:flex; align-items:flex-start; gap:12px; min-width:0}
.uc-text{display:flex; flex-direction:column; gap:3px; min-width:0}
h2.uc-title{font-size:18px; font-weight:600}
.uc-flow{font-size:12.5px; color:var(--text-caption)}
.uc-meta{font-size:12px; color:var(--text-caption); font-family:var(--font-mono); white-space:nowrap}
.chev{width:9px; height:9px; border-right:2px solid var(--text-caption); border-bottom:2px solid var(--text-caption); transform:rotate(-45deg); transition:transform .15s; flex:none}
details[open] > summary .chev{transform:rotate(45deg)}
.uc-body{padding:0 14px 14px; display:flex; flex-direction:column; gap:8px}
details.step{background:var(--bg); border-radius:10px; overflow:hidden; scroll-margin-top:20px}
details.step > summary{list-style:none; cursor:pointer; padding:12px 14px; display:flex; align-items:center; gap:12px}
details.step > summary::-webkit-details-marker{display:none}
.step-main{display:flex; flex-direction:column; gap:2px; min-width:0; flex:1}
.step-name{font-weight:600; color:var(--text-primary); font-size:14.5px}
.step-short{font-size:13px; color:var(--text-caption)}
.done-pill{font-size:11px; font-weight:600; padding:3px 9px; border-radius:999px; background:var(--accent-tint); color:var(--accent-deep); white-space:nowrap}
.step-body{display:grid; grid-template-columns:minmax(0,1.55fr) minmax(0,1fr); gap:18px; padding:0 14px 16px; align-items:start}
@media (max-width:760px){.step-body{grid-template-columns:minmax(0,1fr)}}
.shot{margin:0}
.shot img{width:100%; height:auto; border-radius:8px; box-shadow:inset 0 0 0 1px var(--bg-alt2); background:var(--bg-alt); display:block}
.words{display:flex; flex-direction:column; gap:12px; min-width:0}
.words p{margin:0; font-size:14px}
.label{font-family:var(--font-head); font-weight:600; font-size:10.5px; letter-spacing:.08em; text-transform:uppercase; color:var(--text-caption); margin-bottom:3px}
.say{background:var(--say-bg); border-radius:8px; padding:10px 12px}
.say p{color:var(--text-primary)}
.say.recall p{filter:blur(5px); user-select:none; cursor:pointer}
.watch{background:var(--watch-bg); border-radius:8px; padding:10px 12px}
.watch p{color:var(--watch-text)}
.check-line{display:flex; align-items:center; gap:8px; font-size:13px}
.check-line input{accent-color:var(--accent); width:16px; height:16px}
.panel{background:var(--bg-alt); border-radius:14px; padding:22px; display:flex; flex-direction:column; gap:12px; max-width:90ch}
.panel h2{font-size:18px; font-weight:600}
.panel ol,.panel ul{margin:0; padding-left:20px; display:flex; flex-direction:column; gap:6px}
.panel p{margin:0}
footer.brand{display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap; padding-top:12px; border-top:1px solid var(--bg-alt2)}
footer.brand img{width:112px; height:auto; display:block}
.footer-meta{font-size:12px; color:var(--text-caption); max-width:90ch}
body.hide-say .say, body.hide-say .land, body.hide-say .ask, body.hide-watch .watch{display:none}
/* SC teaching blocks */
.teach{display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:12px; padding:0 14px 16px}
.box{border-radius:8px; padding:10px 12px; min-width:0}
.box p{margin:0; font-size:14px}
.box p + p{margin-top:6px}
.open{background:var(--bg-alt)}
.said{background:var(--said-bg)}
.said blockquote{margin:0; color:var(--said-text); font-size:14px}
.said blockquote + blockquote{margin-top:8px}
.said .who{display:block; font-size:12px; color:var(--text-caption); font-style:normal; margin-top:2px}
.said .none{color:var(--text-caption); font-size:13.5px}
.land{background:var(--land-bg)}
.land p{color:var(--land-text)}
.land .d{font-family:var(--font-mono); font-size:11px; border:1.5px solid var(--land-text); border-radius:5px; padding:0 4px; margin-right:4px}
.ask{background:var(--bg-alt)}
.ask dt{font-weight:600; color:var(--text-primary); font-size:14px}
.ask dd{margin:2px 0 8px; font-size:14px}
.ask .src{font-size:11.5px; color:var(--text-caption)}
.who-in{font-size:13px}
.chip-label{font-size:11px; font-weight:600; padding:2px 8px; border-radius:999px; white-space:nowrap; margin-left:8px; vertical-align:2px}
.chip-label.theirs{background:var(--said-bg); color:var(--said-text)}
.chip-label.ours{background:#F1ECFA; color:#4B2C86; box-shadow:inset 0 0 0 1px #B9A6DE}
.opener{background:#F1ECFA}
.opener p{color:#2E1A55; font-weight:600}
.why{background:#F6F3FC}
.why .notours{font-size:12.5px; color:#4B2C86; font-weight:600}
.why .src{font-size:11.5px; color:var(--text-caption)}
ol.clicks{margin:0; padding-left:20px; display:flex; flex-direction:column; gap:4px; font-size:14px}
ol.clicks b, .box b{color:var(--text-primary)}
table.typed, table.logins{border-collapse:collapse; font-size:13.5px; margin-top:4px}
table.typed td, table.logins td, table.logins th{padding:4px 10px 4px 0; text-align:left; vertical-align:top}
table.logins th{font-family:var(--font-head); font-size:10.5px; letter-spacing:.08em; text-transform:uppercase; color:var(--text-caption); font-weight:600}
.pw{font-family:var(--font-mono); white-space:nowrap}
.recallable.recall > :not(.label){filter:blur(5px); user-select:none}
.recallable.recall{cursor:pointer; position:relative}
.ask.recallable.recall > dl{filter:none; user-select:auto}
.ask.recallable.recall dd{filter:blur(5px); user-select:none}
.recallable.recall::after{content:"Recall it, then click to check"; position:absolute; right:10px; top:8px; font-size:11px; color:var(--accent-deep); font-weight:600}
.uc-intro{background:var(--bg); border-radius:10px; padding:14px; display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:12px}
.uc-intro p{margin:0; font-size:14px}
.bridge{background:var(--accent-tint); border-radius:10px; padding:10px 14px}
.bridge p{margin:0; color:var(--text-primary); font-size:14px}
@media (max-width:520px){.flow-arrow{display:none} .stat-num{font-size:21px}}
@media (prefers-reduced-motion: reduce){*{transition:none !important}}
</style>
"""

ARROW = ('<svg class="flow-arrow" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 1l5 5-5 5" fill="none" '
         'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')

SCRIPT = """
<script>
(function () {
  var store = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
                set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  var ns = 'clickpath:' + document.title + ':';
  var steps = Array.prototype.slice.call(document.querySelectorAll('details.step'));
  var blocks = Array.prototype.slice.call(document.querySelectorAll('details.uc-block'));
  var flowBtns = Array.prototype.slice.call(document.querySelectorAll('.flow-step'));
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip[data-uc]'));
  var search = document.getElementById('search');
  var onlyTodo = document.getElementById('onlyTodo');
  var active = {};
  function selected() { return Object.keys(active).filter(function (k) { return active[k]; }); }
  function apply() {
    var q = (search && search.value || '').trim().toLowerCase();
    var ucs = selected(), shown = 0;
    steps.forEach(function (s) {
      var ok = (!ucs.length || ucs.indexOf(s.dataset.uc) >= 0) && (!q || s.dataset.text.indexOf(q) >= 0);
      if (ok && onlyTodo && onlyTodo.checked) { var b = s.querySelector('input[data-key]'); ok = !(b && b.checked); }
      s.hidden = !ok; if (ok) shown++;
    });
    blocks.forEach(function (b) {
      var any = b.querySelectorAll('details.step:not([hidden])').length > 0;
      b.hidden = !any; if (q && any) b.open = true;
    });
    flowBtns.concat(chips).forEach(function (el) { el.setAttribute('aria-pressed', active[el.dataset.uc] ? 'true' : 'false'); });
    var strip = document.querySelector('.flow-strip'); if (strip) strip.classList.toggle('filtered', ucs.length > 0);
    var rc = document.getElementById('resultsCount');
    if (rc) rc.innerHTML = '<b>' + shown + '</b> of ' + steps.length + ' steps' + (ucs.length ? ' in ' + ucs.length + ' use case' + (ucs.length > 1 ? 's' : '') : '');
    var empty = document.getElementById('emptyState'); if (empty) empty.hidden = shown > 0;
  }
  function toggleUc(uc) { active[uc] = !active[uc]; apply(); }
  flowBtns.forEach(function (b) { b.addEventListener('click', function () { toggleUc(b.dataset.uc);
    if (active[b.dataset.uc]) { var blk = document.getElementById('uc-' + b.dataset.uc); if (blk) { blk.open = true; blk.scrollIntoView({behavior: 'smooth', block: 'start'}); } } }); });
  chips.forEach(function (c) { c.addEventListener('click', function () { toggleUc(c.dataset.uc); }); });
  if (search) search.addEventListener('input', apply);
  var reset = document.getElementById('resetFilters');
  if (reset) reset.addEventListener('click', function () { active = {}; if (search) search.value = ''; if (onlyTodo) onlyTodo.checked = false; apply(); });
  document.getElementById('expandAll').addEventListener('click', function () { blocks.concat(steps).forEach(function (d) { d.open = true; }); });
  document.getElementById('collapseAll').addEventListener('click', function () { steps.forEach(function (d) { d.open = false; }); });
  document.querySelectorAll('.tab-btn').forEach(function (t) { t.addEventListener('click', function () {
    document.querySelectorAll('.tab-btn').forEach(function (x) { x.setAttribute('aria-selected', x === t ? 'true' : 'false'); });
    document.querySelectorAll('.tab-panel').forEach(function (p) { p.classList.toggle('active', p.id === t.getAttribute('aria-controls')); });
  }); });
  // SC only: talk track, watch-outs, practice mode, rehearsal ticks
  function bindToggle(id, cls) { var el = document.getElementById(id); if (!el) return;
    el.addEventListener('change', function () { document.body.classList.toggle(cls, !el.checked); }); }
  bindToggle('showSay', 'hide-say'); bindToggle('showWatch', 'hide-watch');
  var practice = document.getElementById('practice');
  if (practice) practice.addEventListener('change', function () {
    document.querySelectorAll('.recallable').forEach(function (s) { s.classList.toggle('recall', practice.checked); }); });
  document.querySelectorAll('.recallable').forEach(function (s) { s.addEventListener('click', function () { s.classList.remove('recall'); }); });
  document.querySelectorAll('.pw-toggle').forEach(function (b) { b.addEventListener('click', function () {
    var pw = document.getElementById(b.getAttribute('aria-controls')); if (!pw) return;
    var show = b.getAttribute('aria-pressed') !== 'true';
    pw.textContent = show ? pw.dataset.pw : '••••••••'; b.setAttribute('aria-pressed', show ? 'true' : 'false');
    b.textContent = show ? 'Hide' : 'Show'; }); });
  var boxes = Array.prototype.slice.call(document.querySelectorAll('input[data-key]'));
  function progress() { var n = boxes.filter(function (b) { return b.checked; }).length;
    var t = document.getElementById('progressText'); if (t) t.textContent = n + ' of ' + boxes.length + ' rehearsed';
    var f = document.getElementById('progressFill'); if (f) f.style.width = (boxes.length ? 100 * n / boxes.length : 0) + '%';
    var s = document.getElementById('statRehearsed'); if (s) s.textContent = n + '/' + boxes.length;
    boxes.forEach(function (b) { var p = b.closest('details.step').querySelector('.done-pill'); if (p) p.hidden = !b.checked; }); }
  boxes.forEach(function (b) { b.checked = store.get(ns + b.dataset.key) === '1';
    b.addEventListener('change', function () { store.set(ns + b.dataset.key, b.checked ? '1' : '0'); progress(); apply(); }); });
  var clear = document.getElementById('clearTicks');
  if (clear) clear.addEventListener('click', function () { boxes.forEach(function (b) { b.checked = false; store.set(ns + b.dataset.key, '0'); }); progress(); apply(); });
  if (onlyTodo) onlyTodo.addEventListener('change', apply);
  progress(); apply();
})();
</script>"""


def page(title, body, fragment):
    head = ('<title>%s</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n%s\n%s'
            % (esc(title), FONTS, STYLE))
    if fragment:
        return head + "\n" + body + SCRIPT
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            + head + "\n</head>\n<body>\n" + body + SCRIPT + "\n</body>\n</html>\n")


def clean_heading(h):
    return re.sub(r"^(UC\d+\s*[—–-]\s*|\d+\.\s*)", "", h or "")


def shell(eyebrow, title_html, lede, stats, draft, flow, tabs, panels, footer):
    stat_html = "".join('<div class="stat-tile"><span class="stat-num"%s>%s</span><span class="stat-label">%s</span></div>'
                        % ((' id="%s"' % i) if i else "", esc(n), esc(l)) for n, l, i in stats)
    tab_html = "".join('<button class="tab-btn" role="tab" id="tab-%s" aria-selected="%s" aria-controls="panel-%s">%s</button>'
                       % (k, "true" if i == 0 else "false", k, esc(label)) for i, (k, label) in enumerate(tabs))
    panel_html = "".join('<section class="tab-panel%s" id="panel-%s" role="tabpanel" aria-labelledby="tab-%s">%s</section>'
                         % (" active" if i == 0 else "", k, k, content) for i, (k, content) in enumerate(panels))
    return ('<div class="shell">%s<header class="masthead"><div class="accent-tab" aria-hidden="true"></div>'
            '<span class="eyebrow">%s</span><h1 class="title">%s</h1>%s<div class="stat-strip">%s</div></header>'
            '<section class="flow-wrap" aria-label="Demo flow"><div class="flow-head"><span class="rail-title">Demo flow</span>'
            '<span class="hint">Click a use case to focus on it</span></div><div class="flow-strip">%s</div></section>'
            '<div class="tabbar" role="tablist" aria-label="Sections">%s</div>%s'
            '<footer class="brand"><span class="footer-meta">%s</span>%s</footer></div>'
            % (draft, esc(eyebrow), title_html, ('<p class="lede">%s</p>' % esc(lede)) if lede else "", stat_html, flow,
               tab_html, panel_html, footer, ('<img alt="Creatio" src="%s">' % LOGO) if LOGO else ""))


def flow_strip(order, headings, counts):
    return "".join('<button type="button" class="flow-step" data-uc="%s" aria-pressed="false"><span class="flow-top">'
                   '<span class="num-badge">%d</span><span class="flow-count">%d step%s</span></span>'
                   '<span class="flow-name">%s</span>%s</button>'
                   % (esc(uc), i, counts[uc], "" if counts[uc] == 1 else "s", esc(headings[uc]), ARROW)
                   for i, uc in enumerate(order, 1))


def rail(order, headings, extra=""):
    chips = "".join('<button type="button" class="chip" data-uc="%s" aria-pressed="false"><span class="sq"></span>%s</button>'
                    % (esc(uc), esc(headings[uc])) for uc in order)
    return ('<aside class="rail" aria-label="Filters"><div class="rail-block"><label class="rail-title" for="search">Search</label>'
            '<input type="text" class="search" id="search" placeholder="Screen, step or words…" autocomplete="off"></div>'
            '<div class="rail-block"><span class="rail-title">Use case</span><div class="chip-row">%s</div></div>%s'
            '<button type="button" class="text-btn" id="resetFilters">Reset filters</button></aside>' % (chips, extra))


def results(blocks_html):
    return ('<main style="min-width:0"><div class="results-head"><div class="results-count" id="resultsCount" aria-live="polite"></div>'
            '<div style="display:flex;gap:14px"><button type="button" class="text-btn" id="expandAll">Expand all</button>'
            '<button type="button" class="text-btn" id="collapseAll">Collapse all</button></div></div>%s'
            '<div class="empty" id="emptyState" hidden>No steps match. Clear the search or the use case filter.</div></main>' % blocks_html)


def uc_block(i, uc, heading, flow_text, steps_html, n, intro="", outro=""):
    return ('<details class="uc-block" id="uc-%s" open><summary><span class="uc-title-wrap"><span class="num-badge">%d</span>'
            '<span class="uc-text"><h2 class="uc-title">%s</h2>%s</span></span><span style="display:flex;align-items:center;gap:12px">'
            '<span class="uc-meta">%d step%s</span><span class="chev"></span></span></summary><div class="uc-body">%s%s%s</div></details>'
            % (esc(uc), i, esc(heading), ('<span class="uc-flow">%s</span>' % esc(flow_text)) if flow_text else "",
               n, "" if n == 1 else "s", intro, steps_html, outro))


def rich(s):
    """Escape, then **UI label** → bold (clicks name the exact labels on screen) and `file or command` → code."""
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", esc(s))
    return re.sub(r"`([^`]+)`", r'<code style="font-family:var(--font-mono);font-size:.92em">\1</code>', s)


def quote_html(q):
    who = q.get("who", "")
    if q.get("partner"):
        who = "Partner said · " + who
    at = (" · " + q["at"]) if q.get("at") else ""
    return '<blockquote>“%s”<span class="who">%s%s</span></blockquote>' % (esc(q.get("quote")), esc(who), esc(at))


def confirmed(quotes, where, report):
    """They said = confirmed customer (or partner) words only. Inferred or assumed lines are dropped and reported."""
    keep = []
    for q in quotes or []:
        if str(q.get("tag", "")).upper() == "C" and q.get("quote") and q.get("who"):
            keep.append(q)
        else:
            report.append("%s: dropped a 'they said' line that isn't confirmed (tag C with who): %s"
                          % (where, (q.get("quote") or "")[:60]))
    return keep


def answers(items, where, report):
    out = []
    for it in items or []:
        a, src = it.get("a"), it.get("source")
        if not (a and src):
            report.append("%s: '%s' has no source in knowledge/ or the approved plan, so the answer is '%s'"
                          % (where, (it.get("q") or "")[:50], CONFIRM))
            a, src = CONFIRM, ""
        out.append('<dt>%s</dt><dd>%s%s</dd>' % (esc(it.get("q")), rich(a), ('<br><span class="src">Source: %s</span>' % esc(src)) if src else ""))
    return out


THEIRS = ("Pain", "Asked", "Asked (must)")
OURS = ("Differentiator", "SC idea", "Our idea")
CANT_RX = re.compile(r"\b(can't|cannot|can not|unable to|doesn't have|don't have|no way to)\b", re.I)


def plan_steps(sc, base):
    """build-plan.json (sc-demo-plan) steps, numbered from 1, when clickpath-sc.json names it as "plan"."""
    p = sc.get("plan")
    if not p:
        return {}
    p = p if os.path.isabs(p) else os.path.normpath(os.path.join(base, p))
    if not os.path.isfile(p):
        return {}
    return {str(i): s for i, s in enumerate(json.load(open(p, encoding="utf-8")).get("steps", []), 1)}


def merge_plan(c, st, plan):
    """Fill a step's label, our_idea, minutes and differentiator from its build-plan step (card runbook_step).
    What the SC wrote in clickpath-sc.json wins."""
    ps = plan.get(str(c.get("runbook_step") or ""), {})
    st = dict(st)
    if ps.get("our_idea") and not st.get("our_idea"):
        st["our_idea"] = ps["our_idea"]
    st.setdefault("label", ps.get("label") or ("Our idea" if st.get("our_idea") else None))
    d = ps.get("differentiator") or {}
    if d:
        ld = dict(st.get("land") or {})
        ld.setdefault("d_id", d.get("id"))
        ld.setdefault("d_line", d.get("line"))
        ld.setdefault("competitor", d.get("competitor"))
        st["land"] = ld
    return st


def label_chip(label):
    if not label:
        return ""
    return '<span class="chip-label %s">%s</span>' % ("ours" if label in OURS else "theirs", esc(label))


def teach_blocks(c, st, cat, report, key):
    """The SC teaching blocks for one step, from the card plus its clickpath-sc.json entry."""
    top, low = [], []
    label = st.get("label")
    if not label:
        report.append("%s: no label (Pain · Asked · Asked (must) · Differentiator · SC idea · Our idea)" % key)
    elif label not in THEIRS + OURS:
        report.append("%s: label '%s' is not one of Pain · Asked · Asked (must) · Differentiator · SC idea · Our idea" % (key, label))
    idea = st.get("our_idea") or {}
    if label == "Our idea":
        if not (idea.get("why") and idea.get("source") and idea.get("ask")):
            report.append("%s: an Our idea step needs our_idea {why, source, ask}" % key)
        if idea.get("ask"):
            top.append('<div class="box opener"><div class="label">Open with this question</div><p>%s</p></div>' % rich(idea["ask"]))
    op = st.get("open") or {}
    if op:
        lines = [("Record", op.get("record")), ("Find it", op.get("find")), ("Before you start", op.get("state"))]
        top.append('<div class="box open"><div class="label">Open</div>%s</div>'
                   % "".join("<p><b>%s:</b> %s</p>" % (esc(k), rich(v)) for k, v in lines if v))
    else:
        report.append("%s: no 'open' (record, how to find it, its state before you start)" % key)
    clicks = st.get("clicks") or ([c["action"]] if c.get("action") else [])
    if clicks:
        typed = "".join("<tr><td>%s</td><td><b>%s</b></td></tr>" % (esc(f), esc(v)) for f, v in st.get("type") or [])
        top.append('<div><div class="label">Click</div><ol class="clicks">%s</ol>%s</div>'
                   % ("".join("<li>%s</li>" % rich(x) for x in clicks),
                      ('<div class="label" style="margin-top:8px">Type</div><table class="typed">%s</table>' % typed) if typed else ""))
    see = st.get("see") or c.get("result")
    if see:
        top.append('<div><div class="label">You will see</div><p>%s</p></div>' % rich(see))
    if st.get("signed_in"):
        top.append('<p class="who-in"><span class="label" style="display:inline">Signed in as</span> %s</p>' % esc(st["signed_in"]))
    if label in OURS and (idea.get("why") or st.get("why_showing")):
        why = idea.get("why") or st.get("why_showing")
        low.append('<div class="box why"><div class="label">Why we\'re showing this</div>'
                   '<p class="notours">Not their words: they didn\'t ask for this. %s (I)</p><p>%s</p>%s</div>'
                   % (esc(label), rich(why), ('<p class="src">Source: %s</p>' % esc(idea["source"])) if idea.get("source") else ""))
    elif label in OURS:
        report.append("%s: a %s step needs 'why we're showing this' (our_idea.why or why_showing)" % (key, label))
    if label == "Our idea":
        if st.get("they_said"):
            report.append("%s: Our idea step: 'they said' left out (they didn't raise it)" % key)
    else:
        quotes = confirmed(st.get("they_said"), key, report)
        if quotes or label not in OURS:
            said = "".join(quote_html(q) for q in quotes) or (
                '<p class="none">%s</p>' % esc(st.get("they_said_none") or "Nothing they said maps to this step."))
            low.append('<div class="box said"><div class="label">They said</div>%s</div>' % said)
    ld = st.get("land") or {}
    if ld:
        d_id = ld.get("d_id")
        if d_id and d_id not in cat:
            report.append("%s: %s is not in the differentiator catalogue" % (key, d_id))
        parts = ['<p><b>%s</b></p>' % rich(ld.get("point"))] if ld.get("point") else []
        if ld.get("why"):
            parts.append("<p><b>Why it matters to them:</b> %s</p>" % rich(ld["why"]))
        if ld.get("kpi"):
            parts.append("<p><b>KPI:</b> %s</p>" % rich(ld["kpi"]))
        if d_id:
            parts.append('<p><span class="d">%s</span>%s%s</p>' % (esc(d_id), esc(cat.get(d_id, "")),
                                                                  (": " + rich(ld["d_line"])) if ld.get("d_line") else ""))
        if ld.get("competitor"):
            if CANT_RX.search(ld["competitor"]):
                report.append("%s: competitor angle says what they can't do; the catalogue says never argue that" % key)
            parts.append("<p><b>Competitor angle:</b> %s</p>" % rich(ld["competitor"]))
        elif d_id:
            report.append("%s: %s has no competitor angle" % (key, d_id))
        low.append('<div class="box land recallable"><div class="label">Land this</div>%s</div>' % "".join(parts))
    else:
        report.append("%s: no 'land this'" % key)
    say = st.get("say") or c.get("say")
    if say:
        low.append('<div class="box say recallable"><div class="label">Say</div><p>%s</p></div>' % rich(say))
    asks = answers(st.get("if_they_ask"), key, report)
    if asks:
        low.append('<div class="box ask recallable"><div class="label">If they ask</div><dl style="margin:0">%s</dl></div>' % "".join(asks))
    watch = st.get("watch") or c.get("attention")
    if watch:
        low.append('<div class="box watch"><div class="label">Watch out</div><p>%s</p></div>' % rich(watch))
    return top, low


def logins_html(sc, creds, fragment, report):
    rows = []
    for i, l in enumerate(sc.get("logins") or []):
        u = l.get("username", "")
        if u in creds:  # demo stands hold no confidential data: shown in plain view (Renzo, 13 Nov 2026)
            pw = '<span class="pw" data-pw="%s"><b>%s</b></span>' % (esc(creds[u]), esc(creds[u]))
        else:
            pw = '<span class="hint">%s</span>' % esc(l.get("password_hint") or "Not in Stand-logins/stand-logins.json yet")
            report.append("login %s: no password found%s" % (u, "" if creds else " (no --credentials given)"))
        rows.append("<tr><td>%s</td><td><b>%s</b>%s</td><td>%s</td><td>%s</td></tr>"
                    % (esc(l.get("role")), esc(u), ('<br><span class="hint">%s</span>' % esc(l["url"])) if l.get("url") else "",
                       pw, esc(l.get("steps", ""))))
    if not rows:
        return ""
    return ('<h2>Logins</h2><table class="logins"><tr><th>Role</th><th>Username</th><th>Password</th><th>Steps</th></tr>%s</table>'
            % "".join(rows))


def meeting_card(sc, base, report):
    """The deal's meeting card (sc-requirements/scripts/meeting_card.py) as a tab, isolated in an iframe so its styles
    don't mix with the click path's. clickpath-sc.json "meeting_card" names the file; otherwise the newest
    meeting-card-*.html in the deal folder (the click path folder's parent) is used."""
    import glob as _glob
    path = sc.get("meeting_card")
    if path:
        path = path if os.path.isabs(path) else os.path.join(base, path)
    else:
        found = sorted(_glob.glob(os.path.join(os.path.dirname(base), "meeting-card-*.html")), key=os.path.getmtime)
        path = found[-1] if found else None
    if not path:
        return None
    if not os.path.exists(path):
        report.append("meeting card %s not found: no 'If they ask what they need' tab" % path)
        return None
    with open(path, encoding="utf-8") as fh:
        doc = fh.read()
    return ('<div class="panel"><iframe title="Meeting card" srcdoc="%s" style="width:100%%;height:80vh;border:0;'
            'border-radius:10px;background:#fff"></iframe></div>' % html.escape(doc, quote=True))


def sc_page(spec, shots, sc=None, creds=None, fragment=False, report=None, base="."):
    sc, creds, report = sc or {}, creds or {}, report if report is not None else []
    cat = catalogue_ids()
    plan = plan_steps(sc, base)
    if sc.get("plan") and not plan:
        report.append("plan %s not found: labels, our ideas and competitor angles not read from it" % sc["plan"])
    labels = []
    cards = spec["cards"]
    sections = spec.get("sections", {})
    steps_sc = sc.get("steps", {})
    ucs_sc = sc.get("use_cases", {})
    order = list(dict.fromkeys(c["uc"] for c in cards))
    headings = {uc: clean_heading(ucs_sc.get(uc, {}).get("heading") or sections.get(uc, {}).get("heading", uc)) for uc in order}
    counts = {uc: sum(1 for c in cards if c["uc"] == uc) for uc in order}
    blocks = []
    for i, uc in enumerate(order, 1):
        rows = []
        for c in [c for c in cards if c["uc"] == uc]:
            key = card_key(c)
            st = steps_sc.get(key, {})
            if sc and not st:
                report.append("%s: no entry in clickpath-sc.json" % key)
            st = merge_plan(c, st, plan) if sc else st
            if st.get("label") in THEIRS and any(l == "Our idea" for _, l in labels):
                report.append("%s: one of their scenes comes after an Our idea step; put our ideas after their own scenes" % key)
            labels.append((key, st.get("label")))
            fig = ""
            if c.get("shot") and os.path.isfile(os.path.join(shots, c["shot"])):
                src, w, h = img_data(os.path.join(shots, c["shot"]))
                fig = '<figure class="shot"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy"></figure>' % (src, w, h, esc(c.get("title")))
            top, low = teach_blocks(c, st, cat, report, key)
            for l in c.get("links") or []:
                url = l.get("url") if isinstance(l, dict) else l
                top.append('<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(url), esc(l.get("label", "Open in Creatio") if isinstance(l, dict) else "Open in Creatio")))
            top.append('<label class="check-line"><input type="checkbox" id="done-%s" data-key="%s"> Rehearsed</label>' % (esc(key), esc(key)))
            text = " ".join([str(c.get(k) or "") for k in ("title", "short", "action", "result", "say", "attention")]
                            + [json.dumps(st, ensure_ascii=False)]).lower()
            mins = (" · %s min" % st["minutes"]) if st.get("minutes") else ""
            rows.append('<details class="step" data-uc="%s" data-text="%s" id="step-%s"><summary><span class="num-badge">%s</span>'
                        '<span class="step-main"><span class="step-name">%s%s</span><span class="step-short">%s%s</span></span>'
                        '<span class="done-pill" hidden>Rehearsed</span><span class="chev"></span></summary>'
                        '<div class="step-body">%s<div class="words">%s</div></div><div class="teach">%s</div></details>'
                        % (esc(uc), esc(text), esc(key), esc(c.get("step")), esc(c.get("title")), label_chip(st.get("label")),
                           esc(c.get("short") or ""), esc(mins), fig, "".join(top), "".join(low)))
        u = ucs_sc.get(uc, {})
        intro = ""
        if sc:
            pains = confirmed(u.get("pain"), uc + " pain", report)
            if not u.get("value_story"):
                report.append("%s: no 30-second value story" % uc)
            uc_labels = [l for k, l in labels if k.startswith(uc + "-")]
            ours_only = bool(uc_labels) and all(l in OURS for l in uc_labels)
            if not pains and not ours_only:
                report.append("%s: no pain in their words" % uc)
            intro = ('<div class="uc-intro"><div class="box land recallable"><div class="label">Value story (30 seconds)</div><p>%s</p></div>'
                     '<div class="box said"><div class="label">The pain, in their words</div>%s</div></div>'
                     % (rich(u.get("value_story", "")), "".join(quote_html(q) for q in pains) or ("<p class=\"none\">They haven't raised this: it's our idea. Open with the question.</p>"
                                                         if ours_only else '<p class="none">Not in their words yet.</p>')))
        outro = ""
        if u.get("bridge"):
            outro = '<div class="bridge"><div class="label">Bridge to what comes next</div><p>%s</p></div>' % rich(u["bridge"])
        elif sc:
            report.append("%s: no bridge line" % uc)
        flow_txt = " → ".join(sections.get(uc, {}).get("flow", []))
        blocks.append(uc_block(i, uc, headings[uc], flow_txt, "".join(rows), counts[uc], intro, outro))
    extra = ('<div class="rail-block"><span class="rail-title">Show</span><div class="toggle-list">'
             '<label class="check-line"><input type="checkbox" id="showSay" checked> Say, land this, if they ask</label>'
             '<label class="check-line"><input type="checkbox" id="showWatch" checked> Watch-outs</label>'
             '<label class="check-line"><input type="checkbox" id="practice"> Practice mode (hide say, land this and if they ask; click to check)</label></div></div>'
             '<div class="rail-block"><span class="rail-title">Rehearsal</span><div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>'
             '<span class="hint" id="progressText"></span><label class="check-line"><input type="checkbox" id="onlyTodo"> Only steps not rehearsed</label>'
             '<button type="button" class="text-btn" id="clearTicks">Clear ticks</button></div>')
    explore = '<div class="layout">%s%s</div>' % (rail(order, headings, extra), results("".join(blocks)))
    before = ("<li><b>Rehearse on the device, network and login you'll present with</b> (phone or tablet app, VPN, SSO), "
              "and have the fallback ready: web view or a recorded clip.</li>")
    before += "".join("<li>%s</li>" % rich(x) for x in spec.get("before_start", []) + sc.get("before_start", []))
    notes = "".join("<li>%s</li>" % rich(x) for x in spec.get("notes", []) + spec.get("issues", []) + sc.get("notes", []))
    faq = answers(sc.get("faq"), "faq", report)
    story = sc.get("story")
    reset = sc.get("reset") or spec.get("reset")
    prep = ('<div class="panel">%s<h2>Before you start</h2><ol>%s</ol>%s%s%s%s%s</div>'
            % (('<h2>The story in one line</h2><p>%s</p>' % rich(story)) if story else "",
               before, logins_html(sc, creds, fragment, report),
               ('<p><b>Reset:</b> %s</p>' % rich(reset)) if reset else "",
               ('<p><b>Login and story:</b> %s</p>' % esc(spec["persona"])) if spec.get("persona") else "",
               ('<h2>Hard questions</h2><div class="box ask"><dl style="margin:0">%s</dl></div>' % "".join(faq)) if faq else "",
               ('<h2>Notes</h2><ul>%s</ul>' % notes) if notes else ""))
    mins = sum(float(s.get("minutes") or 0) for s in steps_sc.values())
    stats = [(len(order), "Use cases", ""), (len(cards), "Steps", ""),
             (sum(1 for c in cards if c.get("shot")), "Screens", "")]
    if mins:
        stats.append(("%g min" % mins, "Demo time", ""))
    if any(l for _, l in labels):
        th = sum(1 for _, l in labels if l in THEIRS)
        ou = sum(1 for _, l in labels if l in OURS)
        stats.append(("%d · %d" % (th, ou), "From them · our ideas", ""))
    stats.append(("0/%d" % len(cards), "Rehearsed", "statRehearsed"))
    title = spec.get("title", "Demo click path")
    tabs, panels = [("path", "Click path"), ("prep", "Before you start")], [("path", explore), ("prep", prep)]
    card = meeting_card(sc, base, report)
    if card:
        tabs.append(("needs", "If they ask what they need"))
        panels.append(("needs", card))
    return shell("Demo practice · SC only", esc(title), sc.get("lede", ""), stats, "", flow_strip(order, headings, counts),
                 tabs, panels,
                 "For the SC only. Stand: %s · version %s. Not for the customer: send the customer recap instead. "
                 "Memorise the beats (record, moment, value line), not a word-for-word script."
                 % (esc(spec.get("instance", "")), esc(spec.get("spec_version", ""))))


def check_customer(text):
    hits = []
    for rx, label in INTERNAL:
        m = rx.search(text)
        if m:
            hits.append("%s ('%s')" % (label, m.group(0)))
    for m in VENDOR_WORDS.finditer(text):
        hits.append("vendor word ('%s')" % m.group(0))
    for rx, label in AI_TELLS:
        if rx.search(text):
            hits.append(label)
    return hits


def customer_page(spec, ov, shots, approved):
    hidden = set(ov.get("hide", []))
    cards = [c for c in spec["cards"] if card_key(c) not in hidden]
    order = list(dict.fromkeys(c["uc"] for c in cards))
    headings = {uc: clean_heading(ov.get("sections", {}).get(uc) or spec.get("sections", {}).get(uc, {}).get("heading", uc)) for uc in order}
    counts = {uc: sum(1 for c in cards if c["uc"] == uc) for uc in order}
    problems = []
    for k in ("title", "intro", "simulated", "contact"):
        for h in check_customer(ov.get(k, "")):
            problems.append("%s: %s" % (k, h))
    for uc in order:
        for h in check_customer(headings[uc]):
            problems.append("section %s heading: %s" % (uc, h))
    blocks = []
    for i, uc in enumerate(order, 1):
        rows = []
        for j, c in enumerate([c for c in cards if c["uc"] == uc], 1):
            key = card_key(c)
            text = ov.get("cards", {}).get(key)
            if not text:
                text = c.get("result", "")
                problems.append("%s: no customer words; using the SC 'result' text" % key)
            title = ov.get("titles", {}).get(key, c.get("title", ""))
            for h in check_customer(title + " " + text):
                problems.append("%s: %s" % (key, h))
            fig = ""
            if c.get("shot") and os.path.isfile(os.path.join(shots, c["shot"])):
                src, w, hgt = img_data(os.path.join(shots, c["shot"]), crop=ov.get("crop", {}).get(key))
                fig = '<figure class="shot"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy"></figure>' % (src, w, hgt, esc(title))
            rows.append('<details class="step" data-uc="%s" data-text="%s"><summary><span class="num-badge">%d</span>'
                        '<span class="step-main"><span class="step-name">%s</span></span><span class="chev"></span></summary>'
                        '<div class="step-body">%s<div class="words"><p>%s</p></div></div></details>'
                        % (esc(uc), esc((title + " " + text).lower()), j, esc(title), fig, esc(text)))
        blocks.append(uc_block(i, uc, headings[uc], "", "".join(rows), counts[uc]))
    explore = '<div class="layout">%s%s</div>' % (rail(order, headings), results("".join(blocks)))
    about = ('<div class="panel"><h2>About this demo</h2><p>%s</p>%s</div>'
             % (esc(ov.get("simulated", "Shown on a Creatio demo site with example data. Connections to your other systems were simulated.")),
                ('<p>%s</p>' % esc(ov["contact"])) if ov.get("contact") else ""))
    draft = "" if approved else '<div class="draft">DRAFT: not yet checked by the solution consultant. Do not send.</div>'
    title = ov.get("title", "%s and Creatio" % ov.get("customer", ""))
    stats = [(len(order), "Use cases", ""), (sum(1 for c in cards if c.get("shot")), "Screens", ""),
             (ov.get("date", "").replace("Demo on ", ""), "Demo", "")]
    body = shell(ov.get("eyebrow", "What you saw"), esc(title), ov.get("intro", ""), stats, draft,
                 flow_strip(order, headings, counts), [("path", "What you saw"), ("about", "About this demo")],
                 [("path", explore), ("about", about)],
                 esc(ov.get("simulated", "Example data on a Creatio demo site.")))
    return body, problems


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "demo"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cards")
    ap.add_argument("--customer")
    ap.add_argument("--shots")
    ap.add_argument("--out")
    ap.add_argument("--slug")
    ap.add_argument("--sc")
    ap.add_argument("--credentials")
    ap.add_argument("--fragment", action="store_true")
    ap.add_argument("--approved", action="store_true")
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.cards))
    spec = json.load(open(a.cards, encoding="utf-8"))
    shots = a.shots or os.path.join(base, "shots")
    out_dir = a.out or base
    ov_path = a.customer or os.path.join(base, "clickpath-customer.json")
    ov = json.load(open(ov_path, encoding="utf-8")) if os.path.isfile(ov_path) else {}
    sc_path = a.sc or os.path.join(base, "clickpath-sc.json")
    sc = json.load(open(sc_path, encoding="utf-8")) if os.path.isfile(sc_path) else {}
    slug = a.slug or slugify(ov.get("customer") or spec.get("artifact_title") or "demo")
    cred_file = a.credentials or team_logins_file()
    # Automatic: a click path that lists no logins gets every login the team file holds for its stand.
    if cred_file and not (sc.get("logins")) and sc is not None:
        auto = stand_logins(cred_file, spec.get("instance"))
        if auto:
            sc["logins"] = auto
            print("Logins: %d taken from the team file for stand %s" % (len(auto), spec.get("instance")))
    usernames = [l.get("username") for l in sc.get("logins") or [] if l.get("username")]
    creds = read_credentials(cred_file, usernames, spec.get("instance")) if cred_file else {}
    if cred_file:
        print("Logins file %s: password found for %d of %d login(s) on stand %s%s" % (
              os.path.basename(cred_file), len(creds), len(usernames), spec.get("instance", "?"),
              ""))
    elif usernames:
        print("No logins file: SharePoint Stand-logins/stand-logins.json not found (or pass --credentials).")

    sc_file = os.path.join(out_dir, "%s-click-path-sc%s.html" % (slug, "-fragment" if a.fragment else ""))
    name = "%s practice" % (ov.get("customer") or spec.get("artifact_title", "Demo"))
    report = []
    sc_html = page(name, sc_page(spec, shots, sc, creds, a.fragment, report, base), a.fragment)
    open(sc_file, "w", encoding="utf-8").write(sc_html)
    print("SC version:", sc_file, "(%d KB)" % (os.path.getsize(sc_file) // 1024))
    if not sc:
        print("No SC overlay (%s): the SC page has the cards only. Write clickpath-sc.json to teach the demo." % sc_path)
    for r in report:
        print("SC GAP", r)

    if not ov:
        print("No customer overlay (%s): customer version not built. Write it first." % ov_path)
        return
    approved = bool(a.approved or ov.get("approved"))
    unreviewed = [card_key(c) for c in spec["cards"] if c.get("shot") and card_key(c) not in set(ov.get("hide", []))
                  and card_key(c) not in set(ov.get("screens_reviewed", []))]
    if approved and unreviewed:
        print("REFUSED: %d screenshot(s) not reviewed yet; it stays a DRAFT." % len(unreviewed))
        approved = False
    body, problems = customer_page(spec, ov, shots, approved)
    if problems and approved:
        print("REFUSED: the customer version still has %d problem(s); it stays a DRAFT." % len(problems))
        approved = False
        body, problems = customer_page(spec, ov, shots, False)
    # Logins and passwords: a hard stop, not a DRAFT note.
    plain = re.sub(r"<[^>]+>", " ", re.sub(r'src="data:[^"]+"', "", body))
    plain = html.unescape(plain)
    leaks = ["login wording ('%s')" % m.group(0) for m in LOGIN_RX.finditer(plain)]
    leaks += ["username '%s'" % u for u in usernames if re.search(r"\b%s\b" % re.escape(u), plain, re.I)]
    leaks += ["a password from the credentials file" for p in creds.values() if p and p in plain]
    if leaks:
        print("STOPPED: the customer page would show a login or password: %s. Customer file not written." % "; ".join(leaks))
        sys.exit(2)
    cu_file = os.path.join(out_dir, "%s-click-path-customer.html" % slug)
    open(cu_file, "w", encoding="utf-8").write(page(ov.get("page_name", "%s demo recap" % ov.get("customer", "Demo")), body, a.fragment))
    print("Customer version:", cu_file, "(%d KB)" % (os.path.getsize(cu_file) // 1024), "APPROVED" if approved else "DRAFT")
    for p in problems:
        print("CHECK", p)
    if unreviewed:
        print("LOOK at %d screenshot(s) before approving (other customers' names, test records, logins, URLs, "
              "placeholders): %s. List them in 'screens_reviewed' once checked." % (len(unreviewed), ", ".join(unreviewed)))


if __name__ == "__main__":
    main()
