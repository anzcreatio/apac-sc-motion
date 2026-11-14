# B1. Stand prep and the object model

**Path P1 · 75 min · lab stand · Skills:** `creatio-demo-prep`, `creatio-object-model`, `creatio-schema-naming`
(app-dev toolkit), `creatio-demo-spot`

## Why it matters

Everything else hangs off the object model and the package it lives in. Get the package wrong and pages save into
an automatic package, you get cyclic dependencies, and the demo can't be harvested. Get the model wrong (a duplicate
Status column, an object nobody can open) and every page and process after it inherits the mess. This module builds
the Kestrel model in your own lab app, the way the toolkit would on a real build.

## Lab (scope: `fixtures/kestrel-lab-scope.md` → Object model)

1. **Read before write.** Claude reads `get-guidance core-rules` and `routing` from clio, then the stand's **schema
   prefix** and current package. **Never change the prefix or any shared setting on a lab stand**: just note it as `<p>`.
2. **Read `creatio-demo-prep`** together: which of its steps apply to a fresh customer stand (prefix, branding,
   feature flags, current package) and which you skip on a lab stand (all of the shared ones). Say why in one line.
3. **Create your lab app** `Academy Kestrel (XX)` with Claude (the prep skill's "working application" step, adapted:
   your initials in the code). Confirm the package name contains `Acad<Initials>` and record it in `lab-log.md`.
4. **Names first:** ask Claude to use `creatio-schema-naming` for the two lookups and two objects, with your initials
   in each code. Check the proposed names and titles before anything is created.
5. **Census, then build:** for Job, ask Claude what the **stock** Case object would give us (Status, Priority,
   SolutionDate...) and why the lab still uses its own object (shared stand). Then create the lookups (with values),
   Site and Job with `creatio-object-model`, in your lab package only.
6. **Every new object gets a section and pages** (the rule people forget): make sure Site and Job each have a section
   in your lab app (pages are polished in B2).
7. **Read it back:** `get-entity-schema-properties` for Job: every column, type and lookup reference as planned.
8. **Spot change:** use `creatio-demo-spot` for one bounded change, e.g. add "Clock paused" (boolean) to Job. Notice
   its preflight and how it routes the change to `creatio-object-model`.
9. Add every schema you created to `<practice dir>/lab-log.md`.

## Check (pass criteria)

- [ ] Four schemas exist, all in the lab package (`designPackageName` / package listing shows `Acad<Initials>`).
- [ ] Priority lookup holds P1-P4 with SLA hours 4 / 24 / 72 / 240; Status holds the five values.
- [ ] Job and Site each open from a section in `Academy Kestrel (XX)`.
- [ ] No compile or restart was run (or, if the toolkit said one was required, the SC approved it first and it's logged).
- [ ] `lab-log.md` lists every schema.

## Traps

- **New columns in the base package, not the app's design package**, or you get cyclic dependencies (toolkit rule).
- **Saving while the current package is wrong** creates an automatic package with Primary = true in someone's app.
  Check the current package before the first save.
- **A duplicate column of the same meaning** (a second Status) is a structure defect; on a real deal, reuse the stock
  one and add your values to the stock lookup.
- **Data bindings adopt rows by Name**: duplicate lookup names bind the wrong Id.
- **Package hygiene:** never add a server-built app package to a `push-workspace` folder (it wipes server schemas);
  deleting a package by name in Configuration once removed **both** packages of that name (1 Nov 2026 incident).
- **Prefix change needs a cache clear and restart**: one more reason it's never done on a lab stand.
