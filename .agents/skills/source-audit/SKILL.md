---
name: source-audit
description: >
  Audit a theme packet's source coverage, citations, and machine-readable
  metadata. Use before committing a new or refreshed research theme. Verifies
  that claims are backed by source labels and that sources.json is usable.
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

3. Confirm `briefing.md` labels source quality and does not cite Google snippets
   as evidence.

4. Confirm `research-log.md` includes:
   - query batches,
   - SERP depth (`--result-pages`),
   - extraction summary,
   - HN/socli or documented absence,
   - limitations.

5. Confirm source URLs are canonical. Remove Google redirect wrappers and
   tracking/protobuf-like metadata parameters such as `ved`, `ei`, and `usg`.

6. Confirm CDP daemon lifecycle commands in the log do not include unattended
   `start`, `restart`, `keepalive`, or `active-browser-probe` unless a human
   approval note is present.

## Output

Append a short audit note to the theme `research-log.md` if you changed
anything. Otherwise, report the validation command and the source coverage in
chat.
