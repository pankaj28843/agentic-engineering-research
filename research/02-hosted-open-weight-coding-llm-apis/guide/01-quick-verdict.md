# 01 — Quick verdict and the one-week plan

## The answer in one page

If your goal is **minimal, cheap, safe-enough, and reliable enough for a one-week coding trial**, use this default stack:

1. **Provider front door:** OpenRouter with a tiny prepaid balance and no auto top-up.
2. **Provider policy:** enable or require zero-data-retention routing where possible; on requests, use OpenRouter provider preferences rather than the default “route anywhere” posture.
3. **Primary test models:** Kimi K2.6, Qwen3-Coder 480B A35B, DeepSeek V4 Flash/Pro or DeepSeek V3.1 Terminus, and Llama 4 Maverick.
4. **Baselines:** your normal Claude Opus and GPT-5.5 route, tested on the same tasks and same validation commands.
5. **Safety posture:** run only public, synthetic, or redacted code unless you have explicitly accepted provider/jurisdiction risk.
6. **Decision rule:** keep the open-weight route only if it passes your own issue-fix tasks at materially lower cost without creating hidden review/debug debt.

The recommended first provider is OpenRouter not because it is always the safest endpoint, but because it is the **smallest experiment surface**: one API key, one OpenAI-compatible endpoint, many current model pages, model price/context metadata, and provider routing controls. OpenRouter says it does not store prompts or responses unless you opt into private I/O logging or product-improvement use, while it does store request metadata such as token counts and latency ([OpenRouter data collection](https://openrouter.ai/docs/guides/privacy/data-collection)). It also exposes Zero Data Retention controls and a per-request `provider.zdr` preference ([OpenRouter ZDR docs](https://openrouter.ai/docs/guides/features/zdr)). That is exactly what you need for a bounded, one-week comparison.

The recommended safety backup is DeepInfra direct. DeepInfra says inference inputs are not stored to disk, outputs are not stored, prompts are not used for training, and content is held only in memory during inference, with exceptions for Google/Anthropic endpoints and some bulk/image behavior ([DeepInfra data privacy](https://docs.deepinfra.com/account/data-privacy)). DeepInfra also publishes very competitive pricing for Qwen3-Coder and Llama 4 on its pricing page, including Qwen3-Coder-480B-A35B-Instruct-Turbo at 256k context, $0.30/M input, $1.00/M output, and Llama-4-Maverick at 1024k context, $0.15/M input, $0.60/M output ([DeepInfra pricing](https://deepinfra.com/pricing)).

The recommended skeptical rule is: **do not call a provider “safe” only because the model weights are open.** The model license and the provider’s data handling are different layers. A hosted open-weight model can still log prompts, retain data, route through a third party, require user identifiers, or impose a context/output cap that is lower than the model card implies.

## Why not just use the cheapest direct API?

DeepSeek direct pricing is astonishingly cheap. The current DeepSeek pricing page lists V4 Flash with 1M context, 384K maximum output, $0.14/M cache-miss input, $0.0028/M cache-hit input, and $0.28/M output; V4 Pro is currently discounted to $0.435/M cache-miss input and $0.87/M output until the listed discount deadline ([DeepSeek API pricing](https://api-docs.deepseek.com/quick_start/pricing)). If the only goal were cost, DeepSeek direct would be the obvious first click.

But your request included **safe and reliable**, not just cheap. DeepSeek’s privacy policy is not the same as a zero-retention enterprise inference contract. It says the service collects prompts/inputs, may use personal data to improve and train technology, retains personal data as long as necessary for service/legal/business purposes, and processes/stores personal data in the People’s Republic of China ([DeepSeek privacy policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)). For non-sensitive experiments this may be acceptable; for private client code, secrets, security bugs, or unreleased product logic, it is a different risk category from a zero-retention endpoint.

So the cheap direct API is useful, but it is not the default safest path. Treat it as:

- **green** for public OSS issues, toy repos, benchmark harnesses, and generated fixtures;
- **yellow** for internal code already approved for third-party processing;
- **red** for secrets, unreleased IP, regulated data, or client code without explicit approval.

## The model shortlist

For the one-week trial, keep the model list small. Too many models will turn your week into a leaderboard addiction instead of a decision.

| Role | Model/route | Why it belongs in the trial | Main caveat |
|---|---|---|---|
| Best open-weight coding candidate | Kimi K2.6 | Official Kimi launch claims state-of-the-art coding, long-horizon execution, and agent swarm capabilities, with partner quotes about long-running coding reliability ([Kimi K2.6](https://www.kimi.com/blog/kimi-k2-6)). | Vendor-heavy evidence; must test on your repo. |
| Cost/value code agent | Qwen3-Coder 480B A35B | Qwen says the model is built for agentic coding, has 480B total / 35B active parameters, 256K native context, and 1M with YaRN; it ships Qwen Code and Claude Code proxy instructions ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)). | Tool-call format and provider implementation matter. |
| Ultra-cheap long context | DeepSeek V4 Flash/Pro or V3.1 Terminus | DeepSeek direct gives 1M context on V4 models at extremely low prices; OpenRouter lists V3.1 Terminus at 163.8K context and low price ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing), [OpenRouter DeepSeek V3.1 Terminus](https://openrouter.ai/deepseek/deepseek-v3.1-terminus)). | Privacy/jurisdiction and model-version churn. |
| Long-context cheap control | Llama 4 Maverick | OpenRouter and DeepInfra show Llama 4 Maverick around 1M context at $0.15/M input and $0.60/M output ([OpenRouter Llama 4 Maverick](https://openrouter.ai/meta-llama/llama-4-maverick), [DeepInfra pricing](https://deepinfra.com/pricing)). | Not obviously the best code model; use as long-context/control baseline. |
| Expensive frontier baseline | Claude Opus 4.7 | Anthropic says Opus 4.7 is targeted at advanced software engineering and long-running coding tasks, priced at $5/M input and $25/M output, with 1M context in docs ([Anthropic Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7), [Claude docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7)). | Expensive; tokenizer and effort settings affect cost. |
| Expensive frontier baseline | GPT-5.5 | OpenAI pricing says GPT-5.5 is $5/M input, $0.50/M cached input, and $30/M output; model docs list 1,050,000 context and 128,000 max output ([OpenAI pricing](https://openai.com/api/pricing/), [OpenAI GPT-5.5 docs](https://developers.openai.com/api/docs/models/gpt-5.5)). | Long-context surcharge above 272K input in docs; can become very expensive. |

## One-week schedule

### Day 0: set the guardrails

Do not start by asking models to change your main repository. Start by defining the box.

- Create API keys with minimum permissions.
- Add hard dollar caps: `$10` OpenRouter, `$5–10` DeepInfra/direct provider, and whatever small amount you need for Opus/GPT baselines.
- Disable prompt/completion logging unless you need it for debugging and the code is non-sensitive.
- Turn on ZDR/provider filters where supported. OpenRouter documents account-wide and per-request ZDR enforcement ([OpenRouter ZDR](https://openrouter.ai/docs/guides/features/zdr)).
- Prepare a redacted or public evaluation repository if your normal repo contains secrets, client data, or unreleased proprietary logic.
- Define the same validation commands for every model: unit tests, type checks, build, lint, and one end-to-end smoke test.

The setup day is where most cheap experiments become expensive or unsafe. If you do not cap spend and define acceptable data classes, a “cheap model test” can become uncontrolled data transfer.

### Days 1–2: run easy and medium tasks

Start with tasks that have objective validation:

- fix a failing test;
- add a small feature with existing patterns;
- refactor a function and keep tests passing;
- generate missing tests for a known bug;
- update docs from code.

For each task, run the same prompt through one baseline and two open-weight candidates. Do not over-optimize prompts yet. The first thing you want to measure is not “best possible result,” but “default usefulness.” If Kimi, Qwen, or DeepSeek needs a fragile prompt ritual to avoid breaking tools, that is part of its real cost.

### Days 3–4: run long-context tasks

Now test the reason you are looking at 256K–1M context windows:

- summarize a subsystem from many files;
- propose a refactor after reading a package;
- find dead code across a module;
- explain a bug by tracing data flow;
- compare two implementations.

Use actual token counts. Do not trust the marketing context window alone. GPT-5.5 docs list 1,050,000 context and 128,000 max output, but also say prompts above 272K input tokens are priced at 2x input and 1.5x output for the full session ([OpenAI GPT-5.5 docs](https://developers.openai.com/api/docs/models/gpt-5.5)). Claude Opus 4.7 has 1M context and 128K max output, but Anthropic warns its tokenizer can use roughly 1x to 1.35x as many tokens as Opus 4.6 depending on content ([Claude Opus 4.7 docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7)). Qwen’s model may support 1M via extrapolation, but a given hosted route may advertise only 262K total context ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/), [OpenRouter Qwen3-Coder](https://openrouter.ai/qwen/qwen3-coder)).

### Days 5–6: agentic tasks and tool calling

This is the decisive part. Coding agents fail differently from chat models. Run tasks that require tools, edits, and validation loops:

- make a multi-file feature change;
- debug with logs and tests;
- migrate an API call;
- fix a flaky test;
- implement a small PRP-like plan.

For each run, log:

- total input/output tokens;
- cost;
- time to first useful edit;
- number of tool-call/schema errors;
- number of test runs;
- number of human interventions;
- whether the final diff was accepted, edited, or discarded.

Kimi’s official page emphasizes long-horizon coding, 4,000+ tool-call examples, and partner comments about tool-calling reliability ([Kimi K2.6](https://www.kimi.com/blog/kimi-k2-6)). Qwen’s launch page emphasizes Qwen Code, OpenAI-compatible API usage, and Claude Code integration ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)). Those are exactly the claims to validate.

### Day 7: decide with a scorecard, not vibes

Use four gates:

1. **Correctness:** did tests and builds pass without human patching?
2. **Maintenance:** did the model follow local patterns, or did it add clever junk?
3. **Cost:** was the real task cost at least 5–10x lower than Opus/GPT for comparable outcomes?
4. **Safety/reliability:** did the provider route satisfy your data policy, and did the endpoint stay stable enough?

Possible decisions:

- **Adopt for broad use:** rare; only if open-weight candidates match baseline quality on your repo.
- **Adopt for cheap first pass:** likely; use open weights for summaries, tests, exploration, and simple patches, then escalate to Opus/GPT for hard tasks.
- **Adopt for long-context reading only:** use Llama/DeepSeek/Qwen to read huge context cheaply, but keep edits on Opus/GPT.
- **Reject for now:** if tool calling, diff quality, or provider reliability burns too much time.

## The most likely outcome

The most realistic outcome is not full replacement. It is **tiered routing**:

```text
Cheap/read/research tier:
  Qwen3-Coder, Kimi K2.6, DeepSeek, Llama 4

Default coding tier:
  best open-weight candidate if it passes your week

Escalation tier:
  Claude Opus / GPT-5.5 for hard architecture, fragile migrations, security-sensitive review, or when the cheap model stalls
```

That still matters. If 60–80% of daily coding-agent tokens move from `$5/$25+` baselines to `$0.15–$0.75` input and `$0.60–$3.50` output routes, your bill drops sharply while Opus/GPT remain available for the work where they earn their price.

## Concrete starting configuration

If you want the shortest path from research to action, use this configuration for the first two days. It is intentionally conservative.

```text
Budget:
  OpenRouter: $10, no auto top-up
  DeepInfra:  $5-$10, no auto top-up
  DeepSeek:   optional $5, public/redacted only

Data:
  No secrets
  No production logs
  No client repositories
  No private security vulnerabilities
  Public or redacted evaluation repo first

Routes:
  Qwen3-Coder: DeepInfra direct, then OpenRouter pinned provider comparison
  Kimi K2.6:   OpenRouter with ZDR/provider constraints
  Llama 4:     DeepInfra or OpenRouter for reading/control
  DeepSeek:    direct only for public/redacted long-context experiments
  Opus/GPT:    baseline and escalation only
```

The reason to keep both OpenRouter and DeepInfra is not redundancy for its own sake. OpenRouter answers the market question: “Which current hosted model looks best quickly?” DeepInfra answers the simpler direct-provider question: “Can I run Qwen or Llama with a clearer inference privacy posture and fewer routing surprises?” Direct DeepSeek answers a different question: “How much does ultra-cheap 1M-context reading change my workflow when the data is safe to send?” These are three different experiments.

Start with a public repository if possible. If you do not have one, create a synthetic evaluation repo with the same stack shape as your real work: a few modules, tests, a realistic bug, a small feature, and a build command. A synthetic repo will not fully predict behavior on your real codebase, but it catches provider/tool problems without risking private data. Once tool calls, context size, and cost logging work, move to redacted private tasks if your policy allows.

During the first two days, avoid clever routing. Do not try six providers for every model. Pick one route per model and learn the failure modes. After that, compare provider routes for the model that actually looked promising. This prevents the evaluation from exploding into a matrix where no task has enough repeats to matter.

Use Opus/GPT sparingly but fairly. Run each baseline on enough paired tasks to know what “good” looks like, especially one simple patch, one medium multi-file change, and one hard/ambiguous task. Then stop using the baselines as default readers. The point is to preserve expensive frontier models for the jobs where they still earn their cost.

Finally, write down the “escalation boundary” as you discover it. For example: “Qwen is fine for tests and small patches but escalates after one failed validation loop,” or “Kimi is the default for medium refactors, Opus only reviews architecture-sensitive diffs,” or “Llama is a reader only.” This boundary is more valuable than a single model ranking because it turns the week into a reusable workflow.
