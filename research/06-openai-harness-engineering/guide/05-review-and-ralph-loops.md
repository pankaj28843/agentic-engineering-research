# 05 - Review And Ralph Loops

OpenAI's [blog](https://openai.com/index/harness-engineering/) says humans interact with the system mostly through prompts, let Codex open pull requests, instruct Codex to review its own changes locally, request specific agent reviews both locally and in the cloud, respond to feedback, and iterate until agent reviewers are satisfied. It calls this effectively a Ralph Wiggum Loop. The post also says human review is possible but not always required, and that review effort has moved toward agent-to-agent review.

This is a major process shift. In a human-first workflow, code review is a social and technical checkpoint. In a high-throughput agent workflow, review becomes another feedback channel in the harness. The review must be precise enough for the authoring agent to act on, and the authoring agent must be allowed to push back when the review is wrong.

OpenAI's official [Codex code review in GitHub](https://developers.openai.com/codex/github/code-review/) docs describe a public version of this idea: Codex can review pull request diffs, follow repository guidance, and post focused GitHub reviews. The saved docs say Codex flags serious issues and can be requested with `@codex review` or enabled for automatic reviews. That is not identical to OpenAI's internal loop, but it shows the product surface that makes review another agent-readable event.

## ELI5

Imagine a student writes an essay, then another student checks it, then the first student fixes it, then a third student checks the fix. The teacher does not need to rewrite every sentence. The teacher sets the rubric and checks the final result.

A Ralph-style loop is the essay cycle for code. The author agent writes, reviewer agents critique, the author responds, tests run, and the loop continues until the rubric is met or a real blocker appears.

## Review As A Prompt Channel

The video transcripts reinforce the idea that everything becomes a prompt channel: tests, logs, review comments, error messages, docs, and even lints. In the `CeOXx-XTYek` transcript, the discussion around review describes authoring agents responding to review feedback, and the need for reviewer agents to bias toward important findings rather than noisy comments. The transcript also discusses allowing the authoring agent to push back instead of blindly appeasing every reviewer.

This matters because naive agent review can create a bad loop:

1. Author agent opens PR.
2. Reviewer agent posts many low-value comments.
3. Author agent treats every comment as mandatory.
4. The PR grows.
5. More comments appear.
6. Human attention is burned anyway.

The harness must define review policy. Good review agents should focus on correctness, safety, architecture, and acceptance criteria. Good author agents should address real issues and explicitly push back on weak ones.

## A Review Protocol

A practical protocol:

- Every PR must include acceptance criteria and validation evidence.
- Authoring agent must run local self-review before external review.
- Reviewer agents must classify findings by severity and evidence.
- Authoring agent must either fix each actionable finding or reply with a reasoned rejection.
- Review comments from humans, agents, and CI are all pulled into one workpad.
- The loop ends only when required reviewers are satisfied or a blocker is recorded.

You can encode this in `AGENTS.md`:

```md
## PR Review Loop

Before handoff:

1. Run `make validate`.
2. Summarize acceptance criteria and evidence.
3. Run local self-review.
4. Request `@codex review` for correctness and security.
5. Address each actionable comment or reply with explicit pushback.
6. Re-run validation after changes.
```

Better, put the detailed policy in `docs/REVIEW.md` and keep `AGENTS.md` as a pointer.

## Local Self-Review

Self-review is cheap and often catches obvious issues. The authoring agent can inspect its own diff with a code-review stance:

```bash
git diff --stat
git diff -- src tests docs
make validate
```

Then prompt:

```text
Review this diff for correctness, missing tests, architecture violations, and mismatch with the acceptance criteria. Lead with concrete findings and file references. Do not comment on style unless it affects behavior or maintainability.
```

For a stronger local loop, spawn a separate agent in the same worktree but with a different prompt. Do not let it edit. Ask it to write a findings file:

```text
.agent-artifacts/review/local-review.md
```

The authoring agent then has to address that file. This keeps review artifacts durable.

## Agent-To-Agent Review

OpenAI's article says the team requests additional agent reviews locally and in the cloud. Public Codex docs show GitHub review as one cloud surface. You can also run local parallel reviewers:

```bash
codex exec --sandbox read-only \
  "Review this PR for security regressions. Write findings to .agent-artifacts/review/security.md"

codex exec --sandbox read-only \
  "Review this PR for architecture violations against docs/ARCHITECTURE.md. Write findings to .agent-artifacts/review/architecture.md"
```

The important constraint is read-only for reviewers unless you intentionally want a competing implementation. A reviewer should not quietly edit the PR. It should produce high-signal findings.

Review prompts should include negative guidance:

- Do not list speculative concerns without evidence.
- Do not request broad refactors outside the PR scope.
- Do not treat every preference as a blocker.
- Do include file paths, line references, and reproduction evidence.
- Do distinguish must-fix from optional.

## Ralph-Style Loops

A Ralph-style loop is a repeated same-prompt or same-policy execution loop. In OpenAI's description, Codex reviews, responds, gets reviewed again, and iterates until reviewers are satisfied. In your local harness, a loop can be as simple as:

```bash
while true; do
  make validate || exit 1
  codex exec --sandbox read-only "Review current diff. If no serious issues, write PASS to .agent-artifacts/review/status.txt."
  if rg -q '^PASS$' .agent-artifacts/review/status.txt; then
    break
  fi
  codex exec "Address actionable review findings in .agent-artifacts/review/*.md, then update validation notes."
done
```

That shell sketch is intentionally simple. A production loop needs stopping conditions:

- Maximum iterations.
- Maximum wall-clock time.
- Maximum token or cost budget.
- Required evidence after each iteration.
- Blocker detection.
- Human escalation when the loop repeats the same failure.

Without stop rules, loops waste money and can damage the codebase. OpenAI's blog still keeps humans in the loop at a higher layer. Autonomy is bounded.

## Throughput Changes Merge Philosophy

The OpenAI article says conventional merge norms can become counterproductive when agent throughput is high. Pull requests are short-lived, blocking gates are minimal, and some flakes are addressed with follow-up runs instead of blocking progress indefinitely. This would be reckless in some contexts. In OpenAI's described context, corrections are cheap and waiting is expensive.

The replicable lesson is not "drop all gates." It is "align gates with your correction cost." If your app has regulated data, production financial actions, or hard-to-roll-back migrations, you need stronger gates. If a change is low-risk, isolated, and covered by fast cleanup loops, blocking it for weak review comments may waste scarce attention.

Use a merge policy matrix:

| Risk | Examples | Merge posture |
|---|---|---|
| Low | docs, internal dev scripts, isolated UI copy | agent review plus validation may be enough |
| Medium | feature logic, API behavior, migrations with rollback | require targeted tests and human or senior-agent review |
| High | auth, billing, secrets, destructive data changes | require human review, security review, rollback plan, and production evidence |

This keeps autonomy tied to consequence.

## Human Review Still Matters

OpenAI does not remove humans. The blog says humans prioritize work, translate feedback into acceptance criteria, and validate outcomes. That is a different review layer. Instead of reading every line, a human can inspect:

- Was the task framed correctly?
- Are the acceptance criteria complete?
- Does validation evidence prove the behavior?
- Did reviewers find serious issues?
- Did the authoring agent address or reasonably reject them?
- Does the change preserve architecture and product intent?

This is more like reviewing a control system than reviewing a patch. It is still hard engineering work.

## Replication Steps

Create a review artifact directory:

```bash
mkdir -p .agent-artifacts/review
```

Add `docs/REVIEW.md`:

```md
# Review Policy

Reviewers must classify findings:

- Blocker: correctness, safety, security, data loss, or acceptance failure.
- Important: likely bug or maintainability issue.
- Optional: style or local improvement.

Authoring agents must fix blockers, decide important findings, and may ignore optional findings with a note.
```

Add a script:

```bash
#!/usr/bin/env bash
set -euo pipefail
mkdir -p .agent-artifacts/review
git diff --stat > .agent-artifacts/review/diffstat.txt
make validate | tee .agent-artifacts/review/validation.log
```

Then teach Codex:

```md
Before handoff, run `scripts/prepare-review`, request or perform review, and update `.agent-artifacts/review/summary.md`.
```

## The Review Loop As Harness

Review is not only a gate. It is a way to feed taste back into the system. A repeated review comment should become a doc, lint, test, or generator. A repeated false positive should become reviewer prompt guidance. A repeated merge failure should become a preflight check. This is how human judgment compounds instead of being spent repeatedly.

That is the OpenAI pattern in miniature: make feedback visible, make it actionable, encode the durable part, and let agents run the loop.

## Reviewer Roles

One reviewer agent should not try to be every reviewer. Split roles when the task is big enough:

- Correctness reviewer: bugs, edge cases, acceptance criteria, missing tests.
- Architecture reviewer: layer boundaries, dependency direction, module ownership.
- Security reviewer: secrets, auth, permissions, injection, unsafe network or filesystem use.
- UX reviewer: rendered behavior, accessibility, layout, copy, visual regression evidence.
- Release reviewer: migration, rollout, rollback, CI, production observability.

Each role gets a narrower prompt and produces fewer findings. This reduces noisy review. It also makes disagreements easier to resolve: a security blocker has a different standard from a style suggestion.

Example security reviewer prompt:

```text
Review only for security and data-safety regressions. Treat speculative issues as non-blocking unless there is a concrete exploit path. For each finding, include file path, risk, evidence, and a minimal fix. Do not comment on style or architecture unless it creates security risk.
```

Example architecture reviewer prompt:

```text
Review against docs/ARCHITECTURE.md and architecture.yaml. Focus on layer violations, duplicated boundary logic, and new dependencies. Do not request broad refactors outside this PR.
```

The authoring agent then receives role-labeled findings. A human can audit the role that matches the risk.

## Handling Disagreement

Agent-to-agent review needs a disagreement protocol. Without one, loops can oscillate. If the author rejects a finding, it should write the finding ID, decision, reason, evidence, and whether a human should decide.

Example:

```md
Finding SEC-2 rejected.
Reason: reviewer assumed user input reaches `exec`, but the value is parsed through `AllowedCommandSchema` and then matched against a constant allowlist.
Evidence: `src/commands/run.ts`, `tests/commands/run.test.ts`.
Human decision needed: no.
```

For high-risk disagreements, require human review. For low-risk disagreements, let the author proceed if validation passes and the rejection is reasoned.

## Loop Telemetry

Ralph-style loops should produce metrics: iteration count, findings per reviewer, findings accepted, findings rejected, validation failures by command, wall-clock time, token usage if available, and final state. This helps tune the harness. If one reviewer produces many rejected findings, its prompt is too broad or its standard is wrong. If validation fails after every accepted finding, authoring prompts may be making unscoped changes. If loops often hit max iterations, tasks may be too large.

Symphony's token accounting docs show why even token metrics need care: live usage can include cumulative totals and latest increments with different semantics. If you track loop cost, define exactly which event path is counted.

## Post-Merge Review

The OpenAI evidence suggests some human review shifts post-merge in high-throughput contexts. A safe local version is post-merge audit for low-risk changes: merge after validation and agent review, run staging or production monitors, have a cleanup/review agent scan merged changes daily, file follow-up issues for non-blocking improvements, and escalate regressions quickly.

This is not appropriate for every system. Use it for low-risk, reversible changes first. The harness question is whether correction is cheap enough and detection is fast enough. If not, keep pre-merge gates.

## Review Findings As Training Data For The Repo

After each meaningful review, ask whether the finding revealed a missing doc, missing lint, missing test, bad reviewer prompt, or ambiguous product acceptance criterion. Then update the durable substrate. This is how a team moves from spending attention to investing attention. A review comment that only fixes one PR is a cost. A review comment that becomes a lint or runbook is an asset.
