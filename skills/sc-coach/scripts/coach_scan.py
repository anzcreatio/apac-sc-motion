"""First pass for sc-coach: find the moments a speaker explained something or answered a question, and flag them.

It does the mechanical part only (who spoke when, hedges, jargon, vendor words, length, the customer question that came
before). Claude does the judgement: is it clear, is the claim approved, does it open doubts, and the rewrites.

  python coach_scan.py --transcript "<file>" --speaker "Renzo Huruiti" [--speaker "Willy Noviandy"]
                       [--min-words 40] [--json out.json]

Reads both transcript shapes we get:
  Teams copy:   "Renzo Huruiti  0:03" on one line, the words on the next lines
  Timestamped:  "[12:34] Renzo Huruiti: words"   (also "[12:34] Huruiti, Renzo: words")
Consecutive turns by the same speaker are merged into one moment. A Teams copy has one time per turn, so times
inside a long turn are estimates: write them as ~mm:ss.
"""
import argparse
import json
import re
import sys

HEDGES = [
    "i think", "i believe", "i guess", "i suppose", "should be able to", "should be possible", "in theory",
    "theoretically", "probably", "maybe", "might be able", "hopefully", "i'm not sure", "not 100%", "not a hundred",
    "if i'm not mistaken", "i'd have to check", "kind of", "sort of", "more or less", "as far as i know",
    "to be honest", "honestly", "i would say", "it depends", "potentially", "i'm pretty sure", "i hope",
    "don't quote me", "roughly", "something like that", "or something",
]
FILLERS = ["um", "uh", "you know", "like,", "basically", "actually", "so yeah", "yeah, so"]
JARGON = [
    "low-code", "low code", "no-code", "no code", "freedom ui", "business process designer", "bpmn", "dcm",
    "case management", "object model", "entity", "schema", "lookup", "odata", "api", "rest", "sdk", "package",
    "compile", "orchestration", "orchestrate", "composable", "agentic", "llm", "rag", "embedding", "prompt",
    "copilot", "ai skill", "mcp", "tenant", "multi-tenant", "on-prem", "saas", "paas", "metadata", "workflow engine",
    "out of the box", "ootb", "configuration", "configure", "customisation", "customization", "integration layer",
    "middleware", "sso", "rbac", "role-based", "sandbox", "deployment", "instance", "stand", "clio", "studio",
    "omnichannel", "360", "single pane", "data model", "kpi",
]
VENDOR = [
    "seamless", "leverage", "unlock", "empower", "robust", "streamline", "cutting-edge", "cutting edge", "transform",
    "holistic", "synergy", "elevate", "harness", "game-changer", "game changer", "world-class", "best-in-class",
    "revolution", "supercharge", "ecosystem", "paradigm", "single source of truth", "at scale", "next-generation",
    "next generation",
]
ABSOLUTES = ["never", "always", "100%", "a hundred percent", "guarantee", "everything", "any system", "anything",
             "no limit", "unlimited", "fully", "completely", "instantly", "zero"]

TEAMS = re.compile(r"^(?P<name>[^\[\]\d][^\t]{1,80}?)\s{2,}(?P<t>\d{1,2}:\d{2}(?::\d{2})?)\s*$")
STAMP = re.compile(r"^\[(?P<t>\d{1,2}:\d{2}(?::\d{2})?)\]\s*(?P<name>[^:]{1,80}):\s*(?P<text>.*)$")


def norm(name):
    name = re.sub(r"\(.*?\)", "", name).strip()
    if "," in name:  # "Huruiti, Renzo" or "Uy, Ivy B."
        last, first = [p.strip() for p in name.split(",", 1)]
        name = first + " " + last
    return re.sub(r"\s+", " ", name).lower()


def parse(path):
    turns, cur = [], None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            m = STAMP.match(line)
            if m:
                cur = {"t": m["t"], "speaker": m["name"].strip(), "text": m["text"].strip(),
                       "lines": [[m["t"], m["text"].strip()]]}
                turns.append(cur)
                continue
            m = TEAMS.match(line)
            if m:
                cur = {"t": m["t"], "speaker": m["name"].strip(), "text": "", "lines": [[m["t"], ""]]}
                turns.append(cur)
                continue
            if cur is not None and line.strip() and not line.startswith(("#", ">", "---")):
                cur["text"] = (cur["text"] + " " + line.strip()).strip()
                cur["lines"][-1][1] = (cur["lines"][-1][1] + " " + line.strip()).strip()
    return turns


def merge(turns):
    out = []
    for t in turns:
        if out and norm(out[-1]["speaker"]) == norm(t["speaker"]):
            out[-1]["text"] += " " + t["text"]
            out[-1]["lines"] += t["lines"]
            out[-1]["end"] = t["t"]
        else:
            out.append(dict(t, end=t["t"]))
    return out


QSTART = re.compile(r"(^|[.!?,]\s+|\b(?:so|and|but|okay|ok|yeah|right)[, ]+)(how|what|can|could|does|do|is|are|will|would|"
                    r"where|when|why|who|which|have you|has it|is there|are there)\b", re.I)


def is_question(text):
    return "?" in text or bool(QSTART.search(text[-400:]))


def hits(text, words):
    low = " " + text.lower() + " "
    found = []
    for w in words:
        pat = r"(?<![a-z])" + re.escape(w) + r"(?![a-z])"
        n = len(re.findall(pat, low))
        if n:
            found.append("%s x%d" % (w, n) if n > 1 else w)
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--speaker", action="append", required=True, help="the SC(s) to coach; repeat for each")
    ap.add_argument("--min-words", type=int, default=40, help="shorter turns count only if they answer a question")
    ap.add_argument("--json")
    x = ap.parse_args()

    wanted = {norm(s) for s in x.speaker}
    turns = merge(parse(x.transcript))
    if not turns:
        sys.exit("No speaker turns found: is this a Teams transcript?")
    moments = []
    for i, t in enumerate(turns):
        if norm(t["speaker"]) not in wanted:
            continue
        words = len(t["text"].split())
        # the customer's question may sit 1-2 turns back (the AE says "good question") and speech-to-text often
        # drops the "?", so also accept question-shaped openings
        # crosstalk ("Awesome." "Yeah." "If.") can sit between the question and the answer: look back 6 turns,
        # stopping at an earlier real answer by the SC
        prev = None
        for j in range(i - 1, max(-1, i - 7), -1):
            if norm(turns[j]["speaker"]) in wanted:
                if len(turns[j]["text"].split()) >= 12:
                    break
                continue
            if is_question(turns[j]["text"]):
                prev = turns[j]
                break
        asked = prev is not None
        if words < x.min_words and not (asked and words >= 5):
            continue
        m = {
            "n": len(moments) + 1, "start": t["t"], "end": t["end"], "speaker": t["speaker"], "words": words,
            "answers_question": asked,
            "question": (prev["speaker"] + ": " + prev["text"][-300:]) if asked else None,
            "hedges": hits(t["text"], HEDGES), "fillers": hits(t["text"], FILLERS),
            "jargon": hits(t["text"], JARGON), "vendor_words": hits(t["text"], VENDOR),
            "absolutes": hits(t["text"], ABSOLUTES),
            "too_long": words > 180, "text": t["text"], "lines": t["lines"],
        }
        m["flags"] = sum(bool(m[k]) for k in ("hedges", "jargon", "vendor_words", "absolutes", "too_long"))
        moments.append(m)

    for m in moments:
        tag = " Q" if m["answers_question"] else ""
        print("#%d %s-%s %s, %d words%s | hedges: %s | jargon: %s | vendor: %s | absolutes: %s%s" % (
            m["n"], m["start"], m["end"], m["speaker"], m["words"], tag, ", ".join(m["hedges"]) or "-",
            ", ".join(m["jargon"]) or "-", ", ".join(m["vendor_words"]) or "-", ", ".join(m["absolutes"]) or "-",
            " | TOO LONG" if m["too_long"] else ""))
    speakers = sorted({t["speaker"] for t in turns})
    print("\n%d moments for %s. Speakers seen: %s" % (len(moments), ", ".join(x.speaker), "; ".join(speakers)))
    if x.json:
        with open(x.json, "w", encoding="utf-8") as fh:
            json.dump({"transcript": x.transcript, "speakers": x.speaker, "moments": moments}, fh,
                      ensure_ascii=False, indent=1)
        print("wrote", x.json)


if __name__ == "__main__":
    main()
