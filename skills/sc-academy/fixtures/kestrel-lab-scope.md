# Lab scope: "Kestrel dispatch desk" (FICTIONAL, SC Academy modules B1-D1)

> The small demo every trainee builds in the stand modules. About 6 hours in total. Each trainee builds on **their own
> training stand** (Renzo, 14 Nov 2026: one stand per person for training), in the lab app **Academy Kestrel** and
> its package containing **Acad<Initials>**. `<p>` = the schema prefix you set in B1.

## Hero story (one use case, UC1)

Westfield Parramatta logs a **P1** job: "Chiller 2 tripped, food court has no cooling". The dispatcher opens the
**dispatch desk**, sees the job flagged **at risk**, and the system has already **raised a task** for the dispatch
lead. The dispatcher asks **Creatio.ai** for a client update; it drafts one from the job, the dispatcher confirms,
and it is saved on the job.

## Built the way a real deal is built

A Kestrel job is a **Case**: reuse the stock object, its Status, Priority and SolutionDate, and add Kestrel's values
to the stock lookups (`creatio-object-model` "reuse the stock column"). Only what Case doesn't have is new. Because the
stand is yours alone, changing stock objects is fine here, always in your lab package; D1 resets it.

## Object model (B1)

| Object | Reuse or new | What |
|---|---|---|
| Case (job) | **reuse** | Status = stock `CaseStatus` (add or rename: New, Allocated, On site, Waiting on client, Complete) · Priority = stock `CasePriority` (P1 Emergency, P2 Urgent, P3 Standard, P4 Planned; other values inactive) · SLA due = stock `SolutionDate` · Client = stock `Account` · Description = stock `Symptoms` or `Subject` (pick one, say why) |
| Case, new columns | new, replacing schema in the lab package | Site (lookup to `<p>Site`), At risk (boolean), Lead alerted (boolean), Client update (text, long) |
| `CasePriority`, new column | new | SLA hours (number: 4, 24, 72, 240) |
| `<p>Site` | **new** (no stock object means "site") | Name, Client (Account), Address, Induction required (boolean), Access notes (text) |

## Pages (B2)

Case form page as a **replacing copy in your lab package** (header with Status, Description, SLA due, Client update,
Site), Case list with a quick filter on Status, Site mini page. Labels above fields, placeholders, nothing empty.

## Data and home page (B3)

3 client Accounts ("Westfield Parramatta (Kestrel lab)", "Macquarie Park Tower (Kestrel lab)", "Liverpool Council
depot (Kestrel lab)"), 3 sites (Westfield: induction required), 8 jobs across the statuses, SLA due spread over the
next 2 days. **Hero record:** `KJ-1042`, Westfield Parramatta, P1, New, SLA due in 3 hours, At risk = yes.
Home page **Dispatch desk**: KPIs open jobs and P1 at risk; chart jobs by status; list of at-risk jobs.

## Process (C1)

`<p>AcadP1Alert`: starts when a Case is added with Priority = P1 → adds a Task (Activity) "P1 <number>: call the
client within 15 minutes", owner = your own contact → sets Lead alerted = yes. Native route, IsTracing on.

## AI skill (C2)

**Kestrel client update**: on the open job, reads the case, site, priority and status, drafts a 3-line client
update in Kestrel's voice, asks "Save this update to the job?", and only after yes writes Client update. Confirm-then-act.

## Prove, click path, harvest, reset (D1)

UC1 rehearsed on a twin of KJ-1042; click path cards; `sc-clickpath` pages into the practice folder; an L1 harvest
entry written to the practice folder only; then reset: lab records and the lookup values you added, then the lab app
and package (your yes), so the stand is ready for the next course run.
