---
name: sc-desk
description: An APAC solution consultant's work desk, so deals never stall on our side - keeps each deal's commitments ledger (what, owner, due, source, status; captured from meeting reviews, next-steps slides, AE briefs and follow-up drafts), spots stalls (no activity for 7 days, an overdue commitment, a demo under 3 days away with no approved build plan, a harvest overdue, an approved recap not sent, no next meeting booked), writes the daily brief (top 5 actions, today's meetings and prep, a follow-up draft for each stalled deal), the Friday desk view (each SC's deals by health, quality trend, tips) and a load check. Reads Outlook calendar and sent mail read-only when the Microsoft 365 connector is on. Use when an SC asks "what's on today", "what's on my plate", "what am I waiting on", says "done: <something>" or "add: <something>", asks whether a deal is stalled or their week is overloaded, after a meeting review, or on the 8 am scheduled run.
---

# sc-desk

> **Mac:** run every `python …` command below as `python3 …` (`sc-setup` records which one works in `~/.apac-sc-motion.json`).

The SC's task desk: what we promised, what's slipping, what to do today. Agreed with Renzo 14 Nov 2026.

**This is an SC task desk, not a second CRM.** Never record pipeline stage, forecast, probability or deal value, and
never ask for them. If the SC mentions one ("it's at proposal now", "it's worth 400k"), say once: "That belongs in
the AE's CRM; please ask <AE> to update it." The desk's only deal-level state is **active / parked / closed** for our
own work, and "how close to a decision" is worked out fresh from the folder each run (never saved).

Script: `python scripts/desk.py <command>` (paths relative to this skill; team root from `~/.apac-sc-motion.json`;
`sc` initials from the same file). Ledger: `<deal>/commitments.json`. Briefs: on the SC's own PC only,
`~/.apac-sc-motion/desk/<date>-brief.md`. Weekly (Renzo): team totals in `Lessons/desk/weekly/<yyyy-Www>.md`, the
per-SC view in his local `SC-Desk` folder.

**Private per SC** (Renzo, 14 Nov 2026; `../../standards/FEEDBACK-LOOP-v0.2.md` §5): the desk is the SC's own. Work
only on the deals of the SC in `~/.apac-sc-motion.json`; the script refuses another SC's deal, brief, ledger or
workload. If an SC asks about another SC's work ("what's Willy working on?", "is Ferdhi busy?", "show me Renzo's
brief"), say "That's <name>'s to share: ask them, or Renzo", and don't summarise, count or hint at it. Only Renzo (`rh`,
team lead) may look across SCs, and he sets who owns a deal (`owner`). Deal folders themselves stay team-readable
(one folder per account, hand-overs, onboarding): the desk just never surfaces another SC's deals.

## Pick the mode

| The SC says | Mode |
|---|---|
| "what's on today", "my day", "what's on my plate", the 8 am scheduled run | **A. Daily brief** |
| "done: <what>", "sent the recap", "booked the next session for the 20th" | **B. Update the ledger** |
| "add: <what> for <deal>, <owner>, <date>", or a meeting review just finished | **B** / **C. Capture** |
| "is <deal> stalled?", "what am I waiting on?" | `desk.py scan --deal <deal>` or `scan`, answer in a short table |
| "am I overloaded?", "can I take this demo?" | **D. Load check** |
| Friday, with `sc-weekly-lessons` | **E. Weekly view** |
| "connect my calendar / Outlook" | **F. Outlook (read-only)** |

## A. Daily brief

1. **Outlook first, if connected** (mode F): pull today's and the next 7 days' calendar into a scratch JSON, and
   check sent mail since the last brief for each active deal (record what you find with `touch`).
2. Run `python scripts/desk.py brief [--calendar <scratch json>]` (written to the SC's own PC, never SharePoint). Add `--preview` until the SC's deals have a
   ledger: it shows the commitments it **would** capture from meeting reviews (marked "preview", nothing written).
3. Show it in chat, **questions first** (the brief's own Questions section, then any of yours). Then the top 5
   actions table, today's meetings with prep gaps, the follow-up drafts, the open commitments. Keep the SC's words.
4. **Follow-up drafts:** the script writes a starting draft per stalled deal (at most 3, addressed to the AE so they
   can forward or adapt it). Rework each in plain words (`../../standards/WRITING-STYLE-v0.1.md`): short, one ask,
   their names, what we owe and what they owe. No "SC check" warning line. **Never send mail, never save a draft into Outlook, never book a meeting.** The SC or the AE sends it.
5. Offer the one action you'd do first, and do it on their yes (e.g. run `sc-harvest`, finish the AE brief).

The brief ranks actions by deadline and how close the deal is to the customer's decision: a demo under 3 days with no
approved plan, meeting prep gaps for the next 2 working days, our overdue commitments, an approved recap not sent, a
harvest overdue, commitments due in 2 working days, what the customer owes us, then idle deals and missing next
meetings. Deals idle for 3+ weeks with nothing booked are asked about ("still live, or park it?"), not drafted for.

## B. Update the ledger

| SC says | Run |
|---|---|
| "done: send the slides" | `desk.py done --match "send the slides"` (more than one match: show them, ask which, rerun with `--deal --id`) |
| "drop that, they said no" | `desk.py drop --deal <deal> --id C-00N --note "<their words>"` |
| "add: pricing options for EWB, Deszantara, Friday" | `desk.py add --deal east-west-bank-rh --what "Pricing options" --owner "Deszantara" --due-text "Friday" --source chat` (or `--due yyyy-mm-dd`) |
| "booked the next session for 20 Nov" | `desk.py meeting --deal <deal> --date 2026-11-20 --what "Working session"` |
| "sent the recap" (or Outlook shows it sent) | `desk.py touch --deal <deal> --what "Recap sent by Andrew" --recap-sent` |
| "park Suntory until late Jan" | Ask the date ("which day should I bring it back?"), then `desk.py status --deal suntory-oceania --set parked --until 2027-01-20` |
| "these deals are mine" | `desk.py owner --deal <deal> --sc rh` per deal (only folders made before 12 Nov 2026 lack the suffix) |

Due dates: the script reads only clear ones ("this week", "next week", "Fri", "20 Nov", ISO). "Late January",
"before the break", "RFP + 3 days" stay **no date**, and the brief asks the SC for one. Never invent a date.
`side` is **us** when one of our people (SCs, the deal's AE, Creatio) owns it, even jointly; else **them**.

## C. Capture

After `sc-meeting-review` writes its Commitments table (and whenever the SC asks):

1. `python scripts/desk.py capture --deal <deal>`: a numbered dry run of new candidates from the meeting reviews'
   **Commitments** tables, the deck's **next steps** actions, the AE brief's next step and promises ("we'll…") in
   follow-up drafts. Already-captured items are skipped.
2. Show the list and ask **one** question at the top: "Which of these did we actually agree? (default: all from the
   review; next-steps slide and AE brief lines only if they agreed)". Fix owners and dates in their words.
3. `desk.py capture --deal <deal> --apply --pick 1,2,4`, then `add` for anything missing. If the review names the
   next meeting with a date, run `meeting` too.

Other skills write through the same commands: `sc-meeting-review` (Commitments), `sc-demo-plan` (`build_ae_brief.py`
next step: capture after the meeting, not before) and follow-up emails from `sc-workshop`.

## D. Load check

`python scripts/desk.py load [--week 2026-W47] [--calendar <json>]`. Counts the week's demos, customer meetings,
build hours left (approval-pack items not yet logged done in `build/build-log.jsonl`, spread over the weeks to the
demo) and our commitments due. Limits (in `desk.py`, `LOAD`): 3 demos, 8 customer meetings, 24 build hours, 2 demos on
one day, 8 commitments due. Over a limit: suggest what to move (build work first; never a customer session within 2
working days) and who could take build items over (the SC with the lightest week). Suggestions only: the SC and AE
decide, and anything to the customer goes through the AE. Run it before saying yes to a new demo date too.

## E. Weekly view (Fridays, inside `sc-weekly-lessons` step 0b)

Renzo only (the script refuses anyone else). `python scripts/desk.py week` writes the **team page**
`Lessons/desk/weekly/<week>.md` (+ `.json` for next week's trend) with totals only, no SC or deal named, and the
**per-SC view** to his local `%USERPROFILE%\SC-Desk\desk-<week>.md` (`--private-out` to change it):

- **Each SC's deals by health** (private view): red (our commitment overdue, demo close with no approved plan, harvest overdue),
  amber (anything else stalled), green, parked. Plus each SC's load for the coming week. The team page shows only
  the team's count per colour.
- **Quality trend (team):** demo bar items met or planned in the latest plans, harvests within 2 working days,
  approved answers added to the explanations library, deal timing medians from `deal-dates.json`. No coaching
  scores: coaching stays on each SC's PC (`../../standards/FEEDBACK-LOOP-v0.2.md` §5).
- **One or two tips**, from this week's most common stall.


## F. Outlook (Microsoft 365 connector, read-only)

Renzo said yes to Outlook calendar and mail (14 Nov 2026). The connector is optional: without it the desk runs from
the deal folders.

- **Check:** are the Microsoft 365 tools (`outlook_calendar_search`, `outlook_email_search`) in this session? If not
  and the SC wants it, suggest the connector (`suggest_connectors`, keyword "calendar"); they connect it themselves.
- **Calendar:** search today to 7 days ahead. Save to a scratch file as a JSON list of `{subject, start, end,
  attendees, location}` (names, not email addresses, where you can) and pass `--calendar`. The script links an event
  to a deal by the customer's name and shows only deal meetings; personal items are counted, never listed.
- **Sent mail:** for each active deal, search the SC's sent items since the last brief for the customer's name or
  the AE plus "recap", "follow up", "slides". For each real hit, `touch` the deal with one line ("Recap sent to
  Scott, 13 Nov"); add `--recap-sent` when the recap went. Don't copy mail bodies into the ledger or the brief.
- **Never** send, reply, forward, draft in Outlook, accept or create meetings, or read mail unrelated to a deal.

## Scheduled daily brief (8 am, each SC's own PC)

Offered by `sc-setup` (step 4); Renzo's is set up. Create it with the scheduled-tasks tool, only after showing the
SC their first brief and getting a yes: task id `sc-desk-daily-brief`, cron `0 8 * * 1-5` (local time, weekdays),
prompt:

> Run the apac-sc-motion skill sc-desk, mode A (daily brief) for SC `<initials>`. If the Microsoft 365 connector is
> available, read today's and the next 7 days' Outlook calendar and the sent mail since yesterday, read-only, as the
> skill's mode F says; otherwise use the deal folders only. The brief stays on this PC (`~/.apac-sc-motion/desk/`).
> Put the questions at the top, then the top 5 actions, today's meetings and the follow-up drafts. Never send mail,
> never draft in Outlook, never change a deal folder except through desk.py's own commands, and don't capture new
> commitments without the SC: list them as preview.

The task runs while the Claude app is open; if the PC is off at 8, it runs at the next launch.

## Rules

- **Not a CRM** (top of this file). No stage, forecast, value or probability anywhere.
- **Nothing is sent.** Drafts carry no "SC check" warning line; the SC reads them before they go.
- The ledger is the SC's: capture is a dry run until the SC picks what was agreed. Never close a commitment the SC
  didn't confirm, except a recap or follow-up Outlook shows as sent (say so in the brief).
- Only `commitments.json` is written in a deal folder; everything else the desk reads.
- **Private per SC** (top of this file): never show one SC another SC's brief, commitments, stalls or workload.
- Never in practice folders (`Deals/_practice/`).

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is
none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).

**Feedback as you go** (`../../standards/FEEDBACK-LOOP-v0.2.md`): when the SC corrects a ranking, a draft or a
stall ("that's not stalled, they're on leave"), write a feedback file (`Source: chat`, skill `sc-desk` + mode)
without asking. After a brief, ask **one** short question ("Was the top 5 right today?") and log the answer
(`Source: asked`).
