# Chat tracking v0.1: one row per chat, the desk shows what's open

Agreed with Renzo 18 Nov 2026 (mock-up B approved, with a Due column). Moved into the plugin from Renzo's own
`CLAUDE.md` (16 Nov rule) so every SC gets it. Loaded into every chat by the SessionStart hook.

**Track deals, not chats.** The record is `<deal>/00-chats.md` (shared, one row per chat, works across machines and
SCs). There is no master chat: `sc-desk` shows open work in the 8 am brief and whenever the SC asks "what's running?".

## 1. When a chat is about a customer

As soon as the first message names an account, or a deal skill runs on it (not motion/plugin work, not scheduled
tasks, not `Deals/_practice/`):

1. **Take a number:** `python <plugin>/skills/sc-desk/scripts/desk.py chat-open --deal <deal> --stage <Stage> --topic "<2-4 words>"`.
   It creates `00-chats.md` if missing (asks for the short name only if it can't tell), writes the row at once
   (status 🟢 Active) and prints the number and title. Never number from the sidebar.
2. **Sidebar** (if the session has the sidebar tools): `list_sections`; if the customer has none, `create_section`
   `<Customer full name> (<SHORT>)` (or just the name), then `move_sessions` self. Never a near-duplicate.
3. **Title:** `set_session_title` self → `<Customer> NN · <Stage> · <topic>`, under ~50 characters.

Stages: `Intake`, `FM prep`, `Meeting review`, `Demo plan`, `Build`, `Deck`, `RFP`, `Workshop`, `Click path`,
`Sizing`, `Proposal`, `Admin`.

## 2. Keep the row current

At every wrap-up (and whenever the status changes):

`desk.py chat-set --deal <deal> --no NN --status <active|waiting-sc|waiting-customer|done|parked> --next "<next step>" [--due yyyy-mm-dd] [--outcome "<one line>"] [--topic "..."]`

- **Next** is one short action ("Approve build plan"). **Due** only when someone gave a date; otherwise leave it out
  and the desk shows "unknown". Never invent a date.
- **Waiting on SC** = the SC must act (approve, answer, send). **Waiting on customer** = the customer or AE owes
  something.
- Status **done** → mark the chat completed in the sidebar (`mark_completed`) if the session has it.

## 3. Seeing it

`desk.py work` (or "what's running?" in any chat) → the 📋 Open work table: Deal · # · Stage · Status · Next ·
Due · Age, sorted by due date, ⚠️ on overdue rows and on anything waiting on the SC for more than 3 days. The daily
brief includes the same table. Private per SC like the rest of the desk (lead sees all).
