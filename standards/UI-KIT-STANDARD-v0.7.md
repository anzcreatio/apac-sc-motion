# UI kit standard v0.7: reusable, no-code, upgrade-safe custom components and the pages around them

> Applies to every component in `labUiKit`, the team's shared package of custom Freedom UI components. First written
> for East West Bank (12 Nov 2026), updated after the Navalo build (13 Nov 2026), where three components were built,
> installed and used live (v0.2: two components; v0.3: Flow timeline and its lessons; v0.4: pickers for every setting,
> five more components, and the look of the pages they sit on; v0.5, 18 Nov 2026: §2c native patterns harvested from a
> clean Creatio 10 stand, and the tokens rule corrected; v0.6, 19 Nov 2026: §2d, the rules from every Freedom UI page
> of Creatio Academy › Front-end development, checked against the kit). Sources: the AI-driven development kit's
> `dev-custom-components` skill, Creatio Academy front-end guides (version 10, 37 pages, §2d), and what broke on the
> builds. Demo bar §6 points here.

## 1. The components

| Component (`type`) | What it does | Set up in the designer (no code) | Status (19 Nov 2026) |
|---|---|---|---|
| Group holdings (`usr.GroupHoldings`) | One card per group (business, brand, entity) with the open record's related records: total, record count, status pill, red or amber top bar when a status needs attention; empty groups dashed | Records object, link column, group column, lookup that lists every group, title / second line / amount / status / note columns, statuses to hide, status colours (`Active=positive; Hardship=critical`), empty-card text, currency, reload-on field | **Live** on Navalo (11014108, Creatio 10.0), kit 0.5.0 |
| Decision checks (`usr.DecisionChecks`) | Each rule that routes a record: passed, not met or waiting, with detail ("$6,000 over $40,000"), limit bar and a result pill | Record object; checks list (yes/no field, field equals a value incl. `Link.Column` paths, all related records done, amount within a limit); result column and label; currency; reload-on field | **Live** on Navalo, kit 0.5.0 |
| Flow timeline (`usr.FlowTimeline`) | The record's journey: each step with who and when, time since the previous step, an open step "so far", steps not reached yet muted; header "so far" until every step is done, then "end to end"; targets per step and end to end | Record object; steps list (a date on the record, dates on related records each or latest, native approval requested and decided); who (column or fixed text); target hours per step; hide until it happens; total target; reload-on field | **Live** on Navalo application page, kit 0.5.0 (rehearsed 13 and 14 Nov) |
| Stage funnel (`usr.StageFunnel`) | Records by stage as clickable tiles with counts and a bar; the clicked stage goes to a page field so a list filters on it | Records object, stage column, stages in order, optional filter column and page field, selected-stage page field | **Live** on Navalo dealer home and performance page, kit 0.5.0 |
| Request checklist (`usr.RequestChecklist`) | What is still needed from someone: "N of M in", Needed / Received pills, asked and received times, a button that marks an item received (and can trigger an upload on the page) | Items object, link, name, status (lookup filled in), done value, requested-on and received-on dates, button text, mark on click | **Live** on Navalo portal application page, kit 0.5.0 (writes data: says so in its panel) |
| Group overlap (`usr.GroupOverlap`) | People by the combination of groups they hold with ("Payright + Taurus: 4"), headline "N of M in two or more"; or only people in one group (who to offer next), leaving out anyone with a record that meets an exclusion; click a tile to list and open them | Records object, person and group columns (lookup objects filled in), amount, combinations to show, condition rows, exclusion rows, wording | **Live** on Navalo performance page, kit 0.5.0 |
| Rate against target (`usr.RateTarget`) | Share of records meeting a condition out of a base, with a target line and "N points under target", overall and one bar per group; higher or lower is better | Records object, base and success condition rows, labels, target %, direction, group column, label for no group (e.g. Direct), bars at most | **Live** on Navalo performance page, kit 0.5.0 |
| Cycle time (`usr.CycleTime`) | Median and slowest 10% between two dates, per group, against a target; "N of M inside target" | Records object, from and to date columns, condition rows, target hours, group column | **Live** on Navalo performance page, kit 0.5.0 |
| Criteria scorer (`usr.CriteriaScorer`) | Scores a record 1–3 per criterion with descriptions; live weighted total | Criteria object, score object, link and value columns, total column. Criteria are records (name, three descriptions, weight, active, order) | **Live** on EWB (11014930, Creatio 10.1), kit 0.6.1 (`ewb-components`; native tokens, pickers, row cap) |
| Step strip (`usr.StepStrip`) | Child records as editable steps with a flag and flag text; add between, reorder | Child object, link, order, title, subtitle, flag and flag-text columns, captions | **Live** on EWB (11014930, Creatio 10.1), kit 0.6.1 (`ewb-components`; native tokens, pickers, row cap) |
| Priority matrix (`usr.PriorityMatrix`) | Records on two axes, size by a third, drag to rescore, ranked list | Object, x, y, size, label, rank and filter columns, axis captions | **Live** on EWB (11014930, Creatio 10.1), kit 0.6.1 (`ewb-components`; native tokens, pickers, row cap) |
| Guided review (`usr.GuidedReview`) | Section-by-section review: Keep / Change against drafted values; tells the page which section is open | Object, section and question records, output attribute | **Live** on EWB (11014930, Creatio 10.1), kit 0.6.1 (`ewb-components`; native tokens, pickers, row cap) |
| Who's working (`usr.SessionIdentity`) | Name and role once per visit; stamps them on save and on a contribution log | Stamp columns, log object, prompt text | **Live** on EWB (11014930, Creatio 10.1), kit 0.6.1 (`ewb-components`; native tokens, pickers, row cap) |
| Help panel (`usr.HelpPanel`) | A slim "how this works" line that opens the page's guidance, with a User guide link (`guideUrl`, site paths or https only) | Text, guide link and label | **Live** on EWB (11014930, Creatio 10.1), kit 0.6.1 (`ewb-components`; native tokens, pickers, row cap) |
| Card tiles (`usr.CardTiles`) | One tile per card or request with its status; counts a sent card, splits own cards from other units' | Records object, date and owner columns, statuses | **Live** on EWB (11014930, Creatio 10.1), kit 0.6.1 (`ewb-components`; native tokens, pickers, row cap) |
| Map (`usr.GeoMap`) | Records with latitude/longitude on an OpenStreetMap map (web only). Area map: up to 3 layers, heat, area borders, filters, outside-the-area rings, bars, owner comparison. Near a point: radius list from a click, GPS or named points. Record check on a record page: duplicates nearby and at the same point, value benchmark, GPS, address search, pin to address, optional stored result | Layers (object, latitude/longitude, name, colour-by with colours, owner, date, area, filters, pop-up, photo, shape); areas (object, GeoJSON border, centre); periods, bars, share, reached condition; radii and named points; record check (layer, radius, same point, value/date columns, tolerance, rules object, address search, up to 5 store columns); page fields | **Published** in `main` (kit 0.7.0 to 0.8.3, 19 Nov 2026). Tested on clean82 (11014982, 18 Nov 2026): BPD Bali Peta Cabang and the collateral check reproduced from settings only, numbers identical to `usr.BpdMap`. 19 Nov: Leaflet loads only on a page with a map (own 148 KB chunk); address search off unless set (it sends addresses outside Creatio); colours hex or palette names only; open-record link fixed (0.8.1). Set-up guide: kit `GEO-MAP-README.md` |
| Record inbox (`usr.RecordInbox`) | The records waiting for the signed-in user (or a shared queue) on any object: count, oldest, age against a target with text, up to three actions per row that each run a named business process; comment box in the row, optional native confirmation, "already handled" re-check, focus to the next row, Show more | Object; queue condition rows (sent to the server); assigned-to column + who (contact, user, company, nobody); optional link to the open record; title and up to 4 detail columns; waiting-since date + target hours; sort; page size; per action: button, process, record parameter, comment parameter + label + needed, confirm, style, done text; reload-on field | **Published** (kit 0.8.3, 19 Nov 2026, `Library/ui-kit/packages/labUiKit-0.8.3-2026-11-19.zip`). Live on clean82 gallery (`UsrUiKitGallery`: home page on Activity and Case, portal desktop for external users): every action, the guards, keyboard-only pass, portal user, request budget (2f, 2g). Writes data through processes, which must check rights themselves (2g) |
| Trace map (`usr.TraceMap`) | A chain of linked records left to right; highlight what a change affects | Objects, link, label and status columns | Idea (Phase 2) |

**No code for the next customer:** drag the component from **Custom components** in the Freedom UI Designer palette,
pick its settings in the panel, save the page. Every setting and a worked example: the kit repo `README.md`.

## 2. Build rules

| Rule | Why |
|---|---|
| Remote module with `@creatio-devkit/common` (`@CrtViewElement`, `@CrtInput`, `@CrtOutput`, designer definitions); devkit and Angular pinned to the clio template | The documented, supported way to extend Freedom UI |
| Data only through the devkit `Model` API (`Model.create(schema).load(...)`, forward paths as `{name, path}` attributes) and `crt.*` requests; no internal services, no hard-coded URLs | The devkit API is the contract that survives upgrades |
| Shadow DOM; never style or read Creatio's own screen elements | A Creatio restyle can't break the component, and the component can't break Creatio |
| **Look: kit tokens chained to Creatio's tokens (v0.5).** Each `--kit-*` token (`shared/_kit-tokens.scss`) reads `--usr-kit-*` first, then the matching Creatio token (§2c), then the measured value: `var(--usr-kit-x, var(--crt-…, #measured))`. Creatio 10 does set its tokens at page level (primitives on `:root`, colours on `body.freedom-theme`), and they reach inside our Shadow DOM (tested 18 Nov 2026). Navalo 0.1.1 looked off because it used names that don't exist (`--crt-color-primary`, `--crt-font-family`, `--crt-border-radius-medium`, `--crt-color-surface` are all empty) | Matches the native cards next to it, follows a customer's theme and dark mode, and a page can still override every value |
| Every setting optional with a safe default; nothing set shows **Set me up**; a new record shows **Save the record**; a load error shows a short alert inside the component, never an exception into the page | A wrong setting or an upgrade never breaks the page |
| `type` names never change; settings are added, never renamed or removed (old names still read, like `caption` → `heading` in 0.1.1); the kit carries a version | Pages built on an older kit keep working |
| A `refreshOn` input bound to a page field (`$PDS_<Column>`) so the component reloads when that field changes; a sequence guard drops stale loads | The live demo needs no Refresh click |
| Optional steps stay hidden until they happen (Flow timeline `hideUntilDone`); wording never claims "done" or "end to end" while a step is still to come | A straight-through record must not show a pending approval it will never need |
| Dates show as stored (the user's profile time zone); "so far" uses the browser clock. Present from a machine in the profile's time zone, and seed demo dates relative to the demo day (a future date sorts before a live stamp) | Otherwise an open step is off by the time-zone difference, and a rehearsal before the demo day scrambles the order |
| Read-only components never write data; components that write say so in their panel | No surprises on a customer stand |
| `labUiKit` holds components only: no objects, no standard schema changes, depends only on `CrtCore` + `CrtUIv2`, JS only. Delete clio's C# scaffold (`Files/src/cs`, `Files/Libs`) after `new-ui-project` | Installs on any stand without a compile |
| Accessibility: keyboard use, ARIA labels, visible focus (the native ring, §2c), `aria-expanded` on anything that collapses (native expansion panels leave it out; we don't), text beside every colour, visually hidden state text, `role=meter` on bars; loading state; container queries for laptop and tablet | NFR practices in the dev kit |
| Strings in resource files, English first | Translation without code changes |
| **Every setting is picked, not typed (0.5.0).** Panels use the shared picker: object from the stand's objects, column filtered by type (one step through a lookup allowed), lookup values as ticks or an ordered list, a colour per value, page fields, numbers with their unit, choices, condition rows (field, is / is not / is empty / has a value, values). A lookup column fills in its lookup object. Each picker saves the same text the component read before, and falls back to a text box when the stand can't be read | A business analyst sets a component up from drop-downs; pages built before the pickers keep working ("configuration over customisation" in RFPs) |
| A condition that leaves people out applies to the person, not the row: anyone with any record that meets it is left out of every group (Group overlap `excludePeople`) | Otherwise a customer in arrears with one business is offered a loan by another (responsible lending) |

**Measured native look (Freedom UI profile card, Creatio 10.0):** white card, `0.8px rgba(0,0,0,.1)` border, 8px
radius, 16px 24px padding, Montserrat. Title 16/500 `#181818`, label 12/500 `#606060`, value 13/500 `#181818`.
Positive `#0C8701`, critical `#D2310D`, accent `#004FD6`. Full set of tokens and patterns: §2c.

## 2c. Native patterns (harvested 18 Nov 2026)

Read-only harvest of a clean Creatio 10 stand (11014982, Sales Enterprise). It covered 14 native page schemas
(Contacts, Accounts, Opportunities, Leads, Cases and Orders form pages, three list pages, five page templates) and
measured the rendered Contacts list, Contacts form and the home page. Only what the stand shows from the outside:
schemas, computed styles, ARIA and CSS tokens. No compiled Creatio code was read. Check again on each major version.

### Tokens to use (exact names; anything else is empty)

| Group | Tokens (value on this stand) |
|---|---|
| Spacing (`:root`) | `--crt-spacing-0` 0 · `-50` 2 · `-100` 4 · `-150` 6 · `-200` 8 · `-250` 10 · `-300` 12 · `-400` 16 · `-500` 20 · `-600` 24 · `-700` 28 · `-800` 32 · `-900` 36 · `-1000` 40 px |
| Radius (`:root`) | `--crt-radius-0` 0 · `-50` 2 · `-100` 4 · `-150` 6 · `-200` 8 · `-250` 10 · `-300` 12 · `-400` 16 · `-600` 24 · `-800` 32 · `-infinite` 999 px |
| Font size (`:root`) | `--crt-font-size-50` 10 · `-100` 12 · `-200` 13 · `-300` 14 · `-400` 16 · `-500` 18 · `-600` 20 · `-700` 24 · `-800` 28 · `-900` 32 px |
| Line height (`:root`) | `--crt-line-height-100` 16 · `-200` 18 · `-300` 20 · `-400` 24 · `-600` 32 · `-700` 36 px |
| Weight (`:root`) | `--crt-font-weight-regular` 400 · `-medium` 500 · `-semi-bold` 600 · `-bold` 700 |
| Font (theme) | `--crt-font-family-body`, `--crt-font-family-heading` (Montserrat) |
| Text (theme) | `--crt-color-text-body` #181818 · `-heading` #0d2e4e · `-muted` #606060 · `-disabled` #757575 · `-link` #004fd6 · `-link-hover` #0041b5 · `-success` #0b8500 · `-error` #d2310d · `-accent` #ff4013 |
| Surfaces (theme) | `--crt-color-background-base` #fff · `-interaction-hover` #eff4fb · `-interaction-selected` #e3ebfa · `-primary` #004fd6 · `-primary-soft` #e3ebfa · `-success-soft` #e6f0e5 · `-error-soft` #fbe9e5 · `-disabled-subtle` #ededed |
| Borders (theme) | `--crt-color-border-base` #dfdfdf · `-muted` #ededed · `-selected` #004fd6; card border `--container-border-color` rgba(0,0,0,.1) |
| Icons (theme) | `--crt-color-icon-base` #0d2e4e · `-action-hover` #004fd6 · `-muted` #606060 · `-success` · `-error` |
| Palette (theme) | 18 named colours, each with `-hover` and `-pastel`: `blue`, `celestial-blue`, `light-blue`, `navy-blue`, `violet`, `purple`, `coral`, `red`, `bright-red`, `orange`, `orange-red`, `green`, `dark-green`, `light-green`, `turquoise`, `dark-turquoise` (e.g. `--crt-color-violet` #7848ed) |
| Focus | `--focus-outline-outer-color` #0d2e4e, `--focus-outline-inner-color` white |

Every colour has a twin under `.dark-mode`, so a component on these tokens follows dark mode with no extra work. Native
components write them with a fallback, e.g. `var(--crt-color-background-base, var(--background))`: do the same.

**Rehearsed 18 Nov 2026 (kit 0.5.5, Stage funnel on clean82, live data):** card, border, radius, padding and title
match the native card exactly; the keyboard focus ring is the native one and keeps the tile's 8px radius; tokens are
read live (track `#e1e5e9` from `--crt-color-background-secondary-soft`). With `.dark-mode` on the body the kit card
turns dark with the native card. But Creatio's dark semantic colours look like inversions (success `#f47aff`, pink),
so before a customer uses dark mode, check status colours on that stand. Rehearsal traps: changing only the `#` part
of the URL doesn't reload the kit's JS, so use a real reload (a new `?r=` query); a fresh load straight onto a blank
page's `#Section/...` hangs on the splash, so load `#Desktop` first.

### Component patterns (measured)

| Element | Native look | Our rule |
|---|---|---|
| Card / container | White, 1px `rgba(0,0,0,.1)` border, radius 8, padding 16 × 24, gap 24 (schema: `color: "primary"`, `borderRadius: "medium"`, padding `medium`/`large`) | `@include card`; padding `--crt-spacing-400` × `-600` |
| Page title | h1 24/600 `text-heading`, 32 line | Not ours: the page header owns it |
| Card title | 16/500 `text-body`, 20 line | `@include title` |
| Section title (expansion panel) | 14/500 `text-heading`, collapse arrow before it, + / refresh / ⋮ / search icons after | Collapsible blocks copy this order |
| Field | 52px tall with label above: label 12/500, value 13/500 `text-body` | `@include label` / `value` |
| Link | 13/500 `text-link`, underline on hover only | Same |
| List | Rows and header 40px; header 12/400 `text-muted`; cells 14/400 `text-body`, padding 0 × 6 | Lists inside a component use 40px rows |
| Chip / status | Pill radius 16, padding 1 × 8, 13/500; text in a palette colour on the same colour at 20% (e.g. violet on violet 20%); score chips solid with white text | `@include pill` uses palette tokens: no new colours |
| Button | 32px, radius 4, padding 0 × 16, 14/500; primary solid #004fd6 white text; secondary text `text-heading`, no fill | Same sizes; one primary button per component at most |
| Icon button | 32 × 32, icon only, hover fill `background-interaction-hover` | `@include ghost-button` |
| Focus | Two inset rings: 1px `#0d2e4e` outside, 2px white inside, radius 4, no outline | `@include focus-ring` on every focusable element |
| Tabs | 36px, UPPERCASE 14/500; selected `text-heading` with underline, others `text-link`; `role=tab` + `aria-selected` | Tabs inside a component copy this |
| Home page widget | Glass card `rgba(24,24,24,.8)` + blur, radius 8; title 14–16/500 white; metric 28/600 white | A component for a home page needs a glass variant (white text) or sits in a white card (§2b) |
| Page loading | Glass page with a small centred logo skeleton | Component loading: a skeleton in the component's own shape, never a spinner over the page |

### Schema conventions (how native pages are put together)

| Pattern | What native pages do | Use it for |
|---|---|---|
| Size and spacing words | `gap`, `padding`, `borderRadius` take `none` / `small` / `medium` / `large`, never pixels | Our designer settings offer the same words, not pixel boxes |
| Layout | `crt.GridContainer` with `minmax(32px, 1fr)` columns and `minmax(max-content, 32px)` rows; `crt.FlexContainer` with `wrap: nowrap` and `alignItems: stretch` | Placing our component (§3) |
| Text | `crt.Label` with `labelType` (`headline-1/3`, `body`, `body-large`), `labelThickness`, `labelColor: auto` | Labels around our components |
| Captions | All from resources (`#ResourceString(...)#`), never literal text in the body | Already rule: strings in resource files |
| Data source names | `PDS` for the page record; list data sources `<Name>DS`; list attribute `<Name>` with `<Name>_PredefinedFilter` and the search filter as `filterAttributes`, `loadOnChange: true` | Name our data attributes the same way so they read like native ones |
| Hide when empty | Attribute with converter `crt.HideComponentWithNoItems` and a trigger on the list | A component with nothing to show hides itself or says so; it never shows an empty frame |
| Actions | Buttons and menu items call `crt.*` requests (`crt.CreateRecordRequest`, `crt.OpenPageRequest`, `crt.RunBusinessProcessRequest`, `crt.LoadDataRequest`, `crt.ExportDataGridToExcelRequest`); `clickMode: menu` for a button with a menu | Our components raise the same requests, so page handlers and business rules still apply |
| Icon buttons | `iconPosition: only-icon` (27 of 43 buttons), sizes `medium` or `large` | Header tools in our components: icon only, with an ARIA label |

## 2d. Academy rules (front-end guides, version 10, read 19 Nov 2026)

All 37 Freedom UI pages under Academy › Development on Creatio platform › Front-end development (`/guides/dev/sitemap.xml`;
the 24 Classic UI pages don't apply). Kit column = `main` 0.5.5 checked against the rule on 19 Nov.

### Build route

| Rule (Academy page) | Kit |
|---|---|
| Deferred remote-module format: `main.ts` exports `RemoteEntryDefinition`, webpack `uniqueName`, `commonChunk: true`, runtime and design features load separately; no `@CrtInterfaceDesignerItem` on components (Migrate to deferred format; legacy = built for 8.3.3 and earlier) | ✅ |
| Designer entry per component in `runtime.designer-definitions.ts`: same `type`, `toolbarConfig` (caption + **icon, required**), `defaultPropertyValues`, `propertiesPanel` (Freedom UI remote module; Localization) | ✅ |
| Components `ViewEncapsulation.ShadowDom` + `ChangeDetectionStrategy.OnPush`; `@CrtInput` with `@Input`, `@CrtOutput` with `@Output` + `EventEmitter`; field-like components take `@CrtValidationInput` (`CrtValidationInfo`) (Implement Freedom UI component) | ✅ ShadowDom + OnPush 8 of 8 |
| An `AGENTS.md` at the project root pointing at the guides bundled in `node_modules/@creatio-devkit/common` and `@creatio/interface-designer` (every example's first step) | ✅ |
| No libraries that register as globals (lodash and the like) under Module Federation (Freedom UI remote module) | Rule |
| Pin versions **exactly** (no `^`): Angular, `@creatio-devkit/common`, `@creatio/interface-designer`, `class-transformer`; record them per Creatio version in §6 (no Academy page gives versions) | ✅ pinned exactly (kit 0.6.2) |
| Images and icons through `DomSanitizer.bypassSecurityTrustResourceUrl()`; Base64 when a stand may have no internet (Assets in the remote module) | Rule (kit uses inline SVG) |

### Change detection: zoneless

Creatio 10.2 has zoneless as a beta (`EnableZoneless` additional feature); **10.2.1 turns it on by default**
(Migrate to zoneless). Every component must work without zone.js:

| Rule | Kit |
|---|---|
| Angular 20+ with `provideZonelessChangeDetection()`; no `zone.js` in polyfills (build and test); no `NgZone` events | ✅ Angular 22, provider in `remote-app-context.ts` |
| Await every fetch, Model call and `HandlerChainService.process()`; no `setTimeout` waits or timer loops to wait for the page; stop page-lifetime timers in `crt.HandleViewModelDestroyRequest` / `ngOnDestroy`; `try`/`finally` to reset a mask or a locked button | Rule; check on every review |
| NG0908 "requires Zone.js" in the console = a component isn't zoneless-ready: migrate it, don't import zone.js (that intercepts the whole page) | Rule |
| Test: a 10.2 stand with `EnableZoneless` on: clicks, saves, close the page, run a process; nothing runs on a closed page, no new console errors | ⚠️ Not yet done: needs a 10.2 stand |

### Settings panels (Academy: "setup areas")

| Rule (Setup area basics; Collection-based setup area; Error handling) | Kit |
|---|---|
| Panel `implements PropertyPanel` from `@creatio/interface-designer`, is a `@CrtViewElement`, registered in the design feature (`design-feature.module`, `design.feature-activation`, `design.feature-definition`) and linked by `propertiesPanel` | ✅ (`kit-panel-base.ts`) |
| The panel instance is reused across components of the same type: reload all state on every `viewNodeEditor` setter call | ✅ |
| `getPropertyValue` / `setPropertyValue` are async: await them; clear with `{ constant: null }`; read with `value ?? default` | ✅ |
| Wrap the panel in `crt-interface-designer-properties-panel-wrapper` and use `@creatio/interface-designer/styles/properties-panel-styles`; panel encapsulation `Emulated` (Academy examples) | Wrapper ✅; panels stay `ViewEncapsulation.None` **on purpose**: every own selector is `.kit-` prefixed (nothing leaks into the Designer) and `Emulated` would cut the panel styles off from the shared picker inside it |
| **Show errors in the panel**, not only the console: catch the specific `SchemaValidationError` subclasses first (`DataSourceAlreadyExists`, `ViewModelAttributeAlreadyExists`, `BoundViewModelAttributeRemoval`, …), fall back to `SchemaValidationError`, rethrow the rest; message in a `role="alert"` area, e.g. "Changes are not applied: …" | ✅ shown in the panel (`kit-panel-errors.ts`, kit 0.6.2) |
| Call `canRemoveAttribute` / `canRemoveDataSource` before removing; check `getDataSourceEditor` / `getAttributeConfig` before creating (create throws if it exists); can't remove → say so as information, not an error | Rule (kit creates only the `recordId` binding today) |
| Check required settings before writing anything that creates schema objects; an Apply button only when applying creates data sources or attributes (saving constants on change is fine) | ✅ constants save on change |
| **Since 10.1 the Designer saves only properties that differ from the default** (`UseViewConfigDefaultsFilter`): the component must apply the same default as `defaultPropertyValues` when a setting is missing from the schema (Client schema overview) | Rule: §2 "every setting optional with a safe default" covers it; keep the two defaults identical |

### Data

| Rule (Data sources; Model class; Best practices for data fetching) | Kit |
|---|---|
| Our route: `Model.create(...)` + `load({ attributes, parameters, options })` inside the component. Academy's other route: a page data source + an `isCollection` attribute bound with `bindToAttribute` (follows the page's filters and the data-source designer). Use that route when a list must follow page filters | Model route ✅ |
| Select only the columns you need; **cap the rows** (paging `rowCount`) on anything that loads a whole object; sort in the query, not in code | ✅ row cap on whole-object loads (0.6.1); Stage funnel counts on the server (0.6.2) |
| Independent loads in parallel (`Promise.all`); share one in-flight promise for the same query; a timeout on slow calls | Rule (`refreshOn` sequence guard stays) |
| Before a write, `canSave` / `canDelete`: disable the action and say why instead of failing | **Corrected 0.8.3:** `canSave` on a `Model.create` model only answers "may create", so it is used before inserts only; updates rely on the server's record rights ("not saved" when nothing changed, 0.6.4) and deletes on `canDelete` with the record Id (2g) |
| `update` / `delete` pick the record by filter: always filter on the primary key only | ✅ (`byId`) |
| What a refused write returns is not documented: check the result **and** catch a rejected promise (our `ensureOk`, go-live test E5) | EWB branch ✅; `main` gets it when EWB merges back |
| Calculated attributes (`from`, `converter`, `filter`, `triggers`, `triggersOptions.debounce`) for page-side derived values instead of handler code; read-only, lazy; `crt.Input` can't bind to them | Use on pages around components |
| Collection callbacks (`registerOnCollectionChangeCallback`): register on init, keep the function reference, unregister on destroy (unregistering an unknown callback throws), treat a bulk add (10+) as a refresh | Rule if a component listens to a page list |

### Strings, icons, page logic

| Rule | Kit |
|---|---|
| Remote-module strings in `src/assets/i18n/*.json` (ngx-translate or own service), language from `SysValuesService.loadSysValues().userCulture`; **designer definitions are not translated automatically** in the deferred format: the module returns translated captions and defaults (Localization). Page-schema captions stay `#ResourceString` / `$Resources.Strings` | ⚠️ No i18n yet: English strings in code. Needed before a non-English customer |
| Palette icons: SVG, transparent, trim 72 × 64 (live area 56 × 50), stroke 2.5 px, corner radius 3 px, Academy palette (#70ACEE live area, #004FD6, #FF4013, #181818 …); show the function, not the layout (Requirements for icons) | Size ✅ 72 × 64; check stroke, radius and palette per icon |
| Custom converters `@CrtConverter`, request handlers `@CrtRequestHandler`, validators `@CrtValidator` (sync, `validate()` returns `null` or `{ error: { message } }`) register in the runtime module **and** `discovery`. Type prefix `usr.` for everything we make (Academy samples use `crt.` for custom requests: we don't) | Not used yet |
| **A request handler with no `scopes` runs on every page**: always scope ours to named pages | Rule |
| Business logic in request handlers, not custom view models; destroy handlers synchronous; `#ResourceString` resolves once, bindings stay live; built-in converters (`crt.IsEqual`, `crt.ToObjectProp`, `crt.InvertBooleanValue` …) and validators (`crt.Required`, `crt.MaxLength` …) before custom ones (Overview; converters; validators references) | Rule |
| Classic UI wrapped components can't go in the Designer palette: always build a Freedom UI remote module (Classic UI remote module) | ✅ |

## 2e. Field lessons (Creatio Community forum, read 19 Nov 2026)

40 component threads and articles on community.creatio.com (picked from 449 search hits across 23 searches). Forum
answers carry no staff badge and many date from 8.0–8.2; where they disagree with §2d (version 10), §2d wins. Several
older answers say custom components "can't have a settings panel": outdated since setup areas (8.3.3+).

### Inputs, outputs, lifecycle

| Lesson (source) | Kit |
|---|---|
| **Bound inputs arrive after `ngOnInit` / `ngAfterViewInit`**: read them in `ngOnChanges` or `@CrtInput` setters; never wait with `setTimeout`; a value that never arrives still shows the empty or "Set me up" state | ✅ all 8 use `ngOnChanges` |
| One component instance can live across record opens: reload on every `recordId` change, reset state when it goes empty. **Re-open test:** open record A, back to the list, open record B, check B's data shows | Rule; add to every rehearsal |
| Bind `recordId` to the page record (`$Id`), never to a column of another data source (that one comes back undefined on the second open) | ✅ panel binds `Id` |
| The component can't discover its page or object: everything comes through bound inputs; if it needs the object name, make it a setting | ✅ |
| Output to the page: `@Output() @CrtOutput()` `EventEmitter`, bound in the element's values as `{ request: "usr.<name>" }`, reaches a page request handler (scope it, §2d) | Pattern for future components |
| No Designer hooks when a component is dropped or deleted: nothing may depend on side effects at placement; deleting a component doesn't clean up what its panel created | Rule |
| No global event bus or `BroadcastChannel` between components (it crosses browser tabs); talk through bound attributes and `crt.*` / `usr.*` requests | Rule |
| Never call `customElements.define` / `sdk.registerViewElement` from page handlers (throws "name already used" on the second open); the remote module registers once, guarded by `customElements.get` | ✅ |
| `@CrtInput({ propertyBindable: true })` (seen in a forum article) is not in the public devkit types ("Excluded from this release"): don't use it; ordinary `@CrtInput` binds fine | ✅ not used |

### Data and services

| Lesson (source) | Kit |
|---|---|
| **Counts and totals: a Model `type: "function"` attribute** with `functionConfig: { aggregation: AggregationFunction.Count, type: "aggregation", aggregationEval: "all" }` and the filter as `ModelParameterType.Filter`. Never load every row and use `.length` | ✅ Stage funnel (0.6.2, verified on clean82: one `KitCount` row per stage, row fallback). Group overlap, Rate against target and Cycle time need row data (combinations, per-group bars, medians): they keep rows under the cap |
| `load` attributes and filter paths must be real object column names (`Usr…`); a page attribute name comes back silently empty (only `Id`). Show our alert when a configured column returns nothing | Pickers save real columns ✅; add the check |
| No client ESQ (the devkit `EntitySchemaQuery` has no executor) and no Classic `ProcessModuleUtilities`: Model and `crt.*` requests only | ✅ |
| Run a process from code through `HandlerChainService.instance.process({ type: 'crt.RunBusinessProcessRequest', processName, processParameters, $context })` (the forum's `request:` / `params:` shape and `processParamters` typo fail). Keep one tested snippet in the kit before using it | ⚠️ untested |
| Portal (external) users: Model calls run under the portal user's object permissions; a custom C# web service needs `[DefaultServiceRoute, SspServiceRoute]` on the class and the `0/ssp/rest/` path. Test every component on a portal page **logged in as a portal user** | ⚠️ Request checklist is on a portal page: run that test |
| A filtered Model load returning HTTP 500 or one row on 8.0.6–8.0.9 = known `FilterGroup` bug (workaround: `Object.assign({}, filters)` with `items` copied); fixed later | 8.x stands only |
| Custom converters in calculated attributes need 8.3.2+ | Version note |

### Build, dev loop, platform limits

| Lesson (source) | Kit |
|---|---|
| "Remote entry with name '…' does not exist" (the most-asked error): (a) running `npm start` / `ng serve` outside Creatio: expected, a remote module needs Creatio's runtime; (b) template macros left in the project (`<%projectName%>`, `<%vendorPrefix%>`) or the webpack `uniqueName` not matching the project name. After scaffolding, search the project for `<%` | Troubleshooting row |
| No live preview against a stand. Mock look and feel with a local harness if useful, logic in Jest, data and Designer behaviour on a stand only. Dev loop: `ng build`, `push-workspace` (no compile: don't use `clio compile-package` for our JS-only kit), hard refresh (Ctrl+F5) in the Designer and the page | ✅ our route |
| Build error "The 'compilation' argument must be an instance of Compilation" = two webpack or Angular-builder versions installed: clean `node_modules` and the lockfile, versions pinned exactly (§2d) | Troubleshooting row |
| **Custom components don't render in the mobile app** (different UI framework). Mobile pages use native fields; say so in the build plan | §8 |
| Sidebars: `crt.OpenSidebarRequest` passes no data; the sidebar's view model is created once and only hidden on close (no Init/Resume on reopen). Don't promise "the sidebar shows the current record" without testing reopen | Demo caution |
| Long page actions: `request.$context.maskService.showBodyMask()` / `hideBodyMask()` in `try`/`finally` (no custom message). Our components keep their own skeleton | Pattern for page buttons |
| Check the native controls first (e.g. multiselect is native since 8.2.1) before building a component | Rule (demo plan) |
| Version floors: setup areas (our pickers) need **8.3.3+**; the coding-agent and design-token route **8.3.4+**. Don't offer the kit on an older customer stand | §6 |
| Zoneless timeline (Creatio staff, 17 Nov 2026): 10.2 Dec 2026–Jan 2027 (zoneless optional), **10.2.1 about Feb 2027 (default)**. It also covers page handlers and client modules around our components: await everything there too. Open question (unanswered on the forum): updates after the first `await` in a handler; until answered, `await Promise.all(...)` first, then set state once | §6 |
| Marketplace patterns worth copying: a colour per value and theme/size in the setup panel; search and copy; column layout saved per user; row click opens the record; README tells the customer to add `labUiKit` as a dependency of the page's package | Ideas |

## 2f. Efficiency budget (v0.7, measured on Record inbox, 19 Nov 2026)

| Rule | How it is checked | Record inbox on clean82 |
|---|---|---|
| One page load + one server count per refresh; page size + 1 rows to know there is more; selected columns only | Count the component's SelectQuery calls on a fresh open | ✅ 2 per inbox (rows=6 for page size 5, and the count) |
| No polling and no timers. Reload on `refreshOn`, after an action, and when the tab becomes visible again at most every 30 s; the listener is removed on destroy | Unit test + review | ✅ |
| Lookup values, captions and the current user cached per object for the page's life | Second open makes no lookup reads | ✅ |
| `OnPush` + signals; no function calls in templates (computed signals instead) | Review | ✅ |
| Nothing left behind: no kit elements in the DOM after leaving the page; heap growth no worse than native pages over 10 open/close cycles (no forced GC, so compare with a native control) | `performance.memory` loop vs a native list-to-list loop | ✅ 0 elements left; +4.7 MB per cycle vs +9.1 MB native control |
| Heavy libraries load only where used (dynamic `import()`, own chunk) | Build output: the chunk is reached only through `.e(<chunk>)` | ✅ Leaflet (Map) 148 KB own chunk |
| Bundle growth per new component: **+15 KB gzipped runtime** at most; report raw and gzipped | `ng build` before and after | Record inbox +9.8 KB gzipped (+41 KB raw: devkit code is bundled because the remote shares nothing) |

## 2g. Security (v0.7)

| Rule | Why |
|---|---|
| A component that runs processes runs only the process names in its settings, checked against `^[A-Za-z][A-Za-z0-9_]*$`, and passes only the record Id and a trimmed, length-capped comment; an unsafe setting is refused and shown, never run | A page user cannot make it run anything else |
| Before a process: re-read that the record still meets the queue condition ("already handled"); lock the buttons while it runs | No double actions, no acting on stale data |
| **A process an action runs must itself only act on records the running user may change.** Pattern (gallery): a shared sub-process `UsrRecord_CheckCanChangeSubProcess` (object name + record Id) runs `UserConnection.DBSecurityEngine.GetEntitySchemaRecordRightLevel` and throws unless `CanEdit`; every action process calls it first. One compile for all; they stay no-code | Tested 19 Nov on clean82: a portal user can run processes through `ProcessEngineService.svc/RunProcess`, also without the component. After hardening, his direct call on a Supervisor task was refused (`success: false`, record unchanged); his own case and the employee's records still worked |
| **`Model.canSave` on a model from `Model.create` answers "may this user CREATE records of the object"** (Creatio picks the check by the model's mode; no request is sent), not "may they edit this record" | It let a read-only portal user through and could block someone who may edit but not create. Kit 0.8.3 uses it before inserts only; the devkit has no public record-level check (its `RightsService` covers system operations only) |
| A refusal reads in plain words in the row; the platform's raw text goes to the console (0.8.2) | "An error has occurred during the process execution" tells a user nothing |
| Opening a record: `crt.UpdateRecordRequest` with `entityName` + `recordId` and **no `$context`** | Creatio's handler reads `$context._subscriptions`; an empty `{}` throws on home pages and nothing opens (fixed 0.8.1 in Record inbox, Group overlap, Map) |
| Record data only through Angular interpolation: no `innerHTML`, no `bypassSecurityTrust*` for text, no URLs from data. A setting that ends up in HTML (a Map marker colour) is validated | No XSS through data or settings |
| A component that sends data outside Creatio (address search, tiles) is off unless set, and its panel says what leaves | Customer data stays in Creatio by default |
| Portal users get **desktops**, not workplace home pages: test a component for external users on a desktop (`CentralAreaDesktopTemplate`) with read on its `Desktop` record for All external users | A home page or a page URL redirects a portal user to the portal desktop |

## 2b. The pages around the components (look)

A polished component on a cheap-looking page still looks cheap. These rules apply to every page we build for a demo:
home pages, dashboards and record pages (Renzo, 15 Nov 2026: "any text that has the transparent background and
therefore shows the grey like background looks cheap").

| Rule | Do this |
|---|---|
| **No text directly on the grey page background** | Every heading, subtitle and section label sits on a white card: a `crt.FlexContainer` with `color: "#FFFFFF"`, `borderRadius: "medium"`, padding medium / large, the label inside it. Applies to page titles, section headings and any explanatory line |
| One header card per page | Title (headline-3, semibold, `#0D2E4E`), one-line subtitle (body, `#606060`) and the page's buttons in **one** white card in one 12-column row; never title and subtitle on separate grid rows (that leaves an empty band) |
| Headline numbers first | Metric tiles in the top band (4 or 6 across, 2 rows tall), then work lists, then charts; never metrics under the lists |
| Lists on home pages | Row numbers **always on** and users can **add columns** (the + in the list header): `features.rows.numeration: true`, `features.columns.adding: true`, `features.columns.toolbar: true` (Renzo, 16 Nov 2026). No row checkboxes (`selection: false`). Column headings short enough to show in full ("Still needed", not "Docs outstanding"); on a 4-column list allow for the + button |
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
| Build check (v0.7) | Before every install: `ng build` exit code 0 **and** `remoteModuleEntry.js` in the output folder. A failed build leaves the folder empty, and `push-workspace` then installs a package with no JS, which breaks every kit component on the stand (happened 19 Nov on clean82 for 2 minutes: a worktree whose `node_modules` predated a new dependency). Run `npm ci` after pulling a change to `package.json` |
| Test | `npx ng test` (the project's Jest builder). Plain `npx jest` fails most suites: wrong runner, not a fault |
| Build | `npx ng build` → `packages/labUiKit/Files/src/js/ui_kit` |
| Release (0.8.4+) | Only the kit's `scripts/release.ps1` picks a version. Chats commit and add a bullet under `## Unreleased` in the kit's `CHANGELOG.md` (and a row in `RELEASE-QUEUE.md`); nobody edits `package.json`, `descriptor.json` or `KIT_VERSION`. It refuses a dirty tree, a hand-edited or mismatched version and an empty Unreleased; runs the tests and the build check; tags `kit-x`; writes `Library/ui-kit/packages/labUiKit-x-<date>.zip`. Every kit element carries `data-kit-version` (DevTools → Elements → search it) |
| Install (0.8.4+) | Only through the kit's `scripts/install.ps1` (Windows PowerShell: clio 8.1 sees no stands under pwsh 7.7), with Renzo's yes per stand. Stands in the kit's `stands.json` only; deal stands (Navalo, EWB, BPD Bali) only with that deal's OK (`-DealOk`); never a downgrade; healthy stand first, one heavy job per stand, waits until settled, never retries (BUILD-RULES §1b); reads the version back and logs the install in `INSTALLS.md`. Never `push-pkg` or `push-workspace` labUiKit by hand |
| Check | In the designer palette (**Custom components**), then live on a page with real data; on a 10.2+ stand also with `EnableZoneless` on (§2d checklist) |
| Export | `release.ps1` writes the package (0.8.4+). `clio pull-pkg labUiKit -e <env>` only to check what a stand really runs (the package label can be wrong on stands from before 0.8.4) |

**One package, one version line.** Every branch ships the same package UId (`bd7e46b4-…`), so installing one branch
replaces the other on a stand. Merge before installing on a stand that has another branch's components. Today (18 Nov
2026, updated 19 Nov): **`main` = 0.8.4 since 19 Nov** (release flow, `data-kit-version`, install safety; versions, installs and history in the kit's `CHANGELOG.md` and `INSTALLS.md`). Before that, **`main` = 0.8.3** (Map 0.7.0, Record inbox 0.8.0, open-record fix 0.8.1, readable process refusal 0.8.2, no misleading `canSave` 0.8.3; `a1fccc2`, 152 tests; published `Library/ui-kit/packages/labUiKit-0.8.3-2026-11-19.zip`). Before that, **`main` = 0.6.4 since 18 Nov evening** (fast-forwarded to `ewb-components` `2b2721c`: 0.6.3 stage re-check before unit writes, 0.6.4 "not saved" when a write changes no rows; 121 tests; package `Library/ui-kit/packages/labUiKit-0.6.4-2026-11-18.zip`). Before that, **`main` = 0.6.2** (`ewb-components` 0.6.1 fast-forwarded in 19 Nov, then the §2d/§2e to-dos, `c92cebc`; installed on clean82 only):
the Navalo components plus the 7 EWB components, all on `_kit-tokens`, all on pickers, with shape skeletons and a row
cap. Build OK, 19 suites / 116 tests pass. New work goes on `main`; installs need a yes per stand (EWB stand only after
a clean-stand test, with the EWB chat told first).

**Choice-picker default (fixed in 0.6.2):** an unset setting shows "Default" (or the panel's own "Yes/No (default)") instead of the first option, and an empty choice clears the setting (`{ constant: null }`) so the component's default applies.

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
| 10.1 | 11014930-demo (EWB) | `ewb-components` 0.6.1 live 19 Nov 2026 (main merged in, EWB components aligned to v0.6) |
| 10.x clean (10.1.796) | 11014982-demo (`clean82`) | **0.8.3 19 Nov**: gallery package `UsrUiKitGallery` (home page, portal desktop, five processes incl. the rights check, `gallery/seed.py` data), CrtProcessBuilder installed for clio process builds; keyboard-only and portal-user tests passed. 0.6.2 rehearsed 19 Nov (Stage funnel server counts match 104 records). 0.5.5 first install on a stand that never had `labUiKit` (no compile, no restart); Stage funnel rehearsed on live data, look and focus match native (18 Nov 2026) |
| 10.2.1 | none yet | ⚠️ Zoneless on by default (about Feb 2027; 10.2 with it optional Dec 2026–Jan 2027): run the §2d zoneless test before any customer stand moves to 10.2.1 |
| Below 8.3.3 | – | Not offered: no setup areas (our pickers) |

Pinned versions (kit `main`, 19 Nov 2026): Angular 22.0.8, `@creatio-devkit/common` 0.1000.3, `@creatio/interface-designer`
0.1000.3, TypeScript 6.0.3. Not yet proven: keyboard-only pass, zoneless on a 10.2 stand.

## 7. After every Creatio upgrade (10 minutes)

1. Open the gallery page (or one real page per component): it loads, shows data and, for writing components, saves one
   change.
2. Record the Creatio version in §6 and the kit README. If anything fails, fix the kit once and republish to the library.

## 8. Not promised

- Every future Creatio release: we follow the supported route and smoke-test after upgrades.
- Right-to-left layouts and languages beyond English.
- The mobile app: custom components don't render there (different UI framework); mobile pages use native fields.

## 9. Changes

| Version | Date | Change | Evidence |
|---|---|---|---|
| v0.7 (addition) | 19 Nov 2026 | §4 Release and Install rows: versions picked only by the kit's `release.ps1`, installs only through `install.ps1` (stand list, deal OK, no downgrade, BUILD-RULES §1b stand safety, install log), `data-kit-version` on every element | Kit 0.8.4 release flow; a sandbox 502 from back-to-back installs in another chat |
| v0.7 | 19 Nov 2026 | Record inbox (§1); §2f efficiency budget and §2g security, measured on clean82 (process-side rights check, `canSave` only means "may create", no `$context` when opening records, portal desktops); build check before every install (§4); Map: lazy Leaflet, address search off by default, colour validation. File renamed from v0.6 to v0.7 on 19 Nov 2026 (version clean-up) | Record inbox build, gallery rehearsal, keyboard and portal tests on clean82; kit `main` `a1fccc2` |
| v0.6 | 19 Nov 2026 | New §2d: the rules from all 37 Freedom UI pages of Academy › Front-end development (build route, zoneless for 10.2.1, settings panels, data, strings, icons, handlers), each checked against kit 0.5.5; new §2e: field lessons from 40 Community forum threads (inputs after init, re-open test, counts by aggregation, portal-user test, common build errors, mobile not supported, version floors); §4 zoneless check; §6 versions pinned, the 10.2.1 date and the 8.3.3 floor; §8 mobile | Academy version-10 guides and community.creatio.com threads read 19 Nov 2026; kit `main` source |
| v0.5 | 18 Nov 2026 | §2c native patterns (tokens, component looks, schema conventions); tokens rule corrected; rehearsal on clean82 | Clean stand 11014982, kit 0.5.5 |
| v0.4 | 15 Nov 2026 | Section 2b page look rules (no text on the grey page background, one header card, metrics first, lists with row numbers and add-column, one accent colour, palette chart colours by meaning, slots fit their cards); every setting picked not typed (0.5.0 pickers); person-level exclusion; five more components in section 1; versions 0.5.0 | Navalo 14-15 Nov: plan 15 build (labUiKit 0.5.0) and Renzo's "looks cheap" feedback on the lending overview (`Lessons/feedback/2026-11-15-renzo-huruiti-home-pages-look-cheap.md`) |
| v0.3 | 13 Nov 2026 | Flow timeline added (live); rules for optional steps, honest wording and time zones; traps: moves on inserted components, stale baseline after page rules; native next-step banners as the pattern; versions 0.1.5 | Navalo FWP1–FWP6, 13 Nov (labUiKit 0.1.3–0.1.5) |
| v0.2 | 13 Nov 2026 | Promoted from the EWB deal folder. Two live components added; status per component; look rule changed to kit tokens with measured native fallbacks; refreshOn, read-only and naming rules; page-placement traps; build/test/ship, one-package rule; versions tested | Navalo build 13 Nov (labUiKit 0.1.0–0.1.2, CWP1–CWP7) |
| v0.1 | 12 Nov 2026 | First standard, six components planned | East West Bank (`Deals/east-west-bank-rh/06-ui-kit-standard.md`) |
