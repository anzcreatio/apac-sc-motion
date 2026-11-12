# POC brief: Kestrel Facility Services

> From the fit-gap (`sc-rfp`), 2026-11-12. Input for `sc-demo-plan` in **proof mode**: it maps every Build line to a scene and a test. Internal.

| | |
|---|---|
| Build (live in the POC) | 6 lines, about 21.0 h of configuration per requirement (the plan adds data model, seed data, channels, AI, rehearsal and buffer: expect 2–3×) |
| Show (screenshot or clip) | 11 |
| Tell (written answer; the bid team) | 8 |
| Must-haves met without building anything | 66.7% |

## 1. Build: every line needs a scene and a test

Group these into 3–5 scenes around their journeys (and their named use cases, if the RFP has them). The plan's coverage table must list every ref below; `rfp.py coverage` checks it.

### 2. Job logged

| Ref | Requirement | How (fit) | Test (draft: the plan sharpens it) | Hours |
|---|---|---|---|---|
| W1-03 | ~The SLA due time is worked out from each client's contract, not one P1 to P4 list, and the clock pauses while the job is waiting on the client, for … | Service agreements (Service Creatio) hold response times per priority per contract with a working calendar; a 'waiting … (configure) | Draft: they see it work live on their example data (Service agreements (Service Creatio) hold response times per priority per contract with a working calendar; a 'waiting on client' status with the paused flag stops the clock, limited to contracts that allow it by a rule on the agreement.) | 4 |

### 3. Technician assigned

| Ref | Requirement | How (fit) | Test (draft: the plan sharpens it) | Hours |
|---|---|---|---|---|
| W1-06 | ~After hours, the dispatcher can approve a callout up to a set limit; above it, the on-call manager approves. | After-hours callout approval in a business process, with the limit held as data so the business changes it ($1,500 vs $… (configure) | Draft: they see it work live on their example data (After-hours callout approval in a business process, with the limit held as data so the business changes it ($1,500 vs $2,000) without IT.) | 3 |

### 4. Technician attends and diagnoses

| Ref | Requirement | How (fit) | Test (draft: the plan sharpens it) | Hours |
|---|---|---|---|---|
| W1-07 | ~Technicians can see the full job, fill in the job sheet, take photos and get the client's sign-off on their phone in basements, plant rooms and hosp… | Creatio mobile app configured for technicians (job, job sheet, photos) with offline mode and sync when back in signal. … (configure) | Draft: they see it work live on their example data (Creatio mobile app configured for technicians (job, job sheet, photos) with offline mode and sync when back in signal. Client signature capture offline and Freedom UI mobile offline coverage need a product check.) | 4 |

### 5. Quote and parts (in parallel)

| Ref | Requirement | How (fit) | Test (draft: the plan sharpens it) | Hours |
|---|---|---|---|---|
| W1-11 | ~The quote to the client (over the NTE) and the parts order to the supplier can run at the same time on the job, with the approval limits: quotes und… | Quote and parts order as their own records with approval processes (quote: supervisor under $10,000, Operations Manager… (configure) | Draft: they see it work live on their example data (Quote and parts order as their own records with approval processes (quote: supervisor under $10,000, Operations Manager over; parts: technician up to $500, supervisor above), both open on the job at once.) | 4 |

### 7. Invoice raised

| Ref | Requirement | How (fit) | Test (draft: the plan sharpens it) | Hours |
|---|---|---|---|---|
| W1-17 | ~The invoice line description is drafted from the technician's notes and the job sheet in client-friendly wording, and a billing officer checks it be… | A Creatio.ai skill drafts the invoice line from the tech notes and job sheet; the billing officer reviews and approves … (ai) | Draft: they see it work live on their example data (A Creatio.ai skill drafts the invoice line from the tech notes and job sheet; the billing officer reviews and approves it before it goes to MYOB.) | 3 |

### Across the journey

| Ref | Requirement | How (fit) | Test (draft: the plan sharpens it) | Hours |
|---|---|---|---|---|
| W1-22 | ~One job record from the client's request to the invoice, with the full set of statuses, including waiting on client, waiting on parts and return vis… | The job is a Service Creatio case captioned 'Job', with their statuses, including Waiting on client (clock paused), Wai… (configure) | Draft: they see it work live on their example data (The job is a Service Creatio case captioned 'Job', with their statuses, including Waiting on client (clock paused), Waiting on parts and Return visit booked.) | 3 |

## 2. Gaps to handle in the POC story

Don't hide them: show the workaround or say how it's handled. These are the evaluator's likely questions.

| Ref | Requirement | Fit | Workaround |
|---|---|---|---|
| | None | | |

## 3. Show: evidence to collect (library screenshots, clips, standard screens)

| Ref | Requirement | Evidence |
|---|---|---|
| W1-02 | ~Something reads the client's email, pulls out the site, the contact and what's broken, and drafts the job; t… | D3; email-to-case in Service Creatio (Academy); AI-GOVERNANCE-PACK-LITE-v0.1 'can say': in-country AI hosting… |
| W1-05 | ~At assignment, the dispatcher can see whether the technician has the site's induction. | Business Studio objects and business rules |
| W1-08 | ~Clients are told when the technician is on the way, on site and done, without ringing dispatch. | Creatio Marketplace SMS connector (check) |
| W1-09 | ~Before arriving, the technician gets a summary of the site's job history: the last visits to that plant room… | D3; AI-GOVERNANCE-PACK-LITE-v0.1 'can say': in-country AI hosting incl. Australia; residency, retention and p… |
| W1-10 | ~When the technician's estimate goes over the client's not-to-exceed amount, the technician is prompted to ra… | Business rules on mobile pages (check offline behaviour) |
| W1-13 | ~The return visit is booked as soon as both are done: the client has said yes and the part has arrived, and d… | Business processes (parallel paths with a join) |
| W1-14 | ~Finance can see which jobs are ready to invoice before they land on the desk. | Freedom UI lists and dashboards |
| W1-15 | ~A return visit can be told apart from a new job, so first-time fix is measured rather than guessed. | Business Studio objects and dashboards |
| W1-18 | ~If the invoice is more than ten percent over the quote, it goes back to operations to explain before it's se… | Business rules and processes |
| W1-21 | ~A quick client feedback survey after the job. | Service Creatio case satisfaction (object model: Case.SatisfactionLevel) |
| W1-23 | ~Dispatch sees every open job, what's about to breach and where the technicians are, so a P1 about to breach … | Freedom UI dashboards; D5 |

## 4. Questions to settle before building

- **W1-01**: Which two portals have an API, and can we see the documentation?
- **W1-03**: Which contracts allow the pause?
- **W1-06**: Is the limit $1,500 or $2,000?
- **W1-08**: Do clients want SMS, email or both?
- **W1-13**: Who records that a part has arrived (depot or site)?
- **W1-16**: How often: as it happens, same day or end of day?
- **W1-19**: Should this be in the new system or stay in MYOB AP?
- **W1-20**: Which portals have an API?
- **W1-23**: Which fleet GPS system, and can it share locations?
- **W1-24**: Which client contracts have data clauses?
- **W1-27**: Which client contracts carry data clauses?

## 5. Low-confidence lines to confirm (product or SC)

- **W1-07** (configure): ~Technicians can see the full job, fill in the job sheet, take photos and get the client's sign-off on their phone in basements, plant room…
- **W1-10** (configure): ~When the technician's estimate goes over the client's not-to-exceed amount, the technician is prompted to raise a quote before doing the w…
- **W1-19** (integration): ~Maybe: the supplier's invoice is read and matched to the job by the PO number or the site address (depends on accounts payable staying in …
- **W1-20** (integration): ~For portal clients, the invoice and the signed job sheet go into the client's portal with the job number the portal expects.
- **W1-24** (ai): ~Client data in emails and job notes (names, phone numbers, hospital ward details, photos) is handled in line with the clients' contract cl…
- **W1-27** (standard): ~A written answer on where client data is processed by AI, what's kept and what can be switched off per client, for the risk committee.

SC check required before this is used with the customer or the bid team.
