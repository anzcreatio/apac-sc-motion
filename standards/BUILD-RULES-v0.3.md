# Build rules v0.3: while configuring a demo stand

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

The SC shouldn't have to sit at the laptop approving steps (Renzo, 14 Nov 2026). Everything that would normally
stop the build is approved **once, upfront**, together with the build plan; then the build runs to the end.

**The approval pack** (`<deal>/build/approval-pack.json`, written by `sc-demo-plan` with the build plan and confirmed
by the SC in chat in one go):

| Item | Approved upfront |
|---|---|
| `scope` | Exactly the build plan: the objects, pages, processes, AI and data it lists, in our own packages |
| `stand` | The stand by name, and whether it's **ours alone** (clean) or shared |
| `compiles` | Pre-approved for the schema and code items the plan lists. A refresh is still tried first; every compile is logged |
| `restarts` | Pre-approved **only on our own clean stand**, up to `max_restarts` (default 3). Shared stand: never without asking |
| `custom_code` | Custom components and code the plan marks custom are pre-approved, **once the rollback plan is written** (section 3) |
| `auto_rollback` | If a change breaks something, roll back by its plan, log it, and carry on with the rest |
| `data` | Create and replace demo data in our packages; run the reset script |
| `decisions` | Small choices the plan doesn't settle: take the default, write it in `build/decisions.md` (what, options, what we chose, why), keep going |

**Hard stops** (the build pauses and notifies the SC, approval pack or not):
1. Anything outside the approved scope, or touching `Custom` or another deal's packages.
2. A restart on a shared stand.
3. A sign-in, password, MFA or token refresh that needs the SC.
4. Deleting anything that isn't our demo data.
5. The same failure twice after a rollback.
6. Anything that reaches a customer.

**While it runs:**
- **At the start:** ask the desktop app to keep the laptop awake (the keep-awake tool, where it's available), and confirm
  the approval pack in one line ("Building on <stand>, approved: …").
- **Don't ask in chat mid-build.** A question that isn't a hard stop goes in `decisions.md` with the default taken.
- **At the end, or at a hard stop:** send a notification (a push notification where it's available), then the
  **build report**: what was built, each compile, restart and rollback (with why), the decisions log, what failed,
  and what needs the SC. Same report at a hard stop, plus the one thing needed to continue.

**Tool approval prompts.** Claude Code's own prompts aren't covered by these rules; they need a permission
allowlist. `sc-setup` offers to install `standards/build-permissions.json` into the SC's settings (the clio tools,
python, node and `npm run`, the browser, and edits in the deal, builds and plugin folders). The clio destructive tool,
`rm -rf` and recursive deletes still ask; `git push` and reading `CREDENTIALS.md` are denied. Settings load in the next
session, so set this up before the build session starts.

## Changes

| Version | Date | Change |
|---|---|---|
| v0.3 | 14 Nov 2026 | Section 4: one approval pack upfront (scope, stand, compiles, restarts on our own stand, custom code, auto-rollback, data, decisions log), then a non-stop build with six hard stops; keep-awake, notifications and a build report; permission allowlist via `sc-setup` (Renzo) |
| v0.2 | 13 Nov 2026 | Section 3: a rollback plan before custom components, code, standard-object or shared-setting changes (Renzo) |
| v0.1 | 13 Nov 2026 | First version: compile and restart with permission; token check before debugging (Renzo) |
