.PHONY: validate extract-harness-articles build-harness-book

validate:
	uv run python scripts/validate_research.py

extract-harness-articles:
	uv run python scripts/extract_theme_articles.py research/01-harness-engineering --scratch-root tmp/research-web-critical/agentic-engineering-harness-engineering

build-harness-book:
	uv run python scripts/build_theme_book.py research/01-harness-engineering --formats markdown,epub
