# Confidential customer terms v0.1

**What it is:** how we keep a customer's confidential terms (their own category names, criteria, internal programme
names, anything they asked us not to share) inside their deal folder, while still harvesting the lessons and patterns
for the team. **Agreed:** Renzo, 16 Nov 2026: "we should not copy the [confidential] names but we still want to
harvest the lessons learnt, but we should remove any confidential type of information and labelling. But we can
replace with generic naming convention."

## 1. The rule

- **The deal folder keeps the original.** Transcripts, preps and decks for that customer may use their terms.
- **Everything shared uses the generic label.** Library modules and READMEs, the demo-library catalogue, feedback
  files, lessons files, registers, `TEAM-LESSONS.md`, the weekly digest, training material, and any deck or page for
  another audience.
- **Never-harvest items are not harvested at all**, not even generically: criteria values, thresholds, scoring
  weights, lists the customer curates (for example their investor list).
- When in doubt, treat it as confidential and ask the SC.

## 2. The file

`<deal>/confidential.json`, kept with `skills/sc-lessons/scripts/confidential.py`:

| Command | What it does |
|---|---|
| `add --deal <d> --term "<their term>" --generic "<label>"` | Lists a term and its generic label |
| `never --deal <d> --item "<described generically>"` | Lists something that must never be harvested |
| `show --deal <d>` | What's listed (prints the generic labels only) |
| `redact --deal <d> --in <file> [--out <file>]` | Replaces every listed term with its generic label |
| `scan --deal <d> <files or folders>` | Exit 1 and lists the hits if a term is still present |
| `scan --all <files or folders>` | Same, against every deal's terms (for team-wide outputs) |

**Generic labels:** describe the role, not the customer: "Archetype A" to "Archetype E", "the customer's curated
investor list", "a priority founder category". Keep the same label for the same term everywhere, so lessons still
read consistently.

## 3. Who does what

| When | Skill | Step |
|---|---|---|
| A transcript, email or SC says "don't share", "confidential", "internal only" | Any skill that reads it (`sc-guide` as-built, `sc-meeting-review`, `sc-first-meeting`) | Propose the terms and generic labels to the SC at the top of the message; on their yes, `confidential.py add` |
| Before writing anything outside the deal folder | `sc-harvest`, `sc-lessons`, `sc-meeting-review` (Lessons/ outputs), `sc-guide` mode C | `redact` the draft, then `scan --deal`. A hit = don't write; fix it first |
| Before the digest or team lessons go out | `sc-weekly-lessons` | `scan --all` over the digest, `TEAM-LESSONS.md` and the week's new feedback files |
| A deck for this customer | `sc-deck` | No change needed. A deck or page for anyone else: `scan --deal` on its `deck.json` first |

`scan` never prints the term itself, so its output is safe to paste into a shared log.

## 4. Changes

| Version | Date | Change | Evidence |
|---|---|---|---|
| v0.1 | 16 Nov 2026 | First version: per-deal terms file, generic labels, never-harvest list, scan before any shared write | A live customer asked that its own founder categories are not shared; the partner's walkthrough transcript in the deal folder named them. Feedback `2026-11-16-renzo-huruiti-confidential-generic-labels.md` |
