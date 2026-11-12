# Solution model: Kestrel Facility Services

> `sc-workshop`, 2026-11-12. Their world in Creatio terms, for `sc-demo-plan` (Part 1, Part 2, example data, home page) and the toolkit runbook. Internal. Tags: C confirmed in the room · I inferred · A assumed.

## Outcomes

| id | measure | baseline | target | owner | tag | src |
|---|---|---|---|---|---|---|
| out:sla-breach | Reactive jobs that breach their SLA (mostly response: the attend-within time) | About 14% (12% to nearly 18% by month); abatements about $41k last quarter on the two contracts that enforce them | Under 5% | Greg Halloran, Operations Manager | C | W1 00:10:12 |
| out:first-time-fix | First-time fix | About 70-75%, an estimate: not measured today | Not set yet: to be agreed once it can be measured | Ravi Menon, Field Technician Supervisor | C | W1 00:11:32 |
| out:invoice-lag | Days from job complete to invoice sent | 19 days on average (3 days to 6 weeks) | 5 days | Not agreed: finance (sends the invoice) or operations (closes the job) | C | W1 00:12:29 |

## Things they track (objects)

| id | their_word | kind | creatio | schema | fields | volume | tag | src |
|---|---|---|---|---|---|---|---|---|
| obj:Job | Job | transaction | Case |  | Job number → Client → Site → Site contact → Description → Priority (P1-P4) → Contract → SLA due time → Source (email, portal, phone) → Client portal job number → After hours → Assigned technician → Status | About 5,500/month (more in summer); 600-700 after hours (dispatch estimate, summer) | C | W1 00:11:22, 00:26:35 |
| obj:Client | Client | master | Account |  | Name → Portal client (yes/no) → Contracts |  | C | W1 00:44:21 |
| obj:Site | Site | master | new | UsrSite | Client → Address → Induction required → Access notes |  | I | W1 00:44:21, 00:48:52 |
| obj:Contract | Contract | master | ServicePact |  | Client → Not-to-exceed (NTE) amount → Response times by priority → Clock pauses while waiting on client → Abatements apply |  | C | W1 00:26:49, 00:27:58 |
| obj:Quote | Quote | transaction | new | UsrQuote | Job → Amount → What's needed → Built by → Approved by → Client decision | About 1 in 10 jobs (~550/month; Greg's guess, more in summer) | C | W1 00:28:22, 00:33:08 |
| obj:PartsOrder | Parts order | transaction | new | UsrPartsOrder | Job → Supplier → Part → Cost → PO number (from MYOB) → Ordered by → Approved by → Deliver to (depot or site) |  | C | W1 00:40:41 |
| obj:JobSheet | Job sheet | transaction | new | UsrJobSheet | Job → Hours → Parts used → What was done (tech notes) → Photos → Client signature | One per attendance (about 5,500 jobs/month plus return visits) | C | W1 00:45:43, 01:37:06 |
| obj:Visit | Return visit | transaction | Activity |  | Job → Technician → Booked for → On site → Done | To confirm (Ravi; JobTrak can't tell, the export may help) | C | W1 00:42:40 |
| obj:Technician | Technician | master | Contact |  | Trade → State / region → Subcontractor → Site inductions held → Mobile | About 400 (about 60 subcontractors) | C | W1 00:02:13 |
| obj:Supplier | Supplier | master | Account |  | Name → Trade (HVAC, electrical, plumbing, fire) | About 5 main suppliers | C | W1 00:40:41 |

## Stages

| id | object | stages | end_states | who_moves | branches | note | tag | src |
|---|---|---|---|---|---|---|---|---|
| stg:Job | obj:Job | New → Allocated → Dispatched → On Site → Waiting on client → Waiting on parts → Return visit booked → Complete → Closed → Cancelled | Closed → Cancelled | New: Dispatcher (assigns a technician); Allocated: Dispatcher (rings or texts the technician); Dispatched: Technician ('on site'; today an SMS to dispatch, often forgotten); On Site: Technician / dispatcher (quote or parts needed, or done); Waiting on client: Client approves or declines the quote; dispatch records it (I: dispatch emails the quote, 00:33:29); Waiting on parts: None; Return visit booked: Technician ('done'); Complete: Dispatcher, once the job sheet is in; Closed: End: finance invoices in MYOB | yes | Quote to client (over NTE) and parts order to supplier can be open at once; the return visit is booked only when both are done. One stage column can't hold that: the Quote and Parts order records carry their own status and a process joins them and moves the job to Return visit booked. New statuses asked for: Waiting on client, Waiting on parts, Return visit booked (W1 00:59:16). | C | W1 00:27:22, 00:42:40, 00:59:16 |
| stg:Quote | obj:Quote | Draft → Internal approval → Sent to client → Approved or declined | Approved or declined | Draft: Dispatcher (smaller jobs, Word template) or supervisor (big ones); Internal approval: Supervisor under $10,000; Operations Manager over $10,000; Sent to client: Client (property manager); the dispatcher records the answer | no |  | I | W1 00:33:20-00:34:14 |
| stg:PartsOrder | obj:PartsOrder | Requested → Ordered → Arrived |  | Requested: Technician up to $500; a supervisor above that; Ordered: None | no |  | I | W1 00:40:56-00:42:13 |

## Roles

| id | name | does | approves | count | tag | src |
|---|---|---|---|---|---|---|
| role:dispatcher | Dispatcher | Logs jobs, works out the SLA due time, assigns and rings technicians, updates statuses, builds small quotes | After-hours callouts up to the limit (disputed) | 22 (14 Parramatta, 5 Melbourne, 3 Brisbane) | C | W1 00:01:55 |
| role:dispatch-lead | Dispatch Team Lead | Runs the dispatch team |  | 1 | C | W1 00:01:55 |
| role:after-hours-dispatcher | After-hours dispatcher | Covers after hours from home; writes overnight jobs in a Word doc | After-hours callouts up to the limit | Usually 2 on the roster | C | W1 00:01:55, 00:49:57 |
| role:on-call-manager | On-call manager | Approves after-hours callouts above the dispatcher's limit | After-hours callouts above the limit |  | C | W1 00:29:55 |
| role:technician | Technician | Attends, diagnoses, does the work, fills in the job sheet | Parts orders up to $500 | About 400 (about 60 subcontractors) | C | W1 00:02:13 |
| role:supervisor | Field technician supervisor | Builds quotes for big jobs, orders big parts | Quotes under $10,000; parts orders over $500 |  | C | W1 00:33:22, 00:41:34 |
| role:ops-manager | Operations Manager | Owns SLA reporting to clients; signs off the workshop playback | Quotes over $10,000 | 1 | C | W1 00:34:10 |
| role:ops-coordinator | Operations coordinator | Corrects the monthly SLA report by hand (two days a month) |  | 1 | C | W1 00:33:51 |
| role:billing-officer | Billing officer | Rewrites tech notes into invoice lines, keys invoices into MYOB, uploads to client portals |  | To confirm (Leanne, this week) | C | W1 00:45:56, 00:46:30 |

## Rules

| id | rule | value | disputed | tag | src |
|---|---|---|---|---|---|
| rule:sla-per-contract | SLA attend-within time per client contract and priority | P1 4 hours metro (2 hours for the hospitals); P2 next business day; varies by contract | no | C | W1 00:10:26 |
| rule:sla-pause | SLA clock pauses while the job is waiting on the client's quote approval, where the contract allows | Contract by contract: most property managers, not the hospitals (Greg to confirm the list) | no | C | W1 00:59:16 |
| rule:nte | Not-to-exceed amount per contract: under it the job just gets done; over it needs a quote | $1,000 for most; $500 for a couple of councils; $2,500 for one shopping centre group | no | C | W1 00:27:58 |
| rule:quote-approval | Internal approval before a quote goes to the client | Supervisor under $10,000; Operations Manager over $10,000 | no | C | W1 00:34:10 |
| rule:parts-approval | Parts order approval | Technician up to $500; supervisor above | no | C | W1 00:41:34 |
| rule:afterhours-callout | After-hours callout: dispatcher approves up to a limit, the on-call manager above it | $1,500 (dispatch's after-hours guide) or $2,000 (Greg: raised last financial year) | yes | C | W1 00:30:08-00:30:43 |
| rule:over-quote-check | Invoice more than this over the approved quote goes back to operations to explain before it's sent | 10% | no | C | W1 00:46:58 |
| rule:nte-overage | Work over the NTE without an approved quote can't be billed (written off) | Any amount over the NTE | no | C | W1 00:46:58 |
| rule:return-visit-trigger | Return visit booked only when the client has approved the quote (if any) and the part has arrived (if any) | Both done | no | C | W1 00:42:40 |
| rule:induction | Technician must hold the site's induction where the site requires one; checked at assignment | Per site: induction required yes/no; per technician: inductions held (kept in a spreadsheet today) | no | C | W1 00:48:52 |
| rule:po-on-parts | Every parts order gets a MYOB purchase order number, recorded on the job | PO number from MYOB | no | I | W1 00:41:50 |

## Systems

| id | name | owns | direction | frequency | tag | src |
|---|---|---|---|---|---|---|
| sys:JobTrak | JobTrak (in-house job system) | Jobs and statuses today; end of life, about 18 months left; being replaced (board decision) | in | One-off (history migration not discussed) | I | W1 00:43:57 |
| sys:MYOB | MYOB Advanced | Finance, payroll, purchasing (PO numbers), AP, invoicing; the client and site list. Stays | both |  | C | W1 00:44:08-00:44:52 |
| sys:Outlook | Microsoft 365 / Outlook shared mailbox (jobs@) | Client job emails (about 60% of requests). Stays | in | Continuous | C | W1 00:25:36, 00:45:09 |
| sys:ClientPortals | Three client (property manager) portals | Clients' work orders (about 25% of requests) and invoice + job sheet uploads. Clients' systems: can't be changed; two may have an API, one is a website only | both | Checked by hand, meant to be every 15 minutes | C | W1 00:25:44, 00:44:58, 00:47:28 |
| sys:FleetGPS | Fleet GPS system (vans) | Van locations; dispatch has no login | in |  | I | W1 00:29:02 |
| sys:Spreadsheets | Dispatch spreadsheets | Contract SLA times per client; site inductions held | in | One-off load, then replaced | C | W1 00:26:49, 00:49:08 |

## Channels and devices

| id | step | channel | where | tag | src |
|---|---|---|---|---|---|
| chn:intake | 1. Request received | email | About 60% email (shared mailbox), 25% client portals, 15% phone (mostly after hours or urgent) | C | W1 00:25:24 |
| chn:tech-mobile | 4-5. Technician on site | phone app | On site; basements, plant rooms, lifts and hospitals have no signal: must work offline and catch up later | C | W1 00:31:51-00:32:36 |
| chn:after-hours-home | 2. Job logged (after hours) | web | After-hours dispatchers at home; JobTrak is unusable over the VPN | C | W1 00:49:57-00:50:13 |
| chn:client-updates | 3-5. Tech on the way, on site, done | SMS | To the client: on the way, on site, done (channel not discussed; SMS assumed) | A | W1 00:50:41 |
| chn:dispatch-room | Across the journey | web | Big screen in the dispatch room | C | W1 00:13:35 |
| chn:portal-upload | 8. Invoice sent | portal | Invoice and job sheet uploaded into the client's portal | C | W1 00:47:28 |

## AI moments

| id | task | today | who_confirms | data | tag | src |
|---|---|---|---|---|---|---|
| ai:invoice-line | Draft the invoice line description from the technician's notes and job sheet, in client-friendly wording | Billing team rewrites tech notes by hand: 2 minutes a job, 10 if they ring the tech; most of the 5,500 jobs a month | Billing officer, before it goes (at least to start with) | Tech notes, job sheet | C | W1 01:20:28-01:20:59 |
| ai:job-from-email | Read the client's email and draft the job: site, contact, what's broken, suggested priority | Dispatcher copies the email into JobTrak: 5-15 minutes a job | Dispatcher checks every job; the priority always needs a human eye | Client emails, which can hold names, phone numbers, hospital ward details and photos (data concern: Darren) | C | W1 01:21:02-01:21:29, 01:21:58 |
| ai:site-history | Summarise the site's job history for the technician before they arrive | Techs go in blind | Nobody: informational, the technician uses it or not | Past jobs and job sheets for the site | C | W1 01:21:32-01:21:52 |
| ai:supplier-invoice-match | Read a supplier invoice and match it to the job by PO number or site address (a 'maybe') | Finance can't match supplier invoices to jobs | Not discussed: depends on the answer in open | Supplier invoices (AP lives in MYOB) | C | W1 01:23:14-01:23:26 |

## Example data

| id | what | status | tag | src |
|---|---|---|---|---|
| ex:job-sheet | Job sheet spreadsheet used for the big clients, client names stripped (Shannon, this week) | asked |  |  |
| ex:jobtrak-export | One month of JobTrak jobs, anonymised: real statuses and timings (Darren, after the privacy officer, about a week) | asked |  |  |
| ex:sla-spreadsheet | Contract SLA times spreadsheet | asked |  |  |
| ex:quote-template | The Word quote template | none |  |  |

## Requirements in the register

25 ours: 3 must, 4 should, 3 could, 15 not ranked; 23 tagged C.

## Gaps (24)

| Where | Missing | Follow-up question |
|---|---|---|
| obj:Client | no volume | Roughly how many clients do you have? |
| obj:Site | no volume | Roughly how many sites do you have? |
| obj:Contract | no volume | Roughly how many contracts do you have? |
| obj:PartsOrder | no volume | Roughly how many parts orders a month? |
| stg:Job | nobody moves it on from: Waiting on parts | Who moves a job on from “Waiting on parts”? |
| stg:PartsOrder | nobody moves it on from: Ordered | Who moves a parts order on from “Ordered”? |
| role:on-call-manager | no head count | Roughly how many on-call managers are there? |
| role:supervisor | no head count | Roughly how many field technician supervisors are there? |
| sys:MYOB | no frequency | *ours to fix* |
| sys:FleetGPS | no frequency | *ours to fix* |
| rule:afterhours-callout | open question | Is the dispatcher's after-hours callout limit $1,500 or $2,000? (The after-hours guide and the team still use $1,500.) |
| sys:MYOB | open question | How often should completed jobs go to MYOB, and clients and sites come back: as it happens, same day, or end of day? (Leanne would like same day at least.) |
| rule:sla-pause | open question | Which contracts allow the SLA clock to pause while a quote is with the client? |
| out:first-time-fix | open question | Once first-time fix can be measured, what target would you set? (No number needed yet.) |
| out:invoice-lag | open question | Who should own invoice lag (job complete to invoice sent): finance, operations, or both? |
| role:billing-officer | open question | How many people in finance process invoices, including the AP helpers at month-end and the part-timer in Melbourne? |
| obj:Visit | open question | Roughly how many return visits a month, and how many of those are waiting on a part? |
| ai:job-from-email | open question | Which client contracts have data clauses we should check our written answer on AI and client data against? |
| sys:ClientPortals | open question | Which of the three client portals have an API, and can you share their names or documentation? |
| sys:FleetGPS | open question | Which fleet GPS system are the vans on, and could it share van locations with the new system? |
| sys:JobTrak | open question | Do you want job history brought across from JobTrak, and if so how far back? |
| ai:supplier-invoice-match | open question | Is matching supplier invoices to jobs something you'd want in the new system, or does it stay with accounts payable in MYOB? |
| W1-22 | open question | Should a short client feedback survey after each job be on the list? (Not ranked in workshop 1.) |
| W1-27 | our action: Send the written answer on where client data is processed by AI, what's kept and what can be switched off (governance pack can-say lines; Creatio security for the rest) | *ours to fix* |
