# Lab scope: "Kestrel dispatch desk" (FICTIONAL, SC Academy modules B1-D1)

> The small demo every trainee builds in the stand modules. About 6 hours in total. Built only in the trainee's lab
> app **Academy Kestrel (XX)**, package containing **AcadXx** (XX = initials). Names below use `<p>` for the stand's
> schema prefix (read it in B1, never change it) and `Xx` for the initials.

## Hero story (one use case, UC1)

Westfield Parramatta logs a **P1** job: "Chiller 2 tripped, food court has no cooling". The dispatcher opens the
**dispatch desk**, sees the job flagged **at risk**, and the system has already **raised a task** for the dispatch
lead. The dispatcher asks **Creatio.ai** for a client update; it drafts one from the job, the dispatcher confirms,
and it is saved on the job.

## Why the lab uses its own objects (and a real deal wouldn't)

On a real deal a Kestrel job is a **Case** (reuse the stock object and its columns: `creatio-object-model` "reuse
the stock column"). Lab stands may be shared, so a trainee never changes stock objects: everything below is new and
carries the trainee's initials, so two trainees on one stand never collide.

## Object model (B1)

| Object | Kind | Columns |
|---|---|---|
| `<p>AcadXxJobPriority` | lookup | Name (P1 Emergency, P2 Urgent, P3 Standard, P4 Planned), SLA hours (number: 4, 24, 72, 240) |
| `<p>AcadXxJobStatus` | lookup | New, Allocated, On site, Waiting on client, Complete |
| `<p>AcadXxSite` | object | Name, Client (Account), Address, Induction required (boolean), Access notes (text) |
| `<p>AcadXxJob` | object | Number (text), Site, Client (Account), Priority, Status, Description, Technician (Contact), SLA due (date/time), At risk (boolean), Lead alerted (boolean), Client update (text, long) |

## Pages (B2)

Job form page (cloned from the **request** donor: header with status, Description, SLA due, Client update),
Job list page with quick filter on Status, Site mini page. Labels above fields, placeholders, nothing empty.

## Data and home page (B3)

3 sites (Westfield Parramatta: induction required; Macquarie Park office tower; Liverpool council depot) on existing
Accounts named "Kestrel lab client <Xx> …" (created by the lab). 8 jobs across the statuses, SLA due spread over the
next 2 days. **Hero record:** `KJ-1042`, Westfield Parramatta, P1, New, SLA due in 3 hours, At risk = yes.
Home page **Dispatch desk (Xx)**: KPIs open jobs and P1 at risk; chart jobs by status; list of at-risk jobs.

## Process (C1)

`<p>AcadXxP1Alert`: starts when a Job is added with Priority = P1 → adds a Task (Activity) "P1 <job number>: call
the client within 15 minutes", owner = the trainee's own contact → sets Lead alerted = yes. Native route, IsTracing on.

## AI skill (C2)

**Kestrel client update (Xx)**: on the open job, reads job, site, priority and status, drafts a 3-line client update
in Kestrel's voice, asks "Save this update to the job?", and only after yes writes Client update. Confirm-then-act.

## Prove, click path, harvest, reset (D1)

UC1 rehearsed on a twin of KJ-1042; click path cards; `sc-clickpath` pages into the practice folder; an L1 harvest
entry written to the practice folder only; then reset: lab records, then the lab app and package (SC's yes).
