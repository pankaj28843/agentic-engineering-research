# Open Questions: Harness Engineering

## Behavior harnesses

- Which patterns reliably validate functional behavior when the tests themselves are agent-authored?
- Where do approved fixtures outperform Gherkin-style specs, screenshots, or LLM judges?
- Can mutation testing, property testing, and browser-driven user journeys be made cheap enough for frequent agent loops?

## Evaluator agents

- How should evaluator prompts be calibrated against human judgment?
- When does a separate evaluator add value versus becoming expensive theater?
- What traces should be kept so an evaluator's misses can improve the harness?

## Harness economics

- Which harness components are load-bearing for small teams versus enterprise-scale codebases?
- How should teams measure ROI beyond PR counts and token spend?
- What is the break-even point for custom linters, structural tests, and doc-gardening agents?

## Security boundaries

- What is the minimum safe sandbox for local coding agents with browser and shell access?
- How should MCP tools be classified by risk and routed through human approval?
- How can prompt-injection and memory-poisoning tests become routine harness sensors?

## Harness maintenance

- How do teams keep `AGENTS.md`, skills, docs, tests, and custom tools coherent as they evolve?
- Can meta-harness systems safely propose changes to the harness itself?
- What should a "harness coverage" metric look like, analogous to test coverage or mutation score?

## Follow-up source targets

- Meta-Harness paper and artifact.
- SlopCodeBench paper.
- Stripe Minions Part 2.
- Cursor long-running agents preview.
- Open-source harness repositories from `walkinglabs`, `ai-boost`, and `humanlayer`.
