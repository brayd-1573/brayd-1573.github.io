# Inference Rundown — weekly routine instructions

You are producing this week's **Inference Rundown**: a one-page weekly digest on LLM inference
published on Brayden's site at `/rundown/<date>/`. Brayden reads it to stay current, to find
upstream contributions, and to stay motivated while working toward an inference-engineer role.

**Reader profile (use it to judge relevance):** student building inference systems from scratch:
`tiny-llm` (MLX: attention, RoPE, KV cache, quantized matmul, FlashAttention, continuous batching,
paged attention) and `tiny-vllm`. Strong in Python, learning CUDA/Triton/Metal kernels, roofline
analysis, and vLLM internals. Wants: what's important in production inference, what to read,
what to contribute, what the job market rewards.

## Budget (keep runs cheap)

- All raw data comes from `tools/digest/gather.py` as one compact JSON file. Read it once.
  Do **not** re-fetch sources it already covers, and never print raw HTML or full API responses.
- Hard caps for the whole run: **≤ 6** `--pr` lookups, **≤ 5** `--issue` lookups,
  **≤ 4** web searches, **≤ 4** page fetches. Fetch a page only to verify a claim you'll publish.
- Don't explore the repo. You only touch the two files listed in step 7.

## Steps

1. `python3 tools/digest/finalize.py --last` gives you the next issue number, last week's
   contribution picks and question, and recently used URLs (don't repeat those items).
2. `python3 tools/digest/gather.py --out /tmp/rundown.json` takes about a minute. Then read `/tmp/rundown.json`.
   If last week had picks: `python3 tools/digest/gather.py --followup <n1,n2,...>`.
   If `errors` lists a failed source, fill that gap with at most one web search.
3. **Merged PRs**: from `vllm_merged_prs.top_candidates` (pre-ranked, noise removed), shortlist
   up to 6 and run `gather.py --pr <n>` on each. Publish the 3–5 most significant: new kernels,
   scheduler/KV-cache/attention changes, real perf wins with numbers, architectural shifts.
   Prefer ones that map to what Brayden has built. Set `read_the_diff: true` on 1–2 whose diff
   is small enough and instructive enough to actually read.
4. **Contribution picks**: from `vllm_good_first_issues`, choose up to 5 candidates and run
   `gather.py --issue <n>`. Reject any that are claimed ("I'll work on this", assignee, or an
   open linked PR) or stale/blocked. Publish 2–3 with honest `fit` (1–5), a `why_you` tied to
   his projects, and 2–4 concrete `first_steps` (files to open, how to repro). `status` says
   e.g. "Unclaimed, last activity Nov 10". For follow-ups, report status neutrally
   ("still open, no PR yet", "claimed by someone else", "fixed in #123"). **Never** comment
   on whether Brayden worked on it.
5. **Everything else**, from the bundle (plus capped searches):
   - `news` (3–8): NVIDIA/AMD/hardware, CUDA/Triton/PyTorch changes, inference startups
     (funding, launches, pricing), market moves, notable discussions. Use `blog_feeds`,
     `hacker_news`, `releases`. Skip non-inference gossip unless it plausibly affects the
     inference market or jobs (then say how in one line).
   - `releases` (0–6): only notable ones, one-line summary of what matters for inference.
   - `papers` (2–5): from `papers_hf_trending` (upvotes = community signal) and
     `papers_arxiv_recent`. Inference/serving/kernels/quantization/long-context only.
     `signal` is concrete ("142 HF upvotes", "HN front page"). `reproduce` is yes/maybe/no
     depending on whether it's feasible on a single GPU or a Mac in a weekend.
   - `videos` (0–5): from `youtube`: talks, lectures, tutorials and breakdowns about inference,
     GPUs or kernels. Skip off-topic conference talks. `length` only if known.
   - `jobs`: summary of what inference roles are asking for this week (from `jobs_hn_hiring` +
     ≤ 1 search), 3–6 `skills` with short notes, 0–5 `postings` (link to the HN comment or
     careers page). Set `null` if there's nothing real to say.
6. **Personal + question**:
   - `building`: from `my_activity` (public repos only). If there are no commits, set
     `building: null` (the section hides). No guilt or streak language, ever.
   - `question`: a new back-of-envelope inference question (memory-bandwidth bound decode,
     KV-cache sizing, batch-size break-even, TP comm cost, quantization bytes, etc.) with a
     `hint` and a worked `answer` showing the arithmetic. The answer is published next week.
   - `last_answer`: last week's `question` prompt + answer (from step 1), or `null`.
7. Write `_data/digests/<DATE>.json`, where `DATE=$(TZ=America/Chicago date +%F)`. Then run
   `python3 tools/digest/finalize.py _data/digests/<DATE>.json` and fix the file until it prints `OK`
   (it also writes `_digests/<DATE>.md`). Commit only those two files:
   `git add _data/digests/<DATE>.json _digests/<DATE>.md && git commit -m "rundown: issue <N>"`,
   then `git push origin HEAD:main`. Pushing to `main` deploys the page, and a workflow
   opens the notification issue. If the push to main is refused, push to `claude/rundown-<DATE>`
   and say so in your final message.

## Writing rules

- **Every item must come from the bundle or a page or search you actually read.** Never invent
  numbers, benchmarks, quotes, or URLs. Copy URLs exactly.
- Concise and technical, like a sharp senior engineer briefing a junior colleague. No hype words
  ("revolutionary", "game-changing"). Concrete numbers beat adjectives.
- `headline` (≤ 110 chars): this week's single most important development, stated specifically.
- `tldr` (≤ 700 chars): 2–4 sentences on the week's big picture and the one thing to read.
- Inline markdown (`code`, **bold**, links) is allowed in summary/why/claim fields; plain text in titles.

## Schema (`_data/digests/<DATE>.json`)

```json
{
  "issue": 1,
  "date": "2026-11-22",
  "window": {"from": "2026-11-15", "to": "2026-11-22"},
  "headline": "…",
  "tldr": "…",
  "stats": [{"value": "412", "label": "vLLM PRs merged"}, {"value": "3", "label": "major releases"}],
  "building": {"note": "…", "repos": [{"name": "tiny-llm", "url": "https://…", "commits": 4, "highlights": ["…"]}],
               "upstream": [{"title": "…", "url": "https://…", "state": "open"}]},
  "prs": [{"number": 123, "title": "…", "url": "https://github.com/vllm-project/vllm/pull/123",
           "area": "kv-cache", "summary": "what changed", "why_it_matters": "…", "read_the_diff": false}],
  "contribute": [{"number": 456, "title": "…", "url": "https://…", "difficulty": "starter|moderate|stretch",
                  "fit": 4, "why_you": "…", "first_steps": ["…", "…"], "status": "Unclaimed, …"}],
  "followups": [{"title": "#456 …", "url": "https://…", "status": "still open, no PR yet"}],
  "news": [{"title": "…", "url": "https://…", "source": "SemiAnalysis",
            "tag": "hardware|software|startups|market|jobs|open-source|policy", "summary": "…"}],
  "releases": [{"repo": "vllm-project/vllm", "tag": "v0.x.y", "url": "https://…", "summary": "…"}],
  "papers": [{"title": "…", "url": "https://arxiv.org/abs/…", "authors": "A, B et al.", "claim": "…",
              "why_it_matters": "…", "signal": "120 HF upvotes", "reproduce": "yes|maybe|no", "reproduce_note": "…"}],
  "videos": [{"title": "…", "url": "https://www.youtube.com/watch?v=ID", "video_id": "ID", "channel": "GPU MODE",
              "kind": "talk|lecture|tutorial|breakdown|interview|demo", "length": "1:12:03", "why": "…"}],
  "jobs": {"summary": "…", "skills": [{"name": "Triton", "note": "…"}], "postings": [{"company": "…", "role": "…", "url": "https://…"}]},
  "question": {"prompt": "…", "hint": "…", "answer": "worked arithmetic…"},
  "last_answer": {"prompt": "…", "answer": "…"}
}
```

`stats`: 2–4 numbers taken from the bundle (e.g. `vllm_merged_prs.merged_total`, papers scanned,
releases). `followups`, `releases`, `videos` may be empty lists; `building`, `jobs`, `last_answer` may be `null`.

Finish with a 3-line summary: issue number, URL `https://brayd-1573.github.io/rundown/<DATE>/`,
and any sources that failed.
