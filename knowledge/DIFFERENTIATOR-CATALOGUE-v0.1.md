# Differentiator catalogue v0.1 (draft)

Owner: APAC SC team (we define our own differentiators). Status: **draft**. Proof points and competitor facts were checked
in the research pass `differentiators-research-2026-11-03.md` (design workspace `research/`, not in the plugin) (3 Nov 2026).
Always attribute claims as shown here ("customers reported, per…"), and recheck prices before quoting them.

## 1. The rule: what every demo must show (core set **approved by Renzo, 3 Nov 2026**)

| Tier | Differentiators | Rule |
|---|---|---|
| **Core, every deal** | **D1** Change at the speed of business · **D3** AI that acts, governed | Every demo has a D1 proof moment and a D3 proof moment |
| **Track core** | **P (Platform): D2** One platform · **A (AI Studio): D5** Fits your landscape | Every P demo shows D2; every A demo shows D5. P+A shows both. **Industry rule: every manufacturing demo shows D5** (approved 3 Nov 2026) |
| **Supporting** | **D4** Business owns the rules · **D6** Time to value · **D7** Lower cost to own and change | Used where the pains call for them. D6 and D7 live mainly in the Proposal, not the demo |

**Why only 2 + 1 core:** a 45–60-minute demo has room for 3–4 scenes. Asking for all 7 would turn it back into a
feature tour. **Gate A checks the core set**, and the rest are optional.

## 2. The catalogue

### D1 · Change at the speed of business (core)
| Field | Content |
|---|---|
| **Claim (customer words)** | "When your business changes, your system changes the same day, without a project." |
| **Pain it answers** | Every change needs IT or the vendor; backlogs; workarounds in spreadsheets and email; tools that lag the business |
| BFSI example | A new product, a regulatory form or a hardship rule takes months to land in the system |
| Manufacturing example | A new dealer programme or warranty rule waits for an ERP/CRM change cycle |
| **Discovery question** | "When the business needs a change in your current system, how long does it take, and who has to do it?" |
| **Proof moment (≤ 1 min)** | The customer corrects one of our assumptions in the demo → the SC changes the rule live (a value or a new row, e.g. a separate limit for investment loans) and re-runs a record that now routes differently. (Validation moments are designed to create this.) Adding a field takes ~1.5 min; a process change takes 3–6 min and is a planned set piece only (measured at Scentia; see [M6 live-change kit](M6-LIVE-CHANGE-KIT-v0.1.md)). A: change a rule the agent reads, and the agent behaves differently on the next request; don't edit the agent's prompt live |
| **Sandbox asset** | Scentia: 3 rehearsed live changes (`CHANGES.md`). To build: a standard "live change" kit per Core/Industry module |
| **Competitor contrast** | Show, don't argue: competitors also sell low-code. Our point is that a business analyst makes the change live in the meeting. Never say "they can't" |
| **Proof point** | "Customers reported a 68% reduction in application development time" (Nucleus Research 26077, Apr 2026; customer-interview based). **Don't use** "10x faster" (a roadmap deck title, not a measurement) |

### D2 · One platform (track core for P)
| Field | Content |
|---|---|
| **Claim** | "Sales, service, workflow, portals and AI on one data model, not separate clouds stitched together." |
| **Pain it answers** | Customer data split across systems; re-keying; no single view; integration projects for every new need |
| BFSI example | Lending, service and complaints in different tools; staff swivel between screens (GSB test: "older CRM plus core screens") |
| Manufacturing example | Quotes, dealer portal and after-sales service in different systems |
| **Discovery question** | "To see everything about one customer today, how many screens does your team open?" |
| **Proof moment** | Follow one customer from enquiry → case/application → portal update → dashboard without leaving the app |
| **Sandbox asset** | GOC Greek Schools (portal + enrolment + order + payments); Pertamina (ticketing + KB + dashboards); Ord Minnett wealth sandbox |
| **Competitor contrast** | Microsoft: Dynamics 365 app + Power Apps + Copilot Studio credits + M365 Copilot are licensed separately. Salesforce: industry clouds, Agentforce and Data Cloud are separate add-ons. Creatio packages platform, CRM products and AI Studio under one vendor (but compare like-for-like; see D7) |
| **Proof point** | Gartner MQ for CRM Sales Platforms 2026: **Visionary** (don't say "only Visionary" without checking the graphic) · Forrester Wave **Strong Performer**: CRM Software for Financial Services Q1 2025; Customer Service Solutions Q1 2026 · Manufacturing: IDC MarketScape Worldwide B2B CRM Platform Software for Industrial Manufacturing 2024, **Leader** (June 2024, 12 vendors; vendor-reported, IDC report not seen) · Banking stories: OTP Bank (80% of corporate banking processes automated, reported), Ent Credit Union (+18% new deposit conversions, reported) |

### D3 · AI that acts, governed (core)
| Field | Content |
|---|---|
| **Claim** | "AI that does the work inside your process, and asks a person before it acts where it matters." |
| **Pain it answers** | Skilled staff doing admin; AI pilots that only chat and never complete a task; risk teams blocking AI they can't control |
| BFSI example | Document checks before credit assessment (Harbourline mock); routine enquiries in the contact centre (GSB test) |
| Manufacturing example | Triage of warranty claims or quality reports; drafting quotes from an enquiry |
| **Discovery question** | "If AI took one task off your team tomorrow, which would it be, and what would it be allowed to do on its own?" |
| **Proof moment** | The agent does the customer's task end to end → asks a named person to confirm → the action lands in the record → the audit trail is shown |
| **Sandbox asset** | Sovico (AI briefing skill); Pertamina AI-interaction log; AI Studio agents calling Creatio processes as tools. To build: agent test set + confirm-then-act pattern |
| **Competitor contrast** | **"Agentic" is table stakes, not a differentiator.** Salesforce markets Agentforce and "agentic CRM", Microsoft has generally available Dynamics 365 service agents, and ServiceNow sells AI agents for banking. Our difference is **how**: agents are built and changed no-code on the same platform where the process, data and approvals live, with a confirm-then-act step and an audit trail the business can see. Never claim to be the only one with agents |
| **Governance** | Say only what `AI-GOVERNANCE-PACK-LITE-v0.1.md` allows |

### D4 · Business owns the rules (supporting)
| Field | Content |
|---|---|
| **Claim** | "Your business people change thresholds, SLAs, pricing and approvals themselves, as data, not code." |
| **Pain it answers** | Rules hidden in code or in people's heads; inconsistent decisions; IT tickets for a threshold change |
| **Discovery question** | "Who can change an approval limit or an SLA today, and how long does it take?" |
| **Proof moment** | A business user changes a rule value (e.g. a $1.2m approval limit) → the next record routes differently |
| **Sandbox asset** | Scentia `labPackRule` (rules as data) |
| **Competitor contrast** | Optional; usually shown, not argued |

### D5 · Fits your landscape (track core for A)
| Field | Content |
|---|---|
| **Claim** | "We work alongside your core banking, ERP, contact centre and Microsoft tools. No rip-and-replace." |
| **Pain it answers** | Fear of another failed big-bang project; an incumbent platform that must stay; AI that can't reach the data |
| BFSI example | The loan system stays until renewal (Harbourline); the contact-centre platform stays (GSB) |
| Manufacturing example | SAP stays; Creatio runs the dealer, service or quality process around it (Pact) |
| **Discovery question** | "Which systems have to stay, and what must a new solution talk to?" |
| **Proof moment** | Architecture picture with their named systems → a simulated sync in the demo (a record arrives from "their" system; the update goes back) |
| **Sandbox asset** | Scentia simulated Salesforce sync; Ord Minnett coexistence with Xplan/AdviserLogic. To build: a generic "their system" stand-in for core banking and ERP |
| **Competitor contrast** | Suites that are strongest when you move everything onto them. Lead with *their* named systems staying, not with a claim about the competitor |

### D6 · Time to value (supporting, Proposal)
| Field | Content |
|---|---|
| **Claim** | "Weeks to the first live outcome, not quarters, because most of it is configured, not coded." |
| **Pain it answers** | Long projects; benefits arriving after the budget cycle; the failed-project scar tissue |
| **Discovery question** | "By when does this need to show results, and what happened last time you ran a project like this?" |
| **Proof moment** | "This demo, on your process, was built in N days." + a phased roadmap with a first release in weeks |
| **Sandbox asset** | Build logs and prompt logs (Scentia `PROMPT-LOG.md`) |
| **Proof point** | Howdens deployed Creatio in 12 weeks; Xledger UK, a 3-month low-code rollout (vendor case studies; one customer each, not a benchmark). Strongest proof is our own: "this demo was built in N days" |

### D7 · Lower cost to own and change (supporting, Proposal) **new**
| Field | Content |
|---|---|
| **Claim** | "Lower cost to license, run and change, because changes don't need specialists." |
| **Pain it answers** | Licence renewals that keep rising; paying consultants for every change ("lower licence costs" is a common BDR trigger) |
| **Discovery question** | "What do you spend each year on changes to your current system, not just licences?" |
| **Proof moment** | Not a demo scene. In the Proposal: a 3-year cost-of-change comparison with assumptions stated |
| **Creatio facts** | From 1 May 2026: **Unlimited** plan (unlimited users, agents, apps, workflows; priced by organisation size), with Growth and Enterprise still per user. **AI Studio comes with every Business Studio licence**; AI use is bought as annual **AI credit packages**. Never say "AI is free" or "unlimited means no cost limits" |
| **Competitor contrast** | As listed at time of writing: Salesforce Agentforce, Flex Credits $500 per 100k (~$0.10 per action), $2 per conversation, or per-user add-ons from $125/user/month · Microsoft Copilot Studio, $200 per 25k-credit pack per month or pay-as-you-go, on top of separately licensed Dynamics 365, Power Apps and M365 Copilot. **Build a like-for-like 3-year scenario per deal**; Creatio meters AI too |
| **Don't use** | "37% lower TCO / 70% faster than Salesforce and Microsoft" as a general fact (vendor-promoted study, switchers only, no public method); "Gartner says 40% of CRM projects fail" (no primary source); "75% Salesforce overspend" (competitor survey). If needed: "Nucleus Research reports customers saw 20–40% lower TCO" (2026), attributed |

## 3. Where each touchpoint shows a differentiator

| Touchpoint | What to show | Differentiators |
|---|---|---|
| BDR call | One line in the booking pitch: "Our team will show you how organisations like yours change their process the same day, and how AI takes tasks off the team." | D1, D3 |
| Discovery (hypothesis slide) | Each hypothesis maps to a D-ID (in the card, not on the slide) | All |
| Discovery (validation) | When they correct a hypothesis: "That's exactly the kind of change you'd make yourselves in Creatio." | D1 |
| One-pager | "What we'll show you" names the outcome; the differentiator is implied, not named | D1–D5 |
| Demo | Core set + track core, each scene ends with value + metric | D1, D3 + D2/D5 |
| Proposal | "Why Creatio for you": 3 differentiators chosen by their pains, each with proof | Any, plus D6 and D7 |
| Partner pack | Which differentiators were promised, so delivery keeps them true | — |
| Any touchpoint where delivery risk comes up | "Creatio stays involved through delivery": words only from `DELIVERY-ASSURANCE-v0.2.md` §6 (a service, not a differentiator; no prices) | — |

## 4. Proof gaps to close

| Gap | Why it matters | Action |
|---|---|---|
| **No named public bank or manufacturer reference in AU, NZ, ID, MY, VN or SG** | "Trusted by banks in the region" can't be said today | Ask Creatio APAC marketing for referenceable local customers; until then use global stories (OTP Bank, Ent Credit Union, Howdens) and say where they are |
| AI Studio designers marked "coming soon" in the Academy (Workflow and Code Agent Designers) | Don't demo or promise what isn't released | Check the Academy before each AI Studio demo |
| Creatio list prices only confirmed via third-party sites | Price claims in Proposals | Get the official price book from Creatio sales ops |

## 5. Changes applied (3 Nov 2026)
- D1 proof moment corrected to measured times: the ≤90 s promise holds for rule values and rows, not for fields or process steps (M6 kit, harvested from Scentia).
- Process §9.2 points to this file; Gate A wording is now "D1 + D3 + the track core (D2 for P, D5 for A) appear at least once".
- W1 Output 7 picks from D1–D7; W3 scenes include the core set (W2 v0.2 no longer suggests scenes).
