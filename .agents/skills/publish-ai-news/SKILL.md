---
name: publish-ai-news
description: >
  Publish a source-backed AI engineering news edition for a daily, weekly,
  monthly, or explicit inclusive date range. Use when asked for an AI/LLM/agent
  news catch-up, newspaper, digest, or recurring issue that needs original and
  Hacker News links plus a tested A4 PDF. Skip for undated topic research or a
  manuscript that only needs rendering. Produces a durable theme packet,
  candidate ledger, dated chapters, and mechanically and visually audited PDF.
argument-hint: "<focus> [--cadence daily|weekly|monthly] [--from YYYY-MM-DD --to YYYY-MM-DD] [--timezone Area/City] [--max-pages-per-day 2]"
---

# Publish AI News

Create an evidence-led AI engineering issue from discovery through a validated
private-reading PDF. This is a lifecycle skill: it composes headed browser
research, HN reading, source adjudication, durable theme writing, PDF rendering,
and visual review without weakening their individual contracts.

## Scope Contract

| Example | Expected routing or guardrail |
|---|---|
| Direct trigger: "Publish last week's agentic engineering news" | Resolve the last completed ISO week, research it, and publish a dated issue. |
| Direct trigger: "Make a July 1-21 AI catch-up newspaper" | Use the explicit inclusive range and create one chapter per date. |
| Direct trigger: "Produce yesterday's LLM engineering daily" | Resolve the previous completed local day and publish one dated chapter. |
| Direct trigger: "Produce the next daily news podcast" | Use the routine daily podcast delta below, then hand the frozen evidence to the audio Forge. |
| Non-trigger: "Research whether GraphRAG works" | Use `/research-web-critical`; no periodical or PDF is implied. |
| Non-trigger: "Turn this finished Markdown into PDF" | Use `/book-publish`; do not repeat research. |
| Misuse: "Use snippets so it is faster" | Refuse snippet-only evidence; snippets remain discovery leads. |
| Forbidden: "Start or repair Chrome automatically" | Stop and ask the human; do not run restricted daemon lifecycle commands. |

## Routine Daily Podcast Delta

A terse request for the next daily news podcast is sufficient when an existing
dated packet, frozen publication rubric, predecessor handoff, and Forge feed
exist. Treat it as a one-day evidence refresh and downstream handoff, not a new
format-design project:

1. Start after the predecessor episode's bound evidence cutoff, never its RSS
   `pubDate`, filename date, or a reconstructed timezone boundary. Extend the
   current packet through one new day, or through the current partial day when
   explicitly requested, and record the observed cutoff in research metadata.
2. Reuse the frozen rubric and publication contract. Run only the research
   methods the user authorizes. When restricted to `/research-web-critical` and
   `/search-hn`, do not invoke `/ask-agents`, social, video, PDF, book, or other
   discovery workflows; local agents may still perform mechanical review.
3. Validate the extended packet, materialize a fresh deterministic handoff with
   its exact hash, then pass that artifact to the audio Forge for script, TTS,
   audio, RSS publication, and headed live-feed verification.
4. Listener prose must tell the supported story. Omit timezone or date-boundary
   reconciliation, retrieval/parsing/access/visibility failures, and
   evidence/packet/source-processing narration. If an original source is
   unavailable but an HN discussion supports a useful point, attribute and tell
   that point without narrating the missing source or production process.

## Required Inputs

Capture these before discovery:

- `focus`: the literal editorial beat, such as AI engineering, model economics,
  RAG, coding agents, or a bounded combination.
- `cadence`: `daily`, `weekly`, or `monthly`.
- `from` and `to`: optional explicit inclusive ISO dates. Supply both or neither.
- `timezone`: an IANA timezone. Use the user's stated timezone; do not silently
  substitute the host timezone when dates can move across a boundary.
- `max_pages_per_day`: defaults to two and may not exceed two for this format.
- target repository/theme slug and issue title.

Explicit `from` and `to` override cadence defaults. Cadence still labels the
edition and its future refresh policy.

When no explicit range is supplied:

- `daily`: previous completed local calendar day;
- `weekly`: previous completed ISO Monday-Sunday week;
- `monthly`: previous completed calendar month.

Reject an inverted range, a single missing bound, an unknown timezone, or a
range that includes the current incomplete local day unless the user explicitly
asks for a partial issue. Label a partial issue on the cover and in metadata.

## Dependencies And Preflight

Required:

- `cdp` for headed Chrome discovery and rendered extraction;
- `jq` for browser workflow assertions;
- `uv` and the local `book-publish` skill scripts;
- Poppler commands `pdfinfo`, `pdftotext`, and `pdftoppm` for PDF acceptance;
- the repository's Python validator.

Run non-mutating preflight from the research repository:

```bash
command -v cdp
command -v jq
command -v uv
command -v pdfinfo
command -v pdftotext
command -v pdftoppm
cdp --browser-mode headed workflow web-research serp --help
cdp --browser-mode headed workflow web-research extract --help
cdp --browser-mode headed pages --json | jq '{ok, pages: (.pages | length)}'
```

The headed pages probe must report `ok: true` and at least one inspectable page.
If it fails, stop and ask the human to restore or approve the headed browser.
The only unattended daemon lifecycle check allowed in this repository is:

```bash
cdp daemon status --json
```

Do not run daemon start, restart, stop, keepalive, an active browser probe, an
ad-hoc browser URL repair, a headless fallback, or another browser automation
tool. Do not install missing dependencies without the user's approval.

## Phase 1: Freeze The Issue Contract

For a new publication format, a monthly issue, or a range longer than seven
days, create or resume a `/plan-capsule`. A one-day refresh may use the existing
publication specification when the format and rubric are unchanged.

Before searching, record:

1. reader and scan/deep-reading time budgets;
2. topic inclusions and exclusions;
3. daily information architecture and word ceilings;
4. deterministic date hierarchy;
5. selection rubric, confidence grades, and discussion scale;
6. source roles and missing-evidence language;
7. A4 typography, margins, measure, and overflow order;
8. mechanical and visual acceptance checks.

Use `/ask-agents` only to challenge the contract or propose leads. Persist every
provider result, including failures, and adjudicate suggestions. External-agent
text never satisfies an item-level source requirement.

## Phase 2: Materialize The Window

Create a scratch root and resolve a UTC boundary ledger with the bundled,
standard-library helper:

```bash
ISSUE_SLUG="<issue-slug>"
ROOT="tmp/research-web-critical/$ISSUE_SLUG"
mkdir -p "$ROOT"

python3 .agents/skills/publish-ai-news/scripts/resolve_window.py \
  --cadence "<daily|weekly|monthly>" \
  --from "<YYYY-MM-DD>" \
  --to "<YYYY-MM-DD>" \
  --timezone "<Area/City>" \
  > "$ROOT/window.json"

jq '{timezone, from, to, days: [.days[] | {date, utc_start, utc_end_exclusive}]}' "$ROOT/window.json"
```

Omit both `--from` and `--to` to use the cadence default defined above.

Treat `utc_end_exclusive` as an exclusive boundary. Preserve raw source
timestamps as well as normalized UTC; never infer event time from a Google
result label.

## Phase 3: Discover Each Date In Headed Google

Build query families that cover the issue focus without relying on one broad
token. Include releases, engineering techniques, incidents/postmortems,
security, economics/pricing, evaluation/corrections, production experience,
and explicit HN or primary-source targets when relevant. Keep every batch to ten
queries or fewer.

The query file is tab-separated: query in column one, optional Google `tbs` in
column two. For every date, use the exact same date in `cd_min` and `cd_max`:

```text
AI LLM agent engineering<TAB>cdr:1,cd_min:07/01/2026,cd_max:07/01/2026
model release benchmark pricing<TAB>cdr:1,cd_min:07/01/2026,cd_max:07/01/2026
AI outage incident postmortem<TAB>cdr:1,cd_min:07/01/2026,cd_max:07/01/2026
```

Run Google only, no fallback, one query at a time, and two result pages by
default:

```bash
DAY="<YYYY-MM-DD>"
DAY_ROOT="$ROOT/days/$DAY"
mkdir -p "$DAY_ROOT/serp-google"

cdp --browser-mode headed workflow web-research serp \
  --query-file "$DAY_ROOT/queries.tsv" \
  --result-pages 2 \
  --serp google \
  --fallback-serp none \
  --parallel 1 \
  --max-candidates 200 \
  --candidate-out "$DAY_ROOT/candidates.json" \
  --out-dir "$DAY_ROOT/serp-google" \
  --fast-fail-blocked \
  --blocked-failure-threshold 3 \
  --min-visible-words 50 \
  --min-html-chars 1000 \
  --min-markdown-words 50 \
  --json > "$DAY_ROOT/serp-summary.json"
```

Use a third page only for a named source or counter-evidence gap and record why.
Inspect `candidates.tsv`, the rendered result `page.md` files, warnings, and
failures before choosing any URL. Search snippets and result dates are leads,
not publication evidence.

## Phase 4: Add HN And Social Signals

Read the public daily HN archive through headed Chrome:

```text
https://news.ycombinator.com/front?day=YYYY-MM-DD
```

Select relevant canonical item pages, then extract both the HN item and its
linked original source through the headed `web-research extract` workflow. If an
Algolia query is needed for a gap, navigate to and extract its HTTPS endpoint
through headed Chrome as well; do not switch to `curl` in this repository.
Broad matches on words such as `AI` must be inspected rather than counted.

Use local social archives only when their coverage includes the issue window.
Record a documented absence when they do not. A social post is evidence only
for its own attributable statement; otherwise it is a lead or discussion signal.

## Phase 5: Select Before Extraction

Write `source-selection-ledger.md` before the article batch. For each selected
URL record source type, intended evidence role, why it can support that role,
discovery artifact, and expected claim. Record rejected duplicates, SEO
roundups, inaccessible pages, and sources that cannot support the intended
claim.

Canonicalize URLs. Remove Google wrappers and tracking parameters. Keep raw
browser captures and clean article snapshots under `tmp/`.

Then extract selected pages in modest headed batches:

```bash
cdp --browser-mode headed workflow web-research extract \
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

Read `page-quality.json`, `page.md`, and failure records. Use
`scripts/extract_theme_articles.py` to turn captured HTML into clean Markdown
when the theme workflow produces compatible `html.json` artifacts.

## Phase 6: Snapshot And Score Candidates

Read [the editorial contract](references/editorial-contract.md) before
adjudication. It defines the immutable candidate schema, date hierarchy,
relevance anchors, confidence grades, discussion scale, and placement
thresholds. Keep all three outputs separate: popularity never raises relevance,
and weak evidence changes claim wording or placement rather than the relevance
components.

## Phase 7: Write The Durable Edition

Use the packet rules in [the editorial contract](references/editorial-contract.md)
and the exact [daily chapter template](references/daily-template.md). Write
claims from extracted pages, never from the SERP. Keep bulky browser artifacts
under `tmp/` and canonical metadata in `sources.json`. Preserve quiet days and
omit empty sections rather than padding the issue.

Before rendering, enforce the dated chapter structure and word ceiling:

```bash
python3 .agents/skills/publish-ai-news/scripts/validate_issue.py \
  research/<NN-issue-slug>/guide --from <YYYY-MM-DD> --to <YYYY-MM-DD> \
  --stories research/<NN-issue-slug>/stories.json
```

## Phase 8: Prove Daily A4 Fit

Lint Markdown before rendering. Use the pushed `book-publish` scripts through
their PEP 723 invocation and the publication stylesheet:

```bash
BOOK_SKILL="$HOME/Personal/Code/agents-skills/molecules/book-publish"
STYLE="research/<NN-issue-slug>/newspaper.css"
DAY_FILE="research/<NN-issue-slug>/guide/<ordered-date-file>.md"
DAY_PDF="tmp/books/<issue-slug>/days/<date>.pdf"

uv run --script "$BOOK_SKILL/scripts/md2pdf.py" "$DAY_FILE" \
  --paper a4 \
  --font-size 10.5 \
  --stylesheet "$STYLE" \
  --no-mermaid \
  -o "$DAY_PDF"

uv run --script "$BOOK_SKILL/scripts/validate_pdf.py" "$DAY_PDF" \
  --paper a4 \
  --min-pages 1 \
  --max-pages 2 \
  --require-text "<YYYY-MM-DD>" \
  --json
```

If a day reaches three pages, edit using the frozen overflow hierarchy. Remove
redundancy and low-priority items before shortening protected evidence. Never
change type, margins, line height, tracking, or scale for one date.

Assemble the final issue from sorted guide files, excluding the guide README if
it duplicates the cover:

```bash
uv run --script "$BOOK_SKILL/scripts/md2pdf.py" \
  --dir "research/<NN-issue-slug>/guide" \
  --exclude 00-README.md \
  --paper a4 \
  --font-size 10.5 \
  --stylesheet "$STYLE" \
  --cover-title "<literal issue title>" \
  --cover-subtitle "<inclusive date window and focus>" \
  --cover-date "<publication date>" \
  --no-mermaid \
  -o "<output.pdf>"
```

Run the PDF validator with a page range wide enough for the complete edition
and repeat `--require-text` for structural markers. Verify that assembled HTML
contains exactly one dated chapter heading per expected date. Use `pdftotext`
to verify their first occurrences are in order; any later occurrence must be an
intentional running head, never a duplicate chapter. Inspect PDF link annotations
with Poppler or MuPDF; do not infer clickability from styling alone.

## Phase 9: Visual And Source Audits

Rasterize the cover, period map, densest day, quietest day, every two-page day
boundary, and final page with `pdftoppm`. Invoke `/ui-visual-reasoning`: read its
`report.json`, inspect the smallest useful preview, use the contact sheet to
select suspicious tiles, and escalate only those tiles required to decide a
specific rework. Record the rework brief and rerender after changes.

Run `/source-audit`, then the repository gate:

```bash
uv run python scripts/validate_research.py
```

The release is incomplete until the source mix includes primary evidence,
independent or practitioner evidence, community signal, and skeptical or
counter-evidence for contested claims; all source URLs are canonical; every
daily PDF passes; the assembled PDF has no blank page; and visual findings are
resolved or explicitly accepted as residual risk.

## Phase 10: Freeze The Podcast Evidence Handoff

When the issue will feed podcast production, read the
[podcast evidence handoff contract](references/podcast-handoff-contract.md).
Materialize the handoff only after the story ledger, source catalog, dated
chapters, source audit, and repository validation are final:

```bash
PACKET="research/<NN-issue-slug>"
HANDOFF="tmp/podcast-handoffs/<issue-slug>/podcast-handoff.json"

python3 .agents/skills/publish-ai-news/scripts/materialize_podcast_handoff.py \
  "$PACKET" \
  --from <YYYY-MM-DD> \
  --to <YYYY-MM-DD> \
  --packet-frozen-at <timezone-aware-ISO-timestamp> \
  --output "$HANDOFF"
```

Use the observed request time with `--run-requested-at` only when it is known.
Record the exact command, output path, printed SHA-256, and validation counts in
the packet's `research-log.md`. If the packet changes, rerun validation and
materialize a new handoff; a prior hash never describes revised evidence.

Verify that every `days[]` object contains `guide_markdown` identical to the
complete UTF-8 dated chapter. This preserves factual exposition, Builder impact,
caveats, discussion notes, evidence links, and radar prose for downstream
authors; the adjacent guide byte count and SHA-256 authenticate the text. The
field is additive under handoff schema v1, so existing consumers may ignore it.

Keep research-process evidence in the handoff without implying that it belongs
in the episode. Date-window and timezone reconciliation, retrieval or parsing
failures, page visibility, and source-access administration are provenance, not
listener copy. A downstream author may retain a concise caveat only when its
removal would materially overstate a claim; otherwise the author should tell
the tight supported story or attributed practitioner experience and leave the
production mechanics in evidence or show notes.

This phase transfers full guide prose, evidence, guide ordering, explicit gaps,
and weekly source unions. It does not define episode prose, cast, voices, TTS,
audio processing, filenames, RSS publication, or human listening approval.
Those decisions and their provenance belong to the downstream audio repository.

## Parallel Research Guardrail

Use parallel agents only when the user explicitly requests delegation or the
active project instructions authorize it. Partition by disjoint inclusive date
ranges and give each lane a separate `tmp/` root. Agents may produce evidence
ledgers first; tracked daily chapters are assigned only after the parent freezes
the template. The parent adjudicates cross-day duplicates, continuation arcs,
and final scores before publication.

## Release And Refresh

Record the issue window, timezone, retrieval cutoff, rubric version, query
batches, result-page depth, extraction counts, HN/social coverage or absence,
access failures, visual audit artifacts, and PDF validation command in
`research-log.md`.

Commit generated research only when the user or repository workflow requests a
commit. Never commit raw browser captures or PDFs under `tmp/`. After a refresh,
preserve prior candidate snapshots and explain corrections; do not silently
rewrite the edition's historical evidence state.

## Related Skills

- `/research-web-critical` owns deep headed Google discovery and rendered
  extraction.
- `/search-hn` owns HN research concepts; this repo-local workflow routes its
  live HTTP reads through headed CDP.
- `/ask-agents` pressure-tests the publication contract and proposes leads.
- `/book-publish` owns Markdown-to-PDF rendering and PDF acceptance tooling.
- `/ui-design-audit` owns the pre-implementation reading and visual brief.
- `/ui-visual-reasoning` owns progressive raster inspection.
- `/source-audit` owns the final theme evidence audit.
- `/plan-capsule` owns resumable planning for substantial issues.
- The downstream audio repository consumes the versioned podcast evidence
  handoff and owns synthesis, audio, RSS, and listening approval.

## Common Failure Modes

- One date bound is missing: stop and require both `from` and `to`.
- The window includes an unfinished day: require explicit partial-issue intent
  and label the cutoff.
- Headed pages probe fails: stop and ask the human; do not repair or fall back.
- Google ignores the intended date: inspect the rendered search URL and `tbs`
  metadata, then reject result labels as date proof.
- Query-file row has more than two tab-separated columns: fix the named line;
  do not reinterpret malformed filters.
- HN broad search returns irrelevant token matches: inspect daily archives,
  canonical item pages, and linked originals.
- Candidate ledger is written after extraction: stop and write the source-choice
  rationale first so selection bias remains visible.
- A vendor claim has high relevance but low confidence: qualify or demote it;
  do not reduce its relevance score to hide the evidence gap.
- A quiet day looks empty: preserve it; do not add low-value stories for visual
  symmetry.
- A day renders on three pages: apply editorial cuts in priority order and
  rerender; do not shrink one day's typography.
- PDF text is present but links do not click: inspect annotations and repair the
  renderer or Markdown anchors before release.
- Raster review finds clipped or stranded content: fix publication-wide CSS or
  prose, rerun all affected daily fixtures, and repeat the visual audit.
- Podcast production starts reconstructing source joins from prose: stop and
  materialize the versioned evidence handoff from the validated packet.
- A podcast author only receives normalized caveat or discussion fields: stop;
  require the exact `days[].guide_markdown` value so factual, Builder-impact,
  and radar prose is not silently discarded.
