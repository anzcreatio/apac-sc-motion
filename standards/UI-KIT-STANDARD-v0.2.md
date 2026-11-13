# UI kit standard v0.2: reusable, no-code, upgrade-safe custom components

> Applies to every component in `labUiKit`, the team's shared package of custom Freedom UI components. First written
> for East West Bank (12 Nov 2026), updated after the Navalo build (13 Nov 2026), where two components were built,
> installed and used live. Sources: the AI-driven development kit's `dev-custom-components` skill, Creatio Academy "Add
> the remote module to the library of the Freedom UI Designer", and what broke on the two builds. Demo bar §6 points
> here.

## 1. The components

| Component (`type`) | What it does | Set up in the designer (no code) | Status (13 Nov 2026) |
|---|---|---|---|
| Group holdings (`usr.GroupHoldings`) | One card per group (business, brand, entity) with the open record's related records: total, record count, status pill, red or amber top bar when a status needs attention; empty groups dashed | Records object, link column, group column, lookup that lists every group, title / second line / amount / status / note columns, statuses to hide, status colours (`Active=positive; Hardship=critical`), empty-card text, currency, reload-on field | **Live** on Navalo (11014108, Creatio 10.0), kit 0.1.2 |
| Decision checks (`usr.DecisionChecks`) | Each rule that routes a record: passed, not met or waiting, with detail ("$6,000 over $40,000"), limit bar and a result pill | Record object; checks list (yes/no field, field equals a value incl. `Link.Column` paths, all related records done, amount within a limit); result column and label; currency; reload-on field | **Live** on Navalo, kit 0.1.2 |
| Criteria scorer (`usr.CriteriaScorer`) | Scores a record 1–3 per criterion with descriptions; live weighted total | Criteria object, score object, link and value columns, total column. Criteria are records (name, three descriptions, weight, active, order) | Built for EWB (branch `ewb-components`, kit 0.2.0), not installed |
| Step strip (`usr.StepStrip`) | Child records as editable steps with a flag and flag text; add between, reorder | Child object, link, order, title, subtitle, flag and flag-text columns, captions | Built for EWB, not installed |
| Priority matrix (`usr.PriorityMatrix`) | Records on two axes, size by a third, drag to rescore, ranked list | Object, x, y, size, label, rank and filter columns, axis captions | Built for EWB, not installed |
| Guided review (`usr.GuidedReview`) | Section-by-section review: Keep / Change against drafted values; tells the page which section is open | Object, section and question records, output attribute | Built for EWB, not installed |
| Who's working (`usr.SessionIdentity`) | Name and role once per visit; stamps them on save and on a contribution log | Stamp columns, log object, prompt text | Built for EWB, not installed |
| Trace map (`usr.TraceMap`) | A chain of linked records left to right; highlight what a change affects | Objects, link, label and status columns | Idea (Phase 2) |

**No code for the next customer:** drag the component from **Custom components** in the Freedom UI Designer palette,
fill its settings panel, save the page. Every setting and a worked example: the kit repo `README.md`.

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
| Read-only components never write data; components that write say so in their panel | No surprises on a customer stand |
| `labUiKit` holds components only: no objects, no standard schema changes, depends only on `CrtCore` + `CrtUIv2`, JS only. Delete clio's C# scaffold (`Files/src/cs`, `Files/Libs`) after `new-ui-project` | Installs on any stand without a compile |
| Accessibility: keyboard use, ARIA labels, visible focus, text beside every colour, visually hidden state text, `role=meter` on bars; loading state; container queries for laptop and tablet | NFR practices in the dev kit |
| Strings in resource files, English first | Translation without code changes |

**Measured native look (Freedom UI profile card, Creatio 10.0):** white card, `0.8px rgba(0,0,0,.1)` border, 8px
radius, 16px 24px padding, Montserrat. Title 16/500 `#181818`, label 12/500 `#606060`, value 13/500 `#181818`.
Positive `#0C8701`, critical `#D2310D`, accent `#004FD6`.

## 3. Placing a component on a page (clio)

| Trap | Do this |
|---|---|
| `update-page` append is refused on full form pages | Save in replace mode: the existing body unchanged plus the insert; dry run first |
| The validator rejects nested `caption`, `label`, `title`, `tooltip`, `placeholder` keys as inline text | Name nested text fields something else (`heading`); top-level captions as `$Resources.Strings.<Key>` plus `resources` |
| A new item lands first in a tab and reorders the others | Set every `index` in the tab explicitly |
| A list keeps a user's old column layout after a page change | List menu ⋮ → Restore default settings |

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
= 0.1.2 (Navalo, 2 components); `ewb-components` = 0.2.0 (merged 0.1.1, lacks the 0.1.2 look).

## 5. Where things live

| What | Where |
|---|---|
| Source | Private GitHub `anzcreatio/lab-ui-kit`; working copy `C:\Projects\builds\ui-kit\` (never in a deal folder) |
| Built package, README, screenshots | SharePoint `Library/ui-kit/` (L1 since 13 Nov 2026) |
| Gallery page (Phase 2) | A sample page on the master stand with each component on sample objects |

## 6. Creatio versions

| Version | Stand | Result |
|---|---|---|
| 10.0 | 11014108-demo (Navalo) | Group holdings and Decision checks installed, placed, used live (13 Nov 2026) |
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
| v0.2 | 13 Nov 2026 | Promoted from the EWB deal folder. Two live components added; status per component; look rule changed to kit tokens with measured native fallbacks; refreshOn, read-only and naming rules; page-placement traps; build/test/ship, one-package rule; versions tested | Navalo build 13 Nov (labUiKit 0.1.0–0.1.2, CWP1–CWP7) |
| v0.1 | 12 Nov 2026 | First standard, six components planned | East West Bank (`Deals/east-west-bank-rh/06-ui-kit-standard.md`) |
