# 07 — Model-Checking Agent Workflows with TLA+

Model checking is the formal-methods family that feels most like exploring a maze.

You define possible states. You define moves from one state to another. You define rules that must always hold. Then the model checker explores the maze and tries to find a path to a bad state.

For coding agents, this is a natural fit because agents are state machines wearing a chat interface.

## The agent as a state machine

A coding agent loop might look like this:

```text
Idle
  -> ReadTask
  -> Plan
  -> EditFiles
  -> RunTests
  -> InspectErrors
  -> Repair
  -> AskHuman
  -> Finish
```

Each arrow is an action. Each action changes state.

A state might include:

```text
files_changed: true/false
tests_passed: true/false
approval: true/false
retry_count: 0..3
secrets_loaded: true/false
last_tool: shell/browser/editor
```

Now you can ask formal questions:

```text
Can Finish happen while tests_passed=false?
Can Deploy happen while approval=false?
Can retry_count exceed 3?
Can secrets_loaded=true and last_tool=browser_search?
Can the agent get stuck forever in Repair?
```

These are model-checking questions.

## TLA+ in one paragraph

Leslie Lamport describes TLA+ as a high-level language for modeling programs and systems, especially concurrent and distributed ones, using simple mathematics to describe things precisely ([TLA+](https://lamport.azurewebsites.net/tla/tla.html)). TLA+ is not mainly about writing production code. It is about writing a precise model of behavior so tools can check design properties.

The TLA+ tools page lists the important tools: SANY for parsing and syntax checks, TLC as an explicit-state model checker, Apalache as a symbolic model checker, and TLAPS as a proof system ([TLA+ tools](https://lamport.azurewebsites.net/tla/tools.html)).

For coding-agent users, the most important piece is TLC-like thinking:

```text
small model + important property -> explore possible states -> find counterexample
```

## A tiny agent policy model

Pretend an agent can run tests, ask approval, deploy, or retry.

Variables:

```text
tests_passed ∈ {true, false}
approval ∈ {true, false}
deployed ∈ {true, false}
retry_count ∈ 0..3
```

Actions:

```text
RunTests: tests_passed becomes true or false
AskApproval: approval becomes true
Deploy: deployed becomes true
Retry: retry_count increases
```

Property:

```text
Always: deployed implies tests_passed and approval
```

If the model allows `Deploy` without checking `tests_passed` and `approval`, the model checker can find a counterexample trace:

```text
Initial: tests_passed=false, approval=false, deployed=false
Action: Deploy
Bad state: deployed=true, tests_passed=false, approval=false
```

That trace is more useful than a vague warning. It tells the agent developer exactly how the workflow permits a bad action.

## Why LLM-generated models are tempting

Writing TLA+ requires skill. A coding agent can read code, infer state variables, draft actions, and propose invariants. That is tempting because it lowers the cost of formal modeling.

The 2026 SIGOPS article [Can LLMs model real-world systems in TLA+?](https://www.sigops.org/2026/can-llms-model-real-world-systems-in-tla/) explains exactly this frontier. The authors asked Claude to write a TLA+ spec for Etcd’s Raft implementation. The spec passed syntax checks and ran through TLC. But it looked more like the Raft paper’s spec than Etcd’s actual implementation details.

That is the central warning:

```text
A generated model can be syntactically correct and still not be a model of your system.
```

## SysMoBench: from syntax to conformance

The SIGOPS article describes SysMoBench, a benchmark for LLM-generated TLA+ specs of real systems. It evaluates generated specs in four phases:

1. **Syntax phase** — does the spec compile?
2. **Runtime phase** — can TLC execute it without error?
3. **Conformance phase** — do transitions match traces from real code?
4. **Invariant phase** — does the spec satisfy key safety/liveness properties?

The results are the interesting part. LLMs do well on syntax and often runtime. But conformance and invariants expose the gap. The article reports that leading LLMs cluster near 100% syntax, while average conformance and invariant scores are much lower. It gives concrete ZooKeeper examples where the generated spec used textbook-looking patterns that did not match actual code behavior.

One failure mode is **extra states**: the spec enters states the real system never reaches. In the ZooKeeper example, the model accumulated votes with set union when the implementation overwrote old votes by sender.

Another failure mode is **missing states**: the spec fuses multi-step code behavior into one guard, making transitions impossible even though real code reaches them.

For coding agents, this is an important distinction:

```text
syntax success = the model is well-formed
runtime success = the model can run
conformance success = the model resembles the real system
invariant success = the important property holds
```

You need the last two for serious assurance.

## Agent workflows need conformance too

The same problem appears when modeling an agent harness.

Suppose an agent framework has a real behavior:

```text
1. propose tool call
2. pre-tool hook checks policy
3. human approval may be requested
4. tool call executes
5. post-tool hook logs result
```

An LLM-generated model might simplify it to:

```text
tool call executes if policy_ok
```

That simplification might miss a race:

- policy is checked before a file changes,
- file changes before tool execution,
- tool now acts on a different state.

Or it might miss the fact that approval expires, or that a subagent can call a tool through another path. The model might prove “safe” because it left out the unsafe transition.

Therefore, for agent workflows, model checking should be paired with trace validation:

```text
agent run logs -> event traces -> check whether model permits those transitions
```

That is the same lesson as SysMoBench.

## Where model checking helps coding-agent design

Model checking is especially useful for agent behavior that is:

- stateful,
- concurrent,
- retry-heavy,
- approval-gated,
- distributed across subagents,
- tool-chain dependent,
- hard to cover with example tests.

Examples:

### Approval workflow

Property:

```text
No irreversible action happens before human approval.
```

Actions:

```text
AskHuman, Approve, Reject, Deploy, ChargeCard, SendEmail
```

Model-checking question:

```text
Is there any path where Deploy happens without Approve?
```

### Retry budget

Property:

```text
The agent eventually stops retrying after N failures.
```

Actions:

```text
ToolFail, Retry, Escalate, Stop
```

Question:

```text
Can the agent loop forever?
```

### Multi-agent handoff

Property:

```text
A subagent cannot use a tool outside the parent task scope.
```

Actions:

```text
Delegate, NarrowScope, ToolCall, ReturnResult
```

Question:

```text
Can scope be lost during delegation?
```

### Memory consistency

Property:

```text
A fact marked untrusted is never used as trusted evidence.
```

Actions:

```text
ReadWeb, WriteMemory, PromoteFact, UseFact
```

Question:

```text
Can untrusted data become trusted without validation?
```

## How to start without learning all of TLA+

You can apply model-checking thinking before writing TLA+.

Start with a table:

| State variable | Possible values | Why it matters |
|---|---|---|
| `tests_passed` | true/false | deploy gate |
| `approval` | none/requested/granted/denied | irreversible actions |
| `retry_count` | 0..3 | loop bound |
| `data_scope` | public/internal/secret | tool policy |
| `agent_role` | planner/editor/reviewer | permission split |

Then list actions:

| Action | Preconditions | State changes |
|---|---|---|
| `RunTests` | files_changed | tests_passed := true or false |
| `Deploy` | tests_passed and approval=granted | deployed := true |
| `Retry` | retry_count < 3 | retry_count := retry_count + 1 |
| `Escalate` | retry_count >= 3 | human_required := true |

Then list properties:

```text
DeployRequiresGreenTests
DeployRequiresApproval
RetriesAreBounded
SecretsNeverLeaveAllowedTools
ReviewerCannotEditCode
```

This table is already most of the modeling work. TLA+ or another model checker is the next step when the table becomes important enough.

## The coding-agent opportunity

A good coding agent can help with this process:

1. Read the harness code.
2. Identify state variables and actions.
3. Draft a state-machine model.
4. Draft safety and liveness properties.
5. Run the model checker.
6. Explain counterexamples.
7. Propose harness changes.
8. Rerun checks.

But the human must review the abstraction. Ask:

- Did the model include all tool-call paths?
- Did it include subagents?
- Did it include failed approvals?
- Did it include timeouts?
- Did it include memory writes?
- Did it include data classification?
- Did it include real implementation quirks?

The SysMoBench lesson is that LLMs are good at writing something that looks like TLA+. The hard part is writing a model that matches the system.

## Summary

Model checking is how you ask, “Can this workflow reach a bad state?”

For coding agents, bad states are often operational:

```text
deployed_without_tests
secret_sent_to_browser
approval_skipped
retry_loop_unbounded
subagent_exceeded_scope
memory_poisoned_as_trusted
```

TLA+ and related tools give a disciplined way to model those states. LLMs can help draft models, but conformance checks and human review are essential. A beautiful model of the wrong workflow is just another hallucination with mathematical syntax.
