---
name: guide-book-publish
description: >
  Publish this repository's research/<NN-theme-slug>/guide/ chapters as private
  reading books with embedded local images. Use when asked to build
  $book-publish-style artifacts for theme guides, all guides, a combined guide
  book, EPUB/MOBI/PDF, Kindle handoff files, or a private handoff directory. Skip
  for generic Markdown books outside this repo; use book-publish there.
  Produces tmp/books/... artifacts via scripts/build_theme_book.py and verifies
  EPUB/MOBI outputs plus embedded images.
argument-hint: "[research/<theme>|--all|--combined] [--formats markdown,epub,pdf,mobi]"
---

# Guide Book Publish

Use this repo-local skill to publish durable `research/*/guide/` chapters into
private reading artifacts. It is a thin repo-specific wrapper around
`scripts/build_theme_book.py`; do not rewrite source guide chapters for a
publishing-only request.

## Routes

Single theme:

```bash
uv run python scripts/build_theme_book.py \
  research/01-harness-engineering \
  --formats markdown,epub,mobi
```

All themes individually plus one combined corpus book:

```bash
uv run python scripts/build_theme_book.py \
  --all \
  --combined \
  --formats markdown,epub,mobi,kindle-epub
```

Combined corpus only:

```bash
uv run python scripts/build_theme_book.py \
  --combined \
  --formats markdown,epub,mobi
```

Unicode-faithful PDF:

```bash
uv run python scripts/build_theme_book.py \
  research/09-production-llm-systems-engineering \
  --formats markdown,pdf
```

Outputs default to `tmp/books/<book-slug>/`. The script copies local guide
images into each generated book folder and rewrites image links to
`assets/<theme-slug>/...`, so generated Markdown links resolve and Pandoc can
embed the images into EPUB/PDF artifacts.

## RSS2Kindle Handoff

If the user asks to populate an rsync remote-transfer handoff folder and has
not already given explicit human approval for that local copy in the current turn, ask once
before copying MOBIs to the user-provided private handoff directory. Do not
commit machine-specific hostnames or absolute local paths. After that explicit
approval, run:

```bash
uv run python scripts/build_theme_book.py \
  --all \
  --combined \
  --formats markdown,epub,mobi \
  --copy-mobi-to "$BOOK_EXPORT_DIR"
```

Equivalent make target:

```bash
make stage-book-exports BOOK_EXPORT_DIR="$BOOK_EXPORT_DIR"
```

Then the user can pull the files from their private remote host with a command
kept outside committed repo files, for example:

```bash
# The human must explicitly approve this remote transfer; the agent must never run it.
rsync -avhP "$REMOTE_HOST:$REMOTE_HANDOFF_DIR/*.mobi" "$LOCAL_HANDOFF_DIR"
```

## Verification

Run the repo validator after script or skill edits:

```bash
uv run python scripts/validate_research.py
```

Verify an EPUB has embedded local images:

```bash
unzip -l tmp/books/01-harness-engineering/01-harness-engineering.epub | \
  rg 'EPUB/(media|assets)/.+\.(png|webp|jpg|jpeg|gif|svg)'
```

Direct EPUBs use `scripts/theme_book_epub.css`: the page and document canvas
have zero book-defined margin, transparent backgrounds, and no forced body
font or foreground color. Kindle or another reader therefore owns its canvas,
theme, font, and spacing controls. Verify the packaged stylesheet rather than
assuming Pandoc used the source CSS:

```bash
unzip -p \
  tmp/books/09-production-llm-systems-engineering/09-production-llm-systems-engineering.epub \
  'EPUB/styles/*.css' | rg '@page|background|font-family|color|margin'
```

Verify MOBI output:

```bash
file tmp/books/01-harness-engineering/01-harness-engineering.mobi
```

PDF publication is intentionally fail-closed. It requires Pandoc, XeLaTeX,
Poppler `pdftotext`, fontconfig, and the exact `DejaVu Sans` plus
`DejaVu Sans Mono` families. The publisher checks both fonts against the
complete generated Markdown corpus, treats Pandoc/LaTeX missing-character
warnings as fatal, and verifies the publication's critical Unicode glyphs in
extracted PDF text. Independently inspect them with:

```bash
pdftotext -enc UTF-8 \
  tmp/books/09-production-llm-systems-engineering/09-production-llm-systems-engineering.pdf \
  - | rg '↘|≈|─'
```

Use `--formats markdown` when only checking concatenation, image rewriting, or
combined-book structure. Use `--formats markdown,epub,mobi` before a Kindle
handoff.

## Guardrails

- Keep generated artifacts under `tmp/books/` unless the user explicitly asks
  for a handoff directory.
- Do not commit generated Markdown, EPUB, PDF, MOBI, or copied image bundles
  from `tmp/books/`.
- Do not run CDP daemon lifecycle commands for this skill.
- Never ship a PDF after an engine, font, corpus-coverage, missing-character,
  or `pdftotext` validation failure. Other successfully generated formats may
  still be reported with the PDF limitation.
- For non-research Markdown books, hand off to the global `book-publish` skill
  instead of broadening this repo-local workflow.

## Common Failure Modes

- `pandoc not found`: install Pandoc or build `--formats markdown` only.
- `xelatex not found`: install XeTeX; the publisher does not fall back to a
  legacy or otherwise undeclared PDF engine.
- Required PDF font unavailable or missing corpus glyphs: install exact
  `DejaVu Sans` and `DejaVu Sans Mono` font families and refresh fontconfig.
- `pdftotext not found`: install Poppler so PDF text round-trip validation can
  run.
- `ebook-convert not found`: install Calibre before requesting MOBI or
  Kindle-EPUB.
- `No .mobi files were produced to copy`: include `mobi` in `--formats`, or use
  `--copy-mobi-to`, which adds MOBI generation automatically.
- Empty EPUB image check: confirm the source guide contains local image links
  and that the referenced files exist under the theme's `assets/` directory.
