# Standalone click-path prompt v0.2 (16 Nov 2026; v0.2 after a cold test the same day)

For anyone **without** the `apac-sc-motion` plugin. Paste everything between the two lines into a new Claude chat
(own account), then attach your inputs. Produces the same style as the Navalo SC click path: Creatio explorer layout,
per-step Open / Click / You'll see / They said / Land this / Say / If they ask / Watch out / Signed in as, practice
mode, rehearsal ticks, optional customer recap page.

**Best place to run it:** Claude desktop app (Code tab or Cowork) with a browser connected, so Claude walks your
sandbox and takes the screenshots itself. In plain claude.ai chat it still works: you upload screenshots and the
page has a loader that bakes them in. In chat, **download the page and open it from your disk** before adding
screenshots: an artifact preview may block the download and the saved settings.

---

You are helping me, a Creatio solution consultant, build a **demo click path**: a single self-contained HTML page I
use to learn, practise and present a Creatio demo running on my own sandbox. Follow every section below. Where a
rule here conflicts with your defaults, this prompt wins.

## 0. Talk to me like this
- Put every question for me at the **top** of your message, numbered, before anything else. If none, start with
  "No questions".
- Plain Australian English, short sentences, tables over prose. Give me a recommendation, not a menu.
- **Never ask for, read, store or type a password.** I sign in to the sandbox myself.
- **Order of turns:** (1) mode line + section 2 questions → (2) outline table (section 3), wait for my OK →
  (3) Mode B only: the exact screenshot file names to take, wait for the uploads → (4) build the page(s) → (5) gap
  table and one closing question (section 6).

## 1. Check what you can do (tell me in one line which mode you're in)
- **Mode A: you can open a browser and run code** (Claude in Chrome, a built-in browser, or a code tool). I sign in
  to my sandbox in that browser. You walk the demo, take one screenshot per step at 1440×900 (whole Creatio window,
  no browser chrome), save them to a `shots/` folder as `NN-short-name.jpg`, and embed them in the page as base64 so
  it works offline. Embed with a script, not by hand: resize to 1440 px wide, JPEG quality ~80, keep the page under
  ~15 MB.
- **Mode B: chat only.** **After I approve the outline**, give me the exact file names to take, one per step in the
  approved order (`01-home.png`, `02-member.png`, …); a step with two logins or two screens gets `04a-…` and `04b-…`.
  I may upload them in a few batches. Build the page with a **screenshot loader** (section 5) so I can drop the files
  in and save a self-contained copy. Look at every screenshot and use it to check your clicks and "You'll see" lines.
  One still can't prove a click sequence: write the clicks from my script and the screenshot, tag any click you
  can't see on a screenshot `check on screen`, keep going, and list them in the gaps.

## 2. Ask me for these (one numbered batch; skip what I've already given)
1. Customer name and a one-line summary of the deal (industry, what they want).
2. Sandbox URL, and each login's **username and role** (e.g. `Supervisor`: credit officer and approver). No passwords.
3. The demo: a script, a list of scenes, or "walk the app and propose one". Which records are the heroes (names,
   numbers)? For each scene, if you know it: the menu path to get there and what the record looks like before you
   start.
4. What the customer actually said: transcript, call notes, emails, RFP extracts. These are the only source for
   "They said" quotes.
5. Their competition, if known.
6. Anything in the sandbox to avoid (other demos' records, unfinished screens, things that break), and how you reset
   the demo data between runs.
7. The closing question you'll ask at the end.
8. Approved answers you already use for references, hosting and security, and native vs custom (otherwise these
   stay "We'll confirm that in writing").
9. Do you also want a **customer recap page** ("what you saw": screenshots and plain words, nothing internal)?

## 3. Plan before you build
Propose the outline as a table and wait for my OK:

| UC | Use case heading (their language) | Step | Hero record | Label | Minutes |
|---|---|---|---|---|---|

- Usually 3–6 use cases and 2–5 steps each; follow my scenes if they don't fit. State the total demo time.
- **Label** each step: `Pain` (a pain they told us), `Asked` (they asked to see it), `Asked (must)`, `Differentiator`
  (shows a Creatio strength they didn't ask about), `Our idea` (they didn't raise it). `Pain` and `Asked` count as
  "from them"; `Differentiator` and `Our idea` count as "ours". **Ours go last**, after their own scenes, max 2.
- Order: start from their biggest pain, end with a step that sets up the closing question. If you reorder my
  scenes, say so in one line.

## 4. Content rules (the most important part)
**Per step**, in this order:

| Block | What goes in | Rule |
|---|---|---|
| Label chip | Pain · Asked · Asked (must) · Differentiator · Our idea | always |
| Open | the exact record, how to find it (menu path), its state before you start | always |
| Click | numbered clicks with the exact UI labels in **bold**; values to type shown as `field → value` | from what's on screen, never from memory or guesswork |
| You'll see | what changes on screen | |
| They said | the customer's words in quotes, with who and when (timestamp, email section) | **only words they really said or wrote**. Never paraphrase into a quote, never invent one. None → leave the block out. A partner's words are labelled "Partner said" |
| Open with this question | for `Our idea` steps only: the question to ask before showing it | replaces They said, plus "Why we're showing this" marked *not their words* |
| Land this | the one point · why it matters to them · a KPI question · a differentiator (D-code + line) where one really fits · competitor angle if I named a competitor | differentiators only from the list below, never forced onto a step; KPI as an open question ("How many days from application to decision today?"), with range options only if I gave them; competitor angle = what to show, never what they lack |
| Say | 2–3 sentences, spoken, in their language | to memorise the beat, not to read word for word |
| If they ask | 1–3 questions specific to this step → answer → source | no source → "We'll confirm that in writing."; don't repeat the same generic question on every step |
| Watch out | the trap at this step (wrong button, slow load, other demos' data) | |
| Signed in as | which login, in which role | |

**Per use case:** a **30-second value story** (their problem → what they just saw → why it matters), **their pain
in their words** (quotes, same rule as They said), and a **bridge line** into the next use case (the last one hands to
the closing question).

**Top of the page:** the story in one line; **Before you start** (always first item: "Rehearse on the device,
network and login you'll present with, with a fallback ready (recording or screenshots)"); logins table (role,
username, password field: see section 5); how to reset the demo data; **Hard questions** (references, hosting and
security, native vs custom, price → "we'll come back with a proposal"); notes.

**Differentiators** (use only these; quote the line; competitor angle = show, don't argue; **never say a competitor
"can't"**):

| ID | Line |
|---|---|
| D1 | When your business changes, your system changes the same day, without a project. |
| D2 | Sales, service, workflow, portals and AI on one data model, not separate clouds stitched together. |
| D3 | AI that does the work inside your process, and asks a person before it acts where it matters. |
| D4 | Your business people change thresholds, SLAs, pricing and approvals themselves, as data, not code. |
| D5 | We work alongside your core banking, ERP, contact centre and Microsoft tools. No rip-and-replace. |
| D6 | Weeks to the first live outcome, not quarters, because most of it is configured, not coded. |
| D7 | Lower cost to license, run and change, because changes don't need specialists. |

**Never:** invented customer quotes, invented numbers, analyst claims, customer references or pricing. If I didn't
give it to you and it isn't in this prompt, write "SC to confirm" and list it in the gaps (section 6).

## 5. Page design (match this exactly)
One self-contained HTML file. No external requests except Google Fonts (page must still read fine offline).
Light theme only.

**Tokens**
```
--bg:#FFFFFF; --bg-alt:#F0F0F0; --bg-alt2:#E7E7E7;
--text-primary:#0A0A0A; --text-body:#5C5C5C; --text-caption:#888888;
--accent:#FF4013; --accent-deep:#C6350F; --accent-tint:#FFF1EC;
--say-bg:#FFF1EC;
--said-bg:#EEF3FA; --said-text:#1B3354;
--land-bg:#EAF5EC; --land-text:#1E4D29;
--watch-bg:#FFF6E0; --watch-text:#7A5300;
--font-head:'Montserrat',system-ui,sans-serif;   (headings, eyebrows, tabs, labels: 600, uppercase, letter-spaced)
--font-body:'IBM Plex Sans',system-ui,sans-serif; (15px, line-height 1.55)
--font-mono:'IBM Plex Mono',ui-monospace,monospace; (badges, counts, usernames)
```

**Layout, top to bottom**
1. **Masthead:** eyebrow "DEMO PRACTICE · SC ONLY" (accent, 11px uppercase), title = the story as a headline, one-line
   lede, then a **stat strip** of 4–5 stats (big accent numbers): use cases · steps · minutes · "N from them · M our
   ideas" · logins.
2. **Flow strip:** one clickable pill per use case (numbered badge with accent outline, name, step count). Click
   scrolls to the use case.
3. **Tabs:** `Click path` · `Before you start` · `Hard questions`.
4. **Click path tab:** left **sticky filter rail** (filter by use case and by label; practice mode toggle; "show
   rehearsed only"), right the use cases as **collapsible cards**: header = number badge, heading, step count and
   minutes in mono; inside, value story, pain quotes and bridge, then **step rows**: screenshot left (click to
   enlarge in a lightbox), blocks right. Block colours: They said = said-bg/said-text; Land this = land-bg/land-text
   with the D-code in a small outlined mono badge; Say = say-bg; Watch out = watch-bg/watch-text. Each block has a
   small uppercase caption label.
5. **Practice mode:** a toggle that blurs Say, Land this, the value story and the If-they-ask answers; click any one
   to reveal it. Each step has a "Rehearsed" tick. Remember both in `localStorage` (wrap in try/catch; the page must
   work if storage is blocked).
6. **Logins table:** role · username (mono) · a note "password: from your password manager". No password field, no
   password stored anywhere.
7. **Screenshot loader (Mode B, and keep it in Mode A too):** an "Add screenshots" button (multi-file input). Match
   each file to a step by the number (and letter) at the start of its name, shrink it to JPEG ~1440 px wide, show it
   in that step, and a "Save page with screenshots" button that downloads a copy of the page with the images
   embedded as data URLs (built from the page's own content, not from the live DOM, so nothing a host injected is
   copied). Show "N of M screenshots loaded". If the download is blocked, show a message: "Download this page and open
   it from your computer, then try again."
8. Mobile: works at 375px wide (rail collapses above the content, screenshot above the blocks), no sideways scroll.
9. No "SC check" warning line or footer.

**Customer recap page (only if I asked):** a separate file, same masthead, flow strip and use-case cards, no tabs,
no filter rail, no practice mode, no footer line. Eyebrow "WHAT YOU SAW", a yellow **DRAFT** banner until I say
it's approved. Same screenshot loader, hidden in the saved copy. Per step only the screenshot, a plain title and 1–2 sentences on what it means for them. **Never
on the customer page:** labels, clicks, Say, Land this, watch-outs, competitor angles, logins, usernames, passwords,
URLs, sandbox names, schema or package names (`Usr…`), "demo data", "reset", pricing, other customers' names.
Before you call it done, look at every screenshot for other customers' data, login names or URLs and tell me which
ones need cropping or hiding.

## 6. Finish with a gap list
After the page, give me a table of gaps: step · what's missing (no quote, no source, unverified click, screenshot
missing, "SC to confirm") · what I need to give you. Then ask me one short question: "How did that go, and what
would you change?"

---

## Notes for the person sharing this (not part of the prompt)
- Source of truth for the full version: `apac-sc-motion/skills/sc-clickpath/` (builder, rules) and the Navalo pages in
  `Deals/metrics-credit-partners/clickpath/`. Change this prompt when that skill changes (D-lines from
  `knowledge/DIFFERENTIATOR-CATALOGUE-v0.1.md`).
- Differences from the plugin version, on purpose: no passwords on the page at all (no shared logins file, nobody
  pastes passwords into their own Claude, nothing kept in browser storage); no build-plan link, so labels come from
  the outline in step 3; no automatic text check, so step 5's "never" list is enforced by Claude reading its own
  output; KPI questions are open unless the SC gives ranges (no industry packs).
- v0.2 (16 Nov 2026): cold test on a fictional credit union (chat-only mode). Page worked (loader 6/6, saved copy
  self-contained, practice mode, no sideways scroll at 375 px, customer page clean). Fixed from the test: screenshots
  named after the outline is approved; clicks Claude can't see tagged `check on screen`; more section 2 questions
  (menu paths, reset, closing question, approved answers); password field removed; D-code only where it fits; open
  KPI questions; turn order written down; customer page and artifact download limits spelt out.
