# 02 — Why Coding Agents Make This Urgent

Coding agents change the economics of software. They can produce more code, more quickly, with less typing from the human. That is useful. It is also dangerous, because the bottleneck moves from **writing** code to **knowing whether the code matches the intention**.

A normal developer can misunderstand a requirement. A coding agent can misunderstand it at machine speed, then confidently edit ten files, add tests that match its misunderstanding, and explain itself beautifully. The output may feel professional while being wrong in exactly the way the user did not notice.

This is the “intent gap.” The recent Microsoft/RiSE paper [Intent Formalization: A Grand Challenge for Reliable Coding in the Age of AI Agents](https://arxiv.org/html/2603.17150v1) makes that gap the central problem. Agentic coding tools can plan, write code, run tests, and iterate, but the fundamental question remains: does the generated code actually do what the user intended?

## The simple duplicate example

The intent-formalization paper uses a tiny example that is worth repeating because it is so ordinary.

User says:

```text
Given a list of integers, remove duplicates.
```

Does that mean this?

```text
[1, 2, 3, 2, 4] -> [1, 2, 3, 4]
```

Or this?

```text
[1, 2, 3, 2, 4] -> [1, 3, 4]
```

The first keeps one copy of each value. The second removes every value that appears more than once. Both are reasonable interpretations of the English sentence. A human developer might ask a follow-up question. An LLM may choose the statistically common meaning and move on.

If the coding agent writes tests for its own chosen interpretation, the tests may pass. If it writes documentation for its own chosen interpretation, the docs may look tidy. If it writes code for its own chosen interpretation, the implementation may be internally consistent. But it can still be wrong for the user.

Formal methods do not magically know the user’s meaning. Their value is that they force meaning to become explicit. A contract, property, invariant, or temporal rule makes the ambiguity visible.

## AI makes code abundant; verification becomes the scarce thing

When code was expensive to write, the human naturally spent time thinking through each step. When code becomes cheap, more wrong code can exist. This does not mean coding agents are bad. It means the verification budget must grow.

A useful slogan for agentic engineering is:

```text
When generation gets cheaper, checking gets more important.
```

The [DafnyBench](https://arxiv.org/html/2406.08467v1) paper says formal verification can provide rigorous mathematical proof that software meets a specification, but also notes the traditional cost problem: formally verifying code can take far more human work than writing it. LLMs attack exactly that cost. They can draft annotations, invariants, lemmas, and proof hints. The formal tool then rejects bad drafts.

This is the complementary-strength story:

| LLM strength | Formal-methods strength |
|---|---|
| Generate candidate code quickly | Reject code that violates a property |
| Translate prose into candidate specs | Check logical consistency or expose counterexamples |
| Suggest proof tactics or invariants | Accept only mechanically valid proof steps |
| Explore many variants | Search state space or solve constraints precisely |
| Repair after feedback | Produce stable errors/counterexamples as feedback |

The important word is **candidate**. The LLM produces candidates. The verifier decides whether the candidate satisfies the check.

## Why ordinary tests are not enough for agents

Tests are still essential. Do not throw them away. Most real projects should add better tests before they add heavy formal methods.

But agents create several failure modes that tests alone often miss:

1. **Ambiguous intent.** The test suite may encode the agent’s interpretation, not the user’s intention.
2. **Too many paths.** Agents can call tools in many orders. You cannot write one example test for every possible sequence.
3. **Stateful workflows.** An agent can read memory, write memory, call a tool, retry, ask another agent, and continue. Bugs live in the sequence.
4. **Policy boundaries.** A test might show the happy path works, but not prove the agent can never call `deploy` before approval.
5. **Security and privacy.** Data can flow through tool chains in ways the developer did not anticipate.

This is why the newer sources in this theme shift from “verify generated code” to “verify the harness and behavior around the agent.” [AgentRaft](https://arxiv.org/html/2603.07557v1) studies data over-exposure across LLM agent tools using function-call graphs and runtime taint tracking. [AgentGuard](https://arxiv.org/html/2509.23864v1) proposes runtime verification of agent behavior through event abstraction, online learning, and probabilistic model checking. [SEVerA](https://arxiv.org/html/2603.25111v2) treats agentic code generation as constrained learning with hard formal specifications.

These are not ordinary unit-test stories. They are control-boundary stories.

## The LLM is not the part you usually verify

A common beginner mistake is to ask, “Can we formally verify the LLM?” For a frontier model, that is mostly not the practical path. The model is enormous, stochastic, and opaque. Some research verifies narrow neural-network properties, but that does not scale to “the whole LLM will always be safe.”

The practical path is to verify or constrain the system **around** the LLM:

```text
+-------------------+
| user requirement  |
+---------+---------+
          |
          v
+-------------------+       +-------------------+
| LLM planner/coder | ----> | proposed artifact |
+-------------------+       +-------------------+
          |                           |
          |                           v
          |                 +-------------------+
          |                 | checker / monitor |
          |                 +-------------------+
          |                           |
          +<------ errors / counterexamples ----+
```

The LLM can remain nondeterministic. The harness can still enforce deterministic rules:

- do not run destructive shell commands without approval,
- do not write outside the repository,
- do not deploy unless CI passed,
- do not send secrets to the browser,
- do not mark a proof complete unless Lean/Dafny accepts it,
- do not accept a TLA+ spec merely because it compiles.

That last rule matters. The 2026 SIGOPS article [Can LLMs model real-world systems in TLA+?](https://www.sigops.org/2026/can-llms-model-real-world-systems-in-tla/) found that leading LLMs often produce syntactically valid TLA+ specs, but conformance and invariant checks reveal that the specs can model a textbook protocol rather than the actual implementation. The article’s Etcd/Raft example is the core lesson: a generated spec can look polished and still not describe the system you care about.

## Why “specification” is the bottleneck

Formal verification begins after someone says what should be true. That “someone” may be a human, an LLM, a DSL, a set of tests, or a mined property. But the property must exist.

The intent-formalization agenda argues that the new bottleneck is validating specifications. There is no perfect oracle that tells us whether a formal spec captures the user’s real intent ([paper](https://arxiv.org/html/2603.17150v1), [RiSE blog](https://risemsr.github.io/blog/2026-03-05-shuvendu-intent-formalization/)). A proof can show code matches the spec, but it cannot show the spec matches the unstated wish in the user’s head.

That is why the best coding-agent workflows keep humans at the spec boundary. The agent can draft a contract, but the human should read the examples and ask:

- Is this property too weak?
- Is it too strong?
- Did it miss edge cases?
- Is it proving the implementation instead of the intention?
- Could the agent satisfy this property by cheating?

A verifier can be stricter than a human about logic. A human still has to be stricter than the machine about meaning.

## Where this leaves normal developers

You do not need to start by proving a whole service. Start by formalizing the rules that would be expensive to get wrong.

For a coding agent, those rules are often not deep algorithms. They are operational boundaries:

- where it may write,
- which commands it may run,
- when it must ask approval,
- which files are sensitive,
- which tests must pass,
- what data may flow into which tools,
- how many retries are allowed,
- when the task is considered done.

That is formal-methods thinking even if the first implementation is a policy file and a runtime monitor rather than Lean or Coq.

The path is:

```text
vague safety wish
  -> explicit policy
  -> observable events
  -> checker or monitor
  -> feedback to the agent
  -> audit trail for the human
```

Coding agents make this urgent because they move faster than human review. Formal methods matter because they give the agent a hard boundary it cannot persuade.
