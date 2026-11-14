"""SC Academy: progress, stand guard, feedback, skill fingerprints and the weekly training note.

Team root (the synced SharePoint folder) comes from ~/.apac-sc-motion.json ("sharepoint_root"), APAC_SC_ROOT, or --root.
Everything the course writes lives in <team root>/Lessons/training/ and the trainee's practice folder
<team root>/Deals/_practice/<sc>-academy-kestrel/. The course itself (course.json, modules/) lives in the plugin and
only changes when Renzo approves (see `stamp`).

Trainee
  python academy.py status    --sc "Willy Noviandy"               where they are, what's next
  python academy.py start     --sc "Willy Noviandy" --initials wn  create the progress file + practice folder
  python academy.py stand     --sc "..." --name <clio env> [--url <url>] [--renzo-ok]
                                                                    record the training stand (refuses a deal's or another trainee's stand)
  python academy.py at        --sc "..." --module B1 --step 3      save the current step
  python academy.py result    --sc "..." --module B1 --result pass|fail [--note "..."]
                                                                    record the hands-on check (pass closes the module)
  python academy.py feedback  --sc "..." --module B1 --hardest "..." --lab "..." --useful 4 [--change "..."]
                                                                    the three end-of-module questions -> Lessons/feedback/

Course upkeep (Renzo, Fridays via sc-weekly-lessons)
  python academy.py refresh                       fingerprint every SKILL.md (toolkit, app-dev toolkit, this plugin),
                                                  diff against the module stamps and the last run, mark stale modules,
                                                  write a draft per stale module to Lessons/training/_drafts/
  python academy.py stamp --module B1 --authoring     the author records what the module was written against (pending)
  python academy.py stamp --module B1 --by "Renzo Huruiti"
                                                  only after Renzo's yes: the module is approved as it is
  python academy.py weekly [--days 7]             tips for Renzo -> Lessons/training/weekly/<yyyy-Www>.md
  python academy.py pages [--out <dir>]           readable HTML module pages (default Lessons/training/pages/)

Another course on the same engine: put --course <course.json> before the command (state goes to its "state_dir";
"watch_docs" adds runbooks and other docs to the fingerprints). Used by sc-customer-academy.
"""
import argparse
import datetime
import difflib
import glob
import hashlib
import html
import json
import os
import platform
import re
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
PLUGIN_ROOT = os.path.normpath(os.path.join(SKILL_DIR, "..", ".."))
COURSE = os.path.join(SKILL_DIR, "course.json")
CONFIG = os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json")
INSTALLED = os.path.join(os.path.expanduser("~"), ".claude", "plugins", "installed_plugins.json")
CACHE = os.path.join(os.path.expanduser("~"), ".claude", "plugins", "cache")

SOURCES = {  # prefix used in course.json -> how to find the skills folder
    "toolkit": ("creatio-demo-toolkit@", os.path.join("creatio-demo-lab", "creatio-demo-toolkit")),
    "appdev": ("creatio-ai-app-development-toolkit@", None),
}


# ---------------------------------------------------------------- plumbing

def today():
    return datetime.date.today().isoformat()


def kebab(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def team_root(arg=None):
    if arg:
        return arg
    if os.environ.get("APAC_SC_ROOT"):
        return os.environ["APAC_SC_ROOT"]
    try:
        with open(CONFIG, encoding="utf-8") as fh:
            root = json.load(fh).get("sharepoint_root")
        if root and os.path.isdir(root):
            return root
    except (OSError, ValueError):
        pass
    sys.exit("No team root: run sc-setup, set APAC_SC_ROOT, or pass --root <SharePoint folder>")


def state_dir():
    """Where this course keeps progress and state, relative to the team root (course.json "state_dir")."""
    return (load_json(COURSE, {}) or {}).get("state_dir", "Lessons/training").split("/")


def tdir(root, *parts):
    p = os.path.join(root, *state_dir(), *parts)
    os.makedirs(p if not os.path.splitext(p)[1] else os.path.dirname(p), exist_ok=True)
    return p


def load_json(p, default=None):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def save_json(p, data):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, p)
    return p


def course():
    c = load_json(COURSE)
    if not c:
        sys.exit("course.json missing or invalid: %s" % COURSE)
    return c


def modules(c, include_planned=False):
    out = []
    for path in c["paths"]:
        if path.get("status") == "planned" and not include_planned:
            continue
        for m in path["modules"]:
            out.append(dict(m, path=path["id"], path_status=path.get("status", "live")))
    return out


def module_by_id(c, mid):
    for m in modules(c, include_planned=True):
        if m["id"].lower() == mid.lower():
            return m
    sys.exit("No module %s in course.json" % mid)


# ---------------------------------------------------------------- progress

def progress_path(root, sc):
    return os.path.join(tdir(root), "%s.json" % kebab(sc))


def get_progress(root, sc, must=True):
    p = load_json(progress_path(root, sc))
    if p is None and must:
        sys.exit("No progress file for %s yet: run `academy.py start --sc \"%s\" --initials <xx>` first" % (sc, sc))
    return p


def put_progress(root, prog):
    prog["updated"] = today()
    return save_json(progress_path(root, prog["sc"]), prog)


def next_module(c, prog):
    done = prog.get("done", {})
    for m in modules(c):
        if m["id"] not in done and m["id"] not in prog.get("skipped", []):
            return m
    return None


def cmd_start(a):
    root = team_root(a.root)
    c = course()
    prog = get_progress(root, a.sc, must=False)
    if prog:
        print("Progress file already exists for %s (module %s). Nothing changed." % (a.sc, prog.get("module")))
        return
    practice = os.path.join("Deals", "_practice", "%s-academy-kestrel" % kebab(a.sc.split()[0]))
    os.makedirs(os.path.join(root, practice), exist_ok=True)
    first = modules(c)[0]["id"]
    prog = {"sc": a.sc, "initials": a.initials.lower(), "course_version": c["version"], "module": first, "step": 1,
            "practice_dir": practice.replace("\\", "/"), "stand": None, "lab_package": None,
            "started": {first: today()}, "done": {}, "skipped": [], "results": [], "notes": [], "updated": today()}
    print(put_progress(root, prog))
    print("Practice folder: %s" % os.path.join(root, practice))


def cmd_status(a):
    root = team_root(a.root)
    c = course()
    prog = get_progress(root, a.sc)
    stale = load_json(os.path.join(tdir(root, "_state"), "stale.json"), {}).get("stale", {})
    print("%s: course %s, stand %s" % (prog["sc"], prog.get("course_version"),
                                      (prog.get("stand") or {}).get("name", "not set")))
    for m in modules(c):
        mark = "done %s" % prog["done"][m["id"]] if m["id"] in prog.get("done", {}) else (
            "skipped" if m["id"] in prog.get("skipped", []) else (
                "NOW (step %s)" % prog.get("step") if m["id"] == prog.get("module") else ""))
        flag = "  [being updated]" if m["id"] in stale else ""
        print("  %-4s %-48s %s%s" % (m["id"], m["title"], mark, flag))
    nm = next_module(c, prog)
    print("Next: %s" % ("%s %s" % (nm["id"], nm["title"]) if nm else "path complete"))


def cmd_at(a):
    root = team_root(a.root)
    prog = get_progress(root, a.sc)
    m = module_by_id(course(), a.module)
    prog["module"], prog["step"] = m["id"], a.step
    prog.setdefault("started", {}).setdefault(m["id"], today())
    if a.note:
        prog.setdefault("notes", []).append("%s %s: %s" % (today(), m["id"], a.note))
    print(put_progress(root, prog))


def cmd_result(a):
    root = team_root(a.root)
    c = course()
    prog = get_progress(root, a.sc)
    m = module_by_id(c, a.module)
    prog.setdefault("results", []).append({"module": m["id"], "result": a.result, "date": today(), "note": a.note or ""})
    if a.result == "pass":
        prog.setdefault("done", {})[m["id"]] = today()
        nm = next_module(c, prog)
        if nm:
            prog["module"], prog["step"] = nm["id"], 1
            prog.setdefault("started", {}).setdefault(nm["id"], today())
        else:
            prog["module"], prog["step"] = None, None
    print(put_progress(root, prog))
    fails = sum(1 for r in prog["results"] if r["module"] == m["id"] and r["result"] == "fail")
    if a.result == "fail" and fails >= 2:
        print("Second fail on %s: suggest the trainee books 15 minutes with Renzo (it shows in Friday's tips)." % m["id"])


# ---------------------------------------------------------------- stand guard

def cmd_stand(a):
    """Each trainee has a training stand of their own. Refuse a stand named in a real deal's notes or another trainee's file."""
    root = team_root(a.root)
    prog = get_progress(root, a.sc)
    needles = [n for n in {a.name, (a.url or "").split("//")[-1].split("/")[0].split(".")[0]} if n and len(n) >= 4]
    hits = []
    deals = os.path.join(root, "Deals")
    for d in glob.glob(os.path.join(deals, "*")):
        base = os.path.basename(d)
        if base.startswith("_") or not os.path.isdir(d):
            continue
        for f in glob.glob(os.path.join(d, "**", "*.md"), recursive=True) + glob.glob(os.path.join(d, "*.json")):
            try:
                with open(f, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            if any(n.lower() in text.lower() for n in needles):
                hits.append("%s/%s" % (base, os.path.relpath(f, d).replace("\\", "/")))
                break
    for f in glob.glob(os.path.join(root, *state_dir(), "*.json")):
        other = load_json(f) or {}
        if other.get("sc") and other.get("sc") != prog["sc"] and (other.get("stand") or {}).get("name", "").lower() == a.name.lower():
            hits.append("training: already %s's training stand (one stand per trainee)" % other["sc"])
    if hits and not a.renzo_ok:
        print("REFUSED: %s is named in real deal notes or used by another trainee:" % a.name)
        for h in hits[:10]:
            print("  - %s" % h)
        print("Each SC trains on a stand of their own with no customer demo. Ask Renzo for yours; only with his yes re-run with --renzo-ok.")
        sys.exit(2)
    prog["stand"] = {"name": a.name, "url": a.url, "checked": today(), "deal_hits": hits,
                     "renzo_ok": bool(a.renzo_ok)}
    prog["lab_package"] = prog.get("lab_package") or "Acad%s" % prog["initials"].capitalize()
    print(put_progress(root, prog))
    print("Training stand %s recorded. Lab app 'Academy Kestrel', package name must contain %s." % (
        a.name, prog["lab_package"]))


# ---------------------------------------------------------------- feedback

def cmd_feedback(a):
    root = team_root(a.root)
    m = module_by_id(course(), a.module)
    ini = (get_progress(root, a.sc, must=False) or {}).get("initials") or "unknown"
    d = os.path.join(root, "Lessons", "feedback", ini)  # private per SC (FEEDBACK-LOOP v0.2 section 5)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "%s-%s-academy-%s.md" % (today(), kebab(a.sc), m["id"].lower()))
    n = 2
    while os.path.exists(p):
        p = os.path.join(d, "%s-%s-academy-%s-%d.md" % (today(), kebab(a.sc), m["id"].lower(), n))
        n += 1
    sev = "blocker" if a.blocker else ("annoying" if (a.useful or 5) <= 2 else "idea")
    text = "\n".join([
        "# Academy %s %s: %s" % (m["id"], m["title"], (a.hardest or "no notes")[:80]),
        "- SC: %s · Deal: academy (fictional Kestrel) · Skill + step: sc-academy, module %s · Source: training · Module: %s · Kind: process · Date: %s"
        % (a.sc, m["id"], m["id"], today()),
        "- What happened: hardest or unclear: %s" % (a.hardest or "-"),
        "- What happened: did the lab work as written: %s" % (a.lab or "-"),
        "- What they'd change: %s" % (a.change or "-"),
        "- How it felt (1-5): %s (useful for real deals)" % (a.useful if a.useful is not None else "-"),
        "- Skills used: %s" % ", ".join(m.get("skills", [])),
        "- Severity: %s" % sev, ""])
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(p)


# ---------------------------------------------------------------- fingerprints

def plugin_dir(prefix, cache_sub):
    data = load_json(INSTALLED, {}) or {}
    for key, entries in (data.get("plugins") or data).items():
        if isinstance(entries, list) and key.startswith(prefix) and entries:
            p = entries[0].get("installPath")
            if p and os.path.isdir(p):
                return p, entries[0].get("version")
    if cache_sub:
        vers = sorted(glob.glob(os.path.join(CACHE, cache_sub, "*")), key=os.path.getmtime)
        if vers:
            return vers[-1], os.path.basename(vers[-1])
    return None, None


def frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith(" "):
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip().strip('"')
    return out


def scan():
    """Every SKILL.md we can see: {"toolkit:creatio-object-model": {name, version, hash, path, lines}}, plus the
    course's watch_docs (e.g. "appdev-doc:runbooks/01-environment-setup.md") for guidance that isn't a SKILL.md."""
    found, where = {}, {}
    roots = []
    for src, (prefix, sub) in SOURCES.items():
        p, ver = plugin_dir(prefix, sub)
        override = os.environ.get("ACADEMY_%s_DIR" % src.upper())  # testing: a copy of a plugin folder
        if override:
            p, ver = override, "override"
        if p:
            roots.append((src, os.path.join(p, "skills"), ver))
    pj = load_json(os.path.join(PLUGIN_ROOT, ".claude-plugin", "plugin.json"), {})
    roots.append(("plugin", os.path.join(PLUGIN_ROOT, "skills"), pj.get("version")))
    for src, skills, ver in roots:
        where[src] = {"skills": skills, "version": ver}
        for f in sorted(glob.glob(os.path.join(skills, "*", "SKILL.md"))):
            with open(f, "rb") as fh:
                raw = fh.read().replace(b"\r\n", b"\n")
            text = raw.decode("utf-8", errors="replace")
            fm = frontmatter(text)
            name = fm.get("name") or os.path.basename(os.path.dirname(f))
            key = "%s:%s" % (src, os.path.basename(os.path.dirname(f)))
            found[key] = {"name": name, "version": fm.get("version") or ver, "hash": hashlib.sha256(raw).hexdigest()[:16],
                          "lines": text.count("\n"), "path": f}
    for src, patterns in ((load_json(COURSE, {}) or {}).get("watch_docs") or {}).items():
        if src not in where:
            continue
        base = os.path.dirname(where[src]["skills"])
        for pat in patterns:
            for f in sorted(glob.glob(os.path.join(base, pat))):
                with open(f, "rb") as fh:
                    raw = fh.read().replace(b"\r\n", b"\n")
                rel = os.path.relpath(f, base).replace("\\", "/")
                found["%s-doc:%s" % (src, rel)] = {"name": rel, "version": where[src]["version"],
                                                  "hash": hashlib.sha256(raw).hexdigest()[:16],
                                                  "lines": raw.count(b"\n"), "path": f}
    return found, where


def clio_version():
    for cmd in (["clio", "--version"], ["clio", "ver"]):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            out = (r.stdout or r.stderr).strip().splitlines()
            if r.returncode == 0 and out:
                return out[0][:80]
        except (OSError, subprocess.SubprocessError):
            continue
    return None


def snapshot(root, key, info):
    p = os.path.join(tdir(root, "_state", "snapshots"), key.replace(":", "__").replace("/", "__"), "%s.md" % info["hash"])
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(info["path"], encoding="utf-8", errors="replace") as src, open(p, "w", encoding="utf-8") as dst:
            dst.write(src.read().replace("\r\n", "\n"))
    return p


def read_snapshot(root, key, h):
    p = os.path.join(root, *state_dir(), "_state", "snapshots", key.replace(":", "__").replace("/", "__"), "%s.md" % h)
    try:
        with open(p, encoding="utf-8") as fh:
            return fh.read().splitlines()
    except OSError:
        return None


def cmd_refresh(a):
    root = team_root(a.root)
    c = course()
    found, where = scan()
    state_dir = tdir(root, "_state")
    last = load_json(os.path.join(state_dir, "fingerprints.json"), {}) or {}
    last_sk = last.get("skills", {})
    for k, v in found.items():
        snapshot(root, k, v)

    changed = sorted(k for k in found if k in last_sk and last_sk[k]["hash"] != found[k]["hash"])
    new = sorted(k for k in found if k not in last_sk) if last_sk else []
    gone = sorted(k for k in last_sk if k not in found)

    covered = set()
    stale = {}
    for m in modules(c, include_planned=True):
        covered.update(m.get("skills", []))
        if m.get("path_status") == "planned":
            continue
        why = []
        for s in m.get("skills", []):
            stamp = (m.get("built_against") or {}).get(s)
            cur = found.get(s)
            if cur is None:
                if s.split(":")[0] in where:
                    why.append({"skill": s, "change": "missing", "was": stamp})
            elif stamp is None:
                why.append({"skill": s, "change": "never stamped", "now": cur["hash"]})
            elif stamp != cur["hash"]:
                why.append({"skill": s, "change": "changed", "was": stamp, "now": cur["hash"],
                            "version": cur["version"]})
        if why:
            stale[m["id"]] = {"title": m["title"], "file": m["file"], "why": why}
    ignore = set(c.get("not_taught", {}).keys())
    srcs = c.get("teaches_sources") or ["toolkit", "appdev", "plugin"]
    uncovered = sorted(k for k in found if k not in covered and k not in ignore and k.split(":")[0] in srcs
                       and not k.startswith(("plugin:sc-academy", "plugin:sc-customer-academy")))

    drafts = []
    ddir = tdir(root, "_drafts")
    for mid, s in stale.items():
        p = os.path.join(ddir, "%s-%s.md" % (today(), mid))
        lines = ["# Draft update: module %s %s (%s)" % (mid, s["title"], today()), "",
                 "> Written by `academy.py refresh`. **Not live.** Claude fills 'Proposed edits'; Renzo approves; only then",
                 "> the module file changes in the plugin and `academy.py stamp --module %s --by \"Renzo Huruiti\"` runs." % mid,
                 "", "Module file: `skills/%s/%s`" % (os.path.basename(SKILL_DIR), s["file"]), "", "## What changed", ""]
        for w in s["why"]:
            lines.append("- `%s`: %s%s" % (w["skill"], w["change"],
                                            " (now version %s)" % w.get("version") if w.get("version") else ""))
        for w in s["why"]:
            if w["change"] != "changed":
                continue
            old = read_snapshot(root, w["skill"], w["was"])
            new_txt = read_snapshot(root, w["skill"], w["now"])
            lines += ["", "### Diff of %s" % w["skill"], ""]
            if old is None or new_txt is None:
                lines.append("(No snapshot of the stamped version: read the new SKILL.md in full: `%s`)" %
                             found[w["skill"]]["path"])
                continue
            diff = list(difflib.unified_diff(old, new_txt, "stamped", "now", n=1, lineterm=""))
            lines += ["```diff"] + diff[:400] + (["... (%d more lines)" % (len(diff) - 400)] if len(diff) > 400 else []) + ["```"]
        lines += ["", "## Proposed edits (Claude, for Renzo)", "", "_Section, current text, proposed text, why. Lab and check still pass?_", ""]
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        drafts.append(p)

    save_json(os.path.join(state_dir, "fingerprints.json"),
              {"date": today(), "machine": platform.node(),
               "sources": where, "clio": clio_version(),
               "skills": {k: {kk: v[kk] for kk in ("name", "version", "hash", "lines")} for k, v in found.items()}})
    hist = load_json(os.path.join(state_dir, "history.json"), []) or []
    hist.append({"date": today(), "changed": changed, "new": new, "gone": gone, "stale": sorted(stale)})
    save_json(os.path.join(state_dir, "history.json"), hist[-60:])
    save_json(os.path.join(state_dir, "stale.json"), {"date": today(), "stale": stale, "uncovered": uncovered,
                                                      "since_last_run": {"changed": changed, "new": new, "gone": gone}})

    print("Skills seen: %d (%s)" % (len(found), ", ".join("%s %s" % (k, v["version"]) for k, v in where.items())))
    print("Since last run (%s): %d changed, %d new, %d gone" % (last.get("date", "never"), len(changed), len(new), len(gone)))
    for k in changed + new + gone:
        print("  %s %s" % ("changed" if k in changed else "new" if k in new else "gone", k))
    print("Stale modules: %d" % len(stale))
    for mid, s in stale.items():
        print("  %s %s: %s" % (mid, s["title"], "; ".join("%s %s" % (w["skill"], w["change"]) for w in s["why"])))
    print("Skills no module teaches: %d%s" % (len(uncovered), (": " + ", ".join(uncovered)) if uncovered else ""))
    for p in drafts:
        print("draft: %s" % p)


def cmd_stamp(a):
    """Record the hash of every skill a module uses, as they are now.

    --by "Renzo Huruiti"  Renzo approved the module as it is: status approved.
    --authoring           whoever wrote or updated the module: status pending until Renzo stamps it himself.
    """
    if a.authoring:
        by, status = "authoring session, waiting for Renzo's approval", "pending"
    elif a.by and "renzo" in a.by.lower():
        by, status = a.by, "approved"
    else:
        sys.exit("Only Renzo approves course changes (--by \"Renzo Huruiti\", after his yes in chat); "
                 "an author records a pending stamp with --authoring.")
    c = course()
    found, _ = scan()
    ids = [m["id"] for m in modules(c)] if a.module.lower() == "all" else [a.module]
    for path in c["paths"]:
        for m in path["modules"]:
            if m["id"] in ids or m["id"].lower() in [i.lower() for i in ids]:
                m["built_against"] = {s: found[s]["hash"] for s in m.get("skills", []) if s in found}
                m["stamped"] = {"date": today(), "by": by, "status": status}
    c["updated"] = today()
    with open(COURSE, "w", encoding="utf-8") as fh:
        json.dump(c, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("Stamped %s (%s) in %s. Commit it with the module edit; it goes live with the next release." % (
        ", ".join(ids), status, COURSE))


# ---------------------------------------------------------------- weekly tips

def cmd_weekly(a):
    root = team_root(a.root)
    c = course()
    since = (datetime.date.today() - datetime.timedelta(days=a.days)).isoformat()
    mods = {m["id"]: m for m in modules(c)}
    progs = [load_json(p) for p in glob.glob(os.path.join(root, *state_dir(), "*.json"))]
    progs = [p for p in progs if p and p.get("sc")]
    stuck, fails, finished = [], {}, []
    for p in progs:
        mid = p.get("module")
        started = (p.get("started") or {}).get(mid)
        if mid and started and started <= (datetime.date.today() - datetime.timedelta(days=7)).isoformat():
            stuck.append((mid, (datetime.date.today() - datetime.date.fromisoformat(started)).days, p.get("step")))
        for r in p.get("results", []):
            if r["result"] == "fail":
                fails.setdefault(r["module"], []).append(r.get("note", ""))
        finished += [m for m, d in (p.get("done") or {}).items() if d >= since]
    fb = {}
    for f in glob.glob(os.path.join(root, "Lessons", "feedback", "*.md")) + glob.glob(os.path.join(root, "Lessons", "feedback", "*", "*.md")):
        try:
            with open(f, encoding="utf-8") as fh:
                t = fh.read()
        except OSError:
            continue
        if "Source: training" not in t:
            continue
        mm = re.search(r"Module: (\w+)", t)
        dm = re.search(r"Date: (\d{4}-\d\d-\d\d)", t)
        if not mm or (dm and dm.group(1) < since):
            continue
        rating = re.search(r"How it felt \(1-5\): (\d)", t)
        hard = re.search(r"hardest or unclear: (.*)", t)
        lab = re.search(r"did the lab work as written: (.*)", t)
        fb.setdefault(mm.group(1), []).append({"rating": int(rating.group(1)) if rating else None,
                                              "hard": hard.group(1).strip() if hard else "",
                                              "lab": lab.group(1).strip() if lab else ""})
    st = load_json(os.path.join(root, *state_dir(), "_state", "stale.json"), {}) or {}
    week = datetime.date.today().isocalendar()
    wk = "%d-W%02d" % (week[0], week[1])
    L = ["# SC Academy: tips for Renzo, %s" % wk, "",
         "> `academy.py weekly`, %s, last %d days. Patterns, not people: no names next to ratings." % (today(), a.days), "",
         "## Decisions for you", ""]
    n = 0
    for mid, s in (st.get("stale") or {}).items():
        n += 1
        L.append("%d. Module %s %s is stale (%s). Draft in `%s/_drafts/`: approve the update?" % (
            n, mid, s["title"], "; ".join("%s %s" % (w["skill"], w["change"]) for w in s["why"]), "/".join(state_dir())))
    pend = [m["id"] for m in modules(c) if (m.get("stamped") or {}).get("status") != "approved"]
    if pend:
        n += 1
        L.append("%d. Module(s) %s are not approved by you yet (new or updated). Read them (`academy.py pages`), then "
                 "approve with `stamp --module <id> --by \"Renzo Huruiti\"`?" % (n, ", ".join(pend)))
    unc = st.get("uncovered") or []
    if unc:
        n += 1
        L.append("%d. %d skill(s) no module teaches: %s. Add a module, add to a planned path, or mark not taught?" % (
            n, len(unc), ", ".join(unc)))
    if not n:
        L.append("None this week.")
    L += ["", "## Where people get stuck", "", "| Module | Signal | Detail |", "|---|---|---|"]
    rows = 0
    for mid, days, step in stuck:
        L.append("| %s %s | on it for %d days | step %s |" % (mid, mods.get(mid, {}).get("title", ""), days, step)); rows += 1
    for mid, notes in fails.items():
        L.append("| %s %s | %d failed check(s) | %s |" % (mid, mods.get(mid, {}).get("title", ""), len(notes),
                                                         "; ".join(x for x in notes if x)[:200])); rows += 1
    for mid, items in fb.items():
        rs = [i["rating"] for i in items if i["rating"]]
        low = [i for i in items if (i["rating"] or 5) <= 3 or (i["lab"] and not i["lab"].lower().startswith(("yes", "-")))]
        if rs:
            L.append("| %s %s | usefulness %.1f / 5 (%d answers) | %s |" % (
                mid, mods.get(mid, {}).get("title", ""), sum(rs) / len(rs), len(rs),
                "; ".join((i["hard"] or i["lab"])[:90] for i in low)[:300])); rows += 1
    if not rows:
        L.append("| - | nothing this week | |")
    L += ["", "## Progress", "", "| Measure | Value |", "|---|---|",
          "| Trainees with a progress file | %d |" % len(progs),
          "| Modules finished this week | %d |" % len(finished),
          "| Trainees who finished path 1 | %d |" % sum(1 for p in progs if all(m in (p.get("done") or {}) for m in mods)),
          "| Training feedback files this week | %d |" % sum(len(v) for v in fb.values()), ""]
    sug = [m for m in unc][:3]
    L += ["## Suggested new modules", ""]
    if sug:
        L += ["- `%s`: no module teaches it yet" % s for s in sug]
    for p in c["paths"]:
        if p.get("status") == "planned":
            L.append("- Planned path %s %s: %s" % (p["id"], p["title"], ", ".join(m["title"] for m in p["modules"])))
    out = os.path.join(tdir(root, "weekly"), "%s.md" % wk)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))
    print(out)


# ---------------------------------------------------------------- readable pages

def md_to_html(md):
    out, inlist, intable, incode = [], False, False, False

    def inline(s):
        s = html.escape(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)

    for line in md.splitlines():
        if line.startswith("```"):
            out.append("</pre>" if incode else "<pre>")
            incode = not incode
            continue
        if incode:
            out.append(html.escape(line))
            continue
        if intable and not line.startswith("|"):
            out.append("</table>"); intable = False
        if inlist and not re.match(r"^\s*([-*]|\d+\.) ", line):
            out.append("</ul>"); inlist = False
        if line.startswith("|"):
            cells = [x.strip() for x in line.strip().strip("|").split("|")]
            if all(re.match(r"^:?-+:?$", x) for x in cells if x):
                continue
            if not intable:
                out.append("<table>"); intable = True
                out.append("<tr>%s</tr>" % "".join("<th>%s</th>" % inline(x) for x in cells))
            else:
                out.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(x) for x in cells))
        elif re.match(r"^#{1,4} ", line):
            lvl = len(line.split(" ")[0])
            out.append("<h%d>%s</h%d>" % (lvl, inline(line[lvl + 1:]), lvl))
        elif re.match(r"^\s*([-*]|\d+\.) ", line):
            if not inlist:
                out.append("<ul>"); inlist = True
            out.append("<li>%s</li>" % inline(re.sub(r"^\s*([-*]|\d+\.) ", "", line)))
        elif line.startswith(">"):
            out.append("<blockquote>%s</blockquote>" % inline(line.lstrip("> ")))
        elif line.strip():
            out.append("<p>%s</p>" % inline(line))
    return "\n".join(out)


CSS = """:root{--bg:#fff;--fg:#1d2433;--mute:#5b6475;--line:#d9dee7;--accent:#0b6e75;--code:#f3f5f8}
@media (prefers-color-scheme: dark){:root{--bg:#141820;--fg:#e6e9ef;--mute:#a3abba;--line:#2c3340;--accent:#4fc3c9;--code:#1e2430}}
body{background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,Segoe UI,sans-serif;max-width:900px;margin:0 auto;padding:24px 16px}
h1,h2,h3{color:var(--accent);line-height:1.25}table{border-collapse:collapse;width:100%;margin:12px 0;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}th{background:var(--code)}
code,pre{background:var(--code);border-radius:4px}code{padding:1px 4px}pre{padding:10px;overflow-x:auto}
blockquote{color:var(--mute);border-left:3px solid var(--line);margin:8px 0;padding-left:10px}a{color:var(--accent)}"""


def cmd_pages(a):
    c = course()
    out = a.out or tdir(team_root(a.root), "pages")
    os.makedirs(out, exist_ok=True)
    idx = ["# %s" % c["title"], "", c["about"], "", "| Path | Module | Minutes | Needs a stand |", "|---|---|---|---|"]
    for m in modules(c):
        src = os.path.join(SKILL_DIR, m["file"])
        with open(src, encoding="utf-8") as fh:
            body = fh.read()
        name = os.path.basename(m["file"]).replace(".md", ".html")
        with open(os.path.join(out, name), "w", encoding="utf-8") as fh:
            fh.write("<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
                     "<title>%s %s</title><style>%s</style><p><a href='index.html'>Course index</a></p>%s" % (
                         m["id"], html.escape(m["title"]), CSS, md_to_html(body)))
        idx.append("| %s | [%s %s](%s) | %s | %s |" % (m["path"], m["id"], m["title"], name, m.get("minutes", ""),
                                                      "yes" if m.get("stand") else "no"))
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as fh:
        fh.write("<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
                 "<title>SC Academy</title><style>%s</style>%s" % (CSS, md_to_html("\n".join(idx))))
    print(os.path.join(out, "index.html"))


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root")
    ap.add_argument("--course", help="another course.json using this engine (e.g. ../sc-customer-academy/course.json)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start"); s.add_argument("--sc", required=True); s.add_argument("--initials", required=True)
    s = sub.add_parser("status"); s.add_argument("--sc", required=True)
    s = sub.add_parser("at"); s.add_argument("--sc", required=True); s.add_argument("--module", required=True)
    s.add_argument("--step", type=int, required=True); s.add_argument("--note")
    s = sub.add_parser("result"); s.add_argument("--sc", required=True); s.add_argument("--module", required=True)
    s.add_argument("--result", choices=["pass", "fail"], required=True); s.add_argument("--note")
    s = sub.add_parser("stand"); s.add_argument("--sc", required=True); s.add_argument("--name", required=True)
    s.add_argument("--url"); s.add_argument("--renzo-ok", action="store_true")
    s = sub.add_parser("feedback"); s.add_argument("--sc", required=True); s.add_argument("--module", required=True)
    s.add_argument("--hardest"); s.add_argument("--lab"); s.add_argument("--useful", type=int, choices=range(1, 6))
    s.add_argument("--change"); s.add_argument("--blocker", action="store_true")
    sub.add_parser("refresh")
    s = sub.add_parser("stamp"); s.add_argument("--module", required=True); s.add_argument("--by")
    s.add_argument("--authoring", action="store_true")
    s = sub.add_parser("weekly"); s.add_argument("--days", type=int, default=7)
    s = sub.add_parser("pages"); s.add_argument("--out")
    a = ap.parse_args()
    if a.course:
        global COURSE, SKILL_DIR
        COURSE = os.path.abspath(a.course)
        SKILL_DIR = os.path.dirname(COURSE)
    {"start": cmd_start, "status": cmd_status, "at": cmd_at, "result": cmd_result, "stand": cmd_stand,
     "feedback": cmd_feedback, "refresh": cmd_refresh, "stamp": cmd_stamp, "weekly": cmd_weekly,
     "pages": cmd_pages}[a.cmd](a)


if __name__ == "__main__":
    main()
