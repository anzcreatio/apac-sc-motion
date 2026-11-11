"""Build the two click-path pages for a demo from the toolkit's click-path cards.

Usage:
    python build_clickpath.py <cards.json> [--customer <clickpath-customer.json>] [--shots <dir>] [--out <dir>]
                              [--slug <name>] [--fragment] [--approved]

Inputs
  cards.json        the creatio-demo-clickpass cards (title, persona, before_start, reset, sections, cards[...]).
  --customer        overlay with the customer-facing words (default: clickpath-customer.json beside cards.json):
                    {customer, page_name, title, eyebrow, date, intro, simulated, contact, approved,
                     sections: {UC1: "heading"}, titles: {"UC1-2": "..."}, cards: {"UC1-2": "what it means for them"},
                     hide: [...], crop: {"UC1-3": [l, t, r, b] fractions}, screens_reviewed: [...]}
  --shots           screenshot folder (default: shots/ beside cards.json)

Outputs (default: the folder of cards.json)
  <slug>-click-path-sc.html        for the SC: clicks, talk track, watch-outs, before you start, practice mode, ticks
  <slug>-click-path-customer.html  for the customer: screenshots and plain words only. DRAFT banner until approved
                                   ("approved": true or --approved), refused while a check fails or a shown screenshot
                                   is not in screens_reviewed.
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
  --say-bg:#FFF1EC; --watch-bg:#FFF6E0; --watch-text:#7A5300; --draft-bg:#FFF6E0; --draft-text:#7A5300;
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
body.hide-say .say, body.hide-watch .watch{display:none}
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
    document.querySelectorAll('.say').forEach(function (s) { s.classList.toggle('recall', practice.checked); }); });
  document.querySelectorAll('.say').forEach(function (s) { s.addEventListener('click', function () { s.classList.remove('recall'); }); });
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


def uc_block(i, uc, heading, flow_text, steps_html, n):
    return ('<details class="uc-block" id="uc-%s" open><summary><span class="uc-title-wrap"><span class="num-badge">%d</span>'
            '<span class="uc-text"><h2 class="uc-title">%s</h2>%s</span></span><span style="display:flex;align-items:center;gap:12px">'
            '<span class="uc-meta">%d step%s</span><span class="chev"></span></span></summary><div class="uc-body">%s</div></details>'
            % (esc(uc), i, esc(heading), ('<span class="uc-flow">%s</span>' % esc(flow_text)) if flow_text else "",
               n, "" if n == 1 else "s", steps_html))


def sc_page(spec, shots):
    cards = spec["cards"]
    sections = spec.get("sections", {})
    order = list(dict.fromkeys(c["uc"] for c in cards))
    headings = {uc: clean_heading(sections.get(uc, {}).get("heading", uc)) for uc in order}
    counts = {uc: sum(1 for c in cards if c["uc"] == uc) for uc in order}
    blocks = []
    for i, uc in enumerate(order, 1):
        rows = []
        for c in [c for c in cards if c["uc"] == uc]:
            key = card_key(c)
            fig = ""
            if c.get("shot") and os.path.isfile(os.path.join(shots, c["shot"])):
                src, w, h = img_data(os.path.join(shots, c["shot"]))
                fig = '<figure class="shot"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy"></figure>' % (src, w, h, esc(c.get("title")))
            words = []
            if c.get("action"):
                words.append('<div><div class="label">Click</div><p>%s</p></div>' % esc(c["action"]))
            if c.get("result"):
                words.append('<div><div class="label">You will see</div><p>%s</p></div>' % esc(c["result"]))
            if c.get("say"):
                words.append('<div class="say"><div class="label">Say</div><p>%s</p></div>' % esc(c["say"]))
            if c.get("attention"):
                words.append('<div class="watch"><div class="label">Watch out</div><p>%s</p></div>' % esc(c["attention"]))
            for l in c.get("links") or []:
                url = l.get("url") if isinstance(l, dict) else l
                words.append('<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(url), esc(l.get("label", "Open in Creatio") if isinstance(l, dict) else "Open in Creatio")))
            words.append('<label class="check-line"><input type="checkbox" id="done-%s" data-key="%s"> Rehearsed</label>' % (esc(key), esc(key)))
            text = " ".join(str(c.get(k) or "") for k in ("title", "short", "action", "result", "say", "attention")).lower()
            rows.append('<details class="step" data-uc="%s" data-text="%s" id="step-%s"><summary><span class="num-badge">%s</span>'
                        '<span class="step-main"><span class="step-name">%s</span><span class="step-short">%s</span></span>'
                        '<span class="done-pill" hidden>Rehearsed</span><span class="chev"></span></summary>'
                        '<div class="step-body">%s<div class="words">%s</div></div></details>'
                        % (esc(uc), esc(text), esc(key), esc(c.get("step")), esc(c.get("title")),
                           esc(c.get("short") or ""), fig, "".join(words)))
        flow_txt = " → ".join(sections.get(uc, {}).get("flow", []))
        blocks.append(uc_block(i, uc, headings[uc], flow_txt, "".join(rows), counts[uc]))
    extra = ('<div class="rail-block"><span class="rail-title">Show</span><div class="toggle-list">'
             '<label class="check-line"><input type="checkbox" id="showSay" checked> What to say</label>'
             '<label class="check-line"><input type="checkbox" id="showWatch" checked> Watch-outs</label>'
             '<label class="check-line"><input type="checkbox" id="practice"> Practice mode (blur what to say)</label></div></div>'
             '<div class="rail-block"><span class="rail-title">Rehearsal</span><div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>'
             '<span class="hint" id="progressText"></span><label class="check-line"><input type="checkbox" id="onlyTodo"> Only steps not rehearsed</label>'
             '<button type="button" class="text-btn" id="clearTicks">Clear ticks</button></div>')
    explore = '<div class="layout">%s%s</div>' % (rail(order, headings, extra), results("".join(blocks)))
    before = "".join("<li>%s</li>" % esc(x) for x in spec.get("before_start", []))
    notes = "".join("<li>%s</li>" % esc(x) for x in spec.get("notes", []) + spec.get("issues", []))
    prep = ('<div class="panel"><h2>Before you start</h2><ol>%s</ol>%s%s%s</div>'
            % (before or "<li>No checklist in the click path.</li>",
               ('<p><b>Reset:</b> %s</p>' % esc(spec["reset"])) if spec.get("reset") else "",
               ('<p><b>Login and story:</b> %s</p>' % esc(spec["persona"])) if spec.get("persona") else "",
               ('<h2>Notes</h2><ul>%s</ul>' % notes) if notes else ""))
    stats = [(len(order), "Use cases", ""), (len(cards), "Steps", ""),
             (sum(1 for c in cards if c.get("shot")), "Screens", ""), ("0/%d" % len(cards), "Rehearsed", "statRehearsed")]
    title = spec.get("title", "Demo click path")
    return shell("Demo practice · SC only", esc(title), "", stats, "", flow_strip(order, headings, counts),
                 [("path", "Click path"), ("prep", "Before you start")], [("path", explore), ("prep", prep)],
                 "For the SC only. Stand: %s · version %s. Not for the customer: send the customer recap instead."
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
    ap.add_argument("--fragment", action="store_true")
    ap.add_argument("--approved", action="store_true")
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.cards))
    spec = json.load(open(a.cards, encoding="utf-8"))
    shots = a.shots or os.path.join(base, "shots")
    out_dir = a.out or base
    ov_path = a.customer or os.path.join(base, "clickpath-customer.json")
    ov = json.load(open(ov_path, encoding="utf-8")) if os.path.isfile(ov_path) else {}
    slug = a.slug or slugify(ov.get("customer") or spec.get("artifact_title") or "demo")

    sc_file = os.path.join(out_dir, "%s-click-path-sc.html" % slug)
    name = "%s practice" % (ov.get("customer") or spec.get("artifact_title", "Demo"))
    open(sc_file, "w", encoding="utf-8").write(page(name, sc_page(spec, shots), a.fragment))
    print("SC version:", sc_file, "(%d KB)" % (os.path.getsize(sc_file) // 1024))

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
