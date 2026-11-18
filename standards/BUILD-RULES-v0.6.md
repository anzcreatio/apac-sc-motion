# Build rules v0.6: while configuring a demo stand

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
`UserSessionTimeout` long enough for the build; clio sees the stand; the browser pane is signed in; no other session
or SC holds the stand (toolkit lock); the permission setup is loaded (a **new** session in auto mode). Then
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

## Changes

| Version | Date | Change |
|---|---|---|
| v0.6 | 18 Nov 2026 | §5: custom components start on the UI kit (vendored kit-data / kit-write / tokens); the deal folder holds source, README, page bodies, seed scripts and a handover note by build end (report checks); headless checks when the pane is signed out; clio traps; web map = custom component (Renzo, after the BPD Bali map build) |
| v0.5 | 16 Nov 2026 | Building on top of a master stand (demo bar §6c): library modules named in the pack's `extends` are in scope and go into the restore point; a master that another deal holds (`in_use_by`) is a hard stop (Renzo) |
| v0.4 | 14 Nov 2026 | Section 4 rewritten: pre-flight before leaving, restore point, check each item and fail soft (two tries, then skip and carry on), irreversible decisions = hard stop, time budget and plan fingerprint, scope check in the report; caps enforced by `approval_pack.py`; auto-mode rules for the hard stops; edits only in deal and builds folders (Renzo) |
| v0.3 | 14 Nov 2026 | Section 4: one approval pack upfront (scope, stand, compiles, restarts on our own stand, custom code, auto-rollback, data, decisions log), then a non-stop build with six hard stops; keep-awake, notifications and a build report; permission allowlist via `sc-setup` (Renzo) |
| v0.2 | 13 Nov 2026 | Section 3: a rollback plan before custom components, code, standard-object or shared-setting changes (Renzo) |
| v0.1 | 13 Nov 2026 | First version: compile and restart with permission; token check before debugging (Renzo) |
