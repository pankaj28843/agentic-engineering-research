# 1. The Restaurant With Several Kitchens

## ELI5 hook

Imagine a restaurant with four kitchens. One makes salads quickly, one makes
ordinary meals, one handles difficult allergy-safe dishes, and one does not
cook at all: it answers whether a table reservation exists. A good manager
does not send every order to the cheapest kitchen. First the manager checks
whether the kitchen can safely handle the ingredients, the deadline, and the
kind of meal. Then the manager chooses among the safe kitchens. Finally someone
checks that the order is complete before it is called a success.

LLM routing is that manager. A model is one kitchen. A route is the whole
qualified path: the model or deterministic handler, the context it may see,
the tools it may propose, the provider and region, the budget, the retry and
fallback rules, the validator, and the definition of an accepted outcome. The
same model name can appear in two different routes with different data
boundaries or service guarantees. “Use model X” is therefore an incomplete
operating decision.

The durable question is not “which model is smartest?” It is “which eligible
path can produce an accepted result for this request at the required risk,
latency, and total cost?”

## Mechanism: envelope, eligibility, choice, outcome

Start every request with a canonical envelope. It should contain an
authenticated tenant and actor, request and idempotency IDs, workload class,
consequence level, sensitivity and residency class, context size, tool and
schema requirements, deadline, budget, and acceptance test. Some fields come
from the request; others come from trusted systems. A prompt must never be
allowed to invent identity or consequence.

The router then performs four different jobs:

1. **Eligibility:** deterministic policy removes routes that cannot handle the
   data, authority, tool, schema, region, budget, or consequence. These are
   hard constraints. If a route is outside the allowed set, its low price does
   not matter.
2. **Choice:** among the remaining route enums, a rule, classifier, predictor,
   or bounded policy can optimize quality, latency, capacity, and cost. This is
   a soft decision only within the envelope.
3. **Execution:** the selected worker receives a versioned prompt envelope and
   returns a typed answer or a proposal. A worker does not receive broader
   authority because a router selected it.
4. **Acceptance:** deterministic checks, independent evaluation where needed,
   and human approval for consequential effects decide whether the result is
   accepted. A fluent response that fails its contract is a failed attempt.

The path can be sketched as:

```text
request → canonical envelope → eligible routes → chosen route
       → worker/tool proposal → validation/approval → accepted outcome
```

This separates three prices that are often confused. The **cheapest token** is
the provider's marginal unit price under its current terms. The **cheapest
attempt** is the route's cost before repairing, retrying, escalating, or
reviewing. The **cheapest accepted outcome** includes every part of the path
and divides by results that passed the acceptance contract. Only the last
measure answers whether a policy helps the business.

The routing literature gives useful bounded examples. [FrugalGPT](https://arxiv.org/html/2305.05176)
describes prompt adaptation, model approximation, and cascades under a cost or
quality objective. [RouteLLM](https://arxiv.org/html/2406.18665) frames routing
as choosing between model endpoints using preference data and evaluates that
choice on stated benchmark settings. Those papers make the mechanism concrete;
they do not prove that a router trained or measured elsewhere will generalize
to an enterprise workload.

## Worked example: twelve requests, four lanes

The following numbers are **illustrative assumptions** for learning. A generic
enterprise receives twelve help-desk requests in one hour. Three are factual
questions covered by a versioned internal FAQ. Four ask for a short summary of
an already-approved document. Three ask for a policy interpretation with
uncertain evidence. Two propose changing account state.

| Requests | First eligibility decision | Route shape | Acceptance check |
|---:|---|---|---|
| 3 | No model needed | deterministic FAQ lookup | document version and permission match |
| 4 | Low consequence, short context | efficient generation route | required fields, citation to supplied document, tone rubric |
| 3 | Ambiguous policy question | efficient attempt, then capable escalation if needed | evidence coverage plus calibrated human sample |
| 2 | State-changing proposal | capable proposal route only | schema, authorization, exact action digest, human approval |

Suppose the efficient route costs one unit for an attempt and the capable route
costs four units. The FAQ costs one-tenth of a unit. Those are not prices; they
are a simple accounting scale. Sending all twelve requests to the efficient
model appears cheap, but it ignores that the two state-changing requests have
an authority requirement and that the three policy questions may need a second
attempt. Sending everything to the capable model is easy to explain but pays
for capability that the FAQ and routine summaries do not need.

The manager's decision record for a policy question might say:

```text
eligible = {efficient-readonly, capable-readonly}
reason   = {consequence:medium, evidence_ambiguity:high, tools:none}
choice   = efficient-readonly
stop     = escalate if evidence validator abstains; max one escalation
success  = citation coverage + policy rubric + no unresolved contradiction
```

The router is not allowed to return `delete-account-provider` or to turn a
read-only question into a write. It can select only a declared enum, and the
deterministic policy owns the authority boundary.

## Failure drill: fluent and false-cheap

The efficient route answers all three ambiguous policy questions with polished
sentences. One contradicts the source, one omits a jurisdictional exception,
and one invents a missing date. A dashboard that counts HTTP success reports
three successes. An acceptance ledger reports zero accepted answers unless a
repair or human review makes them pass.

The false saving came from treating transport completion as business success.
The missing signals were evidence coverage, contradiction detection, and an
abstention state. The honest terminal states are accepted, repairable,
escalated, blocked, or failed. A router should not hide uncertainty by trying
providers until one sounds confident. The [honest practitioner guide to LLM
routing](https://seangeng.com/writing/the-honest-guide-to-llm-routing) is a
useful skeptical reading here: routing depends on a quality signal that is
good enough for the actual task distribution. [Tian Pan's cascade discussion](https://tianpan.co/blog/2025/11/03/llm-routing-model-cascades)
also helps separate a sequential cascade from a magic quality oracle.

## Reader exercises

1. Take twenty requests from one real workflow and put each into a
   deterministic, low-risk, ambiguous, or consequential lane. For each one,
   write the fact that makes a route eligible and the test that makes an
   outcome accepted.
2. Write one sentence of product promise for each lane. If the sentence uses
   “always,” test whether the underlying route can actually guarantee it.
3. Draw a route with two candidate providers. Mark what the router may choose
   and what only trusted deterministic policy or a human may authorize.
4. Add every cost that would be invisible if you measured only the first model
   call: validator, escalation, queue, retrieval, tool, human rework, and
   abandoned or indeterminate attempts.

## The route card: the manager's order slip

Before a route can be measured, write a route card. It is short enough for an
operator to read during an incident and precise enough for a replay. Start
with the user journey rather than the provider. “Summarize an approved
document for an employee” is a journey. “Call provider X” is an implementation
detail that might change.

A useful card contains:

```text
purpose and accepted business outcome
request strata and consequence classes
permitted data, tenant, region, and retention
required context, language, schema, and tools
eligible route enum set and disallowed paths
latency, budget, and retry ceiling
validation, approval, and terminal states
owner, baseline, review date, and rollback action
```

The card makes a hidden trade visible. Suppose a support team says “answer in
under five seconds.” Does that mean the first useful sentence, the complete
answer, or the time until a human can take over? Suppose it says “use the
cheapest qualified model.” Qualified by what evidence, and who refreshes that
evidence? Route economics cannot answer an undefined product promise.

The card also records negative space. A readonly policy lookup may not call a
write tool. A public summary may not be reused for a restricted tenant. A
classifier may rank three route enums but may not emit a provider string. The
negative rules are often easier to test than a vague positive claim.

Use a route ID that names the contract, not just the model: `readonly-summary-
v3`, `restricted-policy-region-r-v2`, or `proposal-human-gated-v1`. The
registry entry then binds the ID to an immutable model or deterministic
handler pin. When a model alias changes upstream, the route record does not
silently change. Create a new revision, replay it, and make the difference
visible in the decision log.

Finally, choose the baseline before the experiment. The card should say what
would happen if the router were deleted tomorrow. That could be a deterministic
FAQ, a fixed model, or a direct capable route. If nobody can state the
baseline, a reported saving has no counterfactual.

## From kitchen map to route choice

The first implementation can be a table, not a learned service. Give every
request a route card and every route a contract. A table row says: when these
trusted fields match, these enums are eligible; this validator decides pass;
this fallback is allowed; this owner receives the evidence. The table is easy
to review and gives a learned router a safe target later.

Notice what the table does not contain. It does not contain a free-form model
recommendation, an instruction to reveal hidden context, or a promise that one
provider will remain available. It contains a bounded decision and the reason
for it. A later classifier can reduce the work of finding the row, but the row
still defines the boundary.

When a route changes, compare the old and new card. Did the data class change?
Did a tool become available? Did the acceptance rubric move? Did the route
add a retry or an evaluator? Each change can alter cost and risk even if the
model pin stays the same. Require a new replay when the accepted outcome or
authority boundary changes.

## Checkpoint

If the team cannot explain a route in one paragraph, the route card is not
ready. Name the trusted facts, the eligible set, the choice signal, the
acceptance test, and the terminal state. Then name the counterfactual fixed
baseline. The first useful routing improvement is often discovering that a
deterministic handler can serve part of the workload or that a product promise
is missing an acceptance condition. Keep that discovery in the design record;
it is evidence about the workload, not a failure to build a router.

## Source slot

The primary research mechanism is [FrugalGPT](https://arxiv.org/html/2305.05176)
and [RouteLLM](https://arxiv.org/html/2406.18665). The practitioner and
counter-evidence slot is [Sean Geng's routing guide](https://seangeng.com/writing/the-honest-guide-to-llm-routing)
and [Tian Pan's cascade account](https://tianpan.co/blog/2025/11/03/llm-routing-model-cascades).
The source index labels papers as bounded measurements and practitioner pages
as implementation or skeptical evidence. The architecture in this chapter is
a proposal until the fixed replay, shadow, canary, reliability, security, and
rollback gates pass.
