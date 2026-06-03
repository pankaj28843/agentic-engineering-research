# Briefing

## Verdict

OpenAI harness engineering is best understood as an agent operating environment, not a prompting style. The primary OpenAI blog says the team built an internal beta with Codex writing application logic, tests, CI, documentation, observability, and tooling, while humans steered through prompts and feedback loops. The supporting evidence makes the mechanism clear: Codex became more capable because the repo, app, tools, and review process were reshaped so the agent could see, act, validate, and recover.

For practitioners, the replicable lesson is not "ban humans from coding." It is: make the important parts of your engineering system legible to the agent, then enforce the non-negotiable parts mechanically. Per-worktree app instances, browser/CDP validation, local logs/metrics/traces, short `AGENTS.md` files, versioned plans, custom lints, and cleanup loops are the pieces that translate human judgment into repeatable agent context.

## Confidence

High confidence:

- OpenAI's public article explicitly describes per-worktree app boot, CDP wiring, local observability, repository knowledge as system of record, architecture invariants, custom lints, agent review loops, and garbage-collection work.
- OpenAI's Codex docs explicitly describe worktrees, local environments, integrated terminal, in-app browser, browser use, computer use, skills, AGENTS.md discovery, approvals, sandboxing, and code review.
- Symphony's public source explicitly implements a Linear-to-workspace-to-Codex app-server runner with workflow configuration, retries, blocked state, workspace cleanup, logging, token accounting, and optional dashboard/API.

Medium confidence:

- The videos are consistent with the blog and add practitioner texture around human review, observability, agent-to-agent feedback, and harness-first thinking. They are transcripts, not formal specifications.
- X/Twitter posts show current public discussion from Ryan Lopopolo, but they are social signal and can change or disappear.

Low confidence:

- YouTube comments are weak signal only.
- Exact product rate limits may change quickly. The packet dates the official pages and avoids making permanent pricing promises.

## What Changed After Evidence Review

The initial instinct could be to frame harness engineering as a local toolchain for coding agents. The evidence pushed the frame wider. The OpenAI blog emphasizes repo knowledge, architecture, taste, review, merge philosophy, autonomy, and cleanup just as much as browser control. Symphony pushed the frame wider again: once an environment is harnessed, the next step is not "run Codex once," but "schedule work, isolate workspaces, track state, retry, surface blocked runs, and clean up."

The video set also changed the emphasis. Transcripts repeatedly point to human attention as the scarce resource. The useful goal is not maximum autonomy everywhere. It is moving humans to the layer where they provide acceptance criteria, product judgment, and control-system design, while agents execute bounded loops.

## Failure Modes

- Thin repo knowledge: a giant instruction file crowds out task context and rots. The OpenAI pattern is short entry points plus indexed docs.
- Invisible runtime state: if the agent cannot inspect the app, logs, metrics, traces, tests, and review state, it guesses.
- Soft architecture: documentation alone does not keep high-throughput agent output coherent. Invariants need lints, tests, and CI.
- Review deadlock: reviewer agents and author agents need permission to push back; otherwise they can create busywork loops.
- Autonomy without boundaries: browser, computer use, network access, secrets, and destructive actions need explicit stop points.
- Cleanup lag: agent-generated patterns compound quickly. Background doc-gardening and refactoring loops become part of the harness.

## Practitioner Implications

A serious Linux/macOS practitioner can replicate the useful parts without copying OpenAI's private stack:

- Use git worktrees or dedicated clones for each agent task.
- Start one app instance per worktree, with deterministic ports and logs.
- Give the agent Playwright/CDP evidence, screenshots, DOM snapshots, and browser traces.
- Expose logs, metrics, and traces through local scripts or query endpoints.
- Keep `AGENTS.md` short and link to `docs/`, `plans/`, runbooks, architecture rules, and validation commands.
- Encode architectural rules as tests or lints with remediation-rich error messages.
- Use agent review loops, but route comments, pushback, and final acceptance through a clear policy.
- Schedule cleanup work as recurring agent tasks, not as occasional human heroics.

## Remaining Unknowns

- OpenAI explicitly says it does not yet know how architectural coherence evolves over years in a fully agent-generated system.
- The exact private OpenAI harness is not public.
- Symphony is a public engineering preview and should be hardened before use in untrusted environments.
- The best balance between human review, agent review, automated merge, and post-merge cleanup is codebase-specific.
- Product subscriptions, included models, and limits change frequently; official pages need rechecking before spend decisions.

