# 03 — The Main Tools: Specs, Model Checkers, Proof Assistants, Verifiers

Formal methods can feel like a shelf full of mysterious instruments. The trick is to group them by the question they answer.

- **Specification:** What exactly should be true?
- **Model checking:** Can any reachable state break the rule?
- **Theorem proving:** Can a mechanically checked proof establish the rule?
- **Program verification:** Does this code satisfy its contract?
- **Runtime verification:** Is this running system violating the rule right now?
- **Static analysis / symbolic execution / SMT:** Can logical constraints expose a bug without running every input?

A coding agent can use all of these as external senses. The agent may write text, code, or plans, but the tool gives a non-chatty answer: accepted, rejected, counterexample, timeout, or unknown.

## Formal specification: the recipe card

A specification is a recipe card for correctness. It says what the dish must be, not every detail of how to cook it.

For a normal function, a specification might include:

```text
requires input is not null
requires refund_amount <= original_charge
ensures output.status == "approved" or output.status == "rejected"
ensures account.balance == old(account.balance) - refund_amount
```

For an agent workflow, a specification might include temporal rules:

```text
Always: deploy can happen only after tests_passed.
Always: external_email can happen only after human_approved.
Eventually: after three failed retries, the agent stops and asks for help.
Never: secret data flows into browser.search.
```

Notice that these are not all code-level properties. Some are workflow properties. Some are security policies. Some are business rules. That is why formal methods matter for agentic engineering: the agent’s behavior is bigger than generated code.

## Dafny: the friendly bridge from code to proof

Dafny is a good first formal-methods tool for programmers because it looks close to normal imperative programming. The official site calls it a “verification-aware programming language” with native support for recording specifications and a static program verifier ([Dafny](https://dafny.org/)). It supports common programming concepts and proof tools such as preconditions, postconditions, termination conditions, loop invariants, read/write specs, quantifiers, lemmas, and calculational proofs.

Here is the ELI5 version of Dafny:

```text
You write code.
You also write promises about the code.
Dafny tries to prove the code keeps the promises.
If Dafny cannot prove it, it complains before runtime.
```

A tiny Dafny-flavored sketch:

```dafny
method Abs(x: int) returns (y: int)
  ensures y >= 0
  ensures y == x || y == -x
{
  if x < 0 { y := -x; }
  else { y := x; }
}
```

The verifier checks that every path satisfies the postconditions. For loops, the hard part is often the invariant: the fact that remains true each time through the loop. That is exactly where LLMs are being used: ask the model to propose invariants and assertions, run Dafny, feed back errors, and try again.

Dafny’s role in the recent coding-agent literature is large because it combines executable-looking programs with formal contracts and automated SMT-backed verification. It gives the LLM a clear target: produce annotations that make verification succeed without changing the program’s meaning.

## TLA+: the state-machine lens

TLA+ is useful when you care about states and transitions more than line-by-line implementation. Leslie Lamport describes it as a high-level language for modeling programs and systems, especially concurrent and distributed ones, based on simple mathematics ([TLA+](https://lamport.azurewebsites.net/tla/tla.html)).

A TLA+ style model asks:

```text
What are the variables?
What is the initial state?
What actions can change the state?
What must always be true?
What should eventually happen?
```

This is a natural fit for agents. An agent loop has states:

```text
Idle -> Planning -> ToolCall -> Observing -> UpdatingMemory -> Done
```

And actions:

```text
plan
call_tool
write_file
run_tests
ask_human
retry
finish
```

Then you can check rules like:

```text
Never call deploy unless tests_passed = true.
Never write secrets to external_tool.
Eventually stop retrying after retry_count >= 3.
```

The TLA+ tools page describes SANY for parsing/syntax checks, TLC as an explicit-state model checker, Apalache as a symbolic model checker using SMT, and TLAPS as a proof system ([TLA+ tools](https://lamport.azurewebsites.net/tla/tools.html)).

The important coding-agent lesson is that syntax is not enough. The SIGOPS/SysMoBench article showed that LLMs can often write TLA+ modules that compile and run, while failing conformance checks against the real system behavior ([SIGOPS](https://www.sigops.org/2026/can-llms-model-real-world-systems-in-tla/)). A model checker can prove properties of the model. It cannot rescue you if the model describes the wrong thing.

## Lean and proof assistants: a compiler for arguments

Lean is an open-source programming language and proof assistant ([Lean](https://lean-lang.org/)). A proof assistant checks formal proofs. If the proof checks, the theorem is accepted. If a tactic fails, the assistant tells you the remaining proof state or error.

For coding agents, this creates a loop:

```text
LLM proposes tactic or lemma
Lean checks it
if it fails, Lean returns proof state/error
LLM tries another tactic or lemma
```

This is different from asking an LLM, “Explain why this theorem is true.” The LLM’s explanation may be beautiful and wrong. Lean’s kernel is not impressed by beauty. It accepts only valid proof terms.

[COPRA](https://arxiv.org/html/2310.04353v4) is a foundational example of an LLM used as an in-context proof agent. It repeatedly asks GPT-4 for tactic applications inside a stateful backtracking search, executes those tactics in Lean or Coq, and uses proof-environment feedback in the next prompt. [Prover Agent](https://arxiv.org/abs/2506.19923) combines informal reasoning, a formal prover model, Lean feedback, and auxiliary lemmas. [A Minimal Agent for Automated Theorem Proving](https://arxiv.org/html/2602.24273v1) argues that iterative refinement, memory, and library search are the core scaffolding pieces.

The pattern is the same each time: the model searches; the proof assistant checks.

## Runtime monitors: the bouncer at the door

Not every property should be proved before the run. Some properties are best enforced at the moment an agent tries to act.

A runtime monitor is like a bouncer at a club door. It does not care what the agent was thinking. It checks the event:

```text
tool_name = "shell"
command = "rm -rf /tmp/prod-data"
approval = false
```

Then it says:

```text
blocked: destructive command requires approval
```

[AgentGuard](https://arxiv.org/html/2509.23864v1) is research on runtime verification for AI agents. It observes raw agent input/output, abstracts that into formal events, learns a Markov Decision Process online, and applies probabilistic model checking. [GoPlus AgentGuard](https://github.com/GoPlusSecurity/agentguard) is an open-source runtime security guard for coding-agent environments such as Claude Code, Codex, OpenClaw, and others, using hooks to scan skills and evaluate tool actions.

Runtime verification is especially practical for coding agents because many risky actions are visible:

- shell command,
- file write,
- network call,
- browser action,
- database write,
- secret access,
- deploy,
- email send,
- memory write.

You may not be able to prove what the LLM will think. You can often block what the wrapper will allow.

## SMT, SAT, symbolic execution, and static analysis: the hidden engines

Many formal tools rely on solvers. SAT solvers answer Boolean satisfiability questions. SMT solvers handle richer theories: integers, arrays, bitvectors, algebraic datatypes, and more. Symbolic execution explores program paths with symbolic inputs instead of concrete inputs. Abstract interpretation proves properties by approximating program behavior.

For this guide, you do not need to know all solver internals. You need the shape:

```text
program/spec -> logical constraints -> solver -> sat/unsat/unknown/counterexample
```

Dafny uses automated reasoning and SMT-style verification conditions under the hood. Apalache uses SMT for TLA+ checking. Agent privacy tools such as [AgentRaft](https://arxiv.org/html/2603.07557v1) borrow program-analysis ideas like call graphs and taint tracking.

These engines are important because they are independent of the LLM. The model can make a claim. The solver can refute it.

## The tool map for coding agents

Here is a beginner map:

| Problem | Formal-ish tool family | Agent use |
|---|---|---|
| “What did the user mean?” | specs, examples, contracts, DSLs | agent drafts; human reviews |
| “Can this code satisfy the contract?” | Dafny, F*, SPARK, Verus, SMT-backed verifiers | agent writes annotations and repairs errors |
| “Can this protocol deadlock?” | TLA+, PlusCal, model checking | agent drafts model; checker finds counterexample |
| “Can this theorem be proved?” | Lean, Coq, Isabelle | agent proposes tactics/lemmas; kernel checks |
| “Can this tool sequence violate policy?” | temporal logic, runtime monitors | monitor blocks or asks approval |
| “Can private data leak across tools?” | taint tracking, call graphs, data-flow analysis | analyzer traces data through agent tools |
| “Can the agent cheat the check?” | diff-checkers, code immutability, semantic validation | harness prevents modifying target logic |

## The key habit

Do not start by asking, “Which formal method should I use?” Start by asking:

```text
What property would be expensive to get wrong?
Can I state it precisely?
Can I observe or model the events involved?
Can a machine check it?
What should happen when the check fails?
```

That is enough to begin. The named tools are just different ways to answer those questions.
