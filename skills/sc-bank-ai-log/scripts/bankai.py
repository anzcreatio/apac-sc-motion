"""Bank.AI requirements log (sc-bank-ai-log). Customer requirements and pains from BFSI deals, with our proposed
configuration and fit, for the Bank.AI team. No demo, deck, meeting, commercial or competitor content.

  python bankai.py from-register --deal-config <deal>/bank-ai.json --register R --verdicts V --source "TOR compliance matrix"
      Add every rated requirement in our scope from an sc-rfp or sc-workshop register (upsert by id).
  python bankai.py add --deal-config <deal>/bank-ai.json --lines lines.json
      Add lines Claude wrote from a transcript, workshop, customer document or demo plan (same fields as the log).
  python bankai.py index
      Rebuild Bank-AI-Requirements/INDEX.md and README.md across all banks.

Output: <team root>/Bank-AI-Requirements/<deal folder>/log.jsonl + README.md. Team root from ~/.apac-sc-motion.json.
Lines that break a rule (commercial or demo words, a competitor or a person in our fields) stop the run.
"""
import argparse
import collections
import datetime
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

FOLDER = "Bank-AI-Requirements"
GAP_FITS = {"custom", "partner", "roadmap", "no"}
FIT_LABEL = {"standard": "Standard", "configure": "Configure (no code)", "ai": "AI (Creatio.ai / AI Studio)",
             "marketplace": "Marketplace app", "integration": "Integration", "custom": "Custom development",
             "partner": "Third-party / partner", "roadmap": "Roadmap", "no": "Not supported", "n/a": "Not a product question"}
COMPETITORS = ["Salesforce", "Microsoft Dynamics", "Dynamics 365", "Dynamics", "Pega", "Pegasystems", "Oracle Siebel",
               "Siebel", "Zoho", "HubSpot", "ServiceNow", "Freshworks", "SugarCRM", "Zendesk", "Veeva", "nCino", "Backbase"]
OURS_BANNED = r"(?i)\b(price|pricing|priced|discount|commercials?|demo(s|ed|ing)?|deck|presentation|slides?|win themes?|competitors?|bid(s|ding)?|man-?days? cost)\b"
FIELDS = ["id", "bank", "country", "segment", "source_type", "source", "date", "area", "requirement", "english",
          "priority", "tag", "proposed_configuration", "fit", "confidence", "gap", "gap_note", "question"]
AREAS = [
    ("AI", r"\bai\b|artificial intel|machine learning|chatbot|predicti|gen ?ai|\bllm\b|next best"),
    ("Collections", r"collect|arrear|overdue|tagih|delinquen|recover"),
    ("Onboarding and KYC", r"\bkyc\b|onboard|know your|e-?kyc|\baml\b|due diligence|account opening|identity verif"),
    ("Lending and origination", r"\bloan|lending|kredit|pinjam|gadai|pawn|leasing|credit (application|scor|approv)|financing|origination"),
    ("Wealth, brokerage and investment banking", r"invest|brokerage|portfolio|trading|securities|equit|mutual fund|wealth|ifist|\bipo\b|underwrit|mandate"),
    ("Agents and partners", r"\bagents?\b|partner management|broker|referral|mitra|dealer"),
    ("Marketing, campaigns and loyalty", r"campaign|marketing|segment|promo|\bcdp\b|loyalty|journey|customer data platform"),
    ("Sales and leads", r"\blead|opportunit|pipeline|cross-?sell|up-?sell|prospect|sales"),
    ("Service and complaints", r"complain|ticket|\bcase|keluhan|\bsla\b|contact care|helpdesk|service request"),
    ("Channels and contact centre", r"whatsapp|\bsms\b|e-?mail|\bchat|telephon|\bcti\b|call cent|omni|portal|mobile app|channel"),
    ("Security and compliance", r"security|access control|\brole|permission|audit|encrypt|\biso\b|complian|privacy|\bojk\b|regulat|password|\bsso\b|authenticat|data protection"),
    ("Integration and architecture", r"integrat|\bapi|interface|architect|core banking|middleware|\besb\b|scalab|reliab|availab|deploy|cloud|saas|on-?prem|hosting|devops|performance|disaster|backup|monitoring"),
    ("Customer 360 and data", r"360|single view|customer data|profile|data management|master data|nasabah|data quality"),
    ("Reporting and analytics", r"report|dashboard|analytic|\bkpi|insight"),
    ("Workflow and platform", r"workflow|process|approval|configur|low-?code|no-?code|admin|platform|module|task"),
]


def team_root():
    cfg = os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json")
    try:
        return json.load(open(cfg, encoding="utf-8"))["sharepoint_root"]
    except Exception:
        sys.exit("No team root: run sc-setup first (~/.apac-sc-motion.json)")


def area_of(text, section, area_map):
    for k, v in (area_map or {}).items():
        if k.lower() in (section or "").lower():
            return v
    t = "%s %s" % (section or "", text or "")
    for name, rx in AREAS:
        if re.search(rx, t, re.I):
            return name
    return "Other"


def redact(text, words):
    out = str(text or "")
    for w in sorted(words, key=len, reverse=True):
        if w:
            out = re.sub(r"(?i)(?<!\w)%s(?!\w)" % re.escape(w), "[vendor]", out)
    return out


def guard(line, cfg):
    """Errors for our own fields (we must never write these); customer text is redacted instead."""
    E = []
    ours = " ".join(str(line.get(k) or "") for k in ("proposed_configuration", "gap_note", "question", "area"))
    m = re.search(OURS_BANNED, ours)
    if m:
        E.append("%s: our fields mention '%s' (no demo, deck, commercial or competitor content)" % (line["id"], m.group(0)))
    for w in COMPETITORS + cfg.get("competitors", []) + cfg.get("people", []):
        if re.search(r"(?i)(?<![\w-])%s(?![\w-])" % re.escape(w), ours):
            E.append("%s: our fields name '%s'" % (line["id"], w))
    return E


def clean_customer(line, cfg):
    words = COMPETITORS + cfg.get("competitors", [])
    people = cfg.get("people", [])
    for k in ("requirement", "english", "source"):
        if line.get(k):
            v = redact(line[k], words)
            for p in people:
                v = re.sub(r"(?i)(?<![\w-])%s(?![\w-])" % re.escape(p), "[name removed]", v)
            line[k] = v
    return line


def load_log(path):
    rows = collections.OrderedDict()
    if os.path.exists(path):
        for ln in open(path, encoding="utf-8"):
            if ln.strip():
                r = json.loads(ln)
                rows[r["id"]] = r
    return rows


def deal_dir(cfg_path):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    deal = cfg.get("deal_folder") or os.path.basename(os.path.dirname(os.path.abspath(cfg_path)))
    return cfg, deal, os.path.join(team_root(), FOLDER, deal)


def write(cfg, deal, out, new_lines):
    E = []
    for ln in new_lines:
        E += guard(ln, cfg)
    if E:
        print("%d problems, nothing written:" % len(E))
        for e in E[:40]:
            print("  " + e)
        sys.exit(1)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "log.jsonl")
    rows = load_log(path)
    for ln in new_lines:
        rows[ln["id"]] = {k: ln.get(k) for k in FIELDS}
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows.values():
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    open(os.path.join(out, "README.md"), "w", encoding="utf-8").write(readme(cfg, list(rows.values())))
    gaps = sum(1 for r in rows.values() if r.get("gap"))
    print("%s: %d lines in the log (%d added or updated), %d gaps -> %s" % (cfg["bank"], len(rows), len(new_lines), gaps, out))


def base(cfg):
    return {"bank": cfg["bank"], "country": cfg["country"], "segment": cfg.get("segment", "")}


def from_register(a):
    cfg, deal, out = deal_dir(a.deal_config)
    reg = json.load(open(a.register, encoding="utf-8"))
    ver = {v["rid"]: v for v in json.load(open(a.verdicts, encoding="utf-8"))}
    kind = reg.get("kind") or "rfp"
    lines = []
    for q in reg["requirements"]:
        v = ver.get(q["rid"])
        if q.get("scope") != "ours" or not v or v.get("fit") in (None, "n/a"):
            continue
        ex = q.get("extra") or {}
        pr = ex.get("priority") or {True: "must", False: "should", None: "unranked"}[q.get("mandatory")]
        fit = v.get("fit")
        gap = fit in GAP_FITS
        note = " ".join(x for x in [v.get("workaround") and "Workaround: " + v["workaround"]] if x) if gap else ""
        ln = dict(base(cfg), id="%s:%s" % (deal, q["rid"]), source_type="workshop" if kind == "workshop" else "rfp",
                  source=("%s, %s %s" % (a.source, q.get("sheet") or "", q.get("src_id") or "")).strip(),
                  date=reg.get("built") or datetime.date.today().isoformat(),
                  area=area_of((v.get("english") or "") + " " + q["text"], q.get("section"), cfg.get("area_map")),
                  requirement=q["text"], english=v.get("english") or (None if (reg.get("language") or "en") == "en" else None),
                  priority=pr, tag=ex.get("tag") or "C", proposed_configuration=v.get("how"), fit=fit,
                  confidence=v.get("confidence"), gap=gap, gap_note=note, question=v.get("question"))
        lines.append(clean_customer(ln, cfg))
    write(cfg, deal, out, lines)


def add(a):
    cfg, deal, out = deal_dir(a.deal_config)
    lines = []
    for ln in json.load(open(a.lines, encoding="utf-8")):
        ln = dict(base(cfg), **ln)
        ln.setdefault("date", datetime.date.today().isoformat())
        ln["id"] = ln["id"] if ln["id"].startswith(deal + ":") else "%s:%s" % (deal, ln["id"])
        ln["gap"] = ln.get("fit") in GAP_FITS
        if not ln.get("area"):
            ln["area"] = area_of((ln.get("english") or "") + " " + ln.get("requirement", ""), "", cfg.get("area_map"))
        lines.append(clean_customer(ln, cfg))
    write(cfg, deal, out, lines)


def short(t, n=160):
    t = " ".join(str(t or "").split())
    return (t if len(t) <= n else t[:n - 1] + "…").replace("|", "/")


def readme(cfg, rows):
    by_area = collections.OrderedDict()
    for r in sorted(rows, key=lambda r: (r["area"], r["id"])):
        by_area.setdefault(r["area"], []).append(r)
    fits = collections.Counter(r["fit"] for r in rows)
    gaps = [r for r in rows if r.get("gap")]
    srcs = sorted({r["source_type"] for r in rows})
    L = ["# %s: customer requirements for Bank.AI" % cfg["bank"], "",
         "| | |", "|---|---|", "| Bank | %s |" % cfg["bank"], "| Country | %s |" % cfg["country"],
         "| Segment | %s |" % cfg.get("segment", ""), "| Context | %s |" % cfg.get("context", ""),
         "| Sources | %s |" % ", ".join(srcs), "| Requirements | %d (%d gaps) |" % (len(rows), len(gaps)),
         "| Updated | %s |" % datetime.date.today().isoformat(), "",
         "Every line is the customer's requirement in their words (English translation where needed), with the "
         "configuration we'd propose and its fit. Full data: `log.jsonl` (one JSON object per line).", "",
         "## Gaps first (custom, partner, roadmap or not supported)", "",
         "| Ref | Area | Requirement | Fit | What we'd do |", "|---|---|---|---|---|"]
    for r in gaps:
        L.append("| %s | %s | %s | %s | %s |" % (r["id"].split(":", 1)[1], r["area"], short(r.get("english") or r["requirement"]),
                                                 FIT_LABEL.get(r["fit"], r["fit"]), short((r.get("gap_note") or "") + " " + (r.get("proposed_configuration") or ""), 200)))
    if not gaps:
        L.append("| | | None | | |")
    L += ["", "## Fit across all requirements", "", "| Fit | Lines |", "|---|---|"] + \
         ["| %s | %d |" % (FIT_LABEL.get(k, k), n) for k, n in fits.most_common()]
    L += ["", "## Requirements by area", ""]
    for area, rs in by_area.items():
        L += ["### %s (%d)" % (area, len(rs)), "", "| Ref | Priority | Requirement | Proposed configuration | Fit |", "|---|---|---|---|---|"]
        L += ["| %s | %s | %s | %s | %s |" % (r["id"].split(":", 1)[1], r.get("priority") or "", short(r.get("english") or r["requirement"]),
                                             short(r.get("proposed_configuration"), 180), r["fit"]) for r in rs]
        L.append("")
    return "\n".join(L) + "\n"


SCHEMA = """## Fields in each `log.jsonl` line

| Field | Meaning |
|---|---|
| `id` | `<deal>:<customer ref>`, stable across updates |
| `bank`, `country`, `segment` | Who asked |
| `source_type`, `source`, `date` | rfp · workshop · transcript · document; where exactly (clause, sheet, minute) |
| `area` | Business area (lending, collections, KYC, wealth, service, channels, AI, security, integration, …) |
| `requirement`, `english` | The customer's words; English translation when the original isn't English |
| `priority`, `tag` | must · should · could · unranked; C the customer said it · I inferred · A assumed |
| `proposed_configuration`, `fit`, `confidence` | What APAC presales would configure, and how well the product fits today |
| `gap`, `gap_note`, `question` | true when the fit is custom, partner, roadmap or not supported; the workaround; what to ask the customer |
"""


def index(a):
    root = os.path.join(team_root(), FOLDER)
    os.makedirs(root, exist_ok=True)
    rows = []
    for d in sorted(os.listdir(root)):
        p = os.path.join(root, d, "log.jsonl")
        if os.path.isfile(p):
            rows += list(load_log(p).values())
    banks = sorted({r["bank"] for r in rows})
    by_area = collections.defaultdict(list)
    for r in rows:
        by_area[r["area"]].append(r)
    L = ["# APAC banking requirements: index for Bank.AI", "",
         "%d requirements from %d banks (%s). Updated %s. Each bank's folder has a README (gaps first) and `log.jsonl`." % (
             len(rows), len(banks), ", ".join(banks), datetime.date.today().isoformat()), "",
         "## By business area", "", "| Area | Requirements | Banks | Gaps | Gap share |", "|---|---|---|---|---|"]
    for area, rs in sorted(by_area.items(), key=lambda kv: -sum(1 for r in kv[1] if r.get("gap"))):
        g = sum(1 for r in rs if r.get("gap"))
        L.append("| %s | %d | %d | %d | %.0f%% |" % (area, len(rs), len({r['bank'] for r in rs}), g, 100.0 * g / len(rs)))
    L += ["", "## Every gap, by area", ""]
    for area, rs in sorted(by_area.items()):
        gs = [r for r in rs if r.get("gap")]
        if not gs:
            continue
        L += ["### %s" % area, "", "| Bank | Ref | Requirement | Fit | Workaround / proposal |", "|---|---|---|---|---|"]
        L += ["| %s | %s | %s | %s | %s |" % (r["bank"], r["id"].split(":", 1)[1], short(r.get("english") or r["requirement"]),
                                             r["fit"], short((r.get("gap_note") or "") + " " + (r.get("proposed_configuration") or ""), 200)) for r in gs]
        L.append("")
    open(os.path.join(root, "INDEX.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    open(os.path.join(root, "README.md"), "w", encoding="utf-8").write(
        "# Bank-AI-Requirements\n\nWhat APAC banks and financial services customers ask for, in their words, with the "
        "configuration APAC presales would propose and how well the product fits today. Kept by the APAC SC team "
        "(`sc-bank-ai-log`) for the Bank.AI team. It holds customer requirements only: no sales, demo, commercial or "
        "competitor content.\n\nStart with `INDEX.md` (gaps across banks), then each bank's `README.md`. To feed "
        "Claude, give it the `log.jsonl` files.\n\n" + SCHEMA)
    print("Index: %d requirements, %d banks, %d gaps -> %s" % (len(rows), len(banks), sum(1 for r in rows if r.get("gap")), root))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("from-register"); p.add_argument("--deal-config", required=True); p.add_argument("--register", required=True)
    p.add_argument("--verdicts", required=True); p.add_argument("--source", required=True)
    p = sp.add_parser("add"); p.add_argument("--deal-config", required=True); p.add_argument("--lines", required=True)
    sp.add_parser("index")
    a = ap.parse_args()
    {"from-register": from_register, "add": add, "index": index}[a.cmd](a)


if __name__ == "__main__":
    main()
