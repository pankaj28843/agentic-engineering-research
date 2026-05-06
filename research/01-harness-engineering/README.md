# Theme 01: Harness Engineering for Coding Agent Users

Harness engineering is the practice of designing the outer system around coding agents: instructions, tools, state, sandboxes, feedback loops, tests, evaluators, and human escalation paths. This theme starts from Birgitta Böckeler's Martin Fowler article and triangulates it against Anthropic, OpenAI, Stripe, LangChain, Simon Willison, OWASP, HN, and local social signals.

## Files

- [briefing.md](briefing.md) — evidence-weighted synthesis and skeptical verdict.
- [source-index.md](source-index.md) — human-readable source catalog.
- [research-log.md](research-log.md) — query batches, extraction notes, and limitations.
- [sources.json](sources.json) — machine-readable source metadata validated by `scripts/validate_research.py`.
- [open-questions.md](open-questions.md) — follow-up research agenda.

## One-sentence takeaway

Harness engineering is not a fancy synonym for prompt files: the strongest evidence points to a control-system discipline combining feedforward guidance, deterministic and inferential sensors, durable state, least-privilege execution, and human attention focused "on the loop" rather than micromanaging every generated line.

## Current confidence

High confidence that harness engineering is a useful organizing frame; medium confidence about the economics and generality of current vendor success stories; high confidence that behavior verification, security boundaries, and harness maintenance remain the hard unsolved parts.
