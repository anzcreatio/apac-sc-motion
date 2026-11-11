# Industry Pack template v0.1

Every pack (Core, BFSI, Manufacturing, and any later sub-segment) uses **exactly this structure**, so W1 can read any
pack the same way and an SC can maintain one without training.

**Inheritance:** Core = General industry. BFSI and Manufacturing are **overlays**: they list only what differs from or
adds to the Core (their own pains, terms, regulation, KPIs, journeys). Anything not overridden is inherited from Core.

**Owner:** one SC per pack. **Harvest:** after every deal, the owner adds what was confirmed (a new pain, a real KPI,
a term) and marks hypotheses that missed. **Version** the file when it changes materially.

**Minimum viable pack:** §2 with 8+ hypotheses · §3 with 3 journeys · §4 with ~10 KPIs · §5 · §8 · §9 with 5+ AI tasks.

---

## 0. Pack header
| Field | Value |
|---|---|
| Pack | (Core / BFSI / Manufacturing / sub-segment) |
| Inherits from | (Core, or n/a) |
| Owner (SC) | |
| Version / date | |
| Segments covered | (e.g. "retail + business banking, lending; not insurance") |
| Deals harvested | (list of deals whose findings are in this pack) |

## 1. Top pains and consequences
| ID | Pain (internal wording) | Consequence (cost, risk, customer, growth) | Typical owner | Journey |
|---|---|---|---|---|

## 2. Hypothesis library (what W1 picks from)
Each hypothesis is something the customer could say "no" to (never a truism).

| ID | Slide wording (≤12 words, an industry observation) | Track (P / A) | Usual owner | Journey / task | KPI | Differentiators | Signals that make it likely (for W1 research) | Hit / miss log |
|---|---|---|---|---|---|---|---|---|

## 3. Reference journeys (3)
Per journey: 6–9 steps in neutral terms + the likely customer terms, who does each step, the usual systems, and the
2–3 steps where it usually breaks. This is the picture shown in the "Break" block.

| Step | Neutral term | Customer terms we've heard | Who | Usual system | Typical break |
|---|---|---|---|---|---|

## 4. KPI benchmarks
| KPI | Journey | Typical range | Range question ("closer to X, Y or Z?") | Source + date | Quality (Strong / Medium / Weak / our estimate) |
|---|---|---|---|---|---|

## 5. Personas and terminology
| Persona | What they do all day | What they look at | What they'd love to stop doing |
|---|---|---|---|

**Terminology map:** neutral term → terms used in this industry (and words to avoid).

## 6. Regulation and compliance hooks
| Obligation / theme | What it means for the process | Demo hook (rule, audit, SLA) | Source |
|---|---|---|---|

## 7. Typical landscape and competitors
| System type | Common products in APAC | Stays or goes? | Integration story (D5) |
|---|---|---|---|

| Competitor | Their angle | Our counter (from the differentiator catalogue only) |
|---|---|---|

## 8. Demo modules and proof moments (design; nothing built before process sign-off)
| Module | Journeys / tasks covered | Core-set proof moments in it (D1, D3, D2/D5) | Exists today? (portfolio asset) | Build size |
|---|---|---|---|---|

## 9. AI use-case library (Track A and the AI scene in every P demo)
| ID | Task | Agent alone | Human approves | Data / systems touched | Value maths | Proof moment | Agent pattern |
|---|---|---|---|---|---|---|---|

## 10. Harvest log
| Date | Deal | What we learned | Changed in pack |
|---|---|---|---|
