---
name: sc-sizing
description: Recommend on-premise (or customer-managed cloud) infrastructure for a Creatio APAC deal - servers per environment (application, database, Redis, load balancer, Kubernetes, RabbitMQ, MongoDB, Creatio.ai), a reduced-footprint option, storage (object storage, database, backups) and the software stack - starting from Creatio's system requirements calculator and adjusted with Creatio Academy and the infrastructure team's rules. Produces a customer-ready Word document and Excel sheet worded as a recommendation pending review by Creatio's infrastructure team, plus an internal file with every source and a draft note for the infra review. Use when an SC asks about hardware sizing, server specs, on-prem or self-hosted requirements, infrastructure for an RFP or RFI, storage or database sizing, Redis or Kubernetes questions, minimum or POC hardware, or how many servers a customer needs - including a brand-new deal where sizing is the only ask (for example a partner ran the earlier stages): it creates the deal folder without starting the motion from the beginning.
---

# sc-sizing

> **Mac:** run every `python …` command below as `python3 …`.

On-prem sizing questions come up on most bank deals. The answer has to be useful to the customer's infra team, but it
is never ours to confirm: **Creatio's infrastructure team (Sergey Sinienok) reviews every sizing before it is final**
(Renzo, 18 Nov 2026). So the documents are customer-ready in content and tone, and every one says, politely, that it's
a recommendation pending that review.

Paths are relative to this skill's folder; plugin root = `../..`. Script: `scripts/sizing.py`.
Rules (stack, editions, rules R1–R31 with sources, storage method, customer wording): `../../knowledge/SIZING-RULES-v0.1.json`.
Background: `references/calculator-notes.md` (how the calculator behaves), `references/academy-onsite-notes.md`
(everything sizing-related in Academy's on-site deployment guides, with URLs).

## Hard rules

1. **The calculator is the base.** `sizing.py calc` fetches it live per environment and saves the page in
   `<deal>/sizing/`. Never type server specs from memory or from an old deal.
2. **Every change to the calculator is a rule with a source** (R1–R31). No rule fits → don't improvise: put it in the
   infra note as a question.
3. **Recommendation, not commitment.** Customer text never says guaranteed, will support, ensures, certified,
   definitive, final sizing, 100% and the like (`check` refuses them). Use: recommend, suggest, plan for, starting
   point, based on, to be confirmed. The status line always shows: *Preliminary recommendation, pending review by
   Creatio's infrastructure team* → *under review* → *reviewed …, to be confirmed against your detailed workload*.
4. **Infra review before it leaves.** Send the internal file's draft note to Sergey; set `review --status in_review`.
   Only he moves it to `infra_reviewed` (`--by "Sergey Sinienok"`). The SC sends the documents; Claude never sends.
5. **Ask about high availability first (R1).** The fault-tolerant scheme multiplies hardware. Many customers don't
   need it outside production, or at all for a POC.
6. **Out of scope:** licences (that's `sc-bom`: on-prem needs the right edition, ML needs the predictive service
   on-site licence, AI needs the right package), and the LLM's own hardware when Creatio.ai is on-prem (R28: involve
   Roman Prus first; on-prem AI is limited).
7. **No customer names in the plugin.** Past cases are generic labels (`../../standards/CONFIDENTIAL-TERMS-v0.1.md`).

## Inputs

| Input | Where | If missing |
|---|---|---|
| Users, portal, HA, environments, stack, services, volumes, retention | The customer's RFI/RFP, the AE, meeting reviews, `rfp/register.json` | `intake_questions` Q1–Q12 in the rules file: ask the top ones, record the rest as assumptions (tag A) |
| Products in scope | `bom.json`, `deck.json` summary | Ask: bank products are Windows only today (ST11) |
| The customer's own template | RFI spreadsheet | Fill it from the `.xlsx` (one row per server type, per environment) |

## Starting a deal with sizing only

Some deals reach us mid-way: a partner ran discovery and the demo, and all they need from us is a sizing. **Start
there; don't run the motion from the beginning** (Renzo, 18 Nov 2026). No transcript, deck, demo-depth question or
first-meeting pack is needed.

1. **Folder.** `python scripts/sizing.py start --account "<customer full name>" [--partner "<partner>"] [--asked-by "<who>"]`.
   It follows the deal folder rule (`../sc-setup/SKILL.md`): reuses the account's folder with any SC suffix, stops on
   a close match (ask the SC, then pass that folder to `new` or rerun with `--confirm-new`), otherwise creates
   `Deals/<kebab-account>-<sc>/`. It writes `00-deal-start.md` (entry: sizing only, partner, who asked) and
   `sizing.json` with `entry.type = "sizing-only"`. It prints `DEAL=<folder>`.
2. **Chat.** Number and title the chat as usual (`../../standards/CHAT-TRACKING-v0.1.md`) with stage **`Sizing`**:
   `python ../sc-desk/scripts/desk.py chat-open --deal "<folder>" --stage Sizing --topic "<2-4 words>" --short <SHORT>`.
3. **Dates.** Record only what's known (`../sc-guide/scripts/deal_dates.py set … --field sc_notified`). No first-call
   date is fine on a partner deal; don't ask for it.
4. Then the steps below from step 2 (fill inputs). The BFSI rule still applies: a bank's requirements and our
   proposed infrastructure go to `sc-bank-ai-log`.
5. **Later.** If the deal moves into discovery, a demo or a proposal, `sc-guide` picks it up from the folder; the
   sizing stays as it is. Never start the motion on your own because the folder looks empty.

## Steps

1. **Start.** Sizing-only deal: see above. A deal already in the motion:
   `python scripts/sizing.py new "<deal folder>" --customer "<short name>"` writes `<deal>/sizing.json`.
   If one exists, update it; never start a second.
2. **Fill inputs.** Each input is `{value, tag, source}` (tags **C** customer said · **P** partner said · **I**
   inferred · **A** assumed). Values:
   - `active_users` (busiest time of day), `named_users`, `portal_users`
   - `scheme`: `fault_tolerant` or `simple`; `minimise`: true to trade Redis HA for a smaller footprint (R2)
   - `app_platform`: `netfw` (Windows + IIS) or `net` (Linux, PostgreSQL only); `db`: `mssql` | `pg` | `oracle`
   - `recovery`: `full` (typical for banks) | `simple`; `bulk_email`
   - `components`: any of `global_search`, `dedup`, `ml`, `email_listener`, `creatio_ai`; with
     `email_listener` also `mailboxes` and `email_flow_per_s`
   - `horizon_years`, `file_store` (`s3` default, R29), `platform`, `kubernetes`, `siem`, `products`
   - `environments`: list of `{name, kind}` with kind `prod`, `nonprod` (10% of prod users, R8) or `poc` (R13).
     Set `users` on an environment only if the customer gave a number.
   - `storage.activities`: `{label, per_user_per_day, size_mb, users, shared}` (mark content uploaded once for
     everyone as `shared`), `records_per_month`, `initial_db_gb` (migrated data), `replicas` of the object store.
   - `assumptions`: one line each, in customer language (they appear in the document to confirm).
3. **Calculate.** `python scripts/sizing.py calc <deal>/sizing.json`. It fetches the calculator per environment,
   applies the rules and writes a **recommended** and a **reduced** configuration per environment. If the fetch fails,
   open the link (`sizing.py url`) in the browser, save the page text as `<deal>/sizing/calc-<env>.txt` and rerun
   with `--offline <deal>/sizing`.
4. **Storage.** `python scripts/sizing.py storage <deal>/sizing.json`: files per month, usable object storage at 1, 3
   and 5 years with ~30% headroom, DB data, log/temp, backups (4–5×), second copy and app-node disk (Sergey's
   method, Oct 2026).
5. **Check.** `python scripts/sizing.py check <deal>/sizing.json`. Fix every ERROR; read every WARN to the SC.
6. **Build.** `python scripts/sizing.py build <deal>/sizing.json --nn <next number>` writes:
   - `NN-sizing.docx`: customer-ready recommendation (basis, assumptions to confirm, architecture, servers per
     environment with the reduced option, storage, software, what could change it, next steps)
   - `NN-sizing.xlsx`: the same servers, one sheet per environment, plus storage (easy to paste into an RFI template)
   - `NN-sizing-internal.md`: inputs with tags, calculator links and snapshots, every rule used with its source,
     warnings, open questions, conflicts between sources, and the **draft note to the infra team**
7. **Infra review.** Give the SC the draft note (they send it with the `.docx`). `review --status in_review`. When
   Sergey replies: apply his corrections, rebuild, `review --status infra_reviewed --by "Sergey Sinienok" --notes "…"`.
   **Every correction he makes is a lesson:** log it as feedback (step 9) so the rule is added to the next rules version.
8. **Tell the SC** in at most eight lines: environments and server counts, the biggest cost driver (usually HA), the
   reduced option, storage at the horizon, assumptions the customer must confirm, and the warnings. Then the files.
9. Ask one short "how did that go?" question and log feedback as usual (`../sc-guide/SKILL.md` mode C).

## Quick answers (no full run)

Questions like "do they need Redis Enterprise?" or "can Redis go on the app server?": answer from the rules file
(`editions`, `rules`) with the source, in recommendation wording. The common ones:

| Question | Answer (source) |
|---|---|
| MS SQL Standard or Enterprise? | Both supported; depends on their HA and performance needs (ED1) |
| Redis Enterprise needed? | No; Redis 7.4+ Open Source is enough (ED2) |
| Elasticsearch licence? | Open-source-compatible distributions are enough (ED3) |
| Replace Redis? | No, Redis is the only supported cache (ED4) |
| 6 Redis servers, really? | Only for a Redis Cluster. With HA but a small footprint, 1 node is a fair trade-off; never 2–3 with home-grown failover (R2, R3) |
| Redis on the app server? | Merging is possible but not recommended (R15); fine for a POC (R13) |
| Docker or Kubernetes for the services? | Kubernetes (R5) |
| Linux with MS SQL? | Not on the .NET line yet; Linux means PostgreSQL (ST4) |
| Non-production size? | Calculator at 10% of production users (R8) |
| Files in the database? | Recommend S3-compatible object storage from day one (R29, R30) |

## When to run it

| Moment | What |
|---|---|
| Customer asks "what hardware do we need?" or an RFI has a sizing tab | Full run; assumptions tagged A go back as questions |
| POC on-prem | `kind: poc` environment (R13) |
| Meeting review or RFP answers bring real numbers | Update inputs, `calc`, rebuild, back to infra review if numbers moved |

## Outputs

`<deal>/sizing.json` (source), `<deal>/sizing/calc-*.txt` (calculator snapshots), `NN-sizing.docx` and
`NN-sizing.xlsx` (customer-ready after infra review), `NN-sizing-internal.md` (internal).
