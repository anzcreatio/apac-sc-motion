# B3. Demo data and a home page

**Path P1 · 60 min · your training stand · Skills:** `creatio-demo-data-population`, `creatio-dashboards-homepages`

## Why it matters

An empty list or a zero KPI kills a demo faster than a missing feature. Data is part of the build: a **hero record**
the story runs on, enough believable records around it that every view has something, and dates that are still right
on demo morning. The home page is the first screen the customer sees; it should open on their outcome (P1s at risk),
not on a menu.

## Lab (scope: `fixtures/kestrel-lab-scope.md` → Data and home page)

1. **Plan the data** with Claude from the scope: 3 client Accounts (marked "(Kestrel lab)"), 3 sites, 8 jobs (Cases),
   hero `KJ-1042`. Dates **relative to now** (SLA due in 3 h, etc.), not fixed timestamps.
2. **Mail guard first:** ask Claude to run the skill's mail-guard check before the insert (does anything notify on
   insert?). A training stand should email no one; on a real stand this check is what keeps customers' contacts safe.
3. **Seed** with `creatio-demo-data-population`, one record per request where a process may trigger on insert.
4. **Hero-record check:** the skill's check on `KJ-1042`: every field the story shows is filled; the record opens.
5. **Write the reset** into the practice folder: `lab-reset.json` (what to re-set on the hero and its twins, with
   dates relative to now). This is what D1 re-runs.
6. **Home page** `Dispatch desk` with `creatio-dashboards-homepages`: KPIs open jobs and P1 at risk, a chart by
   status, a list of at-risk jobs. Run the after-save visual check; look at it yourself.
7. Add records and the home page to `lab-log.md`.

## Check (pass criteria)

- [ ] 8 jobs over at least 4 statuses; `KJ-1042` is P1, New, at risk, SLA due within 4 hours of now.
- [ ] No widget on the home page shows blank or zero; numbers match an OData count Claude runs.
- [ ] `lab-reset.json` exists and re-running it restores the hero.
- [ ] The SC can say why demo dates must be relative and when to re-seed (demo morning, in the demo's time zone).

## Traps

- **Fixed dates go stale** before the demo. Navalo (Nov 2026) was re-seeded on demo morning in Sydney time after the
  PC's time zone changed; the reset now does it.
- **DataService datetimes** must be quoted `"\"yyyy-MM-ddTHH:mm:ss.000\""`.
- **Batch inserts race** when a process triggers on insert: insert one per request.
- **Money widgets show the stand's currency only**: on a real deal set the base currency at prep, not after.
- **Which surface is it?** A home page and a dashboard tab are different surfaces in the skill; ask Claude to name it
  before building.
