# 26. Risk tiers need prevention, detection, and response

Risk-tiered authorization and continuous detection are complements, not alternatives. Prevention narrows what an agent can do; detection finds suspicious behavior that still occurs; response limits the duration and blast radius after a signal. The right mix depends on consequence, reversibility, data sensitivity, privilege, exposure, observability, and recovery—not a universal green, amber, or red label.

The [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) proposes green/amber/red use tiers paired with scanning of agent conversation logs. The retreat is a dependent, anonymous witness network. It establishes that practitioners are trying this pattern, not that those colors, training rules, or monitoring practices reduce incidents. The audit also found no official privacy, employment, union, or worker-consultation evidence sufficient to prescribe blanket prompt monitoring.

## A plain-language model: gate, guardrail, alarm, brake

Think of agent governance as four functions:

- A **gate** decides whether this identity may attempt this action on this resource now.
- A **guardrail** constrains parameters, tools, credentials, network reach, and execution environment.
- An **alarm** records and detects suspicious outcomes, policy violations, drift, and novel patterns.
- A **brake** revokes authority, contains damage, rolls back changes, and starts incident response.

Training belongs around these functions, but cannot replace them. A person may forget policy, a model may behave differently after an update, and a previously safe workflow may receive new data or privileges. Conversely, logging every conversation does not stop an irreversible transfer or deletion before it happens.

A tier is simply a reusable control bundle. It should describe the workload and consequence, not confer trust on the model. “Low risk” remains low only while its data, tools, outputs, users, and dependencies match the approved envelope.

## What the strongest sources support

[NIST SP 800-207](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf) is an official normative architecture for zero trust, not an AI-agent study. It removes implicit trust based on network location and centers per-session, least-privilege decisions on identity, resource state, context, policy, and telemetry. It separates the policy engine, policy administrator, and enforcement point and allows incremental or report-only deployment. Applying those principles to agents is a reasoned transfer: put authorization outside the model and reassess it continuously.

NIST also supplies counterevidence to simplistic detection. It names policy-engine compromise, stolen credentials, insider action, encrypted-traffic limits, telemetry privacy, false positives and negatives, user fatigue, and incorrect policy decisions as residual risks. More observation can create more data without creating better decisions.

Microsoft’s [agent-security maturity guidance](https://learn.microsoft.com/en-us/agents/adoption-maturity-model/maturity-model-security-governance) names inventory, ownership, risk categorization, identity, access, logs, approval boundaries, service levels, incident handling, privacy, and periodic reassessment. This is official vendor practice, not a measured maturity progression; its numbered levels have no comparative outcome study.

A separate Microsoft guide on [least privilege for AI agents](https://www.microsoft.com/en-us/security/blog/2026/07/16/least-privilege-for-ai-agents-identity-access-and-tool-binding/) recommends first-class agent identity, a named owner, task-scoped roles, just-in-time access, curated tools, downstream authorization, logging, and lifecycle revocation. These are concrete preventive controls from an identity vendor. The scenarios do not establish incidence or efficacy, and the implementation timeline on the page is advice rather than evidence.

The commercially conflicted [Open Agent Passport preprint](https://arxiv.org/html/2603.20953v1) demonstrates a pre-tool-call policy hook that evaluates declared capabilities and parameters, fails closed, returns structured denials, and signs a decision record. Its authors own the evaluated product and CTF. The highest-assurance CTF policy allowed zero capability and zero transfer value, the comparison was non-randomized, large-enterprise scale was untested, and the design does not cover content-layer harms or formal delegation. It makes the architecture tangible; it does not prove a universal tier.

The field case [*Caging the Agents*](https://arxiv.org/pdf/2603.17419) describes nine healthcare-company agents and four high-severity configuration or credential findings. The authors document same-day remediation and a target design combining gVisor, a credential proxy, per-agent egress allowlists, and trusted-metadata labeling. The paper is a self-evaluated commercial preprint; its abstract blurs already deployed controls with a target architecture still being migrated. Performance and coverage claims lack independent benchmarks. Its practical contribution is showing that detection found misconfiguration while prevention and containment still had to be redesigned.

Together these sources support a control architecture, not an incident-reduction estimate.

## Detection’s hidden costs

Detection can fail in both directions. False negatives leave dangerous behavior invisible; false positives consume responder time, delay legitimate work, and train people to ignore alerts. Models and users may learn to evade simple pattern rules. Logs can omit downstream side effects while retaining sensitive prompts, source code, personal data, or employee communications.

Continuous content monitoring therefore needs a separate governance contract: defined purpose, minimum necessary fields, access controls, retention, security, contestability, worker involvement, and deletion. Aggregate action metadata may be enough for some workflows; content inspection may be necessary for others. The corpus does not determine what is lawful or proportionate in a particular jurisdiction.

Some environments have mandatory preventive constraints arising from law, contract, safety case, or data policy. A detection-first preference cannot waive a requirement that data must not leave a boundary, a person must approve an action, or a separation of duties must hold. Because applicable legal authorities were absent from the audit, teams must map those obligations with their own legal, privacy, security, and worker representatives rather than infer them from vendor frameworks.

## Why fixed colors decay

A personal summarizer using public documents and no tools may deserve a lighter bundle than an agent changing payroll or production infrastructure. But labels conceal component differences. A “team use” tool can access a high-risk database; a company-wide tool can perform only reversible read operations.

Risk also changes over time. A model update alters behavior. A new connector changes reachable resources. A wider user population changes exposure. A better rollback mechanism may lower consequence, while weaker detection may raise it. Tiers must be local, versioned, and reassessed after material changes, incidents, and control failures.

The audit found vendor frameworks with fixed promotion periods and accuracy or availability thresholds. Those values are unvalidated author taxonomies. They should not be copied into policy.

## The tier-and-control worksheet

Complete one worksheet per workflow or component.

### 1. Describe the consequence

- What decision or action is automated?
- Which data, systems, people, and third parties can be affected?
- Is the action reversible, and how long does reliable rollback take?
- What is the credible worst-case blast radius?
- Which legal, contractual, safety, or human-approval constraints are mandatory?

### 2. Describe authority

- Named agent identity and human owner.
- Allowed tools, resources, parameters, spend, duration, and network destinations.
- Just-in-time credential source and expiry.
- Downstream authorization and separation-of-duties checks.
- Explicit denied actions and an emergency exception path.

### 3. Design detection

- Events recorded before, during, and after action.
- Signals tied to known hazards, plus anomaly or drift checks where justified.
- Expected false-positive and false-negative costs.
- Detection owner, response time, and escalation route.
- Privacy purpose, minimized fields, access, retention, contestability, and deletion.

### 4. Design the brake

- Automatic pause or revocation conditions.
- Human stop authority and reachable on-call owner.
- Containment, rollback, credential rotation, and evidence preservation.
- Recovery test and incident-learning loop.

### 5. Assign a local tier

Name the tier only after the controls are specified. Record why the bundle is sufficient, what evidence supports it, and the next reassessment trigger. Test one denied action, one false alert, one missed signal, and one rollback. If responders cannot explain what happens, the tier is decorative.

## Evidence judgment

- **Architecture confidence:** moderate to high. Official and practice sources converge on external authorization, least privilege, logging, detection, revocation, and reassessment.
- **Tier thresholds:** low. No universal color scheme, promotion period, or quantitative gate was validated.
- **Detection efficacy:** unknown. No comparative production dataset measures incident reduction, evasion, false positives, or response burden.
- **Privacy and labor boundary:** unresolved. The corpus is insufficient for blanket conversation-monitoring policy.
- **Counterexample:** excessive controls can create cost without proportional value, while detection alone cannot satisfy mandatory preventive obligations or stop irreversible actions.

The defensible principle is not “detect instead of prevent.” It is “prevent what must not happen, detect what cannot be fully prevented, and rehearse the response.”

Podcast hook: An agent passes the green gate, gains a new connector, and quietly becomes red without changing its label. The episode follows the gate, alarm, and brake as the risk envelope moves.

Continue reading: [Chapter 27, “Slopsquatting and hallucinated dependencies”](27-slopsquatting.md), applies the architecture to a specific threat chain; Chapter 46 tiers autonomy at component level.
