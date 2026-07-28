#!/usr/bin/env python3
"""Publish research guide chapters as private reading books.

The repo's durable source of truth remains chapter-wise Markdown under
research/<theme>/guide/. This script builds generated reading artifacts under
tmp/books/ by default:

- one book for each selected theme,
- one combined corpus book when requested,
- Markdown/EPUB/PDF/MOBI/Kindle-EPUB outputs,
- copied local guide images so generated Markdown links resolve and Pandoc can
  embed those images into EPUB/PDF outputs,
- stable internal links between concatenated chapters,
- each theme's searchable source index and small machine-readable guide
  fixtures as publication appendices.
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
PDF_ENGINE = "xelatex"
PDF_MAIN_FONT = "DejaVu Sans"
PDF_MONO_FONT = "DejaVu Sans Mono"
PDF_REQUIRED_GLYPHS = ("↘", "≈", "─")

ALLOWED_FORMATS = {"markdown", "epub", "pdf", "mobi", "kindle-epub"}
FORMAT_ALIASES = {
    "all": {"markdown", "epub", "pdf", "mobi", "kindle-epub"},
    "ebook": {"markdown", "epub", "mobi", "kindle-epub"},
    "ebooks": {"markdown", "epub", "mobi", "kindle-epub"},
}
SUPPORTED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
SUPPORTED_FIXTURE_EXTS = {".json", ".jsonl", ".yaml", ".yml"}

MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(\s+[\"'][^\"']*[\"'])?\)")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(\s+[\"'][^\"']*[\"'])?\)")
HTML_IMAGE_RE = re.compile(r"(<img\b[^>]*\bsrc=[\"'])([^\"']+)([\"'][^>]*>)", re.IGNORECASE)
MISSING_GLYPH_WARNING_RE = re.compile(
    r"(?:missing (?:character|glyph)|glyph[^\n]*missing|"
    r"does not contain[^\n]*(?:character|glyph))",
    re.IGNORECASE,
)


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
    publication_priority = {
        "00-README.md": 0,
        "lab-fixture.md": 1,
    }
    return sorted(
        (path for path in guide_dir.glob("*.md") if path.is_file()),
        key=lambda path: (publication_priority.get(path.name, 2), path.name),
    )


def source_index_file(theme_dir: Path) -> Path | None:
    path = theme_dir / "source-index.md"
    return path if path.is_file() else None


def fixture_files(theme_dir: Path) -> list[Path]:
    """Return small text fixtures that should remain available in the book."""

    fixture_root = theme_dir / "guide" / "fixtures"
    if not fixture_root.exists():
        return []
    return sorted(
        path
        for path in fixture_root.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_FIXTURE_EXTS
    )


def publication_anchor(theme_dir: Path, path: Path) -> str:
    """Return a stable, globally unique Pandoc identifier for one source file."""

    rel = path.resolve().relative_to(theme_dir.resolve()).as_posix()
    without_suffix = rel[: -len(path.suffix)] if path.suffix else rel
    slug = re.sub(r"[^a-z0-9]+", "-", f"{theme_dir.name}-{without_suffix}".lower())
    return f"pub-{slug.strip('-')}"


def publication_anchor_map(spec: BookSpec) -> dict[Path, str]:
    anchors: dict[Path, str] = {}
    used: set[str] = set()
    for theme in spec.themes:
        files = list(chapter_files(theme))
        source_index = source_index_file(theme)
        if source_index is not None:
            files.append(source_index)
        files.extend(fixture_files(theme))
        for path in files:
            anchor = publication_anchor(theme, path)
            if anchor in used:
                raise SystemExit(f"Duplicate publication anchor {anchor}: {path}")
            anchors[path.resolve()] = anchor
            used.add(anchor)
    return anchors


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


def rewrite_local_markdown_links(
    text: str,
    source_document: Path,
    anchors: dict[Path, str],
) -> str:
    """Rewrite included local files to book anchors and unwrap unresolved ones."""

    def replace(match: re.Match[str]) -> str:
        label, ref, title = match.group(1), match.group(2), match.group(3) or ""
        if not should_rewrite_ref(ref):
            return match.group(0)
        target, suffix = resolve_ref(ref, source_document)
        anchor = anchors.get(target)
        if anchor is None:
            return label
        if suffix.startswith("#") and len(suffix) > 1:
            # The target Markdown heading remains in the concatenated document.
            # Preserve its explicit fragment rather than linking to the file's H1.
            anchor = suffix[1:]
        return f"[{label}](#{anchor}{title})"

    return MARKDOWN_LINK_RE.sub(replace, text)


def add_first_heading_anchor(text: str, anchor: str, *, heading: str | None = None) -> str:
    """Attach an explicit ID to the first H1, or create one when absent."""

    pattern = re.compile(r"^#\s+(.+?)(?:\s+\{#[^}]+\})?\s*$", re.MULTILINE)
    match = pattern.search(text)
    if match is None:
        label = heading or "Untitled source"
        return f"# {label} {{#{anchor}}}\n\n{text}"
    label = heading or match.group(1)
    replacement = f"# {label} {{#{anchor}}}"
    return text[: match.start()] + replacement + text[match.end() :]


def source_comment(path: Path) -> str:
    try:
        rendered = path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        rendered = path.resolve().as_posix()
    return rendered


def fixture_fence(path: Path) -> str:
    return "json" if path.suffix.lower() in {".json", ".jsonl"} else "yaml"


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
    anchors = publication_anchor_map(spec)

    for theme_idx, theme in enumerate(spec.themes):
        if spec.combined:
            if theme_idx:
                parts.append("\n\\newpage\n\n")
            theme_anchor = re.sub(r"[^a-z0-9]+", "-", f"pub-theme-{theme.name}".lower()).strip("-")
            parts.append(f"# {theme_title(theme)} {{#{theme_anchor}}}\n\n")
            parts.append(f"<!-- Source theme: {source_comment(theme)} -->\n\n")

        for chapter in chapter_files(theme):
            parts.append(f"\n<!-- Source chapter: {source_comment(chapter)} -->\n\n")
            chapter_text = chapter.read_text(encoding="utf-8").strip() + "\n"
            chapter_text, copied = rewrite_image_links(chapter_text, chapter, theme, spec.output_dir)
            chapter_text = rewrite_local_markdown_links(chapter_text, chapter, anchors)
            chapter_text = add_first_heading_anchor(
                chapter_text,
                anchors[chapter.resolve()],
            )
            copied_images += copied
            parts.append(chapter_text)
            parts.append("\n")

        fixtures = fixture_files(theme)
        if fixtures:
            appendix_anchor = re.sub(
                r"[^a-z0-9]+",
                "-",
                f"pub-{theme.name}-machine-readable-fixtures".lower(),
            ).strip("-")
            parts.append("\n\\newpage\n\n")
            parts.append(f"# Machine-readable fixture appendix {{#{appendix_anchor}}}\n\n")
            parts.append(
                "These versioned files are printed here so the reading artifact "
                "retains the replay contract even when it is offline.\n\n"
            )
            for fixture in fixtures:
                anchor = anchors[fixture.resolve()]
                rel = fixture.relative_to(theme).as_posix()
                parts.append(f"## `{rel}` {{#{anchor}}}\n\n")
                parts.append(f"```{fixture_fence(fixture)}\n")
                parts.append(fixture.read_text(encoding="utf-8").rstrip())
                parts.append("\n```\n\n")

        source_index = source_index_file(theme)
        if source_index is not None:
            parts.append("\n\\newpage\n\n")
            parts.append(f"<!-- Source index: {source_comment(source_index)} -->\n\n")
            source_text = source_index.read_text(encoding="utf-8").strip() + "\n"
            source_text = rewrite_local_markdown_links(source_text, source_index, anchors)
            source_text = add_first_heading_anchor(
                source_text,
                anchors[source_index.resolve()],
                heading=f"Evidence appendix — {theme_title(theme)}",
            )
            parts.append(source_text)
            parts.append("\n")

    markdown_path.write_text("".join(parts), encoding="utf-8")
    return markdown_path, copied_images


def run_command(cmd: list[str]) -> None:
    print("$ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)  # noqa: S603


def run_captured(
    cmd: list[str],
    *,
    echo_output: bool = True,
) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(cmd), flush=True)
    result = subprocess.run(  # noqa: S603
        cmd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if echo_output and result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if echo_output and result.stderr:
        print(
            result.stderr,
            end="" if result.stderr.endswith("\n") else "\n",
            file=sys.stderr,
        )
    return result


def require_executable(name: str, purpose: str) -> str:
    executable = shutil.which(name)
    if not executable:
        raise SystemExit(
            f"{name} not found on PATH; {purpose}. "
            "Build --formats markdown,epub if PDF tooling is unavailable"
        )
    return executable


def parse_fontconfig_charset(raw: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for token in raw.split():
        try:
            if "-" in token:
                start, end = token.split("-", 1)
                ranges.append((int(start, 16), int(end, 16)))
            else:
                codepoint = int(token, 16)
                ranges.append((codepoint, codepoint))
        except ValueError as exc:
            raise SystemExit(f"fontconfig returned an invalid charset token: {token}") from exc
    if not ranges:
        raise SystemExit("fontconfig returned an empty font charset")
    return ranges


def font_supports(codepoint: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= codepoint <= end for start, end in ranges)


def require_font_coverage(
    family: str,
    corpus: str,
    *,
    fc_match: str,
    fc_query: str,
) -> Path:
    match = run_captured(
        [fc_match, "--format=%{family}\t%{file}\\n", family],
        echo_output=False,
    )
    if match.returncode != 0:
        raise SystemExit(f"fontconfig could not resolve required PDF font: {family}")
    first_line = match.stdout.splitlines()[0] if match.stdout.splitlines() else ""
    matched_families, separator, raw_path = first_line.partition("\t")
    family_names = {item.strip() for item in matched_families.split(",")}
    if not separator or family not in family_names:
        replacement = matched_families or "nothing"
        raise SystemExit(
            f"required PDF font {family!r} is unavailable; fontconfig matched {replacement!r}"
        )
    font_path = Path(raw_path)
    if not font_path.is_file():
        raise SystemExit(
            f"required PDF font {family!r} resolved to a missing file: {font_path}"
        )

    query = run_captured(
        [fc_query, "--format=%{charset}\\n", str(font_path)],
        echo_output=False,
    )
    if query.returncode != 0:
        raise SystemExit(f"fontconfig could not inspect required PDF font: {family}")
    ranges = parse_fontconfig_charset(query.stdout)
    codepoints = {
        ord(character)
        for character in corpus
        if character.isprintable() and not character.isspace()
    }
    missing = sorted(
        codepoint for codepoint in codepoints if not font_supports(codepoint, ranges)
    )
    if missing:
        rendered = ", ".join(
            f"U+{codepoint:04X} {chr(codepoint)!r}" for codepoint in missing[:12]
        )
        remainder = len(missing) - 12
        if remainder > 0:
            rendered += f", and {remainder} more"
        raise SystemExit(
            f"required PDF font {family!r} does not cover the publication corpus: "
            f"{rendered}"
        )
    return font_path


def require_pdf_toolchain(markdown_path: Path) -> tuple[str, str]:
    engine = require_executable(
        PDF_ENGINE,
        f"install a Unicode-capable {PDF_ENGINE} engine to build PDF",
    )
    pdftotext = require_executable(
        "pdftotext",
        "install Poppler so generated PDF text can be validated",
    )
    fc_match = require_executable(
        "fc-match",
        "install fontconfig so required PDF fonts can be resolved",
    )
    fc_query = require_executable(
        "fc-query",
        "install fontconfig so required PDF font coverage can be verified",
    )
    corpus = markdown_path.read_text(encoding="utf-8")
    require_font_coverage(
        PDF_MAIN_FONT,
        corpus,
        fc_match=fc_match,
        fc_query=fc_query,
    )
    require_font_coverage(
        PDF_MONO_FONT,
        corpus,
        fc_match=fc_match,
        fc_query=fc_query,
    )
    return engine, pdftotext


def validate_pdf_text(
    pdf_path: Path,
    markdown_path: Path,
    *,
    pdftotext: str,
) -> None:
    result = run_captured(
        [pdftotext, "-enc", "UTF-8", str(pdf_path), "-"],
        echo_output=False,
    )
    if result.returncode != 0:
        pdf_path.unlink(missing_ok=True)
        raise SystemExit(
            f"PDF publication validation failed: pdftotext exited {result.returncode}"
        )
    source = markdown_path.read_text(encoding="utf-8")
    required = [glyph for glyph in PDF_REQUIRED_GLYPHS if glyph in source]
    missing = [glyph for glyph in required if glyph not in result.stdout]
    if missing:
        pdf_path.unlink(missing_ok=True)
        rendered = ", ".join(f"U+{ord(glyph):04X} {glyph!r}" for glyph in missing)
        raise SystemExit(
            "PDF publication validation failed: generated text lost required "
            f"Unicode glyph(s): {rendered}"
        )


def run_pandoc(markdown_path: Path, output_path: Path, *, title: str, author: str) -> None:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise SystemExit("pandoc not found on PATH; install pandoc or build markdown only")
    pdf_toolchain: tuple[str, str] | None = None
    if output_path.suffix.lower() == ".pdf":
        pdf_toolchain = require_pdf_toolchain(markdown_path)
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
    if pdf_toolchain is not None:
        engine, _ = pdf_toolchain
        cmd.extend(
            [
                "--pdf-engine",
                engine,
                "--variable",
                f"mainfont={PDF_MAIN_FONT}",
                "--variable",
                f"monofont={PDF_MONO_FONT}",
            ]
        )
    result = run_captured(cmd)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode,
            cmd,
            output=result.stdout,
            stderr=result.stderr,
        )
    warnings = "\n".join((result.stdout, result.stderr))
    if pdf_toolchain is not None and MISSING_GLYPH_WARNING_RE.search(warnings):
        output_path.unlink(missing_ok=True)
        raise SystemExit(
            "PDF publication failed: Pandoc/LaTeX reported a missing-character "
            "or missing-glyph warning"
        )
    if pdf_toolchain is not None:
        _, pdftotext = pdf_toolchain
        validate_pdf_text(output_path, markdown_path, pdftotext=pdftotext)


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
