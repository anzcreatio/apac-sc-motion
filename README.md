# apac-sc-motion

The Creatio APAC solution consulting motion as a Claude Code plugin: the same instructions, standards, templates and
library for every SC, updated in one place.

## What's in it (v0.14.0)

| Skill | Use it for |
|---|---|
| `sc-guide` | **Start here.** Onboards a new SC step by step, tells any SC what's next on a deal, logs feedback for the Friday digest |
| `sc-setup` | First run on a machine: finds the synced SharePoint folder, checks Python, PowerPoint, toolkit |
| `sc-first-meeting` | Discovery/BDR transcript → standard deck + light-config brief (Business Studio, then AI) + meeting plan |
| `sc-deck` | Build, rebuild, render or restyle a deck from a deal's `deck.json`; slide library; new templates |
| `sc-rfp` | RFP / TOR in any layout → requirements register, honest fit-gap (standard to no, confidence, evidence, POC tier, effort), bid / no-bid recommendation, and a consistency check of the bid team's answers. The bid team writes the response |
| `sc-workshop` | Australia (no RFP): 2-hour requirements workshops, one journey each. Pre-work email, draft journey, agenda and capture sheet; then from the transcript a requirements register (rated with the `sc-rfp` engine: gaps and effort, no bid decision), a solution model in Creatio terms for `sc-demo-plan`, a follow-up email from the gaps, and a playback for the customer to sign off |
| `sc-requirements` | After the demo build, before any RFP: a neutral business requirements checklist in the customer's words (with how to verify and a suggested scoring tab) for the AE to send, plus an internal file tracing every line to the source, demo scene, fit and differentiator |
| `sc-demo-plan` | Plan a demo build: demo bar (the floor), Business Studio first then AI, library and pattern book reuse, custom components where they earn it, open space for the SC, demo script for the toolkit |
| `sc-clickpath` | Two HTML pages from the demo click path: SC practice guide (clicks, talk track, watch-outs, practice mode) and a customer-safe recap (DRAFT until the SC approves; text and screenshot checks) |
| `sc-harvest` | After every demo: L1 into the demo library within 2 working days (read-only package export, build log, customer-specific list, manual steps) |
| `sc-weekly-lessons` | Friday digest: collects the week's evidence, measures, and proposes at most 3 changes (2+ deals each) for Renzo to approve; applies and publishes approved ones |
| `sc-meeting-review` | After a meeting: presented deck vs generated deck (`deck_diff.py`), transcript scorecard, living solution summary update, next-session enhancements, lessons |
| `sc-lessons` | Learn from past deals: every deal-start skill runs `learn_from_deals.py` first (team lessons, questions, limits, and what worked on similar deals by any SC; "Applied from past deals" in the output). Also a chat of its own for lessons learnt: paste notes or an R&D email; it files feedback and updates the shared registers of product limitations and discovery questions (`Lessons/registers/`) |
| `sc-coach` | Explain Creatio so a customer can't misread it: reviews a transcript for every explanation and answer (plain words, no hedging, approved claims only, no new doubts, length) with customer-ready and dead-simple rewrites and the top 3 habits; "how do I explain X?" in one line, 30 seconds and deeper; the team's library of approved explanations (`Lessons/registers/explanations.json`). Coaching is for the SC, not about them: it stays on their own PC and they choose what to share with Renzo |
| `sc-academy` | Learn to build Creatio demos with Claude: one module per skill area on a fictional deal (Kestrel), each with a guided lab, a hands-on check and three feedback questions; progress per SC in `Lessons/training/`; labs on your own training stand, built the way a real deal is, with a reset. Keeps itself current: fingerprints every toolkit and plugin SKILL.md, marks modules stale and drafts updates for Renzo to approve; Friday tips on where people get stuck |
| `sc-desk` | The SC's work desk, so deals never stall on our side (a task desk, not a CRM: no stage, forecast or value): each deal's commitments ledger (`commitments.json`, captured from meeting reviews, next-steps slides, AE briefs, follow-ups; "done: <what>" closes one), stall checks, a daily brief ("what's on today", or 8 am weekdays as a scheduled task: top 5 actions, today's meetings and prep, follow-up drafts never sent), a Friday desk view (deals by health, quality trend, tips) and a load check. Reads Outlook calendar and sent mail read-only when the Microsoft 365 connector is on. Private to each SC: briefs stay on the SC's PC, and it never shows another SC's deals or workload. Renzo's Friday view: team totals in `Lessons/desk/weekly/`, per-SC view in his local folder |
| `sc-customer-academy` | Customer enablement (a one-hour session, a workshop up to 3 hours, or the full course): teach a customer's team to build and extend their own Creatio apps (including on top of their CRM) with Claude and Creatio's public AI App Development Toolkit. Track 1 business builders, Track 2 developers and IT; their dev or sandbox only (refuses anything that looks like production); feedback per module; a customer pack (workbook pages + the `creatio-build-coach` skill) they keep after the SC's check. Keeps itself current from the toolkit's skills and runbooks |
| `sc-inbox` | Review new Knowledge Hub / corporate decks dropped in SharePoint `_inbox`; propose library and catalogue updates |

| Folder | What |
|---|---|
| `standards/` | `DECK-STANDARD-v0.5.md` (slide order, two stages, `deck.json` format) · `WRITING-STYLE-v0.1.md` (sound like an SC) · `DEMO-BAR-v0.3.md` (the minimum for every demo) |
| `knowledge/` | Industry packs, differentiator catalogue, AI governance "can say" lines, live-change kit, call sheet |
| `skills/sc-deck/templates/` | Slide templates: `creatio-designed-2026` (default), `creatio-2026` |
| `patterns/` | Pattern book: demo ideas from our deals, competitors and the Knowledge Hub (screenshots in SharePoint `Patterns/`) |
| `library/` | Reusable demo modules catalogue (Phase 2) |
| `lessons/` | What we learned from the field and what changed because of it |
| `tests/deck/` | Fictional sample deck that exercises every slide type |

New SCs: open SharePoint `Plugin/START-HERE.md` and paste its prompt into Claude.

## Where things live

| What | Where | Why |
|---|---|---|
| Skills, standards, templates, catalogue | This repo | Versioned; everyone updates with one command |
| Deals, transcripts, presented decks | SharePoint **APAC Solution Consulting** → Documents → `Deals/<account>-<initials>/` (rule in `sc-setup`) | Customer data stays in the Creatio tenant; synced to each SC |
| Corporate slides | SharePoint `Slide-library/` | Large binaries; `library:<file>` in `deck.json` |
| New templates and corporate content | SharePoint `_inbox/` | Download from the Knowledge Hub, drop here; `sc-inbox` reviews |
| Weekly digests | SharePoint `Lessons/` | Readable by the team |

## Install (each SC, once, Windows or Mac)

**Self-serve:** open SharePoint **APAC Solution Consulting → Documents → `Plugin/START-HERE.md`** and paste its prompt
into Claude. Claude finds the synced folder and installs the plugin. After a restart, `sc-guide` takes the SC through
setup (`sc-setup`) and onboarding. The overview deck is `Plugin/APAC-SC-Motion-Overview.pptx` (source: `rollout/overview/`).

By hand, in a terminal, with your own synced path:

| | Path to the plugin |
|---|---|
| Windows | `C:\Users\<you>\OneDrive - Creatio\APAC Solution Consulting - Documents\Plugin\apac-sc-motion` |
| Mac | `~/Library/CloudStorage/OneDrive-Creatio/APAC Solution Consulting - Documents/Plugin/apac-sc-motion` (or under `OneDrive-SharedLibraries-Creatio`) |

```
claude plugin marketplace add "<path>"
claude plugin install apac-sc-motion@apac-sc
```

Then restart Claude and say **"start the sc-guide"**.

**Updates:** when Renzo announces a new version, run `claude plugin marketplace update apac-sc`, then
`claude plugin update apac-sc-motion@apac-sc`, and restart Claude Code. `PUBLISHED.txt` in the folder shows the
version and date.

**Don't edit files in the SharePoint `Plugin` folder.** Every publish overwrites it. Send changes to Renzo.

## Publishing a new version (Renzo)

1. Change and test here (the git repo), bump `version` in `.claude-plugin/plugin.json`, add a `CHANGELOG.md` line, commit.
2. `powershell -ExecutionPolicy Bypass -File publish.ps1` (refuses uncommitted work or an unchanged version).
3. Tell the SCs to update.

Later, when Creatio IT gives us a company GitHub repo: push this repo there, and each SC runs
`claude plugin marketplace add <repo URL>` once. Nothing else changes.

## Changing the motion

1. Change the skill, standard or template here. Bump the version in the file name for standards
   (`DECK-STANDARD-v0.5.md`) and in `.claude-plugin/plugin.json`.
2. Rebuild `tests/deck/sample-fictional/deck.json` with `--render` and look at every slide.
3. Add a line to `CHANGELOG.md` and, if it came from the field, a file in `lessons/`.
4. A change to the standard needs evidence from **2+ deals or 2+ SCs**, or one serious failure.
