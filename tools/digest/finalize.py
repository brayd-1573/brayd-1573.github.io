#!/usr/bin/env python3
"""Validate a rundown data file.

  python3 tools/digest/finalize.py --last              # print last issue's picks/question (for follow-ups)
  python3 tools/digest/finalize.py _data/digests/2026-11-22.json

The data file is the single source of truth: the Astro site reads _data/digests/*.json
directly (src/content.config.ts) and renders /rundown/<YYYY-MM-DD>/ from it. Exits non-zero
with a list of problems if the JSON doesn't match the schema in tools/digest/INSTRUCTIONS.md.
These checks mirror the site's build-time schema, so a file that passes here also builds.
"""

import glob
import json
import os
import re
import sys
from datetime import datetime, timezone

DATE_RE = r"\d{4}-\d{2}-\d{2}"

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(ROOT, "_data", "digests")

LIMITS = {  # key: (min, max)
    "stats": (2, 4), "prs": (3, 3), "contribute": (2, 3), "news": (3, 6),
    "papers": (2, 5), "videos": (0, 5), "releases": (0, 6), "followups": (0, 5),
}
ITEM_KEYS = {
    "stats": ["value", "label"],
    "prs": ["number", "title", "url", "area", "summary", "why_it_matters"],
    "contribute": ["number", "title", "url", "difficulty", "fit", "why_you", "first_steps", "status"],
    "news": ["title", "url", "source", "tag", "summary"],
    "papers": ["title", "url", "authors", "claim", "why_it_matters", "signal", "reproduce"],
    "videos": ["title", "url", "video_id", "channel", "kind", "why"],
    "releases": ["repo", "tag", "url", "summary"],
    "followups": ["title", "url", "status"],
}
INT_FIELDS = {  # non-string item fields (everything else in ITEM_KEYS must be a string)
    ("prs", "number"): int, ("contribute", "number"): int, ("contribute", "fit"): int,
    ("contribute", "first_steps"): list, ("stats", "value"): (str, int, float),
}


def _is(v, want):
    """isinstance, but booleans never count as numbers."""
    return isinstance(v, want) and not (isinstance(v, bool) and want is not bool)


def _name(want):
    return " or ".join(t.__name__ for t in want) if isinstance(want, tuple) else want.__name__


ENUMS = {
    ("contribute", "difficulty"): {"starter", "moderate", "stretch"},
    ("news", "tag"): {"hardware", "software", "startups", "market", "jobs", "open-source", "policy"},
    ("papers", "reproduce"): {"yes", "maybe", "no"},
    ("videos", "kind"): {"talk", "lecture", "tutorial", "breakdown", "interview", "demo"},
}


def existing():
    return sorted(glob.glob(os.path.join(DATA_DIR, "*.json")))


def last():
    files = existing()
    if not files:
        print(json.dumps({"previous_issue": None, "next_issue_number": 1}))
        return
    d = json.load(open(files[-1]))
    print(json.dumps({
        "previous_issue": d.get("issue"), "previous_date": d.get("date"), "next_issue_number": d.get("issue", 0) + 1,
        "days_since_previous": (datetime.now(timezone.utc).date() - datetime.strptime(d["date"], "%Y-%m-%d").date()).days,
        "previous_contribute_numbers": [c.get("number") for c in d.get("contribute", [])],
        "previous_question": d.get("question"),
        "recent_urls": sorted({i.get("url") for k in ("prs", "news", "papers", "videos")
                               for f in files[-3:] for i in json.load(open(f)).get(k, [])}),
    }, indent=1))


def validate(path):
    errs = []
    try:
        d = json.load(open(path))
    except Exception as e:  # noqa: BLE001
        return [f"not valid JSON: {e}"], None
    key = os.path.splitext(os.path.basename(path))[0]
    if not re.fullmatch(DATE_RE, key):
        errs.append("file name must be YYYY-MM-DD.json")
    if d.get("date") != key:
        errs.append(f"date field must equal file name ({key})")
    for k, t in [("issue", int), ("headline", str), ("tldr", str), ("window", dict), ("question", dict)]:
        if not isinstance(d.get(k), t):
            errs.append(f"missing/invalid top-level '{k}' ({t.__name__})")
    w = d.get("window") if isinstance(d.get("window"), dict) else {}
    if not all(re.fullmatch(DATE_RE, str(w.get(x, ""))) for x in ("from", "to")):
        errs.append("window needs 'from' and 'to' as YYYY-MM-DD")
    if isinstance(d.get("headline"), str) and len(d["headline"]) > 110:
        errs.append("headline > 110 chars")
    if isinstance(d.get("tldr"), str) and len(d["tldr"]) > 700:
        errs.append("tldr > 700 chars")
    for k, (lo, hi) in LIMITS.items():
        items = d.get(k, [])
        if not isinstance(items, list) or not lo <= len(items) <= hi:
            errs.append(f"'{k}' must be a list of {lo}-{hi} items (got {len(items) if isinstance(items, list) else type(items).__name__})")
            continue
        for i, it in enumerate(items):
            for f in ITEM_KEYS[k]:
                if it.get(f) in (None, "", []):
                    errs.append(f"{k}[{i}] missing '{f}'")
            if "url" in it and not str(it["url"]).startswith("https://"):
                errs.append(f"{k}[{i}].url must be https://")
            for f in ITEM_KEYS[k]:
                want = INT_FIELDS.get((k, f), str)
                if it.get(f) not in (None, "", []) and not _is(it[f], want):
                    errs.append(f"{k}[{i}].{f} must be {_name(want)}")
            for (sec, field), allowed in ENUMS.items():
                if sec == k and it.get(field) not in allowed:
                    errs.append(f"{k}[{i}].{field} must be one of {sorted(allowed)}")
        if k == "contribute":
            for i, it in enumerate(items):
                if not all(isinstance(x, str) for x in it.get("first_steps") or []):
                    errs.append(f"contribute[{i}].first_steps must be a list of strings")
                if not (isinstance(it.get("fit"), int) and 1 <= it["fit"] <= 5):
                    errs.append(f"contribute[{i}].fit must be int 1-5")
        if k == "videos":
            for i, it in enumerate(items):
                if not re.fullmatch(r"[A-Za-z0-9_-]{11}", str(it.get("video_id", ""))):
                    errs.append(f"videos[{i}].video_id must be the 11-char YouTube id")
    q = d.get("question") or {}
    if not isinstance(q.get("prompt"), str) or not isinstance(q.get("answer"), str) or not q["prompt"] or not q["answer"]:
        errs.append("question needs 'prompt' and 'answer' (answer is revealed next week)")
    la = d.get("last_answer")
    if la is not None and not (isinstance(la, dict) and isinstance(la.get("prompt"), str) and isinstance(la.get("answer"), str)
                               and la["prompt"] and la["answer"]):
        errs.append("last_answer must be null or have prompt+answer")
    if q.get("hint") is not None and not isinstance(q.get("hint"), str):
        errs.append("question.hint must be a string or omitted")
    b = d.get("building")
    if b is not None:
        if not isinstance(b, dict) or not isinstance(b.get("repos", []), list):
            errs.append("building must be null or an object with a 'repos' list")
        else:
            if b.get("note") is not None and not isinstance(b.get("note"), str):
                errs.append("building.note must be a string or null")
            for i, r in enumerate(b.get("repos", [])):
                if not (isinstance(r.get("name"), str) and str(r.get("url", "")).startswith("https://")
                        and _is(r.get("commits"), int)):
                    errs.append(f"building.repos[{i}] needs name, https url, integer commits")
                if not all(isinstance(h, str) for h in r.get("highlights", [])):
                    errs.append(f"building.repos[{i}].highlights must be strings")
            for i, u in enumerate(b.get("upstream", []) or []):
                if not (u.get("title") and str(u.get("url", "")).startswith("https://") and u.get("state")):
                    errs.append(f"building.upstream[{i}] needs title, https url, state")
    j = d.get("jobs")
    if j is not None:
        if not isinstance(j, dict) or not isinstance(j.get("summary"), str) or not j["summary"]:
            errs.append("jobs must be null or have a summary")
        else:
            for i, s in enumerate(j.get("skills", []) or []):
                if not isinstance(s.get("name"), str) or not s["name"]:
                    errs.append(f"jobs.skills[{i}] needs a name")
                if s.get("note") is not None and not isinstance(s.get("note"), str):
                    errs.append(f"jobs.skills[{i}].note must be a string")
            for i, p in enumerate(j.get("postings", []) or []):
                if not (p.get("company") and p.get("role") and str(p.get("url", "")).startswith("https://")):
                    errs.append(f"jobs.postings[{i}] needs company, role, https url")
    return errs, d


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--last":
        last()
        return
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    errs, d = validate(path)
    if errs:
        print("INVALID:\n- " + "\n- ".join(errs))
        sys.exit(1)
    print(f"OK: {path} valid")


if __name__ == "__main__":
    main()
