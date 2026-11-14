---
name: sc-requirements
description: After the demo configuration for a Creatio APAC deal, produce a business requirements checklist the customer can paste into their RFP or evaluation - a neutral spreadsheet in their words (Ref, Area, Requirement, Why it matters, Priority, How to verify, vendor response columns, a suggested scoring tab) generated from an internal master that traces every line to what the customer said, the demo scene that showed it, our fit and the differentiator it plays to. Use when an SC has built or shown a demo and wants to shape the customer's requirements or RFP, asks for a requirements checklist or business requirements spreadsheet, or the AE wants something to send after a demo.
---

# sc-requirements

> **Mac:** run every `python …` command below as `python3 …` (`sc-setup` records which one works in `~/.apac-sc-motion.json`).

After the demo is configured, we hand the customer **their requirements, written well**, before anyone else writes them.
A business owner who pastes our checklist into their RFP is asking every vendor to prove what we've already shown
(Renzo, 12 Nov 2026). The AE sends it; the SC writes it.

Paths are relative to this skill's folder; plugin root = `../..`. Script: `scripts/requirements.py`.

## Inputs

| Input | Where |
|---|---|
| What they said | Transcripts, `*meeting-review*`, `deck.json` (`understanding`, `summary`), first-meeting prep |
| What we built and showed | The demo plan's scene table, `clickpath/cards.json` |
| Requirements already rated | `rfp/register.json` + `verdicts.json` or `workshop/register.json` (if there's an RFP or a workshop) |
| Rubric, claims, governance | `../sc-rfp/FIT-RUBRIC.md`, `../../knowledge/DIFFERENTIATOR-CATALOGUE-v0.1.md`, `../../knowledge/AI-GOVERNANCE-PACK-LITE-v0.1.md` |
| Named competitors | The three pre-build questions in the demo plan |

## Steps

1. **Ask first (top of the message):** who receives it (recommend the business owner, not procurement) and whether
   an RFP is already being written (then send it now; if it's out, use `sc-rfp` instead).
2. **Write the master** `NN-requirements-master.json` in the deal folder (format below). 40–80 lines, grouped by area
   in the order of their journey. For each line:
   - **Their words, outcomes not features.** "Area managers see every overdue job by region each morning", never
     "dashboard", never our product terms.
   - **Why it matters** in their terms (the pain or the outcome they named).
   - **Priority:** **Must** only when they said it (tag C) and our fit is high confidence. Otherwise Should or Could.
   - **How to verify:** what a vendor must show. Use "shown live", "an evaluator changes it during the session",
     "on sample data" wherever we can do it: that's where we win.
   - **Internal:** tag C/I/A and source (quote and minute), the demo scene, the register ref, fit and confidence
     (rubric), the differentiator (D1–D7), and `favours` with one line on why it plays to us (leave it empty if it doesn't).
3. **Balance:** most lines are what any good field or service solution needs; about **15–35%** play to our strengths
   (`favours`). More than that reads as vendor-written and gets stripped.
4. **Build:**
   `python scripts/requirements.py build --master NN-requirements-master.json --customer NN-requirements-checklist.xlsx --internal NN-requirements-internal.xlsx`
   It refuses to build if customer text names Creatio terms or a competitor, if a Must isn't C + high confidence, or
   if any line has a fit we'd fail (custom, partner, roadmap, no).
5. **Review with the SC**, then the SC deletes the red DRAFT line on the Read me sheet and the AE sends the customer
   file. **The internal file never goes to the customer.**

## Master format

```json
{"customer": "…", "title": "<Customer>: <area> requirements checklist", "date": "yyyy-mm-dd",
 "competitors": ["names from the pre-build questions, plus the usual ones"],
 "intro": ["2-3 short paragraphs in the customer's terms; no product names"],
 "scoring": [{"criterion": "Fit to the requirements", "weight": 0.40, "what": "…"},
             {"criterion": "Shown live in the evaluation", "weight": 0.25, "what": "…"},
             {"criterion": "Your team can change it without code", "weight": 0.20, "what": "…"},
             {"criterion": "Cost to own over 3 years", "weight": 0.15, "what": "…"}],
 "lines": [{"ref": "BR-01", "area": "…", "requirement": "…", "why": "…", "priority": "Must | Should | Could",
            "verify": "…", "internal": {"tag": "C", "source": "Scott 20:41 (11 Nov)", "scene": "UC1 …",
            "register": "W1-03", "fit": "configure", "confidence": "high", "diff": "D4", "favours": ""}}]}
```

## Outputs

| File | Sheets | Who |
|---|---|---|
| `NN-requirements-checklist.xlsx` | Read me (purpose, how to respond, red DRAFT line), Requirements (vendor response as a drop-down: Standard · Configuration without code · Custom code · Third-party product · Not available), Scoring (suggested weights) | Customer, after the SC check |
| `NN-requirements-internal.xlsx` | Internal (never send): source, scene, fit, differentiator, why it favours us · Summary | SC, AE |

## The requirements library and the meeting card

Customers often want us to tell them what their requirements should be, not be asked "what do you need?" (Renzo,
13 Nov 2026). This skill owns the shared answer: `../../knowledge/requirements-library.json`.

| | |
|---|---|
| **What a line is** | A best-practice requirement in plain words, by industry → journey → stage: why it matters, a KPI (exact unit, sourced), how we show it, fit (`standard` or `configure` only), **proof** (`proven` = shown live on a demo; `standard` = in the product, not yet shown), `recommend_first`, D-point, source |
| **Creatio safe** | Only `standard` / `configure`, high confidence. Never custom, partner or roadmap. A line linked to an open product limitation (`Lessons/registers/product-limits.json`) drops out of the card automatically |
| **Seed** | Banking, multifinance lending, omnichannel customer service (Renzo, 13 Nov 2026) |
| **Who approves** | Renzo, on Friday. Only `approved: true` lines reach the card |

**The meeting card** (one page, phone friendly, internal):
`python scripts/meeting_card.py --industry <banking|multifinance|service> [--journey "<name>"] --deal "<deal folder>"`
→ `<deal>/meeting-card-<industry>.html`. It gives the SC three moves: **peers** ("what we see at organisations like
yours…", 2–3 lines from their stage) → **recommend** ("for you, I'd start with…", the top 3, proven first) →
**ask** ("which of these matter most?"; their ranking goes into the meeting review as C). It also lists open product
limitations under "check first". `sc-first-meeting` and `sc-demo-plan` attach the card to the prep; the SC click path
shows it as a tab; the SC can publish it as a private artifact to read on a phone.

**How it grows** (every proposal waits for Friday; the asymmetric rule in `../../standards/FEEDBACK-LOOP-v0.2.md`):
- After step 2 of this skill: propose master lines that aren't in the library, with customer names stripped out,
  as a feedback file (`Kind: process`, "requirements library proposal") listing the new lines.
- `sc-meeting-review`: lines they picked, ranked or rejected → proposals (change `recommend_first`, reword, retire).
- `sc-harvest`: a line shown on a harvested demo → propose `proof: proven` with `proven_on`.
- Renzo applies approved lines in the plugin (`approved: true`, `added`, `added_by`) and publishes.

## Rules

- Never write a requirement we'd fail. It comes back in their RFP and scores against us.
- No product names, no Creatio terms, no competitor names in anything the customer sees.
- Security, hosting and AI data lines only from the governance pack's "can say" lines (for example AI hosted in
  Australia; not New Zealand until confirmed).
- If the customer later issues an RFP, run `sc-rfp` on it: the consistency check shows which of our lines they kept.
- Customer-facing: SC check required before this is used with the customer.

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).

**Feedback as you go** (`../../standards/FEEDBACK-LOOP-v0.2.md`): when the SC corrects, overrides or rejects what
you produced, write a feedback file (`Source: chat`, with this skill and step) without asking. At the end of the run,
ask **one** short question about how it went, tied to what just happened, and log the answer (`Source: asked`).
Never in practice folders.
