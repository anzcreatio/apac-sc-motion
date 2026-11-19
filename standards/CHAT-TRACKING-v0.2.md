# Chat tracking v0.2: one row per chat, a mark on every open chat, "end chat" closes it

Agreed with Renzo 18 Nov 2026 (mock-up B approved, with a Due column); v0.2 agreed 19 Nov 2026 (status mark in every
open chat's title). Moved into the plugin from Renzo's own `CLAUDE.md` (16 Nov rule) so every SC gets it. Loaded into
every chat by the SessionStart hook.

**Track deals, not chats.** The record is `<deal>/00-chats.md` (shared, one row per chat, works across machines and
SCs). There is no master chat: `sc-desk` shows open work in the 8 am brief and whenever the SC asks "what's running?".
**The sidebar shows what's open:** every open chat's title starts with a status mark, a closed chat has none.

## 1. When a chat is about a customer

As soon as the first message names an account, or a deal skill runs on it (not motion/plugin work, not scheduled
tasks, not `Deals/_practice/`):

1. **Take a number:** `python <plugin>/skills/sc-desk/scripts/desk.py chat-open --deal <deal> --stage <Stage> --topic "<2-4 words>"`.
   It creates `00-chats.md` if missing (asks for the short name only if it can't tell), writes the row at once
   (status 🟢 Active) and prints the number and title. Never number from the sidebar.
2. **Sidebar** (if the session has the sidebar tools): `list_sections`; if the customer has none, `create_section`
   `<Customer full name> (<SHORT>)` (or just the name), then `move_sessions` self. Never a near-duplicate.
3. **Title:** `set_session_title` self → `🟢 <Customer> NN · <Stage> · <topic>`, under ~50 characters.

Stages: `Intake`, `FM prep`, `Meeting review`, `Demo plan`, `Build`, `Deck`, `RFP`, `Workshop`, `Click path`,
`Sizing`, `Ready` (readiness check before a meeting, `sc-ready`), `Proposal`, `Admin`.

## 2. The title mark: every chat, not only customer chats

Why: an open loop keeps pulling at attention until it is closed or has a clear next step (Zeigarnik; Masicampo &
Baumeister 2011). A mark that only open chats carry shows the loops at a glance, and the two marks that need someone
(🟡, 🔵) stand out because most chats don't carry them.

| Title starts with | Meaning | Set when |
|---|---|---|
| 🟢 | In progress, nothing needed from the SC right now | First reply of every new chat; wrap-up with no question for the SC |
| 🟡 | **Your move:** the SC must answer, approve or send | Wrap-up asks the SC a question or for a go-ahead |
| 🔵 | Waiting on the customer or AE | The next step is theirs |
| *(none)* | Ended or parked | "end chat" or "park this" |

1. **New chat:** in the first reply, `set_session_title` self → `🟢 <title>`. Customer chat: the §1 title. Any other
   chat: the app's title (`get_session` self) or 2-4 words naming the work.
2. **Every wrap-up:** pick the mark from the table. Rename only when the mark changes. Change only the mark, never
   the rest of a title the SC wrote. Customer chat: the mark matches the `chat-set` status (§3).
3. **Offer the close:** when the work the SC asked for looks finished, the wrap-up's question is "End this chat?"
   with an **End chat** button first. One click closes it; nobody has to remember the command.
4. **"end chat"** (also "close chat", "we're done", the End chat button): remove the mark from the title; customer
   chat → `chat-set --status done --outcome "<one line>"`; `mark_completed` if the session has it. Reply in one line.
5. **"park this":** remove the mark; customer chat → `chat-set --status parked --next "<what restarts it>"`. The desk
   still lists parked customer chats.
6. **Reopened:** the SC writes in an ended or parked chat → `🟢` again (customer chat: `chat-set --status active`).
7. **No mark** on scheduled or unattended runs (the 8 am brief, Monday tasks): nobody works in them afterwards.
8. If the app asks the SC to approve a rename, that's expected for a title they wrote. If they decline, leave it.

## 3. Keep the row current

At every wrap-up (and whenever the status changes):

`desk.py chat-set --deal <deal> --no NN --status <active|waiting-sc|waiting-customer|done|parked> --next "<next step>" [--due yyyy-mm-dd] [--outcome "<one line>"] [--topic "..."]`

- **Next** is one short action ("Approve build plan"). **Due** only when someone gave a date; otherwise leave it out
  and the desk shows "unknown". Never invent a date.
- **Waiting on SC** = the SC must act (approve, answer, send) = 🟡. **Waiting on customer** = the customer or AE owes
  something = 🔵. **Active** = 🟢.
- Status **done** → mark the chat completed in the sidebar (`mark_completed`) if the session has it.

## 4. Seeing it

`desk.py work` (or "what's running?" in any chat) → the 📋 Open work table: Deal · # · Stage · Status · Next ·
Due · Age, sorted by due date, ⚠️ on overdue rows and on anything waiting on the SC for more than 3 days. The daily
brief includes the same table. Private per SC like the rest of the desk (lead sees all).

**Still open?** The daily brief also lists chats whose title still starts with 🟢 🟡 🔵 and that nobody has touched
for more than 3 days (`list_sessions`, `lastActivityAt`), any chat, not only customer chats. For each, the SC says
end, park or keep. Remembering to close later is the step people forget; this catches what slipped.
