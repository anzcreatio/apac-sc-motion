---
name: sc-coach
description: Coach a Creatio APAC solution consultant to explain Creatio in plain, confident, customer-ready words - review a meeting transcript for every moment the SC explained a feature or answered a question (plain words, no hedging that plants doubt, approved claims only, no new doubts opened, length), rewrite the weak ones as a customer-ready line and a dead-simple analogy, give the top three habits to work on, answer "how do I explain X?" in one line, 30 seconds and deeper with what not to say and the likely follow-up, and keep the team's shared library of approved explanations. Use when an SC asks how they explained something, asks for coaching on a call, asks how to explain or answer a question about Creatio, says an answer came out wrong or too long, or when sc-meeting-review runs on a transcript.
---

# sc-coach

> **Mac:** run every `python …` command below as `python3 …`.

The goal: every SC explains Creatio so a customer can't misread it, with nothing that plants doubt, and the team gives
**one consistent answer** to the same question.

**Coaching is for the SC, not about the SC** (Renzo, 14 Nov 2026; `../../standards/FEEDBACK-LOOP-v0.2.md` §5). It stays
on the SC's own PC, and they choose what, if anything, Renzo sees. The first time an SC uses the coach, say so in two
lines: "This is for you, not about you. It stays on your PC unless you share it." Never show one SC another SC's
coaching, and never coach a recording someone else passed along unless the SC on it asked. The coach gets better only through approved changes (the library and
the standards), never by changing itself.

**Read first:** `../../standards/WRITING-STYLE-v0.1.md` (spoken lines, §4) · `../../knowledge/DIFFERENTIATOR-CATALOGUE-v0.1.md`
(the only source of claims) · `../../knowledge/AI-GOVERNANCE-PACK-LITE-v0.1.md` (AI, data, hosting and security: **only**
its "can say" lines) · the explanations library (below) · the team lessons page
`<team root>/Lessons/explaining-it/EXPLAINING-IT-LESSONS.md` (use its lesson numbers in the habits when one fits).

## Modes

| The SC says | Mode |
|---|---|
| shares a transcript, "coach me on this call", "how did I explain…" | **A. Review a transcript** |
| "how do I explain X", "what do I say when they ask Y" | **B. How do I explain X** |
| "too long", "a customer wouldn't say that", rejects or edits a rewrite | **C. Learn from feedback** (also inside A and B) |
| called by `sc-meeting-review` Part B | **D. Short coaching section** |

## The explanations library (shared, SharePoint)

`<team root>/Lessons/registers/explanations.json`, edited **only** through `../sc-lessons/scripts/registers.py`:

```
python ../sc-lessons/scripts/registers.py list --register explanations
python ../sc-lessons/scripts/registers.py add-explanation --topic "..." --question "..." --one-liner "..." --thirty "..." \
   [--deeper "..."] [--analogy "..."] [--dont-say "..."] [--follow-up "..."] [--follow-up-answer "..."] \
   [--claims D1,D3] [--audience business|it|exec] [--source-ref "<deal> <date> <mm:ss>"] [--deal <account>] \
   --by "<SC name>" [--supersedes E-00N]
```

- **Use approved entries first, word for word** (status `approved`). Say which ID you used.
- A `proposed` entry may be shown, marked **DRAFT, not yet the team answer**.
- A new good answer (one the SC liked, or a rewrite that worked) is **proposed, never added silently**: tell the SC
  "I'll propose this for the library", add it with `add-explanation` (it lands as `proposed`), and Renzo approves on
  Friday with `approve-explanation` (`sc-weekly-lessons`). An improved version of an approved one uses `--supersedes`;
  the old one stays the team answer until the new one is approved.
- An entry may claim only catalogue IDs (`--claims D1,D3`). AI, data, hosting or security wording must be a governance
  pack "can say" line, or the entry isn't proposed.

## Scoring (modes A and D)

Score every moment on six checks, each **ok / weak / fail**. **Overall = the worst check.**

| Check | Fail looks like | Why it matters |
|---|---|---|
| **Answered it** | The question asked isn't answered, or the yes/no comes after minutes of context, or a misread by the customer ("so it only works with X") is left standing | They leave with the wrong answer, or none |
| **Plain words** | Product or IT words to a business audience without a picture: low-code, Freedom UI, object, DCM, MCP, LLM, orchestration, package, configure, instance | The customer stops listening or nods without understanding |
| **Confidence** | Hedges that plant doubt: "I think", "should be able to", "in theory", "maybe", "probably", "if I'm not mistaken", "to be honest" | A hedge about the product reads as "it might not". (A hedge about *their* business, "correct me if I'm wrong", is fine.) |
| **Approved claims** | A claim not in the catalogue, any AI/data/hosting/security line outside the "can say" lines, an absolute ("always", "100%", "anything", "never") | Over-claims come back in the RFP and the POC |
| **Opens doubts** | Volunteering a limit, a workaround or "that's a roadmap thing" unasked; knocking or naming a competitor's strength (show, don't argue); "it depends" with no follow-through; another customer's details or numbers; idioms that jar ("massage your data") | New questions we then have to close |
| **Length** | Over about 90 seconds spoken (~180 words) for one point; the answer arrives after the explanation | They remember the first and last sentence |

**Where a fact may come from:**

| Kind of statement | Allowed source | Otherwise |
|---|---|---|
| Why Creatio wins (differentiators, proof points, customer stories) | The catalogue only, tagged D1-D7 | Don't say it |
| AI, data, hosting, security, privacy, credit decisions | The governance pack's "can say" lines only, word for word (in-country hosting only where the pack names the country) | "I'll confirm in writing" |
| Plain product facts (the iPad app, offline, roles, a menu) | Shown on screen in this call, or Creatio's official docs or corporate slides (name which) | "I'll confirm" |
| Another customer's project | Only what the catalogue publishes about them | Leave it out |

**Order of the fixes:** over-claims and governance breaches first (one is enough to hurt a deal), then answers to
the customer's own questions, then habits.

**Other speakers:** don't score the AE or partner, but if they over-claim and the SC lets it stand, add an unscored
note ("Left standing: …, the clean line is …").

Not every long turn is a problem: a planned demo walk-through can run long if each point lands. Score what the
customer heard, not the transcript's grammar (speech-to-text errors and fillers are not the SC's fault; only call out
fillers when they bury the answer).

**Honest beats confident.** If the honest answer is "not out of the box" or "I'll confirm", the rewrite keeps it, said
cleanly once with the next step ("We'll confirm with R&D by Friday"). Never coach an SC into a claim we can't back.
Check `Lessons/registers/product-limits.json` before writing a rewrite that touches a known limit (if the register
doesn't exist yet, say so in the file and carry on).

## A. Review a transcript

1. **Who is coached:** the SC running this session, on their own meeting. If the transcript has other SCs, coach
   only the one who asked; the others aren't scored. **Renzo coaching an SC's recording** (only when that SC sent it
   and asked): the coaching note is written for that SC to read, Renzo passes it on, and no copy is kept on his PC.
2. **First pass:** `python scripts/coach_scan.py --transcript "<file>" --speaker "<SC full name>" [--speaker "<2nd SC>"] --json "<scratch>/scan.json"`.
   It lists every turn of 40+ words, or any answer to a question (`Q`, with the question), with hedges, jargon,
   vendor words, absolutes and length flagged, plus per-line timestamps. It is a sieve, not the score: read the
   transcript around each moment and look for questions it missed. A Teams copy has one time per turn: times inside
   a long turn are estimates, written `~mm:ss`.
3. **Pick the moments that matter:** every answer to a customer question, every explanation of a feature or of
   Creatio itself. Skip small talk, logistics and the agenda. For long monologues, split by point.
4. **Score each** on the six checks. Write the coaching file (below). For each **weak or fail** moment:
   - **Quote** (verbatim, shortest piece that shows it) and the **minute** (`mm:ss`).
   - **Why it's weak**: one line, naming the check.
   - **Customer-ready:** what to say instead, spoken, the length it should be, answer first. Use the library entry if
     one is approved (cite its ID).
   - **Dead simple:** the same point with an everyday analogy a 12-year-old would get (e.g. "like adding a column to a
     spreadsheet, except the whole team's screens update").
5. **Strong moments too:** list the 2-3 best, with why they worked. They are library candidates.
6. **Top three habits:** patterns across the call, each with how often it happened, one example minute and the drill
   (e.g. "Answer first: say the yes/no in the first sentence, then the why. 7 of 12 answers buried it.").
7. **Library:** list a proposal for each question that came up with no approved entry, and ask the SC once, at the
   top: "Propose these N for the team library?" Add the ones they agree to (`add-explanation`, lands as proposed).
   Hold any whose wording isn't backed (see the sources table). Questions the SC couldn't answer go to the meeting
   review, not here.

### Where the coaching goes: the SC's own PC (Renzo, 14 Nov 2026)

Write the coaching note to `~/.apac-sc-motion/coaching/<yyyy-mm-dd>-<deal>-coaching.md` on the SC's own PC (create the
folder). **Never** on SharePoint, OneDrive, in the deal folder or in a feedback file. No scores per person go anywhere
else: not the digest, the desk or the meeting review.

**At the end of the run, ask once** (in the questions at the top): "Want to share anything with Renzo? Nothing / your
top 3 habits / the full note." Default nothing; don't ask again in the same chat. On a yes, write the part they chose
as a short message for them to send Renzo themselves (Teams or email). Claude never sends it.

**Team learning, with consent:** when a habit or a strong moment would help everyone, ask: "OK to add an anonymised
version to the team lessons?" On yes, write a do / don't / drill with no SC, deal, customer or call named to
`<team root>/Lessons/explaining-it/_proposed/<yyyy-mm-dd>-<slug>.md`; Renzo approves on Friday into
`Lessons/explaining-it/EXPLAINING-IT-LESSONS.md`. Library proposals (below) are about the answer, not the person, and
need no extra consent.

File layout:

```
# Coaching: <SC> · <deal> · <meeting date>
Source: <transcript path> · Moments scored: N · Private to <SC> (shared only by their choice)

## Scorecard
| # | mm:ss | Topic | Answered | Plain | Confident | Claims | Doubts | Length | Overall |

## Top three habits
1. ...

## The moments to fix
### <n>. <topic> (<mm:ss>)
> "<quote>"
- Why: ...
- Customer-ready: "..."
- Dead simple: "..."
- Library: E-00N used / proposed / none

## What worked (keep doing)

## Left standing (other speakers, unscored)

## Library proposals
```

## B. How do I explain X

1. Check the library. An **approved** entry → give it as is (cite the ID), adapted only to the audience if asked.
2. Otherwise draft:

| Part | Rule |
|---|---|
| **One-liner** | ≤ 20 words, answer first, plain words |
| **30 seconds** | ~70 words spoken: the answer, one example from their world, what it means for them |
| **Deeper** | for the IT person: how it works, still no slogans, claims from the catalogue only |
| **Dead simple** | the everyday analogy |
| **Don't say** | the words or claims that cause trouble here, and why (jargon, over-claim, governance "don't say yet") |
| **Likely follow-up** | the question they ask next, and its answer (one-liner) |

3. Tag every claim with its D-ID; AI/data/hosting/security lines quote the governance pack's "can say" words.
4. Ask: "Want me to propose this for the team library?" On yes, `add-explanation` (lands as proposed).

## C. Learn from feedback

When the SC says "too long", "a customer wouldn't say that", "that's wrong", edits a rewrite, or rejects one:

1. Fix the answer for them now.
2. Log a feedback file **without asking** (`../../standards/FEEDBACK-LOOP-v0.2.md` §2): `Source: chat`,
   `Skill + step: sc-coach, <mode/step>`, their words about the coach, what changed. It's shared, so it's about the
   coach only: never their score, a weak quote or the customer.
3. If it touches a library entry, propose the fix (`add-explanation --supersedes E-00N`). If it is about how the coach
   writes (length, tone, analogies), propose the style change in the feedback file ("What they'd change") for the
   Friday digest. **Don't change this skill or the standards yourself**: the digest decides (2+ SCs or deals).

At the end of every run, ask **one** short question tied to what happened ("Were the dead-simple versions too
childish, or about right?") and log the answer (`Source: asked`). Never in practice folders (`Deals/_practice/`):
coach there, but log nothing.

## D. Short coaching section (from sc-meeting-review)

Only when the SC running the review is the SC who presented (never on another SC's meeting). Run steps A1-A4, then:
- Write the full coaching note on the SC's own PC (as above) and ask the sharing question once.
- Return to the meeting review **only** `## Better answers to their questions`: the 2 best customer-ready answers to
  questions the customer asked (their question, our better answer), useful for the deal. **No habits, scores, weak
  quotes or a path to the coaching note**: the review sits in the deal folder, which every SC can read.

## Talking to the SC

Questions at the **top** of every message, numbered, before any summary ("No questions" if none). Recommend, don't
list options. Plain Australian English, tables, short lines. Be direct about weak answers and specific about the fix:
this is coaching, not marking. No "SC check" warning line on any output (rule since 17 Nov 2026).
