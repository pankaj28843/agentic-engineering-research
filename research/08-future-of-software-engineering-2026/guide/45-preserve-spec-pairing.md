# 45. Preserve spec-pairing

> **Report point:** Team design, bullet 45, page 12 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** Shared reasoning is a credible mechanism to preserve; spec-pairing has not been shown to improve team outcomes.

When an agent performs much of the implementation, pairing on every keystroke can feel artificial. Abandoning collaboration altogether creates a different risk: the person operating the agent sees the assumptions, alternatives, and failures, while everyone else sees only a polished patch.

The useful move is to pair where shared judgment has leverage. Collaborators frame the outcome, expose domain constraints, challenge risky assumptions, and agree on evidence for acceptance. The agent can then generate candidates inside that jointly understood boundary. This is a practice hypothesis, not a proven replacement for conventional pairing.

## A plain-language model: pair around commitments

A specification is not a large requirements document. It is the smallest shared account of:

- the outcome that should change;
- the constraints that must remain true;
- examples that distinguish acceptable from unacceptable behavior;
- uncertainties and rejected alternatives;
- the evidence and owner needed to accept the consequence.

Spec-pairing means two people make those commitments legible before or during agent-assisted implementation. One person should understand the domain or operational consequence; the other should be able to challenge the framing. They may be engineers, product collaborators, operators, designers, security specialists, or domain experts. Seniority alone does not make a good pair.

This shifts collaboration from “watch me type” to “help me decide what this change means.” It does not imply that implementation is clerical. Difficult debugging, unfamiliar technology, and novel algorithms may still deserve close implementation pairing.

## What the evidence permits

Observed work shows that AI changes interaction patterns. In a [13-interview study of generative-AI users](https://arxiv.org/html/2405.01543v1), participants described using AI as a rubber duck, iterating through corrections, and sometimes relying less on human collaboration. Because recruitment selected existing users and measured no team outcomes, the study supports a redistribution-of-conversation hypothesis, not a claim that AI causes silos.

A [workplace case covering two teams](https://scholarspace.manoa.hawaii.edu/bitstreams/4f29b0c8-06ac-4d5d-9fa0-52eb93321eb2/download) observed 28 people, including 15 developers, over 49 programming sessions in 25 observation days. Humans tended to handle more domain questions in paired work while AI handled more technical questions. Pairing was not randomized, task mixes differed, and no retained-learning or ownership outcome was measured.

A controlled [study of 19 advanced students](https://www.se.cs.uni-saarland.de/publications/docs/WSD+.pdf) counted more annotated “knowledge-transfer episodes” in human–human sessions than human–AI sessions. An episode was a perceived gap and an attempt to address it, not knowledge gained or remembered. It would be incorrect to turn the episode counts into proof that human pairing transfers more knowledge.

The [agentic-codebase principles](https://maintainable.software/agentic-engineering-part-2-agentic-codebase-principles/) provide useful design vocabulary—locality, explicit boundaries, navigability, and verifiability—but are a conceptual framework rather than comparative evidence. Together these sources justify preserving explanation and challenge as mechanisms to test. They do not establish that spec-pairing improves inclusion, quality, delivery, learning, or collective ownership.

## Choose a bounded pilot

Start with one team, one work class, and four to six weeks. Suitable work has meaningful domain or operational choices but is not an emergency. Avoid mandating the practice across every task before learning whether it helps.

Declare three comparison paths:

1. **Live spec-pairing:** two collaborators frame and challenge synchronously.
2. **Asynchronous specification review:** one person drafts; another comments and must resolve material uncertainty before implementation.
3. **Solo with sampled review:** a person works alone, while a subset of changes receives the same post hoc understanding check.

These are not clean experimental treatments unless work is assigned comparably. At minimum, tag task risk, novelty, and size so the team does not compare a risky paired migration with a trivial solo rename and announce a winner.

Before the pilot, choose a privacy-safe way to identify who participated and how. Do not require raw agent transcripts as proof of labor. The artifact should expose decisions, not surveil the entire interaction.

## Run a 25-minute specification session

Use a short shared template:

1. **Outcome:** one sentence describing the user or system change.
2. **Invariants:** what must not change, including security, data, performance, and operational limits.
3. **Examples:** at least one normal, boundary, and failure case.
4. **Unknowns:** questions that would invalidate the plan.
5. **Options:** the chosen approach and one credible alternative.
6. **Acceptance evidence:** tests, observations, review, rollout, and rollback needed.
7. **Ownership:** who can approve, operate, and explain the result.

Assign two roles. The **framer** proposes and records the model. The **challenger** probes ambiguity, counterexamples, and hidden dependencies. Rotate the roles across changes; otherwise one person becomes the permanent author and the other a ceremonial reviewer. The challenger must contribute at least one material question or explicitly state why none was found. Quantity is not the goal—the rule simply makes passive attendance visible.

Only after the core boundary is understood should the agent generate alternatives or implementation. If the agent surfaces a new architectural choice, pause and update the shared specification rather than letting the private agent conversation silently redefine the work.

## Keep implementation connected to the pair

Spec-pairing fails if its artifact is abandoned at implementation time. Link every candidate to the examples and invariants. When a candidate violates or expands them, return to the pair or asynchronous reviewer. Record rejected alternatives briefly, especially when the rejection reflects domain knowledge not obvious in code.

At review, someone other than the operator should explain the change from the specification before inspecting the operator’s explanation. This is a sample of shared understanding, not a test of an individual. A reviewer who cannot explain the intended outcome and first rollback action has found an ownership gap, even if the patch is technically correct.

For distributed teams, use an asynchronous two-pass protocol. The framer posts the template; the challenger gets a protected response window and can mark “ready,” “needs decision,” or “cannot review.” Time-zone delay and accessibility are costs to measure. Do not force a live call where a written artifact gives quieter or non-native speakers a better chance to challenge.

## Measure functions rather than attendance

Compare the three paths using a balanced scorecard:

- **Shared understanding:** after a delay, can two participants and one likely maintainer independently state outcome, key constraint, and rollback?
- **Decision quality:** how many material ambiguities or alternatives were resolved before implementation, and how many returned later as rework?
- **First-pass acceptance:** accepted candidates divided by submitted candidates, with the denominator visible.
- **Rework and defects:** clarification loops, rejected candidates, rollbacks, incidents, and repair time.
- **Ownership distribution:** how many people can review, operate, or modify the area without the original operator?
- **Inclusion:** who speaks, authors, challenges, or opts for asynchronous participation; collect qualitative reports of dominance and accessibility barriers.
- **Cost:** elapsed coordination time, waiting, interruption, and implementation time.

Do not combine these into one “collaboration score.” More interaction can coexist with worse inclusion; a faster decision can concentrate ownership; a longer session can prevent expensive rework. Review the outcomes separately.

Use a delayed sample rather than an immediate recital. Ask participants about a change one or two weeks later and after an ownership rotation. This still does not establish durable learning, but it is closer to the claimed function than counting messages or meeting minutes.

## Failure signals and counterexamples

Spec-pairing is failing when the challenger merely edits wording, the same senior person decides every tradeoff, the agent has already fixed the solution before discussion, or the template expands into a ceremony for trivial work. It is also failing when coordination delays outweigh any reduction in rework, when people cannot participate accessibly, or when private reasoning remains essential to operate the result.

There are legitimate exceptions. A reversible low-risk edit with strong automated checks may need only asynchronous sampling. An incident may require one accountable operator to act immediately and document decisions afterward. A research spike can stay deliberately open-ended. Conversely, unfamiliar or irreversible work may require more than a pair: include the relevant domain, security, or operations authority.

An agent can also reduce isolation in some contexts by helping a person rehearse questions or obtain low-stakes explanations. The interview evidence includes such rubber-duck use. That possibility is another reason to compare functions rather than declaring human interaction inherently superior.

## Stop, adapt, or roll back

Define stop rules before launch. Pause the pilot if downstream rework or failure rises materially across two review windows, if specification wait becomes the dominant delay without a compensating outcome, or if participants report repeated exclusion or coercion. Stop immediately if artifacts become individual evaluation evidence or if people are pressured to expose private prompts beyond what the work requires.

Adapt by reducing scope, moving to asynchronous review, rotating roles, or raising the risk threshold for mandatory pairing. If the practice still adds ceremony without measurable shared reasoning, return to the previous workflow and retain only the useful artifact fields. Preserve the collected aggregates and delete unnecessary person-level participation data according to the pilot contract.

Success is not “everyone paired.” A credible local result is narrower: for a defined class of work, a defined collaborative path produced more recoverable reasoning or distributed ownership without unacceptable delivery, inclusion, or quality cost. The unresolved evidence gap remains: no selected workplace study shows that spec-pairing causes those outcomes over time.

## The practical artifact: a specification handoff card

Before implementation proceeds, the pair should be able to hand another teammate this compact card:

- Outcome and accountable owner
- Three invariants or constraints
- Normal, boundary, and failure examples
- Largest uncertainty
- Chosen and rejected approach
- Acceptance and rollback evidence
- People who can explain and operate the change

If the card cannot be completed, the work may not be ready for rapid candidate generation. If it is complete but no one beyond the operator can explain it later, the pairing practice did not perform its intended function.

Podcast hook: If an agent writes the patch, what exactly should two humans still do together—and how can they tell whether shared reasoning survived?

Continue reading: [Chapter 14: Superpowered silos versus spec-pairing teams](14-superpowered-silos-vs-spec-pairing.md) examines the evidence and uncertainty behind this practice.
