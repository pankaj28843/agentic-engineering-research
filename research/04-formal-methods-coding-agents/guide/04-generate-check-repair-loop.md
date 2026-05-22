# 04 — The Generate-Check-Repair Loop

The most important pattern in this whole theme is simple enough to fit on a napkin:

```text
LLM generates candidate
checker rejects or accepts
LLM repairs using checker feedback
repeat until accepted or stop
```

This pattern is powerful because the two sides have opposite personalities.

The LLM is imaginative. It can guess invariants, write proof sketches, translate prose, search for lemmas, and try many code variants.

The checker is stubborn. It does not care whether the explanation sounds confident. It accepts only artifacts that satisfy its rules.

Together they form a useful loop. The LLM expands the search. The formal tool prunes the search.

## Why this is different from “AI writes tests”

A coding agent can write tests too. That is useful, but tests written by the same agent can share the same misunderstanding. If the agent thinks “remove duplicates” means “keep one copy,” it may write tests for that behavior and pass them.

A formal checker does not solve the intent problem by itself, but it makes the property explicit and hard to ignore. If the property says “the result contains no element that appeared more than once in the input,” the agent cannot pass by implementing the other meaning.

The loop therefore has two review points:

```text
Human reviews: does the spec mean the right thing?
Checker reviews: does the artifact satisfy the spec?
```

Both are necessary. The human guards meaning. The checker guards logic.

## The loop in Dafny

Dafny makes the loop concrete:

```text
1. Start with a Dafny method and desired specification.
2. LLM proposes annotations: assertions, invariants, decreases clauses, lemmas.
3. Dafny verifier checks the program.
4. If verification fails, Dafny returns errors.
5. LLM uses the errors to propose different annotations.
6. Stop when verified, timed out, or human intervenes.
```

[DafnyBench](https://arxiv.org/html/2406.08467v1) measured this kind of work at benchmark scale. It tests whether LLMs can generate enough hints for the Dafny verifier to verify more than 750 programs with about 53,000 lines of code. The paper reports that the best model and prompting scheme achieved a 68% success rate, and it measures how retrying with error-message feedback changes performance.

That last part is the agentic piece. The verifier’s error is not just a failure. It becomes a tool observation for the next attempt.

[dafny-annotator](https://arxiv.org/html/2411.15143v1) makes the loop even clearer. It uses an LLM to propose annotations, tries inserting them at valid locations, keeps the first annotation that Dafny accepts, and repeats until verification succeeds or a maximum number of trials is reached. The paper reports that a base LLaMA 3.1 8B guided greedy search succeeded on only 15.7% of held-out methods, while fine-tuning with DafnyBench plus synthetic DafnySynth data increased success to about 50.6%.

The lesson is not “LLMs are now perfect.” The lesson is “verifier feedback gives the LLM a structured way to improve.”

## The loop in theorem proving

Proof assistants give an even stricter version of the same loop:

```text
1. The theorem is stated in Lean or Coq.
2. LLM proposes a tactic or proof fragment.
3. Proof assistant executes/checks it.
4. If it fails, the assistant returns the proof state or error.
5. LLM tries again, maybe with backtracking, memory, or lemma search.
```

[COPRA](https://arxiv.org/html/2310.04353v4) is built around stateful backtracking search. It repeatedly asks a general-purpose LLM for tactic applications, executes them in Lean or Coq, and builds the next prompt from proof-environment feedback, search history, and retrieved lemmas.

[A Minimal Agent for Automated Theorem Proving](https://arxiv.org/html/2602.24273v1) shows why the agent wrapper matters. The paper identifies iterative proof refinement as the biggest factor, with memory preventing the prover from running in circles and library search helping with Lean’s Mathlib context.

That looks familiar to coding-agent users. It is the same pattern as editing code after test failures, except the failure signal is a formal proof state rather than a unit-test assertion.

## The loop in TLA+ modeling

Model checking has its own version:

```text
1. LLM drafts a TLA+ model.
2. SANY checks syntax.
3. TLC or another model checker explores states.
4. Counterexample reveals a broken invariant or impossible transition.
5. LLM repairs the model or the design.
```

The problem is that a model can pass syntax and still describe the wrong system. The SIGOPS/SysMoBench article found that leading LLMs do well on syntax and often runtime execution, but struggle on conformance and invariant phases when generated TLA+ specs are compared against actual implementation traces ([SIGOPS](https://www.sigops.org/2026/can-llms-model-real-world-systems-in-tla/)).

This gives a sharper loop:

```text
LLM drafts model
syntax checker checks grammar
model checker checks internal properties
trace conformance checks model-vs-code alignment
human checks abstraction and intent
```

For coding agents, that is the difference between “write a plausible model of Raft” and “model exactly how this Etcd code updates this field in this action.”

## The loop in runtime enforcement

Runtime verification turns the loop into a gate:

```text
1. Agent proposes a tool call.
2. Monitor abstracts the event.
3. Policy or temporal rule checks the event against history.
4. If allowed, tool call runs.
5. If forbidden, action is blocked or escalated.
6. The block becomes feedback to the agent.
```

Example:

```json
{
  "tool": "shell",
  "command": "git push origin main",
  "tests_passed": false,
  "human_approved": false
}
```

Policy:

```text
Always: git push requires tests_passed and human_approved.
```

Result:

```text
blocked: push requires green tests and approval
```

[GoPlus AgentGuard](https://github.com/GoPlusSecurity/agentguard) implements this kind of practical guard posture for agent environments. Its README describes pre-tool hooks, action evaluation, skill scanning, trust tracking, protection levels, and integrations with Claude Code, Codex, OpenClaw, and Hermes Agent. It is not a full theorem prover. It is a runtime safety layer. That is often exactly what a coding-agent harness needs.

## What makes a good repair loop?

A weak loop says only:

```text
failed
```

A strong loop gives actionable structure:

```text
postcondition might not hold at line 42
counterexample: x = -1
invariant missing: i <= a.Length
policy violation: external_email before approval
trace mismatch: model used set union, code overwrote map entry
```

The stronger the failure signal, the easier it is for the agent to repair.

Good repair loops have five ingredients:

1. **A clear property.** The agent knows what must be true.
2. **A deterministic checker where possible.** Same artifact should usually produce same result.
3. **Structured feedback.** Error messages, counterexamples, proof states, traces, or policy reasons.
4. **A bounded retry budget.** Infinite repair loops are just expensive spinning.
5. **A human escalation path.** Some failures mean the spec is wrong or ambiguous.

## The “cheating” problem

Agents optimize for passing the check. That is both useful and dangerous.

If you tell an agent, “Make the tests pass,” it may delete the failing test. If you tell it, “Make Dafny verify,” it may weaken the specification or subtly change program logic. [DafnyPro](https://arxiv.org/html/2601.05385v1) explicitly addresses this by using a diff-checker to prevent modifications to base program logic. [SEVerA](https://arxiv.org/html/2603.25111v2) also discusses failures where agents cheat by modifying the input program or violating domain policy, and introduces formal output contracts and verified fallbacks.

The lesson for coding agents is practical:

```text
Do not only check the final success flag.
Also check what the agent changed to get success.
```

A safe loop separates artifacts:

- source code the agent may edit,
- source code the agent may not edit,
- specification the agent may draft but human must approve,
- tests the agent may add but not delete without approval,
- verifier result logs,
- final diff.

## The role of humans in the loop

Formal methods can reduce human review burden, but they do not eliminate human judgment. The human’s best role shifts upward:

- not “read every generated line,”
- but “review the property, approve the risk boundary, inspect counterexamples, and decide when the model is too weak.”

This is what the intent-formalization agenda means by validating specifications. There is no oracle for whether the spec captures user intent ([Intent Formalization](https://arxiv.org/html/2603.17150v1)). The verifier can say whether code satisfies a property. The human must still ask whether that property is worth satisfying.

## The napkin architecture

A practical coding-agent formal loop looks like this:

```text
          +-------------------+
          | human requirement |
          +---------+---------+
                    |
                    v
          +-------------------+
          | draft contract    |  <--- LLM helps
          +---------+---------+
                    |
          human approves meaning
                    |
                    v
+---------+-------------------------------+
| coding agent writes code / proof / plan |
+---------+-------------------------------+
                    |
                    v
          +-------------------+
          | formal checker    |
          +---------+---------+
        pass        |        fail
         |          v
         |   counterexample/error
         |          |
         |          v
         |   agent repair attempt
         v
  final artifact + proof/check log
```

That is the central engineering idea of this guide: do not ask the LLM to be trustworthy by itself. Place it inside a loop where untrusted proposals meet trusted checks.
