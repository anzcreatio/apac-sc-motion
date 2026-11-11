# apac-sc-motion

The Creatio APAC solution consulting motion as a Claude Code plugin: the same instructions, standards, templates and
library for every SC, updated in one place.

## What's in it (v0.4.0, Phase 1)

| Skill | Use it for |
|---|---|
| `sc-setup` | First run on a machine: finds the synced SharePoint folder, checks Python, PowerPoint, toolkit |
| `sc-first-meeting` | Discovery/BDR transcript → standard deck + light-config brief (Business Studio, then AI) + meeting plan |
| `sc-deck` | Build, rebuild, render or restyle a deck from a deal's `deck.json`; slide library; new templates |
| `sc-demo-plan` | Plan a demo build: demo bar (the floor), Business Studio first then AI, library and pattern book reuse, custom components where they earn it, open space for the SC, demo script for the toolkit |
| `sc-meeting-review` | After a meeting: presented deck vs generated deck (`deck_diff.py`), transcript scorecard, living solution summary update, next-session enhancements, lessons |
| `sc-inbox` | Review new Knowledge Hub / corporate decks dropped in SharePoint `_inbox`; propose library and catalogue updates |

| Folder | What |
|---|---|
| `standards/` | `DECK-STANDARD-v0.3.md` (slide order, two stages, `deck.json` format) · `WRITING-STYLE-v0.1.md` (sound like an SC) · `DEMO-BAR-v0.1.md` (the minimum for every demo) |
| `knowledge/` | Industry packs, differentiator catalogue, AI governance "can say" lines, live-change kit, call sheet |
| `skills/sc-deck/templates/` | Slide templates: `creatio-designed-2026` (default), `creatio-2026` |
| `patterns/` | Pattern book: demo ideas from our deals, competitors and the Knowledge Hub (screenshots in SharePoint `Patterns/`) |
| `library/` | Reusable demo modules catalogue (Phase 2) |
| `lessons/` | What we learned from the field and what changed because of it |
| `tests/deck/` | Fictional sample deck that exercises every slide type |

Coming next: `sc-harvest` + demo library (Phase 2), `sc-clickpath`, `sc-weekly-lessons` (Phase 3).

## Where things live

| What | Where | Why |
|---|---|---|
| Skills, standards, templates, catalogue | This repo | Versioned; everyone updates with one command |
| Deals, transcripts, presented decks | SharePoint **APAC Solution Consulting** → Documents → `Deals/<account>/` | Customer data stays in the Creatio tenant; synced to each SC |
| Corporate slides | SharePoint `Slide-library/` | Large binaries; `library:<file>` in `deck.json` |
| New templates and corporate content | SharePoint `_inbox/` | Download from the Knowledge Hub, drop here; `sc-inbox` reviews |
| Weekly digests | SharePoint `Lessons/` | Readable by the team |

## Install (each SC, once, about 5 minutes)

The plugin is published to the team SharePoint site: **APAC Solution Consulting → Documents → `Plugin/apac-sc-motion`**.

1. Sync the site if you haven't: open it in SharePoint → Documents → **Add shortcut to OneDrive**. Wait until the
   `Plugin` folder shows up in File Explorer.
2. In a terminal (PowerShell), with your own synced path:
   ```
   claude plugin marketplace add "C:\Users\<you>\OneDrive - Creatio\APAC Solution Consulting - Documents\Plugin\apac-sc-motion"
   claude plugin install apac-sc-motion@apac-sc
   ```
3. Restart Claude Code, then say: **"run sc-setup"**. It finds your SharePoint folder and checks Python, PowerPoint
   and the demo toolkit.

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
   (`DECK-STANDARD-v0.3.md`) and in `.claude-plugin/plugin.json`.
2. Rebuild `tests/deck/sample-fictional/deck.json` with `--render` and look at every slide.
3. Add a line to `CHANGELOG.md` and, if it came from the field, a file in `lessons/`.
4. A change to the standard needs evidence from **2+ deals or 2+ SCs**, or one serious failure.
