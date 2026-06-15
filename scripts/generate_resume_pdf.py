#!/usr/bin/env python3
"""Generate PDF resume from resume-pdf.html with local HTTP server for assets."""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

PROJECT_ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = PROJECT_ROOT / "resume-pdf.html"
PDF_PATH = PROJECT_ROOT / "assets" / "aanchal-kataria-resume.pdf"
PORT = 8765

CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def findChrome() -> str | None:
    for path in CHROME_PATHS:
        if Path(path).exists():
            return path
    return shutil.which("google-chrome") or shutil.which("chromium")


def startServer() -> ThreadingHTTPServer:
    handler = partial(SimpleHTTPRequestHandler, directory=str(PROJECT_ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def generateWithChrome(chromePath: str, pageUrl: str) -> None:
    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    command = [
        chromePath,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=25000",
        f"--print-to-pdf={PDF_PATH}",
        pageUrl,
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)


def main() -> int:
    if not HTML_PATH.exists():
        print(f"Missing source HTML: {HTML_PATH}", file=sys.stderr)
        return 1

    photoPath = PROJECT_ROOT / "assets" / "aanchal-photo.png"
    if not photoPath.exists():
        print(f"Warning: photo not found at {photoPath}", file=sys.stderr)

    chromePath = findChrome()
    if not chromePath:
        print(
            "Chrome/Chromium not found. Open resume-pdf.html in a browser and use Print → Save as PDF.",
            file=sys.stderr,
        )
        return 1

    server = startServer()
    pageUrl = f"http://127.0.0.1:{PORT}/resume-pdf.html"

    try:
        time.sleep(0.5)
        generateWithChrome(chromePath, pageUrl)
    except subprocess.CalledProcessError as error:
        print(error.stderr or error.stdout or str(error), file=sys.stderr)
        return 1
    finally:
        server.shutdown()

    print(f"Generated: {PDF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
