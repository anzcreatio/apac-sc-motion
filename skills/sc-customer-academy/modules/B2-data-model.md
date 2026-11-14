# B2. Extend your CRM data: objects, fields and lookups

**Track 1 · 75 min · your development environment · Uses:** the toolkit's schema naming and data modelling

## Why it matters

Your CRM already holds clients, contacts, opportunities and cases. Most new apps should **build on those**, not copy
them: add the fields you need to the existing objects, add lookups for choices, and create new objects only for
things that don't exist yet. Good names and the right reuse now save painful clean-ups later, because pages,
processes, reports and integrations all point at the data model.

## Lab (practice scenario)

1. **Where will this live?** Ask Claude which package your changes will go into. It must be **your own** writable
   package, not a locked installed package.
2. **Reuse first:** ask Claude to look at Account and Contact and tell you which scenario fields already exist and
   which are new ("Number of sites", "Inspection frequency" on Account; "Is inspector", "Licence expiry" on Contact).
3. **Names:** ask Claude to propose names and titles for the new fields and objects, using the toolkit's naming
   rules. Check them: titles a colleague would understand, codes without spaces.
4. **Lookups first:** create the Inspection status, Overall result and Severity lookups with their values.
5. **Extend the CRM objects:** add the new fields to Account and Contact.
6. **New objects:** Site, Inspection and Finding, linked as in the scenario.
7. **Read it back:** ask Claude to show each object's fields, types and links as they now are in Creatio.

## Check

- [ ] Account and Contact have the new fields; no second "client" or "person" object was created.
- [ ] The three lookups hold the scenario's values.
- [ ] Site, Inspection and Finding exist with the right links.
- [ ] Everything is in your own package (ask Claude to confirm the package for each change).

## Watch out for

- **Locked packages:** installed-app packages are often read-only. Changes go into a writable package of your own.
- **A new field that duplicates an existing one** (a second "Status"): reuse the existing one.
- **Deleting objects or fields can't be undone** and can break pages and reports. Claude will ask first; say no
  unless you're sure, and never in an environment other people use.

## For the facilitator

- If several participants share one environment, agree a package per person before the lab.
- Keep an eye on which package each change lands in; it matters in D1-D2.
