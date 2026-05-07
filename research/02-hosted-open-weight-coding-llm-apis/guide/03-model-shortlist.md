# 03 — The model shortlist: Qwen, Kimi, DeepSeek, Llama, Opus, and GPT-5.5

## Why shortlist at all?

The hosted model market changes too fast to evaluate everything. Google search surfaced Qwen3-Coder, Kimi K2.x, DeepSeek V3/V4, Llama 4, MiniMax, GLM, GPT-OSS, Mistral/Devstral, and many provider-specific variants. HN and GitHub signals add even more candidates. But a one-week coding evaluation cannot be a full leaderboard. It needs a small model set with clear jobs.

The shortlist below is optimized for your stated goal: **frontier-ish open-weight coding/development models, hosted cheaply, compared against Opus/GPT-5.5, with safety and reliability in mind**.

## Candidate 1: Qwen3-Coder 480B A35B

### What it is

Qwen3-Coder is Alibaba/Qwen’s coding-focused model family. The official launch page says the flagship Qwen3-Coder-480B-A35B-Instruct is a 480B-parameter mixture-of-experts model with 35B active parameters, supports 256K context natively and up to 1M with extrapolation, and is designed for coding plus agentic browser/tool use ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)). The Qwen GitHub repository repeats the agentic-coding framing and notes support across Qwen Code, Cline, Claude Code, and specialized function-call formats ([QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder)).

The important phrase is **agentic coding**, not just “code completion.” Qwen’s post-training section says the team used long-horizon reinforcement learning for tasks like SWE-Bench, where the model must plan, use tools, receive feedback, and make decisions across multi-turn interactions ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)). That maps directly to coding-agent use.

### Why it belongs in your week

Qwen3-Coder is the best “cheap first-pass coder” candidate. It is widely hosted, cheap per token, and directly integrated with developer tools. Qwen’s launch page includes `Qwen Code`, an OpenAI-compatible API setup, Cline setup, and Claude Code proxy/router instructions ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)). That makes it less theoretical than a model that only has a paper.

OpenRouter lists Qwen3-Coder 480B A35B at 262,144 context, `$0.22/M` input, and `$1.80/M` output ([OpenRouter Qwen3-Coder](https://openrouter.ai/qwen/qwen3-coder)). DeepInfra’s pricing page lists Qwen3-Coder-480B-A35B-Instruct-Turbo at 256k context, `$0.30/M` input, `$0.10/M` cached input, and `$1.00/M` output ([DeepInfra pricing](https://deepinfra.com/pricing)). DeepInfra’s own Qwen3-Coder provider benchmark says its Turbo route had the lowest blended price and tied-lowest time-to-first-token among tracked providers, while warning that JSON mode was not available on that route ([DeepInfra Qwen3-Coder benchmark](https://deepinfra.com/blog/qwen3-coder-480b-a35b-api-benchmarks)).

### What to test

Do not test Qwen only on standalone LeetCode-style code. Test:

- repository search and explanation;
- multi-file edits;
- existing pattern preservation;
- test-writing from a bug report;
- tool-call stability inside your coding agent;
- long-context comprehension at 100K–200K tokens.

### Main caveat

Qwen’s strength depends on function-call integration. The Qwen repository warns about tool-parser and tokenizer requirements ([QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder)). GitHub search also surfaced small compatibility proxies for malformed Qwen tool calls in OpenCode contexts ([research log](../research-log.md)). That does not disqualify Qwen; it tells you to measure tool-call errors explicitly.

## Candidate 2: Kimi K2.6

### What it is

Kimi K2.6 is Moonshot’s latest open-source/open-weight coding model in the Kimi K2 line. Moonshot’s launch page says Kimi K2.6 features state-of-the-art coding, long-horizon execution, and agent swarm capabilities, and is available through Kimi.com, the Kimi App, API, and Kimi Code ([Kimi K2.6](https://www.kimi.com/blog/kimi-k2-6)). The older Kimi K2 repository describes Kimi K2 as a 1T-total-parameter MoE with 32B active parameters, optimized for tool use, reasoning, and autonomous problem solving, with 128K context for the K2 Instruct line ([MoonshotAI/Kimi-K2](https://github.com/MoonshotAI/Kimi-K2)).

Kimi K2.6’s launch page is unusually focused on long-running engineering work. It describes examples like 12-hour/13-hour autonomous coding runs, thousands of tool calls, performance optimization, and partner feedback from coding-tool companies ([Kimi K2.6](https://www.kimi.com/blog/kimi-k2-6)). These are vendor claims, but they are claims about exactly the workload you care about: not just generating a function, but staying coherent through a long task.

### Why it belongs in your week

Kimi is the most plausible open-weight “Opus replacement attempt” in this set. OpenRouter lists Kimi K2.6 at 262,144 context, `$0.75/M` input, and `$3.50/M` output ([OpenRouter Kimi K2.6](https://openrouter.ai/moonshotai/kimi-k2.6)). That is far more expensive than DeepSeek or Llama, but still dramatically cheaper than Opus/GPT baselines. If Kimi can solve the hard coding tasks that Qwen or DeepSeek cannot, it could become your default medium/hard open model.

The HN and Google signals around Kimi were strong. HN Algolia returned high-engagement stories for Kimi K2 Thinking and Kimi K2.6, and Google page 2–3 surfaced discussions claiming Kimi K2.6 was challenging Claude/GPT on coding tasks. These are community signals, not proof. The important thing is that enough practitioners are trying Kimi in coding-agent contexts to justify a week of hands-on evaluation.

### What to test

Kimi should get the hardest open-weight tasks:

- multi-hour agentic tasks;
- ambiguous bug fixes requiring investigation;
- codebase-wide refactor planning;
- UI generation or full-stack scaffolding if relevant;
- tool-call-heavy tasks where the model must recover from failures.

You should compare Kimi directly with Opus/GPT on the same prompts. If Kimi is only slightly cheaper but needs much more review, use it selectively. If it handles medium-hard tasks at a fraction of Opus cost, it becomes the key model.

### Main caveat

The Kimi launch evidence is vendor-heavy. Partner quotes are useful, but many are from organizations that benefit from Kimi’s success or are part of the launch ecosystem ([Kimi K2.6](https://www.kimi.com/blog/kimi-k2-6)). Treat the launch page as a hypothesis generator. Your repo decides.

## Candidate 3: DeepSeek V4 / V3.1 Terminus

### What it is

DeepSeek is the cost-disruption candidate. The current DeepSeek API pricing page lists V4 Flash and V4 Pro, both with 1M context and 384K maximum output, OpenAI-format and Anthropic-format base URLs, thinking/non-thinking modes, JSON output, tool calls, chat prefix completion, and FIM completion in non-thinking mode ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)).

OpenRouter’s DeepSeek V3.1 page lists V3.1 at 32,768 context and `$0.15/M` input, `$0.75/M` output, while V3.1 Terminus is listed at 163,840 context and `$0.27/M` input, `$0.95/M` output ([OpenRouter DeepSeek V3.1](https://openrouter.ai/deepseek/deepseek-chat-v3.1), [OpenRouter DeepSeek V3.1 Terminus](https://openrouter.ai/deepseek/deepseek-v3.1-terminus)). DeepSeek’s own direct API has moved beyond that in the extracted pricing page, so keep version names fresh.

### Why it belongs in your week

DeepSeek belongs because it changes the economics of long context. A 600K-token reading task on GPT-5.5 can be dollars; on DeepSeek V4 Flash it can be cents. The direct pricing page lists V4 Flash cache-miss input at `$0.14/M`, output at `$0.28/M`, and cache-hit input at `$0.0028/M` ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)). Even if quality is lower, that is too cheap to ignore for reading, summarization, and first-pass exploration.

DeepSeek also appears in independent and benchmark contexts. SWE-bench’s captured leaderboard listed DeepSeek V3.2 high reasoning among competitive models under the same mini-SWE-agent harness, below the top Opus/Gemini entries but in the same broad range as many frontier-ish candidates ([SWE-bench](https://www.swebench.com/)). LiveCodeBench/Vals listed DeepSeek V4 among top competitive-programming performers, with open-weight models now competitive with frontier closed models ([Vals LiveCodeBench](https://www.vals.ai/benchmarks/lcb)).

### What to test

Use DeepSeek for two classes of tasks:

- **cheap long-context reading:** summarize packages, find relevant files, explain call graphs, compare approaches;
- **low-risk implementation attempts:** public bugs, synthetic tasks, or redacted code.

If you use direct DeepSeek, avoid sensitive/private code unless policy permits it. If you use DeepSeek through OpenRouter, apply ZDR/provider filters where possible and inspect which provider is actually serving the route.

### Main caveat

The privacy policy is the caveat. DeepSeek’s policy says prompts/inputs may be collected, retained, used to improve/train technology, and processed/stored in China ([DeepSeek privacy policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)). That does not make DeepSeek “bad”; it makes it a non-default route for proprietary code.

## Candidate 4: Llama 4 Maverick and Scout

### What they are

Llama 4 is Meta’s open model family. Meta’s Llama 4 pages emphasize large-context, multimodal, multilingual models ([Llama 4](https://www.llama.com/models/llama-4/)). OpenRouter lists Llama 4 Maverick at 1,048,576 context, `$0.15/M` input, and `$0.60/M` output ([OpenRouter Llama 4 Maverick](https://openrouter.ai/meta-llama/llama-4-maverick)). DeepInfra’s pricing page lists Llama-4-Maverick-17B-128E at 1024k context, `$0.15/M` input, and `$0.60/M` output, and Llama-4-Scout-17B-16E at 320k context, `$0.08/M` input, and `$0.30/M` output ([DeepInfra pricing](https://deepinfra.com/pricing)).

### Why they belong in your week

Llama 4 belongs less as a best coder and more as a **cheap long-context control**. If Llama 4 Maverick can read a huge repository or architecture document for pennies, it can serve as a context-expansion assistant even if Kimi/Qwen/Opus do the final edit. It also helps distinguish “model intelligence” from “context availability.” If Llama can read the whole repo but still makes poor edits, you learn that raw context was not the bottleneck.

### What to test

Use Llama for:

- repository summarization;
- codebase map generation;
- long document digestion;
- issue triage across many files;
- comparison against DeepSeek for long-context reading.

Do not expect it to beat Kimi or Opus on hard agentic coding without evidence from your own tasks.

### Main caveat

Context windows vary by provider. OpenRouter’s Llama 4 Scout page showed provider entries with 327.7K, 131.1K, and 1.31M context depending on route ([OpenRouter Llama 4 Scout](https://openrouter.ai/meta-llama/llama-4-scout)). Always check the actual endpoint, not only the model family.

## Baseline 1: Claude Opus 4.7

### What it is

Anthropic describes Claude Opus 4.7 as its latest generally available Opus model, with improvements in advanced software engineering and long-running tasks. The launch page says pricing remains the same as Opus 4.6: `$5/M` input and `$25/M` output ([Anthropic Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7)). Anthropic’s docs say Opus 4.7 supports a 1M token context window, 128K max output, adaptive thinking, and task budgets; they also recommend high or xhigh effort for coding/agentic use cases ([Claude Opus 4.7 docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7)).

### Why it belongs

Opus is the quality baseline. If your current workflow uses Opus or a similar high-end Claude model, do not replace it in theory. Run it on the same tasks and measure how much human intervention it needs.

### Caveat

Anthropic warns that Opus 4.7 uses a new tokenizer that may use roughly 1x to 1.35x as many tokens as Opus 4.6, and that effort levels change token usage ([Claude Opus 4.7 docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7)). So baseline cost must be measured, not estimated from old Claude runs.

## Baseline 2: GPT-5.5

### What it is

OpenAI’s pricing page calls GPT-5.5 “a new class of intelligence for coding and professional work” and lists `$5/M` input, `$0.50/M` cached input, and `$30/M` output ([OpenAI pricing](https://openai.com/api/pricing/)). The model docs list GPT-5.5 at 1,050,000 context and 128,000 max output ([OpenAI GPT-5.5 docs](https://developers.openai.com/api/docs/models/gpt-5.5)). OpenAI’s announcement includes benchmark tables for agentic, reasoning, and long-context categories, including comparisons against Claude Opus 4.7 and Gemini 3.1 Pro ([OpenAI GPT-5.5 announcement](https://openai.com/index/introducing-gpt-5-5/)).

### Why it belongs

GPT-5.5 is the expensive frontier comparator, especially for long-context and coding. If open-weight models look close on cheap tasks but fail on complex reasoning, GPT-5.5 helps identify where the quality ceiling still matters.

### Caveat

The GPT-5.5 docs say prompts above 272K input tokens are priced at 2x input and 1.5x output for the full session, and regional processing adds a 10% uplift ([OpenAI GPT-5.5 docs](https://developers.openai.com/api/docs/models/gpt-5.5)). That means the advertised `$5/$30` is not the whole story for huge repo contexts.

## The recommended model roster for your first week

Use exactly this set unless you have a special reason to expand:

| Slot | Model | Provider route to start | Purpose |
|---|---|---|---|
| A | Kimi K2.6 | OpenRouter ZDR/provider-filtered route | Hard open-weight coding challenger |
| B | Qwen3-Coder 480B | DeepInfra direct or OpenRouter provider-pinned route | Cheap agentic coding and repo work |
| C | DeepSeek V4 Flash/Pro or V3.1 Terminus | Direct for non-sensitive work; OpenRouter/DeepInfra for safer routing | Ultra-cheap reasoning/long context |
| D | Llama 4 Maverick | DeepInfra or OpenRouter | Long-context cheap control |
| E | Claude Opus 4.7 | Official Anthropic or existing approved route | Quality baseline |
| F | GPT-5.5 | Official OpenAI or existing approved route | Frontier long-context baseline |

Stop there. A seventh model is only useful after one of these fails a specific role.
