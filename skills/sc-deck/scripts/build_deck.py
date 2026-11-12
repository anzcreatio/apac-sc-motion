"""Build a customer deck from a deal's deck.json on a slide template.

Usage:
    python build_deck.py <deck.json> [--out <file.pptx>] [--render]

deck.json format: standards/DECK-STANDARD (repo root). Paths inside deck.json (screenshots, library files) are relative
to the deck.json folder unless absolute. The template is chosen by deck.json "template" (default creatio-2026) and
lives in ../templates/<name>/template.json, so a new corporate template needs a new template.json, not new code.

Slides of type "library" are corporate slides copied (in Python, with their pictures and video) from a .pptx in the
SharePoint Slide-library. --render exports every slide to PNG (render_deck.py: PowerPoint on Windows or Mac).
"""
import argparse
import copy
import json
import math
import re
import os
import subprocess
import sys

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(os.path.dirname(HERE), "templates")
SC_CHECK = "SC check required before this is used with the customer."
WARNINGS = []


# ---------------------------------------------------------------- template and helpers

class Tpl:
    """The active template: frame shapes, content area, colours, font."""

    def load(self, name):
        path = name if os.path.isfile(name) else os.path.join(TEMPLATES, name, "template.json")
        with open(path, encoding="utf-8") as fh:
            cfg = json.load(fh)
        self.dir = os.path.dirname(os.path.abspath(path))
        self.cfg = cfg
        self.base = os.path.join(self.dir, cfg["base"])
        a = cfg["area"]
        self.L, self.T, self.W, self.B = a["left"], a["top"], a["width"], a["bottom"]
        self.R = self.L + self.W
        self.font = cfg.get("font", "Calibri")
        c = {k: RGBColor.from_string(v) for k, v in cfg["colours"].items()}
        self.ACC, self.TINT, self.INK, self.GREY = c["accent"], c["tint"], c["ink"], c["grey"]
        self.RULE, self.WHITE, self.SOFT = c["rule"], c["white"], c["soft"]
        self.BODY = self.GREY if cfg.get("body") == "grey" else self.INK
        self.font_bold = cfg.get("font_bold")  # a heavier face instead of bold, when the template has one
        self.shapes = cfg["shapes"]
        icons = cfg.get("icons")
        self.icons = os.path.join(self.dir, icons) if icons else None
        return self


T = Tpl()


def warn(slide_no, msg):
    WARNINGS.append("slide %s: %s" % (slide_no, msg))


def textbox(slide, name, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return tf


def run(tf, text, size, color=None, bold=False, first=True, align=None, space_before=0):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    if align is not None:
        p.alignment = align
    p.space_before = Pt(space_before)
    r = p.add_run()
    r.text = text
    face = T.font_bold if (bold and T.font_bold) else T.font
    r.font.name, r.font.size, r.font.bold = face, Pt(size), bold and not T.font_bold
    r.font.color.rgb = color if color is not None else T.INK
    return p


def shape(slide, kind, name, x, y, w, h, fill=None, line=None, line_w=1.0):
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    s.name = name
    s.shadow.inherit = False
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(line_w)
    return s


def rule(slide, name, x, y, w):
    shape(slide, MSO_SHAPE.RECTANGLE, name, x, y, w, 0.01, fill=T.RULE)


def est_h(text, size, w, line=1.25):
    """Rough height in inches of wrapped text: good enough to stack blocks and flag overflow."""
    cpl = max(8, int(w * 72 / (size * 0.52)))
    lines = sum(max(1, math.ceil(len(part) / cpl)) for part in str(text).split("\n"))
    return lines * size * line / 72


def set_text(shp, text):
    tf = shp.text_frame
    p = tf.paragraphs[0]
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        p.add_run().text = text
    for extra in tf.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)


def fit_title(shp, title):
    """Big template titles (40 pt) wrap into the content: shrink a 2-line title, and warn on 3+ lines."""
    base = T.cfg.get("title_pt")
    if not base:
        return
    width = T.cfg.get("title_width", T.W)

    def lines_at(pt):
        return max(1, math.ceil(len(title) * pt * 0.5 / 72 / width))

    size = base
    if lines_at(base) > 1:
        size = T.cfg.get("title_pt_2_lines", int(base * 0.75))
        if lines_at(size) > 2:
            size = T.cfg.get("title_pt_3_lines", int(base * 0.62))
            warn(CURRENT["slide"], "title too long for two lines: shorten it (one sentence, about 10 words)")
    for p in shp.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(size)


CURRENT = {"slide": None}


def number(slide, name, x, y, text, size=0.28, fill=None):
    dot = shape(slide, MSO_SHAPE.OVAL, name, x, y, size, size, fill=fill or T.INK)
    tf = dot.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    run(tf, text, 11, T.WHITE, bold=True, align=PP_ALIGN.CENTER)


def chip(slide, name, x, y, shown, labels=("You'll see this today", "Next time")):
    text = labels[0] if shown else labels[1]
    w = 0.25 + len(text) * 0.085
    c = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, name, x, y, w, 0.3, fill=T.ACC if shown else T.SOFT)
    tf = c.text_frame
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    run(tf, text, 10, T.WHITE if shown else T.GREY, bold=True, align=PP_ALIGN.CENTER)
    return w


def icon(slide, name, x, y, size=0.42, slide_no=None):
    """Place a template icon (PNG in the template's icons folder). Returns the width used (0 if none)."""
    if not name or not T.icons:
        return 0
    path = os.path.join(T.icons, name + ".png")
    if not os.path.isfile(path):
        warn(slide_no, "icon '%s' not in the template (%s)" % (name, ", ".join(available_icons())))
        return 0
    pic = slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(size), Inches(size))
    pic.name = "Icon " + name
    return size


def available_icons():
    if not T.icons or not os.path.isdir(T.icons):
        return []
    return sorted(os.path.splitext(f)[0] for f in os.listdir(T.icons) if f.endswith(".png"))


NOTES_BODY = (
    '<p:sp xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
    '<p:nvSpPr><p:cNvPr id="3" name="Notes Placeholder 2"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
    '<p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr><p:spPr/>'
    '<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>'
)


def notes_frame(slide):
    """The speaker-notes text frame; some corporate templates' notes masters have no body, so add one."""
    ns = slide.notes_slide
    if ns.notes_text_frame is None:
        from lxml import etree
        ns.shapes._spTree.append(etree.fromstring(NOTES_BODY))
    return ns.notes_text_frame


def caption(slide, x, y, w, text):
    run(textbox(slide, "Caption", x, y, w, 0.28), text, 10, T.GREY)


def quote(slide, x, y, w, q, size=16):
    words = q["text"].strip("“”\"")
    h = est_h(words, size, w) + 0.45
    tf = textbox(slide, "Quote", x, y, w, h)
    run(tf, "“" + words + "”", size, T.INK, bold=True)
    run(tf, q.get("who", ""), 11, T.GREY, first=False, space_before=5)
    return h


CONFIG = os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json")  # written by the sc-setup skill


def team_root(start=None):
    """The synced SharePoint document library (holds Deals, Slide-library, _inbox, Lessons)."""
    env = os.environ.get("APAC_SC_ROOT")
    if env:
        return env
    if os.path.isfile(CONFIG):
        with open(CONFIG, encoding="utf-8") as fh:
            root = json.load(fh).get("sharepoint_root")
        if root and os.path.isdir(root):
            return root
    p = os.path.realpath(start or os.getcwd())
    while True:
        if os.path.isdir(os.path.join(p, "Slide-library")):
            return p
        parent = os.path.dirname(p)
        if parent == p:
            sys.exit("Can't find the team SharePoint folder: run the sc-setup skill or set APAC_SC_ROOT")
        p = parent


def slide_library(start=None):
    return os.path.join(team_root(start), "Slide-library")


# ---------------------------------------------------------------- frame and deck plumbing

class Deck:
    def __init__(self, spec, deck_dir):
        self.spec, self.dir = spec, deck_dir
        self.meta = spec.get("meta", {})
        self.prs = Presentation(T.base)
        self.source = self.prs.slides[T.cfg.get("frame_slide", 1) - 1]
        self.base_ids = list(self.prs.slides._sldIdLst)
        self.slides = []  # (slide, kind)
        self.lib_parts = []

    def path(self, p):
        if p.startswith("library:"):
            return os.path.join(slide_library(self.dir), p[len("library:"):])
        return p if os.path.isabs(p) else os.path.normpath(os.path.join(self.dir, p))

    def layout(self, name):
        for master in self.prs.slide_masters:
            for lay in master.slide_layouts:
                if lay.name == name:
                    return lay
        return self.source.slide_layout

    def new(self, title=None, sub=None, kind=None):
        lay = self.source.slide_layout
        if kind == "cover" and T.cfg.get("cover_layout"):
            lay = self.layout(T.cfg["cover_layout"])
        elif kind in ("library", "section") and T.cfg.get("plain_layout"):
            lay = self.layout(T.cfg["plain_layout"])
        slide = self.prs.slides.add_slide(lay)
        for ph in list(slide.placeholders):
            ph._element.getparent().remove(ph._element)
        keep = set(T.shapes.values())
        for sh in self.source.shapes:
            if sh.name in keep:
                slide.shapes._spTree.append(copy.deepcopy(sh._element))
        names = {s.name: s for s in slide.shapes}
        if T.shapes.get("title") in names:
            t = names[T.shapes["title"]]
            if title is None:  # section, cover, library: no frame title
                t._element.getparent().remove(t._element)
            else:
                set_text(t, title)
                t.width = Inches(T.cfg.get("title_width", T.W))
                fit_title(t, title)
        sub_shape = names.get(T.shapes.get("subtitle"))
        if sub_shape is not None:
            if sub:
                set_text(sub_shape, sub.upper() if T.cfg.get("subtitle_case") == "upper" else sub)
            else:
                sub_shape._element.getparent().remove(sub_shape._element)
        return slide

    def finish(self, out):
        ids = self.prs.slides._sldIdLst
        by_part = {self.prs.part.related_part(sid.rId): sid for sid in ids}
        ordered = [by_part[s.part] for s, _ in self.slides]
        for sid in self.base_ids:
            self.prs.part.drop_rel(sid.rId)
        for sid in list(ids):
            ids.remove(sid)
        for sid in ordered:
            ids.append(sid)
        page = 0
        for slide, kind in self.slides:
            if kind == "library":  # corporate slides keep their own numbering
                continue
            page += 1
            for sh in slide.shapes:
                if sh.name == T.shapes.get("page"):
                    set_text(sh, str(page))
        last = self.slides[-1][0]
        notes = notes_frame(last)
        if SC_CHECK not in notes.text:
            notes.text = (notes.text + "\n" if notes.text else "") + SC_CHECK
        self.prs.core_properties.title = self.meta.get("title", "Creatio")
        self.prs.save(out)


# ---------------------------------------------------------------- pictures

class Pic:
    """A placed screenshot. Coordinates in deck.json are in the screenshot's frame (its own pixels, or the
    'region' frame when the file holds a region of a larger frame)."""

    def __init__(self, x, y, w, crop):
        self.x, self.y, self.w, self.crop = x, y, w, crop
        self.scale = w / (crop[2] - crop[0])
        self.h = (crop[3] - crop[1]) * self.scale

    @property
    def bottom(self):
        return self.y + self.h

    def to_slide(self, px, py):
        return self.x + (px - self.crop[0]) * self.scale, self.y + (py - self.crop[1]) * self.scale


def picture(deck, slide, sc, x, y, w, max_h=None):
    path = deck.path(sc["file"])
    iw, ih = Image.open(path).size
    region = sc.get("region") or [0, 0, iw, ih]
    crop = sc.get("crop") or region
    geo = Pic(x, y, w, crop)
    if max_h and geo.h > max_h:  # too tall: shrink to fit the height
        w = w * max_h / geo.h
        geo = Pic(x, y, w, crop)
    span_w, span_h = region[2] - region[0], region[3] - region[1]
    pic = slide.shapes.add_picture(path, Inches(x), Inches(y), width=Inches(w), height=Inches(geo.h))
    pic.crop_left, pic.crop_top = (crop[0] - region[0]) / span_w, (crop[1] - region[1]) / span_h
    pic.crop_right, pic.crop_bottom = (region[2] - crop[2]) / span_w, (region[3] - crop[3]) / span_h
    pic.name = "Screen " + os.path.splitext(os.path.basename(path))[0]
    pic._element.nvPicPr.cNvPr.set("descr", sc.get("alt", ""))
    pic.line.color.rgb = T.RULE
    pic.line.width = Pt(0.75)
    return geo


# ---------------------------------------------------------------- writing style check (standards/WRITING-STYLE)

VENDOR_WORDS = re.compile(
    r"(seamless(ly)?|leverag\w*|unlock\w*|empower\w*|robust|streamlin\w*|cutting[- ]edge|transformativ\w*|"
    r"holistic|synerg\w*|elevat\w*|harness\w*|game[- ]chang\w*|world[- ]class|revolutioni[sz]\w*|supercharg\w*|"
    r"delv\w*|ecosystem|paradigm|single source of truth|at scale|next[- ]generation)", re.I)
AI_TELLS = [
    (re.compile("—"), "em dash"),
    (re.compile(r"not (just|only) [^.]{1,60}but", re.I), "'not just X but Y'"),
    (re.compile(r"it'?s not [^.]{1,40}, it'?s", re.I), "'it's not X, it's Y'"),
    (re.compile(r"whether you'?re", re.I), "'whether you're'"),
    (re.compile(r"fast-paced", re.I), "'fast-paced'"),
]
SKIP_KEYS = {"notes", "file", "alt", "icon", "type", "region", "crop", "box", "image", "corner", "layout", "tag",
             "who_key", "fill", "labels", "skip", "slides", "screenshot"}


def visible_text(d, key=None):
    if isinstance(d, str):
        if key not in SKIP_KEYS:
            yield key, d
    elif isinstance(d, dict):
        for k, v in d.items():
            if k not in SKIP_KEYS:
                yield from visible_text(v, k)
    elif isinstance(d, list):
        for v in d:
            yield from visible_text(v, key)


def style_check(d, n):
    if d["type"] == "library":
        return
    title = d.get("title", "")
    if title and d["type"] != "cover":
        if ":" in title:
            warn(n, "style: colon in the title ('%s'): one idea per title" % title[:50])
        if len(title.split()) > 12:
            warn(n, "style: title has %d words; aim for about 8" % len(title.split()))
    for key, text in visible_text(d):
        for m in VENDOR_WORDS.finditer(text):
            warn(n, "style: vendor word '%s' in %s" % (m.group(0), key))
        for rx, label in AI_TELLS:
            if rx.search(text):
                warn(n, "style: %s in %s" % (label, key))
        if ";" in text and key not in ("quote",):
            warn(n, "style: semicolon in %s: split into two sentences" % key)


# ---------------------------------------------------------------- slide types

def s_cover(deck, slide, d, n):
    for sh in list(slide.shapes):
        sh._element.getparent().remove(sh._element)
    fill = RGBColor.from_string(d.get("fill") or T.cfg.get("cover_fill", str(T.INK)))
    shape(slide, MSO_SHAPE.RECTANGLE, "Cover background", 0, 0, 13.34, 7.5, fill=fill)
    if d.get("image"):  # full-bleed photo, cropped to the slide; title sits on accent blocks
        path = deck.path(d["image"])
        iw, ih = Image.open(path).size
        pic = slide.shapes.add_picture(path, 0, 0, Inches(13.333), Inches(7.5))
        target = 13.333 / 7.5
        if iw / ih > target:
            cut = (1 - target * ih / iw) / 2
            pic.crop_left = pic.crop_right = cut
        else:
            cut = (1 - iw / ih / target) / 2
            pic.crop_top = pic.crop_bottom = cut
        pic.name = "Cover image"
    run(textbox(slide, "Brand", 0.75, 0.65, 6, 0.6), d.get("brand", T.cfg.get("brand", "")), 26, T.WHITE, bold=True)
    has_pic = bool(d.get("screenshot"))
    tw = 5.9 if has_pic else 11.5
    if d.get("image"):
        th = est_h(d["title"], 36, 7.5) + 0.3
        box = shape(slide, MSO_SHAPE.RECTANGLE, "Title block", 0.75, 2.45, 7.8, th, fill=T.ACC)
        tf = box.text_frame
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        run(tf, d["title"].upper(), 36, T.WHITE, bold=True, align=PP_ALIGN.LEFT)
        y = 2.45 + th + 0.2
        for key, size in (("subtitle", 18), ("date", 14)):
            if d.get(key):
                b = shape(slide, MSO_SHAPE.RECTANGLE, "Cover " + key, 0.75, y, 0.3 + len(d[key]) * size * 0.0085, 0.45, fill=T.ACC)
                run(b.text_frame, d[key].upper(), size, T.WHITE, bold=True)
                y += 0.6
    else:
        run(textbox(slide, "Title", 0.75, 2.45, tw, 1.9), d["title"], 36, T.WHITE, bold=True)
        if d.get("subtitle"):
            run(textbox(slide, "Subtitle", 0.75, 4.35, tw, 0.6), d["subtitle"], 18, T.WHITE)
        if d.get("date"):
            run(textbox(slide, "Date", 0.75, 5.0, tw, 0.4), d["date"], 16, T.WHITE)
    if has_pic:
        picture(deck, slide, d["screenshot"], 7.0, 2.1, 6.34, max_h=4.6)


def s_understanding(deck, slide, d, n):
    rows = d["rows"]
    if rows and "today" in rows[0]:
        _today_want(deck, slide, d, n)
    else:
        _cards(deck, slide, d, n)
    if d.get("caption"):
        caption(slide, T.L, 6.9, T.W, d["caption"])


def _today_want(deck, slide, d, n):
    rows = d["rows"]
    if not 3 <= len(rows) <= 5:
        warn(n, "understanding has %d rows; the standard is 3-5" % len(rows))
    topic_w, gap_arrow = 2.15, 0.62
    cell_w = (T.W - topic_w - 0.1 - gap_arrow) / 2
    today_x = T.L + topic_w + 0.1
    want_x = today_x + cell_w + gap_arrow
    run(textbox(slide, "Header today", today_x, T.T, cell_w, 0.35), d.get("today_label", "Today"), 14, T.GREY, bold=True)
    run(textbox(slide, "Header want", want_x, T.T, cell_w, 0.35), d.get("want_label", "Where you want to be"), 14, T.ACC, bold=True)
    timing = d.get("timing") or []
    avail = (T.B - 0.35) - (T.T + 0.45) - (1.25 if timing else 0)
    pitch = min(0.98, avail / max(1, len(rows)))
    cell_h = pitch - 0.16
    top = T.T + 0.45
    for i, r in enumerate(rows):
        y = top + i * pitch
        run(textbox(slide, "Topic %d" % (i + 1), T.L, y, topic_w, cell_h, anchor=MSO_ANCHOR.MIDDLE), r["topic"], 15, T.INK, bold=True)
        for label, x, text, fill, size, bold, colour in (
            ("Today", today_x, r["today"], T.SOFT, 13, False, T.GREY),
            ("Want", want_x, r["want"], T.TINT, 14, True, T.INK),
        ):
            box = shape(slide, MSO_SHAPE.RECTANGLE, "%s %d" % (label, i + 1), x, y, cell_w, cell_h, fill=fill)
            tf = box.text_frame
            tf.margin_left = tf.margin_right = Inches(0.16)
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf.word_wrap = True
            run(tf, text, size, colour, bold=bold, align=PP_ALIGN.LEFT)
            if est_h(text, size, cell_w - 0.32) > cell_h:
                warn(n, "'%s' text in row %d may not fit" % (label, i + 1))
        shape(slide, MSO_SHAPE.RIGHT_ARROW, "Arrow %d" % (i + 1), today_x + cell_w + (gap_arrow - 0.28) / 2,
              y + cell_h / 2 - 0.13, 0.28, 0.26, fill=T.ACC)
        shape(slide, MSO_SHAPE.RECTANGLE, "Want bar %d" % (i + 1), want_x, y, 0.06, cell_h, fill=T.ACC)
    if timing:
        line_y = top + len(rows) * pitch + 0.45
        run(textbox(slide, "Topic timing", T.L, line_y - 0.2, topic_w, 0.4), d.get("timing_label", "Timing"), 15, T.INK, bold=True)
        end_x = want_x + cell_w
        marks_x = [today_x + (end_x - today_x) * j / max(1, len(timing)) for j in range(len(timing))]
        shape(slide, MSO_SHAPE.RECTANGLE, "Timeline", today_x, line_y - 0.015, end_x - today_x, 0.03, fill=T.RULE)
        if len(marks_x) > 1:
            shape(slide, MSO_SHAPE.RECTANGLE, "Timeline now", today_x, line_y - 0.02, marks_x[1] - today_x, 0.04, fill=T.ACC)
        mw = (end_x - today_x) / len(timing) - 0.2
        for j, (mx, m) in enumerate(zip(marks_x, timing)):
            colour = T.ACC if j == 0 else T.INK
            shape(slide, MSO_SHAPE.OVAL, "Mark %d" % (j + 1), mx, line_y - 0.11, 0.22, 0.22, fill=colour)
            tf = textbox(slide, "Mark %d text" % (j + 1), mx, line_y + 0.2, mw, 0.7)
            run(tf, m["when"], 13, colour, bold=True)
            run(tf, m["what"], 13, T.INK, first=False, space_before=2)


TAG_LABEL = {"C": "You told us", "P": "We understand", "I": "We understand", "A": "We think"}


def _cards(deck, slide, d, n):
    rows = d["rows"]
    count = len(rows)
    with_icons = any(r.get("icon") for r in rows)
    cols = count if count <= (5 if with_icons else 3) else math.ceil(count / 2)
    gap = 0.4
    w = (T.W - gap * (cols - 1)) / cols
    lines = math.ceil(count / cols)
    footer = d.get("footer")
    avail = T.B - T.T - (0.8 if footer else 0.3)
    h = min(2.4, avail / lines)
    for i, r in enumerate(rows):
        x = T.L + (i % cols) * (w + gap)
        y = T.T + 0.1 + (i // cols) * h
        yy = y + 0.12
        if r.get("icon"):
            yy += icon(slide, r["icon"], x, y + 0.05, 0.5, n) + 0.25
        else:
            rule(slide, "Card rule %d" % i, x, y, w)
        if r.get("tag"):
            run(textbox(slide, "Card %d tag" % (i + 1), x, yy, w, 0.25), TAG_LABEL.get(r["tag"], r["tag"]), 10,
                T.ACC if r["tag"] == "C" else T.GREY, bold=True)
            yy += 0.3
        run(textbox(slide, "Card %d" % (i + 1), x, yy, w, 0.4), r["topic"], 17, T.INK, bold=True)
        # Narrow cards (4-5 in a row) wrap more than the estimate says: allow for it.
        yy += est_h(r["topic"], 17, w) * (1.35 if w < 2.6 else 1.0) + 0.1
        text = r.get("text", "")
        if r.get("tag") == "C" and text and not text.startswith("“"):
            text = "“" + text + "”"
        tf = textbox(slide, "Card %d text" % (i + 1), x, yy, w, h - (yy - y))
        run(tf, text, 14, T.BODY)
        if r.get("note"):
            run(tf, r["note"], 13, T.GREY, first=False, space_before=6)
        if est_h(text + " " + r.get("note", ""), 14, w) + (yy - y) > h:
            warn(n, "card %d may not fit" % (i + 1))
    if footer:
        box = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, "Footer", T.L, T.B - 0.75, T.W, 0.65, fill=T.SOFT)
        box.adjustments[0] = 0.12
        tf = box.text_frame
        tf.margin_left = Inches(0.25)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        run(tf, footer, 16, T.INK, bold=True, align=PP_ALIGN.LEFT)


def s_facts(deck, slide, d, n):
    tf = textbox(slide, "Statement", T.L, T.T + 0.2, 6.1, 4.6)
    run(tf, d["statement"], 24, T.INK, bold=True)
    if d.get("sub"):
        run(tf, d["sub"], 16, T.GREY, first=False, space_before=18)
    x, w = T.L + 6.7, T.W - 6.7
    y = T.T + 0.3
    pitch = min(1.5, (T.B - y - 0.2) / max(1, len(d["facts"])))
    for i, f in enumerate(d["facts"]):
        rule(slide, "Fact rule %d" % i, x, y, w)
        run(textbox(slide, "Fact %d figure" % (i + 1), x, y + 0.12, 2.1, 1.2), f["figure"], 22, T.ACC if f.get("accent") else T.INK, bold=True)
        run(textbox(slide, "Fact %d text" % (i + 1), x + 2.15, y + 0.15, w - 2.15, 1.2), f["text"], 14, T.BODY)
        y += pitch
    rule(slide, "Fact rule end", x, y, w)


def s_why(deck, slide, d, n):
    reasons = d["reasons"]
    y = T.T + 0.2
    height = min(1.3, (T.B - y - 0.1) / max(1, len(reasons)))
    for i, r in enumerate(reasons):
        rule(slide, "Reason rule %d" % i, T.L, y, T.W)
        run(textbox(slide, "Reason %d" % (i + 1), T.L, y + 0.2, 4.1, height - 0.3), r["title"], 18, T.INK, bold=True)
        run(textbox(slide, "Reason %d text" % (i + 1), T.L + 4.3, y + 0.2, T.W - 4.3, height - 0.3), r["text"], 16, T.BODY)
        if est_h(r["text"], 16, T.W - 4.3) > height - 0.25:
            warn(n, "reason %d may not fit" % (i + 1))
        y += height
    rule(slide, "Reason rule end", T.L, y, T.W)


def s_hypothesis(deck, slide, d, n):
    head_h = est_h(d["headline"], 24, T.W) + 0.1
    confirm = d.get("confirm") or []
    parts = d["parts"]
    if len(parts) != 3:
        warn(n, "hypothesis has %d parts; the standard is 3" % len(parts))
    gap = 0.4
    w = (T.W - gap * (len(parts) - 1)) / len(parts)
    part_h = 0.7 + max(est_h(p["text"], 14, w) for p in parts) + (0.4 if any("shown" in p for p in parts) else 0)
    # Without the confirm list (questions live on the next-steps slide), centre headline and parts vertically.
    top = T.T + 0.05 if confirm else T.T + max(0.05, (T.B - T.T - head_h - 0.5 - part_h) / 2)
    run(textbox(slide, "Headline", T.L, top, T.W, head_h), d["headline"], 24, T.INK, bold=True)
    y = top + head_h + (0.5 if not confirm else 0.3)
    if confirm:
        y = max(2.6, y)
    bottom = y
    for i, p in enumerate(parts):
        x = T.L + i * (w + gap)
        rule(slide, "Part rule %d" % i, x, y, w)
        run(textbox(slide, "Part %d" % (i + 1), x, y + 0.12, w, 0.4), p["title"], 17, T.INK, bold=True)
        th = est_h(p["text"], 14, w)
        run(textbox(slide, "Part %d text" % (i + 1), x, y + 0.6, w, th + 0.1), p["text"], 14, T.BODY)
        yy = y + 0.6 + th + 0.15
        if "shown" in p:
            chip(slide, "Part %d status" % (i + 1), x, yy, p["shown"])
            yy += 0.4
        bottom = max(bottom, yy)
    if confirm:
        cy = max(4.5, bottom + 0.2)
        run(textbox(slide, "Confirm label", T.L, cy, T.W, 0.35), d.get("confirm_label", "We'd like to check these with you"), 15, T.INK, bold=True)
        tf = textbox(slide, "Confirm list", T.L, cy + 0.42, T.W, 1.6)
        for j, item in enumerate(confirm[:3]):
            run(tf, "%d.  %s" % (j + 1, item), 15, T.INK, first=j == 0, space_before=0 if j == 0 else 7)
        if cy + 0.42 + 3 * 0.35 > T.B + 0.1:
            warn(n, "confirm list runs past the bottom")


def s_component(deck, slide, d, n):
    """One part of the solution before there are screens: what it does (Business Studio), then where AI helps."""
    y = T.T
    if d.get("lead"):
        lh = est_h(d["lead"], 18, T.W) + 0.1
        run(textbox(slide, "Lead", T.L, y, T.W, lh), d["lead"], 18, T.INK, bold=True)
        y += lh + 0.25
    left_w = T.W * 0.58
    x2 = T.L + left_w + 0.45
    w2 = T.R - x2
    run(textbox(slide, "How label", T.L, y, left_w, 0.35), d.get("how_label", "How it works"), 14, T.GREY, bold=True)
    yy = y + 0.45
    for i, p in enumerate(d.get("points", [])):
        iw = icon(slide, p.get("icon"), T.L, yy + 0.1, 0.4, n)
        tx, tw = (T.L + 0.6, left_w - 0.6) if iw else (T.L, left_w)
        if not iw:
            rule(slide, "Point rule %d" % i, T.L, yy, left_w)
        run(textbox(slide, "Point %d" % (i + 1), tx, yy + 0.1, tw, 0.4), p["title"], 16, T.INK, bold=True)
        th = est_h(p.get("text", ""), 14, tw)
        run(textbox(slide, "Point %d text" % (i + 1), tx, yy + 0.5, tw, th), p.get("text", ""), 14, T.BODY)
        yy += 0.6 + th + 0.1
    if yy > T.B:
        warn(n, "points run past the bottom")
    if d.get("ai"):
        ai = d["ai"]
        items = ai if isinstance(ai, list) else [ai]
        box_h = 0.6 + sum(est_h(t, 14, w2 - 0.4) + 0.15 for t in items)
        box = shape(slide, MSO_SHAPE.RECTANGLE, "AI box", x2, y, w2, box_h, fill=T.TINT)
        shape(slide, MSO_SHAPE.RECTANGLE, "AI bar", x2, y, 0.06, box_h, fill=T.ACC)
        tf = textbox(slide, "AI text", x2 + 0.25, y + 0.15, w2 - 0.4, box_h - 0.3)
        run(tf, d.get("ai_label", "Where AI helps"), 14, T.ACC, bold=True)
        for t in items:
            run(tf, t, 14, T.INK, first=False, space_before=6)
        y2 = y + box_h + 0.25
    else:
        y2 = y
    if "shown" in d:
        cw = chip(slide, "Status", x2, y2, d["shown"])
        if "ai_shown" in d:  # platform today, AI next time is the common case under a half-day config
            chip(slide, "AI status", x2 + cw + 0.15, y2, d["ai_shown"], labels=("AI: today", "AI: next time"))
        y2 += 0.5
    if d.get("quote"):
        y2 += quote(slide, x2, y2 + 0.1, w2, d["quote"], size=15) + 0.1
    if y2 > T.B + 0.05:
        warn(n, "right-hand column (AI box, status, quote) runs past the bottom (%.1f in): shorten the AI lines or the quote" % y2)


def s_screen(deck, slide, d, n):
    """One or two screenshots with numbered highlights, plus a column of blocks (keys, quote, point, figure, table, steps)."""
    screens = d["screens"]
    if d.get("layout") == "row" and len(screens) == 2:
        return _screen_row(deck, slide, d, n)
    icon_blocks = any(isinstance(b, dict) and b.get("icon") for b in d.get("blocks", []))
    pic_w = d.get("width", (7.8 if icon_blocks else 8.6) if len(screens) == 1 else 8.0)
    right = d.get("layout", "picture_left") == "picture_left"
    col_w = T.W - pic_w - 0.4
    pic_x = T.L if right else T.L + col_w + 0.4
    col_x = T.L + pic_w + 0.4 if right else T.L
    y = T.T + 0.05
    takeaway = next((b for b in d.get("blocks", []) if isinstance(b, dict) and "takeaway" in b), None)
    blocks = [b for b in d.get("blocks", []) if b is not takeaway]
    reserve = 0.9 if takeaway else 0.35
    max_h = (T.B - y - reserve - 0.2 * (len(screens) - 1)) / len(screens)
    pics, keys = [], []
    for si, sc in enumerate(screens):
        w = sc.get("width", pic_w)
        geo = picture(deck, slide, sc, pic_x, y, w, max_h=max_h)
        pics.append(geo)
        for hl in sc.get("highlights", []):
            box = hl["box"]
            x1, y1 = geo.to_slide(box[0], box[1])
            x2, y2 = geo.to_slide(box[2], box[3])
            shape(slide, MSO_SHAPE.RECTANGLE, "Highlight %d" % (len(keys) + 1), x1, y1, x2 - x1, y2 - y1, line=T.ACC, line_w=2)
            if hl.get("text"):
                keys.append(hl["text"])
                mx = x2 if hl.get("corner", "tr") == "tr" else x1
                number(slide, "Marker %d" % len(keys), mx - 0.14, y1 - 0.14, str(len(keys)))
        y = geo.bottom + 0.2
    last = pics[-1]
    caption(slide, pic_x, last.bottom + 0.05, pics[-1].w, d.get("caption", deck.meta.get("example_caption", "Example data")))
    cy = T.T + 0.05
    for b in blocks:
        if b == "keys" or (isinstance(b, dict) and "keys" in b):
            for i, text in enumerate(keys):
                number(slide, "Key %d" % (i + 1), col_x, cy + 0.02, str(i + 1))
                h = est_h(text, 15, col_w - 0.38)
                run(textbox(slide, "Key %d text" % (i + 1), col_x + 0.38, cy - 0.04, col_w - 0.38, h + 0.1), text, 15, T.INK)
                cy += max(0.55, h + 0.25)
            cy += 0.15
        elif "quote" in b:
            cy += quote(slide, col_x, cy, col_w, b["quote"], size=15) + 0.2
        elif "point" in b and not b.get("_indent"):
            h = est_h(b["point"], 15, col_w)
            run(textbox(slide, "Point", col_x, cy, col_w, h + 0.1), b["point"], 15, T.BODY)
            cy += h + 0.3
        elif "heading" in b:
            iw = icon(slide, b.get("icon"), col_x, cy - 0.02, 0.38, n)
            hx = col_x + (0.55 if iw else 0)
            hw = col_w - (hx - col_x)
            hh = est_h(b["heading"], 16 if iw else 15, hw)
            run(textbox(slide, "Heading", hx, cy, hw, hh + 0.05), b["heading"], 16 if iw else 15, T.INK, bold=True)
            cy += max(0.45, hh + 0.12)
            if iw:  # the next point lines up with the heading text, not the icon
                b2 = blocks[blocks.index(b) + 1] if blocks.index(b) + 1 < len(blocks) else None
                if isinstance(b2, dict) and "point" in b2:
                    b2["_indent"] = 0.55
        elif "point" in b and b.get("_indent"):
            px, pw = col_x + b["_indent"], col_w - b["_indent"]
            h = est_h(b["point"], 14, pw)
            run(textbox(slide, "Point", px, cy, pw, h + 0.1), b["point"], 14, T.BODY)
            cy += h + 0.35
        elif "figure" in b:
            f = b["figure"]
            run(textbox(slide, "Figure", col_x, cy, col_w, 0.9), f["value"], 48, T.ACC, bold=True)
            h = est_h(f.get("label", ""), 15, col_w)
            run(textbox(slide, "Figure label", col_x, cy + 0.95, col_w, h + 0.1), f.get("label", ""), 15, T.BODY)
            cy += 1.1 + h + 0.25
        elif "steps" in b:
            tf = textbox(slide, "Steps", col_x, cy, col_w, 3.0)
            h = 0
            for i, text in enumerate(b["steps"]):
                run(tf, "%d.  %s" % (i + 1, text), 15, T.INK, first=i == 0, space_before=0 if i == 0 else 9)
                h += est_h(text, 15, col_w) + 0.13
            cy += h + 0.3
        elif "table" in b:
            t = b["table"]
            cols = t["columns"]
            first_w = col_w * 0.42
            other_w = (col_w - first_w) / max(1, len(cols) - 1)
            if t.get("title"):
                run(textbox(slide, "Table label", col_x, cy, col_w, 0.4), t["title"], 15, T.INK, bold=True)
                cy += 0.48
            for ci, label in enumerate(cols[1:]):
                run(textbox(slide, "Column %d" % ci, col_x + first_w + ci * other_w, cy, other_w, 0.3), label, 12, T.GREY, bold=True)
            cy += 0.34
            for ri, row in enumerate(t["rows"]):
                rule(slide, "Table rule %d" % ri, col_x, cy, col_w)
                run(textbox(slide, "Row %d" % (ri + 1), col_x, cy + 0.1, first_w, 0.4), row[0], 15, T.INK)
                for ci, val in enumerate(row[1:]):
                    last_col = ci == len(row) - 2
                    run(textbox(slide, "Cell %d %d" % (ri + 1, ci + 1), col_x + first_w + ci * other_w, cy + 0.1, other_w, 0.4),
                        val, 15, T.INK if last_col else T.GREY, bold=last_col)
                cy += 0.56
            rule(slide, "Table rule end", col_x, cy, col_w)
            cy += 0.35
    if cy > T.B + 0.1:
        warn(n, "right-hand column runs past the bottom (%.1f in)" % cy)
    if takeaway:
        run(textbox(slide, "Takeaway", T.L, last.bottom + 0.5, T.W, 0.5), takeaway["takeaway"], 18, T.INK, bold=True)


def _screen_row(deck, slide, d, n):
    """Two screenshots side by side, each with its heading and point underneath (e.g. before and after a live change)."""
    gap = 0.4
    w = (T.W - gap) / 2
    blocks = [b for b in d.get("blocks", []) if isinstance(b, dict)]
    pairs, cur = [], []
    for b in blocks:  # heading (+ point) per screen
        if "heading" in b and cur:
            pairs.append(cur)
            cur = []
        cur.append(b)
    if cur:
        pairs.append(cur)
    text_h = 1.2
    max_h = T.B - T.T - text_h - 0.35
    bottoms = []
    for i, sc in enumerate(d["screens"]):
        x = T.L + i * (w + gap)
        geo = picture(deck, slide, sc, x, T.T, w, max_h=max_h)
        bottoms.append(geo.bottom)
    y0 = max(bottoms) + 0.1
    caption(slide, T.L, y0, T.W, d.get("caption", deck.meta.get("example_caption", "Example data")))
    for i, group in enumerate(pairs[:2]):
        x = T.L + i * (w + gap)
        y = y0 + 0.35
        for b in group:
            if "heading" in b:
                iw = icon(slide, b.get("icon"), x, y - 0.02, 0.38, n)
                hx = x + (0.55 if iw else 0)
                run(textbox(slide, "Heading %d" % i, hx, y, w - (hx - x), 0.4), b["heading"], 16, T.INK, bold=True)
                y += 0.45
            elif "point" in b:
                h = est_h(b["point"], 14, w - 0.55)
                run(textbox(slide, "Point %d" % i, x + 0.55, y, w - 0.55, h + 0.05), b["point"], 14, T.BODY)
                y += h + 0.15
        if y > T.B + 0.1:
            warn(n, "text under screen %d runs past the bottom" % (i + 1))


def s_summary(deck, slide, d, n):
    parts = d["parts"]
    if len(parts) not in (3, 4, 6):
        warn(n, "summary has %d parts; the standard is 3, 4 or 6" % len(parts))
    labels = d.get("labels", ["In today's demo", "Still to show you"])
    groups = [(labels[0], [p for p in parts if p.get("shown")]), (labels[1], [p for p in parts if not p.get("shown")])]
    groups = [g for g in groups if g[1]]
    gap = 0.4
    w = (T.W - gap * (len(groups) - 1)) / len(groups)
    if d.get("outcome"):
        run(textbox(slide, "Outcome", T.L, T.T - 0.05, T.W, 0.5), d["outcome"], 18, T.INK, bold=True)
        top = T.T + 0.55
    else:
        top = T.T
    most = max(len(g[1]) for g in groups)
    pitch = min(1.5, (T.B - 0.6 - top - 0.5) / most)
    num = 0
    for gi, (heading, rows) in enumerate(groups):
        x = T.L + gi * (w + gap)
        run(textbox(slide, "Heading %d" % gi, x, top, w, 0.4), heading, 15, T.ACC if gi == 0 and rows[0].get("shown") else T.GREY, bold=True)
        y = top + 0.5
        for i, p in enumerate(rows):
            num += 1
            rule(slide, "Group %d rule %d" % (gi, i), x, y, w)
            if d.get("numbered", True):
                number(slide, "Part %d number" % num, x, y + 0.17, str(num), size=0.3, fill=T.ACC if p.get("shown") else T.GREY)
                tx, tw = x + 0.45, w - 0.45
            else:
                tx, tw = x, w
            run(textbox(slide, "Part %d" % num, tx, y + 0.14, tw, 0.4), p["title"], 18, T.INK, bold=True)
            run(textbox(slide, "Part %d text" % num, tx, y + 0.6, tw, pitch - 0.65), p["text"], 15, T.BODY)
            if est_h(p["text"], 15, tw) > pitch - 0.6:
                warn(n, "summary part %d may not fit" % num)
            y += pitch
        rule(slide, "Group %d rule end" % gi, x, y, w)
    caption(slide, T.L, T.B - 0.55, T.W, d.get("caption", "Based on what we know so far."))


def s_roadmap(deck, slide, d, n):
    steps = d["steps"]
    gap = 0.35
    width = (T.W - gap * (len(steps) - 1)) / len(steps)
    line_y = T.T + 0.65
    shape(slide, MSO_SHAPE.RECTANGLE, "Timeline", T.L, line_y, T.W, 0.03, fill=T.INK)
    for i, s in enumerate(steps):
        x = T.L + i * (width + gap)
        dot = 0.24
        shape(slide, MSO_SHAPE.OVAL, "Stage %d" % (i + 1), x, line_y - dot / 2 + 0.015, dot, dot, fill=T.ACC if i == 0 else T.INK)
        run(textbox(slide, "Step %d title" % (i + 1), x, line_y + 0.35, width, 0.95), s["title"], 17, T.INK, bold=True)
        run(textbox(slide, "Step %d what" % (i + 1), x, line_y + 1.35, width, 1.6), s["what"], 14, T.BODY)
        run(textbox(slide, "Step %d when" % (i + 1), x, line_y + 2.97, width, 0.7), s.get("when", ""), 13, T.ACC if i == 0 else T.GREY, bold=True)
    if d.get("timing"):
        rule(slide, "Timing rule", T.L, 5.6, T.W)
        run(textbox(slide, "Timing", T.L, 5.72, T.W, 0.5), d["timing"], 16, T.INK, bold=True)
    caption(slide, T.L, 6.3, T.W, d.get("caption", "Our suggested order, to refine with you."))


def _next_timeline(deck, slide, d, n):
    """Designed next steps: a row of steps on a line, each with an icon, when (accent), what and who."""
    actions = d["actions"]
    gap = 0.3
    w = (T.W - gap * (len(actions) - 1)) / len(actions)
    line_y = T.T + 0.95
    shape(slide, MSO_SHAPE.RECTANGLE, "Timeline", T.L + 0.6, line_y, T.W - 1.2, 0.01, fill=T.RULE)
    for i, a in enumerate(actions):
        x = T.L + i * (w + gap)
        bg = shape(slide, MSO_SHAPE.RECTANGLE, "Icon bg %d" % (i + 1), x, line_y - 0.33, 0.66, 0.66, fill=T.WHITE)
        if not icon(slide, a.get("icon"), x + 0.1, line_y - 0.23, 0.46, n):
            number(slide, "Step %d" % (i + 1), x + 0.17, line_y - 0.16, str(i + 1), size=0.32, fill=T.ACC)
        y = line_y + 0.6
        run(textbox(slide, "When %d" % (i + 1), x, y, w, 0.4), a.get("when", ""), 16, T.ACC, bold=True)
        h = est_h(a["what"], 14, w)
        run(textbox(slide, "What %d" % (i + 1), x, y + 0.5, w, h + 0.1), a["what"], 14, T.INK)
        if a.get("who"):
            run(textbox(slide, "Who %d" % (i + 1), x, y + 0.6 + h + 0.15, w, 0.35), a["who"], 12, T.GREY)
    qs = d.get("questions") or []
    if qs:
        box = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, "Question", T.L, T.B - 1.0, T.W, 0.8, fill=T.SOFT)
        box.adjustments[0] = 0.12
        tf = box.text_frame
        tf.margin_left = Inches(0.3)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.word_wrap = True
        run(tf, qs[0], 17, T.INK, bold=True, align=PP_ALIGN.LEFT)
        if len(qs) > 1:
            warn(n, "timeline layout shows one question; the others belong in the notes")
    if not any(a.get("when") for a in actions):
        warn(n, "no action has a date; the standard asks for a named person and a date")


def s_next_steps(deck, slide, d, n):
    questions = d.get("questions") or []
    actions = d["actions"]
    if d.get("layout") == "timeline" or (T.icons and d.get("layout") != "table"):
        if len(actions) <= 5:
            return _next_timeline(deck, slide, d, n)
    if questions:
        left_w = 5.3
        run(textbox(slide, "Questions title", T.L, T.T, left_w, 0.4), d.get("questions_label", "Questions for you"), 15, T.INK, bold=True)
        tf = textbox(slide, "Questions", T.L, T.T + 0.5, left_w, 4.6)
        for i, text in enumerate(questions):
            run(tf, "%d.  %s" % (i + 1, text), 16, T.INK, first=i == 0, space_before=0 if i == 0 else 14)
        x = T.L + left_w + 0.6
    else:
        x = T.L
    w = T.R - x
    has_when = any(a.get("when") for a in actions)
    when_w = 1.5 if has_when else 0
    who_w = 1.9
    what_w = w - who_w - when_w
    if has_when:
        run(textbox(slide, "When label", x, T.T, when_w, 0.4), "When", 15, T.INK, bold=True)
    run(textbox(slide, "Who label", x + when_w, T.T, who_w, 0.4), "Who", 15, T.INK, bold=True)
    run(textbox(slide, "What label", x + when_w + who_w, T.T, what_w, 0.4), d.get("actions_label", "Next step"), 15, T.INK, bold=True)
    y = T.T + 0.5
    pitch = min(1.08, (T.B - y - 0.1) / max(1, len(actions)))
    for i, a in enumerate(actions):
        rule(slide, "Step rule %d" % i, x, y, w)
        if has_when:
            run(textbox(slide, "When %d" % (i + 1), x, y + 0.14, when_w - 0.1, 0.9), a.get("when", ""), 14, T.ACC, bold=True)
        run(textbox(slide, "Who %d" % (i + 1), x + when_w, y + 0.14, who_w - 0.1, 0.9), a["who"], 14, T.INK, bold=True)
        run(textbox(slide, "What %d" % (i + 1), x + when_w + who_w, y + 0.14, what_w, 0.9), a["what"], 15, T.BODY)
        y += pitch
    rule(slide, "Step rule end", x, y, w)
    if not has_when:
        warn(n, "no action has a date; the standard asks for a named person and a date")


def s_section(deck, slide, d, n):
    run(textbox(slide, "Section", T.L, 2.6, T.W, 1.4, anchor=MSO_ANCHOR.MIDDLE), d["text"], 32, T.INK, bold=True)
    if d.get("sub"):
        run(textbox(slide, "Section sub", T.L, 4.05, T.W, 0.8), d["sub"], 18, T.GREY)


RID_ATTRS = ("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed",
             "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}link",
             "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")


def copy_library(deck, d, n):
    """Copy corporate slides from a library .pptx into the deck, in Python (PowerPoint automation is blocked on
    sensitivity-labelled decks). Pictures, video and media come along; the slide uses the target layout with the
    same name, or the plain layout with a warning."""
    from pptx.opc.package import Part
    from pptx.opc.packuri import PackURI
    path = deck.path(d["file"])
    src = Presentation(path)
    copied = {}
    for num in d["slides"]:
        if not 1 <= num <= len(src.slides):
            warn(n, "%s has no slide %d" % (os.path.basename(path), num))
            continue
        s = src.slides[num - 1]
        lay_name = s.slide_layout.name
        lay = deck.layout(lay_name)
        if lay.name != lay_name:
            lay = deck.layout(T.cfg.get("plain_layout", "Blank"))
            warn(n, "library slide %d uses layout '%s', not in this template: shown on '%s'" % (num, lay_name, lay.name))
        new = deck.prs.slides.add_slide(lay)
        for ph in list(new.placeholders):
            ph._element.getparent().remove(ph._element)
        rid_map = {}
        for rid, rel in s.part.rels.items():
            kind = rel.reltype.split("/")[-1]
            if kind in ("slideLayout", "notesSlide"):
                continue
            if rel.is_external:
                rid_map[rid] = new.part.rels.get_or_add_ext_rel(rel.reltype, rel.target_ref)
                continue
            tp = rel.target_part
            if tp.partname not in copied:
                base, ext = os.path.splitext(str(tp.partname))
                name = PackURI("%s-lib%d%s" % (base, len(deck.lib_parts) + 1, ext))
                copied[tp.partname] = Part(name, tp.content_type, deck.prs.part.package, tp.blob)
                deck.lib_parts.append(name)
            rid_map[rid] = new.part.relate_to(copied[tp.partname], rel.reltype)
        src_csld = s._element.cSld
        bg = src_csld.find("{http://schemas.openxmlformats.org/presentationml/2006/main}bg")
        if bg is not None:
            new._element.cSld.insert(0, copy.deepcopy(bg))
        for el in src_csld.spTree.iterchildren():
            if el.tag.endswith("}nvGrpSpPr") or el.tag.endswith("}grpSpPr"):
                continue
            new.shapes._spTree.append(copy.deepcopy(el))
        for el in new._element.iter():
            for attr in RID_ATTRS:
                v = el.get(attr)
                if v in rid_map:
                    el.set(attr, rid_map[v])
        timing = s._element.find("{http://schemas.openxmlformats.org/presentationml/2006/main}timing")
        if timing is not None:  # video play settings
            new._element.append(copy.deepcopy(timing))
        src_notes = s.notes_slide.notes_text_frame.text if s.has_notes_slide and s.notes_slide.notes_text_frame is not None else ""
        extra = d.get("slide_notes", {}).get(str(num), "")
        if src_notes or extra:
            notes_frame(new).text = chr(10).join(x for x in (extra, src_notes) if x)
        deck.slides.append((new, "library"))


def s_build(deck, slide, d, n):
    """What we've set up for today: the configured elements, Business Studio first, then AI, each with where to see it."""
    groups = [(d.get("platform_label", "Business Studio"), d.get("platform", [])), (d.get("ai_label", "AI"), d.get("ai", []))]
    groups = [g for g in groups if g[1]]
    gap = 0.5
    w = (T.W - gap * (len(groups) - 1)) / len(groups)
    if d.get("lead"):
        lh = est_h(d["lead"], 16, T.W) + 0.1
        run(textbox(slide, "Lead", T.L, T.T - 0.1, T.W, lh), d["lead"], 16, T.BODY)
        top = T.T - 0.1 + lh + 0.2
    else:
        top = T.T
    most = max(len(g[1]) for g in groups)
    pitch = min(1.15, (T.B - top - 0.6) / max(1, most))
    for gi, (label, items) in enumerate(groups):
        x = T.L + gi * (w + gap)
        run(textbox(slide, "Group %d" % gi, x, top, w, 0.35), label, 15, T.ACC if gi == 0 else T.INK, bold=True)
        y = top + 0.5
        for i, it in enumerate(items):
            rule(slide, "Item rule %d %d" % (gi, i), x, y, w)
            iw = icon(slide, it.get("icon"), x, y + 0.14, 0.38, n)
            tx, tw = (x + 0.55, w - 0.55) if iw else (x, w)
            run(textbox(slide, "Item %d %d" % (gi, i), tx, y + 0.12, tw - 1.3, 0.4), it["name"], 16, T.INK, bold=True)
            if it.get("see"):
                run(textbox(slide, "See %d %d" % (gi, i), x + w - 1.3, y + 0.14, 1.3, 0.3), it["see"], 11, T.ACC, bold=True, align=PP_ALIGN.RIGHT)
            th = est_h(it.get("what", ""), 13, tw)
            run(textbox(slide, "Item %d %d what" % (gi, i), tx, y + 0.5, tw, th + 0.05), it.get("what", ""), 13, T.BODY)
            if 0.5 + th > pitch:
                warn(n, "'%s' description may not fit" % it["name"])
            y += pitch
    caption(slide, T.L, T.B + 0.05, T.W, d.get("caption", "Set up on a demo site with example data, in about half a day."))


def platform_spec(deck, d, n):
    """The standard platform section (01 AI Studio, 02 AI Twin, 03 Business Studio, 04 AI Coding Agent) from the
    Slide-library catalogue, so every deck tells the same platform story and picks up new versions automatically."""
    cat_path = os.path.join(slide_library(deck.dir), "catalogue.json")
    with open(cat_path, encoding="utf-8") as fh:
        std = json.load(fh)["standard_sets"][d.get("set", "platform")]
    slides = list(std["slides"])
    for extra in d.get("add", []):  # optional extras, e.g. the AI Studio callouts
        if extra not in slides:
            slides.append(extra)
    slides.sort()
    for drop in d.get("drop", []):
        warn(n, "platform slide %s dropped: the standard is the whole set (say why in the notes)" % drop)
        slides = [x for x in slides if x != drop]
    return {"type": "library", "file": "library:" + std["file"], "slides": slides,
            "slide_notes": dict(std.get("notes", {}), **{str(k): v for k, v in d.get("slide_notes", {}).items()})}


def s_library(deck, slide, d, n):
    pass  # handled by copy_library


TYPES = {
    "cover": s_cover, "understanding": s_understanding, "facts": s_facts, "why": s_why,
    "hypothesis": s_hypothesis, "component": s_component, "screen": s_screen, "summary": s_summary,
    "roadmap": s_roadmap, "next_steps": s_next_steps, "section": s_section, "library": s_library, "build": s_build,
    "platform": s_library,
}
NO_TITLE = {"cover", "library", "section"}


def build(spec_path, out=None, render=False):
    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    T.load(spec.get("template", "creatio-designed-2026"))
    deck_dir = os.path.dirname(os.path.abspath(spec_path))
    deck = Deck(spec, deck_dir)
    for i, d in enumerate(spec["slides"], start=1):
        kind = d["type"]
        if kind not in TYPES:
            sys.exit("slide %d: unknown type %r (known: %s)" % (i, kind, ", ".join(TYPES)))
        if d.get("skip"):
            continue
        if kind == "platform":
            copy_library(deck, platform_spec(deck, d, i), i)
            continue
        if kind == "library":
            copy_library(deck, d, i)
            continue
        CURRENT["slide"] = i
        style_check(d, i)
        slide = deck.new(None if kind in NO_TITLE else d.get("title", ""), d.get("subtitle"), kind)
        TYPES[kind](deck, slide, d, i)
        if d.get("notes"):
            notes_frame(slide).text = d["notes"]
        deck.slides.append((slide, kind))
    kinds = {d["type"] for d in spec["slides"] if not d.get("skip")}
    for core in ("understanding", "platform", "hypothesis", "summary", "next_steps"):
        if core not in kinds and core not in spec.get("meta", {}).get("waive", []):
            warn("deck", "no '%s' slide: the standard deck has one (or list it in meta.waive with a reason)" % core)
    out = out or os.path.join(deck_dir, spec.get("out", "deck.pptx"))
    deck.finish(out)
    lib = sum(1 for _, k in deck.slides if k == "library")
    print("built %s (%d slides%s)" % (out, len(deck.slides), ", %d from the slide library" % lib if lib else ""))
    if render:
        png_dir = os.path.splitext(out)[0] + "-png"
        r = subprocess.run([sys.executable, os.path.join(HERE, "render_deck.py"), out, png_dir])
        print("rendered to", png_dir) if r.returncode == 0 else print("WARNING render skipped (see above); the deck is built")
    for w in WARNINGS:
        print("WARNING", w)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("deck_json")
    ap.add_argument("--out")
    ap.add_argument("--render", action="store_true", help="export every slide to PNG for checking")
    a = ap.parse_args()
    build(a.deck_json, a.out, render=a.render)
