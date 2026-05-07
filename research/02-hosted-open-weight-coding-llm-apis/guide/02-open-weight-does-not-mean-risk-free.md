# 02 — What “open weight” buys you, and what it does not

## The core confusion

People often say “open source model” when they mean three different things:

1. the **weights are downloadable**;
2. the **license permits some commercial use**;
3. the **hosted API is safe to send private code to**.

Those are not the same. A model can publish weights while the hosted endpoint still logs prompts. A model can be cheap while the provider stores data in a jurisdiction you cannot use. A provider can say it does not train on prompts while still retaining them for abuse monitoring. A route can be zero-retention for one provider but not another provider of the same model. For coding-agent users, the provider layer matters as much as the model layer because the payload is your codebase, logs, stack traces, architecture, and sometimes secrets.

The safest mental model is a stack:

```text
Your repository and prompts
        ↓
Coding-agent harness: tools, diff format, test runner, retries
        ↓
API gateway or direct provider: OpenRouter, DeepInfra, Together, Fireworks, Groq, Cerebras, DeepSeek, Alibaba
        ↓
Hosted model implementation: quantization, context cap, tool parser, cache, rate limit
        ↓
Model weights and license: Qwen, Kimi, DeepSeek, Llama, etc.
```

Open weights live at the bottom. Privacy and reliability failures often happen in the middle.

## What open weights actually buy you

Open weights can still be extremely valuable. They create competition. They let multiple providers host the same or similar model. They make it possible for provider prices to collapse from Opus/GPT-level dollars to cents per million tokens. They allow on-prem or self-hosted deployment if the workload justifies it. They let the community inspect model cards, licenses, and sometimes technical reports.

Qwen3-Coder is a useful example. Qwen’s launch page says Qwen3-Coder-480B-A35B-Instruct is a 480B-parameter MoE model with 35B active parameters, 256K native context, and 1M context with extrapolation; it is explicitly framed for agentic coding, tool use, and repository-scale work ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)). The GitHub repository and model-card ecosystem make the model visible to many providers and tools ([QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder)). That openness is why you can try Qwen through Alibaba, OpenRouter, DeepInfra, Together, and others instead of only one vendor.

Kimi K2.6 is another example. Moonshot’s Kimi page says Kimi K2.6 is open-sourced and available via Kimi.com, the API, Kimi Code, and model weights; the launch claims state-of-the-art coding, long-horizon execution, and agent swarm capabilities ([Kimi K2.6](https://www.kimi.com/blog/kimi-k2-6)). The Kimi K2 repository describes the older K2 line as a 1T-total-parameter MoE with 32B active parameters and 128K context for K2 Instruct ([MoonshotAI/Kimi-K2](https://github.com/MoonshotAI/Kimi-K2)). Again, the openness creates multiple access paths.

DeepSeek and Llama demonstrate a third advantage: open models pressure frontier pricing. DeepSeek’s current API pricing page advertises 1M context and very low per-million-token rates for V4 Flash/Pro ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)). Meta’s Llama 4 pages emphasize open models with large context and multimodal capabilities ([Llama 4](https://www.llama.com/models/llama-4/)). When hosted providers compete on these weights, input prices like `$0.08–$0.30/M` become common for some open-weight routes.

## What open weights do not buy you

### They do not guarantee privacy

The strongest counterexample is DeepSeek direct. The price/context story is excellent: 1M context, 384K max output, and V4 Flash at $0.14/M cache-miss input and $0.28/M output ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)). But the privacy policy says DeepSeek collects user input such as prompts, uploaded files, chat history, and other content; uses data to improve and train technology; retains personal data for service, legal, and business purposes; and stores/processes personal data in the People’s Republic of China ([DeepSeek privacy policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)). That may be fine for public or redacted work. It is not the same as a zero-retention inference endpoint.

OpenRouter’s provider-logging docs show why this distinction matters. The same marketplace can include providers with zero retention, providers that retain prompts for 30 days, providers with unknown retention, and providers that may train on prompts. OpenRouter’s table marks DeepInfra, Fireworks, Together, Groq, Cerebras, Moonshot AI, and many others as zero-retention by default, while DeepSeek is listed as “prompts retained for unknown period” and “may train” ([OpenRouter provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging)). This does not mean every DeepSeek model route is unusable. It means you must know which endpoint you are using.

### They do not guarantee the advertised context window on every API

Model cards may say one thing; provider endpoints may expose another. Qwen says Qwen3-Coder has 256K native context and can extend to 1M with YaRN ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)). OpenRouter’s Qwen3-Coder page lists 262,144 context and provider entries around 262.1K total context with 65.5K max output for common routes ([OpenRouter Qwen3-Coder](https://openrouter.ai/qwen/qwen3-coder)). DeepInfra’s pricing page lists Qwen3-Coder-480B-A35B-Instruct-Turbo at 256k context ([DeepInfra pricing](https://deepinfra.com/pricing)). Those are good windows, but they are not the same as a guaranteed 1M API window.

Llama 4 is similar. Meta’s Llama materials emphasize very large context windows ([Llama 4](https://www.llama.com/models/llama-4/)), and OpenRouter lists Llama 4 Maverick at 1,048,576 context ([OpenRouter Llama 4 Maverick](https://openrouter.ai/meta-llama/llama-4-maverick)). But OpenRouter’s provider entries for Llama 4 Scout show variation: one route has 327.7K context, another 131.1K, and another 1.31M ([OpenRouter Llama 4 Scout](https://openrouter.ai/meta-llama/llama-4-scout)). “The model supports X” is not the same as “the provider you called gave you X.”

### They do not guarantee tool-calling compatibility

A coding agent is not just a chatbot. It needs stable function calling, structured outputs, file edits, command results, and sometimes provider-specific reasoning modes. Qwen’s own docs warn that Qwen3-Coder function calling relies on newer parsers in SGLang and vLLM, with updated special tokens and token IDs in the repository README ([QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder)). That is a normal model-integration detail, but it matters. If your coding harness expects OpenAI-style tools and the provider’s parser is slightly off, you can lose the value of a strong model.

The GitHub search surfaced small compatibility projects like `qwen3-call-patch-proxy`, described as an HTTP proxy that fixes malformed Qwen3-Coder tool calls for OpenCode ([GitHub search artifact in research log](../research-log.md)). A 36-star proxy is not proof of a systemic failure, but it is a useful warning: agentic coding quality depends on the entire harness, not just benchmark scores.

### They do not guarantee reliability

Provider pages often show “recent uptime,” but that is not a contract. OpenRouter model pages expose recent uptime per provider route; for example, the captured pages showed different recent uptime values across DeepSeek/Qwen/Kimi/Llama routes ([OpenRouter Qwen3-Coder](https://openrouter.ai/qwen/qwen3-coder), [OpenRouter DeepSeek V3.1](https://openrouter.ai/deepseek/deepseek-chat-v3.1)). OpenRouter also documents provider routing and fallbacks, including routing to providers that can handle prompt size and parameters ([OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)). That helps, but it also means a request can silently move across providers unless you pin or constrain it.

Reliability for coding work has at least five dimensions:

- **availability:** does the request succeed?
- **latency:** does the agent wait too long and time out?
- **throughput:** can it generate long diffs at useful speed?
- **schema fidelity:** do tool calls parse correctly?
- **behavioral stability:** does the model stop looping and finish tasks?

A provider can be available but fail schema fidelity. A model can be cheap but so slow that the agent becomes unusable. A model can pass a benchmark but hallucinate local APIs in your codebase.

## The provider-policy triangle

When choosing a hosted open-weight API, evaluate three policy questions independently:

### 1. Who stores prompts and outputs?

OpenRouter says it does not store prompts or responses unless you opt into private input/output logging or OpenRouter use of inputs/outputs, and it stores request metadata such as token counts and latency ([OpenRouter data collection](https://openrouter.ai/docs/guides/privacy/data-collection)). DeepInfra says it does not store inputs or outputs to disk for inference, holds them in memory while processing, and deletes them after inference ([DeepInfra data privacy](https://docs.deepinfra.com/account/data-privacy)). DeepSeek’s privacy policy says inputs may be collected and retained ([DeepSeek privacy policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)).

These are materially different answers.

### 2. Who trains on prompts?

OpenRouter’s provider-logging table distinguishes retention from training. Some providers do not train but retain data. Some are zero-retention. Some may train. OpenRouter says users can opt out of routing to providers that train on prompts and can require providers to comply with data policies ([OpenRouter provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging)). DeepInfra says it does not train on your API data except for Google/Anthropic model exceptions where the receiving company’s policy applies ([DeepInfra data privacy](https://docs.deepinfra.com/account/data-privacy)). DeepSeek says users may have a right to opt out of training/optimization, but also describes using data to improve and train technology ([DeepSeek privacy policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)).

For private coding work, “does not train” is necessary but not sufficient. Retention can still be unacceptable.

### 3. Where is processing routed?

OpenRouter can route across providers, and its docs explain provider selection, ignored providers, sorting, and data-policy constraints ([OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)). It also supports EU in-region routing for enterprise customers according to the provider-logging docs ([OpenRouter provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging)). DeepSeek says it stores/processes personal data in China ([DeepSeek privacy policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)). Anthropic and OpenAI have separate data residency or regional processing pricing paths; Anthropic docs mention a 1.1x multiplier for US-only inference on Opus 4.7 and newer models ([Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing)), and OpenAI pricing references data residency/regional processing ([OpenAI pricing](https://openai.com/api/pricing/)).

The region question is often ignored in hobby benchmarks. It should not be ignored for company code.

## The practical policy matrix

Use this matrix before sending a repository:

| Workload | Acceptable model/provider policy | Recommended route |
|---|---|---|
| Public OSS issue | Any provider allowed by project policy; no secrets | Cheapest useful route, including DeepSeek direct or OpenRouter free/cheap routes |
| Private hobby repo | No prompt training; retention acceptable if you personally accept it | OpenRouter with provider filters; DeepInfra direct; avoid secrets |
| Startup proprietary code | Zero retention preferred; no training; spend cap; provider allowlist | OpenRouter ZDR + pinned DeepInfra/Fireworks/Together, or DeepInfra direct |
| Client/regulatory code | Contractual approval, data processing terms, region, audit | Do not use ad-hoc open-weight providers without legal/security approval |
| Security vulnerabilities | Treat as sensitive; avoid providers with unknown retention | Use approved enterprise endpoints or local/on-prem where possible |

This is deliberately stricter than many online posts. The point of a one-week evaluation is to learn cheaply, not to accidentally leak your product.

## How open-weight economics can still be worth it

The price gap is real. OpenAI’s official GPT-5.5 pricing page lists `$5/M` input and `$30/M` output ([OpenAI pricing](https://openai.com/api/pricing/)). Claude Opus 4.7 is `$5/M` input and `$25/M` output ([Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing)). In contrast, OpenRouter lists Qwen3-Coder at `$0.22/M` input and `$1.80/M` output ([OpenRouter Qwen3-Coder](https://openrouter.ai/qwen/qwen3-coder)), Kimi K2.6 at `$0.75/M` input and `$3.50/M` output ([OpenRouter Kimi K2.6](https://openrouter.ai/moonshotai/kimi-k2.6)), DeepSeek V3.1 Terminus at `$0.27/M` input and `$0.95/M` output ([OpenRouter DeepSeek Terminus](https://openrouter.ai/deepseek/deepseek-v3.1-terminus)), and Llama 4 Maverick at `$0.15/M` input and `$0.60/M` output ([OpenRouter Llama 4 Maverick](https://openrouter.ai/meta-llama/llama-4-maverick)).

That gap means open-weight APIs can be economically transformative even if they only handle part of the workflow. A cheap model can read a large repo, draft tests, classify issues, summarize logs, or attempt a first patch. Then a frontier model can review or complete the hard cases. This is often better than an all-or-nothing replacement question.

## The rule to remember

Open weights answer: **Can many people run this model?**

A safe hosted API answers: **What happens to my code when I send it?**

A good coding-agent route answers: **Can this model, through this provider, inside this harness, repeatedly ship correct diffs under my budget and policy constraints?**

Your one-week evaluation should test the third question.
