"""SessionStart hook for apac-sc-motion: tells the SC when an update is waiting and, once after an update, what's new.

- Update available: the published version (synced SharePoint folder, `Plugin/apac-sc-motion`) is newer than the
  installed one -> one line with the update command and the titles of what they're missing.
- Chat standards: standards/CHAT-FORMAT-*, CHAT-TRACKING-* and TOOL-ROUTING-* (newest) go into every session's context, also
  after compaction, so plain chats follow them too (18 Nov 2026).
- What's new: the installed version is newer than `seen_version` in ~/.apac-sc-motion.json -> the changelog entries
  since then, shown once; then `seen_version` is saved.

Reads only local files (SharePoint is synced by OneDrive). Never fails the session: any error -> silent exit 0.
Test: python whats_new.py --root <plugin dir> --config <json> --dry-run
"""
import json
import os
import re
import sys

UPDATE_CMD = "claude plugin update apac-sc-motion@apac-sc"
HEADING = re.compile(r"^## (\d+(?:\.\d+)+)\b(.*)$")
MAX_LINES = 40  # keep the session start short


def vkey(v):
    return tuple(int(x) for x in v.split("."))


def read_json(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def changelog(path):
    """[(version, title, [body lines])], newest first, as written."""
    entries, cur = [], None
    with open(path, encoding="utf-8-sig") as f:
        for line in f.read().splitlines():
            m = HEADING.match(line)
            if m:
                title = re.sub(r"^\s*\([^)]*\)\s*:?\s*", "", m.group(2)).strip()
                cur = (m.group(1), title, [])
                entries.append(cur)
            elif line.startswith("## "):
                cur = None  # e.g. "## Library update": not a release
            elif cur is not None and line.strip():
                cur[2].append(line)
    return entries


def between(entries, low, high):
    """Entries with low < version <= high (low may be None = only `high`)."""
    out = []
    for v, title, body in entries:
        k = vkey(v)
        if k <= vkey(high) and ((low is None and k == vkey(high)) or (low is not None and k > vkey(low))):
            out.append((v, title, body))
    return out


STANDARDS = ("CHAT-FORMAT", "CHAT-TRACKING", "TOOL-ROUTING")  # loaded into every chat (newest version of each in standards/)


def standards(root):
    """The chat standards as session context, so every chat (not only skill runs) follows them."""
    d = os.path.join(root, "standards")
    parts = []
    for stem in STANDARDS:
        try:
            files = sorted((f for f in os.listdir(d) if re.match(re.escape(stem) + r"-v[\d.]+\.md$", f)),
                           key=lambda f: vkey(re.search(r"v([\d.]+)\.md$", f).group(1).rstrip(".")))
            if files:
                with open(os.path.join(d, files[-1]), encoding="utf-8-sig") as f:
                    parts.append(f.read().strip())
        except (OSError, ValueError, AttributeError):
            pass
    if not parts:
        return ""
    return ("apac-sc-motion chat standards (follow in every reply and every customer chat this session; "
            "plugin dir: " + os.path.abspath(root) + "):\n\n" + "\n\n---\n\n".join(parts))


def main(argv):
    args = dict(zip(argv[::2], argv[1::2])) if len(argv) % 2 == 0 else {}
    dry = "--dry-run" in sys.argv
    root = args.get("--root") or os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cfg_path = args.get("--config") or os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json")

    installed = read_json(os.path.join(root, ".claude-plugin", "plugin.json"))["version"]
    cfg = read_json(cfg_path) if os.path.exists(cfg_path) else {}

    user, context = [], []

    if not cfg.get("sharepoint_root"):
        user.append("apac-sc-motion: not set up on this computer yet. Ask Claude to run `sc-setup`.")
        context.append("The apac-sc-motion plugin is not set up (no ~/.apac-sc-motion.json). Offer to run the "
                       "sc-setup skill before any other apac-sc-motion skill.")
    else:
        pub_dir = os.path.join(cfg["sharepoint_root"], "Plugin", "apac-sc-motion")
        pub_json = os.path.join(pub_dir, ".claude-plugin", "plugin.json")
        if os.path.exists(pub_json):
            published = read_json(pub_json)["version"]
            if vkey(published) > vkey(installed):
                missing = []
                try:
                    missing = between(changelog(os.path.join(pub_dir, "CHANGELOG.md")), installed, published)
                except OSError:
                    pass
                titles = "; ".join(t for _, t, _ in missing[:5] if t)
                user.append(f"apac-sc-motion {published} is available (you have {installed}). "
                            f"Run `{UPDATE_CMD}`, then start a new session."
                            + (f" New: {titles}." if titles else ""))
                context.append(f"The SC's apac-sc-motion plugin is out of date ({installed} installed, {published} "
                               f"published). Mention it once at the top of your first reply and give the command "
                               f"`{UPDATE_CMD}` (they run it in a terminal, then start a new session).")

        seen = cfg.get("seen_version")
        if seen is None or vkey(installed) > vkey(seen):
            new = between(changelog(os.path.join(root, "CHANGELOG.md")), seen, installed)
            if new:
                lines = []
                for v, title, body in new:
                    lines.append(f"{v}: {title}" if title else v)
                    lines.extend(body)
                if len(lines) > MAX_LINES:
                    lines = lines[:MAX_LINES] + ["(more in the plugin's CHANGELOG.md)"]
                actions = [l for l in lines if "Each SC" in l]
                head = f"apac-sc-motion updated to {installed}" + (f" (from {seen})" if seen else "")
                user.append(head + ". What's new: " + "; ".join(f"{v} {t}" for v, t, _ in new[:6])
                            + (". Action for you inside: ask Claude what to do." if actions else "."))
                context.append(head + ". Changelog since the SC last saw it:\n" + "\n".join(lines) +
                               "\n\nAt the top of your first reply, tell the SC in 2-4 plain bullets what changed "
                               "for them, and list any 'Each SC:' action as a numbered question asking if they want "
                               "to do it now. Do this once; don't repeat it later in the session.")
            if not dry:
                cfg["seen_version"] = installed
                with open(cfg_path, "w", encoding="utf-8") as f:
                    json.dump(cfg, f, indent=2)

    rules = standards(root)
    if rules:
        context.insert(0, rules)

    if user or context:
        print(json.dumps({
            "systemMessage": "\n".join(user),
            "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "\n\n".join(context)},
        }))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main([a for a in sys.argv[1:] if a != "--dry-run"]))
    except Exception:
        sys.exit(0)
