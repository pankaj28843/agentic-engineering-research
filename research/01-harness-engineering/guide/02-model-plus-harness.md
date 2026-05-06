# Chapter 02 — Model plus harness

**You'll learn:** why a raw LLM is not a useful coding agent by itself, what capabilities the harness adds, and how to reason from desired behaviour back to harness design.

Source jumps: LangChain's [Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness), Addy Osmani's [Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/), HumanLayer's [12 Factor Agents](https://github.com/humanlayer/12-factor-agents), and Anthropic's [long-running harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

## The model is the brain, not the body

A large language model is astonishingly capable, but by itself it is closer to a brain in a jar than to a software engineer. It can predict text. It can reason over what is in its context window. It can emit code. But it cannot, by itself, open your repository, run a test, inspect a browser, remember yesterday's progress, create a git commit, ask for approval, or stop itself from reading secrets. All of those require a surrounding system.

That surrounding system is the harness. LangChain phrases it bluntly: [“If you're not the model, you're the harness”](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness). This is useful because it prevents a common mistake: treating model selection as the only engineering lever. A frontier model in a weak harness can behave worse than a slightly weaker model in a strong harness because the strong harness gives it better tools, clearer state, safer execution, and sharper feedback.

A simple agent loop looks like this:

```text
context so far
   │
   ▼
LLM decides next action
   │
   ├── final answer? ──► stop
   │
   └── tool call ─────► deterministic code runs tool
                          │
                          ▼
                      observation appended to context
                          │
                          └── loop
```

HumanLayer's [12 Factor Agents](https://github.com/humanlayer/12-factor-agents) makes a related point: good production agents are “mostly just software,” with LLM steps inserted where they create leverage. The magical part is often a structured-output decision inside a larger deterministic system. That framing is healthy. It turns “agent design” back into software engineering.

## The harness capabilities, one by one

LangChain derives harness components by asking what behaviour we want from a model and what the model cannot do out of the box. This is a good way to avoid cargo-culting agent features. Do not add a vector database, MCP server, browser, subagent, or memory file because it sounds modern. Add it because it gives the model a behaviour it otherwise lacks.

### Durable storage: filesystem and git

Models operate on context. Repositories operate on files. The filesystem is therefore the first serious harness primitive. It lets the agent read source, write changes, store intermediate notes, and offload information that does not fit in context. Git then adds history, branches, diffs, rollback, and a collaboration surface.

This sounds mundane, but it is foundational. Anthropic's long-running agent harness uses a progress file plus git history so each fresh context window can understand what previous sessions did. OpenAI's Codex setup treats repository-local docs and execution plans as the system of record. Stripe's minions create branches, push to CI, and prepare pull requests. These are not model capabilities; they are harness capabilities.

### Action: tools, bash, and code execution

A model can suggest a command, but only a harness can run it. Most coding agents therefore give the model tools: read file, write file, search files, run shell command, apply patch, inspect browser, query logs, call MCP servers, and so on.

Bash is the general-purpose escape hatch. Instead of pre-building a tool for every possible action, the harness can let the agent write and execute small scripts. This gives the model a computer-like environment rather than a narrow form. It is powerful and dangerous. A harness that grants shell access must also decide where that shell runs, what it can reach, and which commands need approval.

### Observation: tests, logs, screenshots, traces

A coding agent that cannot observe its work is just guessing. Tests and linters give computational observations. Browser automation gives UI observations. Logs, metrics, and traces give runtime observations. Screenshots and DOM snapshots make frontend state visible. Tool outputs tell the agent whether an action worked.

OpenAI's article is especially concrete: Codex can boot an app per git worktree, drive it through Chrome DevTools Protocol, inspect DOM snapshots and screenshots, query logs with LogQL, and query metrics with PromQL. That makes prompts like “ensure startup completes in under 800ms” or “no span in these journeys exceeds two seconds” tractable. The point is not that every repo needs OpenAI's stack. The point is that the agent can only reason about what the harness makes legible.

### Memory: repository knowledge and context retrieval

Models have a training cutoff and no persistent memory unless the harness supplies one. For coding work, the best memory is often boring: versioned files in the repo. `AGENTS.md`, `docs/architecture.md`, product specs, design notes, execution plans, generated schema references, and troubleshooting guides are memory surfaces.

The mistake is dumping all memory into every prompt. Böckeler's [context engineering memo](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html) warns that context is scarce even when windows are large. OpenAI's “map, not encyclopedia” pattern says the same thing: keep the always-loaded entry point small and use progressive disclosure to point agents to deeper sources.

### Control flow: orchestration, continuation, handoffs

A single loop can do a lot, but longer work needs control flow. The harness may split work into planner, coder, reviewer, evaluator, and cleanup agents. It may run subagents in parallel. It may intercept a model's attempt to stop and continue in a clean context. It may route tasks to different models. It may require a sprint contract before implementation.

Anthropic's initializer/coding-agent split is the clearest public example in the sources. The initializer sets up files that make the project understandable across sessions. Later coding agents work incrementally, one feature at a time, and leave state behind. This is orchestration, even if Anthropic notes that the “separate agents” in that post mainly differ by prompt.

### Constraints: permissions, schemas, boundaries

A harness also prevents action. It scopes tools, validates output schemas, blocks dangerous commands, enforces architecture boundaries, and requires approval for high-risk operations. OWASP's [AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) treats least privilege, memory isolation, human approval, output validation, monitoring, and secure multi-agent communication as core controls. OpenAI statically enforces dependency directions and taste invariants. Stripe isolates devboxes from production resources and the internet.

Constraints are not anti-agent. They are what make autonomy tolerable.

## Why the same model behaves differently in different harnesses

If you have used multiple coding agents backed by similar models, you have likely felt this. One agent edits files cleanly; another mangles patches. One remembers to run tests; another stops after writing code. One can drive a browser; another cannot inspect the UI. One handles long tasks; another loses the plot. The model matters, but the harness changes the behaviour.

LangChain points out an even subtler issue: model training and harness design co-evolve. Agent products post-train models with their tools and workflows in the loop. That can make a model very good at one edit mechanism or tool protocol and weaker when dropped into another. This is not necessarily a defect. Humans also get good at the tools they practice. But it means “model capability” and “harness capability” are entangled.

For a team, the practical lesson is simple: evaluate agents in the harness you will actually use. A benchmark score in one harness is a clue, not a guarantee. If your repo needs browser evidence, private docs, custom linters, a weird build system, or strict security boundaries, your local harness will dominate the experience.

## Behaviour-first harness design

The most useful design question is:

> What behaviour do I want the agent to show, and what harness feature would make that behaviour more likely or more verifiable?

Here are examples:

| Desired behaviour | Harness feature |
|---|---|
| Agent remembers project conventions | Short `AGENTS.md` plus linked docs |
| Agent does not one-shot huge tasks | Plan file, feature list, one-feature-at-a-time instruction |
| Agent verifies UI behaviour | Browser automation, screenshots, DOM snapshots |
| Agent fixes simple lint failures itself | Fast local lint hook with agent-readable error messages |
| Agent avoids architectural drift | Structural tests and dependency rules |
| Agent avoids secrets | Sandbox, blocked paths, read-only tools, secret scanning |
| Agent asks before risky actions | Human approval middleware by risk level |
| Agent resumes after context exhaustion | Progress file, git commits, continuation loop |
| Agent learns from repeated failures | Harness update checklist after review |

This table is more important than any specific framework. It teaches the habit: start from behaviour, then engineer the environment.

## A diagram to carry forward

```text
                 ┌──────────────────────────────┐
                 │            Model             │
                 │  predicts, reasons, chooses  │
                 └──────────────┬───────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
  Context & memory         Tools & action          Feedback & control
  AGENTS.md, docs          shell, MCP, browser     tests, logs, review
  plans, files, git        sandbox, APIs           approval, linters
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                ▼
                     Useful coding agent behaviour
```

The model is still central. A weak model will not become brilliant because you wrote a nice `AGENTS.md`. But as models become stronger, the harness becomes the place where their general capability is shaped into local reliability.

## Chapter takeaways

- “Agent = model + harness” is broad, but it captures a vital truth: the model is not the whole system.
- Filesystem, git, tools, observations, memory, orchestration, and constraints are harness capabilities.
- The same model can behave very differently in different harnesses.
- Good harness design starts from desired behaviour, not from fashionable components.
- For coding agents, the strongest harness primitives are often boring software engineering: files, tests, logs, shells, docs, git, and permissions.

**Next:** [Chapter 03 — Guides and sensors](03-guides-and-sensors.md).
