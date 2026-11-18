"""Checks for sc-sizing against cases the Creatio infrastructure team has reviewed (generic labels, no customer
names). Offline: uses saved calculator pages in fixtures/. Run after any change to sizing.py or SIZING-RULES:

  python tests/sizing/test_sizing.py

Prints PASS or the failures.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SCRIPT = os.path.join(ROOT, "skills", "sc-sizing", "scripts", "sizing.py")
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
sys.path.insert(0, os.path.dirname(SCRIPT))
import sizing  # noqa: E402

fails = []


def ok(cond, what):
    if not cond:
        fails.append(what)


def run(*args):
    return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True, encoding="utf-8")


def deal(tmp, name, inputs, envs, storage=None, assumptions=None):
    d = os.path.join(tmp, name)
    r = run("new", d, "--customer", "Fictional " + name)
    ok(r.returncode == 0, f"{name}: new failed {r.stderr}")
    p = os.path.join(d, "sizing.json")
    s = json.load(open(p, encoding="utf-8"))
    for k, v in inputs.items():
        s["inputs"][k] = {"value": v, "tag": "C", "source": "test"}
    s["environments"] = envs
    if storage:
        s["storage"].update(storage)
    s["assumptions"] = assumptions or []
    json.dump(s, open(p, "w", encoding="utf-8"))
    return p


def lines(p, env, cfg="recommended"):
    s = json.load(open(p, encoding="utf-8"))
    e = next(x for x in s["plan"]["environments"] if x["name"] == env)
    return {ln["role"]: (ln["count"], ln["cores"], ln["ram_gb"]) for ln in e[cfg]}


tmp = tempfile.mkdtemp()
try:
    rules = sizing.rules()
    ids = [r["id"] for r in rules["rules"]]
    ok(len(ids) == len(set(ids)), "rule ids unique")
    ok(all(r["source"] for r in rules["rules"]), "every rule has a source")

    # 1. Bank RFI, 20,000 users, fault tolerant (infra-reviewed Jan 2026)
    p = deal(tmp, "rfi-20k", {"active_users": 20000, "scheme": "fault_tolerant", "db": "pg", "recovery": "full",
                              "components": ["global_search", "dedup", "ml", "email_listener"]},
             [{"name": "Production", "kind": "prod", "users": None}, {"name": "UAT", "kind": "nonprod", "users": None}],
             assumptions=[{"text": "Production needs high availability.", "tag": "C"}])
    r = run("calc", p, "--offline", os.path.join(FIX, "rfi-20k"))
    ok(r.returncode == 0, f"rfi-20k calc: {r.stderr}")
    prod = lines(p, "Production")
    ok(prod.get("app") == (21, 8, 53), f"prod app 21 x 8 cores / 53 GB, got {prod.get('app')}")
    ok(prod.get("db") == (2, 144, 1106), f"prod DB 2 x 144 / 1106, got {prod.get('db')}")
    ok(prod.get("redis", (0,))[0] == 6, "prod Redis cluster 6 (no minimise)")
    ok("k8s_balancer" not in prod, "R6: no Kubernetes balancer line")
    ok(prod.get("k8s_master", (0,))[0] == 3 and prod.get("k8s_node", (0,))[0] == 3, "prod Kubernetes 3 + 3")
    red = lines(p, "Production", "reduced")
    ok(red.get("app")[1:] == (8, 32), f"R9 reduced app 8 / 32, got {red.get('app')}")
    ok(red.get("db")[1:] == (128, 1024), f"R10 reduced DB 128 / 1024 (infra comment), got {red.get('db')}")
    uat = lines(p, "UAT")
    ok(uat.get("app") == (5, 4, 24), f"UAT (10% = 2,000 users) app 5 x 4 / 24, got {uat.get('app')}")
    ok(uat.get("db") == (2, 16, 116), f"UAT DB 2 x 16 / 116, got {uat.get('db')}")
    ured = lines(p, "UAT", "reduced")
    ok(ured.get("redis", (0,))[0] == 1, "R4 reduced non-prod: single Redis")
    ok(ured.get("app", (0,))[0] == 3 and ured.get("db", (0,))[0] == 1, "R11 halved app 3, DB 1")
    ok(ured.get("k8s_master", (0,))[0] == 1, "reduced non-prod: 1 Kubernetes master")
    r = run("build", p, "--nn", "21")
    ok(r.returncode == 0, f"rfi-20k build: {r.stdout} {r.stderr}")
    for f in ("21-sizing.docx", "21-sizing.xlsx", "21-sizing-internal.md"):
        ok(os.path.exists(os.path.join(os.path.dirname(p), f)), f"built {f}")
    md = open(os.path.join(os.path.dirname(p), "21-sizing-internal.md"), encoding="utf-8").read()
    ok("Draft note to the infrastructure team" in md and "R10" in md, "internal md has rules and infra note")

    # 2. minimise in fault tolerant -> one Redis (R2)
    s = json.load(open(p, encoding="utf-8"))
    s["inputs"]["minimise"] = {"value": True, "tag": "C", "source": "test"}
    json.dump(s, open(p, "w", encoding="utf-8"))
    run("calc", p, "--offline", os.path.join(FIX, "rfi-20k"))
    ok(lines(p, "Production").get("redis", (0,))[0] == 1, "R2: minimise -> 1 Redis node in production")

    # 3. Storage: securities firm, 80 RMs (infra method Oct 2026): 62.4 GB/month -> ~1 / 3 / 5 TB usable
    sp = sizing.storage_plan({"inputs": {"horizon_years": {"value": 3}}, "plan": {}, "storage": {
        "activities": [
            {"label": "Visit photos", "per_user_per_day": 5, "size_mb": 5, "users": 80},
            {"label": "Other attachments", "per_user_per_day": 25, "size_mb": 0.2, "users": 80},
            {"label": "Complaint documents", "per_user_per_day": 5, "size_mb": 1, "users": 80},
            {"label": "Daily news", "per_user_per_day": 3, "size_mb": 1, "users": 80},
            {"label": "Monthly news", "per_user_per_day": 0.05, "size_mb": 20, "users": 80}],
        "records_per_month": 56000, "replicas": 2}}, rules)
    ok(abs(sp["files_gb_month"] - 62.4) < 0.05, f"62.4 GB files a month, got {sp['files_gb_month']}")
    ok([h["usable_gb"] for h in sp["horizons"]] == [1000, 3000, 5000], f"usable 1/3/5 TB, got {sp['horizons']}")
    ok(abs(sp["db_growth_gb_month"] - 1.0) < 0.05, "~1 GB DB growth a month for ~56k records")
    ok(sp["db_log_temp_gb"] == [50, 100] and sp["app_node_gb"] == [50, 100], "log/temp and app node ranges")

    # 4. POC (R13): app + DB + one combined services VM
    p = deal(tmp, "poc-10", {"active_users": 10, "scheme": "simple", "db": "pg", "recovery": "simple"},
             [{"name": "POC", "kind": "poc", "users": None}])
    run("calc", p, "--offline", os.path.join(FIX, "poc-10"))
    poc = lines(p, "POC")
    ok(set(poc) == {"app", "db", "poc_svc"}, f"POC lines app, db, services VM; got {set(poc)}")
    ok(poc.get("poc_svc") == (1, 6, 16), "POC services VM 6 CPU / 16 GB")

    # 5. Global search alone: calculator shows no cluster; R5 adds the simple Kubernetes set
    p = deal(tmp, "gs-only", {"active_users": 300, "scheme": "simple", "db": "mssql", "recovery": "full",
                              "components": ["global_search"]},
             [{"name": "Production", "kind": "prod", "users": None}])
    run("calc", p, "--offline", os.path.join(FIX, "gs-only"))
    g = lines(p, "Production")
    ok(g.get("k8s_master", (0,))[0] == 1 and g.get("k8s_node", (0,))[0] == 2, f"GS only: 1 + 2 Kubernetes, got {g}")

    # 6. R31 capacity: 400 mailboxes at 3 emails/s overflows the calculator's worker nodes
    p = deal(tmp, "el", {"active_users": 20000, "scheme": "fault_tolerant", "db": "pg", "recovery": "full",
                         "components": ["global_search", "dedup", "ml", "email_listener"],
                         "mailboxes": 400, "email_flow_per_s": 3},
             [{"name": "Production", "kind": "prod", "users": None}])
    shutil.copy(os.path.join(FIX, "rfi-20k", "calc-production.txt"), os.path.join(tmp, "el-calc-production.txt"))
    os.makedirs(os.path.join(tmp, "elfix"), exist_ok=True)
    shutil.copy(os.path.join(FIX, "rfi-20k", "calc-production.txt"), os.path.join(tmp, "elfix", "calc-production.txt"))
    run("calc", p, "--offline", os.path.join(tmp, "elfix"))
    ok(lines(p, "Production").get("k8s_node", (0,))[0] > 3, "R31 raises worker nodes for heavy mailbox sync")
    ok(sizing.el_replicas(400, 3) == (15, 14), f"EL 400 mailboxes, flow 3 -> 15 workers, 14 API; got {sizing.el_replicas(400, 3)}")
    ok(sizing.el_replicas(100, 0.5) == (0, 4), "EL 100 mailboxes, flow <1 -> 0 workers, 4 API")

    # 7. Guards: .NET + MS SQL refused; definitive wording refused
    p = deal(tmp, "guard", {"active_users": 100, "app_platform": "net", "db": "mssql"},
             [{"name": "Production", "kind": "prod", "users": None}])
    ok(run("calc", p).returncode != 0, "ST4: .NET + MS SQL refused")
    p = deal(tmp, "wording", {"active_users": 20000, "scheme": "fault_tolerant", "db": "pg", "recovery": "full",
                              "components": ["global_search", "dedup", "ml", "email_listener"]},
             [{"name": "Production", "kind": "prod", "users": None}],
             assumptions=[{"text": "This configuration is guaranteed to handle peak load.", "tag": "A"}])
    shutil.copy(os.path.join(FIX, "rfi-20k", "calc-production.txt"), os.path.join(tmp, "elfix", "calc-production.txt"))
    run("calc", p, "--offline", os.path.join(tmp, "elfix"))
    r = run("check", p)
    ok(r.returncode != 0 and "guaranteed" in r.stdout, "wording check catches 'guaranteed'")
    ok(run("build", p, "--nn", "5").returncode != 0, "build refuses on wording errors")

    # 9. Sizing-only start: create, reuse with any suffix, stop on a close match
    root = os.path.join(tmp, "team")
    os.makedirs(os.path.join(root, "Deals", "harbour-lending-wn"))
    os.makedirs(os.path.join(root, "Deals", "northwind-bank"))
    sc = sizing.team_config().get("sc")
    if sc:
        r = run("start", "--account", "Fictional Pawn Co", "--partner", "Partner X", "--root", root)
        d = os.path.join(root, "Deals", f"fictional-pawn-co-{sc}")
        ok(r.returncode == 0 and os.path.isdir(d), f"start creates <kebab>-<sc>: {r.stdout} {r.stderr}")
        ok(os.path.exists(os.path.join(d, "00-deal-start.md")), "start writes 00-deal-start.md")
        s = json.load(open(os.path.join(d, "sizing.json"), encoding="utf-8"))
        ok(s.get("entry", {}).get("type") == "sizing-only" and s["entry"]["partner"] == "Partner X", "entry recorded")
        r = run("start", "--account", "Fictional Pawn Co", "--root", root)
        ok(r.returncode == 0 and "already exists" in r.stdout, "second start reuses, no second sizing.json")
        r = run("start", "--account", "Harbour Lending", "--root", root)
        ok(r.returncode == 0 and "harbour-lending-wn" in r.stdout and
           not os.path.exists(os.path.join(root, "Deals", f"harbour-lending-{sc}")), "reuses another SC's folder")
        r = run("start", "--account", "Northwind Bank Group", "--root", root)
        ok(r.returncode != 0 and "northwind-bank" in r.stdout, "close match stops and asks")
        r = run("start", "--account", "Northwind Bank Group", "--root", root, "--confirm-new")
        ok(r.returncode == 0, "--confirm-new creates it anyway")
    else:
        print("note: no 'sc' in ~/.apac-sc-motion.json, start tests skipped")

    # 8. Status wording is never definitive
    for k, t in rules["wording"]["status"].items():
        ok(any(w in t.lower() for w in ("pending", "review", "to be confirmed")), f"status '{k}' stays tentative")
    r = run("review", p, "--status", "infra_reviewed")
    ok(r.returncode != 0, "infra_reviewed needs --by")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

if fails:
    print("FAIL")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("PASS")
