# Changelog

## 0.9.1 (12 Nov 2026)
- `sc-rfp`: `ours_ids` in the map for sheets that mix our scope and the bid team's (Pegadaian); summaries and the
  consistency check show the English translation for non-English RFPs. Tested on Pegadaian (Bahasa, 49 of 112 lines ours).

## 0.9.0 (11 Nov 2026): RFP fit-gap
- New skill `sc-rfp` (+ `scripts/rfp.py`, `FIT-RUBRIC.md`): scan any RFP/TOR layout, map columns (SC confirms), build a
  register (ours vs bid team), rate every requirement in parallel batches, fit-gap workbook, bid / no-bid page, and a
  consistency check of the bid team's answers. Tested on Mandiri Sekuritas (blank, 190 lines) and Adira (87 FR lines,
  blind, checked against the submitted answers).
- `sc-guide`: `sc-rfp` added to the motion map.

## 0.8.0 (11 Nov 2026): onboarding
- New skill `sc-guide`: onboards a new SC one step at a time (8 steps, progress saved in SharePoint
  `Lessons/onboarding/<sc>.json`), tells any SC the next step on a deal, logs feedback to `Lessons/feedback/`.
  Blind-tested: practice runs go to `Deals/_practice/`, older deal folders matched loosely, asks whether the meeting happened.
- SharePoint `Plugin/START-HERE.md`: the paste-in prompt that installs the plugin and starts the guide.
- `sc-weekly-lessons`: the digest now reads SC feedback and onboarding progress.
- `sc-first-meeting`: uses the folder the caller names (practice), never the real deal.

## 0.7.3 (11 Nov 2026)
- Library: `field-sales-visit` AI complete; the Suntory briefing agent's instructions were read from AI Studio (read-only).

## 0.7.2 (11 Nov 2026)
- `sc-harvest` step 3b: the AI is saved as text in `Library/<id>/ai/` (agent instructions word for word, skill
  prompts, MCP tool definitions, AI process steps, set-up scripts, tests). Catalogue modules get an `ai` list.
- Backfill: `field-sales-visit` AI folder (tools complete; agent instructions still to copy from AI Studio).

## 0.7.1 (11 Nov 2026)
- `build_deck.py`: narrow card rows (4–5 cards) leave room for titles that wrap to three lines.
- Lessons from the Suntory demo review (`lessons/2026-11-11-suntory-oceania.md`).

## 0.7.0 (11 Nov 2026): weekly digest W46, all three proposals applied
- `DEMO-BAR-v0.2.md` item 7: Full and Proof demos on a clean stand or the library master stand, never next to another
  customer's demo; rehearse on the presenting device, network and login with the fallback ready.
- `sc-demo-plan`: asks for the stand and the presenting device alongside the three pre-build questions.
- `sc-clickpath`: the SC page's "Before you start" always opens with the device rehearsal line.
- `CORE-PACK-v0.2.md`: J4 field visit (from Suntory) and J5 project or site selling (from H&G).

## 0.6.0 (11 Nov 2026)
- New skill `sc-weekly-lessons` (+ `scripts/collect_week.py`): the Friday digest. Collects deck reviews, meeting
  reviews, coverage scores, demo plans, transcripts, lessons, inbox and pattern intake, harvest and recap status;
  measures; proposes at most 3 changes backed by 2+ deals (or one serious failure); applies only what Renzo approves.
  First digest: SharePoint `Lessons/weekly/2026-W46.md`.

## 0.5.1 (11 Nov 2026)
- Click path pages now use the Creatio Workflow Explorer navigation (Renzo's preference): stat strip, demo-flow
  strip, tabs (Click path / Before you start; What you saw / About this demo), sticky filter rail, collapsible use
  cases and steps, Creatio logo. Same safety checks.

## 0.5.0 (11 Nov 2026): demo library and click paths
- Demo library: every demo harvested to **L1 within 2 working days** (demo bar item 8); item 9 + §6b **build for reuse**
  (own packages, module and customer layers, neutral schema names, seed data in the package, manual steps written down).
- New skill `sc-harvest` (+ `scripts/list_package.py` to decode exports offline). First harvest, all L1, read-only:
  `site-selling` (H&G, 5 packages), `field-sales-visit` (Suntory, 5 packages; shared-stand dependency flagged),
  `enquiry-recruitment` (SAHE, 3 packages). Packages, source, scripts and READMEs in SharePoint `Library/`.
- New skill `sc-clickpath` (+ `scripts/build_clickpath.py`): two self-contained HTML pages per demo, SC practice and
  customer-safe recap; customer page checks text for internal terms and requires a screenshot review; DRAFT until
  approved. Built for H&G and Suntory; the review caught another customer's agent name, other demos' accounts and
  orders, a test record and placeholders in the screenshots.
- `sc-demo-plan`: package plan + harvest in the build order. `sc-meeting-review`: checks the L1 harvest.

## 0.4.1 (11 Nov 2026)
- Before any build, `sc-demo-plan` (step 0) and `sc-first-meeting` (step 5b) ask the three pre-build questions:
  competition, anything else the customer gave us (RFP, email, documents), anything else to know. Answers recorded.
- Every skill: questions for the SC go at the top of the message.

## 0.4.0 (11 Nov 2026): Phase 1, demo configuration
- `standards/DEMO-BAR-v0.1.md`: the minimum for every demo (8 items; Light, Full and Proof levels), element labels
  (Pain, Asked, Asked (must), Differentiator, SC idea), nothing banned, time and buffer, custom components, outside
  best practice, prospect branding.
- `patterns/`: pattern book (16 patterns: 14 from our builds, 2 from the PRC test), SharePoint `Patterns/` for
  screenshots and `_inbox` for new ideas (`sc-inbox` handles intake).
- New skill `sc-demo-plan`: pains and asks, hero journey, labelled scenes, Business Studio then AI, reuse, custom
  components, live change, open space for the SC, demo bar check, hours, proof mode, demo script for the toolkit.
- Tested on Perth Radiological Clinic (`tests/demo-plan/`, not shipped): 12 findings fixed the same day.
- `sc-first-meeting` uses the Light bar; `sc-meeting-review` records which patterns landed. Knowledge links fixed.

## 0.3.1 (11 Nov 2026)
- Published to SharePoint (`Plugin/apac-sc-motion`) with `publish.ps1`; README install and update steps for SCs.

## 0.3.0 (11 Nov 2026)
- `platform` slide type: the whole platform set (01 AI Studio, 02 AI Twin, 03 Business Studio, 04 AI Coding Agent) from
  `Slide-library/catalogue.json` → `standard_sets.platform`, with speaker notes; required in every deck.
- `standards/WRITING-STYLE-v0.1.md` (from Renzo's edits and click-path lines) + builder style check.
- `DECK-STANDARD-v0.3.md`: two stages (components before the build, `build` slide + screens after); `build` slide type;
  `row` screen layout; title fitting.
- `sc-first-meeting` step 7: second pass after the light config is built.
- Proof: both blind decks redone (`tests/blind/<deal>/blind-deck-v3`) with natural wording and real stand screenshots.

- Blind test of `sc-first-meeting` on H&G and Suntory (`lessons/2026-11-11-blind-test-fm-v0.3.md`): top pain and
  hypothesis matched what was presented; about 10–11 of 13 slides presentable after wording edits (Claude's reading).
  Fixed: title fitting (40 → 30 pt on 2 lines), component overflow warning, `ai_shown`, one question on the timeline,
  coverage scoring rule, AE/BDR claims rule, same-day meeting rule, research age rule, `library/catalogue.json`,
  broken knowledge links, standard example and row limits.
- New skill `sc-meeting-review` + `deck_diff.py`: presented vs generated deck, slide by slide (kept / edited / library /
  hand-made / dropped, words removed and added, % of the deck from the kit), reports to SharePoint `Lessons/deck-edits/`;
  transcript scorecard, living summary update, next-session enhancements (Business Studio then AI), lessons.
  First run: H&G old 3-slide kit vs presented deck = 43% from the kit (2 edited, 8 library, 13 hand-made).

## Library update (11 Nov 2026, no code change)
- First `sc-inbox` run on 4 Knowledge Hub decks: Slide-library now holds a merged platform overview (9), Hello (19),
  Telecom (9), Technical (85) and AI Advisory (11) files; old files in `_old/`. Catalogue and governance proposals
  pending. See `lessons/2026-11-11-inbox-knowledge-hub.md`.

## 0.2.0 (11 Nov 2026)
- Standard look = `creatio-designed-2026`, built from `Suntory Introduction Nov 2026.pptx` (the Suntory deck as
  presented): frame, caps label, 26 orange icons, cover photo, timeline next steps. `DECK-STANDARD-v0.2.md`.
- Library slides now copied in Python with their pictures and video (PowerPoint refuses automation on 'Confidential'
  labelled decks). `office_deck.ps1`: render/extract only, read-only, never quits a PowerPoint the SC had open.
- `creatio-2026` base rebuilt from the H&G deck as presented.
- New skill `sc-inbox` + `inbox_scan.py`: new corporate decks in SharePoint `_inbox` compared slide by slide with the
  Slide-library; proposals for library, catalogue and governance; nothing applied without approval.
- SharePoint `Slide-library/catalogue.json` (2 files, 16 slides; 7 duplicates flagged).
- Suntory `deck.json` rebuilt to the 18-slide presented deck; compared slide by slide.

## 0.1.0 (11 Nov 2026): Phase 0
- Repo and plugin skeleton (`.claude-plugin/plugin.json`, `marketplace.json`).
- `sc-deck`: one template-driven deck builder (`build_deck.py`) replacing the per-deal build scripts; 12 slide types;
  corporate slides from the SharePoint Slide-library; render to PNG; PowerPoint always closed after use.
- `standards/DECK-STANDARD-v0.1.md`, from the H&G, Suntory and Telkomsel decks as presented.
- `sc-first-meeting` (FM v0.3): FM v0.2 plus the full standard deck, a component slide per hypothesis part
  (Business Studio first, then AI), and a light-config brief split into Business Studio and AI.
- `sc-setup`: finds the synced SharePoint folder, checks tools.
- `knowledge/`: packs, catalogue, governance pack, live-change kit and call sheet copied from the design workspace.
- Tested: H&G, Suntory and Telkomsel decks rebuilt from `deck.json` alone and compared with what was presented.
