# 51. Operationalize green, amber, and red governance

> **Report point:** Governance, bullet 51, page 13 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Practice judgment:** Use revisable local tiers to allocate authority and evidence; no universal colors, thresholds, or promotion timetable has been validated.

A risk tier is useful only when it changes a decision. Calling an agent “red” without naming who can approve it, what evidence is required, which actions are prohibited, and when the classification will be revisited creates governance theater.

Green, amber, and red are memorable labels, not natural categories. The evidence base supports layered controls and risk-calibrated autonomy, but it does not validate fixed accuracy thresholds, fixed trial periods, or a universal three-color scheme. Build the tiers from the consequences and controllability of your own use cases.

This chapter is an operating playbook. [Chapter 26](26-risk-tiers-detection.md) holds the evidence and limitations behind the architecture.

## Start with use cases, not models

Inventory an **agent use case** as a combination of:

```text
purpose + data + tools + identity + environment + output path + consequence
```

“Claude,” “Codex,” or “internal model” is not an inventory item. The same model summarizing public documentation and modifying production identity policy represents two different risks. A model upgrade can also alter behavior without changing the use-case label.

For each use case, record:

- the accountable business and technical owners;
- who or what invokes it;
- data read, retained, or disclosed;
- tools, credentials, resources, and network destinations available;
- whether the action is advisory, reversible, or externally consequential;
- the evidence used before an output becomes a decision or deployment;
- detection, rollback, revocation, and incident paths;
- model, harness, evaluator, and policy versions.

[NIST SP 800-207](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf) is not an agent-governance trial, but its zero-trust architecture supplies a useful transfer: do not grant implicit trust because a request originates “inside,” and evaluate access per session against identity, resource, and policy. [Microsoft’s agent security maturity model](https://learn.microsoft.com/en-us/agents/adoption-maturity-model/maturity-model-security-governance) provides staging vocabulary, not empirically validated gates. Use both as design inputs, not compliance proof.

## Define the tier contract

A workable local contract might look like this:

| Tier | Typical consequence | Default authority | Required evidence | Human decision |
|---|---|---|---|---|
| Green | Low impact, reversible, no sensitive data or privileged side effect | Propose or execute inside a narrow sandbox | Deterministic checks, provenance, complete logs, tested rollback | Sampled review and named owner |
| Amber | Material internal impact, sensitive context, or bounded write access | Propose; limited execution behind policy gates | Independent verification, scoped credentials, change review, staged release | Named approver for consequential action |
| Red | Safety, legal, financial, identity, production-wide, or hard-to-reverse impact | No autonomous consequential action by default | Domain assurance case, threat analysis, strong isolation, explicit sign-offs, response rehearsal | Designated risk owner and domain authority |

These examples are deliberately qualitative. A typo in public documentation may be green; the same text change in a legal disclosure may be red. A database migration with excellent rollback may be amber, while an irreversible deletion remains red even if a benchmark reports high accuracy.

Classify using at least:

- severity and scale of plausible harm;
- reversibility and time to recover;
- data sensitivity and residency;
- privileges and reachable resources;
- external or customer-facing effect;
- maturity of specifications and independent checks;
- observability and detection latency;
- uncertainty introduced by novelty or material change.

When uncertainty is high, classify upward temporarily. “Red” should mean stronger decision rights, not a permanent ban on learning.

## Assign decision rights

Each tier needs an accountable owner who can accept residual risk. Platform teams can own common mechanisms; they should not silently accept a product’s domain consequence. Security can define prohibited capabilities and minimum controls; it cannot alone decide that a generated clinical, financial, or employment outcome is correct.

Write down:

- who proposes a new use case;
- who classifies it and resolves disagreements;
- who approves initial operation and each consequential action;
- who can override, suspend, revoke, and restore it;
- who investigates incidents and notifies affected parties;
- who owns records, retention, access, and deletion;
- who reassesses after model, tool, data, policy, or business changes.

Avoid committees in which everyone advises and nobody is accountable. For red uses, record separate technical, domain, and risk sign-off where those competencies differ.

## Train for decisions, not slogans

Training should be role-specific. Users need to recognize data boundaries, generated dependency risk, misleading confidence, and escalation triggers. Approvers need to interrogate provenance, independence of checks, rollback, and residual harm. Platform operators need identity, policy, secrets, isolation, logging, and revocation practice. Incident responders need to reconstruct agent, user, tool, model, and policy activity.

Use realistic exercises. A green exercise might test whether someone notices a generated nonexistent package. An amber exercise might involve a valid tool request with an overbroad resource scope. A red tabletop might combine prompt injection, credential misuse, incorrect approval evidence, and a rollback failure.

Completion of a slide deck is not competence. Ask participants to make and explain bounded decisions against scenarios, including one ambiguous case.

## Log evidence without turning work into surveillance

Governance needs reconstructable evidence: use-case identity, initiating principal, model/harness/tool versions, policy decision, requested and authorized action, resource scope, relevant test or approval result, side effect, and rollback. Protect log integrity and make revocation visible.

Do not interpret this as permission to retain every prompt, conversation, or employee thought indefinitely. The audited corpus lacks the official privacy, employment, worker-consultation, and jurisdiction-specific sources needed to prescribe blanket content monitoring. Before collecting content, define purpose, minimization, access, retention, contestability, and worker involvement with appropriate legal and representative authorities.

Structured action metadata is often more useful and less intrusive than indiscriminate transcript capture. Sensitive payloads can be referenced through controlled identifiers, hashes, or separately protected stores where lawful and technically suitable.

## Run a 30-day tier pilot

Choose three to six real use cases spanning consequences but exclude an unprepared catastrophic-risk deployment.

1. Inventory each use case and draft its tier contract.
2. Run ambiguous scenarios through the classification process and record disagreements.
3. Instrument policy decisions, approvals, denials, overrides, revocations, and rollbacks.
4. Test one incident per tier, including a failed or unavailable approver.
5. Review weekly for friction, shadow use, false assurance, missing owners, and tier drift.
6. At day 30, retain, merge, split, or retire tiers based on observed decisions.

Measure:

- time from use-case proposal to bounded operation;
- unauthorized attempts blocked and legitimate actions wrongly blocked;
- approval wait and override frequency;
- unclassified or shadow use discovered;
- evidence completeness and reconstruction time;
- rollback and revocation success;
- incidents, near misses, and downstream rework;
- user-reported workarounds and policy comprehension.

Do not optimize “more green.” A team can game adoption by classifying risk downward. Nor should zero incidents automatically prove the controls worked; exposure may be low, reporting weak, or harmful outcomes delayed.

## Promotion, demotion, and stop rules

Promotion to more authority requires evidence on representative tasks, including adversarial and failure cases, plus stable rollback and monitoring. It does not occur merely because a fixed number of weeks passed. Demote after a material model or tool change, an incident, loss of observability, policy drift, or evidence that the verifier shares the producer’s blind spot.

Pause a use case when:

- the accountable owner or revocation path is missing;
- sensitive data or credentials cross an undeclared boundary;
- required evidence cannot be reconstructed;
- approval work is routinely bypassed;
- false assurance makes operators trust unsupported outputs;
- rollback or containment fails in rehearsal or operation.

Rollback means more than switching off the model. Revoke credentials, stop queued actions, quarantine artifacts, restore affected systems, preserve authorized evidence, and reassess dependent workflows.

## What good operation looks like

The goal is calibrated authority. Low-consequence work moves with little ceremony because its sandbox, evidence, and recovery are strong. High-consequence work receives domain judgment and independent controls. Every use case has an owner, a visible path to challenge decisions, and a date or trigger for reassessment.

The colors are allowed to disappear. If five tiers, a continuous score, or domain-specific classes make decisions clearer, use them. The test is whether the model changes permissions, evidence, decision rights, and response in a way people can explain.

Podcast hook: If “red” changes no permission and “green” has no rollback test, are they risk tiers—or just traffic-light wallpaper?

Continue reading: [Chapter 52: Treat agent-generated application code as untrusted](52-agent-generated-application-code-untrusted.md) applies the tier contract across a concrete generation-to-runtime path.
