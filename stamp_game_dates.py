#!/usr/bin/env python3
"""Stamp data-added on game cards whose play URL is new in this commit.

Requires git history. Existing cards are not assigned fake dates. The script
only stamps cards without data-added whose normalized play URL did not exist
in the previous committed index.html.
"""
from __future__ import annotations
import datetime as dt
import re
import subprocess
from pathlib import Path

INDEX = Path("index.html")
CARD_RE = re.compile(r'<article\b(?P<attrs>[^>]*\bclass\s*=\s*["\'][^"\']*\bgame-card\b[^"\']*["\'][^>]*)>(?P<body>.*?)</article\s*>', re.I | re.S)
HREF_RE = re.compile(r'<a\b(?=[^>]*\bclass\s*=\s*["\'][^"\']*\bplay-btn\b[^"\']*["\'])[^>]*\bhref\s*=\s*(["\'])(.*?)\1', re.I | re.S)
DATE_RE = re.compile(r'\bdata-added\s*=\s*(["\']).*?\1', re.I | re.S)


def normalize_url(url: str) -> str:
    url = url.strip().replace('&amp;', '&')
    url = re.sub(r'#.*$', '', url)
    # Treat a trailing slash as equivalent for host-root links only.
    return url.rstrip('/') if re.match(r'^https?://[^/]+/$', url, re.I) else url


def urls_in(html: str) -> set[str]:
    found = set()
    for m in CARD_RE.finditer(html):
        link = HREF_RE.search(m.group('body'))
        if link:
            found.add(normalize_url(link.group(2)))
    return found


def previous_html() -> str | None:
    for rev in ("HEAD^:index.html", "HEAD~1:index.html"):
        p = subprocess.run(["git", "show", rev], capture_output=True, text=True, encoding="utf-8")
        if p.returncode == 0:
            return p.stdout
    return None


def main() -> None:
    if not INDEX.exists():
        raise SystemExit("Không tìm thấy index.html ở thư mục gốc repository.")
    current = INDEX.read_text(encoding="utf-8")
    previous = previous_html()
    if previous is None:
        print("Không có bản index.html trước đó; giữ nguyên ngày để tránh đánh dấu sai toàn bộ game.")
        return
    old_urls = urls_in(previous)
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    changed = 0

    def patch_card(match: re.Match[str]) -> str:
        nonlocal changed
        attrs, body = match.group('attrs'), match.group('body')
        link = HREF_RE.search(body)
        if not link:
            return match.group(0)
        url = normalize_url(link.group(2))
        # Existing URL means this card is not newly added. If the URL changed
        # since the previous commit, refresh its date even when the card already
        # had a stale data-added attribute.
        if url in old_urls:
            return match.group(0)
        changed += 1
        if DATE_RE.search(attrs):
            attrs = DATE_RE.sub(f'data-added="{today}"', attrs, count=1)
            return '<article' + attrs + '>' + body + '</article>'
        return '<article' + attrs + f' data-added="{today}">' + body + '</article>'

    updated = CARD_RE.sub(patch_card, current)
    if updated != current:
        INDEX.write_text(updated, encoding="utf-8", newline="")
    print(f"Đã gắn ngày {today} cho {changed} game mới.")

if __name__ == '__main__':
    main()
