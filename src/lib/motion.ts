// Scroll-triggered motion. Everything here is progressive enhancement: without JS (or with
// prefers-reduced-motion) the final text/state is shown immediately.

const GLYPHS = '01#/\\<>_-=+*[]{}%$';
const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

/**
 * [data-decode]          → mono "decode": characters resolve left→right through random glyphs.
 * [data-decode="type"]   → typewriter with a block caret (for proportional headlines).
 * Optional data-delay="ms". The accessible text is always the full string (sr-only copy).
 */
function prepDecode(el: HTMLElement) {
  const text = (el.textContent ?? '').replace(/\s+/g, ' ').trim();
  el.dataset.text = text;
  el.innerHTML = `<span class="sr-only">${esc(text)}</span><span class="dc" aria-hidden="true"><span style="opacity:0">${esc(text)}</span></span>`;
}

function runDecode(el: HTMLElement) {
  const text = el.dataset.text ?? '';
  const out = el.querySelector<HTMLElement>('.dc');
  if (!out) return;
  const type = el.dataset.decode === 'type';
  const perChar = type ? 34 : 22;
  const dur = Math.min(type ? 2200 : 900, Math.max(320, text.length * perChar));
  const delay = Number(el.dataset.delay ?? 0);
  let t0 = 0;
  const frame = (now: number) => {
    if (!t0) t0 = now;
    const p = Math.min(1, Math.max(0, (now - t0 - delay) / dur));
    const n = Math.floor(p * text.length);
    if (p >= 1) {
      out.innerHTML = type ? `${esc(text)}<span class="caret" style="animation-iteration-count:4"></span>` : esc(text);
      return;
    }
    const done = esc(text.slice(0, n));
    const rest = text.slice(n);
    if (type) {
      out.innerHTML = `${done}<span class="caret"></span><span style="opacity:0">${esc(rest)}</span>`;
    } else {
      const g = rest
        .slice(0, 4)
        .split('')
        .map((c) => (c === ' ' ? ' ' : GLYPHS[(Math.random() * GLYPHS.length) | 0]))
        .join('');
      out.innerHTML = `${done}<span class="dc-ghost">${esc(g)}</span><span style="opacity:0">${esc(rest.slice(4))}</span>`;
    }
    requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);
}

export function initMotion() {
  const decs = [...document.querySelectorAll<HTMLElement>('[data-decode]')];
  const reveals = [...document.querySelectorAll<HTMLElement>('[data-reveal]')];
  if (reduced() || !('IntersectionObserver' in window)) {
    reveals.forEach((el) => el.classList.add('in'));
    return;
  }
  decs.forEach(prepDecode);
  const io = new IntersectionObserver(
    (entries) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        const el = e.target as HTMLElement;
        io.unobserve(el);
        if (el.hasAttribute('data-decode')) runDecode(el);
        else el.classList.add('in');
      }
    },
    { rootMargin: '0px 0px -8% 0px', threshold: 0.1 },
  );
  decs.forEach((el) => io.observe(el));
  reveals.forEach((el) => io.observe(el));
}
