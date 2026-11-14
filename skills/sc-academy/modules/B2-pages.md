# B2. Freedom UI pages

**Path P1 · 75 min · lab stand · Skills:** `creatio-freedom-pages`, `creatio-golden-pages`, `creatio-ui-guidelines` (app-dev toolkit)

## Why it matters

Pages are what the customer sees for 90% of a demo. "Mature, competition-beating, clean" is our bar (Renzo), and the
toolkit gets there by **cloning audited donor pages**, never by composing from an empty template, and by auditing
every save. Here you learn the clone-then-adapt flow, the audits that gate "done", and how to check a page yourself.

## Lab (scope: `fixtures/kestrel-lab-scope.md` → Pages)

1. **Find the active pages** for Job and Site (`list-pages`), and their package. Anything not in your lab package is
   off limits; on a real deal you'd make a replacing copy in your own package.
2. **Pick the donor:** Claude runs `creatio-golden-pages`' `pick_donor.py` for a **request** form on Job. Read the
   replace map with Claude: which donor elements stay, which fields map to Job's.
3. **Clone the Job form page** with Claude: header with Status, Description, SLA due, Client update; labels above fields,
   placeholders on every input. Save.
4. **Run the gates** the skill names after every save (golden standard audit, page-fields audit, the visual check).
   Fix until they exit 0. Then open the page in the browser yourself (you sign in).
5. **Site → mini page** (≤ 6 user fields → mini page by default). Job list page: quick filter on Status.
6. **Review against `creatio-ui-guidelines`:** gaps, empty areas, label wording, contrast. Change one thing the review
   finds.
7. Add the pages to `lab-log.md`.

## Check (pass criteria)

- [ ] Job form, Job list and Site mini page exist, all with `designPackageName` = your lab package.
- [ ] The golden-standard and page-field audits exit 0 on the Job form (or each waiver has a written reason).
- [ ] In the browser: labels above fields, no empty tab or blank area, the Status quick filter works.
- [ ] The SC can explain why we clone donors and never edit a page in another package.

## Traps

- **Editing a page in another package** raises "Cyclic dependencies detected" on save: the most expensive mistake to
  undo. Replacing copy in your own package first.
- **`update-page` returning success isn't done.** Done = audits pass and you've seen it on screen.
- **Browsers cache old pages and chunks**: hard refresh first; after a UI deploy, use a private window before a demo.
  Refresh before asking for any compile (BUILD-RULES §1).
- **List `dependencies` in a DIFF body** go inside the root merge op; a separate merge is silently dropped and the
  expanded list shows all records.
- **A custom quick filter** must repeat the chip config inside `_filterOptions.expose[].converters[].args[0].config`,
  or the whole list breaks at runtime.
