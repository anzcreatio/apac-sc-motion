# Lessons: the decks we actually presented (11 Nov 2026)

**Source:** H&G `07-creatio-and-hg-deck.pptx` (10 Nov), Suntory `11-Suntory-Creatio-positioning-v2.pptx` (11 Nov),
Telkomsel `02-first-meeting-slides.pptx` (12 Nov). Each was rebuilt from a `deck.json` with the standard builder and
compared slide by slide (Phase 0 test).

## What the SC changed after generation (the learning signal)

| # | Change | Deals | Action |
|---|---|---|---|
| 1 | Cover changed to red, date removed | H&G, Suntory | **Adopted** in deck standard v0.1 (2 deals) |
| 2 | Generated 3-slide pack grew into a full deck: Creatio intro, why Creatio, one slide per screen, roadmap, next steps | H&G (23 slides), Suntory (10) | **Adopted**: the standard is now the whole deck, not 3 slides |
| 3 | 8 corporate AI Studio slides inserted by hand | H&G | **Adopted**: `library` slide type + SharePoint `Slide-library` (first file: `creatio-ai-studio-overview-2026-11.pptx`) |
| 4 | Confirm questions removed from the hypothesis slide | H&G | Adopted as default (the next-steps slide already carries them). Watch: 1 deal |
| 5 | Playback "What we heard" (quotes) replaced by "Today → where you want to be", no quotes | H&G | Both layouts kept (`understanding` rows vs cards). Watch which the next 2 deals use |
| 6 | Slide 2 retitled "Context we are using to showcase Creatio today" | H&G | Not adopted (1 deal). Watch |
| 7 | Suntory deck in a richer designed style: hero image, icons, eyebrow labels, logo top right | Suntory | **Adopted** (Renzo, 11 Nov): template `creatio-designed-2026` is the default |
| 8 | The real Suntory deck was `Suntory Introduction Nov 2026.pptx` (18 slides), not v2 (10): 8 corporate platform/AI slides added after "Built for one way of selling" | Suntory | Same pattern as H&G #3 → **2 deals**: a platform/AI section from the Slide-library belongs in the standard deck after the understanding slides |
| 9 | Next steps: owners removed from the slide, dates rounded to the month, the closing question moved to the notes | Suntory | Allowed (owners in notes). Watch: 1 deal |
| 10 | Hand-made layouts the builder doesn't have: orange "Built for one way" statement slide, two screenshots side by side with text under each, grouped cards with icon lists | Suntory | Candidates for new slide types if a second deal uses them |

## Gaps the standard now catches

- Suntory's presented deck had **no hypothesis slide and no solution summary** (the summary was a separate file).
  The builder now warns when a required slide is missing.
- Next steps without dates (H&G) → warning; the rule is a named person and a date.

## Library

- The two corporate files harvested from H&G and Suntory share 7 of 8 slides (found by `sc-inbox`'s scan). Keep
  `creatio-platform-overview-2026-11.pptx`; only slide 6 of the H&G file is unique. Consolidate on Renzo's OK.

## Process lesson

- An orphaned PowerPoint/Word automation process locked a deal folder for a day. `office_deck.ps1` always quits
  Office in a `finally` block, unless the SC already had PowerPoint open.
- PowerPoint refuses automation on Creatio 'Confidential'-labelled decks ("Automation rights are not granted"), and a
  failed attempt leaves a hidden PowerPoint that can't be closed by script. Library slides are now copied in Python;
  PowerPoint is only used read-only to render and extract.
