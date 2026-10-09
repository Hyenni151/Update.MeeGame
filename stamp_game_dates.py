#!/usr/bin/env python3
"""Stamp data-added=YYYY-MM-DD on newly added MeeGame cards in index.html.

The script compares the current index.html with the previous Git commit. Existing
cards keep their dates; newly added play URLs receive today's date if they do not
already have data-added. Legacy cards without dates remain legacy/old.
"""
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "index.html"
CARD_RE = re.compile(
    r'(?P<open><article\b(?=[^>]*\bclass=["\'][^"\']*\bgame-card\b[^"\']*["\'])[^>]*>)'
    r'(?P<body>.*?)'
    r'(?P<close></article\s*>)',
    re.IGNORECASE | re.DOTALL,
)
PLAY_RE = re.compile(
    r'<a\b(?=[^>]*\bclass=["\'][^"\']*\bplay-btn\b[^"\']*["\'])[^>]*\bhref=["\']([^"\']+)["\'][^>]*>',
    re.IGNORECASE | re.DOTALL,
)


def canonical_url(url: str) -> str:
    """Normalize enough URL variation to avoid treating trailing slash as new."""
    url = url.strip()
    try:
        p = urlsplit(url)
        host = (p.hostname or "").lower()
        if p.port:
            host += f":{p.port}"
        path = p.path.rstrip("/") or "/"
        return urlunsplit((p.scheme.lower(), host, path, p.query, ""))
    except ValueError:
        return url


def urls_in(html: str) -> set[str]:
    found: set[str] = set()
    for match in CARD_RE.finditer(html):
        play = PLAY_RE.search(match.group(0))
        if play:
            found.add(canonical_url(play.group(1)))
    return found


def previous_html() -> str:
    result = subprocess.run(
        ["git", "show", "HEAD^:index.html"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.stdout if result.returncode == 0 else ""


def main() -> int:
    if not HTML_PATH.exists():
        print("ERROR: index.html not found at repository root", file=sys.stderr)
        return 2

    current = HTML_PATH.read_text(encoding="utf-8")
    previous_urls = urls_in(previous_html())
    today = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).date().isoformat()
    added_count = 0

    def update_card(match: re.Match[str]) -> str:
        nonlocal added_count
        opening = match.group("open")
        body = match.group("body")
        whole = match.group(0)
        play = PLAY_RE.search(whole)
        if not play:
            return whole
        url = canonical_url(play.group(1))
        if url in previous_urls:
            return whole
        # Do not overwrite an explicit date supplied by the editor.
        if re.search(r'\bdata-added=["\']\d{4}-\d{2}-\d{2}["\']', opening, re.I):
            return whole
        opening = opening[:-1].rstrip() + f' data-added="{today}">'
        added_count += 1
        return opening + body + match.group("close")

    updated = CARD_RE.sub(update_card, current)
    if updated != current:
        HTML_PATH.write_text(updated, encoding="utf-8", newline="")
    print(f"Date: {today}")
    print(f"Previously known game links: {len(previous_urls)}")
    print(f"New game cards stamped: {added_count}")
    print(f"Updated index.html: {'yes' if updated != current else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
