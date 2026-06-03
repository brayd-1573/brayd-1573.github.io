# Blog Setup Guide

## Initial Setup Completed ✓

Your blog has been customized with:
- ✅ Personal information in `_config.yml`
- ✅ Custom About page highlighting your ML systems engineering goals
- ✅ First introductory blog post
- ✅ Nashville/Chicago timezone configured
- ✅ GitHub and LinkedIn links
- ✅ Vanderbilt email address

## Next Steps

### 1. GitHub Pages Configuration

To deploy your blog to `https://brayd-1573.github.io`:

1. Push this repository to GitHub (if you haven't already):
   ```bash
   git add .
   git commit -m "Initial blog setup for ML systems journey"
   git push origin main
   ```

2. Enable GitHub Pages in your repository:
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Pages**
   - Under "Build and deployment":
     - Source: **GitHub Actions** (not "Deploy from a branch")
   - The site will automatically deploy via the workflow in `.github/workflows/pages-deploy.yml`

3. Wait a few minutes for the first deployment to complete

### 2. Local Development

To preview your blog locally:

```bash
# Install dependencies (first time only)
bundle install

# Run the development server
bundle exec jekyll serve

# Or use the provided script
bash tools/run.sh
```

Visit `http://localhost:4000` in your browser.

### 3. Writing New Posts

Create new posts in the `_posts/` directory with the naming format:
```
YYYY-MM-DD-title-of-post.md
```

**Template:**
```markdown
---
title: "Your Post Title Here"
date: 2026-06-03 12:00:00 -0500
categories: [Category1, Category2]
tags: [tag1, tag2, tag3]
---

Your content here...
```

**Recommended Categories:**
- Technical (for deep dives and tutorials)
- Projects (for project write-ups)
- Learning (for learning experiences)
- Career (for career insights)
- Open Source (for contribution stories)

**Recommended Tags:**
- `cuda`, `gpu-optimization`, `ml-systems`
- `pytorch`, `tensorflow`, `triton`
- `cpp`, `rust`, `python`
- `distributed-systems`, `performance`
- `open-source`, `career`

### 4. Customization Ideas

#### Add a Profile Picture
Update `_config.yml`:
```yaml
avatar: /assets/img/avatar.jpg  # Add your photo to assets/img/
```

#### Enable Comments
Choose a comment system (Giscus recommended for GitHub-based commenting):
```yaml
comments:
  provider: giscus
  giscus:
    repo: brayd-1573/brayd-1573.github.io
    repo_id: YOUR_REPO_ID
    category: Announcements
    category_id: YOUR_CATEGORY_ID
```

Get your IDs from [giscus.app](https://giscus.app)

#### Add Google Analytics
Get a tracking ID from [Google Analytics](https://analytics.google.com) and add to `_config.yml`:
```yaml
analytics:
  google:
    id: G-XXXXXXXXXX
```

### 5. Content Ideas for Your Journey

**Technical Deep Dives:**
- CUDA programming tutorials
- GPU architecture explanations
- ML model optimization case studies
- Performance profiling techniques

**Project Showcases:**
- Course projects from Vanderbilt
- Personal GPU optimization experiments
- Contributions to ML frameworks
- Benchmarking studies

**Learning Logs:**
- New concepts you're mastering
- Books and papers you're reading
- Online courses you're taking
- Conferences or talks attended

**Career Development:**
- Internship application experiences
- Interview preparation tips
- Networking at ML systems events
- Industry trend analyses

### 6. Repository Settings Checklist

- [ ] Repository is public
- [ ] GitHub Pages is enabled via GitHub Actions
- [ ] Repository description mentions ML systems/GPU optimization
- [ ] Topics/tags added (e.g., `machine-learning`, `gpu`, `systems-programming`)
- [ ] First post is published and visible

### 7. Building Your Presence

**Short-term:**
- Write 1-2 technical posts per month
- Share posts on LinkedIn
- Engage with ML systems community on GitHub

**Medium-term:**
- Start contributing to open source ML systems projects
- Document your contributions on the blog
- Build a portfolio of GPU optimization projects

**Long-term:**
- Establish yourself as a thought leader in ML systems
- Use blog as portfolio for internship/job applications
- Network with engineers at NVIDIA/FAANG companies

## Resources

- [Chirpy Theme Documentation](https://github.com/cotes2020/jekyll-theme-chirpy/wiki)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Pages Docs](https://docs.github.com/en/pages)

## Troubleshooting

**Build fails on GitHub Actions:**
- Check the Actions tab in your repository for error logs
- Ensure all YAML frontmatter in posts is valid
- Verify no syntax errors in `_config.yml`

**Local server won't start:**
```bash
# Update dependencies
bundle update

# Clear cache and rebuild
bundle exec jekyll clean
bundle exec jekyll serve
```

**Posts not showing up:**
- Check the date isn't in the future
- Ensure filename format is correct: `YYYY-MM-DD-title.md`
- Verify YAML frontmatter is properly formatted

---

Good luck on your ML systems engineering journey! 🚀
