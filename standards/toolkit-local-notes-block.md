<!-- apac-sc-motion build rules v0.8 (19 Nov 2026). Added by sc-setup; full text: apac-sc-motion standards/BUILD-RULES-v0.8.md -->
## APAC SC team build rules (apac-sc-motion)

1. **Compile and restart only when really needed, and only with the SC's OK (or the approval pack's).** Pages, captions, layouts, business
   rules, lists, dashboards, data, settings, processes saved in the designer and AI prompts need a browser refresh
   (hard refresh, then clear the site cache), not a compile. Schema, C# source code, script tasks and package installs
   may need a compile; a restart only if the app requires it or a refresh doesn't show the change. Before any compile
   or restart, tell the SC what changed, why a refresh isn't enough, what goes down and for how long, and wait for a yes.
2. **When calls suddenly fail (401, 403, "unauthorised", a login page instead of JSON, or calls that worked a minute
   ago), check the OData token or session first:** refresh the login and retry once before debugging the change. Never
   type a password or open CREDENTIALS.md: if the refresh needs a sign-in, ask the SC.
3. **Rollback plan first.** Before installing a custom component, deploying code (C#, script task, JS component),
   changing a standard object or a shared setting: back up (package export, page body, setting values) into the deal's
   build folder, then write in the build log how to undo it step by step, how to check it worked, and the demo's plan B
   (native screen or backup clip). Keep custom work in its own package so rollback = remove one package.
4. **Approve upfront, build non-stop** (`skills/sc-demo-plan/scripts/approval_pack.py`). Read `<deal>/build/approval-pack.json`
   first. Pre-flight with the SC before they leave (stand, token, session timeout, clio, browser sign-in, no lock),
   then a restore point (export the deal's packages), then `log` every step: attempt, done, rollback, compile, restart,
   decision. Exit 3 = hard stop (notify the SC, stop that line of work); exit 4 = give up that item after two tries
   (leave it rolled back, carry on with what doesn't depend on it). Check each item before `done`; `check` between
   items. On a master stand (pack `master`, demo bar §6c), the library modules in `extends` are in scope and go in the
   restore point; a master another deal holds (`in_use_by` in library/stands.json) is a hard stop. Reversible choices: default + log; irreversible ones stop. Don't ask in chat otherwise. Keep the laptop
   awake, notify at the end, run `report`.
5. **Custom components start on the UI kit** (`UI-KIT-STANDARD` §2) even outside `labUiKit`: copy the kit's `kit-data.ts`,
   `kit-write.ts` and `_kit-tokens.scss` in unchanged (devkit `Model` reads with row caps, writes through `canSave` +
   `ensureOk`, Creatio tokens), strings in a resource file, devkit pinned exactly, own JS-only package.
6. **By build end the deal folder holds what another SC needs:** component source (no `node_modules`/`.angular`/`dist`),
   its README (reads, writes, settings), saved page bodies, seed scripts and data, a handover note. `report` lists gaps.
7. **Pane signed out? Check headless:** clio `page-smoke`, or Playwright with clio's session (`get-browser-session`).
   Delete any record a rehearsal saves. Tell the SC plainly it was the real stand, and send the pictures.
8. **clio traps:** `create-app` names the package after the app code; Lead/Account columns from a new package need
   `add-package-dependency` first; `rows-file` must sit in the OS temp folder or the workspace; a component package:
   `create-package` first, then `push-workspace` with the server package's UId in the descriptor. A web map is a custom
   component (no native one): Leaflet + OpenStreetMap passes the default CSP.
9. **Configuration quality (BUILD-RULES §6).** Before page-body, handler, custom-component or C# work, on VPN, load R&D's `creatio-instructions-mcp` (ships with the plugin; not for processes or data) and follow its "Traps verified on a stand". Handlers:
   `return this.next?.handle(request)` and `scopes`; new lookup data = a new data binding; C# as source, never a DLL;
   bulk processes in the background; one business rule per field; "missing in the Designer" = add the package
   dependency; extend standard objects, lookups not text; Read Data columns only; no default-valued properties in page
   bodies; NCD naming (`Contact_FormPage`, `AddButton`, `<Domain>Agent`); demo agents use delegated credentials.
10. **Mobile pages (BUILD-RULES §7).** Web and mobile pages are separate. Build mobile pages with R&D's
   `creatio-mobile-page-conversion` skill (plan approved first, publishing approved separately; phone only). Check
   what the app shows before publishing (it replaces it). No custom components on mobile: native fields instead.
   Offline: test every business rule with the network off. Live lists: `cacheConfig.readMode: 2`. Mobile workplace
   with every demo login; `Mobile.UseSysWorkplaceForModuleRegistration` on existing stands.
<!-- end apac-sc-motion build rules -->
