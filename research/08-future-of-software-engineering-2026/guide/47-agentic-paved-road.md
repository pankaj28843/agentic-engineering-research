# 47. Build an opinionated agentic paved road

> **Report point:** Team design, bullet 47, page 12 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** A coherent platform contract is supportable; its adoption, safety, and delivery effects must be demonstrated locally.

An agentic paved road is the easiest supported route from an approved task to a reviewable, observable, recoverable change. It packages identities, tools, context, verification, logs, deployment boundaries, and help into a product that teams can choose. It is not a compulsory framework, a universal prompt, or a central team’s claim to know every product domain.

The design test is demanding: the paved road must make the safer route easier while preserving legitimate escape. If teams routinely bypass it, the problem may be the road, not the teams.

## A plain-language model: a road with services and exits

A physical road is useful because its surface, signs, guardrails, maintenance, and emergency services reduce the work of each journey. It does not decide every destination or ban all side roads. An internal platform should work similarly.

[Microsoft’s platform-engineering definition](https://learn.microsoft.com/en-us/platform-engineering/what-is-platform-engineering) treats the platform as a product that offers self-service capabilities and governance through paved paths. That is an official vendor definition, not evidence that any particular platform improves outcomes. The [agentic-codebase principles](https://maintainable.software/agentic-engineering-part-2-agentic-codebase-principles/) add useful hypotheses about locality, explicit boundaries, and verifiability; they also provide no comparative platform study.

For agents, the road should reduce repeated decisions about safe identity, allowed tools, dependency policy, isolated execution, tests, and rollback. Product teams still own intent, domain behavior, and operational consequences. The platform owns the reliability and legibility of the route it offers.

## The minimum platform contract

Start with one golden path for one high-frequency, bounded use case, such as creating a draft change in a non-production repository. State the contract in observable terms.

### 1. Identity and ownership

Every agent execution has a distinct identity, an accountable human or team owner, and a lifecycle for issue, rotation, and revocation. [Microsoft’s least-privilege guidance](https://www.microsoft.com/en-us/security/blog/2026/07/16/least-privilege-for-ai-agents-identity-access-and-tool-binding/) recommends task-scoped roles, just-in-time access, curated tools, downstream authorization, logs, and revocation. Use those as normative implementation dimensions, not claims of measured effectiveness.

### 2. Narrow tools and resource boundaries

Expose task-specific operations rather than a broadly privileged shell where practical. A tool contract includes allowed verbs, resources, parameters, side effects, denial behavior, and downstream authorization. A schema improves inspectability but is not authorization by itself.

### 3. Context and dependency policy

Provide the smallest maintained context that helps the agent navigate the supported task: service ownership, interfaces, test commands, local constraints, and approved dependency routes. Generated dependencies remain proposals. Apply source, provenance, version, and review controls appropriate to the work rather than trusting a plausible package name.

### 4. Isolated execution

Choose containment from a threat model. Separate secrets, restrict egress, use disposable environments where feasible, and make the boundary visible to users. A [bounded field case involving nine healthcare-company agents](https://arxiv.org/pdf/2603.17419) describes gVisor, credential proxying, per-agent egress, and content labels as a target architecture, while also documenting migration gaps and maintenance burden. It supports concrete design questions, not a claim that one sandbox is sufficient.

### 5. Verification and release evidence

Provide deterministic checks, policy gates, provenance, and an artifact that a reviewer can inspect. Tests and scans are evidence inputs, not merge authority. Product teams should be able to add domain checks without forking the platform.

### 6. Logs, observation, and recovery

Record relevant actions, policy decisions, tool versions, and artifact provenance without collecting unrelated worker conversations. Define alert ownership, rollback, credential revocation, and the manual fallback. The platform must fail in an understandable way.

### 7. Support and service levels

Publish who supports the road, expected response for blocked work and security issues, supported versions, planned change notice, and incident communication. Without a support contract, self-service merely transfers debugging to product teams.

### 8. Escape hatches

Document how a team can request an exception, use an alternative, or extend the road. Require an owner, reason, scope, compensating controls, review date, and route back. An escape hatch is not an unlogged bypass; it is feedback about a case the product does not yet serve.

## Co-design before construction

Select two or three product teams with different but bounded needs. Observe a real task end to end and identify repeated friction, security decisions, missing context, and current workarounds. Ask what teams must retain control over. Draft the thinnest contract that removes a shared burden without absorbing domain ownership.

Create a one-page service blueprint:

| Stage | Product-team responsibility | Platform responsibility | Evidence returned |
|---|---|---|---|
| Frame | Outcome, constraints, risk | Supported task and policy visibility | Accepted task contract or clear denial |
| Execute | Domain input and oversight | Identity, tools, isolation, context | Action and provenance record |
| Verify | Domain acceptance | Standard tests and policy gates | Reviewable results and uncertainty |
| Release | Accountable authorization | Supported deployment boundary | Release and rollback record |
| Operate | Outcome and incident ownership | Platform health and support | Alerts, diagnostics, and recovery route |

Review it with users before building. A platform that optimizes a central team’s assumptions can create a polished obstacle.

## Make the platform team its first serious user

Dogfooding is an architectural test, not proof of external fit. The platform team should use the paved road to change and operate the platform itself where risk permits. This exposes missing diagnostics, circular dependencies, unpleasant approval paths, and recovery gaps.

Record every privileged manual step needed to rescue the platform. A road that works only because its builders have hidden administrator knowledge is not self-service. Product teams should be able to see status, identify the failed boundary, and follow a documented escalation without knowing the platform internals.

Dogfooding has limits: platform work may be unusually familiar, and its team may tolerate rough edges other users cannot. Keep co-design and external pilots.

## Pilot opt-in adoption

Offer the road to a small set of teams for four to eight weeks while their previous supported path remains available. Provide office hours and a feedback channel. Do not count a mandate as adoption.

Measure a balanced set:

- **Discovery and onboarding:** eligible teams, teams that try the road, time to first safe completed change, and abandonment stage.
- **Use and escape:** repeat use, eligible work completed on-road, exception requests, approved alternatives, and silent bypasses discovered.
- **Service quality:** availability, latency, failed runs, diagnostic clarity, support response and resolution time.
- **Delivery:** end-to-end time, rework, failed changes, rollbacks, and operational incidents for comparable tasks.
- **Safety:** policy denials, incorrect allows or denies found through sampling, privilege exceptions, and recovery exercises.
- **Experience:** product-team confidence, retained domain control, accessibility, and qualitative friction.
- **Platform burden:** maintenance effort, support load, exception-review time, and cost per successful change.
- **Learning:** whether teams can explain and operate the result without the platform team; treat this as a local sample, not proven knowledge transfer.

Show denominators. “Ten teams adopted” means little if ten were mandated or one hundred were eligible. Do not combine these measures into one platform score. High use can reflect coercion; low exception volume can reflect an unusable process; fast completion can conceal later recovery.

Compare with the prior path or a carefully matched work class, while preserving task risk and novelty. This is still observational unless assignment is controlled. State that limitation.

## Exceptions are product discovery

Review escape-hatch requests on a regular cadence. Classify them as missing capability, unacceptable latency, incompatible domain constraint, temporary incident route, regulatory requirement, experimentation, or documentation failure. Publish the decision and review date.

Promote a recurring exception into the road only when multiple teams share the need and the platform can own its reliability. Preserve a plugin or extension boundary for local behavior. Retire features that create broad complexity for rare use.

An exception process can become coercive if approval is slow or politically costly. Track time to decision and rejected requests, and let an independent architecture or risk owner hear appeals. Teams should not be forced to misclassify work merely to meet delivery pressure.

## Failure signals, stop rules, and rollback

The pilot is failing if teams need platform engineers for routine recovery, if silent bypass grows, if one global context bundle leaks or confuses domains, if the platform expands privileges for convenience, or if support queues erase any delivery gain. Repeated false denials, unexplained policy decisions, unavailable rollback, and inability to revoke identities are immediate safety signals.

Stop onboarding new teams after a security boundary failure, artifact provenance loss, failed credential revocation, or an incident the platform cannot reconstruct. Restore the previous supported path for affected work, revoke or narrow platform identities, and preserve incident evidence. A versioned contract allows product teams to pin or return to the last known path while the platform is repaired.

Pause rather than mandate when adoption is low. Interview eligible non-users and compare their tasks; do not “solve” low adoption by removing exits. If the road raises end-to-end delay, rework, or support burden across two review windows without compensating safety evidence, reduce its scope or roll back the pilot.

The platform should publish deprecation and migration rules so that rollback is organizationally possible, not merely technically possible. A team must retain access to its artifacts, logs, and manual operating route.

## The unresolved efficacy question

The security and platform corpus converges on a plausible bundled contract: identity, narrow tools, containment, verification, logs, rollback, support, and exceptions. It does not compare an agentic paved road with alternatives or measure a general effect on adoption, safety, trust, delivery, or learning.

That gap changes the recommendation. Build the smallest road whose behavior can be observed, keep exits real, and let local results determine expansion. “Opinionated” should mean explicit defaults and ownership, not frozen architecture.

Podcast hook: What makes a paved road trustworthy—the guardrails, the repair crew, or the fact that teams are still allowed to leave it?

Continue reading: [Chapter 15: From platform engineering to agentic credibility](15-platform-agentic-credibility.md) explains why product behavior and earned trust matter more than a platform label.
