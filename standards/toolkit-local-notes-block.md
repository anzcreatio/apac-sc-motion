<!-- apac-sc-motion build rules v0.1 (13 Nov 2026). Added by sc-setup; full text: apac-sc-motion standards/BUILD-RULES-v0.1.md -->
## APAC SC team build rules (apac-sc-motion)

1. **Compile and restart only when really needed, and only with the SC's OK.** Pages, captions, layouts, business
   rules, lists, dashboards, data, settings, processes saved in the designer and AI prompts need a browser refresh
   (hard refresh, then clear the site cache), not a compile. Schema, C# source code, script tasks and package installs
   may need a compile; a restart only if the app requires it or a refresh doesn't show the change. Before any compile
   or restart, tell the SC what changed, why a refresh isn't enough, what goes down and for how long, and wait for a yes.
2. **When calls suddenly fail (401, 403, "unauthorised", a login page instead of JSON, or calls that worked a minute
   ago), check the OData token or session first:** refresh the login and retry once before debugging the change. Never
   type a password or open CREDENTIALS.md: if the refresh needs a sign-in, ask the SC.
<!-- end apac-sc-motion build rules -->
