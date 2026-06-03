#!/usr/bin/env python3
"""Publish research guide chapters as private reading books.

The repo's durable source of truth remains chapter-wise Markdown under
research/<theme>/guide/. This script builds generated reading artifacts under
tmp/books/ by default:

- one book for each selected theme,
- one combined corpus book when requested,
- Markdown/EPUB/PDF/MOBI/Kindle-EPUB outputs,
- copied local guide images so generated Markdown links resolve and Pandoc can
  embed those images into EPUB/PDF outputs.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_ROOT = ROOT / "research"
DEFAULT_OUTPUT_ROOT = ROOT / "tmp" / "books"
DEFAULT_COMBINED_SLUG = "agentic-engineering-guides"
DEFAULT_COMBINED_TITLE = "Agentic Engineering Research Guides"
DEFAULT_AUTHOR = "Agentic Engineering Research"

ALLOWED_FORMATS = {"markdown", "epub", "pdf", "mobi", "kindle-epub"}
FORMAT_ALIASES = {
    "all": {"markdown", "epub", "pdf", "mobi", "kindle-epub"},
    "ebook": {"markdown", "epub", "mobi", "kindle-epub"},
    "ebooks": {"markdown", "epub", "mobi", "kindle-epub"},
}
SUPPORTED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}

MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(\s+[\"'][^\"']*[\"'])?\)")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(\s+[\"'][^\"']*[\"'])?\)")
HTML_IMAGE_RE = re.compile(r"(<img\b[^>]*\bsrc=[\"'])([^\"']+)([\"'][^>]*>)", re.IGNORECASE)


@dataclass(frozen=True)
class BookSpec:
    slug: str
    title: str
    themes: tuple[Path, ...]
    output_dir: Path
    combined: bool = False


@dataclass
class BuildResult:
    spec: BookSpec
    produced: list[Path]
    markdown_path: Path
    copied_images: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "theme_dirs",
        nargs="*",
        type=Path,
        help="Theme directories, e.g. research/01-harness-engineering",
    )
    parser.add_argument(
        "--all",
        dest="all_themes",
        action="store_true",
        help="Build one individual book for every research/* theme.",
    )
    parser.add_argument(
        "--combined",
        action="store_true",
        help="Also build one combined book from the selected themes. With no theme dirs, combines all themes.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Output root (default: tmp/books).",
    )
    parser.add_argument(
        "--formats",
        default="markdown",
        help=(
            "Comma-separated formats: markdown,epub,pdf,mobi,kindle-epub. "
            "Aliases: ebook,ebooks,all. Default: markdown."
        ),
    )
    parser.add_argument("--title", help="Title override when building exactly one individual theme.")
    parser.add_argument("--combined-title", default=DEFAULT_COMBINED_TITLE, help="Combined book title.")
    parser.add_argument("--combined-slug", default=DEFAULT_COMBINED_SLUG, help="Combined output slug.")
    parser.add_argument("--author", default=DEFAULT_AUTHOR, help="Metadata author.")
    parser.add_argument(
        "--copy-mobi-to",
        type=Path,
        help="Copy generated .mobi files to an explicit handoff directory.",
    )
    return parser.parse_args()


def parse_formats(raw: str, *, copy_mobi_to: Path | None) -> set[str]:
    formats: set[str] = set()
    for item in (part.strip().lower() for part in raw.split(",")):
        if not item:
            continue
        if item in FORMAT_ALIASES:
            formats.update(FORMAT_ALIASES[item])
        else:
            formats.add(item)

    if not formats:
        raise SystemExit("No formats requested.")

    unknown = formats - ALLOWED_FORMATS
    if unknown:
        allowed = ", ".join(sorted(ALLOWED_FORMATS | set(FORMAT_ALIASES)))
        raise SystemExit(f"Unknown formats: {', '.join(sorted(unknown))}. Allowed: {allowed}")

    if copy_mobi_to is not None:
        formats.add("mobi")

    return formats


def all_theme_dirs() -> list[Path]:
    if not RESEARCH_ROOT.exists():
        raise SystemExit(f"Missing research root: {RESEARCH_ROOT}")
    themes = [path.resolve() for path in sorted(RESEARCH_ROOT.iterdir()) if path.is_dir()]
    if not themes:
        raise SystemExit(f"No theme directories found under {RESEARCH_ROOT}")
    return themes


def dedupe(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    out: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            out.append(resolved)
            seen.add(resolved)
    return out


def validate_theme_dir(theme_dir: Path) -> Path:
    theme_dir = theme_dir.resolve()
    if not theme_dir.exists():
        raise SystemExit(f"Theme directory does not exist: {theme_dir}")
    guide_dir = theme_dir / "guide"
    if not guide_dir.exists():
        raise SystemExit(f"Missing guide directory: {guide_dir}")
    if not chapter_files(theme_dir):
        raise SystemExit(f"No chapter files found in {guide_dir}")
    return theme_dir


def selected_theme_dirs(args: argparse.Namespace) -> list[Path]:
    if args.all_themes:
        return all_theme_dirs()
    if args.theme_dirs:
        return dedupe([validate_theme_dir(path) for path in args.theme_dirs])
    if args.combined:
        return all_theme_dirs()
    raise SystemExit("Pass one or more theme dirs, --all, or --combined.")


def theme_title(theme_dir: Path) -> str:
    readme = theme_dir / "README.md"
    if readme.exists():
        for line in readme.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return theme_dir.name.replace("-", " ").title()


def chapter_files(theme_dir: Path) -> list[Path]:
    guide_dir = theme_dir / "guide"
    if not guide_dir.exists():
        return []
    return sorted(path for path in guide_dir.glob("*.md") if path.is_file())


def build_specs(args: argparse.Namespace) -> list[BookSpec]:
    output_root = args.output_root.expanduser().resolve()
    themes = selected_theme_dirs(args)
    specs: list[BookSpec] = []

    individual_themes: list[Path] = []
    if args.all_themes:
        individual_themes = themes
    elif args.theme_dirs:
        individual_themes = themes

    for theme in individual_themes:
        title = args.title if args.title and len(individual_themes) == 1 else theme_title(theme)
        specs.append(
            BookSpec(
                slug=theme.name,
                title=title,
                themes=(theme,),
                output_dir=output_root / theme.name,
                combined=False,
            )
        )

    if args.combined:
        combined_title = args.title if args.title and not individual_themes else args.combined_title
        specs.append(
            BookSpec(
                slug=args.combined_slug,
                title=combined_title,
                themes=tuple(themes),
                output_dir=output_root / args.combined_slug,
                combined=True,
            )
        )

    if not specs:
        raise SystemExit("No books selected. Pass a theme dir, --all, or --combined.")
    return specs


def local_image_destination(image_path: Path, theme_dir: Path, output_dir: Path) -> tuple[Path, str]:
    image_path = image_path.resolve()
    try:
        rel = image_path.relative_to(theme_dir.resolve())
    except ValueError:
        rel = Path(image_path.name)

    rel_parts = list(rel.parts)
    if rel_parts and rel_parts[0] == "assets":
        rel_parts = rel_parts[1:]
    if not rel_parts:
        rel_parts = [image_path.name]

    dest_rel = Path("assets") / theme_dir.name / Path(*rel_parts)
    return output_dir / dest_rel, dest_rel.as_posix()


def should_rewrite_ref(ref: str) -> bool:
    lowered = ref.lower()
    return not lowered.startswith(("http://", "https://", "data:", "mailto:", "#"))


def resolve_ref(ref: str, chapter: Path) -> tuple[Path, str]:
    suffix = ""
    clean_ref = ref
    for marker in ("#", "?"):
        if marker in clean_ref:
            clean_ref, rest = clean_ref.split(marker, 1)
            suffix = marker + rest
            break
    return (chapter.parent / clean_ref).resolve(), suffix


def copy_local_image(ref: str, chapter: Path, theme_dir: Path, output_dir: Path) -> str | None:
    if not should_rewrite_ref(ref):
        return None
    source, suffix = resolve_ref(ref, chapter)
    if not source.exists() or source.suffix.lower() not in SUPPORTED_IMAGE_EXTS:
        return None

    dest, rewritten = local_image_destination(source, theme_dir, output_dir)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists() or source.stat().st_mtime_ns > dest.stat().st_mtime_ns:
        shutil.copy2(source, dest)
    return rewritten + suffix


def rewrite_image_links(text: str, chapter: Path, theme_dir: Path, output_dir: Path) -> tuple[str, int]:
    copied = 0

    def replace_markdown(match: re.Match[str]) -> str:
        nonlocal copied
        alt, ref, title = match.group(1), match.group(2), match.group(3) or ""
        rewritten = copy_local_image(ref, chapter, theme_dir, output_dir)
        if rewritten is None:
            return match.group(0)
        copied += 1
        return f"![{alt}]({rewritten}{title})"

    def replace_html(match: re.Match[str]) -> str:
        nonlocal copied
        prefix, ref, suffix = match.group(1), match.group(2), match.group(3)
        rewritten = copy_local_image(ref, chapter, theme_dir, output_dir)
        if rewritten is None:
            return match.group(0)
        copied += 1
        return f"{prefix}{rewritten}{suffix}"

    text = MARKDOWN_IMAGE_RE.sub(replace_markdown, text)
    text = HTML_IMAGE_RE.sub(replace_html, text)
    return text, copied


def unwrap_local_markdown_links(text: str) -> str:
    """Drop generated-book links to source-local files.

    Theme guide indexes often link to sibling chapter files such as
    01-introduction.md and ../sources.json. After we concatenate chapters into
    one book, those links point at files that are not present in the EPUB, and
    Calibre reports them as missing resources. The text remains useful, so keep
    the label and remove only the generated link target.
    """

    def replace(match: re.Match[str]) -> str:
        label, ref = match.group(1), match.group(2)
        if not should_rewrite_ref(ref):
            return match.group(0)
        target = ref.split("#", 1)[0].split("?", 1)[0]
        if target:
            return label
        return match.group(0)

    return MARKDOWN_LINK_RE.sub(replace, text)


def build_markdown(spec: BookSpec, author: str) -> tuple[Path, int]:
    spec.output_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = spec.output_dir / "assets"
    if assets_dir.exists():
        shutil.rmtree(assets_dir)

    markdown_path = spec.output_dir / f"{spec.slug}.md"
    generated = datetime.now(timezone.utc).date().isoformat()
    parts = [
        f"% {spec.title}\n",
        f"% {author}\n",
        f"% {generated}\n\n",
        "---\n",
        f"title: {json.dumps(spec.title, ensure_ascii=False)}\n",
        f"author: {json.dumps(author, ensure_ascii=False)}\n",
        "lang: en-US\n",
        "---\n\n",
    ]
    copied_images = 0

    for theme_idx, theme in enumerate(spec.themes):
        if spec.combined:
            if theme_idx:
                parts.append("\n\\newpage\n\n")
            parts.append(f"# {theme_title(theme)}\n\n")
            parts.append(f"<!-- Source theme: {theme.relative_to(ROOT)} -->\n\n")

        for chapter in chapter_files(theme):
            rel = chapter.relative_to(ROOT)
            parts.append(f"\n<!-- Source chapter: {rel} -->\n\n")
            chapter_text = chapter.read_text(encoding="utf-8").strip() + "\n"
            chapter_text, copied = rewrite_image_links(chapter_text, chapter, theme, spec.output_dir)
            chapter_text = unwrap_local_markdown_links(chapter_text)
            copied_images += copied
            parts.append(chapter_text)
            parts.append("\n")

    markdown_path.write_text("".join(parts), encoding="utf-8")
    return markdown_path, copied_images


def run_command(cmd: list[str]) -> None:
    print("$ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)  # noqa: S603


def run_pandoc(markdown_path: Path, output_path: Path, *, title: str, author: str) -> None:
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
        f"{markdown_path.parent}:{ROOT}",
        "-o",
        str(output_path),
    ]
    run_command(cmd)


def run_ebook_convert(source: Path, output_path: Path) -> None:
    ebook_convert = shutil.which("ebook-convert")
    if not ebook_convert:
        raise SystemExit("ebook-convert not found on PATH; install Calibre for MOBI/Kindle EPUB")
    run_command([ebook_convert, str(source), str(output_path)])


def build_book(spec: BookSpec, formats: set[str], author: str) -> BuildResult:
    print(f"\n=== Building {spec.slug} ===", flush=True)
    markdown_path, copied_images = build_markdown(spec, author)
    produced: list[Path] = []
    if "markdown" in formats:
        produced.append(markdown_path)

    needs_epub = bool({"epub", "mobi", "kindle-epub"} & formats)
    epub_path = spec.output_dir / f"{spec.slug}.epub"
    if needs_epub:
        run_pandoc(markdown_path, epub_path, title=spec.title, author=author)
        produced.append(epub_path)

    mobi_path = spec.output_dir / f"{spec.slug}.mobi"
    if "mobi" in formats:
        run_ebook_convert(epub_path, mobi_path)
        produced.append(mobi_path)

    kindle_epub_path = spec.output_dir / f"{spec.slug}.kindle.epub"
    if "kindle-epub" in formats:
        source = mobi_path if mobi_path.exists() else epub_path
        run_ebook_convert(source, kindle_epub_path)
        produced.append(kindle_epub_path)

    if "pdf" in formats:
        pdf_path = spec.output_dir / f"{spec.slug}.pdf"
        run_pandoc(markdown_path, pdf_path, title=spec.title, author=author)
        produced.append(pdf_path)

    return BuildResult(
        spec=spec,
        produced=produced,
        markdown_path=markdown_path,
        copied_images=copied_images,
    )


def copy_mobis(results: list[BuildResult], destination: Path) -> list[Path]:
    destination = destination.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for result in results:
        mobi_path = result.spec.output_dir / f"{result.spec.slug}.mobi"
        if not mobi_path.exists():
            continue
        target = destination / mobi_path.name
        shutil.copy2(mobi_path, target)
        copied.append(target)
    if not copied:
        raise SystemExit("No .mobi files were produced to copy.")
    return copied


def size_str(path: Path) -> str:
    return f"{path.stat().st_size / 1024:,.0f} KB" if path.exists() else "missing"


def main() -> int:
    args = parse_args()
    formats = parse_formats(args.formats, copy_mobi_to=args.copy_mobi_to)
    specs = build_specs(args)

    results: list[BuildResult] = []
    try:
        for spec in specs:
            results.append(build_book(spec, formats, args.author))
    except subprocess.CalledProcessError as exc:
        print(f"Command failed with exit code {exc.returncode}", file=sys.stderr)
        return exc.returncode

    copied_mobis: list[Path] = []
    if args.copy_mobi_to:
        copied_mobis = copy_mobis(results, args.copy_mobi_to)

    print("\n=== build_theme_book summary ===")
    for result in results:
        print(f"{result.spec.slug}:")
        print(f"  markdown: {result.markdown_path}")
        print(f"  copied image reference(s): {result.copied_images}")
        for path in result.produced:
            print(f"  - {path} ({size_str(path)})")
    if copied_mobis:
        print("Copied MOBI files:")
        for path in copied_mobis:
            print(f"  - {path} ({size_str(path)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
