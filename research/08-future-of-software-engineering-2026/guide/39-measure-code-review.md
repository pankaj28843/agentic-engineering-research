# 39. Measure code review without teaching people to game it

> **Report point:** Playbook, bullet 39, pages 11–12 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Playbook judgment:** Measure the path from concern to verified outcome, alongside learning, design change, latency, and reviewer load. Comment counts and “defects found” are unsafe primary targets.

Code review is asked to do several jobs at once: catch defects, challenge intent, improve design, spread knowledge, enforce policy, and establish accountability. A metric that mixes those jobs produces a reassuring number and a weak decision.

The simplest counts are especially dangerous. More comments can mean deeper review, noisier automation, contentious style preferences, or worse initial changes. Fewer defects can mean better code, shallower inspection, or reclassification. Faster merge can mean efficient collaboration or premature approval.

This playbook builds a balanced review measurement system. Its purpose is not to rank reviewers or prove that humans beat agents. It is to decide which review mode adds independent value for which change class, at what cost.

## Plain mental model: measure the chain and the counterweight

Review is a chain:

```text
change → inspection → valid concern → resolution → independent verification
       → downstream result
```

Every link needs a denominator. “Ten findings” means little without the number and risk of changes reviewed, whether findings were valid and novel, whether fixes worked, and what escaped.

Every quality measure also needs a counterweight:

| Desired signal | Counterweight |
|---|---|
| More valid findings | False alarms and duplicate findings |
| Faster merge | Escaped defects and rework |
| Broad review coverage | Reviewer load and depth |
| More reviewers | Coordination latency and diffusion of responsibility |
| More agent comments | Human triage time and correlated misses |
| Fewer production defects | Change mix, exposure, and reporting delay |

The governing question is not “did review happen?” It is “what additional, independently verified outcome did this review mode contribute?”

## Establish a baseline before changing policy

Use a fixed recent window—long enough to include meaningful production exposure—and stratify changes by risk, size, novelty, component maturity, and authoring mode. Do not compare an agent’s routine dependency bumps with humans’ high-risk architectural changes.

For each sampled change, record:

- review mode: synchronous pairing, asynchronous human, agent, hybrid, deterministic gate, or exception;
- risk and reversibility;
- authoring mode, without using it as an individual performance label;
- time waiting for first review, active review time, author rework time, and total merge latency;
- concerns by class: correctness, security, operability, architecture, requirement, policy, maintainability, and style;
- concern validity, novelty, severity, and disposition;
- independent evidence that a resolution worked;
- post-merge rework, rollback, incident, or escaped defect during the observation window;
- knowledge or ownership outcome, sampled rather than guessed.

Normalize time by active effort and waiting. A review that takes twenty minutes of attention after a two-day queue has two distinct costs.

## Define the metrics before seeing results

### 1. Verified concern yield

Count concerns confirmed by an independent signal or accountable domain decision, divided by review effort. Split out findings already caught by another required check. A static analyzer repeated by an agent is not unique detection.

Report severity and change exposure. Do not combine a typo and an authorization bypass into “two defects.”

### 2. Resolution quality

Measure the share of confirmed concerns that receive a verified fix, explicit risk acceptance, or justified deferral. Track fix-induced regressions. A comment is not a result.

The strongest direct study in this packet illustrates the gap. [Charoenwet and colleagues](https://link.springer.com/article/10.1007/s10664-024-10496-y) examined security-related comments in OpenSSL and PHP. Their final sets included 188 and 123 concerns; fixes were attempted for 39% and 41%, and 37% were classified as successfully resolved in each project. Comments were concerns, not confirmed vulnerabilities, and the historical observational design supplies no no-review counterfactual. It does show why detection and resolution must remain separate.

### 3. Escaped outcomes

Track post-merge defects, incidents, emergency rework, rollbacks, and customer-visible harm plausibly inside the reviewed change boundary. Use severity and exposure time. Have a blinded or cross-functional sample classify attribution; do not let the reviewer alone decide whether review “should have caught” an escape.

Rare severe events need narrative analysis as well as rates. Absence during a short window is not proof of safety.

### 4. Design and requirement changes

Record when review changes an interface, responsibility boundary, failure strategy, rollout design, or requirement before merge. Require a short reason and evidence, not the number of discussion turns. This is a distinct outcome from defect detection.

### 5. Learning and ownership

Sample transfer rather than count participants. After selected reviews, ask another responsible engineer to explain the change’s intent, major risks, operation, and rollback. Track whether ownership is concentrated, whether support handoffs work, and whether repeated questions become durable documentation or automation. Never turn comprehension checks into surveillance or individual scorecards.

### 6. Flow and load

Measure first-response latency, active review time, queue age, interruptions, after-hours burden, reviewer concentration, and abandoned or superseded reviews. Track author wait separately from organization effort. Agent tokens and tool cost belong in the same ledger, but money and human attention are not interchangeable.

## Run a safe comparison

Choose recurring, bounded change classes: small API changes, data migrations, dependency updates, or test refactors. Predeclare eligibility and exclusions. High-consequence changes retain required human and specialist controls during the experiment.

Compare plausible modes:

- existing human review;
- deterministic checks plus focused human review;
- agent pre-review plus human decision;
- two-person pairing before the pull request;
- risk-qualified asynchronous review with post-merge sampling.

Randomize or rotate modes where practical. If teams choose their own mode, record selection factors and do not claim causality. Keep a common hidden-fault or historical-bug set for controlled changes, and use the same downstream observation window. Agent and human reviewers should not receive different problem statements.

The historical evidence is inconsistent enough to demand this care. [McIntosh and colleagues](https://rebels.cs.uwaterloo.ca/papers/emse2016_mcintosh.pdf) modeled post-release defects in four releases from Qt, VTK, and ITK. Review coverage was about 98%, 96%, 39%, and 98%, yet coverage was a significant predictor in only two of the four systems. The study is observational, pre-agent, and component-level. It supports neither “review coverage works” nor “review is useless.” It shows that coverage is too coarse to be the outcome.

## Protect the measurement from Goodhart’s law

Publish explicit anti-gaming rules:

- comment volume is diagnostic only and never a target;
- reviewers receive no reward for blocking, approving, or finding a quota;
- authors are not penalized for surfaced concerns;
- style findings generated deterministically are removed from human-yield counts;
- severity changes require a second classifier;
- sampled audits include false negatives, not only visible comments;
- review modes are evaluated at team or workflow level, not as individual league tables;
- metric definitions and exclusions are versioned;
- qualitative cases accompany aggregates.

Review the measurement itself monthly. Look for comment splitting, delayed merges to improve a response metric, concern downgrading, easy-change selection, automated noise, and under-reporting of post-merge failures. If a metric changes behavior faster than it improves decisions, demote it.

Practitioner reports can motivate what to observe but not supply baselines. The [Stack Overflow decision-fatigue account](https://stackoverflow.blog/2026/05/21/coding-agents-are-giving-everyone-decision-fatigue/) describes higher output accompanied by reviewer burden. It lacks matched defect and effort data. Treat review pressure as a hypothesis for the load ledger, not as proof that review is the bottleneck.

## Use decision rules, not a universal winner

After enough comparable changes and exposure, decide by failure class and risk:

| Pattern | Decision |
|---|---|
| Repeated deterministic findings | Encode a check; remove them from manual review |
| Human domain review adds unique severe findings | Route those changes to qualified humans earlier |
| Agent pre-review finds valid issues with low triage cost | Keep it as a sensor, not merge authority |
| Agent comments mostly duplicate checks or create noise | Narrow prompts/scope or remove the stage |
| Review changes architecture but arrives late | Move it to design or pairing |
| Low-risk review adds delay with no unique signal | Trial sampling or post-merge review with rollback |
| Escapes cluster despite broad coverage | Change the oracle, reviewer expertise, or change size |

Do not infer that a mode with zero observed escapes is safest when its sample is small or exposure is low. Report uncertainty and denominators.

## Stop conditions and rollback

Pause the experiment if severe escapes increase, required specialists are bypassed, post-merge classification cannot be performed, review queues breach a service threshold, or people begin optimizing visible counts. Stop individual-level reporting immediately if it affects psychological safety or discourages incident disclosure.

Rollback means restoring the previous gate for the affected change class, retaining collected evidence, and removing automated comments or dashboards that distort behavior. Preserve improvements that are independently justified—such as a deterministic policy check—even if the comparison design fails.

Set a review-policy expiry date. Models, tools, teams, and codebases change; a 2026 result is not a permanent charter. Re-run sampled calibration after material model upgrades, organizational changes, or incidents.

## Evidence boundary

No selected study directly compares contemporary human, agent, and hybrid review on matched production changes with downstream outcomes and total cost. The 2026 paper arguing that agents supersede humans is a position paper without such an experiment. A retreat room’s inability to cite evidence is not evidence of no effect.

The defensible local result is a portfolio: automate deterministic findings, place domain judgment where it changes outcomes, use agents where they add independently verified signal, and reduce gates whose cost exceeds their demonstrated value. Keep escaped harm, learning, design, latency, and load visible together so no attractive proxy becomes the definition of good review.

Podcast hook: The team doubled its review comments, cut merge time, and still shipped the defect. Which dashboard taught everyone to optimize the wrong thing?

Continue reading: [Chapter 40, “Turn lint findings into agent instructions”](40-lint-to-agent-instructions.md), tests whether deterministic feedback can prevent repeat repair work without creating a new prompt bureaucracy.
