---
name: sc-harvest
description: Add a finished Creatio demo to the APAC demo library - export what was built read-only, write the build log, the customer-specific list and the install steps, and register it at level L1 (the minimum for every demo, within 2 working days); later promote modules to L2 (installable with seed data and reset) or L3 (generic, tested on the master stand) when they are reused. Use after a demo or proof, when an SC asks to harvest, save or reuse a demo build, when sc-meeting-review flags a missing harvest, or when a plan wants to reuse a library module.
---

# sc-harvest


> **Mac:** run every `python …` command below as `python3 …` (`sc-setup` records which one works in `~/.apac-sc-motion.json`).
Every demo built through this process starts the demo library (Renzo, 11 Nov 2026). **L1 is the minimum, within 2
working days of the demo.** Higher levels are earned by reuse, not required up front.

Paths are relative to this skill's folder; plugin root = `../..`.

## Levels

| Level | Contains | Promote when |
|---|---|---|
| **L0 Pattern** | An idea in `../../patterns/catalogue.json` | It's built on a deal → L1 |
| **L1 Reference** (minimum) | Read-only **package export** of what was built · build log · screenshots and click path · **the AI as text** (agent instructions, skill prompts, tool definitions) · **customer-specific list** · manual steps that don't export · patterns covered · catalogue entry | Someone reuses it once → L2 |
| **L2 Package** | L1 + installs cleanly on a fresh stand with its seed data and a reset; customer layer split out | Used on 2+ deals → L3 |
| **L3 Module** | Generic (`lab` prefix, neutral names and example data), passes `creatio-uc-readiness` on the master stand, own click path | — |

Master stands: listed in `../../library/stands.json` (demo bar §6c); the first is `11011710-demo`. Owner: Renzo.

## L1 harvest (after every demo)

1. **Ask first** (at the top of your message): which stand and packages hold the build, and anything built outside
   them. Don't guess package names; read the deal's build log or demo plan.
2. **Export read-only:** `clio pull-pkg <Package> -e <env>` for each package, per the `creatio-demo-clone` skill (§1).
   Never write to the stand. Save the `.zip` files to SharePoint `Library/<module-id>/packages/`, named
   `<Package>-<yyyy-mm-dd>.zip`.
3. **List what's inside:** `python scripts/list_package.py "<Library/<id>/packages>"` decodes every export offline
   and writes `contents.json` (schemas, data bindings, files, dependencies). Check `DependsOn` for packages that
   belong to another demo on a shared stand: those won't install on a clean stand.
3b. **Capture the AI as text** (Renzo, 11 Nov 2026). A package export doesn't carry AI Studio agents and often misses
   the tool registrations, so save every AI element of the demo to `Library/<module-id>/ai/`:

   | File | What | Where it comes from |
   |---|---|---|
   | `agent-<name>.md` | Agent name, mode, model, channel, the environments it's deployed to, the tools it uses, and its **full instructions, word for word** | AI Studio: read-only (Studio CLI/API `GET`), or ask the SC to copy it from the agent page |
   | `skill-<name>.md` | Creatio.ai skill prompts (all 7 sections) and the action processes they call | The skill page, or the package if it's bound |
   | `mcp-tools.json` | Each MCP tool: external name, description, input and output schema, source (process or C# action) | The `McpTool` rows or the build script that registered them |
   | `ai-steps.md` | AI steps inside business processes: the process, the prompt, what a person confirms | The process designer or the package |
   | `register-*.py` / `.sql` | Any script that set the AI up | The deal's `build/` folder |
   | `README.md` | Install order for the AI part, what to rename per customer, and how it was tested (questions asked, answers expected) | Write it |

   If an agent's instructions only exist in AI Studio and you can't read them, mark the file **"instructions
   missing"** and ask the SC to paste them in. Never save credentials, tokens or real customer data.
4. **Check the build-for-reuse rules** (`../../standards/DEMO-BAR-v0.3.md` §6b): own packages, two layers, neutral
   names, seed data in the package, manual steps written down. Note every break; don't fix the stand.
5. **Write `Library/<module-id>/README.md`** (SharePoint):
   - What it does, in one paragraph, and the pains it served (their words, the deal).
   - **Install:** packages in order and dependencies, then the manual steps (settings, flags, timers, DCM rows, AI
     Studio agents, users and rights).
   - **Customer-specific list:** every name, caption, logo, data set and term to change when reusing it.
   - Screenshots (copy from the click path) and the click path link.
   - Gotchas from the build log.
6. **Register it** in `../../library/catalogue.json` → `modules` (format below), level L1, and link the patterns it
   covers (update those patterns' `proven` field).
6b. **Built on a master stand?** (the plan's `master`). Update its entry in `../../library/stands.json`: add the
   journey (module, packages, deal, date), new personas, the home page link and data set, and the restore point path.
   Then list what takes the stand back to neutral (the customer package to remove, captions and seed data to swap)
   and ask the SC to approve that clean-up (it writes to the stand, so it's the toolkit's job with their yes). Set
   `in_use_by` back to null and `status` to `ready` only once it's done; until then `in_use`.
7. **Report** in ≤ 8 lines: module id, packages exported, rule breaks, what reuse would cost (hours to rebrand).

## Promotion

- **To L2** when a plan reuses an L1: install on a fresh stand (`creatio-demo-clone` §4, ask before any install),
  split the customer layer, add seed data bindings and a reset, record the measured install-and-rebrand time.
- **To L3** when used on 2+ deals: rename to `lab` + neutral names, generic example data, run `creatio-uc-readiness`
  on the master stand, record a click path. Propose it to Renzo; it's a day of work.

## Catalogue format (`library/catalogue.json` → `modules[]`)

`{id, name, level, what, pains, patterns, source_deal, built, stand, packages: [{name, file, layer: module|customer}],
manual_steps, customer_specific, ai: [{type: agent|skill|mcp_tool|process_step, name, file, complete: true|false}], reuse_estimate_h, sharepoint, harvested, owner, notes}`

## Rules

- Read-only on every stand. Installs and compiles only with the SC's explicit yes, per the toolkit's gates.
- Never put credentials, real customer data or customer documents in the library. Demo data only.
- Packages and screenshots go to SharePoint `Library/`; only the catalogue and READMEs' summaries go in git.

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is
none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).

**Feedback as you go** (`../../standards/FEEDBACK-LOOP-v0.2.md`): when the SC corrects, overrides or rejects what
you produced, write a feedback file (`Source: chat`, with this skill and step) without asking. At the end of the run,
ask **one** short question about how it went, tied to what just happened, and log the answer (`Source: asked`).
Never in practice folders.
