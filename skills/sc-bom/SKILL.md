---
name: sc-bom
description: Work out which Creatio licences and products (SKUs) a Creatio APAC deal needs - a bill of materials (BOM) built from what we know about the customer (deck.json solution summary, demo plan, RFP or workshop register, meeting reviews, AE brief licence answers) - with the candidate Unlimited tier, what's extra to quote, what's still TBC, every commercial and technical gotcha that applies, and the sizing questions to ask next. Internal only, no prices, no users per module; the AE and Deal Desk own the quote. Writes NN-bom.md and an NN-bom.xlsx for Deal Desk. Use when an SC or AE asks which licences, products, SKUs, editions, add-ons or AI packages a deal needs, asks for a BOM or bill of materials, asks what to put in front of Deal Desk, or wants the licence questions for the next meeting.
---

# sc-bom

> **Mac:** run every `python …` command below as `python3 …` (`sc-setup` records which one works in `~/.apac-sc-motion.json`).

The SC says **which** products the solution needs and what can bite us later. The AE and Deal Desk own the price and
the user numbers (Renzo, 13 Nov 2026, log item 74). A good BOM means Deal Desk quotes the right thing first time and
nothing turns up after signature (storage, a connector, a VPN tunnel, an AI package).

Paths are relative to this skill's folder; plugin root = `../..`. Script: `scripts/bom.py`.
Catalogue (SKUs, tiers, gotchas, sizing questions, rules): `../../knowledge/BOM-CATALOGUE-v0.1.json`.

## Hard rules

1. **INTERNAL ONLY.** Never send the BOM, the tier or any line of it to a customer or partner. The customer hears
   "we'll put options together".
2. **No prices and no users per module.** No dollar amounts anywhere; qty only for blocks, GB and environments.
   `bom.py check` refuses both. User numbers the customer gives go to the AE for Deal Desk, not into the BOM.
3. **Unlimited is the default** (since 1 May 2026). Per seat only when the customer can't accept Unlimited, with the
   reason recorded.
4. **The tier is a candidate.** Deal Desk validates it; the CEO approves every Unlimited quote before any number is shared.
5. **Every Yes or TBC has a reason and a tag.** The reason is a requirement, pain or demo scene, in their words, with
   its source. Tags: **C** they said it · **P** a partner said it · **I** we inferred it · **A** we assumed it. A Yes on
   an A is really a TBC: ask.
6. **OPEN items stay open.** The catalogue's `open_items` (AI allowance on Unlimited, Unlimited storage, VPN and
   region SKU names, CRM app editions) are Deal Desk questions. Show them; never pick an answer.

## Inputs

| Input | Where | If missing |
|---|---|---|
| What they need | `deck.json` (`understanding`, `summary`), `01-fm-prep.md`, the latest `*meeting-review*` | Run `sc-first-meeting` first; a BOM from the BDR call alone is all TBC |
| What we'll show or showed | The demo plan's scene table, `build-plan.json` | Fine before a demo: mark scene-driven lines TBC |
| Requirements | `rfp/register.json` + verdicts, or `workshop/register.json` | Skip |
| Licence answers | The AE brief summary the AE sends back ("Licence answers: …"), or what the SC says | Use the sizing questions as the ask |
| Size and structure | Revenue, AUM (BFSI), employees, legal entity, group: from the handoff, prep or research (source + date) | Ask; the tier stays unknown |
| Hosting and AI | `../../knowledge/AI-GOVERNANCE-PACK-LITE-v0.1.md` "can say" lines | — |
| Delivery risk | `../../knowledge/DELIVERY-ASSURANCE-v0.2.md` (decides line V1: Delivery Assurance or No-Code Magic) | — |
| Team gotchas | SharePoint `Lessons/registers/bom-gotchas.json` (read by the script) | Catalogue only |

## Steps

1. **Start or reopen the BOM.** First time: `python scripts/bom.py new "<deal folder>"` writes `<deal>/bom.json`.
   Otherwise open the existing `bom.json` and update it; never start a second one. List what you read in `inputs`
   (file and date).
2. **Deal facts.** Fill `deal_facts` (value, tag, source): customer, legal entity, group, country, hosting region,
   commercial model, revenue and AUM in **USD millions**, employees, existing customer, deployment. Convert other
   currencies with the rate and date in `source`. Then `python scripts/bom.py tier --revenue … --aum … --employees …`
   and say the candidate tier and why in one line.
3. **Walk every SKU** in the catalogue in order and set `needed` Yes / No / TBC with `why` and `tag`. Use each SKU's
   `consider_when`. Name each Marketplace app or connector on M1–M3 (`name`). Think about what's easy to miss:
   - every AI scene shown or planned needs **A1 AI Package**, also on Unlimited; BYO LLM or on-prem AI is **A3 Freedom**;
   - merged or large books → **I3 database** and **I4 file storage** (separate allowances); heavy integration → **I2 blocks**;
   - Creatio cloud reaching on-prem systems → **I7 VPN tunnel**; data residency → **I9**;
   - on-premise deployment → the licence lines here; the servers and storage are `sc-sizing`;
   - brokers, dealers or customers logging in → **U1–U3 portals**; mobile-only field staff → **U4**; approvers → **U5**;
   - partner delivery risk → **V1 Delivery Assurance** (else No-Code Magic).
4. **Gotchas.** For every gotcha that applies (the script works out which from the lines and facts), set `status`
   (Covered · Needs quote · Ask customer · N/A) and `answer`. Do the same for each team gotcha under `team_gotchas`.
5. **Sizing answers.** Record what the customer has answered in `sizing` (answer, tag). Unanswered questions linked to
   a Yes or TBC line become the ask for the next meeting.
6. **Check:** `python scripts/bom.py check <deal>/bom.json`. Fix every ERROR. Before it goes to Deal Desk use
   `--final` (every line decided, every applicable gotcha with a status).
7. **Build:** `python scripts/bom.py build <deal>/bom.json --nn <next number>` writes `NN-bom.md` and `NN-bom.xlsx`
   (template v0.2: Summary for the AE first, then Read me, Deal, SKUs, Gotchas, Sizing questions, Tiers). The Summary
   tab is formulas: it fills in when opened in Excel.
8. **Feed the next meeting.** `python scripts/bom.py questions <deal>/bom.json --max 6` prints the open sizing
   questions as `licence` entries for `ae-brief.json` (`sc-demo-plan` step 13 uses them). When the AE sends the answers
   back, put them in `sizing` and the facts, and rebuild.
9. **Tell the SC** in at most eight lines: candidate tier, the products (Yes), extras to quote, what's TBC, the
   gotchas that need a quote, the questions for next time. Then: "Send the .xlsx to Deal Desk with the user numbers
   from the AE." Ask one short "how did that go?" question and log feedback as usual (`../sc-guide/SKILL.md` mode C).

## When to run it

| Moment | What |
|---|---|
| After `sc-first-meeting` | First pass: mostly TBC, gives the AE the licence questions |
| After the demo plan or build | Lines driven by scenes (AI, portals, connectors) become Yes or No |
| After a meeting review with new facts or answers | Update and rebuild |
| RFP or workshop register rated | Requirements firm up the lines; licensing rows in an RFP stay with the bid team, but the BOM feeds them |
| Before the proposal (`W5-Close.md`) | `check --final`, then send to Deal Desk |

## New gotchas

When a deal teaches us something (Deal Desk corrected a line, a customer hit a limit after signature), log it with
`/sc-lessons`: `python ../sc-lessons/scripts/registers.py add-gotcha --area … --gotcha … --applies-when … --question … --source-ref … --by …`.
It applies to the next BOM straight away (it only makes us more careful). Renzo folds proven ones into the next
catalogue version at the Friday digest.

## Outputs

`<deal>/bom.json` (the source), `<deal>/NN-bom.md`, `<deal>/NN-bom.xlsx`. All internal.
