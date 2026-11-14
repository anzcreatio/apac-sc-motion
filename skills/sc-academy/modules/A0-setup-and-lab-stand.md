# A0. Setup and your lab stand

**Path P1 · 45 min · no stand writes · Skills:** `sc-setup`, `sc-guide`

## Why it matters

Every later module assumes three things work: the SharePoint folder, the toolkits (creatio-demo-toolkit and clio),
and a stand you're allowed to break. Most lost hours on real builds were setup, not configuration: clio pointing at
the wrong settings file, a plugin blocking clio, a token that expired. Fix them here, once, with nothing at stake.

## Lab

1. **Run `sc-setup`** with Claude (say "run sc-setup"). Fix what's red one item at a time. You need, for this course:
   SharePoint folder found, Python, `creatio-demo-toolkit` installed, clio answering. PowerPoint only for A1.
2. **Practice folder:** Claude runs `academy.py start`; check that `Deals/_practice/<first-name>-academy-kestrel/`
   now exists in File Explorer or Finder.
3. **Pick your lab stand.** Best: a practice stand of your own. Otherwise a stand you name that holds **no customer
   demo**. Register it in clio **yourself** (`clio reg-web-app …` in your own terminal; Claude never registers stands
   or types passwords).
4. **Claude records it:** `academy.py stand --sc "<you>" --name <env> --url <url>`. If it refuses, the stand appears in
   a real deal's notes: pick another one, or ask Renzo.
5. **Prove clio reaches it:** ask Claude to run `list-packages` on the stand (read-only). Note the stand's Creatio
   version in the About dialog (10.x or 8.x changes some commands later).
6. **Find the toolkit notes:** ask Claude where `sc-setup` wrote the build rules into your toolkit notes, and open
   `standards/BUILD-RULES-v0.4.md` §1 (compile and restart only with your OK). Read it, two minutes.

## Check (pass criteria)

- [ ] Progress file `Lessons/training/<you>.json` has a `stand` with `deal_hits` empty (or `renzo_ok`).
- [ ] `list-packages` on that stand returned a list (proves auth, not just a ping).
- [ ] The SC can say, in their own words, when a compile or restart is allowed.

## Traps (from real builds)

- **Windows, Claude desktop: clio envs registered in a terminal are invisible to Claude** until the clio
  `appsettings.json` is copied into the Claude app's packaged copy (`%LOCALAPPDATA%\Packages\Claude_…\LocalCache\
  Local\creatio\clio\`). Check both files before you blame clio. Back up first. Restart Claude after.
- **`healthcheck` passing proves nothing**; `list-packages` proves auth.
- **Plugins that fight clio:** `ai-driven-delivery-assurance-review` can block clio, `ai-driven-development-kit`
  prompts on every stand write, `ai-driven-ai-studio` duplicates the toolkit's executor. Disable them for demo work
  (you run `claude plugin disable …` yourself).
- **The toolkit sometimes suggests signing in with demo credentials.** Our rule wins: you sign in, Claude never types
  a password.
- **Calls suddenly return 401/403 or an HTML login page:** the token expired. Re-authenticate first, then debug
  (BUILD-RULES §2).
