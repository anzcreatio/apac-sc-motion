# Practice scenario: Kestrel Facility Services (fictional)

> A made-up company for the labs, so everyone builds the same thing. The short sessions use the mini version;
> the full course modules B2-B5 use the whole scenario. Use your own use case
> for the capstone (B6). No real customer data anywhere in the labs.

## Mini version (one-hour session and workshop)

Clients are existing **Accounts**. Each client has **Sites**. A site gets **Inspections**: date, inspector,
result (Pass, Pass with actions, Fail), notes. One rule in the workshop: Notes required when the result is Fail.
That's all.

## The company

Kestrel maintains commercial buildings (air conditioning, electrical, plumbing, fire services) for property managers,
shopping centres and offices. Its clients and their contacts are already in Creatio as **Accounts** and **Contacts**.

## What they want to build

**Site inspections.** A supervisor visits a client site, inspects it against a checklist, records what's wrong, and
any serious finding becomes a follow-up job for the dispatch team.

| Thing | In Creatio |
|---|---|
| Client | existing **Account** (extend it: "Number of sites", "Inspection frequency") |
| Site | new object: Name, Client (Account), Address, Induction required (yes/no), Access notes |
| Inspection | new object: Site, Inspector (Contact), Date, Status (Planned, In progress, Completed, Cancelled), Overall result (Pass, Pass with actions, Fail), Notes |
| Finding | new object: Inspection, Severity (Low, Medium, High, Critical), Description, Photo, Follow-up needed (yes/no) |
| Contact | existing **Contact** (extend it: "Is inspector", "Licence expiry") |

## Rules

- A **Critical** finding sets the inspection's result to **Fail**.
- An inspection can't be **Completed** without an overall result.
- Sites with "Induction required" show a warning on the inspection page.

## Practice records

3 client accounts with "(practice)" in the name, 4 sites, 6 inspections across the statuses, 8 findings. One hero
inspection: **Westfield Parramatta, Completed, Fail, one Critical finding (switchboard overheating)**.
