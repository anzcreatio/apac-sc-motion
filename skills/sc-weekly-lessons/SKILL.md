---
name: sc-weekly-lessons
description: Run the APAC SC team's weekly lessons digest - gather the week's evidence (presented-deck comparisons, meeting reviews, first-meeting coverage scores, demo plans, lessons files, inbox and pattern intake, library harvests, customer recaps waiting, SC feedback and onboarding progress) and propose at most three changes to the motion (skills, standards, packs, templates, library), each backed by two or more deals or SCs, for Renzo to approve; then apply only what he approves and publish. Use on Fridays, when Renzo asks for the weekly digest or lessons, asks what should change in the motion, or asks how the team is tracking.
---

# sc-weekly-lessons


> **Mac:** run every `python …` command below as `python3 …` (`sc-setup` records which one works in `~/.apac-sc-motion.json`).
The motion improves every week, by evidence, with Renzo deciding (agreed 11 Nov 2026). Fifteen minutes of his time.

Paths are relative to this skill's folder; plugin root = `../..`.

## Steps

0. **Deal timing:** `python ../sc-guide/scripts/deal_dates.py stats` → `Lessons/stats/deal-timing.md` (medians: first call → SC notified → demo). Put the three medians and the deals missing a date in the digest.
1. **Collect:** `python scripts/collect_week.py` (default: last 7 days) → `Lessons/weekly/<yyyy-Www>-evidence.json`
   on SharePoint. Read it, then read the files it lists (deck reviews, meeting reviews, demo plans, new transcripts,
   lessons files, open inbox items).
1b. **Feedback and registers** (`../../standards/FEEDBACK-LOOP-v0.1.md`): read every feedback file and every new
   register entry the collector lists. **Group them by skill and step** (and by Source: asked / chat / transcript /
   lessons). New product limitations and discovery questions are already live: list them under "New this week" so
   Renzo sees them, and flag any that should become a rule. Practice folders never count.
   **Explanations library** (`explanations.json`): list every `proposed` entry for Renzo's yes or no; on yes run
   `registers.py approve-explanation --id E-00N --by "Renzo Huruiti"`, on no `retire-explanation` with his reason.
   **Coaching** (`Lessons/coaching/`, private): count habits across the week's files and report them anonymised
   ("4 calls: the answer came after the explanation"). Never name the SC or quote them in the digest. A habit seen on
   2+ calls becomes a proposed lesson for `Lessons/explaining-it/EXPLAINING-IT-LESSONS.md` (do, don't, drill; no SC,
   customer or call named; Renzo approves).
   **Team lessons** (`Lessons/TEAM-LESSONS.md`): every approved change and every watch-list signal that reaches 2+
   deals or SCs becomes or updates a lesson there, generalised: no SC, deal or customer named, no quotes. Bump its
   version and add a Changes row, then rebuild the easy-read page: `python scripts/team_lessons_page.py` (writes
   `Lessons/TEAM-LESSONS.html`) and, on Renzo's PC, republish the team Artifact
   (https://claude.ai/artifact/NGdcrEhPXZvyx1vhpy1Ji6) from `team_lessons_page.py --fragment --out <scratch file>`.
   On Renzo's PC, refresh his per-SC view: `python ../sc-coach/scripts/coach_board.py`.
1c. **Training** (`../sc-academy/SKILL.md` modes U and W): `python ../sc-academy/scripts/academy.py refresh` (marks
   course modules stale when a toolkit or plugin SKILL.md changed, drafts updates in `Lessons/training/_drafts/`),
   fill each draft's "Proposed edits", then `python ../sc-academy/scripts/academy.py weekly`. Put its "Decisions for
   you" (stale modules, modules not yet approved, skills no module teaches) in the digest's questions, and where
   trainees get stuck under the watch list. Training feedback files (`Source: training`) are about the course, not a
   deal: group them by module, and they don't count towards the 2-deal rule for motion changes. Course changes
   don't use the 3-proposal cap: apply each only on Renzo's yes (`academy.py stamp --by "Renzo Huruiti"`).
   Same for the customer course: `python ../sc-academy/scripts/academy.py --course ../sc-customer-academy/course.json
   refresh`, then `python ../sc-customer-academy/scripts/customer_academy.py tips` (feedback `Source:
   customer-training`, by module and role; accounts named, participants never).
2. **Find patterns, not anecdotes.** For each candidate change: what happened, on which deals or with which SCs,
   and what it cost or gained. Group the same signal across deals.
3. **Propose at most 3 changes**, ranked by impact. Each needs **evidence from 2+ deals or 2+ SCs**, or one serious
   failure (a customer saw something they shouldn't, a demo broke live, a wrong claim). For each: the change in one
   line, the evidence, the exact file and edit, the effort, and the risk if we don't.
4. **Watch list:** signals from one deal only. Carry them forward; promote when a second deal shows the same.
5. **Measures** (one table, trend against last week's digest where there is one):

   | Measure | Source |
   |---|---|
   | Share of each presented deck that came from the kit | deck reviews |
   | Six-question coverage per new deal (n / 6) | first-meeting preps |
   | Demos harvested to L1 within 2 working days | library catalogue vs builds |
   | Customer recaps waiting for SC approval | click path overlays |
   | Inbox and pattern items waiting | `_inbox`, `Patterns/_inbox` |
   | Proposals approved / applied last week | last digest |

6. **Write `Lessons/weekly/<yyyy-Www>.md`** (SharePoint, the team reads it). Questions first: the proposals to
   approve (numbered), then anything else waiting on Renzo. Then measures, proposals in detail, watch list, and
   housekeeping (drafts to approve, harvests due, inbox). Plain words (`../../standards/WRITING-STYLE-v0.1.md`).
7. **Ask Renzo** which proposals to apply (at the top of your message).
8. **Apply only what's approved:** edit the files, bump the version in the file name when a standard or pack
   changes materially, update `../../CHANGELOG.md` and the plugin version, commit, `publish.ps1`, then tell the SCs to
   update. Record "Applied" or "Declined (why)" against each proposal in the digest.

## Rules

- Never change the motion without Renzo's yes. The digest proposes; he decides.
- Three proposals at most. If there are more, pick the three with the most evidence and impact; the rest go on the
  watch list.
- Evidence means files: a deck review, a transcript quote with time, a meeting review, a lessons entry. Not memory.
- **Patterns, not people.** Never put an SC's name next to a "how it felt" note or a rating in the digest; the
  feedback files keep the name for one-on-one coaching.
- Customer names stay in the deal folders; the digest names deals by account, never quotes customer data beyond
  what's needed.

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is
none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).
