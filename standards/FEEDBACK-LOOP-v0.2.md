# Feedback loop v0.2: how what we learn gets back into the motion

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

`<team root>/Lessons/feedback/<sc initials>/<yyyy-mm-dd>-<sc-kebab-name>-<short-slug>.md` (one folder per SC, private:
§5). Files from before 14 Nov 2026 sit flat in `Lessons/feedback/`; readers take both.

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

## 5. Who sees what: private per SC (Renzo, 14 Nov 2026)

An SC's own working notes are **theirs and Renzo's** (Renzo leads the team and runs the Friday digest). No SC can
read or ask about another SC's.

| What | Where | Who sees it |
|---|---|---|
| Feedback files | `Lessons/feedback/<sc>/` | The SC and Renzo |
| Coaching | `Lessons/coaching/<sc>/` | The SC and Renzo |
| Daily desk briefs | The SC's own PC only (`~/.apac-sc-motion/desk/`), never SharePoint | The SC |
| Desk ledger, workload, desk health | Commands run only for the SC's own deals | The SC; Renzo for the Friday view (his local folder) |
| Friday digest, team lessons, team desk page | SharePoint `Lessons/` | Everyone: patterns and totals only, no SC named |

**Claude's rule in every skill:** the SC is whoever `sc` in `~/.apac-sc-motion.json` says. Show them only their own
feedback, coaching, briefs, commitments and workload. If they ask about another SC's ("what feedback did Willy give?",
"what's Ferdhi working on?", "show me Willy's brief"), say: "That's <name>'s to share: ask them, or Renzo." Don't
summarise it, count it per person or hint at it. Team patterns come only from the Friday digest, anonymised. Only
when `sc` is `rh` (Renzo) may Claude show another SC's.

**What makes it really private (Renzo does this once):** Claude's rule is a courtesy, not a lock. The files are on a
SharePoint site every SC syncs, and anyone can edit their own config file. On SharePoint, break inheritance on each
`Lessons/feedback/<sc>/` and `Lessons/coaching/<sc>/` folder and give access to that SC and Renzo only. Briefs never
leave the SC's PC, so they need nothing.

## 6. Changes

| Version | Date | Change | Evidence |
|---|---|---|---|
| v0.1 | 13 Nov 2026 | First version: four sources, one store, registers with the asymmetric rule, Friday grouping by skill and step | Renzo, team walkthrough 13 Nov 2026 |
| v0.2 | 14 Nov 2026 | Feedback in one folder per SC; §5 who sees what: feedback, coaching, briefs and workload private to the SC and Renzo; Claude never shows one SC another's | Renzo, 14 Nov 2026 |
