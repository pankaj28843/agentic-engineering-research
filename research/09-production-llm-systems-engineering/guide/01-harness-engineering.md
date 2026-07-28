# 1. Harness engineering: make good work the easy path

Harness engineering is the design of the environment around an AI worker:
instructions, tools, permissions, repository knowledge, feedback signals,
verification, and recovery. A prompt asks for an outcome. A harness makes the
outcome observable and gives the agent a bounded way to reach it.

That distinction is the first important move in production AI engineering.
When a coding agent repeatedly fails, rewriting “please be careful” is rarely
the durable fix. The better question is the one an experienced platform
engineer already knows how to ask:

> What capability, signal, constraint, or feedback loop is missing from the
> operating environment?

## ELI5: a chef needs a kitchen, not a longer order

Imagine telling a skilled chef, “Make a safe, excellent dinner.” That sentence
does not provide fresh ingredients, labelled allergy information, clean
equipment, a thermometer, or a ticket showing which table ordered what.

The order is the prompt. The kitchen is the harness.

A good kitchen does not guarantee a perfect meal, but it makes important facts
visible, catches common mistakes early, and limits the blast radius of a bad
decision. The same is true for an agent. Its “kitchen” might contain a
repository map, a test runner, an isolated worktree, browser access, structured
logs, a schema-defined deployment tool, and a rule requiring evidence before
completion.

## The control loop

A useful harness implements a closed loop:

```text
intent → inspect → act → observe → verify → repair or stop
```

Each arrow needs an engineered interface.

1. **Intent:** a task has an acceptance contract, relevant constraints, and a
   definition of done.
2. **Inspect:** the agent can discover code, docs, runtime state, and prior
   decisions without receiving an enormous context dump.
3. **Act:** tools expose narrow, typed operations with appropriate authority.
4. **Observe:** logs, traces, screenshots, diffs, and command results are
   legible to the agent.
5. **Verify:** deterministic checks and risk-calibrated review test the result.
6. **Repair or stop:** bounded retries address a diagnosed failure; budgets and
   terminal conditions prevent endless motion.

OpenAI’s production account,
[OpenAI, “Harness engineering: leveraging Codex in an agent-first world”](https://openai.com/index/harness-engineering/),
describes a team making its application, browser, logs, metrics, architecture,
and repository knowledge directly legible to coding agents. The reported scale
and productivity are a first-party case, not a controlled comparison. Its most
transferable evidence is the mechanism: once code generation became cheap,
human QA and missing environmental feedback became the bottlenecks.

The independent synthesis
[Martin Fowler site, “Harness engineering for coding agent users”](https://martinfowler.com/articles/harness-engineering.html)
frames a harness in terms of feed-forward steering and feedback regulation.
That is a helpful corrective to the idea that a harness is merely a collection
of prompts. Architecture fitness functions, maintainability checks, runtime
sensors, and human judgment all regulate different failure classes.

## Five layers of a production harness

### 1. A navigable source of truth

Put durable facts where both people and agents can find and validate them:
versioned architecture maps, service contracts, commands, decision records,
and current plans. Keep the initial instruction surface short and use it as a
map to deeper material.

The failure mode is a giant “everything manual.” It consumes context, mixes
current rules with archaeology, and becomes impossible to verify. Progressive
disclosure is better: start with the route, then load the smallest relevant
document.

### 2. Narrow tools with explicit contracts

Prefer `deploy(environment, artifact_digest)` over “run any shell command on
production.” A tool contract should define:

- required and optional arguments;
- types, bounds, and accepted identifiers;
- side effects and idempotency behavior;
- authority and tenant scope;
- success, retryable failure, and permanent failure results;
- safe timeouts and cancellation.

The model may choose a tool probabilistically. Authorization, validation, and
idempotency must remain deterministic.

### 3. Legible runtime evidence

Agents cannot respond to signals they cannot see. Expose the same evidence a
careful engineer would need: command exit status, focused logs, trace IDs,
metrics tied to a service objective, browser state, and before/after artifacts.
Avoid dumping entire log stores into context. Give the agent query tools and
stable identifiers so it can inspect on demand.

### 4. Mechanical quality gates

Move cheap, objective checks close to the action: formatting, type checks,
schema validation, tests, policy checks, dependency rules, and architectural
constraints. Reserve model review and human review for properties that require
judgment.

A model reviewing another model is not an independent oracle. It can share the
same blind spot. Use different evidence channels: tests for behavior, static
analysis for known patterns, runtime probes for integration, and humans for
consequence-heavy ambiguity.

### 5. Isolation, budgets, and recovery

Give each task a disposable or clearly scoped environment. Bound wall-clock
time, tokens, tool calls, monetary spend, and destructive authority. Record
checkpoints and make cleanup reliable. A six-hour autonomous run can be useful
only if it cannot quietly consume unlimited resources or operate on unrelated
state.

## Harness engineering is not prompt engineering

The two cooperate, but they fix different problems.

| Symptom | Prompt-level response | Harness-level response |
| --- | --- | --- |
| Agent edits the wrong module | Clarify the requested module | Provide an architecture map and scope validator |
| It claims success without running tests | Ask it to test | Make test evidence part of the completion contract |
| It repeats a charge after timeout | Say “do not retry twice” | Use an idempotency key and queryable operation state |
| It misses a browser regression | Describe the UI more carefully | Give it an isolated app plus browser observation |
| It forgets a long task’s decision | Repeat the history | Persist a decision/progress ledger and reload it |

If changing adjectives fixes the failure, prompt engineering may be enough. If
the fix changes what can be known, done, observed, or enforced, it is harness
engineering.

## A worked design: the issue-to-pull-request agent

Suppose an agent receives “Fix checkout occasionally charging twice.”

A weak harness supplies the repository and a shell. A production harness
instead does the following:

1. resolves the issue, affected service, data classification, and allowed
   environments;
2. supplies a short service map and links to payment invariants;
3. creates an isolated worktree and disposable test stack;
4. exposes trace search using a sanitized incident correlation ID;
5. provides a fake payment gateway capable of delayed and duplicated replies;
6. requires a failing regression test before implementation;
7. makes the charge tool require an idempotency key;
8. runs tests, a duplicate-delivery scenario, and a browser checkout journey;
9. records the diff, evidence, unresolved risks, and rollback note;
10. stops for human approval before any production mutation.

The model still reasons about the bug. The harness supplies the conditions
under which that reasoning can become trustworthy engineering work.

## What not to copy from a case study

OpenAI reports an unusual greenfield experiment in which agents wrote all code
and the team accepted a high-throughput merge philosophy. That does not prove
that minimal blocking gates fit a medical device, a payment ledger, or a
legacy monolith. “Corrections are cheap” is a workload property, not a law.

Similarly, community discussion around
[Hacker News, “Harness engineering: Leveraging Codex in an agent-first world”](https://news.ycombinator.com/item?id=48416264)
is useful for surfacing terminology disputes and skepticism, but comments are
experience reports, not representative measurement. Retain the objections as
test hypotheses: does the proposed harness reduce accepted-task time, or only
increase generated change?

## A small adoption ladder

Start with one repetitive workflow.

1. Write its observable acceptance contract.
2. Give the agent read-only discovery and a disposable workspace.
3. Add one deterministic verifier for the most frequent costly mistake.
4. Record tool calls, test results, elapsed time, review time, and later
   defects.
5. Add authority only after the lower-risk loop is reliable.
6. Turn every recurring failure into one of three things: a better source of
   truth, a tighter tool, or a stronger sensor.

Measure cost per **accepted** task, not lines changed, tokens consumed, or pull
requests opened.

## Interview checkpoint

**Question:** “How would you improve an unreliable coding agent?”

A strong answer first classifies failures. Missing or stale facts suggest
context work. Ambiguous intent suggests a task contract. Unsafe or malformed
actions suggest tool and authorization controls. False completion suggests
verification and observability. Repeated loops suggest budgets and terminal
conditions. Model or prompt changes come after the environment has been made
diagnosable.

**Explain it back:** What information would you need to decide whether a
failure belongs to the model, prompt, context assembler, tool implementation,
or verifier?

## Field exercise

Choose one engineering task you perform weekly. Draw its current
`intent → act → verify` path. Mark every point where a human silently supplies
memory, judgment, credentials, or visual inspection. Those hidden inputs are
your first harness backlog.

## Capstone increment

Draw architecture v1 for the tenant-aware document operations assistant:
source of truth → context/retrieval → model proposal → read/write tools →
verifier → approval-bound commit → terminal state. Save one terminal evidence
record for a successful run and one for a safe stop.

**Definition of done:** another engineer can identify who owns every effect
and can distinguish “the model said it finished” from verified completion.
Context, caches, budgets, and tenant scope remain labelled placeholders; later
chapters fill them in.

Next: [Context engineering](02-context-engineering.md) zooms into the subsystem
that decides what the model is allowed to know on each inference call.
