# Creatio Delivery Assurance: packages and when to use them (v0.1)

> **INTERNAL ONLY.** For SCs and AEs. Never paste this file, the source deck or the prices into a customer output.
> Customers can hear *that* Delivery Assurance exists and what it does (the "can say" lines below); the AE owns the
> package and the price.
>
> **Source (C):** `Delivery Assurance - Jan2026 (2).pptx` (16 slides, author Andie Dovgan, saved 16 Nov 2026), dropped
> in SharePoint by Renzo on 16 Nov 2026, filed in `_inbox/_done/2026-11-16/`. Earlier versions (Aug 2024, Oct 2025
> "Delivery Assurance Package") are superseded by this one. Prices are as written on the slide ("$", currency not
> stated); check with the AE before quoting anything.

## 1. What it is

A paid Creatio (vendor) governance service that sits **alongside the partner's implementation**. It aligns three
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

## 3. Packages

All four give access to the whole framework; they differ in limits and intensity. All are **"No ARR tie"** (not tied
to the licence value).

| | **#1 Start Right** | **#2 Build & Run Quality** | **#3 Strategy & Scale** | **Freedom** |
|---|---|---|---|---|
| Price (per year, as on slide) | $30,000 | $65,000 | $125,000 | $TBD, **approval required** |
| Best for | First implementation, team skills | Active projects, production quality | Enterprise scale, complex integrations | Non-standard needs, specific problems, staffing gaps |
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

Full per-line limits: deck slides 10–15 (source file above).

## 4. When an SC should raise it (partner delivery risk)

Raise it with the AE first, then with the customer. Recommend a package, don't list all four.

| Signal in the deal | Why it's a delivery risk | Suggest |
|---|---|---|
| New or small partner, first Creatio project of this size, or partner not chosen yet | Rework, wrong patterns, scope creep | #1 (requirements + design review before build) |
| Customer wants an internal CoE / to own the platform after go-live | Skills gap after the partner leaves | #1 or #2 (CoE workshops, training, maturity assessment) |
| RFP fit-gap shows custom, partner or integration lines (`sc-rfp`, `sc-workshop`) | Custom code and integrations are where projects fail | #2 (design + integrations reviews, code review hours) |
| Core-system integrations (core banking, ERP, LOS), regulated customer (BFSI), many entities or countries | Data sync, security, performance | #3 (4 integration reviews, data sync validation, 2×/month governance) |
| Customer has been burned by a previous CRM project, or asks "how do we know the partner will deliver?" | Trust in delivery, not in the product | #2; frame it as the vendor staying in the room |
| Existing customer with a slow or unhealthy instance, or a stalled rollout | Adoption and performance | Freedom or #1 (health check, automation workshop) |

**Where it goes in our motion**

- **First meeting / discovery:** listen for the signals above; note them in the brief as delivery risks (tag **I** until
  the customer says it). Don't pitch it in a first meeting unless they ask about delivery risk.
- **RFP fit-gap (`sc-rfp`):** every requirement rated *custom*, *partner* or *integration* is a reason to propose DA.
  Mention it in the bid/no-bid recommendation for "bid with conditions".
- **Proposal (W5):** a line in the delivery approach: "Creatio Delivery Assurance (package proposed by the AE)". Price
  only from the AE.
- **Partner Pack (W5):** list which DA reviews are planned (requirements, design, integrations, go-live) so the partner
  plans for them; they're checkpoints, not extra work for us.

## 5. Can say / don't say (customer conversations)

| Can say | Don't say |
|---|---|
| "Creatio offers Delivery Assurance: we stay involved alongside your partner, reviewing requirements, design, integrations and go-live readiness." | Any price, hour count or package name, unless the AE has approved it for this deal |
| "It's there to catch design problems early, before they become rework." | That Creatio guarantees the partner's delivery, timeline or outcome |
| "It can also help you build your own Centre of Excellence so you own the platform after go-live." | That it replaces the partner, or that Creatio will build anything |
| "There are a few levels depending on project size and complexity; your AE can take you through them." | Anything about the Freedom package (needs internal approval) |

## 6. Open points

- Currency and whether prices are list or negotiable: not on the deck. Ask the AE / Delivery team before quoting.
- Who runs DA in APAC (named contact): not on the deck. Add it here when known.

SC check required before any of this is used with a customer.
