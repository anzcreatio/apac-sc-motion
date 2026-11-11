# Manufacturing pack v0.1 (overlay on Core)

## 0. Pack header
| Field | Value |
|---|---|
| Pack | **Manufacturing** (overlay). Lists only what differs from or adds to the Core pack; everything else is inherited |
| Inherits from | Core v0.1 (`CORE-PACK-v0.1.md`) |
| Owner (SC) | (to assign) |
| Version / date | v0.1 · 3 Nov 2026 |
| Segments covered | Discrete and process manufacturers selling B2B and through dealers/distributors: industrial equipment, building products, packaging, consumer goods, **contract manufacturing** (incl. TGA-licensed therapeutic goods and food). AU first; then ID, MY, VN, SG, NZ. **Not** covered: MES/shop floor, production planning, batch release (these stay in ERP/MES/QMS) |
| Deals harvested | Pact Group (AU, contract manufacturing + packaging), discovery stage. Research: `manufacturing-pack-research-2026-11-03.md` (design workspace `research/`, not in the plugin) |

> **Status: draft.** §4 and §6 come from the research pass (each row flagged). Everything in §1–§3, §5, §8 and §9
> without a footnote is **A (Assumed)** until a deal confirms it.
>
> **How this overlay changes the Core motion (read this first):**
> 1. **Lead with one use case and coexistence, not with "CRM".** Manufacturing deals are often *not* CRM replacements.
>    The ERP (often SAP) stays, the incumbent CRM may stay (Pact: Microsoft Dynamics), and existing AI agents stay.
>    The pitch is "one process, live in weeks, running alongside what you have." (Pact lesson, §10.)
> 2. **D5 (Fits your landscape) appears in every manufacturing demo, P or A.** The catalogue makes D5 track core only
>    for A. This overlay *adds* it for P too; it doesn't remove D2. **Needs Renzo's sign-off** (the core set is his call).
> 3. **D2 is shown inside the use case** ("one record from dealer claim to supplier recovery"), never as "move
>    everything onto one platform", which fights the coexistence story.
> 4. **Core §7 "incumbent CRM: goes or coexists; replace at renewal" is overridden:** in manufacturing, assume the
>    incumbent CRM stays. Don't plan a replacement unless the customer raises it.

---

## 1. Top pains and consequences (additions to Core CP1–CP10)

Sector context (Strong, Ai Group Oct 2026 [1]): productivity growth **−2.9%**, input prices **+10.7%** in 2025-26,
**52%** of manufacturers report recruitment difficulty. Process-level pains below are **A (Assumed)**; the context
explains *why* they hurt now (cost, productivity, skills), not that they exist at a given customer.

| ID | Pain (internal wording) | Consequence | Typical owner | Journey |
|---|---|---|---|---|
| MP1 | Configured / made-to-order quotes need engineering and pricing checks by a few experts | Slow quotes; lost tenders; margin leakage from inconsistent discounts | GM Sales / Estimating | MJ1 |
| MP2 | Won quotes re-keyed into the ERP; specs lost between sales and production | Order errors, rework, credit notes; OTIF misses | Customer service / order desk | MJ1 |
| MP3 | Warranty claims arrive by email/PDF from dealers and are checked by hand | Slow dealer reimbursement; fraud and duplicate claims slip through; warranty cost ≈1.3% of sales in US data [3] | Service / warranty manager | MJ2 |
| MP4 | Warranty costs paid but not recovered from component suppliers | Recoverable cost written off; ACL s274 gives *suppliers* recovery rights against manufacturers, so the manufacturer carries the cost [17] | Warranty / Finance | MJ2 |
| MP5 | Dealers and distributors have no self-service view of orders, claims, stock, programmes | Calls and emails to the order desk; weak dealer loyalty; channel data invisible | Channel / Sales ops | MJ2, MJ1 |
| MP6 | Field technicians lack service history and parts information | Repeat visits (low first-time fix); cost per job; customer downtime | Service manager | MJ2 |
| MP7 | Customer complaints not linked to batch/lot, NCR or CAPA | Slow root cause; recall scope unclear; audit findings | Quality manager | MJ3 |
| MP8 | CAPAs overdue; evidence gathered by hand for audits (GMP, food, ISO 9001) | Regulator or customer audit findings; licence risk (TGA has fined a manufacturer for licence breaches [13]) | Quality / Regulatory | MJ3 |
| MP9 | Reportability decisions (ACCC 2-day, TGA recall) depend on a few experts | Missed statutory clocks; inconsistent decisions [15][16] | QA / Regulatory affairs | MJ3 |
| MP10 | Contract-manufacturing clients (brand owners/sponsors) chase status by email | Relationship strain; account managers as human routers | Contract manufacturing BU | MJ1, MJ3 |
| MP11 | IT landscape fixed (ERP + CRM + AI agents); any new tool is "another silo" | CIO says no to platforms; only a scoped use case with a clear integration story gets through | CIO / enterprise architect | All |

## 2. Hypothesis library

Slide wording ≤12 words, an industry observation the customer can say "no" to. All rows **A (Assumed)** until logged.
Use Core C-H01…C-H14 as well; the most relevant in manufacturing are **C-H03** (quote approvals), **C-H06** (re-keying),
**C-H10** (change backlog) and **C-H13** (AI pilots stall).

| ID | Slide wording | Track | Usual owner | Journey / task | KPI | D-IDs | Signals that make it likely (W1 research) | Hit / miss |
|---|---|---|---|---|---|---|---|---|
| M-H01 | Warranty claims are checked by hand against serial and entitlement | P | Service / warranty manager | MJ2 · MAI-T1 | Claim cycle time; cost per claim | D3, D2 | Dealer network; multi-year warranties; claim forms as PDF on the website; consumer goods (ACL) | |
| M-H02 | Dealers phone or email to ask order, claim and stock status | P | Channel / sales ops | MJ2 · MAI-T4 | Calls per dealer per month; portal order share | D2, D5 | "Find a dealer" page; no dealer login on the website; distributor-led markets (ID, VN) | |
| M-H03 | Configured quotes wait days for engineering and pricing checks | P | GM Sales / estimating | MJ1 · MAI-T3 | Quote turnaround; quote-to-win % | D4, D1, D3 | Made-to-order or configurable products; "request a quote" forms; tender-driven sales | |
| M-H04 | Won quotes are re-keyed into the ERP as sales orders | P | Order desk / customer service | MJ1 | Order-entry time; order error rate | D5, D2 | SAP/Pronto/Epicor job ads mentioning "order entry"; separate CRM and ERP | |
| M-H05 | Customer complaints sit in inboxes, not linked to batch or lot | P | Quality manager | MJ3 · MAI-T2 | Complaint closure time; % complaints linked to batch | D2, D5 | TGA- or food-regulated products; recalls on the ACCC/TGA/FSANZ lists; ISO 9001 | |
| M-H06 | Corrective actions stay open long after the root cause is known | P | Quality manager | MJ3 · MAI-T6 | CAPA cycle time; % CAPAs overdue | D4, D1 | Audit findings mentioned publicly; QA hiring; GMP licence | |
| M-H07 | Whether a complaint is reportable depends on one expert's judgement | P / A | QA / regulatory affairs | MJ3 · MAI-T2 | Time to reportability decision; reports within 2 days | D3, D4 | Consumer goods (ACCC mandatory reporting); TGA sponsor or contract manufacturer | |
| M-H08 | Warranty costs get paid but rarely recovered from suppliers | P | Warranty manager / Finance | MJ2 · MAI-T7 | % warranty cost recovered | D2, D5 | Imported components; OEM assembly; warranty provision in the annual report | |
| M-H09 | Technicians arrive without the service history or the right parts | P | Service manager | MJ2 · MAI-T5 | First-time fix rate; repeat visits | D2, D3 | Installed equipment; service agreements; field technician job ads | |
| M-H10 | Sales can't see ERP orders, credit and stock in one place | P | GM Sales / key account manager | MJ1 · MAI-T8 | Prep time per account; order-status calls | D5, D2 | SAP + separate CRM; sales reps asking customer service for order status | |
| M-H11 | Key-account forecasts live in spreadsheets, disconnected from the ERP | P | Key account / demand planning | KAM · MAI-T8 | Forecast accuracy; time to build the forecast | D2, D4 | Retail/grocery customers; S&OP mentions; contract volumes | |
| M-H12 | Contract-manufacturing clients chase project and batch status by email | P | Contract manufacturing BU | MJ3, MJ1 · MAI-T4 | Status enquiries per client; NPS | D2, D5 | Contract/toll manufacturing division (e.g. Pact's Jalco, Pascoes, APM [32]) | |
| M-H13 | A new CRM project is off the table; one use case isn't | P / A | CIO | All | Weeks to first live use case | D5, D6 | CRM already in place; recent ERP programme; CIO talks "architecture" | ✔ Pact (CIO) |
| M-H14 | AI pilots answer questions but don't act inside ERP-driven processes | A | CIO / Operations | MAI-T1–T8 | Tasks completed by agents; minutes saved | D3, D5 | Copilot or other agents already deployed; AI mentioned in annual report; Ai Group: 53% use standalone AI [1] | |
| M-H15 | Changing a warranty rule or dealer programme needs an IT project | P | Service / channel manager | MJ2 | Time to change a rule | D1, D4 | Annual dealer programme changes; rules in ERP customisations | |

## 3. Reference journeys (3)

Chosen because they (a) sit *around* the ERP rather than inside it, so coexistence is natural, (b) carry a
regulatory or cash hook, and (c) each have an obvious AI task. Dealer portal is folded into MJ2 (and MJ1 for dealer
quotes). KAM/forecast collaboration stays as hypotheses (M-H10, M-H11) only; it's weaker as a first use case. **A (Assumed).**

### MJ1 · Configured quote to ERP order (overlay of Core J1)
| Step | Neutral term | Customer terms we've heard | Who | Usual system | Typical break |
|---|---|---|---|---|---|
| 1 | Request received | RFQ, enquiry, tender, spec, drawing | Customer / dealer → inside sales | Email, web form, tender portal | ⚠ Specs arrive as PDFs/drawings; re-read by hand |
| 2 | Qualify and check feasibility | technical review, feasibility, "can we make it" | Estimator / engineering | Email, spreadsheet, CAD/PLM | ⚠ Queues on 1–2 experts |
| 3 | Configure and cost | configure, BOM, costing, price build-up | Estimator | Spreadsheet, ERP price conditions | ⚠ Spreadsheet pricing; stale material costs |
| 4 | Approve price and terms | margin approval, discount approval, deal desk | Sales manager / GM / Finance | Email | ⚠ Waits in inboxes (Core C-H03) |
| 5 | Send quote and follow up | quotation, offer, revision | Sales rep / dealer | Word/PDF, CRM | Revisions not versioned |
| 6 | Win and confirm | PO received, order acknowledgement | Customer → order desk | Email | |
| 7 | Create sales order in ERP | order entry, SO, job | Order desk | **ERP (stays)** | ⚠ Re-keyed; spec lost; credit check missed |
| 8 | Confirm delivery date and track | ATP, delivery date, order status | Order desk / sales | ERP | ⚠ Sales and customer can't see status → calls |

### MJ2 · Warranty claim to resolution and supplier recovery (overlay of Core J3)
| Step | Neutral term | Customer terms we've heard | Who | Usual system | Typical break |
|---|---|---|---|---|---|
| 1 | Claim submitted | warranty claim, RMA, return, service request | Dealer / end customer | Email, PDF form, phone | ⚠ Incomplete: no serial, photos or proof of purchase |
| 2 | Check entitlement | warranty check, serial lookup, coverage | Warranty administrator | ERP (serial/sales history), spreadsheet | ⚠ Manual lookups across ERP screens |
| 3 | Triage and decide route | assess, inspect, repair vs replace | Warranty admin / technical | Email | ⚠ Experts as bottleneck; inconsistent decisions |
| 4 | Field visit or return | service job, dispatch, return to depot | Service coordinator / technician | Field service tool, calendar | ⚠ No history or parts info → repeat visit |
| 5 | Repair / replace / credit | repair, swap-out, credit note | Technician / order desk | ERP (parts, credit note) | ⚠ Credit re-keyed into ERP |
| 6 | Reimburse dealer | claim payment, labour reimbursement | Warranty admin / Finance | ERP (AP) | ⚠ Dealer waits weeks; calls to chase |
| 7 | Recover from supplier | supplier claim, chargeback, back-charge | Warranty / procurement | Email, spreadsheet | ⚠ Not done or not tracked (M-H08) |
| 8 | Analyse and feed quality | failure analysis, Pareto, NCR | Quality | Spreadsheet | Patterns found late; links to MJ3 |

### MJ3 · Customer complaint to CAPA (incl. regulated contract manufacturing; overlay of Core J3)
| Step | Neutral term | Customer terms we've heard | Who | Usual system | Typical break |
|---|---|---|---|---|---|
| 1 | Complaint received | product quality complaint, customer complaint, feedback, adverse event | Customer / brand owner / sponsor → customer service | Email, phone, portal | ⚠ Logged in inboxes; missing batch/lot |
| 2 | Log, identify batch and classify | complaint register, batch/lot lookup, severity | Customer service / QA | ERP (batch), QMS or spreadsheet | ⚠ Batch lookup by hand |
| 3 | Assess reportability | reportable?, health hazard evaluation, recall assessment | QA / regulatory affairs | Email, expert judgement | ⚠ One expert; statutory clocks (ACCC 2 days [15][16]; TGA PRAC [14]) |
| 4 | Investigate | investigation, root cause, 5-why, retained sample | QA / production | QMS, LIMS, paper | ⚠ Evidence scattered |
| 5 | Raise NCR / CAPA | non-conformance, deviation, CAPA | QA | QMS or spreadsheet | ⚠ CAPA owners in other teams; no reminders |
| 6 | Respond to the customer | complaint response, investigation report | QA / account manager | Email, Word | ⚠ Slow; brand owner chases status (M-H12) |
| 7 | Verify effectiveness and close | effectiveness check, closure | QA manager | QMS | ⚠ CAPAs left open (M-H06) |
| 8 | Trend and report | complaint trending, management review, audit pack | QA manager | Spreadsheet | ⚠ Audit evidence compiled by hand |

**Scope line for MJ3 (important):** Creatio runs intake, routing, customer communication, tasks and deadlines. Where a
GMP-validated QMS exists (batch release, deviations), it **stays** and Creatio hands over to it. If Creatio itself holds
GMP records, PIC/S Annex 11 (computerised systems) applies [13] and the *customer* must validate it. Never claim
"GMP-compliant" or "validated".

## 4. KPI benchmarks (manufacturing additions)
Detail and caveats: `the research file` (design workspace `research/`, not in the plugin). Core rule applies: use for
**range questions**, quote only Strong rows (attributed), and never cite competitor research.

| KPI | Journey | Typical range | Range question | Source + date | Quality |
|---|---|---|---|---|---|
| Warranty claims as % of product sales | MJ2 | **1.30%** avg (US, 2025); autos ~2–3.4% | "Is warranty closer to 0.5, 1.5 or 3% of sales for you?" | Warranty Week, SEC-filing analysis, 2026 [3] | **Strong** (method), **US only** |
| Warranty accrual as % of sales | MJ2 | **1.43%** avg (US, 2025) | Use with Finance: "What do you provision each year?" | Warranty Week, 2026 [3] | **Strong**, US only (2025 figure via summary) |
| Cost to process one warranty claim | MJ2 / MAI-T1 | USD ~18–65 (vendor estimates) | "Roughly how many hours does one claim take end to end?" | Vendor blogs, 2025–26 [12]; APQC measure exists but paywalled [33] | **Weak** |
| Warranty claim resolution time | MJ2 | 3–7 days (vendor) | "Days, weeks or a month before a dealer is paid?" | Vendor blogs [12] | **Weak** |
| First-time fix rate (field service) | MJ2 | Avg ~75–80%; best-in-class ~88% | "Closer to 70, 80 or 90%?" | Aberdeen, 2013 (secondary) [4] | **Medium**, old |
| Quote lead-time reduction with configurators | MJ1 | Avg **85.5%** reduction (estimated, engineering-oriented firms) | "How long does a configured quote take: hours, days or weeks?" | Haug, Hvam & Mortensen, *AI EDAM* (Cambridge), ~2012 [5] | **Medium** (peer-reviewed, small sample, old) |
| ETO quoting practice | MJ1 | Top performers >2× as likely to use configurators; 53% more likely to automate quotes | Context only | Tech-Clarity, ~2016 [6] | **Medium**, old |
| Quote turnaround (absolute) | MJ1 | Inherit Core row (24 h–4.5 days) | Core | CPQ-vendor blogs | **Weak** |
| CAPA time to closure | MJ3 | Common *targets*: minor 30 d, major 45 d, critical 60 d | "How many CAPAs are past their due date right now?" | AssurX (vendor), 2022 [7] | **Weak** (targets, not actuals) |
| OTIF | MJ1 | "Good" is 95–99%; definitions vary so much that comparisons mislead | Ask their definition first, then "closer to 85, 90 or 95%?" | DHL glossary [9] (Weak); McKinsey on definitions [8] (Strong for the caveat) | **Weak** |
| Customer portal demand vs availability (distribution) | MJ2 | ~30% of distributors offer a portal; >70% of customers prefer online service | "What share of your dealers would order online if they could?" | Industrial Distribution, date not shown [11] | **Weak** |
| Aftersales portal use (B2B buyers aware of one) | MJ2 | 79% use them | Context only | Spryker-commissioned survey, ~2024 [10] | **Medium** (vendor) |
| AI adoption, AU manufacturers | All (AI) | 53% standalone AI, 29% embedded AI (last 12 months) | "Where is AI already in use here?" | Ai Group, Oct 2026 [1] | **Strong** |
| Recruitment difficulty, AU manufacturers | All | 52% (vs 45% all industries) | Supports "do more with the same team" | Ai Group, Oct 2026 [1] | **Strong** |
| TGA recall reporting clock | MJ3 | Interim report **6 weeks**, close-out **12 weeks** after the action starts | Not a benchmark: an SLA to build in | TGA PRAC, from 5 Mar 2025 [14] | **Strong** (regulator; read via summary) |
| % warranty cost recovered from suppliers; dealer portal order share; complaint closure time; CAPA % overdue | MJ2, MJ3 | **No credible source found** | Ask open: "What does it look like today?" | — | — |

**Don't use:** the "FDA CAPA average >400 days" figure (unclear whose process it measures); portal-vendor "60–80% of
orders move to the portal" claims; vendor "AI processes 75–85% of claims" claims.

## 5. Personas and terminology (manufacturing additions to Core §5)
| Persona | What they do all day | What they look at | What they'd love to stop doing |
|---|---|---|---|
| CIO / enterprise architect | Protects the ERP; rationalises apps; AI strategy | Architecture, integration, licences, risk | Adding "another silo"; custom ERP modifications |
| GM Sales / Commercial | Margin, key accounts, channel | Quote pipeline, margin, OTIF | Approving discounts by email at night |
| Estimator / applications engineer | Feasibility, configuration, costing | Specs, drawings, BOM, cost sheets | Re-reading PDFs; costing small jobs by hand |
| Order desk / customer service | Order entry, status calls, changes | ERP order screens, inbox | Answering "where's my order?"; re-keying quotes |
| Dealer / distributor principal | Sells, installs, claims warranty | Orders, claims, programmes, rebates | Calling the manufacturer for every status |
| Warranty administrator | Checks entitlement, approves, pays, recovers | Claims queue, serial history | Chasing missing photos and serials |
| Service manager / field technician | Dispatch, repair, maintenance | Job list, asset history, parts | Repeat visits; paperwork after the job |
| Quality manager / QA | Complaints, NCRs, CAPAs, audits | Complaint register, CAPA list, audit findings | Building audit evidence by hand; chasing CAPA owners |
| Regulatory affairs (TGA/food) | Reportability, recalls, licence conditions | Statutory clocks, recall status | Deciding reportability from incomplete facts |
| Key account manager (incl. contract mfg) | Account plans, forecasts, client reviews | Volumes vs contract, issues, forecast | Building forecasts in spreadsheets; status emails |

**Terminology map** (neutral → manufacturing terms; use the customer's own word once known):
customer → account / customer / **dealer / distributor / channel partner** / **brand owner / sponsor** (contract
manufacturing; "sponsor" is the TGA term for the party responsible for the product in Australia) ·
enquiry → **RFQ / tender / spec** · quote → **quotation / configured quote / price build-up / costing** ·
order → **sales order (SO)**; the customer's document is the **PO** · product → **SKU / part / material (SAP) / item** ·
price → **price list / conditions (SAP) / rebate / special pricing agreement** ·
case → **complaint / product quality complaint / NCR / deviation / service job / RMA / warranty claim** ·
corrective action → **CAPA** · batch → **batch / lot / serial** · customer status → **order acknowledgement / ATP / OTIF**.

**Words to avoid:** "CRM" (Pact had one; lead with the use case) · "replace SAP/your ERP" · "single source of truth"
(the ERP is the master for product, price and orders) · "GMP-compliant / validated system" (the customer validates;
we support) · "Industry 4.0 / digital twin / MES" (not our space; invites the wrong comparison) · Core's list also applies.

## 6. Regulation and compliance hooks (manufacturing additions to Core §6)
*Orientation only; check the current text before citing to a customer. Dates = when the source was published/updated.*

| Obligation / theme | What it means for the process | Demo hook (rule, audit, SLA) | Source |
|---|---|---|---|
| **TGA GMP: PIC/S Guide (PE009) as Manufacturing Principles** (AU, therapeutic goods). Annexes 4, 5, 14 excluded; Annex 11 applies. PE009-16 adopted; PE009-17 consulted on (2025). Complaints & recalls: Part I Ch 8; outsourcing: Ch 7 (written contract giver/acceptor) | Contract manufacturers need written complaint handling, recall readiness, and clear split of duties with the sponsor/brand owner. Computerised systems holding GMP records must be validated | Complaint record with batch link, owner, due date and audit trail; "contract giver" field driving who must be told; confirm-then-act on every status change | TGA PE009; Federal Register explanatory statement F2025L00990, Aug 2025 [13]. **Medium-High**: confirm current PE009 version |
| **TGA recalls: PRAC** (replaced URPTG, 5 Mar 2025) | The Australian **sponsor** runs and reports recalls; it needs a risk analysis from the **manufacturer**. Interim report 6 weeks, close-out 12 weeks | Recall task with 6- and 12-week SLA timers; manufacturer risk-analysis request generated from the complaint | TGA news page + KWM, 2025 [14]. **Medium-High** (read via summary) |
| **ACCC recall notification** (AU, consumer goods) | Notify the ACCC within **2 days** of taking recall action | 2-day SLA timer from "recall decided"; notification task with owner | productsafety.gov.au; HWL Ebsworth, 2026 [15][16]. **Medium-High** |
| **ACCC mandatory reporting** (AU, consumer goods) | Report within **2 days** of becoming aware of a death, serious injury or illness associated with a product; no need to verify first. Guidance updated Jul 2026 | Complaint intake flags "injury/illness mentioned" → 2-day timer → regulatory affairs approves the report (agent never files) | HWL Ebsworth, Jul 2026 [16]. **Medium-High** |
| **Australian Consumer Law: consumer guarantees, warranties against defects, manufacturer indemnity (s274, s276)** | Retailers/dealers who remedy a failure can recover from the manufacturer (can't be contracted out; 3-year limit). Warranty documents need prescribed mandatory text | Dealer claim captures consumer-guarantee vs voluntary warranty; s274 indemnity claims tracked separately; warranty-text template | HWL Ebsworth; JWS, 2024 [17]. **Medium-High**: read the ACL text before quoting |
| **Food recall: FSANZ Standard 3.2.2 cl 12** (AU/NZ) | Manufacturers, wholesalers and importers need a **written recall system** and must follow it; annual review + mock recall recommended | Recall plan as a process; mock-recall run with timestamps and evidence pack | FSANZ, 2023–26 [18]. **Medium-High**; check protocol edition |
| AU mandatory climate disclosure (AASB S2): Group 2 from FY starting 1 Jul 2026; Group 3 from 1 Jul 2027 | Large customers will ask suppliers for emissions data | Low relevance; at most a "supplier data request" task. **Don't lead with it** | CA ANZ, Aug 2026; KPMG [19]. **High** for dates |
| **Indonesia: BPOM** food recall regulation (Jul 2025); CPOB (drug GMP) covers complaints & recalls | Documented recall procedure + batch/lot traceability; report recalls to BPOM | Same complaint→recall flow, Bahasa labels; BPOM report task | Tilleke & Gibbins, 2025 [20]. **Medium** |
| **Indonesia: TKDN local content** (MOI Reg 35/2025, from ~Dec 2025; certification 10 working days) | Tenders (esp. government/SOE) need TKDN certificates per product | Quote checks the product's TKDN % and certificate expiry before a tender quote goes out | ABNR; SSEK, 2025–26 [21]. **Medium**; thresholds are sector-specific |
| **Malaysia: NPRA** product quality reporting and recall guideline (DRGD App. 34); NPRA GMP inspections | Same complaint→recall pattern for registered products | Recall/report tasks with NPRA fields | NPRA [22]. **Medium-High** (not read in full) |
| Malaysia NSRF (IFRS S1/S2): large Main Market issuers from FY 2025 | Supplier ESG data requests | Low relevance | IFRS Foundation profile, Jun 2025 [23] |
| **Singapore**: SGX climate reporting (Scope 1–2 from FY 2025; wider rollout deferred, tiered, Aug 2025). HSA in ASEAN GMP MRA | Supplier data requests; GMP mutual recognition | Low relevance | Linklaters; Rajah & Tann, 2025 [24] |
| **Vietnam: EPR, Decree 05/2025/ND-CP** (amends 08/2022) | Producers/importers recycle at mandatory rates or pay the environment fund | Low relevance (reporting, not customer process). **Later decrees 48/2026, 110/2026 not verified. Vietnam recall rules: unsure; don't state** | Tilleke; KPMG Vietnam, 2025 [25] |
| NZ climate disclosure (XRB standards, Dec 2022) | Large listed issuers etc. | Low relevance. **2025–26 changes not verified** | IAS Plus, 2022 [26] |
| ASEAN GMP (traditional medicines/health supplements) Ch 9 | Written complaint procedure incl. considering a recall | Same MJ3 flow for ASEAN health-supplement makers | ASEAN, 2021 [27] |

## 7. Typical landscape and competitors

### The coexistence story (lead with this; D5)
**One sentence for the CIO:** "Your ERP stays the system of record, your CRM and AI agents stay; Creatio runs one process
around them, end to end, and writes back what each system needs."

| Data / action | Master system (stays) | What Creatio does |
|---|---|---|
| Customer/account master | ERP (sold-to/ship-to) and/or incumbent CRM (e.g. Dynamics at Pact) | Reads; never creates a competing master. New accounts go back to the master |
| Products, BOM, price conditions, stock, serials, batches | ERP | Reads via API for quotes, entitlement checks, batch lookup |
| Sales orders, credit notes, invoices, payments | ERP | Creates the order/credit **in the ERP** via API at the hand-off step (MJ1 step 7, MJ2 step 5–6), or raises a task for the order desk where no API exists |
| Batch release, deviations under GMP | Validated QMS / ERP QM | Hands over (MJ3 step 5); holds intake, communication, tasks and deadlines |
| The *process* itself (quote approval, claim, complaint, dealer request) | **Creatio** | Owns status, rules, SLAs, approvals, portal, audit trail and AI tasks |
| Existing AI agents (Copilot, others) | Customer's AI platform | Creatio's process actions can be called as tools by other agents, and Creatio agents act inside the process with confirm-then-act. **A (Assumed): confirm the exact interop (e.g. MCP) with Creatio product before saying it** |

**Rules:** no ERP customisation required for the first use case (A, confirm per deal); integration through the ERP's
standard APIs or the customer's middleware. **Don't claim a certified SAP connector** unless one is confirmed on the
Creatio Marketplace for that deal (not verified in this pass).

| System type | Common products in APAC | Stays or goes? | Integration story (D5) |
|---|---|---|---|
| ERP (enterprise) | SAP (S/4HANA, ECC), Oracle, Microsoft Dynamics 365 F&O. SAP is the most common ERP in **global** manufacturing case studies [28] | **Stays** | System of record (table above); Creatio reads master data, writes orders/credits |
| ERP (mid-market, AU/NZ) | Dynamics 365 Business Central, Epicor, Pronto Xi, MYOB Advanced/Acumatica, NetSuite, SAP Business One, SYSPRO, Infor [29] | **Stays** | Same pattern; check API maturity early (Pronto/older on-prem may need middleware) **A** |
| Incumbent CRM | Dynamics 365 Sales (Pact), Salesforce, in-house | **Stays** (overrides Core) | Creatio reads accounts/contacts; the use case doesn't duplicate pipeline |
| QMS / LIMS (regulated) | Specialist QMS, ERP QM modules, paper | **Stays** for GMP records | Creatio = intake + customer comms + tasks; handover at NCR/CAPA |
| Field service | ERP service module, specialist FSM, spreadsheets | Often goes for the scoped use case; stays if mature | Job history to Creatio; jobs back to ERP for billing |
| Dealer / B2B ordering portal | ERP web shop, none | Often **none** → Creatio portal | Portal reads ERP order/stock status; doesn't take orders unless agreed |
| Productivity / AI | Microsoft 365, Teams, Copilot | Stays | Email, calendar, Teams; see AI row above |

**ERP share data is weak** (case-study corpus, web-tech detection). Say "most manufacturers we meet run SAP, Dynamics
or a local mid-market ERP", never a market-share number.

### Competitors (counters from the differentiator catalogue only)
| Competitor | Their angle | Our counter (catalogue only) |
|---|---|---|
| Salesforce Manufacturing Cloud + Agentforce | Industry cloud for manufacturers: sales agreements, account forecasts, rebates, partner/dealer sites, manufacturing agent templates incl. warranty [30] | **D2**: industry clouds, Agentforce and Data Cloud are separate add-ons · **D7**: like-for-like 3-year cost incl. Agentforce pricing as listed (Flex Credits USD 500 per 100k; USD 2 per conversation; per-user add-ons from USD 125/user/month); Creatio meters AI too · **D3**: "agentic" is table stakes; our difference is *how* (no-code, confirm-then-act, visible audit trail). Never "they can't" |
| Microsoft (Dynamics 365 Sales/Field Service, Power Platform, Copilot Studio) | "You already run Dynamics / M365" (Pact) | **D5**: we work *alongside* their Dynamics and M365; lead with their systems staying · **D2**: Dynamics app + Power Apps + Copilot Studio credits + M365 Copilot licensed separately · **D7**: Copilot Studio USD 200 per 25k-credit pack/month or PAYG, on top of other licences · **D1** |
| SAP (Sales/Service Cloud, SAP CX) | "Stay in SAP" | **No SAP facts in the catalogue → don't argue.** **D5**: SAP stays the system of record; Creatio runs the process around it · **D1**: business-led change shown live · D6 time to the first use case |
| ServiceNow (Field Service, AI agents) | Enterprise workflow; CIO-owned platform | Core counter: **D1** business-led change; **D7** cost at mid-market scale |
| Oracle (CX, Field Service) | Suite fit with Oracle ERP | **No Oracle facts in the catalogue → don't argue.** **D5**, **D1** |
| Specialist QMS / warranty / CPQ point tools | Depth in one function | **Don't fight the validated QMS** (it stays). **D2**: the customer-facing process across sales, service, quality and portal on one model · **D1** |

Proof we *can* use: Creatio named a **Leader** in IDC MarketScape: Worldwide B2B CRM Platform Software for Industrial
Manufacturing **2024** (Jun 2024, 12 vendors) [31] (vendor announcement of an analyst report; attribute it). Global
references from the catalogue (Howdens 12 weeks, BSN Sports). **No public AU/ASEAN manufacturing reference** (catalogue §4).

## 8. Demo modules and proof moments (design only; nothing built before process sign-off)
**Honest baseline: the team has no manufacturing demo assets today.** "Partly" means a Core asset pattern can be reused,
not a manufacturing scene. Sizes: S ≈ 1–2 days, M ≈ 3–5 days, L ≈ 1.5–2+ weeks (our estimate, AI-assisted build).

| Module | Journeys / tasks covered | Core-set proof moments in it (D1, D3, D2/D5) | Exists today? (portfolio asset) | Build size |
|---|---|---|---|---|
| **MM1 "Their ERP + CRM" stand-in** | Coexistence picture; simulated SAP/Dynamics: account, product/serial/batch, order status, order/credit write-back | **D5** (record arrives from "SAP", order goes back); D2 | Partly: Core M7 pattern (Scentia simulated Salesforce sync). No ERP-shaped data | **M** (S once Core M7 exists) |
| **MM2 Warranty + dealer portal** | MJ2 steps 1–7; dealer portal (claim, status); MAI-T1, T4, T7 | **D3** claim triage + confirm-then-act; **D1** add a claim field/rule live; D2 dealer → claim → recovery on one record; D5 entitlement from "SAP" | No. Reusable: Pertamina ticketing/SLA (Core M4), Scentia portals (Core M3) | **L** |
| **MM3 Complaint → reportability → CAPA** (GMP/food flavour) | MJ3 steps 1–7; MAI-T2, T6; ACCC 2-day and TGA 6/12-week timers | **D3** complaint classified, reportability *flagged*, QA confirms; **D1/D4** change a severity rule live; D5 batch lookup in "SAP", handover to QMS | No. Reusable: Core M4 (case + SLA) | **M** |
| **MM4 Configured quote → ERP order** | MJ1; MAI-T3 (RFQ PDF → draft quote); approval matrix | **D4** margin threshold as data (Scentia `labPackRule` pattern); **D3** draft quote from an RFQ; D5 SO created in "SAP" | No (Core M2 isn't built either). **Don't build a real product configurator**: rule-table pricing for 1 product family | **M–L** |
| **MM5 Manufacturing AI scenes** | MAI-T1–T8 | **D3** | Partly: Core M5 (Sovico AI skill, Pertamina AI log, AI Studio agents) | **M** on top of MM2–MM4 |
| **MM6 Live-change kit (manufacturing)** (entries LC-MM in [M6](../M6-LIVE-CHANGE-KIT-v0.1.md)) | Warranty period by product, dealer tier, CAPA due days, reportability keywords | **D1**, **D4** | Partly: Core M6 pattern | **S** once MM2/MM3 exist |
| **MM7 Outcome dashboard** | Claim ageing, CAPA overdue, quote turnaround, dealer requests | D2 | Partly: Core M1 | **S** |

**Build order recommendation:** MM1 + MM3 first (matches the live Pact interest: one regulated use case + coexistence),
then MM2 (broadest manufacturing appeal), then MM4. Don't build all before a second manufacturing deal confirms the
journeys.

## 9. AI use-case library (manufacturing)
Patterns as in Core §9. **Governance (AI-GOVERNANCE-PACK-LITE):** agents never make GMP, batch-release,
reportability, recall or payment decisions; they prepare and flag, a named person confirms. Confirm-then-act and the
audit log are **designed into our process** (governance #7, #8), not platform guarantees. Don't say "AI data never
leaves Australia".

| ID | Task | Agent alone | Human approves | Data / systems touched | Value maths | Proof moment | Agent pattern |
|---|---|---|---|---|---|---|---|
| MAI-T1 | **Warranty claim triage + entitlement check** | Reads the claim (email/PDF/photos); checks serial, purchase date, coverage in "ERP"; spots duplicates; lists missing items; drafts the dealer request; proposes approve/reject/inspect | Approve/reject; any payment | Claim, dealer, ERP serial/sales history, warranty rules | Claims/month × minutes saved × cost/hour; days to dealer payment; leakage from duplicates | Dealer email arrives → claim created, entitlement checked, missing photo requested; administrator approves in one click; audit trail shown | Document check (Core AI-T1) + intake & triage (AI-T2) |
| MAI-T2 | **Complaint intake + reportability flag** | Classifies complaint; extracts product, batch/lot; looks up batch in "ERP"; flags injury/illness words → starts ACCC 2-day timer; suggests severity | Reportability decision; regulator report; recall decision | Complaint, ERP batch, rules (keywords, severity matrix) | Hours to classify; % statutory clocks met | "Customer reports a rash" → flagged as possibly reportable, 2-day timer running, QA lead asked to decide | Intake & triage + monitor & alert (Core AI-T8) |
| MAI-T3 | **RFQ to draft quote** | Reads RFQ/spec PDF; maps to product options; builds a draft quote from price rules; flags non-standard items for engineering | Price/margin approval; send | RFQ, product rules, ERP prices | Quote turnaround; estimator hours | PDF spec dropped in → draft quote with 2 flagged items; manager approves the margin exception | Prepare-and-confirm (Core AI-T5) |
| MAI-T4 | **Dealer / client status agent** (portal, email, chat) | Answers "where's my order/claim/batch?" from Creatio + ERP; acts within policy (e.g. resend docs) | Anything outside policy; hand-off with summary | Portal user, ERP order status, claim/complaint records | Status calls × cost per contact | Dealer asks in the portal → agent answers with live "SAP" status; out-of-policy request handed to a person with a summary | Customer self-service (Core AI-T3) |
| MAI-T5 | **Pre-visit technician briefing** | Summarises asset history, open claims, likely fault and parts from past jobs | n/a (read-only) | Asset/serial, service history, parts list | First-time fix; repeat visits | "Brief me for this job" → one-page briefing incl. suggested parts | Internal copilot on records (Core AI-T6) |
| MAI-T6 | **NCR / CAPA investigation assistant** | Finds similar past complaints/NCRs; drafts problem statement and 5-why; proposes CAPA owner and due date; chases overdue owners | Root cause, CAPA approval, closure | Complaints, NCRs, CAPAs | CAPA cycle time; % overdue | Complaint → 3 similar past NCRs found; draft CAPA; QA manager edits and approves | Prepare-and-confirm + monitor & alert |
| MAI-T7 | **Supplier recovery claim pack** | Groups approved claims by failed component and supplier; drafts the supplier claim with evidence | Send to supplier | Claims, parts, supplier records | % warranty cost recovered (× warranty spend, ≈1.3% of sales in US data [3]) | Month-end: agent proposes 4 supplier claims worth $X; warranty manager approves and sends | Prepare-and-confirm |
| MAI-T8 | **Key-account briefing with ERP data** | Combines Creatio activity, open claims/complaints and ERP volumes vs contract/forecast | n/a | CRM/Creatio, ERP sales history | Prep time per review | "Brief me on this account" → volumes vs forecast, open issues, risks | Internal copilot on records |

## 10. Harvest log
| Date | Deal | What we learned | Changed in pack |
|---|---|---|---|
| 3 Nov 2026 | **Pact Group** (AU; packaging + contract manufacturing incl. TGA-licensed health & wellness [32]) | **Differentiators ≠ CRM features.** CRM was out of scope (Microsoft Dynamics stays); the CIO wanted **one use case** (possibly TGA compliance in contract manufacturing) **plus a coexistence architecture** with SAP, Microsoft and their existing AI agents. A CRM-feature pitch would have failed | Overlay leads with use case + D5 (§0 note); M-H13 (✔), M-H12; MJ3 + MM3 prioritised; §7 coexistence story; Core §7 "replace at renewal" overridden. Landscape detail is from our deal notes, not public sources |
| 3 Nov 2026 | Research pass | IDC MarketScape industrial-manufacturing CRM recognition is **2024** (the catalogue research had "year not shown"). No AU/ASEAN manufacturing reference found. Process KPIs (warranty cost per claim, CAPA, OTIF, portal adoption) only have weak vendor data | §7 proof line; §4 quality flags; gaps listed in the research file |

---

## Footnotes
[1] Ai Group, *Manufacturing in Australia 2026: Performance and Outlook*, Oct 2026. https://www.australianindustrygroup.com.au/resourcecentre/research-economics/manufacturing-in-australia-2026/
[2] Trading Economics, Ai Group industry index – manufacturing, 2026. https://tradingeconomics.com/australia/industry-index-manufacturing
[3] Warranty Week (2025 claims and accrual rates, US manufacturers). https://www.warrantyweek.com/ ; https://www.warrantyweek.com/statistics
[4] Aberdeen Group, "Fixing First-Time Fix" (2013), via https://www.asentria.com/wordpress/wp-content/uploads/2019/09/aberdeen-group-report-repairing-field-efficiency.pdf and https://fsd.servicemax.com/university/first-time-fix-rate-field-service-metrics-that-matter/
[5] Haug, Hvam & Mortensen, "Impact of product configurators on lead times in engineering-oriented companies", *AI EDAM*. https://www.cambridge.org/core/journals/ai-edam/article/impact-of-product-configurators-on-lead-times-in-engineeringoriented-companies/107D0DB206626EE028613F59CB0DF203
[6] Tech-Clarity, ETO best practices. https://tech-clarity.com/documents/Tech-Clarity-Perspective-ETO-Best-Practices-Summary.pdf
[7] AssurX, 8 CAPA KPIs, 2022. https://assurx.com/8-capa-kpis-you-should-be-measuring-now
[8] McKinsey, "Defining on-time, in-full in the consumer sector". https://www.mckinsey.com/capabilities/operations/our-insights/defining-on-time-in-full-in-the-consumer-sector
[9] DHL, OTIF glossary. https://lot.dhl.com/glossary/on-time-in-full-otif/
[10] Spryker, self-service portals study. https://spryker.com/press-releases/self-service-portals-study
[11] Industrial Distribution. https://www.inddist.com/operations/blog/13764355/distributors-claim-theyre-easy-to-do-business-with-but-lack-tools-to-prove-it
[12] Vendor warranty-cost blogs: https://www.claimlane.com/resources/blog/cost-per-warranty-claim ; https://bruviti.com/blogs/warranty-claims-automation-ai
[13] TGA, PIC/S Guide to GMP PE009: https://www.tga.gov.au/sites/default/files/pe009-pics-guide-gmp-medicinal-products.pdf ; explanatory statement F2025L00990 (Aug 2025): https://www.legislation.gov.au/F2025L00990/asmade/2025-08-28/es/original/word ; TGA fine: https://www.tga.gov.au/news/media-releases/australian-manufacturer-fined-almost-160000-allegedly-breaching-conditions-its-medicines-manufacturing-licence
[14] TGA, recall reforms and PRAC: https://www.tga.gov.au/news/news-articles/recall-reforms-update-and-new-procedure ; KWM: https://www.mallesons.com/au/en/insights/latest-thinking/navigating-the-new-procedure-for-recalls-product-alerts-and-product-corrections.html
[15] ACCC Product Safety, tell the ACCC of the recall. https://www.productsafety.gov.au/business/recall-an-unsafe-product/tell-the-accc-of-the-recall
[16] HWL Ebsworth, ACCC updated mandatory reporting guidelines (2026). https://hwlebsworth.com.au/accc-publishes-updated-mandatory-reporting-guidelines-what-businesses-need-to-know/
[17] HWL Ebsworth, ACL suppliers and manufacturers: https://hwlebsworth.com.au/the-australian-consumer-law-suppliers-and-manufacturers-who-is-ultimately-liable-to-consumers-for-defective-goods/ ; JWS (2024): https://jws.com.au/what-we-think/enforcement-actions-for-consumer-guarantee-failures-and-supplier-indemnities/
[18] FSANZ, food recalls: https://www.foodstandards.gov.au/food-recalls/faqbusiness ; https://www.foodstandards.gov.au/business/food-recalls
[19] CA ANZ (Aug 2026): https://www.charteredaccountantsanz.com/news-and-analysis/insights/research-and-insights/navigating-climate-related-financial-disclosures-a-pathway-for-group-2-and-group-3-entities ; KPMG: https://assets.kpmg.com/content/dam/kpmg/au/pdf/2024/australian-sustainability-reporting-legislation-standards-guide.pdf
[20] Tilleke & Gibbins, food recall regulations in Indonesia, Thailand and Vietnam. https://www.tilleke.com/insights/food-recall-regulations-in-indonesia-thailand-and-vietnam
[21] ABNR, MOI Reg 35/2025: https://www.abnrlaw.com/news/new-local-content-rules-key-changes-under-moi-regulation-no-35-of-2025 ; SSEK: https://ssek.com/blog/revamping-indonesias-tkdn-rules-what-moi-reg-35-2025-means-for-industry/
[22] NPRA, DRGD Appendix 34. https://npra.gov.my/easyarticles/images/users/1153/drgd_appendices/APPENDIX-34-Guideline-for-Product-Quality-Reporting-and-Recall-Procedures.pdf
[23] IFRS Foundation, Malaysia jurisdiction profile (Jun 2025). https://www.ifrs.org/content/dam/ifrs/publications/sustainability-jurisdictions/pdf-profiles/malaysia-ifrs-profile.pdf
[24] Linklaters: https://sustainablefutures.linklaters.com/post/102l487/singapore-extended-timelines-for-most-climate-reporting-requirements-for-listed ; Rajah & Tann: https://sg.rajahtannasia.com/viewpoints/mandatory-climate-reporting-for-listed-issuers-from-fy-2025-and-large-non-listed-companies-to-follow-from-fy-2027/
[25] Tilleke & Gibbins, Decree 05 EPR: https://www.tilleke.com/insights/decree-05-updates-extended-producer-responsibility-regulations-in-vietnam ; KPMG Vietnam: https://kpmg.com/vn/en/insights/2025/02/key-amendments-to-vietnam-environment-protection-regulations.html
[26] IAS Plus, NZ climate standards (Dec 2022). https://www.iasplus.com/en/news/2022/12/nz-climate-standard
[27] ASEAN GMP training, Ch 9 Complaints and Recalls. https://asean.org/wp-content/uploads/2021/01/ASEAN-TMHS-GMP-Training-%E2%80%93-Chapter-9-Complaints-and-Recalls-FD.pdf
[28] ERP Research, ERP market share: https://erpresearch.com/erp-market-share ; wmtips, ERP in Australia: https://www.wmtips.com/technologies/erp/country/au
[29] BusinessHub: https://businesshub.com.au/erp/best-cloud-erp-for-australian-mid-sized-manufacturers ; Pronto: https://www.pronto.net/pronto-xi-epicor-alternative/ ; SYSPRO survey: https://www.australianmanufacturing.com.au/manufacturers-eye-smart-tech-adoption-amid-ongoing-labour-and-integration-hurdles-syspro-finds/
[30] Salesforce AU, manufacturing AI: https://www.salesforce.com/au/manufacturing/artificial-intelligence/ ; partner channel: https://www.salesforce.com/au/manufacturing/partner-channel-engagement-software/ (anticipate their pitch only; not a counter source)
[31] Creatio, IDC MarketScape industrial manufacturing CRM 2024. https://www.creatio.com/company/news/23238
[32] Pact Group, health & wellness contract manufacturing: https://pactgroup.com/products-services/contract-manufacturing/health-and-wellness/
[33] APQC, cost to process warranty claims per claim (paywalled). https://www.apqc.org/resources/benchmarking/open-standards-benchmarking/measures/total-cost-perform-process-process-18
