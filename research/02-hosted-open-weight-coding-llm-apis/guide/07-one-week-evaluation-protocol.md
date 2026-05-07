# 07 — A one-week evaluation protocol you can actually run

## Purpose

The purpose of this week is not to crown a universal winner. The purpose is to answer a narrow operational question:

> Which hosted open-weight model/provider routes can reduce my Opus/GPT-5.5 coding-agent spend without violating my safety policy or increasing human review/debug time too much?

That means every run must be comparable. Same task. Same repository state. Same validation commands. Same logging. Same human-review rubric.

## What success looks like

At the end of the week, you should be able to say one of these:

1. **Adopt broadly:** an open-weight route handles most tasks with acceptable quality, cost, and policy.
2. **Adopt as cheap first pass:** open models handle reading, tests, simple patches, and drafts; Opus/GPT handle hard work.
3. **Adopt for long-context reading only:** open models are useful for repo digestion but not trusted for final patches.
4. **Reject for now:** cheap routes burn too much time or fail safety/reliability gates.

The expected result is usually option 2 or 3.

## Pre-week setup

### 1. Define data classes

Before any API call, label what you are allowed to send.

| Data class | Examples | Allowed routes |
|---|---|---|
| Public | OSS repo, public docs, synthetic benchmark tasks | Any route with spend cap |
| Redacted | private code with secrets/client data removed | OpenRouter ZDR/provider-filtered, DeepInfra direct, approved routes |
| Private | internal proprietary code | only routes that satisfy your policy |
| Sensitive | secrets, credentials, security bugs, client data, regulated data | do not use ad-hoc hosted open-weight APIs |

This is not bureaucracy. DeepSeek direct may be the cheapest route, but its privacy policy says prompts/inputs may be collected, retained, used to improve/train technology, and stored/processed in China ([DeepSeek privacy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)). OpenRouter and DeepInfra have different data-handling claims ([OpenRouter data collection](https://openrouter.ai/docs/guides/privacy/data-collection), [DeepInfra data privacy](https://docs.deepinfra.com/account/data-privacy)). You need to know what you are sending.

### 2. Create provider budget caps

Suggested caps:

| Provider | First-week cap |
|---|---:|
| OpenRouter | `$10` |
| DeepInfra | `$5–10` |
| DeepSeek direct | `$5`, public/redacted only |
| Opus/GPT baselines | `$20–50` depending task count |

Disable auto-recharge. Long-context retries can multiply cost. GPT-5.5’s docs say prompts above 272K input tokens are priced at 2x input and 1.5x output for the full session ([GPT-5.5 docs](https://developers.openai.com/api/docs/models/gpt-5.5)). Do not discover that accidentally.

### 3. Pick the model roster

Use this roster:

- Kimi K2.6 via OpenRouter provider-filtered route;
- Qwen3-Coder via DeepInfra direct and/or OpenRouter provider-pinned route;
- DeepSeek V4 Flash/Pro direct for non-sensitive tasks, or DeepSeek V3.1 Terminus through OpenRouter if you need the gateway;
- Llama 4 Maverick via DeepInfra/OpenRouter;
- Claude Opus 4.7 baseline;
- GPT-5.5 baseline.

Do not add more models until you have data. Extra models create noise.

### 4. Define validation commands

For each repository, write the commands once:

```bash
# Example only; replace with repo commands
make test
make lint
make typecheck
make build
```

If a task cannot be validated mechanically, it is a weak evaluation task. Include some subjective tasks, but the week should be dominated by mechanically checkable work.

### 5. Create the run log

Create `model-eval-log.csv` or a Markdown table with these fields:

```text
date,task_id,repo,data_class,model,provider,route_pinned,zdr_required,
input_tokens,output_tokens,cost_usd,wall_clock_minutes,request_errors,
tool_schema_errors,context_errors,test_command,tests_passed,human_interventions,
final_status,review_notes
```

The final status values should be constrained:

- `accepted` — merged or would merge with no human code edits;
- `edited` — useful but required human code edits;
- `discarded` — not useful enough;
- `escalated` — moved to Opus/GPT or another model;
- `unsafe` — tried to send data to unacceptable route or exposed sensitive information.

## Task suite

Use at least 12 tasks. The exact number can be smaller if tasks are expensive, but 12 gives you enough variety.

### Category A: repository reading

Goal: measure cheap context comprehension.

Tasks:

1. Explain a module’s architecture from source files.
2. Trace a data flow from input to output.
3. Find likely files for a bug report.
4. Summarize test coverage gaps.

Candidate routes:

- Llama 4 Maverick;
- DeepSeek V4 Flash direct if data class permits;
- Qwen3-Coder for 200K-class contexts;
- Opus/GPT baseline for one or two runs.

Validation:

- compare answer against code;
- check whether cited files/functions exist;
- score hallucinations;
- track context size.

### Category B: simple patches

Goal: measure basic accepted-patch cost.

Tasks:

1. Fix a failing unit test.
2. Add a small option/flag with existing patterns.
3. Update docs from code behavior.
4. Add missing edge-case tests.

Candidate routes:

- Qwen3-Coder;
- Kimi K2.6;
- DeepSeek;
- Opus/GPT baseline.

Validation:

- tests pass;
- diff is minimal;
- style matches project;
- no unrelated rewrites.

### Category C: medium multi-file changes

Goal: measure real coding-agent utility.

Tasks:

1. Implement a small feature across 3–6 files.
2. Refactor a function/class with tests.
3. Add input validation across API + tests + docs.
4. Migrate a small deprecated API call.

Candidate routes:

- Kimi K2.6 first;
- Qwen3-Coder second;
- Opus/GPT baseline;
- DeepSeek if non-sensitive.

Validation:

- full test command;
- review for pattern adherence;
- count human interventions;
- inspect whether the model created hidden complexity.

### Category D: hard/ambiguous tasks

Goal: identify escalation boundary.

Tasks:

1. Debug a failing integration test with misleading symptoms.
2. Propose and implement a small architecture improvement.
3. Fix a flaky test by identifying root cause.
4. Make a change requiring careful backward compatibility.

Candidate routes:

- Kimi K2.6;
- Opus 4.7;
- GPT-5.5;
- optionally Qwen/DeepSeek if earlier results are strong.

Validation:

- acceptance tests;
- human code review;
- design review;
- time-to-solution.

Hard tasks are where cheap models may lose despite low token price. Track review debt carefully.

## Daily schedule

### Day 0: environment and dry run

- Add API keys.
- Confirm OpenRouter privacy/ZDR/provider settings.
- Confirm DeepInfra direct route works.
- Confirm DeepSeek direct only with non-sensitive data.
- Run one trivial prompt per model.
- Confirm token/cost logging.
- Confirm validation commands.

Do not evaluate quality yet. Day 0 is plumbing.

### Day 1: reading tasks

Run Category A tasks through Llama 4, DeepSeek, Qwen, and one frontier baseline. The goal is to learn context/cost behavior.

Questions:

- Which route can ingest enough files?
- Which route hallucinates least?
- Which route is fast enough?
- Is a 1M context route useful, or does it drown in context?

Expected result:

- Llama/DeepSeek are very cheap reading candidates.
- Qwen is better if the task stays within 200K-class context.
- Opus/GPT gives quality reference but costs much more.

### Day 2: simple patches

Run Category B tasks. Use Qwen, Kimi, DeepSeek, and one baseline. Each task should have tests.

Questions:

- Does Qwen produce valid edits/tool calls?
- Does Kimi justify its higher price?
- Does DeepSeek make correct patches or only plausible ones?
- How much human repair is needed?

Expected result:

- Qwen should be attractive on cost if integration works.
- Kimi may look overqualified for simple tasks.
- DeepSeek may be excellent on public/simple tasks, but do not forget data policy.

### Day 3: provider route comparison

Pick the best model from Day 2 and compare providers:

- Qwen via DeepInfra direct vs OpenRouter provider-pinned route;
- Kimi via OpenRouter route(s) if multiple providers are available;
- Llama via DeepInfra vs OpenRouter if relevant.

Measure:

- time-to-first-token;
- output throughput;
- request errors;
- schema errors;
- total cost;
- final diff quality.

This is where provider benchmarks meet reality. Artificial Analysis and DeepInfra pages show provider variation ([Artificial Analysis Qwen providers](https://artificialanalysis.ai/models/qwen3-coder-480b-a35b-instruct/providers), [DeepInfra Qwen benchmark](https://deepinfra.com/blog/qwen3-coder-480b-a35b-api-benchmarks)). Your harness may have different bottlenecks.

### Day 4: medium changes

Run Category C tasks. Kimi and Qwen are the main open candidates. Run Opus/GPT on a subset for baseline.

Questions:

- Which model preserves architecture?
- Which model follows tests and tooling?
- Which model over-edits?
- Does Kimi close the quality gap enough to become default?

Expected result:

- Kimi may be strongest among open candidates for multi-step tasks.
- Qwen may be better cost/value if diffs are valid.
- Opus/GPT may still require fewer human interventions.

### Day 5: hard tasks

Run Category D tasks. Limit the number; they are expensive in human time.

Questions:

- Where do open models fail?
- Are failures obvious or subtle?
- Does a cheap model produce a useful plan even if it cannot finish?
- Is escalation to Opus/GPT faster than repeated open-model retries?

Expected result:

- frontier models may still win on hard ambiguous tasks;
- Kimi/Qwen may still be useful for investigation/planning;
- repeated cheap retries can become a time sink.

### Day 6: rerun with improved prompting

Now that you know failure modes, give open models a fair second pass. Improve only general instructions, not task-specific hints that the baseline did not receive.

Possible improvements:

- require a plan before edits;
- require minimal diffs;
- require test-first behavior;
- require tool-call JSON discipline;
- limit max files changed;
- require citing files/functions before modifications.

Do not keep tweaking until every model wins. The goal is a maintainable workflow, not a benchmark hack.

### Day 7: score and decide

Compute:

```text
accepted_rate = accepted_tasks / attempted_tasks
useful_rate = (accepted + edited) / attempted_tasks
avg_cost_accepted = total_cost / accepted_tasks
avg_wall_clock_accepted = total_minutes / accepted_tasks
schema_error_rate = schema_errors / attempted_tasks
escalation_rate = escalated / attempted_tasks
```

Then fill this decision table:

| Route | Accepted rate | Useful rate | Avg cost accepted | Avg minutes accepted | Policy OK? | Recommended role |
|---|---:|---:|---:|---:|---|---|
| Kimi K2.6 | | | | | | |
| Qwen3-Coder | | | | | | |
| DeepSeek | | | | | | |
| Llama 4 | | | | | | |
| Opus 4.7 | | | | | | |
| GPT-5.5 | | | | | | |

## Scoring rubric

Use a 0–3 score for each dimension.

### Correctness

- 0: fails tests or cannot produce usable output;
- 1: partial idea but broken implementation;
- 2: tests pass after human edits;
- 3: tests pass without human code edits.

### Patch quality

- 0: unrelated rewrites or dangerous changes;
- 1: works but ugly/fragile;
- 2: mostly matches project style;
- 3: minimal, idiomatic, maintainable.

### Agent reliability

- 0: repeated tool/schema failures;
- 1: occasional parse/tool issues;
- 2: mostly stable;
- 3: stable across task types.

### Cost

- 0: close to Opus/GPT without quality;
- 1: 2–5x cheaper;
- 2: 5–10x cheaper;
- 3: >10x cheaper for comparable usefulness.

### Safety/policy

- 0: unacceptable for data sent;
- 1: acceptable only for public/redacted tasks;
- 2: acceptable for private hobby/internal low-risk code;
- 3: acceptable for your target production data class.

A model that scores 3 on cost and 0 on safety is not a default model. A model that scores 3 on correctness and 0 on cost is a baseline, not a savings route.

## Prompt template for comparable runs

Use a neutral prompt structure across models:

```text
You are working in <repo>. Task: <task>.

Rules:
- First inspect relevant files before editing.
- Make the smallest correct change.
- Follow existing style and tests.
- Do not modify unrelated files.
- After editing, run: <validation commands>.
- If tests fail, debug once and rerun.
- Report: changed files, validation result, remaining risks.

Data sensitivity: <public/redacted/private>. Do not include secrets in output.
```

For tool-call-prone models, add:

```text
Use valid tool calls only. Do not invent tool names. If a tool fails,
read the error and continue with the available tools.
```

For over-editing models, add:

```text
Patch budget: change at most <N> files unless you explicitly explain why more are required.
```

## Logging examples

Example row:

```text
2026-05-08,T03,public-cli,Qwen3-Coder,DeepInfra,yes,yes,
185000,8200,0.064,14,0,1,0,"make test",yes,1,edited,
"Good plan and tests; one tool-call retry; needed naming cleanup."
```

Example summary:

```text
Qwen3-Coder: best cost/value on simple patches; occasional tool-call parse errors.
Kimi K2.6: best open route for medium multi-file changes; slower but higher acceptance.
DeepSeek V4: excellent cheap reader on public repo; not used for private code.
Llama 4: cheap long-context summaries; weak final patch quality.
Opus: still best hard-task closer.
GPT-5.5: strong long-context baseline but expensive above 272K input.
```

## Common evaluation mistakes

### Mistake 1: comparing different tasks

If Qwen gets the easy bug and Opus gets the hard architecture migration, you learned nothing. Use paired tasks.

### Mistake 2: ignoring output price

Coding agents can produce long outputs. Kimi’s `$3.50/M` output is still cheap versus Opus/GPT, but it is much more than Llama/DeepSeek. Track output.

### Mistake 3: filling the context window unnecessarily

Long context is not free. A model may do better with curated files than with the whole repo. Test both curated and broad context.

### Mistake 4: treating a partial patch as success

If you had to rewrite half the model’s diff, log it as `edited`, not `accepted`.

### Mistake 5: ignoring provider route

“Qwen failed” may mean “this provider’s Qwen tool-call implementation failed.” Record provider and route.

### Mistake 6: sending sensitive data during curiosity tests

Use public/redacted tasks until the provider policy is reviewed.

## Decision examples

### If Kimi wins medium/hard tasks

Adopt:

```text
Default: Kimi K2.6 for medium coding tasks.
Cheap read/simple: Qwen or Llama.
Escalation: Opus/GPT.
```

### If Qwen is stable and cheap

Adopt:

```text
Default first pass: Qwen3-Coder.
Hard retry: Kimi.
Escalation: Opus/GPT.
```

### If DeepSeek is best but policy blocks it

Adopt only for public/redacted tasks:

```text
Public OSS: DeepSeek V4.
Private code: Qwen/DeepInfra or OpenRouter ZDR route.
Escalation: Opus/GPT.
```

### If all open models require too much review

Adopt for reading only:

```text
Repo summaries/log triage: Llama/DeepSeek/Qwen.
Code edits: Opus/GPT.
```

That is still a useful savings pattern because reading tokens dominate many agent sessions.

## Final deliverable from the week

At the end, save a short decision note:

```markdown
# Hosted open-weight coding API evaluation — <date>

## Routes tested

## Repositories/tasks

## Data policy used

## Results table

## Accepted roles

## Rejected routes and why

## Budget spent

## Next refresh date
```

This turns a one-week experiment into durable operational knowledge.
