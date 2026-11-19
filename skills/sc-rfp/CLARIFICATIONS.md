# RFP clarification checklist (sc-rfp step 8)

Built from the Navalo RFP (18–19 Nov 2026). Go through every topic, keep only what changes our answer, sizing, price
or demo, and write the questions by `../../standards/CUSTOMER-QUESTIONS-v0.1.md`.

## 1. Dates and asks first

| Check | How |
|---|---|
| Their deadlines | Work out each one from the issue date in business days (participation, clarifications, response, demo, BAFO). Put them in the chat row (`desk.py chat-set --due`) |
| Where each ask comes from | Some asks are only in the cover email, not the RFP files (Navalo: "nominate an executive sponsor" was in the 12 Nov email, the RFP sheet only had "Primary contact"). Quote the source when the SC has to raise it internally |
| Document status | A file titled "Draft" next to one titled "Final": ask which is the set |

## 2. Topics to check

| Topic | What to look for | Example question |
|---|---|---|
| Weighting and gates | No weights given; "mandatory gates" mentioned but not listed; Day 1 vs End state | "Which criteria are mandatory gates, and what does a pass look like?" |
| Which parts apply | Parts for platforms we don't sell (middleware, marketing); multi-platform overlays; vendor + partner propositions | "Would you still like us to answer B3?" + "Will answering it bring our score down?" |
| Requirements they reference but didn't send | "Traceability matrix against prioritised requirements" with no list | "Is this one of the documents pending NDA?" |
| Format | Architecture, implementation, commercials: separate or attached; commercials separate | — |
| Day 1 scope and volumes | Businesses, products, channels, teams, target date; volumes today and in 5 years | Keep the example list (licensing and TCO depend on it) |
| Systems of record and middleware | Real-time account views, transactions, who owns the APIs, when middleware is chosen | "Should we assume your middleware will give the CRM documented APIs into those systems?" |
| **Where cases live** | CRM **and** workflow both in scope: criteria often allow cases in either ("through an integrated CRM or directly within the workflow system"). The core lending or banking system may keep hardship or collections | "Which system should be the main place cases are created and worked?" |
| Channels | Broker, aggregator and dealer platforms (direction in/out); portal logins and their volume; customer app or portal | — |
| Third-party services | Customer IdP and its admin APIs, staff SSO, verification services, e-signature, SMS, email | — |
| Documents and migration | Records system, retention schedule by type, what migrates from where | — |
| Regulation | APRA CPS 230 / 234, material service provider, licences a SaaS vendor is asked to hold | — |
| Residency | Support access from outside the country; AI processing | Answer only from the governance pack's "can say" lines later |
| Contract | Their paper or ours; a draft before the response | — |
| References | Must they be local and in the same industry; calls during due diligence | Ask the rule plainly, don't reveal the gap |
| Demo | Journeys (when, same for all), sample data, who drives; a live change for every vendor | Promise the outcome, not the internals |

## 3. Reading traps

| Trap | Reality |
|---|---|
| "Service Management" category (incident, problem, change, SLA) | The vendor's own IT service operations, not customer service. Scope `bid` |
| Multi-platform overlay (two references of "the exact combination") | Applies only if we bundle platforms. One platform → rate n/a and confirm in a question. Don't bundle a middleware partner to win it |
| "Configuration over customisation" weighted | No custom components in the proof demo, or label them custom in the configuration inventory |
