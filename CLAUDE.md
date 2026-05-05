# Agent Instructions — Blog Project

This project follows the **WAT framework** (Workflows, Agents, Tools) — see `~/TONY-1/CLAUDE.md` for full details.

**Quick reference:**
- Check `tools/` before building anything new
- Don't create or overwrite workflows without asking
- Fix errors → update the workflow → move on
- Local files are disposable; deliverables go to cloud services (the deployed site is the deliverable)

## Project Objective

A personal long-form blog. The user writes about career direction, future goals, deep thinking, and how their majors and work can be used to help others. Sincere voice, slow cadence, no SEO games.

The **writing** is the product. Everything else (build pipeline, design, hosting) exists to get out of the way of the writing.

## Publishing workflow

**Fully automated (default):**
1. Write `posts/YYYY-MM-DD.md` in Obsidian — `# Title` on line 1, body below
2. Save. Obsidian Git auto-pushes to GitHub within ~5 minutes.
3. GitHub Actions builds and deploys automatically → live at **https://yuhyunchoi0521.github.io**

**Manual fallback:**
- Run `python3 tools/build.py` then drag `site/` to Netlify → **https://yuhyunchoi0521.netlify.app**

## Stack — locked

- **Source**: markdown files in `posts/` named `YYYY-MM-DD.md` or `YYYY.MM.DD.md` (dots or dashes both work). No frontmatter. Date from filename. Title from first `# H1` in the body (if absent, formatted date is used).
- **Build**: `tools/build.py` — markdown + Jinja2 → static HTML in `site/`
- **Design**: hand-tuned CSS in `static/style.css`. No frameworks, no Tailwind, no JS.
- **Deploy**: auto via GitHub Actions on every push → **live at https://yuhyunchoi0521.github.io** (see [workflows/deploy.md](workflows/deploy.md)). Netlify (https://yuhyunchoi0521.netlify.app) kept as manual fallback.

## Design — locked

The aesthetic is modeled on **anthropic.com / claude.ai** marketing pages:

- Background `#F5F1EB` (warm cream)
- Body text `#2C2A26` on cream
- Serif throughout: `Charter, "Iowan Old Style", "Source Serif Pro", Georgia, serif`
- Accent `#CC785C` (Anthropic terracotta) for links and rules
- Max content width 640px, line-height 1.7, generous vertical rhythm
- No web fonts — system serif fallback chain
- No images required, no JS

If the user asks for a "redesign," edit `static/style.css` directly. Do not regenerate the design per post.

## Hard Rules

1. **Posts are the user's voice.** Do not draft entire posts unprompted. When asked, edit, copyedit, or restructure — but do not invent the user's opinions, experiences, or career thinking. If a draft needs content the user didn't write, ask.

2. **Markdown is source of truth.** `posts/*.md` is the only thing that matters long-term. The `site/` folder is build output and can be wiped at any time. Never edit files in `site/` by hand.

3. **No tracking, no third-party JS, no analytics in v0.** Don't add Google Analytics, Plausible, fonts.googleapis.com, comment widgets, or any external request. If the user wants stats later, discuss before adding.

4. **No AI-generated filler, no SEO stuffing.** This blog is about sincere thinking. No "10 reasons why" listicles, no keyword optimization, no auto-generated meta descriptions that don't reflect the post.

5. **Token efficiency.** The design lives in CSS once and renders for free for visitors — Claude is not in the loop on pageviews. Never propose a per-post "Claude renders the HTML" architecture; the user was explicitly worried about this and the static-site choice resolves it.

6. **Don't add features the user didn't ask for.** v0 is intentionally minimal: posts, index, no tags, no search, no RSS, no dark mode. Add them only on request.

## Automation Infrastructure

- **GitHub repo:** `yuhyunchoi0521/yuhyunchoi0521.github.io` (public)
- **Live URL:** https://yuhyunchoi0521.github.io
- **Git auth:** SSH (`~/.ssh/id_ed25519` — added to GitHub account)
- **Deploy action:** `peaceiris/actions-gh-pages@v3` → pushes `site/` to `gh-pages` branch
- **Pages source:** Deploy from branch → `gh-pages`, `/ (root)`
- **Obsidian Git:** auto-commit + push every 5 min from the blog vault
- **Full setup notes:** [workflows/github_pages_setup.md](workflows/github_pages_setup.md)

## File Layout

```
posts/                          # markdown source — the writing
templates/                      # Jinja2 HTML templates (base, index, post)
static/                         # style.css and any assets
tools/                          # build.py, new_post.py, serve.py
workflows/                      # SOPs for writing, design tweaks, deploy
.github/workflows/              # GitHub Actions pipeline
site/                           # build output — gitignored, regeneratable
.tmp/                           # disposable scratch
.obsidian/                      # Obsidian vault config + Git plugin
```

## Phase Status

- [x] Phase A — Foundations (scaffold: CLAUDE.md, structure, build pipeline)
- [x] Phase B — First post written and tested
- [x] Phase C — Live at https://yuhyunchoi0521.netlify.app (Netlify, manual)
- [x] Phase D — Fully automated: Obsidian Git → GitHub → GitHub Actions → https://yuhyunchoi0521.github.io
- [ ] Phase E — Optional polish (RSS, tags, dark mode — only if user asks)
