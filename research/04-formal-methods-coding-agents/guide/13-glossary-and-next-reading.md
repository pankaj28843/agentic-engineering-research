# 13 — Glossary and Next Reading Path

This final chapter is a memory aid. Use it when the terminology starts to blur.

## Two-sentence summary

Formal methods are ways to state and check precise properties of systems using mathematical logic, model exploration, proof assistants, verifiers, or runtime monitors. For coding agents, the practical pattern is to treat the LLM as an untrusted generator inside a loop where independent tools check code, specs, proofs, workflows, tool calls, and data flows.

## Core glossary

### Formal methods

Mathematically rigorous techniques and tools for specification, design, and verification. NASA’s definition emphasizes well-formed logical statements and mechanically checkable deduction steps ([NASA](https://shemesh.larc.nasa.gov/fm/fm-what.html)).

### Specification

A precise statement of what should be true. Specs can be preconditions, postconditions, invariants, temporal rules, type refinements, state machines, or theorem statements.

### Verification

Checking that an artifact satisfies a specification. The artifact might be code, a model, a proof, a plan, a tool-call trace, or a workflow.

### Validation

Checking that the specification itself means what humans intended. This is the hard part in AI-generated code, emphasized by [Intent Formalization](https://arxiv.org/html/2603.17150v1).

### Model

A simplified representation of a system. A model is useful if it preserves the behavior relevant to the property being checked.

### Model checking

Exploring states of a model to find violations of safety or liveness properties. TLA+ with TLC is a classic example ([TLA+ tools](https://lamport.azurewebsites.net/tla/tools.html)).

### Safety property

A “bad thing never happens” property.

Examples:

```text
never deploy without tests
never refund more than original charge
never leak secrets to browser.search
```

### Liveness property

A “good thing eventually happens” property.

Examples:

```text
every request eventually gets a response
a retry loop eventually stops or asks a human
```

### Invariant

A fact that should always remain true. In loops, invariants are facts true before and after each iteration. In agent workflows, invariants are rules like “approval is required before deployment.”

### Precondition

A condition that must be true before an operation is allowed.

### Postcondition

A condition that must be true after an operation completes.

### Proof assistant

A tool like Lean or Coq that checks formal proofs. Lean describes itself as a programming language and proof assistant for formally verified code ([Lean](https://lean-lang.org/)).

### Program verifier

A tool that checks code against specifications. Dafny is a verification-aware programming language with native specs and a static verifier ([Dafny](https://dafny.org/)).

### SMT solver

A solver for logical constraints over theories such as integers, arrays, and bitvectors. Many verification tools use SMT solvers under the hood.

### Counterexample

A concrete or symbolic path showing how a property can fail. Counterexamples are one of the best feedback signals for coding agents.

### Autoformalization

Translating natural language into formal specifications. LLMs can help, but humans must review whether the formalization captures intent.

### Runtime verification

Checking execution traces while the system runs. [AgentGuard](https://arxiv.org/html/2509.23864v1) applies this idea to AI agents.

### Taint tracking

Tracking labeled data as it flows through a system. [AgentRaft](https://arxiv.org/html/2603.07557v1) uses runtime taint tracking to detect data over-exposure in LLM agents.

### Temporal logic

A logic for rules over time: always, eventually, until, before, after. Useful for tool-call and workflow policies.

### Vacuous verification

A proof or verification that passes because the spec is too weak or impossible to violate. Example: `requires false` or `ensures true`.

### Agent harness

The system around the LLM: tools, prompts, permissions, state, memory, tests, monitors, approval gates, and audit logs. Formal methods are often most practical in the harness rather than inside the LLM.

## The five patterns to remember

### 1. LLM as spec drafter

The agent turns prose into candidate contracts.

Risk: it formalizes the wrong thing.

Control: human reviews examples, non-examples, and spec meaning.

### 2. LLM as proof/code generator

The agent writes code, invariants, lemmas, or tactics.

Risk: invalid artifacts or cheating.

Control: verifier/proof assistant checks; protected files prevent spec weakening.

### 3. LLM as model builder

The agent drafts a TLA+ or state-machine model.

Risk: model compiles but does not match implementation.

Control: conformance checks against traces, as emphasized by [SysMoBench](https://www.sigops.org/2026/can-llms-model-real-world-systems-in-tla/).

### 4. LLM as tool user under policy

The agent calls shell, browser, editor, database, email, or deploy tools.

Risk: unsafe action or data leak.

Control: runtime monitor, tool policy, data labels, approval gates.

### 5. LLM as self-improving component

The agent learns or tunes itself for better performance.

Risk: optimization violates safety constraints.

Control: hard formal constraints, guarded outputs, verified fallbacks, as explored by [SEVerA](https://arxiv.org/html/2603.25111v2).

## Recommended reading path

### If you are brand new

1. NASA’s [What is Formal Methods?](https://shemesh.larc.nasa.gov/fm/fm-what.html) for the baseline definition and limitations.
2. Dafny’s [official overview](https://dafny.org/) to see program verification in a programmer-friendly form.
3. Lean’s [official site](https://lean-lang.org/) to understand proof assistants at a high level.
4. TLA+ [home page](https://lamport.azurewebsites.net/tla/tla.html) and [tools page](https://lamport.azurewebsites.net/tla/tools.html) to understand model checking.

### If you care about coding agents and specs

1. [Intent Formalization](https://arxiv.org/html/2603.17150v1) for the research agenda.
2. The [RiSE blog version](https://risemsr.github.io/blog/2026-03-05-shuvendu-intent-formalization/) for a readable summary.
3. [From Natural Language to Verified Code](https://arxiv.org/html/2604.22601v1) for NL-to-Dafny experiments and the importance of self-healing plus functional validation.

### If you care about verified code generation

1. [DafnyBench](https://arxiv.org/html/2406.08467v1) for the benchmark.
2. [dafny-annotator](https://arxiv.org/html/2411.15143v1) for LLM plus search.
3. [DafnyPro](https://arxiv.org/html/2601.05385v1) for 2026 harness improvements such as diff-checking and proof-strategy hints.
4. [Dafny Autopilot](https://github.com/Beneficial-AI-Foundation/dafny-autopilot) for a user-facing IDE-style workflow.

### If you care about proof assistants

1. [COPRA](https://arxiv.org/html/2310.04353v4) for stateful LLM proof search.
2. [Prover Agent](https://arxiv.org/abs/2506.19923) for informal/formal prover coordination and auxiliary lemmas.
3. [A Minimal Agent for Automated Theorem Proving](https://arxiv.org/html/2602.24273v1) for the scaffold components that matter.
4. HN’s [Lean discussion](https://news.ycombinator.com/item?id=47047027) for practitioner explanations and caveats.

### If you care about agent runtime safety

1. [AgentGuard paper](https://arxiv.org/html/2509.23864v1) for runtime verification framing.
2. [GoPlus AgentGuard](https://github.com/GoPlusSecurity/agentguard) for concrete coding-agent hooks and action evaluation.
3. [AgentRaft](https://arxiv.org/html/2603.07557v1) for data over-exposure and taint tracking.
4. [AgentVerify](https://preprints.org/manuscript/202604.1029) for LTL over memory/tool/MCP/human boundaries, labeled as preprint.
5. [SEVerA](https://arxiv.org/html/2603.25111v2) for formally guarded self-evolving agents.

### If you care about TLA+ and model conformance

1. [Can LLMs model real-world systems in TLA+?](https://www.sigops.org/2026/can-llms-model-real-world-systems-in-tla/) for the SysMoBench story.
2. HN’s [TLA+ discussion](https://news.ycombinator.com/item?id=48065254) for practitioner reactions.
3. TLA+ [tools](https://lamport.azurewebsites.net/tla/tools.html) for TLC, Apalache, and TLAPS.

## The one-page playbook

When a coding agent is doing risky work:

```text
1. Ask for contract before code.
2. Include examples and non-examples.
3. Human approves meaning.
4. Agent writes code/proof/model.
5. Independent checker runs.
6. Counterexamples feed repair.
7. Protected files prevent cheating.
8. Runtime monitor gates risky tool calls.
9. Data labels prevent leaks.
10. Audit trail records checks and approvals.
```

## The final warning

A formal method answers the question you ask. Coding agents make it easier to ask many questions quickly. They also make it easier to ask the wrong question fluently.

So the craft is not only proof. The craft is choosing the right property, checking it with the right tool, and keeping the human responsible for intent.
