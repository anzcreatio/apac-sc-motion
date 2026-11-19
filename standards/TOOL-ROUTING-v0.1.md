# Tool routing v0.1: which tool for which Creatio job

Agreed with Renzo 19 Nov 2026. Loaded into every session by the plugin's SessionStart hook, so the right guidance is
used in ad-hoc chats too, not only in builds that read `BUILD-RULES`. Before you touch any of these, load what the
"Use first" column names. Builds still follow `BUILD-RULES` (newest version) in full.

| Job | Use first | Then |
|---|---|---|
| **Custom component** (Angular remote module, view element, settings panel) | `UI-KIT-STANDARD` (newest) + R&D's `creatio-instructions-mcp`: `resolve_creatio_instructions` once, then `get_instructions_batch` for `freedom-ui/view-element.md`, Angular, TypeScript, styles | Tell the build "Read AI_GUIDES from @creatio libraries"; one prompt for the component, one for Designer registration (`BUILD-RULES` §6) |
| **Handler, converter, validator, page-body edit, C#** | R&D's `creatio-instructions-mcp` (client-unit schemas, `freedom-ui/handlers.md`, composable-app guide); follow its "Traps verified on a stand" | `BUILD-RULES` §6 (handlers `next` + `scopes`, source-only C#) |
| **Mobile page** | R&D's `creatio-mobile-page-conversion` skill (AI app development toolkit), plan first | `BUILD-RULES` §7 (check before publishing; no custom components on mobile; offline rules) |
| **Pages, processes, data, dashboards, AI skills, AI Studio through clio** | Demo toolkit (`creatio-demo-toolkit`) | `BUILD-RULES` |
| **Naming objects, columns, lookups** | R&D's `creatio-schema-naming` skill | NCD naming in `BUILD-RULES` §6; our demo prefix counts as the package convention |

R&D's instruction server needs the Creatio VPN. Off VPN it fails to connect: say so in one line and carry on with the
toolkit and our standards. If the AI app development toolkit isn't installed, say so and point the SC to `sc-setup`.

## Changes

| Version | Date | Change |
|---|---|---|
| v0.1 | 19 Nov 2026 | First version: custom components, pro-code, mobile, clio work, naming (Renzo) |
