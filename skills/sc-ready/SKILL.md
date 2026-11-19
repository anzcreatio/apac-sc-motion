---
name: sc-ready
description: Readiness check before a Creatio APAC customer meeting or demo - quiz the solution consultant from memory on the deal (their pain in their numbers, who signs off, the competitor, the hypothesis, the differentiators that fit, the closing question) plus one past lesson, then the three questions the customer is most likely to ask, the 60-second story without the deck, and only then a short crib sheet aimed at what they missed, ending in a ready / not-ready call. Use when an SC says they are presenting or meeting a customer tomorrow or today, asks "am I ready?", "test me", "quiz me on <deal>", "prep me for the meeting", or wants a morning recheck. Pilot (learning loop) - only for SCs with "ready" in the pilot list.
---

# sc-ready

> **Mac:** run every `python …` command below as `python3 …`.

The SC remembers a deal by recalling it, not by re-reading Claude's summary. So we **test first and teach after**
(`../../standards/LEARNING-LOOP-v0.1.md`, Renzo 18 Nov 2026). Script: `scripts/ready.py` (private log, the SC's PC only).

**Pilot gate:** `python scripts/ready.py pilot --feature ready`. Off → tell the SC it's a pilot and offer a plain
crib sheet instead (step 5 only). On → the steps below.

## Chat

Number and title it as a deal chat (`../../standards/CHAT-TRACKING-v0.2.md`), stage **`Ready`**, topic e.g.
"demo tomorrow". Wrap-up: status done, outcome = the verdict.

## Read the deal (silently, before the first question)

From the deal folder: `01-fm-prep.md` (six answers, hypothesis, meeting plan, closing question), `deck.json`
(agenda goal, hypothesis, components, next steps), the latest `NN-demo-plan.md` and AE brief, meeting reviews,
the pre-build answers (competition), `deal-dates.json` (what and when), `00-deal-start.md` if any. Only what's
there: a question whose answer isn't in the folder is not asked; list it as a **gap** instead (that's a prep gap,
not an SC miss). Never show the SC these files before the quiz.

## Steps

1. **Quiz (5 min, from memory).** Say: "Answer from memory, short is fine, 'don't know' is fine." Ask 5–6 numbered
   questions in one message, picked from what the meeting needs:
   - their main pain **in their own words or numbers** · who signs off and who'll be in the room · the competitor and
     our one line against them · the 3 parts of the hypothesis · the 2 differentiators that fit (D1–D7) · the
     closing question **word for word** · for a demo: the order of scenes and the moment that should land.
   - plus **1 recall question** from `python scripts/ready.py pick --deal <deal>`, asked as a scenario, not read out.
     None due → skip it.
   Mark each: right / partly / missed. Be fair: their words are fine if the meaning is right. A number must be the
   right number. Then `ready.py recall --id <L-id> --ok|--miss` for the recall question.
2. **Likely customer questions (3 min).** The 3 questions this customer is most likely to ask (from the transcript's
   doubts, their industry pack, the competitor, `sc-coach`'s explanation library, AI/data/hosting from the
   governance pack). The SC answers each in one line. Then give the approved answer (one line, plus what not to
   say). Only "can say" lines for AI, data, hosting and security; claims only from the differentiator catalogue.
3. **60-second story.** "Tell me the meeting in 60 seconds, no deck: who they are, what hurts, what we'll show, what
   we'll ask." Typed or dictated. Point out what's missing or out of order (max 3 points), and what was strong.
4. **Score and verdict.** Score = right + ½ partly over the quiz questions. **Ready** = closing question right, main
   pain right, and ≥ 70% overall; otherwise **not ready**, with the 1–2 things to fix tonight. A gap in the folder is
   a fix too (e.g. "no competitor on record: ask the AE"). Save:
   `ready.py quiz --deal <deal> --score N --of M --misses "<q>|<q>" --verdict ready|not-ready`.
5. **Crib sheet (≤ 8 points).** Misses first (with the right answer and where it came from), then the must-say
   lines (closing question word for word, the pain in their numbers), then anything risky to avoid. Nothing they
   already got right unless it's the closing question. Then **up to 2 💡 Learn points**, picked by impact (what
   would hurt most if they didn't know it: a promise we can't keep, a compliance or regulator trap, the wrong buyer,
   a competitor trap), logged with `ready.py learn` (§2 of the standard). The crib sheet goes in chat only, not in
   the deal folder.
6. **Morning recheck (optional).** Offer: "Want a 2-minute recheck in the morning?" If they come back:
   `ready.py misses --deal <deal>`, ask only those again, save with `ready.py quiz ... --recheck`.

End with the one "how did that go?" question (feedback loop).

## Rules

- **Quiz before crib. Always.** Don't summarise the deal first, even if asked "remind me about X" mid-quiz: say
  "answer what you can, the crib sheet is right after."
- Coaching, not grading: plain, warm, no lecture. "Don't know" is a fine answer; it's the point of the check.
- Scores, misses and Learn points stay private (`~/.apac-sc-motion/learn/`). Never in the deal folder, never shown
  to another SC.
- No customer contact, nothing sent.
- The SC was clearly short of time ("5 minutes!") → quiz 3 questions (closing question, main pain, the competitor),
  then the crib sheet. Still test first.
