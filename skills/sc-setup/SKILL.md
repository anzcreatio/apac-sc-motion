---
name: sc-setup
description: One-time setup and health check for a Creatio APAC solution consultant using the apac-sc-motion plugin, on Windows or a Mac - finds the synced APAC Solution Consulting SharePoint folder, records it in ~/.apac-sc-motion.json, and checks Python, python-pptx, Pillow, openpyxl, python-docx, PyMuPDF (Mac), PowerPoint, the deck builder, the demo toolkit and clio. Use on a new machine, when a deck build can't find the Slide-library or Deals folder, or when the SC asks whether their setup is ready.
---

# sc-setup

Run the checks one at a time, fix what you can without changing system settings, and finish with a short table:
check · status · fix. Explain each fix in one line before you run it, and **ask before installing anything**.

## 0. Which computer

Find out from the session (platform `win32` or `darwin`), don't ask. Then use that column everywhere below.

| | Windows | Mac |
|---|---|---|
| Shell | PowerShell (or Git Bash) | Terminal (zsh) |
| Python command | `python` | `python3` |
| Home | `C:\Users\<me>` | `/Users/<me>` |

Every skill in this plugin writes commands as `python …`. **On a Mac, run them as `python3 …`.** Record which one
works in the config file (`"python"` below) so other skills can read it.

## 1. Find the team folder

The SharePoint site **APAC Solution Consulting** (library Documents) holds `Deals`, `Slide-library`, `Plugin`,
`_inbox` and `Lessons`. It's synced through OneDrive ("Add shortcut to OneDrive" or "Sync"). Look for a folder named
`APAC Solution Consulting - Documents` that contains `Deals` and `Plugin`:

| Windows | Mac |
|---|---|
| `C:\Users\<me>\OneDrive - Creatio\APAC Solution Consulting - Documents` | `~/Library/CloudStorage/OneDrive-Creatio/APAC Solution Consulting - Documents` |
| `C:\Users\<me>\Creatio\APAC Solution Consulting - Documents` | `~/Library/CloudStorage/OneDrive-SharedLibraries-Creatio/APAC Solution Consulting - Documents` |

If none matches, search one level down from the OneDrive folders (Windows: `C:\Users\<me>\OneDrive*`, `C:\Users\<me>\Creatio*`;
Mac: `~/Library/CloudStorage/*`) for a folder whose name contains "APAC Solution Consulting".

Not found → tell the SC: open the site in the browser → Documents → **Add shortcut to OneDrive** (or **Sync**), wait
a minute until it shows in File Explorer or Finder, then say "try again". Never create the folders locally: they
wouldn't sync.

Found → write `~/.apac-sc-motion.json` (Windows: `C:\Users\<me>\.apac-sc-motion.json`):

```json
{"sharepoint_root": "<full path>", "python": "python | python3", "platform": "windows | mac", "checked": "<yyyy-mm-dd>"}
```

Suggest (don't force) keeping `Deals` and `Plugin` downloaded: Windows right-click → **Always keep on this device**;
Mac right-click in Finder → **Always Keep on This Device**. Builds then don't wait for downloads.

## 2. Check the tools

| Check | Windows | Mac | Fix |
|---|---|---|---|
| Python 3.10+ | `python --version` | `python3 --version`. **Before you run it on a Mac, warn the SC:** if Python isn't installed, macOS may pop up a "Command Line Tools" install dialog: click **Cancel** | Windows: install from python.org, tick **Add python.exe to PATH**. Mac: install from **python.org only** (the Apple command-line tools' python3 is often 3.9, too old). The SC installs it; you don't. Then start a new Claude session so the new PATH is picked up |
| Python packages | `python -c "import pptx, PIL, openpyxl, docx"` | `python3 -c "import pptx, PIL, openpyxl, docx, pymupdf"` | `python -m pip install --user python-pptx pillow openpyxl python-docx` (Mac: `python3 -m pip install --user python-pptx pillow openpyxl python-docx pymupdf`). If a Mac says "externally managed environment", add `--break-system-packages` only after the SC agrees, or use a virtual environment |
| PowerPoint | Run with the PowerShell tool (not Bash, which mangles the `$` signs): `$pp = New-Object -ComObject PowerPoint.Application; $pp.Version; $pp.Quit()` | `ls "/Applications/Microsoft PowerPoint.app"` | Install Microsoft 365 desktop apps |
| Deck builder | `python <plugin root>/skills/sc-deck/scripts/build_deck.py <plugin root>/tests/deck/sample-fictional/deck.json --out <system temp>/sample.pptx --render` (full paths: the session usually isn't in the plugin folder) | the same with `python3`; the first render asks the SC to let Claude control PowerPoint and may ask PowerPoint for file access: they click **OK** / **Grant Access** | Read the error. On a Mac, if the render can't run (exit 2), the deck is still built: open the .pptx for the SC and mark rendering "look by eye" |
| Demo toolkit (for configuration) | the `creatio-demo-toolkit` skills are listed in this session | same | Install the plugin (Renzo has the instructions) |
| clio (for configuration) | the clio MCP tools are available | same | Install clio; the SC registers environments themselves |

The toolkit and clio are only needed to **configure** demos. An SC can prepare first meetings, decks, RFP fit-gaps
and workshops without them: mark them "later", not "failed".

## 3. Rules

- Never register clio environments, type passwords, create accounts or open `CREDENTIALS.md` files.
- Never change system settings (PATH, execution policy, security prompts). If one is needed, tell the SC what to do.
- Never put `node_modules`, build caches or videos in a deal folder: it syncs to every SC. Build workspaces live
  outside SharePoint: `C:\Projects\builds\<account>\` on Windows, `~/Projects/builds/<account>/` on a Mac.

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).
