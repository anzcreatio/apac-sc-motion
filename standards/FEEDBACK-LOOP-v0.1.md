# Feedback loop v0.1: how what we learn gets back into the motion

**Why:** what SCs change, how a meeting felt, what a customer pushed back on and what R&D tells us are the best
evidence we have, and most of it gets lost in chats and transcripts (Renzo, 13 Nov 2026). Everything lands in **one
place**, and the Friday digest turns patterns into changes.

## 1. Four ways in, one store

| Source | When | How | Writes |
|---|---|---|---|
| **asked** | At the end of every skill run | **One short question**, tied to what just happened, and the SC can skip it. Examples: "You cut 2 steps from the mock-up: too long, or the wrong steps?" · "How did the meeting feel, 1–5, and what would you change?" | A feedback file |
| **chat** | Whenever the SC corrects, overrides or rejects an output, or adds a rule | Claude logs it **without asking**: what changed, the SC's words, the skill and step | A feedback file |
| **transcript** | `sc-meeting-review` | The customer's reactions (landed, fell flat, questions we couldn't answer) next to the SC's own 1–5 rating | A feedback file + the review |
| **lessons** | Any time, in a chat of its own: `/sc-lessons` | The SC pastes anything: notes, an R&D email, a thought after a meeting. Claude splits it into items and routes each one | Feedback files + the registers (§3) |

Not for practice folders (`Deals/_practice/`): they would distort the digest.

## 2. The feedback file

`<team root>/Lessons/feedback/<yyyy-mm-dd>-<sc-kebab-name>-<short-slug>.md`

```
# <one-line summary>
- SC: <name> · Deal: <account> · Skill + step: <skill, step> · Source: asked / chat / transcript / lessons · Kind: commercial / functional / process / deal · Date: <yyyy-mm-dd>
- What happened: <their words>
- What they'd change: <their words>
- How it felt (1-5): <optional>
- Severity: blocker / annoying / idea
```

Keep their words. One file per item.

## 3. Registers: shared, live, and you can update them

These live on SharePoint at `<team root>/Lessons/registers/`, never in the plugin. Skills read them at run time, so
a new entry works for every SC straight away. Edit them only through `skills/sc-lessons/scripts/registers.py`, which
keeps the JSON valid and the IDs unique.

| Register | Holds | Read by |
|---|---|---|
| `product-limits.json` | What the product can't do (or can't do yet): area, the limitation, the workaround, source (R&D, Support, docs, field), version, status `open` / `fixed`, `fixed_in` | Requirements library (marks lines "check first"), `sc-rfp` fit, `sc-demo-plan`, release-notes digest (closes fixed ones) |
| `discovery-questions.json` | Questions we should have asked: topic (sizing, commercial, technical, process), the question, the signal that says "ask it now", the lesson behind it | `sc-first-meeting` meeting questions, `sc-demo-plan`, the BOM sizing sheet |

**The asymmetric rule (Renzo, 13 Nov 2026):**
- Anything that only makes us **more careful** goes live **straight away**: a product limitation, a question to ask, a gotcha.
- Anything that **expands what we claim** waits for Renzo's Friday approval: a new claim, a proof point, a "can say" line, a requirements library line.

Every entry has an `id`, `source`, `date`, `reported_by`, `status` and, when it replaces an older one, `supersedes`.
Nothing is deleted. A fixed limitation stays, with `status: fixed` and `fixed_in`.

## 4. Fridays (`sc-weekly-lessons`)

- Group the feedback files and new register entries **by skill and step**.
- Propose a change only when the same signal comes from **2+ deals or 2+ SCs** (or one serious failure). Single notes go on the watch list.
- **Report patterns, not people.** The digest never names an SC next to a "how it felt" note or a rating; the files keep the name for one-on-one coaching.
- At most 3 changes a week; Renzo decides.

## 5. Changes

| Version | Date | Change | Evidence |
|---|---|---|---|
| v0.1 | 13 Nov 2026 | First version: four sources, one store, registers with the asymmetric rule, Friday grouping by skill and step | Renzo, team walkthrough 13 Nov 2026 |
