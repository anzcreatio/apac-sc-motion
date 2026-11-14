---
name: sc-rfp
description: Fit-gap an RFP, TOR or requirements list for a Creatio APAC deal - read the customer's spreadsheet or PDF in whatever layout it comes, build one requirements register (their IDs and words, Bahasa kept), split our scope from the bid team's, rate every requirement honestly (standard, configure, AI, Marketplace, integration, custom, partner, roadmap, no) with confidence, evidence, POC tier and effort, recommend bid / bid with conditions / no-bid from the fit % and the big gaps, and check the bid team's compliance answers against the fit-gap. Use when an SC gets an RFP, TOR, tender, requirements matrix or compliance sheet, asks for a fit-gap or a bid/no-bid view, or wants to check a filled compliance sheet before it's submitted.
---

# sc-rfp


> **Mac:** run every `python …` command below as `python3 …` (`sc-setup` records which one works in `~/.apac-sc-motion.json`).
The bid team writes the RFP response. **We give them the fit-gap and a bid / no-bid recommendation**, and, before they
submit, a consistency check of their answers against it (Renzo, 11 Nov 2026). The POC is planned from the same
register with `sc-demo-plan` (proof mode).

Paths are relative to this skill's folder; plugin root = `../..`. Script: `scripts/rfp.py`. Rubric: `FIT-RUBRIC.md`.

## Inputs

| Input | Required | If missing |
|---|---|---|
| The RFP / TOR file(s): xlsx, PDF or Word | Yes | Ask |
| Deal folder `<team root>/Deals/<account>/` (or `<account>-<initials>/`) | Yes | Reuse the account's folder if it exists with any suffix; otherwise create `<kebab-case-account>-<sc>/` by the deal folder rule in `sc-setup`. Files go in `rfp/`, the original as `00-<name>.<ext>` (never edit it) |
| Competition (names), other customer info, the deadline | Ask at the top (the pre-build questions) | Note "unknown" |
| The customer's scoring or weights | If given | Count every requirement equally |

## Steps

1. **Ask first (at the top):** the three pre-build questions (competition, anything else from the customer, anything
   else to know), the submission deadline, and what the customer's own compliance codes mean if the sheet uses codes
   (e.g. `FS/MM/LM/NV/NS`). Don't guess a code's meaning.
2. **Scan:** `python scripts/rfp.py scan rfp/00-<file>.xlsx --out rfp/scan.json`. For a PDF or Word file, extract the
   requirement table into a spreadsheet first (keep their numbering) and scan that.
3. **Map:** write `rfp/map.json` from the scan: per sheet the header row, ID, text, mandatory and answer columns, how
   sections are shown, and **scope** (`ours` = functional, technical, security, architecture; `bid` = commercial,
   legal, licensing, project, people, SLA, support terms). Show the SC the map as a short table (sheet · rows · scope)
   and wait for an OK. Map format:

   ```json
   {"customer": "…", "language": "en|id", "codes": {"standard": "FS", "configure": "FS", "custom": "LM", "no": "NS"},
    "sheets": [{"sheet": "5.1 …", "prefix": "F-", "header_row": 2, "id_col": "A", "text_col": "B", "mo_col": "C",
                "section": {"mode": "prefix_colon | row | col", "col": "…", "id_col": "B", "text_col": "C"},
                "answer_cols": {"compliance": "G", "explanation": "H", "code": "D"}, "extra_cols": {"weight": "…"},
                "scope": "ours | bid", "ours_ids": ["optional: row IDs that are ours when one sheet mixes both"],
                "default_section": "…"}]}
   ```
4. **Register:** `python scripts/rfp.py register rfp/00-<file>.xlsx --map rfp/map.json --out rfp/register.json`.
   Check the counts against the sheet (spot-check the first and last requirement of each sheet).
5. **Rate** every `ours` requirement with `FIT-RUBRIC.md` → `rfp/verdicts.json`. Over ~60 requirements, split into
   batches of about 50 and rate them in parallel (one subagent each, given the rubric, the differentiator catalogue,
   the governance pack and the library catalogue). Translate Bahasa into `english`. Rate blind: don't read any answers
   already in the sheet while rating.
6. **Review:** read every `low` confidence verdict and every must-have gap yourself; fix what's wrong; list the rest
   for the SC to check (product questions go to Creatio product or presales ops).
7. **Build the outputs:**
   `python scripts/rfp.py fitgap --register rfp/register.json --verdicts rfp/verdicts.json --out rfp/01-fit-gap.xlsx --summary rfp/02-bid-no-bid.md --deal "<Customer>"`
   - `01-fit-gap.xlsx`: Fit-gap (one row each, their code proposed), Summary, Bid team (not ours), Questions.
   - `02-bid-no-bid.md`: the recommendation, the numbers, the big gaps. Rule: **Bid** = must-have fit ≥ 90% and no
     must-have we can't do · **Bid with conditions** = 75–90%, or a must-have needing custom or partner work ·
     **No-bid** = under 75%, or a must-have we can't do with no workaround. The SC and AE decide; we recommend.
8. **Win themes and POC brief:** propose 3 win themes (their pains + where the named competitors are weak + our
   differentiators). Then `python scripts/rfp.py poc --register rfp/register.json --verdicts rfp/verdicts.json --out rfp/05-poc-brief.md --deal "<Customer>"`
   (Build lines grouped with draft tests, must-have gaps to handle, Show evidence, questions, low-confidence lines) and
   hand it to `sc-demo-plan` in proof mode. `rfp.py coverage` later checks every Build ref made it into the plan and
   the click path.
9. **Consistency check** (when the bid team shares their filled sheet): copy it in as `rfp/03-bid-team-answers-<date>.xlsx`,
   map its answer columns into a register, then
   `python scripts/rfp.py check --register <that register> --verdicts rfp/verdicts.json --out rfp/04-consistency-<date>.md --xlsx rfp/04-consistency-<date>.xlsx`.
   It lists every line where their answer claims more than we found, says "comply" for something that depends on an
   integration or Marketplace app, or says "comply" while their own explanation mentions integration, custom work or a
   third party. The SC talks it through with the bid team; we never edit their sheet.

## Rules

- **BFSI deal (bank, lender, multi-finance, pawn, securities, insurer):** when this step is done, run `sc-bank-ai-log` to add the customer's requirements and our proposed configuration to the Bank.AI log. Requirements only: nothing about the demo, the meeting, commercials or competitors.
- Honest verdicts. "Can be met" is not "standard". When unsure: the weaker fit, lower confidence, and a question.
- AI, data, hosting, security and residency answers come only from the governance pack's "can say" lines.
- Claims and proof points come only from the differentiator catalogue. No competitor comparisons in the fit-gap.
- Never change the customer's file or the bid team's file. Customer documents stay in the deal folder on SharePoint,
  never in the plugin repo.
- Every output ends with "SC check required before this is used with the customer or the bid team."

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).

**Feedback as you go** (`../../standards/FEEDBACK-LOOP-v0.2.md`): when the SC corrects, overrides or rejects what
you produced, write a feedback file (`Source: chat`, with this skill and step) without asking. At the end of the run,
ask **one** short question about how it went, tied to what just happened, and log the answer (`Source: asked`).
Never in practice folders.
