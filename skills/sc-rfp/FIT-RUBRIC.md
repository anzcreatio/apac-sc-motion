# Fit rubric (sc-rfp)

One verdict per requirement. Be honest: the bid team answers the customer, and the fit-gap is what keeps their answers
true. **"Can be met" is not the same as "standard".** When unsure, pick the weaker fit and lower the confidence.

## Fit

| fit | Use when | Example |
|---|---|---|
| `standard` | Out of the box in a Creatio product (Sales, Marketing, Service, Financial Services Creatio, Customer 360, Studio). Name the product and feature in `how` | Lead management with qualification stages |
| `configure` | No-code in Business Studio: objects, fields, pages, lists, business rules, processes, approvals, dashboards, roles. Days, not weeks | A deal object for IB mandates with its own stages |
| `ai` | Creatio.ai (AI Twin, AI skills on a record, AI steps in processes) or an AI Studio agent | Next best action suggested on the client page |
| `marketplace` | Needs a Creatio Marketplace app (name it if you know it; say "check" if you don't) | WhatsApp channel connector |
| `integration` | Creatio supports it (REST/OData API, webhooks, CTI framework, email/calendar sync, file import), but it needs work with another system | Portfolio holdings pulled from the core trading system |
| `custom` | Code: C# source-code, custom Freedom UI components, heavy scripting | A bespoke revenue allocation engine |
| `partner` | A third-party product or partner service carries it | Voice recording by the telephony vendor |
| `roadmap` | Not available today; only if you know it's announced | — |
| `no` | Creatio can't do it, or it contradicts how the platform works | Fully offline patching of a SaaS site |
| `n/a` | Not a product question (commercial, legal, project, people) | "The vendor shall have a local entity" |

## Other fields

| Field | Rule |
|---|---|
| `how` | One or two sentences in plain English: the product, feature or approach. No marketing words |
| `confidence` | `high` = you know this feature exists as described · `medium` = very likely, check the detail · `low` = unsure: needs a product or SC check |
| `evidence` | Where it's backed: a Creatio Academy or product page you know, a differentiator ID (D1–D7) from `knowledge/DIFFERENTIATOR-CATALOGUE-v0.1.md`, a library module from `library/catalogue.json`. For AI data use, hosting location, data residency, certifications and security posture: **only** the "can say" lines in `knowledge/AI-GOVERNANCE-PACK-LITE-v0.1.md`; if they don't cover it, `confidence: low` and "confirm with Creatio security". A product security *feature* documented in Creatio Academy (session timeout, password policy, audit log, SSO, roles) can be cited from Academy at `medium` or `high` |
| `tier` | `Build` (show it live in the POC: must-haves at the heart of their journeys and anything that proves we're better; aim for 15–25% of lines) · `Show` (exists; a screenshot or short clip is enough) · `Tell` (a written answer: non-functional, security, architecture, admin) |
| `hours` | Only for `Build`: POC hours for an SC with the demo toolkit (configure items usually 1–4 h) |
| `mandays` | Implementation effort beyond standard (configure, integration, custom, marketplace set-up), as a first estimate; 0 for standard |
| `workaround` | For custom, partner, roadmap and no: the best alternative, if any |
| `question` | Ask the customer when the requirement is ambiguous or the fit depends on their answer |
| `english` | Only when the requirement isn't in English: your translation |

Never invent features, certifications, numbers or customer names. Never claim a competitor comparison.
