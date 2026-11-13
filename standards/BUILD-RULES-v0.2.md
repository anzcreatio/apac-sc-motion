# Build rules v0.2: while configuring a demo stand

**What it is:** three habits every demo build follows, whichever tool runs it (the demo toolkit, clio, or Claude by hand).
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

**Before any compile or restart, ask the SC**, in one message: what changed, why a refresh isn't enough, what will be
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

## Changes

| Version | Date | Change |
|---|---|---|
| v0.2 | 13 Nov 2026 | Section 3: a rollback plan before custom components, code, standard-object or shared-setting changes (Renzo) |
| v0.1 | 13 Nov 2026 | First version: compile and restart with permission; token check before debugging (Renzo) |
