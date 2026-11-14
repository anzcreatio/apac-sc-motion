# B4. Change what's already there: extend CRM pages safely

**Track 1 · 60 min · your development environment · Uses:** the toolkit (targeted changes) and UI guidelines

## Why it matters

Much of your work won't be new apps. It'll be changes to the CRM you already use: a field on the account page, a
list of a client's inspections, a rule that highlights an expired licence. Done right, these changes sit in **your
own package, on top of** the product, so a Creatio update doesn't wipe them and you can remove them cleanly.

## Lab (practice scenario)

1. **A small change, no plan needed:** ask Claude "On the Account page, add Number of sites and Inspection frequency
   next to the industry field." It's a targeted change, so it goes straight to building, but it should still tell
   you which page and which package it will change.
2. **Show related records:** "On the Account page, add a tab with this client's inspections." Check it in the browser.
3. **A rule on a product page:** "On the Contact page, show Licence expiry only when Is inspector is ticked."
4. **Ask where each change lives:** which page and which package. It must be your package, layered on the
   product's page, not an edit of the product's own page.
5. **Undo one change** with Claude: remove the tab, then put it back. Notice how easy that is when changes live in
   your package.

## Check

- [ ] Both Account page changes and the Contact rule work in the browser.
- [ ] Claude confirms every change is in your package, on top of the product page.
- [ ] You removed and restored one change.

## Watch out for

- **Editing the product's page directly** (in a package you don't own) causes errors and is lost on updates. Always
  your own package.
- **The page you changed may not be the one users see:** some products open different pages per record type. Ask
  Claude to check which page actually opens.
- **Hiding a product field and adding your own copy** creates two sources of truth. Reuse the product's field.

## For the facilitator

- Use pages that exist in their product (Sales, Service and FinServ differ). Adjust steps 1-3 to their product.
