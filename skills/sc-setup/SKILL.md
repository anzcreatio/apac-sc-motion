---
name: sc-setup
description: One-time setup and health check for a Creatio APAC solution consultant using the apac-sc-motion plugin, on Windows or a Mac - finds the synced APAC Solution Consulting SharePoint folder, records it and the SC's initials (rh, wn, fa: the suffix on new deal folders) in ~/.apac-sc-motion.json, holds the deal folder naming rule, and checks Python, python-pptx, Pillow, openpyxl, python-docx, PyMuPDF (Mac), PowerPoint, the deck builder, the demo toolkit and clio. Use on a new machine, when a deck build can't find the Slide-library or Deals folder, or when the SC asks whether their setup is ready.
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
{"sharepoint_root": "<full path>", "python": "python | python3", "platform": "windows | mac", "sc": "rh | wn | fa", "checked": "<yyyy-mm-dd>"}
```

Suggest (don't force) keeping `Deals` and `Plugin` downloaded: Windows right-click → **Always keep on this device**;
Mac right-click in Finder → **Always Keep on This Device**. Builds then don't wait for downloads.

## 1b. Who is this SC (initials)

New deal folders carry the creator's initials as a suffix (see "Deal folder rule" below). Claude can't see which
Claude account is signed in, so the initials are stored once in the config as `"sc"`:

| SC | `sc` |
|---|---|
| Renzo | `rh` |
| Willy | `wn` |
| Ferdhi | `fa` |

Suggest one from the computer login (Windows `$env:USERNAME`, Mac `whoami`; e.g. `r.huruiti` → `rh`) and **ask the SC
to confirm** it; never save a guess. A new SC not in the table: ask for two lowercase letters and tell Renzo to add
them here. Keep any other keys already in the file.

## Deal folder rule (every skill that creates a deal folder follows it)

1. Name: `<team root>/Deals/<kebab-case-account>-<sc>/`, e.g. `adira-finance-rh`. The suffix goes on the deal folder
   only, never on subfolders (`rfp/`, `workshop/`, `click*/`) or files.
2. **One folder per account.** Before creating, look in `Deals/` for the account with no suffix or any suffix
   (`<account>`, `<account>-rh`, `<account>-wn`, …). Found → use it, don't create a second one. Close match (e.g.
   `bank-mandiri` vs `mandiri`) → ask the SC.
3. No `sc` in the config → run step 1b first. Never guess the initials.
4. The suffix records who **created** the folder. Never rename it, even when the deal moves to another SC (renaming
   breaks saved paths). Folders made before 12 Nov 2026 have no suffix and stay as they are.

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

**Build rules into the toolkit (once the toolkit is installed).** The toolkit reads a local notes file for each skill
that survives its updates. Ask the SC, then add our build rules to the one for `creatio-demo-build`:
1. Get the path: `python <toolkit root>/scripts/helpers/local_notes.py path creatio-demo-build` (toolkit root =
   the newest `creatio-demo-toolkit/<version>` folder under `~/.claude/plugins/cache/`).
2. If the file doesn't already contain `apac-sc-motion build rules`, append `../../standards/toolkit-local-notes-block.md`
   to it (create the file if it's missing). If an older version of the block is there, replace just that block.
   Never change anything else in the file.

**Permission allowlist for unattended builds (ask first).** So a demo build can run without the SC approving
every command, offer to merge `../../standards/build-permissions.json` into `.claude/settings.local.json` of the
folder the SC starts build sessions in (ask which; default the folder they use for deals work). Replace `<DEALS>`
with their `Deals` path and `<BUILDS>` with their builds folder (Windows `C:/Projects/builds`, Mac
`~/Projects/builds` written out in full), forward slashes. Read the file first and merge, never overwrite; leave
out the `_what` line. Tell them it loads in the next session. Never touch the user-level settings or the permission
mode.

## 2b. Daily brief at 8 am (offer it, don't force it)

Once the team folder and initials are set, show the SC their first desk brief (`sc-desk` mode A:
`python <plugin root>/skills/sc-desk/scripts/desk.py brief --preview --no-write`), then ask: "Want this every
weekday at 8 am on this PC?" On a yes, create the scheduled task exactly as `sc-desk` "Scheduled daily brief" says
(task id `sc-desk-daily-brief`, cron `0 8 * * 1-5`, their initials in the prompt). It runs while the Claude app is
open. Optional: the Microsoft 365 connector (read-only) adds their Outlook meetings and sent follow-ups; they connect
it themselves.

## 3. Rules

- Never register clio environments, type passwords, create accounts or open `CREDENTIALS.md` files.
- Never change system settings (PATH, execution policy, security prompts). If one is needed, tell the SC what to do.
- Never put `node_modules`, build caches or videos in a deal folder: it syncs to every SC. Build workspaces live
  outside SharePoint: `C:\Projects\builds\<account>\` on Windows, `~/Projects/builds/<account>/` on a Mac.

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).
