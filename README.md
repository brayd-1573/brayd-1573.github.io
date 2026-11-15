# brayd-1573.github.io

Personal site of Brayden Cox: ML systems & LLM inference. Built with [Astro](https://astro.build),
deployed to GitHub Pages by `.github/workflows/pages-deploy.yml` on every push to `main`.

## Develop

Requires Node 22 (see `.nvmrc`).

```bash
npm install
npm run dev       # http://localhost:4321
npm run verify    # production build + internal link check (what CI runs)
```

## Where things live

| What | Where |
| --- | --- |
| Bio, links, focus areas, projects | `src/data/profile.ts` |
| Blog posts (Markdown, `YYYY-MM-DD-slug.md` → `/posts/slug/`) | `src/content/posts/` |
| Design tokens (colors, type, dark/light) | `src/styles/global.css` |
| Inference Rundown data (one JSON per issue) | `_data/digests/<YYYY-MM-DD>.json` |
| Rundown pages (`/rundown/`, `/rundown/<date>/`) | `src/pages/rundown/`, `src/styles/rundown.css` |
| Rundown schema (build-time validation) | `src/content.config.ts` (mirrors `tools/digest/finalize.py`) |

## Inference Rundown

A weekly Claude Code routine follows `tools/digest/INSTRUCTIONS.md`: it runs `tools/digest/gather.py`,
writes `_data/digests/<date>.json`, validates it with `tools/digest/finalize.py`, and pushes to `main`.
The deploy workflow builds the page, then the `notify-rundown` job opens a GitHub issue linking to
`https://brayd-1573.github.io/rundown/<date>/`. Actions → *Build and Deploy* → *Run workflow*
redeploys and re-sends the notification for the latest issue.

Post ideas: `CONTENT_IDEAS.md`.
