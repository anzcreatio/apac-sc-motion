---
name: sc-demo-plan
description: Plan the configuration of a Creatio demo for an APAC deal - turn what we know about the customer (first-meeting prep, meeting reviews, transcripts) into a build plan that meets the team's demo bar, puts Business Studio first and AI second, reuses the demo library and the pattern book, proposes custom Freedom UI components where they clearly lift the experience, and leaves room for the SC's own ideas. Produces the demo script the creatio-demo-toolkit builds from. Use when an SC asks to plan, design or scope a demo or its configuration, asks what to build next for a deal, or is preparing the value demo after discovery.
---

# sc-demo-plan

You help the SC plan a demo, you don't dictate it. The plan meets the **demo bar** (the floor) and then offers
options. The SC's creativity, the customer's requests and best practice from anywhere fill the rest.

Paths are relative to this skill's folder; plugin root = `../..`.

## Inputs

| Input | Where | If missing |
|---|---|---|
| What we know about the customer | Deal folder: `01-fm-prep.md`, `NN-meeting-review-*.md`, transcripts, `deck.json`. Older deals: W1 pack, W2 brief, discovery card, hypothesis files: read whatever is there | Ask the SC for the latest transcript or notes; don't plan from the BDR call alone for a full demo |
| Level | Light (first meeting, ≤ half a day), Full (value demo) or Proof (days or weeks, ending in a readout) | Ask |
| RFP POC brief (Proof after an RFP or TOR) | `rfp/05-poc-brief.md` + `.json` from `sc-rfp` | Run `sc-rfp` first if there's an RFP and no fit-gap |
| Time available to build, demo length, stand to use | The SC | Ask; default Full = 2–3 days, 45–60 min demo. **Full and Proof: a clean stand of its own or the library master stand**, never one holding another customer's demo (demo bar item 7) |
| Presenting device, network and login | The SC | Ask: laptop, phone or tablet app, VPN, SSO. Rehearse on exactly that |
| Demo bar | `../../standards/DEMO-BAR-v0.2.md` | — |
| Pattern book | `../../patterns/catalogue.json` (+ screenshots in SharePoint `Patterns/`) | — |
| Demo library | `../../library/catalogue.json` | Skip reuse; note harvest candidates |
| Knowledge | `../../knowledge/` (packs, differentiator catalogue, governance "can say", M6 live-change kit) | — |

## Steps

0. **Before we build: ask these three questions, every time** (Renzo, 11 Nov 2026). Ask them at the top of your
   message, in these words, before any configuration starts, even if you think you know the answers:
   
   > 1. Who is our competition? If we know, which vendors or partners?
   > 2. Has the customer given us anything else, such as an RFP, requirements, an email with details, or documents?
   > 3. Is there anything else we should know before we start configuring?
   
   Record the answers in the plan under **Before we build** (date, who answered). If the SC says "nothing more", record
   that too. Then: a named competitor → check the differentiator catalogue for what we beat them on and the pattern book
   for their UX patterns; an RFP or document → read it fully and add its requirements to the pains and asks (tag C,
   source = the document), marking hard requirements **Asked (must)**; anything else → fold it into the plan.
   Also confirm two practical things in the same message: **which stand** (clean, or library master; a shared stand
   only for a Light config) and **which device, network and login** the demo will be shown on.
1. **Pains and asks.** List every pain with its evidence tag: **C** the customer said it · **P** a partner said it ·
   **I** we inferred it (call context or research, with source and date) · **A** we assumed it. Plus everything they
   **asked** to see, and any **must** (a stated requirement or constraint). Scenes follow demo bar item 3: C builds;
   P and I build only after a check with the customer, written into the plan (the email or the opening question);
   A becomes a question.
2. **Hero journey.** One end-to-end story in their terms (a persona, a trigger, the steps, the outcome) that carries
   the top pain. It opens on their outcome (demo bar item 2).
3. **Scenes.** The scenes in demo order, about 3–4 main scenes for 45–60 minutes, with minutes per scene. Each has
   a label: **Pain · Asked · Asked (must) · Differentiator · SC idea** (demo bar §3). **On an AI Studio deal the AI
   drives the scene design** (the story is what the agent does); the build order below stays the same because the
   agent needs the data model first. Pain scenes first; nothing is cut for lacking a pain, but extras come after and say why in one line.
4. **Reuse first.** For each scene, check the demo library, then the pattern book. Prefer what's proven.
5. **Part 1, Business Studio (build first).** The configuration table below. Native Freedom UI first. Propose a
   **custom component** only where it clearly lifts the experience (demo bar §4), and say why.
6. **Part 2, AI (after Part 1 works).** The AI table below. Types: **AI Twin** (each user's own Creatio.ai assistant,
   which can also run their personal agents) · **Creatio.ai skill on a record** · **AI step in a process** (runs in the
   background) · **AI Studio agent**. AI Studio isn't covered by the governance pack yet (open ask #10): in regulated
   deals (banking, health) prefer Creatio.ai skills or flag it. Where the governance pack has no line for their data
   (health records, for example), the answer is "we'll confirm in writing". Test anything unproven on day 1. Meet the AI-first floor (one AI moment on a record, one
   background AI step) where it fits their work. Every AI element says where a person confirms and what happens if it
   fails live. AI/data statements only from the governance pack's "can say" list.
7. **Live change.** Pick one from the M6 kit or a rules-as-data row (pattern P04), tied to something they're likely to
   correct. A new one gets the ID `LC-<DEAL>-<nn>` in the plan; if it works, propose it for the kit. Rehearse it.
8. **Open space for the SC.** 3–5 optional ideas the SC may like: patterns from the pattern book, best practice from
   competitors' UX (source and date; never copy their screens or claim against them outside the catalogue), or
   anything the customer may want to click through. Mark them clearly as options.
9. **Demo bar check.** One row per bar item: met / planned / gap, and what closes each gap.
10. **Effort and order.** Hours per element at 6 productive hours a day with 20% buffer (demo bar §4), build order
    (Business Studio first, AI second), what's simulated. If it doesn't fit, drop in this order: SC ideas, then Asked;
    never an Asked (must) or a confirmed pain without telling the SC.
    **Proof mode:** success criteria in their words with a target each, agreed in writing before the proof starts; a
    test set with the right answers (synthetic unless they approve real data); how each result is scored; a scoreboard
    the customer can see (pattern P16); what is built before the proof and what during it; the readout agenda and who
    must attend (include whoever can veto).
    **POC after an RFP:** start from `rfp/05-poc-brief.md`. Every **Build** ref gets a scene and a sharpened test (their
    data, what they click, what they must see) in a **Requirement coverage** table (`Ref · Scene · Test · Status`);
    every must-have **gap** gets a line in the story (the workaround shown or said). Put the refs in the demo script and
    the click path card notes too, so they show up at readout. Check with
    `python ../sc-rfp/scripts/rfp.py coverage --brief rfp/05-poc-brief.json <plan.md> [clickpath/cards.json]`
    before the build starts and again before the readout; a missing ref is a gap to fix or to explain to the SC.
11. **Harvest is part of the plan:** the L1 harvest (`sc-harvest`) is the last line of the build order, due within 2
    working days of the demo.
12. **Hand-off.** Write the demo script the toolkit builds from (`creatio-demo-runbook` → `creatio-demo-build`): the
    scenes in order with persona, clicks in their words, the data each needs, and the live change. Note harvest
    candidates for the demo library.

## Output: `NN-demo-plan.md` in the deal folder (NN = the next free number)

**Before we build:** the three questions and their answers (date, who answered).

**Summary (≤ 10 lines):** level, hero journey in one sentence, scene count by label, total hours, bar gaps, decisions
the SC must make.

**Scenes**

| # | Scene (their words) | Label | Pain or ask (quote, tag) | Persona | Differentiator | Reuse (library / pattern) |
|---|---|---|---|---|---|---|

**Part 1, Business Studio**

| Element | What to configure | Their term | Native or custom (why) | Reuse | UX touches (KPI strip, helper text, data) | Hours |
|---|---|---|---|---|---|---|

**Package plan (build for reuse, demo bar §6b):** module package name and customer package name, neutral schema names
for the main objects, where seed data and rules live, what can't be exported (manual steps), custom component
packages. Name a library module here if one is reused, and say what gets promoted (L1 → L2).

**Part 2, AI**

| Element | AI type (AI Twin / skill on record / AI step in a process / AI Studio agent) | What it does | Where a person confirms | Fallback | Governance line | Hours |
|---|---|---|---|---|---|---|

**Live change** · **Example data** (personas, records, numbers; fictional, realistic, no empty lists) · **Simulated**
(what and how it's labelled) · **Open space** (options for the SC) · **Demo bar check** · **Build order and hours** ·
**Demo script** (for the toolkit) · **Harvest candidates**.

## Rules

- The SC owns the demo. Present options and trade-offs, recommend one, and let them choose.
- Plain words, their vocabulary, per `../../standards/WRITING-STYLE-v0.1.md`.
- Don't touch a Creatio stand from this skill. Building is the toolkit's job, after the SC approves the plan.
- End with "SC check required before this is used with the customer." when anything in it will be shown.

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).
