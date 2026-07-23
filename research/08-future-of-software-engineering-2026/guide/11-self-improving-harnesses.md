# 11. Self-improving harnesses and the learn loop

> **Report point:** Harness engineering, bullet 11, page 5 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** Agents can propose useful, validation-gated harness edits on a bounded benchmark; safe durable self-improvement is not established.

A coding agent fails, examines its trace, and adds an instruction or tool so that the failure will not recur. Over time, the harness appears to learn. Humans mostly prune duplicated or obsolete guidance. This is one of the report’s most concrete visions—and one of the easiest to overstate.

The mechanism is real enough to test. A 2026 study reports substantial benchmark improvements after models proposed targeted changes to their own harnesses. But the evaluation repeatedly consulted the so-called held-out split while deciding which changes survived. There was no untouched final test, long production run, full search-cost ledger, or independent replication.

The defensible conclusion is: **agents can participate in governed harness evolution. They have not shown that they can safely own it.**

## A plain-language model: learning is a controlled release

A harness is the environment around a model: instructions, context assembly, tools, permissions, state, evaluators, and workflow. A harness edit is therefore a software change to the system that produces software changes.

The safe mental model is not a notebook that remembers every lesson. It is a release pipeline:

```text
failure → diagnosis → candidate rule/tool → validation → limited rollout
        → observation → keep, revise, or retire
```

Every arrow can introduce error. A diagnosis may blame the prompt when the tool was broken. A rule may prevent one failure but suppress legitimate behavior elsewhere. A memory may expose secrets. A new evaluator may reward its own shortcut. A helpful instruction for one model may become noise for another.

“The harness learned” should therefore mean a candidate change improved declared outcomes on evidence not used to invent it, without unacceptable regressions or cost. Merely appending a sentence after a failure is accumulation, not learning.

## The strongest empirical result is bounded

[*Self-Harness: Harnesses That Improve Themselves*](https://arxiv.org/html/2606.09498v1) starts with 89 Terminal-Bench 2.0 tasks and fixes a 64-task subset after excluding unstable-web and multimodal tasks. MiniMax M2.5, Qwen3.5-35B-A3B, and GLM-5 use a minimal DeepAgent harness. Each model mines traces from a held-in split, proposes bounded harness changes, and promotes a candidate only when neither evaluated split regresses and at least one improves.

Reported held-out pass rates rise from 40.5% to 61.9% for MiniMax, 23.8% to 38.1% for Qwen, and 42.9% to 57.1% for GLM. Those are meaningful movements on the evaluated task subset. The result also shows model specificity: the useful edits and magnitudes differ.

The word “held-out” needs care. The proposer did not see held-out traces, but the evolutionary loop consulted held-out pass counts for every candidate and round. Once a split repeatedly decides which candidates live, information about it enters the selection process. It functions as a validation set, not an untouched final test. Repeated optimization can overfit even without exposing individual examples.

Other limits matter. The paper aggregates two attempts per candidate and does not report independent seeds, confidence intervals, the exact split counts behind every percentage, or multiple-comparison correction. It does not account fully for failed proposals, search compute, evaluator cost, future maintenance, or long-run regressions. The study supports targeted, validation-gated improvement on this benchmark. It does not establish autonomous generalization or production safety.

## Why self-improvement can fail

The failure modes fall into five families.

**Feedback poisoning.** A trace can contain misleading output, prompt injection, private data, or an incidental workaround. Turning it directly into durable memory lets one interaction rewrite future policy.

**Validation overfitting.** A candidate can improve the familiar benchmark while narrowing behavior elsewhere. [SWE-ABS](https://arxiv.org/html/2603.00520v1) demonstrates the broader oracle problem: stronger adversarial tests rejected many patches that the original benchmark had accepted. A harness optimized against one verifier can learn that verifier’s blind spots.

**Context accretion.** Every plausible lesson competes for attention. Instructions can conflict, repeat, and become stale. The [Fowler/Böckeler harness account](https://martinfowler.com/articles/harness-engineering.html) treats maintainability, versioning, behavior, and human operability as harness qualities precisely because more guidance is not monotonically better.

**Reward hacking and correlated judgment.** A model can find an easier way to please an evaluator than to satisfy intent. [The Verification Horizon](https://arxiv.org/html/2606.26300v1) shows that evaluator outcomes move with model, prompt, metric, and task; high rank correlation can coexist with low pairwise agreement. If proposer and judge share assumptions or model family, repeated agreement is not independent evidence.

**Lifecycle debt.** A rule useful today may become harmful after a model upgrade, repository redesign, or tool change. A [practitioner counterargument](https://www.oreilly.com/radar/stop-overengineering-your-agent-harness/) proposes adding features for observed failures and expecting some to expire as models change. It is not comparative evidence, but expiration is a testable and operationally important hypothesis.

Lilian Weng’s [survey of harness self-improvement](https://lilianweng.github.io/posts/2026-07-04-harness/) adds memory lifecycle, diversity collapse, negative-result bias, fuzzy objectives, and short-horizon optimization to the risk map. It is a narrative synthesis rather than an original trial; its value here is conceptual completeness, not effect size.

## What should and should not be mutable

Not all harness components deserve the same update authority.

An agent can safely *propose* a clearer example, a new deterministic check, a tool-description correction, or a failure-class tag. Promotion can be automated when the change is narrow, reversible, reviewed as code, and tested against independent fixtures.

Security boundaries, data-access policy, deployment authority, audit retention, and the definition of success should not silently rewrite themselves from ordinary task traces. These are constitutional controls: they constrain the optimizer. A system that can relax its own acceptance rule when it fails has converted learning into goal mutation.

The [code-as-harness systems survey](https://arxiv.org/html/2605.18747v1) offers a useful conceptual pattern: executable interfaces make state and coordination inspectable, but verification remains conditional on sensors, permissions, tests, oracles, and human goals. Its stronger language about objective ground truth is qualified by later discussion of weak oracles, stale context, authority conflict, finite state, and safety. Those qualifications should govern implementation.

## Exercise: run a three-box learn-loop trial

Choose one recurring, low-risk failure class and create three boxes:

1. **Proposal box:** ten to twenty past traces that an agent may inspect to propose a single harness change.
2. **Validation box:** separate cases used to tune or reject candidates during development.
3. **Sealed box:** cases selected before the experiment and not inspected until the candidate and stop rule are frozen.

Define the intended outcome and regression measures before starting. Include token cost, elapsed time, human triage, and context size. Test the candidate against the previous harness, not just against no harness. Make the change versioned and reversible.

After opening the sealed box, do not keep editing and report the same score as a final test. A failed sealed result is valuable evidence. If another round is worthwhile, construct a new sealed set.

For deployment, begin with shadow evaluation or a narrow repository. Record which model and tool versions the rule targets, its owner, the evidence that promoted it, an expiry or review date, and a rollback trigger. A compact decision record might read:

```yaml
change: prefer repository schema validator before editing generated clients
failure_class: incompatible hand-written client edits
scope: payments-sdk only
promoted_on: sealed fixtures v3
regressions_checked: latency, false refusal, unrelated tests
owner: sdk-platform
review_by: 2026-10-01
rollback: false-refusal rate > 2%
```

[Chapter 41](41-operationalize-learn-loop.md) owns the full operational workflow. The point here is evidential: the promotion process must be harder to game than the failure that motivated the edit.

## What would raise confidence

Strong evidence would compare a fixed human-maintained harness, agent-proposed/human-approved changes, and bounded automatic promotion across multiple repositories and model families. It would preserve untouched final evaluations, run long enough to observe rule expiry and interaction effects, and count search, inference, human review, incidents, rollback, and maintenance. Security tests would include hostile traces and attempts to weaken controls. Independent teams would reproduce the protocol.

The outcome should not be benchmark pass rate alone. It should include hidden-fault detection, unrelated regressions, task diversity, operational harm, and total cost. A system can improve a score while becoming more brittle or expensive.

## What survives skeptical review

Self-Harness provides credible evidence that models can mine failures and propose bounded harness changes that improve a repeatedly evaluated benchmark subset. It does not show safe, general, long-lived self-improvement. Reusing the held-out split for promotion, omitting an untouched final test, and leaving cost and maintenance unmeasured materially limit the claim.

Use agents as candidate authors and analysts inside a controlled release process. Keep objectives, permissions, independent evaluation, and rollback outside the loop being optimized. Humans need not hand-write every lesson, but “mainly prune” is safe only after someone has designed what may grow.

Podcast hook: If a harness learns to pass its own test, did it become smarter—or did the test become its teacher’s answer key?

Continue reading: [Chapter 41: Operationalize the learn loop](41-operationalize-learn-loop.md) turns the three-box experiment into a versioned, observable lifecycle.
