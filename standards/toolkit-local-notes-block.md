<!-- apac-sc-motion build rules v0.3 (14 Nov 2026). Added by sc-setup; full text: apac-sc-motion standards/BUILD-RULES-v0.3.md -->
## APAC SC team build rules (apac-sc-motion)

1. **Compile and restart only when really needed, and only with the SC's OK (or the approval pack's).** Pages, captions, layouts, business
   rules, lists, dashboards, data, settings, processes saved in the designer and AI prompts need a browser refresh
   (hard refresh, then clear the site cache), not a compile. Schema, C# source code, script tasks and package installs
   may need a compile; a restart only if the app requires it or a refresh doesn't show the change. Before any compile
   or restart, tell the SC what changed, why a refresh isn't enough, what goes down and for how long, and wait for a yes.
2. **When calls suddenly fail (401, 403, "unauthorised", a login page instead of JSON, or calls that worked a minute
   ago), check the OData token or session first:** refresh the login and retry once before debugging the change. Never
   type a password or open CREDENTIALS.md: if the refresh needs a sign-in, ask the SC.
3. **Rollback plan first.** Before installing a custom component, deploying code (C#, script task, JS component),
   changing a standard object or a shared setting: back up (package export, page body, setting values) into the deal's
   build folder, then write in the build log how to undo it step by step, how to check it worked, and the demo's plan B
   (native screen or backup clip). Keep custom work in its own package so rollback = remove one package.
4. **Approve upfront, build non-stop.** Read `<deal>/build/approval-pack.json` before building. Within it, don't ask
   in chat: compiles for listed items, restarts on our own clean stand (max in the pack), custom code once its
   rollback is written, auto-rollback, demo data. Small choices: take the default, log it in `build/decisions.md`.
   Stop only for: out of scope (or Custom / another deal's packages), a restart on a shared stand, a sign-in the SC
   must do, deleting non-demo data, the same failure twice after a rollback, anything reaching a customer. Keep the
   laptop awake, notify at the end or a stop, and finish with a build report.
<!-- end apac-sc-motion build rules -->
