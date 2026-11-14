# B1. From an idea to an approved Business Plan

**Track 1 · 75 min · no changes to Creatio · Uses:** the toolkit's app orchestrator (Business Plan first)

## Why it matters

The toolkit never builds from a one-line wish. It asks the business questions first (who uses it, what they track,
the statuses, the rules, what they need to see), writes a **Business Plan** with a technical handoff, and builds only
once you've approved it in the conversation. This is the most valuable habit in the course: the plan is what your
colleagues and IT review, and it's how you get what you meant rather than what you typed.

## Lab (practice scenario: site inspections, `practice-scenario.md`)

1. **Ask for the app in one sentence:** "I want a site inspections app for our facilities team." Notice that Claude
   doesn't build anything: it confirms what it understood and asks questions.
2. **Answer its questions** from the practice scenario. When it asks something the scenario doesn't cover, decide as
   the business owner and say so ("assume monthly inspections").
3. **Read the Business Plan:** the eight sections (outcome, roles, objects, statuses, logic, UX, analytics, edge
   cases) and the technical handoff. Find which existing CRM objects it **reuses** (Account, Contact) and which are new.
4. **Change one thing** before approving, for example a missing rule ("a Critical finding sets the result to Fail")
   or a page rule ("show the induction warning when the site requires one").
5. **Don't approve yet.** Save the plan text for B3. We build in B3, after the data model work in B2.

## Check

- [ ] A Business Plan with all eight sections exists, including the scenario's rules.
- [ ] It reuses Account and Contact rather than creating new client or person objects.
- [ ] You changed at least one thing and saw the plan update.
- [ ] Nothing was created in Creatio during this module.

## Watch out for

- **Approving a plan you skimmed.** Approval is what Claude builds from. Read the objects and statuses carefully.
- **Choices typed as free text** (status, severity): they should be lookups.
- **Asking for "a new Customer object"** when Account already exists: say "use our existing accounts".
- **A saved file isn't approval.** Approval is your clear "yes, build this" in the conversation.

## For the facilitator

- A participant with their own use case can do B1 on it too, but keep the practice scenario for B2-B5.
- Watch for over-scoping: suggest "first version" scope in the plan.
