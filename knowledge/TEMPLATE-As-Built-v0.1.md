# As-built summary template v0.1 (existing customers)

**When:** step 1 of the existing-customer path (`skills/sc-guide/SKILL.md` mode D). We inherit or extend a solution
that's already live: a partner's handover, a "reverse demo", a go-live walkthrough, or the SC's own earlier build.
**Not a meeting review:** there's no deck of ours to compare and often no customer in the room.
**Save as:** `<deal>/01-as-built-<yyyy-mm-dd>.md`. Internal: never sent to the customer as is.
**Evidence tags** on every line: C confirmed by the customer · P said by the partner or the builder · I inferred · A assumed.
A partner's walkthrough is **P**, not C, even when it describes what the customer wants.

---

```
# <Customer>: as-built summary (<date>)

| | |
|---|---|
| Customer | <name, what they do> |
| Live since | <go-live date or "not live yet"> |
| Delivered by | <delivery partner and people, or Creatio team> |
| Account owner | <who owns the account and the roadmap: Creatio / partner / both> |
| Customer contacts | <main contact, who changes things today> |
| Sources | <transcripts, documents, scope slides, with dates> |

## 1. Purpose
What problem it solves and the one output the customer cares about, in their terms.

## 2. Flow
Numbered steps from input to outcome: what triggers each, what it produces, which system or source it uses.

## 3. Where AI is used, and where rules decide
| Step | Driven by (process / integration / AI skill / agent / person) | Sources |
|---|---|---|
Who can override an AI answer, and how.

## 4. Who can change what today
| Change | Who can do it (customer business user / customer IT / partner / Creatio) | How |
|---|---|---|

## 5. Known limits
What it can't do, and what the customer accepted as out of scope.

## 6. Asked for, not built
Requests and scope items not delivered yet (their words, tagged). These feed the roadmap's first horizon.

## 7. Confidential
Terms or data the customer asked us not to share. Propose each with a generic label and, on the SC's yes, record it:
`python skills/sc-lessons/scripts/confidential.py add --deal <deal> --term "..." --generic "..."`.
Write the generic labels everywhere in this file except where the original is needed to work on the deal.

## 8. Ownership gaps (only when the account owner changes or the customer wants to own more)
| Part | Who holds it now | What's needed to take it over |
|---|---|---|
| Package source and versions | | |
| Integrations: API contracts, credentials, who pays the subscription | | |
| AI skills, agents and their prompts | | |
| Support: who fixes it when it breaks | | |
| Documentation | | |

## 9. Next step
The roadmap (`sc-guide` mode D step 3), with an owner per item.
```

---

**v0.1 (16 Nov 2026):** first version, from a partner's internal walkthrough of a delivered founder-screening solution
(feedback `2026-11-16-renzo-huruiti-as-built-capture.md`, `…-delivery-partner-and-ownership.md`).
