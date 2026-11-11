"""Build the two click-path pages for a demo from the toolkit's click-path cards.

Usage:
    python build_clickpath.py <cards.json> [--customer <clickpath-customer.json>] [--shots <dir>] [--out <dir>]
                              [--fragment] [--approved]

Inputs
  cards.json        the creatio-demo-clickpass cards (title, persona, before_start, reset, sections, cards[...]).
  --customer        overlay with the customer-facing words (default: clickpath-customer.json beside cards.json):
                    {customer, title, date, intro, simulated, sections: {UC1: "heading"},
                     cards: {"UC1-2": "what it means for them"}, hide: ["UC2-4"], approved: false}
  --shots           screenshot folder (default: shots/ beside cards.json)

Outputs (default: the folder of cards.json)
  <slug>-click-path-sc.html        for the SC: clicks, talk track, watch-outs, reset, practice mode, progress
  <slug>-click-path-customer.html  for the customer: screenshots and plain words only. DRAFT banner until approved
                                   (overlay "approved": true or --approved, refused while the safety check finds anything)
Both files are self-contained (screenshots embedded), so they work offline. --fragment writes them without the
<!doctype>/<html>/<head>/<body> wrapper, for publishing as a Claude artifact.
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


STYLE = """
<style>
/* Layout: one reading column of numbered steps, grouped by use case; screenshot first, words beside or below. */
:root {
  --bg: #f7f6f4; --surface: #ffffff; --ink: #1d1b19; --muted: #5f5a54; --line: #e3dfda;
  --accent: #e8400f; --accent-soft: #fdebe4; --warn: #8a5a00; --warn-soft: #fff4dc; --ok: #2f7a4b;
  --font-display: "Montserrat", "Segoe UI", system-ui, sans-serif;
  --font-body: "Inter", "Segoe UI", system-ui, sans-serif;
  --radius: 10px;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #161514; --surface: #201f1d; --ink: #f1eeea; --muted: #b3ada6; --line: #34312e;
  --accent: #ff6a3d; --accent-soft: #3a2219; --warn: #f2c66b; --warn-soft: #33290f; --ok: #7cc79a; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #161514; --surface: #201f1d; --ink: #f1eeea; --muted: #b3ada6; --line: #34312e;
  --accent: #ff6a3d; --accent-soft: #3a2219; --warn: #f2c66b; --warn-soft: #33290f; --ok: #7cc79a; color-scheme: dark }
* { box-sizing: border-box }
body { background: var(--bg); color: var(--ink); font: 15px/1.55 var(--font-body); margin: 0 }
.wrap { max-width: 1040px; margin: 0 auto; padding-block: 28px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)) }
header.top { display: grid; gap: 10px; padding-bottom: 20px; border-bottom: 1px solid var(--line) }
.eyebrow { font: 600 12px/1 var(--font-display); letter-spacing: .08em; text-transform: uppercase; color: var(--accent) }
h1 { font: 600 clamp(26px, 4vw, 36px)/1.15 var(--font-display); margin: 0; text-wrap: balance }
h2 { font: 600 22px/1.25 var(--font-display); margin: 0; text-wrap: balance }
h3 { font: 600 17px/1.3 var(--font-display); margin: 0; text-wrap: balance }
.lede { color: var(--muted); max-width: 68ch; margin: 0 }
.meta { display: flex; flex-wrap: wrap; gap: 8px 16px; color: var(--muted); font-size: 13px }
.banner { background: var(--warn-soft); color: var(--warn); border: 1px solid var(--warn); border-radius: var(--radius);
  padding: 10px 14px; font-weight: 600 }
.panel { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 16px 18px }
.panel h3 { margin-bottom: 8px }
.panel ul, .panel ol { margin: 0; padding-left: 20px; display: grid; gap: 4px }
.tools { display: flex; flex-wrap: wrap; gap: 8px; align-items: center }
button { font: 600 13px/1 var(--font-body); color: var(--ink); background: var(--surface); border: 1px solid var(--line);
  border-radius: 999px; padding: 9px 14px; cursor: pointer }
button[aria-pressed="true"] { background: var(--accent); border-color: var(--accent); color: #fff }
button:focus-visible, a:focus-visible, input:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px }
nav.toc { display: flex; flex-wrap: wrap; gap: 6px }
nav.toc a { color: var(--ink); text-decoration: none; border: 1px solid var(--line); border-radius: 999px; padding: 6px 12px;
  font-size: 13px; background: var(--surface) }
section.uc { display: grid; gap: 16px; padding-top: 36px }
.flow { display: flex; flex-wrap: wrap; gap: 6px; color: var(--muted); font-size: 13px }
.flow span + span::before { content: "→"; margin-right: 6px; color: var(--accent) }
article.step { display: grid; grid-template-columns: minmax(0, 1.55fr) minmax(0, 1fr); gap: 18px; align-items: start;
  background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 16px }
article.step.done { opacity: .62 }
.shot { margin: 0; display: grid; gap: 6px }
.shot img { width: 100%; height: auto; border-radius: 6px; border: 1px solid var(--line); background: var(--bg) }
.shot figcaption { color: var(--muted); font-size: 12px }
.words { display: grid; gap: 10px; min-width: 0 }
.num { font: 600 12px/1 var(--font-display); color: var(--accent); letter-spacing: .06em }
.label { font: 600 11px/1.2 var(--font-display); text-transform: uppercase; letter-spacing: .08em; color: var(--muted); margin-bottom: 2px }
.say { background: var(--accent-soft); border-radius: 8px; padding: 10px 12px }
.say.hidden-say p { filter: blur(5px); user-select: none }
.watch { background: var(--warn-soft); color: var(--warn); border-radius: 8px; padding: 10px 12px; font-size: 14px }
.words p { margin: 0 }
.check { display: flex; gap: 8px; align-items: center; font-size: 13px; color: var(--muted) }
.links a { color: var(--accent) }
footer.end { margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--line); color: var(--muted); font-size: 13px; display: grid; gap: 6px }
@media (max-width: 760px) { article.step { grid-template-columns: minmax(0, 1fr) } }
@media (prefers-reduced-motion: no-preference) { article.step { transition: opacity .2s } }
</style>
"""

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Montserrat:wght@600&display=swap">'


def page(title, body, fragment, script=""):
    head = "<title>%s</title>\n<meta name=\"claude:viewport-fit-sides\" content=\"cover\">\n%s\n%s" % (esc(title), FONTS, STYLE)
    if fragment:
        return head + "\n" + body + script
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            + head + "\n</head>\n<body>\n" + body + script + "\n</body>\n</html>\n")


def sc_page(spec, shots, fragment):
    cards = spec["cards"]
    sections = spec.get("sections", {})
    order = list(dict.fromkeys(c["uc"] for c in cards))
    toc = "".join('<a href="#%s">%s</a>' % (esc(u), esc(sections.get(u, {}).get("heading", u))) for u in order)
    before = "".join("<li>%s</li>" % esc(x) for x in spec.get("before_start", []))
    out = ['<div class="wrap">', '<header class="top">', '<div class="eyebrow">Demo practice · SC only</div>',
           "<h1>%s</h1>" % esc(spec.get("title", "Demo click path")),
           '<p class="lede">%s</p>' % esc(spec.get("persona", "")),
           '<div class="meta"><span>Stand: %s</span><span>%d steps</span><span>Version: %s</span></div>' % (
               esc(spec.get("instance", "")), len(cards), esc(spec.get("spec_version", ""))),
           "</header>", '<div style="display:grid;gap:12px;padding-top:20px">']
    if before or spec.get("reset"):
        out.append('<div class="panel"><h3>Before you start</h3><ol>%s</ol>%s</div>' % (
            before, ('<p style="margin:8px 0 0"><strong>Reset:</strong> %s</p>' % esc(spec["reset"])) if spec.get("reset") else ""))
    out.append('<div class="tools"><button type="button" id="practice" aria-pressed="false">Practice: hide what to say</button>'
               '<button type="button" id="clear">Clear ticks</button><span class="meta" id="progress"></span></div>')
    out.append('<nav class="toc" aria-label="Use cases">%s</nav></div>' % toc)
    for uc in order:
        sec = sections.get(uc, {})
        out.append('<section class="uc" id="%s"><h2>%s</h2>' % (esc(uc), esc(sec.get("heading", uc))))
        if sec.get("flow"):
            out.append('<div class="flow">%s</div>' % "".join("<span>%s</span>" % esc(f) for f in sec["flow"]))
        for c in [c for c in cards if c["uc"] == uc]:
            key = card_key(c)
            fig = ""
            if c.get("shot") and os.path.isfile(os.path.join(shots, c["shot"])):
                src, w, h = img_data(os.path.join(shots, c["shot"]))
                fig = '<figure class="shot"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy"><figcaption>%s</figcaption></figure>' % (
                    src, w, h, esc(c.get("title")), esc(c.get("shot")))
            parts = ['<div class="num">%s · STEP %s</div><h3>%s</h3>' % (esc(uc), esc(c.get("step")), esc(c.get("title")))]
            if c.get("who"):
                parts.append('<div class="meta">Who: %s</div>' % esc(c["who"]))
            if c.get("action"):
                parts.append('<div><div class="label">Click</div><p>%s</p></div>' % esc(c["action"]))
            if c.get("result"):
                parts.append('<div><div class="label">You will see</div><p>%s</p></div>' % esc(c["result"]))
            if c.get("say"):
                parts.append('<div class="say"><div class="label">Say</div><p>%s</p></div>' % esc(c["say"]))
            if c.get("attention"):
                parts.append('<div class="watch"><div class="label">Watch out</div><p>%s</p></div>' % esc(c["attention"]))
            links = c.get("links") or []
            if links:
                parts.append('<div class="links">%s</div>' % " · ".join(
                    '<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(l.get("url", l) if isinstance(l, dict) else l),
                                                                         esc(l.get("label", "Open") if isinstance(l, dict) else "Open")) for l in links))
            parts.append('<label class="check"><input type="checkbox" id="done-%s" data-key="%s"> Rehearsed</label>' % (esc(key), esc(key)))
            out.append('<article class="step" id="step-%s">%s<div class="words">%s</div></article>' % (esc(key), fig, "".join(parts)))
        out.append("</section>")
    notes = "".join("<span>%s</span>" % esc(n) for n in spec.get("notes", []) + spec.get("issues", []))
    out.append('<footer class="end"><span>For the SC only. Not for the customer: use the customer version instead.</span>%s</footer></div>' % notes)
    script = """
<script>
(function () {
  var store = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
                set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  var ns = "clickpath:" + document.title + ":";
  var boxes = Array.prototype.slice.call(document.querySelectorAll('input[type=checkbox][data-key]'));
  function update() {
    var n = 0;
    boxes.forEach(function (b) { var a = b.closest('article'); if (b.checked) { n++; a.classList.add('done'); } else { a.classList.remove('done'); } });
    document.getElementById('progress').textContent = n + ' of ' + boxes.length + ' rehearsed';
  }
  boxes.forEach(function (b) { b.checked = store.get(ns + b.dataset.key) === '1';
    b.addEventListener('change', function () { store.set(ns + b.dataset.key, b.checked ? '1' : '0'); update(); }); });
  document.getElementById('clear').addEventListener('click', function () {
    boxes.forEach(function (b) { b.checked = false; store.set(ns + b.dataset.key, '0'); }); update(); });
  var btn = document.getElementById('practice');
  btn.addEventListener('click', function () {
    var on = btn.getAttribute('aria-pressed') !== 'true';
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    document.querySelectorAll('.say').forEach(function (s) { s.classList.toggle('hidden-say', on); });
  });
  document.querySelectorAll('.say').forEach(function (s) { s.addEventListener('click', function () { s.classList.remove('hidden-say'); }); });
  update();
})();
</script>"""
    return "".join(out), script


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


def customer_page(spec, ov, shots, fragment, approved):
    cards = [c for c in spec["cards"] if card_key(c) not in set(ov.get("hide", []))]
    sec_names = ov.get("sections", {})
    order = list(dict.fromkeys(c["uc"] for c in cards))
    problems = []
    for k in ("title", "intro"):
        for h in check_customer(ov.get(k, "")):
            problems.append("%s: %s" % (k, h))
    out = ['<div class="wrap">']
    if not approved:
        out.append('<div class="banner">DRAFT: not yet checked by the solution consultant. Do not send.</div>')
    out += ['<header class="top" style="padding-top:%s">' % ("16px" if not approved else "0"),
            '<div class="eyebrow">%s</div>' % esc(ov.get("eyebrow", "What you saw")),
            "<h1>%s</h1>" % esc(ov.get("title", "%s and Creatio" % ov.get("customer", ""))),
            '<p class="lede">%s</p>' % esc(ov.get("intro", "")),
            '<div class="meta"><span>%s</span><span>%d screens</span></div>' % (esc(ov.get("date", "")), len(cards)), "</header>"]
    for uc in order:
        heading = sec_names.get(uc) or spec.get("sections", {}).get(uc, {}).get("heading", uc)
        heading = re.sub(r"^(UC\d+\s*[—–-]\s*|\d+\.\s*)", "", heading)
        for h in check_customer(heading):
            problems.append("section %s heading: %s" % (uc, h))
        out.append('<section class="uc" id="%s"><h2>%s</h2>' % (esc(uc), esc(heading)))
        for i, c in enumerate([c for c in cards if c["uc"] == uc], 1):
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
            out.append('<article class="step">%s<div class="words"><div class="num">%d</div><h3>%s</h3><p>%s</p></div></article>' % (
                fig, i, esc(title), esc(text)))
        out.append("</section>")
    out.append('<footer class="end"><span>%s</span><span>%s</span></footer></div>' % (
        esc(ov.get("simulated", "Shown on a Creatio demo site with example data. Connections to your other systems were simulated.")),
        esc(ov.get("contact", ""))))
    return "".join(out), problems


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

    body, script = sc_page(spec, shots, a.fragment)
    sc_file = os.path.join(out_dir, "%s-click-path-sc.html" % slug)
    open(sc_file, "w", encoding="utf-8").write(page("%s practice" % (ov.get("customer") or spec.get("artifact_title", "Demo")), body, a.fragment, script))
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
    body, problems = customer_page(spec, ov, shots, a.fragment, approved)
    if problems and approved:
        print("REFUSED: the customer version still has %d problem(s); it stays a DRAFT." % len(problems))
        approved = False
        body, problems = customer_page(spec, ov, shots, a.fragment, False)
    cu_file = os.path.join(out_dir, "%s-click-path-customer.html" % slug)
    open(cu_file, "w", encoding="utf-8").write(page(ov.get("page_name", "%s demo recap" % ov.get("customer", "Demo")), body, a.fragment))
    print("Customer version:", cu_file, "(%d KB)" % (os.path.getsize(cu_file) // 1024), "APPROVED" if approved else "DRAFT")
    for p in problems:
        print("CHECK", p)
    shown = [card_key(c) for c in spec["cards"] if card_key(c) not in set(ov.get("hide", [])) and c.get("shot")]
    reviewed = set(ov.get("screens_reviewed", []))
    todo = [k for k in shown if k not in reviewed]
    if todo:
        print("LOOK at %d screenshot(s) before approving (other customers' names, test records, logins, URLs, "
              "placeholders): %s. List them in 'screens_reviewed' once checked." % (len(todo), ", ".join(todo)))


if __name__ == "__main__":
    main()
