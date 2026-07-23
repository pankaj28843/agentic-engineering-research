# 41. Operationalize the learn loop without letting failures write policy

> **Report point:** Playbook, bullet 41, pages 11–12 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Playbook judgment:** Failures may propose bounded harness changes; they should not promote themselves. Human review, scenario evaluation, untouched tests, versioning, expiry, and rollback remain required.

A coding agent fails, a human supplies the missing instruction, and the next run succeeds. The obvious temptation is to append that lesson to the shared harness forever. Repeated often, this creates an apparently self-improving system—and a pile of contradictory local memories.

The safe alternative separates observation, proposal, evaluation, and promotion:

```text
failure → classified evidence → bounded proposal → comparative evaluation
        → human decision → canary → expiry or renewal
```

The failure is allowed to nominate a change. It is not allowed to define the lesson, choose the evaluation, and approve itself.

## Plain mental model: a failure is a witness, not a legislator

One failed task can reveal a real missing capability. It can also be a one-off environment outage, a bad task, a stale dependency, a model-specific quirk, an evaluator error, or an adversarial attempt to plant instructions. Turning every failure into policy is like rewriting traffic law from every driver complaint.

The learn loop should answer five questions:

1. What failed, under which exact context?
2. Which failure class and causal evidence support a harness change?
3. What is the smallest reversible proposal?
4. On which affected and unaffected scenarios does it help or harm?
5. Who accepts the maintenance and residual risk?

## Instrument before learning

Capture enough evidence to reproduce the failure without retaining unnecessary secrets or personal content:

- task and risk class;
- repository, model, harness, tool, and environment versions;
- relevant prompt or instruction provenance;
- tool calls, deterministic diagnostics, and exit states;
- evaluator result and raw evidence;
- human intervention, if any;
- retry behavior and cost;
- data-access purpose and redaction;
- whether the trace may be used for learning.

Do not ingest arbitrary issue text, web content, terminal output, or model-written “lessons” into a durable instruction store. Treat all of it as untrusted evidence. Separate control-plane instructions from task content, and require provenance for every proposal.

## Classify before proposing

Use a small taxonomy:

- missing or ambiguous instruction;
- missing tool or permission;
- faulty tool or environment;
- weak or wrong evaluator;
- model reasoning or planning failure;
- stale context or memory;
- task/specification defect;
- transient failure;
- suspected prompt injection or poisoned content;
- unresolved.

Require more than recurrence count. Three similar symptoms can have different causes. Conversely, one high-severity near miss may justify an immediate temporary guardrail. Record causal support, counterexamples, affected scope, and consequence.

The [Fowler/Böckeler harness model](https://martinfowler.com/articles/harness-engineering.html) helps locate proposals: change feed-forward guidance when the agent lacked stable context; change feedback when the system failed to expose a property; change neither when the task or environment was defective. The source is practitioner synthesis, so the taxonomy should organize investigation rather than claim an effect.

## Constrain proposals

Every proposal needs a machine-readable change card:

| Field | Requirement |
|---|---|
| Trigger evidence | Trace IDs and failure classification |
| Hypothesis | Why this change should alter the failure |
| Target | Exact instruction, tool, evaluator, memory item, or workflow step |
| Scope | Repositories, task classes, models, and risk tiers |
| Non-goals | Behavior intentionally unaffected |
| Abuse case | How the change could be gamed or poisoned |
| Evaluation | Affected, neighboring, adversarial, and untouched scenarios |
| Budget | Tokens, latency, infrastructure, and human review |
| Owner | Proposer, accountable maintainer, approver |
| Lifecycle | Version, canary, expiry, rollback |

Prefer the smallest change: retrieve a rule only after a diagnostic, add a missing schema field, improve an error message, or create a focused evaluator case. Do not respond to one failure by adding broad autonomy, hidden memory, or a generic “always be careful” instruction.

An agent may draft the card and patch, but a human owner must validate the classification and scope. Security-sensitive proposals require the relevant security or data owner. A proposal derived from untrusted content must show that it cannot move that content into the control plane.

## Maintain four evaluation partitions

1. **Trigger set:** failures that motivated the proposal.
2. **Neighbor set:** similar tasks not used to draft it.
3. **Regression set:** unrelated capabilities likely to be affected by added context, changed tools, or evaluator behavior.
4. **Untouched final set:** hidden from proposal generation and consulted only at a release decision.

Add adversarial cases for instruction conflicts, shortcuts, false diagnostics, malformed outputs, permission denial, and injected “lessons.” Use repeated runs when the model is stochastic. Compare the candidate with the current harness under the same model, effort, tools, and budget.

[*Self-Harness*](https://arxiv.org/html/2606.09498v1) is the strongest bounded empirical example in this packet. On 64 filtered Terminal-Bench tasks, validation-gated harness edits improved reported held-out pass rates for MiniMax, Qwen, and GLM model families. Yet the held-out pass counts were consulted repeatedly during candidate promotion, making that split adaptively reused rather than an untouched final test. Candidate-search cost, failed proposals, long-run regression, production safety, and maintenance were not measured. The study supports bounded, validation-gated change and model specificity; it does not prove safe autonomous self-improvement.

## Promotion is a governed decision

Require all of these before canary:

- trigger improvement is reproducible;
- neighbor performance improves or stays within its declared floor;
- regression and adversarial sets do not show material harm;
- the untouched final set meets the release threshold;
- no new privilege or data use appears without approval;
- total work, not only pass rate, stays within budget;
- an owner accepts support and expiry.

Version every promoted artifact immutably. Record its parent, evidence card, supported models, tool dependencies, and rollback target. Sign or otherwise protect the release record where tampering matters.

Canary by repository, task class, or small traffic share. Compare failures, refusals, latency, cost, overrides, and incidents with the previous version. Never canary a permission expansion as though it were mere prompt text.

## Protect against one-offs and poisoned lessons

Use several controls:

- minimum recurrence or severity rationale;
- independent human classification;
- deduplication by cause rather than wording;
- allowlisted proposal targets;
- no direct writes from task content to shared instructions;
- negative tests showing that malicious text cannot promote policy;
- least-privilege access for the proposer;
- immutable provenance and review logs;
- expiry unless renewed with evidence.

The [Verification Horizon](https://arxiv.org/html/2606.26300v1) shows why the evaluator itself belongs inside the risk boundary. Monitors suppressed known shortcut behaviors in bounded experiments, but “clean” meant that predefined triggers were absent; evaluator ranking and agreement changed with model, prompt, and metric. An agent can optimize the visible proxy while the real failure moves elsewhere. Rotate hidden faults, review evaluator disagreements, and never let a single learned judge authorize its own updates.

## Metrics that expose total work

Track:

- trigger, neighbor, regression, adversarial, and final-set outcomes;
- unique failure classes resolved and newly introduced;
- false proposals and rejected proposals;
- candidate-search and evaluation compute;
- human classification, review, and maintenance time;
- tokens, calls, latency, and retries per successful task;
- instruction/context size and retrieval precision;
- overrides, rollbacks, incidents, and expired artifacts;
- performance by model and repository, not only aggregate;
- time from observed failure to safe promotion.

Use a cost ledger that includes failed candidates. Reporting only the winning patch makes search look free.

## Stop conditions and rollback

Stop automatic proposal generation if suspected poisoned content reaches cards, provenance is incomplete, the final set has been exposed, owners cannot reproduce decisions, or rejected proposals consume more than the agreed budget without new failure coverage. Freeze promotion if evaluator changes and harness changes are bundled; change one decision surface at a time.

Roll back when canary correctness, severe-risk coverage, refusal behavior, latency, or cost crosses its envelope. Repoint users to the pinned prior version, revoke any new credential or tool grant, quarantine memories added by the candidate, and preserve traces for analysis. Do not “fix forward” repeatedly while exposure continues.

Every promoted change receives a review-by date. Re-run the comparison after major model or tool upgrades. [*Stop Overengineering Your Agent Harness*](https://www.oreilly.com/radar/stop-overengineering-your-agent-harness/) advances the practitioner counter-hypothesis that harness features can expire as models improve. It has no controlled result, but the operational implication is testable: periodically compare the feature with its absence and delete it when marginal value disappears.

## What survives skeptical review

Validation-gated harness adaptation has bounded benchmark support. The selected evidence does not establish untouched generalization, production safety, long-run stability, or a positive total-cost return. Weak evaluators, adaptive reuse, poisoned inputs, and accumulating instructions are live failure modes.

A credible learn loop is therefore conservative: instrument failures, classify them, constrain proposals, evaluate against several partitions, retain an untouched release test, require accountable human promotion, canary, version, expire, and roll back. The system learns only when the organization can also forget.

Podcast hook: The agent turns yesterday’s failure into tomorrow’s policy—and quietly learns the attacker’s instruction along with it.

Continue reading: [Chapter 42, “Govern and prune shared skills”](42-govern-prune-shared-skills.md), applies the learn loop to reusable capabilities that cross team and model boundaries.
