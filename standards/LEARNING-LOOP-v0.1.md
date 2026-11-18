# Learning loop v0.1: Claude makes the SC sharper, not dependent

Agreed with Renzo 18 Nov 2026 (log §4). **Pilot: on only for SCs whose `~/.apac-sc-motion.json` has
`"pilot": ["call-it-first", "ready"]`** (Renzo first, 2 weeks). Check with
`python <plugin>/skills/sc-ready/scripts/ready.py pilot`; off → skip every step in this file, change nothing.

Why (evidence, so the rules make sense):

| Finding | So we |
|---|---|
| People stop checking automation that is usually right (automation complacency, Parasuraman & Manzey 2010) | Ask the SC for their own call before Claude's, and flag runs of skips |
| Making an answer yourself, and recalling it, makes it stick; re-reading barely does (generation effect, Slamecka & Graf 1978; testing effect, Roediger & Karpicke 2006) | Quiz before the crib sheet, never the reverse |
| Testing before studying helps even when you get it wrong (pretesting, Richland et al. 2009) | The readiness quiz comes first, the points after |
| The first answer you see frames everything after it (anchoring) | Show the SC facts (quotes) before Claude's interpretation |
| Experts learn fastest from worked examples of reasoning (Sweller) | 💡 Learn points: Claude's rule, its evidence, the habit |
| Spaced recall beats one-off review | One past Learn point comes back in each readiness quiz |

Not the goal: making SCs analyse everything. Friction only where the SC's own judgement is the skill (discovery read,
hypothesis, what to demo, closing question). Formatting, building and arithmetic stay fully delegated.

## 1. Call it first (`sc-first-meeting` step 1b, `sc-demo-plan` step 1b)

1. Claude shows **facts only**: the six answers (or the pains list) as quotes with who said it and when, plus the
   coverage score. No hypothesis, no ranking, no demo idea yet. In the same message as the step's existing
   questions (demo depth, the three pre-build questions), so there is still one stop.
2. The SC writes **3 lines** (about 2 minutes). First meeting: top 3 pains · the hypothesis in one line · the one
   thing they'd show. Demo plan: the 3 pains to demo · the hero journey in one line · the moment that should land.
   The SC was on the call → they skip the quotes and just write the 3 lines.
3. Save it before Claude does its own work: `ready.py call --deal <deal> --stage fm|demo-plan --text "<3 lines>"`.
   "Skip" is allowed: `ready.py call ... --skip` (logged; 3 skips in a row and `ready.py pilot` says so: mention it once).
4. Claude does the step as normal, then adds **Your call vs mine**: a table (theirs · mine · same/different) and,
   for each difference, why, with the evidence. Then up to 2 💡 Learn points (§2). Agreement is said plainly: when
   the SC was right and Claude's first read wasn't, say that too.
5. Log the comparison: `ready.py call --deal <deal> --stage ... --match <0-3>` (how many of the 3 lines matched).

## 2. 💡 Learn points

Shown with the 💡 mark (`CHAT-FORMAT-v0.2`). **At most 2 per output.** Pick by **impact**: first the point that
would cost the most if the SC didn't know it (a risk to the deal, a promise we can't keep, a compliance or
regulator trap, the wrong buyer, a competitor trap), then the one that most changes what we show or say. Never
one just to fill the slot: zero is fine.

Triggers: the SC's call missed something Claude used · a fact the SC may not know · a non-obvious reasoning move.

Three lines, every time:

> 💡 **Learn:** <the rule, reusable on the next deal, not a fact about this one>
> **Evidence:** <quote / source, who, when, C/I/A tag>
> **Next time:** <the habit: what to look for or do>

Log each one: `ready.py learn --deal <deal> --rule "..." --evidence "..." --next "..." [--risk high]`. If it is
about the motion rather than the SC, offer (don't do) a feedback file in `Lessons/feedback/`.

## 3. Readiness check (`sc-ready`)

The SC says "presenting tomorrow, am I ready?". Quiz first (5–6 from memory, plus 1 past Learn point), then the
3 likely customer questions, the 60-second story without the deck, then the crib sheet (≤ 8 points, misses first,
≤ 2 Learn points). Verdict: ready / not ready + the 1–2 things to fix tonight. Optional morning recheck = the misses
only. Details: `skills/sc-ready/SKILL.md`.

## 4. Privacy

Calls, matches, Learn points and quiz scores live on the SC's own PC only: `~/.apac-sc-motion/learn/`. Never in the
deal folder, never SharePoint, never shown to another SC (the coaching rule, `FEEDBACK-LOOP-v0.2`). The SC may share
their own.

## 5. What the pilot measures (after 2 weeks, Renzo reviews)

`ready.py stats`: calls made vs skipped, match rate over time, quiz score first try, misses that came back right
in the morning, Learn points re-asked and got right. Decide: roll out, change, or drop.
