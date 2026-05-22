# 01 — The Toy Box Version: What Formal Methods Are

Imagine you are building a toy train track.

Testing is when you put a few trains on the track and see whether they fall off. You try the red train, the blue train, the train with three wagons, the train going fast, and maybe the train going backward. If all those examples work, you feel better.

Formal methods are when you first draw a precise map of the track and then ask a stricter question: “Can any train, from any allowed starting point, ever fall off the track?” If the map is small enough and the rule is precise enough, a machine can explore every possible position or check a proof that the train stays on the track.

That is the ELI5 version. The adult version is NASA’s definition: formal methods are “mathematically rigorous techniques and tools for the specification, design and verification of software and hardware systems,” where the specifications are well-formed statements in mathematical logic and verification is a rigorous deduction that can be mechanically checked ([NASA](https://shemesh.larc.nasa.gov/fm/fm-what.html)).

The most important word in that definition is **specific**. Formal methods do not prove a fuzzy sentence like “the whole product is good.” They prove claims like:

- this function returns a sorted list,
- this counter never becomes negative,
- this lock is never held by two owners at once,
- this distributed protocol never commits two conflicting values,
- this coding agent never runs `deploy` before tests pass,
- this tool-using agent never sends a secret to an external API.

A formal method is useful when the property is important, the model is honest enough, and the checking cost is lower than the cost of discovering the bug later.

## Tests are examples; proofs are promises under assumptions

A test is a story about one trip through the program:

```text
Given input [3, 1, 2]
When sort() runs
Then the answer should be [1, 2, 3]
```

That is valuable. A good test suite can catch many mistakes. But a test suite is still a list of examples. If the code fails on `[3, 2, 2, 1]` and nobody wrote that test, the test suite will not complain.

A formal specification tries to say the deeper rule:

```text
For every valid input list xs:
  output contains the same elements as xs
  output is ordered from smallest to largest
```

Then a verifier tries to prove the implementation always satisfies that rule. If it cannot prove it, the tool may produce an error or a counterexample.

That does not mean the formal proof is divine truth. It means: **if the specification says the right thing, and if the model’s assumptions match the real world closely enough, then the checked property holds inside that model.**

That sentence is the whole philosophy. Formal methods are strong because they are precise. They are limited because they are only as good as the precision you feed them.

## The three nouns: model, property, proof

Formal methods become much easier when you separate three things.

### 1. The model

A model is a simplified version of the system. It might be the actual code, a state machine, a TLA+ spec, a Dafny program, a Lean theorem, a protocol diagram, or a finite abstraction of a workflow.

A model is like a map. A map is not the city. It leaves things out. That is fine if it leaves out the right things. A subway map ignores building shapes, traffic lights, and tree locations because those do not matter for finding train stops. But if your question is “Can a fire truck reach this building?” the subway map is the wrong model.

NASA’s page makes the same point in a more formal way: complete state-space analysis of real systems is rarely practical, so people analyze high-level designs, critical components, reduced models, and hierarchical slices ([NASA](https://shemesh.larc.nasa.gov/fm/fm-what.html)).

### 2. The property

A property is the thing you want to be true.

Some properties are **safety** properties: “bad thing never happens.” Examples:

- no negative balance,
- no duplicate refund,
- no deployment without green CI,
- no tool call that leaks a secret.

Some properties are **liveness** properties: “good thing eventually happens.” Examples:

- every request eventually receives a response,
- the agent eventually stops retrying,
- a consensus protocol eventually decides if the network behaves as assumed.

Some properties are **functional correctness** properties: “the output matches the mathematical meaning of the input.” Example: sorting really sorts and preserves elements.

### 3. The proof or check

The proof or check is the machine-verifiable evidence. In a model checker, the machine may explore states looking for a counterexample. In a proof assistant, the machine checks proof steps. In an SMT-backed verifier, the tool reduces verification conditions to logical constraints and asks a solver. In runtime verification, a monitor checks the actual trace of events as the system runs.

This is why formal methods pair so naturally with coding agents. The LLM can invent candidate artifacts quickly. The checker can say “no.” The “no” is gold. It is not a vague opinion. It is usually an error, failed obligation, missing invariant, rejected tactic, or counterexample.

## The main families in plain language

### Formal specification

A formal specification is a requirement written in a precise language instead of fuzzy prose. It can look like preconditions and postconditions, type refinements, temporal logic, invariants, state machines, or mathematical theorems.

Informal:

```text
Refunds above $500 need approval.
```

More formal:

```text
refund_amount > 500 implies manager_approved == true
```

The formal version is not automatically better. It is better only if it captures the intended policy. If the real policy is “refunds of $500 or more need approval,” the formal version above is wrong at exactly $500.

### Model checking

Model checking explores possible states. It is especially useful when the bug is hidden in a combination of timing, concurrency, retries, messages, and failures. Leslie Lamport describes TLA+ as a high-level language for modeling programs and systems, especially concurrent and distributed ones, using simple mathematics to describe things precisely ([TLA+](https://lamport.azurewebsites.net/tla/tla.html)). The TLA+ tools page describes TLC as an explicit-state model checker and Apalache as a symbolic model checker using SMT ([TLA+ tools](https://lamport.azurewebsites.net/tla/tools.html)).

If tests are “try these 30 paths,” model checking is “walk every path in this small universe and tell me if any path breaks the rule.”

### Theorem proving and proof assistants

A proof assistant is like a compiler for mathematical arguments. Lean describes itself as an open-source programming language and proof assistant that enables correct, maintainable, formally verified code ([Lean](https://lean-lang.org/)). The LLM may propose a proof, but Lean accepts it only if the proof checks.

The HN discussion around Lean captured the beginner-friendly intuition well: a theorem prover is not just a bigger pile of tests; it is closer to a program that has to compile as a proof ([HN Lean discussion](https://news.ycombinator.com/item?id=47047027)).

### Program verification

Program verification proves code against a spec. Dafny is the most useful source in this guide because it looks like a bridge from normal programming to proof. The official Dafny site calls it a “verification-aware programming language” with native support for specifications and a static verifier ([Dafny](https://dafny.org/)). It supports preconditions, postconditions, termination conditions, loop invariants, lemmas, and other proof machinery.

### Runtime verification

Runtime verification watches the actual execution. Instead of proving every possible path before deployment, it checks the path the system is taking now. This is useful for agents because tool calls, memory writes, and API requests are observable. [AgentGuard](https://arxiv.org/html/2509.23864v1) frames this as an inspection layer that observes raw agent I/O, abstracts events, learns a model, and applies probabilistic model checking.

## A tiny mental model

Use this whenever the topic feels intimidating:

```text
Informal wish:  "The agent should not do dangerous thing X."
Formal property: "X is forbidden unless approval=true and tests_passed=true."
Model:          "The agent loop has states and tool-call events."
Checker:        "Before every tool call, test the property."
Action:         "Block, ask human, or continue."
```

Formal methods are not one tool. They are a habit: turn wishes into checkable claims, then let machines be stubborn about those claims.
