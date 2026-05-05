#!/usr/bin/env python3
"""Create a new post file: posts/YYYY-MM-DD.md (or YYYY-MM-DD-slug.md if today exists).

Usage:
  python3 tools/new_post.py             # creates posts/2026-05-02.md
  python3 tools/new_post.py my-thoughts # creates posts/2026-05-02-my-thoughts.md
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "posts"

STUB = "# \n\n"


def main() -> int:
    if not POSTS_DIR.exists():
        POSTS_DIR.mkdir(parents=True)

    today = date.today().isoformat()
    suffix = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    suffix = re.sub(r"[^\w-]", "-", suffix).strip("-").lower()

    filename = f"{today}-{suffix}.md" if suffix else f"{today}.md"
    path = POSTS_DIR / filename

    if path.exists():
        sys.stderr.write(
            f"{path.name} already exists.\n"
            f"Pass a suffix to disambiguate: python3 tools/new_post.py second\n"
        )
        return 1

    path.write_text(STUB, encoding="utf-8")
    print(f"Created {path.relative_to(ROOT)}")
    print(f"Open it and write your # Title on the first line.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
