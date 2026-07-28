# 10. Function calling and tool contracts

A model does not call your function. It emits a proposal—tool name plus
arguments—which the host application may validate, authorize, execute,
observe, and return to the model.

This distinction is the security and reliability boundary:

> model output is intent; trusted application code owns effects.

## ELI5: the model fills out a work order

A building resident can submit “unlock apartment 4B.” A work order with the
right boxes is not itself a door opening. The building system checks the
resident, apartment, time, permission, duplicated request, and current lock
state before acting.

Tool calling is the same. The LLM writes the work order. Your orchestrator is
the access-control system and dispatcher.

## The end-to-end protocol

```text
user/context
  → expose eligible tool contracts
  → model proposes call
  → parse and schema validate
  → resolve canonical resources
  → authorize against caller and current state
  → apply policy/budget/approval
  → execute idempotently with deadline
  → return typed observation
  → model continues or stops
```

Every transition should produce a traceable state and error class.

## A good contract

Suppose an agent can propose a refund:

```json
{
  "name": "propose_refund",
  "arguments": {
    "order_id": "ord_...",
    "amount_minor": 1299,
    "currency": "DKK",
    "reason_code": "duplicate_charge",
    "evidence_ids": ["trace_...", "payment_..."]
  }
}
```

The contract should state:

- this creates a proposal, not a settled payment;
- the caller must be authenticated and scoped to the order tenant;
- amount is integer minor units with an upper bound;
- currency must match the ledger;
- accepted reason codes are enumerated;
- evidence is required;
- retries use a caller-supplied operation ID;
- outcomes include `accepted_for_review`, `denied`, `already_exists`, and
  typed retryable failure.

Names are UX for the model. Make them distinct and action-specific. A vague
`manage_order` tool invites selection and argument ambiguity.

## Tool-choice and argument errors are different

The
[Shishir G. Patil et al., “The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models”](https://proceedings.mlr.press/v267/patil25a.html)
evaluates multiple function-calling settings, including selection and
multi-turn behavior. The
[Shirley Kokane et al., “ToolScan: A Benchmark for Characterizing Errors in Tool-Use LLMs” (arXiv:2411.13547)](https://arxiv.org/html/2411.13547v2)
develops an error taxonomy. Benchmark rankings change with model versions and
datasets; the durable contribution is separating failure classes.

At runtime distinguish:

- no tool when one is required;
- unnecessary tool;
- wrong tool;
- correct tool with malformed arguments;
- correct schema but wrong entity/value;
- wrong ordering or missing dependency;
- repeated non-idempotent call;
- failure to react to the observation;
- fabricated success without execution.

A global “tool-call success rate” cannot direct a fix.

## Expose less, retrieve more

Hundreds of tool descriptions consume context and create confusing
near-duplicates. A registry can expose a small initial discovery surface, then
load detailed contracts for an eligible subset.

[Anthropic, “Introducing advanced tool use on the Claude Developer Platform”](https://www.anthropic.com/engineering/advanced-tool-use)
describes tool search, programmatic calling, and example-based guidance. These
are current provider features and token-efficiency claims, not universal
protocol semantics. Whatever discovery mechanism is used, authorization must
filter the candidate set before a tool becomes callable.

Do not let an untrusted document register a new privileged tool.

## Validation has layers

1. **Transport:** complete response, expected tool-call envelope.
2. **Schema:** types, required fields, enums, bounds.
3. **Canonicalization:** IDs resolve; units and dates normalize.
4. **Referential integrity:** resources belong to the same tenant/workflow.
5. **Business invariant:** state transition is legal.
6. **Authorization:** the initiating principal has this permission now.
7. **Consequence policy:** approval, rate, budget, and risk gates pass.

The model should not provide trusted `tenant_id`, `role`, price, or approval.
Derive those from authenticated server state.

## Idempotency and ambiguous outcomes

Tools meet unreliable networks. A timeout can mean “nothing happened” or “the
effect succeeded and the reply was lost.”

For a mutating operation:

- create a stable idempotency key before the first attempt;
- persist operation state;
- reuse the same key on retry;
- expose a status query;
- distinguish retryable transport errors from permanent domain rejection;
- never tell the model to invent a fresh key after uncertainty.

If the operation cannot be made idempotent, require reconciliation or human
approval rather than automatic retry.

## Typed observations

Return compact structured results:

```json
{
  "status": "already_exists",
  "proposal_id": "refund_42",
  "canonical_order_id": "ord_7",
  "next_allowed_actions": ["inspect_proposal", "finish"],
  "retryable": false
}
```

Do not return a 20,000-line stack trace as the only observation. Keep the raw
artifact behind a reference and provide an error class, relevant fields, and
safe next actions.

Tool output is untrusted when it contains web pages, email, repository text, or
third-party data. Delimit it as data and prevent it from rewriting system
policy.

## Recovery without “retry until lucky”

A self-healing orchestrator may choose a new tool, correct arguments, or
compensate after failure. The recent preprint
[Rahul Suresh Babu and Adarsh Agrawal, “Self-Healing Agentic Orchestrators for Reliable Tool-Augmented Large Language Model Systems” (arXiv:2606.01416)](https://arxiv.org/html/2606.01416v1)
explores that direction. It should not be read as permission for unconstrained
autonomy. Recovery must preserve authorization, idempotency, budgets,
lineage, and terminal conditions.

A useful policy table is deterministic:

| Error | Automatic response |
| --- | --- |
| Schema violation | One corrected proposal with validation errors |
| Rate limit | Bounded backoff within deadline |
| Permanent domain denial | Surface denial; do not retry |
| Ambiguous mutation | Query operation state or reconcile |
| Authorization denied | Stop and audit metadata-safely; never request approval |
| Approval required after authorization | Persist the exact proposal and wait; reauthorize at commit |
| Unknown tool | Refresh eligible registry once, then stop |

## Worked example: deployment tool

Do not expose `shell(command)` and hope the prompt says “production is
important.” Expose:

```text
plan_deployment(service, artifact_digest, environment)
run_preflight(plan_id)
request_approval(plan_id)
execute_deployment(approved_plan_id, idempotency_key)
observe_rollout(plan_id)
rollback(plan_id, reason, idempotency_key)
```

The server resolves environment policy, verifies artifact signatures, checks
ownership, and controls credentials. The model coordinates a state machine;
it never receives a general production shell or signs its own approval.

## Interview checkpoint

**Question:** “How do you make LLM function calling reliable?”

A strong answer treats the model call as an untrusted proposal. It discusses
narrow contracts, eligible-tool discovery, schema and semantic validation,
server-derived identity, authorization, idempotency, typed outcomes, deadlines,
retries by error class, observability, evals, and human approval for
high-consequence effects.

**Explain it back:** Why is `strict: true` useful but insufficient for
`transfer_money`?

## Capstone increment

Define one tenant-scoped `read_document(canonical_document_id, version)` tool
and one reversible `update_document_metadata(...)` tool. Include server-derived
identity, canonical IDs, authorization, preconditions, idempotency, deadline,
typed observations, audit fields, and reconciliation for an ambiguous write.
Resolve both tools from a trusted registry, pin server identity and the approved
schema digest, and classify returned fields as untrusted data rather than
instructions. Reuse Chapter 9's recovery/result states rather than inventing
prose errors.

**Definition of done:** a duplicate write is harmless, an unknown outcome is
reconciled before retry, an unregistered or digest-changed tool cannot execute,
and neither tool can act on a document merely because the model supplied its
ID.

Next: [Agent budgets and termination](11-agent-budgets-and-termination.md)
adds liveness and resource contracts around repeated model/tool turns.
