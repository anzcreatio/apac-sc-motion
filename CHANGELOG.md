# Changelog

**Chats never edit the version.** Any chat that changes the plugin commits the change and adds a bullet under
`## Unreleased` below: what changed for SCs, and any one-off action as "**Each SC: …**". Only `publish.ps1` picks the
version: it turns Unreleased into `## <version> (<d Mon yyyy>): <title>`, bumps `plugin.json`, commits, publishes and
tags `v<version>` (and refuses if `plugin.json` was changed by hand). The Monday task `sc-release-message` (Renzo's PC)
turns last week's entries into a Teams message in SharePoint `Plugin/release-messages/`.

## Unreleased

- **New build rules reach your demo toolkit by themselves.** After each plugin update, session start refreshes our
  build-rules block in the demo toolkit's notes (only that block, with a backup next to the file). You no longer need
  to re-run `sc-setup` for new rules. If the block was edited by hand, it says so and leaves it alone.
- **`sc-setup` checks for R&D's AI app development toolkit**, needed for mobile pages (build rules §7) and schema naming.
- **Each SC:** if `sc-setup` says the AI app development toolkit is missing, install it (it gives the two commands).

## 0.36.3 (19 Nov 2026): Install safety, UI kit 0.8.4, channels-showcase


- **Installs and other heavy jobs: one at a time per stand (build rules §1b, in every build session).** Before a package install, push, compile or restart, the stand must answer `/0/ping` with 200 and nothing else heavy may run on it; afterwards wait until it has settled (about 2 minutes) before the next one; never retry a failed install straight away. Back-to-back installs and a retry once took a sandbox down with a 502.
- **UI kit 0.8.4: releases and installs in one place.** Versions are picked only by the kit's `release.ps1`; installs only through `install.ps1` (stand list, deal OK, no downgrade, stand safety, install log). Every kit component shows its build as `data-kit-version`. Package: `Library/ui-kit/packages/labUiKit-0.8.4-2026-11-19.zip`.
- **Demo library: `channels-showcase` (L2, install-tested 19 Nov).** Social comments to cases with triage rules and a stage bar, "Check in core system" integration with an integration log (live relay `channels-relay.apac-sc-demos.workers.dev`), Contact "Conversations" tab, Channels and integrations Overview home, Kestrel Bank demo data, Telegram channel with AI answers from the knowledge base and handoff. Packages and install guide: SharePoint `Library/channels-showcase/`.

## 0.36.2 (19 Nov 2026): Release flow: versions picked only at publish


- **Versions are picked only at publish time.** Chats add changes under "Unreleased" in the changelog; `publish.ps1`
  assigns the next version, so two chats can no longer release the same number. Session start tells Renzo how many
  changes are waiting. Nothing changes for SCs.

## 0.36.1 (19 Nov 2026): which tool for which Creatio job, in every chat

- **New `standards/TOOL-ROUTING-v0.1.md`, loaded into every session** (like the chat standards), so Claude picks the
  right guidance in ad-hoc chats too: custom component → UI kit standard + R&D's instruction server; handlers, page
  bodies, C# → R&D's instruction server; mobile page → R&D's mobile conversion skill + build rules §7; pages,
  processes, data and AI through clio → demo toolkit; naming → R&D's schema naming skill.
- **Version clean-up:** the UI kit standard's file is now named `UI-KIT-STANDARD-v0.7.md` to match its content (it
  was v0.7 inside a v0.6 file name). Links in the plugin are updated.
- Nothing to do: it loads on your next session after updating.

## 0.36.0 (19 Nov 2026): build rules v0.8, mobile pages

- **Build rules v0.8 §7 (new), mobile pages**, from Creatio's mobile team pages in Confluence: web and mobile pages
  are separate (a web change doesn't reach the app); build mobile pages with R&D's `creatio-mobile-page-conversion`
  skill, plan first, phone only; check what the app shows before publishing, because publishing replaces it; convert
  related form pages that buttons open; no custom components on mobile (they show a placeholder), so plan native
  fields; offline demos: test every business rule with the network off; live lists set to always fetch fresh data;
  mobile workplace with every demo login. Rule 10 in the toolkit notes block.
- **Each SC:** re-run `sc-setup` once to pick up rule 10 in the demo toolkit's notes.

## 0.35.1 (19 Nov 2026): Bank.AI log asks first, with a one-sentence reminder

- `sc-bank-ai-log` now drafts the lines, then asks you before writing anything: one sentence on what the log is for
  (your bank's requirements, our proposed configuration and fit, gaps first, for Creatio's Bank.AI team; no prices,
  competitors or names) and how many lines and gaps it will add. Say yes and it writes them.
- Also ships the UI kit standard update from another chat (commit `ca7bf11`, 19 Nov): Record inbox, efficiency (2f),
  security (2g) and a build check in `standards/UI-KIT-STANDARD-v0.6.md`.

## 0.35.0 (19 Nov 2026): build rules v0.7, configuration quality from Creatio Confluence

- **Build rules v0.7 §6 (new):** rules from Creatio's internal Confluence (NCD no-code standards, R&D guides, support
  checklists) that the demo toolkit doesn't have yet: on a shared stand, a test case and no improvised steps; new
  lookup data in a new data binding; C# as source only; Freedom UI handlers pass to `next` and set `scopes`; bulk
  processes in the background; demo AI agents on delegated credentials; "missing in the Designer" means a package
  dependency; one business rule per field; CSP for blocked calls; how to prompt for a generated process; data model,
  metadata and NCD naming rules; two prompts for a custom component. Rule 9 in the toolkit notes block.
- **R&D's instruction server ships with the plugin** (`.mcp.json`: `creatio-instructions-mcp`). It's 41 documents R&D
  writes for AI agents: Freedom UI page metadata, handlers, components, C#, composable apps, each with "traps verified
  on a stand" (e.g. a `merge` on a list's columns replaces the whole array; a reload can still run the old client
  code). Claude loads it before page-body, handler, component or C# work. Not for processes, dashboards or data.
  Creatio VPN only: off VPN it shows "failed to connect", which is harmless.
- **Each SC:** nothing to install. If you added `creatio-instructions-mcp` by hand, remove that copy:
  `claude mcp remove --scope user creatio-instructions-mcp`. Re-run `sc-setup` once to pick up rule 9 in the toolkit notes.

## 0.33.1 (19 Nov 2026): duplicates in a demo need one feature switched on

- **Build rules v0.6 §5, new row:** the Freedom UI "Potential duplicates found" pop-up on save (Contacts: Edit record,
  Merge, Save anyway) only appears once the feature `EnableDeduplicationFreedomUI` is registered and switched on. Demo
  stands don't have it, so a duplicate contact saves with no warning. Feature toggles page → Create feature → switch
  on → Save changes → reload the page; no compile. It's on for the signed-in user only, so add every demo login.
  Found on bpd-bali-map, 19 Nov 2026.

## 0.34.0 (19 Nov 2026): RFP clarification questions, two sheets from one list

- **`sc-rfp` step 8b, clarification questions:** right after the fit-gap, Claude goes through a checklist
  (`skills/sc-rfp/CLARIFICATIONS.md`: weights and gates, which parts apply, Day 1 scope and volumes, systems of record
  and middleware, **which system owns cases** when CRM and workflow are both in scope, channels, third-party services,
  documents, regulation, residency, contract, references, demo) and keeps only what changes the answer, sizing, price
  or demo.
- **Two sheets from one list** (`scripts/clarify.py`): a working sheet for you (topic, what we need, why we ask,
  status, dropped questions with the reason) and a 4-column customer sheet (#, criterion IDs, question, their answer).
  Numbering is redone on every build, so cutting or adding a question never leaves gaps. Edited the customer sheet by
  hand? `clarify.py read` brings your changes back.
- **New standard `standards/CUSTOMER-QUESTIONS-v0.1.md`** for any question list a customer answers: one question per
  row, the reason inside the question only where it helps, state our assumption, cut what we can assume or what shows
  our hand, offer to answer optional parts (and ask how that's scored), no references to earlier calls, promise the
  outcome rather than a walkthrough of the internals. The cover email is drafted in your voice from your own sent emails.
- **RFP reading traps** (map step): a "Service Management" category is the vendor's own operations (bid team); a
  multi-platform overlay is n/a when we propose one platform. Deadlines are worked out from the issue date, and asks
  that are only in the cover email are flagged.
- `rfp.py` accepts verdicts as a list or as a dict keyed by requirement ID.
- Built from Renzo's edits on the Navalo RFP (19 Nov 2026).
- **Each SC:** nothing to install.

## 0.33.0 (19 Nov 2026): open chats carry a status mark; say "end chat" to close one

- **Chat tracking v0.2** (`standards/CHAT-TRACKING-v0.2.md` §2, replaces v0.1): every new chat's title starts with
  🟢. The mark changes as the work moves: 🟡 means it's your move (Claude asked you something), 🔵 means the customer
  or AE owes the next step. A closed chat has no mark, so the sidebar shows what's open at a glance.
- **Close chats on purpose:** say **"end chat"** (or press the End chat button Claude offers when the work looks
  finished). Claude removes the mark and, in a customer chat, marks the row done in `00-chats.md`. "Park this"
  removes the mark but keeps the chat on the desk.
- **Daily brief:** a new "Still open?" list shows marked chats nobody has touched for 3 days, so you can end, park or
  keep each one.
- **Each SC:** nothing to install. Your older chats have no mark; that's fine: start using "end chat" from today.

## 0.32.6 (18 Nov 2026): build rules v0.6, lessons from the BPD Bali map build

- **Build rules v0.6** (`standards/BUILD-RULES-v0.6.md` §5, and rules 5–8 in the block your demo toolkit reads):
  custom components start on the UI kit from day one (copy the kit's `kit-data`, `kit-write`, `_kit-tokens`); by
  build end the deal folder holds the component source (no `node_modules`), its README, the saved page bodies, the
  seed scripts and a handover note; when the browser pane is signed out, check headless with clio `page-smoke` or
  Playwright with clio's session; clio traps (package named after the app code, Lead/Account need package
  dependencies, `rows-file` in the temp folder, component package created first).
- **Web maps:** Freedom UI web pages have no map component (register L-001). A map is a custom component: Leaflet +
  OpenStreetMap passes Creatio's default security policy. Plan GPS, address search and pin → address from the start.
- **Build report** (`approval_pack.py report`) now lists the handover material in the deal folder and flags
  `node_modules`, `.angular` or `dist` folders that must not be synced.
- **Each SC:** run `sc-setup` once after updating, so the demo toolkit's notes get build rules v0.6.

## 0.32.5 (18 Nov 2026): UI kit 0.6.4 in the library; channels and integrations playbook

- **UI kit `labUiKit` 0.6.4** is now the one kit: Navalo and East West Bank components in one package (15
  components). Install file: SharePoint `Library/ui-kit/packages/labUiKit-0.6.4-2026-11-18.zip` (JS only, no compile,
  no restart). New since 0.5.0: every setting is a picker, native Creatio look, row caps, and writing components check
  permissions and the record's stage before saving, and say "not saved" when Creatio refuses.
- **`standards/UI-KIT-STANDARD-v0.6.md`**: kit status updated (Academy and forum to-dos done in 0.6.2; panels keep
  `ViewEncapsulation.None` on purpose, with `.kit-` prefixed selectors).
- **New `knowledge/CHANNELS-AND-INTEGRATIONS-PLAYBOOK-v0.1.md`**: how to configure and show integrations, chat
  channels (WhatsApp, Messenger, Instagram, Telegram, SMS, web chat), social comments and WhatsApp/SMS from a campaign,
  from Creatio Academy 8.3 and version 10. Nothing in it is proven on our stands yet: rehearse on a clean stand first.

## 0.32.4 (19 Nov 2026): custom components follow the Creatio Academy rules

- **`standards/UI-KIT-STANDARD-v0.6.md`** (was v0.5). New §2d: the rules from all 37 Freedom UI pages of Creatio
  Academy › Front-end development, each checked against the kit: build route (deferred format, Designer entries,
  ShadowDom + OnPush), zoneless change detection, settings panels (Academy "setup areas"), data loading, strings,
  icons, request handlers.
- **Heads-up for custom components:** Creatio 10.2.1 turns zoneless change detection on by default. Our kit is ready
  for it (Angular 22, zoneless provider) but not yet tested on a 10.2 stand: don't move a customer stand with our
  components to 10.2.1 before that test.
- Kit to-dos it found: pin library versions exactly, show settings-panel errors in the panel, cap rows on components
  that load a whole object, check `canSave` / `canDelete` before writes, translation files before a non-English customer.
- New §2e: field lessons from 40 Creatio Community forum threads. For SCs: custom components don't show in the
  **mobile app** (use native fields there), the kit needs **Creatio 8.3.3 or later**, and test a component by opening
  two records in a row (record A, then record B).

## 0.32.3 (18 Nov 2026): every Word document in the Creatio look

- **New `standards/DOC-STANDARD-v0.1.md` + `standards/doc-kit/creatio_doc.py`.** Every Word document the motion makes
  (playbacks, sizing, proposals, partner packs, anything Claude writes in Word) uses the creatio.com look: logo,
  orange cover band, Montserrat headings with orange section labels, navy tables, key-number tiles, estimates shaded
  orange, status line in the footer. Export a PDF through Word so the fonts travel, and check every page.
- **`sc-workshop` playback** now uses the kit; `workshop.py playback ... --pdf` also writes the PDF.
- `sc-sizing` moves to the kit in 0.33.0.
- **Each SC:** install the Montserrat font if `sc-setup` says it's missing (free from Google Fonts), then update the
  plugin (`claude plugin marketplace update apac-sc`, then `claude plugin update apac-sc-motion@apac-sc`).

## 0.32.2 (18 Nov 2026): custom components follow Creatio's own design tokens

- **`standards/UI-KIT-STANDARD-v0.5.md`** (was v0.4). New §2c, native patterns harvested read-only from a clean
  Creatio 10 stand: the exact `--crt-*` token names (spacing, radius, type, colours, palette, focus), how native
  cards, fields, lists, chips, buttons, tabs, focus and home-page widgets look, and the schema conventions native
  pages follow (size words not pixels, `PDS`/`<Name>DS` naming, `crt.*` requests, hide-when-empty converter).
- **Correction:** v0.4 said Creatio's `--crt-*` tokens aren't set at page level. They are, and they reach inside a
  component's Shadow DOM. The Navalo issue came from guessed token names that don't exist.
- **UI kit (`labUiKit`, not yet installed anywhere):** tokens now chain `--usr-kit-*` → Creatio token → measured
  value, so components follow a customer's theme and dark mode; the native focus ring and hover colour; pills in the
  native shape. Built locally; needs a rehearsal on a stand before the next deal uses it.

## 0.32.1 (18 Nov 2026): sizing fix

- **`sc-sizing`:** the database Data, Tempdb and Logs disks were dropped from the sizing when the calculator showed a
  decimal size (for example "Data — 1224.9 GB", which happens at larger user counts). Fixed. If you ran a sizing for
  more than a few hundred users, run `calc` and `build` again.
- **Each SC:** update the plugin (`claude plugin marketplace update apac-sc`, then `claude plugin update apac-sc-motion@apac-sc`) and restart Claude Code.

## 0.32.0 (18 Nov 2026): learning loop pilot (Renzo only)

- **Nothing changes for you yet.** This is a 2-week pilot on Renzo's deals (review 2 Dec). It only switches on for
  an SC whose `~/.apac-sc-motion.json` has `"pilot": ["call-it-first", "ready"]`.
- What's being tried: Claude asks for the SC's own 3-line call (pains, hypothesis, what to show) before writing the
  first-meeting pack or demo plan, then shows where it differs and why; a readiness check before a meeting
  (`sc-ready`: quiz from memory first, crib sheet after); and 💡 Learn points (at most 2, the ones that matter most).
  The goal: Claude makes us faster without making us dependent. Rules: `standards/LEARNING-LOOP-v0.1.md`.
- Chat format v0.2 adds the 💡 mark; new chat stage `Ready`.

## 0.31.0 (18 Nov 2026): start a deal with just a sizing request

- 📣 **When a partner has already run discovery and the demo and all they need is a sizing, start there.** Tell Claude
  "<customer> needs an on-prem sizing" and `sc-sizing` creates the deal folder by the usual rule (it reuses the
  account's folder whoever made it, and asks you on a close match). No transcript, deck or first-meeting pack needed.
- The folder gets `00-deal-start.md` (entry: sizing only, partner, who asked), and the chat is numbered with the new
  stage **`Sizing`**.
- `sc-guide` won't push you back to the first meeting on these deals. It moves them into the motion only when you
  say the deal is going to discovery, a demo or a proposal.

## 0.30.0 (18 Nov 2026): on-prem hardware sizing (`sc-sizing`)

- 📣 **New skill `sc-sizing`: ask Claude "what hardware does this customer need on-prem?"** and get a customer-ready
  Word document and Excel sheet: servers per environment (application, database, Redis, load balancer, Kubernetes,
  RabbitMQ, MongoDB, Creatio.ai), a reduced-footprint option with its trade-offs, storage at 1, 3 and 5 years
  (object storage, database, backups) and the software stack.
- It starts from Creatio's system requirements calculator (fetched live for every environment, page saved in the deal
  folder) and adjusts it only with sourced rules: Academy's on-site guides plus everything Sergey Sinienok has told
  us (Redis 1 or 6 nodes, Kubernetes for the services, no separate Kubernetes balancer, non-prod at 10% of users,
  how to reduce for a minimum, POC layout, files in S3 from day one, his storage method).
- **Everything is worded as a recommendation pending review by Creatio's infrastructure team**, and the check
  refuses words like "guaranteed" or "final sizing". An internal file lists every source and has a draft note for
  Sergey; nothing is final until he has reviewed it.
- Quick answers too: MS SQL edition, Redis Enterprise, Elasticsearch licence, "do we really need 6 Redis servers?".
- Tested against the bank RFI Sergey reviewed in January (every line matches) and his storage example from October.
- **Each SC: the next time a customer asks for on-prem sizing, run `sc-sizing` and send the draft note to Sergey with
  the document before it goes to the customer.**

## 0.29.0 (18 Nov 2026): replies you can scan, one table of your open work, creatio.com-style slides, no "SC check" lines

One update with everything since 0.26.0 (0.27.0 and 0.28.0 were never published on their own).

- 📣 **Every Claude reply has the same shape**: ❓ Questions for you first (each with Claude's default, so a one-word
  answer works), ⚠️ Watch out only for a real risk, ✅ Done with file links, then tables. Six marks, one meaning
  each; none in customer files. Applies in every chat (`standards/CHAT-FORMAT-v0.1.md`).
- 📣 **"What's running?" in any chat shows your 📋 Open work**: every customer chat that isn't done, across your
  deals: Stage, Status (🟢 active · 🟡 waiting on you · 🔵 waiting on the customer · ⏸ parked), Next, **Due** (or
  "unknown"), Age and a "Do first" line; ⚠️ on overdue and on anything waiting on you 3+ days. The 8 am brief shows it
  too, in a **Desk** sidebar section. Each customer chat keeps its row in `<deal>/00-chats.md`, is titled
  `<Customer> NN · <Stage> · <topic>` and sits in one sidebar section per customer (`standards/CHAT-TRACKING-v0.1.md`).
- 📣 **Decks can look like creatio.com**: eight new slide types (big statement, "what you run today" landscape with a
  source per tile, side-by-side compare, orange section band, dated milestones, product screen on navy, photo cards,
  the customer's words as a quote), deck standard v0.6. Every visual must make a point; `photo_cards` takes brand
  photos only. Try: `python skills/sc-deck/scripts/build_deck.py tests/deck/visual-types/deck.json --render`.
- **New default cover**: orange gradient, customer lockup in spaced capitals, a real product screen off the right
  edge. Put `\n` in the title to choose line breaks; `"art": false` or a `fill` brings back the plain cover.
- 📣 **No more "SC check required…" line** on anything the plugin makes (decks, emails, RFP, workshop, BOM, desk
  drafts, build plans, AE briefs). You still review everything and Claude never sends; DRAFT banners stay.
- **Each SC: start a new session after updating, ask "what's running?" and tell Claude which older chats are done.
  Delete any "SC check" line from drafts you made before 17 Nov.**

## 0.26.0 (17 Nov 2026): customer self-install guides for Claude + the Creatio toolkit (Windows and Mac)

- 📣 **You can now send a customer one page that gets Claude Code, clio and Creatio's AI App Development Toolkit
  running on their own Windows or Mac machine.** `sc-customer-academy` pre-work `F0` ("Before you come") links to two
  new guides, `modules/F0-install-windows.md` and `modules/F0-install-mac.md`: a few steps by hand, then one prompt
  pasted into Claude Code that installs everything and connects their **sandbox** site. Creatio's Academy setup-wizard
  page (what F0 used to point to) returns 404.
- Rules built in: the customer types every password in their own terminal (never in Claude, never `sudo` in
  Claude's shell); only public tools; covers Business Studio, not AI Studio. Fixes from real failures included:
  Mac uses Microsoft's .NET 10 installer (no Homebrew), the clio `rollForward` fix when only a newer .NET is
  installed, and the Windows Claude app's private copy of clio's settings.
- The customer pack (`customer_academy.py pack`) now ships both guides in every format, full course included, and
  links them from the workbook index. `B0` points to them too. Course v0.3.
- **Not yet tested on a clean machine.** On your first customer run, be on a call and log anything that breaks
  (`sc-guide` mode C).
- **Each SC: before you next run customer enablement, read the two guides once so you can walk a customer through them.**

## 0.25.1 (17 Nov 2026): NEW in the Slide-library: AI coding agent explainer deck

- 📣 **New deck for when a customer asks "what is the AI Coding Toolkit / AI coding agent?"**
  `Slide-library/ai-coding-agent-explainer-2026-11.pptx`, 5 slides on the designed template: (1) describe it,
  approve the plan, it's built; (2) where it runs and what it can touch (diagram, for IT); (3) what it can build and
  fix; (4) three screens from our own builds, made-up data; (5) why it matters. Customer-safe talk track in the
  speaker notes.
- Use it whole, or pull slides into a deal deck:
  `{"type": "library", "file": "library:ai-coding-agent-explainer-2026-11.pptx", "slides": [2, 4]}`.
- **Before you present it, read the SC-only rules** in `Deals/_examples/ai-coding-toolkit-explainer/README.md`:
  no "10x", no data-residency claims for the coding agent, be upfront that the agent itself needs a licence, never
  name the customers behind slide 4.
- `sc-deck`: new `map` slide type (the customer's platform as a hub, connected and wider opportunities around it).
- **Each SC: open the new deck once (Slide-library/ai-coding-agent-explainer-2026-11.pptx) and read its README, so it's ready the next time a customer asks.**

## 0.25.0 (16 Nov 2026): which licences a deal needs (sc-bom)

- **New skill `sc-bom`**: the bill of materials. From what we know about the customer (solution summary, demo plan,
  RFP or workshop register, meeting reviews, the AE's licence answers) it marks every Creatio product Yes / No / TBC with
  a reason and an evidence tag, works out the candidate Unlimited tier, lists what's **extra to quote** (AI Package,
  credit blocks, storage, dedicated blocks, VPN tunnel, region, Marketplace connectors), checks every gotcha that
  applies, and ranks the sizing questions for the next meeting. Writes `NN-bom.md` and `NN-bom.xlsx` (the AE's
  one-page summary first) for Deal Desk. **Internal only: no prices, no users per module** (the AE and Deal Desk own
  the quote). `bom.py check` refuses prices and user counts and enforces the rules (Unlimited needs an AI Package,
  Studio needs AI Platform and support, per seat needs a reason).
- **New `knowledge/BOM-CATALOGUE-v0.1.json`** (internal): 34 SKUs, the 7 Unlimited tiers, 18 gotchas, 13 sizing
  questions, from the FY27 Unlimited and 10x AI pricing decks (13 Nov 2026). Four items stay **OPEN** for Deal Desk
  (Unlimited AI allowance, Unlimited storage, VPN and region SKU names, CRM app editions).
- `sc-demo-plan`: the AE brief's licence questions now come from the BOM (`bom.py questions`), plus user numbers by role
  for Deal Desk. `sc-meeting-review` step 5a updates the BOM when a meeting gives sizing facts. `sc-guide` suggests
  `sc-bom` after a demo plan, a demo or the AE's licence answers.
- `sc-lessons`: new `registers.py add-gotcha` (SharePoint `Lessons/registers/bom-gotchas.json`); new gotchas apply to
  the next BOM straight away.
- Test: `python tests/bom/test_bom.py` (fictional deal).

## 0.24.0 (16 Nov 2026): existing customers, confidential terms, who owns what

### Confidential customer terms (new standard)
- **`standards/CONFIDENTIAL-TERMS-v0.1.md`**: when a customer asks us not to share something (their own categories,
  criteria, programme names), it stays in their deal folder. Everything shared (library, lessons, feedback, the
  Friday digest, team lessons) uses a generic label instead, e.g. "Archetype A". Criteria values and curated lists
  are never harvested at all.
- New script `skills/sc-lessons/scripts/confidential.py` (`add`, `never`, `show`, `redact`, `scan`). `scan` stops a
  shared write if a listed term is still there, and never prints the term itself.
- `sc-harvest`, `sc-lessons`, `sc-meeting-review`, `sc-weekly-lessons`, `sc-deck` and `sc-guide` (feedback) now check
  it before writing anything outside the deal folder.
- **Each SC: if a customer has asked you not to share something, tell Claude on that deal: "add confidential terms".**

### Existing customers get their own path (`sc-guide` mode D)
- For a customer already live on Creatio (often delivered by a partner): **as-built summary → gaps → Now / Next /
  Later roadmap with an owner per item → session deck → customer enablement → review and harvest.** Start with
  "what's next on <account>" as usual; the guide picks mode D when the solution is live.
- New template `knowledge/TEMPLATE-As-Built-v0.1.md` for a partner's handover or "reverse demo" (a meeting review
  didn't fit: there's no deck of ours to compare). `sc-meeting-review` now points handovers there.
- `deal_dates.py event` records a handover, go-live and each session (training / roadmap / enablement / QBR).
  Existing customers stay out of the sales-speed medians and get their own table in the stats.

### Who delivers and who owns each step
- Roadmap slides take an `owner` line per step (who can own it after handover). Required on existing-customer decks
  (`DECK-STANDARD-v0.5.md`).
- `sc-first-meeting` records the delivery partner and the account owner at the top of the prep.
- Taking over from a partner: customer-facing words stay "you own it", never a contrast with the partner; the
  as-built's "ownership gaps" table (source, API contracts and credentials, prompts, support) is filled first.
- **Each SC: nothing to do.** Rebuild a deck to use the roadmap owner line.

## 0.23.0 (16 Nov 2026): build on top of master stands

- **`standards/DEMO-BAR-v0.3.md`** (was v0.2), new §6c: when a new deal's use cases are complementary to a master
  stand (same industry or cross-industry, extends its core objects and personas, no clash), build on top of it as a
  new `lab<Module>` package instead of starting clean. One customer layer at a time; it comes off after the demo, so
  masters grow into one coherent solution with many journeys. Items 7 and 9 updated.
- **New `library/stands.json`**: the stand register (masters, status, journeys, personas, who holds it, off limits).
  First master `11011710-demo` (H&G's customer layer comes off first). `11013904-demo` is off limits.
- **`standards/BUILD-RULES-v0.5.md`** (was v0.4): on a master, the library packages in `extends` are in scope and go
  in the restore point; a master held by another deal is a hard stop. `approval_pack.py check` enforces it.
- `sc-demo-plan`: step 4 checks the master stands, plan has a stand plan, `build-plan.json` takes `master` and
  `extends`. `sc-harvest` step 6b updates the register and asks for the clean-up back to neutral.
- **Each SC: re-run `sc-setup`** to refresh the build-rules block in the toolkit notes (v0.5). Before a build, check
  `library/stands.json` for a master that fits.

## 0.22.0 (16 Nov 2026): Delivery Assurance knowledge (internal)

- **New `knowledge/DELIVERY-ASSURANCE-v0.2.md`** (internal only), from the Jan 2026 Delivery Assurance deck: the
  Start / Build / Grow framework, the three packages plus Freedom and what each includes, which partner-risk signals
  call for which package, and what you can and can't say to a customer. APAC owner: **Alex Klochkov**.
- Customers can hear that **Creatio stays involved and supports them through delivery**. Claude now raises it when a
  deal shows partner delivery risk: a talk track in the `sc-first-meeting` meeting plan, a line on the roadmap or
  next-steps slide (`sc-deck`), the workshop close (`sc-workshop`), a scorecard row in `sc-meeting-review`, and the
  bid recommendation and delivery answers in `sc-rfp`.
- **No prices, hours or package names in anything Claude produces.** Ask Claude in chat and it gives indicative
  prices with a warning that they may be out of date; check the latest with Alex before using them.
- **Each SC: nothing to do.** Raise it with your AE when a deal has a new partner, heavy integrations or a customer
  burned by a past CRM project.

## 0.21.0 (16 Nov 2026): one sidebar section per customer, UI kit standard v0.4, deck standard v0.5

### Deck standard v0.5 (decks that don't look AI-made)
- **`standards/DECK-STANDARD-v0.5.md`** (was v0.4), from the Navalo deck as presented on 16 Nov.
- No small caps label above slide titles any more (it read as AI-made). Bring it back with `"kicker": true` on a slide.
- Agenda: numbered cards, no minutes or names, solid orange "Today's goal" panel. Minutes and owners go to the speaker notes as a run sheet.
- Next steps: no owner names on the slide; they're in the notes, so say them out loud.
- `"show_owners": true` on an agenda or next-steps slide gives you the old layout.
- **Each SC: nothing to do.** Rebuild a deck to get the new look.

### One sidebar section per customer
- **New chat section rule** (`sc-setup`, used by `sc-guide` and `sc-first-meeting`): in the Claude desktop app, Claude files every chat about a customer under that customer's own sidebar section (creating it the first time, e.g. `Bussan Auto Finance (BAF)`), so all of a deal's chats sit together. Skipped where there's no sidebar (claude.ai, CLI) and for practice, scheduled and plugin chats.
- `HOW-TO-RUN-A-DEAL.md` mentions it.
- **Each SC: nothing to do.** Old chats stay where they are; file them by dragging them onto a section if you want.

### UI kit standard v0.4 (pages that look finished)
- **`standards/UI-KIT-STANDARD-v0.4.md`** (was v0.3). New section 2b, the look of every demo page around our components:
  **no text directly on the grey page background** (titles, subtitles and section headings on white cards), one
  header card per page, headline numbers first, lists with row numbers always on and an add-column (+) button, one
  accent colour, chart colours by meaning,
  slots that fit their cards, and a top-to-bottom check at 1440 x 900 before calling a page done.
- Section 1 now lists all eight live `labUiKit` 0.5.0 components (Stage funnel, Request checklist, Group overlap, Rate
  against target, Cycle time added); new build rules: every setting picked, not typed; exclusions apply to the person.
- `DEMO-BAR-v0.2.md` section 6 points to v0.4.
- **Each SC: before showing a home page or dashboard, check it against section 2b.**

## 0.20.1 (15 Nov 2026): how to run a deal, on one page
- **New: `HOW-TO-RUN-A-DEAL.md`** in SharePoint `Plugin/` (next to START-HERE). One page: each step of a deal with
  the exact line to start its chat, when to start a **new chat** (every new step, another deal, a long chat, after an
  update) and when to stay in the same one, plus the ten habits that win deals. Ask Claude "how do I run a deal?"
  any time and it shows you the page.
- The rule of thumb: **start each step in a new chat with "what's next on <account>"**. Everything is saved in the
  deal folder, so a new chat loses nothing.
- **Each SC: read `Plugin/HOW-TO-RUN-A-DEAL.md` (5 minutes).**

## 0.20.0 (15 Nov 2026): sc-desk so deals never stall on our side; coaching for you, not about you; every deal learns from the last
- **New: `sc-desk`.** Say **"what's on today"** and you get your top 5 actions (ranked by deadline and how close the
  deal is to the customer's decision), today's customer meetings with what's ready and what isn't, a ready-to-send
  follow-up draft for each stalled deal (addressed to the AE; your SC check; **never sent automatically**), and your
  open commitments.
- **Commitments ledger per deal** (`commitments.json`: what, owner, due, source, status). `sc-meeting-review` now
  captures its Commitments table onto it (you pick what was agreed); it also reads next-steps slides, the AE brief and
  follow-up drafts. Say **"done: send the slides"** to close one, "add: …" to add one, "booked the next session for
  the 20th" to record it.
- **Stall checks:** no activity for 7 days, a commitment overdue, a demo under 3 days away with no approved build
  plan, a harvest overdue, an approved recap not sent, no next meeting on record. `sc-guide` "what's next" puts these
  first.
- **Load check:** "am I overloaded?" counts the week's demos, meetings, build hours left and commitments due, and
  suggests what to move (build work first, never a customer session in the next 2 days) or hand over.
- **Fridays:** `sc-weekly-lessons` adds the desk view (`Lessons/desk/weekly/`): each SC's deals by health, next
  week's load, a team quality trend (demo bar, harvest on time, coaching anonymised, deal timing) and one or two tips.
- **Outlook (optional, read-only):** with the Microsoft 365 connector on, the brief reads your calendar and checks
  your sent mail for follow-ups and recaps. It never sends, drafts in Outlook or books meetings.
- **A task desk, not a CRM:** it never tracks pipeline stage, forecast or value. Ask the AE to update their CRM.
- **Private to you.** Your brief stays on your own PC (never SharePoint), and the desk only ever shows your own
  deals, commitments and workload: ask about another SC's and Claude will say it's theirs to share. Renzo sees the
  team's Friday view; the team page shows totals only, no names.
- **Coaching is for you, not about you (feedback loop v0.2).** `sc-coach` now keeps your coaching (scores, weak
  moments, habits) on your own PC only, never on SharePoint. At the end it asks once whether you want to share
  anything with Renzo (nothing, your top 3 habits, or the full note); you send it yourself. Nothing about how you
  performed is in the Friday digest, the desk view or a deal folder, and Claude never shows one SC another's coaching.
- A habit worth teaching becomes a team lesson only if you say yes, anonymised (no SC, deal or customer named).
- **Meeting reviews** no longer hold your own rating or habits: the review keeps "Better answers to their
  questions" for the deal. If you rate how you did, it stays in your private coaching note.
- **Training results** (`sc-academy`) stay on your PC too; only which training stand is yours is shared.
- **Every deal starts from what the team has learnt.** `sc-first-meeting`, `sc-demo-plan`, `sc-deck`, `sc-rfp` and
  `sc-workshop` now begin by reading the team lessons for that step, the questions to ask and product limits, and the
  learnings from similar deals by any SC (same industry or pains): what landed, what SCs changed in the deck before
  presenting, keep / change / stop lessons and reusable library modules. Each output gets an **Applied from past
  deals** section saying what we're doing differently and where it came from; drop any line that doesn't fit.
  Learnings only, never people: no coaching, ratings or quotes of our own people.
- Questions, limits and gotchas apply from the next deal; changes to the standard deck or a skill still wait for
  Friday. The Friday digest counts how many lessons each deal start used.
- **Feedback about the skills and Claude is for everyone**: still in `Lessons/feedback/`, with your name so Renzo
  can follow up. It's about the tool only, never your performance.
- **Each SC: run `sc-setup` once more** (or say "set up my daily brief"): it shows your first brief and offers to
  run it every weekday at 8 am on your PC.

## 0.19.0 (14 Nov 2026): sc-coach, explain it so they can't misread it; sc-academy, learn to build
- **New: `sc-coach`.** Share a meeting transcript and it finds every moment you explained a feature or answered a
  question, and scores each one: did it answer the question, plain words, confidence (no "I think", "should be able to", "in theory"), approved
  claims only (catalogue and governance "can say" lines; over-claims flagged), whether it opened new doubts, and
  length. Each weak one comes back with the quote and minute, why, a customer-ready rewrite and a dead-simple version
  with an everyday analogy, plus your top three habits to work on. Or ask "how do I explain X?" for a one-liner,
  30-second and deeper answer, what not to say, and the likely follow-up.
- **Explanations library** (`Lessons/registers/explanations.json`, through `registers.py add-explanation`): the
  team's approved answers, used first and word for word so we all say the same thing. New answers are proposed,
  never added silently; Renzo approves them on Friday.
- **Coaching is private** to you and Renzo (`Lessons/coaching/<initials>/`). The Friday digest only counts patterns,
  never names or quotes anyone. What we all learn from it goes on a team page, **`Lessons/explaining-it/EXPLAINING-IT-LESSONS.md`**:
  10 lessons so far, each with a do, a don't and a drill, anonymised. Read it before your next call.
- **New: team lessons page, `Lessons/TEAM-LESSONS.md`.** Everything we've learnt across deals so far (before the
  meeting, the deck, building and rehearsing, explaining it, claims and AI, after the meeting), with no names or deals.
  The Friday digest keeps it up to date; `sc-guide` shows it to new SCs. Easy-read version: `Lessons/TEAM-LESSONS.html`
  (top 5 before every call, a filter per stage, search, do / avoid cards; works on a phone).
- `sc-meeting-review` now adds a short "Explaining it" section (no scores, no weak quotes: the review is in the deal
  folder) and writes the full coaching to your private folder.
- Tell the coach when a rewrite is too long or "a customer wouldn't say that": it logs the feedback and proposes the
  fix for Friday.
- **New: `sc-academy`.** Say "train me" and Claude teaches you to build Creatio demos with our skills, one step at a
  time, on a fictional deal (Kestrel Facility Services). Path 1, nine modules (about 10 hours, any number of
  sittings): setup and your lab stand, first meeting, demo plan and approval pack, stand prep and object model,
  Freedom UI pages, demo data and a home page, business processes, a Creatio.ai skill, then readiness, click path,
  harvest (dry run) and reset. Each module: why it matters, the skills, a guided lab, a hands-on check Claude
  verifies, and traps from our own builds. Progress is saved (`Lessons/training/<you>.json`), so "next module" picks
  up where you left off.
- **Your own training stand.** Each SC trains on a stand of their own, with no customer demo on it; the course
  refuses a stand that appears in a real deal's notes or is already another trainee's. Labs are built the way a real
  deal is (stand prep, stock Case reused, replacing copies of stock pages), all in the lab app and its `Acad<initials>`
  package, and the last module resets the stand, with your yes.
- **Three questions at the end of every module** (hardest part, did the lab work, how useful 1-5) become feedback
  files (`Source: training`) for the Friday digest.
- **The course keeps itself current.** On Fridays `sc-weekly-lessons` fingerprints every toolkit and plugin skill,
  marks a module stale when a skill it teaches changes, and drafts the update with the diff. Nothing changes in the
  course until Renzo approves it. While a module is being updated, Claude teaches from the current skill and tells you.
- To start: when you have an hour and your training stand, say "train me".
- **New: `sc-customer-academy`.** Teach a customer's team to build and extend their own Creatio apps, including on
  top of their CRM, with Claude and **Creatio's public AI App Development Toolkit** (nothing internal goes in front
  of the customer). Track 1, business builders, 7 modules: builder kit and ground rules, Business Plan first, extend
  CRM data, build the app and pages, extend CRM pages safely, brand and mobile, a capstone on their own use case.
  Track 2, developers and IT, 4 modules: environments and packages, source control and deployment with rollback,
  Classic to Freedom UI, governance for AI-assisted building. About 14 hours for both.
- Say "prepare customer enablement for <account>": it asks for their product, people, tracks and **dev or sandbox
  environment** (it refuses anything that looks like production unless the customer confirms it isn't), then guides
  each session step by step. Their feedback stays in the deal folder; the team copy names the role, not the person.
- **Customer pack:** workbook pages plus a Claude skill (`creatio-build-coach`) they keep after we leave. It stays a
  DRAFT until you've checked every page. You send it; Claude never does.
- It keeps itself current from the toolkit's own skills and runbooks; Renzo approves every course change.
- **Start short:** a **one-hour session** ("Your first Creatio app in an hour": ask in plain words, approve the plan,
  build, then extend the CRM client page with it) and a **workshop of up to 3 hours** (the hour, then their own idea,
  one "make it yours" change, and how it gets live properly). Both need a 15-minute "Before you come" checklist done
  by their IT beforehand (no installing in the room), use exact prompts to copy, plain words with a one-page glossary,
  and a mini practice scenario. The full course stays for customers who want depth. `prep --format 1h|3h|full`.

## 0.18.1 (14 Nov 2026): approve upfront, build non-stop, safely
- Build rules v0.4 (`standards/BUILD-RULES-v0.4.md` section 4). With the build plan, `sc-demo-plan` sends one
  approval pack to confirm (`scripts/approval_pack.py new`): the plan's items, the stand, compiles, restarts (our own
  clean stand only), custom components once each rollback is written, two tries per item, demo data, and reversible
  decisions on defaults. Then: a 5-minute pre-flight while you're still there, a restore point of the deal's packages,
  and a build that doesn't stop to ask. Each item is checked as it's built; one that fails twice is rolled back and
  skipped while the rest carry on. Hard stops: out of scope, a restart not approved, a sign-in only you can do,
  deleting non-demo data, a choice that can't be undone, the plan changing, the time budget running out, anything to
  a customer. You get a notification and `build/build-report.md` at the end.
- `sc-setup` offers the permission setup (`standards/build-permissions.json`): an allowlist plus auto-mode rules that
  block passwords and credentials files, `git push`, unapproved restarts, deleting outside our demo packages and
  sending anything to a customer. Builds only edit the deal and builds folders.
- **Each SC:** after updating, say "run sc-setup" once (build rules into your toolkit notes, permission setup), and
  start each build in a new chat in auto mode.

## 0.18.0 (13 Nov 2026): today's goal, feedback loop, /sc-lessons, meeting card
- **Today's goal opens every demo deck** (DECK-STANDARD v0.4, FM v0.6). The agenda slide shows "Today's goal": the
  decision we'll ask for at the end, word for word. The SC asks the same question on the next-steps slide. The
  builder warns if a demo deck has no agenda, if the closing question uses different words, or if "not yet" doesn't
  pin down what to do next. Wording by meeting type in the standard §1b (`meta.meeting`: first_demo, value_demo, proof).
  `sc-meeting-review` records the answer, and a "not yet" becomes the next session's first scene.
- **Feedback as you go** (`standards/FEEDBACK-LOOP-v0.1.md`). Every skill logs your corrections as feedback without
  asking, and asks one short question at the end of the run. The meeting review asks how it felt (1-5). The Friday
  digest groups feedback by skill and step and reports patterns, not people.
- **New: `/sc-lessons`**, a chat of its own for lessons learnt. Paste notes or an R&D email; it files them and
  updates the shared registers on SharePoint (`Lessons/registers/`): product limitations and questions we should
  ask. Those go live for everyone straight away; anything that expands what we claim waits for Friday.
- **Meeting card** for "tell us what we need": `sc-requirements/scripts/meeting_card.py` builds a one-page, phone
  friendly card from the new requirements library (banking, multifinance lending, omnichannel service): peers → I'd
  start with → which matter most. Only lines Renzo has approved show (the seed shows as DRAFT until then).
- **Where we win** strip at the top of every build plan: steps from them vs our ideas, D1-D7 shown by step, and the demo bar's required set (D1 live change, D3 AI with a person confirming, track core) ticked or flagged in red. Optional `track` in `build-plan.json`; the builder warns on anything missing.
- `sc-demo-plan`: an "our idea" step stays in the demo even if the customer hasn't answered its question; show it
  after their scenes and open with the question.
- **SC click path that teaches the demo** (`sc-clickpath`). Per step: Open (record, how to find it, its state),
  numbered Click steps with exact labels, You'll see, They said (confirmed words only), Land this (point, KPI,
  differentiator and competitor angle), Say, If they ask (sourced, otherwise "we'll confirm in writing"), Watch out,
  Signed in as. Per use case: a 30-second value story and a bridge to the next. Every step shows whether it's theirs
  or our idea. Practice mode hides the talk track so you recall it. A third tab shows the deal's meeting card. Demo
  logins appear on the SC page (and its phone copy) from SharePoint `Stand-logins/stand-logins.json`; never on the
  customer page. New `second_browser.py` takes screenshots that need two users signed in at once.
- **Each SC:** update the plugin. Add the logins of any stand you demo on to SharePoint
  `Stand-logins/stand-logins.json` yourself (Claude never does). For two-user screenshots, `pip install playwright`
  once.

## 0.17.0 (13 Nov 2026): demo depth, build rules, Bank.AI log, deal dates, custom components
- Build rules (`standards/BUILD-RULES-v0.2.md`): try a browser refresh before any compile or restart and ask the SC
  first; when calls suddenly fail (401/403, a login page instead of JSON), check and refresh the OData token first;
  before a custom component, code, a standard-object or shared-setting change, back up and write a rollback plan (undo
  steps, how to check, the demo's plan B). `sc-setup` adds a short version to the demo toolkit's local notes for
  `creatio-demo-build`.
- New skill `sc-bank-ai-log` (BFSI deals): the customer's requirements in their words, our proposed configuration, fit
  and gaps, written to SharePoint `Bank-AI-Requirements/` for the Bank.AI team. No demo, meeting, commercial,
  competitor or people content (the script refuses it). Hooked into sc-first-meeting, sc-rfp, sc-workshop,
  sc-demo-plan and sc-meeting-review. Backfilled: Pegadaian, Mandiri Sekuritas, Adira Finance (320 lines, 17 gaps);
  Navalo added 13 Nov (10 lines).
- Deal dates on every deal: `deal-dates.json` records the first call (BDR, AE or discovery), when the SC got the
  transcript, and the demo (planned, then done); Claude asks only for missing dates (`sc-guide/scripts/deal_dates.py`).
  The Friday digest reports the medians in `Lessons/stats/deal-timing.md`.
- `sc-first-meeting` (FM v0.5) asks first: **introduction to Creatio, or a detailed demo on their pains?**
  Introduction = the plan as before (light config, ≤ half a day). Detailed = best-practice pains from the pack (tagged
  I) on the understanding slide, a success-criteria email for the AE so the customer ranks them before the meeting,
  and the configuration planned at Full level through `sc-demo-plan` (three questions, build plan, approval). Less than
  3 working days to the meeting → Claude says so and suggests the hero journey only or moving the meeting. `sc-guide`
  asks the same question on a new deal.
- `sc-demo-plan` build plan: a new `custom` screen type draws custom Freedom UI components as wireframes
  (`layout`: `journey` = steps with pain flags, `matrix` = a value × ease board with a ranked list, `scorer` =
  criteria scored 1–3 with a total, `trace` = what they said → requirement → what we built → status). A `record` screen can carry one too (`"custom": {...}`), and `"wide": true` gives a
  step the full width. Custom parts show a dashed purple frame and a "custom" badge. First used on East West Bank.
- Fix: build plan pages now declare UTF-8, so "·", "…" and quotes no longer show as garbled characters.
- New `standards/UI-KIT-STANDARD-v0.3.md`: the rules for custom Freedom UI components in the shared `labUiKit`
  (no-code settings, upgrade-safe, one package), which components exist and where they're proven, and the traps when
  placing them on a page. Three are live on Navalo: Group holdings, Decision checks and Flow timeline (a record's
  journey with who, when and time between steps). Native next-step banners are the pattern for "what do I do now". Demo bar §6 now points to it:
  check the kit before building a new component.
- **Each SC:** after updating, say "run sc-setup" once, so the build rules reach your demo toolkit notes.

## 0.16.1 (12 Nov 2026): faster deck checks
- `sc-deck` and `sc-first-meeting`: Claude still looks at every slide on the first build. After a fix it looks
  again only at the slides it changed, unless the change can affect every slide (template, shared fields, slides added
  or moved, library slides, new builder). Same checks, roughly half the tokens on a typical deck.

## 0.16.0 (12 Nov 2026): Claude tells you about updates
- When you open Claude, the plugin now checks SharePoint. If a newer version is published, Claude tells you and
  gives you the update command. After you update, Claude shows what's new once, and offers any one-off step.
- Runs on Windows and Mac, reads only the synced SharePoint folder, and stays silent when there's nothing new.
- **Each SC: update this once by hand. From now on Claude reminds you.**

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
