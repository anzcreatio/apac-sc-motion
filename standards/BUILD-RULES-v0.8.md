# Build rules v0.8: while configuring a demo stand

**What it is:** how every demo build runs, whichever tool does it, whichever tool runs it (the demo toolkit, clio, or Claude by hand).
**Agreed:** Renzo, 13 Nov 2026. `sc-setup` copies the short version into the demo toolkit's local notes for
`creatio-demo-build`, so every build session reads it.

## 1. Compile and restart only when it's really needed, and only with the SC's OK

A compile or restart takes the stand down for minutes and can break other sessions on it. Most changes don't need one.

| The change | What to do first |
|---|---|
| Freedom UI page, caption, layout, business rule, list or filter, dashboard, home page | **Refresh the browser** (hard refresh). Still old? Clear the browser cache for the site, then refresh |
| Data (records, lookups, seed scripts), system setting values, rights | Refresh. Log out and in if it's a rights change |
| Business process (saved in the designer), AI skill prompt, AI Studio agent | Refresh; re-open the record or the panel. No compile |
| Object schema change (new column, new object), C# source code, process with a script task, package install | **May** need a compile. Check the toolkit's verdict and the error first |
| The app says it must restart, or a compile finished and the change still isn't there after a refresh | **May** need a restart |

**Before any compile or restart, ask the SC** (unless the approval pack in section 4 already covers it), in one message: what changed, why a refresh isn't enough, what will be
down and for roughly how long, and whether anyone else is on the stand. Wait for a yes. Never compile or restart "to be
safe", and never restart a shared stand without the SC's OK.

### 1b. Package installs and other heavy jobs: one at a time, healthy before, settled after

An install uploads the package, backs up, installs and restarts the stand's app; on a cloud stand `push-pkg` can take
15 minutes or more. Starting a second package straight after the first, then retrying when it failed, once took a
sandbox down with a 502 until Creatio support restarted it. For every package install, `push-workspace`, compile or restart:

| Rule | How |
|---|---|
| 1. Healthy stand first | `<stand url>/0/ping` answers 200 within 10 s. Slow (that stand was timing out at 40 s before it went down) or failing: don't start; tell the SC |
| 2. One chat per stand (stand lock) | Never start one while another runs on the same stand, from any chat or person. The plugin enforces it: every clio write to a stand (MCP, `clio ... -e`, the kit's `install.ps1`) takes a 30-minute lease on that stand in SharePoint `Stands/locks/`; a write while another chat holds it asks the SC ("in use by ... go ahead anyway?"), or in an unattended run is refused (a hard stop). A long build holds the stand on purpose: `python <plugin>/hooks/stand_lock.py hold --stand <env> --hours 8 --why "<build>"`, `release` at the end (session end frees it too). `stand_lock.py status` or `desk.py work` shows which stands are in use |
| 3. Wait until it has settled | Afterwards, `/0/ping` answers 200 steadily for about 2 minutes before the next job, a version check or a demo |
| 4. Never retry straight away | A failed job: check `/0/ping`, tell the SC what failed and whether the stand answers, wait for a yes before trying again |
| 5. Slow is not stuck | A long install while the stand still answers 200 is working: wait. Never start a second copy |
| 6. A package install counts as a compile | Ask the SC before **each** install (unless the approval pack lists it), and report after each one before the next: what was installed, how long it took, whether the stand compiled. An install can compile the stand for minutes (one build installed 4 times, about 10 minutes of compiling, without asking: a stand without the cliogate package needs an install for things like AI skills) |

`labUiKit` installs go through the kit's `scripts/install.ps1`, which enforces rules 1–4 (UI kit standard §4).

## 2. When calls suddenly fail, check the token first

Rarely, the OData session or token expires mid-build. Signs: `401` or `403`, "unauthorised" or "authentication
failed", a login page coming back instead of JSON, or calls that worked a minute ago now failing.

1. **Check the token or session first:** re-run the toolkit's or clio's login or refresh step, then retry the call once.
2. Works? Carry on and note it in the build log.
3. Still failing? Only now start debugging the change itself.
4. Never type a password and never open `CREDENTIALS.md`. If the refresh needs a password or a sign-in, ask the SC to do it.

## 3. A rollback plan before anything risky

**Before** you install a custom component, deploy code (C# source code, a script task, a JS component, a package
from outside), change a standard object or a shared system setting, or make any change you can't undo with one click,
write the rollback in the build log, and tell the SC in one line. Needed for anything marked custom in the demo plan;
not needed for pages, captions, rules or data in our own package.

| Write down | Example |
|---|---|
| **Backup taken first** | Package exported (`clio` pull or the toolkit's package backup) to `<deal>/build/pkg-backup/<yyyy-mm-dd>/`; the page's current body saved as `backup-<page>-v<n>.js`; system setting values noted |
| **What breaks if it fails** | "The Site page won't open"; "compile fails and the stand is down" |
| **How to roll back, step by step** | Remove the component from the page and save the backed-up body · uninstall or delete the package · restore the setting value · re-run the reset script |
| **How we check it worked** | The page opens; the click path's first three steps pass |
| **Plan B for the demo** | Show the native version of the screen, or the backup screenshot / clip from the click path |

Rules:
- Keep custom components and code in **their own package** (demo bar §6b), so rolling back is removing one package.
- Never roll back on a stand someone else is using without the SC's OK (it may need a compile or restart: section 1).
- After a rollback, note in the build log what failed and why, so the next build doesn't repeat it.

## 4. Approve upfront, then build non-stop

The SC shouldn't have to sit at the laptop approving steps (Renzo, 14 Nov 2026), and walking away mustn't add risk.
So: approve once, check before leaving, keep a way back, and let code (not good intentions) enforce the limits.
Script: `skills/sc-demo-plan/scripts/approval_pack.py` (exit 0 = carry on, 3 = hard stop, 4 = give up this item).

**1. The approval pack** (with the build plan, one reply from the SC). `approval_pack.py new` writes
`<deal>/build/approval-pack.json` from `build-plan.json` and prints the checklist to send: scope = the plan's items
(B1…), the stand and whether it's ours alone, compiles for listed schema and code items, restarts (our own clean stand
only, max 3), custom components and code once each rollback is written, auto-rollback, two tries per item, demo data
and reset, reversible decisions on defaults. It stores the plan's fingerprint and a time budget (plan hours × 1.5).

**2. Pre-flight, with the SC still there (about 5 minutes).** Stand reachable and signed in; OData token fresh;
`UserSessionTimeout` long enough for the build; clio sees the stand; the browser pane is signed in; the stand's URL
is in the desktop app's **Settings → Allowed sites** (otherwise a stand on a private network, e.g. through the VPN,
asks before every click and script, which stops an unattended build; only the SC can add it); no other session
or SC holds the stand (toolkit lock); the permission setup is loaded: the session is in auto mode **and** its
working folder's `.claude/settings.local.json` allows `mcp__Claude_Browser` and has our `autoMode` rules (read the
file; if it's missing or lacks them, stop: the SC opens a new chat from the folder `sc-setup` set up, or re-runs that
step of `sc-setup`). Then
`log --kind preflight-ok` and tell the SC "safe to leave". A sign-in found later is a hard stop, so find it now.

**3. Restore point before the first change.** Export every package of the deal (on a master stand, also every
module in `extends`, and note the stand's state) into
`build/pkg-backup/<date>/`, then `log --kind restore-point`. `start` refuses without a pre-flight and a restore point.
This lets the SC undo the whole build in one step, on top of each change's own rollback (section 3).

**4. Build item by item, check as you go, fail soft.** For each item: `log --kind attempt --item Bn`, build it, then
check it (its click-path steps or `creatio-uc-readiness` for that scene) before `done`. If it breaks: roll it back by its
plan (`rollback`) and try again. After two tries the script says **give up**: leave it rolled back, mark it, and carry
on with every item that doesn't depend on it. Run `check` between items (plan unchanged, time budget left).

**5. Decisions.** A choice the plan doesn't settle: if it can be undone (a caption, a colour, an order, a default
value), take the default and `log --kind decision --reversible yes`; it's listed for the SC to check before the demo.
If it can't be undone (renaming or deleting an object or column, a standard-object schema change, a data migration,
anything on a shared stand), it's a **hard stop**.

**Hard stops** (the script returns 3, or Claude sees one): out of scope or touching `Custom` / another deal's
packages (on a master stand, a library module named in the pack's `extends` is in scope, backed up in the restore point) · a restart not pre-approved (shared stand, or over the limit) · a sign-in, password or MFA the SC must do ·
deleting anything that isn't our demo data · an irreversible decision · the plan changed after approval · time budget
spent · a master stand another deal holds (`in_use_by`) · anything reaching a customer. On a hard stop: stop that line of work, finish anything independent that's safe,
notify the SC, and write the report.

**6. Finish.** `log --kind end`, then `report` writes `build/build-report.md`: every item's status, compiles,
restarts and rollbacks with reasons, decisions to check, what needs the SC, and a **scope check** (compare what's in
our packages on the stand with the items; anything extra is listed). Keep the laptop awake for the whole build
(keep-awake where available) and send a notification at the end or at a hard stop.

**7. Permissions: auto mode plus our rules.** Most build commands are chained (`cd … &&`, variables), so an allowlist
alone never matches them; auto mode decides. `sc-setup` installs `standards/build-permissions.json` into the folder the
SC builds from: an allowlist for the plain cases **and auto-mode rules** that block, whatever the instructions say:
reading `CREDENTIALS.md` or typing passwords, `git push`, restarting or recompiling a stand the approval pack doesn't
allow, deleting Creatio data or packages outside the deal's demo packages, and sending anything to a customer. Edits
are allowed only in the deal folder and the builds folder, not the plugin or the instructions. Settings load in the
next session.

## 5. Custom components, checks and handover (v0.6)

From the BPD Bali map build (18 Nov 2026): each of these cost rework or blocked a check that night.

| Rule | Why |
|---|---|
| **A custom component starts on the UI kit from day one**, even when it won't go into `labUiKit` yet: copy the kit's `kit-data.ts` (devkit `Model` reads, row caps), `kit-write.ts` (`canSave` + `ensureOk`) and `_kit-tokens.scss` into the project unchanged, with a header line naming the kit version; follow `UI-KIT-STANDARD` §2 (settings with safe defaults, strings in a resource file, devkit pinned exactly, error inside the component, skeleton). Keep it in its own JS-only package, never in the app package | Raw `fetch`/PATCH made a refused write look saved and hard-coded colours didn't follow the theme; moving it later becomes lift-and-shift, not a rewrite |
| **By the end of the build, the deal folder holds everything another SC needs to change it:** component source (no `node_modules`, `.angular`, `dist`), its README (what it reads and **writes**, every setting), the page bodies saved, the seed scripts and data files, and a handover note. `approval_pack.py report` lists what's missing | The source lived only on one PC; nobody else could have changed the demo |
| **When the browser pane is signed out** (a session restart signs it out; a sign-in is the SC's), don't stop the checks: verify headless with clio `page-smoke` (fields, buttons, console errors) or Playwright with clio's stored session (`get-browser-session` → `storageState`) for screenshots and clicks. A rehearsal that saves a record deletes it after. Report it in plain words: "a Chrome signed in to your sandbox opened the real page; here is the picture", and send the images | The SC can't sign in at 2 am; and "headless screenshots" alone read as "not real" |
| **clio traps:** `create-app` names the package after the app **code** (not the name you planned); a column on `Lead` or `Account` from a new app package needs `add-package-dependency` first (the owning layers: `SalesEnterprise`, `CrtLeadOppMgmtApp`, `CrtOCMInLeadOppMgmt`, `CrtCustomer360App` on a Sales Enterprise stand), else "Reference schema 'Lead' was not found"; `odata-create` / `odata-update` `rows-file` must sit in the OS temp folder or the clio workspace; a new package for a component: `create-package` first (unlocked), then `push-workspace` with the descriptor's UId set to the server package's UId, C# scaffold removed | Each one failed once on the BPD Bali build |
| **Freedom UI web has no map component** (register L-001): a map is a custom component (Leaflet + OpenStreetMap passes Creatio's default CSP: `img-src *`, Nominatim in `connect-src`). Plan GPS geotag, address search and pin → address from the start; address search is approximate, GPS and a pin are exact | The SC asked for auto-filled coordinates after seeing the first version |
| **Duplicates in the demo? Register `EnableDeduplicationFreedomUI` first.** The Freedom UI "Potential duplicates found" pop-up on save (Contacts: Edit record · Merge · Save anyway) needs that feature plus `ESDeduplication`, `DeduplicationWebApiUrl` set and a duplicate rule with "Use this rule on save". Demo stands don't ship the feature registered, so a duplicate saves silently. Feature toggles page (`/0/Nui/ViewModule.aspx#BaseSchemaModuleV2/FeaturesPage`) → Create feature → switch on → Save changes → reload the page; no compile. The page turns it on for the signed-in user only: add every demo login (or "All employees"). Undo = switch it off. Bulk "Show duplicate" works without it, but its page shows the results only after a reload, so run it before the demo | 19 Nov 2026, bpd-bali-map (v10.1.0): a second "James Smith" saved with no warning until the feature was added (source: Academy 8.3.3 Twin changelog) |

## 6. Configuration quality (v0.7)

From Creatio's internal Confluence (NCD no-code standards, R&D, support checklists; read 19 Nov 2026, sources in
`research/CONFLUENCE-BEST-PRACTICE-2026-11-19.md` in the motion folder). The demo toolkit already covers idempotent
processes, recursion guards, no hard-coded values and gateways; these are the rules it doesn't.

**Before pro-code work:** when the `creatio-instructions-mcp` server is connected (it ships with the plugin; Creatio
VPN only), call `resolve_creatio_instructions` once, then `get_instructions_batch` for what you're about to touch:
**page bodies** (`viewConfigDiff`, `modelConfigDiff`, view model), **handlers, converters, validators**, **custom
components** (Angular, TypeScript, SCSS) and **C#** (composable-app guide: data bindings, rights, services). Read the
"Traps verified on a stand" and "Guardrails for LLM" sections and follow them where they're stricter than the toolkit.
It doesn't cover processes, dashboards, data model, demo data or AI Studio: the toolkit stays the guide there. Our
demo prefix counts as the package naming convention. Off VPN it fails to connect; carry on with the toolkit.

| Area | Rule | Why |
|---|---|---|
| Safety | **Shared or customer stand:** the change is tested on our own stand first, a backup is taken, and the build log names **a test case that proves it worked** and what to do if it fails. Do nothing that isn't in the plan; no ad-hoc SQL transactions | Support's rule for customer sites (2025): improvised steps are what break them |
| Safety | **Data bindings:** new lookup records go in a **new** binding, never an edit of an existing one (updates install only new bindings). Columns that must overwrite need `ForceUpdate`; install type `Install` | An edited binding never reaches a stand that already has it |
| Safety | **C# goes into a package as source only**, never a compiled DLL | A DLL built for another platform version installs fine, then fails at the first call |
| Safety | **Freedom UI handlers:** always `return this.next?.handle(request)` unless stopping the chain on purpose, and always set `scopes: ['<PageSchema>']`. Nothing slow in init or attribute-change handlers | Without scopes it runs on every page; without `next` save and other platform handlers silently stop |
| Safety | **Bulk process runs** go in the background, split into batches (10 run at once by default), never during a demo or rehearsal | Foreground runs one by one in the user session and loads the stand |
| Safety | **AI Studio integrations:** demo agents use delegated (user) credentials, not shared integration credentials | APD-8145 (internal, Aug 2026): any user can attach a shared-credential integration. Internal only, never to customers |
| Efficiency | **"Works at runtime, missing in the Designer"** = a missing package dependency, not a bug. Add the dependency to the highest common package, or edit from runtime | Saves a debugging loop |
| Efficiency | **One business rule per field.** Several rules on one field with different conditions don't add up; only one fires. Combine the conditions | Support checklist |
| Efficiency | **"Refused to connect" in the console** = CSP. Check `CSPMode` and the trusted-sources lookup; add the source through a data binding | Support checklist |
| Efficiency | **Generated processes (clio):** prompt as trigger → records → steps in order → who's responsible → exact values and timings → package and version. No branching, record sets or sub-processes yet: plan those as manual steps or separate processes | R&D toolkit page (Sep 2026) |
| Quality | **Data model:** extend the standard object before creating a new one; lookups, not text, for statuses and types; a detail for repeating items; no stored derived values; an external-Id column for anything integrated | R&D data-model best practice (Apr 2026) |
| Quality | **Processes:** one job each, fits on one screen; Read Data reads only the columns needed, sorting off; always a failure path | R&D and NCD process standards |
| Quality | **Page bodies:** don't write properties that keep their default value (`color: default`, `disabled: false`, `iconPosition`) | Less metadata, fewer upgrade problems (R&D, 2022) |
| Quality | **Naming (NCD):** object codes singular PascalCase, `ContactInAccount` for relations; pages `<Entity>_FormPage` / `_ListPage` / `_MiniPage`; components `AddButton`, not `Button_Add`; lookup column codes without `Id`; business rules "Action: target"; dashboards `<Title>Widget`; agents `<Domain>Agent`, never "AI" in the name; titles in sentence case | Demos that read like the product hand over cleanly to delivery |
| Quality | **Custom components with an agent:** one prompt for the component (behaviour, config panel, data binding, validation, accessibility), a separate one for Designer registration; tell it to "Read AI_GUIDES from @creatio libraries" | How R&D builds components with agents (Jul 2026) |

## 7. Mobile pages (v0.8)

From Creatio's Confluence (mobile team and Academy drafts, read 19 Nov 2026; sources in
`research/CONFLUENCE-BEST-PRACTICE-2026-11-19.md` §6). Layout, crashers and refresh rules stay in the toolkit's
`mobile-golden-standard.md`.

| Rule | Why |
|---|---|
| **Web and mobile pages are separate.** Plan a mobile page for every screen the demo shows on a phone; a web change after conversion must be copied to the mobile page by hand | A web page never appears in the app by itself |
| **Build mobile pages with R&D's `creatio-mobile-page-conversion` skill**, plan first: the SC approves the plan before anything is built, and approves publishing separately. Phone layout only (no tablet); Freedom UI web pages only | The skill reads the web page, says what can't move, and recreates page business rules |
| **Before publishing, check what the app shows today.** Registering a section or default mobile edit page replaces the current one. To rebuild, say "update the existing mobile page" (otherwise a duplicate); a rebuild wipes Mobile Designer edits | On a shared stand this changes other people's demos |
| **Convert the related object's form page too** when a button opens it (e.g. New on Products) | Otherwise the button opens nothing on mobile |
| **No custom components on mobile.** A UI kit or other `usr.*` component shows a placeholder; put native fields or widgets in the mobile page and say so in the build plan. Mobile pages are JSON only; logic goes in handlers through `@creatio/mobile-common` | The app is compiled Flutter; R&D's mobile custom-component design is still a draft (16 Nov 2026) |
| **Offline demo: test every business rule with the network off.** Only model-level rules run on the device; page rules and rules needing server code or unsynchronised data don't | They silently don't fire offline |
| **Live demo lists: always fresh.** Set the list attribute's `cacheConfig.readMode` to `2` (forceRemote) | Otherwise the app can show cached data from before the presenter's change |
| **Mobile workplace:** Workplace setup → Usage type Mobile → sections → user groups (every demo login). On an existing stand switch on `Mobile.UseSysWorkplaceForModuleRegistration`; a user on a legacy workplace switches to "Main workplace" in the app's Settings. Sync the app after | The section is missing from the app otherwise (8.3.2+) |

## Changes

| Version | Date | Change |
|---|---|---|
| v0.8 (addition 3) | 20 Nov 2026 | §1b rule 2: stand lock, enforced by the plugin's hook (leases on every clio write, hold for a long build, ask or refuse when another chat holds the stand) (Renzo, after one chat silently overwrote another chat's kit install on clean82 11 minutes after it) |
| v0.8 (addition 2) | 20 Nov 2026 | §1b rule 6: a package install counts as a compile: ask before each one, report after each (Renzo, after a build installed its package 4 times without stopping to ask) |
| v0.8 (addition) | 19 Nov 2026 | §1b: package installs and other heavy jobs one at a time per stand, healthy stand first, wait until settled, never retried straight away (Renzo, after a sandbox went down with a 502 from back-to-back installs and a retry) |
| v0.8 | 19 Nov 2026 | §7 mobile pages from Creatio Confluence: web and mobile pages separate, R&D conversion skill plan first, check before publishing, related form pages, no custom components on mobile, offline business rules, fresh lists, mobile workplace (Renzo) |
| v0.7 | 19 Nov 2026 | §6 configuration quality from Creatio Confluence: shared-stand change discipline, data bindings, source-only C#, handler `next` + `scopes`, bulk processes, AI Studio credentials, Designer dependency gap, business rules, CSP, process prompts, data model, metadata, NCD naming, component prompts; load R&D's instructions MCP when on VPN (Renzo) |
| v0.6 (addition) | 19 Nov 2026 | §5: duplicates in a demo need the `EnableDeduplicationFreedomUI` feature registered (Renzo, after the bpd-bali-map dedup test) |
| v0.6 | 18 Nov 2026 | §5: custom components start on the UI kit (vendored kit-data / kit-write / tokens); the deal folder holds source, README, page bodies, seed scripts and a handover note by build end (report checks); headless checks when the pane is signed out; clio traps; web map = custom component (Renzo, after the BPD Bali map build) |
| v0.5 | 16 Nov 2026 | Building on top of a master stand (demo bar §6c): library modules named in the pack's `extends` are in scope and go into the restore point; a master that another deal holds (`in_use_by`) is a hard stop (Renzo) |
| v0.4 | 14 Nov 2026 | Section 4 rewritten: pre-flight before leaving, restore point, check each item and fail soft (two tries, then skip and carry on), irreversible decisions = hard stop, time budget and plan fingerprint, scope check in the report; caps enforced by `approval_pack.py`; auto-mode rules for the hard stops; edits only in deal and builds folders (Renzo) |
| v0.3 | 14 Nov 2026 | Section 4: one approval pack upfront (scope, stand, compiles, restarts on our own stand, custom code, auto-rollback, data, decisions log), then a non-stop build with six hard stops; keep-awake, notifications and a build report; permission allowlist via `sc-setup` (Renzo) |
| v0.2 | 13 Nov 2026 | Section 3: a rollback plan before custom components, code, standard-object or shared-setting changes (Renzo) |
| v0.1 | 13 Nov 2026 | First version: compile and restart with permission; token check before debugging (Renzo) |
