# Future of Software Engineering 2026: A Skeptical Reader and Field Guide

This guide expands every literal bullet in Thoughtworks' 2026 European
retreat report into its own source-linked chapter. It preserves the report's
agenda while testing its claims against primary research, official artifacts,
practice evidence, counterexamples, and explicit negative findings.

There are **53 numbered report-bullet chapters**, **six management
interludes**, and this index: **60 Markdown files** when complete. Interludes
carry lettered filenames and are visibly labeled “not a report bullet.”

## Three reading routes

For the fast orientation, read Chapters 01–05, the six management interludes,
and the [briefing](../briefing.md).

For the evidence route, read 06–35. These chapters distinguish what a study,
policy, case, or perspective actually establishes from the retreat's
interpretation.

For the implementation route, read 36–53. Each playbook has prerequisites,
measures, exception paths, failure signals, and a stop or rollback rule. A
recommendation is a bounded experiment, not a universal mandate.

## Part 0 — Five claims that organize the report

1. [When trust becomes the constraint](01-verification-is-the-bottleneck.md)
2. [Harness engineering becomes a discipline](02-harness-engineering-discipline.md)
3. [The apprenticeship cliff](03-apprenticeship-cliff.md)
4. [Boardroom confidence versus engineering reality](04-executive-engineer-gap.md)
5. [Why legacy modernization is near-term value](05-legacy-modernization-value.md)

[Management interlude — sequence discipline before acceleration](05a-management-sequence-discipline.md)

## Part 1 — What survives evidence review

### Verification

6. [Constraint tests and human-legible approval rigs](06-constraint-tests-approval-rigs.md)
7. [Three layers of migration trust](07-three-layers-migration-trust.md)
8. [Hybrid evals and councils of judges](08-hybrid-evals-council-judges.md)
9. [Does manual code review work?](09-manual-code-review-evidence.md)

### Harness engineering

10. [What the 4x and 90% harness claims really show](10-harness-4x-90-percent-claims.md)
11. [Self-improving harnesses and the learn loop](11-self-improving-harnesses.md)
12. [Who owns the harness?](12-harness-ownership.md)

### Team design

13. [The two clocks of agentic delivery](13-two-clocks.md)
14. [Superpowered silos versus spec-pairing teams](14-superpowered-silos-vs-spec-pairing.md)
15. [Can platform teams earn agentic credibility?](15-platform-agentic-credibility.md)
16. [Domain-driven design at agentic speed](16-ddd-agentic-speed.md)

### Apprenticeship and learning

17. [Design quorums, non-AI drills, and orchestration curricula](17-apprenticeship-countermeasures.md)
18. [The squeezed seven-to-ten-year cohort](18-mid-career-identity-strain.md)
19. [Does LLM use erode critical thinking?](19-llm-critical-thinking.md)

### Legacy modernization

20. [Port first, improve second](20-port-first-improve-second.md)
21. [Bespoke compilers become affordable](21-bespoke-compilers-affordable.md)
22. [Turning modernization into board-legible investment](22-board-legible-modernization.md)

### The expectation gap

23. [Stories, benchmarks, and executive learning](23-stories-benchmarks-executive-learning.md)
24. [Security incidents and token-budget shock](24-security-token-budget-shock.md)
25. [Two-to-three-times, ten-times, and the predicted bubble](25-productivity-hype-bubble.md)

[Management interlude — manage the story, not just the metric](25a-management-story.md)

### Governance

26. [Risk tiers plus detection over prevention](26-risk-tiers-detection.md)
27. [Slopsquatting and hallucinated dependencies](27-slopsquatting.md)
28. [Delay, registries, microVMs, and internal zero trust](28-layered-supply-chain-mitigations.md)

### Tokenomics and sovereignty

29. [The 1,400x tokenomics claim](29-tokenomics-1400x.md)
30. [The hidden specialization of self-hosting](30-self-hosting-specialization.md)
31. [A middle path for coding inference](31-coding-inference-middle-path.md)

[Management interlude — token and infrastructure economics as governance](31a-management-token-governance.md)

### Open source

32. [Reimplementing contribution intent from scratch](32-reimplement-contribution-intent.md)
33. [Will open source shift from code to specs?](33-open-source-code-to-specs.md)

### Conspicuously human

34. [Cameras, drum machines, and centaurs](34-historical-human-machine-analogies.md)
35. [Keeping human judgment in the loop](35-human-judgment-loop.md)

[Management interlude — protect differentiated human value](35a-management-human-value.md)

## Part 2 — Bounded implementation playbooks

### Testing and verification

36. [Replace generic BDD with simple approval rigs](36-replace-generic-bdd.md)
37. [Make three-tier verification the migration default](37-default-three-tier-verification.md)
38. [Coverage, adversarial probing, then mutation testing](38-coverage-adversarial-mutation.md)
39. [Measure code review or stop calling it a guarantee](39-measure-code-review.md)

### Harness and context engineering

40. [Turn lint findings into agent instructions](40-lint-to-agent-instructions.md)
41. [Operationalize a learn loop](41-operationalize-learn-loop.md)
42. [Govern and prune shared skills](42-govern-prune-shared-skills.md)
43. [Narrow schema-defined tools for infrastructure agents](43-narrow-infrastructure-tools.md)

### Team design and ways of working

44. [Instrument the two clocks](44-instrument-two-clocks.md)
45. [Preserve spec-pairing](45-preserve-spec-pairing.md)
46. [Tier autonomy by risk and reversibility](46-tier-autonomy.md)
47. [Build an opinionated agentic paved road](47-agentic-paved-road.md)

### People and skill formation

48. [Run design quorums deliberately](48-run-design-quorums.md)
49. [Add non-AI learning checkpoints](49-non-ai-learning-checkpoints.md)
50. [Support the mid-career cohort](50-support-mid-career-cohort.md)

### Governance

51. [Operationalize green, amber, and red governance](51-operationalize-risk-tiers.md)

[Management interlude — calibrate autonomy to risk](51a-management-risk-calibrated-autonomy.md)

52. [Treat agent-generated application code as untrusted](52-agent-generated-application-code-untrusted.md)
53. [Delay and screen new dependencies](53-delay-screen-dependencies.md)

[Management interlude — plan for a compressed hype cycle](53a-management-compressed-hype-cycle.md)

## How claims are labeled

- **Established here** means a retained source directly supports the bounded
  statement after its method and limits are included.
- **Inference** connects multiple sources or transfers a mechanism; the text
  says so.
- **Retreat claim** preserves what participants reported without turning an
  anonymous recollection into independent evidence.
- **Hypothesis** is a proposition worth testing.
- **Negative finding** records that a targeted audit did not locate adequate
  support.

The [source index](../source-index.md) and [research log](../research-log.md)
show how those judgments were made.
