# Chat format v0.2: replies the SC can scan

Agreed with Renzo 18 Nov 2026 (mock-up A approved). Loaded into every chat by the plugin's SessionStart hook, so it
applies to plain chats as well as skill runs. Customer-facing content (decks, emails, documents) follows
`WRITING-STYLE-v0.1.md` instead: no emoji there.

## 1. Reply order (every reply that isn't a one-liner)

| Order | Block | Rule |
|---|---|---|
| 1 | `## ❓ Questions for you` | Always first. Numbered. Each question ends with **my default** so a one-word answer works. None → write "No questions" (one line, no heading needed) |
| 2 | `## ⚠️ Watch out` | Only for a real risk or blocker (deadline at risk, something broken, a rule about to be broken). Usually absent, so it gets noticed when it appears |
| 3 | `## ✅ Done` / `📄 Files` | What changed, as a table with file links |
| 4 | Detail | Tables and short numbered steps. No paragraph longer than 3 lines |

Put `---` between blocks 1, 2 and 3.

## 2. Marks: seven, one meaning each, never decorative

| Mark | Meaning | Only in |
|---|---|---|
| ❓ | Needs the SC's answer | Questions heading |
| ⚠️ | Risk, blocker, overdue, stale | Watch-out heading, flagged table cells |
| ✅ | Done | Done heading, finished rows |
| 🟢 🟡 🔵 ⏸ | Active · Waiting on SC · Waiting on customer · Parked | Work-status cells |
| 📋 | Desk view | Desk brief / open-work heading |
| 📄 | Files produced | Files heading |
| 💡 | Learn: a rule worth keeping, with its evidence and the habit (max 2 per output, picked by impact) | Learning-loop steps only (`LEARNING-LOOP-v0.1.md` §2; v0.2, 18 Nov 2026) |

No other emoji. Never in customer-facing files.

## 3. Emphasis

- **Bold** only for a decision, an action or the one number that matters. At most about 3 per reply.
- Tables for anything with 3+ comparable items (status, options, files).
- One recommendation, not a menu. A judgement call says so.

## 4. Blocking questions use the app, not just text

When the work can't go on until the SC answers, also ask through the app's question UI (the next-step box buttons or
the question dialog) where the session has it. Formatting can't make someone read; a button they must press can.

## 5. Limits

The app renders GitHub markdown: no coloured text. Don't rely on `> [!NOTE]`-style callouts (not checked in the
app). Emoji, bold, headings, tables and `---` work on Windows and Mac.
