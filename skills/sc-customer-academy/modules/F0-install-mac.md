# Set up Claude to build in Creatio (Mac)

Time: about 20 minutes. You'll end up with Claude Code connected to your **sandbox** (test) Creatio site through
Creatio's **AI App Development Toolkit** and **clio** (the tool Claude uses to talk to Creatio). Both are free and
public, and you keep them.

## Before you start (10 minutes, by hand)

A prompt can't install the app that reads it, and one install needs your Mac password, which you should never give
to Claude. So these steps are yours:

1. A Claude plan that includes Claude Code: **Pro, Max, Team or Enterprise** (the free plan doesn't).
2. Install the **Claude desktop app** from claude.ai/download and sign in with your own account.
3. Your own **Creatio login** for your **sandbox** (test) site, not the one your business runs on.
   **Find your site address:** open the sandbox in your browser and copy the address up to and including
   `.creatio.com` (for example `https://yourcompany-dev.creatio.com`). Leave off anything after it, such as `/0/Shell/`.
4. **Install .NET 10.** Go to https://dotnet.microsoft.com/en-us/download/dotnet/10.0, and under **SDK** download the
   **macOS Installer** for your Mac: **Arm64** for Apple chips (M1 or later), **x64** for Intel (Apple menu →
   About This Mac shows which). Open the file and click through; it asks for your Mac password in a normal pop-up.
5. In the Claude app, open the **Code** tab, choose an empty folder (for example `Documents/creatio-build`), and paste
   the prompt below as your first message. Approve the commands Claude asks to run.

## The prompt

```text
Set up this Mac for building in Creatio with Creatio's AI App Development Toolkit. Work one step at a time, tell me
in one line what each step does before you run it, and check each step worked before moving on.
If a download fails (connection reset, timeout), run the same command again before trying anything else.
Never ask for any password in chat, never run sudo, and never run a command that needs a password: give it to me to
run in my own Terminal window and wait.

1. Check whether this Mac is Apple silicon or Intel.
2. .NET: I should already have installed the .NET 10 SDK myself. Check with `dotnet --list-sdks`; if `dotnet` isn't
   found, try /usr/local/share/dotnet/dotnet --list-sdks. If there's no 10.x SDK, stop and tell me to install it from
   https://dotnet.microsoft.com/en-us/download/dotnet/10.0 (the macOS Installer for my chip), then wait.
3. clio: `dotnet tool install clio -g` (or `dotnet tool update clio -g` if it's already there).
   - Make sure the .NET tools folder is on my PATH permanently: add `export PATH="$PATH:$HOME/.dotnet/tools"` to
     ~/.zprofile (create it if missing; don't add it twice). Your own shell doesn't pick up ~/.zprofile changes by
     itself: run `source ~/.zprofile` before each later command.
   - Check it actually starts: `clio ver` (the first run can take 30 seconds).
   - If it won't start and the error names a missing framework (Microsoft.NETCore.App 10.0.0 or 8.0.0): in EVERY
     clio.runtimeconfig.json under ~/.dotnet/tools/.store/clio/, set "runtimeOptions": { "rollForward":
     "LatestMajor" }, keeping everything else, and check again. Don't use the DOTNET_ROLL_FORWARD environment
     variable instead: it works in a terminal but not when Claude starts clio. A clio update overwrites these files,
     so redo the fix after any update.
   - Don't run any other clio command yet (registering comes later, and I do it myself).
4. The toolkit plugin. Find the `claude` command: first on PATH; if it's not there, look for the copy bundled with
   the desktop app under ~/Library/Application Support/Claude/claude-code/ (the newest version folder, inside
   claude.app/Contents/MacOS/claude). Then run:
   claude plugin marketplace add https://github.com/Creatio-Platform/creatio-ai-app-development-toolkit.git
   claude plugin install creatio-ai-app-development-toolkit@creatio
   If you can't find `claude` at all, tell me to type these two lines myself in this chat instead:
   /plugin marketplace add https://github.com/Creatio-Platform/creatio-ai-app-development-toolkit.git
   /plugin install creatio-ai-app-development-toolkit@creatio
5. Ask me for my sandbox site address (ending in .creatio.com, nothing after it). Check with me that it's a sandbox
   or test site, never the live one my business runs on.
   Connecting to Creatio needs my Creatio password, so I do it myself. Give me these two commands to run in my own
   Terminal window (Applications → Utilities → Terminal, not this chat), with my site address filled in and my login
   and password left for me to fill in. Tell me to keep the single quotes around the password:
   clio reg-web-app sandbox -u <my-site-address> -l <my-login> -p '<my-password>' -a
   clio ping-app -e sandbox
   Then wait until I tell you what ping-app said.
6. Give me a short table: what was installed, the version of each, and anything that didn't work. Then tell me to
   quit the Claude app completely (Cmd+Q), open it again, open this same folder and paste the check prompt.
```

## Connect to Creatio (you, not Claude)

Claude gives you the two `clio …` commands. Open **your own** Terminal window (not the Claude chat, and not a window
Claude opened), paste the first one, replace `<my-login>` and `<my-password>` with your Creatio login (keep the
single quotes around the password), and press Enter. Then run the second one and tell Claude what it said.

- Your password stays on your computer. Never type it into Claude.
- Use the site address only, without `/0/Shell/`.
- If Terminal says `clio: command not found`, close Terminal, open a new window and try again.

## After the restart: the check prompt

```text
Which Creatio sites can you see through the clio tools? List the apps on sandbox. Don't change anything.
If you can't see sandbox, run `source ~/.zprofile` and then `clio ping-app -e sandbox`, and tell me what it says.
Never show the contents of clio's settings file (it holds my password).
If the toolkit asks whether it may send usage data to Creatio, ask me; it's my choice.
```

You should see **sandbox** and a list of apps. If not, send a screenshot to your Creatio contact.

## What this covers (and what it doesn't)

- **Covers Business Studio:** Claude builds and changes apps, pages, objects and branding in your Creatio site,
  through Creatio's AI App Development Toolkit.
- **Doesn't cover AI Studio:** AI Studio agents are set up in AI Studio itself. This toolkit doesn't build them.

## House rules for building

1. **Sandbox only.** Never connect Claude to your live Creatio site for building.
2. **Build in your own package**, not in Creatio's own packages.
3. If colleagues build on the same site, don't edit the same page or object at the same time. The last save wins.
4. Claude asks before it changes things. Read its plan, and say no when you're not sure.
5. Start by describing the app in plain words, for example "Create an app to track partner onboarding requests".
   The toolkit writes a Business Plan first and builds only after you approve it.

## For the facilitator

- Nothing to fill in: Claude asks for the sandbox address and names the connection `sandbox`.
- **Not yet tested end to end on a clean Mac** (17 Nov 2026). It was tightened from real failures on an SC's Mac:
  Homebrew PATH problems (so it uses Microsoft's .NET installer, no Homebrew), `sudo` that can't run in Claude's
  shell, and a newer .NET (11) that stops clio starting (the `rollForward` fix). The first customer run: be on a
  call, and log anything that breaks as feedback (`sc-guide` mode C).
- The password rule is absolute: the customer types it in their own Terminal, never in Claude.
- Only public tools: never install `creatio-demo-toolkit` or our plugin on a customer machine.
