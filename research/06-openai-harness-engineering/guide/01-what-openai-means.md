# 01 - What OpenAI Means

OpenAI's [harness engineering post](https://openai.com/index/harness-engineering/) is easy to misread as a productivity story: a team used Codex, got a lot of code, and shipped quickly. That is true but too small. The more important story is that the team changed the job of engineering. Humans stopped being the direct source of code and became designers of the environment in which Codex could do the work.

The post says the team ran a five-month experiment building an internal beta software product with no manually written code. Codex wrote application logic, tests, CI configuration, documentation, observability, internal tools, review comments, scripts, and production dashboard definitions. The team reports roughly a million lines of code and about 1,500 pull requests, with a small human group steering the process. This is primary OpenAI evidence, not an independent benchmark. Still, the details matter because they explain how the output became possible.

The key phrase in the post is short enough to quote: "Humans steer. Agents execute." The sentence sounds simple, but it hides a large operating model. Steering is not passive supervision. It means selecting work, translating feedback into acceptance criteria, deciding what good looks like, building tools that expose missing context, and turning repeated judgment into reusable checks. Execution is not blind code generation. It means the agent can run tools, read docs, inspect app state, review feedback, open PRs, validate changes, and iterate.

## ELI5

Think about a remote-control car. A weak harness is like giving someone a car, a blindfold, and a vague instruction to "drive to the store." A strong harness is like giving the car headlights, mirrors, GPS, road signs, brakes, a dashboard, and a rule that it must stop at red lights. The driver still matters, but now the car can move safely for longer stretches.

In software, Codex is the driver. The harness is everything around it: repository instructions, source code, tests, browser controls, logs, metrics, traces, issue tracker, review comments, CI, and cleanup jobs. OpenAI's lesson is that the agent's output improves when those surfaces become clear enough for the agent to use.

## The Scarce Resource Is Human Attention

The OpenAI post frames human time and attention as the scarce resource. That one sentence explains many otherwise surprising choices. If human attention is scarce, then the harness should not optimize for the maximum number of human-readable prompts or review meetings. It should optimize for high-quality evidence that the agent can consume and that humans can audit quickly.

For example, a long instruction manual can feel helpful to humans, but the OpenAI article says the "one big AGENTS.md" approach failed. It used too much context, turned into non-guidance because everything was important, rotted quickly, and was hard to verify. The alternative was a short `AGENTS.md` as a map plus deeper versioned docs elsewhere in the repo. That is a context-management decision, but it is also a human-attention decision: maintain small entry points, then let agents follow links to the relevant source of truth.

The same attention logic explains browser validation. A human can visually inspect a page, notice an overflow, and tell Codex what is wrong. But if every UI fix requires a human to be the browser, human QA becomes the bottleneck. OpenAI says they made the app bootable per git worktree, wired Chrome DevTools Protocol into the runtime, and created skills for DOM snapshots, screenshots, and navigation. Now Codex can reproduce bugs and validate fixes directly. Human review can move from "look at every page" to "audit the evidence and decide whether this class of checks is adequate."

## What "Agent-Generated" Means

OpenAI's article is careful about the claim that the codebase is agent-generated. It does not mean humans are absent. It means humans do not directly write the code. Humans still prioritize, translate user feedback, define acceptance criteria, validate outcomes, and feed lessons back into the repository. The human role becomes more like a platform lead or engineering manager for a team of agents: decide what the system needs, encode rules, and inspect results.

This distinction matters for replication. Banning yourself from typing code is not the magic. The useful experiment is forcing every missing capability to become agent-accessible. If Codex cannot diagnose a startup regression, do not just fix the bug by hand. Add logs, metrics, a startup probe, a test, or a runbook so Codex can diagnose the next one. If Codex keeps violating an architecture rule, do not just write a review comment each time. Write a lint, structural test, or code generator that prevents the mistake.

That is the discipline: when the agent fails, ask what environmental capability is missing. The answer may be a tool, a document, a schema, a boundary parser, a test fixture, a dashboard, a local action, or a cleanup loop.

## The OpenAI System, Compressed

The internal harness described by OpenAI has several pieces that reinforce each other:

- Repository-local knowledge: a short `AGENTS.md`, structured docs, execution plans, design docs, architecture docs, and quality docs.
- App legibility: per-worktree app boot, CDP/browser control, screenshots, DOM snapshots, and navigation skills.
- Runtime legibility: local logs, metrics, traces, LogQL, PromQL, and worktree-scoped observability.
- Architecture legibility: fixed domain layers, allowed dependency directions, provider boundaries, structural tests, and custom lints.
- Review legibility: agent reviewers, local review, cloud review, human or agent feedback, and loops until reviewers are satisfied.
- Autonomy boundaries: humans still prioritize, translate feedback, validate outcomes, and handle judgment.
- Entropy control: golden principles, recurring cleanup, doc gardening, quality grades, and targeted refactoring PRs.

None of these pieces is exotic by itself. What is unusual is that they are arranged for agent legibility. A human-first repo often treats docs, tests, logs, and CI as helpful but secondary. In OpenAI's story, those artifacts are the product surface the agent works through.

## Practitioner Translation

For a Linux or macOS practitioner, the starting point is not to build a million-line product. It is to build one tiny vertical slice where the agent can see the whole loop.

Create a repo with a short `AGENTS.md`:

```md
# AGENTS.md

## Start Here

- Read `docs/ARCHITECTURE.md` before changing service boundaries.
- Read `docs/VALIDATION.md` before claiming a feature works.
- Run `make validate` before handoff.
- For UI work, run `make dev-worktree` and capture browser evidence.
```

Then add a small `docs/` tree:

```text
docs/
  ARCHITECTURE.md
  VALIDATION.md
  PRODUCT.md
  QUALITY.md
  plans/
    active/
    completed/
```

Next, make validation executable. Do not rely on "remember to check the page." Add a script:

```bash
#!/usr/bin/env bash
set -euo pipefail
npm test
npm run lint
npx playwright test
```

Finally, make the app inspectable per task. Use git worktrees:

```bash
git worktree add ../myapp-agent-123 -b agent/123
cd ../myapp-agent-123
npm install
PORT=4301 npm run dev
```

This is not yet OpenAI's harness, but it has the same shape: a task-specific workspace, a short map, deeper docs, and a validation command.

## What Not To Copy Blindly

Do not copy the "no manual code" constraint as a moral rule. It was a forcing function for OpenAI's experiment. For most teams, the better rule is: every repeated manual rescue should become a harness improvement. If a human fixes a bug by hand once, that may be fine. If a human fixes the same class of bug repeatedly, the harness is missing a capability.

Do not assume agent-generated code is inherently coherent. OpenAI explicitly discusses drift and cleanup. High throughput makes architectural decay faster unless the harness encodes architecture and taste.

Do not assume private OpenAI practices are fully public. The blog gives strong high-level evidence. The public [Symphony](https://github.com/openai/symphony) repo gives source-backed orchestration patterns. It does not prove the private internal implementation.

The reliable takeaway is narrower and more useful: Codex works better when the engineering environment is legible, bounded, inspectable, and self-correcting.

## Your First OpenAI-Shaped Task

The first task to try should be small but complete. Pick a UI bug or API behavior that can be reproduced, changed, validated, reviewed, and cleaned up in one branch. Do not start with a vague product epic. A good first task prompt:

```text
In a fresh worktree, reproduce the mobile settings footer overflow at /settings with viewport 390x844. Save before evidence. Fix the overflow without changing desktop layout. Add or update a Playwright regression. Save after evidence. Run make validate. Update docs/plans/active/settings-footer-overflow.md with decisions, commands, and artifact paths.
```

This prompt contains the harness shape: worktree, reproduction, browser evidence, scoped fix, regression test, validation command, and durable plan. If Codex fails, the failure is informative. Missing setup script? Add one. Cannot find docs? Improve `AGENTS.md`. Cannot prove the visual state? Improve browser evidence. Test command unclear? Fix `docs/VALIDATION.md`.

That is why the OpenAI experiment used the no-manual-code constraint as pressure. It forced every missing piece to become visible. You can get most of the benefit by adopting a softer rule: when a task fails, improve the harness before trying the same prompt again.
