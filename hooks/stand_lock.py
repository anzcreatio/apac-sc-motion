#!/usr/bin/env python3
"""Stand lock: one chat at a time writes to a Creatio stand (build rules §1b rule 2, 20 Nov 2026).

Why: chats could not see each other on a stand. On 20 Nov one chat reinstalled a UI kit build on clean82 eleven
minutes after another chat's release install and silently overwrote it. Process checks miss clio's MCP (one
long-lived process, no stand on its command line), the Mac and other SCs.

How it works (no one has to remember anything):
- A PreToolUse hook sees every clio write (MCP tools, `clio ... -e <stand>` in Bash/PowerShell, the kit's
  `install.ps1 -Stand <stand>`). Reads (get-, list-, find-, odata-read, pull-pkg, ...) are never checked.
- No lock, or a lock held by this chat, or an expired one: the write goes ahead and this chat holds a 30-minute
  lease on the stand, renewed by every write.
- Held by another chat: the write stops. Attended chat: Claude Code asks the SC ("clean82 is in use by ...: go
  ahead anyway?"); yes takes the lock over (PostToolUse). Unattended run (overnight build): refused, a hard stop.
- A long build holds the stand on purpose: `stand_lock.py hold --stand <env> --hours 8 --why "overnight build"`.
  `release` frees it; session end frees every lock the chat held.
- Locks are small JSON files in SharePoint `Stands/locks/<stand>.json`, so the Mac and other SCs see them too
  (OneDrive sync takes seconds to a minute: good enough for "who is on this stand", not a mutex).
- The stand key is the stand's host (`11014982-demo`), read from clio's settings (names and URLs only), so two
  clio names for the same stand share one lock.
- Fails open: any error, no SharePoint root, no config: the hook says nothing and the tool runs as before.

CLI:  status [--all] · hold --stand <env> [--hours 8] [--why ...] · release [--stand <env>] · take --stand <env>
Hook: --hook pre | post | end   (JSON on stdin from Claude Code)
"""
import argparse
import datetime as dt
import json
import os
import re
import socket
import sys
from urllib.parse import urlparse

LEASE_MIN = 30
MAX_HOLD_H = 16
READ_PREFIXES = ("get-", "list-", "find-", "validate-", "read", "show-", "describe", "search", "odata-read",
                 "execute-esq", "page-smoke", "ping", "healthcheck", "check-", "pull-", "docs", "guidance",
                 "help", "version", "info", "send-telemetry", "withdraw-telemetry")
CLIO_WRITE_IN_SHELL = re.compile(
    r"\bclio(?:\.exe)?\s+([a-z][\w-]*)\b[^\n|;&]*?(?:-e|--environment)[\s=]+[\"']?([\w.-]+)", re.I)
KIT_INSTALL = re.compile(r"install\.ps1\b[^\n|;&]*?-Stand\s+[\"']?([\w.-]+)", re.I)


# ---------- basics ----------
def now():
    return dt.datetime.now(dt.timezone.utc)


def iso(t):
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(s):
    try:
        return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except Exception:
        return None


def cfg():
    try:
        with open(os.path.join(os.path.expanduser("~"), ".apac-sc-motion.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def lock_dir(root=None):
    r = root or os.environ.get("STAND_LOCK_ROOT") or cfg().get("sharepoint_root")
    if not r or not os.path.isdir(r):
        return None
    d = os.path.join(r, "Stands", "locks")
    os.makedirs(d, exist_ok=True)
    return d


def clio_settings_files():
    base = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), ".local", "share")
    files = [os.path.join(base, "creatio", "clio", "appsettings.json")]
    pk = os.path.join(base, "Packages")
    if os.path.isdir(pk):
        for d in os.listdir(pk):
            if d.lower().startswith("claude"):
                files.append(os.path.join(pk, d, "LocalCache", "Local", "creatio", "clio", "appsettings.json"))
    files.append(os.path.join(os.path.expanduser("~"), ".clio", "appsettings.json"))
    return files


def stand_key(env):
    """clio environment name → stand host (11014982-demo); reads names and URLs only."""
    env = (env or "").strip()
    if not env:
        return ""
    if "://" in env:
        return (urlparse(env).hostname or env).split(".")[0].lower()
    for f in clio_settings_files():
        try:
            with open(f, encoding="utf-8-sig") as h:
                envs = (json.load(h) or {}).get("Environments") or {}
            for name, e in envs.items():
                if name.lower() == env.lower() and isinstance(e, dict) and e.get("Uri"):
                    return (urlparse(e["Uri"]).hostname or "").split(".")[0].lower() or env.lower()
        except Exception:
            continue
    return re.sub(r"[^\w.-]", "_", env.lower())


def lock_path(d, key):
    return os.path.join(d, key + ".json")


def read_lock(d, key):
    try:
        with open(lock_path(d, key), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def write_lock(d, key, data):
    tmp = lock_path(d, key) + ".tmp-%d" % os.getpid()
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, lock_path(d, key))


def live(lock):
    e = parse((lock or {}).get("expires", ""))
    return bool(e and e > now())


def me(session=None):
    c = cfg()
    return {
        "session": session or os.environ.get("CLAUDE_CODE_SESSION_ID") or "",
        "chat": os.environ.get("CLAUDE_CODE_HOST_SESSION_ID") or "",
        "sc": c.get("sc", ""),
        "machine": socket.gethostname(),
    }


def mine(lock, who):
    return bool(lock and who["session"] and lock.get("holder", {}).get("session") == who["session"])


def ago(ts):
    t = parse(ts or "")
    if not t:
        return "?"
    m = int((now() - t).total_seconds() // 60)
    return "%d min ago" % m if m < 120 else "%.1f h ago" % (m / 60)


def describe(lock):
    h = lock.get("holder", {})
    who = "SC %s on %s" % (h.get("sc") or "?", h.get("machine") or "?")
    chat = (" · chat %s" % h["chat"]) if h.get("chat") else ""
    why = (" · %s" % lock["why"]) if lock.get("why") else ""
    return "%s%s%s · last: %s %s · free at %s" % (
        who, chat, why, lock.get("last_action", "?"), ago(lock.get("renewed")),
        parse(lock["expires"]).astimezone().strftime("%H:%M") if parse(lock.get("expires", "")) else "?")


def take(d, key, env, who, action, kind="lease", hours=None, why=""):
    old = read_lock(d, key) or {}
    t = now()
    keep_hold = mine(old, who) and old.get("kind") == "hold" and live(old)
    if kind == "hold":
        exp = t + dt.timedelta(hours=min(float(hours or 8), MAX_HOLD_H))
    elif keep_hold:
        exp = max(parse(old["expires"]), t + dt.timedelta(minutes=LEASE_MIN))
    else:
        exp = t + dt.timedelta(minutes=LEASE_MIN)
    envs = sorted(set((old.get("envs") if mine(old, who) else []) + [env]))
    data = {
        "stand": key, "envs": envs, "holder": who,
        "kind": "hold" if (kind == "hold" or keep_hold) else "lease",
        "why": why or (old.get("why", "") if mine(old, who) else ""),
        "since": old.get("since") if mine(old, who) and live(old) else iso(t),
        "renewed": iso(t), "expires": iso(exp), "last_action": action,
    }
    write_lock(d, key, data)
    return data


# ---------- what is this tool call? ----------
def target(tool, inp):
    """→ (env, action) for a stand write, else None."""
    inp = inp or {}
    if tool.startswith("mcp__") and "clio" in tool.lower():
        cmd = inp.get("command") if tool.endswith("clio-run") or tool.endswith("clio-run-destructive") else tool.split("__")[-1]
        args = inp.get("args") if isinstance(inp.get("args"), dict) else inp
        if isinstance(args, dict) and isinstance(args.get("args"), dict) and not args.get("environment-name"):
            cmd = cmd or args.get("command")
            args = args["args"]
        env = (args or {}).get("environment-name") or (args or {}).get("uri") or ""
        cmd = (cmd or "").lower()
        if not env or not cmd or cmd.startswith(READ_PREFIXES):
            return None
        return env, cmd
    if tool in ("Bash", "PowerShell"):
        text = str(inp.get("command", ""))
        if "stand_lock.py" in text:
            return None
        m = KIT_INSTALL.search(text)
        if m and "-DryRun" not in text:
            return m.group(1), "kit install.ps1"
        for m in CLIO_WRITE_IN_SHELL.finditer(text):
            verb = m.group(1).lower()
            if not verb.startswith(READ_PREFIXES):
                return m.group(2), "clio " + verb
    return None


# ---------- hook modes ----------
def out(obj):
    sys.stdout.write(json.dumps(obj))


def hook(mode):
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    try:
        d = lock_dir()
        if not d:
            return 0
        who = me(data.get("session_id"))
        if mode == "end":
            for f in os.listdir(d):
                if f.endswith(".json"):
                    k = f[:-5]
                    if mine(read_lock(d, k), who):
                        os.remove(lock_path(d, k))
            return 0
        t = target(data.get("tool_name", ""), data.get("tool_input"))
        if not t:
            return 0
        env, action = t
        key = stand_key(env)
        lock = read_lock(d, key)
        if mode == "post":
            take(d, key, env, who, action)
            return 0
        if lock and live(lock) and not mine(lock, who):
            reason = ("Stand lock: %s is in use by another chat (%s). Writing now can clash with its build "
                      "(build rules §1b rule 2). Check with that chat or the SC first." % (key, describe(lock)))
            attended = os.environ.get("CLAUDE_CODE_SESSION_ATTENDED", "1") != "0"
            out({"hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask" if attended else "deny",
                "permissionDecisionReason": reason + (" Approve to take the stand over." if attended else
                                                      " Unattended run: stop and report this as a hard stop."),
            }})
            return 0
        take(d, key, env, who, action)
    except Exception:
        return 0
    return 0


# ---------- CLI ----------
def cli(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Stand lock: who is writing to which Creatio stand.")
    ap.add_argument("--hook", choices=["pre", "post", "end"])
    ap.add_argument("--root", help="team SharePoint root (default from ~/.apac-sc-motion.json)")
    sp = ap.add_subparsers(dest="cmd")
    p = sp.add_parser("status"); p.add_argument("--all", action="store_true", help="include expired locks")
    p = sp.add_parser("hold"); p.add_argument("--stand", required=True); p.add_argument("--hours", type=float, default=8)
    p.add_argument("--why", default="")
    p = sp.add_parser("release"); p.add_argument("--stand")
    p = sp.add_parser("take"); p.add_argument("--stand", required=True); p.add_argument("--why", default="")
    a = ap.parse_args(argv)
    if a.hook:
        return hook(a.hook)
    d = lock_dir(a.root)
    if not d:
        print("No team SharePoint root (run sc-setup): stand locks are off.")
        return 1
    who = me()
    if a.cmd in (None, "status"):
        rows = []
        for f in sorted(os.listdir(d)):
            if not f.endswith(".json"):
                continue
            L = read_lock(d, f[:-5])
            if L and (live(L) or getattr(a, "all", False)):
                rows.append((L, live(L)))
        if not rows:
            print("No stand in use.")
            return 0
        print("| Stand | Held by | Since | Free at | Status |\n|---|---|---|---|---|")
        for L, ok in rows:
            h = L.get("holder", {})
            print("| %s (%s) | SC %s on %s%s%s | %s | %s | %s |" % (
                L["stand"], ", ".join(L.get("envs", [])), h.get("sc", "?"), h.get("machine", "?"),
                " · this chat" if mine(L, who) else (" · chat " + h["chat"] if h.get("chat") else ""),
                (" · " + L["why"]) if L.get("why") else "", ago(L.get("since")),
                parse(L["expires"]).astimezone().strftime("%d %b %H:%M"), "🟢 in use" if ok else "expired"))
        return 0
    if not who["session"]:
        print("Run this from inside a Claude chat (it needs CLAUDE_CODE_SESSION_ID to know who holds the stand).")
        return 1
    if a.cmd in ("hold", "take"):
        key = stand_key(a.stand)
        L = read_lock(d, key)
        if a.cmd == "hold" and L and live(L) and not mine(L, who):
            print("Refused: %s is in use by another chat (%s). Use `take` only with the SC's OK." % (key, describe(L)))
            return 2
        L = take(d, key, a.stand, who, "hold" if a.cmd == "hold" else "take over", kind="hold",
                 hours=getattr(a, "hours", 8), why=a.why)
        print("%s held by this chat until %s%s." % (key, parse(L["expires"]).astimezone().strftime("%d %b %H:%M"),
                                                   (" (" + L["why"] + ")") if L["why"] else ""))
        return 0
    if a.cmd == "release":
        keys = [stand_key(a.stand)] if a.stand else [f[:-5] for f in os.listdir(d) if f.endswith(".json")]
        freed = []
        for k in keys:
            if mine(read_lock(d, k), who):
                os.remove(lock_path(d, k)); freed.append(k)
        print("Released: " + (", ".join(freed) if freed else "nothing (this chat held no stand)"))
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(cli(sys.argv[1:]))
