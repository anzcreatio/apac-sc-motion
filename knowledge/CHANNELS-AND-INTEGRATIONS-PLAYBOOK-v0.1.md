# Channels and integrations playbook v0.1

How to configure and **show working** in a demo: (1) integrations, (2) chat channels (WhatsApp, Messenger,
Instagram, Telegram, SMS, web chat), (3) social media comments, (4) WhatsApp and SMS from a marketing campaign.

- **Source:** Creatio Academy (8.3 and version 10 pages) and Marketplace listings, read 18 Nov 2026. Every row
  names its source in §8. Toolkit field notes (creatio-demo-toolkit 4.1.1) are referenced, not repeated.
- **Evidence:** C = Academy or Marketplace says so · I = our inference · A = assumed. **Nothing here has been proven
  on one of our stands yet** (see §9). A row moves to "proven" only after a clean-stand rehearsal.
- **Versions matter more than usual here.** Academy's latest is **version 10** (10.0 / 10.1). Several answers
  differ between 8.3 and 10. Check the stand's version first (`get-app-info` or About).

---

## 0. The answer in one table: what's native, what isn't

| Need | Native? | Best demo route | Evidence |
|---|---|---|---|
| Call an external API from Creatio | ✅ Native (Web services + **Call web service** process element) | Public API, process with tracing on, record changes | C |
| External system pushes data into Creatio | ✅ Native (**Webhook service**, OData 4 + OAuth) | POST a JSON webhook → Webhooks section → new record | C |
| WhatsApp chat | ✅ Native: Twilio (8.x, 10) or **Meta Cloud API (10.1+)** | Twilio sandbox (same day). Meta direct needs verification: hours to days | C |
| Facebook Messenger chat | ✅ Native | A spare test Facebook Page | C |
| Telegram chat | ✅ Native | @BotFather bot: **the fastest real channel (minutes)** | C |
| SMS chat (two-way) | ✅ Native from **8.3.3**, Twilio only | Twilio trial number | C |
| Web chat | ✅ Native from **10.0** (Web Chat app) | "Test in preview mode": no website needed | C |
| Instagram Direct | ❌ Not native | Marketplace: Beesender (paid) | C |
| Facebook / Instagram **post comments**, mentions | ❌ Not native | Simulated Meta webhook → case (§3); live = Hootsuite (FB only) or Beesender (IG) | C (not native), I (route) |
| Google reviews | ❌ Nothing found, native or Marketplace | Simulated webhook only | C (search) |
| Facebook / Instagram / LinkedIn **lead forms** | ✅ Native (Lead Generation app) | Facebook forms section, or webhook with `EntityName: Lead` | C |
| WhatsApp / SMS **inside the campaign canvas** | ❌ Not in core (no SMS, WhatsApp or Business process element in 8.3 or 10). Creatio's **Omnichannel Marketing** app adds SMS (8.3.4+, Twilio, **Europe-only recipients**) and bulk WhatsApp | §4 route B (no code) unless the canvas element itself is the point | C |

**What to say on stage when it isn't native:** "Lead forms, Messenger, WhatsApp, Telegram and SMS are out of the box.
Comments, mentions and reviews come in through a partner app or a webhook into a case." Never claim native comments
or reviews. (Fits the differentiator catalogue's openness story; claims still only from the catalogue.)

---

## 1. Integrations: show them working

### 1a. Outbound: Web service + process (no code)

1. **Studio → Web services → New web service → REST** (or App Hub → app → Integrations tab). Paste the endpoint
   for auto setup, or fill Name, Code (`Usr` prefix), URI, retries, package. URI protocol must match Creatio's (https).
2. **Method:** address with `{placeholders}` (become parameters), type, JSON, timeout (default 5,000 ms).
   Tick **Use authentication** only if the service needs it (403 otherwise).
3. **Parameters:** magic wand "From field 'Method address'"; response via **Example in JSON** → pick fields
   (JSONPath, e.g. `$.rates.AUD`). Empty response values = wrong JSONPath.
4. **Auth:** Basic = two system settings (text + encrypted) — they **don't travel with the package**, re-enter after
   install. OAuth 2.0 = app with client ID/secret, redirect URL copied exactly. **No API-key type:** send the key as a
   Query or Header parameter.
5. **Send a test request** on the method: shows request and response (JSON or raw HTTP). Good on stage.
6. **Process:** Call web service element → service → method → map parameters → max time. Outputs: **Success**
   (status < 400), Http status code, one output per response field → Modify data / Add data. Branch on Success
   (error path to a visible "integration failed" activity, not just Terminate). Arrays need a Script task.
7. **From a page or an AI skill:** no-code route = button or AI skill action runs the process (system actions are
   processes). Calling from page code (`HttpClientService`) is code: only when Renzo agrees (OOTB first).

Academy worked example: currency rates from Fixer (timer → Read data → Call web service → Add data). Fixer needs a
free key in practice (the page contradicts itself; I). **Pick a keyless public API for a demo where possible (A).**

### 1b. Inbound: Webhook service (no code)

1. Register the target object's code in the **Webhook entities** lookup (Contact, Lead, Order, Submitted form are
   there by default).
2. Give the technical user **Creatio Webhook Service** (`WebhookService`) rights on that object. It has none.
3. URL: any section → **Data import → Web forms and pages → Other landing pages → Get the Webhook URL**. One URL per
   sending system.
4. Sender: **POST only**, `application/json` or `multipart/form-data`. Body = `EntityName` + column codes; lookups
   as `<Column>Id` + GUID. No attachments.
5. Default process "Create object records based on incoming webhooks" **polls every minute, 50 at a time** →
   allow up to ~60 s on stage. For other logic (a case, a custom object, AI triage): deactivate the default process
   (don't delete) and build your own on the webhook record.
6. Proof: Studio → **Webhooks** (chart, Total/Done/Failed tiles, row detail with parse errors).
7. On-site only: OAuth app "Webhook Account Service Identity" (`https://webhooks.creatio.com`) + IdentityServer and
   SocialAccountServiceUrl settings. Cloud: out of the box.

### 1c. External system reads/writes Creatio: OData 4 + OAuth

System Designer → Import and integration → **OAuth 2.0 integrated applications** → New → keep "separate technical
user" → copy Client Id + secret → token from `{IdentityServer}/connect/token` (client_credentials) →
`{url}/0/odata/<Entity>`. Least-privilege rights on the technical user. Max 20,000 rows per response.

### 1d. The on-stage proof sequence (I: our recommendation)

| Beat | What the audience sees | Native proof |
|---|---|---|
| 1 | Something outside sends data (Postman, a form, Make) | — |
| 2 | It lands: Studio → Webhooks, status Done | Webhooks section |
| 3 | A record appears (lead, case) | the record |
| 4 | Creatio calls out (enrichment, credit check, ERP stock) and the record updates | Call web service outputs |
| 5 | "Under the hood": Process log → Call web service → **Show trace data** (JSON in/out) | Process tracing (turn on for the demo only) |
| 6 | Failure is handled: a wrong ID → Success = false → visible task for a person | Success branch |

There is **no built-in outbound call log**. If the customer asks for an integration log, add a small custom
`Integration log` object written by the process (I; community pattern). It's a good-looking demo extra.

**Stand-in for a customer system we can't reach:** a mock API we control (A: e.g. a static JSON on a public mock
service, or our own endpoint). Name it honestly in the script: "simulating your ERP".

### 1e. Ready-made connectors worth knowing

| Connector | Note | Evidence |
|---|---|---|
| Creatio.ai add-in for Teams / Outlook | Teams app 8.3.1+, meeting summaries 8.3.3+; Entra admin consent | C |
| Zapier connector (Creatio, free) | 7.12.4+, both UIs; create/update records, start processes | C |
| Make.com connector (Experceo, free) | 8.0+ | C (snippet) |
| Power Automate | No Academy page; inbound via webhooks | C (absence) |

---

## 2. Chat channels

### 2a. Where you set them up

| Version | Menu | Who works the chats |
|---|---|---|
| 8.3 | System Designer → **Chat settings** → Channels / Queues | Communication panel (agent sets status **Active**) |
| 10 (and 8.3.4+ with the free **Customer Communication Hub** app) | **Customer Communication Hub** → Manage channels → Add channel; Chat Routing tab for queues | **Agent Inbox** (Contact Center app) |

**Before any channel** (C): permission `CanManageChats`; system settings `IdentityServerUrl`,
`IdentityServerClientId`, `IdentityServerClientSecret` filled (empty → Creatio support ticket: **ask early, it's
the slow step**); a queue with routing "To an available agent" and **the presenter in Queue agents** (toolkit:
`ChatQueueOperator`; Tauron lost a demo rehearsal to this).

### 2b. Channel recipes

| Channel | Setup (short) | Demo traps | Evidence |
|---|---|---|---|
| **Telegram** (fastest) | @BotFather `/newbot` → token → Add channel → Telegram → token, queue → Next → AI → Save | Fresh bot only (an existing webhook blocks it); one bot = one channel; token can't be changed | C |
| **WhatsApp via Twilio** | Twilio sandbox: "When a message comes in" = `https://sm-receiver.creatio.com/api/webhook/LeadGen/whatsapp` → Add channel → WhatsApp (Twilio): number, Account SID, Auth Token, queue | Sandbox join **expires after 72 h**: re-join before the demo. Turn **off** Twilio HTTP Basic Auth for media. 8.3: media **incoming only**; agent-started chats Classic UI only (10: supported). Number binds to one instance, last wins | C + toolkit `whatsapp-channel.md` |
| **WhatsApp via Meta Cloud API** (10.1+) | Meta Business portfolio + WABA + a number not on the WhatsApp app + payment method → Add channel → WhatsApp → Meta sign-in window → queue | **Not same-day:** Meta verification hours to days. Allow pop-ups | C |
| **Facebook Messenger** | Admin of a Facebook **Page** → Add channel → Messenger → log in → pick Page → queue | **One Page ↔ one Creatio instance, last wins:** use a demo-only Page or you'll steal another SC's | C |
| **SMS** (8.3.3+) | Twilio number → "A message comes in" = same `sm-receiver…` URL → Add channel → SMS: number, SID, token, queue | Twilio only; long messages billed per part; keep trial and production accounts apart | C |
| **Web chat** (10.0+) | Web Chat + Contact Center + CCH installed, `WebChatServiceUrl` set → Add channel → Web chat: logo, colour, queue, welcome → **Test in preview mode** | Preview creates **real** chats; visitor is "Unknown contact" until linked | C |
| **Instagram Direct** | Not native. Beesender Omnichannel (Marketplace, about US$1,000/month) or Beesender Chat Master | Paid; IG must be a professional account linked to a Page | C |

### 2c. AI on a channel

Channel → AI settings → "AI handles conversation first" → personality → **Enable handoff** (8.3.4+ with CCH;
FB, Telegram, WhatsApp, SMS; 10 adds web chat and "Audience rollout %"). Seed and **index** the knowledge base first.
Plain-text replies; idle AI chats close after 15 min. Everything in the toolkit's `whatsapp-channel.md` applies to
every chat channel, above all: AI user rights on side-effect objects (`Reminding`), register-then-report not
confirm-then-act, ban citation markers, rehearse the skill in the panel by also attaching it to the root agent.

### 2d. Outbound from a process: **Send chat message** (C, 8.3)

From = channel, To = recipient, template ("Chat template" in Message templates) or text. It creates a Completed chat;
a reply opens a new chat in the queue. WhatsApp 24-hour rule applies: outside 24 h only a Meta-approved template
gets through. **This element is the key to §4 route B.**

---

## 3. Social media comments, mentions, reviews

**Not native** (C). Options, best first for a demo:

| # | Route | When | Evidence |
|---|---|---|---|
| A | **Simulated Meta event (recommended stand-in):** POST a JSON shaped like a Meta `feed`/`comments` event to the Creatio webhook → own process → **Case** (category "Social comment", channel Facebook/Instagram) or a custom `Social interaction` object → link/create contact → AI skill for sentiment, urgency, suggested reply → routed owner | Any demo; only documented Creatio features; no Meta app review | I (built from C parts) |
| B | **Hootsuite connector** (Creatio, free + paid Hootsuite): comments sent from Hootsuite become cases | Live Facebook, X, YouTube; **not Instagram**; 8.3.1+, Customer 360 or Case Management | C |
| C | **Beesender Chat Master** (US$30/user/month): Instagram comments + DMs as chats → lead/case | Live Instagram; 8.3.0+ | C |
| D | **Real Meta webhooks via a relay** (Make, Zapier, Power Automate, Azure Function) → Creatio webhook | Production design. Creatio's endpoint is POST-only and can't answer Meta's GET verification, so a relay is required (I). Meta permissions: `pages_manage_metadata`, `pages_read_engagement`; Instagram adds `instagram_manage_comments`; Advanced Access = Business Verification + App Review | C (Meta docs) + I |
| E | YouScan "Social media cases" | Social listening; **Classic UI only**, 2023 | C |

Say it plainly in the demo script: route A is "how it works when your Meta page is connected"; the reply back to
Facebook is shown as a drafted reply, not posted (A).

---

## 4. WhatsApp and SMS from a marketing campaign

### 4a. Facts

- Core campaign elements (8.3 and 10): Add audience, Triggered adding, Add from event/landing/Facebook form,
  Eliminate duplicates, **Add data, Modify data**, Timer, Random split, form-submitted conditions, Exit,
  **Bulk email** (the only message element), Add to event, Send audience to Google/Meta Ads (8.3.4+). (C)
- **No SMS, WhatsApp, Business process or webhook element.** The SMS element on toolkit stands is the `MapDemo`
  mock: it sends nothing. (C, matches toolkit)
- **Omnichannel Marketing app** (Creatio, 8.3.4+, Freedom UI): SMS section + "SMS touchpoints" in campaign flows;
  bulk WhatsApp with Meta-approved templates (v1.2.233, 3 Nov 2026). Twilio. **SMS to contacts in Europe only**
  (Academy) → likely unusable for APAC SMS. WhatsApp as a flow element: not confirmed. Price conflicting on the
  listing: ask Creatio. (C)

### 4b. Routes, recommendation first

| Route | How | Cost | Use when |
|---|---|---|---|
| **B. Campaign → Modify data → process → Send chat message (recommended)** | Campaign step sets a flag (e.g. `UsrWhatsAppStep = "Offer 1"`) on the contact/lead → process starts on signal "Record modified" filtered on that field → **Send chat message** on the WhatsApp (or SMS) channel with an approved template → reply lands in Agent Inbox as a chat → AI or agent picks it up → flag cleared / outcome written back → next campaign condition reads it | No code; 2–4 h on a stand with a working channel (A) | Default. Shows the real thing: campaign, WhatsApp delivered to a phone, two-way reply in the CRM |
| B2. Same, but Call web service to Twilio's API | Instead of Send chat message | No code; credentials in system settings | No chat channel on the stand, or SMS where the SMS channel isn't set up |
| C. Omnichannel Marketing app | Install, connect Twilio, SMS touchpoint in the flow | Licence question; Europe-only SMS | European audience on 8.3.4+ |
| D. Marketplace connector with a campaign element | Twilio SMS/MMS Connector (Solutions Metrix, Freedom UI, delivered/undelivered branches, ~US$9,975/yr); Consimple (WhatsApp element, Classic UI) | Paid; vendor trial | Customer must see an SMS element on the canvas with delivery branches |
| E. **Custom campaign element** (Academy dev example `sdkCustomCampaignElement`) | 7 schemas: element module, properties panel, replacing `CampaignElementSchemaManagerEx`, C# flow element (`GetAudienceQuery`, `SingleExecute`), C# element schema, event handler (validate), log item type (8.3.4+); compile; clear cache | Code + compile + rollback plan (BUILD-RULES); **the example sends nothing**: we'd write the Twilio send loop | Only when "we can extend the canvas" is itself the pitch (a partner/IT audience) |

**Challenge on route E (judgement call):** it looks the most impressive, but it's the least reliable for a demo:
compile on the stand, Classic-style designer code, a send loop we'd own, and a version split at 8.3.4. Route B shows
the same business outcome with no code, and the audience can't tell the difference on the canvas unless we point at
it. Build E once on a clean stand as a library module if deals keep asking, not per deal.

### 4c. WhatsApp marketing rules that bite a demo (C: Creatio usage policy; I for timing)

- Business-started messages need a **Meta-approved template** (Marketing / Utility / Authentication). Submit it
  **days ahead**; marketing templates can be rejected.
- Every recipient must have **opted in**; opt-outs honoured. Demo with our own phones only.
- Twilio sandbox: recipients must `join` first (72 h); it's fine for a demo, not a pilot.

---

## 5. Choosing the demo route: decision order

1. **What does the customer actually use?** (WhatsApp in ID/MY/PH, SMS in AU, Messenger/Instagram for retail.)
   Show that channel, not all of them.
2. **Stand version?** 10.x → CCH + Agent Inbox + web chat. 8.3 → Chat settings, no web chat, Meta WhatsApp not
   available.
3. **Real or simulated?** Real when the channel is native and the provider can be set up before the demo
   (Telegram, Twilio sandbox, Messenger with a demo Page). Simulated (webhook or "simulate intake" process with
   Origin stamped) when it needs Meta review, a paid connector or the customer's own system. **Say which on the
   script and in the build plan.**
4. **One real channel beats four simulated ones.** A WhatsApp message arriving on a phone in the room is the beat
   people remember (I).

## 6. Pre-demo checklist (add to the click path)

| Check | Why |
|---|---|
| Presenter is a queue agent (and Active on 8.3) | Chats arrive nowhere otherwise |
| Twilio sandbox re-joined from every demo phone in the last 72 h | Sandbox drops the join |
| One inbound message per channel sent and seen in Agent Inbox the same morning | Provider side breaks silently |
| WhatsApp template approved; send it once to our own phone | Outside 24 h nothing else is delivered |
| AI user has rights on side-effect objects; knowledge base indexed | Silent AI failures (toolkit) |
| Webhook test POST shows Done; default process active (or ours) | Polls every minute |
| Process tracing on for the integration process | The "under the hood" beat |
| Facebook Page / bot / number not bound to another stand | Last integration wins |
| Fallback recording of each live beat | Provider outages |

## 7. Lead times (put them in the build plan)

| Item | Lead time | Evidence |
|---|---|---|
| IdentityServer settings empty → Creatio support | Days (A) | C (need), A (time) |
| Telegram bot, web chat preview | Minutes | C |
| Twilio trial / sandbox, SMS number | Under an hour | C |
| Messenger with a demo Page | An hour if we already have the Page (A) | — |
| Meta Cloud API WhatsApp | Hours to days (Meta verification) | C |
| WhatsApp template approval | Allow days | I |
| Marketplace connector trial (Beesender, Solutions Metrix) | Vendor-dependent, ask a week ahead (A) | — |
| Meta app review for comments (production) | Weeks (A); not for demos | — |

## 8. Sources (read 18 Nov 2026)

Academy (8.3 unless marked):
- REST web service setup: academy.creatio.com/guides/no-code-customization/8.3/base-integrations/web-services/set-up-the-rest-web-service-integration
- Web service authentication (v10): academy.creatio.com/guides/no-code-customization/base-integrations/web-services/web-service-authentication
- Call web service element: …/8.3/bpm-tools/process-elements-reference/system-actions/call-web-service-process-element
- Currency rates example: …/8.3/bpm-tools/bpm-process-examples/update-currency-exchange-rates-with-web-service-integration
- Process tracing: …/8.3/bpm-tools/business-process-administration/trace-process
- Webhook service: …/8.3/base-integrations/webhook-service-integration/overview, /retrieve-a-webhook, /process-webhooks
- OData basics: academy.creatio.com/guides/dev/development-on-creatio-platform/8.3/integrations-and-api/data-services/odata/basics/overview
- OAuth 2.0 apps (8.2): …/8.2/base-integrations/oauth-2-0/set-up-the-oauth-2-0-authorization-instruction
- Chats 8.3: …/8.3/base-integrations/set-up-chats/ (set-up-chat-processing, whatsapp/set-up-whatsapp-integration,
  whatsapp/feature-comparison-for-whatsapp, set-up-facebook-messenger-integration, set-up-sms-integration,
  ai-automation-for-chat-channels)
- Customer Communication Hub (v10): academy.creatio.com/guides/creatio-apps/products/crm-tools/inbound-communications/communications-setup/customer-communication-hub/
  (set-up-the-whatsapp-channel, set-up-the-whatsapp-channel-meta-cloud-api, set-up-the-telegram-channel,
  set-up-the-web-chat-channel, set-up-chat-routing, feature-comparison-for-whatsapp)
- Send chat message element: …/8.3/bpm-tools/process-elements-reference/user-actions/send-chat-message-process-element
- Chat on-site access (v10): academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/chat-access-setup
- Facebook lead ads: academy.creatio.com/documents?id=2499&ver=8.3 · LinkedIn (8.0): …/8.0/base-integrations/set-up-automatic-lead-registration-from-linkedin
- Campaign element reference (8.3 and v10): academy.creatio.com/guides/creatio-apps/8.3/products/marketing-tools/marketing-campaings/campaign-element-reference
- Omnichannel Marketing (v10): …/products/marketing-tools/omnichannel-marketing/omnichannel-marketing-overview, …/whatsapp-usage-policy
- Custom campaign element (dev, 8.3): academy.creatio.com/guides/dev/development-on-creatio-platform/8.3/platform-customization/freedom-ui/marketing-campaigns-basics/examples/implement-a-campaign-element
- Release notes 10.1: academy.creatio.com/guides/resources/release-notes/10-1-unlimited-release-notes

Marketplace (marketplace.creatio.com/app/…): omnichannel-marketing, lead-generation, web-chat,
hootsuite-connector-creatio, beesender-chat-master-creatio, beesender-omnichannel-creatio,
social-media-cases-creatio, twilio-smsmms-connector-creatio, consimple-messenger-campaigns-creatio,
salesup-multichannel-bulk-messaging-creatio, gms-connector-creatio, psiog-whatsapp-connector-creatio,
zapier-connector-creatio, experceo-makecom-connector-creatio. Customer Communication Hub: marketplace.creatio.com/node/33096.

Meta: developers.facebook.com/docs/graph-api/webhooks/getting-started, …/webhooks/reference/page/,
…/documentation/instagram-platform/webhooks/fields, …/docs/graph-api/overview/access-levels/. Twilio sandbox:
twilio.com/docs/whatsapp/sandbox.

## 9. Not yet proven: the open items

| # | Open item | How we close it |
|---|---|---|
| 1 | Every recipe above is from documentation only | Rehearse on a clean stand (§10) and mark rows "proven <date, stand>" |
| 2 | Can Send chat message **start** a conversation on Telegram, Messenger, SMS (not just WhatsApp)? | Test on the stand |
| 3 | WhatsApp templates under Meta Cloud API | Test when a 10.1 stand + a Meta number exist |
| 4 | Webhook URL format in 8.3/10 | Read it off the stand |
| 5 | Omnichannel Marketing price and whether WhatsApp is a flow element | Ask Creatio (product team) |
| 6 | Which of our stands are 10.x vs 8.3 | `library/stands.json` |

## 10. Next step proposed: a channels showcase module

Build once, on our own clean stand, as a demo library module: Telegram + Twilio sandbox WhatsApp + SMS channels into
one queue with AI handoff; a webhook intake (simulated social comment → case + AI triage); a Call web service
enrichment with tracing; a campaign using route B. Then every deal copies the beats instead of rebuilding them.
Needs Renzo's approval and the usual build plan (BUILD-RULES).
