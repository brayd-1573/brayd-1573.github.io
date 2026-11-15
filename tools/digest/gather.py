#!/usr/bin/env python3
"""Collect raw material for the weekly Inference Rundown.

Pure stdlib so it runs anywhere. Every source is fetched and *pre-filtered* here so
the agent only reads a compact JSON bundle instead of raw pages/APIs (this is the
main token saver). Each source fails independently; failures are listed under
"errors" instead of crashing the run.

Usage:
  python3 tools/digest/gather.py [--days 7] [--out /tmp/rundown.json]
  python3 tools/digest/gather.py --pr 12345          # details for one vLLM PR
  python3 tools/digest/gather.py --issue 12345       # details + recent comments for one vLLM issue
  python3 tools/digest/gather.py --followup 1,2,3    # status of previously suggested issues

Set GITHUB_TOKEN or GH_TOKEN to raise the GitHub rate limit (optional).
"""

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

GH_USER = "brayd-1573"
SITE_REPO = f"{GH_USER}/{GH_USER}.github.io"
VLLM = "vllm-project/vllm"
UA = "Mozilla/5.0 (inference-rundown digest bot)"

# vLLM title prefixes worth surfacing vs. noise.
VLLM_KEEP = re.compile(
    r"\[(kernel|perf|performance|core|v1|attention|attn|quantization|quant|spec ?decode|speculative|"
    r"scheduler|sched|kv|kv ?cache|kv ?connector|distributed|model ?runner|torch\.compile|compile|"
    r"cuda ?graph|feature|feat|moe|fp8|fp4|nvfp4|hardware|rocm|tpu|cpu|optimization|engine|p/d|"
    r"disagg|lora|sampler|sampling|executor|worker|memory|ep|dp|tp|pp)\b",
    re.I,
)
VLLM_DROP = re.compile(r"\[(doc|docs|ci|ci/build|build|test|tests|misc|chore|typo|frontend|tool ?parser)\]", re.I)

INFERENCE_KW = re.compile(
    r"\b(inference|serving|serve|decod|kv[- ]?cache|quantiz|speculative|attention|kernel|throughput|"
    r"latency|batching|gpu|cuda|triton|vllm|sglang|tensorrt|llama\.cpp|flash ?attention|moe|mixture[- ]of[- ]experts|"
    r"long[- ]context|prefill|token(s)?/s|fp8|fp4|int4|sparsit|pruning|distill|compression|accelerat|"
    r"h100|h200|b200|b300|gb200|blackwell|rubin|tpu|asic|groq|cerebras|nvidia|amd|mi300|mi350|mi355|mi400)\b",
    re.I,
)

ERRORS = []


# ---------------------------------------------------------------- helpers
_GH_TOKEN_OK = True  # flipped off if the ambient token is scoped too narrowly (e.g. cloud sessions)


def fetch(url, accept=None, gh=False, timeout=30):
    global _GH_TOKEN_OK
    headers = {"User-Agent": UA}
    if accept:
        headers["Accept"] = accept
    tok = None
    if gh:
        headers["Accept"] = "application/vnd.github+json"
        tok = (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")) if _GH_TOKEN_OK else None
        if tok:
            headers["Authorization"] = f"Bearer {tok}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        if tok and e.code in (401, 403):  # token not valid for this repo: retry anonymously from now on
            _GH_TOKEN_OK = False
            headers.pop("Authorization", None)
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        raise


def gh_json(path, **params):
    q = ("?" + urllib.parse.urlencode(params)) if params else ""
    return json.loads(fetch(f"https://api.github.com{path}{q}", gh=True))


def gh_search(q, kind="issues", sort=None, pages=1, per_page=100):
    items = []
    for page in range(1, pages + 1):
        params = {"q": q, "per_page": per_page, "page": page}
        if sort:
            params.update(sort=sort, order="desc")
        data = gh_json(f"/search/{kind}", **params)
        items += data.get("items", [])
        if len(data.get("items", [])) < per_page:
            break
        time.sleep(7)  # unauthenticated search limit is 10/min
    return items


def clip(s, n):
    s = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def safe(name, fn, default):
    try:
        return fn()
    except Exception as e:  # noqa: BLE001
        ERRORS.append(f"{name}: {type(e).__name__}: {e}"[:300])
        return default


def parse_date(s):
    if not s:
        return None
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z"):
        try:
            d = datetime.strptime(s.strip(), fmt)
            return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    try:
        d = datetime.fromisoformat(s.strip().replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


# ---------------------------------------------------------------- GitHub: vLLM
def vllm_merged_prs(since):
    items = gh_search(f"repo:{VLLM} is:pr is:merged merged:>={since:%Y-%m-%d}", pages=4)
    total = len(items)
    rows = []
    for it in items:
        t = it["title"]
        if VLLM_DROP.search(t):
            continue
        labels = [l["name"] for l in it.get("labels", [])]
        score = it.get("comments", 0) + 3 * it.get("reactions", {}).get("total_count", 0)
        if VLLM_KEEP.search(t) or any(re.search(r"perf|kernel|quant|spec|kv", l, re.I) for l in labels):
            score += 15
        if re.search(r"\b(\d+(\.\d+)?x|speed ?up|faster|throughput|latency|perf)\b", t, re.I):
            score += 10
        rows.append({
            "n": it["number"], "title": t[:140], "labels": labels[:4],
            "comments": it.get("comments", 0), "reactions": it.get("reactions", {}).get("total_count", 0),
            "author": it["user"]["login"], "score": score,
        })
    rows.sort(key=lambda r: -r["score"])
    return {"merged_total": total, "top_candidates": rows[:45]}


def vllm_pr_detail(n):
    pr = gh_json(f"/repos/{VLLM}/pulls/{n}")
    files = gh_json(f"/repos/{VLLM}/pulls/{n}/files", per_page=100)
    return {
        "n": n, "title": pr["title"], "url": pr["html_url"], "author": pr["user"]["login"],
        "merged_at": pr.get("merged_at"), "additions": pr.get("additions"), "deletions": pr.get("deletions"),
        "files": [f["filename"] for f in files][:25],
        "body": clip(pr.get("body"), 2500),
    }


def vllm_good_first_issues():
    items = gh_search(f'repo:{VLLM} is:issue is:open label:"good first issue" no:assignee', sort="updated")
    time.sleep(7)
    items += gh_search(f'repo:{VLLM} is:issue is:open label:"help wanted" no:assignee', sort="updated", per_page=40)
    out, seen = [], set()
    for it in items:
        if it["number"] in seen or len(out) >= 40:
            continue
        seen.add(it["number"])
        out.append({
            "n": it["number"], "title": it["title"][:140], "url": it["html_url"],
            "labels": [l["name"] for l in it.get("labels", [])][:5],
            "comments": it.get("comments", 0), "created": it["created_at"][:10], "updated": it["updated_at"][:10],
            "body": clip(it.get("body"), 350),
        })
    return out


def vllm_issue_detail(n):
    it = gh_json(f"/repos/{VLLM}/issues/{n}")
    comments = gh_json(f"/repos/{VLLM}/issues/{n}/comments", per_page=100)
    tl = safe(f"timeline {n}", lambda: gh_json(f"/repos/{VLLM}/issues/{n}/timeline", per_page=100), [])
    linked_prs = sorted({
        e["source"]["issue"]["html_url"] for e in tl
        if e.get("event") == "cross-referenced" and e.get("source", {}).get("issue", {}).get("pull_request")
    })
    return {
        "n": n, "title": it["title"], "url": it["html_url"], "state": it["state"],
        "assignees": [a["login"] for a in it.get("assignees", [])],
        "body": clip(it.get("body"), 1500),
        "linked_prs": linked_prs[:8],
        "recent_comments": [
            {"by": c["user"]["login"], "at": c["created_at"][:10], "text": clip(c["body"], 280)} for c in comments[-6:]
        ],
        "user_commented": any(c["user"]["login"] == GH_USER for c in comments),
    }


# ---------------------------------------------------------------- GitHub: user's public work
def user_activity(since):
    repos = gh_json(f"/users/{GH_USER}/repos", sort="pushed", per_page=30, type="owner")
    out = []
    for r in repos:
        pushed = parse_date(r.get("pushed_at"))
        if not pushed or pushed < since or r.get("private"):
            continue
        commits = safe(
            f"commits {r['name']}",
            lambda r=r: gh_json(f"/repos/{r['full_name']}/commits", since=since.isoformat(), author=GH_USER, per_page=50),
            [],
        )
        msgs = [c["commit"]["message"].split("\n")[0][:120] for c in commits]
        if r["full_name"] == SITE_REPO:
            msgs = [m for m in msgs if not m.lower().startswith("rundown")]
        if msgs:
            out.append({"repo": r["full_name"], "url": r["html_url"], "description": (r.get("description") or "")[:150],
                        "commits": len(msgs), "messages": msgs[:15]})
    prs = gh_search(f"author:{GH_USER} is:pr created:>={since:%Y-%m-%d}")
    upstream = []
    for p in prs:
        repo = p["repository_url"].split("/repos/")[-1]
        if not repo.startswith(f"{GH_USER}/"):
            upstream.append({"title": p["title"][:140], "url": p["html_url"], "state": p["state"], "repo": repo})
    return {"repos": out, "prs_opened_elsewhere": upstream}


def releases(since):
    out = []
    for repo in ["vllm-project/vllm", "sgl-project/sglang", "NVIDIA/TensorRT-LLM", "flashinfer-ai/flashinfer",
                 "triton-lang/triton", "pytorch/pytorch", "ggml-org/llama.cpp"]:
        rels = safe(f"releases {repo}", lambda repo=repo: gh_json(f"/repos/{repo}/releases", per_page=5), [])
        for r in rels:
            d = parse_date(r.get("published_at"))
            if d and d >= since and not r.get("draft"):
                out.append({"repo": repo, "tag": r["tag_name"], "url": r["html_url"], "date": r["published_at"][:10],
                            "notes": clip(r.get("body"), 700 if repo != "ggml-org/llama.cpp" else 150)})
        if repo == "ggml-org/llama.cpp":  # releases nearly daily; keep only the latest
            out = [o for o in out if o["repo"] != repo] + [o for o in out if o["repo"] == repo][:1]
    return out


# ---------------------------------------------------------------- papers
def hf_daily_papers(since):
    out, seen = [], set()
    day = datetime.now(timezone.utc)
    while day >= since - timedelta(days=1):
        if day.date() >= datetime.now(timezone.utc).date():  # HF rejects today's (UTC) date until it rolls over
            day -= timedelta(days=1)
            continue
        rows = safe(f"hf papers {day:%Y-%m-%d}",
                    lambda d=day: json.loads(fetch(f"https://huggingface.co/api/daily_papers?date={d:%Y-%m-%d}")), [])
        for r in rows:
            p = r.get("paper", {})
            pid = p.get("id")
            if not pid or pid in seen:
                continue
            seen.add(pid)
            text = f"{p.get('title', '')} {p.get('summary', '')}"
            if not INFERENCE_KW.search(text):
                continue
            out.append({"arxiv": pid, "url": f"https://arxiv.org/abs/{pid}", "title": clip(p.get("title"), 160),
                        "upvotes": p.get("upvotes", 0), "summary": clip(p.get("summary"), 320),
                        "org": (p.get("organization") or {}).get("fullname") if isinstance(p.get("organization"), dict) else None})
        day -= timedelta(days=1)
    out.sort(key=lambda r: -r["upvotes"])
    return out[:25]


def arxiv_recent(since):
    q = ('(cat:cs.DC OR cat:cs.LG OR cat:cs.AR OR cat:cs.CL OR cat:cs.PF) AND '
         '(abs:"LLM inference" OR abs:"LLM serving" OR abs:"KV cache" OR abs:"speculative decoding" '
         'OR abs:"inference serving" OR abs:"decode throughput" OR abs:"attention kernel")')
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": q, "sortBy": "submittedDate", "sortOrder": "descending", "max_results": 80})
    root = ET.fromstring(fetch(url))
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for e in root.findall("a:entry", ns):
        d = parse_date(e.findtext("a:published", default="", namespaces=ns))
        if d and d < since:
            continue
        authors = [a.findtext("a:name", namespaces=ns) for a in e.findall("a:author", ns)]
        out.append({"url": e.findtext("a:id", namespaces=ns).replace("http://", "https://"),
                    "title": clip(e.findtext("a:title", namespaces=ns), 160),
                    "authors": ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else ""),
                    "summary": clip(e.findtext("a:summary", namespaces=ns), 260)})
    return out[:40]


# ---------------------------------------------------------------- news / discussion
def hacker_news(since):
    ts = int(since.timestamp())
    seen, out = set(), []
    for q in ["inference", "vLLM", "SGLang", "CUDA", "Nvidia", "GPU", "LLM serving", "tokens per second", "TensorRT",
              "Groq", "Cerebras", "AMD MI", "quantization", "KV cache", "llama.cpp", "speculative decoding"]:
        data = safe(f"hn {q}", lambda q=q: json.loads(fetch(
            "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
                {"query": q, "tags": "story", "numericFilters": f"created_at_i>{ts},points>25", "hitsPerPage": 20}))), {})
        for h in data.get("hits", []):
            if h["objectID"] in seen:
                continue
            seen.add(h["objectID"])
            out.append({"title": h.get("title"), "url": h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}",
                        "hn": f"https://news.ycombinator.com/item?id={h['objectID']}",
                        "points": h.get("points", 0), "comments": h.get("num_comments", 0)})
    out = [o for o in out if INFERENCE_KW.search(o["title"] or "")]
    out.sort(key=lambda r: -r["points"])
    return out[:30]


def feed(name, url, since, keyword_filter=True, limit=10):
    root = ET.fromstring(fetch(url))
    items = []
    for it in root.iter():
        tag = it.tag.split("}")[-1]
        if tag not in ("item", "entry"):
            continue
        def get(*keys):
            for k in keys:
                el = next((c for c in it if c.tag.split("}")[-1] == k), None)
                if el is not None:  # Elements without children are falsy, so compare to None explicitly
                    return el
            return None

        title_el, link_el = get("title"), get("link")
        title = (title_el.text if title_el is not None else "") or ""
        link = ((link_el.text or link_el.get("href")) if link_el is not None else "") or ""
        date_el = get("pubDate", "published", "updated", "date")
        d = parse_date(date_el.text if date_el is not None else None)
        summ_el = get("description", "summary", "content")
        summary = (summ_el.text if summ_el is not None else "") or ""
        if d is None:
            continue
        if d and d < since:
            continue
        if keyword_filter and not INFERENCE_KW.search(f"{title} {summary}"):
            continue
        items.append({"source": name, "title": clip(title, 160), "url": (link or "").strip(),
                      "date": d.strftime("%Y-%m-%d") if d else None, "summary": clip(summary, 280)})
    return items[:limit]


FEEDS = [
    ("vLLM blog", "https://vllm.ai/blog/rss.xml", False),
    ("NVIDIA Technical Blog", "https://developer.nvidia.com/blog/feed", True),
    ("Hugging Face blog", "https://huggingface.co/blog/feed.xml", True),
    ("PyTorch blog", "https://pytorch.org/blog/feed/", True),
    ("Together AI blog", "https://www.together.ai/blog/rss.xml", True),
    ("SemiAnalysis", "https://semianalysis.com/feed/", False),
    ("r/LocalLLaMA (top this week)", "https://www.reddit.com/r/LocalLLaMA/top/.rss?t=week", True),
]


# ---------------------------------------------------------------- YouTube
YT_CHANNELS = ["GPUMODE", "vllm-project", "NVIDIADeveloper", "umarjamilai", "AndrejKarpathy", "PyTorch",
               "huggingface", "SemiAnalysis", "anyscale", "baseten"]
YT_SEARCHES = ["LLM inference", "vLLM", "CUDA kernel optimization", "GPU inference talk"]


def _yt_age_days(label):
    m = re.search(r"(\d+)\s*(second|minute|hour|day|week|month|year)", label or "")
    if not m:
        return 999
    n, unit = int(m.group(1)), m.group(2)
    return n * {"second": 0, "minute": 0, "hour": 0, "day": 1, "week": 7, "month": 30, "year": 365}[unit]


def _yt_items(page_html):
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", page_html)
    if not m:
        return []
    data, out = json.loads(m.group(1)), []

    def walk(o):
        if isinstance(o, dict):
            if "lockupViewModel" in o:  # channel /videos grid
                lv = o["lockupViewModel"]
                md = lv.get("metadata", {}).get("lockupMetadataViewModel", {})
                parts = [p for row in md.get("metadata", {}).get("contentMetadataViewModel", {}).get("metadataRows", [])
                         for p in row.get("metadataParts", [])]
                labels = [p.get("accessibilityLabel") or p.get("text", {}).get("content", "") for p in parts]
                out.append({"id": lv.get("contentId"), "title": md.get("title", {}).get("content"),
                            "age": next((l for l in labels if "ago" in l), ""),
                            "views": next((l for l in labels if "view" in l), "")})
            elif "videoRenderer" in o:  # search results
                v = o["videoRenderer"]
                txt = lambda k: (v.get(k, {}).get("simpleText") or "".join(r.get("text", "") for r in v.get(k, {}).get("runs", [])))  # noqa: E731
                out.append({"id": v.get("videoId"), "title": txt("title"), "age": txt("publishedTimeText"),
                            "views": txt("viewCountText"), "duration": txt("lengthText"), "channel": txt("ownerText")})
            for val in o.values():
                walk(val)
        elif isinstance(o, list):
            for val in o:
                walk(val)

    walk(data)
    return out


def youtube(days):
    out, seen = [], set()
    for ch in YT_CHANNELS:
        page = safe(f"yt @{ch}", lambda ch=ch: fetch(f"https://www.youtube.com/@{ch}/videos", accept=None), "")
        for v in _yt_items(page)[:6]:  # newest first; cap so one conference dump can't flood the list
            if v["id"] and v["id"] not in seen and _yt_age_days(v["age"]) <= days:
                seen.add(v["id"])
                out.append({**v, "channel": ch, "url": f"https://www.youtube.com/watch?v={v['id']}", "via": "channel"})
    for q in YT_SEARCHES:
        # sp=EgQIAxAB -> filter: uploaded this week, videos only
        url = "https://www.youtube.com/results?" + urllib.parse.urlencode({"search_query": q, "sp": "EgQIAxAB", "hl": "en"})
        page = safe(f"yt search {q}", lambda url=url: fetch(url), "")
        for v in _yt_items(page)[:12]:
            if v["id"] and v["id"] not in seen and _yt_age_days(v["age"]) <= days:
                seen.add(v["id"])
                out.append({**v, "url": f"https://www.youtube.com/watch?v={v['id']}", "via": f"search:{q}"})
    return out[:40]


# ---------------------------------------------------------------- jobs (HN Who is hiring)
def hn_hiring():
    stories = json.loads(fetch("https://hn.algolia.com/api/v1/search_by_date?" + urllib.parse.urlencode(
        {"tags": "story,author_whoishiring", "query": "Who is hiring", "hitsPerPage": 1})))
    if not stories.get("hits"):
        return {}
    s = stories["hits"][0]
    seen, out = set(), []
    for q in ["inference", "vLLM", "CUDA", "GPU kernel", "TensorRT", "Triton"]:
        data = safe(f"hn hiring {q}", lambda q=q: json.loads(fetch("https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
            {"tags": f"comment,story_{s['objectID']}", "query": q, "hitsPerPage": 30}))), {})
        for h in data.get("hits", []):
            if h["objectID"] in seen or h.get("parent_id") != int(s["objectID"]):
                continue
            seen.add(h["objectID"])
            out.append({"url": f"https://news.ycombinator.com/item?id={h['objectID']}",
                        "text": clip(h.get("comment_text"), 420)})
    return {"thread": s.get("title"), "thread_url": f"https://news.ycombinator.com/item?id={s['objectID']}",
            "posts": out[:25]}


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--out", default=None)
    ap.add_argument("--pr", type=int)
    ap.add_argument("--issue", type=int)
    ap.add_argument("--followup", default=None, help="comma-separated vLLM issue numbers from last week")
    a = ap.parse_args()

    if a.pr:
        print(json.dumps(vllm_pr_detail(a.pr), indent=1, ensure_ascii=False))
        return
    if a.issue:
        print(json.dumps(vllm_issue_detail(a.issue), indent=1, ensure_ascii=False))
        return
    if a.followup:
        rows = []
        for n in [int(x) for x in a.followup.split(",") if x.strip()]:
            d = safe(f"followup {n}", lambda n=n: vllm_issue_detail(n), None)
            if d:
                d.pop("body", None)
                d["recent_comments"] = d["recent_comments"][-3:]
                rows.append(d)
        print(json.dumps(rows, indent=1, ensure_ascii=False))
        return

    now = datetime.now(timezone.utc)
    since = now - timedelta(days=a.days)
    bundle = {
        "window": {"from": since.strftime("%Y-%m-%d"), "to": now.strftime("%Y-%m-%d")},
        "my_activity": safe("my_activity", lambda: user_activity(since), {}),
        "vllm_merged_prs": safe("vllm_merged_prs", lambda: vllm_merged_prs(since), {}),
        "vllm_good_first_issues": safe("good_first_issues", vllm_good_first_issues, []),
        "releases": safe("releases", lambda: releases(since), []),
        "blog_feeds": [i for (n, u, kw) in FEEDS for i in safe(f"feed {n}", lambda n=n, u=u, kw=kw: feed(n, u, since, keyword_filter=kw), [])],
        "hacker_news": safe("hacker_news", lambda: hacker_news(since), []),
        "papers_hf_trending": safe("hf_papers", lambda: hf_daily_papers(since), []),
        "papers_arxiv_recent": safe("arxiv", lambda: arxiv_recent(since), []),
        "youtube": safe("youtube", lambda: youtube(a.days), []),
        "jobs_hn_hiring": safe("hn_hiring", hn_hiring, {}),
    }
    bundle["errors"] = ERRORS
    text = json.dumps(bundle, ensure_ascii=False, separators=(",", ":"))
    if a.out:
        with open(a.out, "w") as f:
            f.write(text)
        sizes = {k: len(json.dumps(v)) for k, v in bundle.items()}
        print(json.dumps({"wrote": a.out, "bytes": len(text), "section_bytes": sizes, "errors": ERRORS}, indent=1))
    else:
        print(text)


if __name__ == "__main__":
    main()
