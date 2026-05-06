#!/usr/bin/env python3
"""Validate the durable research repository structure.

This intentionally uses only the Python standard library so `uv run` can execute
it in a fresh checkout without first installing third-party packages.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_ROOT = ROOT / "research"
REQUIRED_THEME_FILES = ("README.md", "briefing.md", "source-index.md", "research-log.md")

def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_agents() -> None:
    agents = ROOT / "AGENTS.md"
    if not agents.exists():
        fail("AGENTS.md is missing")
    text = agents.read_text(encoding="utf-8")
    required = [
        "cdp daemon status --json",
        "Do **not** run `cdp daemon start`",
        "Do **not** run `cdp daemon restart`",
        "tmp/",
    ]
    for needle in required:
        if needle not in text:
            fail(f"AGENTS.md is missing required instruction: {needle}")


def validate_theme(theme_dir: Path) -> None:
    for name in REQUIRED_THEME_FILES:
        path = theme_dir / name
        if not path.exists():
            fail(f"{theme_dir}: missing {name}")
        if not path.read_text(encoding="utf-8").strip():
            fail(f"{path}: file is empty")

    sources_json = theme_dir / "sources.json"
    if not sources_json.exists():
        fail(f"{theme_dir}: missing sources.json")
    data = json.loads(sources_json.read_text(encoding="utf-8"))
    if not isinstance(data, list) or len(data) < 10:
        fail(f"{sources_json}: expected at least 10 source records")
    seen: set[str] = set()
    for idx, item in enumerate(data, 1):
        if not isinstance(item, dict):
            fail(f"{sources_json}: item {idx} is not an object")
        url = item.get("url")
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            fail(f"{sources_json}: item {idx} has invalid url")
        netloc = urlparse(url).netloc
        if not netloc or "." not in netloc:
            fail(f"{sources_json}: item {idx} url has invalid host: {url}")
        if url in seen:
            fail(f"{sources_json}: duplicate url: {url}")
        seen.add(url)
        if not item.get("quality"):
            fail(f"{sources_json}: item {idx} missing quality label")


def validate_markdown_hygiene() -> None:
    for path in ROOT.rglob("*.md"):
        if ".venv" in path.parts or ".git" in path.parts or "tmp" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                fail(f"{path}:{line_no}: trailing whitespace")
        # Catch common broken local links early. External links are source data and are not fetched.
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = (path.parent / target.split("#", 1)[0]).resolve()
            if target.split("#", 1)[0] and not target_path.exists():
                fail(f"{path}: broken local link: {target}")


def main() -> None:
    validate_agents()
    if not RESEARCH_ROOT.exists():
        fail("research/ directory is missing")
    themes = [p for p in sorted(RESEARCH_ROOT.iterdir()) if p.is_dir()]
    if not themes:
        fail("research/ contains no theme directories")
    for theme in themes:
        validate_theme(theme)
    validate_markdown_hygiene()
    print(f"Validated {len(themes)} research theme(s).")


if __name__ == "__main__":
    main()
