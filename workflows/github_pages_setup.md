# Setup — Obsidian → GitHub Pages Automation

## What this is

Documents the full pipeline that was built and the lessons learned setting it up.
If anything breaks or needs to be rebuilt, this is the reference.

## How the pipeline works

```
Write .md in Obsidian (posts/ folder)
    ↓
Obsidian Git auto-commits + pushes to GitHub every 5 minutes
    ↓
GitHub Actions triggers on push to main (.github/workflows/deploy.yml)
    ↓
Ubuntu runner: pip install markdown jinja2 → python3 tools/build.py
    ↓
peaceiris/actions-gh-pages@v3 pushes site/ to gh-pages branch
    ↓
GitHub Pages serves gh-pages branch → https://jonaschoi0521.github.io
```

## What's installed and configured

**GitHub:**
- Repo: `jonaschoi0521/jonaschoi0521.github.io` (public)
- Pages: Settings → Pages → Source: **Deploy from a branch** → branch: `gh-pages`, folder: `/ (root)`
- SSH key: `~/.ssh/id_ed25519` added to https://github.com/settings/ssh (title: MacBook)

**Git remote:**
- Protocol: SSH (not HTTPS)
- Remote: `git@github.com:jonaschoi0521/jonaschoi0521.github.io.git`
- Why SSH: HTTPS personal access tokens require `workflow` scope to push Actions files, which caused repeated auth failures during setup.

**GitHub Actions:**
- Workflow file: `.github/workflows/deploy.yml`
- Deploy action: `peaceiris/actions-gh-pages@v3` (pushes to `gh-pages` branch)
- Permission needed: `contents: write`

**Obsidian:**
- Vault: the blog folder itself (`/projects/career/pipeline/blog/`)
- Plugin: Obsidian Git (v2.38.2), installed manually at `.obsidian/plugins/obsidian-git/`
- Settings: auto commit and sync interval = 5 min, auto pull interval = 5 min

## Key lessons learned

**Use `peaceiris/actions-gh-pages@v3`, not `actions/deploy-pages@v4`.**
The newer `actions/deploy-pages@v4` approach (with `actions/upload-pages-artifact`) returned a genuine 404 on a new `username.github.io` repo even when all workflow steps showed green. Root cause unclear — likely a GitHub environment/CDN propagation issue with new repos. `peaceiris/actions-gh-pages@v3` pushes directly to a `gh-pages` branch, which is simpler and worked immediately.

**Use SSH auth for git remotes, not HTTPS tokens.**
GitHub personal access tokens require the `workflow` scope to push `.github/workflows/` files. Classic tokens can have this scope added, but the macOS keychain caches old tokens and doesn't prompt for new ones, making it hard to rotate. SSH keys bypass this entirely and are the right long-term solution.

**Obsidian Git can't be found via Browse if the plugin CDN is slow.**
Install manually: download `main.js`, `manifest.json`, `styles.css` from the GitHub releases page and drop them into `.obsidian/plugins/obsidian-git/`. Restart Obsidian.

## Verifying the pipeline works

1. Write or edit a file in `posts/` in Obsidian
2. Wait ~5 minutes
3. Check https://github.com/jonaschoi0521/jonaschoi0521.github.io/actions — should show a green run
4. Visit https://jonaschoi0521.github.io — post should be live

Or trigger immediately: Obsidian command palette (Cmd+P) → **Git: Commit all changes** → **Git: Push**

## If something breaks

**Site shows 404:**
- Check GitHub Actions tab — is the latest run green?
- Check repo Settings → Pages — source must be "Deploy from branch" → `gh-pages`
- Check that the `gh-pages` branch exists in the repo

**Push fails (SSH error):**
- Run `ssh -T git@github.com` — if it fails, the SSH key may have been removed from GitHub
- Re-add `~/.ssh/id_ed25519.pub` at https://github.com/settings/ssh

**Obsidian Git stopped pushing:**
- Check Settings → Git in Obsidian — confirm interval is still 5
- Try manual push via command palette
- Check that the git remote is still correct: `git remote -v` in the blog folder

**Build fails on GitHub Actions:**
- Check the Actions log for the error
- Most likely a Python dependency issue — confirm `pip install markdown jinja2` succeeds
- Run `python3 tools/build.py` locally to reproduce
