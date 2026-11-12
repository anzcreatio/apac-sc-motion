# Changelog

Every release needs an entry here: `## <version> (<d Mon yyyy>): <title>`, what changed for SCs, and any one-off action
as "**Each SC: …**". `publish.ps1` refuses to publish without it, tags the commit `v<version>`, and the Monday task
`sc-release-message` (Renzo's PC) turns last week's entries into a Teams message in SharePoint `Plugin/release-messages/`.

## 0.15.2 (12 Nov 2026): release discipline (maintainer only)
- `publish.ps1` stops if this changelog has no entry for the version, and tags each published commit `v<version>`.
- New `release-notes.ps1` prints entries by version or date. A Monday 8 am task drafts the weekly release message
  from it for Renzo to share. Nothing changes for SCs.

## 0.15.1 (12 Nov 2026): deal folders carry the creator's initials
- `sc-setup` step 1b stores the SC's initials as `"sc"` in `~/.apac-sc-motion.json` (`rh` Renzo, `wn` Willy, `fa`
  Ferdhi; suggested from the computer login, the SC confirms). New "Deal folder rule": `<account>-<sc>`, deal folder
  only, one folder per account (reuse it whatever its suffix), never renamed. Folders made before 12 Nov keep their names.
- Applied in `sc-first-meeting`, `sc-guide`, `sc-rfp` and `sc-workshop`. **Each SC: run `sc-setup` once after updating.**

## 0.15.0 (12 Nov 2026): build plan before any build
- **New gate:** `sc-first-meeting` step 6b and `sc-demo-plan` step 12a. The SC approves a visual build plan before any
  stand is touched (Renzo stopped the Navalo build to add it).
- `sc-demo-plan/scripts/build_build_plan.py` + `templates/build-plan.html`: `build-plan.json` → `NN-build-plan.html`.
  A wireframe per demo step drawn from standard layouts (record, list, dashboard, rules table, before/after), so a deal
  writes content, not HTML. Per step: the customer's verbatim quote (**checked against the transcript and email; a
  quote that isn't there stops the build**), or an **"our idea"** blind spot with its source and the question we ask
  (at most 2, after their scenes); minutes against the demo slot; the differentiator and competitor angle; reuse.
  Plus their criteria against our demo (covered / partly / not shown, and what we say about each gap), the build list
  and hours against the budget, data model, example data, what's not built, and decisions with our recommendation.
- First use: Navalo (`Deals/metrics-credit-partners/03-build-plan.html`).

## 0.14.1 (12 Nov 2026): first meeting asks for the website and customer documents
- `sc-first-meeting` (FM v0.4): new inputs. **Company website** (required; ask in the first message, but keep going
  with research and say which site was used) anchors the "right company" check. **Anything the customer has sent**
  (email, brief, RFP): if it arrives after the deck, save it as `00-customer-…` and rework the hypothesis, components
  and next steps against it, because their written criteria outrank the call. From the Navalo deal (Renzo, 12 Nov).

## 0.14.0 (12 Nov 2026): AE brief standard, flow and outputs slides
- `sc-demo-plan` step 13: the AE brief is a standard output for every demo session (`ae-brief.json` →
  `scripts/build_ae_brief.py` → `NN-ae-brief.html`, from `templates/ae-brief.html`): recap tick-boxes, a reaction log,
  the question word for word with replies, the close with licence questions, a Don't list, and a summary back to the SC.
  No opening line, no durations. The agenda slide goes into `deck.json` with the same decision question.
- `sc-deck`: new `flow` (step-by-step diagram) and `outputs` (what each step produces) slide types.
- Rollout deck: the flow slide is now an 8-step diagram, plus a new slide listing what the customer gets and what we
  keep at each step.

## 0.13.0 (12 Nov 2026): requirements checklist and agenda slide
- New skill `sc-requirements` (+ `scripts/requirements.py`): after the demo build, a neutral requirements checklist
  for the AE to send before any RFP (Read me, Requirements with a vendor-response drop-down, suggested Scoring), built
  from an internal master that traces each line to the source, scene, fit and differentiator. Refuses to build on
  our product terms or competitor names in customer text, a Must that isn't C + high confidence, or a fit we'd fail.
  Example: Suntory `17-requirements-checklist.xlsx` (46 lines).
- `sc-deck`: new `agenda` slide type (run of the meeting + the decision we'll ask for); deck standard slide 1b, yes for
  demo meetings; no open "what would make this a success?" slot.
- `sc-guide` and `sc-demo-plan` point to `sc-requirements` after the build.

## 0.12.0 (12 Nov 2026): self-serve rollout, Windows and Mac
- `rollout/`: `START-HERE.md` (one prompt: Claude finds the synced folder on Windows or Mac and installs the plugin,
  with an in-chat `/plugin` fallback when the `claude` command isn't available), the overview deck
  (`rollout/overview/deck.json` → `APAC-SC-Motion-Overview.pptx`, built with `sc-deck`) and the announcement text.
  `publish.ps1` copies START-HERE and the deck to `Plugin/`.
- `sc-setup`: Windows and Mac paths, `python` / `python3`, packages (PyMuPDF on a Mac), PowerPoint check per OS;
  records `python` and `platform` in `~/.apac-sc-motion.json`.
- New `sc-deck/scripts/render_deck.py`: renders on Windows (PowerPoint) or Mac (PowerPoint for Mac or LibreOffice,
  then PyMuPDF); `build_deck.py --render`, `sc-inbox` and `sc-meeting-review` use it. Slide extraction stays Windows only.
- Every skill that runs scripts says to use `python3` on a Mac. `sc-guide`: opening files and updating the plugin work
  on both. Builds folder on a Mac: `~/Projects/builds/<account>/`.

## 0.11.0 (12 Nov 2026): workshops (Australia)
- New skill `sc-workshop` (+ `scripts/workshop.py`, `AGENDA-120.md`, `CAPTURE-SHEET.md`, `PREWORK-EMAIL.md`,
  `DRAFT-JOURNEY.md`): 2-hour requirements workshops, one journey each, starting from a draft journey the room
  corrects. From the transcript: a requirements register (same format as RFPs), a solution model in Creatio terms
  (objects mapped to standard objects, fields, stages, roles, rules, systems, channels, AI moments, example data,
  outcomes), a gap check that drafts the follow-up email, and a playback .docx for the customer to sign off.
- `rfp.py`: `validate` for hand-written registers; workshop registers get "gaps and effort" instead of bid / no-bid.
- `sc-demo-plan` reads the solution model; the playback build between workshops is Light, on a clean stand.
- `sc-guide`: `sc-workshop` in the motion map and next-step table. `sc-setup` checks openpyxl and python-docx.

## 0.10.1 (12 Nov 2026): fixes from the Pegadaian POC plan test
- POC brief: hours labelled as configuration only (plan 2-3x); full draft tests; new section 2b lists claims already
  submitted that say more than our fit-gap (the POC is tested against them).
- `rfp.py coverage`: in a markdown plan a ref must start a table row (a passing mention no longer counts).
- `sc-demo-plan` proof mode: ask whether the customer sets the POC format (their scenarios replace ours), the readout
  language and local test accounts for each channel; TOR-only labels (requirement = Asked (must), C; pain = I);
  plan submitted claims with the bid team.

## 0.10.0 (12 Nov 2026): RFP → POC hand-off
- `rfp.py poc`: POC brief from the fit-gap (Build lines grouped with draft tests, must-have gaps to handle in the story,
  Show evidence, questions, low-confidence lines) + a JSON of the refs.
- `rfp.py coverage`: checks every Build ref and must-have gap appears in the demo plan and the click path cards.
- `sc-demo-plan` proof mode: starts from the POC brief; a Requirement coverage table (ref, scene, test, status); refs
  carried into the demo script and click path notes. `sc-rfp` step 8 produces the brief.

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
