# C2. A Creatio.ai skill

**Path P1 · 60 min · your training stand · Skills:** `creatio-ai-skill-prompts`

## Why it matters

Our rule is **Business Studio first, AI second**, and every AI moment has a person who confirms and a fallback.
A good AI skill is a short deterministic script in seven sections, it reads before it writes, and it asks before it
saves. A bad one searches by column (it can't), sums numbers in text (it gets them wrong), or writes without asking.
This module writes one properly and installs it the toolkit's way: no "paste this into the designer".

## Lab (scope: `fixtures/kestrel-lab-scope.md` → AI skill)

1. **Read the seven sections** with Claude: Role, Trigger phrases, Tool usage rules, Steps, Formatting rules,
   Output format, Constraints. Then the "what system actions can and cannot do" list.
2. **Write the prompt** for `Kestrel client update`: the open case's Id from the page context → read the case, site,
   priority, status → draft 3 lines in Kestrel's voice → ask exactly "Save this update to the job?" → only on yes
   write Client update → confirm what was saved. No sums, no searches by column.
3. **Install it** the skill's schema route, with Claude: the skill schema with the prompt and its action list,
   registered on the agent, a quick-link button on the Case page. Read it back from the server (export and grep a
   sentence), not from the import log.
4. **Rights:** the skill's operation right for your user is a rights change: Claude asks you first, and auto mode
   may block it (switch to manual mode for that one step, exactly as on real builds).
5. **Run it** on `KJ-1042` in the Creatio.ai panel: check it reads the right job, asks before saving, and saves only
   after yes. Then say "no" once: nothing may be written.
6. **Fallback:** write one line in `lab-log.md`: if the AI fails in the demo, what does the presenter show instead?
7. Add the skill and its quick link to `lab-log.md`.

## Check (pass criteria)

- [ ] The prompt has all seven sections in order, and the Output format holds the exact confirm question.
- [ ] Read-back from the server shows the new prompt text and the action list.
- [ ] Live: "no" writes nothing; "yes" writes Client update on `KJ-1042` only.
- [ ] A fallback line exists in `lab-log.md`.

## Traps

- **"There's no API, paste it in"** is wrong: only the `CopilotIntent` view lacks a write API; the schema route works.
- **`SearchEntities` is keywords only**: a step that filters by column silently returns nothing.
- **The model must never count or total in text** (it summed five rows and reported the wrong total). Aggregates
  belong to the Analytics agent or a widget.
- **Lookup Ids come from ResultJson**, never a hard-coded Id table in the prompt; never send an empty Guid.
- **The skill appears for every user of the stand** once it's on the agent: on a real stand, name it for the customer; D1 removes yours.
- **AI on the stand may be broken** for reasons outside the lab (Navalo: Creatio.ai `invalid_client`, a Support
  ticket). If the panel fails before your skill runs, log it, take the fallback, and move on.
