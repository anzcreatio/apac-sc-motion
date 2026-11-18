"""On-premise infrastructure sizing RECOMMENDATION for a Creatio APAC deal.

The Creatio system requirements calculator is the base; the rules in SIZING-RULES-v0.1.json adjust it (Academy +
Creatio infrastructure team guidance). Outputs are customer-ready but always worded as a recommendation pending
review by Creatio's infrastructure team.

  python sizing.py new      <deal folder> [--customer "Name"]   # writes <deal>/sizing.json
  python sizing.py url      <deal>/sizing.json                   # calculator links per environment
  python sizing.py calc     <deal>/sizing.json [--offline DIR]   # fetch calculator, apply rules -> plan
  python sizing.py storage  <deal>/sizing.json                   # storage plan from volumes
  python sizing.py check    <deal>/sizing.json                   # rules + wording; exit 1 on errors
  python sizing.py build    <deal>/sizing.json --nn 21           # NN-sizing.docx + .xlsx + -internal.md
  python sizing.py review   <deal>/sizing.json --status in_review|infra_reviewed [--by "Name"] [--notes "..."]

Rules: ../../knowledge/SIZING-RULES-v0.1.json. Calculator snapshots are saved in <deal>/sizing/ so the source of
every number can be shown later.
"""
import argparse
import datetime
import json
import math
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
RULES = os.path.join(PLUGIN, "knowledge", "SIZING-RULES-v0.1.json")
CALC_URL = "https://academy.creatio.com/resources/system-requirements-calculator/results"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Calculator option ids (decoded 18 Nov 2026 from the calculator form; re-check if the calculator changes)
OPT = {
    "app": {"netfw": "398", "net": "399"},
    "db": {"mssql": "391", "oracle": "392", "pg": "393"},
    "bulk": {True: "420", False: "421"},
    "scheme": {"simple": "401", "fault_tolerant": "402"},
    "recovery": {"simple": "404", "full": "405"},
    "portal": {True: "414", False: "415"},
    "containers": {True: "417", False: "418"},
    "component": {"global_search": "409", "dedup": "410", "ml": "411", "email_listener": "412"},
}
COMPONENTS = ("global_search", "dedup", "ml", "email_listener", "creatio_ai")
TAGS = ("C", "P", "I", "A")
STATUS = ("draft", "in_review", "infra_reviewed")
ROLE_HEADINGS = {
    "Application server": "app",
    "Database server": "db",
    "Caching server (user sessions)": "redis",
    "Load balancer server (web servers)": "lb",
    "Kubernetes master server": "k8s_master",
    "Kubernetes node server": "k8s_node",
    "Kubernetes balancer server": "k8s_balancer",
}
ROLE_LABEL = {
    "app": "Application server", "db": "Database server", "redis": "Caching server (Redis)",
    "lb": "Load balancer", "k8s_master": "Kubernetes master (control plane)", "k8s_node": "Kubernetes worker node",
    "k8s_balancer": "Kubernetes balancer", "rmq": "Message broker (RabbitMQ)", "mongo": "MongoDB (duplicate search)",
    "ai": "Creatio.ai on-site service", "poc_svc": "Services VM (Redis, search, duplicate search, Exchange)",
    "proxy": "Reverse proxy (DMZ, portal)", "svn": "Version control (SVN)",
}
CORE_SIZES = [4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 72, 80, 96, 112, 128, 144, 160, 192, 256]
RAM_SIZES = [8, 16, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1024, 1536, 2048, 3072, 4096]


def load_json(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def save_json(p, data):
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, p)


def rules():
    return load_json(RULES)


def val(s, key, default=None):
    v = s.get("inputs", {}).get(key)
    if isinstance(v, dict):
        v = v.get("value")
    return default if v in (None, "") else v


# ---------------------------------------------------------------- new
def cmd_new(a):
    deal = os.path.abspath(a.deal)
    p = os.path.join(deal, "sizing.json")
    if os.path.exists(p):
        sys.exit(f"{p} exists: open and update it instead of starting a second one")
    r = rules()
    inp = lambda v=None, tag="A": {"value": v, "tag": tag, "source": ""}  # noqa: E731
    data = {
        "customer": a.customer or os.path.basename(deal.rstrip("\\/")),
        "created": datetime.date.today().isoformat(),
        "status": "draft",
        "review": {"by": "", "date": "", "notes": ""},
        "creatio_version": "8.3 / 10 (Academy content identical)",
        "inputs": {
            "active_users": inp(), "named_users": inp(), "portal_users": inp(0),
            "scheme": inp("fault_tolerant"), "minimise": inp(False),
            "app_platform": inp("netfw"), "db": inp("mssql"),
            "bulk_email": inp(False), "recovery": inp("full"),
            "components": inp([]), "mailboxes": inp(0), "email_flow_per_s": inp(0),
            "kubernetes": inp("unknown"), "platform": inp(""), "file_store": inp("s3"),
            "siem": inp("unknown"), "horizon_years": inp(3), "products": inp([]),
        },
        "environments": [
            {"name": "Production", "kind": "prod", "users": None},
            {"name": "UAT", "kind": "nonprod", "users": None},
            {"name": "SIT", "kind": "nonprod", "users": None},
        ],
        "storage": {"activities": [], "files_gb_month": None, "records_per_month": None,
                    "initial_db_gb": 0, "replicas": 2},
        "assumptions": [],
        "open_questions": [q["q"] for q in r["intake_questions"]],
        "plan": {}, "storage_plan": {},
        "inputs_read": [],
    }
    os.makedirs(deal, exist_ok=True)
    save_json(p, data)
    print(f"Wrote {p}. Fill inputs (value, tag C/P/I/A, source), then: sizing.py calc")


# ---------------------------------------------------------------- calculator
def env_users(s, env):
    prod = int(val(s, "active_users", 0) or 0)
    if env.get("users"):
        return int(env["users"]), "set for this environment"
    if env["kind"] == "prod":
        return prod, "production active users"
    if env["kind"] == "poc":
        return 10, "POC: calculator at 10 users (R13)"
    return max(10, math.ceil(prod * 0.10)), "10% of production users (R8)"


def env_scheme(s, env):
    if env.get("scheme"):
        return env["scheme"]
    if env["kind"] == "poc":
        return "simple"
    return val(s, "scheme", "fault_tolerant")  # non-prod follows prod (infra-approved RFI, Jan 2026); reduced option halves it


def calc_options(s, env):
    comps = [c for c in (val(s, "components", []) or []) if c in OPT["component"]]
    if env["kind"] == "poc":
        comps = []
    portal = int(val(s, "portal_users", 0) or 0) > 0 and env["kind"] == "prod"
    ids = [OPT["app"][val(s, "app_platform", "netfw")], OPT["db"][val(s, "db", "mssql")],
           OPT["bulk"][bool(val(s, "bulk_email", False)) and env["kind"] == "prod"],
           OPT["scheme"][env_scheme(s, env)], OPT["recovery"][val(s, "recovery", "full")],
           OPT["portal"][portal], OPT["containers"][bool(comps)]]
    ids += [OPT["component"][c] for c in comps]
    return ids, (int(val(s, "portal_users", 0) or 0) if portal else 0)


def calc_url(s, env):
    users, _ = env_users(s, env)
    ids, portal = calc_options(s, env)
    q = f"?users={users}" + (f"&portal={portal}" if portal else "") + "&options=" + "-".join(ids)
    return CALC_URL + q


def html_to_text(h):
    import html as _html
    h = re.sub(r"(?s)<(script|style|noscript)[^>]*>.*?</\1>", "", h)
    m = re.search(r"(?s)<main[^>]*>(.*)</main>", h)
    h = m.group(1) if m else h
    h = re.sub(r"(?i)<br\s*/?>|</(p|div|tr|li|h\d|td|th)>", "\n", h)
    h = re.sub(r"(?i)<(td|th)[^>]*>", " | ", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = _html.unescape(h).replace(" ", " ")
    return "\n".join(ln.strip() for ln in h.split("\n") if ln.strip())


def fetch(url):
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (sizing helper)"})
            return html_to_text(urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace"))
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(5 * (attempt + 1))
    raise SystemExit(f"Calculator fetch failed ({last}). Open the link in a browser, save the page text to the "
                     f"snapshot file and rerun with --offline.")


def parse_calc(text):
    """Calculator results text -> {role: {key: value}}, plus connection channels and component blocks."""
    lines = text.split("\n")
    try:
        start = next(i for i, ln in enumerate(lines) if ln.startswith("Main application infrastructure"))
    except StopIteration:
        raise SystemExit("Not a calculator results page (no 'Main application infrastructure')")
    end = next((i for i, ln in enumerate(lines) if ln.startswith("Marketplace solution")), len(lines))
    out, cur, key = {}, None, None
    for ln in lines[start + 1:end]:
        if ln in ROLE_HEADINGS or ln == "Connection channels":
            cur = ROLE_HEADINGS.get(ln, "channels")
            out[cur], key = {}, None
            continue
        if ln.endswith("server requirements") or ln.startswith("Global search service"):
            cur, key = None, None  # container blocks: specs come from the rules file (static in the calculator)
            continue
        if cur is None:
            continue
        if ln.startswith("|"):
            v = ln[1:].strip()
            if key is None:
                key = v
                out[cur][key] = ""
            else:
                out[cur][key] = v
                key = None
        elif out[cur]:
            last = list(out[cur])[-1]
            out[cur][last] = (out[cur][last] + "\n" + ln).strip()
    return out


def num(rx, s, default=None):
    m = re.search(rx, s or "")
    return float(m.group(1)) if m else default


def role_line(role, kv, env_name):
    count = kv.get("Number of servers with fail safety") or kv.get("Number of servers") or "1"
    line = {
        "role": role, "label": ROLE_LABEL[role], "count": int(num(r"(\d+)", count, 1)),
        "cores": num(r"Number of cores\s*[—-]\s*(\d+)", kv.get("vCPU", "")),
        "ram_gb": num(r"(\d+(?:\.\d+)?)\s*GB", kv.get("vRAM", "")),
        "os": (kv.get("OS") or "").replace("\n", " / "),
        "software": (kv.get("Software requirements") or kv.get("Software requirements (MSSQL)") or
                     kv.get("Software requirements (PostgreSQL)") or "").split("\n")[0],
        "disks": [], "notes": [], "rules": [], "source": f"CALC ({env_name})",
    }
    for k in ("HDD (OS)", "HDD (application)", "HDD"):
        if kv.get(k):
            gb = num(r"(\d+)\s*GB", kv[k])
            iops = num(r"(\d+)\s*IOPS", kv[k])
            lat = num(r"less\s+th[ae]n\s+(\d+)\s*ms", kv[k])
            name = {"HDD (OS)": "OS", "HDD (application)": "Application", "HDD": "Disk"}[k]
            line["disks"].append({"name": name, "gb": gb, "iops": iops, "latency_ms": lat})
    if kv.get("HDD (Database)"):
        for name, rx in (("Data", r"Data\s*[—-]\s*(\d+)\s*GB,\s*(\d+)\s*IOPS,\s*latency less than (\d+)"),
                         ("Tempdb", r"Tempdb\s*[—-]\s*(\d+)\s*GB,\s*(\d+)\s*IOPS,\s*latency less than (\d+)"),
                         ("Logs", r"Logs\s*[—-]\s*(\d+)\s*GB,\s*(\d+)\s*IOPS,\s*latency less than (\d+)")):
            m = re.search(rx, kv["HDD (Database)"])
            if m:
                line["disks"].append({"name": name, "gb": float(m.group(1)), "iops": float(m.group(2)),
                                      "latency_ms": float(m.group(3))})
    if kv.get("Fault tolerance scheme"):
        line["notes"].append("Calculator HA scheme: " + kv["Fault tolerance scheme"])
    if kv.get("Environment"):
        line["environment"] = kv["Environment"]
    if kv.get("Ratio of virtual and physical cores"):
        line["vcpu_ratio"] = kv["Ratio of virtual and physical cores"]
    return line


def snap_down(v, sizes, floor_ratio):
    """Largest standard size <= v that is still >= floor_ratio of the original; else None."""
    cands = [x for x in sizes if x <= v + 0.5]
    if not cands:
        return None
    best = max(cands)
    return best


def apply_rules(s, env, lines, calc_kv):
    """Recommended config from the calculator + rules. Returns (recommended, reduced, applied rule ids)."""
    comps = set(val(s, "components", []) or [])
    scheme = env_scheme(s, env)
    minimise = bool(val(s, "minimise", False))
    rec, applied = [], []

    for ln in lines:
        if ln["role"] == "k8s_balancer":
            applied.append("R6")
            continue  # R6: logical abstraction, not a server
        if ln["role"] == "redis":
            if scheme == "fault_tolerant" and minimise and env["kind"] == "prod":
                ln["count"] = 1
                ln["rules"].append("R2")
                ln["notes"].append("One Redis node by choice: if it fails the system stays up, users sign in again "
                                   "and some requests are slower.")
                applied.append("R2")
            elif scheme != "fault_tolerant":
                ln["count"] = 1
                ln["rules"].append("R4")
            if ln["count"] not in (1, 6):
                ln["notes"].append("Redis is either one node or a 6-node Redis Cluster (R3).")
        rec.append(ln)

    for ln in rec:  # calculator remarks are for us, not the customer table
        ln["internal"] = [n for n in ln["notes"] if n.startswith("Calculator HA scheme")]
        ln["notes"] = [n for n in ln["notes"] if not n.startswith("Calculator HA scheme")]
    kinds = {ln["role"] for ln in rec}
    if comps & {"global_search", "dedup", "ml", "email_listener"} and env["kind"] != "poc":
        applied += ["R5", "R7"]
        if "k8s_node" not in kinds:  # calculator shows no cluster for global search alone; R5 puts it on Kubernetes
            ft = scheme == "fault_tolerant"
            rec.append(mk("k8s_master", 3 if ft else 1, 2, 4, [("Disk", 30)], "Linux Debian 12", "R5",
                          "CALC Kubernetes set + R5", "Runs the Kubernetes control plane only."))
            rec.append(mk("k8s_node", 3 if ft else 2, 4, 16, [("Disk", 120)], "Linux Debian 12", "R5",
                          "CALC Kubernetes set + R5", ""))
            rec[-1]["notes"] = []
        for ln in rec:
            if ln["role"] == "k8s_node":
                wl = [w for w, c in (("global search", "global_search"), ("bulk duplicate search", "dedup"),
                                     ("machine learning", "ml"), ("Email Listener", "email_listener")) if c in comps]
                ln["notes"].append("Runs the Creatio services as Kubernetes workloads: " + ", ".join(wl) + ".")
                ln["rules"] += ["R5", "R7"]
                need = workload_demand(s, comps, env["kind"])
                cap_c, cap_r = ln["count"] * (ln["cores"] or 4) * 0.8, ln["count"] * (ln["ram_gb"] or 16) * 0.8
                if need["cores"] > cap_c or need["ram_gb"] > cap_r:
                    n = max(math.ceil(need["cores"] / ((ln["cores"] or 4) * 0.8)),
                            math.ceil(need["ram_gb"] / ((ln["ram_gb"] or 16) * 0.8)))
                    ln["internal"].append(f"R31: workloads need ~{need['cores']:.1f} cores / {need['ram_gb']:.0f} GB "
                                          f"({need['detail']}); calculator nodes give ~{cap_c:.0f} / {cap_r:.0f} at 80%. "
                                          f"Raised {ln['count']} -> {n}. Inferred: ask infra to confirm.")
                    ln["notes"].append(f"Node count raised from {ln['count']} to {n} to fit the expected service load "
                                       "of the services above; to be confirmed in the infrastructure review.")
                    ln["count"] = n
                    ln["rules"].append("R31")
                    applied.append("R31")
    if "email_listener" in comps and env["kind"] != "poc":
        rec.append(mk("rmq", 1 if scheme != "fault_tolerant" else 3, 1, 4, [("Disk", 10)], "Linux Debian 12",
                      "R21", "AC-RMQ", "Required by Email Listener; can be shared with Creatio background tasks. "
                      "Can also run inside the Kubernetes cluster."))
        applied += ["R20", "R21"]
    if "dedup" in comps and env["kind"] != "poc":
        rec.append(mk("mongo", 3 if scheme == "fault_tolerant" else 1, 1, 16, [("SSD", None)], "Linux Debian 12",
                      "R22", "AC-GSFAQ", "Starting point; final size depends on the dataset. 3-node replica set "
                      "for high availability. Can run outside the Kubernetes cluster."))
        applied.append("R22")
    if "creatio_ai" in comps:
        rec.append(mk("ai", 1, 4, 8, [("Disk", 20)], "Linux (Ubuntu or Debian), Docker 18.03.1+ or Kubernetes 1.19+",
                      "R27", "AI-ONSITE-2026-07", "Minimum for the Creatio.ai service layer. The language model "
                      "itself is sized separately (R28)."))
        applied += ["R27", "R28"]
    if int(val(s, "portal_users", 0) or 0) > 0 and env["kind"] == "prod":
        rec.append(mk("proxy", 1 if scheme != "fault_tolerant" else 2, None, None, [], "per customer standard",
                      "R19", "AC-PORTAL", "Reverse proxy as the only public component in the DMZ. Portal users "
                      "are served by their own set of application nodes, not shared with internal users."))
        applied.append("R19")
    if env["kind"] == "poc":
        rec = [ln for ln in rec if ln["role"] in ("app", "db")]
        rec.append(mk("poc_svc", 1, 6, 16, [("Disk", 100)], "Linux Debian 12", "R13", "INFRA-POC-2026-07",
                      "Combined for a POC only. Not a production layout."))
        applied.append("R13")
    if env["kind"] == "nonprod":
        applied.append("R8")

    reduced, red_rules = reduce_lines(s, env, rec)
    return rec, reduced, sorted(set(applied)), red_rules


def el_replicas(mailboxes, flow):
    """Email Listener worker and API replicas (AC-EL table)."""
    if not mailboxes:
        return 0, 0
    worker = 0 if flow < 1 else (15 if flow <= 5 else 25)
    if mailboxes > 150:
        worker = max(worker, 2)
        api = math.ceil(mailboxes / 30.0)
    else:
        api = 4
    return worker, api


def workload_demand(s, comps, kind="prod"):
    """Rough Kubernetes workload demand from the calculator's component specs and the Email Listener table."""
    cores, ram, detail = 0.0, 0.0, []
    if "global_search" in comps:
        cores, ram = cores + 4, ram + 12
        detail.append("global search 4/12")
    if "dedup" in comps:
        cores, ram = cores + 1, ram + 3
        detail.append("duplicate search 1/3")
    if "ml" in comps:
        cores, ram = cores + 4, ram + 8
        detail.append("ML 4/8")
    if "email_listener" in comps:
        mb = int(val(s, "mailboxes", 0) or 0)
        if kind != "prod":  # test environments sync a sample of mailboxes (same 10% as users, R8)
            mb = math.ceil(mb * 0.10)
        w, a = el_replicas(mb, float(val(s, "email_flow_per_s", 0) or 0) if kind == "prod" else 0)
        c = w * 0.1 + a * 0.15
        r_ = w * 1.1 + a * 0.85
        cores, ram = cores + c, ram + r_
        detail.append(f"Email Listener {w} workers + {a} API = {c:.1f}/{r_:.0f}")
    return {"cores": cores, "ram_gb": ram, "detail": ", ".join(detail)}


def mk(role, count, cores, ram, disks, os_, rule, source, note):
    return {"role": role, "label": ROLE_LABEL[role], "count": count, "cores": cores, "ram_gb": ram, "os": os_,
            "software": "", "disks": [{"name": n, "gb": g, "iops": None, "latency_ms": None} for n, g in disks],
            "notes": [note] if note else [], "internal": [], "rules": [rule], "source": source}


def reduce_lines(s, env, rec):
    """Reduced (minimum) configuration with its trade-offs."""
    out, used = [], []
    apps = sum(ln["count"] for ln in rec if ln["role"] == "app")
    for ln in rec:
        x = json.loads(json.dumps(ln))
        x["notes"] = list(x["notes"])
        if env["kind"] == "prod":
            if x["role"] == "app" and ((x["cores"] or 0) > 8 or (x["ram_gb"] or 0) > 32):
                x["cores"], x["ram_gb"] = min(x["cores"] or 8, 8), min(x["ram_gb"] or 32, 32)
                x["rules"].append("R9")
                x["notes"].append("Reduced to 8 cores / 32 GB per server.")
                used.append("R9")
            if x["role"] == "db" and (x["cores"] or 0) >= 64:
                c = snap_down(x["cores"] * 0.89, CORE_SIZES, 0.85)
                r = snap_down((x["ram_gb"] or 0) * 0.93, RAM_SIZES, 0.85)
                if c and c >= x["cores"] * 0.85 and c < x["cores"]:
                    x["cores"] = c
                if r and r >= x["ram_gb"] * 0.85 and r < x["ram_gb"]:
                    x["ram_gb"] = r
                x["rules"].append("R10")
                x["notes"].append("Slightly slower at peak load, good performance under regular load.")
                used.append("R10")
            if x["role"] == "redis" and x["count"] == 6 and bool(val(s, "minimise", False)):
                x["count"] = 1
                x["rules"].append("R2")
                used.append("R2")
            if x["role"] == "lb" and apps <= 1:
                x["count"] = 0
                x["rules"].append("R12")
                used.append("R12")
        elif env["kind"] == "nonprod":
            if x["role"] in ("redis", "rmq", "mongo"):
                if x["count"] > 1:
                    x["count"] = 1
                    x["rules"].append("R4")
                    used.append("R4")
            elif x["role"] in ("k8s_master", "k8s_node"):
                simple = 1 if x["role"] == "k8s_master" else 2
                if x["count"] > simple and "R31" not in x["rules"]:
                    x["count"] = simple
                    x["rules"].append("R11")
                    x["notes"].append("Smallest Kubernetes set the calculator uses (1 master, 2 workers).")
                    used.append("R11")
            elif x["count"] > 1:
                x["count"] = math.ceil(x["count"] / 2)
                x["rules"].append("R11")
                x["notes"].append("Server count halved for the reduced configuration.")
                used.append("R11")
        if x["count"] > 0:
            out.append(x)
    return out, sorted(set(used))


def cmd_url(a):
    s = load_json(a.sizing)
    for env in s["environments"]:
        print(f"{env['name']}: {calc_url(s, env)}")


def cmd_calc(a):
    s = load_json(a.sizing)
    deal = os.path.dirname(os.path.abspath(a.sizing))
    snapdir = os.path.join(deal, "sizing")
    os.makedirs(snapdir, exist_ok=True)
    if not val(s, "active_users"):
        sys.exit("inputs.active_users is empty: ask Q1 first")
    if val(s, "app_platform") == "net" and val(s, "db") == "mssql":
        sys.exit("The .NET (Linux) line does not support MS SQL (ST4): use db=pg or app_platform=netfw")
    s["plan"] = {"date": datetime.date.today().isoformat(), "environments": []}
    for env in s["environments"]:
        url = calc_url(s, env)
        slug = re.sub(r"[^a-z0-9]+", "-", env["name"].lower()).strip("-")
        snap = os.path.join(a.offline or snapdir, f"calc-{slug}.txt")
        if a.offline:
            text = open(snap, encoding="utf-8").read()
        else:
            text = fetch(url)
            with open(os.path.join(snapdir, f"calc-{slug}.txt"), "w", encoding="utf-8") as fh:
                fh.write(f"URL: {url}\nFetched: {datetime.datetime.now().isoformat(timespec='minutes')}\n\n{text}")
        kv = parse_calc(text)
        lines = [role_line(role, kv[role], env["name"]) for role in ROLE_HEADINGS.values() if role in kv]
        users, why = env_users(s, env)
        rec, reduced, applied, red = apply_rules(s, env, lines, kv)
        s["plan"]["environments"].append({
            "name": env["name"], "kind": env["kind"], "users": users, "users_why": why,
            "scheme": env_scheme(s, env), "calc_url": url, "snapshot": f"sizing/calc-{slug}.txt",
            "channels": kv.get("channels", {}), "recommended": rec, "reduced": reduced,
            "rules_applied": applied, "reduced_rules": red,
        })
        n = sum(x["count"] for x in rec)
        print(f"{env['name']}: {users} users, {env_scheme(s, env)}, {n} servers recommended, "
              f"{sum(x['count'] for x in reduced)} reduced. Rules {', '.join(applied) or '-'}")
    if val(s, "scheme") == "fault_tolerant" and not any(
            "high availability" in (x.get("text") or "").lower() for x in s.get("assumptions", [])):
        print("NOTE R1: confirm the customer really needs high availability; the simple scheme cuts hardware a lot.")
    save_json(a.sizing, s)


# ---------------------------------------------------------------- storage
def nice_up(gb):
    """Round a capacity up to a plan-friendly figure."""
    if gb >= 1000:
        return math.ceil(gb / 500.0) * 500
    if gb >= 100:
        return math.ceil(gb / 50.0) * 50
    return math.ceil(gb / 10.0) * 10


def storage_plan(s, r):
    d = r["storage_method"]["defaults"]
    st = s.get("storage", {})
    days = st.get("working_days", d["working_days_per_month"])
    rows = []
    monthly_mb = 0.0
    for act in st.get("activities", []):
        users = 1 if act.get("shared") else act.get("users") or int(val(s, "named_users", 0) or val(s, "active_users", 0) or 0)
        mb = act["per_user_per_day"] * act["size_mb"] * days * users
        rows.append({"label": act["label"], "mb_month": round(mb, 1), "users": users,
                     "shared": bool(act.get("shared"))})
        monthly_mb += mb
    files_gb_month = st.get("files_gb_month") or round(monthly_mb / 1000.0, 2)
    head = 1 + d["headroom_pct"] / 100.0
    replicas = st.get("replicas", 2)
    horizons = []
    for y in d["horizons_years"]:
        raw = files_gb_month * 12 * y
        usable = nice_up(raw * head)
        horizons.append({"years": y, "raw_gb": round(raw), "usable_gb": usable, "physical_gb": usable * replicas})
    yrs = int(val(s, "horizon_years", 3) or 3)
    months = 12 * yrs
    recs = st.get("records_per_month") or 0
    growth = recs / 1000.0 * d["db_gb_per_1000_records"]
    files_in_db = val(s, "file_store", "s3") == "db"
    calc_data = 0
    for env in s.get("plan", {}).get("environments", []):
        if env["kind"] == "prod":
            for ln in env["recommended"]:
                if ln["role"] == "db":
                    calc_data = sum(dk["gb"] or 0 for dk in ln["disks"] if dk["name"] == "Data")
    est = (st.get("initial_db_gb", 0) + growth * months) * head
    if files_in_db:
        est += files_gb_month * months * head
    db_data = nice_up(max(est, calc_data, d["db_min_gb"]))
    lo, hi = d["db_backup_multiplier"]
    target = next((h for h in horizons if h["years"] == yrs), horizons[-1])
    return {
        "files_gb_month": files_gb_month, "activities": rows, "horizons": horizons, "replicas": replicas,
        "horizon_years": yrs, "db_growth_gb_month": round(growth, 2), "db_data_gb": db_data,
        "db_data_basis": f"max(estimate {round(est)} GB, calculator data disk {round(calc_data)} GB, floor {d['db_min_gb']} GB)",
        "db_log_temp_gb": d["db_log_temp_gb"], "db_backup_gb": [nice_up(db_data * lo), nice_up(db_data * hi)],
        "file_copy_gb": round(target["usable_gb"] * d["file_secondary_copy_multiplier"]),
        "app_node_gb": d["app_node_gb"], "files_in_db": files_in_db, "source": r["storage_method"]["source"],
    }


def cmd_storage(a):
    s = load_json(a.sizing)
    sp = storage_plan(s, rules())
    s["storage_plan"] = sp
    save_json(a.sizing, s)
    print(f"Files: {sp['files_gb_month']} GB/month. " + "; ".join(
        f"{h['years']}y {gb_txt(h['usable_gb'])} usable" for h in sp["horizons"]))
    print(f"DB data {gb_txt(sp['db_data_gb'])} ({sp['db_data_basis']}); backups "
          f"{gb_txt(sp['db_backup_gb'][0])}-{gb_txt(sp['db_backup_gb'][1])}")


def gb_txt(gb):
    if gb is None:
        return "-"
    if gb >= 1000:
        t = gb / 1000.0
        return f"~{t:.1f} TB".replace(".0 TB", " TB")
    return f"{int(gb)} GB"


# ---------------------------------------------------------------- check
def customer_text(s):
    """Every string that reaches the customer document."""
    out = [a.get("text", "") for a in s.get("assumptions", [])]
    out += s.get("notes_for_customer", [])
    for env in s.get("plan", {}).get("environments", []):
        for ln in env.get("recommended", []) + env.get("reduced", []):
            out += ln.get("notes", [])
    return out


def cmd_check(a, quiet=False):
    s = load_json(a.sizing)
    r = rules()
    errors, warns = [], []
    for k, v in s.get("inputs", {}).items():
        if isinstance(v, dict) and v.get("value") not in (None, "", [], 0, False) and v.get("tag") not in TAGS:
            errors.append(f"inputs.{k}: tag must be one of {TAGS}")
        if isinstance(v, dict) and v.get("tag") == "A" and k in ("active_users", "scheme"):
            warns.append(f"inputs.{k} is an assumption (A): ask the customer before this goes out")
    if s.get("status") not in STATUS:
        errors.append(f"status must be one of {STATUS}")
    if val(s, "app_platform") == "net" and val(s, "db") == "mssql":
        errors.append("ST4: .NET (Linux) needs PostgreSQL")
    if val(s, "db") == "oracle":
        warns.append("Oracle is not in Academy's current stack list (ST3): confirm with the infra team")
    if val(s, "app_platform") == "net" and set(val(s, "products", []) or []) & {"Bank Sales", "Bank Customer Journey", "Lending", "Sales Commerce", "Customer Center"}:
        warns.append("ST11: a product in scope shows .NET Framework only: plan Windows + IIS or confirm with infra")
    plan = s.get("plan", {}).get("environments", [])
    if not plan:
        errors.append("no plan: run sizing.py calc")
    for env in plan:
        for ln in env["recommended"]:
            if ln["role"] == "redis" and ln["count"] not in (1, 6):
                errors.append(f"{env['name']}: Redis count {ln['count']} (R3: 1 or 6)")
            if ln["role"] == "k8s_balancer":
                errors.append(f"{env['name']}: Kubernetes balancer listed as a server (R6)")
            if not ln.get("source"):
                errors.append(f"{env['name']} {ln['label']}: no source")
    if "creatio_ai" in (val(s, "components", []) or []):
        warns.append("R28: on-prem AI is limited. Involve Roman Prus before promising AI scenarios; LLM sized separately")
    bad = []
    for t in customer_text(s):
        for w in r["wording"]["avoid"]:
            if re.search(r"(?<![a-z])" + re.escape(w.lower()) + r"(?![a-z])", (t or "").lower()):
                bad.append(f"'{w}' in: {t[:80]}")
    if bad:
        errors += ["Wording (sounds definitive): " + b for b in bad]
    if not quiet:
        for w in warns:
            print("WARN ", w)
        for e in errors:
            print("ERROR", e)
        print("OK" if not errors else f"{len(errors)} error(s)")
    return errors, warns


# ---------------------------------------------------------------- build
def spec_txt(ln):
    parts = []
    if ln.get("cores"):
        parts.append(f"{int(ln['cores'])}+ cores")
    if ln.get("ram_gb"):
        parts.append(f"{ln['ram_gb']:g} GB RAM")
    return ", ".join(parts) or "see notes"


def disk_txt(ln):
    out = []
    for dk in ln.get("disks", []):
        t = f"{dk['name']} {int(dk['gb'])} GB" if dk.get("gb") else dk["name"]
        if dk.get("iops"):
            t += f", {int(dk['iops'])} IOPS"
        if dk.get("latency_ms"):
            t += f", <{int(dk['latency_ms'])} ms"
        out.append(t)
    return "; ".join(out) or "-"


def cmd_build(a):
    s = load_json(a.sizing)
    r = rules()
    errors, warns = cmd_check(a, quiet=True)
    if errors and not a.draft:
        for e in errors:
            print("ERROR", e)
        sys.exit("Fix the errors first (or --draft for an internal look).")
    if s.get("plan") and not s.get("storage_plan"):
        s["storage_plan"] = storage_plan(s, r)
        save_json(a.sizing, s)
    deal = os.path.dirname(os.path.abspath(a.sizing))
    nn = f"{int(a.nn):02d}"
    docx_p = os.path.join(deal, f"{nn}-sizing.docx")
    xlsx_p = os.path.join(deal, f"{nn}-sizing.xlsx")
    md_p = os.path.join(deal, f"{nn}-sizing-internal.md")
    build_docx(s, r, docx_p)
    build_xlsx(s, r, xlsx_p)
    build_internal(s, r, md_p, warns)
    print(f"Wrote {docx_p}\n      {xlsx_p}\n      {md_p}")


def status_line(s, r):
    return r["wording"]["status"][s.get("status", "draft")]


def build_docx(s, r, path):
    try:
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: F401
        from docx.shared import Pt, RGBColor
    except ImportError:
        sys.exit("python-docx missing: python -m pip install python-docx")
    w = r["wording"]
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading(f"{s['customer']}: Creatio infrastructure recommendation", 0)
    p = d.add_paragraph()
    run = p.add_run(f"Status: {status_line(s, r)}  ·  {datetime.date.today().strftime('%d %B %Y')}")
    run.italic = True
    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    d.add_paragraph(w["intro"])

    d.add_heading("What this is based on", 1)
    d.add_paragraph(w["basis"])
    t = d.add_table(rows=1, cols=2)
    t.style = "Light Grid Accent 1"
    t.rows[0].cells[0].text, t.rows[0].cells[1].text = "Item", "What we have used"
    for label, text in basis_rows(s):
        c = t.add_row().cells
        c[0].text, c[1].text = label, text
    if s.get("assumptions"):
        d.add_paragraph()
        d.add_paragraph("Assumptions we'd like you to confirm:")
        for a in s["assumptions"]:
            d.add_paragraph(a["text"], style="List Bullet")

    d.add_heading("Recommended architecture", 1)
    for para in architecture_text(s):
        d.add_paragraph(para)

    for env in s.get("plan", {}).get("environments", []):
        d.add_heading(f"{env['name']}: recommended servers", 2)
        d.add_paragraph(f"Sized for about {env['users']:,} active users "
                        f"({'high availability' if env['scheme'] == 'fault_tolerant' else 'standard'} configuration).")
        server_table(d, env["recommended"])
        if env["reduced"] and summary(env["reduced"]) != summary(env["recommended"]):
            d.add_paragraph()
            d.add_paragraph(f"Reduced configuration option for {env['name']}", style="Intense Quote")
            d.add_paragraph(w["minimum_caveat"])
            server_table(d, env["reduced"])

    sp = s.get("storage_plan") or {}
    if sp:
        d.add_heading("Storage", 1)
        if not sp["files_in_db"]:
            d.add_paragraph("We recommend storing files (attachments, photos, documents) in S3-compatible object "
                            "storage from day one rather than in the database. The database then holds only the "
                            "file details, which keeps backups, restores, upgrades and test copies fast. Setting "
                            "this up before go-live means nothing needs to be migrated later.")
        t = d.add_table(rows=1, cols=2)
        t.style = "Light Grid Accent 1"
        t.rows[0].cells[0].text, t.rows[0].cells[1].text = "Component", "Suggested capacity"
        for comp, cap in storage_rows(sp):
            c = t.add_row().cells
            c[0].text, c[1].text = comp, cap
        d.add_paragraph()
        d.add_paragraph(w["storage_caveat"])

    d.add_heading("Software", 1)
    for line in software_lines(s):
        d.add_paragraph(line, style="List Bullet")

    d.add_heading("What could change this recommendation", 1)
    for line in ("The number of integrations and how often they run.",
                 "How many sections, pages and business processes are configured, and how heavily they're used.",
                 "Data volumes, file sizes and how long data is kept.",
                 "Peak usage patterns, such as month-end or campaign days.",
                 "Marketplace apps, which can have their own requirements."):
        d.add_paragraph(line, style="List Bullet")
    d.add_paragraph("We recommend testing realistic high-load scenarios during the implementation and reviewing "
                    "the infrastructure if usage grows.")

    d.add_heading("Next steps", 1)
    for i, step in enumerate(w["next_steps"], 1):
        d.add_paragraph(step, style="List Number")
    d.add_paragraph(w["closing"])
    d.save(path)


def summary(lines):
    return [(x["role"], x["count"], x["cores"], x["ram_gb"]) for x in lines]


def server_table(d, lines):
    t = d.add_table(rows=1, cols=5)
    t.style = "Light Grid Accent 1"
    for i, h in enumerate(("Server", "Qty", "Per server", "Storage per server", "Notes")):
        t.rows[0].cells[i].text = h
    for ln in lines:
        c = t.add_row().cells
        c[0].text = ln["label"] + (f"\n{ln['os']}" if ln.get("os") else "")
        c[1].text = str(ln["count"])
        c[2].text = spec_txt(ln)
        c[3].text = disk_txt(ln)
        c[4].text = " ".join(ln.get("notes", []))


def basis_rows(s):
    v = lambda k, d=None: val(s, k, d)  # noqa: E731
    comps = v("components", []) or []
    names = {"global_search": "Global search", "dedup": "Bulk duplicate search", "ml": "Machine learning",
             "email_listener": "Mailbox synchronisation", "creatio_ai": "Creatio.ai on-site"}
    rows = [("Active users (production)", f"{int(v('active_users', 0)):,}")]
    if v("named_users"):
        rows.append(("Named users", f"{int(v('named_users')):,}"))
    if int(v("portal_users", 0) or 0):
        rows.append(("Portal users", f"{int(v('portal_users')):,}"))
    rows += [
        ("Availability", "High availability (no single point of failure)" if v("scheme") == "fault_tolerant"
         else "Standard (one server per role)"),
        ("Application platform", "Windows Server + IIS (.NET Framework)" if v("app_platform") == "netfw"
         else "Linux Debian 12 (.NET 8)"),
        ("Database", {"mssql": "Microsoft SQL Server", "pg": "PostgreSQL", "oracle": "Oracle"}[v("db", "mssql")]),
        ("Optional services", ", ".join(names[c] for c in comps if c in names) or "None"),
        ("Bulk email", "Yes" if v("bulk_email") else "No"),
        ("Environments", ", ".join(e["name"] for e in s["environments"])),
        ("Non-production sizing", "About 10% of production users per environment"),
        ("Storage horizon", f"{v('horizon_years', 3)} years"),
        ("Basis", "Creatio system requirements calculator and Creatio Academy, version 8.3"),
    ]
    return rows


def architecture_text(s):
    v = lambda k, d=None: val(s, k, d)  # noqa: E731
    comps = set(v("components", []) or [])
    out = []
    if v("scheme") == "fault_tolerant":
        out.append("For production we recommend a high-availability layout: several application servers behind a "
                   "load balancer (a web farm), a clustered database, and redundancy for each critical component.")
        if v("minimise"):
            out.append("To keep the footprint down, we suggest a single caching (Redis) node. If it stops, Creatio "
                       "keeps running; users sign in again and some requests take a little longer. Creatio uses the "
                       "same approach in its own cloud.")
        if v("db") == "mssql":
            out.append("For the database, Microsoft SQL Server Always On availability groups is the approach Creatio "
                       "recommends for high availability. Both Standard and Enterprise editions are supported; the "
                       "choice depends on your availability and performance needs.")
    else:
        out.append("We recommend a standard layout with one server per role. If you later need high availability, "
                   "the same design scales out by adding servers.")
    if comps & {"global_search", "dedup", "ml", "email_listener"}:
        out.append("The supporting services (such as search and mailbox synchronisation) are designed to run in "
                   "containers. We recommend a Kubernetes cluster for them, which handles restarts, scaling and "
                   "load balancing for you. The Kubernetes master servers run the cluster itself; the services run "
                   "on the worker nodes.")
    if v("app_platform") == "netfw" and comps & {"global_search", "ml", "email_listener"}:
        out.append("A common pattern is the Creatio application on Windows servers, with the containerised services "
                   "on Kubernetes and the database and cache on virtual machines, each as a cluster.")
    out.append("We recommend each component runs on its own operating system, with all active components in one "
               "data centre. Backup components can sit in a second site for disaster recovery.")
    if int(v("portal_users", 0) or 0):
        out.append("With a portal, portal users are served by their own application servers and a reverse proxy "
                   "is the only component exposed in your DMZ.")
    return out


def storage_rows(sp):
    rows = [("Files (object storage), usable",
             "; ".join(f"{h['years']} year{'s' if h['years'] > 1 else ''}: {gb_txt(h['usable_gb'])}" for h in sp["horizons"])
             + f" (about {sp['files_gb_month']:g} GB of new files a month, plus about 30% headroom)")]
    rows.append(("Files, physical disk", f"About {sp['replicas']}x the usable figure if the object store keeps "
                 f"{sp['replicas']} copies"))
    rows.append(("Database data", f"about {gb_txt(sp['db_data_gb'])} over {sp['horizon_years']} years"))
    rows.append(("Database log and temp", f"{sp['db_log_temp_gb'][0]}-{sp['db_log_temp_gb'][1]} GB"))
    rows.append(("Database backups", f"{gb_txt(sp['db_backup_gb'][0])}-{gb_txt(sp['db_backup_gb'][1])} "
                 "(for example weekly full, daily differential and log backups kept 30 days), ideally on separate storage"))
    rows.append(("Files, second copy", f"up to {gb_txt(sp['file_copy_gb'])} (replication to a second site and/or "
                 "bucket versioning). Deleted files are kept as long as database backups, so we suggest aligning "
                 "the two retention policies"))
    rows.append(("Application servers", f"{sp['app_node_gb'][0]}-{sp['app_node_gb'][1]} GB per server for the "
                 "operating system, application and logs (a central log platform is sized on your side)"))
    return rows


def software_lines(s):
    v = lambda k, d=None: val(s, k, d)  # noqa: E731
    out = []
    if v("app_platform") == "netfw":
        out.append("Application servers: Windows Server 2022 or later, IIS 10 or later, .NET Framework 4.7.2 and .NET 8.")
    else:
        out.append("Application servers: Linux Debian 12 (kernel 5.10 or later) with .NET 8.")
    out.append({"mssql": "Database: Microsoft SQL Server 2022 or later (Standard or Enterprise).",
                "pg": "Database: PostgreSQL 16 or later.",
                "oracle": "Database: Oracle (to be confirmed with Creatio for your version)."}[v("db", "mssql")])
    out.append("Cache: Redis 7.4 or later on Linux Debian 12. Redis Open Source covers everything Creatio needs.")
    if v("scheme") == "fault_tolerant":
        out.append("Load balancer: HAProxy or an equivalent that supports WebSockets (Citrix, Cisco, NginX, FortiGate and MS ARR are known to work).")
    if set(v("components", []) or []) & {"global_search", "dedup", "ml", "email_listener"}:
        out.append("Containers: Kubernetes 1.25 or later on Linux Debian 12.")
    if "global_search" in (v("components", []) or []):
        out.append("Search: an open-source-compatible Elasticsearch distribution is enough.")
    out.append("Virtualisation: VMware vSphere, Microsoft Hyper-V, AWS or Azure are the platforms Creatio lists as supported.")
    return out


def build_xlsx(s, r, path):
    try:
        import openpyxl
        from openpyxl.styles import Alignment, Font, PatternFill
    except ImportError:
        sys.exit("openpyxl missing: python -m pip install openpyxl")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Read me"
    ws["A1"] = f"{s['customer']}: Creatio infrastructure recommendation"
    ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = f"Status: {status_line(s, r)}"
    ws["A2"].font = Font(italic=True)
    ws["A4"] = r["wording"]["intro"]
    ws["A5"] = r["wording"]["basis"]
    ws["A6"] = "Specs are per server. Cores and RAM are starting recommendations; see the notes on each line."
    for c in ("A4", "A5", "A6"):
        ws[c].alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 120
    head = PatternFill("solid", fgColor="1F3864")
    for env in s.get("plan", {}).get("environments", []):
        for cfg in ("recommended", "reduced"):
            if cfg == "reduced" and summary(env["reduced"]) == summary(env["recommended"]):
                continue
            title = f"{env['name']}{' (reduced)' if cfg == 'reduced' else ''}"[:31]
            sh = wb.create_sheet(title)
            sh.append([f"{env['name']}: {'reduced configuration option' if cfg == 'reduced' else 'recommended'}, "
                       f"about {env['users']:,} active users"])
            sh["A1"].font = Font(bold=True)
            sh.append([f"Status: {status_line(s, r)}"])
            sh.append([])
            sh.append(["Server", "Qty", "OS", "CPU cores (per server)", "RAM GB (per server)",
                       "Storage (per server)", "Notes"])
            for cell in sh[4]:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = head
            for ln in env[cfg]:
                sh.append([ln["label"], ln["count"], ln.get("os", ""), ln.get("cores"), ln.get("ram_gb"),
                           disk_txt(ln), " ".join(ln.get("notes", []))])
            for col, wdt in zip("ABCDEFG", (34, 6, 30, 12, 12, 48, 70)):
                sh.column_dimensions[col].width = wdt
            for row in sh.iter_rows(min_row=5):
                for cell in row:
                    cell.alignment = Alignment(wrap_text=True, vertical="top")
    sp = s.get("storage_plan") or {}
    if sp:
        sh = wb.create_sheet("Storage")
        sh.append(["Component", "Suggested capacity"])
        for cell in sh[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = head
        for row in storage_rows(sp):
            sh.append(list(row))
        sh.append([])
        sh.append([r["wording"]["storage_caveat"]])
        sh.column_dimensions["A"].width = 34
        sh.column_dimensions["B"].width = 110
        for row in sh.iter_rows():
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def build_internal(s, r, path, warns):
    rule_by = {x["id"]: x for x in r["rules"]}
    L = [f"# {s['customer']}: sizing recommendation (internal)", "",
         f"Status: **{s.get('status')}** · {status_line(s, r)}"]
    if s.get("review", {}).get("by"):
        L.append(f"Reviewed by {s['review']['by']} on {s['review']['date']}: {s['review'].get('notes', '')}")
    L += ["", "## Inputs", "", "| Input | Value | Tag | Source |", "|---|---|---|---|"]
    for k, v in s["inputs"].items():
        if isinstance(v, dict):
            L.append(f"| {k} | {v.get('value')} | {v.get('tag')} | {v.get('source', '')} |")
    for env in s.get("plan", {}).get("environments", []):
        L += ["", f"## {env['name']} ({env['users']} users, {env['users_why']}, {env['scheme']})", "",
              f"Calculator: {env['calc_url']}  ", f"Snapshot: `{env['snapshot']}`", "",
              "| Server | Qty | Cores | RAM GB | Storage | Rules | Source |", "|---|---|---|---|---|---|---|"]
        for ln in env["recommended"]:
            L.append(f"| {ln['label']} | {ln['count']} | {ln.get('cores') or '-'} | {ln.get('ram_gb') or '-'} | "
                     f"{disk_txt(ln)} | {', '.join(ln['rules']) or '-'} | {ln['source']} |")
        notes = [f"- {ln['label']}: {n}" for ln in env["recommended"] for n in ln.get("internal", [])]
        if notes:
            L += ["", "For the infra review:"] + notes
        L.append(f"\nRules applied: {', '.join(env['rules_applied']) or 'none'}. "
                 f"Reduced option: {', '.join(env['reduced_rules']) or 'same as recommended'}.")
        if env["kind"] == "prod" and env.get("channels"):
            L.append("Connection channels (calculator): " + "; ".join(f"{k} {v}" for k, v in env["channels"].items()))
    used = sorted({x for env in s.get("plan", {}).get("environments", []) for x in env["rules_applied"] + env["reduced_rules"]},
                  key=lambda x: int(x[1:]))
    L += ["", "## Rules used", ""]
    for rid in used:
        L.append(f"- **{rid}** ({rule_by[rid]['source']}): {rule_by[rid]['text']}")
    if warns:
        L += ["", "## Warnings", ""] + [f"- {w}" for w in warns]
    L += ["", "## Open questions for the customer", ""] + [f"- {q}" for q in s.get("open_questions", [])]
    L += ["", "## Known conflicts in the sources", ""] + [f"- {c}" for c in r["conflicts_to_resolve"]]
    L += ["", "## Draft note to the infrastructure team", "", "> Hi Sergey,", ">",
          f"> Could you please review the attached on-prem sizing recommendation for {s['customer']} before we share it?",
          f"> It starts from the calculator ({', '.join(e['name'] for e in s.get('plan', {}).get('environments', []))};"
          " links below) and applies these adjustments: " + (", ".join(used) or "none") + ".",
          "> Assumptions we're least sure about: " + (", ".join(k for k, v in s["inputs"].items()
                                                         if isinstance(v, dict) and v.get("tag") == "A"
                                                         and v.get("value") not in (None, "", [], 0)) or "none") + ".",
          ">"]
    for env in s.get("plan", {}).get("environments", []):
        L.append(f"> - {env['name']}: {env['calc_url']}")
    L += [">", "> Thank you!"]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


# ---------------------------------------------------------------- review
def cmd_review(a):
    s = load_json(a.sizing)
    if a.status not in STATUS:
        sys.exit(f"status must be one of {STATUS}")
    s["status"] = a.status
    if a.status == "infra_reviewed":
        if not a.by:
            sys.exit("--by is required for infra_reviewed (who in the infra team reviewed it)")
        s["review"] = {"by": a.by, "date": datetime.date.today().isoformat(), "notes": a.notes or ""}
    save_json(a.sizing, s)
    print(f"Status: {a.status}. Rebuild to update the documents.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("new"); p.add_argument("deal"); p.add_argument("--customer"); p.set_defaults(f=cmd_new)
    p = sub.add_parser("url"); p.add_argument("sizing"); p.set_defaults(f=cmd_url)
    p = sub.add_parser("calc"); p.add_argument("sizing"); p.add_argument("--offline"); p.set_defaults(f=cmd_calc)
    p = sub.add_parser("storage"); p.add_argument("sizing"); p.set_defaults(f=cmd_storage)
    p = sub.add_parser("check"); p.add_argument("sizing"); p.set_defaults(f=lambda a: sys.exit(1 if cmd_check(a)[0] else 0))
    p = sub.add_parser("build"); p.add_argument("sizing"); p.add_argument("--nn", required=True)
    p.add_argument("--draft", action="store_true"); p.set_defaults(f=cmd_build)
    p = sub.add_parser("review"); p.add_argument("sizing"); p.add_argument("--status", required=True)
    p.add_argument("--by"); p.add_argument("--notes"); p.set_defaults(f=cmd_review)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
