"""sc-desk: an SC's work desk. Commitments ledger, stall detection, daily brief, weekly view, load check.

An SC TASK DESK, NOT A CRM: it never stores pipeline stage, forecast or deal value. "Closeness to a decision" is
worked out fresh from the folder each run (demo done, RFP folder, ...) and never saved.

Ledger (one per deal):  <deal>/commitments.json
Daily brief:            the SC's own PC only, ~/.apac-sc-motion/desk/<yyyy-mm-dd>-brief.md (never SharePoint)
Weekly (Renzo only):    team page Lessons/desk/weekly/<yyyy-Www>.md + .json (totals, no SC named);
                        per-SC view in his local folder (--private-out, default ~/SC-Desk)

PRIVATE PER SC (FEEDBACK-LOOP v0.2 section 5): every command works only on the SC's own deals (`sc` in
~/.apac-sc-motion.json). Another SC's deal, brief or workload is refused, except for the lead (Renzo, rh).

  python desk.py add      --deal <deal> --what "..." --owner "..." [--due 2026-11-20 | --due-text "this week"] [--source "..."] [--side us|them]
  python desk.py done     --match "<words>" [--deal <deal>] [--sc rh] [--note "..."] [--id C-003]   ("done: <what>")
  python desk.py drop     --deal <deal> --id C-003 --note "why"
  python desk.py list     [--deal <deal>] [--sc rh] [--all]
  python desk.py capture  --deal <deal> [--apply [--pick 1,3]]        candidates from reviews, next steps, AE brief, follow-ups
  python desk.py meeting  --deal <deal> --date 2026-11-20 --what "..." [--source "..."]   next meeting booked
  python desk.py touch    --deal <deal> --what "..." [--date ...] [--recap-sent]          activity outside the folder (mail sent)
  python desk.py status   --deal <deal> --set active|parked|closed [--until 2027-01-20] [--note "..."]   desk status, not a sales stage
  python desk.py owner    --deal <deal> --sc rh
  python desk.py scan     [--sc rh] [--deal <deal>] [--json]
  python desk.py brief    [--sc rh] [--calendar events.json] [--out file.md] [--no-write]
  python desk.py week     [--private-out <local folder>] [--no-write]
  python desk.py load     [--sc rh] [--week 2026-W47] [--calendar events.json]

--calendar: a JSON list Claude saves from the Microsoft 365 connector (read-only), each
  {"subject": "...", "start": "2026-11-16T08:30:00+11:00", "end": "...", "attendees": ["..."], "location": "..."}.
Without it the desk uses the deal folders only. The desk never sends mail and never writes to a calendar.
Team root from ~/.apac-sc-motion.json (or --root).
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import statistics
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TEAM = {"rh": "Renzo Huruiti", "wn": "Willy Noviandy", "fa": "Ferdhi Adrian"}
LEDGER = "commitments.json"
CHECK = "Not sent: you or the AE send it."

# Stall and load thresholds (agreed design, 14 Nov 2026). Change here, not in the skill text.
STALE_DAYS = 7          # no activity
PARK_HINT_DAYS = 21     # no activity and nothing ahead: ask whether it's parked
DEMO_PLAN_DAYS = 3      # demo this close needs an approved build plan
HARVEST_WD = 2          # working days after a demo
LOAD = {"demos": 3, "customer_meetings": 8, "build_hours": 24, "same_day_demos": 2, "due_ours": 8}

# Housekeeping files that don't mean the deal moved (ledger, dates backfill, Bank.AI log).
SKIP_FILES = {"desktop.ini", LEDGER, "thumbs.db", "deal-dates.json", "bank-ai.json"}
NOW = dt.datetime.now()
TODAY = NOW.date()


# ---------- basics ----------

def cfg():
    try:
        return json.load(open(os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json"), encoding="utf-8"))
    except Exception:
        return {}


def team_root(arg=None):
    r = arg or cfg().get("sharepoint_root")
    if not r:
        sys.exit("No team root: run sc-setup first, or pass --root")
    return r


LEAD = "rh"  # Renzo leads the team: the only SC who may see another SC's desk (Friday view)


def me():
    sc = cfg().get("sc")
    if sc not in TEAM:
        sys.exit("Who are you? No SC initials in ~/.apac-sc-motion.json: run sc-setup first.")
    return sc


def my_sc(arg=None):
    """The SC to work for. Anyone but the lead can only ever be themselves."""
    who = me()
    if arg and arg != who and who != LEAD:
        sys.exit("That's %s's desk to share: ask them, or Renzo." % TEAM.get(arg, arg))
    return arg or who


def guard_deal(deal):
    """Refuse another SC's deal (lead excepted). Deals with no SC set count as the lead's until claimed."""
    who = me()
    o = owner_sc(deal)
    if who == LEAD or o == who:
        return deal
    if o is None:
        sys.exit("No SC is set on %s yet. If it's yours, ask Renzo to set it (desk.py owner)." % os.path.basename(deal))
    sys.exit("%s is %s's deal: ask them, or Renzo." % (os.path.basename(deal), TEAM.get(o, o)))


def iso(d):
    return d.isoformat() if d else None


def pdate(s):
    if not s:
        return None
    try:
        return dt.date.fromisoformat(str(s)[:10])
    except ValueError:
        return None


def friday(d):
    return d + dt.timedelta(days=(4 - d.weekday()) % 7)


def add_wd(d, n):
    while n > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


def wd_between(a, b):
    """Working days from a (exclusive) to b (inclusive)."""
    n, d = 0, a
    while d < b:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            n += 1
    return n


def plural(n, word):
    return "%d %s%s" % (n, word, "" if n == 1 else "s")


def rjson(p, default=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return default


def wjson(p, data):
    tmp = p + ".tmp"
    json.dump(data, open(tmp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    os.replace(tmp, p)


def rtext(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def norm(s):
    return re.sub(r"[^a-z0-9 ]+", " ", (s or "").lower()).split()


def similar(a, b):
    A, B = set(norm(a)), set(norm(b))
    return bool(A and B) and len(A & B) / len(A | B) >= 0.6


MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
DAYS = {d: i for i, d in enumerate(["mon", "tue", "wed", "thu", "fri", "sat", "sun"])}


def parse_due(text, ref):
    """Only unambiguous phrases. Returns a date or None (then the brief asks the SC). Never guesses 'late January'."""
    t = re.split(r"\.\s|\(|;", (text or "").lower().strip())[0].strip()
    if not t:
        return None
    m = re.search(r"(20\d\d)-(\d\d)-(\d\d)", t)
    if m:
        return pdate(m.group(0))
    m = re.search(r"\b(\d{1,2})\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b(?:\s+(20\d\d))?", t) or \
        re.search(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{1,2})\b(?:,?\s+(20\d\d))?", t)
    if m:
        g = m.groups()
        day, mon = (int(g[0]), MONTHS[g[1]]) if g[0].isdigit() else (int(g[1]), MONTHS[g[0]])
        year = int(g[2]) if g[2] else ref.year
        try:
            d = dt.date(year, mon, day)
        except ValueError:
            return None
        if not g[2] and d < ref - dt.timedelta(days=60):
            d = dt.date(year + 1, mon, day)
        return d
    if re.search(r"\btoday\b", t):
        return ref
    if re.search(r"\btomorrow\b", t):
        return add_wd(ref, 1) if ref.weekday() >= 4 else ref + dt.timedelta(days=1)
    if re.search(r"\b(this week|end of (the )?week|by friday|eow)\b", t):
        return friday(ref)
    if re.search(r"\bnext week\b", t):
        return friday(ref) + dt.timedelta(days=7)
    if re.search(r"\bchristmas\b", t):
        return dt.date(ref.year, 12, 24)
    m = re.search(r"\b(?:by |on |this )?(mon|tue|wed|thu|fri)[a-z]*\b", t)
    if m and not re.search(r"\b(month|monthly)\b", t):
        d = ref + dt.timedelta(days=(DAYS[m.group(1)] - ref.weekday()) % 7 or 7)
        return d
    return None


# ---------- deals and the ledger ----------

def deals_dir(root):
    return os.path.join(root, "Deals")


def all_deals(root):
    out = []
    for n in sorted(os.listdir(deals_dir(root))):
        p = os.path.join(deals_dir(root), n)
        if os.path.isdir(p) and not n.startswith(("_", ".")):
            out.append(p)
    return out


def resolve_deal(root, d):
    if os.path.isdir(d):
        return os.path.normpath(d)
    p = os.path.join(deals_dir(root), d)
    if os.path.isdir(p):
        return p
    hits = [x for x in all_deals(root) if d.lower() in os.path.basename(x).lower()]
    if len(hits) == 1:
        return hits[0]
    sys.exit("Deal folder not found or ambiguous: %s %s" % (d, [os.path.basename(h) for h in hits]))


def load_ledger(deal):
    L = rjson(os.path.join(deal, LEDGER)) or {}
    L.setdefault("deal", os.path.basename(deal))
    L.setdefault("status", "active")
    L.setdefault("items", [])
    return L


def save_ledger(deal, L, event=None):
    if event:
        L.setdefault("history", []).append(dict(event, at=NOW.isoformat(timespec="minutes")))
    L["updated"] = TODAY.isoformat()
    wjson(os.path.join(deal, LEDGER), L)


def owner_sc(deal, L=None):
    L = L if L is not None else load_ledger(deal)
    if L.get("sc"):
        return L["sc"]
    suf = os.path.basename(deal).rsplit("-", 1)[-1]
    return suf if suf in TEAM else None


def next_id(L):
    n = max([int(i["id"].split("-")[1]) for i in L["items"] if re.match(r"C-\d+$", i.get("id", ""))] or [0])
    return "C-%03d" % (n + 1)


def us_names(deal):
    names = set()
    for full in TEAM.values():
        names.update([full.lower(), full.split()[0].lower()])
    names.update(["creatio", "creatio team", "we", "us", "sc", "ae"])
    b = rjson(os.path.join(deal, "ae-brief.json")) or {}
    for k in ("ae", "sc"):
        n = (b.get(k) or {}).get("name")
        if n:
            names.update([n.lower(), n.split()[0].lower()])
    cp = rjson(os.path.join(deal, "clickpath", "clickpath-customer.json")) or {}
    L = rjson(os.path.join(deal, LEDGER)) or {}
    if L.get("ae"):
        names.update([L["ae"].lower(), L["ae"].split()[0].lower()])
    for n in creatio_people(deal) + re.findall(r"([A-Z][a-z]+(?: [A-Z][a-z]+)?) \((?:account executive|solution consultant)", cp.get("contact", "")):
        names.update([n.lower(), n.split()[0].lower()])
    return names


_PEOPLE = {}


def creatio_people(deal):
    """Names the deal's own notes mark as ours: 'Name (AE)', 'Name (Creatio)', 'Name (Creatio AE)'."""
    if deal not in _PEOPLE:
        found = set()
        for p in glob.glob(os.path.join(deal, "*.md"))[:40]:
            for m in re.finditer(r"([A-Z][a-z]+ [A-Z][a-z]+) \([^)]{0,20}?\b(?:AE|Creatio|account executive)\b", rtext(p)):
                if m.group(1).split()[0] not in ("The", "Our", "Their", "Ask", "Send"):
                    found.add(m.group(1))
        _PEOPLE[deal] = sorted(found)
    return _PEOPLE[deal]


def ae_name(deal):
    b = rjson(os.path.join(deal, "ae-brief.json")) or {}
    if (b.get("ae") or {}).get("name"):
        return b["ae"]["name"]
    cp = rjson(os.path.join(deal, "clickpath", "clickpath-customer.json")) or {}
    m = re.search(r"([A-Z][a-z]+(?: [A-Z][a-z]+)?) \(account executive", cp.get("contact", ""))
    return m.group(1) if m else None


def side_of(owner, deal):
    """'us' when any of our people (SCs, the deal's AE, 'Creatio') is named; joint items count as ours."""
    o = (owner or "").lower()
    toks = set(re.split(r"[^a-z]+", o))
    us = us_names(deal)
    return "us" if (toks & {n for n in us if " " not in n}) or any(n in o for n in us if " " in n) else "them"


def customer_names(deal):
    names = set()
    for f, keys in (("clickpath/clickpath-customer.json", ("customer",)), ("ae-brief.json", ("deal",)),
                    ("build-plan.json", ("deal",))):
        d = rjson(os.path.join(deal, f)) or {}
        for k in keys:
            if isinstance(d.get(k), str) and len(d[k]) < 40:
                names.add(d[k].lower())
    base = os.path.basename(deal)
    base = re.sub(r"-(rh|wn|fa)$", "", base)
    names.add(base.replace("-", " "))
    names.update(w for w in base.split("-") if len(w) > 4 and w not in ("finance", "group", "bank", "general", "academy", "partners", "credit", "southern", "higher", "education"))
    L = load_ledger(deal)
    names.update(a.lower() for a in L.get("aliases", []))
    return {n for n in names if n}


# ---------- reading a deal folder ----------

def file_date(path):
    m = re.search(r"(20\d\d-\d\d-\d\d)", os.path.basename(path))
    return pdate(m.group(1)) if m else dt.date.fromtimestamp(os.path.getmtime(path))


def last_activity(deal, L):
    best, what, n = None, None, 0
    for dp, dns, fns in os.walk(deal):
        dns[:] = [d for d in dns if d not in ("node_modules", ".angular", "dist", ".git")]
        for f in fns:
            n += 1
            if n > 4000:
                break
            if f.lower() in SKIP_FILES or f.startswith("~$") or f.endswith(".tmp"):
                continue
            try:
                m = os.path.getmtime(os.path.join(dp, f))
            except OSError:
                continue
            if best is None or m > best:
                best, what = m, os.path.relpath(os.path.join(dp, f), deal)
    d = dt.datetime.fromtimestamp(best).date() if best else None
    t = pdate(L.get("last_touch", {}).get("date"))
    if t and (not d or t > d):
        return t, L["last_touch"].get("what", "logged on the desk")
    return d, what


def dates(deal):
    return rjson(os.path.join(deal, "deal-dates.json")) or {}


def demo_info(deal):
    d = dates(deal).get("demo") or {}
    return pdate(d.get("date")), d.get("status")


def plan_approved(deal):
    """Approved build plan: build/approval-pack.json with approved_by, or a *build-plan*.json marked approved."""
    ap = rjson(os.path.join(deal, "build", "approval-pack.json")) or {}
    if ap.get("approved_by"):
        return True, "build/approval-pack.json (%s)" % ap.get("plan", "")
    for p in glob.glob(os.path.join(deal, "*build-plan*.json")):
        j = rjson(p) or {}
        if j.get("approved") is True or j.get("approved_by"):
            return True, os.path.basename(p)
    return False, None


def has_build_plan(deal):
    return bool(glob.glob(os.path.join(deal, "*build-plan*")) or glob.glob(os.path.join(deal, "*demo-plan*")))


def harvested(deal):
    cat = rjson(os.path.join(PLUGIN, "library", "catalogue.json")) or {}
    base = os.path.basename(deal)
    for m in cat.get("modules", []) + cat.get("candidates", []):
        if m.get("source_deal") in (base, re.sub(r"-(rh|wn|fa)$", "", base)) and m.get("harvested"):
            return pdate(m["harvested"])
    return None


def recap(deal):
    for p in glob.glob(os.path.join(deal, "click*", "clickpath-customer.json")):
        j = rjson(p) or {}
        hold = re.search(r"not to be sent|test (of|only)|don't send|do not send", str(j.get("approved_by", "")), re.I)
        return {"approved": bool(j.get("approved")) and not hold, "approved_by": j.get("approved_by"), "sent": j.get("sent") or j.get("sent_on"),
                "path": os.path.relpath((glob.glob(os.path.join(os.path.dirname(p), "*click-path-customer.html")) or [p])[0], deal)}
    return None


def closeness(deal):
    """How close the deal is to the customer's decision, worked out now from the folder (0-4). Never stored."""
    demo, st = demo_info(deal)
    if glob.glob(os.path.join(deal, "*proposal*")) or os.path.isdir(os.path.join(deal, "rfp")):
        return 4, "RFP or proposal"
    if st == "done" or (demo and demo < TODAY and st != "cancelled"):
        return 3, "after the demo"
    if demo and st in (None, "planned", "moved"):
        return 2, "demo booked"
    if reviews(deal) or glob.glob(os.path.join(deal, "*transcript*demo*")):
        return 2, "after a meeting"
    if glob.glob(os.path.join(deal, "*fm-prep*")) or glob.glob(os.path.join(deal, "deck.json")) or glob.glob(os.path.join(deal, "*W1*")):
        return 1, "first meeting"
    return 0, "early"


def reviews(deal):
    return sorted(glob.glob(os.path.join(deal, "*meeting-review*.md")), key=file_date)


# ---------- capture ----------

def table_after(text, heading_re):
    m = re.search(heading_re, text, re.I | re.M)
    if not m:
        return []
    rows, started = [], False
    for line in text[m.end():].splitlines():
        s = line.strip()
        if s.startswith("|"):
            started = True
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            rows.append(cells)
        elif started and s:
            break
        elif started and not s:
            break
    return rows[1:] if rows else []


def strip_md(s):
    return re.sub(r"\*\*|`|_", "", s or "").strip()


def candidates(deal):
    out = []
    for p in reviews(deal):
        ref = file_date(p)
        for r in table_after(rtext(p), r"^#+\s*\d*\.?\s*Commitments\b.*$"):
            if len(r) >= 2 and r[0]:
                out.append({"what": strip_md(r[0]), "owner": strip_md(r[1]), "due_text": strip_md(r[2]) if len(r) > 2 else "",
                            "ref": ref, "source": "%s (Commitments)" % os.path.basename(p)})
    dk = rjson(os.path.join(deal, "deck.json")) or {}
    dkp = os.path.join(deal, "deck.json")
    for s in dk.get("slides", []):
        if s.get("type") == "next_steps":
            ref = dt.date.fromtimestamp(os.path.getmtime(dkp))
            for a in s.get("actions", []):
                out.append({"what": a.get("what", ""), "owner": a.get("who", ""), "due_text": a.get("when", ""), "ref": ref,
                            "source": "deck.json next steps (proposed on the slide: keep only what was agreed)"})
    b = rjson(os.path.join(deal, "ae-brief.json")) or {}
    ns = b.get("next_step") or {}
    if ns.get("what"):
        p = os.path.join(deal, "ae-brief.json")
        out.append({"what": ns["what"], "owner": ns.get("who", ""), "due_text": "", "ref": dt.date.fromtimestamp(os.path.getmtime(p)),
                    "source": "ae-brief.json next step (suggested: keep only if they agreed)"})
    for p in glob.glob(os.path.join(deal, "*follow*up*.md")) + glob.glob(os.path.join(deal, "*email*.md")):
        if re.search(r"(customer-email|transcript)", os.path.basename(p)):
            continue
        ref = file_date(p)
        flat = re.sub(r"\s*\n\s*", " ", rtext(p))
        for m in re.finditer(r"\b(?:I'll|I will|we'll|we will)\s+([^.;?!]{12,160})", flat, re.I):
            if len(m.group(1).split()) >= 4:
                out.append({"what": m.group(1).strip(), "owner": owner_sc(deal) and TEAM[owner_sc(deal)].split()[0] or "SC",
                            "due_text": "", "ref": ref, "source": "%s (promise in the draft)" % os.path.basename(p)})
    return out


def c_capture(a):
    root = team_root(a.root)
    deal = guard_deal(resolve_deal(root, a.deal))
    L = load_ledger(deal)
    cands, seen = [], []
    for c in candidates(deal):
        if any(similar(c["what"], i["what"]) for i in L["items"]) or any(similar(c["what"], s["what"]) for s in seen):
            continue
        seen.append(c)
        due = parse_due(c["due_text"], c["ref"])
        c.update(due=iso(due), side=side_of(c["owner"], deal))
        cands.append(c)
    if not cands:
        print("%s: nothing new to capture (%d already on the ledger)" % (L["deal"], len(L["items"])))
        return
    pick = None
    if a.pick:
        pick = {int(x) for x in a.pick.split(",") if x.strip()}
    for n, c in enumerate(cands, 1):
        print("%2d. [%s] %s · owner %s · due %s%s · from %s" % (n, c["side"], c["what"], c["owner"] or "?",
              c["due"] or "no date", " (from '%s')" % c["due_text"] if c["due_text"] else "", c["source"]))
    if not a.apply:
        print("\nDry run. Confirm with the SC, then: desk.py capture --deal %s --apply [--pick 1,2,...]" % os.path.basename(deal))
        return
    added = 0
    for n, c in enumerate(cands, 1):
        if pick and n not in pick:
            continue
        L["items"].append({"id": next_id(L), "deal": L["deal"], "what": c["what"], "owner": c["owner"], "side": c["side"],
                           "due": c["due"], "due_text": c["due_text"], "source": c["source"], "status": "open",
                           "added": TODAY.isoformat()})
        added += 1
    save_ledger(deal, L, {"event": "capture", "added": added})
    print("%s: %d added to %s" % (L["deal"], added, LEDGER))


# ---------- ledger commands ----------

def c_add(a):
    root = team_root(a.root)
    deal = guard_deal(resolve_deal(root, a.deal))
    L = load_ledger(deal)
    due = pdate(a.due) if a.due else parse_due(a.due_text, TODAY)
    if a.due and not due:
        sys.exit("--due must be yyyy-mm-dd")
    it = {"id": next_id(L), "deal": L["deal"], "what": a.what, "owner": a.owner, "side": a.side or side_of(a.owner, deal),
          "due": iso(due), "due_text": a.due_text or "", "source": a.source or "chat", "status": "open", "added": TODAY.isoformat()}
    L["items"].append(it)
    L["last_touch"] = {"date": TODAY.isoformat(), "what": "commitment added"}
    save_ledger(deal, L, {"event": "add", "id": it["id"]})
    print("%s %s: %s · %s · due %s" % (L["deal"], it["id"], it["what"], it["owner"], it["due"] or "no date (ask the SC)"))


def my_deals(root, sc, include_unassigned=True):
    out = []
    for d in all_deals(root):
        o = owner_sc(d)
        if o == sc or (include_unassigned and sc == LEAD and o is None):
            out.append(d)
    return out


def c_done(a, status="done"):
    root = team_root(a.root)
    deals = [guard_deal(resolve_deal(root, a.deal))] if a.deal else my_deals(root, my_sc(a.sc))
    hits = []
    for d in deals:
        L = load_ledger(d)
        for it in L["items"]:
            if it["status"] != "open":
                continue
            if (a.id and it["id"] == a.id) or (a.match and (similar(a.match, it["what"]) or
                                                             set(norm(a.match)) <= set(norm(it["what"])))):
                hits.append((d, L, it))
    if not hits:
        sys.exit("No open commitment matches '%s'. Run: desk.py list" % (a.match or a.id))
    if len(hits) > 1 and not a.id:
        print("More than one match: pick one with --deal and --id")
        for d, L, it in hits:
            print("  %s %s: %s (%s)" % (L["deal"], it["id"], it["what"], it["owner"]))
        sys.exit(2)
    d, L, it = hits[0]
    it.update(status=status, closed=TODAY.isoformat(), closed_note=a.note or "")
    L["last_touch"] = {"date": TODAY.isoformat(), "what": "%s: %s" % (status, it["what"])}
    save_ledger(d, L, {"event": status, "id": it["id"]})
    print("%s %s %s: %s" % (L["deal"], it["id"], status, it["what"]))


def c_list(a):
    root = team_root(a.root)
    deals = [guard_deal(resolve_deal(root, a.deal))] if a.deal else my_deals(root, my_sc(a.sc))
    for d in deals:
        L = load_ledger(d)
        items = [i for i in L["items"] if a.all or i["status"] == "open"]
        if not items:
            continue
        print("## %s%s" % (L["deal"], " (%s)" % L["status"] if L["status"] != "active" else ""))
        for i in sorted(items, key=lambda i: i.get("due") or "9999"):
            late = pdate(i.get("due")) and pdate(i["due"]) < TODAY and i["status"] == "open"
            print("  %s [%s] %s · %s · due %s%s%s" % (i["id"], i["side"], i["what"], i["owner"], i.get("due") or "no date",
                                                    " OVERDUE" if late else "", "" if i["status"] == "open" else " (%s)" % i["status"]))


def c_meeting(a):
    root = team_root(a.root)
    deal = guard_deal(resolve_deal(root, a.deal))
    L = load_ledger(deal)
    if not pdate(a.date):
        sys.exit("--date must be yyyy-mm-dd")
    L["next_meeting"] = {"date": a.date, "what": a.what, "source": a.source or "chat"}
    L["last_touch"] = {"date": TODAY.isoformat(), "what": "next meeting booked"}
    save_ledger(deal, L, {"event": "meeting", "date": a.date})
    print("%s: next meeting %s, %s" % (L["deal"], a.date, a.what))


def c_touch(a):
    root = team_root(a.root)
    deal = guard_deal(resolve_deal(root, a.deal))
    L = load_ledger(deal)
    d = a.date or TODAY.isoformat()
    L["last_touch"] = {"date": d, "what": a.what}
    if a.recap_sent:
        L["recap_sent"] = {"date": d, "source": a.what}
    save_ledger(deal, L, {"event": "touch", "what": a.what, "date": d})
    print("%s: activity %s, %s%s" % (L["deal"], d, a.what, " (recap marked sent)" if a.recap_sent else ""))


def c_status(a):
    root = team_root(a.root)
    deal = guard_deal(resolve_deal(root, a.deal))
    L = load_ledger(deal)
    L["status"] = a.set
    L["parked_until"] = a.until if a.set == "parked" else None
    L["status_note"] = a.note or ""
    save_ledger(deal, L, {"event": "status", "status": a.set, "until": a.until})
    print("%s: desk status %s%s" % (L["deal"], a.set, " until %s" % a.until if a.until else ""))


def c_owner(a):
    root = team_root(a.root)
    deal = guard_deal(resolve_deal(root, a.deal))
    if a.sc not in TEAM:
        sys.exit("--sc must be one of %s" % ", ".join(TEAM))
    if me() != LEAD:
        sys.exit("Only Renzo sets who owns a deal on the desk: ask him.")
    L = load_ledger(deal)
    L["sc"] = a.sc
    save_ledger(deal, L, {"event": "owner", "sc": a.sc})
    print("%s: SC %s" % (L["deal"], TEAM[a.sc]))


# ---------- stall detection ----------

def preview_items(deal, L):
    """Capture candidates not yet on the ledger, shown as if captured (read-only preview, nothing written)."""
    out, n = [], 0
    for c in candidates(deal):
        if any(similar(c["what"], i["what"]) for i in L["items"] + out):
            continue
        if c["source"].startswith(("deck.json", "ae-brief.json")):
            continue  # proposals on a slide, not agreed commitments
        n += 1
        out.append({"id": "new-%d" % n, "deal": L["deal"], "what": c["what"], "owner": c["owner"], "side": side_of(c["owner"], deal),
                    "due": iso(parse_due(c["due_text"], c["ref"])), "due_text": c["due_text"], "source": c["source"],
                    "status": "open", "preview": True})
    return out


def scan_deal(deal, calendar=None, preview=False):
    L = load_ledger(deal)
    if preview:
        L["items"] = L["items"] + preview_items(deal, L)
    base = os.path.basename(deal)
    r = {"deal": base, "sc": owner_sc(deal, L), "status": L["status"], "stalls": [], "open": [], "info": {}}
    close, why = closeness(deal)
    r["close"], r["close_why"] = close, why
    last, lastf = last_activity(deal, L)
    r["info"]["last_activity"], r["info"]["last_file"] = iso(last), lastf
    idle = (TODAY - last).days if last else None
    demo, dstat = demo_info(deal)
    r["info"]["demo"], r["info"]["demo_status"] = iso(demo), dstat
    if L["status"] == "closed":
        return r
    if L["status"] == "parked":
        pu = pdate(L.get("parked_until"))
        if pu and pu <= TODAY:
            r["stalls"].append({"kind": "unpark", "text": "Parked until %s: time to pick it up again" % pu, "due": iso(pu)})
        return r

    def stall(kind, text, due=None, owner="us", item=None):
        r["stalls"].append({"kind": kind, "text": text, "due": iso(due), "owner": owner, "item": item})

    for it in L["items"]:
        if it["status"] != "open":
            continue
        r["open"].append(it)
        due = pdate(it.get("due"))
        if due and due < TODAY:
            stall("overdue_ours" if it["side"] == "us" else "overdue_theirs",
                  "%s %s (%s, due %s, %s late)" % ("Overdue:" if it["side"] == "us" else "They owe:", it["what"], it["owner"],
                                                       due, plural((TODAY - due).days, "day")), due, it["side"], it["id"])
    future = []
    if demo and dstat in (None, "planned", "moved") and demo >= TODAY:
        future.append(demo)
        ok, src = plan_approved(deal)
        r["info"]["plan_approved"] = src
        if (demo - TODAY).days <= DEMO_PLAN_DAYS and not ok:
            stall("demo_no_plan", "Demo %s (%s) and no approved build plan%s" % (demo, "today" if demo == TODAY else "in %s" % plural((demo - TODAY).days, "day"),
                  "" if has_build_plan(deal) else " (no plan at all)"), demo)
    if demo and (dstat == "done" or (dstat in (None, "planned") and demo < TODAY)):
        hv = harvested(deal)
        due = add_wd(demo, HARVEST_WD)
        if not hv and TODAY > due:
            stall("harvest", "Harvest overdue: demo %s, due %s (%d working days late)" % (demo, due, wd_between(due, TODAY)), due)
        if dstat in (None, "planned") and demo < TODAY:
            stall("demo_date", "Demo date %s has passed but isn't marked done or moved" % demo, demo)
    rc = recap(deal)
    if rc and rc["approved"] and not rc["sent"] and not L.get("recap_sent"):
        stall("recap", "Customer recap approved (%s) but not marked sent" % (rc["approved_by"] or "yes"))
    nm = pdate((L.get("next_meeting") or {}).get("date"))
    if nm and nm >= TODAY:
        future.append(nm)
    for ev in calendar or []:
        if ev.get("deal") == base and pdate(ev.get("start")) and pdate(ev["start"]) >= TODAY:
            future.append(pdate(ev["start"]))
    r["info"]["next_meeting"] = iso(min(future)) if future else None
    if future and min(future) <= add_wd(TODAY, 2):
        nm_d = min(future)
        ok, gaps = prep_status(deal, "demo" if nm_d == demo else "meeting")
        if any(x["kind"] == "demo_no_plan" for x in r["stalls"]):
            gaps = [g for g in gaps if "build plan" not in g]
        if gaps:
            stall("prep", "%s %s: %s" % ("Demo" if nm_d == demo else "Meeting", nm_d.strftime("%a %d %b"), ", ".join(gaps)), nm_d)
    if idle is not None and idle >= PARK_HINT_DAYS and not future and not r["open"]:
        stall("park_hint", "No activity for %d days and nothing ahead: still live, or park it?" % idle)
        return r
    if idle is not None and idle >= STALE_DAYS:
        stall("idle", "No activity for %d days (last: %s, %s)" % (idle, last, lastf))
    if not future:
        stall("no_meeting", "No next meeting on record")
    for it in r["open"]:
        if not it.get("due") and it["side"] == "us":
            stall("no_date", "No due date: %s (%s)" % (it["what"], it["owner"]), None, "us", it["id"])
    return r


def match_calendar(root, events):
    if not events:
        return []
    names = {os.path.basename(d): customer_names(d) for d in all_deals(root)}
    for ev in events:
        hay = " ".join([ev.get("subject", ""), ev.get("location", ""), " ".join(ev.get("attendees", []))]).lower()
        best = None
        for deal, ns in names.items():
            for n in ns:
                if len(n) >= 4 and re.search(r"\b%s\b" % re.escape(n), hay):
                    if not best or len(n) > best[1]:
                        best = (deal, len(n))
        ev["deal"] = best[0] if best else None
    return events


def load_calendar(root, path):
    if not path:
        return []
    ev = rjson(path)
    if ev is None:
        sys.exit("Can't read the calendar file %s" % path)
    if isinstance(ev, dict):
        ev = ev.get("events") or ev.get("value") or []
    return match_calendar(root, ev)


def c_scan(a):
    root = team_root(a.root)
    deals = [guard_deal(resolve_deal(root, a.deal))] if a.deal else my_deals(root, my_sc(a.sc))
    cal = load_calendar(root, getattr(a, "calendar", None))
    res = [scan_deal(d, cal, a.preview) for d in deals]
    if a.json:
        print(json.dumps(res, indent=1, ensure_ascii=False, default=str))
        return
    for r in res:
        flag = "" if r["stalls"] else " OK"
        print("## %s · %s · SC %s%s" % (r["deal"], r["close_why"], r["sc"] or "not set", flag))
        for s in r["stalls"]:
            print("  - %s" % s["text"])


# ---------- daily brief ----------

SCORE = {"demo_no_plan": 95, "prep": 90, "overdue_ours": 85, "recap": 70, "harvest": 65, "due_soon": 60, "overdue_theirs": 55,
         "demo_date": 50, "unpark": 45, "idle": 40, "no_meeting": 35, "no_date": 20}


def rank(stalls_by_deal):
    acts = []
    for r in stalls_by_deal:
        for s in r["stalls"]:
            if s["kind"] == "park_hint":
                continue
            base = SCORE.get(s["kind"], 30)
            due = pdate(s.get("due"))
            urg = 0
            if due:
                urg = min(15, max(-10, (TODAY - due).days)) if due < TODAY else max(0, 10 - (due - TODAY).days)
            acts.append(dict(s, deal=r["deal"], score=base + urg + 4 * r["close"], close_why=r["close_why"]))
        for it in r["open"]:
            due = pdate(it.get("due"))
            if it["side"] == "us" and due and TODAY <= due <= add_wd(TODAY, 2):
                acts.append({"kind": "due_soon", "deal": r["deal"], "text": "Due %s: %s (%s)" % ("today" if due == TODAY else due, it["what"], it["owner"]),
                             "due": iso(due), "score": SCORE["due_soon"] + 10 - (due - TODAY).days + 4 * r["close"], "close_why": r["close_why"], "item": it["id"]})
    return sorted(acts, key=lambda x: -x["score"])


ACTION = {"demo_no_plan": "Finish the build plan and get it approved (`sc-demo-plan`), or move the demo",
          "overdue_ours": "Do it today, or agree a new date with the AE (`desk.py add` the new one, `drop` the old)",
          "overdue_theirs": "Nudge through the AE: draft below",
          "recap": "Send the approved recap with the AE (draft below), then `desk.py touch --recap-sent`",
          "harvest": "Run `sc-harvest` (L1, about 30 minutes)",
          "demo_date": "Mark it done (`deal_dates.py set --field demo --status done`) or set the new date",
          "idle": "Decide the next move with the AE: draft below",
          "no_meeting": "Ask the AE to book the next session: draft below",
          "no_date": "Give it a date (`desk.py add` again with `--due`, then `drop` this one)",
          "due_soon": "On today's list",
          "unpark": "Is it live again? Say so and I'll set it active",
          "prep": "Close the prep gaps before the meeting"}


def prep_status(deal, kind):
    gaps, ok = [], []
    pptx = [p for p in glob.glob(os.path.join(deal, "*.pptx"))]
    rv = reviews(deal)
    latest_rv = os.path.getmtime(rv[-1]) if rv else 0
    if pptx and max(os.path.getmtime(p) for p in pptx) >= latest_rv:
        ok.append("deck newer than the last review")
    else:
        gaps.append("deck not updated since the last review" if pptx else "no deck")
    if kind == "demo":
        a, src = plan_approved(deal)
        (ok if a else gaps).append("build plan approved" if a else "build plan not approved")
        if glob.glob(os.path.join(deal, "*rehearsal*")):
            ok.append("rehearsal notes")
        else:
            gaps.append("no rehearsal notes")
        if glob.glob(os.path.join(deal, "*reset*")):
            ok.append("reset file")
    if os.path.exists(os.path.join(deal, "ae-brief.json")) or glob.glob(os.path.join(deal, "*ae-brief*")):
        ok.append("AE brief")
    else:
        gaps.append("no AE brief (`sc-demo-plan` build_ae_brief.py)")
    return ok, gaps


def todays_meetings(root, deals, cal):
    out = []
    names = {os.path.basename(d): d for d in deals}
    for ev in cal:
        s = ev.get("start", "")
        if pdate(s) == TODAY:
            d = names.get(ev.get("deal"))
            if not d:
                continue  # personal or internal: not shown (counted below)
            ok, gaps = prep_status(d, "demo" if re.search(r"demo", ev.get("subject", ""), re.I) else "meeting") if d else ([], [])
            out.append({"time": s[11:16], "subject": ev.get("subject", ""), "deal": ev.get("deal"), "ok": ok, "gaps": gaps})
    for d in deals:
        demo, st = demo_info(d)
        nm = pdate((load_ledger(d).get("next_meeting") or {}).get("date"))
        b = os.path.basename(d)
        if any(m["deal"] == b for m in out):
            continue
        if demo == TODAY and st in (None, "planned", "moved"):
            ok, gaps = prep_status(d, "demo")
            out.append({"time": "", "subject": "Demo (deal-dates.json)", "deal": b, "ok": ok, "gaps": gaps})
        elif nm == TODAY:
            ok, gaps = prep_status(d, "meeting")
            out.append({"time": "", "subject": load_ledger(d)["next_meeting"].get("what", "Meeting"), "deal": b, "ok": ok, "gaps": gaps})
    return sorted(out, key=lambda m: m["time"] or "99")


def draft_followup(deal, r, sc):
    """A starting draft for the SC to rework. Never sent: the SC (or the AE) sends it."""
    kinds = {s["kind"] for s in r["stalls"]}
    if not kinds & {"overdue_theirs", "recap", "idle", "no_meeting"}:
        return None
    ae = ae_name(deal) or "<AE>"
    me = TEAM.get(sc, "<SC>").split()[0]
    acct = re.sub(r"-(rh|wn|fa)$", "", r["deal"]).replace("-", " ").title()
    ours = [i for i in r["open"] if i["side"] == "us"]
    theirs = [i for i in r["open"] if i["side"] == "them"]
    lines = ["**To:** %s (internal, so you can forward or adapt it) · **Subject:** %s: next step" % (ae, acct), "",
             "Hi %s," % ae.split()[0], ""]
    if "recap" in kinds:
        lines += ["The recap of what %s saw is approved and ready (`%s`). Can you send it to them with a short note, or shall I draft that note for you?" % (acct, (recap(deal) or {}).get("path", "recap")), ""]
    if theirs:
        lines += ["We're still waiting on %s:" % acct] + ["- %s (%s%s)" % (i["what"], i["owner"], ", due %s" % i["due"] if i.get("due") else "") for i in theirs[:4]] + \
                 ["Could you check in with them this week? A one-line nudge is enough.", ""]
    if ours:
        lines += ["On our side:"] + ["- %s (%s%s)" % (i["what"], i["owner"], ", due %s" % i["due"] if i.get("due") else "") for i in ours[:4]] + [""]
    if "no_meeting" in kinds or "idle" in kinds:
        lines += ["We don't have the next session with them booked. Could you propose two times for the next step?", ""]
    lines += ["Thanks,", me, "", "_%s Please also update your CRM if the deal has moved._" % CHECK]
    return "\n".join(lines)


def c_brief(a):
    root = team_root(a.root)
    sc = my_sc(a.sc)
    deals = my_deals(root, sc)
    cal = load_calendar(root, a.calendar)
    scans = [scan_deal(d, cal, a.preview) for d in deals]
    acts = rank(scans)
    by = {os.path.basename(d): d for d in deals}
    L = ["# What's on today: %s, %s" % (TEAM.get(sc, sc or "SC"), TODAY.strftime("%a %d %b %Y")), ""]
    unassigned = [r["deal"] for r in scans if not r["sc"]]
    parked_q = [r for r in scans if any(s["kind"] == "park_hint" for s in r["stalls"])]
    no_date = [s for x in acts if x["kind"] == "no_date" for s in [x]]
    qs = []
    if unassigned:
        qs.append("These deal folders have no SC set. Which are yours? %s" % ", ".join(unassigned))
    if parked_q:
        qs.append("No activity for 3+ weeks and nothing booked. Still live, or park them (and until when)? %s" % ", ".join(r["deal"] for r in parked_q))
    if no_date:
        qs.append("%d of our commitments have no due date. Give each a date (listed under Open commitments)" % len(no_date))
    L += ["## Questions"] + (["%d. %s" % (n, q) for n, q in enumerate(qs, 1)] or ["No questions"]) + [""]
    L += ["## Top 5 actions", "", "| # | Deal | What | Next move |", "|---|---|---|---|"]
    for n, x in enumerate([x for x in acts if x["kind"] != "no_date"][:5], 1):
        L.append("| %d | %s | %s | %s |" % (n, x["deal"], x["text"], ACTION.get(x["kind"], "")))
    rest = len([x for x in acts if x["kind"] != "no_date"]) - 5
    if rest > 0:
        L.append("\n%d more below the line (run `desk.py scan` for all)." % rest)
    L += ["", "Ranked by deadline and how close the deal is to the customer's decision.", ""]
    meets = todays_meetings(root, deals, cal)
    L += ["## Today's meetings", ""]
    if not cal:
        L.append("_Calendar not connected: meetings from the deal folders only. Connect Microsoft 365 (read-only) to see your Outlook day._")
    if meets:
        L += ["| Time | Meeting | Deal | Ready | Gaps |", "|---|---|---|---|---|"]
        for m in meets:
            L.append("| %s | %s | %s | %s | %s |" % (m["time"] or "?", m["subject"], m["deal"] or "not matched", ", ".join(m["ok"]) or "-", ", ".join(m["gaps"]) or "none"))
    else:
        L.append("No customer meetings today on record.")
    other = len([e for e in cal if pdate(e.get("start")) == TODAY and not e.get("deal")])
    if other:
        L.append("%d other calendar item%s today not linked to a deal (not shown)." % (other, "" if other == 1 else "s"))
    L += [""]
    ahead = sorted([(r["info"]["next_meeting"], r["deal"]) for r in scans if r["info"].get("next_meeting")])[:5]
    if ahead:
        L += ["**Coming up:** " + " · ".join("%s %s" % (pdate(d).strftime("%a %d %b"), n) for d, n in ahead), ""]
    L += ["## Follow-up drafts (never sent automatically)", ""]
    nd = 0
    MAXD = 3
    drafted = []
    for r in sorted(scans, key=lambda r: -max([x["score"] for x in acts if x["deal"] == r["deal"]] or [0])):
        if len(drafted) >= MAXD:
            break
        if r["status"] != "active" or any(s["kind"] == "park_hint" for s in r["stalls"]):
            continue
        kinds = {s["kind"] for s in r["stalls"]}
        if not (kinds & {"overdue_theirs", "recap", "idle"} or ("no_meeting" in kinds and r["close"] >= 2)):
            continue
        dr = draft_followup(by[r["deal"]], r, sc)
        if dr:
            nd += 1
            drafted.append(r["deal"])
            L += ["### %s" % r["deal"], "Why: " + "; ".join(s["text"] for s in r["stalls"] if s["kind"] in ("overdue_theirs", "recap", "idle", "no_meeting")), "", dr, ""]
    if not nd:
        L += ["None today.", ""]
    L += ["## Open commitments", ""]
    anyc = False
    for r in scans:
        for i in sorted(r["open"], key=lambda i: i.get("due") or "9999"):
            anyc = True
            late = pdate(i.get("due")) and pdate(i["due"]) < TODAY
            L.append("- %s %s [%s] %s · %s · %s%s%s" % (r["deal"], i["id"], i["side"], i["what"], i["owner"], i.get("due") or "**no date**",
                                                   " (from '%s')" % i["due_text"] if i.get("due_text") and i.get("due") else "",
                                                   " **overdue**" if late else "") + (" · _preview: from %s, not on the ledger yet_" % i["source"] if i.get("preview") else ""))
    if not anyc:
        L.append("None on the ledger yet. After each meeting review I capture them; or say \"add: <what> for <deal>, <owner>, <date>\".")
    L += ["", "Close one with \"done: <what>\". The desk tracks our tasks only: pipeline stage, forecast and value stay in the AE's CRM.", ""]
    md = "\n".join(L)
    print(md)
    if not a.no_write:
        out = a.out or os.path.join(os.path.expanduser("~"), ".apac-sc-motion", "desk", "%s-brief.md" % TODAY.isoformat())
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(md)
        print("\n-> %s" % out, file=sys.stderr)


# ---------- load check ----------

def week_bounds(spec):
    if spec:
        y, w = spec.split("-W")
        mon = dt.date.fromisocalendar(int(y), int(w), 1)
    else:
        mon = TODAY - dt.timedelta(days=TODAY.weekday())
        if TODAY.weekday() >= 5:
            mon += dt.timedelta(days=7)
    return mon, mon + dt.timedelta(days=4)


def build_hours(deal, mon, fri):
    """Build hours left this week: the approval pack's items not yet logged done in build/build-log.jsonl.
    Spread evenly over the weeks until the demo when a later demo is booked; otherwise all in this week."""
    ap = rjson(os.path.join(deal, "build", "approval-pack.json")) or {}
    items = ap.get("items") or []
    if not items:
        return 0.0
    done = set()
    try:
        for line in open(os.path.join(deal, "build", "build-log.jsonl"), encoding="utf-8"):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("kind") in ("done", "skipped") and e.get("item"):
                done.add(e["item"])
    except OSError:
        pass
    left = sum(float(i.get("hours") or 0) for i in items if i.get("id") not in done)
    if not left:
        return 0.0
    demo, st = demo_info(deal)
    if demo and st in (None, "planned", "moved") and demo > fri:
        weeks = max(1, -(-(demo - mon).days // 7))
        return round(left / weeks, 1)
    return left


def load_for(root, sc, mon, fri, cal):
    deals = my_deals(root, sc, include_unassigned=(sc == my_sc()))
    rows, demos_by_day = [], {}
    demos = meetings = 0
    hours = 0.0
    due_ours = 0
    for d in deals:
        b = os.path.basename(d)
        Ld = load_ledger(d)
        if Ld["status"] != "active":
            continue
        demo, st = demo_info(d)
        if demo and mon <= demo <= fri and st in (None, "planned", "moved"):
            demos += 1
            demos_by_day.setdefault(demo, []).append(b)
            rows.append((demo, b, "demo", closeness(d)[0]))
        nm = pdate((Ld.get("next_meeting") or {}).get("date"))
        if nm and mon <= nm <= fri and nm != demo:
            meetings += 1
            rows.append((nm, b, "meeting", closeness(d)[0]))
        h = build_hours(d, mon, fri)
        if h:
            hours += h
            rows.append((None, b, "build %.0f h" % h, closeness(d)[0]))
        for i in Ld["items"]:
            if i["status"] == "open" and i["side"] == "us" and pdate(i.get("due")) and mon <= pdate(i["due"]) <= fri:
                due_ours += 1
    if sc == my_sc():
        for ev in cal:
            s = pdate(ev.get("start"))
            if s and mon <= s <= fri and ev.get("deal") and not any(r[0] == s and r[1] == ev["deal"] for r in rows):
                meetings += 1
                rows.append((s, ev["deal"], "meeting (calendar)", 0))
    return {"sc": sc, "demos": demos, "customer_meetings": meetings + demos, "build_hours": round(hours, 1), "due_ours": due_ours,
            "same_day_demos": max([len(v) for v in demos_by_day.values()] or [0]), "rows": rows, "by_day": demos_by_day}


def load_check(root, sc, spec=None, cal=None):
    mon, fri = week_bounds(spec)
    me = load_for(root, sc, mon, fri, cal or [])
    others = {s: load_for(root, s, mon, fri, []) for s in TEAM if s != sc}
    over = [(k, me[k], v) for k, v in LOAD.items() if me[k] > v]
    L = ["## Load check: week of %s" % mon.strftime("%d %b"), "",
         "| Measure | You | Limit |", "|---|---|---|"]
    for k, v in LOAD.items():
        L.append("| %s | %s | %s |" % (k.replace("_", " "), me[k], v))
    if not over:
        L += ["", "Fine: nothing over the limits."]
        return "\n".join(L), me, over
    L += ["", "**Overloaded:** " + ", ".join("%s %s (limit %s)" % (k.replace("_", " "), n, v) for k, n, v in over), ""]
    keys = {k for k, _, _ in over}
    light = min(others.items(), key=lambda kv: (kv[1]["build_hours"] + 4 * kv[1]["demos"]))
    builds = sorted([r for r in me["rows"] if r[2].startswith("build")], key=lambda r: r[3])
    if "build_hours" in keys and builds:
        r = builds[0]
        L.append("- **Move build work:** on %s (%s), do only what the next customer session needs this week; the rest goes to next week. "
                 "The deal furthest from a decision goes first." % (r[1], r[2]))
        if me() == LEAD:
            L.append("- **Or hand over:** build items on %s to %s (this week: %s h build, %d demos). You keep the demo; they build from the "
                     "approved plan and its approval pack." % (r[1], TEAM[light[0]], light[1]["build_hours"], light[1]["demos"]))
        else:
            L.append("- **Or hand over:** ask Renzo who has room for build items on %s. You keep the demo; they build from the "
                     "approved plan and its approval pack." % r[1])
    if keys & {"demos", "customer_meetings", "same_day_demos"}:
        soon = add_wd(TODAY, 2)
        movable = sorted([r for r in me["rows"] if r[0] and r[0] > soon and not r[2].startswith("build")], key=lambda r: r[3])
        if movable:
            r = movable[0]
            L.append("- **Move:** %s %s on %s, the deal furthest from a decision. Ask the AE for a date the week after." %
                     (r[1], r[2], r[0].strftime("%a %d %b")))
        else:
            L.append("- Everything is within 2 working days: don't move customer sessions this late; hand over build work instead.")
    if "due_ours" in keys:
        L.append("- **Commitments:** %d of ours are due this week. Ask the AE to take the ones they own, and re-date the rest." % me["due_ours"])
    for day, ds in me["by_day"].items():
        if len(ds) > LOAD["same_day_demos"]:
            L.append("- %s has %d demos (%s): move one." % (day.strftime("%a %d %b"), len(ds), ", ".join(ds)))
    L.append("- Suggestions only: you and the AE decide; tell the customer through the AE.")
    return "\n".join(L), me, over


def c_load(a):
    root = team_root(a.root)
    md, me, over = load_check(root, my_sc(a.sc), a.week, load_calendar(root, a.calendar))
    print(md)


# ---------- weekly view ----------

def health(r):
    k = {s["kind"] for s in r["stalls"]}
    if r["status"] != "active":
        return "parked" if r["status"] == "parked" else "closed"
    if k & {"overdue_ours", "demo_no_plan", "harvest"}:
        return "red"
    if k - {"no_date"}:
        return "amber"
    return "green"


def demo_bar(deal):
    plans = sorted(glob.glob(os.path.join(deal, "*demo-plan*.md")), key=os.path.getmtime)
    if not plans:
        return None
    """(items met or planned, items) from the latest plan's Demo bar check table. A gap or 'partly' counts against."""
    rows = table_after(rtext(plans[-1]), r"^#+\s*\d*\.?\s*Demo bar check.*$")
    ok = tot = 0
    for r in rows:
        st = " ".join(r[1:]).lower().replace("*", "")
        m = re.search(r"\b(met|planned|gap|partly|missing|not met)\b", st)
        if not m:
            continue
        tot += 1
        ok += m.group(1) in ("met", "planned")
    return (ok, tot) if tot else None


def answers_added(root, days=7):
    """Approved answers added to the team's explanations library in the last week (about answers, not people)."""
    j = rjson(os.path.join(root, "Lessons", "registers", "explanations.json")) or {}
    entries = j.get("entries", j) if isinstance(j, dict) else j
    since = TODAY - dt.timedelta(days=days)
    n = tot = 0
    for e in entries if isinstance(entries, list) else []:
        if e.get("status") == "approved":
            tot += 1
            if pdate(e.get("approved_on")) and pdate(e["approved_on"]) >= since:
                n += 1
    return n, tot


def harvest_on_time(deal):
    demo, st = demo_info(deal)
    if not demo or st != "done" or TODAY <= add_wd(demo, HARVEST_WD):
        return None
    hv = harvested(deal)
    return bool(hv and hv <= add_wd(demo, HARVEST_WD))


def timing():
    sys.path.insert(0, os.path.join(HERE, "..", "..", "sc-guide", "scripts"))
    try:
        import deal_dates  # noqa
    except Exception:
        return {}
    root = team_root()
    vals = {"call_to_sc": [], "sc_to_demo": [], "call_to_demo": []}
    for d in all_deals(root):
        j = dates(d)
        f, s, m = (j.get(k, {}).get("date") for k in ("first_call", "sc_notified", "demo"))
        for key, (x, y) in (("call_to_sc", (f, s)), ("sc_to_demo", (s, m)), ("call_to_demo", (f, m))):
            v = deal_dates.days(x, y) if x and y else None
            if v is not None:
                vals[key].append(v)
    return {k: (statistics.median(v), len(v)) for k, v in vals.items() if v}


def tips(per_sc, quality):
    out = []
    kinds = {}
    for sc, rows in per_sc.items():
        for r in rows:
            for s in r["stalls"]:
                kinds[s["kind"]] = kinds.get(s["kind"], 0) + 1
    T = {"no_meeting": "Book the next session before you leave the call: put a date on the next-steps slide and ask for it at the close.",
         "idle": "Every Friday, give each live deal one move for next week, even if it's only a nudge through the AE.",
         "overdue_ours": "Put a real date on everything we promise in the meeting review; 'this week' is fine, 'later' isn't.",
         "harvest": "Book 30 minutes for `sc-harvest` in your calendar the day after each demo.",
         "recap": "Send the customer recap within a day of approving it; it's the cheapest follow-up we have.",
         "no_date": "Give every commitment a due date when you capture it.",
         "overdue_theirs": "Agree with the AE who chases what the customer owes, and when.",
         "demo_no_plan": "Get the build plan approved at least 3 days before the demo."}
    for k, n in sorted(kinds.items(), key=lambda kv: -kv[1]):
        if k in T and len(out) < 2:
            out.append("%s (%d this week)" % (T[k], n))
    if len(out) < 2 and quality.get("demo_bar") and quality["demo_bar"][0] < quality["demo_bar"][1]:
        out.append("Close the demo bar gaps in the plan before building (%d of %d items met)." % quality["demo_bar"])
    return out or ["Nothing stalled: keep the Friday habit of one move per deal."]


def c_week(a):
    if me() != LEAD:
        sys.exit("The Friday desk view is Renzo's (it covers every SC). Your own deals are in your daily brief.")
    root = team_root(a.root)
    y, w, _ = TODAY.isocalendar()
    wk = "%d-W%02d" % (y, w)
    per_sc, quality = {}, {}
    for sc in list(TEAM) + [None]:
        rows = [scan_deal(d) for d in all_deals(root) if owner_sc(d) == sc]
        if rows:
            per_sc[sc] = rows
    bar = [demo_bar(d) for d in all_deals(root)]
    bar = [b for b in bar if b]
    if bar:
        quality["demo_bar"] = (sum(b[0] for b in bar), sum(b[1] for b in bar))
    ht = [harvest_on_time(d) for d in all_deals(root)]
    ht = [h for h in ht if h is not None]
    if ht:
        quality["harvest_on_time"] = (sum(ht), len(ht))
    quality["timing"] = timing()
    prev = None
    for p in sorted(glob.glob(os.path.join(root, "Lessons", "desk", "weekly", "*.json"))):
        if os.path.basename(p)[:8] != wk:
            prev = rjson(p)
    L = ["# SC desk: week %s (%s)" % (wk, TODAY.strftime("%d %b %Y")), "",
         "Our task desk, not a CRM: pipeline stage, forecast and value stay in the AEs' CRM. Team totals only: each SC "
         "sees their own deals in their daily brief.", ""]
    P = ["# SC desk by SC, week %s (private: Renzo only, local folder, never SharePoint)" % wk, "",
         "Deals and load only. Coaching isn't here: it stays on each SC's PC and they share what they choose.", ""]
    snap = {"week": wk, "health": {}, "quality": {k: v for k, v in quality.items() if k != "timing"}}
    team_cnt = {}
    for sc, rows in per_sc.items():
        name = TEAM.get(sc, "SC not set")
        cnt = {}
        for r in rows:
            cnt[health(r)] = cnt.get(health(r), 0) + 1
            team_cnt[health(r)] = team_cnt.get(health(r), 0) + 1
        snap["health"][sc or "unset"] = cnt
        P += ["## %s: %s" % (name, " · ".join("%d %s" % (n, h) for h, n in sorted(cnt.items()))), "",
              "| Deal | Health | Why | Next on record |", "|---|---|---|---|"]
        for r in sorted(rows, key=lambda r: ["red", "amber", "green", "parked", "closed"].index(health(r))):
            why = "; ".join(s["text"] for s in r["stalls"][:2]) or "-"
            P.append("| %s | %s | %s | %s |" % (r["deal"], health(r), why, r["info"].get("next_meeting") or "-"))
        P.append("")
        lc, _, _ = load_check(root, sc, None, []) if sc else ("", None, None)
        if lc:
            P += [lc.replace("## Load check", "### Load next week" if TODAY.weekday() >= 4 else "### Load this week"), ""]
    L += ["## Deals by health (team)", "", " · ".join("%d %s" % (team_cnt.get(h, 0), h) for h in ("red", "amber", "green", "parked", "closed")), ""]

    def pct(t):
        return "%d of %d (%d%%)" % (t[0], t[1], round(100 * t[0] / t[1])) if t and t[1] else "n/a"

    def trend(k):
        p = (prev or {}).get("quality", {}).get(k)
        c = quality.get(k)
        if not p or not c or not p[1] or not c[1]:
            return ""
        d = round(100 * c[0] / c[1]) - round(100 * p[0] / p[1])
        return " (%+d pts)" % d if d else " (same)"
    L += ["## Quality trend (team)", "", "| Measure | This week | Source |", "|---|---|---|",
          "| Demo bar items met or planned in the latest plans | %s%s | `*demo-plan*.md` Demo bar check |" % (pct(quality.get("demo_bar")), trend("demo_bar")),
          "| Demos harvested within %d working days | %s%s | `library/catalogue.json` vs deal dates |" % (HARVEST_WD, pct(quality.get("harvest_on_time")), trend("harvest_on_time")),
          "| Approved answers added to the library this week | %d (%d in all) | `Lessons/registers/explanations.json` |" % answers_added(root)]
    for k, lab in (("call_to_sc", "First call → SC notified"), ("sc_to_demo", "SC notified → demo"), ("call_to_demo", "First call → demo")):
        v = quality["timing"].get(k)
        L.append("| %s, median days | %s | `deal-dates.json` |" % (lab, "%g (n=%d)" % v if v else "n/a"))
    L += ["", "## Tips for next week", ""] + ["%d. %s" % (n, t) for n, t in enumerate(tips(per_sc, quality), 1)] + [""]
    md = "\n".join(L)
    print(md)
    if not a.no_write:
        out = os.path.join(root, "Lessons", "desk", "weekly", "%s.md" % wk)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(md)
        wjson(out[:-3] + ".json", snap)
        print("\n-> %s" % out, file=sys.stderr)
    if not a.no_write:
        pout = a.private_out or os.path.join(os.path.expanduser("~"), "SC-Desk")
        os.makedirs(pout, exist_ok=True)
        pf = os.path.join(pout, "desk-%s.md" % wk)
        open(pf, "w", encoding="utf-8").write("\n".join(P) + "\n")
        print("-> %s (private)" % pf, file=sys.stderr)


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("add"); p.add_argument("--deal", required=True); p.add_argument("--what", required=True)
    p.add_argument("--owner", required=True); p.add_argument("--due"); p.add_argument("--due-text", default="")
    p.add_argument("--source"); p.add_argument("--side", choices=["us", "them"])
    for c in ("done", "drop"):
        p = sp.add_parser(c); p.add_argument("--match"); p.add_argument("--id"); p.add_argument("--deal"); p.add_argument("--sc"); p.add_argument("--note")
    p = sp.add_parser("list"); p.add_argument("--deal"); p.add_argument("--sc"); p.add_argument("--all", action="store_true")
    p = sp.add_parser("capture"); p.add_argument("--deal", required=True); p.add_argument("--apply", action="store_true"); p.add_argument("--pick")
    p = sp.add_parser("meeting"); p.add_argument("--deal", required=True); p.add_argument("--date", required=True)
    p.add_argument("--what", required=True); p.add_argument("--source")
    p = sp.add_parser("touch"); p.add_argument("--deal", required=True); p.add_argument("--what", required=True)
    p.add_argument("--date"); p.add_argument("--recap-sent", action="store_true")
    p = sp.add_parser("status"); p.add_argument("--deal", required=True); p.add_argument("--set", required=True, choices=["active", "parked", "closed"])
    p.add_argument("--until"); p.add_argument("--note")
    p = sp.add_parser("owner"); p.add_argument("--deal", required=True); p.add_argument("--sc", required=True)
    p = sp.add_parser("scan"); p.add_argument("--sc"); p.add_argument("--deal"); p.add_argument("--json", action="store_true"); p.add_argument("--calendar")
    p.add_argument("--preview", action="store_true", help="include capture candidates not yet on the ledger (read-only)")
    p = sp.add_parser("brief"); p.add_argument("--sc"); p.add_argument("--calendar"); p.add_argument("--out"); p.add_argument("--no-write", action="store_true")
    p.add_argument("--preview", action="store_true", help="include capture candidates not yet on the ledger (read-only)")
    p = sp.add_parser("week"); p.add_argument("--private-out"); p.add_argument("--no-write", action="store_true")
    p = sp.add_parser("load"); p.add_argument("--sc"); p.add_argument("--week"); p.add_argument("--calendar")
    a = ap.parse_args()
    if a.cmd == "drop" and not (a.deal and a.id):
        sys.exit("drop needs --deal and --id")
    {"add": c_add, "done": c_done, "drop": lambda x: c_done(x, "dropped"), "list": c_list, "capture": c_capture,
     "meeting": c_meeting, "touch": c_touch, "status": c_status, "owner": c_owner, "scan": c_scan, "brief": c_brief,
     "week": c_week, "load": c_load}[a.cmd](a)


if __name__ == "__main__":
    main()
