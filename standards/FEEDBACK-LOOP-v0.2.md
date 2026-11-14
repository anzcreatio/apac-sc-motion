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

`<team root>/Lessons/feedback/<yyyy-mm-dd>-<sc-kebab-name>-<short-slug>.md` (one shared folder: feedback about the
skills and Claude is for everyone, §5). It is about the tool, never about how the SC performed: no meeting ratings,
coaching scores or weak quotes in a feedback file.

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

## 5. Who sees what (Renzo, 14 Nov 2026)

Two kinds of feedback, kept apart. **Coaching is for the SC, not about the SC:** the aim is that people stay honest
and keep sharing their recordings, so nothing about how someone performed reaches anyone else unless they choose.

| What | Where | Who sees it |
|---|---|---|
| **About the skills and Claude**: feedback files, registers, lessons, the Friday digest, team lessons | SharePoint `Lessons/` | Everyone (global). The SC's name stays on a feedback file so Renzo can follow up |
| **About the SC's performance**: coaching (scores, weak moments, habits), their own 1-5 rating of a meeting, training results | The SC's own PC only, `~/.apac-sc-motion/coaching/` and `~/.apac-sc-motion/training/` | The SC. Renzo sees only what the SC chooses to share |
| The SC's daily desk brief and workload | The SC's own PC (`~/.apac-sc-motion/desk/`); the desk works only on their own deals | The SC; Renzo for the Friday deal view |
| Friday desk team page | SharePoint `Lessons/desk/weekly/` | Everyone: totals only, no SC named |

**Claude's rules in every skill:**
- The SC is whoever `sc` in `~/.apac-sc-motion.json` says. Never show one SC another SC's coaching, meeting
  ratings, training results, brief or workload; say "That's <name>'s to share: ask them". Don't summarise, count
  or hint. Renzo is no exception for coaching: he sees what the SC shares.
- **Sharing is the SC's choice.** At the end of a coaching run ask once: "Want to share anything with Renzo?
  Nothing / your top 3 habits / the full note." Default nothing; never ask twice. On a yes, Claude writes the note for
  the SC to send him themselves (Teams or email); Claude never sends it and keeps no copy anywhere shared.
- **Team learning only with consent, anonymised.** A habit worth teaching becomes a team lesson only if the SC says
  yes, written with no SC, deal, customer or call named (`Lessons/explaining-it/_proposed/`; Renzo approves Fridays).
- **Recordings** are used only for what the SC asked. Coaching never runs on someone else's recording unless that SC
  asked for it; when Renzo coaches a recording an SC sent him, the result goes back to that SC and Renzo keeps no file.
- No scores per person anywhere: not in the digest, the desk view or a deal folder.

## 6. Changes

| Version | Date | Change | Evidence |
|---|---|---|---|
| v0.1 | 13 Nov 2026 | First version: four sources, one store, registers with the asymmetric rule, Friday grouping by skill and step | Renzo, team walkthrough 13 Nov 2026 |
| v0.2 | 14 Nov 2026 | §5 who sees what: feedback about the skills and Claude is global; the SC's performance (coaching, meeting self-ratings, training results) stays on their own PC and is shared only by their choice; desk briefs private; no per-person scores anywhere | Renzo, 14 Nov 2026 |
