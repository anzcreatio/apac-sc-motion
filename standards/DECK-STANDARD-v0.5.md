# Deck standard v0.4

**What it is:** the slides every APAC SC customer deck is made of, their order, and the `deck.json` that builds them.
**Built from:** the decks presented at H&G (10 Nov 2026), Suntory (11 Nov, `Suntory Introduction Nov 2026.pptx`) and
Telkomsel (12 Nov), not from theory. **Default look: `creatio-designed-2026`** (the Suntory deck as presented: white,
Creatio logo top right, 40 pt title with a small orange caps label above it, orange line icons).
**Builder:** `skills/sc-deck/scripts/build_deck.py <deck.json> --render`. One `deck.json` per deal, in the deal folder.

## 1. The deck, in order

| # | Slide type | Required? | What it does | Field source |
|---|---|---|---|---|
| 1 | `cover` | Yes (not in a partner-led slot) | Customer + the outcome in their words. A photo (`image`) with the title on orange blocks, or plain orange | H&G 1, Suntory 1 |
| 1b | `agenda` | **Yes for every demo meeting** (Renzo, 12-13 Nov 2026) | The AE opens with it: numbered cards with what we'll do on the left (**no minutes or names on the slide**: they go to the notes as a run sheet, v0.5); on the right **"Today's goal"**: the decision question, then what happens if it fits and what "not yet" pins down. **The goal is the closing question, word for word**: the SC asks it at the end on the next-steps slide. No open "what would make this a success?" slot: get success criteria before the meeting. Wording by meeting type in §1b | Examples: `Deals/_examples/agenda-and-ae-brief/` |
| 2 | `understanding` | **Yes** | What we currently understand about their pains: **Today → where they want to be**, plus timing. Or cards when we only have what we heard | H&G 2, Suntory 2–3, Telkomsel 1 |
| 3 | `platform` | **Yes, always the whole set** (Renzo, 11 Nov 2026) | The platform story from the Slide-library's standard set: AI Platform + AI CRM, the three studios, **01 AI Studio, 02 AI Twin, 03 Business Studio, 04 AI Coding Agent**, with speaker notes. Extras (AI Studio callouts, AI Twin concept) with `add`. Other corporate slides (analysts, customers, telecom) with `library` | H&G 3–11, Suntory 4–11 |
| 4 | `why` | Optional | Why Creatio fits *them*: 3–4 reasons = our differentiators in their terms | H&G 12, Suntory 9 |
| 5 | `hypothesis` | **Yes** | One headline sentence + 3 parts. Questions to confirm go on the next-steps slide, not here | H&G 13, Telkomsel 2 |
| 5b | `build` | **Yes, once the light config is built** | "What we've set up for today": the configured elements, Business Studio first, then AI, each with its demo step. Sets expectations before the live demo | Field feedback 11 Nov |
| 6 | `component` | **Yes, one per part** (before screens exist) | One part of the solution: how it works (**Business Studio first**), then **where AI helps**, then "you'll see this today / next time" | New in v0.1 |
| 7 | `screen` | **Replaces `component` once the demo is built: 1–2 per part** | Screenshot(s) with numbered highlights, a quote in their words, one point. Backup for the live demo | H&G 14–20, Suntory 4–7 |
| 8 | `summary` | **Yes** | **Your solution at a glance**: numbered parts, "In today's demo" vs "Still to show you". No question on the slide. It changes every meeting (see §4) | H&G 21, Telkomsel 3 |
| 9 | `roadmap` | Optional | Suggested order of phases, with *when* in their terms. No effort or price | H&G 22, Suntory 8 |
| 10 | `next_steps` | **Yes** | Questions for them + actions with **when** on the slide; **who goes in the notes, not on the slide** (v0.5, Suntory + Navalo). A next step still needs a named person and a date: say the names, and the review records them | H&G 23, Suntory 10 |

`section` (a divider such as "Let's see it in Creatio") can go anywhere. A required slide can be left out only by
listing it in `meta.waive` with the reason (e.g. Telkomsel: partner-led, Deloitte owns next steps).

### Two stages of the same deck

| Stage | When | Parts of the solution shown as |
|---|---|---|
| **Before the build** | Right after the first call (`sc-first-meeting`) | `component` slides: how it works, then where AI helps |
| **After the build** (the deck you present) | Once the light config is on the stand and the click path has screenshots | `build` slide + `screen` slides: a real screenshot, 1–3 numbered callouts or icon headings, a one-line summary of each element, the customer's quote |

Renzo, 11 Nov 2026: "slides that actually contain screenshots and summaries of the main elements of our demo
configuration. If that is included in the deck then yes I would present most of this."

## 1b. Today's goal, by meeting type

Use **their top pain in their words**, never RFP language ("does it meet your requirements?" invites "we'll think
about it"). Either answer moves the deal: yes = agree what it takes; not yet = pin down exactly what to do next.
Set `meta.meeting` in `deck.json` to `first_demo`, `value_demo`, `proof` or `intro`.

| Meeting | Goal / decision (example) | If it fits | Not yet |
|---|---|---|---|
| `first_demo` | "Does what you see today fix [top pain] for you?" | Agree what it takes, who's involved and when | "Which part falls short, and what would it need to do?" That becomes the next session |
| `value_demo` | "Is this worth turning into a proposal?" | Proposal, named sponsor, date | "What's missing before you'd consider it?" |
| `proof` | "Does this pass your criteria?" | Go: commercial next steps | "Which criterion failed, and what's the fix?" |

`sc-meeting-review` records the answer, and a "not yet" answer becomes the next demo plan's first scene.

## 2. Rules for the words

**Every word follows `WRITING-STYLE-v0.1.md`** (sound like an SC, not like AI). The builder flags vendor words, colon
titles, titles over 12 words, semicolons and em dashes.


| Rule | Why |
|---|---|
| Their words and their terms; no product or module names in titles | They should recognise their business, not our catalogue |
| Titles are sentences that say the point ("The Build board shows the whole house on one screen") | The title alone should carry the slide |
| Evidence tags in every row of `deck.json`: **C** they said it · **P** a partner said it · **I** our research · **A** our assumption. Cards show them; the today/want layout doesn't (it's captioned as our reading), so the tags live in the JSON and the notes. Only **C** text is ever in quotes. What our own AE/BDR said is never evidence | Never present a partner's words or our guess as theirs |
| Claims only from `DIFFERENTIATOR-CATALOGUE`; AI/data/hosting lines only from the governance pack "can say" list | Same as the whole motion |
| Limits: understanding 3–5 rows (≤ 15 words per cell; **4 rows when there is a timing line**) · hypothesis 3 parts · summary 3, 4 or 6 parts · component 2–4 points + 1–2 AI lines | Slides are read in seconds |
| Talk track, sources and cautions go in `notes`, never on the slide | The deck stays clean; the SC still has everything |
| Screenshots: example data only, captioned ("Example data on fictional sites") | No customer data in a demo deck |
| The last slide's notes end with "SC check required before this is used with the customer." (the builder adds it) | Project rule |

## 3. `deck.json`

```json
{
  "template": "creatio-designed-2026",
  "meta": {"title": "...", "customer": "...", "date": "...", "example_caption": "Example data on fictional sites",
           "deck_standard": "v0.3", "waive": []},
  "out": "05-first-meeting-deck.pptx",
  "slides": [ {"type": "...", "title": "...", "subtitle": "...", "notes": "...", ...} ]
}
```

| Type | Fields |
|---|---|
| every slide | `title`, `subtitle` (the small caps label above the title: **off by default since v0.5**, it reads as AI-made; `"kicker": true` on a slide or `meta.kickers: true` brings it back), `notes` |
| `cover` | `title`, `subtitle`?, `date`?, `image`? (full-bleed photo), `fill`? (hex), `screenshot`? |
| `understanding` | `rows`: `{topic, today, want, tag}` → today/want layout, `want_label`, `timing`: `[{when, what}]`. Or `rows`: `{topic, text, note?, tag?}` → cards (`icon`? per row: up to 5 cards in a row), `footer`? · `caption`? |
| `facts` | `statement`, `sub`?, `facts`: `[{figure, text, accent?}]` |
| `why` | `reasons`: `[{title, text}]` |
| `hypothesis` | `headline`, `parts`: `[{title, text, shown?}]`, `confirm`? (only if there is no next-steps slide) |
| `component` | `lead`, `points`: `[{title, text, icon?}]`, `ai`: string or list, `shown`: true/false (platform part), `ai_shown`? (AI part, when it comes later), `quote`?: `{text, who}` |
| `screen` | `screens`: `[{file, region?, crop?, width?, alt, highlights?: [{box, text?, corner?}]}]` (1 or 2) · `layout`: `picture_left` / `picture_right` / `row` (two screens side by side with a heading and point under each, e.g. before and after a live change) · `width`? · `blocks`: `"keys"`, `{quote}`, `{point}`, `{heading, icon?}`, `{figure: {value, label}}`, `{steps: []}`, `{table: {title, columns, rows}}`, `{takeaway}` · `caption`? |
| `summary` | `outcome`?, `parts`: `[{title, text, shown}]`, `labels`?, `numbered`? (default true), `caption`? |
| `roadmap` | `steps`: `[{title, what, when, owner?}]`, `timing`?, `caption`? · `owner` = who can own the step after handover, in the customer's terms ("Your business team", "Your IT team", "Creatio"); **required on existing-customer roadmaps** (`sc-guide` mode D), optional otherwise |
| `next_steps` | `questions`?, `actions`: `[{when, what, who?, icon?}]` (`who` → notes; `show_owners: true` puts it back on the slide); `layout`: `timeline` (default in the designed look, ≤ 5 steps, one question in a box) or `table` |
| `build` | `lead`?, `platform`: `[{name, what, icon?, see?}]`, `ai`: same, `caption`? (`see` = the demo step, e.g. "Step 2" or "Next time") |
| `section` | `text`, `sub`? |
| `map` | `hub`: `{title, text?}` (their platform, e.g. "Your Creatio"), `left` / `right`: `{label, items: [{title, text, icon}]}` (1-4 each: left = connected to what they have, right = elsewhere in their organisation), `outcome`?, `caption`? · "what else can it do" slides for existing customers (`sc-guide` mode D). Only ideas the customer can configure themselves; say how each is built in the notes |
| `flow` | `steps`: `[{title, skills?: [..], who?, highlight?}]` (up to 8, one row), `loop`?, `title_size`?, `skill_size`? · internal and training decks |
| `outputs` | `rows`: `[{step, customer, internal}]`, `labels`?, `size`? · what each step produces |
| `agenda` | `items`: `[{min, what, who}]` (min + who → notes as a run sheet; `show_owners: true` brings back the old minutes/what/who table and pale goal box), `length`? (warns if the minutes don't add up), `decision` (today's goal = the closing question), `outcomes`: `[{if, then}]` (fits, then not yet), `goal_label`? (default "Today's goal") |
| `platform` | nothing required. `add`: extra slide numbers from the set's `optional` list · `drop`: only with a reason in the notes (the builder warns) · `slide_notes`: override a slide's speaker note. The set itself lives in `Slide-library/catalogue.json` → `standard_sets.platform` |
| `library` | `file`: `library:<name>.pptx` (SharePoint `Slide-library`, listed in its `catalogue.json`), `slides`: `[1, 2, …]`. Copied with pictures and video; best on the designed template, which holds the corporate layouts |

Screenshot coordinates (`crop`, `box`) are in the screenshot's own pixels. When a file holds a region cut from a
larger frame (the click-path HD shots), give that `region` and use frame coordinates.

## 4. The solution summary is a living slide

The `summary` slide's parts are the deal's **current proposed solution**. After each meeting, `sc-meeting-review`
(Phase 3) updates `deck.json`: parts confirmed, added, dropped, or moved from "Still to show you" to "In today's demo".
Keep earlier versions by date in the deal folder (`deck-2026-11-10.json`), so the solution's history is visible.

## 5. Templates and icons

| Template | Use |
|---|---|
| `creatio-designed-2026` | **Default.** Suntory look; icons; corporate layouts for library slides |
| `creatio-2026` | The plain frame used for H&G |

Icons (designed template): `adjustments-horizontal, arrows-shuffle, arrows-split-2, bottle, building-store,
building-warehouse, calendar-event, camera, chart-bar, checklist, clipboard-check, database, device-ipad, hand-click,
headphones, layers-intersect, login, logout, message-chatbot, route, shopping-cart, sparkles, truck-delivery,
user-check, users-group, video` (Tabler line icons, orange). An unknown name gives a warning and no icon.


A template is a folder in `skills/sc-deck/templates/<name>/` with `base.pptx` and `template.json` (frame shapes,
content area, colours, font). **A new corporate template = a new folder, not new code.** Map its title, subtitle
and page-number shapes and its content area, build `tests/deck/sample-fictional`, render it and check every slide.

## 6. What the builder checks

Warnings, not errors: a title too long for two lines (titles shrink to fit two) · a component's right-hand column past the bottom · a required slide missing (unless waived) · row/part counts outside the limits · text that
probably doesn't fit · a right-hand column that runs off the slide · next steps without dates · **a demo meeting
without an agenda** · **a closing question that differs from the agenda's goal** · an agenda without a "not yet"
outcome that pins down the next step. **Always render
(`--render`) and look at every slide before the SC sees it.**

## 7. Changes

| Version | Date | Change | Evidence |
|---|---|---|---|
| v0.1 | 11 Nov 2026 | First standard, from three presented decks | H&G, Suntory, Telkomsel |
| v0.1 | 11 Nov 2026 | Cover red, no date by default | H&G and Suntory covers were both edited to red (2 deals) |
| v0.1 | 11 Nov 2026 | Confirm questions moved from the hypothesis slide to next steps | H&G field edit (1 deal: kept as the default because the next-steps slide already carries them) |
| v0.2 | 11 Nov 2026 | Default look = `creatio-designed-2026`; icons; caps label; next steps as a timeline; cover photo; library slides copied in Python | Renzo chose the Suntory deck as presented. PowerPoint automation is blocked on 'Confidential'-labelled decks |
| v0.3 | 11 Nov 2026 | `platform` slide type: every deck has the whole platform set, 01–04, with speaker notes. 03 Business Studio says "10x": the note tells the SC not to say it and gives the Nucleus figure | Renzo: always include 03 Business Studio and 04 coding agent |
| v0.3 | 11 Nov 2026 | Writing style guide + builder check; `build` slide; screens replace components once the demo is built; `row` screen layout; titles shrink to fit two lines | Renzo: language too AI-sounding; wants screenshots and summaries of the configuration. Blind test 11 Nov |
| v0.4 | 13 Nov 2026 | Agenda shows "Today's goal" = the closing question, word for word; required for every demo meeting; "not yet" outcome pins down what to do next; wording by meeting type (§1b); builder checks all three | Renzo: open the deck with the meeting's key goal, asked so either answer moves the deal |
| v0.5 | 16 Nov 2026 | No caps label (kicker) above titles by default; agenda as numbered cards with no minutes or names, solid accent goal panel; no owners on agenda or next-steps slides (both in the notes); summary with nothing shown yet uses two columns | Navalo as presented: Renzo removed owners (2nd deal after Suntory) and minutes, and had the look restyled "so it doesn't look like Claude made it" |
| v0.5 | 16 Nov 2026 | Roadmap steps take an optional `owner` line (who owns it after handover), required on existing-customer decks. A session deck for a live customer waives the sales slides (`understanding`, `platform`, `hypothesis`, `summary`, `agenda`) in `meta.waive` and opens with a `flow` slide of what they have today | A live customer's training and roadmap session; 2 deals where the partner's role shaped delivery (feedback `…-delivery-partner-and-ownership.md`) |
| v0.5 | 16 Nov 2026 | New `map` slide type: the customer's platform as a hub with icon tiles for connected and wider opportunities | Renzo asked for a visual expansion slide on a live customer's session deck |
| v0.2 | 11 Nov 2026 | Next steps may show the month only and no owner on the slide (owners in the notes) | Suntory field edit (1 deal). Builder still warns without dates |
