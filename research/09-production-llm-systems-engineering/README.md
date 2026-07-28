# Production LLM Systems Engineering

This theme is a source-backed learning series for experienced full-stack
software engineers moving into AI engineering roles in 2026. It connects
application contracts, inference internals, retrieval and evaluation, and
production operations into one end-to-end mental model.

The durable reader is under [`guide/`](guide/00-README.md). The
[`briefing`](briefing.md) is a compact orientation before study and a better
recap after Part III; unfamiliar terms are defined in the guide. The
[`source index`](source-index.md) identifies retained evidence, and the
[`research log`](research-log.md) records search, extraction, review, and
publication decisions.

The current guide contains 22 linked chapters, a short
[model-vocabulary interlude](guide/03a-minimum-model-vocabulary.md), a
machine-readable [`capstone-v2` fixture](guide/lab-fixture.md), and more than
30,000 words. It is
organized from application/context foundations through inference, contracts,
RAG/evals, observability/cost, safety/isolation, adaptation, benchmarking, and
production reliability.

## Reader contract

- Explain every mechanism twice: first with an accurate everyday analogy,
  then with engineering vocabulary and implementation consequences.
- Assume strong web, distributed-systems, database, API, security, and
  observability experience; assume no prior model-serving expertise.
- Distinguish guarantees from best effort, benchmark results from production
  outcomes, and vendor claims from independent evidence.
- Name authors or organizations and recognizable source titles in citations
  so a reader can find the source even when a link is unavailable.
- End each chapter with a runnable design exercise, failure drill, or
  interview-style reasoning check.
