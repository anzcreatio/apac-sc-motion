# Demo library

Every demo built through this process starts the library (Renzo, 11 Nov 2026). **L1 is the minimum, within 2
working days of the demo** (demo bar item 8), done with the `sc-harvest` skill. Modules move up by reuse:

| Level | What | Reuse effort |
|---|---|---|
| L0 Pattern | An idea in `../patterns/` | Build from scratch |
| **L1 Reference** (minimum) | Package export + build log + screenshots + customer-specific list + manual steps | Copy and adapt, about half the build time |
| L2 Package | Installs cleanly with seed data and a reset; customer layer split out | Install and rebrand, 1–2 h |
| L3 Module | Generic, `lab` prefix, tested on the master stand | Install and rebrand, under 1 h |

| Where | What |
|---|---|
| `catalogue.json` (this repo) | Every module: level, what it does, pains, patterns, packages, manual steps, customer-specific list |
| SharePoint `Library/<module-id>/` | Package exports, README with install steps, screenshots |

**Master stands** (`stands.json`, demo bar §6c): neutral stands that grow deal by deal. When a new deal's use cases
are complementary we build on top (a new `lab<Module>` package, one customer layer at a time, taken off after the
demo), so each master becomes one coherent solution with many journeys. First master: `11011710-demo`
(cross-industry; H&G's customer layer comes off first). Off limits: `11013904-demo`. **Owner:** Renzo, moving to the
SE pool later.

Builds are shaped for reuse from the first click: demo bar §6b (own packages, module and customer layers, neutral
schema names, seed data in the package, manual steps written down).
