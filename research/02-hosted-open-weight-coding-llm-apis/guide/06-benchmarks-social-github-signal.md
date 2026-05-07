# 06 — Benchmarks, HN, GitHub, and practitioner signal

## Benchmarks are useful, but they are not your repo

Benchmark pages are maps, not territory. They help identify candidates, but they cannot answer whether a model will understand your project’s conventions, pass your test suite, or avoid over-editing. Aider, SWE-bench, LiveCodeBench, Artificial Analysis, provider benchmarks, GitHub repos, and HN threads each reveal a different slice.

Use them like this:

- **Aider leaderboard:** editing and diff-following ability.
- **SWE-bench:** real GitHub issue resolution under an agent harness.
- **LiveCodeBench:** competitive-programming/code-reasoning ability on fresh problems.
- **Artificial Analysis/provider benchmarks:** speed, latency, provider variance, and price/performance.
- **GitHub repos:** implementation maturity, stars, integration patterns, and tool compatibility.
- **HN/social:** practitioner attention, failure stories, and where people are spending their own money.

Do not use any single benchmark as a purchasing decision.

## Aider leaderboard: code editing, not just code generation

Aider’s leaderboard is useful because Aider is a terminal pair-programming tool and its benchmark focuses on whether models can follow instructions and edit code successfully without human intervention. The extracted page says Aider’s polyglot benchmark tests 225 challenging Exercism coding exercises across C++, Go, Java, JavaScript, Python, and Rust, and tracks percent correct, cost, and correct edit format ([Aider leaderboards](https://aider.chat/docs/leaderboards/)).

That is closer to your workload than a pure chat benchmark. Coding agents succeed by applying edits, not by explaining algorithms.

The captured Aider leaderboard showed:

- `gpt-5 (high)` at 88.0% correct, `$29.08` cost, 91.6% correct edit format;
- `DeepSeek-V3.2-Exp (Reasoner)` at 74.2% correct, `$1.30` cost, 97.3% correct edit format;
- `claude-opus-4-20250514 (32k thinking)` at 72.0% correct, `$65.75` cost, 97.3% correct edit format;
- older `Kimi K2` at 59.1% correct, `$1.24` cost, 92.9% correct edit format;
- older `Qwen3 235B A22B` at 59.6% correct, 92.9% correct edit format ([Aider leaderboards](https://aider.chat/docs/leaderboards/)).

Do not over-interpret those exact values for Kimi K2.6 or Qwen3-Coder 480B; the leaderboard entries visible in the extracted page include older model variants. The useful signal is broader:

1. frontier closed models still occupy the top region;
2. open/cheap models can be much cheaper per benchmark run;
3. edit-format conformance must be measured separately from correctness;
4. model version and reasoning mode matter a lot.

For your week, reproduce the Aider idea locally: every task should record whether the model produced valid diffs/tool calls and whether tests passed.

## SWE-bench: real issue resolution under a shared harness

SWE-bench is important because it uses real software engineering issues, not only synthetic coding puzzles. The extracted page says SWE-bench Verified is a human-filtered subset of 500 instances and uses mini-SWE-agent to evaluate all models with the same harness ([SWE-bench](https://www.swebench.com/)). That shared harness reduces one source of noise.

The captured leaderboard showed high-end closed models still leading, with Claude 4.5 Opus high reasoning at 76.80, Claude Opus 4.6 at 75.60, GPT-5-2 Codex at 72.80, and GPT-5-2 high reasoning at 72.80. It also showed open or open-adjacent contenders in the same competitive neighborhood: Kimi K2.5 high reasoning at 70.80 and DeepSeek V3.2 high reasoning at 70.00 ([SWE-bench](https://www.swebench.com/)).

This is one of the strongest pieces of evidence for a tiered strategy. The gap between the best closed and strong open models is not infinite. But it also shows the open models are not obviously dominating the top. If your repo tasks are SWE-bench-like—real bugs, real tests, existing projects—SWE-bench is more relevant than marketing charts.

### What SWE-bench cannot tell you

SWE-bench cannot tell you:

- whether OpenRouter’s Kimi K2.6 route will stay available during your workday;
- whether a particular provider’s function calling matches your agent;
- whether your project’s architecture is idiosyncratic;
- whether the model will respect your style conventions;
- whether your data policy allows the provider.

So use SWE-bench to choose candidates, then run your own tasks.

## LiveCodeBench/Vals: algorithmic coding pressure

LiveCodeBench is useful because older benchmarks like HumanEval became saturated. The extracted Vals page says LiveCodeBench v6 includes more than 1000 high-quality coding problems from May 2023 to 2025, with easy, medium, and hard splits, hidden tests, and a focus on avoiding saturated benchmarks ([Vals LiveCodeBench](https://www.vals.ai/benchmarks/lcb)).

The page reported top performance from Gemini 3.1 Pro Preview at 88.48%, GPT 5.2 Codex at 87.99%, DeepSeek V4 at 87.48%, and GPT 5.3 Codex at 87.31%; it specifically notes that open-weight models like DeepSeek V4 and Kimi K2.6 are now competitive with frontier closed models ([Vals LiveCodeBench](https://www.vals.ai/benchmarks/lcb)).

This supports trying DeepSeek and Kimi, but LiveCodeBench is not the whole coding-agent problem. Competitive programming rewards isolated reasoning and hidden-test correctness. It does not test whether the model can read your monorepo, use your tools, keep a patch minimal, and avoid damaging unrelated files.

Practical interpretation:

- DeepSeek V4 deserves a long-context/reasoning slot.
- Kimi K2.6 deserves a hard-coding slot.
- LiveCodeBench strength does not eliminate the need for repo-specific tests.

## Artificial Analysis and provider benchmarks: speed matters

Provider benchmarking is where many model comparisons become uncomfortable. The same model can feel different across providers because of batching, quantization, GPU fleet, routing, context caps, time-to-first-token, and output throughput.

Artificial Analysis model/provider pages for Qwen3-Coder and Llama 4 Maverick emphasize price, output speed, latency, and provider variation ([Artificial Analysis Qwen3-Coder providers](https://artificialanalysis.ai/models/qwen3-coder-480b-a35b-instruct/providers), [Artificial Analysis Llama 4 Maverick providers](https://artificialanalysis.ai/models/llama-4-maverick/providers)). The extracted pages did not preserve every chart value cleanly, but they confirm the right dimensions: price, output tokens/sec, latency, context window, JSON/function calling support, and provider choice.

DeepInfra’s own Qwen3-Coder provider benchmark is more directly actionable. It compares Qwen3-Coder 480B across providers and says DeepInfra’s Turbo route had the lowest blended price and tied-lowest time-to-first-token, while Qwen on Cerebras had much higher output throughput and higher price; it also notes JSON-mode availability differences ([DeepInfra Qwen3-Coder benchmark](https://deepinfra.com/blog/qwen3-coder-480b-a35b-api-benchmarks)).

This is why a one-week evaluation should not only ask “which model?” It should ask “which model/provider route?” The same Qwen model at a cheap provider and a fast provider may serve different roles:

- cheap Qwen for batch reading and simple patches;
- fast Qwen/Cerebras for interactive editing;
- Kimi for harder agentic work;
- Opus/GPT for escalation.

## GitHub signal: maturity and integration surface

GitHub search found official and integration repos with strong activity:

| Repo | Signal from local GitHub probe | Why it matters |
|---|---:|---|
| [QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder) | ~16.5K stars, updated on capture date | Official code/model ecosystem, Qwen Code links, function-call notes. |
| [MoonshotAI/Kimi-K2](https://github.com/MoonshotAI/Kimi-K2) | ~10.7K stars, updated on capture date | Official Kimi K2 line, 1T MoE / 32B active description, agentic positioning. |
| [MoonshotAI/Kimi-K2.5](https://github.com/MoonshotAI/Kimi-K2.5) | ~1.9K stars, updated on capture date | Tech-report and newer Kimi line signal. |
| [deepseek-ai/DeepSeek-V3](https://github.com/deepseek-ai/DeepSeek-V3) | ~103K stars, updated on capture date | Enormous community attention and open-weight infrastructure. |
| [Aider-AI/aider](https://github.com/Aider-AI/aider) | ~44K stars, updated on capture date | Mature terminal coding-agent benchmark and integration target. |
| [anomalyco/opencode](https://github.com/anomalyco/opencode) | ~156K stars, updated on capture date | Open-source coding-agent ecosystem with provider flexibility. |
| [fakerybakery/openbridge](https://github.com/fakerybakery/openbridge) | ~386 stars | Bridges Claude Code to other providers like GLM, Kimi, Qwen, DeepSeek. |
| [florath/qwen3-call-patch-proxy](https://github.com/florath/qwen3-call-patch-proxy) | ~36 stars | Small but revealing compatibility proxy for malformed Qwen tool calls in OpenCode. |

Stars are not quality. But official repos, recent updates, and compatibility projects help identify where real users are pushing the models.

The Qwen README is especially useful because it says Qwen3-Coder supports Qwen Code, CLINE, Claude Code, a special function-call format, native 256K context extendable to 1M with Yarn, and 358 coding languages; it also warns about updated tokenizer/tool parser requirements ([QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder)). That is both a feature list and a gotcha list.

The Kimi README says Kimi K2 is a 1T-parameter MoE with 32B active parameters, trained for frontier knowledge, reasoning, coding, tool use, and autonomous problem-solving ([MoonshotAI/Kimi-K2](https://github.com/MoonshotAI/Kimi-K2)). That supports Kimi’s inclusion in the hard-coding slot, but the newest Kimi K2.6 claims still need direct evaluation.

## HN signal: what practitioners are actually discussing

HN is not ground truth, but it is a valuable “where are developers spending attention?” signal. The HN Algolia scrape produced high-engagement stories around exactly this market:

- Qwen3-Coder launch: 765 points / 366 comments linking to the official Qwen page.
- Qwen3-Coder-Next: 735 points / 429 comments linking to Qwen’s later page.
- Kimi K2 Thinking: 936 points / 427 comments.
- Kimi K2.6: 710 points / 372 comments linking to Kimi’s official page.
- Kimi K2.5 technical report: 388 points / 141 comments.
- A practitioner post about reallocating `$100/month` of Claude Code spend to Zed and OpenRouter: 349 points / 234 comments.
- OpenRouter outage/support concerns and status links surfaced as smaller but relevant threads.

The HN signal says the market is not hypothetical. Developers are trying to route coding-agent spend away from all-frontier subscriptions and into OpenRouter/open-model experiments. It also surfaces skepticism: outage reports, “OpenRouter going rogue?” complaints, China/privacy concerns around DeepSeek, and local-model enthusiasm.

How to use HN correctly:

- use it to find models, tools, and failure modes;
- do not cite comment claims as facts unless followed to primary sources;
- treat high comment counts as “contested and worth checking,” not “true.”

## Social/socli signal: spend reallocation and provider interest

The local `socli` search around OpenRouter/Kimi found practitioner-level discussion about using OpenRouter to replace or reduce Claude Code spend. The key pattern was not “everyone agrees OpenRouter is perfect.” It was “developers are actively experimenting with provider routers because single-vendor coding subscriptions are expensive and limiting.” This aligns with the HN story about reallocating `$100/month` Claude Code spend to Zed/OpenRouter.

The practical takeaway is to design your week like a spend-allocation experiment:

- baseline what Opus/GPT currently cost for your tasks;
- route cheap exploration to Qwen/DeepSeek/Llama;
- route hard open-model attempts to Kimi;
- escalate only failed/hard tasks to Opus/GPT;
- compare total accepted-work cost.

## Vendor benchmark claims: useful but label them

Qwen’s launch page includes charts and claims about agentic coding and SWE-bench-style performance ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)). Kimi’s launch page includes claims about benchmark leadership, long-horizon coding runs, and partner usage ([Kimi K2.6](https://www.kimi.com/blog/kimi-k2-6)). OpenAI’s GPT-5.5 announcement includes benchmark tables for agentic, coding, reasoning, long-context, and multimodal tasks ([OpenAI GPT-5.5](https://openai.com/index/introducing-gpt-5-5/)). Anthropic’s Opus 4.7 announcement includes claims around coding and agentic performance ([Anthropic Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7)).

Vendor claims are allowed in this guide, but they are not neutral. Use them as:

- feature discovery;
- benchmark leads;
- model-role hypotheses;
- version/context/pricing references where official.

Do not use them as final proof that one model is best for your repo.

## Evidence-weighted candidate ranking

Based on benchmark, GitHub, HN, pricing, and provider evidence, rank candidates like this for the week:

### 1. Kimi K2.6 for hard open-weight coding

Evidence:

- official launch focuses directly on long-horizon coding and agentic work ([Kimi K2.6](https://www.kimi.com/blog/kimi-k2-6));
- HN attention is high;
- SWE-bench/LiveCodeBench ecosystem shows Kimi-family models in competitive regions ([SWE-bench](https://www.swebench.com/), [Vals](https://www.vals.ai/benchmarks/lcb));
- price remains far below Opus/GPT ([OpenRouter Kimi K2.6](https://openrouter.ai/moonshotai/kimi-k2.6)).

Risk:

- vendor-heavy evidence;
- route/provider reliability must be measured;
- more expensive than Qwen/DeepSeek/Llama.

### 2. Qwen3-Coder for cheap coding-agent work

Evidence:

- official agentic-coding focus and tool integrations ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/));
- official GitHub repo, Qwen Code, function-call docs ([QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder));
- strong provider availability and low price ([OpenRouter Qwen3-Coder](https://openrouter.ai/qwen/qwen3-coder), [DeepInfra pricing](https://deepinfra.com/pricing));
- provider benchmark coverage ([DeepInfra Qwen benchmark](https://deepinfra.com/blog/qwen3-coder-480b-a35b-api-benchmarks)).

Risk:

- tool-call parser/version issues;
- 262K practical endpoint context in common hosted routes.

### 3. DeepSeek V4/V3.1 for cheap long-context and reasoning

Evidence:

- very low direct API price and 1M context ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing));
- LiveCodeBench shows DeepSeek V4 near top coding/problem-solving results ([Vals](https://www.vals.ai/benchmarks/lcb));
- SWE-bench/Aider show strong DeepSeek-family entries ([SWE-bench](https://www.swebench.com/), [Aider](https://aider.chat/docs/leaderboards/)).

Risk:

- direct privacy posture unsuitable for sensitive code ([DeepSeek privacy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html));
- model/version churn.

### 4. Llama 4 Maverick for cheap long-context control

Evidence:

- 1M-class context at very low price via OpenRouter/DeepInfra ([OpenRouter Llama 4 Maverick](https://openrouter.ai/meta-llama/llama-4-maverick), [DeepInfra pricing](https://deepinfra.com/pricing));
- open model ecosystem and provider availability ([Llama 4](https://www.llama.com/models/llama-4/));
- provider benchmark coverage ([Artificial Analysis Llama providers](https://artificialanalysis.ai/models/llama-4-maverick/providers)).

Risk:

- not the strongest coding evidence in this set;
- use as a read/summarize/control model unless it proves itself.

### 5. Opus/GPT-5.5 as quality baselines

Evidence:

- official positioning for professional coding and agentic work ([Anthropic Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7), [OpenAI GPT-5.5](https://openai.com/index/introducing-gpt-5-5/));
- high benchmark positions for frontier closed families;
- existing developer trust and tool support.

Risk:

- high cost;
- GPT-5.5 long-context surcharge; Opus tokenizer/effort token changes ([GPT-5.5 docs](https://developers.openai.com/api/docs/models/gpt-5.5), [Opus docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7)).

## The benchmark lesson

The evidence does **not** support a simple “open weights now beat Opus/GPT” conclusion. It supports a more useful conclusion:

> Open-weight coding models are now good enough, cheap enough, and hosted widely enough that they deserve a measured tier in a coding-agent workflow. They are not automatically safe, not uniformly reliable, and not guaranteed to replace expensive frontier models on hard tasks.

That is the hypothesis the one-week protocol tests.
