---
name: sc-meeting-review
description: After a Creatio APAC customer meeting, review it and feed what we learn back into the deal and the motion - compare the deck the SC actually presented with the deck we generated (slide by slide), review the meeting transcript (what landed, what they corrected, questions we couldn't answer, closing outcome), update the deal's living solution summary in deck.json, propose configuration enhancements for the next session, and log lessons. Use when an SC says a meeting happened, shares a meeting transcript or recording notes, asks how the meeting or the deck went, or asks what to change before the next session.
---

# sc-meeting-review


> **Mac:** run every `python …` command below as `python3 …` (`sc-setup` records which one works in `~/.apac-sc-motion.json`).
Run per meeting, in the deal folder (`<team root>/Deals/<account>/`). Three parts; do the ones the inputs allow.
Nothing customer-facing is sent from here.

## Part A: deck comparison (needs the presented deck)

1. Find the decks: generated = the `out` of the deal's `deck.json`; presented = the newest other `.pptx` in the deal
   folder. Ask the SC "Is `<file>` the deck you presented?" (one question). If they presented from elsewhere, copy it in
   as `NN-presented-<yyyy-mm-dd>.pptx` first.
2. Run `python scripts/deck_diff.py --deal-dir "<deal folder>"` (or `--generated --presented --spec` explicitly).
   It writes `Lessons/deck-edits/deck-review-<deal>-<date>.md` + `.json` on SharePoint.
3. Read the report and, for the edited and hand-made slides, look at the presented slides (render with
   `python ../sc-deck/scripts/render_deck.py <pptx> <dir>`). Classify each change:

   | Kind | Example | Goes to |
   |---|---|---|
   | Deal-specific | A customer's term, a corrected number | The deal's `deck.json` (so the next build has it) |
   | Wording pattern | Titles shortened, quotes removed | Lesson candidate for the deck standard / `sc-first-meeting` |
   | Structure | A slide type added, moved or dropped | Lesson candidate for the standard's slide order |
   | New layout | A hand-made slide the builder can't make | Candidate slide type (`sc-deck`) |
   | Library | Corporate slides added by hand | Check they're in the Slide-library catalogue |

4. Update the deal's `deck.json` with the deal-specific changes, so the presented deck becomes the source.

## Part B: meeting transcript review (needs the transcript)

Save it as `NN-meeting-transcript-<yyyy-mm-dd>.md`. Then write `NN-meeting-review-<yyyy-mm-dd>.md`:

0. **Deal dates:** if this meeting was the demo, record it as done (`python ../sc-guide/scripts/deal_dates.py set --field demo --date <date> --status done`); if the demo moved, set the new date.
1. **Scorecard**

   | Check | Result | Evidence (quote, time) |
   |---|---|---|
   | Playback: what they confirmed, corrected, added | | |
   | Hypothesis: each part confirmed / changed / rejected | | |
   | Each demo scene: landed / neutral / fell flat | | |
   | Live change done, and their reaction | | |
   | Questions we couldn't answer (and who owes the answer) | | |
   | Delivery worries (partner, implementation risk, cost blowouts)? If yes, propose the Delivery Assurance line for next time (`../../knowledge/DELIVERY-ASSURANCE-v0.2.md` §5) | | |
   | Differentiators shown (D-IDs) and any we missed | | |
   | **Today's goal** (agenda) asked again at the close, in the same words? Answer: fits / not yet / no | | |
   | If **not yet**: which part falls short and what it would need to do, **in their exact words** | | |
   | Next step with a named person and a date? | | |

2. **Solution summary update:** copy `deck.json` to `deck-<yyyy-mm-dd>.json` (history), then update the `summary`
   parts: confirmed parts stay, corrected parts reworded in their words, new needs added, rejected parts removed,
   shown parts marked `shown: true`. Update `understanding` rows with corrections (now tag **C**). Rebuild with `sc-deck`.
3. **Configuration enhancements for the next session:** a table, Business Studio first, then AI:
   `pain (their words) · enhancement · Freedom UI or custom component (why) · AI part · library module to reuse · hours`.
   **A "not yet" answer to today's goal comes first** (it's the next session's first scene, tagged C, in their
   words). Then pains they confirmed or raised, then anything they asked to see. Check the demo library and the pattern book
   first; for a bigger next demo, hand over to `sc-demo-plan`.
4. **What landed:** for each scene, the pattern it used (pattern book ID) and the reaction. Patterns that land on 2+
   deals are candidates to build once as a demo library module.
5. **Commitments:** everything we promised, and what they promised, as a `## 5. Commitments` table (What · Owner ·
   When), with a real date where one was said. Then put them on the SC's desk (`../sc-desk/SKILL.md` mode C):
   `python ../sc-desk/scripts/desk.py capture --deal "<deal folder>"`, ask which were agreed, `--apply --pick …`; if
   the next meeting has a date, `desk.py meeting --deal … --date … --what …`.
5b. **Meeting card:** if the SC used it, which lines they picked, ranked or rejected (their words, tag C). Feed the
   ranking into the solution summary, and propose library changes per `sc-requirements` ("How it grows").
6. **Library:** is the L1 harvest done (`library/catalogue.json` has this deal)? If not, and the demo was more than
   2 working days ago, say so first and offer to run `sc-harvest`.
7. **Better answers (sc-coach):** if the SC running this review presented the meeting, offer `../sc-coach/SKILL.md`
   mode D. Their coaching stays on their own PC; the review gets only "Better answers to their questions" (the
   customer's question, our better answer). Never coach another SC's part of the meeting.

## Part C: lessons

Ask the SC first, in one line at the top: **"What would you change next time?"** What they'd change about the
deck, demo or skills goes in a feedback file (`Source: transcript`, `../../standards/FEEDBACK-LOOP-v0.2.md`). How they
felt they did is theirs: if they give a rating, it goes only in their private coaching note, never the review or a
feedback file.

Append to `../../lessons/<yyyy-mm-dd>-<deal>.md`: what we'd keep, change or stop, each with evidence and a proposed
change to a skill, standard, pack or template. Don't change the motion here: the weekly lessons run decides, and a
change needs 2+ deals or 2+ SCs (or one serious failure).

End customer-facing drafts with "SC check required before this is used with the customer."

**BFSI deal:** new requirements or pains the customer stated in this meeting go to `sc-bank-ai-log` (`add`): their words and our proposed configuration only, never the scorecard, the deck comparison or the lessons.

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).

**Feedback as you go** (`../../standards/FEEDBACK-LOOP-v0.2.md`): when the SC corrects, overrides or rejects what
you produced, write a feedback file (`Source: chat`, with this skill and step) without asking. At the end of the run,
ask **one** short question about how it went, tied to what just happened, and log the answer (`Source: asked`).
Never in practice folders.
