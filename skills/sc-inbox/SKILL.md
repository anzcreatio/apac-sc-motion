---
name: sc-inbox
description: Review new corporate material the team has dropped in the SharePoint _inbox (decks downloaded from the Creatio Knowledge Hub, new slide templates, product or AI positioning, customer stories) - read every slide, compare it with the Slide-library and the differentiator catalogue, and propose what to add or update, then apply only what the SC approves. Use when someone says they added files to the inbox, asks what's new from the Knowledge Hub or marketing, asks to refresh the slide library or catalogue, or as part of the weekly lessons run.
---

# sc-inbox


> **Mac:** run every `python …` command below as `python3 …` (`sc-setup` records which one works in `~/.apac-sc-motion.json`).
New corporate material goes in **SharePoint → APAC Solution Consulting → Documents → `_inbox`**. Anyone can drop
files there (download from the Knowledge Hub, then drag in). This skill turns them into reusable, approved knowledge.
**Nothing changes without the SC's yes.**

## Steps

1. **Scan:** `python scripts/inbox_scan.py` → `_inbox/_scans/inbox-scan-<date>.md` (+ `.json`). For each slide: text,
   layout, pictures/video, and the closest Slide-library slide marked **same / changed / new**. PDFs and Word files are
   listed; read those directly.
2. **Look:** render each new deck (`python ../sc-deck/scripts/render_deck.py "<file>"
   "_inbox/_scans/<name>-png"`) and look at the slides marked new or changed.
3. **Judge each new or changed slide** and sort it into one table:

   | Proposal | When | Where it goes |
   |---|---|---|
   | **Add to Slide-library** | Reusable in customer decks: platform, AI, product, industry, proof | `Slide-library/<topic>-<yyyy-mm>.pptx` + `Slide-library/catalogue.json` |
   | **Replace in library** | A newer version of a slide we already have | Same file name, new month; old file to `Slide-library/_old/` |
   | **Catalogue update** | A new claim, proof point, analyst rating, customer story or number | `knowledge/DIFFERENTIATOR-CATALOGUE` (with source file and date). Never invent a claim from a picture |
   | **Governance check** | Anything about AI, data, hosting, security, compliance | Compare with `knowledge/AI-GOVERNANCE-PACK-LITE` "can say" lines; flag conflicts, don't change them |
   | **New template** | A new corporate slide master or style | Propose a new `sc-deck` template folder (see the `sc-deck` skill) |
   | **Ignore** | Internal-only, pricing, outdated, or not for customers | Say why in one line |

4. **Show the SC the table** (≤ 15 rows, most useful first) and ask which to apply.
5. **Apply only the approved rows:** extract slides with `office_deck.ps1 -Action extract`, update
   `Slide-library/catalogue.json` (`{file, slides, topic, title, source, added, notes}`), edit the catalogue with the
   source cited, bump versions and add a line to `../../CHANGELOG.md`.
6. **File the original:** move it to `_inbox/_done/<yyyy-mm-dd>/` and add a short entry to `../../lessons/`
   (what arrived, what we took, what we ignored).

## Patterns (SharePoint `Patterns/_inbox`)

SCs drop demo ideas there: a screenshot, a link, two lines on why it's good (from a competitor demo, the Knowledge
Hub, a partner, their own build). For each: write a draft entry for `../../patterns/catalogue.json` (what, why it
works, pains, native / custom / AI, how to build it in Creatio, hours, **source and date**), put the screenshot in
`Patterns/<source>/`, and show the drafts to Renzo with the inbox table. Competitor patterns: learn the idea, never copy
screens, branding or wording. Approved entries go in; the original moves to `Patterns/_inbox/_done/<date>/`.

## Rules

- Customer-facing claims only from the catalogue: a deck in the inbox is a *source* for the catalogue, not a licence
  to quote it. Numbers keep their exact unit and source.
- Keep Creatio's sensitivity labels. Never remove or change a label to make a file easier to process.
- Big files (video) stay in SharePoint; don't copy them into the repo.

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).
