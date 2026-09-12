# Research log: Smart LLM Routing

## Scope and date

This packet was researched and audited on **2026-09-12** in the Europe/Copenhagen
timezone. The question was how a large regulated enterprise can choose among
deterministic handlers, managed APIs, coding-assistant products, and in-house
open-weight services while measuring quality, authority, latency, and total
accepted-outcome economics.

The research target was durable mechanisms plus current provider facts. Current
prices, names, capabilities, availability, and release dates are treated as
volatile. The packet cites an official dated page for every such claim and does
not use the unresolved labels Astra, OASIS, DeepSeek Flash, GPT-5.6 Luna, or
Fable as if their identity were known.

## Browser method

All live pages, including Hacker News and native social pages, were read with
headed CDP. The permitted unattended daemon check was:

```text
cdp daemon status --json
```

It reported a usable running headed browser. The headed page probe was:

```text
cdp --browser-mode headed pages --json
```

The collection used bounded concurrency and a single result page per Google
pass. Search snippets and rendered Google summaries were candidate leads only;
the selected page was opened and its rendered content captured before it could
be used as evidence. No direct HTTP collector was used.

## Reviewed discovery passes

The work stopped after four productive passes, below the five-pass ceiling.
Each pass was reviewed before the next one was used.

| Pass | Query families | Depth and result | Decision |
|---|---|---|---|
| 01 | LLM routing and cascading; model selection cost quality; routing papers; practitioner accounts; community discussions | One Google result page; 31 candidates plus a targeted page-2 lane recorded in its own scratch directory | Kept broad mechanism, paper, practitioner, and HN leads; excluded snippets as evidence |
| 02 | official AWS/Bedrock routing, pricing, caching, batch, model customization, and GitHub/Copilot availability | One Google result page; 20 official candidates | Added primary pricing, policy, product, and changelog pages; retained redirect failures in the ledger |
| 03 | model/provider capability pages, open-weight serving, local TCO, inference cost, benchmark surfaces | One Google result page; 37 candidates | Added official provider pages, vLLM/SGLang, FinOps, benchmark, and counter-evidence lanes |
| 04 | Mistral/primary model pages; production routing failure evidence; routing cost and latency; regulated governance | One Google result page; 3/3 productive queries; no block, consent, CAPTCHA, or auth signal | Stopped discovery; used only targeted official URLs to close extraction gaps |

Pass 04 query strings were:

- `site:mistral.ai OR site:docs.mistral.ai model pricing open weights enterprise 2026`
- `LLM routing production postmortem cache miss quality regression gateway cost Pragmatic Engineer`
- `EU AI Act generative AI model monitoring logging audit third party providers enterprise governance 2026`, constrained to the explicit 2026-06-20 through 2026-09-12 date window.

The complete visited URL list is [visit-urls.txt](../../tmp/research-web-critical/10-smart-llm-routing/visit-urls.txt).
Pass reviews and candidate records remain under
`tmp/research-web-critical/10-smart-llm-routing/pass-01/` through `pass-04/`.

## Capture and extraction accounting

The selected set contained 81 URLs. The main headed capture produced 78 page
records: 71 passed the quality gate, seven failed it, and three collector
errors were recorded. The seven quality failures received exactly one
timing-only retry using the same headed workflow, body selector, useful-content
readiness checks, and thresholds, with `--wait 30s --settle 4s`. Four recovered
and three remained rejected or bounded context. No second retry was run.

The raw evidence is under
`tmp/research-web-critical/10-smart-llm-routing/`, including:

- `extract-summary.json` — main batch summary;
- `pages/page-quality.json` — per-page quality outcomes;
- `pages/failures.json` and `pages/failed-urls.txt` — failed lanes;
- `pages/retry-01/` — the four recovered captures and three failed retry lanes;
- `source-selection-ledger.md` — selection, retry, rejection, and
  evidence-to-change record;
- `source-index.json` — explicit retry and same-identity redirect mappings.

The four recovered pages were the Sean Geng routing guide, Tian Pan cascade
article, Klique technical deep dive, and Augment token-spend analysis. The
remaining SSRN page rendered security verification, the selected Facebook
Financial Times URL redirected to an unrelated video, and the Uptime Institute
URL rendered a site shell. TrueFoundry's first URL and two LinkedIn URLs were
collector-error lanes. These are recorded, not silently promoted.

Clean article post-processing used the repository script:

```text
uv run python scripts/extract_theme_articles.py research/10-smart-llm-routing --scratch-root tmp/research-web-critical/10-smart-llm-routing
```

It produced 70 article snapshots from the 75 retained records. The five
missing clean snapshots are the AWS intelligent-prompt-routing documentation,
AWS model-customization pricing, Mistral technology, Llama API, and Thoughtworks
zero-cost article. Their final pages were generic or identity-mismatched. The
raw captures remain available for audit, and no durable claim depends on them.

## Practitioner and community signals

The native HN and social collection is summarized in
`tmp/agents/smart-routing/practitioner-social.md`. HN links were opened through
headed CDP; native Reddit and X surfaces were blocked or shell-only under the
available browser conditions, and LinkedIn records did not provide reliable
post evidence. The retained signals suggest hypotheses about category/workflow
routing, router overhead, gateway ownership, utilization, privacy, and hidden
local-serving costs. They are self-selected anecdotes with unknown prevalence.
They are used to design failure drills and measurement questions, never as
causal ROI or market-share evidence.

## Independent review

The local review and distinct provider asks are recorded in
`tmp/agents/smart-routing/ask-agents.md` and
`tmp/agents/smart-routing/ask-agents/local-review.md`. Five distinct provider
lanes were attempted where the harness exposed them: Claude, Perplexity,
Grok, Gemini, and ChatGPT. Claude returned a substantive critique. Perplexity
was dispatched once but ended with an unacknowledged submission failure and no
text. Grok, Gemini, and ChatGPT failed in pre-dispatch readiness/cleanup lanes;
ChatGPT capability remained unverified and was not resubmitted. The full
results, attempts, and failed lanes are retained. Agreement among reviewers is
treated as correlated advice, not proof.

Accepted design constraints include deterministic policy ownership of identity,
residency, authorization, budgets, and tool eligibility; immutable route
registry pins; idempotency and indeterminate-effect handling; reserved
classifier and worker budgets; tenant- and policy-aware cache keys; an
acceptance-rate floor against a fixed baseline; an explicit Copilot scope
matrix; and closed fallback sets for residency-sensitive traffic. Vendor “up
to” percentages, token price alone, an LLM authorization decision, free-form
route discovery, generic cross-boundary fallback, and consensus-as-proof were
rejected.

## Synthesis decisions

The guide uses the following evidence hierarchy:

1. official and regulatory sources establish documented product, price,
   capability, or governance facts as of their linked date;
2. papers and independent benchmarks establish bounded measurements with the
   named workload and method;
3. practitioner and vendor accounts provide implementation mechanisms and
   local results with incentives stated;
4. HN and social sources provide attributed anecdotes and falsifiable questions;
5. architecture, formulas, SLO examples, and rollout rules are proposals until
   replay, shadow, canary, security, reliability, and rollback gates pass.

The synthesis favors a deterministic `R0 → R1 → (R2) → R3 → W → V1 → (A1) → O1`
path. A router may select only from an eligible enum set. Cost is joined to the
accepted business outcome, including failed attempts, evaluator work,
platform capacity, and material human rework. Current provider pages are
lookup points, not timeless constants.

## Limitations and stop conditions

This is an evidence-backed design packet, not production validation. No
enterprise workload replay, shadow run, canary, live cost ledger, provider
contract review, or real side-effect reconciliation was executed. The source
mix is broad but not a random sample. Vendor pages have incentives, papers may
use benchmark distributions unlike this enterprise, and community evidence is
self-selected. The five identity-mismatched page lanes and unavailable native
social surfaces reduce coverage in those specific areas. Those limits are
visible in the source index and are part of the decision record.

The packet must not declare a routing policy successful until the fixed baseline
ladder, stratified acceptance tests, data-boundary checks, latency tails,
capacity reservations, cache isolation, outcome-cost reconciliation, failure
injection, and explicit rollback gates have been run.

## Audit note

Source-audit completed on 2026-09-12. `uv run python
scripts/validate_research.py` passed with 10 themes. The packet contains 75
unique HTTPS source records, with 27 official-primary, 14 primary-research, 14
vendor-practitioner, 11 independent-practitioner, three official-practitioner,
and bounded benchmark, observatory, product-changelog, and community records.
The guide contains 14 numbered chapters and 24,687 words by `wc -w`; every
numbered chapter has inline HTTPS evidence, ELI5 framing, mechanism, worked
example, failure drill, exercises, checkpoint, and source slot. The article
manifest records 75 selected sources, 70 successful clean snapshots, and five
unavailable identity or site-shell lanes; the raw captures and failure records
remain under `tmp/`.

The canonical-URL check found no Google redirect wrappers or tracking
parameters in the durable packet or source index. The daemon-command check
found no forbidden start, restart, stop, keepalive, or active-browser-probe
command in the research artifacts. The source-index generation error was
removed before this final pass. The packet remains design-only: no production
replay, shadow, canary, provider-contract review, or side-effect reconciliation
has been claimed as completed.
