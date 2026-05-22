# 09 — How People Use It Now: The Last-Six-Month View

The visible pattern from late 2025 through May 2026 is not “everyone is formally verifying product code now.” That would be hype.

The real pattern is narrower and more interesting:

1. Researchers are turning LLM/formal-methods pairings into benchmarks and agents.
2. Tool builders are wrapping coding agents with runtime guards and policy checks.
3. Practitioners are experimenting with TLA+, Lean, Dafny, and verification-assisted IDE flows.
4. Community discussions are optimistic but skeptical about wrong specs and overclaimed guarantees.

This chapter is the “what are people actually doing?” layer.

## Pattern 1: LLM-assisted Dafny verification

The Dafny cluster is the strongest evidence for practical code-level verification.

The older foundation is [DafnyBench](https://arxiv.org/html/2406.08467v1), which created a benchmark for LLM-generated verification hints over 750+ programs and about 53k lines of code. The recent extension is [DafnyPro](https://arxiv.org/html/2601.05385v1), a 2026 framework that improves LLM-assisted Dafny verification with a diff-checker, pruning, and proof-strategy hint augmentation. The paper reports 86% correct proofs on DafnyBench with Claude 3.5 Sonnet plus DafnyPro.

People are using this pattern as:

```text
LLM proposes annotations
Dafny checks
LLM repairs
harness prevents cheating
```

The open-source repos show early tooling:

- [DafnyBench repo](https://github.com/sun-wendy/DafnyBench),
- [dafny-annotator repo](https://github.com/metareflection/dafny-annotator),
- [Dafny Autopilot](https://github.com/Beneficial-AI-Foundation/dafny-autopilot), a VS Code extension for filling annotations, verifying selected functions, and explaining annotations.

The adoption signal is early. These repos are not at React-level popularity. But they are concrete, maintained, and aligned with a realistic developer workflow.

## Pattern 2: Natural-language-to-verified-code experiments

[From Natural Language to Verified Code](https://arxiv.org/html/2604.22601v1) is a 2026 example of moving from “help me annotate existing code” to “turn informal problem descriptions into verified Dafny code.”

Its results are instructive:

- contextless prompting fails badly,
- method signatures provide structural anchors,
- self-healing with Dafny verifier feedback improves performance,
- functional validation is needed to avoid vacuous verification.

That is exactly what coding-agent users should expect. A vague prompt is not enough. Structure helps. Feedback helps. Independent tests still help.

This pattern is likely to appear in developer tools as:

```text
issue or requirement -> candidate contract -> code -> verifier -> tests -> repair
```

The hard part is still the contract. That is why [Intent Formalization](https://arxiv.org/html/2603.17150v1) matters. It argues that AI-generated code makes the old intent gap larger. The field needs tools that help translate vague intent into checkable specs and then validate that those specs are meaningful.

## Pattern 3: Proof-search agents for Lean and Coq

Proof assistants are the cleanest “LLM proposes, checker verifies” environment. The recent pattern is agent scaffolding around Lean:

- [COPRA](https://arxiv.org/html/2310.04353v4) uses stateful backtracking, proof-environment feedback, and lemma retrieval.
- [Prover Agent](https://arxiv.org/abs/2506.19923) coordinates informal reasoning, formal prover models, Lean feedback, and auxiliary lemmas, with revisions through 2026.
- [A Minimal Agent for Automated Theorem Proving](https://arxiv.org/html/2602.24273v1) argues that iterative refinement, memory, and search are the core ingredients.

The last six months show a shift toward simpler, more analyzable proof-agent baselines. That is healthy. It helps separate “the model got better” from “the agent architecture got better.”

For coding-agent practitioners, the lesson is not necessarily “use Lean tomorrow.” It is:

```text
If your task has a strict checker, build the agent loop around that checker.
```

Proof assistants just make the lesson obvious.

## Pattern 4: LLM-generated TLA+ models with conformance checks

The May 2026 SIGOPS article [Can LLMs model real-world systems in TLA+?](https://www.sigops.org/2026/can-llms-model-real-world-systems-in-tla/) is one of the most directly relevant sources for agentic engineering.

The authors describe asking Claude to write a TLA+ spec for Etcd’s Raft implementation. The result passed syntax checks and ran through TLC, but looked more like the Raft paper than Etcd’s actual implementation. That motivated SysMoBench, which evaluates generated TLA+ specs through syntax, runtime, conformance, and invariant phases.

The practical use pattern is:

```text
LLM drafts TLA+ spec
model checker catches internal property violations
trace validation checks model-code conformance
agent or human repairs the model
```

The article also notes that frontier coding agents such as Claude Code and Codex already have strong ability in TLA+ modeling workflows and mentions Specula, an agent specialized in TLA+ formal modeling.

This is a good example of the “last six months” frontier: moving from raw LLM spec generation toward specialized agents that read repositories, decide what to model, run checks, and improve conformance.

## Pattern 5: Runtime guards for coding agents

The agent-security side is moving faster into practical tooling than full program verification.

[GoPlus AgentGuard](https://github.com/GoPlusSecurity/agentguard) is the clearest source in this set. It describes a security guard for AI agents that can install hooks for Claude Code, Codex, OpenClaw, and Hermes Agent, evaluate actions before execution, scan skills, log audit events, and run patrol/checkup commands.

This is how people are likely to use formal-methods ideas first in coding-agent environments:

```text
not: prove every generated line correct
but: block dangerous tool calls and data flows by policy
```

Examples:

- block `curl | bash`,
- require confirmation for risky shell commands,
- scan imported skills,
- maintain a trust registry,
- log which skill initiated which action,
- provide pre-tool and post-tool hooks.

These are not all “formal verification” in the academic sense. But they are on the runtime-verification path: observable event, explicit rule, enforcement, audit.

## Pattern 6: Data-flow and privacy analysis for agent tools

[AgentRaft](https://arxiv.org/html/2603.07557v1) shows a more research-heavy version of the same wrapper idea. It studies Data Over-Exposure in LLM agents, where agents transmit sensitive data beyond user intent or functional necessity. It uses cross-tool function call graphs, prompt synthesis, runtime taint tracking, and privacy judging.

This is relevant because tool-using coding agents often have broad access:

- repository files,
- logs,
- environment variables,
- issue descriptions,
- internal docs,
- browser pages,
- package registries.

A coding agent can accidentally move data from a safe context to an unsafe one. Formal data-flow labels are a natural defense:

```text
secret -> may not flow to browser
internal -> may flow to local tests, not external APIs
public -> may flow anywhere
```

The last six months show this becoming a named research problem for agents, not only a generic security concern.

## Pattern 7: Formal constraints for self-evolving agents

[SEVerA](https://arxiv.org/html/2603.25111v2) addresses self-evolving agents: programs synthesized by a planner LLM that call models and tools, then tune components for performance. The risk is that optimization breaks constraints.

SEVerA’s answer is to put hard formal contracts around generative-model calls and use verified fallbacks, so learning can improve soft objectives while preserving hard constraints.

In practical coding-agent terms:

```text
You may improve speed, success rate, or helpfulness.
You may not violate the output contract.
```

This matters because more coding agents will learn from traces, memories, or user feedback. Without hard constraints, self-improvement can become policy erosion.

## Pattern 8: Community skepticism and calibration

HN discussions were valuable because they pushed against overclaiming.

The [TLA+ thread](https://news.ycombinator.com/item?id=48065254) includes optimism about LLMs getting better at TLA+, but also concerns that generated specs are hard to validate and that implementation-coupled approaches like Verus may avoid model drift.

The [Lean thread](https://news.ycombinator.com/item?id=47047027) includes useful beginner explanations: theorem provers are not just tests; they are based on proof checking. It also shows practitioner interest in Lean as AI reasoning infrastructure.

The [LLM-verifier guarantee thread](https://news.ycombinator.com/item?id=46411539) is skeptical of a theoretical convergence paper, questioning whether experiments over a simplified Markov chain really establish useful LLM-verifier guarantees. This is a healthy warning: mathematical vocabulary can make weak claims sound stronger than they are.

## What is not happening yet

The research does **not** support the claim that most coding-agent users are doing full formal verification today.

What appears true:

- researchers are rapidly building benchmarks and agents,
- formal verification is becoming more feasible for assisted workflows,
- runtime policy enforcement is practical now,
- developers are discussing formal verification more because AI-generated code increases verification pressure.

What remains unproven:

- broad production adoption in ordinary web/product teams,
- fully automated natural-language-to-correct-spec pipelines,
- reliable autoformalization without human review,
- verification of large opaque LLMs themselves,
- economic ROI for all codebases.

## A practical maturity ladder

Here is a realistic ladder for how teams may adopt these ideas:

### Level 0: Tests only

Agent writes code. CI runs tests. Human reviews diff.

### Level 1: Stronger executable specs

Add property tests, schemas, assertions, golden examples, and contract tests.

### Level 2: Agent action policies

Add runtime monitors for shell, files, secrets, network, approvals, and deploys.

### Level 3: Model-check critical workflows

Model approval gates, retry loops, memory trust, subagent scope, or distributed protocols.

### Level 4: Verify critical code

Use Dafny, Verus, SPARK, F*, Lean, Coq, or similar for high-value components.

### Level 5: Assisted formalization pipeline

Agent drafts specs and proofs; tools verify; humans approve intent; audit trail preserves evidence.

Most teams are around levels 0-2. Research is pushing levels 3-5.

## The bottom line

People are using formal methods with coding agents in three main ways right now:

1. **As checkers for generated artifacts** — Dafny, Lean, Coq, TLA+.
2. **As policies over agent behavior** — runtime guards, temporal logic, tool-call constraints.
3. **As a research agenda for intent** — translating vague requirements into checkable specifications.

The last six months did not prove that formal methods have gone mainstream. They did show why they are becoming hard to ignore: coding agents make generation cheap, and cheap generation makes reliable checking valuable.
