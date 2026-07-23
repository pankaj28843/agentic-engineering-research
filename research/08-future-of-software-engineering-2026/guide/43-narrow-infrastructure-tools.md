# 43. Replace broad infrastructure tools with narrow, authorized operations

> **Report point:** Playbook, bullet 43, pages 11–12 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Playbook judgment:** A task-specific interface can make infrastructure actions more reviewable and constrain authority, but a schema is not authorization. Identity, downstream policy, side-effect control, logging, revocation, denial, and emergency access are separate design obligations.

A broad cloud CLI is powerful because it combines discovery, identity, parsing, control flow, and nearly every provider action. Giving that interface to an agent also gives the agent a large language of possible mistakes. Telling it “only update the staging deployment” does not remove production commands, wildcard resources, shell composition, or inherited credentials.

The safer pattern is to expose the smallest useful operation: `planStagingDeployment`, `rotateServiceCertificate`, or `scaleWorkerPoolWithinLimit`. A declared input schema improves inspectability. It does not establish who may call the operation, which resource the name resolves to, what downstream service will authorize, or whether the implementation performs hidden side effects.

No audited source compares narrow infrastructure tools with broad CLIs on representative production workloads, confused-deputy failures, operator burden, or incident rates. This playbook builds a least-privilege pilot and keeps that negative finding visible.

## Plain mental model: menu, badge, kitchen, receipt

A schema is the menu: it lists allowed-looking orders. Identity is the badge: it says who is asking. Policy is the waiter checking whether this badge may place this order for this table. The implementation is the kitchen: it must not quietly do something broader. The audit record is the receipt.

All four can fail independently.

```text
intent → narrow schema → authenticated agent → pre-action policy
       → downstream authorization → bounded side effect → signed/immutable record
       → observation and rollback
```

A tool called `restart_service(service)` is not narrow if `service="*"` is accepted, name resolution crosses accounts, the underlying credential is administrator, or the implementation shells out to an unconstrained CLI.

## Start with a threat-and-task inventory

Observe real infrastructure work over a defined period. List recurring operations, actors, resources, parameters, current credentials, side effects, approvals, emergency use, and rollback. Separately list misuse cases:

- wrong account, region, cluster, namespace, or tenant;
- wildcard or ambiguous resource selection;
- excessive scale, spend, retention, or duration;
- destructive ordering and partial failure;
- stale plan applied after state changes;
- credential confused-deputy use;
- indirect privilege escalation through a downstream service;
- unlogged retry or duplicate action;
- prompt-injected parameter or tool choice;
- egress to an unapproved endpoint;
- emergency path becoming the ordinary path.

Choose one frequent, bounded, reversible operation. Do not begin with arbitrary Terraform apply, unrestricted `kubectl`, IAM administration, or a general shell.

The practitioner guidance on [least privilege for kubectl, Terraform, and cloud CLIs](https://kodekloud.com/blog/least-privilege-for-ai-agents-securing-kubectl-terraform-and-cloud-clis/) correctly notes that natural-language tool descriptions cannot constrain a broadly privileged CLI and offers narrow operations, federated credentials, policy, backups, and negative tests. Its incident stories and percentages have opaque provenance; use the mechanisms, not the quantitative claims.

## Write the operation contract

Each tool needs an inspectable contract:

| Area | Required decision |
|---|---|
| Purpose | One operational outcome and named non-goals |
| Identity | Unique agent/workload identity, human owner, caller authentication |
| Resources | Explicit account, region, resource type, allowlist, no implicit wildcard |
| Parameters | Types, enums, ranges, units, cross-field rules, safe defaults |
| Preconditions | Current state, freshness, health, budget, maintenance window |
| Authorization | Pre-action policy and downstream re-authorization |
| Side effects | Writes, external calls, expected duration, idempotency |
| Preview | Read-only plan showing resolved targets and material effects |
| Approval | Risk-based human or automated decision, bound to the exact plan |
| Evidence | Request, identity, policy version, resolution, result, correlation ID |
| Denial | Structured reason, safe retry, escalation without credential leakage |
| Recovery | Compensation, rollback, timeout, partial-failure handling |
| Lifecycle | Owner, version, revocation, expiry, emergency replacement |

Validate semantic constraints, not only JSON types. `replicas: integer` still permits one million. `environment: string` still permits production. Resolve resource identifiers before approval and bind the approval to that resolution and a freshness window.

## Separate schema, authority, and execution

Apply [NIST SP 800-207](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf) as a reasoned transfer, not an agent evaluation. NIST separates policy decision and enforcement roles, rejects implicit trust based on network location, and supports least-privilege, per-session decisions, observation phases, and continual reassessment. It also names residual risks including policy-engine compromise, stolen credentials, denial of service, incorrect decisions, false positives, privacy, and user fatigue.

For the agent tool:

- give the workload a first-class identity rather than a shared human credential;
- issue short-lived, just-in-time authority for the resolved operation;
- enforce policy before execution;
- re-establish authorization at the cloud or cluster boundary;
- keep the execution credential inaccessible to the model;
- constrain network egress and credential use;
- revoke identity, tool, and policy grants independently.

[Microsoft’s least-privilege guidance for AI agents](https://www.microsoft.com/en-us/security/blog/2026/07/16/least-privilege-for-ai-agents-identity-access-and-tool-binding/) supports identity, owner, task-scoped roles, just-in-time access, curated tools, downstream authorization, logs, and lifecycle revocation. It is first-party vendor guidance, not an outcome study; its implementation timing is not evidence-based.

## Build denial before write

Implement in stages:

1. **Resolve and describe.** The tool accepts proposed inputs, resolves exact resources, and returns a plan without credentials capable of writing.
2. **Run negative authorization tests.** Wrong account, wildcard, expired identity, excessive parameter, stale plan, forbidden time, unapproved egress, and replayed approval must fail closed.
3. **Add one reversible write.** Use a dedicated identity and narrow downstream role. Make requests idempotent and cap retries.
4. **Bind approval to intent.** Sign or hash the resolved plan, policy version, identity, parameter set, and expiry. Any change requires a new decision.
5. **Canary.** Limit resources, callers, and time. Observe both successful and denied paths.
6. **Expand one dimension at a time.** More resources, parameters, or callers each trigger threat-model and test updates.

Oracle’s [secure-enforcement description for Fusion AI agents](https://blogs.oracle.com/cloud-infrastructure/fusion-ai-agents-secure-by-enforcement) illustrates read/write separation, just-in-time authority, schema validation, allowlists, fail-closed behavior, separation of duties, and audit. It is product-specific vendor architecture with no comparative attack evaluation.

## Test the confused deputy and schema gaps

The central security test is not “does the agent call the documented function?” It is “can an authorized-looking request cause the tool or downstream service to misuse stronger authority?”

Test:

- caller may update service A but supplies an alias resolving to service B;
- permitted plan is changed before apply;
- resource is replaced between authorization and execution;
- a safe parameter combination becomes unsafe across fields;
- the tool’s implementation passes unchecked flags to a broad CLI;
- downstream API interprets an omitted field more broadly than the wrapper;
- logs claim denial while an asynchronous side effect occurred;
- retry duplicates a non-idempotent action;
- tool error includes a credential or sensitive state;
- emergency identity bypasses ordinary scoping.

The commercially conflicted [Open Agent Passport preprint](https://arxiv.org/html/2603.20953v1) gives a concrete pre-tool pattern: declared capability and parameter rules, fail-closed decisions, structured denials, and signed records. Its reported zero success at the highest CTF tier came from a zero-capability, zero-dollar policy in a non-randomized self-selected setting; the escalation path was unimplemented, audit writes were asynchronous, and large-scale operation was untested. Use the architecture, not “0% attacks” as a production claim.

## Measure benefit and burden

Compare the narrow path with the current human or broad-CLI workflow for the same eligible tasks:

- independently verified task success;
- wrong-resource, excessive-parameter, stale-plan, and unauthorized attempts;
- maximum modeled and observed blast radius;
- denial correctness, false denials, and safe recovery;
- rollback success and partial-failure rate;
- operator active time, queueing, and escalation burden;
- schema/context tokens, calls, retries, latency, and infrastructure cost;
- support tickets and missing-operation requests;
- audit completeness, latency, and tamper evidence;
- emergency-path frequency and duration.

Do not call every denial a prevented incident. Some are user errors, policy defects, or tool gaps. Sample and classify them. Likewise, task success under a narrow tool does not prove the absence of an authorization bypass.

The field case [*Caging the Agents*](https://arxiv.org/pdf/2603.17419) documents four high-severity configuration or credential findings across nine healthcare-company agents and a target design using gVisor, credential proxying, per-agent egress allowlists, and trusted-metadata separation. It also exposes DNS/CDN maintenance, exception burden, brittle prompt controls, and a privileged audit-agent paradox. The paper mixes deployed and target-state claims and supplies no post-control adversarial efficacy study. Its strongest contribution is the operational residuals.

## Emergency access without a permanent bypass

Keep a human-operated, separately authenticated break-glass path for incidents the narrow catalog cannot handle. Require:

- declared incident or change ticket;
- short-lived elevated credential;
- two-person or risk-appropriate approval;
- session recording and command audit where lawful;
- explicit target and expiry;
- after-action review and credential revocation.

Do not expose the broad emergency CLI to the ordinary agent as a fallback. A frequent break-glass event is evidence of a missing operation or an unrealistic policy, not a reason to make the bypass permanent.

## Stop conditions and rollback

Stop rollout when target resolution is ambiguous, downstream authorization cannot be enforced, logs do not match side effects, denial recovery encourages credential sharing, emergency use rises, operator burden exceeds the agreed envelope, or a schema gap permits materially broader action. Revoke immediately on credential leakage or cross-boundary execution.

Rollback by disabling the tool route, revoking its workload identity and downstream grants, canceling outstanding approvals, and returning eligible work to the human-operated path. Preserve audit evidence and any safe read-only planning capability. Do not restore an autonomous broad CLI merely because the narrow tool failed.

## What survives skeptical review

The selected sources converge on an architectural pattern: enforce outside the model, bind identity to narrow tools, authorize before action and downstream, separate credentials, constrain egress and side effects, log, and revoke. They do not quantify comparative incident reduction, confused-deputy prevalence, race conditions, schema completeness, emergency risk, or operator cost.

The defensible move is incremental. Replace one recurring broad-CLI task with a narrow operation, prove its denial and rollback paths, measure outcomes and burden, and expand only when the contract survives adversarial review. The schema makes the menu legible; the security comes from the whole restaurant.

Podcast hook: The agent called the only function it was allowed to call—and that function used an administrator credential on the wrong cluster.

Continue reading: [Chapter 44, “Instrument the two clocks”](44-instrument-two-clocks.md), measures whether a narrower infrastructure path improves trusted delivery rather than merely moving work.
