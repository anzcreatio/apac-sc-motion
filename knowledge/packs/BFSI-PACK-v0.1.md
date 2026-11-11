# BFSI pack v0.1 (overlay on Core)

## 0. Pack header
| Field | Value |
|---|---|
| Pack | **BFSI**: overlay. Lists only what differs from or adds to [CORE-PACK-v0.2.md](CORE-PACK-v0.2.md); everything else is inherited |
| Inherits from | Core v0.1 |
| Owner (SC) | (to assign) |
| Version / date | v0.1 · 3 Nov 2026 |
| Segments covered | **Banking + lending first:** retail and business banking; home, personal and SME lending; the broker channel; customer-owned banks and credit unions; contact centre; complaints and hardship. **Wealth:** short note only (B-W rows in §2, B-M8, AI-B9). **Insurance: later** (not in v0.1). Markets: **AU first**, then ID, MY, VN, SG, NZ (regulation in §6; NZ not researched yet) |
| Deals harvested | None real yet. Seeded from **Mock 01 Harbourline** (fictional bank, lending) and **W1 test 01 Great Southern Bank** (real bank, public research, no call). Research: `bfsi-pack-research-2026-11-03.md` (design workspace `research/`, not in the plugin) |

> **Status: draft.** Anything without a footnote is **A (Assumed)** until a deal confirms it. Footnote numbers match the
> research file's source list. **Mock results are logged as "mock", never as hits:** a fictional call can't confirm a
> hypothesis.
>
> **Inherited from Core without change:** C-H07, C-H08, C-H11, C-H12, C-H13, C-H14; journey J3 (as the base of J-B3);
> AI-T2, AI-T4, AI-T6, AI-T7, AI-T8; modules M1, M6, M7. **Overridden here:** C-H04 → B-H07; C-H09 → B-H10;
> C-H10 → B-H14; J2 → J-B2; AI-T1 → AI-B1/AI-B6; AI-T3 → AI-B8.

---

## 1. Top pains and consequences
Adds to Core CP1–CP10. CP5, CP6, CP9 and CP10 apply in BFSI as written.

| ID | Pain | Consequence | Typical owner | Journey |
|---|---|---|---|---|
| BP1 | Slow time to decision on home loans | Brokers place deals elsewhere; broker channel share falls. Brokers write **81.6%** of new AU home loans (Jun 2026 qtr)[^24], so broker speed is distribution | Head of Lending / Broker Distribution | J-B1 |
| BP2 | Applications arrive incomplete; documents checked by hand | Expensive assessors doing admin; 2–3 rounds of follow-up (mock); slower decisions | Head of Lending Operations | J-B1 |
| BP3 | Brokers chase status by phone | Lending support load; broker frustration | Broker Distribution / Lending Ops | J-B1 |
| BP4 | Onboarding and KYC stall on identity, beneficial-owner and source-of-funds evidence | Lost accounts; slow SME onboarding; AML/CTF exposure | Head of Operations / Financial Crime | J-B2 |
| BP5 | Reformed AML/CTF due diligence must reach existing customers | Large re-check workload before the transition ends (30 Mar 2029, per one source)[^10] | MLRO / Financial Crime | J-B2 |
| BP6 | Hardship notices missed or answered late | Breach of the 21-day rule; enforcement (ASIC v NAB: 345 late responses alleged)[^7]; harm to vulnerable customers | Head of Financial Assistance / Collections | J-B3 |
| BP7 | Complaint deadlines tracked by hand | IDR timeframes breached (30 days; 21 for hardship/default-notice complaints)[^2][^3]; AFCA escalations | Customer Advocate / Complaints | J-B3 |
| BP8 | Scam cases bounce between contact centre and fraud teams | Customer loss; SPF obligations from March 2027[^1] | Head of Fraud / Contact Centre | J-B3 |
| BP9 | Business credit papers built by hand | RM time lost to admin; slow SME decisions | Head of Business Banking / Credit | J-B1 (SME variant) |
| BP10 | AI blocked between pilot and production by risk, with regulators now looking | ASIC banking AI review starting Q2 2026–27[^1]; MAS AI guidelines[^17]; CPS 230 service-provider rules[^8] | CRO / CIO | All (AI) |
| BP11 | New products and regulatory changes take months to reach systems | Late launches; manual workarounds for new rules (D1 BFSI example) | COO / Product | All |

## 2. Hypothesis library

| ID | Slide wording (≤12 words) | Track | Usual owner | Journey / task | KPI | D-IDs | Signals that make it likely | Hit / miss |
|---|---|---|---|---|---|---|---|---|
| B-H01 | Brokers send deals to whichever lender decides fastest | P | Head of Lending / Broker Distribution | J-B1 | Days lodgement → conditional approval; broker share at main aggregator | D2, D4, D1 | Majority of home loans via brokers; listed on ApplyOnline / Loanapp; turnaround in annual report or broker press; new COO with turnaround focus | Mock ✔ (Harbourline) |
| B-H02 | Many home loan applications arrive incomplete, triggering rounds of follow-up | P | Head of Lending Operations | J-B1 step 3–4 | % incomplete on arrival; rounds per file | D3, D2 | Broker-heavy book; self-employed lending; manual doc stores | Mock ✔ |
| B-H03 | Credit assessors spend much of each file checking documents | A | Head of Lending Operations | AI-B1 | Minutes per file on documents | D3, D5 | Assessor hiring ads; "verification of income" backlog; LOS without document AI | Mock ✔ |
| B-H04 | Brokers phone the lender to find out where their deal is | P | Broker Distribution | J-B1 / AI-B2 | Broker status calls per week | D2, D3 | Broker support team or BDM hotline; no broker status portal | Mock ✔ |
| B-H05 | Serviceability gets re-done in spreadsheets because staff don't trust the system | P | Credit / Lending Ops | J-B1 step 5 | Duplicate assessment time; errors | D2, D4 | Heavily customised LOS; policy changes outpacing LOS releases | Mock ✔ |
| B-H06 | Loans above delegated limits wait days for a credit committee | P | Chief Credit Officer | J-B1 step 6 | Days waiting for committee; % of files above DLA | D4, D1 | Committee meets weekly / twice weekly; rising average loan size | Mock ✔ |
| B-H07 | Onboarding stalls while staff chase identity and source-of-funds evidence | P | Head of Operations | J-B2 | Days to open; % incomplete; abandonment | D3, D2 | SME / business accounts; non-resident customers; branch-to-digital shift | |
| B-H08 | New AML/CTF rules mean re-checking existing customers, largely by hand | A | MLRO / Financial Crime | J-B2 / AI-B6 | Reviews per analyst per day; backlog vs 30 Mar 2029 | D3, D4 | AUSTRAC reporting entity; legacy customer base; CDD uplift programme[^9][^10] | |
| B-H09 | Hardship requests are missed when customers don't use the right words | A | Head of Financial Assistance | J-B3 / AI-B3 | % hardship identified at first contact; days to response vs 21 | D3, D4 | Rising arrears; REP 782/815 follow-up[^5][^6]; contact centre also serves hardship (GSB) | Mock ✘ (Harbourline: "They're fine") |
| B-H10 | Complaint deadlines are tracked in spreadsheets, not by the system | P | Customer Advocate / Complaints | J-B3 | % responded within 30 / 21 days; AFCA referrals | D4, D2 | AFCA complaint volume; IDR data reporting to ASIC; complaints team outside the CRM | |
| B-H11 | Scam cases stall when passed between service and fraud teams | P | Head of Fraud / Contact Centre | J-B3 / AI-B7 | Time to first action on a scam report; hand-offs | D2, D3 | Bank designated under the SPF[^11]; separate fraud tooling; scam in contact reasons (GSB) | W1 only (GSB H5, untested) |
| B-H12 | Business credit papers take relationship managers days to assemble | A | Head of Business Banking | AI-B5 | Hours per credit paper; SME time to decision | D3, D2 | SME growth strategy; RM capacity complaints; ASIC/APRA SME lending reviews[^1] | |
| B-H13 | Regulators now expect evidence of how AI treats customers | A | CRO / CIO | All AI / B-M10 | Time from AI pilot to approval | D3, D5 | Board AI mandate; ASIC AI review[^1]; MAS AIRM for SG[^17]; OJK AI governance for ID[^18] | |
| B-H14 | A new product or regulatory change takes months to reach systems | P | COO / Product | All | Time to change | D1, D4 | LOS / core vendor change queues; SPF, AML/CTF, CDR deadlines landing in 2026–27 | |
| B-H15 | Contact centre staff can't see a loan's status without asking lending | P | Head of Contact Centre | J-B1 × J3 | Transfers; callbacks on loan status | D2 | Separate lending and service systems; "older CRM plus core screens" (GSB BDR quote) | W1 only (GSB, indirect) |
| B-W01 | Paraplanning work is tracked in email and spreadsheets beside Xplan | P | Head of Advice / Practice Manager | Wealth / B-M8 | Days per advice job; jobs in flight | D5, D2 | Xplan / AdviserLogic in place; paraplanning team or outsourcer | (A) Ord Minnett build |
| B-W02 | Annual client consent renewals are chased by hand across advisers | P | Head of Advice / Compliance | Wealth / B-M8 | % renewals on time | D4, D2 | Ongoing fee clients; multi-adviser practice | (A) |

## 3. Reference journeys

### J-B1 · Home loan origination via broker (replaces J1 for lending deals)
| Step | Neutral term | Customer terms we've heard | Who | Usual system | Typical break |
|---|---|---|---|---|---|
| 1 | Application received | lodgement, deal, submission | Broker (~70% mock) / branch | Broker platform (ApplyOnline, Loanapp)[^31] → LOS | |
| 2 | Allocate | queue, allocation, triage | Team leader / rules | LOS | ⚠ Waits "a day or two" (mock) |
| 3 | Check documents | VOI, doc check, verification, "conditions" | Credit assessor | LOS doc store, email | ⚠ Half incomplete (mock); 30–40 min/file |
| 4 | Request missing information | RFI, "further info", outstanding items | Assessor ↔ broker | Email, broker platform notes | ⚠ 2–3 rounds (mock) |
| 5 | Assess | serviceability, credit assessment, LVR, LMI | Assessor | LOS + spreadsheet | ⚠ Duplicate work in spreadsheets (mock) |
| 6 | Decide | DLA, credit committee, approval | Assessor ≤ DLA; committee above | LOS, committee papers | ⚠ Committee cadence (twice weekly in mock) |
| 7 | Tell the broker | conditional approval, pre-approval | Lending ops | LOS email | ⚠ No status in between → broker calls |
| 8 | Valuation and formal approval | val, unconditional approval, loan docs | Valuer (outsourced) / ops | Valuation panel, LOS | |
| 9 | Settle | settlement, funding | Settlements team | LOS, PEXA (A) | |

SME variant: steps 3–6 add financials, security and a **credit paper** written by the RM (B-H12, AI-B5).

### J-B2 · Customer onboarding and KYC (retail and SME; replaces Core J2 for banks)
| Step | Neutral term | Customer terms we've heard | Who | Usual system | Typical break |
|---|---|---|---|---|---|
| 1 | Application | account opening, join (mutuals), onboarding | Customer / banker / RM | App, web, branch, RM | ⚠ Abandonment mid-form |
| 2 | Verify identity | eKYC, ID&V, DVS, biometrics | System + ops | eKYC vendor (A) | |
| 3 | Screen | sanctions, PEP, adverse media | System + analyst | Screening tool (A) | False positives |
| 4 | Risk-rate and due diligence | CDD, ECDD/EDD, beneficial owners, source of funds | Ops / financial crime | Spreadsheet, case tool | ⚠ SME ownership structures; evidence chasing |
| 5 | Collect missing evidence | outstanding documents | Ops ↔ customer | Email, uploads | ⚠ 2–3 rounds (Core J2) |
| 6 | Approve | sign-off, compliance approval | Team leader / compliance | Email | ⚠ Queue for high-risk files |
| 7 | Open in core | account set-up, provisioning | Ops | Core banking (Temenos, Data Action, Ultracs, BaNCS…)[^32] | ⚠ Re-keying |
| 8 | Ongoing due diligence | periodic review, KYC refresh, trigger events | Financial crime | Case tool, spreadsheet | ⚠ Backlog; AML/CTF 2026 reforms add load[^10] |

### J-B3 · Hardship or complaint case (extends Core J3)
| Step | Neutral term | Customer terms we've heard | Who | Usual system | Typical break |
|---|---|---|---|---|---|
| 1 | Contact | call, chat, email, branch, broker, AFCA referral | Customer / rep | Contact centre platform (e.g. NiCE at GSB)[^35] | |
| 2 | Recognise what it is | hardship notice, "financial difficulty", complaint, dissatisfaction, scam report, vulnerability | Front-line agent | CRM / notes | ⚠ **Not recognised** (customer doesn't use the words) |
| 3 | Log and acknowledge | acknowledgement | Agent / system | CRM | ⚠ Acknowledge within 24 h / 1 business day (IDR)[^3] |
| 4 | Route | hardship team, complaints / IDR, fraud, collections hold | Agent / rules | Email, queues | ⚠ Hand-offs between teams; collections not paused |
| 5 | Gather information | statement of financial position, info request | Specialist ↔ customer | Email, forms | ⚠ Clock: 21 days to respond, 28 if info requested and not provided (hardship)[^4] |
| 6 | Assess and decide | variation, deferral, arrangement, refund, remediation | Specialist / manager | Core, spreadsheet | ⚠ Clock runs out |
| 7 | Respond in writing | IDR response, hardship outcome letter, AFCA rights | Specialist | Word templates | ⚠ Written response required even when closed quickly (hardship)[^3] |
| 8 | Monitor and close | arrangement monitoring, root cause | Team leader | Spreadsheet | Root causes and IDR data not captured |

## 4. KPI benchmarks (BFSI; Core §4 still applies)
**Rule (from Core):** range questions, not claims. Only Strong rows may be quoted, attributed. Regulatory limits are
limits, not benchmarks: never imply a customer is in breach.

| KPI | Journey | Typical range | Range question | Source + date | Quality |
|---|---|---|---|---|---|
| Broker share of new home loans (AU) | J-B1 | **81.6%** (Jun 2026 qtr), up from 73.7% Jun 2024 | "What share of your new lending comes through brokers?" | MFAA / Cotality, 3 Sep 2026[^24] | **Strong** |
| Application → unconditional approval (broker) | J-B1 | ~**17.2 days** average (a record low at the time) | "Closer to 1, 2 or 3 weeks?" | AFG Mortgage Index via The Adviser, year not shown (~2023)[^25] | Medium, old |
| Lender turnaround to initial credit decision | J-B1 | Typically **5–8 business days**; smaller ADIs 5.6 business days (Jun 2024) | "Closer to 3, 5 or 8 business days?" | Broker Pulse (media-owned broker survey), 2024[^25] | Medium |
| Branch vs broker time to approval | J-B1 | **2 days** vs **16 days** (one bank) | "Is broker business slower than direct for you?" | Bank's parliamentary response, ~2021–22[^26] | Weak, old |
| Application → formal approval (consumer view) | J-B1 | **2–6 weeks** | — (context only) | Mozo guide, undated[^27] | Weak |
| Lodgement → conditional approval; minutes per file on documents; rounds | J-B1 | 8–10 days; 30–40 min/file; 2–3 rounds | "Closer to 3, 7 or 10 days?" | Harbourline mock (fictional) | Our estimate |
| Hardship response | J-B3 | Legal max **21 days** (28 if info requested and not provided) | "How many respond well inside 21 days?" | National Credit Code s72 via ASIC FAQ[^4] | **Strong** (law) |
| Home loan hardship volume trend | J-B3 | **+58%** vs prior 18 months | "Have hardship notices grown since 2024?" | ASIC REP 815, 25 Sep 2025[^6] | **Strong** |
| Customers dropping out of hardship process | J-B3 | ~**35%** at least once | "How many hardship cases stall waiting on the customer?" | REP 782 via law-firm summary, 2024[^5] | Medium (verify) |
| IDR response | J-B3 | Max **30 calendar days**; **21 days** hardship/default-notice complaints; acknowledge within **24 h / 1 business day** | "What share closes inside 10, 20, 30 days?" | RG 271 via AFCA and PwC, 2021[^2][^3] | **Strong** (regulatory; RG text not read) |
| AFCA banking complaints (AU) | J-B3 | FY25 **54,581** (−9%); financial difficulty **4,764** | — (context) | AFCA via trade press, 2025[^29] | Medium |
| Bank contact-centre wait (AU) | J3 | Q4 2024: **0:23** (fastest, GSB) to **6:30** (slowest, ING); Westpac **1:12** | "Closer to 1, 3 or 6 minutes at peak?" | ACXPA mystery shop via Banking Day, Feb 2025[^30] | Medium, old |
| Malaysia complaints | J-B3 | Ack **next day**; decide **5 days** simple, **≤20 days** complex (from 1 Apr 2026) | "How many complex complaints close inside 20 days?" | BNM policy document via The Edge[^21] | Strong-ish (regulatory; PD not read) |
| Corporate onboarding / KYC (inherited) | J-B2 | ~95 days | "Weeks or months?" | Fenergo (Core) | Medium |
| **Gaps** | J-B2, J-B1 | AU retail account-opening time; SME time to decision; bank FCR; cost per KYC refresh in APAC: **no credible public source** | Ask open | — | — |

## 5. Personas and terminology
Adds to Core §5.

| Persona | What they do all day | What they look at | What they'd love to stop doing |
|---|---|---|---|
| Head of Lending Operations | Throughput, SLAs, staffing for spring peaks | Time to decision, pipeline by stage, broker complaints | Explaining to the board why turnaround slipped |
| Credit assessor / underwriter | Checks documents, serviceability, decides within DLA | Work queue, LOS, policy | Chasing brokers for payslips; re-doing serviceability in Excel |
| Head of Broker Distribution / BDM | Broker relationships, aggregator panels | Share of aggregator volume, broker NPS | Fielding "where's my deal?" calls |
| Broker (external) | Lodges, chases, updates the client | Lender turnaround, status | Phoning for status; resubmitting documents |
| Business banker / RM | SME clients, credit papers, reviews | Portfolio, pipeline, covenants | Assembling credit papers by hand |
| Hardship / financial assistance officer | Assesses hardship, sets arrangements | Cases with statutory clocks | Missing the 21-day clock; re-asking for information |
| Complaints / IDR manager (Customer Advocate) | Complaints, AFCA cases, IDR reporting | Open complaints by age, AFCA referrals | Building IDR data and letters by hand |
| Financial crime / AML analyst | CDD, EDD, screening, SMR investigations | Alerts, review backlog | Re-collecting documents for periodic reviews |
| CRO / risk committee | Risk appetite, AI approvals, CPS 230 | Incidents, obligations register, AI inventory | Approving AI they can't see into |
| Wealth: adviser / paraplanner | Reviews, advice docs, client meetings | Xplan / AdviserLogic, job list | Re-keying between Xplan and email/spreadsheets |

**Terminology map (BFSI):**
- **customer → member / customer.** Customer-owned banks and credit unions often say **member**, but not all: **GSB says "customers"** (W1 test 01). Rule: **use the word on their website and annual report**; never guess. Harbourline (mock) says "members".
- application → **lodgement / deal** (broker channel) · decision → **conditional / unconditional (formal) approval**, pre-approval · approval limit → **DLA** (delegated lending authority) · affordability → **serviceability** · document check → **VOI** (verification of income), "conditions", "outstanding items" · request for information → **RFI**.
- onboarding → **account opening / join** (mutuals) · checks → **KYC, CDD, ECDD, PEP, sanctions**, beneficial owners.
- complaint → **IDR complaint**, "expression of dissatisfaction", **AFCA** case · hardship → **financial hardship / financial difficulty / financial assistance** (pick their word).
- Indonesia: **nasabah** = customer · Malaysia: Islamic banks say **financing**, not "loan" (A). Use the customer's English terms in AU/NZ/SG.

**Words to avoid (BFSI, on top of Core):** "CRM" (Harbourline: "people roll their eyes"), "replace your LOS / core", "AI approves loans" / "automated credit decisions", "chatbot" for hardship or scams, "fully compliant" / "guarantees compliance", "reduce headcount", "data never leaves Australia" (governance pack: not yet).

## 6. Regulation and compliance hooks
*For orientation, not legal advice. Verify against the primary text before quoting to a customer. Footnotes give date and
source; "A" = not researched this pass.*

| Obligation / theme | What it means for the process | Demo hook (rule, audit, SLA) | Source |
|---|---|---|---|
| **AU · ASIC banking AI review** (starts Q2 2026–27, i.e. now) | New and proposed AI uses and their customer impact; "customer-facing interactions, decision-making and lending processes"; with APRA | AI inventory record per agent; confirm-then-act; AI action log (B-M10) | ASIC letter, 30 Sep 2026[^1] |
| **AU · ASIC lender conduct and broker oversight review** (Q3 2026–27) | Lender oversight of brokers and referrers; follows mortgage-fraud work with APRA/AUSTRAC | Broker record: accreditation, quality flags, document discrepancies per broker | ASIC letter[^1] |
| **AU · Hardship (National Credit Code s72, s89A)** | Respond within **21 days**; info request → 28 days if not provided; no enforcement while unanswered | Hardship case with statutory clock; info request resets clock; **collections hold** flag | ASIC FAQ[^4]; REP 782/815[^5][^6]; ASIC letter[^1] |
| **AU · IDR (ASIC RG 271)** | Ack 24 h / 1 business day; respond ≤30 days; ≤21 days for hardship/default-notice complaints; written response with AFCA rights | SLA clock by complaint type; IDR letter template; IDR data export | AFCA[^2]; PwC[^3] (RG text not read) |
| **AU · APRA CPS 230** (in force 1 Jul 2025) | Critical operations, tolerance levels, **material service providers** incl. nth parties; contracts updated by renewal or 1 Jul 2026 | Tolerance timers on a critical operation (e.g. hardship); **sales note:** expect MSP due diligence on Creatio and its AI provider | APRA[^8] |
| **AU · AML/CTF Amendment Act 2024** | Reformed CDD from **31 Mar 2026** (AML/CTF Rules 2025); existing customers to new standard by **30 Mar 2029** (one source); tranche 2 from 1 Jul 2026 | CDD checklist as data (D4); periodic-review queue; EDD tasks; AI never tips off or decides an SMR | Home Affairs[^9]; Bright Law[^10] |
| **AU · Scams Prevention Framework** | Banks designated (May 2026); sector codes in draft; commencement **March 2027** | Scam report case: capture, cross-team routing, evidence trail, customer updates | Treasury[^11]; HSF Kramer[^12]; ASIC[^1] |
| **AU · Consumer Data Right** | Non-bank lenders: product data 13 Jul 2026; consumer data from **9 Nov 2026** (largest first). Action initiation is law; no action type declared yet | CDR-sourced transaction data as income evidence in AI-B1 (simulated) | KWM / The Adviser[^13]; Ashurst[^14] |
| AU · Responsible lending, Banking Code / Customer Owned Banking Code, CPS 234, Privacy Act | **A: not researched this pass** | Evidence checklist + audit on assessment; vulnerability flags | — |
| **SG · MAS Guidelines on AI Risk Management** (issued 7 Oct 2026; effective 7 Oct 2027) | AI inventory; materiality per use case; human oversight, testing, monitoring; third-party AI tested on the FI's own data; covers agents | Same B-M10 view; test set per agent | Allen & Gledhill[^17]; MAS consultation[^16] |
| **ID · OJK AI Governance for Indonesian Banking** (29 Apr 2025) | Guideline, minimum benchmark, checked in supervision | B-M10 | OJK[^18] |
| **ID · PDP Law 27/2022** | In force (transition ended Oct 2024); PP 33/2026 effective 16 Jan 2027 (one source); agency not yet operational | Consent and access by role (Core); in-country hosting (governance pack #2) | RSM, Sep 2026[^20] |
| **ID · OJK complaints** | SEOJK 20/2025 reporting from 1 Jan 2027. **Current timeframe unsure** (legacy: 20 working days + 20) | Complaint clock as a configurable rule | regalert; Bank Mandiri AR[^19] |
| **MY · BNM complaints handling PD** (effective 1 Apr 2026) | Ack next day; 5 days simple; ≤20 days complex | SLA clock by complexity | BNM / The Edge[^21] |
| **MY · PDPA amendments** (1 Jun 2025) | DPO, breach notification, portability. **72-hour deadline not confirmed** | Breach/incident case | Baker McKenzie[^22] |
| **VN · PDP Law 91/2025 + Decree 356/2025** (1 Jan 2026) | Banking-specific rules; notify within **72 h** of sensitive-data leakage; transaction history and card data are sensitive | Data classification on fields; incident case with 72 h clock | Vietnam Briefing; Tilleke[^23] |
| VN · SBV-specific rules | **Not found; unsure** | — | — |
| NZ · CoFI, CCCFA, Privacy Act 2020 | **A: not researched** | — | — |

## 7. Typical landscape and competitors
Adds to Core §7.

| System type | Common products in APAC | Stays or goes? | Integration story (D5) |
|---|---|---|---|
| Broker lodgement (AU) | **NextGen ApplyOnline** (claims all AU brokers, 60+ lenders), **Simpology Loanapp**[^31] | Stays | Lodgement arrives from the platform → Creatio file; status goes back to the broker |
| Loan origination (LOS) | **nCino** (Judo, RedZed, Rabobank, ASB, Kiwibank, BNZ, P&N commercial, Summerland)[^33]; vendor LOS, often heavily customised (Harbourline mock) | Stays (often until contract renewal) | Creatio works *around* the LOS: queue, documents, AI check, broker status; decision stays in the LOS |
| Core banking (AU) | **Temenos** (Police Bank; Cognizant country model bank), **Data Action** (Queensland Country), **Ultradata Ultracs** (Illawarra CU), **TCS BaNCS** (GSB)[^32] | Stays | Accounts, balances, arrangements via API or a stand-in (B-M9) |
| Core banking (SEA) | **Temenos** (VIB, VPBank, LPBank, MSB), **Oracle FLEXCUBE** (Kien Long)[^34]; ID/MY: not sourced | Stays | As above |
| Contact centre | **NiCE CXone** (GSB, run by Optus)[^35]; Genesys, Amazon Connect (Core) | Stays | Platform routes; Creatio is the service record and the acting agent |
| Data platform | Databricks (GSB, W1 test) | Stays | Governed data for AI; avoid the "build it ourselves" fight (Core) |
| Settlement | PEXA (A) | Stays | Status only |
| Wealth platforms | **Xplan, AdviserLogic** | Stays | Coexistence proven in the Ord Minnett / Profectus sandbox (catalogue D5) |

| Competitor | Their angle | Our counter (catalogue only) |
|---|---|---|
| Salesforce Financial Services Cloud + Agentforce | Industry cloud for banking; agentic CRM | **D2:** industry clouds, Agentforce and Data Cloud are separate add-ons; Creatio packages platform, CRM and AI Studio · **D7:** like-for-like 3-year scenario incl. AI credits (Creatio meters AI too) · **D1:** live change in the meeting |
| Microsoft (Dynamics 365, Copilot Studio) | "We're a Microsoft shop" (Harbourline, GSB) | **D5:** we work with M365 and their named systems · **D2:** Dynamics 365, Power Apps, Copilot Studio credits and M365 Copilot licensed separately · **D1** |
| nCino | Bank operating system / LOS for lending | No catalogue fact on nCino. **D5:** where nCino is the LOS, it stays; we show the process around it. Never argue against it |
| Pega | Case management and decisioning in large banks (A) | No catalogue fact. **D1 + D4:** show a business user change a rule live; never say "they can't" |
| ServiceNow | Agentic contact centre for banking[^35] | **D1:** business-led change · **D7:** cost at mid-market scale · **D3:** our "how" (no-code agents, confirm-then-act, visible audit), never "only us" |
| NiCE (incumbent contact centre AI) | "AI lives in the contact centre" | **D5:** not replacing it; Creatio is the record and the acting agent it hands off to |
| In-house on the data platform | "We'll build our own agents" | **D3:** governed workflow + front-line UI they'd otherwise build, on their data platform (Core) |
| Local SEA players | **None sourced** this pass | — |

**Proof caution:** the catalogue has **no named bank reference in AU, NZ, ID, MY, VN or SG**. Use OTP Bank and Ent
Credit Union and say where they are.

## 8. Demo modules and proof moments (design only; nothing built before process sign-off)
| Module | Journeys / tasks covered | Core-set proof moments in it (D1, D3, D2/D5) | Exists today? (portfolio asset) | Build size |
|---|---|---|---|---|
| **B-M1 Lending turnaround view** | J-B1 time to decision by stage | D2 (Core M1) | Partly (Pertamina, SJOG dashboards) | S |
| **B-M2 Broker file to conditional approval** | J-B1 steps 1–7, AI-B1 | **D3** doc check + assessor approves · **D1/D4** DLA ($1.2m) changed live · **D5** simulated LOS | No (designed in Harbourline W2) | M |
| **B-M3 Broker status** | J-B1 step 7, AI-B2 | D2 | Partly (Scentia portals, GOC) | S |
| **B-M4 Onboarding + CDD** | J-B2, AI-B6 | D4 CDD rule as data · D3 evidence check · D2 | Partly (Core M3: Scentia, GOC enrolment) | M |
| **B-M5 Hardship + complaints workbench** | J-B3, AI-B3, AI-B4 | D4 statutory clocks as data · D3 hardship spotted in a transcript · D2 | Partly (Pertamina SLA/ticketing) | M |
| **B-M6 Service agent with safe hand-off** | AI-B8, AI-B7 | D3 acts, then hands off on hardship/scam flags · D5 NiCE/Genesys stand-in | Partly (AI Studio agents; GSB W1 design) | M |
| **B-M7 Credit paper copilot** | AI-B5 | D3 | No | M |
| **B-M8 Wealth** | Households/holdings, documents lifecycle, paraplanning jobs; Xplan/AdviserLogic coexistence; AI-B9 | D2, D5 | **Yes** (Ord Minnett / Profectus sandbox) | S (harvest) |
| **B-M9 "Their system" stand-ins** | LOS, core banking, broker platform | D5 | Partly (Core M7, Scentia simulated sync) | S |
| **B-M10 AI evidence view** | AI inventory record, approvals, action log per agent | D3 | No (designed around governance pack #7, #8) | S |

## 9. AI use-case library (BFSI)
**Hard lines in every BFSI agent:** no credit decisions, no hardship outcomes, no SMR decisions, nothing that could tip
off a customer about a suspicion; hardship, vulnerability or scam signals always go to a person (C, Harbourline mock;
A elsewhere).

| ID | Task | Agent alone | Human approves | Data / systems touched | Value maths | Proof moment | Agent pattern |
|---|---|---|---|---|---|---|---|
| AI-B1 | **Loan file document check + broker request** (extends AI-T1) | Matches payslips, statements, ID to the application; checks recency; flags discrepancies; lists what's missing; drafts the broker request | Assessor sends the request; all credit decisions | LOS doc store (stand-in), application, broker platform, CDR data (later) | Files/month × (min today − min after). Mock: 900 × (35 − 7.5) ≈ **410 h/month** (our estimate) | Stale statement flagged in seconds; request drafted; assessor approves; audit shown | Document check |
| AI-B2 | **Broker status answer** | Answers "where's my deal?" from the file, by portal or email | Escalations; anything beyond status | Loan file, broker portal | Status calls/week × minutes. "Hundreds a week" (mock) | Broker asks → answered from the live stage | Customer self-service (partner) |
| AI-B3 | **Hardship signal → case** | Spots possible hardship in a call/chat transcript or email; opens a case with the 21-day clock; drafts the info request; suggests a collections hold | Officer confirms it's a hardship notice; all outcomes | Transcript, customer record, collections | Late/missed notices avoided; days to response | "I've lost hours at work" in a chat → case opened, clock running, officer confirms | Intake + triage |
| AI-B4 | **Complaint recognition + IDR response draft** | Flags dissatisfaction as a complaint; sets the clock by type (30/21 days); drafts the IDR response with AFCA details | Specialist decides and sends | Contact records, case, templates | Complaints/month × drafting time (A: 30–60 min) | Email → complaint logged, ack sent, draft letter ready | Prepare-and-confirm |
| AI-B5 | **Business credit paper first draft** | Assembles the paper from the record, financials, conduct, security | RM edits; credit decides | Customer record, financials, core | Papers/month × hours saved (A) | "Draft the credit paper for this client" → structured draft with sources | Internal copilot on records |
| AI-B6 | **CDD evidence check + periodic review prep** | Checks ID and beneficial-owner documents; flags gaps; drafts the request; summarises the file for review | Analyst sets risk rating; any SMR; never messages about suspicion | Customer record, documents, screening results | Existing customers to refresh by 30 Mar 2029 ÷ months × minutes per review | Review queue: agent pre-fills 10 files; analyst signs off | Document check |
| AI-B7 | **Scam report intake + routing** | Captures details; opens the case; routes to fraud; drafts the customer update | Fraud team: recalls, reimbursement, contact | Contact record, transactions (read), fraud queue | Time to first action × reports | Scam report → case + fraud alert in under a minute | Intake + triage |
| AI-B8 | **Routine banking enquiry with safe hand-off** (BFSI override of AI-T3) | Balance, repayment date, card block, statements | Card reissue / repayment change (configurable); **any hardship, vulnerability or scam signal → person with a summary** | Core via API, record, contact centre platform | Containment × cost per contact (Core) | "When's my repayment?" answered; "I can't pay this month" → hand-off with summary | Customer self-service |
| AI-B9 | **Wealth: meeting → file note + paraplanning job** (AI-T4 variant) | Drafts the file note and the paraplanning job from the meeting | Adviser confirms; no advice content generated | Meeting transcript, household record, Xplan (sync) | Minutes per review meeting × meetings | Review ends → note + job in the queue | Internal copilot on records |

## 10. Harvest log
| Date | Deal | What we learned | Changed in pack |
|---|---|---|---|
| 3 Nov 2026 | Mock 01 Harbourline (**fictional**, lending) | Time to decision is the board KPI; documents may be the **cause** of slow decisions; broker share fell 6% → 4.5%; DLA $1.2m + committee twice weekly; serviceability in spreadsheets; LOS API limited; AU data residency "non-negotiable"; CRO risk committee is the AI gate; "CRM" toxic; hardship **not** a pain there (member service team "fine") | B-H01–B-H06 (logged as mock, not hits); B-H09 mock miss; J-B1; AI-B1; B-M2; words to avoid; hard lines in §9 |
| 3 Nov 2026 | W1 test 01 Great Southern Bank (real, **public research, no call**) | Customer-owned but says **"customers"**; NiCE CXone via Optus; TCS BaNCS; Databricks; contact centre also serves hardship and financial crime; public service levels contradict the BDR's pain; ASIC AI review | Terminology rule (member vs customer); B-H11, B-H15; AI-B8 hand-off rule; §7 landscape |
| 3 Nov 2026 | Research pass | ASIC AI review starts Q2 2026–27 and covers decision-making and lending, not only customer-facing AI; SPF March 2027; AML/CTF CDD reform live 31 Mar 2026; MAS AIRM issued 7 Oct 2026 | §6; B-H08, B-H13; B-M10 |

---

[^1]: ASIC, "2026–27 banking sector priorities", letter to bank boards, 30 Sep 2026 (read). https://download.asic.gov.au/media/0tobhg1c/26-232mr-asic-supervisory-letter-banking-published-30-september-2026.pdf
[^2]: AFCA, "New maximum IDR timeframes" (RG 271, effective 5 Oct 2021; page updated 30 Oct 2023; fetch blocked, via search summary). https://afca.org.au/members/rg271/new-maximum-idr-timeframes
[^3]: PwC, "RG 271 internal dispute resolution: key changes required" (2021). https://www.pwc.com.au/industry/financial-services/assets/publications/regulatory-guide271-internal-dispute-resolution-key-changes-required.pdf
[^4]: ASIC, "FAQs: dealing with consumers and credit" (undated; hardship notice 21/28 days). https://www.asic.gov.au/regulatory-resources/credit/credit-notices-and-offences/faqs-dealing-with-consumers-and-credit
[^5]: ASIC REP 782, "Hardship, hard to get help", 20 May 2024. https://asic.gov.au/regulatory-resources/find-a-document/reports/rep-782-hardship-hard-to-get-help-findings-and-actions-to-support-customers-in-financial-hardship/
[^6]: ASIC REP 815, "Hardship, not as hard to get help", 25 Sep 2025. https://download.asic.gov.au/media/db0d1jmf/rep-815-hardship-not-as-hard-to-get-help-published-25-september-2025.pdf
[^7]: ASIC 24-254MR, ASIC sues NAB over hardship responses, 2024. https://asic.gov.au/about-asic/news-centre/find-a-media-release/2024-releases/24-254mr-asic-sues-nab-for-failing-customers-facing-financial-hardship
[^8]: APRA, CPS 230 Operational Risk Management (in force 1 Jul 2025). https://apra.gov.au/operational-risk-management-0 · Bird & Bird commentary: https://www.twobirds.com/en/insights/2023/australia/apras-cps-230-takes-effect
[^9]: Home Affairs, overview of the AML/CTF Amendment Act 2024. https://www.homeaffairs.gov.au/about-us/our-portfolios/criminal-justice/anti-money-laundering-and-counter-terrorism-financing/anti-money-laundering-and-counter-terrorism-financing-amendment-act/overview-of-the-aml-ctf-amendment-act
[^10]: Bright Law, "AML/CTF April 2026 final consolidated Act and Rules update", Apr 2026. https://www.brightlaw.com.au/aml-ctf-april-2026-final-consolidated-act-and-rules-update/
[^11]: Treasury ministers, SPF sector designation, 28 May 2026. https://ministers.treasury.gov.au/ministers/daniel-mulino-2025/media-releases/albanese-government-steps-industry-protections-stop
[^12]: HSF Kramer, "Stage 1 of the Scams Prevention Framework", Jun 2026. https://www.hsfkramer.com/de/insights/2026-06/stage-1-of-the-scams-prevention-framework
[^13]: KWM, "Loan behold: non-bank lenders to join the CDR". https://www.mallesons.com/au/en/insights/latest-thinking/loan-behold-non-bank-lenders-to-join-the-consumer-data-right.html · The Adviser: https://www.theadviser.com.au/lender/48669-non-banks-plugged-into-open-banking-data-grid
[^14]: Ashurst, "Action initiation under Australia's CDR becomes law" (2024). https://www.ashurstperkinscoie.com/en/insights/action-initiation-under-australia-consumer-data-right-becomes-law/
[^16]: MAS, consultation paper P017-2025 on AI risk management guidelines (13 Nov 2025–31 Jan 2026). https://www.mas.gov.sg/publications/consultations/2025/consultation-paper-on-guidelines-on-artificial-intelligence-risk-management
[^17]: Allen & Gledhill, "MAS publishes AI risk management guidelines", Oct 2026 (read). https://www.allenandgledhill.com/sg/publication/articles/34686/mas-publishes-ai-risk-management-guidelines-setting-out-supervisory-expectations-on-responsible-ai-adoption
[^18]: OJK, "Indonesia Artificial Intelligence Governance for Banking" (29 Apr 2025). https://ojk.go.id/en/Publikasi/Roadmap-dan-Pedoman/Perbankan/Pages/Indonesia-Artificial-Intelligence-Governance-for-Banking.aspx
[^19]: OJK Circular 20/SEOJK.08/2025 summary: https://regalert.today/document/84a6624e-f897-4690-a979-ec72ec55a942/text · Bank Mandiri annual report (legacy 20 working days): https://www.bankmandiri.co.id/documents/38268824/40289827/C.1.1+-+AR++page+719-723.pdf/162a4a7e-e520-ddd3-a7e1-02fb34f76387
[^20]: RSM Indonesia client alert, 18 Sep 2026 (PP 33/2026). https://www.rsm.global/indonesia/en/node/439
[^21]: BNM Policy Document on Complaints Handling (28 Mar 2025; effective 1 Apr 2026). https://www.bnm.gov.my/-/pd-complaints25 · The Edge: https://theedgemalaysia.com/node/749732
[^22]: Baker McKenzie, "Malaysia: PDP (Amendment) Act 2024 to come into force". https://insightplus.bakermckenzie.com/bm/data-technology/malaysia-personal-data-protection-amendment-act-2024-to-come-into-force
[^23]: Vietnam Briefing, Decree 356 (2026). https://www.vietnam-briefing.com/news/vietnam-personal-data-protection-regulation-decree-356.html · Tilleke & Gibbins: https://www.tilleke.com/insights/new-decree-provides-guidance-for-vietnams-personal-data-protection-law/
[^24]: MFAA media release, 3 Sep 2026 (Cotality data; read). https://www.mfaa.com.au/wp-content/uploads/2026/09/MORTGAGE-BROKERS-FACILITATE-A-RECORD-81.6-OF-ALL-NEW-HOME-LOAN-LENDING-IN-AUSTRALIA.pdf
[^25]: The Adviser: AFG 17.2 days https://theadviser.com.au/lender/45591-lenders-reaching-unconditional-approval-in-record-time-afg · Broker Pulse 2024 https://theadviser.com.au/broker/43725-small-adi-turnarounds-fastest-on-record-broker-pulse
[^26]: The Adviser, "Banks explain lagged turnarounds to parliament". https://www.theadviser.com.au/breaking-news/41762-banks-explain-lagged-turnarounds-to-parliament
[^27]: Mozo, "How long does home loan approval take?" (undated). https://mozo.com.au/home-loans/articles/how-long-does-it-take-to-get-your-home-loan-approved
[^29]: The Adviser, AFCA FY25. https://www.theadviser.com.au/compliance/47349-afca-complaints-top-100-000-for-second-consecutive-year · Money Management: https://www.moneymanagement.com.au/news/financial-planning/unacceptably-high-afca-hits-100k-complaints-fy25
[^30]: Banking Day, ACXPA Q4 2024 bank call-centre rankings (Feb 2025). https://bankingday.com/bank-call-centre-customers-wait-longer
[^31]: NextGen ApplyOnline: https://nextgen.net/digital-lodgement/ · First Federal on ApplyOnline: https://www.brokernews.com.au/news/breaking-news/first-federal-goes-live-on-applyonline-with-esign-and-nextgenid-290066.aspx · ANZ × Loanapp (2018): https://exclusives.anz.com.au/newsroom/media/2018/04/anz-partners-with-loanapp-for-lending-innovation/
[^32]: Police Bank × Temenos: https://finextra.com/pressarticle/94328/australias-police-bank-selects-temenos-banking-cloud · Cognizant × Temenos, 21 Aug 2025: https://www.temenos.com/press_release/cognizant-and-temenos-expand-partnership-to-power-core-banking-transformation-in-australia/ · FinTech Futures Aug 2026 (MoveBank; Queensland Country / Data Action): https://www.fintechfutures.com/bankingtech/august-2026-top-five-banking-technology-stories-of-the-month
[^33]: nCino ANZ team spotlight: https://ncino.com/news/ncino-apac-team-spotlight · Summerland Bank × nCino: https://ffnews.com/newsarticle/fintech/summerland-bank-selects-ncino-to-drive-efficiency-through-digital-transformation/
[^34]: VIB × Temenos: https://ffnews.com/newsarticle/fintech/vib-drives-digital-banking-innovation-with-temenos-latest-version-of-banking-platform-powered-by-aws · LPBank: https://www.retailbankerinternational.com/news/lpbank-selects-temenos-to-modernise-retail-and-corporate-banking/ · MSB: https://www.theasianbanker.com/updates-and-articles/best-core-banking-technology-initiative-mid-size-bank-goes-to-vietnam-maritime-commercial-joint-stock-bank-msb-and-temenos-2025
[^35]: NiCE GSB case study, Nov 2025: https://resources.nice.com/wp-content/uploads/2025/11/Great_Southern_Bank-CS-252809.pdf · ServiceNow agentic contact centre for banking: https://www.servicenow.com/docs/r/financial-services-operations/agentic-contact-center-for-banking-landing.html
