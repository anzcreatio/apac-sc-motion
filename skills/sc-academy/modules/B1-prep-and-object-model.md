# B1. Stand prep and the object model

**Path P1 · 75 min · your training stand · Skills:** `creatio-demo-prep`, `creatio-object-model`,
`creatio-schema-naming` (app-dev toolkit), `creatio-demo-spot`

## Why it matters

Everything else hangs off the object model and the package it lives in. Get the package wrong and pages save into
an automatic package, you get cyclic dependencies, and the demo can't be harvested. Get the model wrong (a second
Status column next to the stock one, an object nobody can open) and every page and process after it inherits the
mess. This module preps your stand and builds the Kestrel model exactly as the toolkit would on a real build.

## Lab (scope: `fixtures/kestrel-lab-scope.md` → Object model)

1. **Read before write.** Claude reads `get-guidance core-rules` and `routing` from clio, then the stand's current
   schema prefix and current package.
2. **Prep the stand** with `creatio-demo-prep`, the real "before start" steps: schema prefix, the working application
   **Academy Kestrel** (package name containing `Acad<Initials>`), current package. The prefix change needs a cache
   clear and a restart: on your own training stand that's fine, **with your OK first** (BUILD-RULES §1). Skip
   branding and feature flags unless you want to try them. Every step is read back, not trusted from exit 0.
3. **Names first:** Claude uses `creatio-schema-naming` for the new columns and the Site object. Check names and
   titles before anything is created.
4. **Census, then reuse:** Claude reads Case (`get-entity-schema-properties`) and you decide, field by field, reuse or
   new + reason (the scope's table is the answer key; argue with it if you disagree). Then add Kestrel's values to the
   stock `CaseStatus` and `CasePriority` lookups and make the unwanted stock values inactive (don't delete them).
5. **Build** with `creatio-object-model`, all in your lab package: the new Case columns (replacing schema), SLA
   hours on CasePriority, and the new Site object.
6. **Every new object gets a section and pages** (the rule people forget): Site gets a section in Academy Kestrel;
   Case is reached through the app too.
7. **Read it back:** `get-entity-schema-properties` for Case and Site: every column, type and lookup as planned.
8. **Spot change:** use `creatio-demo-spot` for one bounded change, e.g. add "Clock paused" (boolean) to Case. Notice
   its preflight and how it routes the change to `creatio-object-model`.
9. Record in `<practice dir>/lab-log.md`: every schema, every lookup value added, every value made inactive.

## Check (pass criteria)

- [ ] The prefix and current package are set and read back; the lab package contains `Acad<Initials>`.
- [ ] Case has Site, At risk, Lead alerted and Client update **in the lab package**; no second Status, Priority or
      due-date column exists.
- [ ] CasePriority holds P1-P4 with SLA hours 4 / 24 / 72 / 240; CaseStatus holds the five Kestrel stages.
- [ ] Site opens from a section in Academy Kestrel.
- [ ] Any compile or restart was approved by the SC first and noted in `lab-log.md`.

## Traps

- **Saving while the current package is wrong** creates an automatic package with Primary = true in someone's app.
  Set the current package before the first save; check `designPackageName`.
- **The prefix after a stale cache:** changing it without the cache clear and restart produces a `Usr*` package you
  then have to uninstall. Prefix first, before anything is created.
- **New columns in the base package, not the app's design package**, or you get cyclic dependencies.
- **A duplicate column of the same meaning** is a structure defect; hiding the stock column from the page is
  masking, not a fix.
- **Data bindings adopt rows by Name**: duplicate lookup names bind the wrong Id.
- **Package hygiene:** never add a server-built app package to a `push-workspace` folder (it wipes server schemas);
  deleting a package by name in Configuration once removed **both** packages of that name (1 Nov 2026 incident).
