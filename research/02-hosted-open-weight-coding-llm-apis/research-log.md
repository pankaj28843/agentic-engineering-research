# Research log: Hosted open-weight coding LLM APIs

_Last updated: 2026-05-07_

## Research question

Which hosted open-weight / open-source coding and development model APIs are worth evaluating for one week as cheaper alternatives or complements to Claude Opus and GPT-5.5, with special attention to:

- cheap and predictable `$ / 1M` token pricing;
- actual usable input context length, not only headline context;
- safety/privacy/data retention;
- provider reliability and routing;
- coding-agent usefulness versus Opus/GPT baselines.

## Workflow used

This theme followed the repository’s `theme-deep-research` / `research-web-critical` workflow:

1. Read local research skills and repository validation requirements.
2. Confirmed CDP daemon health with the allowed command:

   ```bash
   cdp daemon status --json
   ```

3. Created scratch workspace:

   ```text
   tmp/research-web-critical/02-hosted-open-weight-coding-llm-apis/
   ```

4. Ran Google SERP batches for model/provider/pricing/privacy/benchmark queries.
5. Queried HN Algolia for Qwen, Kimi, DeepSeek, OpenRouter, open-weight coding models, Aider leaderboards, and Claude Code/open-model terms.
6. Ran GitHub searches/probes for official repos and compatibility tools.
7. Queried OpenRouter’s model API and saved a local snapshot.
8. Extracted selected official/vendor/benchmark/community pages via CDP into `tmp/.../pages/`.
9. Post-processed extracted pages with:

   ```bash
   uv run python scripts/extract_theme_articles.py research/02-hosted-open-weight-coding-llm-apis/sources.json \
     --pages-dir tmp/research-web-critical/02-hosted-open-weight-coding-llm-apis/pages \
     --out-dir tmp/research-web-critical/02-hosted-open-weight-coding-llm-apis/articles
   ```

10. Wrote durable guide files under `research/02-hosted-open-weight-coding-llm-apis/`.

## Scratch artifacts

Key artifacts under `tmp/research-web-critical/02-hosted-open-weight-coding-llm-apis/`:

- `queries-batch1.txt`, `queries-batch2.txt`
- `candidates-batch1.json`, `candidates-batch2.json`
- `batch1/candidates.tsv`, `batch2/candidates.tsv`
- `serp-summary-batch1.json`, `serp-summary-batch2.json`
- `hn-*-stories.json`, `hn-*-comments.json`, `hn-stories.tsv`
- `github-search.md`, `github-official.md`
- `openrouter-model-snapshot.json`
- `socli-openrouter-kimi.json`
- `pages/` rendered CDP captures
- `articles/` post-processed article Markdown
- `articles/manifest.json`

`tmp/` is intentionally gitignored and should not be committed.

## SERP batches

All three Google SERP batches used `result_pages: 3`, `query_count: 10`, `max_candidates: 250`, `serp: google`, and completed with `failure_count: 0` according to the saved `serp-summary-batch*.json` files.

### Batch 1

Covered core model/provider queries:

- Qwen3-Coder hosted API pricing/context;
- Kimi K2/K2.6 coding model API pricing/context;
- DeepSeek V3/V3.1/V4 pricing/context;
- OpenRouter privacy/ZDR/provider routing;
- DeepInfra pricing/privacy;
- open-weight coding model benchmarks;
- Aider/SWE-bench/LiveCodeBench.

Output summary: `serp-summary-batch1.json` reported `ok: true` with no failures.

### Batch 2

Covered additional provider and baseline queries:

- GPT-5.5 pricing/context;
- Claude Opus pricing/context;
- Fireworks/Together/Groq/Cerebras pricing;
- provider reliability/privacy docs;
- Kimi/Qwen newer reports;
- OpenRouter outage/support/social signals.

Output summary: `serp-summary-batch2.json` reported successful candidate collection.

### Batch 3

Covered follow-up sources after initial synthesis:

- Qwen3-Coder-Next official/model-card/report sources;
- missing baseline/provider pages;
- benchmark/provider pages that needed direct extraction;
- additional social/practitioner leads.

Output summary: `serp-summary-batch3.json` reported 250 candidates across 10 queries, 3 result pages, and 0 failures.

## HN research

Queried HN Algolia for:

- `qwen3-coder`
- `kimi-k2`
- `deepseek-coding`
- `openrouter`
- `deepinfra`
- `open-weight-coding-model`
- `aider-leaderboard`
- `claude-code-open-source-model`

Important leads from `hn-stories.tsv`:

| Points/comments | Query | Title | URL |
|---:|---|---|---|
| 936 / 427 | kimi-k2 | Kimi K2 Thinking, a SOTA open-source trillion-parameter reasoning model | https://moonshotai.github.io/Kimi-K2/thinking.html |
| 765 / 366 | qwen3-coder | Qwen3-Coder: Agentic coding in the world | https://qwenlm.github.io/blog/qwen3-coder/ |
| 735 / 429 | qwen3-coder | Qwen3-Coder-Next | https://qwen.ai/blog?id=qwen3-coder-next |
| 710 / 372 | kimi-k2 | Kimi K2.6: Advancing open-source coding | https://www.kimi.com/blog/kimi-k2-6 |
| 388 / 141 | kimi-k2 | Kimi K2.5 Technical Report | https://github.com/MoonshotAI/Kimi-K2.5/blob/master/tech_report.pdf |
| 349 / 234 | openrouter | Reallocating $100/Month Claude Code Spend to Zed and OpenRouter | https://braw.dev/blog/2026-04-06-reallocating-100-month-claude-spend/ |
| 207 / 95 | openrouter | State of AI: An Empirical 100T Token Study with OpenRouter | https://openrouter.ai/state-of-ai |
| 46 / 27 | openrouter | OpenRouter is down | https://status.openrouter.ai |

HN was used as social/practitioner signal and link discovery, not as factual proof. Claims in the guide cite primary sources or extracted pages.

## GitHub research

Saved to `tmp/.../github-official.md` and `tmp/.../github-search.md`.

Important official/tool repositories:

| Repo | Stars at capture | Updated at capture | Role |
|---|---:|---|---|
| [QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder) | 16,497 | 2026-05-07 | Official Qwen3-Coder repo and integration docs. |
| [MoonshotAI/Kimi-K2](https://github.com/MoonshotAI/Kimi-K2) | 10,747 | 2026-05-07 | Official Kimi K2 repo. |
| [MoonshotAI/Kimi-K2.5](https://github.com/MoonshotAI/Kimi-K2.5) | 1,930 | 2026-05-07 | Kimi K2.5 tech report/model source. |
| [deepseek-ai/DeepSeek-V3](https://github.com/deepseek-ai/DeepSeek-V3) | 103,422 | 2026-05-07 | Official DeepSeek open-weight repo. |
| [Aider-AI/aider](https://github.com/Aider-AI/aider) | 44,469 | 2026-05-07 | Coding-agent benchmark/tool source. |
| [anomalyco/opencode](https://github.com/anomalyco/opencode) | 156,360 | 2026-05-07 | Open-source coding-agent ecosystem. |
| [simonw/llm-openrouter](https://github.com/simonw/llm-openrouter) | 344 | 2026-05-07 | OpenRouter integration plugin. |
| [fakerybakery/openbridge](https://github.com/fakerybakery/openbridge) | 386 | 2026-04-28 | Claude Code bridge for alternative providers. |
| [florath/qwen3-call-patch-proxy](https://github.com/florath/qwen3-call-patch-proxy) | 36 | 2026-04-10 | Compatibility signal for Qwen tool calls in OpenCode. |

GitHub API issue encountered and fixed: `gh search` rejected JSON field `comments`; the correct field is `commentsCount`.

## OpenRouter API snapshot

Queried `https://openrouter.ai/api/v1/models` and saved `openrouter-model-snapshot.json` under `tmp/`.

Key values observed in the snapshot/pages:

| Model | Context | Input $/1M | Output $/1M | Notes |
|---|---:|---:|---:|---|
| `qwen/qwen3-coder` | 262K | 0.22 | 1.80 | Cheap coding candidate. |
| `moonshotai/kimi-k2.6` | 262K | 0.75 | 3.50 | Hard open-weight coding candidate. |
| `deepseek/deepseek-chat-v3.1` | 32K | 0.15 | 0.75 | Cheap but shorter gateway route. |
| `deepseek/deepseek-v3.1-terminus` | 164K | 0.27 | 0.95 | Better gateway context. |
| `meta-llama/llama-4-maverick` | ~1.05M | 0.15 | 0.60 | Cheap long-context control. |
| `meta-llama/llama-4-scout` | 327K headline in common route | 0.08 | 0.30 | Cheap, but provider context varies. |
| `openai/gpt-5.5` | ~1.05M | 5.00 | 30.00 | Official docs add long-context surcharge above 272K input. |
| `anthropic/claude-opus-4.7` | ~1M | 5.00 | 25.00 | Expensive baseline. |

These values are time-sensitive. Refresh before buying credits.

## Article extraction

`sources.json` contains 81 sources. CDP extraction summary files show 76 pages extracted successfully in the main pass and 3 Qwen-fix pages extracted successfully in the follow-up pass, with 0 extraction failures in both CDP summaries. `scripts/extract_theme_articles.py` post-processing succeeded for 78/81 sources after fixing Qwen3-Coder-Next source metadata.

Representative extracted article paths:

- `tmp/.../articles/qwenlm-github-io-blog-qwen3-coder/article.md`
- `tmp/.../articles/www-kimi-com-blog-kimi-k2-6/article.md`
- `tmp/.../articles/api-docs-deepseek-com-quick-start-pricing/article.md`
- `tmp/.../articles/cdn-deepseek-com-policies-en-us-deepseek-privacy-policy-html/article.md`
- `tmp/.../articles/openrouter-ai-docs-guides-privacy-data-collection/article.md`
- `tmp/.../articles/openrouter-ai-docs-guides-features-zdr/article.md`
- `tmp/.../articles/openrouter-ai-qwen-qwen3-coder/article.md`
- `tmp/.../articles/aider-chat-docs-leaderboards/article.md`
- `tmp/.../articles/www-swebench-com/article.md`
- `tmp/.../articles/www-vals-ai-benchmarks-lcb/article.md`

## Key source-backed findings

### Qwen3-Coder

Official Qwen source says Qwen3-Coder-480B-A35B-Instruct is a 480B MoE with 35B active parameters, 256K native context, and 1M with extrapolation; it is built for agentic coding and tool use ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)). The official GitHub repo highlights Qwen Code, Cline/Claude Code support, function-call format, and parser/tokenizer caveats ([QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder)).

### Kimi K2.6

Official Kimi source frames Kimi K2.6 as open-source coding focused, with long-horizon execution and agent swarm capabilities ([Kimi K2.6](https://www.kimi.com/blog/kimi-k2-6)). Evidence remains vendor-heavy and should be tested locally.

### DeepSeek

DeepSeek direct pricing is exceptionally low and lists V4 Flash/Pro with 1M context and 384K max output ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)). Privacy policy is the major caveat: data collection, retention, training/improvement use, and China processing/storage language ([DeepSeek privacy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)).

### OpenRouter

OpenRouter docs say prompts/responses are not stored unless optional logging/product-improvement settings are enabled; metadata is stored ([OpenRouter data collection](https://openrouter.ai/docs/guides/privacy/data-collection)). ZDR and provider routing controls are documented ([OpenRouter ZDR](https://openrouter.ai/docs/guides/features/zdr), [provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)). Provider logging policies vary by endpoint/provider ([OpenRouter provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging)).

### DeepInfra

DeepInfra says inference inputs/outputs are not stored to disk, prompts are not used for training, and data is held only in memory during inference, with exceptions for Google/Anthropic and some other flows ([DeepInfra data privacy](https://docs.deepinfra.com/account/data-privacy)). Its pricing makes it a strong direct-provider backup ([DeepInfra pricing](https://deepinfra.com/pricing)).

### Baselines

OpenAI GPT-5.5 official pricing is `$5/M` input, `$0.50/M` cached input, and `$30/M` output ([OpenAI pricing](https://openai.com/api/pricing/)). GPT-5.5 docs list 1,050,000 context and 128,000 max output, with 2x input and 1.5x output pricing for sessions above 272K input tokens ([GPT-5.5 docs](https://developers.openai.com/api/docs/models/gpt-5.5)). Anthropic Opus 4.7 is `$5/M` input and `$25/M` output, with 1M context and 128K max output in docs; tokenizer/effort settings can affect token usage ([Anthropic Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7), [Claude docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7)).

## Current recommendation rationale

OpenRouter is recommended as the minimal one-week front door because it reduces setup friction and supports provider routing/privacy controls. DeepInfra is recommended as direct backup because of clearer inference privacy docs. Direct DeepSeek is recommended only for public/redacted tasks because price/context are excellent but privacy posture is higher-risk. Kimi, Qwen, DeepSeek, and Llama are assigned different roles rather than treated as one generic “open model” bucket.

## Validation command

Before commit/finalization, run:

```bash
uv run python scripts/validate_research.py
```

If validation fails, fix structure/metadata/guide depth before final handoff.

## Source audit note — 2026-05-07

Ran `uv run python scripts/validate_research.py`; validation passed for 2 research themes. Source mix includes official model/provider docs, provider pricing/privacy pages, independent benchmark pages, practitioner reports, HN/social signals, GitHub implementation probes, and skeptical counter-evidence around privacy/routing/provider reliability. `guide/` contains numbered source-linked chapters and no local image assets. `sources.json` URLs were checked for Google redirect/tracking parameters (`ved`, `ei`, `usg`, `google.com/url`, text-fragment wrappers); none were found. CDP daemon lifecycle in this log is limited to the permitted `cdp daemon status --json` check.
