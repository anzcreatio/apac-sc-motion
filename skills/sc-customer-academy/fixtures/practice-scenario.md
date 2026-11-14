# Practice scenario: Kestrel Facility Services (fictional)

> A made-up company for the course labs, so everyone builds the same thing in modules B2-B5. Use your own use case
> for the capstone (B6). No real customer data anywhere in the labs.

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
