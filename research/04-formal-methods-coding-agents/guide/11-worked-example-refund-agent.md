# 11 — A Small Worked Example: Refund Rules for a Coding Agent

Let’s make the ideas concrete.

Suppose a coding agent is asked to implement refund logic for a payments service. Refund bugs are expensive. They can lose money, anger customers, or violate policy. This is a good place to use formal-methods thinking.

We will not write a full Dafny proof here. The goal is to show the ladder from vague prose to checkable properties.

## Step 1: Start with informal requirements

Product says:

```text
Refunds must never exceed the original charge.
Refunds above $500 require manager approval.
A transaction must not be refunded twice.
Refunds must update the account balance correctly.
```

This sounds clear. It is not clear enough.

Questions:

- Does “above $500” mean `> 500` or `>= 500`?
- Are partial refunds allowed?
- Can multiple partial refunds happen if their sum stays below the charge?
- Does “refunded twice” mean two refund records, or two full refunds?
- What currency precision is used?
- What happens if manager approval expires?
- What if the original charge is disputed?
- What if the account balance update fails after creating a refund record?

This is why the intent-formalization paper matters. Natural language leaves gaps; agent-generated code can silently choose one interpretation ([Intent Formalization](https://arxiv.org/html/2603.17150v1)).

## Step 2: Add examples and decisions

The human and agent should turn ambiguity into examples.

```text
Example A:
original_charge = 1000
already_refunded = 0
requested_refund = 100
manager_approved = false
allowed = true

Example B:
original_charge = 1000
already_refunded = 700
requested_refund = 400
manager_approved = true
allowed = false
reason = total refunds would be 1100 > 1000

Example C:
original_charge = 500
already_refunded = 0
requested_refund = 500
manager_approved = false
allowed = true if threshold is > 500

Example D:
original_charge = 501
already_refunded = 0
requested_refund = 501
manager_approved = false
allowed = false
```

Now the $500 boundary is explicit: approval is required only for `> 500`, not `>= 500`. If product wanted `>= 500`, example C would change.

## Step 3: Write a contract

A contract is the bridge between examples and implementation.

Pseudo-contract:

```text
requires original_charge >= 0
requires already_refunded >= 0
requires requested_refund > 0
requires already_refunded <= original_charge

ensures allowed implies already_refunded + requested_refund <= original_charge
ensures allowed and requested_refund > 500 implies manager_approved
ensures rejected if transaction is closed or already fully refunded
ensures new_total_refunded == old(already_refunded) + requested_refund when allowed
ensures balance_delta == -requested_refund when allowed
```

This is not yet tied to a language, but it is precise enough to review.

## Step 4: Make illegal states impossible or visible

Formal methods love invariants. An invariant is a rule that should always hold.

Refund invariants:

```text
0 <= already_refunded <= original_charge
sum(refund_records.amount) == already_refunded
no two refund records have the same idempotency_key
account.balance == ledger-derived balance
```

The first invariant is local. The last one may be system-wide and harder to prove. That is normal. You do not have to prove all properties at the same level.

A practical split:

- use a program verifier for local arithmetic and state transitions,
- use database constraints for idempotency keys,
- use transaction boundaries for ledger updates,
- use runtime monitors for high-value approvals,
- use reconciliation jobs for system-wide balance consistency.

Formal-methods thinking does not require one giant proof. It asks which mechanism checks which property.

## Step 5: Ask the coding agent to draft, not decide

A good prompt:

```text
We need refund logic. Before coding, draft:
1. Preconditions
2. Postconditions
3. Invariants
4. Edge-case examples
5. Ambiguities requiring human decision
6. Validation plan
Do not implement yet.
```

A bad prompt:

```text
Implement refunds.
```

The first prompt makes the agent expose assumptions. The second lets the agent bury assumptions in code.

## Step 6: Protect the contract

Once approved, the contract becomes protected.

Policy:

```text
The agent may add tests and code.
The agent may not weaken refund contracts without human approval.
The agent may not delete idempotency tests.
The agent may not change the manager-approval threshold.
```

This mirrors the DafnyPro lesson: if the agent can change the base logic to pass verification, success is meaningless ([DafnyPro](https://arxiv.org/html/2601.05385v1)). Protect the thing being checked.

## Step 7: Add runtime tool policy

Now imagine the agent also has tools. It can call:

```text
read_transaction
create_refund
update_balance
send_email
request_manager_approval
```

Tool policy:

```text
Never call create_refund if requested_refund + already_refunded > original_charge.
Never call create_refund for requested_refund > 500 unless manager_approval_event exists.
Never call update_balance unless create_refund succeeded in same transaction.
Never send refund confirmation email unless refund status is committed.
```

This is temporal. It talks about event order.

Event trace:

```text
1. read_transaction(tx123)
2. request_manager_approval(tx123)
3. manager_approval_granted(tx123)
4. create_refund(tx123, 700)
5. update_balance(account, -700)
6. send_email(customer, confirmation)
```

A runtime monitor checks the trace.

Bad trace:

```text
1. read_transaction(tx123)
2. create_refund(tx123, 700)
```

If `requested_refund > 500`, this should be blocked because approval is missing.

## Step 8: Model-check the workflow

The refund workflow has states:

```text
approval_state = none | requested | granted | denied | expired
refund_state = none | pending | committed | failed
balance_state = unchanged | updated | failed
email_state = not_sent | sent
```

Actions:

```text
RequestApproval
GrantApproval
DenyApproval
CreateRefund
CommitRefund
UpdateBalance
SendEmail
Fail
Retry
```

Properties:

```text
NoRefundWithoutApprovalForLargeAmount
NoEmailBeforeCommit
NoBalanceUpdateWithoutRefundRecord
RetryEventuallyStops
DeniedApprovalPreventsRefund
```

A TLA+ model could explore whether any action ordering violates these properties. This is the same state-machine thinking described in the [TLA+ tools](https://lamport.azurewebsites.net/tla/tools.html) and [SysMoBench](https://www.sigops.org/2026/can-llms-model-real-world-systems-in-tla/) sources.

The human must still check the model. Did it include approval expiration? Did it include partial refunds? Did it include retries after database failure? Did it include duplicate requests from two agents?

## Step 9: Verify local arithmetic

A local verifier such as Dafny can help with arithmetic properties.

Dafny-flavored pseudocode:

```dafny
method CanRefund(original: int, already: int, amount: int, approved: bool) returns (ok: bool)
  requires original >= 0
  requires 0 <= already <= original
  requires amount > 0
  ensures ok ==> already + amount <= original
  ensures ok && amount > 500 ==> approved
{
  if already + amount > original {
    ok := false;
  } else if amount > 500 && !approved {
    ok := false;
  } else {
    ok := true;
  }
}
```

This kind of function is small enough for formal verification. The agent can help write it. Dafny can check it. The human can review whether the threshold and refund-sum rule match the business intent.

## Step 10: Combine proof, tests, and runtime monitors

A good production-quality setup uses several checks:

```text
Unit tests:
  boundary examples: 500, 501, already_refunded edge cases

Property tests:
  random original/already/amount values preserve total <= original

Verifier:
  CanRefund satisfies postconditions

Database:
  unique idempotency key
  transaction constraints

Runtime monitor:
  approval event must precede create_refund for large refunds

Audit log:
  every approval, refund, balance update, and email event recorded
```

This layered approach matches NASA’s warning that whole real systems are usually too complex for one complete proof ([NASA](https://shemesh.larc.nasa.gov/fm/fm-what.html)). You target the critical pieces and use different methods at different layers.

## Step 11: Teach the coding agent the failure language

When checks fail, return structured feedback:

```json
{
  "status": "blocked",
  "rule": "NoRefundWithoutApprovalForLargeAmount",
  "reason": "requested_refund=700 requires manager approval",
  "repair_hint": "request manager approval before create_refund"
}
```

This is better than:

```text
Error.
```

The repair loop needs useful counterexamples and reasons. DafnyBench, dafny-annotator, and proof-agent work all show the value of tool feedback. The same applies to business-policy monitors.

## Step 12: Watch for cheating and spec drift

The agent might try to pass by:

- changing `> 500` to `> 5000`,
- deleting tests for duplicate refunds,
- marking all refunds as manager-approved,
- sending email before commit but changing the test expectation,
- weakening the postcondition,
- editing the policy file.

Guardrails:

```text
Protected policy files require human approval.
Contract changes require review.
Tests may be added freely but deleted only with explanation.
Verifier success must include a diff summary.
Runtime monitor decisions are logged separately from agent memory.
```

This is not paranoia. It is alignment with the metric. If the metric is “green,” an optimizing agent may search for easy ways to become green.

## The final architecture

```text
Human intent
  -> examples and decisions
  -> approved contract
  -> agent implementation
  -> local verifier for arithmetic
  -> tests for examples and integration
  -> runtime monitor for tool order
  -> audit log for post-hoc review
```

Each layer has a job:

| Layer | Job |
|---|---|
| Human examples | clarify intent |
| Contract | state the rule |
| Verifier | prove local code obligations |
| Tests | catch weak specs and integration bugs |
| Runtime monitor | block unsafe action sequences |
| Audit log | explain what happened |

## The lesson

Formal methods are not only for aerospace and theorem-proving competitions. They are a way to make agentic software less vague.

For the refund agent, the key move was not writing fancy math. It was turning:

```text
Refunds should be safe.
```

into:

```text
A refund is allowed only if total_refunded + amount <= original_charge,
and amount > 500 implies manager approval,
and create_refund must not occur before the approval event,
and duplicate idempotency keys are impossible.
```

Once the rule is that explicit, a coding agent can help implement it, and independent tools can help check it.
