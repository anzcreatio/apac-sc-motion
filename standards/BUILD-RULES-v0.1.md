# Build rules v0.1: while configuring a demo stand

**What it is:** two habits every demo build follows, whichever tool runs it (the demo toolkit, clio, or Claude by hand).
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

## Changes

| Version | Date | Change |
|---|---|---|
| v0.1 | 13 Nov 2026 | First version: compile and restart with permission; token check before debugging (Renzo) |
