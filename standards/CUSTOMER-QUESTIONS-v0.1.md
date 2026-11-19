# Customer questions v0.1: question lists a customer answers

**Applies to:** any list of questions we send a customer to answer in writing: RFP clarifications (`sc-rfp`),
workshop pre-work (`sc-workshop`), success-criteria and sizing questions. Customer wording also follows
`WRITING-STYLE-v0.1.md`.
**Built from:** Renzo's edits to the Navalo RFP clarification sheet (19 Nov 2026). Feedback in SharePoint
`Lessons/feedback/2026-11-19-renzo-huruiti-rfp-clarification-sheet.md`.

## 1. Two files, one source

| File | For | Columns |
|---|---|---|
| **Working** (`NN-questions-working-<date>.xlsx`) | The SC, to edit and track | # · Topic · Criterion IDs · Question · What would help us · Why we're asking (internal) · Status · Customer's answer · Dropped? |
| **Customer** (`NN-<Vendor>-clarification-questions-<Customer>-<date>.xlsx`) | The customer | # · Criterion IDs · Question · Customer's answer |

Build both from one JSON with `sc-rfp/scripts/clarify.py`, so cuts and additions renumber themselves. The SC edits the
working file or the JSON, never only the customer file. If the SC does edit the customer file, read it back, learn
from the changes and carry them into the JSON.

## 2. Writing the questions

| Rule | Instead of | Write |
|---|---|---|
| One question per row. Split anything with "and" into rows (1a, 1b) | "Share the weights, and which criteria are gates?" | 1a weights · 1b gates |
| The reason goes inside the question as one short sentence, **only** where it helps them answer | A "why" column | "…? This will help us put the most detail where it matters more to you." |
| Keep it short. Add answer hints only where a vague answer would hurt us (volumes, system names, dates) | A hint on every row | Volumes: "For example users by team, customers, applications a month. Rough numbers are fine." |
| State the assumption we'll use if they don't answer | (silence) | "For now, we assume you'll be choosing all vendors around the same time." |
| Cut what we can safely assume, or what shows our hand | "Should middleware be out of our pricing?" | (assume it, state it in the response) |
| Lean in rather than opt out of optional sections, and ask how it's scored | "Confirm we don't answer B3" | "Would you still like us to answer B3?" + "Will answering it bring our score down?" |
| Ask about what you know is pending | — | "Is this one of the documents pending NDA?" |
| No references to earlier calls, offers or promises. The sheet gets forwarded | "When we caught up on the 16th we talked about…" | The question on its own |
| Promise the outcome, not a walkthrough of the internals | "We'll show exactly what was changed, step by step" | "We'd commit to show you what the platform did to make the change" |
| Never reveal a gap in the reason | "We don't have Australian references, so…" | Ask the rule plainly |
| Put the questions that change the whole response first, and say so in the instructions | — | "Questions 1 to 4 affect how we put the whole response together" |

## 3. The sheet

- Title, the RFP or meeting it belongs to, the date sent, and a one-line "how to use this sheet" that only mentions
  columns the customer can see.
- Answer column shaded, groups banded, header frozen, filters on, A4 landscape, one page wide.
- No internal notes, no evidence tags, no emoji, no "SC check" lines.

## 4. The email that carries it

- In the SC's voice. Read the SC's own sent or edited emails in `Deals/` first (for example
  `firstcape-rh/03-ae-email-sent-to-ayush-2026-11-18.md`) and match their phrases and sign-off.
- Short body when the sheet is attached: thanks, anything they asked us to confirm, "questions attached", which ones
  first, offer a quick call.
- Nothing "as promised" or "as agreed" unless the meeting record shows it (feedback 18 Nov 2026).
