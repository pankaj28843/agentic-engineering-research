# OpenAI Harness Engineering

This packet is an OpenAI-centered study of harness engineering: the operating system around Codex that lets agents build, review, validate, and clean up software while humans steer at a higher level. It is not a refresh of [the broader harness engineering theme](../01-harness-engineering/README.md); that packet remains background context only.

Start with the guide:

- [Guide index](guide/00-README.md)
- [Executive briefing](briefing.md)
- [Source index](source-index.md)
- [Research log](research-log.md)
- [Asset credits](assets/README.md)

The central claim is narrow: OpenAI's story is not "a better prompt made a coding agent productive." The evidence points to a whole harness: per-worktree app instances, browser/CDP validation, local observability, repository-local knowledge, progressive disclosure, mechanical architecture checks, agent-to-agent review, Ralph-style loops, cleanup agents, and explicit safety boundaries.

## Reading Path

1. Read [chapter 01](guide/01-what-openai-means.md) for the OpenAI experiment and the ELI5 frame.
2. Read [chapter 02](guide/02-legible-apps-and-browsers.md) and [chapter 03](guide/03-repository-knowledge.md) for the two biggest replicable moves: make the app observable to the agent, and make the repository the system of record.
3. Read [chapter 04](guide/04-invariants-and-lints.md), [chapter 05](guide/05-review-and-ralph-loops.md), and [chapter 06](guide/06-symphony-orchestration.md) for the control system.
4. Read [chapter 08](guide/08-replication-playbook.md) if you want Linux/macOS implementation steps.
5. Read [chapter 09](guide/09-capabilities-costs-and-unknowns.md) for current official-plan comparison, autonomy boundaries, and unknowns.

## Evidence Boundaries

- The OpenAI blog post is primary evidence for the internal Codex harness experiment.
- The OpenAI diagrams are copied locally for private study and credited in [assets/README.md](assets/README.md).
- Symphony is treated as public source-code evidence for a scheduler/runner pattern, not as proof that OpenAI's private internal harness is implemented the same way.
- Five YouTube transcripts are used as transcript evidence. One requested video has no usable transcript in the local capsule and is recorded as an access limitation.
- YouTube comments and X/Twitter posts are weak social signal only.
- Subscription and product-capability claims use official OpenAI and Anthropic pages, with fetch dates and uncertainty recorded.

