---
name: sc-deck
description: Build, rebuild, restyle or check a Creatio APAC customer deck from a deal's deck.json using the team deck standard - cover, current understanding, hypothesis, component, screen, solution summary, roadmap and next-steps slides, plus corporate slides pulled from the SharePoint Slide-library. Also renders every slide to PNG for checking, extracts slides into the slide library, and adds a new corporate PowerPoint template. Use whenever an SC asks to make, update, fix or render a deck or slides for a deal, change the solution summary, add corporate slides, or apply a new template.
---

# sc-deck


> **Mac:** run every `python …` command below as `python3 …` (`sc-setup` records which one works in `~/.apac-sc-motion.json`).
The deck is data: `deck.json` in the deal folder is the source, the `.pptx` is built from it. Edit the JSON and
rebuild; don't hand-edit the built deck unless the SC asks (hand edits are lost on the next build, and the
`sc-meeting-review` skill learns from what the SC changed in the presented deck).

Standard: `../../standards/DECK-STANDARD-v0.6.md` (slide order, word rules, every field). Read it before writing JSON.

**Visual types (v0.6, creatio.com style):** reach for `landscape` (what they run + the gap, a source per tile),
`compare` (two ways side by side), `milestones` (dated why-now), `statement` (one big idea), `band` (section
divider), `hero_screen` (a product screen on navy), `quote` (their own words) and `photo_cards` (brand photos only)
where they make the point better than text. Every visual carries a point; no decoration (Navalo: "reads as AI-made").
Example: `../../tests/deck/visual-types/deck.json`.

## Before a new or reworked deck

**Learn from past deals** (`../sc-lessons/SKILL.md` "Learn from past deals"): run
`python ../sc-lessons/scripts/learn_from_deals.py brief --stage deck --deal "<deal folder>" --pains "<their top pains>"`.
Use what fits (what SCs edited or dropped before presenting on similar decks, slides that landed,
approved answers for the speaker notes), and list it in an **Applied from past deals** section (one line each: what we're doing
differently and the lesson id or deal it came from). Then log it: `learn_from_deals.py applied --deal ... --stage deck
--item "<id>: <what we did>"`.

## Commands

| Task | Command (from this skill's folder) |
|---|---|
| Build + render | `python scripts/build_deck.py <deal>/deck.json --render` → `<out>.pptx` and `<out>-png/slide-NN.png` |
| Build to another file | add `--out <file.pptx>` |
| Render any deck | `python scripts/render_deck.py <pptx> <dir>` (Windows: PowerPoint; Mac: PowerPoint for Mac, else LibreOffice, then PyMuPDF). If it can't render (exit 2), the deck is still fine: open it for the SC and ask them to check the slides by eye |
| Put corporate slides in the library (**Windows only**) | `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/office_deck.ps1 -Action extract -Deck <pptx> -Slides "4,5,6" -Out "<team root>/Slide-library/<name>-<yyyy-mm>.pptx"` |

Needs Python 3 with `python-pptx` and `Pillow` (Mac: plus `pymupdf` to render); PowerPoint only to render. Library slides are copied in Python
(PowerPoint automation is refused on Creatio 'Confidential'-labelled decks). `office_deck.ps1` opens decks read-only,
quits PowerPoint afterwards unless the SC already had it open, and never removes a sensitivity label. If a hidden
`POWERPNT.EXE` is left running after a failure, tell the SC rather than killing it.

## Words

Follow `../../standards/WRITING-STYLE-v0.1.md`. The builder prints `style:` warnings (vendor words, colon titles,
long titles, semicolons, em dashes): fix them in `deck.json`, don't ignore them.

**Confidential terms** (`../../standards/CONFIDENTIAL-TERMS-v0.1.md`): a deck for the customer itself may use
their terms, but keep anything they asked us not to share off the slides anyway (decks get forwarded). A deck for
anyone else (another customer, a team or training deck): `python ../sc-lessons/scripts/confidential.py scan --all
<deck.json>` first.

**Delivery support:** when the deal shows partner delivery risk, the roadmap or next-steps slide can carry one line
such as "Creatio supports your team and partner through delivery" (`../../knowledge/DELIVERY-ASSURANCE-v0.2.md`
§5–6). Never a price, hour count or package name on a slide or in the notes.

## After every build

1. Read the warnings. Each one is a fix or a deliberate choice you can explain.
2. **First build: open every PNG** and look: text cut off, overlaps, empty areas, wrong screenshot, placeholder text.
3. Fix in `deck.json`, rebuild, then **open the PNGs of the slides you changed only** (each slide is built from its
   own entry, so the others can't have moved). Keep a list of the slide numbers you edited. **Open every PNG again**
   when the change could touch every slide: template, theme, deal name or other fields shared by all slides, slides
   added, removed or reordered (numbers shift), library slides changed, or a new version of the builder. Each slide
   image costs about 1.2k tokens, so a 15-slide deck is ~18k per full look.
4. Tell the SC the deck path and anything they must check (numbers, quotes, claims).

## Library slides

`{"type": "library", "file": "library:<name>.pptx", "slides": [1, 2]}` pulls slides from the SharePoint
`Slide-library` (what's there: `Slide-library/catalogue.json`; new material arrives through the `sc-inbox` skill). The team root comes from `~/.apac-sc-motion.json` (`sc-setup`), the
`APAC_SC_ROOT` variable, or the nearest parent folder that holds `Slide-library`.

## New corporate template

1. Make `templates/<name>/`, copy the template as `base.pptx`, keep one content slide with the title, subtitle and
   page-number shapes on it.
2. Write `template.json` like `templates/creatio-2026/template.json`: those three shape names, the content area in
   inches, colours, font, cover colour.
3. Build `../../tests/deck/sample-fictional/deck.json` with `"template": "<name>"`, render, check every slide.
4. Bump the deck standard's version and changelog if the default template changes.

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).

**Feedback as you go** (`../../standards/FEEDBACK-LOOP-v0.2.md`): when the SC corrects, overrides or rejects what
you produced, write a feedback file (`Source: chat`, with this skill and step) without asking. At the end of the run,
ask **one** short question about how it went, tied to what just happened, and log the answer (`Source: asked`).
Never in practice folders.
