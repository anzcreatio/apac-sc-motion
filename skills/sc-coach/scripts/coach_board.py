"""Renzo's local view of each SC: their private coaching files and their feedback files, one folder per SC.

  python coach_board.py [--out "%USERPROFILE%\\SC-Coaching"] [--root <team root>]

Reads (team root from ~/.apac-sc-motion.json):
  Lessons/coaching/<initials>/*.md   private coaching from sc-coach
  Lessons/feedback/<initials>/*.md   feedback files (private per SC; older flat files matched by the "SC:" line or name)
Writes, in --out (a local folder, NOT OneDrive or SharePoint, so nothing syncs):
  OVERVIEW.md                        one row per SC: calls coached, latest habits, feedback count
  <initials>-<first-name>/README.md  that SC's coaching (date, deal, habits) and feedback (date, skill, severity)
  <initials>-<first-name>/coaching/  copies of the coaching files
  <initials>-<first-name>/feedback/  copies of the feedback files
It copies and indexes only; it never deletes. Files you put in coaching/ or feedback/ by hand are indexed too.
Run it whenever you want an up-to-date view (the Friday digest runs it).
"""
import argparse
import datetime
import glob
import json
import os
import re
import shutil
import sys

TEAM = {"rh": "Renzo Huruiti", "wn": "Willy Noviandy", "fa": "Ferdhi Adrian"}


def team_root(arg):
    if arg:
        return arg
    try:
        with open(os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json"), encoding="utf-8") as fh:
            return json.load(fh)["sharepoint_root"]
    except (OSError, KeyError, ValueError):
        sys.exit("No team root: run sc-setup, or pass --root <SharePoint folder>")


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def who_wrote(path, text):
    m = re.search(r"SC:\s*([^·\n]+)", text)
    if m:
        name = m.group(1).strip().lower()
        for ini, full in TEAM.items():
            if full.lower() in name or name in full.lower() or name.split()[0] == full.lower().split()[0]:
                return ini
    base = os.path.basename(path).lower()
    for ini, full in TEAM.items():
        if slug(full) in base:
            return ini
    return None


def read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def first_line(text):
    for line in text.splitlines():
        if line.strip():
            return line.lstrip("# ").strip()
    return ""


def habits(text):
    m = re.search(r"## Top three habits\s*\n(.*?)(?=\n## |\Z)", text, re.S)
    if not m:
        return []
    return [re.sub(r"\*\*", "", h).strip(" .") for h in re.findall(r"^\d\.\s+\*\*(.+?)\*\*", m.group(1), re.M)]


def field(text, key):
    m = re.search(re.escape(key) + r":\s*([^·\n]+)", text)
    return m.group(1).strip() if m else ""


def copy_in(src, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, os.path.basename(src))
    if not os.path.exists(dest) or os.path.getmtime(src) > os.path.getmtime(dest):
        shutil.copy2(src, dest)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--out", default=os.path.join(os.path.expanduser("~"), "SC-Coaching"))
    x = ap.parse_args()
    root = team_root(x.root)
    out = os.path.abspath(x.out)
    low = out.lower()
    if "onedrive" in low or "sharepoint" in low:
        sys.exit("--out must be a local folder, not OneDrive or SharePoint: this view is private to you")

    def sc_dir(ini):
        return os.path.join(out, "%s-%s" % (ini, TEAM[ini].split()[0].lower()))

    for ini in TEAM:
        for p in glob.glob(os.path.join(root, "Lessons", "coaching", ini, "*.md")):
            copy_in(p, os.path.join(sc_dir(ini), "coaching"))
    unmatched = []
    for p in glob.glob(os.path.join(root, "Lessons", "feedback", "*.md")) + glob.glob(os.path.join(root, "Lessons", "feedback", "*", "*.md")):
        sub = os.path.basename(os.path.dirname(p))
        ini = sub if sub in TEAM else who_wrote(p, read(p))
        if ini:
            copy_in(p, os.path.join(sc_dir(ini), "feedback"))
        else:
            unmatched.append(os.path.basename(p))

    rows = []
    for ini, full in TEAM.items():
        d = sc_dir(ini)
        os.makedirs(os.path.join(d, "coaching"), exist_ok=True)
        os.makedirs(os.path.join(d, "feedback"), exist_ok=True)
        coach = sorted(glob.glob(os.path.join(d, "coaching", "*.md")), reverse=True)
        fb = sorted(glob.glob(os.path.join(d, "feedback", "*.md")), reverse=True)
        lines = ["# %s: coaching and feedback" % full, "",
                 "Private to %s. Built %s by `sc-coach/scripts/coach_board.py`; re-run it to refresh." % (
                     "you" if ini == "rh" else full.split()[0] + " and Renzo", datetime.date.today().isoformat()), "",
                 "## Coaching (newest first)", ""]
        if coach:
            lines += ["| Date | Call | Top three habits | File |", "|---|---|---|---|"]
            for p in coach:
                t = read(p)
                name = os.path.basename(p)
                date = name[:10]
                call = first_line(t).replace("Coaching:", "").replace(full + " ·", "").strip()
                lines.append("| %s | %s | %s | [open](coaching/%s) |" % (
                    date, call.replace("|", "/"), " · ".join(habits(t)) or "-", name.replace(" ", "%20")))
        else:
            lines.append("No coaching files yet.")
        lines += ["", "## Feedback (newest first)", ""]
        if fb:
            lines += ["| Date | Summary | Skill | Severity | File |", "|---|---|---|---|---|"]
            for p in fb:
                t = read(p)
                name = os.path.basename(p)
                skill = field(t, "Skill + step") or field(t, "Skill")
                lines.append("| %s | %s | %s | %s | [open](feedback/%s) |" % (
                    name[:10], first_line(t).replace("|", "/"), skill.replace("|", "/"),
                    field(t, "Severity").split("(")[0].strip() or "-", name.replace(" ", "%20")))
        else:
            lines.append("No feedback files yet.")
        lines += ["", "## Your notes", "", "One-on-one notes go in [notes.md](notes.md): this README is rebuilt on each run,"
                  " notes.md is never touched.", ""]
        with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        notes = os.path.join(d, "notes.md")
        if not os.path.exists(notes):
            with open(notes, "w", encoding="utf-8") as fh:
                fh.write("# One-on-one notes: %s\n\n" % full)
        latest = habits(read(coach[0])) if coach else []
        rows.append("| [%s](%s/README.md) | %d | %s | %d |" % (
            full, os.path.basename(d), len(coach), " · ".join(latest) or "-", len(fb)))

    ov = ["# SC coaching overview", "", "Private: local folder on Renzo's PC, not synced. Built %s." %
          datetime.date.today().isoformat(), "", "| SC | Calls coached | Latest top habits | Feedback files |",
          "|---|---|---|---|"] + rows
    ov += ["", "Team-safe lessons (anonymised, for every SC): `<team root>/Lessons/explaining-it/EXPLAINING-IT-LESSONS.md`"]
    if unmatched:
        ov += ["", "Feedback files with no SC matched: " + ", ".join(unmatched)]
    with open(os.path.join(out, "OVERVIEW.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(ov) + "\n")
    print("wrote", os.path.join(out, "OVERVIEW.md"))
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
