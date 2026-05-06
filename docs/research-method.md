# Research Method

The default research posture is skeptical, browser-grounded, and reproducible.

## Source ladder

1. Primary/official sources: docs, specs, engineering blogs by the implementing team, papers.
2. Practitioner reports: production writeups, incident reports, postmortems, detailed implementation blogs.
3. Community signals: HN, Reddit, X/LinkedIn archive, GitHub issues and repositories.
4. SERP snippets: discovery leads only. Do not cite snippets as evidence unless the research question is explicitly about the SERP.

## Deep theme workflow

1. Create a theme slug and scratch root under `tmp/research-web-critical/<slug>/`.
2. Build 2-3 query batches, each with at most 10 Google queries.
3. Run paginated SERP collection with 2-3 result pages per query.
4. Inspect `candidates.tsv` before choosing visit URLs. Pages 2-3 matter because dissent, niche implementation reports, and older foundations often appear there.
5. Add HN and local social signals. Treat social posts as leads unless the linked source is fetched or the thread itself is being analyzed.
6. Extract selected pages as rendered Markdown/HTML into `tmp/`.
7. Post-process captured `html.json` files into clean article Markdown snapshots with `scripts/extract_theme_articles.py`; keep those snapshots under `tmp/`.
8. Synthesize claims for and against; label source quality and incentives.
9. Write the main durable artifact as a chapter-wise, source-linked, ELI5 deep-dive guide under `research/<theme>/guide/`. The briefing is only the executive summary.
10. Commit only durable outputs: guide chapters, credited guide assets, briefing, source index, research log, and machine-readable metadata.

## CDP daemon rule

Only `cdp daemon status --json` is allowed as an unattended daemon lifecycle command. If it is not green/running, ask the user to start or restart the daemon. Do not run daemon start/restart/keepalive/active-probe commands without explicit human approval.

## Google URL hygiene

Google result URLs may contain tracking and encoded metadata parameters such as `ved`, `ei`, `usg`, `sa`, and redirect targets under `url=`, `q=`, or `u=`. Use canonical source URLs from `cdp` candidates or page extraction. Do not preserve Google redirect wrappers or cite protobuf-like tracking parameters as evidence.

## Article extraction post-processing

Use the local `article-extractor` dependency to turn noisy captured HTML into source-focused Markdown before writing guide prose:

```bash
uv run python scripts/extract_theme_articles.py \
  research/01-harness-engineering \
  --scratch-root tmp/research-web-critical/agentic-engineering-harness-engineering
```

The resulting `tmp/.../articles/<source>/article.md` files are scratch reading substrate, not committed source-of-truth artifacts.

## Private reading builds

Build a private Markdown/EPUB bundle from a theme guide with:

```bash
uv run python scripts/build_theme_book.py research/01-harness-engineering --formats markdown,epub
```

Outputs go under `tmp/books/` by default.

## Validation

Run:

```bash
uv run python scripts/validate_research.py
```

The validator checks theme packet completeness, guide depth, source metadata, local markdown links, and `AGENTS.md` guardrails.
