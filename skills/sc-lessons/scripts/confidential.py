"""Confidential customer terms: keep them in the deal folder, use generic labels everywhere shared.

Each deal can keep <deal>/confidential.json: terms the customer asked us not to share (their own category names,
criteria, internal programme names) and the generic label that replaces each one in anything written outside the
deal folder (library, lessons, feedback, team lessons, the weekly digest, decks for other audiences).
Standard: standards/CONFIDENTIAL-TERMS-v0.1.md.

  python confidential.py add    --deal <deal folder> --term "<their term>" --generic "<generic label>" [--note "..."] [--by "<name>"]
  python confidential.py never  --deal <deal folder> --item "<what must never be harvested, described generically>" [--by "<name>"]
  python confidential.py show   --deal <deal folder>
  python confidential.py redact --deal <deal folder> --in <file> [--out <file>]      (default: rewrites --in in place)
  python confidential.py scan   [--deal <deal folder> | --all [--root <team root>]] <file or folder> [...]

`scan` exits 1 and lists every hit when a listed term is still present, so a skill can refuse to write.
Matching is case-insensitive on whole words. The deal folder keeps the original wording; only shared outputs are generic.
"""
import argparse
import datetime
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TEXT_EXT = {".md", ".json", ".txt", ".html", ".csv", ".yaml", ".yml"}


def path(deal):
    return os.path.join(deal, "confidential.json")


def load(deal):
    p = path(deal)
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8"))
    return {"deal": os.path.basename(os.path.normpath(deal)), "terms": [], "never_harvest": [], "history": []}


def save(deal, d):
    json.dump(d, open(path(deal), "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def today():
    return datetime.date.today().isoformat()


def pattern(term):
    return re.compile(r"(?<![\w])" + re.escape(term) + r"(?![\w])", re.IGNORECASE)


def team_root():
    try:
        return json.load(open(os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json"), encoding="utf-8"))["sharepoint_root"]
    except Exception:
        sys.exit("No team root: run sc-setup first, or pass --root")


def all_terms(root):
    out = []
    deals = os.path.join(root, "Deals")
    for name in sorted(os.listdir(deals)):
        p = os.path.join(deals, name, "confidential.json")
        if os.path.isfile(p):
            for t in json.load(open(p, encoding="utf-8")).get("terms", []):
                out.append(dict(t, deal=name))
    return out


def add(a):
    d = load(a.deal)
    if any(t["term"].lower() == a.term.lower() for t in d["terms"]):
        sys.exit("'%s' is already listed. Edit confidential.json to change its generic label." % a.term)
    d["terms"].append({"term": a.term, "generic": a.generic, "note": a.note or "", "added": today(), "by": a.by or ""})
    d.setdefault("history", []).append({"action": "add", "generic": a.generic, "date": today(), "by": a.by or ""})
    save(a.deal, d)
    print("%s: 1 term listed (%d in all) -> shared outputs say '%s'" % (d["deal"], len(d["terms"]), a.generic))


def never(a):
    d = load(a.deal)
    d.setdefault("never_harvest", []).append({"item": a.item, "added": today(), "by": a.by or ""})
    save(a.deal, d)
    print("%s: never-harvest item added (%d in all)" % (d["deal"], len(d["never_harvest"])))


def show(a):
    d = load(a.deal)
    if not d["terms"] and not d.get("never_harvest"):
        print("%s: no confidential terms listed" % d["deal"])
        return
    print("%s: %d term(s), %d never-harvest item(s)" % (d["deal"], len(d["terms"]), len(d.get("never_harvest", []))))
    for t in d["terms"]:
        print("  term -> %s%s" % (t["generic"], "  (%s)" % t["note"] if t.get("note") else ""))
    for n in d.get("never_harvest", []):
        print("  never harvest: %s" % n["item"])


def redact_text(text, terms):
    # Longest first, so "Golden Archetype" is replaced before "Golden".
    hits = 0
    for t in sorted(terms, key=lambda t: -len(t["term"])):
        text, n = pattern(t["term"]).subn(t["generic"], text)
        hits += n
    return text, hits


def redact(a):
    terms = load(a.deal)["terms"]
    text = open(a.__dict__["in"], encoding="utf-8").read()
    new, hits = redact_text(text, terms)
    out = a.out or a.__dict__["in"]
    open(out, "w", encoding="utf-8").write(new)
    print("replaced %d occurrence(s) -> %s" % (hits, out))


def files(targets):
    for t in targets:
        if os.path.isdir(t):
            for base, dirs, names in os.walk(t):
                dirs[:] = [x for x in dirs if not x.startswith(".") and x != "__pycache__"]
                for n in names:
                    if os.path.splitext(n)[1].lower() in TEXT_EXT:
                        yield os.path.join(base, n)
        elif os.path.isfile(t):
            yield t


def scan(a):
    if a.deal:
        terms = [dict(t, deal=load(a.deal)["deal"]) for t in load(a.deal)["terms"]]
    elif a.all:
        terms = all_terms(a.root or team_root())
    else:
        sys.exit("Pass --deal <deal folder> or --all")
    if not terms:
        print("no confidential terms listed: nothing to check")
        return
    found = 0
    for f in files(a.targets):
        try:
            text = open(f, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for t in terms:
            n = len(pattern(t["term"]).findall(text))
            if n:
                found += n
                # Never print the term itself: the scan output can end up in shared logs.
                print("HIT %s: %d x term from %s (use '%s')" % (f, n, t["deal"], t["generic"]))
    if found:
        print("%d confidential occurrence(s). Replace them (confidential.py redact) before writing anything shared." % found)
        sys.exit(1)
    print("clean: %d term(s) checked" % len(terms))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("add"); p.add_argument("--deal", required=True); p.add_argument("--term", required=True)
    p.add_argument("--generic", required=True); p.add_argument("--note"); p.add_argument("--by")
    p = sp.add_parser("never"); p.add_argument("--deal", required=True); p.add_argument("--item", required=True); p.add_argument("--by")
    p = sp.add_parser("show"); p.add_argument("--deal", required=True)
    p = sp.add_parser("redact"); p.add_argument("--deal", required=True); p.add_argument("--in", required=True); p.add_argument("--out")
    p = sp.add_parser("scan"); p.add_argument("--deal"); p.add_argument("--all", action="store_true"); p.add_argument("--root")
    p.add_argument("targets", nargs="+")
    a = ap.parse_args()
    {"add": add, "never": never, "show": show, "redact": redact, "scan": scan}[a.cmd](a)


if __name__ == "__main__":
    main()
