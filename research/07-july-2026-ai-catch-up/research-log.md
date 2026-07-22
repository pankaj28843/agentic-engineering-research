# Research Log

## Scope and evidence cutoff

This packet reconstructs AI, LLM, and agentic-engineering developments from 1
through 21 July 2026 in Europe/Copenhagen. It uses a calendar-day ledger with
exclusive UTC boundaries rather than treating a search engine's displayed date
as the event date. The final retrieval cutoff is recorded after the 21 July
refresh; earlier captures preserve their own timestamps under `tmp/`.

The reporting method and page design were frozen before full discovery. The
durable contracts are [publication-spec.md](publication-spec.md) and
[design-audit.md](design-audit.md). Raw browser captures, rendered pages,
provider responses, and scoring work remain under the gitignored `tmp/` tree.

## Headed browser contract

All live search and page extraction used the installed `cdp` command against
headed Chrome. The passive gate was:

```bash
cdp --browser-mode headed pages --json
```

It returned `ok: true` with inspectable page tabs. No unattended daemon start,
restart, stop, keepalive, or active-browser-probe command was run. The workflow
did not use headless Chrome, Playwright, `curl`, or a direct HTTP fallback.

Google discovery used Google only, no fallback, one query at a time, no more
than ten queries in a batch, and two result pages. Each row carried an explicit
Google `tbs` value:

```text
<query><TAB>cdr:1,cd_min:MM/DD/2026,cd_max:MM/DD/2026
```

Rendered Google pages and their `time_filter` metadata are discovery evidence.
Neither snippets nor displayed dates support newspaper claims. Selected
original pages and canonical Hacker News item pages were extracted separately
and inspected before a claim could be drafted.

## Publication design panel

Phase one sent eight distinct requests through headed provider interfaces:
three sequential ChatGPT requests, two Perplexity requests, and one request each
to Grok, Gemini, and Claude. Seven returned substantive results. Claude returned
an acknowledged HTTP 429 cooldown; that result was preserved and was not
retried. Raw results are under:

```text
tmp/ask-agents/july-2026-spec/
```

The accepted and rejected suggestions are recorded in the planning capsule's
`research/panel-synthesis.md`. External-agent prose challenged the method and
layout; it was never accepted as item-level evidence. The final contract
separates relevance, evidence confidence, and discussion intensity, refuses
popularity points, dates the exact material delta, allows quiet days, and edits
content before changing publication-wide typography.

## Date window

The repo-local helper resolved 21 Europe/Copenhagen calendar days. The first day
runs from `2026-06-30T22:00:00Z` through the exclusive boundary
`2026-07-01T22:00:00Z`; the last runs from `2026-07-20T22:00:00Z` through
`2026-07-21T22:00:00Z`. The exact reproducible command is:

```bash
python3 .agents/skills/publish-ai-news/scripts/resolve_window.py \
  --cadence weekly \
  --from 2026-07-01 \
  --to 2026-07-21 \
  --timezone Europe/Copenhagen \
  --now 2026-07-22T00:01:00+02:00
```

Raw publication, event, discussion, and retrieval timestamps are retained when
available. The source timestamp and normalized UTC value are separate fields.
Unknown timezones or publication times remain unknown; they are not reconstructed
from result labels.

## Discovery lanes

The period was split into three disjoint scratch lanes:

```text
tmp/research-web-critical/july-2026-ai-catch-up/segments/jul01-07/
tmp/research-web-critical/july-2026-ai-catch-up/segments/jul08-14/
tmp/research-web-critical/july-2026-ai-catch-up/segments/jul15-21/
```

Each lane captures query files, SERP summaries, candidates, seven HN daily
archives, a source-selection ledger written before article extraction, original
pages, canonical HN item pages, page-quality records, and immutable candidate
snapshots. Candidate counts and HN points/comments measure discovery coverage
only. A discussion score requires inspected substantive comments and records
the technical themes that changed interpretation.

The accepted Google runs before the completed-day refresh covered 31 exact-date
queries, 62 rendered result pages, and 467 candidates with no workflow failures
or warnings: 1-3 July contributed 9 queries, 18 pages, and 100 candidates; 4-7
July contributed 8, 16, and 100; 8-14 July contributed 7, 14, and 133; and the
accepted second 15-21 July batch contributed 7, 14, and 134. An earlier 15-21
July batch reused shared slugs and was discarded rather than mixed with the
accepted immutable artifacts. The final July 21 refresh added one query, two
pages, and 19 candidates, bringing the accepted Google total to 32 queries, 64
pages, and 486 candidates.

The 1-3 July pilot deliberately exposed evidence problems before scaling:
login-gated social posts, missing release dates, mutable repository pages, and
publication artifacts without timezones. Those conditions cause explicit
missing states, qualified wording, demotion, or rejection rather than invented
precision. The later lanes retain the same adjudication rules.

## Tool gaps repaired

The publication reproduced three reusable tool gaps and paused research to
repair them through managed feature requests and capsule-backed improvement
loops.

- `agents-skills` commit `f741fa097fe93aecf8362f14d7c6626177720297`
  documents the reliable PEP 723 renderer invocation, adds ordered custom CSS
  support, forwards styles through the wrapper, and adds a Poppler-backed PDF
  validator. The full owning-repository suite passed, the commit was pushed,
  and a real styled A4 smoke render passed the new validator.
- `cdp-cli` commit `d5ef1eb3e2af1a603590105fd8c7994c5bc67927`
  exposes the exact-date TSV grammar in help, describe metadata, schema, and the
  README, and returns line-numbered errors for malformed rows. Focused and full
  tests, install, installed E2E, passive headed pages, and a scoped exact-date
  Google smoke passed. A final broad-suite repeat was host-load-preflight
  blocked after only a test addition; the changed binary was reinstalled and
  its installed E2E passed. The broad demo was not rerun because it owns daemon
  lifecycle operations forbidden by this repository's human-approval rule.
- `agents-skills` commit `12b715d982fa6a40c28e9eb5c8bad0fb677c4939`
  replaced a context-blind skill-safety check with a canonical scanner that
  distinguishes executable lifecycle commands from prose documenting forbidden
  commands, masks YAML safely, and emits structured JSON. Ten focused tests,
  the full owning-repository validation and install checks, and a scan of all 52
  skills passed with no blockers. Eight operation-specific warnings remained
  visible for human review.

All three commits were pushed to their owning `main` branches before the
publication depended on them.

## Extraction post-processing

The CDP workflow emitted readable `page.md`, `visible.txt`, and `html.json`
artifacts for selected pages. The required post-processing command was:

```bash
uv run python scripts/extract_theme_articles.py \
  research/07-july-2026-ai-catch-up \
  --scratch-root tmp/research-web-critical/july-2026-ai-catch-up
```

It produced 98 clean article snapshots from the 101 cataloged URLs. The
extractor's normalized content fields total 114,659 words; `wc -w` over the
generated Markdown files reports 120,403 shell tokens because it also counts
headers, link syntax, and other Markdown tokens. Three sources had no compatible capture: an access-gated
Anthropic X post, the unselected Ray Myers context article, and an attributable
social post. Two GitHub issue snapshots triggered the under-80-word warning;
their complete headed page captures remain in the same scratch tree. The
machine-readable extraction manifest is
`tmp/research-web-critical/july-2026-ai-catch-up/articles/manifest.json`.
Generated snapshots remain under `tmp/`; the newspaper cites canonical public
URLs and records evidence role and access condition in the durable catalog.

## Social and community evidence

Hacker News coverage uses the public daily archive
`https://news.ycombinator.com/front?day=YYYY-MM-DD`, followed by canonical item
pages and their linked originals through headed CDP. Broad token matches such as
`AI` were inspected and routinely rejected. Social posts qualify only the
attributable statement visible in the captured page; access-gated or
discovery-only posts cannot prove a broader event.

## Limitations

- Google custom-date filters improve discovery boundaries but do not establish
  an event or publication date.
- A rendered page is not automatically independent or correct; source role and
  claim support are adjudicated separately.
- Mutable repository and documentation pages can prove only the captured state
  unless a dated tag, commit, or changelog reconstructs the delta.
- HN archives and item pages do not represent all practitioner communities.
- The completed-day July 21 refresh found five new and six dropped Google URLs
  relative to the earlier candidate set, mostly rank churn. Its material change
  came from the refreshed HN archive and the separately extracted OpenAI
  incident account; no Google snippet was promoted into evidence.

## Final audit record

The 22 July completion pass produced the following evidence:

- Discovery: 32 accepted exact-date Google queries, 64 rendered result pages,
  486 candidates, and 21 canonical daily HN archives, plus a completed-day HN
  refresh. The Google workflows reported no failures or warnings.
- Selection: 56 stories across all 21 dates: 14 leads, 35 secondaries, and 7
  radar items. The issue validator reported zero editorial errors; July 10
  remains an evidence-bounded quiet day with no manufactured lead.
- Sources: 101 canonical URLs and 102 story references. The 101 unique story
  references cover the full catalog; the earlier Hugging Face incident source
  is intentionally reused by its July 21 continuation. The source-family mix is
  47 primary, 42 community, 3 independent, 2 practitioner, 5 secondary, 1
  attributable social, and 1 inaccessible primary. No Google wrapper or
  tracking URL remains.
- Extraction: 98 clean snapshots, 3 documented missing captures, and 2
  under-80-word GitHub warnings. Normalized article content totals 114,659
  words; generated Markdown totals 120,403 `wc -w` tokens.
- Print geometry: the period map is one A4 page. All 21 independent daily PDFs
  passed required-text and 1-2-page validation: 12 one-page chapters and 9
  two-page chapters, 30 pages total. The centered 166 mm body measure is about
  41% wider than the original 118 mm column.
- Assembled publication: 55 A4 pages, PDF 1.7, required opening/date/closing
  text present, each dated chapter heading exactly once and in chronological
  order, and all 101 canonical URLs present as link annotations. The only extra
  external link is the general Hacker News archive; other extras are internal
  table-of-contents links.
- Visual audit: 160 dpi rasters and progressive visual-reasoning artifacts
  covered 10 representative book pages with no processing failures: the cover,
  one-page map, quiet July 10 fixture, both July 15 and July 21 pages, and the
  start, middle, and end of the closing guide. Mechanical validation checked all
  55 pages for nonblank A4 bounds. No blank, clipped, overlapping, or stranded
  content was found.
  The PDF is untagged; correct one-column text extraction mitigates reading-order
  risk but does not replace a semantic tag tree.

Source audit note: `uv run python scripts/validate_research.py` passed all seven
themes. The guide contains 25 numbered Markdown files and 18,104 words, uses
descriptive inline source links, labels vendor claims and counter-evidence,
documents query batches, two-page SERP depth, headed extraction, HN use, and
limitations, and keeps generated article snapshots under `tmp/`. No unattended
daemon lifecycle command appears in the packet.
