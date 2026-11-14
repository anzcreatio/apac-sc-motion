---
name: sc-workshop
description: Plan, run and capture 2-hour requirements workshops for a Creatio APAC deal (the Australian path, where there is no RFP) - one journey per workshop, starting from a draft journey the customer corrects, with pre-work so the room is spent on stages, roles, rules, pains, outcomes and AI moments. Turns the workshop transcript into the same requirements register sc-rfp uses (fit-gap, effort, POC brief) plus a solution model in Creatio terms (objects, fields, stages, roles, rules, systems, channels, AI moments, example data, KPIs) that sc-demo-plan and the demo toolkit build from, a follow-up email for what's still open, and a playback document for the customer to sign off. Use when an SC is planning or has just run a discovery or requirements workshop, says "workshop", wants to capture requirements from a session, or needs the playback for a customer.
---

# sc-workshop


> **Mac:** run every `python …` command below as `python3 …` (`sc-setup` records which one works in `~/.apac-sc-motion.json`).
Australia doesn't send us an RFP: we run workshops and write the requirements ourselves (Renzo, 12 Nov 2026). That's
an advantage: the playback the customer signs off often becomes their evaluation criteria. Do it well and in their words.

**Shape (fixed):** 2 hours per workshop, **one journey per workshop**, after the first meeting or demo. The SC
facilitates, the AE scribes, Teams records (the transcript is how Claude captures, so recording isn't optional).
Three journeys = three workshops. Never squeeze two journeys into one session: it turns into a feature list.

Plugin root = `../..` from this skill's folder. Script: `scripts/workshop.py`; rating engine: `../sc-rfp/`
(`FIT-RUBRIC.md`, `scripts/rfp.py`). **Run the commands from the deal folder** (`workshop/…` paths are relative to it),
calling the scripts by their full path. On Windows, set `PYTHONIOENCODING=utf-8` before printing spreadsheet contents.

## Files (deal folder `<team root>/Deals/<account>/workshop/`)

No deal folder yet → create `<kebab-case-account>-<sc>/` by the deal folder rule in `sc-setup` (reuse the account's
folder if it exists with any suffix).

| File | Made in step | Who sees it |
|---|---|---|
| `wN-00-prework-email.md` | 1 | Customer (via the AE), SC check |
| `wN-01-draft-journey.md` | 1 | SC, and on screen in the room |
| `wN-02-transcript-<yyyy-mm-dd>.md` | 3 | Internal |
| `register.json` (all workshops, refs `W1-01`, `W2-01`…) | 3 | Internal |
| `solution-model.json` → `solution-model.md` | 3 | Internal: `sc-demo-plan` and the toolkit build from it |
| `wN-03-follow-up-email.md` | 4 | Customer, SC check |
| `verdicts.json`, `fit-gap.xlsx`, `gaps-and-effort.md`, `poc-brief.md/.json` | 5 | Internal |
| `playback-<yyyy-mm-dd>.docx` | 6 | Customer, after the SC check, for sign-off |

## Steps

### 1. Before the workshop (a week out)

0. **Learn from past deals** (`../sc-lessons/SKILL.md` "Learn from past deals"): run
   `python ../sc-lessons/scripts/learn_from_deals.py brief --stage workshop --deal "<deal folder>" --pains "<their top pains>"`.
   Use what fits (questions we should ask, what landed in past sessions, after-meeting lessons)
   in the draft journey, the agenda and the pre-work email, and list it in an **Applied from past deals** section (one line each: what we're doing
   differently and the lesson id or deal it came from). Then log it: `learn_from_deals.py applied --deal ... --stage workshop
   --item "<id>: <what we did>"`.
1. **Pick the journey and persona** with the SC, from the deal's prep, meeting reviews and `deck.json`. One journey.
2. **Pre-work email** from `PREWORK-EMAIL.md`: what to send (the spreadsheets, forms and reports they use for this
   journey today; a system list; who does what; monthly volumes) and who must be in the room (the person who does the
   work, their manager, whoever owns the outcome; IT optional). About 20 minutes of their time.
3. **Draft journey** from `DRAFT-JOURNEY.md`: 6–8 steps, each with who, the thing and its status, the system or
   channel, the likely pain, and the five Creatio prompts. Sources: the industry pack journeys
   (`../../knowledge/`), the first-meeting prep and reviews, anything they've sent. **Every line is tagged I or A
   until the room confirms it.** Map each thing to a standard Creatio object now (the toolkit's
   `Creatio-object-model.xlsx` in `creatio-demo-runbook/shared/context-library/`, or the banking one for FinServ) so
   the SC knows which words to listen for.
4. Agenda: `AGENDA-120.md`, unchanged unless the SC has a reason.

### 2. In the room (the SC runs it; this skill isn't running)

The agenda and the capture sheet (`CAPTURE-SHEET.md`) are the SC's and AE's guide. The SC's question is "what's wrong
with this?", not "is this right?": people nod through a draft.

### 3. Capture (same day, from the transcript)

Save the transcript as `wN-02-transcript-<date>.md`. Then write two things from it:

**a. Requirements** into `register.json` (append; keep earlier workshops' rows). One row per requirement, in their
words, with who said it and the minute:

```json
{"source": "workshop", "kind": "workshop", "customer": "…", "language": "en", "codes": null, "built": "yyyy-mm-dd",
 "requirements": [{"rid": "W1-01", "sheet": "Workshop 1: <journey>", "src_id": "00:34:10", "section": "<journey step>",
   "text": "<their words, or a close paraphrase marked ~>", "mandatory": true, "weight": null, "scope": "ours",
   "answer": {}, "extra": {"speaker": "<name, role>", "tag": "C", "priority": "must | should | could | unconfirmed",
   "pain": "<the pain behind it, their words>", "model_refs": ["obj:Job", "rule:approval-limit"]}}]}
```

- `mandatory`: `true` only for what the room voted must in the playback block, `false` for should or could, `null`
  if nobody ranked it (`priority: "unconfirmed"`). Most lines end up unranked after workshop 1, and that's normal: the
  fit-gap reports unranked gaps separately and the playback asks the customer to rank them.
- `tag`: C (someone in the room said or confirmed it) · I (we inferred it, it wasn't contradicted) · A (assumed).
  Draft lines nobody confirmed stay I.
- Commercial, legal or project asks (price, contract, go-live date) are `scope: "bid"`, `priority: "unconfirmed"`,
  tagged C with the speaker: noted, not rated. **AI, data, hosting and security questions are ours** (rated, usually
  Tell), answered from the governance pack.
- **Write requirements as outcomes, not features**: "Area managers see every overdue job by region each morning",
  not "dashboard". The feature is the verdict's job.

**b. Solution model** into `solution-model.json` (merge across workshops). Their world in Creatio terms: what
`sc-demo-plan` Part 1 and Part 2, the example data, the home page, and the toolkit runbook's name check need.

```json
{"customer": "…", "updated": "yyyy-mm-dd",
 "meta":       {"workshop": 1, "date": "2026-11-10", "date_text": "Tuesday 10 November", "journey": "reactive jobs",
                "contact": "<first name for the email>", "from": "<AE name>",
                "journeys": {"Workshop 1: <journey>": ["<step 1>", "<step 2>", "…"]},
                "next": {"date": "2026-11-24", "date_text": "Tuesday 24 November", "journey": "…"}},
 "outcomes":   [{"id": "out:first-time-fix", "measure": "…", "baseline": "…", "target": "…", "owner": "…", "tag": "C", "src": "W1 00:12"}],
 "objects":    [{"id": "obj:Job", "their_word": "Job", "kind": "transaction | master", "creatio": "Case | Order | Lead | … | new",
                 "schema": "UsrSite (only for new)", "fields": ["…"], "volume": "…/month, or a count for master data", "tag": "C", "src": "…"}],
 "stages":     [{"id": "stg:Job", "object": "obj:Job", "stages": ["Logged", "…", "Closed", "Cancelled"], "end_states": ["Closed", "Cancelled"],
                 "who_moves": {"Logged": "…"}, "branches": false, "note": "required when branches is true", "tag": "C", "src": "…"}],
 "roles":      [{"id": "role:dispatcher", "name": "…", "does": "…", "approves": "… above $5,000", "count": 12, "tag": "C", "src": "…"}],
 "rules":      [{"id": "rule:approval-limit", "rule": "…", "value": "$5,000", "disputed": true, "tag": "C", "src": "…"}],
 "systems":    [{"id": "sys:SAP", "name": "…", "owns": "…", "direction": "in | out | both", "frequency": "…", "tag": "C", "src": "…"}],
 "channels":   [{"id": "chn:mobile", "step": "…", "channel": "phone app | email | SMS | web | portal", "where": "on site, no signal", "tag": "C", "src": "…"}],
 "ai_moments": [{"id": "ai:job-summary", "task": "…", "today": "…", "who_confirms": "…", "data": "…", "tag": "I", "src": "…"}],
 "example_data": [{"id": "ex:typical-job", "what": "… (who, by when)", "status": "received | asked | none"}],
 "open":       [{"about": "rule:approval-limit", "ask": "What's the limit for after-hours jobs?", "to": "<their person, or us>"}]}
```

- `creatio`: the standard object it maps to (check the object model first), or `new` with a neutral schema name in
  mind. Their word is the caption (demo bar §6b).
- `branches: true` when a record can go two ways at once: stages can't do that (one stage column, no gateways), so
  it needs a process. Say so in the model.
- A rule the room argued about (`disputed: true`) is the live-change candidate.
- Anything said but not answered goes in `open`, with the question in plain words and who it's for. Our own
  actions (a written answer we owe them) are `"to": "us"`: listed as ours, never asked in the email. Don't fill a field
  with "to confirm" to dodge the check: leave it empty and let the `open` item carry the question (the check won't ask
  twice).
- `example_data` they promised is `asked` (with who and by when): the email lists it under "what you said you'd send".

### 4. Check the model and draft the follow-up

```
python scripts/workshop.py check --model workshop/solution-model.json --register workshop/register.json --md workshop/solution-model.md --followup workshop/wN-03-follow-up-email.md --deal "<Customer>"
```

It renders the model, lists every gap (an object with no Creatio mapping or fields, stages with nobody moving them,
a role with no count, a rule with no value, an outcome with no baseline, target or owner, a system with no direction,
an AI moment with nobody confirming, no example data, a requirement with no source minute or tag, a register ref
pointing at a model id that doesn't exist) and writes the follow-up email from the gaps and `open`. Fix what the
transcript does answer; the rest goes in the email. Exit code 1 while there are gaps (that's normal before the email).
Then **edit the email**: it's a draft. Keep it to the questions that block the next build (about 10); the rest wait
for the next workshop. Questions are grouped by the person they're for.

### 5. Rate, fit-gap and brief (the `sc-rfp` engine)

Rate every `ours` requirement with `../sc-rfp/FIT-RUBRIC.md` → `workshop/verdicts.json` (blind batches as in `sc-rfp`
step 5 when there are more than ~60). Then:

```
python ../sc-rfp/scripts/rfp.py validate --register workshop/register.json
python ../sc-rfp/scripts/rfp.py fitgap --register workshop/register.json --verdicts workshop/verdicts.json --out workshop/fit-gap.xlsx --summary workshop/gaps-and-effort.md --deal "<Customer>"
python ../sc-rfp/scripts/rfp.py poc --register workshop/register.json --verdicts workshop/verdicts.json --out workshop/poc-brief.md --deal "<Customer>"
```

On a workshop register there's **no bid / no-bid**: we wrote the requirements, so the fit % runs high and means little.
The summary is "gaps and effort": the gaps we must handle honestly and the effort beyond standard, before the proposal.

### 6. Playback for sign-off (after the SC check)

```
python scripts/workshop.py playback --model workshop/solution-model.json --register workshop/register.json --out workshop/playback-<date>.docx --deal "<Customer>"
```

Their outcomes, the journey as they described it, the requirements by priority in their words (no fit, no Creatio
feature names, no internal tags), the open questions, and a sign-off line. It's the document the customer may turn
into tender criteria, so it's in their words, never ours.

### 7. Between workshops: the playback build

Workshop N+1 opens on journey N, built. Before any configuration: **the three pre-build questions** (competition with
names; anything else from the customer; anything else to know), then `sc-demo-plan` at **Light** level from
`solution-model.md` and the register (one journey, about a day), on a **clean stand set up with the package plan**,
so it grows into the Full demo. Requirements tagged C build straight away; I and A ones are the opening questions of
the next workshop.

## Rules

- **BFSI deal (bank, lender, multi-finance, pawn, securities, insurer):** when this step is done, run `sc-bank-ai-log` to add the customer's requirements and our proposed configuration to the Bank.AI log. Requirements only: nothing about the demo, the meeting, commercials or competitors.
- One journey per 2-hour workshop. If the customer offers 2 hours for everything, do one journey well and ask for
  the next session.
- Their words in the register, the model captions and the playback. Our product words only in verdicts.
- Nothing in the draft journey counts as confirmed until the room confirms it.
- Claims only from the differentiator catalogue; AI, data, hosting and security answers only from the governance
  pack's "can say" lines.
- Never touch a Creatio stand from this skill.
- Every customer-facing output (pre-work email, follow-up email, playback) ends with "SC check required before this
  is used with the customer."

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).

**Feedback as you go** (`../../standards/FEEDBACK-LOOP-v0.2.md`): when the SC corrects, overrides or rejects what
you produced, write a feedback file (`Source: chat`, with this skill and step) without asking. At the end of the run,
ask **one** short question about how it went, tied to what just happened, and log the answer (`Source: asked`).
Never in practice folders.
