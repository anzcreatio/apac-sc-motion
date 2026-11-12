---
name: sc-setup
description: One-time setup and health check for a Creatio APAC solution consultant using the apac-sc-motion plugin - finds the synced APAC Solution Consulting SharePoint folder, records it in ~/.apac-sc-motion.json, and checks Python, python-pptx, Pillow, openpyxl, python-docx, PowerPoint, the demo toolkit and clio. Use on a new machine, when a deck build can't find the Slide-library or Deals folder, or when the SC asks whether their setup is ready.
---

# sc-setup

Run the checks, fix what you can without changing system settings, and report a short table: check · status · fix.

## 1. Find the team folder

The SharePoint site **APAC Solution Consulting** (library Documents) holds `Deals`, `Slide-library`, `_inbox` and
`Lessons`. It is synced through OneDrive ("Add shortcut to OneDrive" or "Sync"). Look for a folder containing both
`Deals` and `Slide-library` under the user's profile, typically:

- `%USERPROFILE%\OneDrive - Creatio\APAC Solution Consulting - Documents`
- `%USERPROFILE%\Creatio\APAC Solution Consulting - Documents`

Not found → tell the SC to open the site in SharePoint → Documents → **Add shortcut to OneDrive**, wait a minute, and
run this again. Never create the folders locally: they would not sync.

Found → write `~/.apac-sc-motion.json`:

```json
{"sharepoint_root": "<full path>", "checked": "<yyyy-mm-dd>"}
```

Suggest (don't force) right-click `Deals` → **Always keep on this device**, so builds don't wait for downloads.

## 2. Check the tools

| Check | How | Fix |
|---|---|---|
| Python 3.10+ | `python --version` | SC installs Python |
| python-pptx, Pillow, openpyxl, python-docx | `python -c "import pptx, PIL, openpyxl, docx"` | `python -m pip install python-pptx pillow openpyxl python-docx` (ask first; openpyxl and python-docx are for `sc-rfp` and `sc-workshop`) |
| PowerPoint | `powershell -Command "New-Object -ComObject PowerPoint.Application \| % { $_.Version; $_.Quit() }"` | Install Office desktop |
| Deck builder | `python ../sc-deck/scripts/build_deck.py ../../tests/deck/sample-fictional/deck.json --out <temp>/sample.pptx --render` | Read the error |
| Demo toolkit (for configuration) | the `creatio-demo-toolkit` skills are listed in this session | Install the plugin |
| clio (for configuration) | the clio MCP tools are available | Install clio; the SC registers environments themselves |

## 3. Rules

- Never register clio environments, type passwords, create accounts or open `CREDENTIALS.md` files.
- Never put `node_modules`, build caches or videos in a deal folder: it syncs to every SC. Build workspaces live in
  `C:\Projects\builds\<account>\`.

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).
