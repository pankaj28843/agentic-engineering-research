# 04 — Price and actual context matrix

## Read this before the table

“Context length” can mean at least three things:

1. **Model-card context:** what the model architecture/training claims can support.
2. **Provider total context:** what a hosted endpoint allows for input plus output.
3. **Practical input budget:** how much input you should send after reserving room for output, tool results, and retries.

For coding agents, the third number matters most. A model with “262K context” is not a 262K-input model if you need 20K–60K tokens of output, tool traces, and patch text. A model with “1M context” can still become expensive or unreliable when you actually fill it.

The table below uses official/provider pages extracted on 2026-05-07. Prices change quickly; refresh before buying credits.

## Snapshot: key routes and normalized prices

| Model / route | Source | Reported context | Max output when found | Practical input budget for coding | Input $/1M | Output $/1M | Notes |
|---|---|---:|---:|---:|---:|---:|---|
| Qwen3-Coder 480B A35B via OpenRouter | [OpenRouter Qwen3-Coder](https://openrouter.ai/qwen/qwen3-coder) | 262,144 | common provider entries: 65.5K | ~180K–220K | 0.22 | 1.80 | Headline model price; provider entries vary. |
| Qwen3-Coder 480B Turbo via DeepInfra | [DeepInfra pricing](https://deepinfra.com/pricing) | 256K | not clearly listed on pricing page | ~180K–220K | 0.30 / 0.10 cached | 1.00 | Very strong value if DeepInfra route works for your agent. |
| Kimi K2.6 via OpenRouter | [OpenRouter Kimi K2.6](https://openrouter.ai/moonshotai/kimi-k2.6) | 262,144 | provider entries vary: 16.4K to 262K | ~200K–240K | 0.75 | 3.50 | More expensive than Qwen/DeepSeek but plausible harder-task candidate. |
| DeepSeek V4 Flash direct | [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) | 1M | 384K | ~600K–950K depending output reserve | 0.14 cache miss / 0.0028 cache hit | 0.28 | Extremely cheap; privacy policy is the blocker for sensitive code. |
| DeepSeek V4 Pro direct | [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) | 1M | 384K | ~600K–950K | 0.435 discounted, 1.74 standard | 0.87 discounted, 3.48 standard | Discount was listed as extended until 2026-05-31 15:59 UTC. |
| DeepSeek V3.1 Terminus via OpenRouter | [OpenRouter Terminus](https://openrouter.ai/deepseek/deepseek-v3.1-terminus) | 163,840 | common provider entry: 32.8K | ~120K–140K | 0.27 | 0.95 | Safer OpenRouter/provider-filterable route than direct DeepSeek, but shorter context. |
| Llama 4 Maverick via OpenRouter | [OpenRouter Llama 4 Maverick](https://openrouter.ai/meta-llama/llama-4-maverick) | 1,048,576 | common provider entry: 16.4K | ~900K+ for read tasks; less for patch tasks | 0.15 | 0.60 | Great long-context price; not proven best coder. |
| Llama 4 Maverick via DeepInfra | [DeepInfra pricing](https://deepinfra.com/pricing) | 1024K | not clearly listed on pricing page | ~900K+ | 0.15 | 0.60 | Cheap long-context route with DeepInfra privacy stance. |
| Claude Opus 4.7 | [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing), [Opus docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7) | 1M | 128K | ~850K–900K | 5.00 | 25.00 | New tokenizer can use ~1x–1.35x as many tokens as Opus 4.6. |
| GPT-5.5 | [OpenAI pricing](https://openai.com/api/pricing/), [GPT-5.5 docs](https://developers.openai.com/api/docs/models/gpt-5.5) | 1,050,000 | 128K | ~900K; docs imply 922K input + 128K output | 5.00 under 272K; 10.00 above 272K | 30.00 under 272K; 45.00 above 272K | Long-context surcharge applies to full session above 272K input. |

## Price ratios against Opus/GPT

Use ratios carefully. A model that is 30x cheaper but fails half the tasks is not 30x better. Still, the raw economics explain why this market matters.

| Route | Input vs `$5/M` Opus/GPT | Output vs `$25/M` Opus | Output vs `$30/M` GPT-5.5 |
|---|---:|---:|---:|
| Qwen3-Coder OpenRouter `$0.22/$1.80` | 22.7x cheaper | 13.9x cheaper | 16.7x cheaper |
| Qwen3-Coder DeepInfra `$0.30/$1.00` | 16.7x cheaper | 25x cheaper | 30x cheaper |
| Kimi K2.6 `$0.75/$3.50` | 6.7x cheaper | 7.1x cheaper | 8.6x cheaper |
| DeepSeek V4 Flash `$0.14/$0.28` | 35.7x cheaper | 89.3x cheaper | 107.1x cheaper |
| DeepSeek V3.1 Terminus `$0.27/$0.95` | 18.5x cheaper | 26.3x cheaper | 31.6x cheaper |
| Llama 4 Maverick `$0.15/$0.60` | 33.3x cheaper | 41.7x cheaper | 50x cheaper |

These ratios are why a tiered workflow is attractive. You do not need Kimi/Qwen/DeepSeek to beat Opus on every task. You need them to handle enough work that Opus/GPT are reserved for the hard cases.

## Example costs for real coding-agent shapes

### Shape A: medium patch

Assume a coding agent sends 200K input tokens and receives 10K output tokens. This is a realistic “read a moderate subsystem, produce a patch, include tool traces” run.

| Route | Calculation | Approx cost |
|---|---|---:|
| Qwen3-Coder OpenRouter | `0.2×0.22 + 0.01×1.80` | `$0.062` |
| Qwen3-Coder DeepInfra | `0.2×0.30 + 0.01×1.00` | `$0.070` |
| Kimi K2.6 | `0.2×0.75 + 0.01×3.50` | `$0.185` |
| DeepSeek V4 Flash | `0.2×0.14 + 0.01×0.28` | `$0.031` |
| Llama 4 Maverick | `0.2×0.15 + 0.01×0.60` | `$0.036` |
| Claude Opus 4.7 | `0.2×5 + 0.01×25` | `$1.25` |
| GPT-5.5 under 272K | `0.2×5 + 0.01×30` | `$1.30` |

This is the strongest economic case for open-weight coding APIs. A medium patch attempt that costs around `$1.25–$1.30` on Opus/GPT can cost cents on Qwen/DeepSeek/Llama and under 20 cents on Kimi.

### Shape B: large repository read

Assume 600K input and 20K output. Qwen/Kimi 262K routes cannot run this without chunking, so compare 1M-class routes.

| Route | Calculation | Approx cost | Comment |
|---|---|---:|---|
| DeepSeek V4 Flash | `0.6×0.14 + 0.02×0.28` | `$0.090` | Cheap enough for repeated long reads; privacy caveat. |
| Llama 4 Maverick | `0.6×0.15 + 0.02×0.60` | `$0.102` | Cheap long-context control. |
| Claude Opus 4.7 | `0.6×5 + 0.02×25` | `$3.50` | Expensive but high quality. |
| GPT-5.5 above 272K | `0.6×10 + 0.02×45` | `$6.90` | Uses long-context surcharge from GPT-5.5 docs. |

This table explains why long-context triage should not automatically go to GPT-5.5. GPT-5.5 may be better, but at this input size the surcharge makes each large read expensive. Use it when quality matters enough, not as the default file reader.

## Context: model card versus endpoint reality

### Qwen

Qwen’s official page says Qwen3-Coder supports 256K context natively and 1M with YaRN/extrapolation ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)). The Qwen3-Coder-Next repository/material says the Next variant has native 256K and can extend to 1M, with agentic coding focus ([Qwen3-Coder-Next model card](https://huggingface.co/Qwen/Qwen3-Coder-Next)). But OpenRouter and DeepInfra routes captured for the 480B coder are 256K/262K-class endpoints ([OpenRouter Qwen3-Coder](https://openrouter.ai/qwen/qwen3-coder), [DeepInfra pricing](https://deepinfra.com/pricing)).

Practical rule: **budget Qwen for 200K-token-class coding tasks**, not million-token whole-repo dumps, unless a specific provider page shows a 1M Qwen route and you test it.

### Kimi

OpenRouter lists Kimi K2.6 at 262,144 context and `$0.75/$3.50` ([OpenRouter Kimi K2.6](https://openrouter.ai/moonshotai/kimi-k2.6)). The Kimi K2.6 official page emphasizes long-horizon coding and agent swarm behavior more than a simple context number ([Kimi K2.6](https://www.kimi.com/blog/kimi-k2-6)). Older Kimi K2 Instruct model summary lists 128K context ([MoonshotAI/Kimi-K2](https://github.com/MoonshotAI/Kimi-K2)).

Practical rule: **treat Kimi as the hard coding candidate in the 200K-token-class route**, and chunk very large repos.

### DeepSeek

DeepSeek direct V4 is the outlier: 1M context and 384K maximum output in the extracted pricing table ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)). OpenRouter’s V3.1 and V3.1 Terminus routes are much smaller: 32.8K and 163.8K headlines respectively ([OpenRouter DeepSeek V3.1](https://openrouter.ai/deepseek/deepseek-chat-v3.1), [OpenRouter DeepSeek V3.1 Terminus](https://openrouter.ai/deepseek/deepseek-v3.1-terminus)).

Practical rule: **direct DeepSeek is the cheap 1M-context route for non-sensitive work; OpenRouter DeepSeek routes are safer to filter but may have smaller context.**

### Llama

OpenRouter and DeepInfra both show Llama 4 Maverick around 1M context at very low prices ([OpenRouter Llama 4 Maverick](https://openrouter.ai/meta-llama/llama-4-maverick), [DeepInfra pricing](https://deepinfra.com/pricing)). But Llama 4 Scout provider routes vary dramatically on OpenRouter ([OpenRouter Llama 4 Scout](https://openrouter.ai/meta-llama/llama-4-scout)).

Practical rule: **use Llama 4 Maverick for cheap long-context reading experiments; verify coding quality separately.**

### Opus and GPT-5.5

Claude Opus 4.7 docs say it supports 1M context and 128K max output at standard API pricing with no long-context premium, but tokenizer changes can increase token counts ([Claude Opus 4.7 docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7)). GPT-5.5 docs say 1,050,000 context and 128,000 max output, but prompts above 272K input are priced at 2x input and 1.5x output for the full session ([OpenAI GPT-5.5 docs](https://developers.openai.com/api/docs/models/gpt-5.5)).

Practical rule: **Opus is the cleaner expensive 1M coding baseline; GPT-5.5 is a frontier baseline with a long-context pricing cliff.**

## How to estimate your own week

Before the trial, estimate three workloads:

```text
Small task:   40K input + 4K output
Medium task: 200K input + 10K output
Large read:  600K input + 20K output
```

Then calculate:

```text
cost = (input_tokens / 1,000,000 × input_price)
     + (output_tokens / 1,000,000 × output_price)
```

Add a retry multiplier. Coding agents often need multiple turns. A cheap model that retries three times is still often cheaper, but the human wait time may be worse.

Recommended first-week budget:

| Budget item | Suggested cap |
|---|---:|
| OpenRouter open-weight tests | `$10` |
| DeepInfra direct backup | `$5–10` |
| DeepSeek direct non-sensitive tests | `$5` |
| Opus/GPT baselines | enough for 10–20 comparable tasks, usually `$20–50` if using API directly |

This should be enough for a serious week if you avoid huge GPT-5.5 long-context dumps.

## Hidden costs not in per-token price

### Tool-call failures

If a provider’s tool-call format breaks your agent, the token price is irrelevant. Qwen’s own documentation around function-call parser requirements is a reminder that agentic coding depends on exact integration ([QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder)). Track schema errors, invalid JSON, repeated tool calls, and loops.

### Slow generation

A model with low input/output price can still burn developer time if it generates slowly. DeepInfra’s Qwen provider benchmark distinguishes between lowest blended price and higher throughput variants; the cheapest Turbo route had lower throughput than FP8 or Google Vertex alternatives ([DeepInfra Qwen3-Coder benchmark](https://deepinfra.com/blog/qwen3-coder-480b-a35b-api-benchmarks)). For interactive coding, latency matters.

### Review debt

If a cheap model writes plausible but wrong code, the true cost is your review time. This is why every task should log whether the final diff was accepted, edited, or discarded.

### Context packing

If you must chunk Qwen/Kimi tasks because the endpoint is 262K, you may spend extra tokens summarizing and reloading context. A 1M-context DeepSeek/Llama route may be cheaper for reading even if the model is weaker at final patches.

### Provider routing variance

OpenRouter routing can be a benefit and a risk. It can fall back for uptime, but if you do not constrain providers you may get different context caps, prices, latency, or data policies. Use provider selection controls ([OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)).

## Bottom line

- **Cheapest serious long-context route:** DeepSeek V4 Flash direct, if data policy permits.
- **Cheapest safer long-context route:** Llama 4 Maverick via DeepInfra/OpenRouter ZDR route.
- **Best cheap coding-agent candidate:** Qwen3-Coder, especially via DeepInfra/OpenRouter pinned provider.
- **Best open-weight hard-coding challenger:** Kimi K2.6.
- **Quality baselines:** Claude Opus 4.7 and GPT-5.5, with GPT-5.5 long-context surcharge watched closely.

The decision is not “which model has the lowest price.” The decision is which route gives the best **accepted patch per dollar** under your data policy.
