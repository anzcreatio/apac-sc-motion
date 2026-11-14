---
name: sc-clickpath
description: Turn a Creatio demo's click path into two self-contained HTML pages - an SC practice guide the team uses to learn the demo (per step the exact record and how to find it, numbered clicks with the UI labels, what you'll see, what the customer said, the point to land with its KPI and differentiator, what to say, likely questions with sourced answers, watch-outs, who is signed in; per use case a 30-second value story, their pain and a bridge line; the stand's usernames and passwords in plain view; practice mode that hides the talk track until you recall it) and a customer-safe recap ("what you saw": screenshots and plain words only, nothing internal, a DRAFT banner until the SC approves it). Also screenshots steps that need two users at once through a second browser. Use after a demo build or rehearsal, when an SC asks for a click path, practice guide, demo recap, follow-up pack or "what you saw" page, or wants to memorise or rehearse a demo.
---

# sc-clickpath


> **Mac:** run every `python …` command below as `python3 …` (`sc-setup` records which one works in `~/.apac-sc-motion.json`).
Two pages from one click path (Renzo, 11 Nov 2026; SC page made a teaching page 13 Nov 2026): one for us to learn,
practise and present from, one the customer can keep. Both are single HTML files with the screenshots and Creatio
logo inside, so they open offline. Layout follows the Creatio **Workflow Explorer**: masthead with a stat strip, a
clickable demo-flow strip, tabs, a sticky filter rail, and collapsible use cases with step rows. One light Creatio
brand theme.

**What the SC page is for:** the team memorises the demo from it, so presentation quality and the value proposition
go up. **Memorise the beats** (which record, which moment, which value line), **not a word-for-word script**: say the
"Say" lines in your own words.

Paths are relative to this skill's folder; plugin root = `../..`.

## Steps

1. **Cards first.** The toolkit's `creatio-demo-clickpass` skill rehearses the demo and writes `cards.json` + `shots/`
   in the deal folder (`clickpath/`). Use it. If the deal has shots and runbooks but no cards (a build done outside the
   toolkit), write `cards.json` in the same shape from the runbooks' rehearsal results, one card per beat, and say so
   in its `source` field.
2. **Steps that need two users at once** (submitter and approver, agent and supervisor): the first user stays in the
   usual browser; the second gets its own Chrome.
   `python scripts/second_browser.py launch --url <stand url>` → **the SC signs in once per stand in that window**
   (Claude never types a password) → `python scripts/second_browser.py shot "<deal>/clickpath/shots/05x-approver.jpg"
   --url <page>` → `python scripts/second_browser.py close`. It runs Chrome with `--remote-debugging-port=9223` and its
   own profile, screenshots through Playwright `connect_over_cdp`, and closes with CDP `Browser.close`. Add the frame
   to `cards.json` and record the second login in `clickpath-sc.json`.
3. **SC teaching overlay.** Write `clickpath-sc.json` next to `cards.json` (format in the builder's docstring). Sources,
   in this order: `build-plan.json` (each step's quote/triggers, differentiator, minutes, say, not-built lines),
   `01-fm-prep.md`, the transcripts and the customer's emails, the runbooks (records, clicks, traps, reset).
   Per step:

   | Block | What goes in | Rule |
   |---|---|---|
   | **Open** | the exact record, how to find it, its state before you start | always |
   | **Click** | numbered clicks with the exact UI labels in `**bold**`; values to type in `type` | from the rehearsal, not from memory |
   | **You'll see** | what changes on screen | |
   | **They said** | the customer's words with who and when (timestamp or email section) | **C only**. A partner's words get `"partner": true` (shown "Partner said"). Nothing inferred or assumed: the builder drops it |
   | **Land this** | the one point, why it matters to them, a KPI, a differentiator (`d_id` + line) | claims only from `knowledge/` (catalogue; governance "can say" lines; KPIs as the packs' range questions, numbers only from Strong rows, attributed) |
   | **Say** | 2–3 sentences | |
   | **If they ask** | likely question + answer + `source` | no source → the builder writes "We'll confirm that in writing." |
   | **Watch out** | the trap at this step | |
   | **Signed in as** | which login, in which role | |

   **Theirs or ours.** Set `"plan": "../build-plan.json"` in `clickpath-sc.json`: each card's `runbook_step` picks its
   build-plan step, and the builder takes its **label** (Pain · Asked · Asked (must) · Differentiator · SC idea · Our
   idea), its `our_idea {why, source, ask}` and its `differentiator {id, line, competitor}` (what you write in
   `clickpath-sc.json` wins; set `label` there when the plan has none). The SC page shows the label as a chip on every
   step and "N · M, from them · our ideas" in the stat strip. **Our idea steps** (Renzo, 13 Nov; log §4 item 70): after
   their own scenes (the builder warns otherwise), kept even if the customer hasn't answered the question first; the
   first block is **Open with this question** (`our_idea.ask`), then "Why we're showing this" (`why` + source, tag I,
   marked "not their words") replaces They said. Every step with a differentiator shows the **competitor angle** in
   Land this (catalogue only; the builder flags "they can't"). The customer page shows none of this.
   Per use case (`use_cases`): a **30-second value story**, the **pain in their words** (C), and a **bridge line** to
   the next use case (the last one hands to the closing question). Top level: `story`, `before_start`, `reset`,
   `logins` (role, username, url, steps: **no passwords in this file**), `faq` (the hard questions: references,
   hosting, native vs custom, price), `notes`.
4. **Logins and passwords (SC page only, Renzo 13 Nov 2026).** The team keeps **one file** on SharePoint:
   `Stand-logins/stand-logins.json`, `{"<stand>": {"<username>": "<password>"}}` (e.g. `"11014108-demo"`). An SC adds a
   stand's logins there themselves, once. The builder finds it from `~/.apac-sc-motion.json`, picks the stand named in
   `cards.json` `instance`, and shows each username and password **in plain view** in Before you start (demo stands
   hold no confidential data, Renzo 13 Nov 2026), so every SC has them. **Automatic:** if `clickpath-sc.json` lists no `logins`, the page
   gets every login the file holds for that stand. A value can also carry a role:
   `{"Supervisor": {"password": "...", "role": "Credit manager (approver)"}}`. Notepad may save the file as
   `stand-logins.json.txt`: that works too. If a login is missing, tell the SC to add it to that file.
   **Claude never opens that file, never prints a password and never types one.** `--credentials <file>` overrides it.
   The `--fragment` (phone / artifact) copy shows them too. The customer page never does.
5. **Customer words.** Write `clickpath-customer.json` next to `cards.json`:
   `{customer, page_name, title, eyebrow, date, intro, simulated, contact, approved: false,
     sections: {UC1: "heading"}, titles: {"UC1-2": "plain title"}, cards: {"UC1-2": "what it means for them"},
     hide: [...], hide_reasons: {...}, crop: {"UC1-3": [left, top, right, bottom] as 0–1 fractions}, crop_reasons: {...},
     screens_reviewed: [...]}`.
   One or two sentences per step in their words (`../../standards/WRITING-STYLE-v0.1.md`): what it means for them,
   not where to click. Say plainly what was simulated.
6. **Build both:** `python scripts/build_clickpath.py "<deal>/clickpath/cards.json" --slug <account>
   [--credentials "<file>"]` → `<account>-click-path-sc.html` and `<account>-click-path-customer.html` in the same
   folder. Fix every `SC GAP` line (a step without Open or Land this, a use case without a value story, pain or bridge,
   a quote that isn't C, a D-ID not in the catalogue, an answer without a source).
7. **Text check.** The builder flags, in the customer page: stand names and URLs, schema and package names, demo
   wording (runbook, reset, seed data), evidence tags, presenter cautions, pricing, vendor words and AI phrasing, and
   steps without customer words. Fix every one. **Any login wording, username or password in the customer page stops
   the build** (exit 2, no customer file written).
8. **Look at every screenshot** (the text check can't see inside images). Hide or crop anything showing: **other
   customers' names** (shared stands carry other demos' accounts, agents, orders and branding), test records, **login
   names** (e.g. "Waiting on Supervisor" in a timeline), URLs, placeholders, real customer data. Add each checked step
   to `screens_reviewed`. The page stays **DRAFT** until every shown screenshot is reviewed and the text check is clean.
9. **SC review and approval.** The SC reads the SC page (does it teach the demo? are the quotes right?) and the
   customer page, then sets `"approved": true` (or `--approved`) on the customer overlay; rebuild. Only then can the
   customer page go to the customer, typically with the follow-up email after the demo.
10. **Keep and share.** Both files stay in the deal folder (SharePoint). The SC version can also be published as a
    private Claude artifact for practice on a phone (`--fragment`, logins included); the customer version is sent as a
    file or published only after approval, and only when the SC asks.

The SC page's **Before you start** always opens with: rehearse on the presenting device, network and login, with
the fallback ready (demo bar item 7).

**"If they ask what they need" tab.** If the deal folder has a meeting card (`meeting-card-<industry>.html`, built
by `sc-requirements/scripts/meeting_card.py`), the SC page shows it as a third tab, so the SC can answer "tell us
what we need" without leaving the click path. `clickpath-sc.json` `"meeting_card"` names a different file. Never on
the customer page.

## What goes where

| | SC practice version | Customer version |
|---|---|---|
| Per step | Label chip (theirs / ours), Open with this question (our ideas), Screenshot, Open, Click, You'll see, They said or Why we're showing this, Land this (with competitor angle), Say, If they ask, Watch out, Signed in as | Screenshot (cropped where needed), plain title, one or two sentences on what it means for them |
| Per use case | Value story (30 s), their pain in their words, bridge line | Heading |
| Extras | Story in one line, Before you start, logins (username and password in plain view), reset, hard questions, practice mode (hides Say, Land this, the value story and the answers; click to check), rehearsal ticks | What was simulated, who to contact |
| Never | — | Labels, our-idea reasons, competitor angles, clicks, talk track, watch-outs, stand names, logins, passwords, package names, other customers, evidence tags, pricing, "SC check" lines |

## Rules

- The customer page never shows the SC check line; the DRAFT banner does that job until approval.
- Never send or publish the customer page yourself. The SC sends it.
- Example data only. If a screenshot shows real customer data, hide it and tell the SC.
- They said = confirmed words only (C), with who and when. Never put an inferred pain in someone's mouth.
- Claims, KPIs and answers only from `knowledge/` or the SC-approved plan; otherwise "we'll confirm in writing".

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is
none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).

**Feedback as you go** (`../../standards/FEEDBACK-LOOP-v0.2.md`): when the SC corrects, overrides or rejects what
you produced, write a feedback file (`Source: chat`, with this skill and step) without asking. At the end of the run,
ask **one** short question about how it went, tied to what just happened, and log the answer (`Source: asked`).
Never in practice folders.
