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
argument-hint: "[research/<theme>|--all|--combined] [--formats markdown,epub,mobi]"
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

Outputs default to `tmp/books/<book-slug>/`. The script copies local guide
images into each generated book folder and rewrites image links to
`assets/<theme-slug>/...`, so generated Markdown links resolve and Pandoc can
embed the images into EPUB/PDF artifacts.

## RSS2Kindle Handoff

If the user asks to populate an rsync handoff folder and has not already
approved copying in the current turn, ask once before copying MOBIs to the
user-provided private handoff directory. Do not commit machine-specific hostnames
or absolute local paths. After approval, run:

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

Verify MOBI output:

```bash
file tmp/books/01-harness-engineering/01-harness-engineering.mobi
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
- If PDF fails on image or LaTeX handling, still ship Markdown/EPUB/MOBI and
  report the PDF limitation.
- For non-research Markdown books, hand off to the global `book-publish` skill
  instead of broadening this repo-local workflow.

## Common Failure Modes

- `pandoc not found`: install Pandoc or build `--formats markdown` only.
- `ebook-convert not found`: install Calibre before requesting MOBI or
  Kindle-EPUB.
- `No .mobi files were produced to copy`: include `mobi` in `--formats`, or use
  `--copy-mobi-to`, which adds MOBI generation automatically.
- Empty EPUB image check: confirm the source guide contains local image links
  and that the referenced files exist under the theme's `assets/` directory.
