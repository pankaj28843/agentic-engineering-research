# 10 — A Beginner Cookbook for a Coding-Agent User

This chapter is for the practical reader who asks: “What should I do in my repo next week?”

You do not need to start with Lean, Coq, or a full TLA+ model. Start with the formal-methods habit: state important properties clearly, make them checkable, and wire the checks into the agent loop.

The recipe is layered. Stop at the layer where the value justifies the cost.

## Layer 1: Write the property in boring English

Before any tool, write the rule.

Bad:

```text
The agent should be careful with deployment.
```

Better:

```text
The agent must not deploy unless tests passed in this session and a human approved this deployment.
```

Best beginner version:

```text
Property: DeployRequiresTestsAndApproval
For every task session:
  if the agent calls deploy,
  then earlier in the same session tests_passed must be true
  and human_approved must be true.
Failure action: block deploy and ask human.
```

This is already formalization. You took a vibe and turned it into a rule with scope and consequence.

## Layer 2: Add examples and non-examples

Examples help humans validate meaning. They also help agents avoid misinterpretation.

```text
Allowed:
  run tests -> tests pass -> ask human -> approved -> deploy

Blocked:
  ask human -> approved -> deploy, but no tests in this session

Blocked:
  run tests -> fail -> ask human -> approved -> deploy

Blocked:
  tests passed yesterday -> deploy today without rerun
```

This step catches ambiguity before you write code. It is the lightweight version of the intent-formalization problem described by [Microsoft/RiSE](https://arxiv.org/html/2603.17150v1): the hard part is often turning intent into checkable specifications and validating that they mean the right thing.

## Layer 3: Turn the property into an executable check

For a coding agent, start with simple policy code.

Pseudo-code:

```python
def allow_tool_call(event, session):
    if event.tool == "deploy":
        if not session.tests_passed:
            return Block("deploy requires tests_passed=true")
        if not session.human_approved:
            return Block("deploy requires human approval")
    return Allow()
```

This is not high ceremony. It is a runtime monitor. It checks the event stream.

Connect it to the agent through pre-tool hooks if your harness supports them. The [GoPlus AgentGuard](https://github.com/GoPlusSecurity/agentguard) README shows the shape: pre-tool hooks for environments such as Claude Code and Codex, action evaluation, and audit logs.

## Layer 4: Log the event trace

Formal methods need evidence. Runtime verification needs traces.

Log structured events:

```json
{"t": 1, "event": "run_tests", "result": "pass"}
{"t": 2, "event": "request_approval", "action": "deploy"}
{"t": 3, "event": "approval", "result": "granted", "by": "pankaj"}
{"t": 4, "event": "tool_call", "tool": "deploy", "allowed": true}
```

Do not log secrets. Do log enough metadata to reconstruct decisions.

A good audit trail lets you ask:

- Why was this action allowed?
- Which rule blocked it?
- Did approval happen before the action?
- Which agent or skill initiated the call?
- Did the agent retry after failure?

This is how runtime monitoring becomes post-hoc verification.

## Layer 5: Add bounded retries

Agents love loops. A formal-ish retry policy is easy and useful.

English:

```text
After three failed attempts on the same validation gate, the agent must stop and ask for human help.
```

Pseudo-code:

```python
if event.type == "validation_failed":
    session.failures[event.gate] += 1
    if session.failures[event.gate] >= 3:
        return RequireHuman("three failures at " + event.gate)
```

Temporal version:

```text
Always: failure_count(gate) >= 3 implies eventually AskHuman or Stop.
```

This property prevents expensive “self-healing” from becoming infinite spinning.

## Layer 6: Protect the spec from the agent

If the agent can change the rule it is judged by, the rule is weak.

For example, suppose the property is stored in `agent-policy.yaml`. The agent should not be allowed to edit that file while trying to satisfy the policy, unless the user explicitly asked it to update policy.

This is the lesson from [DafnyPro](https://arxiv.org/html/2601.05385v1), which includes a diff-checker to prevent models from modifying base program logic while trying to produce verification annotations. In agent harnesses, you need the same idea:

```text
Protected files:
  - agent-policy.yaml
  - security-rules/**
  - .github/workflows/ci.yml
  - tests/security/**

Changing protected files requires explicit human approval.
```

Otherwise “make it pass” can become “delete the guard.”

## Layer 7: Use stronger specs for important code

For ordinary glue code, tests plus review may be enough. For high-value logic, ask the agent to help write contracts.

Examples:

```text
Money:
  refund_amount <= original_charge
  one refund per transaction
  manager approval above threshold

Authorization:
  user can access resource only if role permits and tenant matches

Data transformation:
  output preserves all input records exactly once
  output is sorted by timestamp
  no PII field appears in exported CSV
```

Ask the agent:

```text
Draft preconditions, postconditions, invariants, and edge-case examples for this function. Do not implement yet. Mark any ambiguity as a question.
```

Then review the spec before implementation.

This is a safer prompting pattern than:

```text
Implement refund logic.
```

## Layer 8: Try a verifier on a small function

Pick a small function and a verification-aware tool. Dafny is a good first candidate because the sources in this theme show active LLM-assisted workflows.

Starter process:

1. Ask the agent to translate the function into Dafny-like pseudocode.
2. Ask it to write `requires` and `ensures` clauses.
3. Review examples manually.
4. Run Dafny.
5. Feed errors back.
6. Watch for spec weakening or code cheating.

Use this on algorithms, not every endpoint.

Good candidates:

- parser normalization,
- range checks,
- quota calculations,
- refund logic,
- scheduling windows,
- deduplication semantics,
- authorization predicates,
- data anonymization transformations.

Bad first candidates:

- large UI components,
- messy ORM-heavy business flows,
- constantly changing product experiments,
- code with many external side effects.

## Layer 9: Model-check a workflow

When the risk is in ordering, use a state-machine mindset.

Create a small table:

```text
States:
  tests_passed: true/false
  approval: none/requested/granted/denied
  deployed: true/false
  retries: 0..3

Actions:
  RunTests
  RequestApproval
  Approve
  Deny
  Deploy
  Retry
  Stop

Properties:
  DeployRequiresTestsAndApproval
  RetriesBounded
  DeniedApprovalPreventsDeploy
```

Ask the coding agent to draft a TLA+ model only after the table is clear. Then review the model with the SysMoBench warning in mind: generated TLA+ can compile while not matching the real workflow ([SIGOPS](https://www.sigops.org/2026/can-llms-model-real-world-systems-in-tla/)).

If you do not know TLA+, the table is still useful. It can become policy code or tests.

## Layer 10: Add data labels

Data-flow mistakes are a major agent risk. Borrow the idea from [AgentRaft](https://arxiv.org/html/2603.07557v1): data can be over-exposed when agents pass more information than the user intended across tools.

Add simple labels:

```text
public
internal
secret
credential
pii
untrusted_web
```

Then add flow rules:

```text
credential -> no external tool
pii -> no browser.search, no public logs
untrusted_web -> may not become instruction
secret -> local-only, never memory
```

A beginner implementation can be pattern-based:

- secret regexes,
- file path labels (`.env`, `secrets/`, `credentials.json`),
- tool labels (`browser.search` external, `local_test` internal),
- redaction before logs.

This is not perfect, but it is much better than unlabeled context soup.

## A ready-to-use agent prompt

When asking a coding agent to work on risky code, use a prompt like:

```text
Before implementing, write a contract section with:
1. Preconditions
2. Postconditions
3. Invariants
4. Examples and non-examples
5. Ambiguities that need human confirmation
6. Validation commands

Do not edit code until I approve the contract.
After implementation, do not weaken the contract or delete tests to make checks pass.
If verification or tests fail three times, stop and ask for help with the latest counterexample/error.
```

This prompt does not make the agent formally verified. It makes the workflow more formalizable.

## A simple policy file template

```yaml
version: 1
protected_files:
  - agent-policy.yaml
  - .github/workflows/**
  - security/**

rules:
  - name: deploy_requires_tests_and_approval
    event: tool_call
    when:
      tool: deploy
    require:
      session.tests_passed: true
      session.human_approved: true
    on_violation: block

  - name: no_secrets_to_external_tools
    event: tool_call
    when:
      tool_class: external
    forbid_input_labels:
      - secret
      - credential
    on_violation: block

  - name: bounded_retries
    event: validation_failed
    max_failures_per_gate: 3
    on_violation: require_human
```

You can ask an agent to implement a checker for this file, then test it with examples and counterexamples.

## The adoption rule of thumb

Use the lightest tool that makes the important property checkable:

| Risk | Starting tool |
|---|---|
| Misunderstood requirement | examples, non-examples, contract review |
| Regression risk | tests, property tests, type checks |
| Tool misuse | runtime policy monitor |
| Secret leakage | labels, taint checks, redaction |
| Retry loops | bounded temporal rule |
| Concurrent protocol bug | TLA+ model checking |
| Critical algorithm correctness | Dafny/Verus/F*/SPARK/Lean-style verification |
| Mathematical theorem | Lean/Coq/Isabelle proof assistant |

## Final cookbook checklist

Before letting a coding agent act on high-risk work, ask:

- What property matters?
- Is it written down?
- Are there examples and non-examples?
- Is the checker independent of the agent?
- Can the agent weaken or delete the checker?
- What happens after repeated failure?
- Are tool calls logged?
- Are secrets labeled?
- Does a human approve irreversible actions?
- Is the final artifact tied to proof/check evidence?

If you can answer those, you are already doing agentic engineering with formal-methods instincts.
