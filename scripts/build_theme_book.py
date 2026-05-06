#!/usr/bin/env python3
"""Build a theme guide into a single Markdown file and optional EPUB/PDF.

The repo's durable source of truth remains the chapter-wise Markdown under
research/<theme>/guide/. This script is a thin publishing helper for private
reading: it concatenates chapters in filename order and, when requested, uses
pandoc to produce ebook/print artifacts under tmp/books/ by default.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT / "tmp" / "books"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("theme_dir", type=Path, help="Theme directory, e.g. research/01-harness-engineering")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT, help="Output root (default: tmp/books)")
    parser.add_argument(
        "--formats",
        default="markdown",
        help="Comma-separated formats: markdown,epub,pdf (default: markdown)",
    )
    parser.add_argument("--title", help="Book title override")
    parser.add_argument("--author", default="Agentic Engineering Research", help="Metadata author")
    return parser.parse_args()


def chapter_files(theme_dir: Path) -> list[Path]:
    guide_dir = theme_dir / "guide"
    if not guide_dir.exists():
        raise SystemExit(f"Missing guide directory: {guide_dir}")
    chapters = sorted(path for path in guide_dir.glob("*.md") if path.is_file())
    if not chapters:
        raise SystemExit(f"No chapter files found in {guide_dir}")
    return chapters


def strip_duplicate_h1(text: str, *, first: bool) -> str:
    """Keep chapters intact; only avoid multiple top-level titles if needed later."""
    return text.strip() + "\n"


def build_markdown(theme_dir: Path, output_dir: Path, title: str, author: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / f"{theme_dir.name}.md"
    generated = datetime.now(timezone.utc).date().isoformat()
    parts = [
        f"% {title}\n",
        f"% {author}\n",
        f"% {generated}\n\n",
        "---\n",
        f"title: {json.dumps(title, ensure_ascii=False)}\n",
        f"author: {json.dumps(author, ensure_ascii=False)}\n",
        "lang: en-US\n",
        "---\n\n",
    ]
    for idx, chapter in enumerate(chapter_files(theme_dir)):
        rel = chapter.relative_to(theme_dir)
        parts.append(f"\n<!-- Source chapter: {rel} -->\n\n")
        parts.append(strip_duplicate_h1(chapter.read_text(encoding="utf-8"), first=(idx == 0)))
        parts.append("\n")
    out.write_text("".join(parts), encoding="utf-8")
    return out


def run_pandoc(markdown_path: Path, output_path: Path, *, title: str, author: str, theme_dir: Path) -> None:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise SystemExit("pandoc not found on PATH; install pandoc or build markdown only")
    cmd = [
        pandoc,
        str(markdown_path),
        "--standalone",
        "--toc",
        "--metadata",
        f"title={title}",
        "--metadata",
        f"author={author}",
        "--resource-path",
        f"{markdown_path.parent}:{theme_dir / 'guide'}:{theme_dir}",
        "-o",
        str(output_path),
    ]
    subprocess.run(cmd, check=True)  # noqa: S603


def main() -> int:
    args = parse_args()
    theme_dir = args.theme_dir.resolve()
    if not theme_dir.exists():
        raise SystemExit(f"Theme directory does not exist: {theme_dir}")
    formats = {item.strip().lower() for item in args.formats.split(",") if item.strip()}
    unknown = formats - {"markdown", "epub", "pdf"}
    if unknown:
        raise SystemExit(f"Unknown formats: {', '.join(sorted(unknown))}")

    title = args.title or (theme_dir / "README.md").read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
    output_dir = args.output_root.resolve() / theme_dir.name
    markdown_path = build_markdown(theme_dir, output_dir, title, args.author)
    print(markdown_path)

    if "epub" in formats:
        epub_path = output_dir / f"{theme_dir.name}.epub"
        run_pandoc(markdown_path, epub_path, title=title, author=args.author, theme_dir=theme_dir)
        print(epub_path)
    if "pdf" in formats:
        pdf_path = output_dir / f"{theme_dir.name}.pdf"
        run_pandoc(markdown_path, pdf_path, title=title, author=args.author, theme_dir=theme_dir)
        print(pdf_path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"pandoc failed with exit code {exc.returncode}", file=sys.stderr)
        raise SystemExit(exc.returncode)
