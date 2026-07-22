BOOK_EXPORT_DIR ?= tmp/book-export

.PHONY: validate extract-harness-articles build-harness-book build-guide-books stage-book-exports

validate:
	uv run python scripts/validate_research.py
	uv run python -m unittest discover -s tests -p 'test_*.py'

extract-harness-articles:
	uv run python scripts/extract_theme_articles.py research/01-harness-engineering --scratch-root tmp/research-web-critical/agentic-engineering-harness-engineering

build-harness-book:
	uv run python scripts/build_theme_book.py research/01-harness-engineering --formats markdown,epub

build-guide-books:
	uv run python scripts/build_theme_book.py --all --combined --formats markdown,epub,mobi

stage-book-exports:
	uv run python scripts/build_theme_book.py --all --combined --formats markdown,epub,mobi --copy-mobi-to "$(BOOK_EXPORT_DIR)"
