# 08 — Coding-agent setup patterns and gotchas

## Goal

This chapter is not a complete manual for every coding tool. It gives setup patterns that keep the one-week evaluation controlled: OpenAI-compatible endpoints, provider routing, data policy, context budgeting, and validation loops.

The details will vary across Aider, OpenCode, Claude Code-compatible bridges, Cline, Qwen Code, custom scripts, and your own harness. The principles are stable.

## Pattern 1: Use OpenAI-compatible endpoints where possible

Most hosted open-weight APIs expose an OpenAI-compatible chat/completions interface. That lets you swap models without rewriting your coding agent.

Examples from source pages:

- Qwen’s launch page shows OpenAI-compatible usage for Qwen Code and other tools, including API base URL and model name setup ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)).
- DeepSeek’s pricing/API page lists OpenAI-format and Anthropic-format API base URLs, plus OpenAI SDK examples ([DeepSeek pricing/API quick start](https://api-docs.deepseek.com/quick_start/pricing)).
- OpenRouter exposes an OpenAI-compatible API and model IDs across many providers/model routes ([OpenRouter docs](https://openrouter.ai/docs)).
- DeepInfra exposes OpenAI-compatible inference for many hosted models and publishes API docs/pricing ([DeepInfra pricing](https://deepinfra.com/pricing)).

A generic environment shape looks like:

```bash
export OPENAI_API_KEY="$PROVIDER_KEY"
export OPENAI_BASE_URL="https://provider.example/v1"
export MODEL="provider/model-id"
```

Actual variable names depend on the tool. Some use `OPENAI_API_BASE`; some use `OPENAI_BASE_URL`; some have config files.

## Pattern 2: Keep model ID and provider route explicit

A model ID alone is not enough. In a gateway like OpenRouter, a model can be served by many providers. OpenRouter’s provider routing docs explain sorting, ignored providers, fallback, and provider preferences ([OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)). OpenRouter’s ZDR docs show a per-request provider preference like requiring `zdr: true` ([OpenRouter ZDR](https://openrouter.ai/docs/guides/features/zdr)).

For evaluation logs, record both:

```text
model: qwen/qwen3-coder
provider: DeepInfra via OpenRouter
route_pinned: yes
zdr_required: yes
```

If your tool cannot expose provider routing settings, use direct provider APIs for sensitive tests or restrict the OpenRouter account settings globally.

## Pattern 3: Separate reading model from editing model

Many coding-agent failures come from asking one model to do everything. Use roles:

```text
Reader: cheap, long context, may be weaker at patches
Editor: stronger coding model, stable tool calls
Reviewer: expensive frontier baseline or human
```

Example routing:

- Llama 4 Maverick or DeepSeek V4 reads 600K tokens and produces a subsystem map.
- Qwen3-Coder or Kimi K2.6 receives the curated map and relevant files to patch.
- Opus/GPT reviews hard diffs or handles failures.

This exploits price differences. Llama 4 Maverick is around `$0.15/M` input and `$0.60/M` output on OpenRouter/DeepInfra ([OpenRouter Llama 4 Maverick](https://openrouter.ai/meta-llama/llama-4-maverick), [DeepInfra pricing](https://deepinfra.com/pricing)). Kimi is more expensive but may be better for hard edits ([OpenRouter Kimi K2.6](https://openrouter.ai/moonshotai/kimi-k2.6)). Opus/GPT are much more expensive but strong baselines ([Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing), [OpenAI pricing](https://openai.com/api/pricing/)).

## Pattern 4: Reserve output context

Do not fill the whole context with files. Reserve space for:

- model plan;
- tool results;
- diffs;
- test failures;
- retries;
- final explanation.

For a 262K route such as OpenRouter Qwen3-Coder or Kimi K2.6, a practical coding input budget is often 180K–220K, not 262K ([OpenRouter Qwen3-Coder](https://openrouter.ai/qwen/qwen3-coder), [OpenRouter Kimi K2.6](https://openrouter.ai/moonshotai/kimi-k2.6)). For GPT-5.5, 1M context is real in the docs, but prompts above 272K input trigger higher pricing for the full session ([GPT-5.5 docs](https://developers.openai.com/api/docs/models/gpt-5.5)). For Opus 4.7, 1M context and 128K max output exist, but tokenizer changes can increase token counts ([Opus 4.7 docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7)).

Practical input budgets:

| Route | Advertised context | Safe first input budget |
|---|---:|---:|
| Qwen3-Coder via OpenRouter/DeepInfra | 256K/262K | 180K–220K |
| Kimi K2.6 via OpenRouter | 262K | 180K–230K |
| DeepSeek V4 direct | 1M | 600K–900K, depending output reserve |
| Llama 4 Maverick | 1M | 700K–950K for reading; less for patching |
| Opus 4.7 | 1M | 800K–900K |
| GPT-5.5 | 1.05M | under 272K for cheap tier; 800K+ only when worth surcharge |

## Pattern 5: Use file lists before file dumps

Long context is tempting. Resist dumping the whole repo by default. First ask a cheap model to build a file map from filenames, package manifests, and small snippets. Then load full files selectively.

A good context pipeline:

```text
1. Send tree + README + test names.
2. Ask model to identify relevant files.
3. Send selected files.
4. Ask for plan.
5. Edit only after plan is checked.
6. Run validation.
```

This often beats whole-repo context because it keeps signal high and cost low. Long context is most useful when the task genuinely requires cross-file evidence.

## Pattern 6: Force validation into the loop

Every coding agent prompt should include the exact validation command. Do not ask “does this look right?” Ask the agent to run tests.

Prompt skeleton:

```text
Task: <task>

Before editing:
- inspect relevant files;
- summarize plan in 3 bullets.

Editing rules:
- smallest correct diff;
- no unrelated files;
- preserve public API unless task says otherwise.

Validation:
- run: <command>
- if it fails, inspect error and fix once;
- report final command output.
```

Why this matters: benchmarks like Aider and SWE-bench measure code edits under validation-like conditions, not just chat quality ([Aider leaderboards](https://aider.chat/docs/leaderboards/), [SWE-bench](https://www.swebench.com/)). Your local process should do the same.

## Pattern 7: Detect tool-call incompatibility early

Before a real task, run a tiny tool-call smoke test:

1. ask the model to read one file;
2. ask it to edit one line in a disposable file;
3. ask it to run `echo ok` or a trivial test;
4. verify the tool call parses and the model recovers from a fake failure.

Qwen’s repository explicitly warns that Qwen3-Coder function calling relies on newer parsers/tokenizer behavior in SGLang/vLLM ([QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder)). GitHub search surfaced `qwen3-call-patch-proxy`, a small proxy that fixes malformed Qwen tool calls for OpenCode ([florath/qwen3-call-patch-proxy](https://github.com/florath/qwen3-call-patch-proxy)). That does not mean Qwen is unreliable; it means you should smoke-test your exact harness.

## Pattern 8: Handle reasoning/thinking modes deliberately

Some models expose reasoning or thinking modes. DeepSeek’s docs describe thinking and non-thinking modes, with features like JSON output, tool calls, FIM completion, and chat prefix completion depending on mode ([DeepSeek pricing/API page](https://api-docs.deepseek.com/quick_start/pricing)). Anthropic Opus 4.7 docs mention effort settings and recommend high or xhigh for coding/agentic workloads ([Opus 4.7 docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7)).

Do not mix modes in a benchmark without logging them. A “cheap model failed” conclusion is weak if it was run in a low-reasoning mode against an Opus high-effort baseline.

Log:

```text
reasoning_mode:
thinking_budget:
effort:
max_output_tokens:
```

## Pattern 9: Avoid accidental prompt logging

OpenRouter says private I/O logging is off by default and prompts/responses are not stored unless you opt in, but you can enable logging for troubleshooting ([OpenRouter data collection](https://openrouter.ai/docs/guides/privacy/data-collection)). That can be useful for public benchmarks and dangerous for private code. DeepInfra says inference data is not stored to disk under its described inference flow ([DeepInfra privacy](https://docs.deepinfra.com/account/data-privacy)). DeepSeek direct has a different privacy posture ([DeepSeek privacy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)).

Checklist:

- disable prompt/completion logging for private code;
- avoid copying prompts into issue trackers;
- scrub `.env`, secrets, tokens, and production logs;
- do not let the agent read your whole home directory;
- use allowlisted paths;
- keep evaluation logs to metadata and summaries, not raw prompts, unless safe.

## Pattern 10: Use escalation as a first-class tool

Do not force cheap models to solve everything. Define escalation triggers:

- two failed test-fix attempts;
- repeated tool/schema errors;
- model wants to rewrite too many files;
- ambiguous architecture decision;
- security-sensitive change;
- patch is plausible but untrusted.

Escalation prompt to Opus/GPT:

```text
An open-weight model attempted this task and produced the following diff/plan.
Review it critically. Do not assume it is correct. Identify issues, then either
fix the minimal necessary code or explain why the approach should be abandoned.
Validation command: <command>.
```

This lets cheap models do exploration while frontier models act as closers.

## Tool-specific notes

### Aider

Aider has direct model support and public leaderboards. The Aider benchmark is relevant because it measures edit success and correct edit format ([Aider leaderboards](https://aider.chat/docs/leaderboards/)). When using Aider with OpenRouter or OpenAI-compatible providers, log model names and edit format. If a model struggles with diffs, try Aider-supported edit modes before rejecting the model, but keep the comparison fair.

### OpenCode

OpenCode-style tools are useful for provider flexibility, and the GitHub ecosystem contains compatibility projects. The `qwen3-call-patch-proxy` repo is specifically about malformed Qwen3-Coder tool calls for OpenCode ([qwen3-call-patch-proxy](https://github.com/florath/qwen3-call-patch-proxy)). If you use OpenCode, test Qwen tool calls before real work.

### Claude Code-compatible bridges

Qwen’s page includes Claude Code integration examples through proxy/router patterns ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)). The GitHub search found `openbridge`, described as a way to use Claude Code with providers such as GLM-4.5, Kimi-K2, Qwen3-Coder, and DeepSeek ([fakerybakery/openbridge](https://github.com/fakerybakery/openbridge)). Bridge tools can be powerful, but they add another compatibility layer. If something fails, identify whether the failure is model, provider, bridge, or Claude Code assumption.

### Qwen Code and Cline

Qwen’s launch page promotes Qwen Code and Cline setup for Qwen3-Coder ([Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/)). These may provide the best native Qwen experience. But if your normal workflow is another coding agent, compare both native and normal harness only if you have time. Otherwise, test the model where you actually work.

## Debugging failures

### Symptom: invalid JSON/tool call

Possible causes:

- model-specific function-call parser mismatch;
- provider route not supporting tool calls;
- bridge translating schema incorrectly;
- prompt encourages free-form output.

Fixes:

- test a direct provider route;
- add stricter tool-call instructions;
- change model/provider;
- use a compatibility proxy if appropriate;
- lower task complexity.

### Symptom: context-limit error

Possible causes:

- provider route context lower than model card;
- max output reserve too large;
- hidden system/tool tokens;
- routing fallback to smaller-context provider.

Fixes:

- inspect provider page;
- pin provider;
- reduce files;
- reserve output;
- chunk with summaries.

### Symptom: good plan, bad patch

Possible causes:

- model is better reader than editor;
- context contains too much irrelevant code;
- tests not included;
- patch budget too broad.

Fixes:

- use model as reader only;
- send fewer files;
- require tests first;
- escalate patch to Kimi/Opus/GPT.

### Symptom: cheap route costs more than expected

Possible causes:

- repeated retries;
- long outputs;
- provider fallback to higher price;
- GPT-5.5 long-context surcharge;
- hidden reasoning tokens.

Fixes:

- cap max turns;
- log provider/route;
- cap output tokens;
- avoid >272K GPT-5.5 unless intentional;
- use cheaper reader model.

## Minimal setup recommendation

For the first week, use this simple architecture:

```text
OpenRouter account:
  - low prepaid balance
  - ZDR/provider policy controls
  - routes: Kimi K2.6, Qwen3-Coder, Llama 4 Maverick, DeepSeek if acceptable

DeepInfra account:
  - direct backup for Qwen3-Coder and Llama 4
  - privacy-simple route for private-ish experiments

Direct DeepSeek account:
  - optional, public/redacted only
  - cheap 1M-context exploration

Existing Opus/GPT account:
  - baselines and escalation
```

This gives you breadth without too many moving parts.

## The golden rule

Every time you change **model**, **provider**, **route**, **reasoning mode**, **tool harness**, or **context size**, you changed the experiment. Record it. Otherwise the week ends with vibes instead of evidence.
