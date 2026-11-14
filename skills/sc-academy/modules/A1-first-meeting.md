# A1. First meeting pack and deck

**Path P1 · 60 min · no stand · Skills:** `sc-first-meeting`, `sc-deck`

## Why it matters

The first meeting decides whether there's a demo at all. The skill turns a BDR call into the standard deck and a
light-configuration brief in under an hour, but only if you feed it the right inputs and challenge what it infers.
What you learn here: how the evidence tags work, what the "demo depth" question changes, and how `deck.json` becomes
slides you can fix without PowerPoint surgery.

## Lab

1. **Copy the input:** Claude copies `fixtures/kestrel-bdr-call.md` into your practice folder as
   `00-bdr-transcript-2026-10-21.md`.
2. **Run `sc-first-meeting`** with deal folder = **your practice folder** (say it explicitly) and the meeting a week
   away. Answer its questions as the SC. Demo depth: **"introduction"**. Competition: ServiceNow, a Salesforce partner.
3. **Read the prep** (`01-fm-prep.md`): find the six-question coverage score and one line tagged **I** (inferred).
   Ask yourself: would Greg agree? If not, correct it and let the skill update the file.
4. **Build the deck** with `sc-deck` from `deck.json`, render it to PNG, and look at every slide.
5. **Make one change through `deck.json`**, not PowerPoint: e.g. reword the hypothesis to lead with "know a P1 will
   breach before it does" (Greg's own words). Rebuild.
6. **Compare** with the real first-meeting notes in `tests/workshop/sample-fictional/01-fm-prep.md`: what did the
   kit get right, what did you have to change?

## Check (pass criteria)

- [ ] `01-fm-prep.md`, `deck.json` and the `.pptx` exist in the practice folder; the deck built with no warnings.
- [ ] The hypothesis slide quotes Greg's P1 ask (C) and nothing on it is a claim outside the differentiator catalogue.
- [ ] The deck's last line/notes carry "SC check required before this is used with the customer."
- [ ] The SC can explain C / P / I / A and which ones may build a scene straight away (only C).

## Traps

- **Not saying the deal folder**: the skill may write into a real deal. Always name the practice folder.
- **Treating the meeting as tomorrow** makes the skill skip the configuration brief.
- **Hand-editing the .pptx** loses the change on the next build. Change `deck.json`, rebuild.
- **Claims:** differentiators only from the catalogue, AI/security answers only from the governance pack's "can say"
  lines. "We'll confirm in writing" is a good answer.
- **No meeting review, Bank.AI log or harvest on a practice folder**: they would pollute the team's digest.
