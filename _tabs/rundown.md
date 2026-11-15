---
title: Inference Rundown
icon: fas fa-microchip
order: 5
toc: false
---

<link rel="stylesheet" href="{{ '/assets/css/rundown.css' | relative_url }}">

{% assign issues = site.digests | sort: 'date' | reverse %}

<div class="rd">
  <p>A weekly rundown of what's happening in LLM inference: notable vLLM merges, open issues I could contribute to, industry and hardware news, papers, talks, and the job market.</p>
  {% include rundown-note.html %}

  {% if issues.size == 0 %}
  <p class="rd-empty">The first issue lands Sunday morning.</p>
  {% else %}
  {% assign latest = issues.first %}
  {% assign ld = site.data.digests[latest.key] %}
  <a class="rd-feature" href="{{ latest.url | relative_url }}">
    <span class="rd-kicker">Latest &middot; Issue {{ ld.issue }} &middot; {{ ld.window.from | date: "%b %-d" }} &ndash; {{ ld.window.to | date: "%b %-d, %Y" }}</span>
    <h2>{{ ld.headline | escape }}</h2>
    <p>{{ ld.tldr | markdownify | strip_html | truncate: 320 }}</p>
    <span class="go">Read issue {{ ld.issue }} &rarr;</span>
  </a>

  {% if issues.size > 1 %}
  <div class="rd-kicker" style="margin-bottom:.4rem">Archive</div>
  <ul class="rd-archive">
    {% for it in issues offset: 1 %}
    {% assign x = site.data.digests[it.key] %}
    <li><span class="n">#{{ x.issue }}</span><span class="d">{{ it.date | date: "%b %-d, %Y" }}</span><a href="{{ it.url | relative_url }}">{{ x.headline | escape }}</a></li>
    {% endfor %}
  </ul>
  {% endif %}
  {% endif %}
</div>
