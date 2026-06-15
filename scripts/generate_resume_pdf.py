#!/usr/bin/env python3
"""Generate PDF resumes from HTML sources with local HTTP server for assets."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PORT = 8765
LOCAL_CONFIG_PATH = PROJECT_ROOT / ".resume-local.json"
WEBSITE_HTML = PROJECT_ROOT / "resume-pdf.html"
JOB_HTML = PROJECT_ROOT / "resume-pdf-job-application.html"
WEBSITE_PDF = PROJECT_ROOT / "assets" / "aanchal-kataria-resume.pdf"
JOB_PDF = PROJECT_ROOT / "assets" / "aanchal-kataria-resume-job-application.pdf"
CONTACT_MARKER = "<h2>Contact</h2>"

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


def loadPhoneNumber() -> str:
    if not LOCAL_CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Missing {LOCAL_CONFIG_PATH.name}. Copy .resume-local.json.example and set your phone number."
        )

    config = json.loads(LOCAL_CONFIG_PATH.read_text(encoding="utf-8"))
    phone = str(config.get("phone", "")).strip()
    if not phone or "X" in phone:
        raise ValueError(
            f"Set a valid phone number in {LOCAL_CONFIG_PATH.name} before generating the job application PDF."
        )
    return phone


def buildJobApplicationHtml() -> None:
    phone = loadPhoneNumber()
    source = WEBSITE_HTML.read_text(encoding="utf-8")
    if CONTACT_MARKER not in source:
        raise ValueError(f"Contact section marker not found in {WEBSITE_HTML.name}")

    phoneLine = f'        <div class="contact-item"><strong>Phone</strong>{phone}</div>\n'
    jobHtml = source.replace(CONTACT_MARKER, f"{CONTACT_MARKER}\n{phoneLine}", 1)
    JOB_HTML.write_text(jobHtml, encoding="utf-8")


def startServer() -> ThreadingHTTPServer:
    handler = partial(SimpleHTTPRequestHandler, directory=str(PROJECT_ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def generateWithChrome(chromePath: str, pageUrl: str, pdfPath: Path) -> None:
    pdfPath.parent.mkdir(parents=True, exist_ok=True)
    command = [
        chromePath,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=25000",
        f"--print-to-pdf={pdfPath}",
        pageUrl,
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)


def main() -> int:
    if not WEBSITE_HTML.exists():
        print(f"Missing source HTML: {WEBSITE_HTML}", file=sys.stderr)
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

    try:
        buildJobApplicationHtml()
    except (FileNotFoundError, ValueError) as error:
        print(f"Warning: {error}", file=sys.stderr)
        print("Skipping job application PDF.", file=sys.stderr)

    variants = [
        (WEBSITE_HTML, WEBSITE_PDF, "Website resume (no phone)"),
        (JOB_HTML, JOB_PDF, "Job application resume (with phone)"),
    ]

    server = startServer()

    try:
        time.sleep(0.5)
        for htmlPath, pdfPath, label in variants:
            if not htmlPath.exists():
                continue
            pageUrl = f"http://127.0.0.1:{PORT}/{htmlPath.name}"
            generateWithChrome(chromePath, pageUrl, pdfPath)
            print(f"Generated ({label}): {pdfPath}")
    except subprocess.CalledProcessError as error:
        print(error.stderr or error.stdout or str(error), file=sys.stderr)
        return 1
    finally:
        server.shutdown()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
