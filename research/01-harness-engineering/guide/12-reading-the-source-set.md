# Chapter 12 — Reading the source set: annotated field notes

**You'll learn:** how the major crawled sources fit together, which ones are primary versus vendor or community signals, and what to read when you want more detail than this guide can carry.

Source jumps: the full source list in [source-index.md](../source-index.md) and machine-readable [sources.json](../sources.json).

## Why this chapter exists

A deep research theme should not leave you with only a polished synthesis. You should also know how to navigate the source landscape yourself. Harness engineering is moving fast, and the vocabulary is still settling. The right reading habit is to separate primary evidence, practitioner patterns, vendor narratives, security guidance, and community skepticism.

This chapter is a map of the source set. It does not replace the [source index](../source-index.md), which lists every extracted source. Instead, it explains the role each source family plays in the argument.

## The spine: Fowler/Thoughtworks

Start with Birgitta Böckeler's [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html). It is the cleanest conceptual spine because it narrows a broad industry slogan into a practical frame for coding-agent users. The important terms are guides, sensors, computational controls, inferential controls, steering loop, quality left, maintainability harness, architecture fitness harness, behaviour harness, harnessability, ambient affordances, harness templates, and Ashby's Law.

The earlier [Harness Engineering memo](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html) is useful because you can see the concept forming. Böckeler reacts to OpenAI's “no manually typed code” experiment, groups its harness into context engineering, architectural constraints, and garbage collection, and immediately notices the missing behaviour-verification piece. Read the memo after the main article if you want to understand how the polished model evolved.

Böckeler's [Context Engineering for Coding Agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html) is the companion piece. It explains reusable prompts, instructions, guidance, context interfaces, tools, MCP servers, skills, slash commands, subagents, and the need to keep context small. If harness engineering is the control system, context engineering is one of the main ways the control system reaches the model.

Fowler's [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html) and [Continuous Delivery](https://martinfowler.com/bliki/ContinuousDelivery.html) are older but load-bearing. They explain why fast automated feedback, self-testing builds, visible status, and deployable states matter. Böckeler's “keep quality left” section is easiest to understand if you already know CI/CD thinking.

Thoughtworks' [Architectural fitness function](https://www.thoughtworks.com/en-de/radar/techniques/architectural-fitness-function) gives the architecture half of the harness a name. A fitness function defines what “better” means for an architectural characteristic and checks it continuously. With agents, this becomes a way to stop architectural drift before human review.

## The broad definition: LangChain and agent frameworks

LangChain's [Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness) is the clearest broad definition: “Agent = Model + Harness.” It lists system prompts, tools, skills, MCPs, filesystem, sandbox, browser, orchestration, handoffs, hooks, middleware, compaction, continuation, and lint checks. It is less bounded than Böckeler's article, but it helps you see the full machinery.

The LangChain piece is especially good for working backwards from desired behaviour. If you want durable storage, you need filesystem and git. If you want action, you need tools and code execution. If you want safe execution, you need sandboxes. If you want current knowledge, you need search and context interfaces. If you want long-horizon work, you need planning, durable state, verification, and continuation. That behaviour-to-harness mapping is a practical design tool.

LangChain is also a vendor source. Treat its framework claims with normal skepticism. The conceptual anatomy is useful even if you do not adopt its library.

HumanLayer's [12 Factor Agents](https://github.com/humanlayer/12-factor-agents) is a practitioner/open-source bridge. Its most important contribution for this theme is the claim that good agents are mostly software, not magic loops. Factors such as owning your prompts, owning your context window, unifying execution state and business state, launch/pause/resume, contacting humans with tool calls, owning control flow, compacting errors into context, and keeping agents small all reinforce the harness mindset.

## Long-running work: Anthropic

Anthropic's [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) is the most concrete long-horizon source. It describes the shift-worker problem, the initializer agent, the coding agent, feature lists, `init.sh`, progress files, git commits, one-feature-at-a-time work, and browser automation. It is valuable because it names actual failure modes: one-shotting too much, running out of context with half-implemented work, and declaring victory too early.

Anthropic's [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) expands into evaluator agents and more complex harness design. The skeptical lesson is cost and calibration. Evaluators can help, but they are not free truth machines. They need checks against human judgement, especially for layout and behaviour.

Anthropic's [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) is broader than coding but useful for context budget, compaction, subagents, and just-in-time retrieval. It supports the same principle as Böckeler and OpenAI: high-signal context beats maximal context.

## Production narratives: OpenAI and Stripe

OpenAI's [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) is a primary source about OpenAI's own internal experiment. Its headline claims are dramatic: no manually written code, roughly a million lines, 1,500 PRs, and about one-tenth the time. Treat those metrics as context, not as promises.

The generalizable details are stronger: short `AGENTS.md` as map, structured docs as system of record, app legibility through browser and observability, architecture constraints enforced by custom linters and structural tests, taste invariants, quality score, and garbage collection against drift. OpenAI's diagrams are worth inspecting because they show what it means to make app UI, logs, metrics, traces, and architecture legible to Codex.

Stripe's [Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) is another primary production report. Its context is a huge mature codebase with unusual constraints. The generalizable details are isolated devboxes, integration with existing developer tooling, Slack/ticket/docs entry points, a web UI for minion decisions, deterministic orchestration around an agent loop, subdirectory-scoped rules, curated MCP tools, fast local lint feedback, selective CI, autofixes, and bounded CI retries.

OpenAI and Stripe agree on a deep point: the scarce resource is human attention. Harnesses exist to spend that attention where it matters.

## Security and failure sources

OWASP's [AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) should be treated as official security guidance. It gives the risk map: prompt injection, tool abuse, data exfiltration, memory poisoning, goal hijacking, excessive autonomy, cascading failures, denial of wallet, sensitive data exposure, and supply chain attacks. It also gives concrete controls: least privilege, input validation, memory security, human-in-the-loop approval, output validation, monitoring, multi-agent security, and data protection.

OWASP's [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) is the deeper prompt-injection reference. Use it when designing browser or document ingestion tools.

Arize's [Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) is a vendor/practitioner failure analysis. It is useful because it names operational failure modes that ordinary logs hide: retrieval noise, hallucinated tool arguments, recursive loops, guardrail failures, pre-training bias overriding retrieved context, schema drift, instruction drift, and code generation safety. Treat product-specific observability claims as vendor claims, but keep the failure taxonomy.

Patrick McCanna's [Bubblewrap sandboxing](https://patrickmccanna.net/a-better-way-to-limit-claude-code-and-other-coding-agents-access-to-secrets/) is a practical local-security source. It reinforces the idea that OS-level controls are more trustworthy than hoping an agent will not touch secrets.

## Practitioner learning patterns

Simon Willison's [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/) is valuable because it focuses on day-to-day practice: red/green TDD, first run the tests, agentic manual testing, linear walkthroughs, interactive explanations, subagents, anti-patterns, and using agents to produce better understanding. It is less about enterprise harness architecture and more about how an individual developer can work safely and learn faster.

The [linear walkthroughs](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/) chapter is especially relevant to this repo. Willison had an agent produce a structured walkthrough of code he had vibe-coded, with real snippets pulled by tools. That is the spirit of this guide: use agents not just to produce artifacts, but to convert dense source material into learning material.

The [approved fixtures](https://lexler.github.io/augmented-coding-patterns/patterns/approved-fixtures/) pattern by Ivett Ördög is small but important. It addresses the problem of reviewing AI-generated tests by moving review to domain-readable input/output fixtures. Keep it in mind whenever a behaviour harness would otherwise require humans to inspect generated assertion code.

## Background theory: cybernetics and variety

The [cybernetics](https://en.wikipedia.org/wiki/Cybernetics) article is reference background, not software practice. Its value is the feedback-loop frame: circular causal processes where outputs return as inputs and influence future action. Böckeler's steering loop is cybernetic in this sense.

[Ashby's Law of Requisite Variety](https://en.wikipedia.org/wiki/Variety_(cybernetics)#Law_of_requisite_variety) explains why topology constraints matter. A regulator needs enough variety to handle the system it regulates; only variety can absorb variety. In software terms, if your agent can generate almost anything and your codebase can take almost any shape, the harness has an impossible regulation problem. Standard topologies, templates, type systems, and architecture boundaries reduce variety so a harness can be strong enough.

## Community signals

Hacker News threads and local social-archive signals are useful for dissent. They surface worries about review burden, sandboxing, slop, cost, and long-term maintainability. They should not outweigh primary sources, but they keep the synthesis from becoming vendor-shaped optimism.

The practical way to use community signals is: treat them as leads to failure modes. If many practitioners complain about unreviewed slop, ask what harness evidence would reduce review toil. If people worry about sandboxing, read OWASP and sandboxing write-ups. If they distrust productivity claims, separate patterns from metrics.

## How to read next

If you have one hour, read:

1. [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html)
2. [Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)
3. [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
4. [OpenAI harness engineering](https://openai.com/index/harness-engineering/)
5. [Stripe Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)

If you are implementing, add:

- [Context Engineering for Coding Agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html)
- [AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [12 Factor Agents](https://github.com/humanlayer/12-factor-agents)
- [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/)

If you are skeptical, read the community threads in the source index and compare them against the vendor case studies.

## Chapter takeaways

- Fowler/Thoughtworks provides the conceptual spine.
- LangChain and HumanLayer explain the broader harness anatomy and software-engineering frame.
- Anthropic gives the best public long-running-agent pattern.
- OpenAI and Stripe give production evidence, strongest as patterns rather than ROI promises.
- OWASP and Arize keep the guide grounded in security and failure modes.
- Simon Willison and approved fixtures show how harness thinking improves individual practice and learning.

**Next:** [Chapter 13 — Open questions](13-open-questions.md).
