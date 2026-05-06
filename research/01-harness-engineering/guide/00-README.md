# Harness Engineering — an ELI5 Deep-Dive Guide

**You'll learn:** how to read this theme as a small private book, what each chapter covers, and where to jump when you want the source article behind a claim.

This guide is a plain-language, source-linked deep dive for an experienced software developer who is new to harness engineering. It is written as a reader's companion, not as a terse briefing. The goal is that you can read it on a phone, in an EPUB, or in printed form and come away understanding the meaty ideas in the crawled source set.

## The promise of this guide

Harness engineering is the discipline of building the system around a coding agent: instructions, tools, state, sandboxes, tests, browser evidence, observability, escalation paths, and the habit of turning repeated failures into durable controls. If that sounds broad, that is exactly why this guide exists. The term can mean “everything except the model,” as LangChain's [Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness) argues, or it can mean the narrower “outer harness” that a coding-agent user builds around a repository, as Birgitta Böckeler frames it in [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html).

The core reading path starts with Böckeler's Fowler article, then triangulates against [the earlier memo](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html), [context engineering for coding agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html), [Anthropic's long-running agent harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [OpenAI's Codex harness write-up](https://openai.com/index/harness-engineering/), [Stripe's Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents), [continuous integration](https://martinfowler.com/articles/continuousIntegration.html), [continuous delivery](https://martinfowler.com/bliki/ContinuousDelivery.html), [cybernetics](https://en.wikipedia.org/wiki/Cybernetics), [Ashby's Law of Requisite Variety](https://en.wikipedia.org/wiki/Variety_(cybernetics)#Law_of_requisite_variety), [architectural fitness functions](https://www.thoughtworks.com/en-de/radar/techniques/architectural-fitness-function), [approved fixtures](https://lexler.github.io/augmented-coding-patterns/patterns/approved-fixtures/), OWASP's [AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html), and practitioner material such as Simon Willison's [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/).

## Chapter map

1. [What is harness engineering?](01-what-is-harness-engineering.md) — the child-simple version, then the precise version.
2. [Model plus harness](02-model-plus-harness.md) — why the model is not the whole agent.
3. [Guides and sensors](03-guides-and-sensors.md) — feedforward, feedback, computational checks, inferential checks.
4. [Context engineering](04-context-engineering.md) — how the harness controls what the model sees.
5. [Quality left](05-quality-left-ci-cd.md) — how CI/CD thinking becomes agent feedback design.
6. [Three harness categories](06-maintainability-architecture-behaviour.md) — maintainability, architecture fitness, and behaviour.
7. [Long-running agents](07-long-running-agents.md) — durable state, feature lists, progress files, git commits, browser verification.
8. [Production case studies](08-production-case-studies.md) — OpenAI Codex and Stripe Minions, with caveats.
9. [Security boundaries](09-security-boundaries.md) — least privilege, sandboxing, prompt injection, memory poisoning, human approval.
10. [The human role](10-human-on-the-loop.md) — why the job shifts from typing code to steering the loop.
11. [Build your first harness](11-build-your-first-harness.md) — a practical starter recipe for a repo like this one.
12. [Reading the source set](12-reading-the-source-set.md) — annotated field notes for the major source families.
13. [Open questions](13-open-questions.md) — behaviour harnessing, harness coverage, drift, economics, and research gaps.
14. [Two-sentence summary](14-two-sentence-summary.md) — the compressed version you should remember.

## Source and scratch artifact policy

The clean article snapshots generated from captured browser HTML live under `tmp/`, not in git. Regenerate them with:

```bash
uv run python scripts/extract_theme_articles.py \
  research/01-harness-engineering \
  --scratch-root tmp/research-web-critical/agentic-engineering-harness-engineering
```

Build a private reading bundle with:

```bash
uv run python scripts/build_theme_book.py \
  research/01-harness-engineering \
  --formats markdown,epub
```

The source index remains in [source-index.md](../source-index.md); machine-readable metadata remains in [sources.json](../sources.json).
