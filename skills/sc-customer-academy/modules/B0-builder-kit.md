# B0. Your builder kit and ground rules

**Track 1 · 60 min · no changes to Creatio · Uses:** Claude Code, Creatio's AI App Development Toolkit, clio

## Why it matters

You'll describe what you want in plain words and Claude builds it in Creatio through the toolkit. That only works
safely when three things are in place: the tools installed, Claude connected to your **development** environment
(never production), and a few habits that keep your changes reviewable and reversible. Get them right once, here.

## Lab

1. **Install the kit** with the install guide for your computer: [Windows](F0-install-windows.md) or
   [Mac](F0-install-mac.md). You paste one prompt into Claude Code; it installs clio and the toolkit. Open Claude
   Code and check the toolkit's skills are listed.
2. **Register your development environment in clio yourself**, in your own terminal, with your own sign-in. Claude
   never needs your password; don't paste it into the chat.
3. **Ask Claude:** "Which Creatio environments can you see, and which one will you use?" It should name your
   development environment and its URL. If it names anything that could be production, stop and fix it now.
4. **Read-only first look:** ask Claude to list the applications and packages in that environment. Nothing changes.
5. **The ground rules**, in your own words (write them down; we'll come back to them): plan before build ·
   development environment only · your work goes in your own package · ask before anything you can't undo ·
   your sign-in stays yours.

## Check

- [ ] Claude names your development environment and its URL, and nothing else.
- [ ] A list of applications and packages came back (that proves the connection works, not just that clio runs).
- [ ] You can say the five ground rules without looking.

## Watch out for

- **Two environments with the same address** registered under different names: Claude will ask which one. Pick
  deliberately, and remove the one you don't use (in clio, yourself).
- **"Sign in with the default login"** offers: say no and register it yourself with your own account.
- **The connection "works" but every call fails** with a login page or a 401 error: your session expired. Sign in
  again, then retry.

## For the facilitator

- Check `plan.json` before the session; the participant's clio URL must match its environment.
- Windows + Claude desktop app: clio environments registered in a terminal can be invisible to the app until the
  clio settings file is copied into the app's packaged copy. The Windows guide's check prompt does this safely.
- If they can't install software on their laptop, solve it with their IT before the session, not during it.
