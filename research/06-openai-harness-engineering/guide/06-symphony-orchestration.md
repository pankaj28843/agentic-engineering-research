# 06 - Symphony Orchestration

OpenAI's public [Symphony](https://github.com/openai/symphony) repository is not the same thing as the private harness in the blog. It is still highly relevant because it shows what the next layer above a harnessed repo can look like: a long-running service that reads work, creates isolated workspaces, runs Codex, tracks status, retries, exposes observability, and cleans up.

The README says Symphony turns project work into isolated, autonomous implementation runs and works best in codebases that have adopted [harness engineering](https://openai.com/index/harness-engineering/). It is labeled a low-key engineering preview for trusted environments. That warning matters. Symphony is evidence of a pattern, not a drop-in production control plane.

## ELI5

If Codex is a worker and a harnessed repo is a well-labeled workshop, Symphony is the dispatcher at the front desk. It reads the list of jobs, gives one job to one worker, creates a separate bench for that worker, watches progress, retries if something breaks, and cleans the bench when the job is done.

Without a dispatcher, a human has to start every agent run by hand. With a dispatcher, humans manage the work queue.

## The Specification

The [Symphony SPEC.md](https://github.com/openai/symphony/blob/main/SPEC.md) defines a long-running automation service. It continuously reads work from an issue tracker, Linear in the current spec version, creates an isolated workspace for each issue, and runs a coding agent session in that workspace.

The spec says the service solves four operational problems:

- It turns issue execution into a repeatable daemon workflow instead of manual scripts.
- It isolates execution in per-issue workspaces.
- It keeps workflow policy in-repo through `WORKFLOW.md`.
- It provides enough observability to debug multiple concurrent agent runs.

The spec's components are a good architecture map for practitioners:

- Workflow loader.
- Config layer.
- Issue tracker client.
- Orchestrator.
- Workspace manager.
- Agent runner.
- Optional status surface.
- Logging.

This is not accidental. A one-off shell script can run Codex. A durable agent operations service needs these layers because work can be concurrent, stateful, retrying, blocked, stale, or terminal.

## The Elixir Implementation

The inspected `elixir/README.md` says the implementation polls Linear, creates a workspace per issue, launches Codex in [App Server mode](https://developers.openai.com/codex/app-server/), sends a workflow prompt, and keeps Codex working until the issue is done. It can serve a client-side `linear_graphql` tool so repo skills can make raw Linear GraphQL calls. If an issue moves to a terminal state, Symphony stops the active agent and cleans up matching workspaces.

The `elixir/WORKFLOW.md` file is especially valuable because it shows a repo-owned contract. It configures:

- Linear tracker kind, project slug, active states, and terminal states.
- Poll interval.
- Workspace root.
- `after_create` and `before_remove` hooks.
- Maximum concurrent agents and maximum turns.
- Codex command.
- Approval policy.
- Thread sandbox.
- Turn sandbox policy and network access.
- The Markdown prompt body for the agent.

This is harness engineering at the queue level. The workflow file is not just a config file; it is a contract that the runner and agent both use.

## Workspaces And Hooks

The inspected `workspace.ex` creates isolated per-issue workspaces. It sanitizes identifiers, maps them to workspace paths, creates directories, runs `after_create`, supports remote workers, and has removal paths that can run `before_remove`. It also validates paths to reduce unsafe deletion or symlink escape risks.

The replication lesson is direct: do not let a scheduler hand agents a shared checkout. Make a workspace manager responsible for:

- Stable workspace naming.
- Path safety.
- Creation.
- Bootstrap.
- Before-run hooks.
- After-run hooks.
- Before-remove hooks.
- Cleanup for terminal work.

For a smaller local version:

```bash
#!/usr/bin/env bash
set -euo pipefail

issue="${1:?issue id}"
safe="$(printf '%s' "$issue" | tr -cs 'A-Za-z0-9._-' '_')"
root="${SYMPHONY_WORKSPACE_ROOT:-$HOME/code/agent-workspaces}"
workspace="$root/$safe"

mkdir -p "$workspace"
cd "$workspace"
if [ ! -d .git ]; then
  git clone "$SOURCE_REPO_URL" .
fi
```

Add hooks as explicit scripts:

```text
hooks/
  after_create
  before_run
  after_run
  before_remove
```

This keeps lifecycle behavior visible to agents and humans.

## Agent Runner And Turns

The inspected `agent_runner.ex` starts a Codex app-server session in the workspace, builds a prompt from the issue and workflow template, runs a turn, then checks whether the issue remains in an active state. If it does and the max-turn limit has not been hit, it sends continuation guidance and runs another turn.

That is a Ralph-style loop embedded in a scheduler. The important design details are:

- Maximum turns are explicit.
- The issue state is refreshed between turns.
- Continuation prompts tell the agent to resume from current workspace state.
- The app-server session is stopped in an `after` block.
- Failures are surfaced to the orchestrator, which owns retry policy.

Practitioners can copy the policy without copying Elixir. A Python or Go runner can do the same: start session, send task, stream updates, refresh issue state, continue until done or max turns, then stop session.

## Orchestrator State

The inspected orchestrator search shows runtime state for running, claimed, blocked, retry attempts, poll intervals, and max concurrency. It reconciles running and blocked issues with tracker state, stops runs when issues become terminal or non-active, schedules retries, handles stalls, and records blocked runs when input or approval is required.

This is the part one-off scripts usually miss. Long-running agent work needs state reconciliation because the external world changes:

- A human may move a ticket to Done.
- A reviewer may request rework.
- A run may stall.
- A worker may crash.
- A required approval may block.
- A retry may be due.
- A workspace may need cleanup.

The orchestrator must be conservative. It should not keep working on terminal tickets. It should not delete unsafe paths. It should not silently spin forever when approval is needed.

## Observability

Symphony's logging docs say logs should be searchable by issue and session, include both Linear internal ID and human-readable issue key, include Codex session ID, and use stable key-value fields. The token accounting docs distinguish cumulative totals from latest increments in Codex app-server token usage.

Those details are mundane and important. If you run ten agents and one melts down, you need to answer:

- Which issue?
- Which workspace?
- Which worker host?
- Which Codex session?
- Which turn?
- Which token usage?
- Which last event?
- Which retry attempt?
- Which logs and artifacts?

Add this to your local runner logs:

```text
event=agent_started issue_id=... issue_identifier=... workspace=... session_id=...
event=turn_completed issue_id=... turn=3 total_tokens=...
event=agent_blocked issue_id=... reason=approval_required
event=workspace_removed issue_identifier=...
```

Do not rely on free-form prose for operational debugging.

## Trust Boundary

Symphony's README warns it is for trusted environments. The spec says implementations must document their trust and safety posture and does not mandate one approval or sandbox policy. The Elixir workflow example uses `approval_policy: never` and network access in its turn sandbox. That may be acceptable for a controlled internal preview. It is not a universal recommendation.

Tie autonomy to environment:

- Personal scratch repo: high autonomy may be fine.
- Company codebase: workspace-write, scoped network, secrets discipline, review gates.
- Production data: strong sandboxing, no destructive actions without human confirmation.
- Regulated domain: explicit audit trail, human approval, and compliance review.

OpenAI's official [agent approvals and security](https://developers.openai.com/codex/agent-approvals-security/) docs describe sandbox modes, approval policies, default no-network posture, and network-proxy controls. Use those controls as part of the runner contract, not as an afterthought.

## Building A Smaller Symphony

For Linux/macOS, a minimal scheduler can start with a local issue file:

```yaml
issues:
  - id: local-001
    title: Fix settings overflow
    state: Todo
```

Then implement:

1. Poll `issues.yaml`.
2. Pick `Todo` issues.
3. Create a git worktree.
4. Run setup hook.
5. Launch Codex with a prompt template.
6. Write logs to `.agent-runs/local-001/`.
7. Mark blocked/done in a local status file.
8. Clean worktree when terminal.

Only after that works should you connect Linear, GitHub, Slack, or remote workers.

## What Symphony Teaches

Symphony's big lesson is that once a repository is harnessed, the bottleneck moves from "can an agent do this task?" to "how do we manage many tasks safely?" That is why the service has workflow loading, config, issue tracking, workspaces, runner, orchestration, observability, and cleanup. It is the operational layer of harness engineering.

The inference, clearly labeled, is that OpenAI's internal harness likely needed similar operational concerns even if the private implementation differs: task queues, workspace isolation, status tracking, retries, review loops, logs, and cleanup. Symphony makes those concerns public and inspectable.

## From Manual Runs To Managed Work

Symphony also clarifies a maturity curve. The first stage of agentic engineering is manual: a human opens a terminal, prompts Codex, watches output, and decides what to do next. The second stage is scripted: a human still chooses the task, but scripts create worktrees, run setup, start the app, and collect evidence. The third stage is managed work: a service reads a queue, assigns work, tracks running state, notices terminal state, and exposes status.

The OpenAI blog mostly describes the second and third stages from the perspective of an internal product team. Symphony gives the public third-stage skeleton. It makes the issue tracker the input, `WORKFLOW.md` the repo-owned policy, workspaces the isolation layer, Codex app-server the execution layer, and logs/dashboard/API the observability layer.

For a practitioner, the key question is when to move stages. Do not jump from manual prompts to a daemon because daemons feel advanced. Move when manual coordination becomes the bottleneck and your lower-level harness is already reliable. If app boot is flaky, a scheduler will amplify flakiness. If validation is unclear, a scheduler will produce unclear handoffs faster. If review policy is noisy, a scheduler will generate review noise at scale.

## A Local Queue Before Linear

Before connecting Linear, build a file-backed queue:

```yaml
# .agent-queue/issues.yaml
issues:
  - id: local-001
    state: Todo
    title: Fix settings overflow on mobile
    priority: 1
    description: >
      Reproduce at /settings on 390x844, fix footer overflow, and attach
      before/after browser evidence.
```

Then make a runner update local status:

```yaml
runs:
  local-001:
    state: Running
    workspace: /home/me/code/myapp-agent-local-001
    started_at: 2026-06-03T00:00:00Z
    last_event: validation_started
```

This gives you most of the orchestration learning without API credentials. You can test workspace creation, prompt rendering, logging, retry, and cleanup. Once the local queue is boring, swap in Linear, GitHub Issues, Jira, or another tracker.

## Prompt Rendering Is Part Of The Contract

Symphony's workflow prompt includes issue identifier, title, state, labels, URL, and description. It also includes instructions about status routing, workpad comments, validation, PR feedback, blockers, and handoff. That is a crucial design point: the scheduler does not only start the agent; it shapes the agent's operating contract.

A local prompt template should include:

- Task identity.
- Current status.
- Workspace path.
- Artifact root.
- Acceptance criteria.
- Validation requirements.
- Review protocol.
- Blocker policy.
- Autonomy boundaries.
- Final response requirements.

If those are scattered across chat, the scheduler is just a launcher. If they are rendered into every run, the scheduler becomes a policy engine.

## Blocked State

Blocked state deserves special treatment. Symphony's Elixir README says if Codex reports that operator input, approval, or MCP elicitation is required, Symphony keeps the issue claimed and exposes it as blocked in runtime state, JSON API, and dashboard. That avoids two bad outcomes: repeatedly redispatching a task that cannot proceed, or silently losing the fact that a human decision is needed.

For a local runner, record:

```yaml
blocked:
  local-001:
    reason: missing STRIPE_API_KEY for integration test
    blocked_at: 2026-06-03T00:15:00Z
    workspace: /home/me/code/myapp-agent-local-001
    next_human_action: provide test-mode key or waive integration validation
```

Blocked state should be specific. "Need help" is not enough. A future agent or human should know what is missing, why it blocks validation, and the exact action needed.

## Cleanup Without Data Loss

Workspaces consume disk. Codex official worktree docs describe automatic cleanup rules for Codex-managed worktrees, including preserving important work and offering restore snapshots. Symphony has workspace removal hooks and terminal-state cleanup. Your local runner should be equally careful.

Before deleting a workspace:

1. Confirm the issue is terminal or explicitly archived.
2. Save final git status.
3. Save latest validation summary.
4. Save uncommitted diff if any.
5. Run `before_remove` hook.
6. Remove only paths under the configured workspace root.

This is another place where path safety matters. A cleanup script that interpolates an issue title into `rm -rf` is unacceptable. Sanitize identifiers, canonicalize paths, reject paths outside the workspace root, and log what was removed.

## Symphony's Practical Warning

The public repository's warning about trusted environments should stay visible. A scheduler can make an unsafe configuration much worse. If it polls a tracker and launches ten agents with network access, broad filesystem access, and no approval prompts, it has become an automated risk multiplier. That may be acceptable in a disposable sandbox. It is not acceptable around production secrets or customer data.

The safe adoption path is incremental: manual run, scripted worktree, evidence contract, review loop, cleanup loop, file-backed queue, then external tracker. Each step should have validation and a rollback path. This keeps the orchestrator from outrunning the harness it depends on.
