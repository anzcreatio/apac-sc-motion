---
name: sc-meeting-review
description: After a Creatio APAC customer meeting, review it and feed what we learn back into the deal and the motion - compare the deck the SC actually presented with the deck we generated (slide by slide), review the meeting transcript (what landed, what they corrected, questions we couldn't answer, closing outcome), update the deal's living solution summary in deck.json, propose configuration enhancements for the next session, and log lessons. Use when an SC says a meeting happened, shares a meeting transcript or recording notes, asks how the meeting or the deck went, or asks what to change before the next session.
---

# sc-meeting-review

Run per meeting, in the deal folder (`<team root>/Deals/<account>/`). Three parts; do the ones the inputs allow.
Nothing customer-facing is sent from here.

## Part A: deck comparison (needs the presented deck)

1. Find the decks: generated = the `out` of the deal's `deck.json`; presented = the newest other `.pptx` in the deal
   folder. Ask the SC "Is `<file>` the deck you presented?" (one question). If they presented from elsewhere, copy it in
   as `NN-presented-<yyyy-mm-dd>.pptx` first.
2. Run `python scripts/deck_diff.py --deal-dir "<deal folder>"` (or `--generated --presented --spec` explicitly).
   It writes `Lessons/deck-edits/deck-review-<deal>-<date>.md` + `.json` on SharePoint.
3. Read the report and, for the edited and hand-made slides, look at the presented slides (render with
   `../sc-deck/scripts/office_deck.ps1 -Action render`). Classify each change:

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

1. **Scorecard**

   | Check | Result | Evidence (quote, time) |
   |---|---|---|
   | Playback: what they confirmed, corrected, added | | |
   | Hypothesis: each part confirmed / changed / rejected | | |
   | Each demo scene: landed / neutral / fell flat | | |
   | Live change done, and their reaction | | |
   | Questions we couldn't answer (and who owes the answer) | | |
   | Differentiators shown (D-IDs) and any we missed | | |
   | Closing question asked? Answer? Next step with a named person and a date? | | |

2. **Solution summary update:** copy `deck.json` to `deck-<yyyy-mm-dd>.json` (history), then update the `summary`
   parts: confirmed parts stay, corrected parts reworded in their words, new needs added, rejected parts removed,
   shown parts marked `shown: true`. Update `understanding` rows with corrections (now tag **C**). Rebuild with `sc-deck`.
3. **Configuration enhancements for the next session:** a table, Business Studio first, then AI:
   `pain (their words) · enhancement · Freedom UI or custom component (why) · AI part · library module to reuse · hours`.
   Only for pains they confirmed or raised. Check the demo library first.
4. **Commitments:** everything we promised, with owner and date.

## Part C: lessons

Append to `../../lessons/<yyyy-mm-dd>-<deal>.md`: what we'd keep, change or stop, each with evidence and a proposed
change to a skill, standard, pack or template. Don't change the motion here: the weekly lessons run decides, and a
change needs 2+ deals or 2+ SCs (or one serious failure).

End customer-facing drafts with "SC check required before this is used with the customer."
