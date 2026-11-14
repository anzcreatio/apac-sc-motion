# C1. Business processes

**Path P1 · 75 min · lab stand · Skills:** `creatio-business-processes`

## Why it matters

Processes are where a demo stops being forms and starts doing the work: the alert before the breach, the task
nobody has to remember. They're also where builds lose the most hours: the wrong route, a formula that never
expands, a signal that sees the old value, a compile that breaks the stand. The skill's first decision is the
**route**; most demo processes are native, need no compile, and are debugged in the designer by the SE.

## Lab (scope: `fixtures/kestrel-lab-scope.md` → Process)

1. **Preflight** with Claude (the skill's §0): is the process designer package on the stand (CrtProcessBuilder),
   which clio version, 10.x or 8.x. Read only. If CrtProcessBuilder is missing, **stop**: installing it is a stand
   change for the stand's owner, not a lab step.
2. **Pick the route** together using the skill's route table: "start when a Job is added with Priority = P1 → add a
   task → set a flag" is **native** (one call, no compile). Say why it's not package injection.
3. **Build** `<p>AcadXxP1Alert` in your lab package: record-added signal on Job filtered on Priority = P1; Add data
   (Activity, title "P1 <job number>: call the client within 15 minutes", owner = your contact); Modify data (Lead
   alerted = yes). **IsTracing on.** Names a customer could read.
4. **Read it back** (`describe-business-process`, saved to a file, it's long): signal, filter, both elements, tracing.
5. **Prove it ran:** add a test P1 job (one insert), then check: process log shows Completed, `SysProcessElementLog`
   has a row per element, the task exists, Lead alerted = yes. Then add a P3 job: nothing should fire.
6. **Change it as a new version:** change the task title with `modify-business-process-as-new-version`, then
   `set-active-business-process-version`. Read back which version is active.
7. Add the process, the test jobs and the tasks to `lab-log.md`.

## Check (pass criteria)

- [ ] The process is in your lab package, active, IsTracing = true.
- [ ] A P1 insert produced exactly one task and set Lead alerted; a P3 insert produced nothing.
- [ ] Element log rows exist for the run (proves tracing).
- [ ] The active version is the new one, and the SC can say how to roll back (activate the earlier version).
- [ ] No compile was run.

## Traps

- **Formulas that read element results** (`[#ReadX.ResultEntity.Col#]`) aren't expanded on create or modify: create
  with placeholders, describe, then set the body in UId meta-path form.
- **Filter values bound to an element parameter** can be stored without the column and silently match nothing
  (Navalo, clio 8.1). Read the filter back.
- **Record-modified signals see the record before the new status**: one process per target status, filtered on it.
- **`isNotNull` filters are saved as IS NULL** (clio bug): avoid.
- **Timer starts can't be built through clio**: designer step for the SE.
- **Versions can't be deleted**; roll back by activating the earlier one.
- **ScriptTask = compile** (on 10.x `compile-creatio process-name=…` once per process, never `compile-package`). Labs
  avoid ScriptTasks; on a real build a compile needs the SC's OK.
- **Status-change emails and tasks belong in the DCM**, not a process.
