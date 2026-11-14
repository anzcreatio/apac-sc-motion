# B3. Build the app and its pages

**Track 1 · 90 min · your development environment · Uses:** the toolkit's app orchestrator and UI guidelines

## Why it matters

Now Claude builds from the approved plan: the app, its sections, list and record pages, and the business rules on
the pages. The toolkit follows Creatio's Freedom UI guidelines (layout, labels, accessibility) so the result looks
native. Your job is to approve the plan, check each page as a user would, and ask for changes in plain words.

## Lab (practice scenario)

1. **Approve the plan from B1.** Tell Claude the data model from B2 already exists so it reuses it. Read the plan
   once more, then say clearly "Yes, build this".
2. **Follow the build report:** sections created one by one, then pages and rules. Ask Claude to explain anything
   you don't understand.
3. **Open the app in your browser** (you sign in). Create a practice inspection for "Westfield Parramatta
   (practice)" with two findings, one of them Critical.
4. **Test the rules:** the Critical finding sets the result to Fail; Completed needs an overall result; the
   induction warning shows for that site.
5. **Ask for two page changes** in plain words, for example "put Overall result next to Status at the top" and
   "show the findings list on the inspection page". Then ask Claude to review the page against the UI guidelines.
6. **Add the practice records** from the scenario so every list has something in it.

## Check

- [ ] The app opens with Sites, Inspections and Findings sections.
- [ ] Each rule from the scenario works on the page, tested by you.
- [ ] Both page changes show after a refresh.
- [ ] The hero inspection (Westfield Parramatta, Fail, one Critical finding) exists.

## Watch out for

- **Old screen after a change:** refresh the browser (hard refresh) before asking for anything else.
- **Web and mobile are separate pages.** A change to the web page doesn't change the mobile one (that's B5).
- **Labels and captions** must be translatable texts. The toolkit does this; don't ask it to hard-code text.
- **Rules that need custom code** are flagged separately in the plan. Keep version one to standard business rules.

## For the facilitator

- Section creation can fail briefly when several builds run at once; the toolkit retries one at a time. Don't let
  participants run builds in parallel in a shared environment.
