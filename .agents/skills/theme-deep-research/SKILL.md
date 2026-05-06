---
name: theme-deep-research
description: >
  Build or refresh a thematic research packet under research/<NN-theme-slug>/
  using browser-grounded web research, HN/social signals, docsearch, and a
  skeptical synthesis. Use when adding a new agentic-engineering theme or doing
  a major refresh of an existing theme. Produces README.md, briefing.md,
  source-index.md, research-log.md, and sources.json, then validates with uv.
argument-hint: "<theme name> [--depth medium|deep|exhaustive]"
---

# Theme Deep Research

Use this for durable repo research, not one-off chat answers.

## Guardrails

- CDP daemon lifecycle: the only unattended daemon command allowed is:

  ```bash
  cdp daemon status --json
  ```

  If it is not green/running, ask the user to start or restart the daemon. Do
  not run `cdp daemon start`, `cdp daemon restart`, `cdp daemon keepalive`, or
  `cdp doctor --active-browser-probe` without explicit human approval.
- Put bulky SERP/page artifacts in `tmp/`, never in git.
- Google snippets and AI summaries are leads only. Cite extracted source pages.
- Keep batches human-paced: <=10 Google queries per batch, `serp --parallel 1`.

## Workflow

1. Pick a slug and create scratch space:

   ```bash
   THEME_SLUG="<theme-slug>"
   ROOT="tmp/research-web-critical/$THEME_SLUG"
   mkdir -p "$ROOT"
   ```

2. Confirm daemon status only:

   ```bash
   cdp daemon status --json
   ```

3. Build query batches. Include direct, critical, comparison, production,
   freshness, GitHub, HN, papers/specs, and official docs queries. Keep each
   batch to 10 lines or fewer.

4. Run paginated SERP collection:

   ```bash
   cdp workflow web-research serp \
     --query-file "$ROOT/queries-batch1.txt" \
     --result-pages 3 \
     --serp google \
     --max-candidates 250 \
     --candidate-out "$ROOT/candidates-batch1.json" \
     --out-dir "$ROOT/batch1" \
     --parallel 1 \
     --min-visible-words 50 \
     --min-html-chars 1000 \
     --min-markdown-words 50 \
     --json > "$ROOT/serp-summary-batch1.json"
   ```

5. Inspect `candidates.tsv` before choosing URLs. Pages 2-3 often surface HN
   threads, criticism, GitHub implementations, and security caveats that the top
   page misses.

6. Add practitioner signals:

   ```bash
   curl -Gs "https://hn.algolia.com/api/v1/search" \
     --data-urlencode "query=<theme>" \
     --data-urlencode "tags=story" \
     --data-urlencode "numericFilters=points>10" \
     --data-urlencode "hitsPerPage=50" > "$ROOT/hn-stories.json"

   command -v socli >/dev/null && \
     socli research "<theme>" --since 365d --out "$ROOT/socli-report.md"
   ```

7. Write a deliberate visit list. Prefer canonical source URLs. If Google emits
   redirect wrappers, extract the true target from `url=`, `q=`, or `u=` and
   discard tracking parameters such as `ved`, `ei`, and `usg`.

8. Extract rendered pages in modest chunks. If a batch fails because the daemon
   drops, stop and ask the user to restore it; do not run daemon repair commands.

   ```bash
   cdp workflow web-research extract \
     --url-file "$ROOT/visit-urls.txt" \
     --max-pages 100 \
     --parallel 4 \
     --selector body \
     --out-dir "$ROOT/pages" \
     --min-visible-words 50 \
     --min-html-chars 1000 \
     --min-markdown-words 50 \
     --json > "$ROOT/extract-summary.json"
   ```

9. Create or update `research/<NN-theme-slug>/` with:
   - `README.md` — short entry point and navigation.
   - `briefing.md` — verdict, confidence, evidence for/against, failure modes,
     hidden assumptions, implications.
   - `source-index.md` — source list with quality labels.
   - `research-log.md` — query batches, source-selection notes, tool artifacts,
     HN/social signal summary, limitations.
   - `sources.json` — URL, title/label, quality, role, and date when known.

10. Validate:

    ```bash
    uv run python scripts/validate_research.py
    ```

## Synthesis rubric

Every briefing should answer:

- What is the evidence-weighted verdict?
- Which claims are well-supported, weakly supported, or contested?
- What changed after reading pages 2-3 of Google results?
- Where do HN/social practitioners agree or disagree?
- What are the likely failure modes and incentives of the sources?
- What should the next researcher do?
