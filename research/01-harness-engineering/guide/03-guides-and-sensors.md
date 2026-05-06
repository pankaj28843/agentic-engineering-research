# Chapter 03 — Guides and sensors

**You'll learn:** Böckeler's core distinction between feedforward guides and feedback sensors, how computational and inferential controls differ, and why a harness needs both.

Source jumps: [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html), [Architectural fitness function](https://www.thoughtworks.com/en-de/radar/techniques/architectural-fitness-function), [Approved Scenarios / Approved Fixtures](https://lexler.github.io/augmented-coding-patterns/patterns/approved-fixtures/), and Stripe's [Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents).

![Fowler harness overview showing guides, sensors, self-correction, and human steering.](../assets/fowler/harness-overview.png)

Image credit: Birgitta Böckeler, [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html). Local copy documented in [assets/README.md](../assets/README.md).

## The two halves of a useful harness

Böckeler's main article gives the cleanest vocabulary in the source set: a coding-agent harness needs **guides** and **sensors**.

A guide is feedforward. It acts before the agent does the work. It says, “here is how to proceed,” “here are the conventions,” “here is the architecture,” “here is the command to bootstrap the app,” or “here is what good looks like.” Guides increase the chance that the first attempt is good.

A sensor is feedback. It acts after the agent does something. It says, “the tests failed,” “the import direction is illegal,” “the screenshot is wrong,” “the browser console has an error,” “the dependency scanner found a vulnerable package,” or “the reviewer thinks this is over-engineered.” Sensors let the agent self-correct.

You need both. A feedback-only harness lets the agent keep walking into the same wall and then says “try again.” A feedforward-only harness gives rules but never tells the agent whether it followed them. The useful loop is: guide, act, sense, correct, and then improve the guide or sensor if the failure repeats.

## Feedforward guides in plain English

A guide is anything that steers the agent before action. Examples include:

- `AGENTS.md` or `CLAUDE.md` saying how to work in the repo.
- A skill that explains how to run visual regression checks.
- A product spec with acceptance criteria.
- Architecture docs describing allowed dependency directions.
- A generated database schema reference.
- A script that scaffolds a new service in the standard shape.
- A code-mod tool that applies known migrations.
- A context interface, such as an MCP server, that tells the agent where to fetch relevant information.

Guides can be prose, code, tools, templates, or examples. The best guides are specific, short at the entry point, and easy to verify. “Write clean code” is weak. “Domain code must not import UI packages; run `npm run dep-cruiser` and fix violations before review” is stronger.

OpenAI's short `AGENTS.md` as table of contents is a guide. Stripe's conditionally applied subdirectory rules are guides. Anthropic's initializer prompt that creates a feature list and progress file is a guide for future sessions. This repo's `AGENTS.md` CDP daemon rule is a guide: it tells agents what daemon lifecycle command is safe unattended and when to ask a human.

## Feedback sensors in plain English

A sensor observes the result of action. Examples include:

- Unit tests, integration tests, type checks, linters, formatters.
- Structural tests for module boundaries.
- Browser automation that clicks through a user path.
- Screenshots, DOM snapshots, accessibility scans, console logs.
- Observability queries: logs, metrics, traces, SLO checks.
- Security scanners: secret detection, dependency checks, permission checks.
- LLM review agents and LLM-as-judge evaluators.
- Human review comments.

The trick is making sensor output useful to the agent. A linter error that says `E203` is less useful than an error that says, “This file imports from a forbidden layer. UI may import service, but service may not import UI. Move the shared type to `packages/types`.” Böckeler calls this a positive kind of prompt injection: the feedback message injects corrective instructions into the next agent step.

Stripe's minions show a production version of this idea. Their first line of defense is a local executable that heuristically selects relevant lints on each git push and returns feedback in less than five seconds. If local checks pass, CI selectively runs from a battery of more than three million tests. If CI fails, failures go back to the minion for one bounded retry, with at most two CI rounds because token, compute, and time costs have diminishing returns.

## Computational versus inferential controls

Böckeler adds a second axis: controls can be **computational** or **inferential**.

Computational controls are deterministic and fast. They run on CPUs. Tests, linters, type checkers, structural analysis, schema validation, dependency checks, and grep-based safety scans belong here. If the same input goes in, the same output should come out. These controls are cheap enough to run often.

Inferential controls use model judgement. AI code review, semantic duplicate detection, “does this answer contradict the retrieved policy?”, and LLM-as-judge evaluation belong here. They can understand meaning that deterministic tools miss, but they are slower, more expensive, and less repeatable.

The sweet spot is not one or the other. Use computational controls wherever you can because they are reliable and cheap. Use inferential controls where meaning matters and deterministic checks are too brittle. Do not ask an LLM to enforce formatting if a formatter can do it. Do not ask a regex to decide whether a design is over-engineered if semantic review is needed.

## A four-cell map

```text
                         Before action                 After action
                    ┌─────────────────────┬─────────────────────────┐
Computational       │ scripts, templates,  │ tests, linters, type     │
fast/deterministic  │ codemods, LSP hints  │ checks, structural rules │
                    ├─────────────────────┼─────────────────────────┤
Inferential         │ AGENTS.md, skills,   │ LLM reviews, semantic    │
semantic/probable   │ specs, examples      │ judges, critique agents  │
                    └─────────────────────┴─────────────────────────┘
```

This map prevents confusion. `AGENTS.md` is usually an inferential feedforward guide: the model reads prose and tries to follow it. A custom linter is a computational feedback sensor. A skill that includes both instructions and a bootstrap script can be mixed: the prose is inferential guidance; the script is computational guidance. An LLM review checklist is inferential feedback.

## Why computational sensors are having a comeback

Before coding agents, teams often underinvested in custom static analysis because it felt expensive. Why write a small linter for a local architecture rule if a senior engineer can catch it in review? Coding agents change the economics. If agents produce more code, review toil becomes the bottleneck. A custom linter that saves ten repeated review comments is now more valuable.

OpenAI says it enforces architecture and taste with custom linters and structural tests. The important detail is that the lints are Codex-generated too, and the error messages contain remediation instructions for agents. That is a harness insight: a linter is not just a red light for humans; it is a teacher for the agent.

Thoughtworks' [architectural fitness function](https://www.thoughtworks.com/en-de/radar/techniques/architectural-fitness-function) concept fits naturally here. A fitness function is an objective integrity assessment of an architectural characteristic. In ordinary software, it helps preserve architecture as the system evolves. In agentic software, it also gives the coding agent a sensor for architectural drift.

## Why behaviour sensors are harder

Maintainability and architecture have many computational hooks: type systems, import graphs, complexity metrics, dependency rules, file-size limits, coverage thresholds. Functional behaviour is harder. A green test suite generated by the same agent that wrote the feature can be false confidence. The agent may test the wrong thing, assert its own misunderstanding, or skip the user path that matters.

Böckeler calls behaviour the elephant in the room. Current high-autonomy workflows often combine a functional spec, an AI-generated test suite, coverage, maybe mutation testing, and manual testing. That is not enough to remove supervision.

The [approved fixtures](https://lexler.github.io/augmented-coding-patterns/patterns/approved-fixtures/) pattern is one partial answer. Instead of reviewing complicated generated assertion code, the team designs domain-readable fixture files that combine input and expected output. The runner is validated once. New cases are reviewed as diffs in a format humans can scan. For a checkout flow, a fixture might show cart input, service calls, and expected output. For Game of Life, it might show ASCII grids. This moves human review to a more meaningful level.

## The harness update habit

A guide or sensor is not automatically good. It earns its place by reducing repeated failure. The habit should be:

1. Notice a repeated agent failure.
2. Decide whether prevention or detection is better.
3. If prevention, add or improve a guide.
4. If detection, add or improve a sensor.
5. Prefer computational controls for crisp invariants.
6. Use inferential controls for semantic judgement.
7. Make the output legible to the agent.
8. Re-test whether the control still matters as models improve.

This habit keeps `AGENTS.md` from becoming a graveyard. Do not stuff every preference into the always-loaded prompt. Encode stable, crisp constraints as tools or tests. Put deeper guidance behind links. Retire rules that no longer pay rent.

## Chapter takeaways

- Guides steer before action; sensors observe after action.
- Computational controls are fast and deterministic; inferential controls are semantic but probabilistic.
- A harness needs both feedforward and feedback; either half alone fails.
- Agent-readable sensor output is a major leverage point.
- Behaviour verification remains the hardest unsolved part of harness design.

**Next:** [Chapter 04 — Context engineering](04-context-engineering.md).
