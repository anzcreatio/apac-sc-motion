# D1. Prove it, click path, harvest, reset

**Path P1 · 75 min · lab stand · Skills:** `creatio-uc-readiness`, `creatio-demo-clickpass`, `sc-clickpath`, `sc-harvest`

## Why it matters

"It worked when I built it" isn't a demo. A use case is ready when it's been rehearsed end to end on a **twin**
record, checked from the database and on screen, and reset. Then the click path teaches the presenter (often not
the builder) exactly what to click and say, and the harvest makes the next SC's build faster. Last, you leave the
lab stand as you found it.

## Lab

1. **Readiness on UC1** (`creatio-uc-readiness`): Claude writes the twin of `KJ-1042` and its reset first, then a
   step file from the hero story (one field per step), and runs it step by step, stopping at each screenshot for a
   visual verdict. Fix anything that fails, re-run until the verdict is green. Note the verdict and path in `lab-log.md`.
2. **ClickPass** (`creatio-demo-clickpass`): one clean rehearsal, no fixes, into click path cards (step, screenshot,
   what to click, what changes, what to say). Output in your practice folder only.
3. **SC click path** (`sc-clickpath`): build the two pages (SC practice + customer recap) into
   `<practice dir>/clickpath/`. Try practice mode. The recap stays **DRAFT**.
4. **Harvest, dry run** (`sc-harvest`): read the skill with Claude and write the L1 entry (build log, customer-specific
   list, install steps) into `<practice dir>/harvest/`. **Never** into `library/catalogue.json` or SharePoint
   `Library/`: it's a lab.
5. **Reset the stand.** Claude reads `lab-log.md`, then lists what it would remove: your lab records (jobs, sites,
   lab client accounts, tasks, the AI skill's agent registration and quick link), then the lab app and its package.
   Everything must contain your initials / `Acad<Initials>`. **You say yes**, Claude deletes, then reads back that
   nothing of yours is left and nothing else changed.
6. **Close:** `academy.py result … --result pass`, the three feedback questions, and tell Renzo you've finished path 1.

## Check (pass criteria)

- [ ] UC1 readiness verdict green, with the path named, from a run on the twin (not the hero).
- [ ] Click path cards and both `sc-clickpath` pages exist in the practice folder; the recap says DRAFT.
- [ ] An L1 harvest entry exists in the practice folder; the team library (`library/catalogue.json`,
      SharePoint `Library/`) is unchanged.
- [ ] After reset, `list-packages` shows no `Acad<Initials>` package and an OData read finds no lab records.

## Traps

- **Rehearsing on the hero record** leaves debris the presenter sees. Twin, always.
- **Polling frames instead of reading each checkpoint**: the runner stops at every shot on purpose.
- **A ClickPass nobody rendered or verified** is refused by its builder: look at every frame.
- **Recaps go to customers only after the SC's approval**; never from training at all.
- **Deleting by package name** once removed two packages with the same name (1 Nov 2026). Delete by exact name, after
  a listing, with your yes; nothing outside `Acad<Initials>`.
- **Harvest to the real library from a lab** would show a fictional demo to every SC as reusable.
