# D3. Classic UI to Freedom UI

**Track 2 · 90 min · your development environment · Uses:** the toolkit's Classic UI expert and Classic-to-Freedom migration

## Why it matters

If you've run Creatio for a while, some of your pages and customisations are in Classic UI. New capabilities land in
Freedom UI. The toolkit can inventory every customisation on a Classic page (what it does, why, and the source that
proves it) and plan and carry out the move to Freedom UI, one page or a whole package at a time, with your approval
at each step.

## Lab (one Classic page of yours, in development)

1. **Pick one Classic page** with a few customisations (a record page with a detail and some field logic).
2. **Inventory it:** ask Claude to describe every customisation on that page. Check the list with whoever built it:
   anything missing or no longer needed?
3. **Plan the migration** for that page: the toolkit writes a migration plan (what moves, what changes, what needs
   a decision). Read it and decide each open point.
4. **Approve and migrate** that one page in development. Compare old and new side by side as a user.
5. **Decide the rest:** with Claude, list the remaining Classic pages and sort them: migrate, retire, or leave for now.

## Check

- [ ] An inventory of the page's customisations, checked by someone who knows them.
- [ ] An approved migration plan and the migrated page working in development.
- [ ] A sorted list of the remaining Classic pages.

## Watch out for

- **Migrating customisations nobody uses:** the inventory is the moment to retire them.
- **Custom code in Classic pages** may need a different approach in Freedom UI; the plan flags these. Decide them
  explicitly, don't let them be copied blindly.
- **Do a whole package only after one page has gone well.**

## For the facilitator

- Only for customers with Classic UI pages. Skip it for Freedom-only customers and spend the time on D2.
