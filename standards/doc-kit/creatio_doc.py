"""Creatio-branded Word documents for the APAC SC motion (DOC-STANDARD-v0.1).

Every Word document the motion produces uses this kit: customer and partner documents, playbacks, sizing,
proposals, internal briefs. Look taken from creatio.com: Montserrat headings, Arial body, #181818 text, #FF4013
accent, #011D59 navy table headers, #F0F0F0 soft panels, Creatio logo, orange cover band, status line in the footer.

    import sys; sys.path.insert(0, "<plugin>/standards/doc-kit")
    from creatio_doc import CreatioDoc
    doc = CreatioDoc(title="On-premises infrastructure recommendation", label="Agrobank · CRMS Sales Module",
                     subtitle="Servers, storage and software, Year 1 to Year 5",
                     meta=[("Prepared for", "Agrobank"), ("Date", "18 November 2026")],
                     status="Preliminary recommendation, pending review by Creatio's infrastructure team",
                     note="How to read this document. Every figure is per server unless it says otherwise.")
    doc.section("Summary", "What we recommend")
    doc.tiles([("36", "servers in Production"), ("5.4 TB", "documents by Year 5")])
    doc.bullets([("Bold lead. ", "Rest of the sentence."), "Plain bullet"])
    doc.table(["Item", "What we used"], rows, widths=[5, 12], highlight={2})   # highlight = estimates to confirm
    doc.save("out.docx"); doc.export_pdf("out.docx", "out.pdf")              # PDF keeps the fonts

No emoji, no "SC check" lines, writing per WRITING-STYLE-v0.1. Render the PDF and look at every page before sending.
"""
import os
import platform
import shutil
import subprocess

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

KIT = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(KIT, "creatio-logo.png")

INK, ORANGE, NAVY, GREY, SOFT, LINE, ZEBRA, ESTIMATE = "181818", "FF4013", "011D59", "5F6368", "F0F0F0", "D9D9D9", "F7F7F7", "FFE9E2"
HFONT, BFONT = "Montserrat", "Arial"


class CreatioDoc:
    def __init__(self, title, label="", subtitle="", meta=None, status="", note="", footer="", cover=True, landscape=False):
        self.d = Document()
        self.n = 0
        self.status = status
        sec = self.d.sections[0]
        w, h = (Cm(29.7), Cm(21)) if landscape else (Cm(21), Cm(29.7))
        sec.page_width, sec.page_height = w, h
        sec.left_margin = sec.right_margin = Cm(2); sec.top_margin = sec.bottom_margin = Cm(1.8)
        self.width_cm = (29.7 if landscape else 21) - 4
        st = self.d.styles["Normal"]
        st.font.name = BFONT; st.font.size = Pt(10); st.font.color.rgb = RGBColor.from_string(INK)
        st.element.rPr.rFonts.set(qn("w:eastAsia"), BFONT)
        st.paragraph_format.space_after = Pt(6); st.paragraph_format.line_spacing = 1.15
        self._footer(footer or " · ".join(x for x in ("Creatio", title, status) if x))
        if cover:
            self._cover(title, label, subtitle, meta or [], status, note)

    # ------------------------------------------------------------------ low level
    def run(self, p, text, size=None, bold=False, color=INK, font=None, italic=False, spacing=None):
        r = p.add_run(text)
        r.bold, r.italic = bold, italic
        r.font.color.rgb = RGBColor.from_string(color)
        if size:
            r.font.size = Pt(size)
        if font:
            r.font.name = font; r._element.rPr.rFonts.set(qn("w:eastAsia"), font)
        if spacing:
            e = OxmlElement("w:spacing"); e.set(qn("w:val"), str(spacing)); r._element.get_or_add_rPr().append(e)
        return r

    def para(self, text="", size=10, bold=False, color=INK, font=None, after=6, before=0, keep=False, muted=False):
        p = self.d.add_paragraph()
        p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.keep_with_next = keep
        if text:
            self.run(p, text, size, bold, GREY if muted else color, font)
        return p

    @staticmethod
    def _shade(cell, fill):
        tcPr = cell._element.get_or_add_tcPr()
        s = OxmlElement("w:shd"); s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), fill)
        tcPr.append(s)

    @staticmethod
    def _borders(table, color=LINE, size="4", inner_h=True, inner_v=False, outer_v=False):
        b = OxmlElement("w:tblBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            e = OxmlElement(f"w:{edge}")
            off = (edge in ("left", "right") and not outer_v) or (edge == "insideV" and not inner_v) or (edge == "insideH" and not inner_h)
            if off:
                e.set(qn("w:val"), "nil")
            else:
                e.set(qn("w:val"), "single"); e.set(qn("w:sz"), size); e.set(qn("w:color"), color)
            b.append(e)
        table._element.tblPr.append(b)

    @staticmethod
    def _pad(table, top=60, bottom=60, left=100, right=100):
        m = OxmlElement("w:tblCellMar")
        for k, v in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
            e = OxmlElement(f"w:{k}"); e.set(qn("w:w"), str(v)); e.set(qn("w:type"), "dxa"); m.append(e)
        table._element.tblPr.append(m)

    def _footer(self, text):
        fp = self.d.sections[0].footer.paragraphs[0]; fp.paragraph_format.space_after = Pt(0)
        self.run(fp, text + "  ·  Page ", 7, False, GREY)
        r = fp.add_run(); r.font.size = Pt(7); r.font.color.rgb = RGBColor.from_string(GREY)
        for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
            if tag:
                f = OxmlElement("w:fldChar"); f.set(qn("w:fldCharType"), tag); r._element.append(f)
            else:
                it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = txt; r._element.append(it)

    def _cover(self, title, label, subtitle, meta, status, note):
        p = self.para(after=40); p.add_run().add_picture(LOGO, width=Cm(3.6))
        cov = self.d.add_table(rows=1, cols=1); self._borders(cov, ORANGE, inner_h=False); self._pad(cov, 500, 500, 400, 400)
        c = cov.rows[0].cells[0]; self._shade(c, ORANGE); c.width = Cm(self.width_cm)
        p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(10)
        if label:
            self.run(p, label.upper(), 8.5, True, "FFFFFF", HFONT, spacing=60)
            p = c.add_paragraph(); p.paragraph_format.space_after = Pt(10)
        self.run(p, title, 26, True, "FFFFFF", HFONT)
        if subtitle:
            p = c.add_paragraph(); p.paragraph_format.space_after = Pt(0)
            self.run(p, subtitle, 11, False, "FFFFFF")
        self.para(after=18)
        rows = list(meta) + ([("Status", status)] if status else [])
        if rows:
            t = self.d.add_table(rows=len(rows), cols=2); self._pad(t, 40, 40, 0, 100)
            for i, (k, v) in enumerate(rows):
                self.run(t.rows[i].cells[0].paragraphs[0], k.upper(), 8, True, ORANGE, HFONT, spacing=20)
                self.run(t.rows[i].cells[1].paragraphs[0], v, 10, k == "Status", INK)
                t.rows[i].cells[0].width = Cm(3.5); t.rows[i].cells[1].width = Cm(self.width_cm - 3.5)
        self.para(after=60)
        p = self.para(after=0)
        if note:
            head, _, rest = note.partition(". ")
            self.run(p, head + ". ", 9, True, INK)
            self.run(p, rest, 9, False, GREY)
        p.add_run().add_break(WD_BREAK.PAGE)

    # ------------------------------------------------------------------ building blocks
    def section(self, label, title, number=True):
        """Small orange spaced label ("01 · SUMMARY") over a Montserrat title. Kept with what follows."""
        self.n += 1
        p = self.para(after=0, before=10, keep=True)
        self.run(p, (f"{self.n:02d}  ·  " if number else "") + label.upper(), 8, True, ORANGE, HFONT, spacing=40)
        p2 = self.para(after=8, keep=True)
        self.run(p2, title, 17, True, INK, HFONT)

    def sub(self, title):
        return self.para(title, 11, True, INK, HFONT, after=4, keep=True)

    def bullets(self, items, size=10, numbered=False, keep=False):
        for i, it in enumerate(items):
            p = self.d.add_paragraph(style="List Number" if numbered else "List Bullet")
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = keep and i < len(items) - 1
            if isinstance(it, tuple):
                self.run(p, it[0], size, True); self.run(p, it[1], size)
            else:
                self.run(p, str(it), size)

    def table(self, headers, rows, widths=None, highlight=None, size=8.5, first_bold=True, keep_together=None):
        """Navy header, light row lines, zebra rows; rows in `highlight` are shaded orange (estimates to confirm).
        Short tables (14 rows or fewer) are kept on one page; the header repeats on long ones."""
        t = self.d.add_table(rows=1, cols=len(headers)); t.alignment = WD_TABLE_ALIGNMENT.CENTER
        self._borders(t); self._pad(t)
        widths = widths or [self.width_cm / len(headers)] * len(headers)
        for i, h in enumerate(headers):
            c = t.rows[0].cells[i]; self._shade(c, NAVY)
            p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0)
            self.run(p, h, size, True, "FFFFFF", HFONT)
        for ri, rw in enumerate(rows):
            cells = t.add_row().cells
            for i, v in enumerate(rw):
                p = cells[i].paragraphs[0]; p.paragraph_format.space_after = Pt(0)
                lines = ("" if v is None else str(v)).split("\n")
                for li, ln in enumerate(lines):
                    self.run(p, ln, size, first_bold and i == 0, INK)
                    if li < len(lines) - 1:
                        p.add_run().add_break()
                if highlight and ri in highlight:
                    self._shade(cells[i], ESTIMATE)
                elif ri % 2:
                    self._shade(cells[i], ZEBRA)
        together = keep_together if keep_together is not None else len(t.rows) <= 14
        for ri, row in enumerate(t.rows):
            trPr = row._tr.get_or_add_trPr()
            trPr.append(OxmlElement("w:cantSplit"))
            if ri == 0:
                trPr.append(OxmlElement("w:tblHeader"))
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
                if together and ri < len(t.rows) - 1:
                    for pp in row.cells[i].paragraphs:
                        pp.paragraph_format.keep_with_next = True
        self.para(after=2)
        return t

    def tiles(self, items):
        """Key numbers: big orange figure over a short grey caption, on soft grey panels."""
        t = self.d.add_table(rows=1, cols=len(items)); t.alignment = WD_TABLE_ALIGNMENT.CENTER
        self._borders(t, "FFFFFF", "24", inner_h=True, inner_v=True, outer_v=True); self._pad(t, 160, 160, 160, 160)
        for i, (big, small) in enumerate(items):
            c = t.rows[0].cells[i]; self._shade(c, SOFT); c.width = Cm(self.width_cm / len(items))
            p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(2)
            self.run(p, big, 22, True, ORANGE, HFONT)
            p2 = c.add_paragraph(); p2.paragraph_format.space_after = Pt(0)
            self.run(p2, small, 8.5, False, GREY)
        self.para(after=2)

    def callout(self, text, bold_lead=""):
        """Soft grey panel for a key message or a decision the reader must make."""
        t = self.d.add_table(rows=1, cols=1); self._borders(t, ORANGE, "12", inner_h=False); self._pad(t, 140, 140, 200, 200)
        c = t.rows[0].cells[0]; self._shade(c, SOFT); c.width = Cm(self.width_cm)
        p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0)
        if bold_lead:
            self.run(p, bold_lead, 10, True)
        self.run(p, text, 10)
        self.para(after=2)

    def signoff(self, line="Name: ______________________   Role: ______________________   Date: ____________"):
        self.para(line, 10, before=12)

    def save(self, path):
        self.d.save(path)
        return path

    # ------------------------------------------------------------------ PDF
    @staticmethod
    def export_pdf(docx_path, pdf_path):
        """Export through Microsoft Word so the brand fonts are embedded. Windows: Word COM via PowerShell.
        Mac: Word via AppleScript. Returns True when the PDF exists."""
        docx_path, pdf_path = os.path.abspath(docx_path), os.path.abspath(pdf_path)
        if platform.system() == "Windows":
            ps = (
                "$w = New-Object -ComObject Word.Application; $w.Visible = $false; $w.DisplayAlerts = 0; $d = $null;"
                f"for ($i=0; $i -lt 10 -and -not $d; $i++) {{ try {{ $d = $w.Documents.Open('{docx_path}', $false, $true) }} catch {{ Start-Sleep -Milliseconds 1500 }} }};"
                "$ok = $false;"
                f"for ($i=0; $i -lt 10 -and -not $ok; $i++) {{ try {{ $d.ExportAsFixedFormat('{pdf_path}', 17); $ok = $true }} catch {{ Start-Sleep -Milliseconds 1500 }} }};"
                "try { $d.Close($false) } catch {}; try { $w.Quit() } catch {}"
            )
            exe = shutil.which("pwsh") or shutil.which("powershell")
            subprocess.run([exe, "-NoProfile", "-Command", ps], check=False)
        elif platform.system() == "Darwin":
            script = (f'tell application "Microsoft Word"\nopen POSIX file "{docx_path}"\n'
                      f'save as active document file name (POSIX file "{pdf_path}" as string) file format format PDF\n'
                      'close active document saving no\nend tell')
            subprocess.run(["osascript", "-e", script], check=False)
        return os.path.exists(pdf_path)
