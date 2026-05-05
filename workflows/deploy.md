# Workflow — Deploy the blog

## Objective

Get the built `site/` folder onto the public internet.

---

## Primary host: GitHub Pages (fully automated)

The blog is connected to GitHub. Every time you push a commit (or Obsidian Git does it automatically), GitHub Actions builds the site and deploys it. Zero manual steps.

**Live URL:** https://jonaschoi0521.github.io

### How it works

```
Write .md in Obsidian
    ↓
Obsidian Git plugin auto-commits + pushes to GitHub (~5 min interval)
    ↓
GitHub Actions triggers on push to main
    ↓
Runs: pip install markdown jinja2 && python3 tools/build.py
    ↓
Deploys site/ to GitHub Pages automatically
    ↓
Live at https://jonaschoi0521.github.io
```

### First-time GitHub setup (one-time only)

If the repo hasn't been connected to GitHub yet:

1. Create the repo at https://github.com/new — name it exactly **`jonaschoi0521.github.io`**, set to **Public**.
2. In the repo Settings → Pages → Source: **Deploy from a branch** → branch: `gh-pages`, folder: `/ (root)`.
3. Push the local repo:
   ```
   git remote add origin https://github.com/jonaschoi0521/jonaschoi0521.github.io.git
   git push -u origin main
   ```
4. Watch the Actions tab at https://github.com/jonaschoi0521/jonaschoi0521.github.io/actions — first build takes ~1 min.

### Obsidian Git setup (one-time only)

1. Open Obsidian. **File → Open Vault → Open Folder as Vault** → select the `blog/` folder.
2. In the vault: Settings → Community Plugins → turn off Restricted Mode → Browse → search **Obsidian Git** → Install → Enable.
3. In Obsidian Git settings:
   - Vault backup interval (minutes): **5**
   - Auto pull interval: **5**
   - Commit message: `auto: {{date}}`
   - Push on backup: **on**
4. Done. Every save auto-commits and pushes within 5 minutes.

### Manual push (if needed)

If you need to deploy immediately without waiting for the timer:

In Obsidian Git: open the command palette (Cmd+P) → **Obsidian Git: Commit all changes** → **Obsidian Git: Push**.

Or from terminal:
```
cd /Users/yuhyunchoi/JONAS-1/projects/career/pipeline/blog
git add posts/ && git commit -m "new post" && git push
```

---

## Fallback: Netlify (manual)

If GitHub Pages ever has issues, the site can still be deployed to Netlify manually.

**Current Netlify URL:** https://yuhyunchoi0521.netlify.app

1. Build locally: `python3 tools/build.py`
2. Drag the `site/` folder onto the existing site's "Deploys" tab at https://app.netlify.com.

---

## Hard rules

- **Never commit `site/`** — it's gitignored. Source of truth is `posts/*.md`.
- **Never commit `.env` or secrets.** The blog has none, keep it that way.
- The GitHub Actions workflow lives at `.github/workflows/deploy.yml` — don't modify it without understanding the full pipeline.

## Notes

- The site is static — no server, no database, no environment variables. Whatever `build.py` produces is exactly what the world sees.
- If a post URL needs to change, the old URL 404s. Add a `404.html` in `static/` if you want a custom not-found page.
- Build time on GitHub Actions is ~30 seconds. The site is live about 1 minute after push.
