# 46. Tier autonomy by risk and reversibility

> **Report point:** Team design, bullet 46, page 12 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** Local decision criteria are defensible; universal tiers, thresholds, and promotion schedules are not validated.

“How autonomous should the agent be?” is too broad to answer at organization level. The same agent may safely reformat an isolated test fixture, need approval before changing a customer-facing API, and have no direct authority to rotate production credentials. Autonomy belongs to a particular action on a particular component under stated controls.

The practical task is to choose where a human must decide, where a human may review after the fact, and where bounded automation may act. Make that decision revisable. A tier is a compact operating contract, not a badge awarded to a model.

## A plain-language model: consequence, recovery, and evidence

Picture two changes. The first regenerates documentation in a preview branch. A bad result is visible and discarded. The second changes a production authorization rule. A bad result may expose data before anyone notices. Both changes might be syntactically simple, yet they deserve different authority because their consequences, observability, and recovery paths differ.

Assess each agent action across eight dimensions:

1. **Consequence:** what harm follows from an incorrect but valid-looking action?
2. **Reversibility:** can the exact prior state be restored, and how quickly?
3. **Blast radius:** how many users, systems, records, or environments can be affected?
4. **Sensitivity:** does the action touch personal, confidential, regulated, or safety-relevant data?
5. **Privilege:** which identities, tools, resources, and downstream capabilities become available?
6. **Observability:** will failure be detected before harm, soon afterward, or only through a user report?
7. **System maturity:** are interfaces stable, tests representative, and operating behavior understood?
8. **Recovery evidence:** has rollback actually been exercised under conditions resembling this action?

Do not average these into a false-precision score. One severe dimension can dominate. A reversible database migration in staging is not equivalent to the same command against a shared production cluster.

## What the evidence supports—and does not

[NIST’s Zero Trust Architecture](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf) supports per-session, least-privilege decisions based on identity, resource state, context, and telemetry, with separate policy decision and enforcement roles. Applying that architecture to coding agents is a reasoned transfer: NIST did not evaluate autonomous software engineering. The document itself warns about policy errors, stolen credentials, telemetry privacy, false decisions, and control-plane chokepoints.

[Microsoft’s agent security and governance maturity model](https://learn.microsoft.com/en-us/agents/adoption-maturity-model/maturity-model-security-governance) names useful practices: inventory, ownership, risk categorization, approval boundaries, logs, incident handling, trust calibration, and reassessment. Its levels are vendor guidance, not an empirically validated progression. Microsoft’s separate [least-privilege guidance](https://www.microsoft.com/en-us/security/blog/2026/07/16/least-privilege-for-ai-agents-identity-access-and-tool-binding/) makes the implementation more concrete: distinct agent identity, task-scoped roles, just-in-time access, curated tools, downstream authorization, logging, and revocation. It reports no comparative incident reduction.

A bounded [nine-agent healthcare-company case](https://arxiv.org/pdf/2603.17419) describes four high-severity configuration or credential findings and a move toward gVisor, a credential proxy, per-agent egress rules, and content labels. The authors also expose migration gaps, policy-maintenance burden, and the paradox of a highly privileged audit agent. It is valuable field detail, not evidence for a universal tier.

One [practitioner counterexample](https://digitalinfrastructures.nl/posts/risk-value/) describes an assistant producing excessive architecture for a nonsensitive chatbot. It cannot quantify control burden, but it makes a vital point: disproportionate governance can destroy value as surely as absent governance can create risk.

No audited source validates fixed green/amber/red meanings, two- or eight-week promotion periods, accuracy percentages, availability gates, or an agent-to-human ratio. Those numbers should not be imported from vendor taxonomies.

## Build an action inventory

Start with actions, not applications. For one service, list what the agent can:

- read, generate, or modify in source control;
- invoke in CI, deployment, infrastructure, ticketing, and data systems;
- access through credentials or delegated user authority;
- publish, merge, deploy, delete, spend, message, or expose externally.

Split broad tools into distinct verbs. “Use GitHub” hides a large difference between reading an issue, opening a draft pull request, merging to a protected branch, and changing repository permissions. “Use cloud CLI” is too broad to classify.

For every action, name the component owner, agent identity, allowed resources, input constraints, side effects, evidence produced, denial behavior, escalation path, and revocation method. An action without an owner or an enforceable boundary cannot graduate to direct execution.

## Define local modes, not universal risk colors

A team can use four modes as a starting vocabulary:

- **Explore:** the agent may read approved context and produce advice or a local artifact; it has no write authority.
- **Propose:** the agent may create a reviewable candidate, such as a draft pull request or plan, but a named human authorizes the consequential action.
- **Act within a reversible envelope:** the agent may execute a narrowly specified action where automated evidence, observation, and tested rollback bound the consequence.
- **Human-controlled:** the agent may assist analysis, but a human performs and verifies the action through a separate path.

These are not maturity stages. “Human-controlled” can be the permanent correct choice for destructive, legally significant, safety-critical, ambiguous, or poorly observable actions. “Act” is not a reward for past good behavior. It is a current judgment about an action and its containment.

Document the decision in a short autonomy card:

| Field | Required statement |
|---|---|
| Action and scope | Exact verb, resource set, and environment |
| Worst credible consequence | Technical, customer, security, financial, and human impact |
| Preconditions | Identity, policy, tests, data state, and change window |
| Evidence before action | Checks independent enough to challenge the candidate |
| Observation | Signal, owner, delay, and false-negative concern |
| Recovery | Tested rollback, maximum tolerable recovery time, and manual fallback |
| Mode | Explore, propose, bounded action, or human-controlled |
| Reassessment trigger | Incident, model/tool change, scope change, drift, or review date |

## Pilot bounded execution

Begin in observe-only or propose mode. Replay representative historical cases, including failures and adversarial boundaries, without granting production authority. Then run in shadow mode: evaluate what the agent would do and compare it with the accountable human decision.

Move one action—not an entire agent—to bounded execution only when:

- the policy is technically enforced outside the model;
- negative authorization tests show disallowed resources and parameters are denied;
- verification covers the failure modes that justify the mode;
- monitoring reaches an accountable person within the harm window;
- rollback has been rehearsed;
- an independent kill switch and credential revocation work;
- the owner accepts the residual risk in writing.

These are prerequisites, not validated numeric gates. A hundred successful low-risk actions cannot prove safety for a rare high-impact boundary case.

## Metrics for promotion, retention, and demotion

Track each action type and denominator:

- attempted, allowed, denied, escalated, and manually overridden actions;
- correct and incorrect denials sampled through review;
- human reversals of agent proposals and their reasons;
- downstream defects, incidents, policy violations, and near misses;
- detection and recovery time;
- unexercised or failed rollbacks;
- privilege and tool-scope changes;
- reviewer delay, approval fatigue, and exception burden;
- work routed around the controlled path.

Measure value too: successful completion, end-to-end latency, user outcome, and operator effort. Otherwise governance can optimize for zero action by making the system unusable. Do not collapse safety and value into one score; expose the tradeoff.

Promotion requires current evidence for the exact action and component. Retention requires that the environment still matches the evidence. Demotion is normal after an incident, a new data class, broader resources, weaker monitoring, a model or tool upgrade, ownership change, or an untested recovery path.

## Boundary cases

A well-tested code edit can still be high consequence if it changes authorization semantics. A production read can be harmful if it exposes sensitive data. A reversible write can be risky if reversal cannot repair messages already sent or secrets already disclosed. A low-blast-radius action can overload a shared service when many agents run concurrently; the [multi-agent slowdown account](https://towardsdatascience.com/why-adding-more-ai-agents-made-our-system-slower/) is a bounded reminder that shared-resource pressure belongs in the decision.

Human approval is not automatically safer. Reviewers can rubber-stamp, become fatigued, or lack the context to detect an error. For consequential actions, improve the evidence and narrow the authority rather than inserting an unspecified “human in the loop.”

## Stop and rollback rules

Stop direct execution immediately after an unexpected privileged action, sensitive-data exposure, failed denial, unavailable kill switch, missed alert beyond the declared harm window, or rollback failure. Revoke the agent’s credentials, disable the action at the enforcement point, preserve the agreed audit trail, and return that action to propose or human-controlled mode.

Pause promotion when override or exception rates rise, reviewers cannot explain approvals, monitoring produces repeated false confidence, or the action’s scope changes faster than its tests. A serious near miss is evidence; do not wait for harm to demote.

Rollback should be component-specific: restore the previous authorization policy, credential scope, tool version, and workflow; verify that queued or delegated actions cannot continue; and test the manual path. Hold a reassessment focused on the failed assumption, not on whether the model appears generally trustworthy.

The unresolved gap is central: no selected source establishes validated autonomy thresholds or comparative tier efficacy. The result of this playbook is a local, auditable risk decision with reversible authority—not a claim that a named tier makes an agent safe.

Podcast hook: Why can the same agent be trusted to edit a preview but forbidden to touch one production permission—and who gets to change that boundary?

Continue reading: [Chapter 26: Risk tiers and detection](26-risk-tiers-detection.md) examines the evidence behind layered, risk-calibrated oversight.
