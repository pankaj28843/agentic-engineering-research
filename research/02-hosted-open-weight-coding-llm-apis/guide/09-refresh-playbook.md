# 09 — Refresh playbook for keeping this guide alive

## Why this guide must be living

Hosted LLM API guidance expires quickly. Prices change, context caps change, provider retention policies change, model aliases move, routing behavior changes, benchmarks update, and community sentiment shifts after outages or surprise releases. A recommendation that is responsible today can be wrong in a month.

This chapter explains how to refresh the theme without turning it into a pile of stale snippets.

## Refresh cadence

Use three refresh levels.

### Light refresh: before a one-week trial

Time: 30–60 minutes.

Refresh:

- OpenRouter model pages/API for shortlisted models;
- DeepInfra pricing and privacy;
- DeepSeek pricing and privacy;
- OpenAI/Anthropic baseline pricing;
- OpenRouter provider logging/ZDR docs;
- one benchmark page (Aider or SWE-bench);
- one HN/social search for outages or recent model releases.

Update:

- price/context tables;
- provider-safety notes;
- one-week roster.

### Medium refresh: monthly

Time: half day.

Refresh:

- all provider pricing pages;
- all official model pages;
- benchmark pages;
- HN and GitHub searches;
- OpenRouter API snapshot;
- source-index and sources.json.

Update:

- guide chapters with changed claims;
- source-index quality labels;
- research-log with new queries and extraction stats.

### Deep refresh: when a major model launches

Time: one or more days.

Trigger examples:

- new Qwen/Kimi/DeepSeek/Llama coding model;
- new Claude/GPT baseline;
- provider privacy policy change;
- major OpenRouter/DeepInfra outage or pricing shift;
- user completes a one-week evaluation and has local results.

Update:

- model shortlist;
- price/context matrix;
- evaluation protocol outcomes;
- recommendation in README/briefing;
- sources.json with new primary sources;
- guide chapters if the conclusion changes.

## Refresh commands

Repository validation:

```bash
uv run python scripts/validate_research.py
```

Equivalent:

```bash
make validate
```

CDP daemon guard, per repository instructions:

```bash
cdp daemon status --json
```

Do not start/restart/stop the daemon without explicit human approval in the current turn.

## Source collection checklist

For each important claim, prefer this order:

1. official model/provider docs;
2. official pricing/API pages;
3. independent benchmark pages;
4. provider benchmark pages;
5. GitHub repos/issues;
6. HN/social signals;
7. news/blog commentary.

Google SERP snippets are leads only. Do not cite snippets as evidence. Extract pages into `tmp/` and write source-grounded claims.

## Suggested search queries

Use Google/CDP or ordinary web search depending on tool availability.

### Model queries

```text
Qwen3-Coder 480B context pricing OpenRouter DeepInfra
Qwen3-Coder Next agentic coding benchmark
Kimi K2.6 coding model context API pricing
Kimi K2.6 SWE-bench LiveCodeBench
DeepSeek V4 API pricing context 1M
DeepSeek V3.1 Terminus OpenRouter context price
Llama 4 Maverick API pricing context coding benchmark
```

### Provider queries

```text
OpenRouter zero data retention provider logging
OpenRouter model API qwen kimi deepseek llama pricing
DeepInfra data privacy inference not stored
DeepInfra Qwen3-Coder benchmark
Fireworks Qwen3 Coder pricing
Together Kimi Qwen DeepSeek pricing
Groq Llama 4 pricing
Cerebras Qwen3 Coder pricing
```

### Baseline queries

```text
Claude Opus 4.7 pricing context max output coding
GPT-5.5 pricing context long context surcharge
OpenAI GPT-5.5 API pricing 272K surcharge
Anthropic Opus 4.7 tokenizer 1M context
```

### Benchmark/community queries

```text
Aider leaderboard Qwen Kimi DeepSeek Opus GPT
SWE-bench Kimi DeepSeek Qwen Claude Opus GPT
LiveCodeBench DeepSeek V4 Kimi K2.6
Artificial Analysis Qwen3 Coder provider benchmark
Hacker News Qwen3-Coder
Hacker News Kimi K2.6
Hacker News OpenRouter outage pricing privacy
```

## OpenRouter API refresh

Use OpenRouter’s public model API to capture a machine-readable snapshot. Example:

```bash
curl -s https://openrouter.ai/api/v1/models \
  | jq '[.data[] | select(.id | test("qwen3-coder|kimi-k2.6|deepseek|llama-4-maverick|gpt-5.5|claude-opus")) | {
      id,
      name,
      context_length,
      pricing,
      top_provider,
      created
    }]'
```

Save the output under `tmp/research-web-critical/02-hosted-open-weight-coding-llm-apis/openrouter-model-snapshot-YYYY-MM-DD.json`. Do not commit large snapshots unless they are curated into `sources.json` or a small table.

Important fields:

- `id`;
- `context_length`;
- prompt/completion pricing;
- top provider context/output if exposed;
- model aliases/new versions.

Then update [04-price-context-matrix.md](04-price-context-matrix.md).

## CDP extraction flow

When doing a medium/deep refresh:

1. Confirm daemon status only:

   ```bash
   cdp daemon status --json
   ```

2. Run Google searches and save SERP candidates under `tmp/`.
3. Select primary/benchmark/provider/community URLs.
4. Extract rendered pages into `tmp/research-web-critical/<slug>/pages/`.
5. Update `sources.json` with source metadata.
6. Run article post-processing:

   ```bash
   uv run python scripts/extract_theme_articles.py research/02-hosted-open-weight-coding-llm-apis/sources.json \
     --pages-dir tmp/research-web-critical/02-hosted-open-weight-coding-llm-apis/pages \
     --out-dir tmp/research-web-critical/02-hosted-open-weight-coding-llm-apis/articles
   ```

7. Write guide changes from extracted article content, not snippets.
8. Run validation.

## Updating sources.json

Each source should include enough metadata for audit. Use the existing schema style from this theme and the validation script. Recommended fields:

```json
{
  "id": "openrouter-qwen3-coder",
  "title": "OpenRouter model page: Qwen3-Coder",
  "url": "https://openrouter.ai/qwen/qwen3-coder",
  "publisher": "OpenRouter",
  "source_type": "provider_pricing",
  "quality": "vendor",
  "role": "pricing_context",
  "accessed": "2026-05-07",
  "notes": "Context, input/output price, provider routes."
}
```

Use quality labels consistently:

- `official` for model/provider docs controlled by the creator;
- `vendor` for provider pages and pricing/benchmark pages;
- `benchmark` for independent or semi-independent benchmark pages;
- `community` for HN/GitHub/social;
- `policy` for privacy/data-retention docs;
- `news` for press/reporting.

## Updating price/context tables

When changing prices, update three locations:

1. [briefing.md](../briefing.md) executive table;
2. [04-price-context-matrix.md](04-price-context-matrix.md);
3. [source-index.md](../source-index.md) if a new source is used.

For each model route, capture:

```text
model id:
provider:
context length:
max output:
input price per 1M:
cache-hit input price per 1M, if any:
output price per 1M:
privacy/retention note:
source URL:
accessed date:
```

Always distinguish **advertised total context** from **practical input budget**.

## Updating provider/privacy claims

Privacy claims are high-risk. Do not paraphrase from memory. Re-read the current docs.

Check:

- Does provider store prompts?
- Does provider store outputs?
- Does provider train on prompts?
- Are there exceptions?
- Is metadata stored?
- Does routing go to third parties?
- Are there region/data-residency options?
- Does the policy apply to API or only chat product?

For OpenRouter, re-check:

- [data collection](https://openrouter.ai/docs/guides/privacy/data-collection);
- [ZDR](https://openrouter.ai/docs/guides/features/zdr);
- [provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging);
- [provider routing](https://openrouter.ai/docs/guides/routing/provider-selection).

For DeepInfra, re-check [data privacy](https://docs.deepinfra.com/account/data-privacy).

For DeepSeek, re-check [privacy policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html) and [pricing/API page](https://api-docs.deepseek.com/quick_start/pricing).

## Updating benchmark claims

For benchmark pages, record both score and context:

- benchmark name;
- task type;
- harness;
- date/version;
- model name and mode;
- score;
- cost if reported;
- why it matters;
- limitation.

Examples:

- Aider is useful for editing/diff conformance but not full repo architecture ([Aider leaderboards](https://aider.chat/docs/leaderboards/)).
- SWE-bench Verified uses real GitHub issues and mini-SWE-agent for model comparison ([SWE-bench](https://www.swebench.com/)).
- LiveCodeBench is strong for competitive-programming freshness but not repo-agent behavior ([Vals LiveCodeBench](https://www.vals.ai/benchmarks/lcb)).
- Artificial Analysis and DeepInfra provider benchmarks are useful for latency/provider variance ([Artificial Analysis Qwen providers](https://artificialanalysis.ai/models/qwen3-coder-480b-a35b-instruct/providers), [DeepInfra Qwen benchmark](https://deepinfra.com/blog/qwen3-coder-480b-a35b-api-benchmarks)).

Do not conflate benchmark families. A model that wins LiveCodeBench may still be poor at tool calling.

## Incorporating local evaluation results

After the user completes the one-week trial, add a new file:

```text
research/02-hosted-open-weight-coding-llm-apis/evaluations/YYYY-MM-DD-one-week-trial.md
```

Suggested structure:

```markdown
# One-week hosted open-weight coding API evaluation — YYYY-MM-DD

## Environment

## Provider settings

## Data policy

## Tasks

## Results table

## Cost summary

## Reliability summary

## Accepted roles

## Rejected routes

## Next actions
```

Then update:

- README one-sentence takeaway if needed;
- briefing verdict;
- guide Chapter 01 and Chapter 07 with outcome notes;
- sources.json only if local evaluation is included as an internal source.

## Validation before committing

Run:

```bash
uv run python scripts/validate_research.py
```

The validation script checks theme structure, required files, source metadata, guide chapter count, and guide word count. This theme should keep at least eight guide chapters and a substantial word count. If you add a new guide chapter, update [guide/00-README.md](00-README.md).

## Anti-staleness rules

- Never leave a price without an accessed date in sources.json.
- Never say “best” without naming benchmark/task/provider.
- Never cite HN or social as factual proof without following the linked source.
- Never collapse model and provider into one label.
- Never recommend direct DeepSeek for private code without repeating the privacy caveat.
- Never compare GPT-5.5 long-context cost without checking the 272K surcharge.
- Never assume Qwen/Kimi 1M context unless the specific hosted route exposes it.
- Never call provider uptime an SLA unless the provider contract says it is.

## Future questions to research

- Are Kimi K2.6 and Qwen3-Coder stable under very long tool-call loops in real coding agents?
- Which provider route has the best accepted-patch-per-hour for Qwen3-Coder?
- Does Llama 4 Maverick provide enough code understanding to serve as a cheap whole-repo reader?
- Is DeepSeek V4 Flash’s quality good enough for public OSS bug fixing at scale?
- How do OpenRouter ZDR/provider filters affect latency and availability?
- Can a local/self-hosted route beat hosted APIs for privacy-sensitive medium-size tasks?
- Which coding-agent harness handles open-weight tool calling most reliably?

## Bottom line

This guide should evolve from market research into operational evidence. The first version says where to start. The next version should say what happened when you actually ran the week.
