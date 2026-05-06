# Chapter 11 — Build your first harness

**You'll learn:** a practical, incremental recipe for turning a normal repository into a more harnessable coding-agent workspace without trying to copy OpenAI or Stripe wholesale.

Source jumps: OpenAI's [AGENTS.md table-of-contents pattern](https://openai.com/index/harness-engineering/), GitHub's [AGENTS.md lessons](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/), OpenAI's [Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md), Böckeler's [harness starting point](https://martinfowler.com/articles/harness-engineering.html#AStartingPoint-AndOpenQuestions), and HumanLayer's [12 Factor Agents](https://github.com/humanlayer/12-factor-agents).

## Do not start with a grand platform

OpenAI and Stripe are inspiring, but copying them literally is a mistake for most teams. You probably do not need hundreds of MCP tools, pre-warmed devboxes, local Prometheus per worktree, or a million-line no-manual-code experiment on day one. You need a small harness that solves your next repeated failure.

Harness engineering is incremental. Start where agents already waste your time:

- They forget how to run tests.
- They use the wrong package manager.
- They miss architecture boundaries.
- They stop after writing code without verification.
- They invent APIs instead of reading docs.
- They make huge changes that are hard to review.
- They ask for permission too often or not at all.
- They keep repeating a review comment.

Each repeated failure is a candidate harness improvement.

## Step 1: make the repo runnable

A coding agent cannot reliably improve a repo it cannot run. Before fancy context engineering, create a boring validation path:

```bash
make setup      # or documented install command
make test       # fast enough for local use
make lint       # style/static checks
make validate   # repo-specific all-in-one gate
```

If the project uses `uv`, `npm`, `pnpm`, `go`, `cargo`, or another tool, state it explicitly. If a virtual environment must be activated, write the exact command. If tests require services, provide a script that starts them. If some checks are slow, separate fast and slow gates.

For this repo, the validation command is:

```bash
uv run python scripts/validate_research.py
```

That command is now part of the harness. It checks structure, source metadata, local links, and guide depth expectations.

## Step 2: write a short `AGENTS.md`

The always-loaded file should be a map and safety contract. It should not be a book. A good starting shape:

```markdown
# Agent Instructions

## Commands
- Setup: ...
- Test: ...
- Validate before handoff: ...

## Repository map
- src/ — application code
- docs/ — durable docs
- tmp/ — scratch, do not commit

## Rules
- Never edit production secrets.
- Ask before running destructive commands.
- Keep changes small and validated.

## Where to read more
- docs/architecture.md
- docs/testing.md
- docs/security.md
```

OpenAI's pattern is “map, not encyclopedia.” GitHub's AGENTS.md guidance similarly emphasizes clear setup, validation commands, project conventions, and concise instructions. The file should be short enough that the agent actually attends to it.

## Step 3: move detail into linked docs

Create deeper docs for stable knowledge:

- `docs/architecture.md` — layers, boundaries, allowed dependencies.
- `docs/testing.md` — test commands, fixture style, browser checks.
- `docs/security.md` — secrets, data, approvals, sandbox assumptions.
- `docs/reliability.md` — logs, metrics, SLOs, incident patterns.
- `docs/product.md` — product principles and acceptance criteria.
- `docs/generated/` — schema or API references generated from source.
- `docs/plans/` — active and completed execution plans.

Docs should be source-linked where possible. If a rule came from an incident, link the incident or summarize it. If a command is required, include it exactly. If a doc is generated, say how to regenerate it.

This research repo now treats each theme guide as a durable learning doc and article snapshots in `tmp/` as the source-processing substrate. That is the same architecture: small entry points, deeper source-backed material.

## Step 4: add cheap computational sensors

Start with checks that are deterministic and cheap:

- Formatter.
- Linter.
- Typechecker.
- Unit tests.
- Local link checker.
- JSON schema validation.
- Secret scanner.
- Import boundary checker.
- File size or generated-file checks.

Make the error messages agent-readable. If a check fails, the output should tell the agent what to run or where to look. If the tool's default output is cryptic, wrap it with a script that prints clearer instructions.

For this repo, `validate_research.py` is the cheap sensor. It can be expanded as the repo's expectations become clearer. That is better than relying on a prompt saying “please write a good guide.”

## Step 5: define done

Agents are prone to declaring victory early. Define done explicitly:

- Code compiles.
- Tests pass.
- Lint passes.
- Docs updated.
- Screenshots captured for UI changes.
- Source links included for research claims.
- No broken local links.
- Open questions recorded.
- Human approval obtained for high-risk actions.

For research themes, “done” should now include:

- Clean article snapshots generated in `tmp/` from captured HTML.
- A chapter-wise ELI5 deep-dive guide under `guide/`.
- Inline links to external sources.
- Images copied locally when used, with credits.
- A briefing for executive summary, not as the main artifact.
- Source index and `sources.json`.
- Validation green.
- Optional EPUB build works.

This is a harness update to prevent shallow outputs.

## Step 6: add behaviour evidence

For app code, behaviour evidence might be browser tests, screenshots, videos, logs, or approved fixtures. For libraries, it might be golden files, property tests, or example-driven docs. For research, it is source-linked chapter prose plus extracted article snapshots.

Ask: what would convince a skeptical human reader without making them re-run the whole task? That evidence should be included in the PR or theme folder.

Approved fixtures are a useful model. They make expected output reviewable by humans. In a research repo, source-linked quotes and local article snapshots play a similar role: they let a reader jump from synthesis to original source.

## Step 7: classify risk and permissions

Write down what agents may do without asking:

- Read files? Usually yes.
- Write inside repo? Usually yes, with validation.
- Delete files? Maybe only inside generated outputs.
- Run tests? Yes.
- Install dependencies? Maybe.
- Start daemons? Often no without human approval.
- Access production data? No.
- Use browser remote debugging? Depends; this repo requires human approval for daemon lifecycle changes.
- Push commits? Depends on workflow.

Make the boundary explicit. Ambiguity causes either unsafe autonomy or constant permission prompts.

## Step 8: keep a failure ledger

A failure ledger is a lightweight table:

| Date | Failure | Cost | Harness change |
|---|---|---|---|
| 2026-05-06 | Theme output too shallow after deep crawl | wasted tokens, poor learning | require ELI5 guide chapters and article extraction |
| ... | Agent missed browser screenshot | review delay | add visual evidence checklist |
| ... | Agent edited generated file | broken regen | add validation check |

This turns frustration into compounding improvement. It also prevents arbitrary rules: every rule should trace to a failure, risk, or explicit design choice.

## Step 9: publish for humans

If the output is meant for human learning, make it readable outside the IDE. For this repo, that means private book formats:

```bash
uv run python scripts/build_theme_book.py \
  research/01-harness-engineering \
  --formats markdown,epub
```

EPUB is an implementation detail, not the soul of the project. The soul is high-quality, source-backed, plain-language deep dives. But publishing matters because it forces chapter order, local links, image paths, and reading flow to be real.

## A starter harness template

For a small repo, create:

```text
AGENTS.md
Makefile
scripts/validate.py
docs/
  architecture.md
  testing.md
  security.md
  research-method.md   # if research repo
.tmp or tmp/           # gitignored scratch
```

Then add:

- One short `AGENTS.md`.
- One validation command.
- One architecture rule as code.
- One behaviour evidence pattern.
- One failure ledger.
- One publishing or handoff command if humans consume artifacts.

Do not build more until failure evidence demands it.

## Chapter takeaways

- Start with runnable commands, short instructions, linked docs, and cheap validation.
- Promote repeated failures into harness changes.
- Define “done” in evidence terms.
- Classify permissions and approval boundaries.
- For this repo, the harness now requires deep, source-linked, ELI5 guide material rather than shallow briefings.

**Next:** [Chapter 12 — Reading the source set](12-reading-the-source-set.md).
