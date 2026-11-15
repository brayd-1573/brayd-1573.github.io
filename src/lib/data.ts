import { getCollection } from 'astro:content';

export async function getPosts() {
  const posts = await getCollection('posts', ({ data }) => import.meta.env.DEV || !data.draft);
  return posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

/** Newest issue first. The id is the file name (YYYY-MM-DD), which is also the URL key. */
export async function getIssues() {
  const issues = await getCollection('digests');
  return issues.sort((a, b) => b.id.localeCompare(a.id));
}

export function excerpt(body: string | undefined, max = 180): string {
  if (!body) return '';
  const para = body
    .split(/\n{2,}/)
    .map((p) => p.trim())
    .find((p) => p && !/^(#|>|```|[-*] |\d+\.|---|\|)/.test(p));
  if (!para) return '';
  const t = para
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/[*_`]/g, '')
    .replace(/\s+/g, ' ');
  return t.length <= max ? t : t.slice(0, t.lastIndexOf(' ', max)) + '…';
}

export function readingTime(body: string | undefined): number {
  return Math.max(1, Math.round((body ?? '').split(/\s+/).length / 230));
}
