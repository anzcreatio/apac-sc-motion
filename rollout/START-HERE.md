# Start here: the APAC SC motion in Claude

You don't need to read anything else. Claude sets you up and then guides you step by step. Works on **Windows and Mac**.
For the why and the flow, flick through `APAC-SC-Motion-Overview.pptx` in this folder (9 slides, 5 minutes).

## 1. Before you start (2 minutes)

- **The SharePoint folder on your computer.** If you can see this file in File Explorer (Windows) or Finder (Mac), you're
  done. If you're reading it in the browser: open the site → Documents → **Add shortcut to OneDrive** (or **Sync**),
  then wait until `APAC Solution Consulting - Documents` appears in File Explorer or Finder.
- **Python 3.** Windows: install from python.org and tick **Add python.exe to PATH**. Mac: install from python.org.
  Not sure? Skip it: Claude checks during setup and tells you what to do.
- **Claude.** Open the **Claude desktop app → Code tab** and start a new session in any folder, for example Documents.

## 2. Paste this into Claude

```
Please set me up for the Creatio APAC SC motion. I'm an SC on the APAC team.
1. Work out whether I'm on Windows or a Mac.
2. Find my synced SharePoint folder "APAC Solution Consulting - Documents" (it contains Deals and Plugin).
   Windows: look under C:\Users\<me>\OneDrive - Creatio\ and C:\Users\<me>\Creatio\
   Mac: look under ~/Library/CloudStorage/OneDrive-Creatio/ and ~/Library/CloudStorage/OneDrive-SharedLibraries-Creatio/
   If it isn't there, search one level down in my OneDrive folders. The plugin is in <that folder>/Plugin/apac-sc-motion.
3. Install the plugin. First check whether `claude --version` works in your shell.
   If it does, run:
     claude plugin marketplace add "<full path to Plugin/apac-sc-motion>"
     claude plugin install apac-sc-motion@apac-sc
   If it doesn't, give me these two lines to type into this chat box myself, one at a time, with the real path filled in
   (for the second one I choose "user" scope in the panel that opens):
     /plugin marketplace add "<full path to Plugin/apac-sc-motion>"
     /plugin install apac-sc-motion@apac-sc
4. Check it worked, then tell me to start a new session (or type /reload-plugins) and say "start the sc-guide".
Don't change any system settings, and ask me before installing anything else.
```

## 3. Then say

```
start the sc-guide
```

Claude takes you through eight short steps (about two hours; stop and continue whenever you like, it remembers where
you got to): setup checks on your computer, the motion, a real deal end to end, a practice first meeting, a practice
demo plan, the rules, how feedback works, and your first real deal.

## After onboarding

| You want to… | Say to Claude |
|---|---|
| Know what to do next on a deal | "what's next on <account>" |
| Continue onboarding | "where was I" |
| Report something that didn't work, or an idea | "feedback: <what happened>" |
| Get the latest version when Renzo announces one | "update the apac-sc-motion plugin" |

**Don't edit files in this `Plugin` folder.** Every new version overwrites them; send ideas through "feedback: …".
Questions: ask Renzo.
