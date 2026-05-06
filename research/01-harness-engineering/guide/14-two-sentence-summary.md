# Chapter 14 — Two-sentence summary

**You'll learn:** the compressed version of the entire guide, plus a short memory checklist for future work.

Harness engineering is cybernetic software engineering for coding agents: build feedforward guides that make good work more likely, feedback sensors that make bad work visible early, and a steering loop that turns repeated failures into durable improvements. A useful harness is not a giant prompt file; it is a coherent control system of context, tools, state, sandboxes, tests, evaluators, docs, permissions, evidence, and human judgement focused where it has the most leverage.

## If you remember only one diagram

```text
         ┌──────────────┐
         │ Human intent │
         └──────┬───────┘
                ▼
      ┌───────────────────┐
      │ Feedforward guide │  AGENTS.md, skills, specs, examples,
      │ before action     │  architecture docs, templates
      └──────┬────────────┘
             ▼
      ┌───────────────────┐
      │ Coding agent      │  model + harness, acting in a sandbox
      └──────┬────────────┘
             ▼
      ┌───────────────────┐
      │ Feedback sensor   │  tests, linters, browser, logs,
      │ after action      │  reviewers, evaluators, humans
      └──────┬────────────┘
             ▼
      ┌───────────────────┐
      │ Harness update    │  encode the lesson as docs, checks,
      │ after repeated    │  tools, templates, or permissions
      │ failures          │
      └───────────────────┘
```

## The memory checklist

- **Model plus harness:** if it is not the model, it is part of the harness.
- **Guides and sensors:** prevention and correction both matter.
- **Computational first:** use deterministic checks where possible.
- **Inferential when needed:** use LLM judgement for semantics, calibrated by humans.
- **Context is scarce:** make `AGENTS.md` a map, not an encyclopedia.
- **Quality left:** run cheap checks early; cap expensive retries.
- **Behaviour is hardest:** green generated tests are not enough.
- **Long tasks need durable state:** feature lists, progress notes, git commits, baseline checks.
- **Security is outside the model:** least privilege, sandboxing, approval, monitoring.
- **Humans stay accountable:** move human attention to judgement and harness improvement.
- **Research output should teach:** every theme should become a source-linked ELI5 deep dive.

## Final source jumps

Start with Birgitta Böckeler's [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html). Then read LangChain's [Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness), Anthropic's [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), OpenAI's [Harness engineering](https://openai.com/index/harness-engineering/), Stripe's [Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents), OWASP's [AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html), and the [approved fixtures](https://lexler.github.io/augmented-coding-patterns/patterns/approved-fixtures/) pattern.
