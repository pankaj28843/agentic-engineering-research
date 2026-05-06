#!/usr/bin/env python3
"""Post-process captured CDP HTML into clean article Markdown snapshots.

The research workflow deliberately keeps bulky browser artifacts under tmp/.
This script turns those bulky captures into smaller, source-focused Markdown
files that are still kept under tmp/ by default. Those extracted article files
are the substrate for writing theme guides without re-reading nav bars,
script blobs, cookie banners, and SERP noise.

Typical use:

    uv run python scripts/extract_theme_articles.py \
      research/01-harness-engineering \
      --scratch-root tmp/research-web-critical/agentic-engineering-harness-engineering

It reads the theme's sources.json, finds matching html.json files under the
scratch root, runs article-extractor on the captured HTML, writes
article.md files under <scratch-root>/articles/, and emits a manifest.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse, urlunparse

from article_extractor import ExtractionOptions, extract_article

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TMP_ROOT = ROOT / "tmp" / "research-web-critical"


@dataclass
class ExtractedArticle:
    url: str
    title: str
    quality: str
    role: str
    source_html_json: str | None
    article_markdown: str | None
    word_count: int
    success: bool
    warnings: list[str]
    error: str | None = None


def slugify(value: str, *, max_len: int = 90) -> str:
    value = value.lower().strip()
    value = re.sub(r"^https?://", "", value)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return (value[:max_len].strip("-") or "article")


def canonical_url(url: str) -> str:
    """Normalize URLs enough to match source metadata to CDP captures."""
    parsed = urlparse(url.strip())
    scheme = parsed.scheme.lower() or "https"
    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    path = parsed.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    # Drop fragments and common tracking query params while preserving meaningful query keys.
    query_items: list[tuple[str, str]] = []
    tracking = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "fbclid"}
    for key, values in parse_qs(parsed.query, keep_blank_values=True).items():
        if key.lower() in tracking:
            continue
        for value in values:
            query_items.append((key, value))
    query = "&".join(f"{key}={value}" for key, value in sorted(query_items))
    return urlunparse((scheme, netloc, path, "", query, ""))


def unwrap_google_url(url: str) -> str:
    parsed = urlparse(url)
    if "google." not in parsed.netloc:
        return url
    params = parse_qs(parsed.query)
    for key in ("url", "q", "u"):
        if key in params and params[key]:
            return unquote(params[key][0])
    return url


def read_sources(theme_dir: Path) -> list[dict[str, Any]]:
    sources_path = theme_dir / "sources.json"
    if not sources_path.exists():
        raise SystemExit(f"Missing {sources_path}")
    data = json.loads(sources_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit(f"{sources_path} must contain a JSON list")
    return [item for item in data if isinstance(item, dict) and item.get("url")]


def html_payload_from_capture(path: Path) -> tuple[str | None, str | None]:
    """Return (url, html) from a cdp html.json capture."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None, None

    payload = data.get("html") if isinstance(data, dict) else None
    if isinstance(payload, str):
        return None, payload
    if not isinstance(payload, dict):
        return None, None

    url = payload.get("url") if isinstance(payload.get("url"), str) else None
    items = payload.get("items")
    if isinstance(items, list):
        html_parts = [item.get("html", "") for item in items if isinstance(item, dict)]
        html = "\n".join(part for part in html_parts if isinstance(part, str))
        return url, html or None
    html = payload.get("html")
    return url, html if isinstance(html, str) else None


def build_capture_index(scratch_root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in scratch_root.rglob("html.json"):
        url, html = html_payload_from_capture(path)
        if not url or not html:
            continue
        index.setdefault(canonical_url(unwrap_google_url(url)), path)
    return index


def build_explicit_source_index(scratch_root: Path) -> dict[str, Path]:
    """Use tmp/source-index.json when CDP captured a redirected canonical URL.

    Some docs move between hosts (for example docs.anthropic.com to
    platform.claude.com), and some pages redirect from old slugs to new slugs.
    The source-index.json file records the selected source URL and the actual
    markdown capture path, so it is a better match than comparing captured URL
    strings alone.
    """
    source_index = scratch_root / "source-index.json"
    if not source_index.exists():
        return {}
    try:
        data = json.loads(source_index.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(data, list):
        return {}
    mapping: dict[str, Path] = {}
    for item in data:
        if not isinstance(item, dict):
            continue
        url = item.get("url")
        markdown = item.get("markdown")
        if not isinstance(url, str) or not isinstance(markdown, str):
            continue
        markdown_path = (ROOT / markdown).resolve() if not Path(markdown).is_absolute() else Path(markdown)
        html_path = markdown_path.parent / "html.json"
        if html_path.exists():
            mapping[canonical_url(unwrap_google_url(url))] = html_path
    return mapping


def article_header(source: dict[str, Any], result_title: str, word_count: int) -> str:
    title = result_title or str(source.get("title") or "Untitled source")
    url = str(source.get("url"))
    quality = str(source.get("quality") or "unknown")
    role = str(source.get("role") or "")
    generated = datetime.now(timezone.utc).date().isoformat()
    return (
        f"# {title}\n\n"
        f"> Source: [{url}]({url})  \n"
        f"> Quality: `{quality}`  \n"
        f"> Role: {role or 'not labelled'}  \n"
        f"> Extracted words: {word_count}  \n"
        f"> Post-processed with `scripts/extract_theme_articles.py` on {generated}.\n\n"
    )


def extract_one(
    source: dict[str, Any],
    capture_path: Path,
    output_root: Path,
    options: ExtractionOptions,
) -> ExtractedArticle:
    source_url = str(source["url"])
    capture_url, html = html_payload_from_capture(capture_path)
    if not html:
        return ExtractedArticle(
            url=source_url,
            title=str(source.get("title") or ""),
            quality=str(source.get("quality") or ""),
            role=str(source.get("role") or ""),
            source_html_json=str(capture_path),
            article_markdown=None,
            word_count=0,
            success=False,
            warnings=[],
            error="capture contained no HTML payload",
        )

    result = extract_article(html, url=source_url, options=options)
    article_dir = output_root / slugify(source_url)
    article_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = article_dir / "article.md"
    metadata_path = article_dir / "metadata.json"

    if result.success:
        markdown = article_header(source, result.title, result.word_count) + result.markdown.strip() + "\n"
        markdown_path.write_text(markdown, encoding="utf-8")
    metadata = {
        "source": source,
        "capture_url": capture_url,
        "capture_html_json": str(capture_path),
        "result_title": result.title,
        "word_count": result.word_count,
        "success": result.success,
        "warnings": result.warnings,
        "error": result.error,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    return ExtractedArticle(
        url=source_url,
        title=result.title or str(source.get("title") or ""),
        quality=str(source.get("quality") or ""),
        role=str(source.get("role") or ""),
        source_html_json=str(capture_path),
        article_markdown=str(markdown_path) if result.success else None,
        word_count=result.word_count,
        success=result.success,
        warnings=result.warnings,
        error=result.error,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("theme_dir", type=Path, help="Theme directory, e.g. research/01-harness-engineering")
    parser.add_argument(
        "--scratch-root",
        type=Path,
        help="Scratch root containing CDP captures. Defaults to tmp/research-web-critical/<theme-slug>",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        help="Where to write article snapshots. Defaults to <scratch-root>/articles",
    )
    parser.add_argument("--min-words", type=int, default=80, help="Minimum words before warning (default: 80)")
    parser.add_argument("--limit", type=int, help="Debug limit: only process first N sources")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when any source lacks a capture or extraction fails.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    theme_dir = args.theme_dir.resolve()
    if not theme_dir.exists():
        raise SystemExit(f"Theme directory does not exist: {theme_dir}")
    theme_slug = theme_dir.name
    scratch_root = (args.scratch_root or (DEFAULT_TMP_ROOT / theme_slug)).resolve()
    output_root = (args.output_root or (scratch_root / "articles")).resolve()

    if not scratch_root.exists():
        raise SystemExit(f"Scratch root does not exist: {scratch_root}")

    sources = read_sources(theme_dir)
    if args.limit:
        sources = sources[: args.limit]

    capture_index = build_capture_index(scratch_root)
    explicit_index = build_explicit_source_index(scratch_root)
    output_root.mkdir(parents=True, exist_ok=True)
    options = ExtractionOptions(min_word_count=args.min_words, include_images=True, include_code_blocks=True)

    records: list[ExtractedArticle] = []
    missing: list[str] = []
    for source in sources:
        url = str(source["url"])
        key = canonical_url(unwrap_google_url(url))
        capture_path = explicit_index.get(key) or capture_index.get(key)
        if capture_path is None:
            missing.append(url)
            records.append(
                ExtractedArticle(
                    url=url,
                    title=str(source.get("title") or ""),
                    quality=str(source.get("quality") or ""),
                    role=str(source.get("role") or ""),
                    source_html_json=None,
                    article_markdown=None,
                    word_count=0,
                    success=False,
                    warnings=[],
                    error="no matching html.json capture found",
                )
            )
            continue
        records.append(extract_one(source, capture_path, output_root, options))

    manifest = {
        "theme_dir": str(theme_dir),
        "scratch_root": str(scratch_root),
        "output_root": str(output_root),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_sources": len(records),
        "successful": sum(1 for record in records if record.success),
        "failed": sum(1 for record in records if not record.success),
        "records": [asdict(record) for record in records],
    }
    manifest_path = output_root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(
        f"Extracted {manifest['successful']}/{manifest['total_sources']} article snapshots to {output_root}",
        file=sys.stderr,
    )
    if missing:
        print(f"Missing captures: {len(missing)}", file=sys.stderr)
    print(manifest_path)

    if args.strict and manifest["failed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
