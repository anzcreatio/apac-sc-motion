# Document standard v0.1: every Word document in the Creatio look

**Rule (Renzo, 18 Nov 2026):** every Word document the SC motion produces uses Creatio's brand look, taken from
creatio.com. That covers customer and partner documents (sizing, workshop playbacks, proposals, partner packs,
RFP answers in Word, as-built summaries, briefs) and internal Word documents too. It applies to every skill and to
any Word document Claude writes ad hoc (including through the generic `docx` skill): build it with the doc kit.
Markdown working files (`.md`) are not Word documents and stay as they are.

**Kit:** `standards/doc-kit/creatio_doc.py` (class `CreatioDoc`) + `standards/doc-kit/creatio-logo.png`.
Never hand-style a Word document; if the kit is missing a block you need, add it to the kit.
First built for the Agrobank sizing (`Deals/agrobank-fa/03-sizing.pdf` is the reference).

## 1. The look

| Element | Spec |
|---|---|
| Colours | Text #181818 · accent orange #FF4013 · navy #011D59 (table headers) · soft grey #F0F0F0 (panels) · muted grey #5F6368 (captions, footer) · zebra rows #F7F7F7 · estimates #FFE9E2 |
| Fonts | Headings Montserrat (bold) · body Arial 10 pt. Open Sans (the website's body font) isn't installed on SC laptops, so Arial |
| Cover | Creatio logo top left · full-width orange band with a small spaced-caps label (`CUSTOMER · TOPIC`), the title in white 26 pt, a one-line subtitle · then Prepared for / Date / Status · a short "How to read this document" note · page break |
| Sections | Small orange spaced label with a number (`01 · SUMMARY`) above a 17 pt Montserrat title. Kept with what follows |
| Tables | Navy header row in white Montserrat, light grey row lines only, zebra rows, first column bold. Short tables (14 rows or fewer) stay on one page; long ones repeat the header |
| Key numbers | Up to 3–4 tiles: big orange figure over a short grey caption, on soft grey panels |
| Callout | Soft grey panel with a thin orange rule for a key message or a decision the reader must make |
| Estimates | Any figure we estimated rather than took from the customer: row shaded #FFE9E2, and listed again in a "To confirm" section |
| Footer | `Creatio · <title> · <status> · Page n`, 7 pt grey, on every page |
| Page | A4 portrait, 2 cm margins (landscape allowed for wide tables) |

## 2. Writing

Customer and partner documents follow `WRITING-STYLE-v0.1.md`: talk to them ("you", "your team"), plain words,
numbers as digits, no vendor words, no em dashes. Never in a customer or partner document: internal names, chats or
past bids, rule ids (R16, ST11), tool names ("calculator", "skill", "Claude"), "SC check" lines, emoji. Every
recommendation that isn't final carries its status line on the cover and in the footer.

## 3. Build, export, check

1. Build with the kit (see the docstring in `creatio_doc.py`).
2. **Export a PDF through Word** (`CreatioDoc.export_pdf(docx, pdf)`; Windows via Word, Mac via Word and AppleScript).
   The PDF embeds Montserrat, so it looks right on the customer's machine. Send customers the PDF unless they need
   to edit; send the `.docx` to colleagues who will edit it.
3. **Look at every page** (render the PDF to images): no heading stranded at the bottom of a page, no table split
   mid-row, no orphan last line on its own page, numbers rounded sensibly (390 Mb/s, not 386.6 Mb/sec).

Montserrat must be installed for the headings (Windows: user fonts; Mac: Font Book). `sc-setup` checks it.

## 4. Where it's applied

| Producer | Status |
|---|---|
| `sc-workshop` playback (`workshop.py playback [--pdf]`) | Uses the kit (0.32.3) |
| `sc-sizing` (`sizing.py build`) | Moves to the kit in 0.33.0 (after the infrastructure team's review). Until then, deal scripts follow this standard (Agrobank: `sizing/build_doc.py`) |
| Any other Word document (proposal, partner pack, as-built summary, RFP response in Word) | Build with the kit |
| PowerPoint | Not covered here: `DECK-STANDARD-v0.6.md` |

## Changelog

| Version | Date | Change |
|---|---|---|
| v0.1 | 18 Nov 2026 | First version, from the Agrobank sizing document (Renzo: apply to every Word document in the motion) |
