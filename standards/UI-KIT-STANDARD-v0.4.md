# UI kit standard v0.4: reusable, no-code, upgrade-safe custom components and the pages around them

> Applies to every component in `labUiKit`, the team's shared package of custom Freedom UI components. First written
> for East West Bank (12 Nov 2026), updated after the Navalo build (13 Nov 2026), where three components were built,
> installed and used live (v0.2: two components; v0.3: Flow timeline and its lessons; v0.4: pickers for every setting,
> five more components, and the look of the pages they sit on). Sources: the AI-driven development kit's `dev-custom-components` skill, Creatio Academy "Add
> the remote module to the library of the Freedom UI Designer", and what broke on the two builds. Demo bar §6 points
> here.

## 1. The components

| Component (`type`) | What it does | Set up in the designer (no code) | Status (15 Nov 2026) |
|---|---|---|---|
| Group holdings (`usr.GroupHoldings`) | One card per group (business, brand, entity) with the open record's related records: total, record count, status pill, red or amber top bar when a status needs attention; empty groups dashed | Records object, link column, group column, lookup that lists every group, title / second line / amount / status / note columns, statuses to hide, status colours (`Active=positive; Hardship=critical`), empty-card text, currency, reload-on field | **Live** on Navalo (11014108, Creatio 10.0), kit 0.5.0 |
| Decision checks (`usr.DecisionChecks`) | Each rule that routes a record: passed, not met or waiting, with detail ("$6,000 over $40,000"), limit bar and a result pill | Record object; checks list (yes/no field, field equals a value incl. `Link.Column` paths, all related records done, amount within a limit); result column and label; currency; reload-on field | **Live** on Navalo, kit 0.5.0 |
| Flow timeline (`usr.FlowTimeline`) | The record's journey: each step with who and when, time since the previous step, an open step "so far", steps not reached yet muted; header "so far" until every step is done, then "end to end"; targets per step and end to end | Record object; steps list (a date on the record, dates on related records each or latest, native approval requested and decided); who (column or fixed text); target hours per step; hide until it happens; total target; reload-on field | **Live** on Navalo application page, kit 0.5.0 (rehearsed 13 and 14 Nov) |
| Stage funnel (`usr.StageFunnel`) | Records by stage as clickable tiles with counts and a bar; the clicked stage goes to a page field so a list filters on it | Records object, stage column, stages in order, optional filter column and page field, selected-stage page field | **Live** on Navalo dealer home and performance page, kit 0.5.0 |
| Request checklist (`usr.RequestChecklist`) | What is still needed from someone: "N of M in", Needed / Received pills, asked and received times, a button that marks an item received (and can trigger an upload on the page) | Items object, link, name, status (lookup filled in), done value, requested-on and received-on dates, button text, mark on click | **Live** on Navalo portal application page, kit 0.5.0 (writes data: says so in its panel) |
| Group overlap (`usr.GroupOverlap`) | People by the combination of groups they hold with ("Payright + Taurus: 4"), headline "N of M in two or more"; or only people in one group (who to offer next), leaving out anyone with a record that meets an exclusion; click a tile to list and open them | Records object, person and group columns (lookup objects filled in), amount, combinations to show, condition rows, exclusion rows, wording | **Live** on Navalo performance page, kit 0.5.0 |
| Rate against target (`usr.RateTarget`) | Share of records meeting a condition out of a base, with a target line and "N points under target", overall and one bar per group; higher or lower is better | Records object, base and success condition rows, labels, target %, direction, group column, label for no group (e.g. Direct), bars at most | **Live** on Navalo performance page, kit 0.5.0 |
| Cycle time (`usr.CycleTime`) | Median and slowest 10% between two dates, per group, against a target; "N of M inside target" | Records object, from and to date columns, condition rows, target hours, group column | **Live** on Navalo performance page, kit 0.5.0 |
| Criteria scorer (`usr.CriteriaScorer`) | Scores a record 1–3 per criterion with descriptions; live weighted total | Criteria object, score object, link and value columns, total column. Criteria are records (name, three descriptions, weight, active, order) | Built for EWB (branch `ewb-components`, kit 0.2.0), not installed |
| Step strip (`usr.StepStrip`) | Child records as editable steps with a flag and flag text; add between, reorder | Child object, link, order, title, subtitle, flag and flag-text columns, captions | Built for EWB, not installed |
| Priority matrix (`usr.PriorityMatrix`) | Records on two axes, size by a third, drag to rescore, ranked list | Object, x, y, size, label, rank and filter columns, axis captions | Built for EWB, not installed |
| Guided review (`usr.GuidedReview`) | Section-by-section review: Keep / Change against drafted values; tells the page which section is open | Object, section and question records, output attribute | Built for EWB, not installed |
| Who's working (`usr.SessionIdentity`) | Name and role once per visit; stamps them on save and on a contribution log | Stamp columns, log object, prompt text | Built for EWB, not installed |
| Trace map (`usr.TraceMap`) | A chain of linked records left to right; highlight what a change affects | Objects, link, label and status columns | Idea (Phase 2) |

**No code for the next customer:** drag the component from **Custom components** in the Freedom UI Designer palette,
pick its settings in the panel, save the page. Every setting and a worked example: the kit repo `README.md`.

## 2. Build rules

| Rule | Why |
|---|---|
| Remote module with `@creatio-devkit/common` (`@CrtViewElement`, `@CrtInput`, `@CrtOutput`, designer definitions); devkit and Angular pinned to the clio template | The documented, supported way to extend Freedom UI |
| Data only through the devkit `Model` API (`Model.create(schema).load(...)`, forward paths as `{name, path}` attributes) and `crt.*` requests; no internal services, no hard-coded URLs | The devkit API is the contract that survives upgrades |
| Shadow DOM; never style or read Creatio's own screen elements | A Creatio restyle can't break the component, and the component can't break Creatio |
| **Look: kit tokens with native fallbacks.** Creatio's `--crt-*` theme variables are **not** set at page level, so a component styled only on them falls back to its own defaults and looks off (Navalo 0.1.1). Use `--kit-*` tokens (`shared/_kit-tokens.scss`) that read `--usr-kit-*` overrides first, then the measured native values below | Matches the native cards next to it; a theme can still override every value |
| Every setting optional with a safe default; nothing set shows **Set me up**; a new record shows **Save the record**; a load error shows a short alert inside the component, never an exception into the page | A wrong setting or an upgrade never breaks the page |
| `type` names never change; settings are added, never renamed or removed (old names still read, like `caption` → `heading` in 0.1.1); the kit carries a version | Pages built on an older kit keep working |
| A `refreshOn` input bound to a page field (`$PDS_<Column>`) so the component reloads when that field changes; a sequence guard drops stale loads | The live demo needs no Refresh click |
| Optional steps stay hidden until they happen (Flow timeline `hideUntilDone`); wording never claims "done" or "end to end" while a step is still to come | A straight-through record must not show a pending approval it will never need |
| Dates show as stored (the user's profile time zone); "so far" uses the browser clock. Present from a machine in the profile's time zone, and seed demo dates relative to the demo day (a future date sorts before a live stamp) | Otherwise an open step is off by the time-zone difference, and a rehearsal before the demo day scrambles the order |
| Read-only components never write data; components that write say so in their panel | No surprises on a customer stand |
| `labUiKit` holds components only: no objects, no standard schema changes, depends only on `CrtCore` + `CrtUIv2`, JS only. Delete clio's C# scaffold (`Files/src/cs`, `Files/Libs`) after `new-ui-project` | Installs on any stand without a compile |
| Accessibility: keyboard use, ARIA labels, visible focus, text beside every colour, visually hidden state text, `role=meter` on bars; loading state; container queries for laptop and tablet | NFR practices in the dev kit |
| Strings in resource files, English first | Translation without code changes |
| **Every setting is picked, not typed (0.5.0).** Panels use the shared picker: object from the stand's objects, column filtered by type (one step through a lookup allowed), lookup values as ticks or an ordered list, a colour per value, page fields, numbers with their unit, choices, condition rows (field, is / is not / is empty / has a value, values). A lookup column fills in its lookup object. Each picker saves the same text the component read before, and falls back to a text box when the stand can't be read | A business analyst sets a component up from drop-downs; pages built before the pickers keep working ("configuration over customisation" in RFPs) |
| A condition that leaves people out applies to the person, not the row: anyone with any record that meets it is left out of every group (Group overlap `excludePeople`) | Otherwise a customer in arrears with one business is offered a loan by another (responsible lending) |

**Measured native look (Freedom UI profile card, Creatio 10.0):** white card, `0.8px rgba(0,0,0,.1)` border, 8px
radius, 16px 24px padding, Montserrat. Title 16/500 `#181818`, label 12/500 `#606060`, value 13/500 `#181818`.
Positive `#0C8701`, critical `#D2310D`, accent `#004FD6`.

## 2b. The pages around the components (look)

A polished component on a cheap-looking page still looks cheap. These rules apply to every page we build for a demo:
home pages, dashboards and record pages (Renzo, 15 Nov 2026: "any text that has the transparent background and
therefore shows the grey like background looks cheap").

| Rule | Do this |
|---|---|
| **No text directly on the grey page background** | Every heading, subtitle and section label sits on a white card: a `crt.FlexContainer` with `color: "#FFFFFF"`, `borderRadius: "medium"`, padding medium / large, the label inside it. Applies to page titles, section headings and any explanatory line |
| One header card per page | Title (headline-3, semibold, `#0D2E4E`), one-line subtitle (body, `#606060`) and the page's buttons in **one** white card in one 12-column row; never title and subtitle on separate grid rows (that leaves an empty band) |
| Headline numbers first | Metric tiles in the top band (4 or 6 across, 2 rows tall), then work lists, then charts; never metrics under the lists |
| Quiet lists on home pages | List widgets without row numbers or row checkboxes (`features.rows.numeration: false`, `selection: false`); column headings short enough to show in full ("Still needed", not "Docs outstanding") |
| One accent colour | The same widget header colour (navy) on every list and chart title on a page; colour is for meaning (status, over target), never for variety |
| Chart colours from the four-colour palette, by meaning | Green `#4E8F6A` good, amber `#C99A3E` needs approval or watch, red `#B5534E` trouble, navy `#1B365D` neutral; one series per category value |
| Slots fit their cards | Set each `rowSpan` to the card's real height (a component or list card does not stretch to fill its slot, so a tall slot leaves a grey band); charts and lists at least 6 rows; check the whole page by scrolling, not just the top |
| Section headings on a long dashboard | One white heading card per section, then that section's cards; ideas beyond the brief under their own heading card |
| Check before calling it done | Look at the page at 1440 x 900, top to bottom: anything on grey, any empty band, any second colour without meaning is a fix |

## 3. Placing a component on a page (clio)

| Trap | Do this |
|---|---|
| `update-page` append is refused on full form pages | Save in replace mode: the existing body unchanged plus the insert; dry run first |
| The validator rejects nested `caption`, `label`, `title`, `tooltip`, `placeholder` keys as inline text | Name nested text fields something else (`heading`); top-level captions as `$Resources.Strings.<Key>` plus `resources` |
| A new item lands first in a tab and reorders the others | Set every `index` in the tab explicitly |
| A list keeps a user's old column layout after a page change | List menu ⋮ → Restore default settings |
| A `move` on a component the same body inserts is discarded | Set the insert's own `parentName` and `index`; keep `move` for template components (e.g. `GeneralInfoTab`) |
| `update-page` reports an external modification after `create-page-business-rules` (rules change the schema but not clio's baseline) | Re-run `get-page`, confirm the live body equals your base plus your change, then pin `checksum` to the live value and pass `target-schema-uid`, with the SC's OK |
| Next-step guidance per stage | Native: one banner per stage (FlexContainer + two labels, hidden by default) and a show/hide page-rule pair per banner; no component needed |

## 4. Build, test, ship

| Step | Command or rule |
|---|---|
| Test | `npx ng test` (the project's Jest builder). Plain `npx jest` fails most suites: wrong runner, not a fault |
| Build | `npx ng build` → `packages/labUiKit/Files/src/js/ui_kit` |
| Install | Renzo's yes per stand. `push-workspace` (application installer): package locked, about a second, no compile, no restart. An early "500" poll in the log is harmless |
| Check | In the designer palette (**Custom components**), then live on a page with real data; zoneless on and off |
| Export | `clio pull-pkg labUiKit -e <env>` (CLI; clio MCP has no pull tool) → SharePoint `Library/ui-kit/packages/`. The `Files/obj` folder in the export is made by the stand; ignore it |

**One package, one version line.** Every branch ships the same package UId (`bd7e46b4-…`), so installing one branch
replaces the other on a stand. Merge before installing on a stand that has another branch's components. Today: `main`
= 0.5.0 (Navalo, 8 components, pickers); `ewb-components` = 0.3.x-0.4.x (EWB components, lacks 0.1.2-0.5.0). Version
numbers on `main` skip what the EWB branch used.

## 5. Where things live

| What | Where |
|---|---|
| Source | Private GitHub `anzcreatio/lab-ui-kit`; working copy `C:\Projects\builds\ui-kit\` (never in a deal folder) |
| Built package, README, screenshots | SharePoint `Library/ui-kit/` (L1 since 13 Nov 2026) |
| Gallery page (Phase 2) | A sample page on the master stand with each component on sample objects |

## 6. Creatio versions

| Version | Stand | Result |
|---|---|---|
| 10.0 | 11014108-demo (Navalo) | Group holdings, Decision checks and Flow timeline installed, placed, used live; full rehearsal of straight-through, approval and lodgement (13 and 14 Nov 2026). 0.5.0 installed 15 Nov: all eight components on pages; pickers built and unit-tested, not yet opened in the live designer |
| 10.1 | 11014930-demo (EWB) | Not installed yet |

Not yet proven: a first install on a stand that never had `labUiKit` (next: master stand `11011710-demo`, which moves
the kit to L3), keyboard-only pass, zoneless off.

## 7. After every Creatio upgrade (10 minutes)

1. Open the gallery page (or one real page per component): it loads, shows data and, for writing components, saves one
   change.
2. Record the Creatio version in §6 and the kit README. If anything fails, fix the kit once and republish to the library.

## 8. Not promised

- Every future Creatio release: we follow the supported route and smoke-test after upgrades.
- Right-to-left layouts and languages beyond English.

## 9. Changes

| Version | Date | Change | Evidence |
|---|---|---|---|
| v0.4 | 15 Nov 2026 | Section 2b page look rules (no text on the grey page background, one header card, metrics first, quiet lists, one accent colour, palette chart colours by meaning, slots fit their cards); every setting picked not typed (0.5.0 pickers); person-level exclusion; five more components in section 1; versions 0.5.0 | Navalo 14-15 Nov: plan 15 build (labUiKit 0.5.0) and Renzo's "looks cheap" feedback on the lending overview (`Lessons/feedback/2026-11-15-renzo-huruiti-home-pages-look-cheap.md`) |
| v0.3 | 13 Nov 2026 | Flow timeline added (live); rules for optional steps, honest wording and time zones; traps: moves on inserted components, stale baseline after page rules; native next-step banners as the pattern; versions 0.1.5 | Navalo FWP1–FWP6, 13 Nov (labUiKit 0.1.3–0.1.5) |
| v0.2 | 13 Nov 2026 | Promoted from the EWB deal folder. Two live components added; status per component; look rule changed to kit tokens with measured native fallbacks; refreshOn, read-only and naming rules; page-placement traps; build/test/ship, one-package rule; versions tested | Navalo build 13 Nov (labUiKit 0.1.0–0.1.2, CWP1–CWP7) |
| v0.1 | 12 Nov 2026 | First standard, six components planned | East West Bank (`Deals/east-west-bank-rh/06-ui-kit-standard.md`) |
