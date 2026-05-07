# Briefing: Hosted open-weight coding LLM APIs

_Last refreshed: 2026-05-07_

## Executive verdict

For a one-week, cost-controlled evaluation of hosted open-weight coding models, the best default is:

1. **Start with OpenRouter** for breadth, but configure it deliberately: low prepaid balance, no auto top-up, ZDR/provider policy controls, and provider allowlists where possible. OpenRouter says prompts/responses are not stored unless optional logging/product-improvement settings are enabled, while metadata is stored ([data collection](https://openrouter.ai/docs/guides/privacy/data-collection)); it supports zero-data-retention routing controls ([ZDR](https://openrouter.ai/docs/guides/features/zdr)).
2. **Use DeepInfra direct as the privacy-simple backup** for Qwen3-Coder and Llama 4. DeepInfra says inference inputs/outputs are not stored to disk, are held in memory only during inference, and are not used for training except documented exceptions ([DeepInfra data privacy](https://docs.deepinfra.com/account/data-privacy)).
3. **Use direct DeepSeek only for public/redacted/synthetic tasks** unless policy explicitly approves it. DeepSeek’s pricing is excellent, but its privacy policy says prompts/inputs may be collected, retained, used to improve/train technology, and processed/stored in China ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing), [DeepSeek privacy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)).
4. **Compare by accepted patch per dollar, not benchmark vibes.** Kimi K2.6 and Qwen3-Coder are the strongest open-weight coding candidates; DeepSeek and Llama are especially attractive for cheap long-context reading; Opus/GPT-5.5 remain quality baselines.

## Recommended one-week model roster

| Role | Model/route | Why | Watch-outs |
|---|---|---|---|
| Hard open-weight coder | Kimi K2.6 via OpenRouter | Official Kimi page emphasizes open-source coding, long-horizon execution, and agent swarms ([Kimi K2.6](https://www.kimi.com/blog/kimi-k2-6)); OpenRouter price is far below Opus/GPT ([OpenRouter Kimi](https://openrouter.ai/moonshotai/kimi-k2.6)). | Vendor-heavy claims; measure tool reliability and latency. |
| Cheap coding-agent default candidate | Qwen3-Coder 480B A35B via DeepInfra/OpenRouter | Qwen says 480B total / 35B active, 256K native context, 1M with extrapolation, agentic coding focus ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)); cheap hosted routes exist. | Tool-call parser/provider compatibility matters ([Qwen GitHub](https://github.com/QwenLM/Qwen3-Coder)). |
| Ultra-cheap long context | DeepSeek V4 Flash/Pro direct or V3.1 Terminus via gateway | Direct V4 page lists 1M context and very low prices ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)); benchmarks show strong DeepSeek-family coding signal. | Direct privacy posture unsuitable for sensitive code without approval. |
| Cheap whole-repo reader/control | Llama 4 Maverick via DeepInfra/OpenRouter | 1M-class context around `$0.15/M` input and `$0.60/M` output ([OpenRouter Llama 4 Maverick](https://openrouter.ai/meta-llama/llama-4-maverick), [DeepInfra pricing](https://deepinfra.com/pricing)). | Not the strongest coding evidence; use first as reader/control. |
| Quality baseline | Claude Opus 4.7 | Anthropic positions it for advanced software engineering; `$5/M` input and `$25/M` output; 1M context in docs ([Anthropic Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7), [docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7)). | Expensive; tokenizer/effort changes affect cost. |
| Frontier baseline | GPT-5.5 | OpenAI prices it at `$5/M` input and `$30/M` output, 1.05M context in docs ([OpenAI pricing](https://openai.com/api/pricing/), [docs](https://developers.openai.com/api/docs/models/gpt-5.5)). | Prompts above 272K input incur 2x input and 1.5x output pricing for full session. |

## Price/context snapshot

| Model / route | Context | Practical input budget | Input $/1M | Output $/1M | Source |
|---|---:|---:|---:|---:|---|
| Qwen3-Coder OpenRouter | 262K | ~180K–220K | 0.22 | 1.80 | [OpenRouter Qwen](https://openrouter.ai/qwen/qwen3-coder) |
| Qwen3-Coder DeepInfra | 256K | ~180K–220K | 0.30 / 0.10 cached | 1.00 | [DeepInfra pricing](https://deepinfra.com/pricing) |
| Kimi K2.6 OpenRouter | 262K | ~200K–240K | 0.75 | 3.50 | [OpenRouter Kimi](https://openrouter.ai/moonshotai/kimi-k2.6) |
| DeepSeek V4 Flash direct | 1M | ~600K–950K | 0.14 cache miss / 0.0028 cache hit | 0.28 | [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) |
| DeepSeek V3.1 Terminus OpenRouter | 164K | ~120K–140K | 0.27 | 0.95 | [OpenRouter Terminus](https://openrouter.ai/deepseek/deepseek-v3.1-terminus) |
| Llama 4 Maverick | ~1M | ~700K–950K | 0.15 | 0.60 | [OpenRouter](https://openrouter.ai/meta-llama/llama-4-maverick), [DeepInfra](https://deepinfra.com/pricing) |
| Claude Opus 4.7 | 1M | ~850K–900K | 5.00 | 25.00 | [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| GPT-5.5 | 1.05M | under 272K cheap tier; ~900K max | 5.00 / 10.00 above 272K | 30.00 / 45.00 above 272K | [OpenAI pricing](https://openai.com/api/pricing/), [docs](https://developers.openai.com/api/docs/models/gpt-5.5) |

## Evidence synthesis

### Model quality

Independent and benchmark sources support trialing open models, but not blindly replacing Opus/GPT. Aider’s leaderboard is relevant because it evaluates instruction following and code editing without human intervention across 225 polyglot tasks ([Aider leaderboards](https://aider.chat/docs/leaderboards/)). SWE-bench Verified uses real GitHub issues and a shared mini-SWE-agent harness; the captured page showed Claude-family models leading while Kimi/DeepSeek-family entries were competitive ([SWE-bench](https://www.swebench.com/)). LiveCodeBench/Vals reported DeepSeek V4 and Kimi K2.6 among competitive coding/problem-solving models near frontier closed systems ([Vals LiveCodeBench](https://www.vals.ai/benchmarks/lcb)).

### Provider economics

The cost gap is real. A 200K-input / 10K-output coding-agent run costs roughly:

- Qwen OpenRouter: `$0.062`;
- Kimi K2.6: `$0.185`;
- DeepSeek V4 Flash: `$0.031`;
- Llama 4 Maverick: `$0.036`;
- Claude Opus: `$1.25`;
- GPT-5.5 under 272K: `$1.30`.

For long reads, GPT-5.5’s >272K surcharge makes cheap long-context routes especially attractive.

### Provider risk

OpenRouter is a fast evaluation gateway, not a magic privacy guarantee. Provider routing must be constrained because provider retention/training policies differ ([OpenRouter provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging), [provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)). DeepInfra’s privacy policy is stronger for direct inference experiments ([DeepInfra data privacy](https://docs.deepinfra.com/account/data-privacy)). DeepSeek direct is cost-leading but privacy-riskier for sensitive code ([DeepSeek privacy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)).

## One-week decision rule

Adopt an open-weight route only if it clears all four gates:

1. **Correctness:** tests/build/lint pass or the output is demonstrably correct.
2. **Maintenance:** diff is minimal and follows local patterns.
3. **Cost:** accepted-work cost is materially below Opus/GPT after retries.
4. **Policy:** provider route is acceptable for the data class sent.

The likely winning architecture is tiered routing:

```text
Cheap reader/research tier: Llama 4, DeepSeek, Qwen
Cheap/default coding tier: Qwen or Kimi if local tests pass
Hard-task escalation tier: Opus or GPT-5.5
```

## Open questions

- Is Kimi K2.6 consistently better than Qwen3-Coder on real multi-file patches, or only on benchmarks/vendor examples?
- Which Qwen provider route gives the best mix of tool-call fidelity, latency, and price?
- Can Llama 4 Maverick serve as a reliable cheap whole-repo reader despite weaker coding evidence?
- How restrictive are OpenRouter ZDR/provider filters in practice for availability and latency?
- What is the true review-debt cost of cheap models on the user’s own repositories?
