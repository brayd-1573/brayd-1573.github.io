// Tiny, safe markdown renderer for Rundown text fields (written by the weekly routine).
// Supports `code`, **bold**, *em*, [links](https://…) and blank-line paragraphs. All other HTML
// is escaped, so nothing in the JSON can inject markup.

const esc = (s: string) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

export function inline(src: string | null | undefined): string {
  if (!src) return '';
  const codes: string[] = [];
  let s = esc(src).replace(/`([^`]+)`/g, (_, c) => `\u0000${codes.push(c) - 1}\u0000`);
  s = s
    .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2">$1</a>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*\w])\*([^*\n]+)\*(?!\w)/g, '$1<em>$2</em>');
  return s.replace(/\u0000(\d+)\u0000/g, (_, i) => `<code>${codes[+i]}</code>`);
}

export function block(src: string | null | undefined): string {
  if (!src) return '';
  return src
    .trim()
    .split(/\n{2,}/)
    .map((p) => `<p>${inline(p).replace(/\n/g, '<br>')}</p>`)
    .join('');
}

export const pad = (n: number, w = 2) => String(n).padStart(w, '0');

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

/** "2026-11-08" -> "Nov 8" (+ ", 2026" when withYear). Parsed as a plain date, no TZ drift. */
export function ymd(s: string, withYear = false): string {
  const [y, m, d] = s.split('-').map(Number);
  return `${MONTHS[m - 1]} ${d}${withYear ? `, ${y}` : ''}`;
}

export function fmtDate(d: Date): string {
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'America/Chicago' });
}

/** Plain-text version of a markdown string (for meta descriptions / excerpts). */
export function plain(src: string, max = 0): string {
  const t = src
    .replace(/`([^`]+)`/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/\*\*?([^*]+)\*\*?/g, '$1')
    .replace(/\s+/g, ' ')
    .trim();
  if (!max || t.length <= max) return t;
  return t.slice(0, t.lastIndexOf(' ', max)).replace(/[,.;:]$/, '') + '…';
}
