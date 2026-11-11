# Core pack v0.1 (General industry)

## 0. Pack header
| Field | Value |
|---|---|
| Pack | **Core** (= General industry). BFSI and Manufacturing inherit everything here and override only what differs |
| Inherits from | n/a |
| Owner (SC) | (to assign) |
| Version / date | v0.1 · 3 Nov 2026 |
| Segments covered | Any mid-to-large organisation with customers, cases or applications: services, education, healthcare, utilities, distribution, public sector |
| Deals harvested | None yet. Content draws on the portfolio (Scentia, GOC, Pertamina, SJOG, Sovico, IJN, Ord Minnett), mock call 01 and W1 test 01 |

> Status: **draft from experience + research.** §4 benchmarks come from the research pass; everything else is
> "A (Assumed)" until a deal confirms it. Log hits and misses in §2 and §10. **Only real deals count as hits;** mocks and tests are logged as "test signal".

---

## 1. Top pains and consequences

| ID | Pain | Consequence | Typical owner | Journey |
|---|---|---|---|---|
| CP1 | Slow response to new enquiries | Lost deals to faster competitors; wasted marketing spend | Head of Sales / Marketing | J1 |
| CP2 | Sales time lost to admin and re-keying | Fewer customer conversations; poor pipeline visibility | Head of Sales | J1 |
| CP3 | Quotes and approvals stuck in email | Slow turnaround; inconsistent pricing and discounting | Sales ops / Finance | J1 |
| CP4 | Onboarding stalls on missing documents and information | Long time to revenue; customer drop-out; staff chasing | Head of Operations | J2 |
| CP5 | No single view of the customer across teams and systems | Repeat questions; errors; handle time; missed cross-sell | COO / Service head | J2, J3 |
| CP6 | Cases not resolved first time; no clear ownership | Repeat contacts; complaints; cost to serve | Head of Service | J3 |
| CP7 | SLAs and obligations tracked by hand | Breaches found late; regulatory and contract risk | Service / Compliance | J3 |
| CP8 | Every change needs IT or the vendor | Backlogs; spreadsheets and workarounds; tools lag the business | COO / CIO | All |
| CP9 | Skilled staff doing routine admin (notes, checks, summaries) | High cost per task; burnout; slow service | Operations | All (AI) |
| CP10 | AI interest without a safe path to production | Pilots that stall in risk review; board pressure unmet | CIO / Risk | All (AI) |

## 2. Hypothesis library

Slide wording is an industry observation, ≤12 words, and something the customer could say "no" to.

| ID | Slide wording | Track | Usual owner | Journey / task | KPI | D-IDs | Signals that make it likely | Hit / miss |
|---|---|---|---|---|---|---|---|---|
| C-H01 | New enquiries wait hours or days for a first response | P | Sales / Marketing | J1 | Speed to first response | D2, D1 | Inbound-led growth; web forms; "leads go cold" | |
| C-H02 | Sales teams spend more time updating systems than selling | P | Head of Sales | J1 | % selling time | D2, D3 | Several tools; spreadsheet pipelines; field sales | |
| C-H03 | Quotes take days because approvals go round by email | P | Sales ops / Finance | J1 | Quote turnaround | D4, D1 | Complex pricing; discount approvals; B2B | |
| C-H04 | Onboarding stalls while teams chase missing documents | P | Operations | J2 | Time to onboard; % incomplete | D3, D2 | Document-heavy onboarding; regulated checks | |
| C-H05 | Customers give up on applications before finishing | P | Digital | J2 | Abandonment rate | D2 | Online applications; mobile-first customers | |
| C-H06 | Staff re-key the same customer details into several systems | P | Operations / IT | J2, J3 | Re-keying time; error rate | D2, D5 | Legacy core/ERP; manual hand-offs | |
| C-H07 | Staff switch between several screens to see one customer | P | Head of Service | J3 | Handle time | D2 | Contact centre; "older CRM plus core screens" | Test signal only (invented BDR quote, GSB W1 test); not a confirmation |
| C-H08 | Customers call back because cases aren't resolved first time | P | Head of Service | J3 | First-contact resolution; repeat contacts | D2, D3 | Complaint volumes; NPS pressure | |
| C-H09 | SLA breaches are found after the fact, not before | P | Service / Compliance | J3 | % within SLA | D4 | Contracted or regulated response times | |
| C-H10 | Every process change waits in the IT backlog | P | COO / CIO | All | Time to change | D1 | Long change queues; vendor-dependent system | |
| C-H11 | Routine questions still reach people; self-service can't finish them | A | Head of Service | AI-T3 | Containment; cost per contact | D3 | High contact volumes; chatbot that only answers FAQs | Test signal only (invented BDR quote, GSB W1 test); not a confirmation |
| C-H12 | Skilled staff spend hours on notes, summaries and checks | A | Operations | AI-T1, T4 | Minutes per task | D3 | Expensive specialists; document-heavy work | Test signal only (fictional mock); not a confirmation |
| C-H13 | AI pilots stall in risk and architecture review | A | CIO / Risk | All (AI) | Time from pilot to production | D3, D5 | Board AI mandate; AI policy in draft | |
| C-H14 | Leaders can't see where work is stuck until customers complain | P | COO | All | Visibility of ageing work | D2 | Growth; new COO; turnaround targets | |

## 3. Reference journeys

### J1 · Enquiry to order
| Step | Neutral term | Customer terms we've heard | Who | Usual system | Typical break |
|---|---|---|---|---|---|
| 1 | Enquiry captured | lead, enquiry, referral, web form | Marketing / reception | Web forms, email, spreadsheet | ⚠ Sits unassigned |
| 2 | Qualify and assign | triage, allocate | Sales manager / BDR | CRM or inbox | ⚠ Manual allocation; slow first response |
| 3 | Meet and understand needs | discovery, fact-find | Sales rep / RM | Calendar, notes | Notes not captured |
| 4 | Propose / quote | quote, proposal, offer | Sales rep | Spreadsheet, Word, ERP | ⚠ Pricing built by hand |
| 5 | Approve | discount approval, deal desk | Manager / Finance | Email | ⚠ Waits in inboxes |
| 6 | Negotiate and win | close, sign | Sales rep | Email, e-signature | |
| 7 | Order / hand over to delivery | order, onboarding, job | Sales → Operations | ERP / ops system | ⚠ Re-keyed into ERP; context lost |

### J2 · Customer onboarding (application → active customer)
| Step | Neutral term | Customer terms we've heard | Who | Usual system | Typical break |
|---|---|---|---|---|---|
| 1 | Application / request | application, enrolment, sign-up | Customer / broker / staff | Portal, PDF form, email | ⚠ Arrives incomplete |
| 2 | Identity and eligibility checks | KYC, verification, eligibility | Ops officer | Third-party checks | |
| 3 | Collect documents | evidence, supporting documents | Ops officer ↔ customer | Email, uploads | ⚠ Back-and-forth, 2–3 rounds |
| 4 | Review and decide | assessment, approval | Assessor / manager | Core system, spreadsheet | ⚠ Queues; manual checks |
| 5 | Set up in core systems | account opening, provisioning | Ops / IT | Core / ERP | ⚠ Re-keying |
| 6 | Welcome and first use | welcome pack, activation | Ops / service | Email, portal | No status visibility for the customer |

### J3 · Service case to resolution
| Step | Neutral term | Customer terms we've heard | Who | Usual system | Typical break |
|---|---|---|---|---|---|
| 1 | Contact | call, email, chat, portal, complaint | Customer | Contact-centre platform, inbox | |
| 2 | Identify the customer | verify, look up | Agent | Several screens | ⚠ Swivel between systems |
| 3 | Classify and route | triage, queue, escalate | Agent / rules | Contact-centre platform, CRM | ⚠ Misrouting; transfers |
| 4 | Resolve or escalate | fix, refer, L1–L3 | Agent / specialist | CRM, knowledge base | ⚠ Knowledge hard to find |
| 5 | Follow-up and approvals | callback, refund approval | Specialist / manager | Email | ⚠ No owner; SLA slips |
| 6 | Close and learn | close, survey, root cause | Team leader | CRM, survey tool | Root causes not tracked |

## 4. KPI benchmarks
Source URLs and detail: `core-kpi-benchmarks-2026-11-03.md` (design workspace `research/`, not in the plugin).
**Rule:** use these to frame *range questions*, not as claims. Only Strong rows may be quoted to a customer, attributed.
Never cite Salesforce's own reports to a prospect (a direct competitor's research can backfire).

| KPI | Journey | Typical range | Range question | Source + date | Quality |
|---|---|---|---|---|---|
| First-contact resolution | J3 | Average ~69% (range 43–88%); 70–79% good; 80%+ world-class (~5% of centres). Complaints ~48% | "Closer to 60, 70 or 80%?" | SQM Group, 2024 | **Strong** |
| Issues fully resolved in self-service | J3 / AI-T3 | ~14% | "Of the people who try self-service, how many finish there?" | Gartner, Aug 2024 | **Strong** |
| Average handle time (AU contact centres) | J3 | ~537 s (~9 min), self-reported | "Closer to 5, 8 or 12 minutes?" | ACXPA (year not named) | Medium |
| After-call work | J3 / AI-T4 | ~45–60 s per contact (vendor data, India); our estimate 30 s–2 min | "Closer to 30 seconds, a minute, or two-plus?" | Vendor; our estimate | Weak |
| Chatbot / virtual agent containment | AI-T3 | 20–40% typical; higher for narrow, mature bots | "Closer to 10, 25 or 40%?" | Vendor sources only | Weak |
| Speed to first response to a web lead | J1 | Only ~37% respond within an hour; average ~42 h in follow-up write-ups; ~7× more likely to qualify if contacted within an hour | "Same hour, same day, or next day?" | HBR, 2011 (2,241 US companies), old | **Strong but old** |
| Share of rep time spent selling | J1 | Under 30% | "Closer to a quarter, a half, or more?" | Salesforce State of Sales (competitor research; don't cite) | Medium |
| Sales cycle (mid-market B2B) | J1 | ~42 days (USD 10–100k deals); ~84 days (>USD 100k) | "Closer to one, two or three months?" | Ebsta × Pavilion (vendor) | Medium |
| Quote turnaround | J1 | 24 h to 4.5 days | "Same day, a few days, or a week?" | CPQ-vendor blogs | Weak |
| Corporate onboarding / KYC review time | J2 (B2B, BFSI) | ~95 days; USD 1,500–3,000 per review | "Weeks or months?" | Fenergo (vendor) | Medium |
| Application abandonment | J2 | 63–68% of consumers have abandoned **at least one** application. **Not** a per-application drop-off rate | "Of applications started, how many finish?" | Signicat (vendor), Europe | Medium; use with care |
| Applications incomplete on arrival | J2 | No credible source; mock and anecdote say "about half" | "A quarter, half, or more?" | none | Our estimate |
| Time spent searching for information | All | ~19% of a knowledge worker's time (2012 estimate built on IDC data, not a survey) | "How much of the day goes on finding things?" | McKinsey, 2012 | Medium, old; label it |
| Lead → opportunity conversion; win rate; case resolution vs SLA; re-keying time; time to change a system | Various | **No credible source found** | Ask open: "What does it look like today?" | — | — |

**Default value inputs** (used by W5 only when the customer gave none; always tagged Assumed and listed for the SC to replace):

| Input | Default (AU, our estimate) |
|---|---|
| Loaded cost per hour: specialist (assessor, underwriter, engineer, case manager) | AUD 70 |
| Loaded cost per hour: support / contact centre / admin | AUD 50 |
| Benefit ramp | Year 1: 50% · Year 2: 90% · Year 3: 100% |
| AI pilot (one task, measured) | 8 weeks, proposed; partner to confirm |
| Phase 1 to first live outcome | 10–12 weeks, proposed; partner to confirm |
| Discount rate for the 3-year view | 10% |

**Gap to close:** the ACXPA 2026 Best Practice Report (Australian contact-centre benchmarks, July 2026) isn't public.
Getting a copy would give us local FCR, handle-time and after-call-work data.

## 5. Personas and terminology
| Persona | What they do all day | What they look at | What they'd love to stop doing |
|---|---|---|---|
| Executive sponsor (COO / GM) | Targets, escalations, board reporting | Turnaround, cost, satisfaction, risk | Finding out about problems from customers |
| Sales rep / relationship manager | Calls, meetings, proposals | Pipeline, next meetings | Updating systems after every call |
| Sales / team manager | Coaching, approvals, forecasting | Pipeline, team activity, SLA | Chasing updates for the forecast |
| Operations / back-office officer | Checks, documents, data entry | Work queue | Chasing missing documents; re-keying |
| Service agent | Contacts, cases | Customer view, knowledge base | Switching screens; writing notes |
| Customer / partner (portal user) | Applies, asks, tracks | Status | Calling to ask "where is it?" |
| IT / enterprise architect | Landscape, integration, security | Architecture, risk | Another silo to integrate |
| Risk / compliance | Obligations, audits | Breaches, audit trail | Evidence gathered by hand |

**Terminology map** (neutral → industry terms; use the customer's own word once known):
customer → client / member / patient / student / dealer · case → ticket / enquiry / complaint / job ·
application → request / enrolment / referral · opportunity → deal / pipeline · quote → proposal / offer.
**Words to avoid by default:** "CRM" (when there's scar tissue or the deal isn't a CRM replacement), "chatbot",
"replace your system", "reduce headcount".

## 6. Regulation and compliance hooks (cross-industry)
*Names below are for orientation; verify the current law before citing it to a customer.*

| Theme | Where it applies | Demo hook |
|---|---|---|
| Privacy and personal data | AU Privacy Act / APPs · Indonesia PDP Law · Malaysia PDPA · Singapore PDPA · Vietnam personal-data rules | Consent fields; access by role; data residency statement (governance pack) |
| Complaints handling and response times | Most regulated sectors; contracts with SLAs | SLA timers; escalation rules; breach dashboard |
| Record keeping and audit | Regulated sectors; public sector | Audit trail on records and on AI actions |
| AI governance | Board AI policies; regulator reviews (e.g. ASIC's review of banks' new and proposed AI uses, incl. decision-making and lending, letter 30 Sep 2026; see BFSI pack) | Confirm-then-act; audit log; governance pack lite |
| Accessibility | Public-facing portals | Accessible portal pages |

## 7. Typical landscape and competitors
| System type | Common in APAC | Stays or goes? | Integration story (D5) |
|---|---|---|---|
| ERP / core | SAP, Oracle, Microsoft Dynamics, MYOB / Xero (SMB, AU), industry cores | Stays | Creatio runs the customer-facing process; orders, accounts and balances sync |
| Productivity | Microsoft 365, Google Workspace | Stays | Email, calendar, Teams |
| Incumbent CRM | Salesforce, Dynamics 365, HubSpot, Zoho, in-house | Goes or coexists | Coexist first where a contract runs; replace at renewal |
| Contact centre | Genesys, NiCE, Amazon Connect, Five9 | Stays | Creatio is the service record and the acting agent; the platform routes |
| Data platform | Databricks, Snowflake, Microsoft Fabric | Stays | Read/write via APIs; AI uses the governed data |

| Competitor | Their angle | Our counter (catalogue only) |
|---|---|---|
| Salesforce | Market leader; industry clouds; Agentforce | D2 one platform and package; D1 change without specialists; D7 like-for-like cost incl. AI credits |
| Microsoft (Dynamics, Power Platform, Copilot Studio) | "You're already Microsoft" | D5 we work with M365; D2 one product vs several licences; D1 |
| ServiceNow | Enterprise workflow and AI agents | D1 business-led change; D7 cost at mid-market scale |
| HubSpot / Zoho | Simple and cheap | D2 depth (case, workflow, portal, AI on one model); D4 |
| Low-code (Power Apps, OutSystems, Mendix) | Build anything | D2 CRM + workflow + AI ready-made, not built from scratch; D6 |
| In-house build (often on the data platform) | "We'll build our own agents" | D3 governed workflow + front-line UI they'd otherwise build; reuse their data platform |

## 8. Demo modules (design only; nothing built before process sign-off)
| Module | Covers | Core-set proof moments | Exists today? | Build size |
|---|---|---|---|---|
| **M1 Outcome dashboard** | Opening "where the time goes" view per journey | D2 | Partly (Pertamina, SJOG dashboards) | S |
| **M2 Enquiry to order** | J1 incl. quote approval | D1, D4 | No (Sovico C360 is a start) | M |
| **M3 Onboarding + portal** | J2 incl. documents and customer status | D2, D3 | Partly (Scentia portals, GOC enrolment) | M |
| **M4 Case + SLA + knowledge** | J3 incl. escalation and portal | D2, D4 | Yes (Pertamina ticketing, SLA, KB) | S (harvest) |
| **M5 AI agents** | The 6 agent patterns in §9 | D3 | Partly (Sovico AI skill, Pertamina AI log, AI Studio agents). **In regulated deals, don't lean on AI Studio governance until the governance pack's AI Studio item is answered** | M |
| **M6 Live-change kit** ([design](../M6-LIVE-CHANGE-KIT-v0.1.md)) | Rehearsed changes per module in 4 tiers; one demo rules object per stand | D1, D4 | Designed; pattern proven at Scentia (`labPackRule`, timed field and process changes) | S (harvest) |
| **M7 "Their system" stand-in** | Simulated ERP / core / contact centre sync | D5 | Partly (Scentia simulated Salesforce sync) | S |

## 9. AI use-case library (Core)
| ID | Task | Agent alone | Human approves | Data / systems | Value maths | Proof moment | Pattern |
|---|---|---|---|---|---|---|---|
| AI-T1 | **Document check + missing-info request** | Checks documents against the application; lists what's missing; drafts the request | Sends the request; any decision | Application record, documents, email | Minutes per file × files per month; rounds of back-and-forth | Stale document flagged in seconds; request drafted; officer approves | Document check |
| AI-T2 | **Enquiry triage and routing** | Reads the enquiry; classifies; sets priority; routes; drafts a first reply | Exceptions; VIP or complaint cases | Inbox / portal, customer record | Time to first response; misroutes | Email arrives → case created, routed and acknowledged | Intake + triage |
| AI-T3 | **Routine enquiry resolution** (chat / email / voice) | Answers and acts on routine requests within policy | Anything outside policy; hand-off with summary | Customer record, core system via API, knowledge | Containment × cost per contact | Customer asks → agent answers and acts → flag → hand-off to a person with a summary | Customer self-service |
| AI-T4 | **Call / meeting summary to the record** | Summarises; updates fields; creates follow-up tasks | Confirms the summary | Transcript, record | After-call work × contacts | Call ends → summary and tasks appear; agent confirms | Internal copilot on records |
| AI-T5 | **Prepare and confirm** (quote, reply, letter) | Drafts from the record and rules | Approves before sending | Record, price rules, templates | Turnaround time | Draft quote built from the opportunity; manager approves in one click | Prepare-and-confirm |
| AI-T6 | **Briefing before a meeting** | Summarises the customer: history, open cases, opportunities, news | n/a (read-only) | Record, activities | Prep time per meeting | "Brief me on this customer" → one-page briefing | Internal copilot on records |
| AI-T7 | **Knowledge answer for staff** | Finds and cites the right policy or article | n/a | Knowledge base | Handle time; consistency | Agent asks a policy question → cited answer | Internal copilot on records |
| AI-T8 | **SLA risk watcher** | Flags cases likely to breach; suggests the next action | Re-prioritises | Cases, SLA rules | % within SLA | Dashboard flags 3 at-risk cases with reasons | Monitor + alert (new pattern) |

## 10. Harvest log
| Date | Deal | What we learned | Changed in pack |
|---|---|---|---|
| 3 Nov 2026 | Mock 01 (fictional bank) | Documents can be the *cause* of slow decisions; "CRM" can be a toxic word | C-H12 added; "words to avoid" default |
| 3 Nov 2026 | W1 test 01 (GSB, public research) | The incumbent contact-centre platform's AI roadmap shapes the pitch; public data can contradict the pain quote | J3 landscape note; C-H07, C-H11 |
