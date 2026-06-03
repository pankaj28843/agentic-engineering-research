# 08 - Replication Playbook

This chapter turns the evidence into a Linux/macOS implementation path. It does not try to recreate OpenAI's private harness. It gives you a serious local harness shape that preserves the useful principles from the [OpenAI blog](https://openai.com/index/harness-engineering/), public [Codex docs](https://developers.openai.com/codex/app/features/), [computer use docs](https://developers.openai.com/api/docs/guides/tools-computer-use), and [Symphony](https://github.com/openai/symphony).

The target reader already knows tmux, remote sessions, persistent goals, and long-running loops. The missing piece is the engineering substrate.

## ELI5

You are building a train track, not just buying a train. The agent is the train. The track is worktrees, docs, tests, browser evidence, logs, review policy, and cleanup. A powerful train without track crashes. A good track lets many trains move safely.

## Phase 1: Repository Skeleton

Create a short map and deeper docs:

```bash
mkdir -p docs/{decisions,generated,plans/active,plans/completed,runbooks}
mkdir -p scripts .agent-artifacts
touch AGENTS.md docs/ARCHITECTURE.md docs/VALIDATION.md docs/PRODUCT.md docs/SECURITY.md docs/QUALITY.md
```

Root `AGENTS.md`:

```md
# AGENTS.md

Use this as a map. Do not treat it as a complete manual.

- Architecture: `docs/ARCHITECTURE.md`
- Validation: `docs/VALIDATION.md`
- Product behavior: `docs/PRODUCT.md`
- Security and approvals: `docs/SECURITY.md`
- Quality and cleanup: `docs/QUALITY.md`
- Active plans: `docs/plans/active/`

Before handoff, run `make validate` and update the active plan.
```

Keep it short. OpenAI's article says a giant `AGENTS.md` failed because it consumed context, diluted guidance, rotted, and was hard to verify. Official [AGENTS.md docs](https://developers.openai.com/codex/guides/agents-md/) support layered instructions and discovery.

## Phase 2: Validation Contract

Create a single validation entrypoint:

```make
validate:
	./scripts/check-doc-links
	./scripts/check-architecture
	npm test
	npm run lint
```

Add `docs/VALIDATION.md`:

```md
# Validation

Required before handoff:

- `make validate`
- For UI changes: browser evidence in `.agent-artifacts/<task>/`
- For API changes: contract or integration test evidence
- For security-sensitive changes: security review artifact
```

Agents need one command that means "prove the work." Humans need one command to audit. If validation is scattered across memory, agents will miss it.

## Phase 3: Worktree-Per-Task Isolation

Create a worktree script:

```bash
#!/usr/bin/env bash
set -euo pipefail

task="${1:?task id}"
port="${2:?port}"
repo="$(git rev-parse --show-toplevel)"
base="$(basename "$repo")"
target="../$base-agent-$task"

git -C "$repo" worktree add "$target" -b "agent/$task"
cd "$target"
printf 'PORT=%s\nTASK_ID=%s\n' "$port" "$task" > .env.agent
mkdir -p ".agent-artifacts/$task"
```

Codex official [Worktrees](https://developers.openai.com/codex/app/worktrees/) docs describe the user-facing version of this: worktrees let independent tasks run without disturbing local work, and Codex-managed worktrees have cleanup rules. Your script should add deterministic task identity and port assignment.

On macOS and Linux, use a port allocator if you run many agents:

```bash
python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
```

Record the chosen port in the active plan.

## Phase 4: App Boot And Browser Evidence

Add a local action:

```bash
#!/usr/bin/env bash
set -euo pipefail
source .env.agent
mkdir -p ".agent-artifacts/$TASK_ID/logs"
npm run dev 2>&1 | tee ".agent-artifacts/$TASK_ID/logs/dev-server.log"
```

Add a Playwright smoke test:

```ts
import { test, expect } from "@playwright/test";

test("home page is usable", async ({ page }) => {
  const url = process.env.APP_URL ?? "http://127.0.0.1:4301";
  await page.goto(url);
  await expect(page.locator("body")).toBeVisible();
  await page.screenshot({ path: `.agent-artifacts/${process.env.TASK_ID}/home.png`, fullPage: true });
});
```

Teach agents:

```md
For UI work, reproduce first with Playwright or browser use, save before/after screenshots, and cite artifact paths in the handoff.
```

If you are using the Codex app, the official [in-app browser](https://developers.openai.com/codex/app/browser/) docs describe browser comments and browser use for local dev servers and file-backed previews. If you are building your own API-level harness, OpenAI's [computer use guide](https://developers.openai.com/api/docs/guides/tools-computer-use) recommends isolated browser or VM environments and explicit confirmation policy.

## Phase 5: Local Observability

Start simple:

```text
.agent-artifacts/<task>/
  logs/
    dev-server.log
    test.log
  screenshots/
  traces/
  validation.md
```

Then add structured logs:

```ts
logger.info("service_started", {
  task_id: process.env.TASK_ID,
  port: process.env.PORT,
  git_sha: process.env.GIT_SHA
});
```

Add a query command:

```bash
#!/usr/bin/env bash
set -euo pipefail
task="${1:?task id}"
pattern="${2:?pattern}"
rg -n "$pattern" ".agent-artifacts/$task/logs"
```

Mature later:

- Local Prometheus for metrics.
- Loki or plain JSON logs for log queries.
- OpenTelemetry collector for traces.
- A task-scoped dashboard.
- Saved query examples in `docs/runbooks/observability.md`.

The OpenAI post uses LogQL and PromQL. You can start with `rg`. The invariant is queryability.

## Phase 6: Architecture Checks

Create `architecture.yaml`:

```yaml
domains_root: src/domains
layers:
  - types
  - config
  - repo
  - service
  - runtime
  - ui
providers_root: src/providers
```

Create `scripts/check-architecture` to enforce allowed imports. Add messages that teach repair:

```text
Architecture violation: ui imports repo directly.
Expected path: ui -> service -> repo.
Read docs/ARCHITECTURE.md#domain-layers and move the call into a service.
```

This follows the OpenAI article's custom lint pattern. The error message is part of the prompt stream.

## Phase 7: Review Loop

Create `docs/REVIEW.md` and require:

- Local self-review.
- Agent review for correctness.
- Agent review for security or architecture when relevant.
- Explicit pushback for weak comments.
- Validation rerun after changes.

Codex's official [GitHub review docs](https://developers.openai.com/codex/github/code-review/) show a public review surface. Locally, use read-only reviewers and durable review files.

Example:

```bash
mkdir -p ".agent-artifacts/$TASK_ID/review"
git diff --stat > ".agent-artifacts/$TASK_ID/review/diffstat.txt"
make validate | tee ".agent-artifacts/$TASK_ID/review/validation.log"
```

Then ask a reviewer agent to write findings to `.agent-artifacts/$TASK_ID/review/findings.md`.

## Phase 8: Ralph-Style Loop With Stop Rules

Write a loop policy before writing a loop script:

```yaml
max_iterations: 5
max_wall_clock_minutes: 180
stop_if_same_failure_repeats: 2
required_artifacts:
  - validation log
  - review summary
  - active plan update
blockers:
  - missing secrets
  - missing credentials
  - external service unavailable
  - approval required for high-impact action
```

Then implement the loop. Do not let agents run indefinitely without a recovery artifact. This packet's PRP plan is a model: after meaningful work, update the durable plan with current phase, artifacts, evidence limitations, validation state, and exact next action.

## Phase 9: Cleanup And Garbage Collection

OpenAI's blog says the team moved from manual Friday cleanup to golden principles and recurring background Codex tasks. Your version can start with:

```text
docs/QUALITY.md
docs/plans/active/cleanup-YYYY-MM-DD.md
scripts/find-large-files
scripts/find-duplicate-helpers
scripts/check-stale-docs
```

Recurring cleanup prompt:

```text
Scan the repository for violations of docs/QUALITY.md. Open a focused plan for the top three issues. Do not refactor broadly. Each proposed cleanup must include validation and rollback notes.
```

This prevents cleanup from becoming "rewrite everything." Garbage collection works because it is small and regular.

## Phase 10: Safety Boundaries

Write `docs/SECURITY.md`:

```md
# Security Boundaries

Agents may:

- Read and edit workspace files.
- Run validation commands.
- Use local browser evidence for unauthenticated dev routes.

Agents must stop or ask for approval before:

- Using secrets not already scoped to the task.
- Sending emails, payments, or external messages.
- Deleting production or cloud data.
- Changing permissions or credentials.
- Installing unreviewed network software.
- Bypassing browser or OS safety prompts.
```

OpenAI's [agent approvals and security](https://developers.openai.com/codex/agent-approvals-security/) docs say sandboxing and approval policy work together, with network off by default in local workspace-write mode unless enabled. Use that as a default posture. Enable network only when the task needs it and the environment is trusted.

## Phase 11: Remote And tmux Operations

For tmux/remote sessions, standardize names:

```bash
tmux new-session -d -s "agent-$TASK_ID" -c "$WORKTREE"
tmux send-keys -t "agent-$TASK_ID" "source .env.agent && scripts/run-dev" C-m
```

Record:

```text
host:
worktree:
tmux session:
port:
git sha:
active plan:
artifact root:
```

If the session dies, a new agent reads the plan and resumes from artifacts. That is exactly why the user asked this packet's PRP to act as a recovery contract.

## Minimum Viable Harness

If you do nothing else, implement this:

1. Short `AGENTS.md`.
2. `docs/ARCHITECTURE.md` and `docs/VALIDATION.md`.
3. `make validate`.
4. Worktree-per-task script.
5. App boot script with deterministic port.
6. Playwright screenshot test.
7. Structured logs under `.agent-artifacts/`.
8. Review policy.
9. Active plan file.
10. Cleanup checklist.

That is enough to make agent work more inspectable. Each failure then tells you what to add next.

## The Implementation Philosophy

Do not start by building a giant orchestrator. Start by making one task fully legible. Then make two tasks isolated. Then make review durable. Then make cleanup recurring. Then add a scheduler. This sequence mirrors the OpenAI story: missing capabilities are discovered by forcing Codex to do real work, then encoded into the harness.

## A Concrete Local Layout

For a serious personal or small-team repo, this layout is enough to start:

```text
.
  AGENTS.md
  Makefile
  architecture.yaml
  docs/
    ARCHITECTURE.md
    PRODUCT.md
    QUALITY.md
    REVIEW.md
    SECURITY.md
    VALIDATION.md
    generated/
    plans/
      active/
      completed/
    runbooks/
      browser-validation.md
      observability.md
  scripts/
    agent-new-worktree
    agent-run-dev
    check-architecture
    check-doc-links
    collect-browser-evidence
    metric-query
    prepare-review
  .agent-artifacts/
```

Add `.agent-artifacts/` to `.gitignore`, but keep the scripts and docs in git. The artifacts are bulky and task-specific; the harness is durable.

## Linux Notes

On Linux, browser automation is usually straightforward:

```bash
npx playwright install --with-deps chromium
```

If you need a desktop-like environment, use a container or VM. For browser-only work, Playwright's isolated browser contexts are often enough. For OS-level UI, use Xvfb or a dedicated VM. Avoid running agents against your main desktop session unless the task is low risk and you can monitor it.

For local networking, bind dev servers to `127.0.0.1`, not `0.0.0.0`, unless the agent needs remote access. If remote agents need access, prefer SSH port forwarding. This keeps the local app from being exposed broadly.

## macOS Notes

On macOS, Playwright web validation is also straightforward, but desktop automation has permission implications. If you use computer-control tools, macOS may require Accessibility and Screen Recording permissions. Treat that as a security boundary. Use a secondary user account, VM, or dedicated machine for high-autonomy desktop work.

For per-task dev servers, avoid sharing one app process across worktrees. Use deterministic ports and make the active port visible with `lsof -iTCP -sTCP:LISTEN -n -P`.

For Multipass-style Ubuntu VMs, the Ryan/X extraction showed current interest in Multipass as an agent orchestrator substrate, but that is social signal only. The practical pattern is still sound: isolate risky agent work in a disposable VM, mount or clone only the needed repo, and keep secrets out unless required.

## Remote Worker Pattern

Symphony's Elixir README mentions local and SSH worker scenarios in its live tests. A small version:

```bash
ssh worker-01 'mkdir -p ~/agent-workspaces'
ssh worker-01 'git clone --depth 1 git@github.com:org/repo ~/agent-workspaces/task-123'
ssh worker-01 'cd ~/agent-workspaces/task-123 && make validate'
```

Record worker host and workspace in the plan. If the worker has different OS packages, document that in `docs/VALIDATION.md`.

## Anti-Footguns

Do not let an early harness run agents with unrestricted filesystem access across your home directory, reuse your personal browser profile for autonomous tasks, share one `.env` full of secrets across all worktrees, give every agent network access because one task needed it, let review agents edit the same branch without coordination, run infinite loops without caps, delete worktrees without saving final status, or trust generated docs without freshness checks.

Each footgun has a safer default: workspace-write sandbox, isolated browser profile, per-task secret scoping, network off unless needed, read-only reviewer agents, explicit loop stop rules, cleanup hooks with snapshots, and generated-doc validation.

## When To Add A Scheduler

Add a Symphony-like scheduler only after you have reliable worktree creation, app boot, validation, durable plan files, review policy, cleanup policy, logs for agent runs, and clear blocked-state handling.

If you add a scheduler before those exist, you automate confusion. The scheduler will produce more unfinished work, not more throughput. OpenAI's public Symphony README says it works best in codebases that have adopted harness engineering. Treat that as an ordering constraint.
