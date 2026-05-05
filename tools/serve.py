#!/usr/bin/env python3
"""Build the site and serve it locally on http://localhost:8000."""

from __future__ import annotations

import http.server
import os
import socketserver
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"
PORT = 8000


def main() -> int:
    result = subprocess.run([sys.executable, str(ROOT / "tools" / "build.py")])
    if result.returncode != 0:
        return result.returncode

    if not SITE_DIR.exists():
        sys.stderr.write("site/ does not exist after build — aborting.\n")
        return 1

    os.chdir(SITE_DIR)
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"Serving {SITE_DIR.relative_to(ROOT)}/ at http://localhost:{PORT}")
        print("Ctrl-C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
