---
name: theme-deep-research
description: >
  Build or refresh a thematic research packet under research/<NN-theme-slug>/
  using browser-grounded web research, HN/social signals, docsearch, article
  extraction post-processing, skeptical synthesis, and a book-like ELI5 guide.
  Use when adding a new agentic-engineering theme or doing a major refresh of an
  existing theme. Produces README.md, guide/ chapters, briefing.md,
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
- Use `cdp --browser-mode headed` for every live web read, including Hacker
  News. Do not use direct HTTP or headless browser fallbacks.
- Google snippets and AI summaries are leads only. Cite extracted source pages.
- Use at most five reviewed research passes. A pass contains one to three
  deliberate query units and begins with one Google results page per query.
  Never pre-plan the next unit or pass before reviewing the current artifacts.
- Stop the Google workflow on the first consent, CAPTCHA, authentication,
  unusual-traffic, or bot-check page. Do not switch engines or continue
  scheduling around a challenge.
- Keep PDF acquisition and conversion as two explicit steps. Acquire the exact
  source with headed CDP and `click --wait-download`, then run
  `cdp workflow pdf-to-markdown <local-pdf>` on the downloaded local file.
  The native workflow reads only an existing embedded text layer and never
  invokes OCR. Treat `text_layer_missing` with `data.reason=ocr_required` as a
  stop/alternate-source decision, not permission to add hidden OCR.

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

3. Choose evidence horizons that fit the topic. Usually pair an evergreen query
   with a justified recent or longer-window query when change over time matters.
   Six months is not a universal default: standards and foundational papers may
   need all-time coverage, while fast-moving product behavior may warrant a
   shorter window and production lessons may need several years. Record the
   reason for every date window in `research-log.md`.

   A query unit is one line in the query file: either an all-time query or a
   query plus a literal tab and Google `tbs` filter. Use only one to three units
   in a pass. Cover direct, critical, production, comparison, paper/spec,
   official-documentation, and practitioner angles across the passes rather
   than front-loading a large batch.

4. Run page-one Google collection for the current pass:

   ```bash
   PASS_ID="01-foundations"
   PASS_ROOT="$ROOT/pass-$PASS_ID"
   mkdir -p "$PASS_ROOT/page-1"

   # One to three reviewed query units. Add a tab-separated tbs filter only
   # when the topic-fit horizon chosen above calls for it.
   printf '%s\n' \
     '<evergreen query>' \
     > "$PASS_ROOT/queries.txt"
   printf '%s\t%s\n' \
     '<windowed query>' \
     'cdr:1,cd_min:<MM/DD/YYYY>,cd_max:<MM/DD/YYYY>' \
     >> "$PASS_ROOT/queries.txt"

   cdp --browser-mode headed workflow web-research serp \
     --query-file "$PASS_ROOT/queries.txt" \
     --serp google \
     --fallback-serp none \
     --parallel 1 \
     --navigation-delay 30s \
     --result-pages 1 \
     --fast-fail-blocked \
     --blocked-failure-threshold 1 \
     --progress stderr \
     --max-candidates 100 \
     --candidate-out "$PASS_ROOT/page-1/candidates.json" \
     --out-dir "$PASS_ROOT/page-1" \
     --min-visible-words 50 \
     --min-html-chars 1000 \
     --min-markdown-words 50 \
     --wait 15s \
     --settle 2s \
     --json > "$PASS_ROOT/page-1/summary.json"
   ```

   Within one invocation, `--navigation-delay 30s` enforces a minimum interval
   between navigation starts. It is pacing, not readiness: `--wait` is the
   per-page readiness deadline and `--settle` requires a continuous quiet
   period after content thresholds pass. Increasing readiness waits does not
   satisfy the pacing requirement, and pacing does not prove useful content.

   CDP now gives each query artifact a collision-safe ID that includes its
   one-based input position and evidence-window identity, for example
   `001-production-llm-systems--all-time/page-1/` or
   `002-production-llm-systems--tbs-<hash>/page-1/`. Repeated text or paired
   horizons therefore remain distinct within the pass.

5. Review the complete page-one artifacts before planning another Google
   invocation. Inspect `candidates.tsv`, the summary, rendered Markdown/HTML,
   block warnings, source mix, duplicated claims, and missing evidence classes.
   Spend at least 30 seconds doing actual artifact inspection and reasoning
   between Google invocations; a blind sleep is not a review. Record the
   resulting keep/reject/gap decisions in `research-log.md`, then choose whether
   to stop, create the next query unit/pass, or escalate a specific query.

   Pages 2–3 are a reviewed escalation, never a blanket default. Escalate only
   when page one exposes a concrete unresolved gap, place the selected query
   units in a new query file, and use a separate output directory:

   ```bash
   mkdir -p "$PASS_ROOT/pages-2-3-escalation"

   cdp --browser-mode headed workflow web-research serp \
     --query-file "$PASS_ROOT/escalated-queries.txt" \
     --serp google \
     --fallback-serp none \
     --parallel 1 \
     --navigation-delay 30s \
     --result-pages 3 \
     --fast-fail-blocked \
     --blocked-failure-threshold 1 \
     --progress stderr \
     --candidate-out "$PASS_ROOT/pages-2-3-escalation/candidates.json" \
     --out-dir "$PASS_ROOT/pages-2-3-escalation" \
     --min-visible-words 50 \
     --min-html-chars 1000 \
     --min-markdown-words 50 \
     --wait 15s \
     --settle 2s \
     --json > "$PASS_ROOT/pages-2-3-escalation/summary.json"
   ```

   This reruns page one for a self-contained escalation artifact; only pages two
   and three are the added discovery depth. Review the escalation before any
   further pass. If progress or captured artifacts show the first challenge,
   stop immediately and ask the user to clear it before a later invocation.

6. Add practitioner and paper evidence only after selecting canonical URLs.
   Prefer the source-native headed collectors:

   ```bash
   mkdir -p "$ROOT/source-native"

   cdp --browser-mode headed workflow hacker-news collect \
     'https://news.ycombinator.com/item?id=<id>' \
     > "$ROOT/source-native/hn-<id>.md"

   cdp --browser-mode headed workflow reddit collect \
     'https://www.reddit.com/r/<subreddit>/comments/<id>/<slug>/' \
     > "$ROOT/source-native/reddit-<id>.md"

   cdp --browser-mode headed workflow x collect \
     'https://x.com/<handle>/status/<id>' \
     > "$ROOT/source-native/x-<id>.md"

   cdp --browser-mode headed workflow linkedin collect \
     'https://www.linkedin.com/posts/<canonical-activity>/' \
     > "$ROOT/source-native/linkedin-<activity-id>.md"

   cdp --browser-mode headed workflow arxiv collect \
     'https://arxiv.org/abs/<version-pinned-paper-id>' \
     > "$ROOT/source-native/arxiv-<paper-id>.md"
   ```

   Search listings and SERP pages remain discovery indexes, not evidence. Check
   the returned item/post/paper identity against the selected canonical URL.
   An identity mismatch, login shell, unrelated feed, empty source-native
   record, or redirect to a different item is not evidence. Correct the URL or
   reject the source.

   Use generic headed extraction for these source classes only when the
   source-native workflow is unavailable and the rendered page independently
   proves the same canonical identity. Label that fallback in
   `research-log.md`; generic markup must never override a source-native
   identity mismatch.

7. Write a deliberate visit list. Prefer canonical source URLs. If Google emits
   redirect wrappers, extract the true target from `url=`, `q=`, or `u=` and
   discard tracking parameters such as `ved`, `ei`, and `usg`.

8. Extract rendered pages in modest chunks. If a batch fails because the daemon
   drops, stop and ask the user to restore it; do not run daemon repair commands.

   ```bash
   cdp --browser-mode headed workflow web-research extract \
     --url-file "$ROOT/visit-urls.txt" \
     --max-pages 100 \
     --parallel 4 \
     --content-extractor auto \
     --selector body \
     --out-dir "$ROOT/pages" \
     --min-visible-words 50 \
     --min-html-chars 1000 \
     --min-markdown-words 50 \
     --json > "$ROOT/extract-summary.json"
   ```

9. Post-process captured HTML into clean article snapshots before synthesis:

   ```bash
   uv run python scripts/extract_theme_articles.py \
     "research/$THEME_SLUG" \
     --scratch-root "$ROOT"
   ```

   Keep the generated `articles/` directory under `tmp/`; it is reading
   substrate, not committed output.

10. Create or update `research/<NN-theme-slug>/` with:
   - `README.md` — short entry point and navigation, pointing first to `guide/`.
   - `guide/00-README.md` plus numbered chapters — the main reader-facing
     artifact. Write this as source-linked, ELI5, book-like learning material,
     not bullet soup. Target enough depth for a serious 1.5-3 hour read on a
     major theme.
   - `assets/README.md` and local image files when diagrams/screenshots are used
     in the guide; credit original sources.
   - `briefing.md` — executive verdict, confidence, evidence for/against,
     failure modes, hidden assumptions, implications.
   - `source-index.md` — source list with quality labels.
   - `research-log.md` — query batches, source-selection notes, tool artifacts,
     article-extraction notes, HN/social signal summary, limitations.
   - `sources.json` — URL, title/label, quality, role, and date when known.

11. Optionally verify private reading output:

    ```bash
    uv run python scripts/build_theme_book.py "research/$THEME_SLUG" --formats markdown,epub
    ```

12. Validate:

    ```bash
    uv run python scripts/validate_research.py
    ```

## Regression cases

| Situation | Required behavior |
| --- | --- |
| The prompt suggests six months for every topic. | Choose and justify topic-fit horizons; normally retain evergreen coverage and add a window only where freshness matters. |
| A pass proposes four queries or page three by default. | Reduce it to one to three query units and one reviewed page; escalate selected gaps separately. |
| A second Google invocation is ready immediately. | Inspect the current artifacts and reason about gaps for at least 30 seconds before invoking Google again. |
| Google shows consent, auth, unusual traffic, CAPTCHA, or a bot check. | Stop on that first page; do not fall back to another engine or continue the pass. |
| A selected HN, Reddit, X, LinkedIn, or arXiv URL is needed as evidence. | Run its headed source-native `collect` workflow and verify returned identity before citation. |
| A generic capture resolves to a different post or profile. | Reject it as evidence; generic extraction cannot repair an identity mismatch. |
| A PDF renders in Chrome. | Acquire it separately with headed `click --wait-download`, then use the local `pdf-to-markdown` workflow; record both provenance steps and never imply OCR. |

## Synthesis rubric

Every theme guide should:

- Teach from first principles in plain language while respecting technical detail.
- Inline links to external sources at the point of use so the reader can jump to
  evidence immediately.
- Preserve meaty details from primary sources, not collapse them into vague
  claims.
- Separate primary evidence, vendor claims, practitioner patterns, community
  skepticism, and open questions.
- Include diagrams or source images where they materially improve learning, with
  local copies and credits.
- End with a compressed summary and next-reading path.

Every briefing should answer:

- What is the evidence-weighted verdict?
- Which claims are well-supported, weakly supported, or contested?
- When deeper results were justified, what changed after the separately reviewed
  pages 2–3 escalation?
- Where do HN/social practitioners agree or disagree?
- What are the likely failure modes and incentives of the sources?
- What should the next researcher do?
