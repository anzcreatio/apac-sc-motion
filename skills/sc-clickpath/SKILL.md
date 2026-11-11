---
name: sc-clickpath
description: Turn a Creatio demo's click path into two self-contained HTML pages - an SC practice guide (every click, what you'll see, what to say, watch-outs, before-you-start checklist, reset, practice mode that hides the talk track, rehearsal ticks) and a customer-safe recap ("what you saw": screenshots and plain words only, nothing internal, a DRAFT banner until the SC approves it). Use after a demo build or rehearsal, when an SC asks for a click path, practice guide, demo recap, follow-up pack or "what you saw" page for a customer, or before sending anything about the demo to a customer.
---

# sc-clickpath

Two pages from one click path (Renzo, 11 Nov 2026): one for us to prepare and practise, one the customer can keep.
Both are single HTML files with the screenshots and Creatio logo inside, so they open offline and can be kept or sent.
Layout follows the Creatio **Workflow Explorer** (Renzo's preferred navigation): masthead with a stat strip, a
clickable demo-flow strip, tabs, a sticky filter rail (search, use-case chips; SC: show/hide talk track and
watch-outs, practice mode, rehearsal progress), and collapsible use cases with step rows that open to the
screenshot and words. One light Creatio brand theme.

Paths are relative to this skill's folder; plugin root = `../..`.

## Steps

1. **Cards first.** The toolkit's `creatio-demo-clickpass` skill rehearses the demo and writes `cards.json` + `shots/`
   in the deal folder (`clickpath/`). Use it; don't rebuild that here.
2. **Customer words.** Write `clickpath-customer.json` next to `cards.json`:
   `{customer, page_name, title, eyebrow, date, intro, simulated, contact, approved: false,
     sections: {UC1: "heading"}, titles: {"UC1-2": "plain title"}, cards: {"UC1-2": "what it means for them"},
     hide: [...], hide_reasons: {...}, crop: {"UC1-3": [left, top, right, bottom] as 0–1 fractions}, crop_reasons: {...},
     screens_reviewed: [...]}`.
   One or two sentences per step in their words (`../../standards/WRITING-STYLE-v0.1.md`): what it means for them,
   not where to click. Say plainly what was simulated.
3. **Build both:** `python scripts/build_clickpath.py "<deal>/clickpath/cards.json" --slug <account>` →
   `<account>-click-path-sc.html` and `<account>-click-path-customer.html` in the same folder.
4. **Text check.** The builder flags, in the customer page: stand names and URLs, schema and package names, demo
   wording (login names, runbook, reset, seed data), evidence tags, presenter cautions, pricing, vendor words and AI
   phrasing, and steps without customer words. Fix every one.
5. **Look at every screenshot** (the text check can't see inside images). Hide or crop anything showing: **other
   customers' names** (shared stands carry other demos' accounts, agents and orders), test records, logins and admin
   names, URLs, placeholders ("no screenshot for this step"), real customer data. Add each checked step to
   `screens_reviewed`. The page stays **DRAFT** until every shown screenshot is reviewed and the text check is clean.
6. **SC approval.** The SC reads the customer page and sets `"approved": true` (or `--approved`); rebuild. Only then
   can it go to the customer, typically with the follow-up email after the demo.
7. **Keep and share.** Both files stay in the deal folder (SharePoint). The SC version can also be published as a
   private Claude artifact for practice on a phone (`--fragment` writes it without the page wrapper); the customer
   version is sent as a file or published only after approval, and only when the SC asks.

## What goes where

| | SC practice version | Customer version |
|---|---|---|
| Per step | Screenshot, what to click, what you'll see, what to say, watch-outs, links | Screenshot (cropped where needed), plain title, one or two sentences on what it means for them |
| Extras | Before you start, reset, practice mode (hide the talk track and recall it), rehearsal ticks | What was simulated, who to contact |
| Never | — | Clicks, talk track, watch-outs, stand names, logins, package names, other customers, evidence tags, pricing, "SC check" lines |

## Rules

- The customer page never shows the SC check line; the DRAFT banner does that job until approval.
- Never send or publish the customer page yourself. The SC sends it.
- Example data only. If a screenshot shows real customer data, hide it and tell the SC.

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is
none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).
