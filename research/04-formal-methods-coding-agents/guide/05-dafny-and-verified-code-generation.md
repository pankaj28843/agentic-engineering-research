# 05 — Verified Code Generation with Dafny

If you want one concrete place where coding agents and formal methods are already meeting, start with Dafny.

Dafny looks like a programming language, but it is designed around verification. The official site says Dafny has native support for recording specifications and a static program verifier, so developers can write provably correct code with respect to specifications ([Dafny](https://dafny.org/)). It compiles to familiar languages such as C#, Java, JavaScript, Go, and Python, but the key idea is not compilation. The key idea is that code and proof obligations live together.

For coding agents, Dafny is attractive because the agent can write familiar-looking code and the verifier can give strict feedback.

## The Dafny mental model

A Dafny method can have:

- `requires` — what must be true before calling,
- `ensures` — what must be true after returning,
- `invariant` — what remains true during a loop,
- `decreases` — why recursion or a loop terminates,
- `assert` — a fact the verifier should be able to prove at that point,
- lemmas — helper proofs.

A beginner way to read Dafny is:

```text
requires = caller's promise
ensures = method's promise
invariant = loop's promise
assert = proof checkpoint
```

The verifier tries to prove all promises. If it cannot, the program does not verify.

## Why LLMs help here

The hard part of Dafny is often not the algorithm. The hard part is helping the verifier see why the algorithm is correct. Humans write loop invariants, assertions, lemmas, and termination arguments. That requires logic skill and tool-specific intuition.

LLMs are not guaranteed to be correct, but they are good at proposing plausible missing text. Dafny can reject wrong proposals. That creates a natural repair loop.

```text
Dafny code with missing invariant
  -> LLM proposes invariant
  -> Dafny checks
  -> error message says what cannot be proved
  -> LLM proposes another invariant or assertion
```

This is why Dafny appears repeatedly in the recent source set.

## DafnyBench: measuring the task

[DafnyBench](https://arxiv.org/html/2406.08467v1) is one of the core benchmark sources. It introduces a benchmark for training and evaluating machine-learning systems for formal software verification. The paper tests whether LLMs such as GPT-4 and Claude 3 can auto-generate enough hints for Dafny to verify over 750 programs with about 53,000 lines of code. It reports that the best model and prompting scheme achieved a 68% success rate.

Why this matters:

1. It turns “LLMs might help formal verification” into a measurable task.
2. It focuses on verification hints, not just code generation.
3. It shows success depends on program size, number of hints, and using error feedback.
4. It gives later tools a benchmark to beat.

DafnyBench also names the adoption problem honestly. Formal verification can provide rigorous mathematical proof that software meets a specification, but it is costly and has a learning curve. The premise is that AI can reduce the friction enough to make formal verification more widely usable.

For coding-agent users, DafnyBench is evidence that the agent can be useful as an assistant to the verifier, not as a replacement for it.

## dafny-annotator: search plus LLM proposals

[dafny-annotator](https://arxiv.org/html/2411.15143v1) is a tool that adds logical annotations to a Dafny method until the verifier can prove it correct. Its core loop is wonderfully agentic:

```text
Given a method and spec
  ask LLM for candidate annotations
  try inserting each candidate at valid locations
  run Dafny
  keep the first accepted annotation
  repeat until verified or out of trials
```

The paper reports that base LLaMA 3.1 8B with greedy search succeeded on only 15.7% of methods from a DafnyBench test set. After creating synthetic data (DafnySynth) and fine-tuning on DafnyBench plus DafnySynth, success improved to about 50.6%.

The interesting lesson is not only the number. It is the recipe:

- make the LLM’s job smaller,
- let search try insertion locations,
- let Dafny validate candidates,
- generate synthetic verified examples because the ecosystem has little training data.

This is a pattern coding-agent builders can steal. If the LLM struggles with a big task, move deterministic pieces out of the prompt and into the harness. Do not ask the model to know the exact insertion point if a programmatic search can try all valid points.

The [Dafny blog post](https://dafny.org/blog/2025/06/21/dafny-annotator/) gives the same project a more accessible ecosystem framing, while the [GitHub repo](https://github.com/metareflection/dafny-annotator) shows that it is not just a paper idea.

## DafnyPro: prevent cheating, prune noise, reuse proof strategies

[DafnyPro](https://arxiv.org/html/2601.05385v1) is a 2026 step forward. It presents an inference-time framework for generating verification annotations in Dafny. Its three main components are:

1. **Diff-checker** — prevents the model from modifying base program logic.
2. **Pruner** — removes unnecessary invariants.
3. **Hint augmentation** — retrieves and applies predefined, problem-independent proof strategies.

The diff-checker is especially important for coding agents. If the agent is rewarded for “make verification pass,” it may change the code instead of proving the intended code. DafnyPro explicitly guards against that.

The paper reports consistent performance gains across Clover, MBPP-Dafny, HumanEval-Dafny, and DafnyBench. On DafnyBench, it reports Claude Sonnet 3.5 enhanced with DafnyPro achieving 86% correct proofs, a 16 percentage point improvement over the base model. It also reports fine-tuned Qwen 7B and 14B models reaching 68% and 70% correct proofs on DafnyBench.

This matters for the “last six months” story because it shows the field moving from simple prompting toward harness engineering:

```text
LLM + verifier feedback
  -> add diff protection
  -> add pruning
  -> add retrieval of proof strategies
  -> distill into smaller models
```

That is exactly how mature coding-agent systems evolve. The raw model is only one component.

## From Natural Language to Verified Code

[From Natural Language to Verified Code](https://arxiv.org/html/2604.22601v1) pushes the loop closer to the user. It studies natural-language problem-to-code generation with Dafny-based verification. The paper introduces NL2VC-60, a dataset of 60 complex algorithmic problems, and evaluates open-weight LLMs with three prompting styles:

- contextless prompts,
- method-signature prompts,
- self-healing prompts with iterative Dafny verifier feedback.

The paper reports that contextless prompting leads to near-universal failure, while structural signatures and self-healing with verifier feedback dramatically improve results. It also integrates uDebug functional validation to avoid vacuous verification, where a model satisfies a weak or trivial spec while not solving the real problem.

That last part is crucial. A formal verifier checks the formal property. If the property is too weak, the code can be verified and useless. Functional tests from uDebug act as a second guard against “proved the wrong thing.”

For coding agents, the lesson is:

```text
Use formal verification and executable tests together.
Formal proof checks the contract.
Tests/examples help catch wrong or weak contracts.
```

## Dafny Autopilot: what a user-facing workflow looks like

The [Dafny Autopilot](https://github.com/Beneficial-AI-Foundation/dafny-autopilot) repository is useful because it looks like a developer tool rather than only a benchmark. Its README describes a VS Code extension that uses models such as GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, or AWS Bedrock to help verify Dafny code.

The features are simple and practical:

- given an incomplete `.dfy` program, use an LLM to fill annotations and verify the result,
- highlight a method/function/predicate/lemma and ask the tool to verify it,
- highlight an annotation and ask for an English explanation,
- configure the path to the Dafny executable and the maximum number of LLM iterations,
- feed Dafny verifier errors back on later attempts.

This is not large-scale production evidence. The repository had modest GitHub traction in the captured metadata. But it shows how formal-methods assistance may enter normal IDE workflows: not as a separate proof lab, but as “right-click, fill annotations, run verifier, inspect diff.”

## What “verified code generation” really means

Be careful with the phrase “verified code generation.” It can mean different levels:

### Level 1: Verified by tests

The agent writes code and tests pass. This is useful but not formal verification.

### Level 2: Verified against weak contracts

The agent writes code and a verifier accepts the contract, but the contract may be too weak. This can create false confidence.

### Level 3: Verified against meaningful human-reviewed contracts

The agent writes code and proof artifacts. The verifier accepts them. The human agrees the spec captures the intended property. This is the useful target.

### Level 4: Verified pipeline from intent to code

The system helps translate natural language into specs, validates those specs, generates code, verifies code, and preserves audit trails. This is the research frontier described by intent formalization and NL2VC-style work.

Most real workflows today are somewhere between levels 2 and 3. The danger is marketing level 2 as level 4.

## How to use Dafny with a coding agent today

A cautious starter workflow:

1. Pick a small algorithmic or policy-critical function.
2. Write the English requirement.
3. Ask the agent to draft Dafny-style preconditions and postconditions.
4. Review examples manually: do the specs match your intent?
5. Ask the agent to implement or annotate.
6. Run Dafny.
7. Feed errors back to the agent.
8. Reject any repair that weakens the spec or changes protected logic without explanation.
9. Keep the final verified artifact and verifier output in the audit trail.

This is not for every CRUD endpoint. It is for code where a bug is expensive: authorization, money movement, cryptography-adjacent logic, concurrency, safety checks, protocol code, transformations, and core invariants.

## The deeper lesson for all coding agents

Dafny teaches a general harness-design lesson:

```text
Make the agent's success condition external, mechanical, and hard to fake.
```

Then add guardrails against the agent gaming that condition:

```text
protect the code it must not edit
protect the spec it must not weaken
combine proof with tests/examples
log every verifier failure and repair
ask humans to approve meaning, not just green checks
```

That is why Dafny is not just a formal-methods language in this guide. It is a worked example of how coding agents become safer when their loop is structured around independent verification.
