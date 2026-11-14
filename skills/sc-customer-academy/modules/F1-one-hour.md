# Your first Creatio app in an hour

**60 minutes · your test site · you'll leave with a working app you built yourself**

You tell Claude what you need in plain words. Claude asks questions, writes a plan, and builds it in Creatio once
you say yes. Today: a small **site inspections** app for a facilities company (`practice-scenario.md`, "mini").

## The three rules (5 min)

1. **Test site only.** Never your live Creatio.
2. **Plan first.** Claude shows a plan; nothing is built until you say "yes, build it".
3. **Ask before deleting.** If Claude wants to delete something, it asks. Say no unless you're sure.

## 1. Ask for the app (15 min)

Type this:

> I want a simple site inspections app. Our clients are already in Creatio as accounts. Each client has sites.
> We inspect a site and record the date, who inspected it, and a result: Pass, Pass with actions, or Fail.

Claude asks a few questions. Answer them in a few words; if you don't know, say "keep it simple".
Then it shows a **plan** (what it will build). Check three things:

- It uses your **existing accounts**, not a new client list.
- It has **Site** and **Inspection**.
- **Result** is a dropdown with the three values.

Want something changed? Just say it ("add a Notes field"). When it looks right, type: **yes, build it**.

## 2. Watch it build, then try it (20 min)

Claude builds the app and tells you when it's done. Then:

1. Open your test Creatio in the browser and find the **Site inspections** app.
2. Add a site for a client, then an inspection with the result **Fail**.
3. Ask for one change, for example:

> On the inspection page, put Result at the top, next to the date.

Refresh the browser to see it.

## 3. Change your CRM (15 min)

The new app is linked to your existing clients. Make the client page show it. Type this:

> On the account page, add a tab that lists this client's inspections.

Open a client: the tab is there, with the inspection you just added. That's the point: you didn't build a separate
system, you **extended your CRM**.

## Wrap up (5 min)

- You built an app and changed your CRM by describing it. Everything you did is in **your own folder of changes**
  (a Creatio package), so your IT team can review it and move it to your live site the proper way.
- Next: the 3-hour workshop (your own idea), or keep practising with your coach (`creatio-build-coach`).

## Check (the facilitator looks with you)

- [ ] The app opens and has a site with a Fail inspection.
- [ ] Your page change shows.
- [ ] The client page has the inspections tab.

## For the facilitator

- **Rehearse the timing on their product and site before the session.** The build is the slow part; if it runs past
  10 minutes, show your own pre-built copy and let theirs finish in the background.
- Groups over 6: build in pairs, one laptop, both type.
- Keep a copy of the three prompts in the chat so anyone who falls behind can paste and catch up.
- No deletes, compiles or restarts in this session. If Claude suggests one, say "not today".
