# Chapter 04 — Context engineering

**You'll learn:** why context engineering is the substrate of harness engineering, why giant instruction files fail, and how progressive disclosure helps agents find the right information at the right time.

Source jumps: Böckeler's [Context Engineering for Coding Agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html), the main [harness article](https://martinfowler.com/articles/harness-engineering.html), OpenAI's [repository knowledge store](https://openai.com/index/harness-engineering/), Anthropic's [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), and LangChain's [context rot discussion](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness).

## Context is what the model can see

A coding agent can only use what reaches its context window or what it can retrieve through tools. If a convention lives in a senior engineer's head, the agent does not know it. If a design decision is buried in Slack, the agent will not find it unless the harness exposes it. If a critical rule appeared fifty turns ago and the current context is full of logs, the model may not attend to it.

Böckeler quotes a simple definition from Bharani Subramaniam: context engineering is “curating what the model sees so that you get a better result.” Harness engineering depends on this. Guides and sensors only help if the harness can put them where the agent can notice and use them.

This is why OpenAI says “agent legibility is the goal.” From Codex's point of view, anything inaccessible in-context effectively does not exist. Repository-local, versioned artifacts are visible; private chat memories are not. The agent-first move is to make the important parts of the organization legible in the repo: architecture, product specs, design principles, quality grades, reliability notes, security notes, generated schemas, and execution plans.

## The big context mistake

The tempting solution is to paste everything into one giant rules file. OpenAI tried that and says it failed in predictable ways:

- Context is scarce; a huge file crowds out the actual task and relevant code.
- Too much guidance becomes non-guidance; when everything is important, nothing is.
- The file rots; stale rules become attractive nuisances.
- A blob is hard to verify mechanically; coverage, freshness, ownership, and links drift.

Böckeler's context memo makes the same point from the coding-agent user side. Context windows have grown, but indiscriminately dumping information into them still hurts quality and cost. More context is not automatically better context. A harness has to decide what is always loaded, what is lazily loaded, what is retrieved by the model, what is invoked by the human, and what is triggered by deterministic software.

## Progressive disclosure

Progressive disclosure means the agent starts with a small, stable entry point and discovers more only when needed. OpenAI's pattern is a short `AGENTS.md` acting as a table of contents, not an encyclopedia. It points to a structured docs directory. The docs directory holds deeper sources of truth: design docs, execution plans, generated references, product specs, quality scores, reliability docs, and security docs.

This is similar to a good onboarding packet for a human. You do not hand a new engineer every document ever written. You give them a map: where architecture lives, where product specs live, how to run tests, who owns what, and how to find details. The agent needs the same map, but with more mechanical precision because it has less common sense about when a detail is load-bearing.

A practical pattern:

```text
AGENTS.md
  short safety rules
  validation commands
  links to deeper docs

docs/
  architecture.md
  testing.md
  security.md
  reliability.md
  product-specs/
  exec-plans/
  generated/

skills/
  task-specific instructions loaded only when relevant
```

The always-loaded layer should be small. The deeper layers should be easy to search, clearly titled, and source-linked. If a doc becomes stale, the harness should have a sensor for that: link checks, generated docs checks, or “doc gardening” tasks.

## Context interfaces

Böckeler separates reusable prompts from context interfaces. Reusable prompts include instructions and guidance: “write E2E tests this way,” “we use yarn, not npm,” “do not keep backward compatibility during this refactor.” Context interfaces tell the agent how to get more context: tools, MCP servers, skills, file search, browser, issue trackers, documentation search, and so on.

The “who decides to load it?” question matters:

- The agent decides: skills, tool calls, file search. This enables autonomy but is nondeterministic.
- The human decides: slash commands or explicit instructions. This is controlled but less autonomous.
- The agent software decides: hooks or path-scoped rules. This is deterministic but requires product support.

A good harness uses all three. For example, path-scoped rules might load TypeScript conventions when TypeScript files are edited. A human might invoke a security audit skill. The agent might search `docs/reliability.md` after seeing an SLO-related task.

## Context rot and compaction

LangChain's harness article uses the phrase “context rot” for the way agent performance degrades as the context window fills. The window may be large, but it is not a clean database. Long transcripts contain stale plans, failed attempts, huge tool outputs, duplicate logs, and half-remembered constraints. The model's attention becomes noisier.

Harnesses fight context rot with several techniques:

- **Compaction:** summarize or offload older context so the task can continue.
- **Tool output offloading:** keep only useful head/tail excerpts in context and store full output in files.
- **Skills:** load only front matter or descriptions initially, then load full details when relevant.
- **Progress files:** preserve durable state outside the transcript.
- **Fresh starts:** use git status, progress notes, and plans to restart in a clean context.

Anthropic's long-running harness shows why compaction alone is insufficient. Even with compaction, an agent building a complex app may one-shot too much, run out of context mid-implementation, or later declare the project done because it sees partial progress. Durable files and explicit session-start routines are needed.

## Agent-friendly docs are not just human docs

Human docs can rely on shared background. Agent-friendly docs need extra structure:

- Explicit commands, not “run the usual tests.”
- Clear ownership and freshness signals.
- Links to source files or generated references.
- Examples of good and bad patterns.
- Short sections with descriptive headings.
- Stable filenames that agents can search.
- Acceptance criteria that can be checked.
- Warnings about destructive actions and approval boundaries.

This does not mean writing robotic prose. It means making implicit context explicit. OpenAI says this is similar to onboarding a new teammate: product principles, engineering norms, and team culture need to be discoverable. The difference is that the agent will not overhear the hallway conversation.

## Context as a cost control

Context is also money. Long prompts, repeated docs, and huge pasted logs burn tokens. Böckeler notes that too much context is a cost factor. Stripe also treats feedback loops as cost-sensitive: CI runs cost tokens, compute, and time, so minions do local checks first and cap CI retries. OpenAI similarly keeps the entry point short and enforces docs mechanically.

Good context engineering therefore reduces both errors and waste. A source-linked chapter guide in this repo is context engineering for future agents and for you as the human reader. Instead of repeatedly crawling and re-summarizing the same sources, the repo should preserve a durable learning substrate: source snapshots in `tmp/`, source metadata in git, and a book-like guide that encodes the synthesis.

## A context checklist for any repo

When you prepare a repo for coding agents, ask:

1. What must the agent always know before doing anything?
2. What can be linked from the always-loaded file instead?
3. What docs are stale, contradictory, or not source-linked?
4. What commands prove the repo is healthy?
5. What context should be generated from code rather than handwritten?
6. What external systems need safe context interfaces?
7. What should never enter context: secrets, PII, production data?
8. What repeated review comments should become docs or checks?
9. What large outputs should be written to files instead of pasted into context?
10. How will a fresh agent resume after context is compacted or lost?

If you cannot answer these, your harness is relying on luck.

## Chapter takeaways

- Context engineering curates what the model sees; harness engineering depends on it.
- A giant `AGENTS.md` is usually an anti-pattern; use a short map plus deeper docs.
- Progressive disclosure protects attention and cost.
- Context interfaces include tools, MCP servers, skills, file search, browser access, and generated references.
- Long-running work needs durable state outside the transcript, not just compaction.

**Next:** [Chapter 05 — Quality left, CI, and CD](05-quality-left-ci-cd.md).
