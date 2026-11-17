# Creatio Delivery Assurance: what it is and when to raise it (v0.2)

> **INTERNAL ONLY.** For SCs and AEs. Never paste this file or the source deck into a customer output.
>
> **Why it matters:** customers buy Creatio through a partner and often fear the partner won't deliver. Delivery
> Assurance lets us say, truthfully, that **Creatio stays involved and supports them through delivery**. That can unlock
> a deal. Raise it whenever we present to a customer and delivery risk is on the table (§4–5).
>
> **APAC owner:** Alex Klochkov (Renzo, 16 Nov 2026). Package, scope and price questions go to Alex, with the AE.
>
> **Source (C):** `Delivery Assurance - Jan2026.pptx` (16 slides, author Andie Dovgan, saved 16 Nov 2026), SharePoint
> `_inbox/_done/2026-11-16/`. Earlier versions (Aug 2024, Oct 2025) are superseded.

## 0. Prices: the rule (Renzo, 16 Nov 2026)

- **No prices in anything we produce**: no deck, proposal, partner pack, email, brief, AE brief, deal file or
  knowledge file other than §7 of this one. That includes internal deal files.
- **In chat with the SC only**, you may give the indicative prices from §7, always with this warning:
  "Indicative only, from the Jan 2026 deck. It may be out of date or wrong; check the latest with Alex Klochkov before
  using it."

## 1. What it is

A Creatio (vendor) governance service that sits **alongside the partner's implementation**. It aligns three
parties: **Customer** (vision and requirements), **Partner** (implementation and context), **Vendor** (platform and
governance). It doesn't replace the partner; Creatio reviews, oversees and coaches while the partner builds.

Three promises on the deck: empower the delivery team (patterns, guidance, a CoE), mitigate risk and ensure quality
(architecture oversight, best-practice checks), maximise long-term ROI (health, performance, roadmap alignment).

## 2. The framework: three phases, 13 services

| Phase | Lifecycle | Strategic focus | Creatio services |
|---|---|---|---|
| **Start** | Elaboration: discovery, training, design | CoE foundation and skills | No-code & CoE training · CoE workshops · Maturity assessment · **Project readiness & requirements review** · **Design review with a Solution Architect** |
| **Build** | Execution & delivery: project implementation | Governance and compliance | **Project governance & oversight** (status + steering) · **Solution review & sign-off** (reverse demos, standards audit, UX) · **Integrations review** (architecture, API, code) · **Go-live readiness review** · Ad-hoc technical resources |
| **Grow** | Adoption & expansion: continuous improvement | Performance and value | Automation & optimisation workshop · Expert consultation (1:1 with architects) · Health check & performance review · Roadmap & release planning |

Who does what (deck slide 7): the **partner/customer** runs discovery, builds the backlog, designs, configures, codes,
integrates, runs UAT and cutover. **Creatio** reviews requirements, reviews the design, runs governance meetings,
reviews the solution and integrations before milestones, and greenlights go-live.

## 3. Packages (no prices; see §0)

All four give access to the whole framework; they differ in limits and intensity. None is tied to the licence value.

| | **#1 Start Right** | **#2 Build & Run Quality** | **#3 Strategy & Scale** | **Freedom** |
|---|---|---|---|---|
| Best for | First implementation, team skills | Active projects, production quality | Enterprise scale, complex integrations | Non-standard needs, specific problems, staffing gaps (**internal approval required**) |
| Governance meetings | 1/month | 1/month, milestone + risk tracking | **2/month**, quarterly alignment review | On request |
| Requirements review | 1/year | Up to 2/year + acceptance criteria | Up to 4/year + gap/overlap report | On request |
| Design reviews | — | Up to 2/year | Up to 4/year + assessment report | On request |
| Solution review | Quarterly | Quarterly + standards audit | Quarterly + defects log, report, sign-off | On request |
| Integrations review | 1/year | Up to 2/year + 16 h code review | Up to 4/year + 20 h code review, data sync check | On request |
| Go-live readiness | 1 checkpoint | + UAT and cutover plan review | Up to 2 + scorecard and gap plan | On request |
| Ad-hoc support | 20 h/year | 40 h/year | 120 h/year + 20 h custom-dev advisory | On request |
| Expert consultations | — | 16 h/year (up to 4 sessions) | 40 h/year (up to 8 sessions) | On request |
| Training / CoE workshops | 2 / 2 per year | 4 / 4 per year + maturity assessment | 6 / 6 per year + train-the-trainer (2) | On request |
| Health check | 1/year (summary) | 1/year | Up to 2/year + detailed report | On request |
| Roadmap | 1 product update demo | + release planning session | Up to 2 + adoption roadmap | On request |

Full per-line limits: deck slides 10–15. Hours and counts are internal too: don't put them in customer content.

## 4. Signals that call for it (partner delivery risk)

Recommend one package to the SC, not all four. With the customer, talk about the support, not the package.

| Signal in the deal | Why it's a delivery risk | Suggest (to the SC) |
|---|---|---|
| New or small partner, first Creatio project of this size, or partner not chosen yet | Rework, wrong patterns, scope creep | #1 (requirements + design review before build) |
| Customer wants an internal CoE / to own the platform after go-live | Skills gap after the partner leaves | #1 or #2 (CoE workshops, training, maturity assessment) |
| RFP fit-gap shows custom, partner or integration lines (`sc-rfp`, `sc-workshop`) | Custom code and integrations are where projects fail | #2 (design + integrations reviews, code review hours) |
| Core-system integrations (core banking, ERP, LOS), regulated customer (BFSI), many entities or countries | Data sync, security, performance | #3 (integration reviews, data sync validation, 2×/month governance) |
| Customer has been burned by a past CRM project or partner, or asks "how do we know this will be delivered?" | Trust in delivery, not in the product | #2; frame it as Creatio staying in the room |
| Existing customer with a slow or unhealthy instance, or a stalled rollout | Adoption and performance | Freedom or #1 (health check, automation workshop) |

## 5. Where it shows up when we present to a customer

| Touchpoint | What we do |
|---|---|
| First meeting (`sc-first-meeting`) | If a §4 signal is in the transcript, put a one-line talk track in the meeting plan for the SC, ready if delivery comes up. Not on a slide unless the customer raised delivery risk |
| Deck (`sc-deck`) | Roadmap or next-steps slide: one line such as "Creatio supports your team and partner through delivery" when a §4 signal applies. No package names, hours or prices |
| Workshop (`sc-workshop`) | The "how we'd start" close and the roadmap can say Creatio reviews requirements and design before the build starts |
| Meeting review (`sc-meeting-review`) | If they asked about implementation risk, cost blowouts or the partner, log it and propose the DA line for the next session |
| RFP (`sc-rfp`) | Bid with conditions, or must-haves rated custom, partner or integration: suggest DA in the recommendation; in answers on delivery or governance, use the "can say" lines |
| Proposal + Partner Pack (W5) | Proposal: a line in the delivery approach. Partner Pack: the planned reviews (requirements, design, integrations, go-live) so the partner plans for them |

## 6. Can say / don't say (customer conversations)

| Can say | Don't say |
|---|---|
| "You won't be on your own with the partner. Creatio stays involved through delivery: we review requirements, design, integrations and go-live readiness alongside them." | Any price, hour count or package name |
| "It's there to catch design problems early, before they become rework." | That Creatio guarantees the partner's delivery, timeline or cost |
| "It can also help you build your own Centre of Excellence so you own the platform after go-live." | That it replaces the partner, or that Creatio will build anything |
| "There are a few levels depending on project size and complexity; we'll work out the right one with you." | Anything about the Freedom package (needs internal approval) |

## 7. Indicative prices: SC chat only

Per year, as on deck slide 8 ("$", currency not stated): #1 $30,000 · #2 $65,000 · #3 $125,000 · Freedom $TBD
(approval required). **Always give the §0 warning with these.** Never copy them into a file.

## 8. Open points

- Currency, and whether prices are list or negotiable: not on the deck. Ask Alex Klochkov.
