# 9. Structured outputs and recovery: syntax is the first gate

Structured output constrains a model response to a machine-readable shape,
usually JSON conforming to a supported schema. It can eliminate a large class
of parsing failures. It cannot prove that values are true, authorized, safe,
fresh, or meaningful.

Think of structured generation as a type boundary around a probabilistic
component. After that boundary, ordinary application validation still applies.

## ELI5: a correctly completed form can still be wrong

A form requires:

- a date in a date box;
- an amount in a number box;
- one value from an approved status list.

A clerk can fill every box in the correct format and still enter tomorrow’s
date, the wrong amount, or another customer’s status. Schema compliance proves
that the form has the right shape—not that the clerk understood the case.

## Four levels of “valid”

Keep these predicates separate:

1. **Syntactic validity:** the bytes parse as JSON.
2. **Schema validity:** required fields, types, enums, and supported structural
   constraints match.
3. **Semantic validity:** the values are coherent and supported by evidence.
4. **Business/policy validity:** the requested operation is permitted now for
   this caller and state.

Only the first two are targets of structured decoding.

```text
model output
  → transport/finish check
  → parse
  → schema
  → semantic/domain validation
  → authorization and policy
  → side effect or presentation
```

Never jump from “parsed successfully” to “execute.”

## How constrained decoding works

Without a structural constraint, the active **sampling policy**—the rules that
turn model scores into a next-token choice—may select a token that makes the
desired syntax invalid. Ordinary filters such as top-*k* or top-*p* already
change which tokens remain eligible; they do not track whether a JSON document
can still satisfy a schema. A structured-output engine compiles the supported
schema into a grammar or state machine and masks tokens that cannot validly
continue the current grammar state.

[OpenAI, “Introducing Structured Outputs in the API”](https://openai.com/index/introducing-structured-outputs-in-the-api/)
describes compiling JSON Schema into a context-free grammar and dynamically
restricting valid next tokens. It also names important exceptions: refusal,
premature termination, unsupported combinations, and one-time schema
preprocessing latency. Its 100% schema score is an OpenAI evaluation for named
models and schema tests, not a claim of semantic correctness.

[Anthropic documentation, “Structured Outputs”](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
provides a second current contract. Its SDK may simplify unsupported schema
features before generation and then validate the result against the original
schema. That difference matters for portability: “JSON Schema” does not imply
identical keyword support, cold-compile behavior, refusal representation, or
limits across providers.

## Design a schema for decisions, not prose storage

A good schema narrows ambiguity. This is an actual JSON Schema, not an instance
with pseudo-values:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.invalid/schemas/invoice-decision-v1.json",
  "title": "Invoice decision",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "decision",
    "invoice_id",
    "evidence_ids",
    "reason_code",
    "confidence"
  ],
  "properties": {
    "schema_version": {"const": "invoice-decision-v1"},
    "decision": {
      "type": "string",
      "enum": ["approve", "reject", "needs_review"]
    },
    "invoice_id": {
      "type": "string",
      "pattern": "^inv_[A-Za-z0-9_-]{1,60}$",
      "maxLength": 64
    },
    "evidence_ids": {
      "type": "array",
      "minItems": 1,
      "maxItems": 20,
      "uniqueItems": true,
      "items": {"type": "string", "minLength": 1, "maxLength": 128}
    },
    "reason_code": {
      "type": "string",
      "enum": ["matched", "amount_mismatch", "missing_evidence", "policy_hold"]
    },
    "confidence": {"type": "number", "minimum": 0, "maximum": 1}
  }
}
```

A conforming instance is ordinary data:

```json
{
  "schema_version": "invoice-decision-v1",
  "decision": "needs_review",
  "invoice_id": "inv_4821",
  "evidence_ids": ["page-2:total", "ledger:po-884"],
  "reason_code": "amount_mismatch",
  "confidence": 0.71
}
```

Negative fixtures should fail for one named reason at a time:

| Mutation | Expected failure |
| --- | --- |
| `"decision": "maybe"` | value is outside the enum |
| `"confidence": 1.4` | value exceeds the maximum |
| omit `evidence_ids` | required property is missing |
| add `"tenant_id": "t-north"` | additional property is forbidden |

Prefer:

- enums over free-form status strings;
- stable IDs over copied names;
- explicit units and currencies;
- `null` or a tagged union for known absence;
- bounded lengths and numeric ranges;
- schema versions;
- evidence references;
- an explicit `needs_review` state.

Avoid asking the model to invent database primary keys, authorization claims,
or timestamps that deterministic code already knows.

Do not hide the user-facing explanation inside a field that downstream code
mistakes for evidence. Store claims and source references separately.

## Structural constraints can affect the answer

Constrained decoding changes which tokens are available at each step. If the
schema forces a decision before the model has room to express uncertainty, it
can produce perfectly formed overconfidence.

The browser-acquired text-layer paper
[Maximilian Schall and Gerard de Melo, “The Hidden Cost of Structure: How Constrained Decoding Affects Language Model Performance” (RANLP 2025)](https://aclanthology.org/2025.ranlp-1.124/)
empirically examines quality effects rather than assuming valid structure is
free. Its tasks and constrained-decoding implementations bound the result, but
the production lesson is general: compare semantic quality with and without
the constraint, and redesign the schema if the representation makes reasoning
harder.

The preprint
[Saibo Geng et al., “Generating Structured Outputs from Language Models: Benchmark and Studies” (arXiv:2501.10868)](https://arxiv.org/html/2501.10868v1)
maps constrained-generation approaches and evaluation dimensions. It supports
testing schema complexity, not choosing a provider solely from one validity
percentage.

## Recovery is a typed state machine

Handle outcomes explicitly:

```text
success
refusal
truncated
transport_error
schema_error
semantic_error
authorization_denied
approval_required
uncertain
```

A safe recovery ladder is:

1. **Classify.** `authorization_denied` is terminal for this action: stop and
   audit metadata-safely. Approval cannot widen RBAC, ABAC, tenant, or
   resource authority. `approval_required` means the caller is currently
   authorized but consequence policy requires an exact, expiring approval;
   wait, then reauthorize at commit.
2. **Retry transient transport failure** with the same request identity,
   deadline, and bounded exponential backoff.
3. **Continue or regenerate truncation** only when the provider contract makes
   this safe; otherwise start a bounded fresh attempt.
4. **Repair a schema failure** using the validator’s focused errors, while
   retaining the original output and attempt lineage.
5. **Re-ground a semantic failure** from authoritative data rather than asking
   the model to “be more accurate.”
6. **Fall back** to a simpler schema, alternate model, deterministic path, or
   human review when the product contract allows it.
7. **Stop** when the retry, time, or consequence budget is exhausted.

With strict constrained decoding, schema retries should be uncommon and may
signal unsupported schema, interruption, or integration error. Do not build an
unbounded “parse → ask model to fix → parse” loop.

[Cadence, “Structured outputs in production: lessons learned”](https://cadence.withremote.ai/blog/structured-outputs-llm-production)
offers practical retry and repair experience. Provider capabilities change
quickly, so its comparative statements are dated practitioner evidence; check
current provider docs before adopting a fallback assumption.

## Worked example: invoice extraction

The model extracts supplier, invoice number, currency, line items, subtotal,
tax, total, and evidence spans.

After schema validation, deterministic code should still:

- resolve the supplier against the authenticated tenant’s records;
- normalize currency and decimal representation;
- check `sum(lines) + tax == total` within an explicit tolerance;
- verify dates and duplicate invoice numbers;
- confirm every high-risk field points to a source span;
- route mismatches or low-quality scans to review;
- make persistence idempotent.

A schema-valid invoice with the wrong total is not “mostly successful.”

## Test matrix

Include:

- optional, nullable, recursive, and union shapes actually used;
- long strings and Unicode;
- adversarial text containing braces or fake instructions;
- refusal and content-filter behavior;
- maximum-token interruption;
- schema compilation cold start and cache invalidation;
- provider/model fallback with the same logical contract;
- semantically impossible but schema-valid values;
- version migration and unknown enum values.

Track syntax, schema, semantic, and business acceptance separately. A single
“JSON success” metric obscures the most costly errors.

## Interview checkpoint

**Question:** “Does strict structured output make function calling safe?”

A strong answer says it can guarantee supported argument shape under stated
completion conditions. It cannot guarantee the correct function, correct
entity, truthful value, caller authority, safe timing, or idempotent effect.
Those are enforced by registry, domain validation, policy, and execution
layers.

**Explain it back:** Why might a schema with only `{"answer": "string"}` be
valid but provide almost no reliability?

## Capstone increment

Define the assistant's streaming protocol and final-result union with explicit
states for `progress`, `result`, `refusal`, `truncated`, `semantic_error`,
`authorization_denied`, `approval_required`, and `uncertain`. For every
non-success state, specify one bounded recovery or terminal route; never turn
it into plausible success text. Validate the checked-in positive and negative
instances against the real schema.

The input is the Chapter 1 terminal-evidence contract. The output is a
versioned schema plus state-transition table. **Definition of done:** each test
matrix row ends in a typed state, and a schema-valid but unsupported claim
cannot enter `result`.

Next: [Function calling and tool contracts](10-function-calling-and-tool-contracts.md)
places structured arguments inside an end-to-end action protocol.
