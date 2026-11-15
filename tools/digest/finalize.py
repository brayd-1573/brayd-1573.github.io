#!/usr/bin/env python3
"""Validate a rundown data file and create its page stub.

  python3 tools/digest/finalize.py --last              # print last issue's picks/question (for follow-ups)
  python3 tools/digest/finalize.py _data/digests/2026-11-22.json

The data file is the single source of truth; the page in _digests/ is a 6-line stub
that points the `rundown` layout at it. Exits non-zero with a list of problems if the
JSON doesn't match the schema in tools/digest/INSTRUCTIONS.md.
"""

import glob
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(ROOT, "_data", "digests")
PAGE_DIR = os.path.join(ROOT, "_digests")

LIMITS = {  # key: (min, max)
    "stats": (2, 4), "prs": (3, 5), "contribute": (2, 3), "news": (3, 8),
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
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", key):
        errs.append("file name must be YYYY-MM-DD.json")
    if d.get("date") != key:
        errs.append(f"date field must equal file name ({key})")
    for k, t in [("issue", int), ("headline", str), ("tldr", str), ("window", dict), ("question", dict)]:
        if not isinstance(d.get(k), t):
            errs.append(f"missing/invalid top-level '{k}' ({t.__name__})")
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
            for (sec, field), allowed in ENUMS.items():
                if sec == k and it.get(field) not in allowed:
                    errs.append(f"{k}[{i}].{field} must be one of {sorted(allowed)}")
        if k == "contribute":
            for i, it in enumerate(items):
                if not (isinstance(it.get("fit"), int) and 1 <= it["fit"] <= 5):
                    errs.append(f"contribute[{i}].fit must be int 1-5")
        if k == "videos":
            for i, it in enumerate(items):
                if not re.fullmatch(r"[A-Za-z0-9_-]{11}", str(it.get("video_id", ""))):
                    errs.append(f"videos[{i}].video_id must be the 11-char YouTube id")
    q = d.get("question") or {}
    if not q.get("prompt") or not q.get("answer"):
        errs.append("question needs 'prompt' and 'answer' (answer is revealed next week)")
    if d.get("last_answer") is not None and not (d["last_answer"].get("prompt") and d["last_answer"].get("answer")):
        errs.append("last_answer must be null or have prompt+answer")
    b = d.get("building")
    if b is not None and not isinstance(b.get("repos", []), list):
        errs.append("building.repos must be a list")
    j = d.get("jobs")
    if j is not None and not j.get("summary"):
        errs.append("jobs must be null or have a summary")
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
    os.makedirs(PAGE_DIR, exist_ok=True)
    stub = os.path.join(PAGE_DIR, f"{d['date']}.md")
    title = f"Inference Rundown #{d['issue']}"
    with open(stub, "w") as f:
        f.write(f"---\ntitle: \"{title}\"\nkey: \"{d['date']}\"\nissue: {d['issue']}\ndate: {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S} +0000\n"
                f"description: {json.dumps(d['headline'])}\n---\n")
    print(f"OK: {path} valid; wrote {os.path.relpath(stub, ROOT)}")


if __name__ == "__main__":
    main()
