# Research log

## 2026-07-28 — Scope and reader contract

- Read the user-provided 22-topic syllabus before research.
- Targeted experienced full-stack engineers who are new to AI engineering.
- Chose an ELI5-first but non-patronizing teaching contract, followed by
  precise systems vocabulary, production consequences, and active exercises.

## 2026-07-28 — Browser-grounded discovery

- Inspected the installed `cdp` workflow help and used only headed CDP reads.
- Ran both recent-window and undated/foundational Google query families.
- Collected 176 rendered SERP pages and 1,391 distinct candidate URLs across
  the broad baseline. Those six broad batches requested `--result-pages 3`;
  one batch ended at 26 rather than 30 scheduled pages. Snippets were treated
  only as leads.
- Selected 97 baseline sources before extraction, balancing primary research,
  official documentation, practitioner evidence, security authorities, and
  community or social signals.
- Used source-native CDP workflows for Hacker News, Reddit, LinkedIn, X, and
  28 arXiv papers.

## 2026-07-28 — Extraction and repair

- Attempted all 97 selected URLs in a bounded, headed extraction batch.
- Retained the initial quality report and ran one timing-only retry for nine
  weak captures at lower concurrency with longer readiness windows.
- Recovered the X and Pinecone pages on retry.
- Classified Meta's page as a visibility-gate false negative because its
  rendered Markdown and HTML bodies were substantial and stable enough for
  article extraction.
- Classified the Unstructured page as a streaming-shell consistency warning:
  its full article body was present, alongside a large framework payload that
  must be removed by article post-processing.
- Replaced five empty browser-PDF views with canonical conference landing
  pages and/or full arXiv HTML. Follow-up exact-title Google searches were
  serialized and completed without block signals.

## 2026-07-28 — Browser-acquired PDF text layers

The installed `cdp` build did not expose a first-class PDF-to-Markdown command.
For each retained PDF, the headed browser opened the exact source, a
same-origin download link was activated in the PDF viewer, and CDP's download
events recorded the final URL, byte count, and local file. Conversion then ran
locally with `convert-docs --ocr never`; `pdftotext -layout` supplied an
independent text-layer and rough completeness check. This is deliberately not
described as CDP doing the conversion: CDP provided authenticated,
browser-equivalent acquisition and provenance, while the converter handled
the existing PDF text layer without OCR.

| Source | Pages | Native-text words | Markdown words | SHA-256 |
| --- | ---: | ---: | ---: | --- |
| *RouterEval* | 28 | 19,022 | 16,834 | `99cad45397f1b8eaab4ada95260192ceafb9557c216622eaef79c9a135ca0b8d` |
| *The Hidden Cost of Structure* | 11 | 6,785 | 6,406 | `36989889cd257c09ab0c5e746fdba5342d1a04ef509a4786e9eb6b7ec092a7b9` |
| *CiteGuard* | 17 | 9,203 | 7,496 | `9d146239cef435dc5dc392f4be97a5f5b997fbc1bdd996fe003e0d1bfec8ffd0` |
| *I Know What You Asked* | 15 | 13,661 | 13,353 | `b7fc6faf7ac47590f755e6ab8c836f64d3b255547701bce1d86207d292ec525a` |
| *Distilling Many-Shot In-Context Learning into a Cheat Sheet* | 21 | 13,135 | 8,760 | `9593dc38c141c868a0430012979d3d78371dffccecbfe3f2e2f8868235e3fa64` |

## 2026-07-28 — Clean article corpus

- Ran `scripts/extract_theme_articles.py` over the selected set.
- Corrected one NVIDIA Dynamo canonical-path mismatch revealed by the first
  pass, then reran the same deterministic post-processing step.
- Materialized 97 of 97 clean article snapshots in gitignored scratch space.
- Kept source-native Hacker News, Reddit, LinkedIn, and X records beside the
  generic captures; thin generic social pages are never treated as evidence
  when the native record contains the actual post or discussion.
- Preserved low-content warnings for later source audit instead of silently
  promoting weak pages.

## 2026-07-28 — Source-catalog reconciliation

- Reconciled all 98 durable `sources.json` records against the 97 clean
  article-manifest records and source-native social or PDF evidence.
- Replaced machine-derived host, slug, and paper-ID labels with exact,
  independently searchable page or paper titles. Curated Hacker News, X,
  LinkedIn, and Reddit labels were retained where the page itself does not
  expose a more reliable standalone title.
- Rebuilt `source-index.md` as a chapter-grouped catalog with named author or
  publishing organization, canonical link, source class, and explicit
  evidence boundary for every source.
- Kept chapter 19's formerly fused KV-cache evidence as two records:
  `CH19-S06` is the *PromptPeek* attack paper, while `CH19-S02` is the
  subsequent *SafeKV* defense paper. That evidence-preserving split explains
  why the durable catalog contains 98 records while the extraction manifest
  contains 97.
- Corrected four misleading extraction headings from their rendered body
  evidence: the Redis threshold article, the vLLM project announcement, the
  Hugging Face quantization concepts page, and the production model-routing
  article.

Further entries will record chapter evidence, local-agent refinement passes,
gap searches, external-review dispositions, validation, and publication.

## 2026-07-28 — Progressive query control loop

- The broad initial baseline exposed a workflow flaw: large preplanned SERP
  batches collect leads, but they do not let extracted evidence reshape the
  next question.
- Codified a maximum of five reviewed research passes, each containing one to
  three deliberate dated or undated query units. Page one is inspected before
  any new unit/pass; pages two and three require a recorded evidence gap.
- The installed CDP workflow now supports a 30-second minimum navigation-start
  interval and collision-safe dated/undated artifact identities. This browser
  pacing is separate from the required interval spent reading artifacts,
  challenging the current synthesis, and planning the next query.
- Retained first-challenge fast failure: consent, CAPTCHA, authentication,
  unusual-traffic, or bot-check output stops later Google scheduling for human
  clearance. Readiness waits and DOM settle intervals are not described as
  rate-limit cooldowns.
- Updated the repository theme-research skill and the sibling `agents-skills`
  web-research skills to encode the same control loop. No commit or push was
  created.

## 2026-07-28 — Local refinement pass 1: learning progression

- A local reviewer assessed prerequisite order, cumulative mental models,
  analogy limits, exercises, and interview progression across all 22 chapters.
  It did not review technical truth or citations.
- Accepted both blocking findings: inserted an unnumbered minimum-model
  vocabulary interlude before Chapter 4 and operationalized the single
  tenant-aware document assistant as a 22-step artifact ladder.
- Added one capstone increment to every numbered chapter, hosted/self-hosted
  serving tracks, prerequisite-safe reading routes, first-use vocabulary, and
  five part checkpoints.
- Preserved the chapter order and the varied worked examples because the review
  found the conceptual spine sound; the capstone sections now provide the
  cumulative portfolio path.
- Disposition and exact validation evidence are retained in gitignored review
  scratch under `reviews/local/pass-01-disposition.md`.

## 2026-07-28 — Local refinement pass 2: technical evidence

- A local reviewer audited every guide file plus the briefing, source catalog,
  research log, chapter evidence memos, rendered article snapshots, and
  no-OCR PDF text.
- Applied all four required corrections: removed an Andrew Ng attribution
  whose capture contained somebody else's assistant comment; demoted a second
  empty LinkedIn root to discovery-only; grounded the vocabulary interlude in
  foundational primary sources; and separated base model probability,
  sampling policy, and grammar masking.
- Tightened causal-decoder/batch wording, separated post-top-k recall harm from
  conditional metadata leakage, and retained two social records only as
  explicitly bounded, intentionally uncited context.
- The complete finding-by-finding disposition is retained in gitignored
  scratch under `reviews/local/pass-02-disposition.md`.

## 2026-07-28 — Pass 2 progressive gap searches

- Began with one broad, undated foundational-vocabulary query. Its page-one
  results were mostly secondary explainers, so none were promoted. After
  reading that negative result, narrowed the next undated unit to the exact
  titles *Attention Is All You Need*, *Language Models are Unsupervised
  Multitask Learners*, and *Sentence-BERT: Sentence Embeddings using Siamese
  BERT-Networks*. Primary sources closed the three definition gaps; no deeper
  results page was justified.
- Ran a separate dated query covering 2025-01-01 through 2026-07-28 for a
  matched model/hardware/traffic comparison of current inference engines using
  tail latency and goodput. Most page-one candidates were weak or
  incomparable. Retained only Siavashi et al., *Blink: CPU-Free LLM Inference
  by Delegating the Serving Stack to GPU and SmartNIC*, as a bounded example
  of how to audit a benchmark—not as a universal engine ranking.
- Recorded Blink's comparison limits adjacent to its use: an additional
  BlueField-3 DPU, disabled unsupported baseline features, omitted
  cancellation and cost, unreleased code, and placeholder conference
  metadata. These limits closed the teaching gap without opening page two.
- Added four durable source records, bringing the catalog from 98 to 102.
  Reran clean article extraction: 101 of 102 sources have rendered-HTML
  snapshots. The sole HTML miss is the direct GPT-2 PDF, whose acquisition and
  native text-layer extraction are recorded separately.

## 2026-07-28 — Native CDP PDF-to-Markdown smoke

- After the earlier five-PDF acquisition work, the sibling `cdp-cli` gained
  `cdp workflow pdf-to-markdown <local-pdf>`. It uses Poppler's embedded text
  layer, never invokes OCR, emits deterministic page-separated Markdown plus
  metadata and hashes, and returns a typed `text_layer_missing` /
  `ocr_required` result when no usable text layer exists.
- Independently exercised the installed command on the GPT-2 paper. Headed CDP
  opened the exact source and captured the download. A broad force-click first
  timed out because the hit-test landed on the PDF viewer body; an exact
  same-origin download anchor with DOM strategy and `--wait-download`
  succeeded.
- The 582,775-byte PDF has SHA-256
  `d9d852e2894556e73f53cb22b7c605a9643d6f0b19bf604b429ed6192fa24f4e`.
  Native extraction reported 24/24 text-bearing pages, 121,981 characters,
  15,404 words, and `ocr_used: false`. Output and per-page provenance live
  under `pass-02-gap-foundations-exact/pdf-markdown/gpt2/`.
- The earlier log entry remains historically accurate for the initial
  five-PDF batch: at that time the installed build lacked this command and the
  external no-OCR converter was correctly identified as separate.

## 2026-07-28 — Local refinement pass 3: production and security gates

- A local reviewer traced the capstone across authorization, tool execution,
  overload, cancellation, telemetry, retry, cost, and failure-state boundaries.
  It found no P0 issue and no missing-literature requirement; the gap was that
  several well-taught controls were not yet falsifiable release gates.
- Required three-principal isolation tests now distinguish same-tenant
  role/object authorization from cross-tenant separation and carry revocation
  through caches, retrieval/citations, memory, tools, streams, telemetry, and
  queued or retried work.
- Added trusted-registry/schema-digest attacks, malicious tool results,
  cross-server shadowing, confused-deputy calls, approval expiry and mutation,
  and fresh authorization at commit. Ambiguous effects must reconcile.
- Integrated Chapter 6's scheduler evidence into the final benchmark and fault
  campaign. Cancellation now passes through requested and cancelling states;
  bounded queues, load shedding, per-tenant fairness, a global retry budget,
  circuit breakers, cleanup, and degraded UX are tested together.
- Added fail-safe telemetry behavior, secret-canary sink tests, a terminal cost
  accounting matrix, benchmark claim/invalidation boundaries, unambiguous
  pre-ranking RAG authorization, and an explicit limit on what the portfolio
  demonstrates.
- Corrected GrowthBook from `independent-practitioner` to
  `vendor-practitioner` and retained it only as a staged-evaluation/rollout
  checklist. No new Google query was opened because existing local evidence
  supported the design corrections and the next proof is product-local
  testing.
- The finding-by-finding record is retained in gitignored scratch under
  `reviews/local/pass-03-disposition.md`.

## 2026-07-28 — Local refinement pass 4: executable learning and interviews

- A local reviewer read the full guide as an experienced full-stack engineer
  entering AI engineering. It confirmed the non-patronizing ELI5 models,
  chapter progression, cumulative capstone, and searchable citation style, but
  found that learners still had to invent too much test data to compare work.
- Added the canonical `capstone-v1` lab fixture: three principals across two
  tenants, same-tenant disjoint ACLs, four versioned documents, poison and
  tombstone records, typed tool outcomes, a scripted mixed arrival trace,
  numeric thresholds, ten JSONL evaluation cases, safe/unsafe candidates, five
  reusable fault trajectories, and one expected trace/cost join.
- Defined a core submission using deterministic simulation or hosted APIs and a
  stretch submission repeating the same contracts on selected live
  infrastructure. Chapters 18, 19, and 22 now reuse the fixture instead of
  expanding into unrelated test programs.
- Added retrieval practice and a trace/sizing exercise to the mandatory model
  vocabulary interlude. Added a reusable 90-second/five-minute systems
  interview rubric plus calibrated RAG and prompt-injection examples.
- Added observability and outcome economics to the interview deep-read route.
  No new research was needed: this pass repaired exercises and learning
  scaffolding rather than opening a factual gap.
- The finding-by-finding record is retained in gitignored scratch under
  `reviews/local/pass-04-disposition.md`.

## 2026-07-28 — Local refinement pass 5: publication integrity

- The final local reviewer reconciled all 102 catalog records, guide citations,
  chapter contracts, machine-readable examples, local links, and the
  standalone-book sequence. It found no P0 issue and no need for another
  browser research pass.
- Updated the book builder so the canonical capstone fixture is published
  immediately after the guide introduction and before Chapter 1, rather than
  after Chapter 22. A disposable Markdown build confirmed the complete order.
- Normalized affected academic citations to retain both cataloged author or
  organization identity and exact searchable titles in an offline ebook.
- Corrected `CH13-S05` from an implied root-post claim to the Lukas Walter and
  Elliot One comment-thread evidence actually captured. The unavailable root
  body is not treated as confirmation of its title or as prevalence evidence.
- Replaced the fixture's pseudo-enum tool response with valid committed,
  not-committed, and unknown JSONL examples; supplied the stable `e-08`
  receipt; and clarified that provider 429 is a variation inside the fifth
  trajectory group.
- The finding-by-finding record is retained in gitignored scratch under
  `reviews/local/pass-05-disposition.md`.

## 2026-07-28 — Source audit gate

- `uv run python scripts/validate_research.py` passed with
  `Validated 9 research theme(s).`
- Confirmed the 102-source mix: 42 primary-research, 5 official-documentation,
  3 official-standard, 5 security-authority, 16 official-practitioner,
  1 implementation-source, 7 independent-practitioner, 8
  vendor-practitioner, 8 community-signal, and 7 native-social-signal records.
  The guide keeps skeptical benchmark limits, vendor incentives, and
  practitioner counter-signals adjacent to contested claims.
- Confirmed 25 guide files and 39,475 words, with substantive numbered
  chapters, inline canonical links, and no uncredited source image dependency.
- Confirmed that the briefing treats Google snippets as discovery leads only;
  the log records headed extraction, native HN/Reddit/LinkedIn/X/arXiv
  workflows, post-processing, limitations, and explicit SERP depth.
- Confirmed that all catalog URLs are canonical: no Google wrappers or
  `ved`/`ei`/`usg` tracking metadata. The lifecycle log contains no unattended
  daemon start, restart, keepalive, or active-browser-probe command.

## 2026-07-28 — Independent ChatGPT review and disposition

- After the five bounded local refinement passes, uploaded one safe review ZIP
  to each of two independent ChatGPT conversations. The 173,969-byte archive
  had SHA-256
  `6a0df2e3405c293325df3a170fe6fb2afabe9048836b2611719e4461177ac9aa`;
  it contained durable theme files and the publisher, not authenticated
  browser state or raw capture evidence.
- The independent learning-progression review returned `REVISE`, with no P0. It
  validated all 23 ELI5 openings, the non-patronizing tone, retrieval
  mechanisms, repetition, citation labels, and catalog consistency. Its P1
  findings were unsafe focused-route dependencies, an unconditional
  quantization artifact, and an overloaded notion of “core.”
- The independent technical/publication review returned `REVISE`, with no P0. Its
  P1 findings were underspecified deterministic serving/cost gates, a combined
  stale-authorization/acknowledgement-loss case, a vacuous egress assertion,
  conflated authorization and approval states, and publication links/source
  evidence being stripped from the ebook.
- Disposition: revised the default and focused routes; made Chapter 8's
  quantization output conditional; defined study core, portfolio core, and
  live stretch; expanded the minimum vocabulary with decoding policy; and
  consolidated retrieval practice onto the canonical fixture.
- Superseded `capstone-v1` with machine-readable `capstone-v2`: a pinned virtual
  engine, eleven expanded arrivals, isolated baseline, faults, eleven
  evaluation cases, deterministic maxima, live-only p95 policy, exact pricing,
  fake zero-byte egress sink, actual JSON Schema positives/negatives, expected
  events, and golden ledger. Split stale authority into `e-09a` and lost
  acknowledgement into `e-09b`; approval can never grant missing authority.
- Corrected `CH09-S05` to Harsh Shuddhalwar / Cadence and synchronized explicit
  author-or-organization metadata into all 102 JSON records. The source page
  identifies May 22, 2026; the evidence boundary remains practitioner
  synthesis.
- Reworked the publisher to retain stable chapter anchors, append the
  searchable source index, and embed small machine fixtures as offline code
  appendices. Added explicit-theme, all-theme, combined, all-plus-combined, and
  EPUB internal-link tests. The reviewers' ZIP-root warning was not applied:
  inspection showed it was a false positive rather than a publication defect.
- Full reviewer outputs and finding-level disposition notes remain in
  gitignored scratch under `reviews/external/`; the durable log records only
  decisions and reproducible identifiers.

## 2026-07-28 — Final publication, audit, and Kindle handoff

- Post-disposition source audit passed with 102 canonical sources in the same
  labelled mix, 25 guide Markdown files, 40,396 words, 102 inline external
  guide links, zero Google wrappers/tracking parameters, synchronized
  author-or-organization metadata, and no unattended browser lifecycle action.
- All 27 repository unit tests passed. The actual publication contained 25
  stable chapter-file anchors, all 102 source rows, the complete
  machine-readable fixture appendix, and no unresolved local Markdown link.
  Both EPUB variants had valid ZIP structure, expected metadata and text, 208
  rendered external URL occurrences, and zero broken internal references
  across 1,693 direct-EPUB and 1,124 compatibility-EPUB checks.
- Generated Markdown, direct EPUB, MOBI, and Kindle-compatibility EPUB under
  gitignored `tmp/books/09-production-llm-systems-engineering/`. The direct
  Pandoc EPUB was selected for Send to Kindle because it is the source-faithful
  artifact rather than the lossy EPUB-to-MOBI-to-EPUB derivative.
- Sent exactly
  `09-production-llm-systems-engineering.epub`, SHA-256
  `d4d1e79f86af5dd0667cfe04ee028fae9f7bd4d7618ae205b1f37b5c2ac92699`,
  through the authenticated headed Amazon.in page. The exact backend request
  returned HTTP 200 and the page displayed “Your files are on the way.”
  Submission state: `acknowledged`. The task-created tab closed successfully;
  no delivery/conversion claim is made beyond Amazon's acknowledgement.

## 2026-07-28 — Cross-repository learning capture and final integration proof

- Updated `cdp-cli` with collision-safe dated/undated SERP artifact identities,
  cancellable per-engine `--navigation-delay`, progressive Google examples,
  and a browser-free `workflow pdf-to-markdown` command that uses only
  Poppler's embedded text layer and fails closed when OCR would be required.
- Proved the installed PDF workflow against the headed-browser-acquired
  structured-decoding paper: 11/11 pages, 6,785 words, source SHA-256
  `36989889cd257c09ab0c5e746fdba5342d1a04ef509a4786e9eb6b7ec092a7b9`,
  `browser_used: false`, and `ocr_used: false`.
- Updated the shared `dev-browser`, `search-web`, and
  `research-web-critical` skills with topic-fit evidence horizons, paired
  evergreen/dated queries, 1–3 query units per reviewed pass, a five-pass
  ceiling, native 30-second navigation pacing, reasoning reviews between
  invocations, first-block stop behavior, source-native HN reads, and the new
  PDF extraction boundary.
- Updated `ask-agents`, `cdp-cli`, and `agent-cli-web` with the same bounded
  ChatGPT terminal-no-answer recovery: inspect the exact acknowledged
  conversation, use any late answer, and otherwise continue that conversation
  once after it is proved terminal. A fresh ask or duplicate upload is not a
  recovery.
- Validation passed in all affected repositories: research validation and
  27/27 tests; `cdp-cli` full verify, installed E2E, demo E2E, help/schema
  checks, and leak scan; `agent-cli-web` tests, vet, install, and installed E2E
  with the exact 11-tab set preserved; shared-skill validation, installation,
  ten scanner regression tests, and a 52-skill scan with zero blockers.
  The four repo-local skills also scan with zero blockers; the two remaining
  `rsync` warnings are explicitly guarded, human-only examples. All four
  worktrees pass `git diff --check`.

## 2026-07-29 — Reader-owned Kindle canvas

- A device review found that the direct EPUB looked like a slightly gray page
  inset inside Kindle's own page. Inspection traced this to Pandoc's default
  EPUB CSS: `background-color: #fdfdfd`, a fixed Georgia body font and
  foreground color, and a 10-pixel `@page` margin.
- Replaced that default with the neutral `scripts/theme_book_epub.css`
  contract, following the established FreshRSS ebook behavior: zero
  book-defined page/document margins, transparent canvas, and no forced body
  font or foreground color. Kindle now owns its theme, font, and spacing.
- Added an integration regression that opens the generated EPUB and checks its
  packaged CSS. The full suite passes with 44 tests, all nine themes validate,
  and the rebuilt direct EPUB passes ZIP integrity.
- Rendered the rebuilt EPUB and a current FreshRSS Kindle EPUB with the same
  Paperwhite profile and 18-point reader margin. Six deterministic Theme 09
  samples showed a plain reader canvas without a nested tinted page.
- Rebuilt the local direct EPUB as SHA-256
  `bed172f534ca00ec19c0087b29effd9ebcab9056c1af4355498b6c2818a58e01`.
  This corrected artifact has not been submitted to Send to Kindle.
