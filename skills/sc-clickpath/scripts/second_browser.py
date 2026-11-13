"""Screenshots that need two users at once (e.g. the submitter in one browser, the approver in another).

The first user stays in the usual browser (the browser pane or your own Chrome). The second user gets a separate
Chrome with its own profile and a debugging port, so this script can screenshot it without touching the first.
Proven 13 Nov 2026 (Renzo).

    python second_browser.py launch [--port 9223] [--profile <dir>] [--url <stand url>]
        Starts Chrome: chrome.exe --remote-debugging-port=9223 --user-data-dir=<profile> --no-first-run <url>
        The SC signs in once per stand in that window (Claude never types the password). The profile keeps the
        sign-in, so later runs only need launch again.
    python second_browser.py shot <out.jpg> [--url <page>] [--match <text in url>] [--width 1440 --height 900]
                                  [--wait 3]
        Connects with Playwright (connect_over_cdp http://127.0.0.1:<port>), picks the tab whose URL contains
        --match (else the first tab), optionally opens --url in it, waits, and saves a screenshot of the viewport.
    python second_browser.py close [--port 9223]
        Closes that Chrome with the CDP command Browser.close.

Default profile: <system temp>/apac-sc-chrome-user2 (never a deal folder: it holds a signed-in session).
Needs: pip install playwright (no browser download needed: it attaches to your Chrome).
Then add the frame to cards.json like any other shot and look at it for other customers' names.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
]


def chrome():
    for p in CHROME_PATHS:
        if os.path.isfile(p):
            return p
    sys.exit("Chrome not found. Install Google Chrome or add its path to CHROME_PATHS.")


def endpoint(port):
    return "http://127.0.0.1:%d" % port


def alive(port):
    try:
        with urllib.request.urlopen(endpoint(port) + "/json/version", timeout=2) as r:
            return json.load(r)
    except Exception:
        return None


def launch(a):
    if alive(a.port):
        print("Second browser already running on port %d." % a.port)
        return
    profile = a.profile or os.path.join(tempfile.gettempdir(), "apac-sc-chrome-user2")
    os.makedirs(profile, exist_ok=True)
    args = [chrome(), "--remote-debugging-port=%d" % a.port, "--user-data-dir=%s" % profile, "--no-first-run",
            "--no-default-browser-check", "--window-size=%d,%d" % (a.width, a.height)]
    if a.url:
        args.append(a.url)
    subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):
        if alive(a.port):
            print("Second browser up on port %d (profile %s). Sign in as the second user in that window." % (a.port, profile))
            return
        time.sleep(0.5)
    sys.exit("Chrome started but port %d did not answer. Close other Chrome windows using that profile and retry." % a.port)


def shot(a):
    if not alive(a.port):
        sys.exit("No second browser on port %d. Run: python second_browser.py launch" % a.port)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint(a.port))
        pages = [pg for ctx in browser.contexts for pg in ctx.pages]
        if not pages:
            pages = [browser.contexts[0].new_page()]
        page = next((pg for pg in pages if a.match and a.match in pg.url), pages[0])
        page.set_viewport_size({"width": a.width, "height": a.height})
        if a.url:
            page.goto(a.url, wait_until="domcontentloaded")
        page.wait_for_timeout(int(a.wait * 1000))
        if "/Login" in page.url or "login" in page.url.lower().rsplit("/", 1)[-1]:
            sys.exit("The second browser is on a sign-in page: ask the SC to sign in there first. No screenshot taken.")
        os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
        page.screenshot(path=a.out, type="jpeg", quality=85)
        print("Saved %s from %s" % (a.out, page.url))
        browser.close()  # disconnects Playwright only; Chrome stays open


def close(a):
    info = alive(a.port)
    if not info:
        print("No second browser on port %d." % a.port)
        return
    import asyncio
    try:
        import websockets  # noqa: F401
    except ImportError:
        websockets = None
    ws = info.get("webSocketDebuggerUrl")
    if websockets and ws:
        async def run():
            async with websockets.connect(ws) as c:
                await c.send(json.dumps({"id": 1, "method": "Browser.close"}))
        asyncio.run(run())
    else:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.connect_over_cdp(endpoint(a.port))
            b.new_browser_cdp_session().send("Browser.close")
    print("Second browser closed.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("launch", "shot", "close"):
        s = sub.add_parser(name)
        s.add_argument("--port", type=int, default=9223)
        s.add_argument("--width", type=int, default=1440)
        s.add_argument("--height", type=int, default=900)
        if name == "launch":
            s.add_argument("--profile")
            s.add_argument("--url")
        if name == "shot":
            s.add_argument("out")
            s.add_argument("--url")
            s.add_argument("--match")
            s.add_argument("--wait", type=float, default=3)
    a = ap.parse_args()
    {"launch": launch, "shot": shot, "close": close}[a.cmd](a)


if __name__ == "__main__":
    main()
