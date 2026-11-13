---
name: sc-lessons
description: Take in lessons learnt and feedback for the Creatio APAC sales motion in a chat of its own - an SC pastes anything (meeting notes, an R&D or Support email, a thought after a demo, something a customer asked that we couldn't answer) and Claude splits it into items, routes each one (commercial, functional product limitation, process, deal), writes the feedback files and updates the shared registers of product limitations and discovery questions on SharePoint. Use when an SC says "log a lesson", "lessons learnt", "R&D said", "we should have asked", "the product can't do", "feedback on the motion", or opens a chat just to record what they learnt.
---

# sc-lessons

> **Mac:** run every `python …` command below as `python3 …` (`sc-setup` records which one works in `~/.apac-sc-motion.json`).

A chat of its own for what we learn (Renzo, 13 Nov 2026). The SC pastes; you sort, file and route. It follows
`../../standards/FEEDBACK-LOOP-v0.1.md`. Team root = `sharepoint_root` in `~/.apac-sc-motion.json`.

## Steps

1. **Take it in.** If the SC hasn't pasted anything yet, ask them to paste it. Read it all, then split it into
   separate items: one lesson, one item.
2. **Sort each item** and show the SC one table before you write anything:

   | # | Item (their words, short) | Kind | Goes to | Live now or Friday? |
   |---|---|---|---|---|

   | Kind | Example | Goes to |
   |---|---|---|
   | **Commercial** | "We should have asked about database size: they have 200 million customers" | `add-question` (topic sizing / commercial) + feedback file. In 0.19.0 also the BOM gotcha register |
   | **Functional** | "Field sales can't do X; R&D confirmed" | `add-limit` (source R&D / Support / docs = confirmed; field = reported) + feedback file |
   | **Process** | "The agenda slide confused them" | Feedback file only → Friday digest |
   | **Deal** | Something about one account only | The deal folder (`<deal>/NN-notes-<date>.md`); no register |
   | **Claim** | "We can now say X", a new proof point, a customer story | Feedback file marked **for Friday**. Never straight into the catalogue or governance pack |

3. **Apply the asymmetric rule.** Items that only make us **more careful** (a limitation, a question to ask) go
   live now. Items that **expand what we claim** wait for Renzo on Friday. Say which is which in the table.
4. **Check for duplicates** first: `python scripts/registers.py list`. If an entry says the same thing, don't add
   a second one. If the new item corrects an old one, add it with `--supersedes <id>`.
5. **On the SC's yes, write:**
   - One feedback file per item, format in the standard §2, with `Source: lessons`.
   - Register entries:
     `python scripts/registers.py add-limit --area "<product or module>" --limit "<what it can't do>" --workaround "<if any>" --source "R&D" --source-ref "<who, when>" --version "<Creatio version if known>" --by "<SC name>" [--deal <account>]`
     `python scripts/registers.py add-question --topic sizing --question "<the question>" --signal "<when to ask it>" --lesson "<what happened>" --by "<SC name>" [--deal <account>]`
   - A limitation that a newer version fixes: `python scripts/registers.py close-limit --id L-004 --fixed-in 8.3.2 --by "<name>"`.
6. **Report** in five lines or fewer: what you filed, what's live now, what waits for Friday, and any item that
   needs Renzo sooner (a blocker on a live deal: suggest they message him too).

## Rules

- Keep the SC's words. Don't polish them into marketing.
- Never add a claim, a proof point or a "can say" line here. Those wait for Friday.
- No customer data beyond what the lesson needs. Record numbers in their exact unit ("200 million customers").
- Practice folders are excluded: don't log lessons from `Deals/_practice/`.

## Talking to the SC

Put every question for the SC at the **top** of your message, numbered, before any summary or detail. If there is
none, say "No questions" first. SCs often read only the top of a long reply before they approve it (Renzo, 11 Nov 2026).
