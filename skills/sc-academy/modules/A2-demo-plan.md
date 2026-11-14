# A2. Demo plan, build plan and approval pack

**Path P1 · 60 min · no stand · Skills:** `sc-demo-plan`, `creatio-demo-runbook`, `creatio-demo-build` (read, not run)

## Why it matters

Builds go wrong before the first click: an inferred pain built as if confirmed, a scene nobody asked for, a stand
shared with another customer, a plan the SC never approved. Our rule is **plan, then a visual build plan the SC
approves, then one approval pack, then build non-stop**. This module walks that chain on Kestrel so the real one feels
familiar, and shows how the toolkit's orchestrator reads the script you hand it.

## Lab

1. **Run `sc-demo-plan`** in your practice folder, level **Light**, using your A1 prep plus
   `tests/workshop/sample-fictional/workshop/solution-model.md` (the workshop that followed). Answer the **three
   pre-build questions** (competition; anything else from the customer; anything else to know) and the stand/device
   questions (stand = your training stand).
2. **Find in the plan:** the hero journey, each scene's label (Pain / Asked / Differentiator / SC idea), Business
   Studio before AI, and the "not built" list. Cut one scene and say why.
3. **Visual build plan:** let the skill render `NN-build-plan.html`; open it. Check each wireframe against the scene.
4. **Approval pack (dry run):** with Claude, run `sc-demo-plan/scripts/approval_pack.py new` against your practice
   folder's `build-plan.json` (approved-by = you, `--max-restarts 1`: your own stand, so a restart can be
   pre-approved). Read the checklist it prints: it's what you confirm
   before leaving a real build running.
5. **Read, don't run, the orchestrator:** open `creatio-demo-build`'s SKILL.md with Claude and find (a) where it reads
   the script, (b) which sibling skill each phase calls, (c) where it stops for a human. Then open
   `creatio-demo-runbook`: how a script becomes "action → result" steps.
6. **Compare** your plan with `fixtures/kestrel-lab-scope.md`, the scope the next modules build.

## Check (pass criteria)

- [ ] A `*demo-plan*.md` and a `*build-plan.html` exist in the practice folder; "Before we build" records the three
      answers with a date.
- [ ] `build/approval-pack.json` exists in the practice folder with restarts capped at 1, and the stand in its
      checklist is **your training stand** (if it names any other stand, the plan picked the wrong one: fix the plan).
- [ ] The SC can name at least five of the hard stops of a non-stop build (BUILD-RULES §4) and one phase of `creatio-demo-build`
      that needs a human.

## Traps

- **"I" pains built as scenes without a check question** to the customer (demo bar item 3).
- **A Full or Proof demo on a shared stand**: never; Light config only.
- **Starting configuration before the SC approves the build plan** (Renzo, 12 Nov 2026). No stand writes until then.
- **Time:** the plan's hours are build hours; readiness, reset, click path and rehearsal come on top (Perth plan: 24 h
  build + ~4 h after).
