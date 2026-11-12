# Gaps and effort: Kestrel Facility Services

> `sc-workshop` with the `sc-rfp` engine, 2026-11-12. Internal. Fit-gap: `fit-gap.xlsx`. No bid / no-bid: we wrote these requirements from the workshops, so the fit % runs high and means little. What matters is below.

| Measure | Value |
|---|---|
| Requirements (ours) | 25 (25 rated; 3 voted must) |
| Met without building anything (standard, configure, AI) | 72.0% (must-haves 66.7%) |
| Must-haves needing custom, partner, roadmap or no | 0 |
| Implementation man-days beyond standard (first estimate) | 74.0 |
| Build hours for the next demo (configuration only) | 21.0 |
| Low-confidence verdicts to check | 6 |

## Gaps to handle honestly (must-haves)

| Ref | Requirement | Fit | Workaround |
|---|---|---|---|
| | None | | |

## Must-haves we're not sure of (low confidence)

A fit we can't stand behind yet is a risk as big as a gap: confirm these with Creatio product before the next session.

| Ref | Requirement | Fit | How |
|---|---|---|---|
| W1-07 | ~Technicians can see the full job, fill in the job sheet, take photos and get the client's sign-off on their phone in basements, plant room… | configure | Creatio mobile app configured for technicians (job, job sheet, photos) with offline mode and sync when back in signal. Client signature cap… |

## Where the implementation effort sits

| Ref | Requirement | Fit | Man-days |
|---|---|---|---|
| W1-16 | ~MYOB Advanced stays: completed jobs, with labour and parts, go to MYOB so finance can raise the invoice there, and cli… | integration | 15 |
| W1-01 | ~Jobs logged in the three client portals are picked up as soon as they're logged, without someone checking each portal … | integration | 10 |
| W1-20 | ~For portal clients, the invoice and the signed job sheet go into the client's portal with the job number the portal ex… | integration | 8 |
| W1-07 | ~Technicians can see the full job, fill in the job sheet, take photos and get the client's sign-off on their phone in b… | configure | 5 |
| W1-19 | ~Maybe: the supplier's invoice is read and matched to the job by the PO number or the site address (depends on accounts… | integration | 5 |
| W1-23 | ~Dispatch sees every open job, what's about to breach and where the technicians are, so a P1 about to breach is caught … | integration | 5 |
| W1-11 | ~The quote to the client (over the NTE) and the parts order to the supplier can run at the same time on the job, with t… | configure | 4 |
| W1-02 | ~Something reads the client's email, pulls out the site, the contact and what's broken, and drafts the job; the dispatc… | ai | 3 |
| W1-03 | ~The SLA due time is worked out from each client's contract, not one P1 to P4 list, and the clock pauses while the job … | configure | 2 |
| W1-05 | ~At assignment, the dispatcher can see whether the technician has the site's induction. | configure | 2 |
| W1-08 | ~Clients are told when the technician is on the way, on site and done, without ringing dispatch. | marketplace | 2 |
| W1-09 | ~Before arriving, the technician gets a summary of the site's job history: the last visits to that plant room and what … | ai | 2 |
| W1-12 | ~Every parts order is recorded against the job with its purchase order number, so the supplier's invoice can be matched… | integration | 2 |
| W1-17 | ~The invoice line description is drafted from the technician's notes and the job sheet in client-friendly wording, and … | ai | 2 |
| W1-22 | ~One job record from the client's request to the invoice, with the full set of statuses, including waiting on client, w… | configure | 2 |

## Fit by category

| Fit | Count |
|---|---|
| Configure, no code (Business Studio) | 11 |
| Integration (Creatio side supported; other system work) | 6 |
| Creatio.ai / AI Studio | 4 |
| Standard (out of the box) | 3 |
| Marketplace app | 1 |

SC check required before this is used with the customer.
