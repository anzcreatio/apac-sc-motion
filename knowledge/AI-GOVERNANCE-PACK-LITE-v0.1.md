# AI governance pack "lite" v0.1: the questions banks ask, and where the answers stand

> **Internal.** Not for customers yet. Source: Creatio Academy "Creatio.ai data privacy" + the linked architecture,
> custom LLM and permissions pages (Version 10 docs, read 3 Nov 2026). Rule: **we never write our own answers.**
> Gaps go to Creatio's security/product teams for an official answer.

| # | Question banks ask | What the public docs say | Status | Gap / who must answer |
|---|---|---|---|---|
| 1 | Which models do you use, and who hosts them? | Creatio has no LLM of its own; the default runs on Microsoft Azure; "only approved LLMs" out of the box; customers can connect their own (OpenAI, Azure OpenAI, LiteLLM-supported, local endpoints) from 8.3.2 | 🟡 Partly | The default model isn't named. Fallback models' hosting isn't described |
| 2 | **Does data stay in Australia?** | The public docs say the LLM is hosted on Azure "in the same region" as the Creatio site. **Internal (Renzo, 3 Nov):** Creatio can host the LLM in any location where its cloud model provider has a region, which includes **Australia (Sydney) and Indonesia (Jakarta)**. Don't name the provider to customers | 🟡 Better, not closed | Provider regions verified (Sydney; Jakarta since Sep 2025). **Still to confirm in writing:** (a) the deployment is pinned to the in-country region, not a cross-region or "global" routing profile, which can process prompts outside the country; (b) the models we demo are available in that region (Jakarta has fewer features than Sydney); (c) fallback models stay in-country; (d) whether this applies to **AI Studio** as well as Creatio.ai |
| 3 | Is our data used to train models? | No: Creatio does not train the LLM on customer data | 🟢 Covered | — |
| 4 | Retention of prompts, responses, logs | "Customer Data is not stored on external services"; processing only; files in customer-dedicated storage | 🟡 Partly | No retention periods. Azure-side retention (abuse monitoring) is only via Microsoft's doc |
| 5 | What data is sent to the model? PII masking? | Page data (structure, record ID, display column), message history, sub-agent/process context; other data fetched on demand; up to 30 list records | 🟡 Partly | **No PII masking/redaction described** |
| 6 | Does the AI respect user permissions? | "Least-privileged RBAC"; execution rights per sub-agent/agent by role | 🟡 Partly | Not explicit that AI reads apply the user's **record-level** rights. Needs confirming |
| 7 | Human control; can AI be switched off? | Off is only indirect (remove role rights) | 🟠 Weak | No approval-before-action feature documented. **We design it in** (confirm-then-act in the process); it's not a platform guarantee |
| 8 | Audit trail of AI interactions | Nothing on the pages read | 🔴 Not covered | Need: what is logged, where, for how long |
| 9 | Certifications | SOC 1, SOC 2, ISO 27001; GDPR/HIPAA-capable; TLS 1.2+, AES-256 at rest | 🟢 Covered | Reports under NDA: who supplies them? |
| 10 | Does this cover **AI Studio** agents? | The page covers "Creatio.ai" (sub-agents, AI Agents, the command centre). AI Studio isn't named | 🔴 Not covered | **Separate answer needed for AI Studio** (Track A deals) |
| 11 | Customer-connected models (e.g. Gemini) | Allowed, but the privacy statements don't say whether they apply | 🟠 Unclear | The customer's own model = the customer's own terms. Needs to be stated |
| 12 | Prompt injection, content filtering, red-teaming | "Red-teaming" and bias checks are mentioned; nothing on injection/filtering | 🟠 Weak | Ask for the official position |

## Use in deals now
- **Safe to say (with the link: https://academy.creatio.com/guides/no-code-customization/ai-tools/creatio-ai/data-privacy):** 3, 9, and "the default model runs on Microsoft Azure in the same region as your Creatio site" (this is in Creatio's public docs, so naming Azure is fine). The "never name the provider" rule applies only to the **in-country hosting option** below.
- This pack is internal. Customer-facing text (e.g. Proposal Appendix A) may use **only** the "can say" lines.
- **Can say (internal basis, Renzo):** "We can host the AI model in-country, including Australia and Indonesia." Never name the cloud model provider.
- **Don't say yet:** "AI data never leaves Australia" (needs written confirmation of in-region routing and fallback models), "everything is logged", "the AI only sees what the user can see",
  "AI Studio is covered by this". Each is unconfirmed.
- **Design around it:** human approval and the audit trail are built into our demo processes (confirm-then-act + a log
  record), so we can *show* control even where the platform doesn't document it.

## Asks to send internally
1. In-country hosting: confirm in writing that it uses in-region routing (no cross-region/global profiles), which models are available in Sydney and Jakarta, where fallback models run, and whether it covers AI Studio (#2, #10).
2. AI interaction logging (#8).
3. Record-level rights on AI reads (#6).
4. PII handling and retention periods (#4, #5).
5. Who supplies SOC 2 / ISO reports and answers bank security questionnaires (#9).
6. In-country AI hosting for **Malaysia, Vietnam, Singapore and NZ** (only AU and ID are confirmed).
7. **APRA CPS 230** (in force 1 Jul 2025): Australian banks will likely treat Creatio and its AI provider as a material service provider. What do we provide (service provider risk pack, exit plan, incident notice)?
8. **MAS AI risk management guidelines** (issued 7 Oct 2026, effective 7 Oct 2027): the expectation that third-party AI is tested on the bank's own data. How do we support it?
9. Manufacturing: anything supporting customers who must **validate** a system that holds TGA/GMP records (don't claim "validated" or "GMP-compliant" until answered).
