# 11. Agent budgets and termination

An agent is a loop whose next step is selected under uncertainty. Production
systems therefore need two complementary contracts:

- a **safety contract**: what states and actions are allowed;
- a **liveness contract**: how the run reaches success, handoff, or bounded
  failure instead of continuing forever.

Budgets are enforceable liveness and consequence limits, not hints in a system
prompt.

## ELI5: give the explorer supplies and return rules

An explorer receives food for two days, a map boundary, a radio check every
hour, and instructions to return when the goal is found, the weather turns, or
half the supplies are gone.

“Explore until you solve it” is not autonomy; it is abandonment. Agent budgets
play the role of supplies, map, check-ins, and return rules.

Where the analogy breaks: supplies constrain exploration but do not prove that
the explorer chose a correct route. Verification and terminal evidence remain
separate gates.

## The budget vector

Do not reduce the budget to tokens. Track at least:

```text
B = {
  wall_clock,
  model_input_tokens,
  model_output_tokens,
  monetary_cost,
  model_turns,
  tool_calls_by_class,
  concurrent_children,
  external_side_effects,
  retries_by_failure_class
}
```

A run may be under its token allowance and already unsafe because it has sent
too many messages, retried a charge, or held a production lock too long.

[Oracle, “Runtime Budget Guardrails for Agentic AI”](https://blogs.oracle.com/ai-and-datascience/runtime-budget-guardrails-agentic-ai)
translates tokens, time, iterations, and tools into runtime controls. It is
vendor practitioner guidance; use its categories and set limits from your
workflow’s value and consequence.

## A state machine, not `while (!done)`

Define explicit states:

```text
created
  → inspecting
  → acting
  → verifying
  → succeeded
  → failed_recoverable
  → approval_required
  → handed_off
  → cancel_requested
      → cancelling
          → cancelled
  → budget_exhausted
```

Define allowed transitions and the evidence required for terminal success.
The model may propose a transition; orchestration code validates it.

Cancellation is a protocol, not an instant label. `cancel_requested` prevents
new work from starting; `cancelling` propagates the signal and inventories
in-flight work; terminal `cancelled` is allowed only after side effects are
reconciled, compensated, or durably recorded as `unknown` with an owner and
next action. A disconnected client does not prove that provider, worker, or
tool work stopped.

“The assistant said done” is not completion evidence. For a code change,
success may require a clean diff scope, named tests, runtime probe, and no
unresolved high-severity review. For research, it may require source coverage
and citation validation.

## Three stopping layers

### Model-visible instruction

Tell the model the goal, remaining budget, stop conditions, and escalation
path. This improves planning but is not enforcement.

### Orchestrator enforcement

The host atomically decrements budgets, denies calls beyond authority, cancels
deadlines, and creates terminal records. This is the control boundary.

### Infrastructure kill switch

Workers, credentials, queues, and sandbox processes need leases and cleanup if
the orchestrator crashes. External mutations need server-side quotas and
revocation.

## Progress versus motion

A loop can consume budget while alternating among plausible actions. Define a
progress signal appropriate to the task:

- new failing test becomes passing;
- unresolved verifier count decreases;
- required evidence coverage increases;
- search frontier shrinks;
- workflow state advances;
- uncertainty is converted into an explicit question.

Detect cycles using repeated tool/argument signatures, unchanged artifacts,
repeated error classes, or a lack of progress over a bounded window. A
different natural-language rationale does not make an identical API call new
progress.

The terminal-agent preprint
[Nghi D. Q. Bui / OpenDev, “Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned” (arXiv:2603.05344)](https://arxiv.org/html/2603.05344v1)
provides a current systems account of open-ended execution. Use its mechanisms
and failure observations carefully; it is a very recent preprint, not a
universal production study.

## Parent and child budgets

Subagents must inherit a portion of a parent’s limits. If every child receives
the full global budget, fan-out multiplies cost and authority.

```text
parent remaining = parent allocation
                 - reserved child allocations
                 - completed spend
```

Use reservation and reclamation, much like a resource scheduler. Limit depth,
width, and total children. A child can return evidence or a proposal; it should
not silently expand the parent’s external authority.

## Behavioral contracts and invariants

The preprint
[Varun Pratap Bhardwaj, “Agent Behavioral Contracts: Formal Specification and Runtime Enforcement for Reliable Autonomous AI Agents” (arXiv:2602.22302)](https://arxiv.org/html/2602.22302v1)
offers vocabulary for permitted behavior, invariants, and runtime
enforcement. Even without formal verification, write key invariants in a
machine-checkable form:

- a read-only run performs no mutating tool;
- a tenant-scoped run never resolves another tenant’s object;
- at most one irreversible action occurs without renewed approval;
- every external mutation carries an idempotency key;
- success is impossible while a required verifier is unresolved;
- a cancelled or expired run cannot start new work.

Test invariants with fault injection and adversarial model outputs.

## Human approval is a state, not a chat phrase

When approval is required:

1. persist the proposed action, inputs, evidence, consequence, and expiry;
2. bind approval to the authenticated approver and exact proposal digest;
3. stop autonomous mutation while waiting;
4. invalidate approval if material inputs change;
5. execute once with idempotency;
6. record outcome.

“The user seemed to agree earlier” is not an authorization token.

Approval is a **consequence gate after authorization**, not a way to acquire
authority. A valid approval can permit an already-authorized principal to
commit one exact action; it cannot grant a missing tenant role, bypass an
object ACL, or revive a deleted target. If commit-time authorization fails,
stop with `authorization_denied`. Reauthorization is a separate authenticated
policy change, followed by a fresh preview and approval.

The Hacker News discussion
[“Do not let an LLM make decisions or execute business logic”](https://news.ycombinator.com/item?id=43542259)
captures practitioner disagreement about where model judgment belongs. It is
not representative evidence, but it sharpens the boundary: models can propose
or classify; application code owns invariants and authority.

## Worked example: incident-response agent

Give the agent:

- 20 minutes wall-clock;
- read-only observability by default;
- bounded log-query and model-token quotas;
- one isolated diagnostic command class;
- no production mutation without an exact approval;
- success evidence: root-cause hypothesis plus supporting traces and a
  reversible mitigation plan;
- stop on containment, contradictory evidence, approval wait, no progress
  across three hypotheses, or budget floor needed for handoff.

Reserve part of the time and tokens for the final handoff. Otherwise the run
can exhaust everything investigating and leave no coherent record.

## Budget exhaustion is a designed outcome

Return:

- what was attempted;
- evidence gathered;
- current hypothesis and uncertainty;
- side effects already performed;
- budgets consumed and remaining;
- why the stop condition fired;
- smallest safe next action.

Do not label exhaustion “agent failure” if the budget protected the system as
designed.

## Interview checkpoint

**Question:** “How do you prevent an autonomous agent from running forever?”

A strong answer defines an orchestrator-enforced budget vector, explicit state
machine and terminal evidence, cycle/no-progress detection, nested child
allocations, deadlines/cancellation, side-effect limits, approvals, and a
useful exhaustion handoff. A `max_iterations` prompt alone is insufficient.

**Explain it back:** Why should the run reserve budget for verification and
handoff before it begins exploring?

## Capstone increment

Instantiate the assistant's run state machine and budget vector. Allocate
calls, input/output tokens, elapsed time, spend, retrieval attempts, read/write
tool calls, retries by class, side effects, and explicit reserves for evidence
verification and handoff. Map exhaustion, denial, partial evidence, ambiguous
write, and success to the typed states from Chapters 9–10.

**Definition of done:** every loop transition consumes a named budget or proves
progress, forced exhaustion produces a useful non-success terminal record, and
a forced cancellation cannot become terminal while an in-flight effect is
unaccounted for.

Next: [Routing, fallback, and degraded UX](12-routing-fallback-and-degraded-ux.md)
shows how a system selects a lane and remains honest when the preferred lane
fails.
