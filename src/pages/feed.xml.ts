import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { site } from '../data/profile';
import { getPosts, excerpt } from '../lib/data';

// Same path as the old Chirpy feed, so existing subscribers keep working.
export async function GET(context: APIContext) {
  const posts = await getPosts();
  return rss({
    title: `${site.name} · Writing`,
    description: site.description,
    site: context.site!,
    items: posts.map((p) => ({
      title: p.data.title,
      pubDate: p.data.date,
      description: p.data.description ?? excerpt(p.body, 280),
      link: `/posts/${p.id}/`,
      categories: p.data.tags,
    })),
  });
}
