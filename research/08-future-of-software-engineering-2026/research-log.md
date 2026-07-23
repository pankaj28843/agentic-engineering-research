# Research Log

## Scope and cutoff

This packet was researched on 23 July 2026 from the
[Thoughtworks report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf),
[Martin Fowler's index](https://martinfowler.com/bliki/FutureOfSoftwareDevelopment.html),
linked participant accounts, and five independent source phases.

The non-OCR report parse contains exactly 53 literal bullet markers. A
chapter-coverage audit reconciled all 53 markers with unique IDs, titles,
slugs, printed pages, governing questions, skeptical tests, capsule slices,
and guide targets. Part 3 contains six headings but no literal bullets; these
are retained as six `NNa-...` management interludes.

## Source phases

| Phase | Topic | Selected | Principal audit result |
|---|---|---:|---|
| 01 | Verification and harness engineering | 28 | 16 KEEP, 9 LEAD-ONLY, 3 REJECT |
| 02 | Teams, learning, and skill formation | 28 | 11 KEEP, 16 LEAD-ONLY, 1 REJECT |
| 03 | Legacy modernization and expectations | 27 | 6 KEEP, 17 KEEP-LIMITED, 3 LEAD-ONLY, 1 REJECT |
| 04 | Governance, tokenomics, and security | 32 | Defense-in-depth and workload-specific economics survive; universal rates and thresholds do not |
| 05 | Open source, specifications, and human judgment | 36 | 22 KEEP, 12 LEAD-ONLY, 2 REJECT |

The five queues contain 151 selected phase entries. Two URLs recur across
phases, yielding 149 distinct phase-source URLs before adding the report and
Fowler index. Seven additional participant and Fowler routes are cataloged as
dependent retreat provenance because chapters use them only to establish what
the overlapping witness network discussed, not as independent evidence.

## Discovery and extraction contract

Every live page was read with `cdp --browser-mode headed`. Search-result
snippets were discovery leads only. Queries were grouped by exact provenance,
technical mechanism, empirical measurement, failure or counterexample,
governance or standards, and practitioner experience. Source selection
preceded long-page extraction.

### Query batches and SERP depth

Each independent phase used a headed batch of ten exact query families
(`Q1`–`Q10`) and requested three Google result pages per query with
`--result-pages 3`. The durable selection ledgers preserve each exact query and
the selected candidate's query, result page, and within-page rank. The
gitignored `queries.json`, page captures, and candidate tables retain the
machine-readable execution evidence:

| Phase | Successful discovery artifact | Queries | Headed result depth |
|---|---|---:|---:|
| 01 verification and harness | `serp-01-verification-harness` | 10 | 3 pages each |
| 02 teams and learning | `serp-02-teams-learning` | 10 | 3 pages each |
| 03 legacy and expectations | `serp-03-legacy-expectations` | 10 | 3 pages each |
| 04 governance and tokenomics | `serp-04-governance-tokenomics-retry` | 10 | 3 pages each |
| 05 open source and human judgment | `serp-05-open-source-human-retry` | 10 | 3 pages each |

The Phase 04 and Phase 05 retry directories are the successful canonical
batches. Failed and partial attempts were retained separately rather than
silently merged. Phase 05's later Q7–Q10 recovery also captured all three
requested pages for each query after the user cleared the browser check.

Rendered artifacts and bulky page snapshots remain under the repository's
gitignored `tmp/` tree. Durable files contain conclusions, source identity,
evidence class, method, denominator, limits, and chapter routing—not raw page
dumps.

### Article post-processing

The final source-audit pass ran the repository cleaner over the captured
`html.json` corpus:

```bash
uv run python scripts/extract_theme_articles.py \
  research/08-future-of-software-engineering-2026 \
  --scratch-root tmp/future-software-engineering-2026 \
  --output-root tmp/future-software-engineering-2026/postprocessed-articles
```

It wrote 142 of 158 source-focused `article.md` snapshots plus a manifest.
Thirteen additional records were PDF-viewer DOM shells that the HTML article
cleaner correctly could not turn into useful articles, and three selected URLs
had no matching `html.json` key. Those sources were not inferred from the
shells: the report used its non-OCR parse; readable PDF sources used
browser-acquired files plus `pdftotext`; and the source audits record the
relevant direct capture or fallback. Five generated snapshots carried
low-content warnings and were not promoted to full-page evidence merely
because the cleaner wrote a file. Clean snapshots, the manifest, PDF text, and
all raw captures remain under `tmp/`.

The browser daemon was checked only with the repository-authorized
`cdp daemon status --json`. It was healthy. No unattended daemon start,
restart, stop, keepalive, or active-browser probe was used.

## Native arXiv and Hacker News extraction

During Phase 05, the local CDP implementation gained source-aware extraction
profiles designed around domain boundaries rather than page-specific scripts:

- arXiv URLs in `/abs`, `/html`, `/pdf`, `/src`, and `/e-print` forms are
  identified and normalized to the official semantic HTML representation when
  available;
- semantic arXiv article content is projected from the document root to
  Markdown, retaining headings, lists, tables, code, figures, links, and
  mathematical structure;
- Hacker News item pages are parsed as a story plus indentation-preserving
  comment tree;
- final URLs are revalidated so redirects cannot silently switch source type;
- exact-host parsing resists lookalike hostnames;
- planned and effective extraction strategies are distinguished when a native
  path falls back to generic rendered HTML;
- retry state preserves browser mode, connection, and state-directory context.

Real headed-browser fixtures were run against an arXiv PDF-form URL and Hacker
News item `46641042`. The arXiv input normalized to semantic HTML and yielded
9 sections and about 10,507 Markdown words. The HN fixture yielded 107
structured comments and about 7,643 Markdown words. Both passed useful-content
quality checks.

This is representation routing, not native PDF-byte or TeX-archive parsing.
When official arXiv HTML is absent, the extractor fails honestly. Browser PDF
fallbacks were therefore downloaded through the headed browser and converted
with `pdftotext`; OCR was never used.

## PDF and access handling

Browser PDF-viewer shells were not treated as article content. Native text was
materialized for the relevant PDFs after browser acquisition. The source
audits record each such fallback and its boundaries.

ScienceDirect Phase 05 source S32 returned the same robot challenge on the
initial extraction, an immediate user-assisted retry, and a later deferred
retry. It was rejected. No title, abstract, DOI, method, or result was inferred
from shell metadata.

Previously blocked Google query pages in Phase 04 and Phase 05 were retried
after the user cleared the browser check. All Phase 05 Q7–Q10 discovery pages
then passed. Their snippets remained non-evidence.

## Hacker News policy

Hacker News was read through headed CDP. Threads were used to locate original
project records, preserve contested practitioner hypotheses, and identify
failure vocabulary. Points, comment counts, and self-selected comments are not
population evidence. Policy claims belong to the linked project, standards
body, or institution.

## Authenticated panel

Authenticated collaborators were assigned distinct adversarial roles:
provenance, technical verification, organizational learning, security and
economics, and editorial integration. Panel responses were classified in a
separate ledger. They supplied questions, falsifiers, and possible source
leads; they did not become factual evidence. A panel-suggested fact required a
separately extracted source before use.

## Evidence audit

Each selected source was read for provenance, method, sample or artifact,
outcomes, conflicts, date sensitivity, and external-validity limits. Sources
were retained as KEEP, KEEP-LIMITED, LEAD-ONLY, or REJECT. The label describes
what the source can support; it is not a vote for or against agentic
engineering.

Repeated participant accounts that lead back to the same retreat were treated
as one dependent witness family. Chatham House handling was preserved:
anonymous bullets were not reverse-attributed by matching them to similar
public anecdotes.

## Source audit — 23 July 2026

The completed guide has 53 report-bullet chapters, six visibly labeled
management interludes, and one reading index. Pandoc plain-text measurement
counted 79,518 words across the numbered chapters, with a range of 1,310–1,769
words, and 6,174 words across the interludes, with a range of 910–1,175 words.
Every content file has one podcast hook and one onward-reading route.

The machine manifest and human source index each contain 158 distinct canonical
URLs. The guide, briefing, packet README, and research log use 121 distinct
evidence-source citations; every one resolves to a manifest entry. Derived
publication links recorded below are outside that evidence count. The other 37
manifest entries remain ledger-only after synthesis, preserving rejected,
lead-only, bounded, or redundant candidates for audit rather than silently
discarding the selection history. Google redirect URLs and tracking parameters
are absent.

The corpus mixes the primary retreat report and public participant routes with
peer-reviewed studies, preprints, official standards and policies,
practitioner and vendor reports, skeptical perspectives, and Hacker News
community signals. Community threads are hypothesis and discovery material,
vendor claims retain their conflict, and neither search snippets nor
authenticated-panel answers are evidence.

The final article post-processing pass wrote 142 of 158 snapshots. Thirteen
failures were browser PDF-viewer shells already handled through browser-acquired
native text plus `pdftotext`, without OCR; three records had no matching HTML
capture and were handled through the documented report parse, direct capture,
or fallback route. Five low-content warnings were not promoted automatically.
The two persistent ScienceDirect access shells are labeled
`rejected-access-shell` in the manifest.

`uv run python scripts/validate_research.py` passed for all eight repository
themes. Residual limits remain explicit in the chapters: the corpus does not
establish universal productivity multipliers, fixed autonomy thresholds,
population rates from community discussion, a measured ecosystem-wide
code-to-spec transition, or a universal human–agent teaming advantage.

## Downstream publication record — 23 July 2026

The research packet passed its source/citation/depth audit and repository
validator before publication. The theme landed in commit `ff1d99e`; the
Unicode-safe PDF compatibility pass landed in `e3a333c`.

### Book

The downstream book build produced:

| Artifact | SHA-256 |
| --- | --- |
| `future-of-software-engineering-2026.pdf` | `23e1a5025564928b3ecd47ff646c7873c67ef2fc427c9e3ba478e270b41c053b` |
| `future-of-software-engineering-2026.epub` | `4d96dcff4217d22a815794e9213d855b3adc9b9fc64cb7102fe2bf503923f7f2` |
| `future-of-software-engineering-2026.mobi` | `541b85672720d9fa662bafaec6a5c5e02cf664f297653706cb0f2225155f2a41` |
| `future-of-software-engineering-2026.kindle.epub` | `955e9d43fabd967bf9c377b4eeaa9c80269a5fc21e01c990f9a826db6cc8f7f2` |

The A5 PDF has 387 pages and 88,522 extractable words. First, middle, and final
page samples were visually inspected without clipping. EPUB and Kindle
archives passed integrity checks, both contained all 60 guide documents, and
the MOBI file passed type validation.

### Podcast

Six three-voice scripts were produced from the guide. The centralized
transcript gate passed all of them with 2,715–2,829 spoken words, 60–75 turns,
12 segments, and 8–11 source anchors each. Estimated runtimes were 18.1–18.9
minutes, and the adjacent-episode duplicate-turn check found no matches.

The synthesized masters run from 1,266.024 to 1,376.232 seconds. Every file
decoded end to end, used mono MP3 at 24 kHz and 96 kbps, and matched its 12
chapter records and expected turn-clip count. Integrated loudness was
−19.4/−19.5 LUFS, true peak was −2.2 to −2.4 dBTP, and loudness range was
3.8–4.0 LU.

The public series is
[Future of Software Engineering 2026: A Skeptical Field Guide](https://rssplayer-feeds.d.pankajsingh.dev/pub/f/7560e3305bfe495771a06dc0c030cbb0fb40a541edc2e229.xml),
feed ID `a6501d38-1535-46a4-8983-ec737f70c8aa`. Its publication receipt has
SHA-256
`9eb04e68368efb0d1fef978e8726b43d1d381ba5ee8e96b4af32a7a21e8ec0c9`.

Live verification used the already-running headed CDP browser. The RSS request
returned HTTP 200, parsed without an XML error, exposed the exact series title,
and contained six ordered items with unique GUIDs, `audio/mpeg` enclosures,
expected byte lengths, and hashes matching the local masters. The episode 6
enclosure also returned HTTP 200; Chrome decoded it to 1,310.583 seconds,
buffered it, and played about 20 seconds without a media error.

Publication URLs and artifact hashes are provenance for derived outputs, not
research evidence, so they are intentionally excluded from `sources.json`.
