# Source index

_Last refreshed: 2026-05-07_

This index summarizes the evidence base for the hosted open-weight coding API guide. The machine-readable list is in [sources.json](sources.json) with 81 sources. Raw rendered pages and extracted article Markdown live under `tmp/research-web-critical/02-hosted-open-weight-coding-llm-apis/` and are intentionally not committed.

## Source quality legend

- **official** — model owner, API owner, official docs, official repository, or policy page.
- **vendor** — hosted provider pricing, routing, benchmark, or product pages.
- **benchmark** — independent or semi-independent benchmark/leaderboard pages.
- **practitioner** — field reports, technical blog posts, or expert commentary.
- **community** — HN, Reddit, local social archive, GitHub search signals.
- **paper** — technical report/preprint.

Google SERP snippets were used only for discovery. Final guide claims use extracted pages and source-linked content.

## Highest-priority official model sources

| Source | Quality | Why it matters |
|---|---|---|
| [Qwen3-Coder: Agentic Coding in the World](https://qwenlm.github.io/blog/qwen3-coder/) | official | Primary Qwen3-Coder launch source: 480B/35B active MoE, 256K native context, 1M extrapolation, agentic coding/tool-use claims, Qwen Code and Claude Code/Cline setup patterns. |
| [QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder) | official | Official repo; confirms Qwen Code ecosystem, function-call/tokenizer/parser caveats, Qwen3-Coder-Next information, and integration details. |
| [Kimi K2.6: Advancing open-source coding](https://www.kimi.com/blog/kimi-k2-6) | official | Primary Kimi K2.6 launch source; claims state-of-the-art coding, long-horizon execution, 4,000+ tool-call examples, and agent swarm behavior. |
| [MoonshotAI/Kimi-K2](https://github.com/MoonshotAI/Kimi-K2) | official | Official Kimi K2 repo; describes the 1T total / 32B active MoE line, agentic intelligence focus, license, and technical links. |
| [DeepSeek API docs: models and pricing](https://api-docs.deepseek.com/quick_start/pricing) | official | DeepSeek direct pricing/context/features; V4 Flash/Pro 1M context and 384K max output; OpenAI/Anthropic-compatible endpoints. |
| [DeepSeek privacy policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html) | official | Critical risk source: input collection, retention, training/improvement use, and China processing/storage language. |
| [Meta Llama 4 model page](https://www.llama.com/models/llama-4/) | official | Llama 4 model-family context for long-context open model candidates. |
| [Qwen3-Coder-Next blog](https://qwen.ai/blog?id=qwen3-coder-next), [tech report](https://arxiv.org/html/2603.00729v1), [HF card](https://huggingface.co/Qwen/Qwen3-Coder-Next) | official / paper | Follow-on Qwen line; useful for future refreshes and local/cheaper agentic coding options. |

## Provider pricing/context sources

| Source | Quality | Key data used |
|---|---|---|
| [OpenRouter Qwen3-Coder](https://openrouter.ai/qwen/qwen3-coder) | vendor | 262K context, `$0.22/M` input, `$1.80/M` output, provider-route context/max-output/uptime hints. |
| [OpenRouter Kimi K2.6](https://openrouter.ai/moonshotai/kimi-k2.6) | vendor | 262K context, `$0.75/M` input, `$3.50/M` output, provider-route variation. |
| [OpenRouter DeepSeek V3.1](https://openrouter.ai/deepseek/deepseek-chat-v3.1) and [V3.1 Terminus](https://openrouter.ai/deepseek/deepseek-v3.1-terminus) | vendor | Gateway-hosted DeepSeek price/context routes: 32K and 164K-class endpoints in captured pages. |
| [OpenRouter Llama 4 Maverick](https://openrouter.ai/meta-llama/llama-4-maverick) and [Scout](https://openrouter.ai/meta-llama/llama-4-scout) | vendor | 1M-class Maverick route and provider variation for Scout; cheap long-context control. |
| [OpenRouter GPT-5.5](https://openrouter.ai/openai/gpt-5.5) and [Claude Opus 4.7](https://openrouter.ai/anthropic/claude-opus-4.7) | vendor | Cross-provider baseline price/context snapshot and provider entries. |
| [DeepInfra pricing](https://deepinfra.com/pricing) | vendor | Qwen3-Coder 256K `$0.30/$1.00`, Llama 4 Maverick 1024K `$0.15/$0.60`, Scout 320K `$0.08/$0.30`, and other hosted open models. |
| [Together pricing](https://www.together.ai/pricing) and model pages | vendor | Alternative provider route for Qwen, Kimi, DeepSeek, Llama; useful for refresh and provider comparison. |
| [Fireworks pricing](https://fireworks.ai/pricing) | vendor | Alternative route/pricing for Llama, DeepSeek, Kimi; useful when provider speed/reliability matters. |
| [Groq pricing](https://groq.com/pricing) | vendor | Fast-inference pricing for hosted open models; useful for latency-sensitive experiments. |
| [Cerebras pricing](https://www.cerebras.ai/pricing) and [model overview](https://inference-docs.cerebras.ai/models/overview) | vendor | High-speed hosted inference pricing; Qwen3-Coder route at higher price but potentially much faster. |
| [OpenRouter models API](https://openrouter.ai/api/v1/models) | official/vendor API | Machine-readable snapshot source for model IDs, context length, and pricing. Local snapshot stored under `tmp/`. |

## Provider privacy/routing sources

| Source | Quality | Key data used |
|---|---|---|
| [OpenRouter data collection and privacy](https://openrouter.ai/docs/guides/privacy/data-collection) | vendor | Prompts/responses not stored unless optional logging/product-improvement opt-ins are enabled; metadata retained. |
| [OpenRouter provider logging and zero data retention](https://openrouter.ai/docs/guides/privacy/provider-logging) | vendor | Provider-by-provider retention/training table; confirms policies vary and routing/provider controls matter. |
| [OpenRouter ZDR](https://openrouter.ai/docs/guides/features/zdr) | vendor | Account/request-level ZDR controls and meaning of zero data retention. |
| [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection) | vendor | Provider selection, fallback, sorting, ignored providers, data-policy routing. |
| [OpenRouter privacy policy](https://openrouter.ai/privacy) | vendor | Broader policy context beyond API docs. |
| [DeepInfra data privacy](https://docs.deepinfra.com/account/data-privacy) | vendor | Key direct-provider privacy evidence: inputs/outputs not stored to disk, memory-only during inference, no training except documented exceptions. |
| [DeepInfra privacy policy](https://deepinfra.com/privacy) | vendor | Broader service privacy policy for DeepInfra. |
| [OpenAI enterprise privacy](https://openai.com/enterprise-privacy/) | official | Baseline enterprise privacy reference; not deeply evaluated in this theme. |

## Baseline frontier model sources

| Source | Quality | Key data used |
|---|---|---|
| [OpenAI GPT-5.5 announcement](https://openai.com/index/introducing-gpt-5-5/) | official | Official positioning and vendor benchmark claims for GPT-5.5. |
| [OpenAI GPT-5.5 model docs](https://developers.openai.com/api/docs/models/gpt-5.5) | official | 1,050,000 context, 128,000 max output, long-context surcharge above 272K input, regional processing uplift. |
| [OpenAI API pricing](https://openai.com/api/pricing/) | official | GPT-5.5 `$5/M` input, `$0.50/M` cached input, `$30/M` output. |
| [Anthropic Opus product page](https://www.anthropic.com/claude/opus) | official | Baseline Opus positioning. |
| [Anthropic Opus 4.7 announcement](https://www.anthropic.com/news/claude-opus-4-7) | official | Opus 4.7 coding/agentic claims and `$5/$25` unchanged pricing statement. |
| [Claude pricing docs](https://platform.claude.com/docs/en/about-claude/pricing) | official | Claude model pricing and regional/US-only inference multipliers. |
| [Claude Opus 4.7 docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7) | official | 1M context, 128K max output, tokenizer/token-count caveat, effort/task-budget guidance. |

## Benchmark and measurement sources

| Source | Quality | Key data used |
|---|---|---|
| [Aider LLM leaderboards](https://aider.chat/docs/leaderboards/) | benchmark | Coding/editing benchmark: 225 polyglot tasks, percent correct, cost, edit-format conformance. Used to emphasize editing reliability, not just chat quality. |
| [Aider OpenRouter docs](https://aider.chat/docs/llms/openrouter.html) | benchmark/tool docs | Evidence that OpenRouter routes are usable in coding-agent workflows. |
| [SWE-bench leaderboards](https://www.swebench.com/) | benchmark | Real GitHub issue resolution; captured leaderboard showed strong closed baselines and competitive Kimi/DeepSeek-family entries under mini-SWE-agent. |
| [Vals LiveCodeBench](https://www.vals.ai/benchmarks/lcb) | benchmark | Fresh competitive coding benchmark; captured page listed DeepSeek V4 and Kimi K2.6 as competitive with frontier closed models. |
| [LiveBench](https://livebench.ai/) | benchmark | General benchmark reference for changing model landscape. |
| [Artificial Analysis Qwen3-Coder provider benchmark](https://artificialanalysis.ai/models/qwen3-coder-480b-a35b-instruct/providers) | benchmark | Provider variance: price, speed, latency, JSON/function-calling dimensions. |
| [Artificial Analysis Llama 4 Maverick providers](https://artificialanalysis.ai/models/llama-4-maverick/providers) | benchmark | Provider variance for cheap long-context Llama routes. |
| [Artificial Analysis Kimi K2.6](https://artificialanalysis.ai/models/kimi-k2-6) | benchmark | Independent-ish model page for Kimi intelligence/speed/price/context tracking. |
| [Artificial Analysis API providers leaderboard](https://artificialanalysis.ai/leaderboards/providers) | benchmark | Provider-level latency/speed/price tracking. |
| [DeepInfra Qwen3-Coder API benchmark](https://deepinfra.com/blog/qwen3-coder-480b-a35b-api-benchmarks) | vendor benchmark | Provider comparison for Qwen3-Coder: blended price, TTFT, throughput, JSON-mode caveats. |

## Practitioner and community sources

| Source | Quality | Key data used |
|---|---|---|
| [Braw.dev field report: reallocating Claude Code spend to Zed and OpenRouter](https://braw.dev/blog/2026-04-06-reallocating-100-month-claude-spend/) | practitioner | Direct practitioner signal that developers are moving fixed coding-agent spend into OpenRouter/open-model experiments. |
| [DeepLearning.AI The Batch issue 351](https://www.deeplearning.ai/the-batch/issue-351/) | practitioner | Broader weekly AI/coding news context around GPT-5.5 and Kimi K2.6. |
| [16x Eval: DeepSeek-V3.1 coding performance](https://eval.16x.engineer/blog/deepseek-v3-1-coding-performance-evaluation) | practitioner | Practitioner benchmark/evaluation view on DeepSeek coding performance. |
| [Interconnects: Kimi K2 and DeepSeek moments](https://www.interconnects.ai/p/kimi-k2-and-when-deepseek-moments) | practitioner | Expert commentary on open-model market dynamics; useful context, not primary evidence. |
| [HN Qwen3-Coder announcement](https://news.ycombinator.com/item?id=44653072) | community | High-engagement practitioner discussion lead for Qwen3-Coder. |
| [HN Kimi K2.6 discussion](https://news.ycombinator.com/item?id=47835735) | community | High-engagement discussion lead for Kimi K2.6. |
| [HN open-weight coding challenge claim](https://news.ycombinator.com/item?id=47993235) | community | Contested/social signal around claims that Kimi beat Claude/GPT/Gemini in a coding challenge. |
| [HN Claude spend to OpenRouter discussion](https://news.ycombinator.com/item?id=47700972) | community | Practitioner-spend and reliability sentiment around OpenRouter. |
| [OpenRouter State of AI](https://openrouter.ai/state-of-ai) | vendor/community | OpenRouter usage/ecosystem report; useful for route/popularity context. |
| [HN Algolia API](https://hn.algolia.com/api/v1/search) | community/API | Used for repeatable HN story/comment discovery across model/provider queries. |
| Local `socli` Reddit signal | community | Local social archive evidence around OpenRouter/open-model routing discussion; raw artifact under `tmp/`. |

## GitHub implementation sources

GitHub was used both as a primary source for official repos and as a community signal for tool integration.

| Source | Role |
|---|---|
| [QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder) | Official model repo and integration docs. |
| [MoonshotAI/Kimi-K2](https://github.com/MoonshotAI/Kimi-K2) | Official model repo and technical links. |
| [MoonshotAI/Kimi-K2.5](https://github.com/MoonshotAI/Kimi-K2.5) | Official newer Kimi line / technical report source. |
| [deepseek-ai/DeepSeek-V3](https://github.com/deepseek-ai/DeepSeek-V3) | Official DeepSeek open-weight repo and ecosystem signal. |
| [Aider-AI/aider](https://github.com/Aider-AI/aider) | Mature terminal coding-agent project and benchmark source. |
| [anomalyco/opencode](https://github.com/anomalyco/opencode) | Open-source coding-agent ecosystem/provider-flexibility signal. |
| [simonw/llm-openrouter](https://github.com/simonw/llm-openrouter) | OpenRouter integration plugin for Simon Willison’s `llm` tool. |
| [fakerybakery/openbridge](https://github.com/fakerybakery/openbridge) | Claude Code bridge for alternative providers like Kimi, Qwen, DeepSeek. |
| [florath/qwen3-call-patch-proxy](https://github.com/florath/qwen3-call-patch-proxy) | Small but important compatibility signal around Qwen tool calls in OpenCode. |

## Coverage gaps

- Direct legal/privacy terms for every provider route (Fireworks, Together, Groq, Cerebras) were not deeply audited beyond pricing and OpenRouter provider logging summaries.
- Actual user-run latency/reliability data is not yet available; this guide proposes a one-week protocol to collect it.
- Kimi K2.6 hands-on evidence is still vendor-heavy relative to Qwen/DeepSeek/older Kimi benchmarks.
- GPT-5.5 and Opus 4.7 were treated as expensive baselines from official docs; this theme did not run live API comparisons.
- Local/self-hosted inference was out of scope except where GitHub/HN signals mentioned it.

## Refresh priority

Before buying credits or running the evaluation, refresh these first:

1. OpenRouter model API/model pages for Qwen, Kimi, DeepSeek, Llama, GPT-5.5, Opus.
2. OpenRouter provider logging/ZDR docs.
3. DeepInfra pricing/privacy.
4. DeepSeek pricing/privacy.
5. Aider/SWE-bench/LiveCodeBench latest pages.
6. HN/OpenRouter outage/support/social signals.
