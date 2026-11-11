# Demo bar v0.1: the minimum for every demo configuration

**What it is:** the floor every Creatio demo meets before a customer sees it. It says **what must be true**, never
**how to build it**. Everything above the floor is the SC's call: their creativity, the pattern book, what the
customer wants to click through.
**Agreed:** Renzo, 11 Nov 2026. "Set a minimum benchmark and the rest to be answered by the SC."

## 1. Two levels

| Level | When | Items that apply |
|---|---|---|
| **Light** | First meeting, ≤ half a day of configuration (`sc-first-meeting`) | 1, 2, 3 (confirmed pains only), 4 (live change only), 7, 8 |
| **Full** | Demo after discovery, the "value demo" (`sc-demo-plan`) | All 8 |
| **Proof** | A proof of concept over days or weeks, ending in a readout (`sc-demo-plan`, proof mode) | All 8, plus written success criteria agreed with the customer, a test set with the right answers, a scoreboard, and a readout plan |

## 2. The bar

| # | Must be true | How we check | Why |
|---|---|---|---|
| 1 | **Their world.** Their name and logo, their words for objects, stages and fields, named personas, realistic example data (no empty lists, no "Test 1", no lorem ipsum) | Open every page in the demo path | They should recognise their business in 10 seconds |
| 2 | **It opens on their outcome.** The first screen is a home page or dashboard showing the result they care about, not a blank list or the standard desktop | The first click of the click path | First impressions set the meeting |
| 3 | **Every confirmed pain has a scene, and one hero journey runs end to end.** A pain they confirmed (C) with no scene is a gap. A pain we inferred (I) or a partner told us (P) can carry a scene only if we check it with the customer before we build (one email, or the first question in the meeting). An assumption (A) is a question, not a scene. Scenes without a pain are allowed (see §3) | The plan's pain-to-scene table | Business sense, not a feature tour |
| 4 | **Differentiators.** One rehearsed live change (D1). AI that acts while a person confirms (D3). Plus the track core: **D2 (one platform) for Platform deals, D5 (fits your landscape) for AI Studio deals, both for combined deals; D5 always in manufacturing** (differentiator catalogue) | The plan's differentiator column | Agreed motion rule |
| 5 | **AI-first floor.** At least one AI moment on a record (AI Twin or a Creatio.ai skill) and one AI step that runs in the background without a click (in a process), where it makes sense for their work. Each has a fallback if it fails live | The plan's Part 2 | Goal (e): AI first, not AI added on |
| 6 | **UX floor.** Native Freedom UI first; no empty views; a summary or KPI strip on the key pages; short helper text where a screen isn't obvious; no leftover sample-data noise in lists or menus; readable at the meeting's screen size | `creatio-ui-guidelines` review + browser check | The quality the customer judges us on |
| 7 | **It works every time.** Every use case passes in the browser (`creatio-uc-readiness`), there's a reset, and there are backup screenshots | Readiness verdicts | No live surprises |
| 8 | **It leaves a trail.** Click path with screenshots (`creatio-demo-clickpass` → deck `screen` slides), a build log, and harvest candidates for the demo library | Files in the deal folder | Feeds the deck (goal c) and the library (goal d) |

## 3. Every element carries a label, nothing is banned

| Label | Meaning | Rule |
|---|---|---|
| **Pain** | Solves a pain they confirmed | The opening and the hero journey are made of these |
| **Asked** | They asked to see it, even if it isn't a pain | Welcome. Keep it short |
| **Asked (must)** | A requirement they stated: no data kept after the work runs, a system that has to stay, a compliance rule | Treated like a pain: never dropped without telling the SC |
| **Differentiator** | Shows D1–D7 | Required set per item 4 |
| **SC idea** | The SC thinks it will land (pattern book, experience, competitor best practice) | Welcome. After the pain scenes, and the SC says why in one line |

Labels are for us, never on screen. They let the plan show the balance at a glance and let the weekly lessons see
what lands.

## 4. Time

About 3–4 main scenes in a 45–60 minute demo, 5–8 minutes each, plus the live change. Plan 6 productive build hours a
day and keep 20% of the build time as buffer for readiness checks, the reset, the click path and rehearsal.

## 5. Their brand

Use the prospect's public logo and colours only on the demo stand and in the deck for them. Never in anything
published or shared with other customers, and never their real customer data.

## 6. Custom components

Propose one when it clearly lifts the experience past what native Freedom UI does well (a whole job on one screen,
a map, a board) and say why in one line. Always mark it **custom** in the plan and the partner pack: partners have to
maintain it. Prefer a component that's generic enough to go into the demo library.

## 7. Best practice from outside

Learn from patterns and UX anywhere: competitors, other vendors' public documentation, analysts, partners. Never copy their screens, branding or wording, and
never claim anything against a competitor outside `DIFFERENTIATOR-CATALOGUE`. Every outside pattern in the pattern
book carries its source and date.

## 8. Changes

| Version | Date | Change | Evidence |
|---|---|---|---|
| v0.1 | 11 Nov 2026 | First bar | Renzo's brief; H&G, Suntory, SAHE builds |
| v0.1 | 11 Nov 2026 | Proof level; C/P/I/A rule for scenes; track core as in the catalogue; Asked (must); time and buffer; prospect branding | PRC test of `sc-demo-plan` |
