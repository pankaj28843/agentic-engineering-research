# 05 — Provider safety, privacy, and reliability

## Provider choice is the real security decision

For coding agents, provider choice is not a billing detail. It is the security boundary. A prompt can contain source code, unreleased product logic, stack traces, secrets accidentally left in files, database schemas, customer identifiers, security vulnerabilities, architecture docs, and internal roadmap details.

The model being “open weight” does not decide where that data goes. The hosted route does. A Qwen, Kimi, DeepSeek, or Llama request can be safe-enough or unsafe depending on whether it is served through a zero-retention provider, a gateway with strict routing, a provider that retains prompts for abuse monitoring, or a direct service that uses inputs for training.

The evaluation question is therefore:

```text
Can this model, through this provider, under this routing policy,
solve my coding tasks with acceptable cost, latency, reliability,
and data handling?
```

## Provider class 1: OpenRouter as evaluator front door

OpenRouter is an aggregator/gateway across many model providers. Its value for a one-week evaluation is speed: one API key, one OpenAI-compatible interface, many models, many provider routes, model price/context pages, and routing controls.

OpenRouter’s data collection docs say it does not store prompts or responses unless you opt into private input/output logging or OpenRouter use of inputs/outputs; it does store metadata such as token counts and latency ([OpenRouter data collection](https://openrouter.ai/docs/guides/privacy/data-collection)). Its ZDR docs say zero data retention means a provider will not store your data for any period of time, and OpenRouter can enforce ZDR globally or per request using provider preferences ([OpenRouter ZDR](https://openrouter.ai/docs/guides/features/zdr)). Its provider-logging docs list default provider retention/training policies and state that provider policies differ ([OpenRouter provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging)).

OpenRouter’s provider selection docs matter because routing is configurable. You can sort providers, ignore providers, allow fallback, and set requirements such as ZDR ([OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)). This is good for reliability and bad if you forget that “model id” is not “provider id.” A request to the same model id can be served by different providers unless constrained.

### When OpenRouter is a good default

OpenRouter is a good starting point when:

- you want to compare many current models quickly;
- you need a single spend cap;
- you need OpenAI-compatible access from a coding agent;
- you can restrict providers for privacy;
- you are testing public, synthetic, or redacted code.

### When OpenRouter is not enough

OpenRouter may be insufficient when:

- your organization requires a direct data processing agreement;
- you need deterministic provider selection for audit;
- you need a guaranteed region or enterprise support path;
- you cannot risk fallback to a provider with weaker retention policy;
- your coding agent needs provider-specific features not exposed through the gateway.

The one-week guide therefore recommends OpenRouter as the **minimal experiment interface**, not as the universal production answer.

## Provider class 2: Direct zero-retention-ish inference providers

### DeepInfra

DeepInfra is the strongest direct-provider candidate in this research set because its privacy page is clear and its prices are competitive. DeepInfra says:

- inference inputs are never stored to disk;
- outputs are never stored;
- data is held only in memory while processing and deleted after inference;
- prompts are not used for training;
- exceptions apply when using Google/Anthropic models and some bulk/image cases ([DeepInfra data privacy](https://docs.deepinfra.com/account/data-privacy)).

DeepInfra’s pricing page lists Qwen3-Coder-480B-A35B-Instruct-Turbo at 256k context, `$0.30/M` input, `$0.10/M` cached input, and `$1.00/M` output; Llama-4-Maverick at 1024k context, `$0.15/M` input, and `$0.60/M` output; and many other open models ([DeepInfra pricing](https://deepinfra.com/pricing)). Its Qwen3-Coder provider benchmark positions DeepInfra’s Turbo route as lowest blended price among compared routes, while also documenting throughput/latency tradeoffs and JSON-mode availability differences ([DeepInfra Qwen3-Coder benchmark](https://deepinfra.com/blog/qwen3-coder-480b-a35b-api-benchmarks)).

For your one-week evaluation, DeepInfra direct is the best backup when you want fewer routing surprises than OpenRouter and stronger published data handling than direct DeepSeek.

### Fireworks, Together, Groq, Cerebras

OpenRouter’s provider-logging table lists Fireworks, Together, Groq, Cerebras, and several others as zero-retention by default ([OpenRouter provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging)). This does not replace reading their direct terms before production, but it gives useful routing candidates inside OpenRouter.

Fireworks publishes serverless pricing for Llama 4 Scout/Maverick around `$0.15–$0.22/M` input and `$0.50–$0.88/M` output depending on model/precision ([Fireworks pricing](https://fireworks.ai/pricing)). Together’s pricing page lists many open models, including DeepSeek, Qwen, Kimi, Llama, GLM, and others, with per-million-token prices ([Together pricing](https://www.together.ai/pricing)). Groq’s pricing page lists very low prices for fast inference models such as Llama 4 Scout and Maverick, plus compound systems ([Groq pricing](https://groq.com/pricing/)). Cerebras lists very high-speed hosted model pricing, including Qwen3-Coder-480B at `$2/M` input and `$8/M` output and Qwen3-Next-80B at `$0.30/M` input and `$0.60/M` output ([Cerebras pricing](https://www.cerebras.ai/pricing)).

These providers may matter if your biggest pain is latency, not price. For example, a Qwen route that costs more but generates faster can be cheaper in developer time. A one-week trial should include at least one fast route if interactive latency is important.

## Provider class 3: Model-owner direct APIs

### DeepSeek direct

DeepSeek direct is the cheapest serious long-context route found in this research. Its pricing page lists V4 Flash at 1M context, 384K max output, `$0.14/M` cache-miss input, `$0.0028/M` cache-hit input, and `$0.28/M` output; V4 Pro has a listed discount period with `$0.435/M` cache-miss input and `$0.87/M` output, otherwise `$1.74/M` and `$3.48/M` ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)). It also documents OpenAI-compatible and Anthropic-compatible API base URLs, thinking/non-thinking modes, JSON output, tool calls, FIM completion, and context caching.

The privacy policy is the reason this is not the default for private code. It says DeepSeek collects inputs such as prompts, uploaded files, and chat history; uses information to improve and train technology; retains information as long as necessary; and stores/processes personal data in China ([DeepSeek privacy policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)).

Use direct DeepSeek for:

- public repos;
- synthetic tasks;
- redacted code;
- long-context experiments where low cost is essential.

Do not use direct DeepSeek for:

- secrets;
- client code;
- private company code without approval;
- security vulnerabilities;
- regulated data.

### Qwen/Alibaba routes

Qwen’s official launch page shows examples using Alibaba Model Studio / DashScope-compatible endpoints and discusses Qwen Code plus integrations ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)). Alibaba Cloud documentation pages surfaced in the extraction set for Qwen3-Coder-Flash pricing and API routes. The Qwen ecosystem is broad, but direct Alibaba/Model Studio data handling and regional policy should be reviewed before sending proprietary code.

For a one-week personal evaluation, Qwen through DeepInfra or a filtered OpenRouter route is simpler than signing up for every model-owner API.

### Moonshot/Kimi direct

Kimi K2.6 is available via Kimi API and Kimi Code according to the launch page ([Kimi K2.6](https://www.kimi.com/blog/kimi-k2-6)). Kimi’s direct route may be attractive if it exposes the newest Kimi behavior fastest or if OpenRouter provider entries lag. For a safety-first trial, still compare privacy terms, retention, region, and logging before using private code.

## Reliability dimensions to measure

Do not reduce reliability to uptime. For coding agents, reliability has at least seven dimensions.

### 1. Request success rate

Does the endpoint return successful responses, or do you see transient 5xx/429 errors? OpenRouter model pages expose recent provider uptime values; those are useful hints but not contractual SLAs ([OpenRouter Qwen3-Coder](https://openrouter.ai/qwen/qwen3-coder), [OpenRouter Kimi K2.6](https://openrouter.ai/moonshotai/kimi-k2.6)). Run your own week-long log.

### 2. Latency and time-to-first-token

A coding agent feels broken if it waits too long before acting. DeepInfra’s Qwen3-Coder benchmark compares time-to-first-token, throughput, and blended price across providers, showing that the cheapest and fastest options can differ ([DeepInfra Qwen3-Coder benchmark](https://deepinfra.com/blog/qwen3-coder-480b-a35b-api-benchmarks)).

### 3. Output throughput

Long diffs require output tokens. If a model is cheap but generates 5 tokens/sec, it may be unusable for large patches. Track tokens/sec or wall-clock time per accepted patch.

### 4. Tool-call/schema fidelity

A model that fails JSON/function-call syntax wastes turns. Qwen’s repository documentation around function-call parser requirements is an explicit reminder ([QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder)). Kimi’s launch page emphasizes tool-call examples and long-horizon execution, which are exactly the claims to test ([Kimi K2.6](https://www.kimi.com/blog/kimi-k2-6)).

### 5. Context-limit behavior

Does the route reject long prompts early? Does it silently truncate? Does it degrade badly near the cap? Provider pages list context, but practical behavior must be tested. GPT-5.5 also introduces a long-context surcharge above 272K input ([GPT-5.5 docs](https://developers.openai.com/api/docs/models/gpt-5.5)), so reliability and cost interact.

### 6. Behavioral stability

Does the model loop, over-edit, ignore instructions, or claim tests passed when they did not? This is a model/harness property, not only a provider property.

### 7. Support/debuggability

Can you inspect provider route, token counts, errors, and billing? OpenRouter metadata and dashboards help; direct providers may offer more or less detail. For a one-week test, export logs daily.

## Privacy posture by route

| Route | Privacy posture for private code | Evidence | Recommended use |
|---|---|---|---|
| OpenRouter with ZDR and provider allowlist | Good for personal/small-team evaluation if configured carefully | Prompts/responses not stored unless opt-in; ZDR controls; provider policies vary ([data collection](https://openrouter.ai/docs/guides/privacy/data-collection), [ZDR](https://openrouter.ai/docs/guides/features/zdr), [provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging)) | Default one-week front door. |
| DeepInfra direct | Good candidate for safer direct inference | Inputs/outputs not stored to disk; memory-only during inference; not used for training, with exceptions ([DeepInfra privacy](https://docs.deepinfra.com/account/data-privacy)) | Primary direct-provider backup. |
| Fireworks/Together/Groq/Cerebras via OpenRouter | Potentially good, verify direct terms | OpenRouter provider table marks many as zero retention ([provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging)) | Provider-pinned alternatives, especially for speed. |
| DeepSeek direct | High risk for sensitive code | Inputs collected/retained; improve/train technology; China processing/storage ([DeepSeek privacy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)) | Public/redacted/synthetic only unless approved. |
| Opus/GPT official | Depends on your account terms and data settings | Official pricing/docs; separate enterprise/privacy terms not fully evaluated here | Baseline if already approved in your workflow. |

## Spend safety

Provider safety includes budget safety. For the first week:

- keep OpenRouter balance low;
- disable auto-recharge;
- set per-provider and daily budget alerts if available;
- log token counts from every run;
- avoid GPT-5.5 prompts above 272K unless intentional because the docs say pricing jumps for the full session above that threshold ([GPT-5.5 docs](https://developers.openai.com/api/docs/models/gpt-5.5));
- use cheap long-context models for exploratory reading;
- keep Opus/GPT for side-by-side baselines and hard escalations.

A “cheap” open-weight evaluation can still waste money if a coding agent loops. Agent loops are especially dangerous with long-context models because every retry resends large context. Set max turns.

## Reliability test harness

For each provider/model run, collect this row:

```text
date:
model:
provider:
route pinned? yes/no
ZDR required? yes/no
input tokens:
output tokens:
cost:
wall-clock time:
time to first token:
request errors:
tool-call/schema errors:
context-limit errors:
tests run:
final status: accepted / edited / discarded
notes:
```

At the end of the week, compute:

- accepted patches per dollar;
- accepted patches per hour;
- median wall-clock time;
- schema-error rate;
- retry count;
- review effort;
- number of times you escalated to Opus/GPT.

Do not choose a provider only from advertised price. Choose the provider/model route that produces the most accepted, policy-compliant work per dollar and per hour.

## Minimal safe starting configuration

If using OpenRouter, the safest minimal configuration is:

1. Use a prepaid balance and no auto-top-up.
2. Enable data-policy settings that avoid providers that train on prompts.
3. Prefer or require ZDR where possible.
4. Pin known providers for sensitive work: DeepInfra, Fireworks, Together, Groq, Cerebras, or another provider you have reviewed.
5. Disable prompt/completion logging unless the repo is non-sensitive.
6. Keep a local log of provider route and token counts.
7. Use a redacted/public repo for first experiments.

If using DeepInfra direct:

1. Verify model context and price on the pricing page immediately before running.
2. Use the OpenAI-compatible endpoint from your coding agent.
3. Keep a small billing cap.
4. Avoid Google/Anthropic routes if relying on DeepInfra’s “not stored/not trained” inference stance, because DeepInfra documents exceptions for those models ([DeepInfra data privacy](https://docs.deepinfra.com/account/data-privacy)).
5. Test Qwen3-Coder and Llama 4 Maverick first.

If using DeepSeek direct:

1. Use only non-sensitive/public/redacted tasks unless approved.
2. Take advantage of context caching and low price for long reads.
3. Do not put API keys, private logs, or unreleased code in prompts.
4. Keep a clear label in your logs that the privacy posture is different.

## Bottom line

- **OpenRouter** is the best evaluation gateway, but only with routing and data-policy controls.
- **DeepInfra** is the best direct-provider backup in this research set for privacy clarity plus price.
- **DeepSeek direct** is the cheapest long-context option but is a sensitive-code risk.
- **Fireworks/Together/Groq/Cerebras** are worth testing when latency or alternate hosting matters.
- **Provider routing must be measured**: uptime, latency, schema errors, context failures, and accepted patches are the real reliability metrics.
