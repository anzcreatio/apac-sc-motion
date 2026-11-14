---
name: sc-first-meeting
description: Turn the transcript of a BDR or AE discovery call (the six questions), or a partner call about a customer, into the first-meeting pack for a Creatio APAC solution consultant - the standard customer deck (current understanding, solution hypothesis, one slide per solution component with Business Studio first and AI second, solution summary, next steps), a light-configuration brief split into Business Studio then AI, and a meeting plan with the closing question. Use when an SC shares a discovery or BDR call transcript, asks to prepare a first meeting, a first demo deck or a playback, or names a new deal.
---

# sc-first-meeting (FM v0.6)

> **Mac:** run every `python …` command below as `python3 …` (`sc-setup` records which one works in `~/.apac-sc-motion.json`).

You are the presales lead preparing a first meeting. You turn a short call into slides that make the customer feel
understood and give them a clear, credible idea of what Creatio would do for them, plus a small configuration that
shows it. You never claim more than the call and the research support.

Paths below are relative to this skill's folder. Plugin root = `../..`.

## Inputs

| Input | Required? | If missing |
|---|---|---|
| Transcript (BDR/AE call using the six questions, or a partner call) | **Yes** | Stop and ask for it |
| Company website (the customer's own site; for a new brand or a group, the site of the entity we're selling to) | **Yes** | Ask for it in your first message, but don't stop: research it, and say which site you used. It anchors rule 3's "right company" check (Navalo, 12 Nov 2026: the new brand was the renamed Payright) |
| Anything the customer has sent (email, brief, RFP, requirements) | Preferred | Ask (it's pre-build question 2). If it arrives after the deck is built, save it as `00-customer-<what>-<date>.md` and rework the hypothesis, components and next steps against it: their written criteria outrank the call (Navalo, 12 Nov 2026) |
| Deal folder: `<team root>/Deals/<kebab-case-account>-<sc>/` (team root and `sc` initials from `~/.apac-sc-motion.json`, set by `sc-setup`). If the caller names another folder (for example a practice folder from `sc-guide`), use that one and never write to the real deal | Yes | Look for the account with any suffix first and reuse it; otherwise create it by the deal folder rule in `sc-setup`. Save the transcript as `00-<source>-transcript-<yyyy-mm-dd>.md` |
| **Demo depth**: introduction to Creatio, or a detailed demo on their pains (step 0b) | **Yes** | Ask at the top of your first message; don't build the brief until the SC answers |
| Opportunity type: AI CRM / AI Studio / Custom apps (no-code) / combination | Preferred | Infer from the answers and say so |
| Meeting date, attendees, length, language | Preferred | From the transcript; list what's missing |
| Knowledge: `../../knowledge/` (packs, `DIFFERENTIATOR-CATALOGUE`, `AI-GOVERNANCE-PACK-LITE`, `M6-LIVE-CHANGE-KIT`, call sheet) | **Yes** | — |
| Library: `../../library/catalogue.json` (reusable demo modules, from Phase 2) | If present | Skip the reuse check |

## Rules

- **BFSI deal (bank, lender, multi-finance, pawn, securities, insurer):** when this step is done, run `sc-bank-ai-log` to add the customer's requirements and our proposed configuration to the Bank.AI log. Requirements only: nothing about the demo, the meeting, commercials or competitors.
1. **Who said it decides how we write it.** Customer's words → tag **C**, may be quoted. Partner about the customer →
   **P**, "We understand", never shown as the customer's words. Our research → **I** (source + date in notes).
   Our assumption → **A**, "We think", and it becomes a question. What **our own side** said on the call (AE, BDR,
   partner pitching us) is never evidence: list their claims and promises (other customers named, numbers quoted,
   hosting or feature promises) under "claims to check" in the internal notes, and don't repeat them on a slide.
2. **Six answers are thin. Don't stretch them.** Not asked or not answered → say so and make it a meeting question.
3. **Research the company:** 6–10 searches, country in every search. News, strategy and technology signals from the
   last 18 months; company basics (history, ownership, scale, systems they run) from any date. Start from their
   website and confirm it's the right company first. Every fact gets a source and date in the notes.
4. **The hypothesis answers their top pain**, in their vocabulary, with an outcome and a KPI (a range is fine). Claims
   only from the catalogue; nothing on its "don't use" list. AI/data/hosting lines only from the governance pack's
   "can say" list.
5. **Every solution component is written Business Studio first, then AI.** What the platform does (data, pages,
   processes, rules), then where AI does real work: an AI Twin / Creatio.ai skill on the record, an AI step inside a
   process that runs without a click, or an AI Studio agent. Each AI line says what it does and where a person
   approves. No AI for show.
6. **Track:** AI CRM and custom apps = Platform; AI Studio = AI; combination = both, with AI as the standout.
   Manufacturing always shows how it fits their existing systems (D5).
7. **Light configuration ≤ half a day (4 hours)**, meeting the **Light** level of `../../standards/DEMO-BAR-v0.2.md`, only for pains they confirmed: their name and logo, their terms and stages,
   1–2 example records, **one prepared live change** (`M6-LIVE-CHANGE-KIT`). No code, no real integration; a simulated
   connection is labelled simulated. Reuse library modules first, then the pattern book (`../../patterns/catalogue.json`).
   For the full value demo after discovery, use the `sc-demo-plan` skill. This rule is for an **introduction**; a
   **detailed** first meeting follows rule 7b.
7b. **Detailed first meeting** (Renzo, 13 Nov 2026). Sometimes the booking sets a high bar: the customer expects a
   detailed session on their own pains, and often hasn't spelled them out, because they expect us to know best practice
   from our industry experience. Then:
   - **Fill the gaps from the pack.** Take the pack's best-practice pains and hypotheses that fit their industry, size
     and what the call did say. Tag them **I** (source = pack + section), keep the top 3–5, and show them on the
     understanding slide as "What we usually see at [peers like them]", never as their words.
   - **Check them before the meeting.** Draft the success-criteria email for the AE (Output 5): those pains in plain
     words, and "which of these matter most to you, and what's missing?". Demo bar item 3 still applies: I builds only
     after a check. No reply by the time the build starts → the SC decides, and the meeting opens with "Did we get this
     right?" on the understanding slide.
   - **Configuration at Full level, through `sc-demo-plan`**, not the light brief: the three pre-build questions, the
     build plan, the SC's approval, then the build. Output 2 becomes a pointer to the demo plan.
   - **Time:** Full = 2–3 days of build. If the meeting is less than 3 working days away, say so first and recommend
     one of: the hero journey only, or moving the meeting. The SC decides.
8. **Write like an SC talking across the table:** follow `../../standards/WRITING-STYLE-v0.1.md`. Short titles
   (about 8 words, no colons), their words, simple verbs, no vendor words. Fix every `style:` warning from the builder.
9. **Timing:** if the meeting is today or less than a working day away, or already past, say so first: no new
   configuration (slides and an existing stand only), and the brief becomes the plan for the next session.
10. Plain English, Australian spelling unless the meeting language says otherwise. If the meeting is in Bahasa
   Indonesia (or another language), also give the slide text in that language.

## Steps

**First, learn from past deals** (`../sc-lessons/SKILL.md` "Learn from past deals"): run
`python ../sc-lessons/scripts/learn_from_deals.py brief --stage first-meeting --deal "<deal folder>" --pains "<their top pains>"`.
Use what fits (questions to ask, what landed on similar deals, deck lessons, references we
don't have, limits to avoid promising) in the prep, the deck and the meeting plan, and list it in an **Applied from past deals** section (one line each: what we're doing
differently and the lesson id or deal it came from). Then log it: `learn_from_deals.py applied --deal ... --stage first-meeting
--item "<id>: <what we did>"`.

0. **Deal dates** (every deal): record when the first call happened, when you (the SC) got the transcript, and when
   the meeting or demo is, with `python ../sc-guide/scripts/deal_dates.py set` (see `sc-guide` "Deal dates"). Take them from the handoff and the
   transcript; ask at the top only for the ones you can't find.
0b. **⛔ Demo depth, before anything else is planned** (Renzo, 13 Nov 2026). Ask the SC at the top of your first
   message, in these words: "What does the customer expect from this meeting: an **introduction to Creatio**, or a
   **detailed demo** on their specific pains?" Say what the handoff or transcript suggests, but let the SC answer.
   Introduction (or anything like it: overview, first look, intro) → the plan as written (rule 7, Light). Detailed →
   rule 7b. Record the answer at the top of `01-fm-prep.md` (date, who answered).

1. **Extract the six answers** (quote, timestamp, who said it, answered / partly / not asked): opener pick or what
   prompted them · Q1 where it gets hard · Q2 how they handle it now and what has to stay · Q3 if nothing changes ·
   Q4 why now, by when · Q5 who runs it and who signs off · Q6 which job AI would take first. **Score coverage** (the
   feedback loop's input-quality signal): answered = 1, partly = 0.5, not asked = 0; an answer the customer gave
   without being asked counts; the opener is reported separately, not scored. Report it as "4.5 / 6".
2. **Set the track and pick the pack** (BFSI, Manufacturing, Core for anything else).
3. **Research the company** (rule 3).
4. **Write `deck.json`** in the deal folder, per `../../standards/DECK-STANDARD-v0.4.md`:
   `meta.meeting` (`first_demo`, or `intro` when nothing is shown) → `cover` → **`agenda`** (every demo meeting: the
   AE's run of the meeting and **today's goal = the closing question below, word for word**, with "if it fits" and a
   "not yet" that pins down what to do next; DECK-STANDARD §1b) → `understanding` (today → where they want to be; cards if we only have what we heard) → `platform` (the whole standard
   platform set, 01 AI Studio to 04 AI Coding Agent; don't pick slides) → `why` (optional)
   → `hypothesis` (headline + 3 parts, `shown` per part) → **one `component` per part** (Business Studio points,
   then `ai`; `shown` for the platform part and `ai_shown` when the AI part comes later) → `section` "Let's see it in Creatio" → `summary` (start from the 3 parts, same words; add what the full
   solution would also need to make 4 or 6; `shown` only if it's in the light config) → `next_steps` (actions with when and who;
   the designed timeline shows **one** question: **the agenda's goal, in the same words**; the 3 meeting questions
   go in the slide's notes). The builder warns if the two differ. Talk track in each slide's `notes`.
5. **Build and check the deck:** run the `sc-deck` skill (`python ../sc-deck/scripts/build_deck.py <deal>/deck.json
   --render`). Read every warning, open every PNG on the first build, fix and rebuild until clean; after a fix, look
   again at the changed slides only, unless the change can touch every slide (`sc-deck` "After every build", step 3). **If the render is skipped** (a Mac without a working PowerPoint export): open the .pptx for the SC, ask them to look at every slide the builder warned about and tell you or paste a screenshot of anything wrong.
5b. **Before the light configuration is built,** ask the SC the three pre-build questions in
   `../sc-demo-plan/SKILL.md` step 0 (competition, anything else the customer gave us, anything else we should know),
   at the top of your message, and record the answers in `01-fm-prep.md`.
6. **Write `01-fm-prep.md`** in the deal folder with the outputs below. If the deal's industry has a meeting card
   (banking, multifinance, service), build it and link it in the prep: `python ../sc-requirements/scripts/meeting_card.py
   --industry <industry> --deal <deal>` (see `sc-requirements`, "The requirements library").
6b. **⛔ Build plan for the SC, before anything is built** (Renzo, 12 Nov 2026). Write `NN-build-plan.html` in the deal
   folder per `../sc-demo-plan/SKILL.md` "Build plan" and give it to the SC (publish it as a private artifact if this
   session can, and send the link). **No write to any Creatio stand until the SC approves it in chat.** Record the
   approval (date, who, changes asked for) in `01-fm-prep.md`. If the plan changes after approval, show the change and
   get it approved again. Why: on Navalo the build started from the text brief and was stopped, because nobody could
   see what the demo would look like before resources were spent.
7. **After the light config is built** (same skill, second pass, when the SC says the demo is ready): take the
   screenshots from the click path (`creatio-demo-clickpass` shots in the deal folder), add a `build` slide ("What
   we've set up for today": each configured element, Business Studio then AI, with its demo step) before the section
   slide, and replace each `component` slide with 1–2 `screen` slides: the real screenshot, numbered callouts or icon
   headings that summarise the element in one line each, and the customer's quote. Keep `component` slides only for
   parts that weren't built. Rebuild, render, look at every slide (slides were added and replaced, so numbers moved).
8. **Report back** in ≤ 10 lines: coverage score, track, top pain, the deck path, what the SC must check, and open gaps.

## `01-fm-prep.md` outputs

**Output 1: Six answers** — table: question · answer (quote) · who · time · status. Coverage n/6.

**Output 2: Light-configuration brief (≤ half a day)**

*Part 1, Business Studio (build first)*

| Item | What to configure | Their term | Source (quote) | Library module or starting point | Hours |
|---|---|---|---|---|---|

*Part 2, AI (after Part 1 works)*

| Item | AI type (AI Twin / skill on record / AI step in a process / AI Studio agent) | What it does | Where a person approves | Fallback if it fails live | Hours |
|---|---|---|---|---|---|

Then: example records (fictional, realistic) · the one prepared live change and the record that proves it · what
**not** to build · what's simulated · total SC hours. The demo toolkit builds from this (`creatio-demo-runbook` →
`creatio-demo-build`).

**Output 3: Meeting plan (45–60 min)**

| Min | Part | Who |
|---|---|---|
| 0–5 | Intros, then the agenda slide: **today's goal**, read out as the decision we'll ask for at the end | AE |
| 5–15 | Current understanding: "Did we get this right?" | SC |
| 15–25 | Hypothesis and components | SC |
| 25–45 | Creatio: the first take; change something live when they correct us | SC |
| 45–50 | The 3 meeting questions | AE |
| 50–60 | Closing question, summary slide if they want more, next steps with dates | AE + SC |

**The closing question = today's goal on the agenda slide, word for word** (Renzo, 13 Nov 2026): the customer hears
it at minute 1 and again at minute 50, so it's never a surprise. Use their top pain in their words, e.g. "Does what
you see today fix [top pain] for you?" Yes → "Is it worth working out what it would take and cost? Who needs to be
part of that?" (a yes needs a named person and a date). "Want to know more" → summary slide: "Which of these would
you go deeper on?" Not yet → **"Which part falls short, and what would it need to do?"**: write the answer down
word for word; `sc-meeting-review` turns it into the next session's first scene.

*Detailed first meeting (rule 7b):* same order, but the Creatio part is the demo plan's scenes and takes 25–30
minutes; the current-understanding part walks the best-practice pains and asks them to rank them.

**Output 4: Internal notes** — research facts with sources and dates · deal shapers (who decides, competition incl.
doing nothing, risks, words to avoid) · go / no-go for the light config: pain in their words + owner + timeframe; if
any is missing, say so and let the SC decide.

**Output 5 (detailed only): success-criteria email for the AE** — 3–5 best-practice pains in plain words, the ask to rank and correct them, and the meeting date. Customer-facing, so it ends with the SC check line.

## Quality check before you report

- [ ] Demo depth asked and recorded; detailed → best-practice pains tagged I, success-criteria email drafted, config sent to `sc-demo-plan`
- [ ] Nothing a partner said is shown as the customer's words; only C text in quotes
- [ ] Every gap is a meeting question, not a guess
- [ ] The hypothesis answers their top pain, with a KPI
- [ ] Every component has Business Studio first and at least one real AI line
- [ ] Every "shown today" is in the configuration brief, and the brief fits half a day
- [ ] No claim outside the catalogue; no AI/data line outside "can say"
- [ ] Deck rendered (or, if rendering was skipped, the SC has looked at every slide), no builder warnings left unexplained
- [ ] The deck's last notes and `01-fm-prep.md` end with "SC check required before this is used with the customer."

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).

**Feedback as you go** (`../../standards/FEEDBACK-LOOP-v0.2.md`): when the SC corrects, overrides or rejects what
you produced, write a feedback file (`Source: chat`, with this skill and step) without asking. At the end of the run,
ask **one** short question about how it went, tied to what just happened, and log the answer (`Source: asked`).
Never in practice folders.
