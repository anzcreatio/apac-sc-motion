# Build rules v0.5: while configuring a demo stand

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

## Changes

| Version | Date | Change |
|---|---|---|
| v0.5 | 16 Nov 2026 | Building on top of a master stand (demo bar §6c): library modules named in the pack's `extends` are in scope and go into the restore point; a master that another deal holds (`in_use_by`) is a hard stop (Renzo) |
| v0.4 | 14 Nov 2026 | Section 4 rewritten: pre-flight before leaving, restore point, check each item and fail soft (two tries, then skip and carry on), irreversible decisions = hard stop, time budget and plan fingerprint, scope check in the report; caps enforced by `approval_pack.py`; auto-mode rules for the hard stops; edits only in deal and builds folders (Renzo) |
| v0.3 | 14 Nov 2026 | Section 4: one approval pack upfront (scope, stand, compiles, restarts on our own stand, custom code, auto-rollback, data, decisions log), then a non-stop build with six hard stops; keep-awake, notifications and a build report; permission allowlist via `sc-setup` (Renzo) |
| v0.2 | 13 Nov 2026 | Section 3: a rollback plan before custom components, code, standard-object or shared-setting changes (Renzo) |
| v0.1 | 13 Nov 2026 | First version: compile and restart with permission; token check before debugging (Renzo) |
