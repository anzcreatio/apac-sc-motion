# Freedom UI mock-up kit v0.1

**What it's for:** any page that shows a partner or customer what a Creatio screen will look like before it's built
(a demo storyboard, a concept page, a one-pager). It makes HTML mock-ups read as Creatio, not as a generic web app.

**Why (Renzo, 20 Nov 2026, Yokogawa):** the first storyboard for InsightTech used our own styling (orange buttons,
our cards and pills). It looked like a website, not Creatio, so a partner couldn't picture the product. Restyled with
the measured Freedom UI values, it reads as Creatio. Lesson: `Lessons/feedback/2026-11-20-renzo-huruiti-mockups-look-like-creatio.md`.

## Rules

| # | Rule |
|---|---|
| 1 | **Use `freedom-ui-mock.css`** (paste it into the page's `<style>`). Never invent Creatio colours, fonts or component shapes. The values come from `../UI-KIT-STANDARD-v0.7.md` §2c, measured on a clean Creatio 10 stand |
| 2 | **Blue is the product's action colour, orange is the brand.** Buttons, links, selected items and the current step are primary blue `#004fd6`. Orange `#ff4013` only for the Creatio logo and the page around the mock-ups |
| 3 | **Screens stay light** in both page themes, like a real screenshot. The page around them follows the viewer's theme |
| 4 | Montserrat everywhere in the screens. Page title 18–24/600 navy `#0d2e4e`; field label 12/500 above a 13/500 value; card title 14–16/500 |
| 5 | Cards: white, 1px `rgba(0,0,0,.1)`, radius 8. Chips: radius 16, a palette colour on its 20% tint. Buttons: 32px, radius 4; one primary (solid blue) per screen, the rest text-only. Tabs: uppercase, the selected one navy with an underline, the others link blue. Lists: 40px rows, muted 12px header |
| 6 | **AI panels in violet** (`#7848ed` on its tint), each ending with the person who decides |
| 7 | Every record page gets the header (title, status chip, Close / Save) and a tab row: it's what makes a mock-up read as Freedom UI |
| 8 | Example data only, fictional names and companies, and a caption saying so. No customer data |
| 9 | Don't show another vendor's screens or compare with them on the page |
| 10 | **The page is for the reader, not about them.** Question boxes are labelled "Question", never "Ask <name>" or "Ask the partner"; no coaching notes on a page the partner or customer sees (Renzo, 20 Nov 2026). A partner-ready storyboard (mock-up + caption + one question per screen) is worth making whenever a partner must picture the demo before the build |

**What the kit can't do:** it's ~80% of the real look. Real screenshots from the stand replace the mock-ups once the
demo is built (deck `screen` slides). Internal build plans keep their wireframes (`sc-demo-plan`), skinned with the
same values.

## Markup (copy and change the words)

```html
<div class="app">
  <div class="app-top"><span class="logo">Creatio</span><span class="crumb">Approvals › Purchase requests › PR-0418</span>
    <span class="who"><span class="avatar">KI</span>Kenji Ito · Tokyo</span></div>
  <div class="app-body"><div class="side"><i></i><i class="on"></i><i></i><i></i></div>
    <div class="main">
      <div class="rec-title"><h4>PR-0418 · Calibration bench upgrade</h4><span class="pill warn">Waiting</span>
        <div class="btns"><span class="btn">Close</span><span class="btn pri">Save</span></div></div>
      <div class="uitabs"><span class="on">General info</span><span>Approvals</span><span>Attachments</span></div>
      <div class="grid3"><div class="field"><span class="lb">Amount</span><span class="v">¥4,800,000</span></div></div>
      <div class="card"><h5>Approval path</h5>
        <div class="path"><div class="node done"><b>Manager</b><span>Approved</span></div><span class="arrow">→</span>
          <div class="node now"><b>Dept head</b><span>Waiting</span></div></div></div>
      <div class="ai"><span class="h">AI summary</span><span class="check">Amount matches the quote</span></div>
    </div></div>
</div>
```

Also in the kit: `.t` list table (`td.edit` + `.was` for a live change), `.ba` before/after, `.audit` change log,
`.toast`, `.bars` chart, `.kpi`, `.phone` frame (`.ph-top`, `.ph-body`), `.steps`/`.canvas`/`.fld`/`.palette` for the
app designer, `.mail` for an incoming email, `.par` for parallel consultation (Japanese ringi 合議), `.stamp` for a seal image, `.notice` for a blocking rule message, `.jp` for Japanese text. Tabs need `[hidden]{display:none!important}` in the page if you test it outside the Artifact viewer. Worked example: `Deals/yokogawa-electric-rh/07-demo-storyboard-2026-11-20.html`.

## Changes

| Version | Date | Change |
|---|---|---|
| v0.1 | 20 Nov 2026 | First kit, from the Yokogawa storyboard (Renzo: "make future mockups more Creatio like") |
