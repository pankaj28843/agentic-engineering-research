---
name: source-audit
description: >
  Audit a theme packet's source coverage, citations, guide depth, and
  machine-readable metadata. Use before committing a new or refreshed research
  theme. Verifies that claims are backed by source labels, the ELI5 guide is
  substantive, and sources.json is usable.
argument-hint: "research/<NN-theme-slug>"
---

# Source Audit

Use this before declaring a research packet ready.

## Checks

1. Validate repository structure:

   ```bash
   uv run python scripts/validate_research.py
   ```

2. Confirm the theme has a source mix:
   - official/primary sources,
   - practitioner implementation reports,
   - community or social signals,
   - at least one skeptical/counter-evidence source for contested themes.

3. Confirm `guide/` is the main reader artifact:
   - numbered chapter files exist,
   - chapters use inline external source links,
   - source diagrams/images used in prose have local copies and credits,
   - the guide is meaty enough to teach the theme, not a thin summary.

4. Confirm `briefing.md` labels source quality and does not cite Google snippets
   as evidence.

5. Confirm `research-log.md` includes:
   - query batches,
   - SERP depth (`--result-pages`),
   - extraction summary,
   - HN/socli or documented absence,
   - limitations.

6. Confirm article-extraction post-processing is documented when CDP captures
   exist, e.g. `scripts/extract_theme_articles.py ...`, and that generated
   article snapshots remain under `tmp/`.

7. Confirm source URLs are canonical. Remove Google redirect wrappers and
   tracking/protobuf-like metadata parameters such as `ved`, `ei`, and `usg`.

8. Confirm CDP daemon lifecycle commands in the log do not include unattended
   `start`, `restart`, `keepalive`, or `active-browser-probe` unless a human
   approval note is present.

## Output

Append a short audit note to the theme `research-log.md` if you changed
anything. Otherwise, report the validation command and the source coverage in
chat.
