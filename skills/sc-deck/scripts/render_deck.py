"""Render every slide of a deck to PNG (slide-01.png, ...), on Windows or a Mac. Read-only on the deck.

    python render_deck.py <deck.pptx> <out dir>          (Mac: python3)

Windows: PowerPoint through office_deck.ps1 (1600x900).
Mac:     PowerPoint for Mac saves a PDF copy (AppleScript); if that fails, LibreOffice (soffice) if installed.
         The PDF becomes PNGs with PyMuPDF (pip install pymupdf).
If nothing can render, it says so and exits 2: the deck itself is fine, the SC just opens it in PowerPoint.
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def pdf_to_png(pdf, out_dir, width=1600):
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz  # older PyMuPDF
    doc = fitz.open(pdf)
    for i, page in enumerate(doc, 1):
        zoom = width / page.rect.width
        page.get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(os.path.join(out_dir, "slide-%02d.png" % i))
    return len(doc)


def mac_pdf(deck, tmp):
    pdf = os.path.join(tmp, os.path.splitext(os.path.basename(deck))[0] + ".pdf")
    # A copy, so PowerPoint never holds or changes the original (OneDrive-synced files lock easily).
    copy = os.path.join(tmp, os.path.basename(deck))
    shutil.copy2(deck, copy)
    script = '''
tell application "Microsoft PowerPoint"
    open POSIX file "%s"
    set p to active presentation
    save p in POSIX file "%s" as save as PDF
    close p saving no
end tell''' % (copy, pdf)
    try:
        subprocess.run(["osascript", "-e", script], check=True, capture_output=True, timeout=300)
        if os.path.exists(pdf):
            return pdf
    except Exception as e:
        print("PowerPoint for Mac export didn't work (%s); trying LibreOffice" % str(e).splitlines()[0][:120])
    soffice = shutil.which("soffice") or "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    if os.path.exists(soffice) or shutil.which("soffice"):
        subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", tmp, copy], check=True,
                       capture_output=True, timeout=300)
        if os.path.exists(pdf):
            return pdf
    return None


def render(deck, out_dir):
    deck = os.path.abspath(deck)
    os.makedirs(out_dir, exist_ok=True)
    for f in glob.glob(os.path.join(out_dir, "slide-*.png")):
        os.remove(f)
    if sys.platform == "win32":
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", os.path.join(HERE, "office_deck.ps1"),
                        "-Action", "render", "-Deck", deck, "-OutDir", os.path.abspath(out_dir)], check=True)
        return len(glob.glob(os.path.join(out_dir, "slide-*.png")))
    try:
        import pymupdf  # noqa: F401
    except ImportError:
        sys.exit("Rendering on a Mac needs PyMuPDF: python3 -m pip install pymupdf")
    with tempfile.TemporaryDirectory() as tmp:
        pdf = mac_pdf(deck, tmp) if sys.platform == "darwin" else None
        if not pdf and shutil.which("soffice"):
            subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, deck], check=True, timeout=300)
            cand = glob.glob(os.path.join(tmp, "*.pdf"))
            pdf = cand[0] if cand else None
        if not pdf:
            print("Couldn't render: no PowerPoint export and no LibreOffice. The deck is fine; open it in PowerPoint to check it.")
            sys.exit(2)
        return pdf_to_png(pdf, out_dir)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    n = render(sys.argv[1], sys.argv[2])
    print("rendered %d slides to %s" % (n, sys.argv[2]))
