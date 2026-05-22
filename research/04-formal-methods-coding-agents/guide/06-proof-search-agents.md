# 06 — Proof-Search Agents with Lean and Coq

If Dafny is the friendly bridge from code to contracts, Lean and Coq are the stricter world of machine-checked proofs.

A proof assistant is like a compiler for arguments. You state a theorem. You provide a proof. The assistant checks whether the proof really establishes the theorem. If the proof checks, it is accepted by a small trusted core. If it does not check, it fails.

For LLMs, this is a perfect playground. The model can guess the next proof step. The proof assistant can reject the guess.

## The ELI5 version

Imagine a math teacher who never gets tired and never accepts hand-waving.

Student says:

```text
Obviously, this follows.
```

Teacher says:

```text
No. Show the exact rule.
```

Student tries another step. The teacher checks again. Eventually, if every step is valid, the proof is accepted.

In theorem-proving agents, the LLM is the student. Lean or Coq is the teacher.

Lean’s official site describes it as an open-source programming language and proof assistant for correct, maintainable, formally verified code ([Lean](https://lean-lang.org/)). The HN Lean discussion gives a helpful programmer analogy: a theorem prover is closer to a proof-checking compiler than to a test suite ([HN](https://news.ycombinator.com/item?id=47047027)).

## Why this matters for coding agents

Many coding-agent failures are reasoning failures:

- “This refactor preserves behavior.” Does it?
- “This invariant is enough.” Is it?
- “This algorithm handles all edge cases.” Really?
- “This generated proof explains correctness.” Does a proof assistant accept it?

The proof assistant gives a hard boundary. The agent may produce a proof-looking string, but the assistant accepts only valid proof terms or tactic scripts.

That makes proof assistants a natural external judge for LLMs.

## COPRA: stateful backtracking with proof feedback

[COPRA](https://arxiv.org/html/2310.04353v4), short for in-COntext PRoof Agent, is a foundational proof-agent example. It uses a high-capacity general-purpose LLM, such as GPT-4 in the paper, to propose tactic applications in Lean and Coq. Those tactics are executed in the proof environment. Feedback from execution is used to build the next prompt, along with search history and retrieved lemmas.

The key words are **stateful backtracking search**.

A naive LLM call looks like this:

```text
Prompt: prove theorem
LLM: here is full proof
Checker: fail
```

COPRA-style search looks more like this:

```text
Proof state A
  -> try tactic 1
    -> proof state B
      -> try tactic 2
        -> fail
      -> backtrack
      -> try tactic 3
        -> proof state C
```

That is much closer to how human proof engineers work. You try a path, inspect the state, back up, use a lemma, and continue.

COPRA’s importance for coding agents is not only that it proves theorem-benchmark problems. It shows that the agent wrapper matters: history, retrieval, backtracking, and tool feedback turn a raw LLM into a proof-search system.

## Prover Agent: informal reasoner plus formal prover

[Prover Agent](https://arxiv.org/abs/2506.19923) takes a more multi-component approach. The arXiv abstract says it integrates LLMs with Lean, coordinates an informal reasoning LLM, a formal prover model, and Lean feedback, and generates auxiliary lemmas. It reports an 88.1% success rate on MiniF2F and 25 solved PutnamBench problems with a smaller sample budget than previous approaches among methods using small language models.

The auxiliary-lemma idea is important. A human mathematician often does not prove a theorem in one jump. They invent smaller facts:

```text
If A is true, then B follows.
If B and C are true, the goal is easier.
This special case handles the hard branch.
```

A proof agent can do the same. The LLM proposes helper lemmas. Lean checks whether they are true and useful. The agent uses accepted lemmas to advance the main proof.

For software agents, this suggests a pattern beyond math:

```text
Big task -> agent invents smaller checkable obligations -> tool checks each obligation -> compose result
```

That can apply to code review, migration planning, security policies, and distributed-system specs.

## Minimal proof agents: what scaffolding really helps?

The 2026 paper [A Minimal Agent for Automated Theorem Proving](https://arxiv.org/html/2602.24273v1) is useful because it asks a practical engineering question: which parts of fancy proof-agent architectures actually matter?

The paper proposes AxProverBase, a minimal baseline with:

- iterative proof refinement,
- library search and context management,
- memory,
- a proposer agent,
- a review system.

Its findings are highly relevant to coding-agent design:

1. Iterative proof refinement is the biggest factor.
2. Memory prevents the prover from running in circles.
3. Search through Lean libraries helps, but less than refinement and memory.
4. More powerful models benefit more when given the right scaffolding.
5. Simple agentic approaches can already be competitive and easier to adopt.

Read that as a general agent lesson:

```text
The model matters, but the loop matters too.
```

A raw frontier model without memory, search, and feedback may waste attempts. A smaller model in a good loop may be surprisingly useful.

## What proof assistants can and cannot guarantee

A proof assistant guarantees that a formal theorem follows from the accepted assumptions and definitions. It does not guarantee that the theorem is interesting, complete, or connected to the real-world claim.

HN commenters on a thread about formally verified science made the key criticism: Lean proves what you tell it to prove; someone still has to know enough to interpret whether the formal statement matches the informal claim ([HN related discussion](https://news.ycombinator.com/item?id=47444212)).

That is the same specification problem from earlier chapters.

A proof can be valid and irrelevant:

```text
Claim in English: this robot vision system is safe.
Formal theorem: a small helper function returns a non-negative integer.
Proof: valid.
Conclusion: not enough.
```

The proof assistant did its job. The human/specification layer failed.

## Why proof assistants are still a big deal

Even with that caveat, proof assistants are powerful because they give a rare thing in AI: a final check that is not based on vibes.

An LLM explanation can hallucinate. A proof-assistant kernel does not accept hallucinated proof steps. That makes theorem proving one of the cleanest examples of “LLM proposes, formal tool disposes.”

This has three implications for coding agents:

### 1. They can become proof engineers

An agent can search for invariants, lemmas, tactics, and proof decompositions. The human does not need to write every proof step if the assistant checks the result.

### 2. They can make formal methods more approachable

A beginner may not know the right Lean tactic or Dafny invariant. An agent can propose candidates and explain accepted proof steps. Dafny Autopilot’s annotation-explanation feature is a small example of this kind of pedagogy in program verification ([repo](https://github.com/Beneficial-AI-Foundation/dafny-autopilot)).

### 3. They can create new failure modes

Agents can loop, overfit to benchmark tasks, introduce irrelevant lemmas, or prove weak statements. Good scaffolding must track proof goals, prevent circular attempts, and require human review of important theorem statements.

## A proof-agent architecture in plain text

```text
+-------------------+
| theorem statement |
+---------+---------+
          |
          v
+-------------------+       +-------------------+
| context retriever | ----> | relevant lemmas   |
+---------+---------+       +-------------------+
          |
          v
+-------------------+       +-------------------+
| LLM proposer      | ----> | tactic / lemma    |
+---------+---------+       +-------------------+
          |                           |
          |                           v
          |                 +-------------------+
          |                 | Lean / Coq check  |
          |                 +---------+---------+
          |                           |
          +<--- proof state / error --+
```

Add memory so the agent does not repeat failed tactics. Add a budget so it does not run forever. Add human review for theorem meaning.

## What this means for non-math codebases

You may not use Lean in your web app. The proof-agent lesson still applies.

A coding agent improves when it has:

- a precise goal,
- a stateful workspace,
- a library or documentation search tool,
- a checker that returns structured errors,
- memory of failed attempts,
- a way to decompose hard goals,
- a strict acceptance criterion.

That is exactly the architecture of a serious coding-agent harness. Proof assistants are the cleanest laboratory for it because the acceptance criterion is mathematically sharp.

## The practical takeaway

If you are building or using coding agents, remember this:

```text
A proof-looking answer is not a proof.
A checker-accepted proof is a proof of a formal statement.
A useful proof is a checker-accepted proof of the statement you actually needed.
```

The agent can help with the first two steps. The human still owns the third.
