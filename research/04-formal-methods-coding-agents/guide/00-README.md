# Formal Methods for Coding Agents — an ELI5 Deep-Dive Guide

**Audience:** a software developer who has used coding agents, tests, CI, and type checkers, but has not used formal methods seriously.
**Promise:** by the end, you should be able to explain what formal methods are, why they matter for coding agents, where people are using them now, and how to start without pretending that every program needs a PhD-level proof.

## The tiny version

A coding agent is like a very fast junior developer who can type, search, run tools, and sometimes surprise you. Formal methods are like extremely picky checkers that ask, “What exactly should always be true?” and then try to prove or disprove that claim using mathematics.

Testing asks: “Did the program work on the examples I tried?”

Formal methods ask: “Can we prove this property for all the cases in the model?”

That difference matters because LLMs are good at producing plausible artifacts: code, explanations, specs, proofs, and plans. Plausible is not the same as correct. The useful modern pattern is therefore not “trust the LLM.” It is:

```text
human intent
  -> LLM drafts a spec / proof / code / plan
  -> formal or semi-formal tool checks it
  -> counterexample or error returns to the agent
  -> agent repairs
  -> human reviews the meaning of the spec
```

NASA’s plain definition is still the best starting point: formal methods are mathematically rigorous techniques and tools for specification, design, and verification, where specifications are well-formed statements in mathematical logic and verification steps can be mechanically checked ([NASA](https://shemesh.larc.nasa.gov/fm/fm-what.html)). NASA also warns that whole real systems are usually too complex to examine completely, so practitioners abstract, target critical components, and automate what they can.

## Chapter map

1. [The toy box version: what formal methods are](01-the-toy-box-version.md) — tests vs proofs, properties, models, and why “prove everything” is the wrong mental model.
2. [Why coding agents make this urgent](02-why-coding-agents-make-this-urgent.md) — the intent gap, abundant AI-generated code, and why verification becomes the job.
3. [The main tools: specs, model checkers, proof assistants, verifiers](03-the-main-tools.md) — Dafny, TLA+, Lean, model checking, theorem proving, runtime monitors.
4. [The generate-check-repair loop](04-generate-check-repair-loop.md) — how LLMs and formal tools complement each other.
5. [Verified code generation with Dafny](05-dafny-and-verified-code-generation.md) — DafnyBench, dafny-annotator, DafnyPro, NL2VC, and VS Code-style workflows.
6. [Proof-search agents with Lean and Coq](06-proof-search-agents.md) — COPRA, Prover Agent, minimal proof agents, and why the proof assistant kernel matters.
7. [Model-checking agent workflows with TLA+](07-model-checking-agent-workflows.md) — states, transitions, TLA+, SysMoBench, and the hard problem of conformance.
8. [Runtime verification and tool-use policies](08-runtime-verification-and-tool-policies.md) — AgentGuard, AgentRaft, AgentVerify, SEVerA, and what to monitor around coding agents.
9. [What people have actually used in the last six months](09-how-people-use-it-now.md) — research patterns, open-source tools, HN signals, and adoption reality.
10. [A beginner cookbook for a coding-agent user](10-beginner-cookbook.md) — how to introduce contracts, policies, and verification gates in practical layers.
11. [A small worked example: refund rules for an agent](11-worked-example-refund-agent.md) — turning informal requirements into contracts, temporal rules, and monitors.
12. [The traps: wrong specs, vacuous proofs, cheating, and hype](12-traps-and-limitations.md) — the skeptical chapter.
13. [Glossary and next reading path](13-glossary-and-next-reading.md) — compressed memory hooks and source-linked reading plan.

## How to read

If you only have 20 minutes, read chapters 1, 2, 4, 8, and 12. If you want to apply this to a coding-agent harness, read chapters 10 and 11 carefully. If you want the research frontier, read chapters 5 through 9 with the source links open.

## Scratch artifacts

The browser captures and article snapshots used to write this guide live under:

```bash
tmp/research-web-critical/formal-methods-coding-agents/
```

Regenerate clean article snapshots with:

```bash
uv run python scripts/extract_theme_articles.py \
  research/04-formal-methods-coding-agents \
  --scratch-root tmp/research-web-critical/formal-methods-coding-agents
```

Build a private reading bundle with:

```bash
uv run python scripts/build_theme_book.py \
  research/04-formal-methods-coding-agents \
  --formats markdown,epub
```
