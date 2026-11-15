// Everything personal on the site lives here. Edit freely; pages re-render from it.

export const site = {
  name: 'Brayden Cox',
  url: 'https://brayd-1573.github.io',
  title: 'Brayden Cox · ML Systems & LLM Inference',
  description:
    'Brayden Cox studies math and computer science at Vanderbilt and builds LLM inference systems: kernels, KV caches, batching and scheduling. Blog, projects, and a weekly inference rundown & digest.',
  role: 'ML systems · LLM inference',
  rundown: 'Inference Rundown & Weekly Digest',
  school: 'Mathematics + Computer Science, Vanderbilt University',
  email: 'brayden.cox2005@icloud.com',
  github: 'https://github.com/brayd-1573',
  linkedin: 'https://www.linkedin.com/in/braydencox1573',
};

export const nav = [
  { href: '/#projects', label: 'Projects' },
  { href: '/posts/', label: 'Blog' },
  { href: '/rundown/', label: 'Rundown' },
  { href: '/about/', label: 'About' },
];

export const focus = [
  {
    k: 'Inference engines',
    v: 'Building the serving path from scratch: attention, RoPE, KV cache, continuous batching, paged attention.',
  },
  {
    k: 'Kernels',
    v: 'Learning to write and profile GPU kernels in CUDA and Triton, and to reason about them with roofline analysis.',
  },
  {
    k: 'Research',
    v: 'Undergraduate research on GPU internals and performance under LLM workloads, with Prof. Aniruddha Gokhale.',
  },
  {
    k: 'Upstream',
    v: 'Reading vLLM internals every week and tracking open issues to contribute to.',
  },
];

export type Project = {
  name: string;
  url: string;
  status: string;
  summary: string;
  points: string[];
  stack: string[];
  credit?: { label: string; url: string };
};

// Honest status: these are course builds in progress. Update `status`/`points` as you go.
export const projects: Project[] = [
  {
    name: 'tiny-llm',
    url: 'https://github.com/brayd-1573/tiny-llm',
    status: 'In progress',
    summary:
      'LLM serving from first principles on Apple Silicon: a Qwen3 inference path built directly on MLX arrays, then a mini vLLM on top.',
    points: [
      'Attention, RoPE, GQA, RMSNorm and sampling written by hand, with MLX as the correctness oracle',
      'KV cache and quantized decode matvec, benchmarked against a synchronized baseline',
      'Continuous batching, chunked prefill and paged KV with FlashAttention-style kernels',
    ],
    stack: ['Python', 'C++', 'MLX'],
    credit: { label: 'Course by skyzh', url: 'https://github.com/skyzh/tiny-llm' },
  },
  {
    name: 'Inference Rundown & Weekly Digest',
    url: '/rundown/',
    status: 'Live · weekly',
    summary:
      'An automated weekly briefing on LLM inference: notable vLLM merges, open issues to contribute to, papers, hardware news and the job market.',
    points: [
      'Stdlib-Python gatherer pre-filters GitHub, arXiv, HF Papers, HN, blogs and YouTube into one compact bundle',
      'A scheduled Claude routine writes a schema-validated JSON issue; this site renders it',
      'GitHub Actions deploys and opens a notification issue on every new edition',
    ],
    stack: ['Python', 'GitHub Actions', 'Astro', 'Claude'],
  },
];
