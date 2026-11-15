import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// Blog posts. File names keep the Jekyll `YYYY-MM-DD-slug.md` convention; the id drops the
// date so URLs stay /posts/<slug>/ exactly as on the old Chirpy site.
const posts = defineCollection({
  loader: glob({
    base: './src/content/posts',
    pattern: '**/*.md',
    generateId: ({ entry }) => entry.replace(/\.md$/, '').replace(/^\d{4}-\d{2}-\d{2}-/, ''),
  }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    description: z.string().optional(),
    tags: z.array(z.string()).default([]),
    categories: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

// Weekly Inference Rundown. The cloud routine writes _data/digests/<YYYY-MM-DD>.json (see
// tools/digest/INSTRUCTIONS.md); the file name is the URL key: /rundown/<YYYY-MM-DD>/.
// This schema mirrors tools/digest/finalize.py so a malformed issue fails the build loudly.
const md = z.string(); // inline markdown allowed
const url = z.string(); // finalize.py enforces https://

const digests = defineCollection({
  loader: glob({
    base: './_data/digests',
    pattern: '*.json',
    generateId: ({ entry }) => entry.replace(/\.json$/, ''),
  }),
  schema: z.object({
    issue: z.number().int().positive(),
    date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
    window: z.object({ from: z.string(), to: z.string() }),
    headline: z.string(),
    tldr: md,
    stats: z.array(z.object({ value: z.union([z.string(), z.number()]), label: z.string() })).min(2).max(4),
    building: z
      .object({
        note: md.optional().nullable(),
        repos: z
          .array(
            z.object({
              name: z.string(),
              url,
              commits: z.number().int(),
              highlights: z.array(z.string()).default([]),
            }),
          )
          .default([]),
        upstream: z.array(z.object({ title: z.string(), url, state: z.string() })).default([]),
      })
      .nullable()
      .optional(),
    prs: z
      .array(
        z.object({
          number: z.number().int(),
          title: z.string(),
          url,
          area: z.string(),
          summary: md,
          why_it_matters: md,
          read_the_diff: z.boolean().default(false),
        }),
      )
      .length(3),
    contribute: z
      .array(
        z.object({
          number: z.number().int(),
          title: z.string(),
          url,
          difficulty: z.enum(['starter', 'moderate', 'stretch']),
          fit: z.number().int().min(1).max(5),
          why_you: md,
          first_steps: z.array(md).min(1),
          status: z.string(),
        }),
      )
      .min(2)
      .max(3),
    followups: z.array(z.object({ title: z.string(), url, status: z.string() })).default([]),
    news: z
      .array(
        z.object({
          title: z.string(),
          url,
          source: z.string(),
          tag: z.enum(['hardware', 'software', 'startups', 'market', 'jobs', 'open-source', 'policy']),
          summary: md,
        }),
      )
      .min(1)
      .max(6),
    releases: z.array(z.object({ repo: z.string(), tag: z.string(), url, summary: md })).default([]),
    papers: z
      .array(
        z.object({
          title: z.string(),
          url,
          authors: z.string(),
          claim: md,
          why_it_matters: md,
          signal: z.string(),
          reproduce: z.enum(['yes', 'maybe', 'no']),
          reproduce_note: z.string().optional().nullable(),
        }),
      )
      .default([]),
    videos: z
      .array(
        z.object({
          title: z.string(),
          url,
          video_id: z.string(),
          channel: z.string(),
          kind: z.enum(['talk', 'lecture', 'tutorial', 'breakdown', 'interview', 'demo']),
          length: z.string().optional().nullable(),
          why: md,
        }),
      )
      .default([]),
    jobs: z
      .object({
        summary: md,
        skills: z.array(z.object({ name: z.string(), note: z.string().optional().nullable() })).default([]),
        postings: z.array(z.object({ company: z.string(), role: z.string(), url })).default([]),
      })
      .nullable()
      .optional(),
    question: z.object({ prompt: md, hint: md.optional().nullable(), answer: md }),
    last_answer: z.object({ prompt: md, answer: md }).nullable().optional(),
  }),
});

export const collections = { posts, digests };
