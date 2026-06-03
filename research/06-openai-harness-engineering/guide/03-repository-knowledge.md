# 03 - Repository Knowledge

OpenAI's [blog](https://openai.com/index/harness-engineering/) says the team made repository knowledge the system of record. That phrase is central. In a normal organization, important knowledge lives in many places: Slack, docs, tickets, dashboards, review comments, meeting memories, architecture sketches, and people's heads. A human engineer can ask around. Codex cannot. From the agent's point of view, knowledge that is not available in context, files, tools, or retrievable sources effectively does not exist.

The post says the team tried one large `AGENTS.md` and found predictable failures: context pressure, guidance dilution, rot, and weak verifiability. The alternative was a short `AGENTS.md` acting as a table of contents, with a structured `docs/` directory holding deeper sources of truth. The article's diagram of repository knowledge is copied here:

![Repository knowledge limits](../assets/openai/limits-of-agent-knowledge.webp)

The visual lesson is simple: the agent sees repository-local, versioned artifacts better than invisible human context. If you want the agent to use a decision, put the decision in the repo. If you want the agent to follow a rule, make the rule discoverable and, where possible, enforce it.

## ELI5

Imagine a substitute teacher walking into a classroom. If the class rules are only in the old teacher's memory, the substitute guesses. If there is a short note on the desk saying "read the blue folder for today's plan, the red folder for safety rules, and the attendance sheet for names," the substitute can run the class. `AGENTS.md` is the note on the desk. `docs/` is the folder system.

The mistake is making the note on the desk into a giant textbook. The substitute will not read it carefully, and nobody will keep it fresh. A short map works better.

## Official AGENTS.md Behavior

OpenAI's [AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md/) says Codex reads instruction files before doing work, layers global and project guidance, walks from the project root toward the current directory, and includes at most one instruction file per directory. It also notes a default combined-size limit and recommends splitting instructions across nested directories or raising the limit when needed.

That official behavior supports a practical structure:

```text
AGENTS.md
docs/
  README.md
  ARCHITECTURE.md
  VALIDATION.md
  PRODUCT.md
  SECURITY.md
  QUALITY.md
  decisions/
  plans/
    active/
    completed/
services/
  billing/
    AGENTS.md
  frontend/
    AGENTS.md
```

The root `AGENTS.md` should be short. It should tell Codex what kind of repo this is, which commands prove work, which docs to read first, and which boundaries are non-negotiable. Specialized subdirectories can add local rules.

## Progressive Disclosure

OpenAI's [Agent Skills](https://developers.openai.com/codex/skills/) docs describe progressive disclosure for skills: Codex initially sees a skill's name, description, and path, then reads the full `SKILL.md` only when needed. The same principle applies to repository knowledge. The agent should start with a small index and expand only into relevant docs.

A strong root map might look like this:

```md
# AGENTS.md

## Repository Map

- `docs/ARCHITECTURE.md`: domain layers and dependency rules.
- `docs/VALIDATION.md`: commands required before handoff.
- `docs/PRODUCT.md`: product principles and user-facing acceptance criteria.
- `docs/SECURITY.md`: data, secrets, network, and approval boundaries.
- `docs/QUALITY.md`: quality scores and known cleanup work.

## Required Commands

- `make validate`
- `make test`

## Working Rule

If a task changes behavior, update the relevant doc or explain why no doc changed.
```

This is intentionally not encyclopedic. It is a router. The deeper docs can be longer because Codex reads them only when task-relevant.

## Plans As First-Class Artifacts

OpenAI's article says plans are first-class artifacts, with lightweight plans for small changes and execution plans for complex work. This packet's own PRP plan follows that pattern: it records current phase, artifacts, limitations, validation state, and next actions so a resumed agent does not rely on chat memory.

For your own harness, make plans durable:

```text
docs/plans/
  active/
    2026-06-03-fix-settings-overflow.md
  completed/
    2026-05-28-add-login-rate-limit.md
  tech-debt-tracker.md
```

Each active plan should include:

- Goal.
- Acceptance criteria.
- Source links or issue links.
- Current status.
- Checklist.
- Decisions.
- Validation commands.
- Evidence artifacts.
- Recovery notes.

The recovery note is not bureaucracy. It is how you get long-running agent loops to survive context compaction, process restarts, and handoffs. If a fact matters, write it to the plan or the repo.

## Generated Knowledge

The OpenAI post mentions generated docs such as database schema docs. Generated knowledge is powerful because it turns opaque runtime state into files the agent can inspect. Examples:

- `docs/generated/db-schema.md`
- `docs/generated/routes.md`
- `docs/generated/openapi.md`
- `docs/generated/design-tokens.md`
- `docs/generated/dependency-graph.md`

The rule is: generated docs must be fresh or clearly marked stale. A stale generated schema is worse than none because the agent will trust it. Add validation:

```bash
#!/usr/bin/env bash
set -euo pipefail

npm run generate:docs
git diff --exit-code docs/generated
```

If the diff is non-empty, CI fails and tells the agent what to regenerate. This is an example of a lint message as prompt injection in the good sense: the error message becomes remediation context.

## Knowledge Freshness And Ownership

OpenAI says they use dedicated linters and CI jobs to validate that the knowledge base is up to date, cross-linked, and structured correctly. They also use a recurring doc-gardening agent to scan for stale or obsolete docs and open fix-up PRs.

A local version can start with simple checks:

```bash
#!/usr/bin/env bash
set -euo pipefail

rg -n "TODO|TBD|stale|deprecated" docs
python scripts/check-doc-links.py
python scripts/check-doc-owners.py
```

The owner check can be crude:

```yaml
docs:
  ARCHITECTURE.md:
    owner: platform
    freshness_days: 30
  SECURITY.md:
    owner: security
    freshness_days: 30
```

The point is not to create paperwork. The point is to make docs maintainable by agents. If a doc has an owner, a freshness period, and validation, an agent can open a useful cleanup PR.

## Off-Repo Knowledge

The hardest part is deciding what to move into the repo. Not every Slack thread belongs in `docs/`. But if a Slack decision changes architecture, product behavior, validation, or safety, it should become a durable artifact.

Use this rule:

- A conversation can stay off-repo if it is transient.
- A decision should enter the repo if future agents must obey it.
- A repeated review comment should become a doc or lint.
- A repeated bug class should become a test, runbook, or generated check.
- A tribal product principle should become `docs/PRODUCT.md`.

This is the same standard you would apply for onboarding humans, but agents make the cost of hidden knowledge visible faster.

## Replication Steps

On Linux/macOS:

```bash
mkdir -p docs/{decisions,generated,plans/active,plans/completed}
touch docs/ARCHITECTURE.md docs/VALIDATION.md docs/PRODUCT.md docs/SECURITY.md docs/QUALITY.md
```

Add a short root map:

```md
# AGENTS.md

Read this file first. Use it as a map, not a complete manual.

- Architecture: `docs/ARCHITECTURE.md`
- Validation: `docs/VALIDATION.md`
- Product: `docs/PRODUCT.md`
- Security: `docs/SECURITY.md`
- Quality and cleanup: `docs/QUALITY.md`

Run `make validate` before handoff.
```

Add a validation target:

```make
validate:
	./scripts/check-doc-links
	./scripts/check-generated-docs
	./scripts/check-architecture
	npm test
```

Then run Codex from the repo root and ask it to list the instruction sources it loaded. The [official AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md/) recommends this kind of verification. If the wrong files load, fix the pathing before you trust longer tasks.

## The Deeper Principle

Repository knowledge is not just documentation. It is the memory substrate for the agent system. Every durable decision has to live somewhere the agent can find, quote, update, and validate. When you do that, prompts get shorter, long loops recover better, reviews become more consistent, and cleanup becomes schedulable.

That is why OpenAI's short `AGENTS.md` move matters. It is not a style preference. It is a context architecture.

## A Knowledge Base Validator

OpenAI's article says the team enforces documentation mechanically. A small repo can do the same. Start with a validator that checks link health, required sections, generated-doc freshness, and plan state.

Example required sections:

```yaml
docs/ARCHITECTURE.md:
  required_headings:
    - Domain Layers
    - Providers Boundary
    - Dependency Rules
docs/VALIDATION.md:
  required_headings:
    - Required Commands
    - UI Evidence
    - API Evidence
docs/SECURITY.md:
  required_headings:
    - Agent Permissions
    - Human Approval Required
    - Secrets
```

The validator's error message should teach the repair:

```text
docs/ARCHITECTURE.md is missing heading "Providers Boundary".
Add the heading and explain how cross-cutting concerns enter each domain.
This matters because scripts/check-architecture enforces provider imports.
```

That message gives the agent enough context to repair the doc. A terse "missing heading" failure would be cheaper for a human who already knows the repo, but weaker for a fresh agent.

## The Plan File As Recovery Memory

The user explicitly asked for the PRP plan to act as an operating contract after compaction. That is the same pattern OpenAI describes with execution plans. A plan file should not merely say "do task." It should let a new agent recover quickly.

A strong plan contains source prompt path or issue URL, current phase, earliest incomplete checklist item, current repo status, artifact paths, evidence limitations, files changed, commands run, validation state, exact next action, and stop conditions. This is more detailed than a human todo list because the reader may be a fresh agent with no memory.

Use this template:

```md
## Status Snapshot <timestamp>

- Current phase:
- Earliest incomplete item:
- Repo reconciliation:
- Files changed:
- Evidence captured:
- Limitations:
- Validation:
- Exact next action:
```

Update it after meaningful work, not every keystroke. Meaningful work includes source capture, file writes, validation failures, validation success, blockers, and changes in next action.

## Knowledge Store Smells

Watch for `AGENTS.md` files that become manuals, docs that say "ask the team," product decisions only in tickets, generated docs with no freshness check, active plans with no status, architecture docs not connected to lints, and review comments repeating the same rule across PRs.

Each smell has a harness repair: split long guidance into indexed docs, move durable decisions into repo docs, add freshness validation, add owner and date metadata, promote repeated review comments into lints, and archive stale docs through cleanup PRs. These repairs are not administrative polish. They decide what the agent can know.

## Agent-Readable Does Not Mean Human-Hostile

OpenAI's article says the repo became optimized first for Codex legibility. That can sound like sacrificing human readability. It should not. Agent-readable artifacts are usually good onboarding artifacts for humans too: clear architecture maps, explicit validation commands, generated schemas, linked decisions, and searchable logs.

The tradeoff appears when humans prefer elegant implicit conventions but agents need explicit structure. In a small expert team, everyone may know that "service never imports UI." In an agent-first repo, write it down and enforce it. The extra explicitness may feel heavy, but it buys repeatability.

The standard is not "make docs verbose." The standard is "make the right next document obvious." That is progressive disclosure for both humans and agents.
