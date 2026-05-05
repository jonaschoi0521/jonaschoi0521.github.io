#!/usr/bin/env python3
"""Build the static blog: posts/YYYY-MM-DD[-slug].md + templates/ + static/ -> site/.

Post format:
  Filename:  posts/2026-05-02.md  or  posts/2026-05-02-second-post.md
  Body:      # Title here
             (blank line, then your post in markdown)
  No frontmatter. Date comes from filename. Title comes from the first # H1.
  If no H1 is present, the formatted date is used as the title.
"""

from __future__ import annotations

import re
import shutil
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import markdown
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError as e:
    sys.stderr.write(
        f"Missing dependency: {e.name}\n"
        "Install with: pip3 install --user markdown jinja2\n"
    )
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "posts"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
SITE_DIR = ROOT / "site"

SITE_TITLE = "Jonas Choi"
SITE_INTRO = (
    "Notes on career, future direction, and how the work I do "
    "can be in service of others."
)
SITE_BYLINE = "Written by Jonas Choi"

FILENAME_RE = re.compile(r"^(\d{4}[-.](\d{2})[-.](\d{2}))(?:[-.](.+))?$")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
SUMMARY_MAX = 180


def extract_title(body: str) -> tuple[str | None, str]:
    """Pull the first `# Heading` out of body. Returns (title, body_without_h1)."""
    m = H1_RE.search(body)
    if not m:
        return None, body
    title = m.group(1).strip()
    new_body = body[: m.start()] + body[m.end():]
    return title, new_body.lstrip("\n")


def excerpt(body: str) -> str:
    """First prose paragraph, plain text, capped at SUMMARY_MAX chars."""
    for chunk in body.strip().split("\n\n"):
        line = chunk.strip()
        if not line or line.startswith(("#", "```", ">", "-", "*", "1.")):
            continue
        line = re.sub(r"\s+", " ", line)
        if len(line) > SUMMARY_MAX:
            line = line[:SUMMARY_MAX].rsplit(" ", 1)[0] + "…"
        return line
    return ""


def load_posts() -> list[dict]:
    md = markdown.Markdown(
        extensions=["fenced_code", "tables", "footnotes", "smarty"],
        output_format="html5",
    )
    posts = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        m = FILENAME_RE.match(path.stem)
        if not m:
            sys.stderr.write(
                f"skip: {path.name} — filename must be YYYY-MM-DD.md "
                "or YYYY-MM-DD-slug.md\n"
            )
            continue
        date_str = m.group(1).replace(".", "-")
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            sys.stderr.write(f"skip: {path.name} — invalid date in filename\n")
            continue

        slug = date_str + (f"-{m.group(4)}" if m.group(4) else "")

        body = path.read_text(encoding="utf-8")
        title, body = extract_title(body)
        date_display = d.strftime("%B %-d, %Y")
        if title is None:
            title = date_display

        md.reset()
        body_html = md.convert(body.strip())

        posts.append({
            "title": title,
            "date": d,
            "date_display": date_display,
            "slug": slug,
            "summary": excerpt(body),
            "body_html": body_html,
        })
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


def render(env: Environment, name: str, **ctx) -> str:
    return env.get_template(name).render(**ctx)


def main() -> int:
    if not POSTS_DIR.exists():
        sys.stderr.write(f"posts/ not found at {POSTS_DIR}\n")
        return 1

    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True)

    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, SITE_DIR / "static")

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    common = {
        "site_title": SITE_TITLE,
        "site_intro": SITE_INTRO,
        "site_byline": SITE_BYLINE,
        "static_prefix": "",
        "year": date.today().year,
        "description": SITE_INTRO,
    }

    posts = load_posts()
    for post in posts:
        html = render(env, "post.html", post=post, **common)
        (SITE_DIR / f"{post['slug']}.html").write_text(html, encoding="utf-8")

    index_html = render(env, "index.html", posts=posts, **common)
    (SITE_DIR / "index.html").write_text(index_html, encoding="utf-8")

    print(f"Built {len(posts)} post{'s' if len(posts) != 1 else ''} → {SITE_DIR.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
