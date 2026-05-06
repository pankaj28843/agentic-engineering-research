# Chapter 01 — What is harness engineering?

**You'll learn:** the simplest mental model for harness engineering, why the phrase matters, and why a good harness is not just a big prompt file.

Source jumps: Böckeler's main [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html), the earlier [Harness Engineering memo](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html), LangChain's [Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness), and OpenAI's [Harness engineering](https://openai.com/index/harness-engineering/).

## The five-year-old version

Imagine a very clever robot helper. The robot can read, write, and use tools, but it has no common sense about your house. It does not know which drawer has the scissors, which vase is expensive, which door leads outside, or which messes are dangerous. If you say, “clean the room,” it might do something useful, but it might also throw away your homework.

A harness is the child-safe room you build around the robot: labels on drawers, soft bumpers on corners, a rule that says “ask before opening the front door,” a checklist for what “clean” means, and sensors that beep if it tries to put toys in the oven. Harness engineering is the work of designing those labels, bumpers, checklists, and beeps so the robot can help more and hurt less.

For coding agents, the “room” is a software repository. The “drawers” are source files, tests, docs, tools, browsers, logs, CI pipelines, issue trackers, and deployment systems. The “robot” is a coding agent such as Claude Code, Codex, Cursor, Copilot coding agent, Aider, Cline, or a custom agent loop. Harness engineering is the discipline of making that environment legible, constrained, and self-correcting.

## The precise version

Böckeler defines the useful bounded context: in agent products, some harness already exists inside the product. The product provider builds a system prompt, retrieval mechanism, tool protocol, context-management logic, and orchestration loop. But coding-agent users still build an *outer harness* for their own codebase and risk profile. That outer harness includes instructions, skills, tools, tests, static analysis, browser checks, architecture rules, docs, and human escalation rules. The purpose is to increase the probability of a good first attempt and to let the agent self-correct before the result reaches human review.

LangChain uses the broader slogan: [“Agent = Model + Harness”](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness). In that definition, everything that is not the model is the harness: system prompts, tools, skills, MCP servers, filesystem, sandbox, browser, orchestration, hooks, compaction, continuation, lint checks, and memory. That broad definition is useful because it reminds us that a model alone is not an agent. A model takes input and emits output. An agent needs machinery around it to remember state, call tools, inspect results, and keep going.

But the broad definition can become so wide that it stops helping. If “harness” means everything, then it explains nothing. The Fowler article narrows the word to the part a team can deliberately engineer around a coding agent. This repository uses that narrower meaning most of the time: *the repo-local and workflow-local control system that makes coding agents safer, more useful, and easier to supervise*.

## Why the term appeared now

The term matters because the industry conversation was stuck on models. People asked which model writes the best React, which model has the longest context window, and which model hallucinates least. Those questions matter, but they miss the other half of the system. OpenAI's Codex team reports building an internal product with no manually typed code, but the important lesson in [their write-up](https://openai.com/index/harness-engineering/) is not “the model is magic.” It is that the team spent its effort designing environments, feedback loops, architecture constraints, repository knowledge, custom linters, browser tooling, observability, and cleanup agents.

Stripe's [Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) show the same pattern from a different organization. Stripe is not asking a generic chatbot to edit a hundreds-of-millions-line codebase with a prayer. It runs minions in isolated devboxes, feeds them internal context through curated tools, interleaves deterministic git/lint/test orchestration with agent loops, and gives them fast local feedback before bounded CI retries. The agent is only useful because the surrounding engineering system is serious.

Böckeler's memo noticed this in OpenAI's article before the full Fowler piece. She grouped OpenAI's harness into context engineering, architectural constraints, and “garbage collection” against entropy. She also spotted the missing piece: functional behaviour verification. Internal maintainability can be checked by many existing tools; verifying that the application does what users need is harder.

## What a harness is not

A harness is not a giant prompt file. A giant prompt file is often a symptom that the team has not built a real harness yet. OpenAI explicitly says its “one big AGENTS.md” approach failed because context is scarce, too much guidance becomes non-guidance, monolithic docs rot, and blobs are hard to verify. Their replacement is a short AGENTS.md as a table of contents plus a structured docs directory with design docs, execution plans, generated references, product specs, quality scores, reliability docs, and security docs.

A harness is also not just a test suite. Tests are sensors: they report something after the agent acts. A good harness also has guides: material that steers the agent before it acts. And a harness is not just an agent framework. Frameworks can provide loops, graphs, state machines, and tool abstractions, but the repo-specific knowledge of “what good looks like here” still has to come from the team.

Finally, a harness is not a guarantee. Böckeler is careful about this. Harnesses externalize part of what experienced human developers carry implicitly: conventions, taste, organizational memory, judgement about trade-offs, and discomfort when code smells wrong. They can reduce review toil and move human attention to higher-leverage points, but they cannot remove human responsibility.

## The steering loop

The simplest useful diagram is this:

```text
human intent
   │
   ▼
feedforward guides ──► coding agent ──► changed code/docs/tests
   ▲                      │
   │                      ▼
harness updates ◄── feedback sensors ◄── test/lint/browser/review evidence
```

The human does not disappear. The human moves from typing every line to steering the loop. When the agent fails in a repeated way, the human asks: what was missing from the harness? A clearer rule? A smaller task shape? A structural test? A linter with an agent-readable error message? A browser screenshot? A safer tool permission? A checklist before finishing?

This is why harness engineering feels like old engineering in new clothes. It borrows from continuous integration, continuous delivery, static analysis, architecture fitness functions, security least privilege, observability, and operations. The new thing is that the consumer of those signals is often an LLM, so the signals need to be both machine-checkable and model-legible.

## A concrete mini-example

Suppose a coding agent keeps adding new helper functions inside random files. A human reviewer repeatedly says, “we already have a shared utility package; use that.” In a prompt-only workflow, this becomes reviewer fatigue. In a harness-engineering workflow, the team turns the failure into controls:

1. A short guide in `AGENTS.md` points to `docs/architecture.md`.
2. `docs/architecture.md` explains where shared utilities live and gives examples.
3. A static check flags duplicate helper names or forbidden import directions.
4. The linter error tells the agent exactly how to fix it: “move this helper to package X or import existing helper Y.”
5. A reviewer skill tells the agent to inspect the diff for new local helper functions before asking humans to review.
6. If the problem still recurs, the team strengthens the computational check rather than adding more prose.

That is harness engineering. The important move is not “write a better prompt.” The important move is “make the desired behaviour part of the environment.”

## Why this matters for this research repo

This repository was initially set up like a research notebook: crawl sources, write a short briefing, keep source metadata. That is not enough. If we burn tokens and browser time to crawl meaty articles, the durable output should be a meaty reader's guide. The briefing still has value as an executive summary, but the main artifact should be a chapter-wise deep dive that teaches the theme from first principles and links back to the original sources.

So the repository's own harness is changing. Future themes should not stop at “verdict, evidence, failure modes.” They should include an ELI5 deep-dive guide, source-linked chapters, local image credits when diagrams are used, extracted article snapshots in `tmp/`, and optional private publishing to EPUB. The point is not to collect links. The point is to turn fast-moving agentic engineering material into personalized reading material that compounds.

## Chapter takeaways

- A model is not an agent; the harness is the system that lets the model act, observe, remember, and self-correct.
- The most useful bounded meaning here is the outer harness a team builds around a coding agent and repository.
- A harness includes guides before action and sensors after action; prompt files alone are not enough.
- The human role shifts from line-by-line production to steering and improving the loop.
- This repo should produce book-like ELI5 deep dives, not just short briefings.

**Next:** [Chapter 02 — Model plus harness](02-model-plus-harness.md).
