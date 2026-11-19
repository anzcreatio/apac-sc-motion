---
name: sc-bank-ai-log
description: Keep the Bank.AI requirements log for a banking or financial services (BFSI) deal - every requirement and pain the customer gives us (RFP, TOR, transcript, workshop, documents) in their words with an English translation, the business area, the configuration we'd propose and how well the product fits, gaps first - written to the SharePoint Bank-AI-Requirements folder so the Bank.AI team can learn what APAC banks need and where the product has gaps. Use on any BFSI deal (bank, lender, multi-finance, pawn, securities, insurer) after a first-meeting prep, an RFP fit-gap, a workshop capture, a meeting with new requirements, or a demo plan; or when asked to update or backfill the Bank.AI log.
---

# sc-bank-ai-log

> **Mac:** run every `python …` command below as `python3 …` (`sc-setup` records which one works in `~/.apac-sc-motion.json`).

The Bank.AI team builds banking features and modules. This log tells them **what APAC banks ask for and where the
product falls short** (Renzo, 13 Nov 2026). It's fed straight into their Claude, so it's structured and plain.

Paths are relative to this skill's folder; plugin root = `../..`. Script: `scripts/bankai.py`.
Output: `<team root>/Bank-AI-Requirements/<deal folder>/log.jsonl` + `README.md`, and `INDEX.md` across all banks.
That folder is shared with the Bank.AI team only; never point them at `Deals`.

## What goes in, what never does

| In | Never in |
|---|---|
| The customer's requirements and pains, **in their words** (Bahasa kept) with an English translation | Demo quality, rehearsal, deck or presentation feedback |
| Where it came from: document and clause, or transcript and minute | Meeting reviews, scorecards, what landed |
| Business area, priority, C/I/A tag | Prices, licences, discounts, commercials, bid strategy, win themes |
| The configuration we'd propose (objects, processes, rules, AI) and the fit (rubric) | Competitor names (the script replaces them with "[vendor]" in customer text) |
| Gaps: custom, partner, roadmap or not supported, with the workaround | People's names (roles only); the bank's name is fine |

## When to run it (BFSI deals only)

A deal is BFSI when the first-meeting prep used the BFSI pack, or the customer is a bank, lender, multi-finance,
pawn, securities or insurance company. Then, after each of these:

| After | Do |
|---|---|
| `sc-rfp` (register + verdicts) or `sc-workshop` (register + verdicts) | `python scripts/bankai.py from-register --deal-config <deal>/bank-ai.json --register <register.json> --verdicts <verdicts.json> --source "<document name>"` |
| `sc-first-meeting`, a transcript, `sc-meeting-review` (requirements only), a customer document | Write the new requirements as lines (format below), then `python scripts/bankai.py add --deal-config <deal>/bank-ai.json --lines <lines.json>` |
| `sc-demo-plan` | Add or update `proposed_configuration` and `fit` on the lines the plan covers (same `id`, via `add`) |
| Any of the above | `python scripts/bankai.py index` |

**Ask the SC before writing** (Renzo, 19 Nov 2026). Draft the lines, then put this at the top of your message, with the
count filled in, and wait for a yes (also as the app's question buttons where the session has them):

> **Bank.AI log:** it records this bank's requirements (their words, our proposed configuration and the fit, gaps first)
> in the shared Bank-AI-Requirements folder, so Creatio's Bank.AI team sees what APAC banks need and where the product
> falls short. No prices, competitors or people's names go in. Write **N lines (G gaps)** now?

Then run `add` and `index`. SCs who don't know the log approve what they can't see; the sentence lets them decide.

First time on a deal, write `<deal>/bank-ai.json`:

```json
{"bank": "Pegadaian", "country": "Indonesia", "segment": "State-owned pawn, gold and lending company",
 "context": "One or two sentences: what they're buying and where the requirements came from.",
 "people": ["names of customer and Creatio people to keep out"], "competitors": ["named vendors"], "area_map": {}}
```

## Lines for `add` (a JSON list)

```json
[{"id": "T1-03", "source_type": "transcript", "source": "Discovery call, 4 Nov 2026, 12:40", "area": "",
  "requirement": "their words", "english": "only if not English", "priority": "must | should | could | unranked",
  "tag": "C", "proposed_configuration": "what we'd configure, product terms are fine", "fit": "configure",
  "confidence": "high", "gap_note": "workaround, only for a gap", "question": ""}]
```

`id`: stable per source (`T1-03` = transcript 1, item 3; `D2-07` = document 2). Leave `area` empty to let the script
choose. Fit and confidence follow `../sc-rfp/FIT-RUBRIC.md`; unrated lines get `"fit": "n/a"` only if they're not a
product question (and are then better left out).

## Rules

- Customer words only in `requirement`; our view only in `proposed_configuration`, `fit`, `gap_note`, `question`.
- The script stops if our fields mention demos, decks, prices, commercials, bids, a competitor or a listed person.
  Fix the line; don't work around the check.
- Honest fits, the same as the fit-gap. Bank.AI acts on the gaps, so a hidden gap is a wasted signal.
- Tell the SC in one line what was added ("Bank.AI log: 12 lines added, 2 gaps").

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).

**Feedback as you go** (`../../standards/FEEDBACK-LOOP-v0.2.md`): when the SC corrects, overrides or rejects what
you produced, write a feedback file (`Source: chat`, with this skill and step) without asking. At the end of the run,
ask **one** short question about how it went, tied to what just happened, and log the answer (`Source: asked`).
Never in practice folders.
