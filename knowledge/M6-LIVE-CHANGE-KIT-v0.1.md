# M6 Live-change kit v0.1 (design; nothing built before sign-off)

> **What it is:** the rehearsed changes an SC makes in front of the customer when they correct one of our
> assumptions. It is the proof for **D1** (change at the speed of business) and **D4** (business owns the rules), and
> the payoff of every validation moment in W3 (the demo design step; plugin skill `sc-demo-plan` from Phase 1).
> **Harvested from Scentia** (rehearsed on a live stand, 28 and 30 Oct 2026): `Scentia/helpers/LIVE-CHANGE-REHEARSAL.md`
> (field + process rule, timed) and `Scentia/partnerpack/CHANGES.md` (rules as data in `labPackRule`).
> **Owner:** the Core pack owner (SC); industry entries by the BFSI and Manufacturing pack owners.

## 1. What Scentia taught us

| Lesson | Evidence | What the kit does about it |
|---|---|---|
| **A rule stored as data changes in seconds; a rule in a process takes minutes** | Process gateway: ~8 min while recording, 3–4 min practised. Field: ~1.5 min. Changing a `labPackRule` value: a record edit | Every module keeps its thresholds in one **demo rules object** (§3). Validation moments use data changes |
| Process changes are too slow for a "We assumed X?" answer | 5–6 min total for field + rule + proof, over the 4-min target | Process changes are a **planned set piece**, at most one per demo, never the answer to a correction (§2, tier 4) |
| Designers open in a new tab; the record tab needs a reload | Rehearsal 28 Oct | Presenter protocol: pre-open designer tabs; reload before proving |
| The page designer's save rewrote the page body and dropped two hidden buttons | Rehearsal 28 Oct | Never live-edit the hero page. Field changes happen on a page that is rolled back from a saved copy after the demo |
| A new field's code stays `labColumnNN` unless edited and confirmed with ✓; title position defaults to the left | Rehearsal 28 Oct | Checklist in tier 3 |
| The process designer's SAVE is a split button: "Save new version" makes a new active version and complicates the rollback | Rehearsal 28 Oct | Always "Save current version"; or switch between a prepared inactive version and the original (Scentia `…PartnerPack1` pattern) |
| A change can trip another rule (a data change exposed an expired enrol-by date) | Rehearsal 30 Oct | Every change has a **proof record** prepared on each side of the boundary, and is rehearsed end to end |
| The line that lands: "a trained configurator close to the business does this; IT still owns architecture, integrations, security and release" | Scentia demo line | Use it after every live change (§5). It is also the honest answer on governance |

## 2. Change tiers

| Tier | What changes | Typical time (practised) | Use it for | Proof |
|---|---|---|---|---|
| **T1 Value** | A value in the demo rules object or a lookup: a limit, a percentage, days, a count | **≤ 30 s** | Validation moments (first choice) | Re-run a prepared record at the boundary: it routes differently |
| **T2 Row** | Add a row: a second limit for another type, a document on a checklist, a lookup value (new status, new reason) | **≤ 1 min** | Validation moments ("it's different for investment loans") | A prepared record of the new type follows the new row |
| **T3 Field / page** | Add a field to a form, make one required, show or hide it by a business rule | **1.5–2 min** + reload | Validation moments only where a T1/T2 change can't answer, and only on a disposable page | The field appears and is used on the next record |
| **T4 Process logic** | A new gateway, step or approval in a process | **3–6 min** (Scentia measured 3–4 min practised, 8 min first time) | **A planned set piece**, max one per demo, announced as "let me show you how a process change works". Never improvised | Two records, one on each side of the new branch |

**Rule:** a validation moment is answered with T1 or T2 wherever possible. Design the demo so the likely corrections
**are** T1/T2 (that is the point of §3). T3 is acceptable. T4 is never the answer to a correction made in the room.

**AI scenes (Track A):** change **a rule value the agent reads** (T1), e.g. "the agent may block a card but a person
approves reissue" as a setting, not by editing the agent's prompt live. A live prompt edit can behave differently
from the rehearsal; keep it for a rehearsed set piece only, with the backup video ready.

## 3. Build requirement: one demo rules object per stand

To build after sign-off with the first modules (M4, then M2/B-M2). Pattern: Scentia `labPackRule`.

| Column | Example |
|---|---|
| Code | `APPROVAL_LIMIT`, `DOC_RECENCY_DAYS`, `SLA_HOURS_P1` |
| Applies to (optional lookup: product, loan type, case category, dealer tier) | *Owner-occupied home loan* |
| Value · Unit | 1200000 · AUD |
| Business owner (role) | Head of Lending Operations |
| Description (customer's words) | "Above this, the credit committee decides" |
| Active | ✔ |

- Processes and business rules **read the value by Code (+ Applies to)**; nothing is hard-coded in a process or formula.
- The record list of this object is a section the presenter can open in one click: **"Business rules"**, named in the
  customer's words on the day (e.g. "Lending policy settings").
- Each rule has **two seed records**, one each side of the boundary (e.g. $1.15m and $1.35m), and a third of a
  different type for T2 changes.
- The reset (Run before demo) restores every rule row to its seed value and deletes rows added in the demo.
- This object is also what the Partner Pack hands over (§4.4 "Rules and approvals: candidates for rules-as-data").

## 4. Change catalogue (rehearse before use; times are targets until measured)

ID scheme: `LC-<module>-<nn>`. "Rehearsed" is filled in when an SC has timed it on a stand.

### Core
| ID | Module | "We assumed…" | Change | Tier | Proof | Rehearsed |
|---|---|---|---|---|---|---|
| LC-M2-01 | M2 Enquiry to order | "…discounts over 10% need a manager's approval" | Discount threshold value | T1 | Two quotes at 8% and 12% | — |
| LC-M2-02 | M2 | "…the same threshold for every product line" | Add a row for a product line | T2 | Quote on that line | — |
| LC-M3-01 | M3 Onboarding + portal | "…these four documents are needed" | Add a document to the checklist | T2 | New application asks for it | — |
| LC-M4-01 | M4 Case + SLA | "…priority 1 cases need a response in 4 hours" | SLA hours value | T1 | New P1 case shows the new due time | — (harvest Pertamina SLA) |
| LC-M4-02 | M4 | "…complaints follow the same SLA as other cases" | Add an SLA row for the complaint category | T2 | New complaint gets its own clock | — |
| LC-M4-03 | M4 | "…escalation goes to the team lead" | Change the escalation role in the rule | T1 | Breach routes to the new role | — |
| LC-M5-01 | M5 AI agents | "…the agent can do X alone" | Toggle the rule the agent reads ("needs approval") | T1 | Same request: agent now asks a person | — |
| LC-GEN-01 | Any form | "…you also track [field]" | Add a field to a disposable page | T3 | Field shows on the next record | ✔ Scentia 28 Oct (~1.5 min) |
| LC-GEN-02 | Any process | (set piece) "Over [N], an extra approval" | New gateway + status step | T4 | Two records either side | ✔ Scentia 28 Oct (3–4 min practised) |

### BFSI
| ID | Module | "We assumed…" | Change | Tier | Proof | Rehearsed |
|---|---|---|---|---|---|---|
| LC-BM2-01 | B-M2 Broker file | "…the delegated lending authority is $1.2m" | DLA value | T1 | $1.15m vs $1.35m file | — |
| LC-BM2-02 | B-M2 | "…the same DLA for every loan type" | Add a row for investment loans | T2 | Investment file at the boundary routes to committee | — (**asked for in the Harbourline mock**) |
| LC-BM2-03 | B-M2 | "…self-employed applicants need 1 year of tax returns" | Document rule: years required | T1/T2 | Self-employed file asks for 2 years | — (**asked for in the Harbourline mock**) |
| LC-BM2-04 | B-M2 | "…payslips older than 30 days are stale" | Recency days value | T1 | Agent flags a different payslip | — |
| LC-BM4-01 | B-M4 Onboarding + CDD | "…enhanced due diligence above risk score N" | CDD threshold | T1 | Customer at the boundary gets EDD | — |
| LC-BM5-01 | B-M5 Hardship + complaints | "…the hardship response clock is 21 days" | Statutory clock value (their policy) | T1 | New case shows the due date | — |
| LC-BM6-01 | B-M6 Service agent | "…the agent can reissue a card" | Rule: reissue needs approval | T1 | Agent now asks a person | — |

### Manufacturing
| ID | Module | "We assumed…" | Change | Tier | Proof | Rehearsed |
|---|---|---|---|---|---|---|
| LC-MM2-01 | MM2 Warranty + dealer portal | "…warranty is 24 months for every product" | Add a row for a product family | T2 | Claim on that family checked against the new period | — |
| LC-MM2-02 | MM2 | "…claims under $500 are auto-approved" | Auto-approve limit | T1 | Two claims either side | — |
| LC-MM3-01 | MM3 Complaint → CAPA | "…CAPA is due in 30 days" | CAPA due days | T1 | New CAPA due date | — |
| LC-MM3-02 | MM3 | "…these words flag a possible reportable event" | Add a keyword to the reportability list | T2 | Complaint with that word is flagged for QA | — |
| LC-MM4-01 | MM4 Quote → order | "…margin under 18% needs approval" | Margin threshold | T1 | Quotes at 17% and 19% | — |

New entries come from W3 Output 6 ("new for rehearsal") and are added here after the demo with their measured time.

## 5. Presenter protocol

**Before the demo**
1. Run before demo (reset). Check each rule row and both boundary records are at their seed values.
2. Open the rules section in a second tab; for T3/T4, pre-open the designer tab (saves ~15–20 s on camera).
3. Rehearse every planned change once on this stand, this week, and write the time in the catalogue.
4. Backup video of each planned change is ready.

**In the room**
1. Ask the validation moment as written in the W3 pack. If they confirm, move on: a "yes" is also a result.
2. If they correct it: "Let's change it now." Do the change. **Say what you're doing in business words** ("I'm adding
   a separate limit for investment loans"), not in product words.
3. **Prove it** on the prepared record, without a manual refresh where possible.
4. Say the line: "That's the kind of change your team makes. Realistically a trained configurator close to the
   business does it; IT still owns architecture, integrations, security and production release."
5. Write the correction down for the Brief (it's now **Confirmed**) and for the Partner Pack's rules table.

**Never**
- Live-edit the hero page in the page designer (its save can rewrite the page).
- Choose "Save new version" in the process designer.
- Improvise a T4 change, or edit an AI agent's prompt live, unless it is the rehearsed set piece.
- Leave a change in place after the demo: roll back, then reset.

**If it goes wrong:** "Let me show you the one we prepared", switch to the backup video, carry on. Note it for the kit.

## 6. After the demo
- Roll back in this order: process versions → page (restore the saved copy) → added rows → then Run before demo.
- Update the catalogue: rehearsed ✔, measured time, stand version, date, anything that went wrong.
- The correction itself goes to the industry pack's harvest log: if customers keep correcting the same assumption,
  change the pack default.

## 7. Open items
| # | Item | Owner |
|---|---|---|
| 1 | Build the demo rules object and the first entries with M4 (harvested from Pertamina) after sign-off | Core pack owner |
| 2 | Time every T1/T2 entry on a stand (none measured yet; only T3/T4 were timed at Scentia) | Each pack owner |
| 3 | Decide where rules live for AI Studio agents (a setting the agent reads through a tool) | SC + SE |
| 4 | Backup videos per module | Each pack owner |
