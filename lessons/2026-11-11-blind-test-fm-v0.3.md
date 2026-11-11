# Blind test: sc-first-meeting (FM v0.3) on H&G and Suntory (11 Nov 2026)

Two fresh agents, each given only the skill, the standard, `knowledge/`, the Slide-library catalogue and the deal's
first-call transcript. Outputs: `tests/blind/<deal>/` (`deck.json`, `01-fm-prep.md`, `blind-deck-v2.pptx`, PNGs).
About 35 minutes and 25–38 tool steps each; about 4 hours of light configuration planned for each.

## Result against the decks actually presented (Claude's reading; Renzo to confirm)

| | H&G | Suntory |
|---|---|---|
| Coverage of the six questions | 3 answered, 2 partly, 1 not asked | 3 answered, 2 partly, 1 not asked |
| Top pain matches what was presented | Yes: manage by site, win the whole house | Yes: right information before the visit (Tom's "top 10 things") |
| Hypothesis vs presented | Near identical (site wish list, gaps, diary) | Presented deck had none; blind adds one (one outlet view, briefed before, captured after) |
| Slides Claude rates presentable after wording edits | 11 of 13 | 10 of 13 |
| What blind had that presented didn't | Dated next steps with owners; AI in every component | Hypothesis slide, solution summary, captured-after-visit (debrief) |
| What presented had that blind didn't | Roadmap slide, live-change slide, screen slides (need the build) | Licensed-visit flow, direct + partner orders (blind put indirect orders in "still to show"), "systems stay" slide |

**Caveat:** the H&G run was contaminated. The deck standard cites H&G slides and titles, and the library README
names the H&G build board. The Suntory run is mostly clean: the library notes mention "outlet 360" and "visit briefing".

## Defects found and fixed the same day

| Defect | Fix |
|---|---|
| 40 pt titles wrapping into the content (unreadable on 2 slides) | Builder shrinks 2-line titles to 30 pt and warns at 3 lines |
| Component right-hand column overflow not checked | Warning added |
| One `shown` flag couldn't say "platform today, AI next time" | `ai_shown` added (second chip) |
| Skill asked for 3 questions on a timeline that shows 1 | One on the slide, two in the notes |
| Standard example still said v0.1 / creatio-2026; 5 today/want rows don't fit with timing | Fixed; 4 rows with timing |
| Coverage scoring undefined | Answered 1, partly 0.5, volunteered counts, opener separate |
| No rule for our own AE/BDR claims | Never evidence; listed under "claims to check" |
| No rule for a meeting today or already past | No new config; brief becomes the next-session plan |
| "Last 18 months" blocked company basics | News 18 months; basics any date |
| `library/catalogue.json` missing; broken links in `knowledge/` | Catalogue created (empty + 3 harvest candidates); links fixed |

## Verdict (Renzo, 11 Nov 2026)

After v3 (natural wording, a "What we've set up for today" slide, stand screenshots with summaries, the whole platform
set 01–04): **"I would use these latest versions of the deck as long as the full platform story is in them."** Pass.

## Open (for pack owners / Renzo)

- **No FMCG field-sales / retail-execution journey** in any pack (Suntory), and **no trade-merchant / distributor
  pack** (H&G: Manufacturing excludes them; Core is thin on quote vs sale). Two of our first three deals hit this.
- Slide-library catalogue has no recommended slide set per track; agents picked by title (both chose platform
  overview 1, 3, 6 and skipped the "10x" slides).
- Future blind tests: remove deal names from standard examples, or test on a deal the kit has never seen.
