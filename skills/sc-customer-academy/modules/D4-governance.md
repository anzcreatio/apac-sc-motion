# D4. Governance for AI-assisted building

**Track 2 · 60 min · no changes to Creatio · Uses:** the toolkit's operating rules, your own policies

## Why it matters

When business builders can build with Claude, governance is what keeps it a strength: clear rules about who builds
what, where, and how it's reviewed, so speed doesn't turn into a mess of unreviewed changes. The toolkit already
builds in some of it (plan before build, approval in the conversation, writable packages only). This module writes
the rest down as your team's policy.

## Lab

1. **What the toolkit already enforces:** ask Claude to summarise the toolkit's own rules: plan approval before a
   build, which changes are "targeted" and skip the plan, environment checks, packages. Note what you'd add.
2. **Write your builder policy** (one page) with Claude's help: who may build (Track 1 graduates), where
   (development only), naming, what needs review (any change to an existing CRM page or object, any delete), who
   releases to production, how often.
3. **Data and AI questions:** list what your security or privacy team will ask (what Claude sees, where data goes,
   telemetry). Ask your Creatio contact for the official answers rather than guessing. Note the toolkit asks for
   telemetry consent: decide your answer as a policy.
4. **Review routine:** agree how a business builder's change gets reviewed (the git diff from D2 plus a look in
   development) and by whom.
5. **Support:** where builders go when stuck (internal owner, then your Creatio partner or Creatio).

## Check

- [ ] A one-page builder policy your IT lead agrees with.
- [ ] A list of data and AI questions, each with an owner to get the official answer.
- [ ] A review routine with named roles.

## Watch out for

- **No policy at all** until something breaks in production.
- **A policy so strict nobody builds**: keep development open and make release the gate.
- **Answering security questions from memory or the internet.** Get the official answer in writing.

## For the facilitator

- Data, hosting and AI answers in the room come only from the governance pack's "can say" lines; anything else is
  "we'll confirm in writing". Note each question and send it through the AE.
