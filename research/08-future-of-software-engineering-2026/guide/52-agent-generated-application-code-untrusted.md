# 52. Treat agent-generated application code as untrusted

> **Report point:** Governance, bullet 52, page 13 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Practice judgment:** Apply defense in depth from generation through runtime; tests, scans, reviews, and sandboxes are evidence layers, not declarations of trust.

“Treat generated code as untrusted” does not mean assume every line is malicious. It means provenance does not grant authority. Human-written code should already face controls; probabilistic generation adds scale, dependency hallucination, prompt-injection paths, and correlated producer–reviewer errors that make the principle harder to ignore.

Trust is also not a bit that flips after CI turns green. A change can pass its tests and still misunderstand intent, expose a secret, add a risky dependency, violate a license, create operational load, or activate only under production data. Build a path in which each layer limits a different failure.

[Chapter 28](28-layered-supply-chain-mitigations.md) explains the evidence for layered controls. This chapter implements the generated-code path.

## Draw the trust boundaries

Map six stages:

```text
request → generation → workspace/build → review/acceptance
        → deployment → runtime
```

At each boundary, name the principal, inputs, reachable resources, policy decision, artifact, and evidence emitted. The person requesting code, the generation worker, build service, deployment controller, and running application should not silently share one identity and credential set.

Applying [NIST’s zero-trust architecture](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf) here is an inference: verify access per session, grant least privilege, and enforce policy around resources rather than trusting network location. NIST SP 800-207 did not evaluate generated code, but its separation of subject, resource, policy decision, and enforcement is directly useful.

## Stage 1: constrain generation

Give the generation process a distinct workload identity. Bind it to the repository, task, tools, and time window. Avoid developer-wide credentials and ambient cloud access.

Provide secrets by reference only when needed, through a broker that can enforce purpose and scope. Prefer synthetic fixtures for development. Treat repository documents, issues, web pages, dependency metadata, and tool output as potentially hostile content; they can carry instructions that conflict with the user’s goal.

Expose narrow task tools instead of a broadly privileged shell where practical. A schema improves inspectability but is not authorization. Bind every operation to resource-level policy, validate parameters, restrict side effects, log the policy result, and test denial paths. [Microsoft’s least-privilege guidance for AI agents](https://www.microsoft.com/en-us/security/blog/2026/07/16/least-privilege-for-ai-agents-identity-access-and-tool-binding/) supports first-class identity and tool binding as an official practice pattern, not as an efficacy trial.

## Stage 2: isolate workspace and build

Run generated changes in an ephemeral environment with a read-only base, declared writable paths, bounded CPU/memory/time, and no host socket. Default-deny network egress; allow specific destinations and methods when the task requires them. Separate package retrieval from arbitrary network access and record resolved artifacts.

Containers reduce accidental interference but share a kernel. MicroVMs or user-space-kernel designs can strengthen isolation, yet still depend on the VMM or interception layer, images, devices, networking, credentials, telemetry, and correct operation. The [Docker comparison of agent sandbox approaches](https://www.docker.com/blog/comparing-sandboxing-approaches-ai-agents/) is a first-party mechanism guide; an [independent microVM survey](https://emirb.github.io/blog/microvm-2026/) provides complementary architectural boundaries. Neither supplies a universal escape-rate comparison.

Build reproducibly where feasible. Pin dependencies, verify expected source and integrity data, create an SBOM or equivalent inventory, and prevent build scripts from inheriting deployment credentials. Preserve the input commit, generator/harness/model version, declared prompt or task record, dependency resolution, build environment, and artifact digest.

Quarantine failed and abandoned builds as evidence, not as reusable artifacts. A later agent should not silently discover a half-built workspace and treat its generated files, downloaded tools, or modified configuration as trusted starting state.

## Stage 3: accumulate independent evidence

Use different checks for different claims:

- compiler, type, schema, and policy checks for encoded constraints;
- unit, property, mutation, integration, and adversarial tests for behavior and test strength;
- static and dependency analysis for selected weakness classes;
- domain review for intent, tradeoffs, and consequences;
- staged execution for environmental behavior;
- provenance and license checks for origin and obligations.

No single green check confers merge authority. The [OpenSSF security-focused guide for AI code-assistant instructions](https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions.html) is useful official practice guidance around validation, dependency hygiene, secrets, and review. It is not proof that following a checklist makes code secure.

Make reviewer independence visible. If the same model generated the patch, tests, and review under the same context, treat agreement as correlated evidence. Use deterministic oracles where possible, hidden faults, separate domain judgment, and security tooling with understood coverage.

## Stage 4: deploy with bounded blast radius

The deployment principal should receive only the authority needed for an approved artifact and environment. The generation process should not possess production deployment credentials. Require signed or otherwise durable provenance that connects reviewed source and build evidence to the deployed artifact.

Use progressive delivery, health gates, quotas, network policy, data-scope restrictions, feature flags, and tested rollback according to consequence. A canary protects little if it can still delete a global resource or exfiltrate a full dataset. Blast radius is about reachable consequence, not merely traffic percentage.

At runtime, enforce application identity and least privilege as though the code may contain an ordinary defect or a hostile path. Monitor security-relevant behavior and service outcomes. Do not depend on a sandbox to identify semantically authorized harm: code can make a valid API call that violates business intent.

The bounded [*Caging the Agents* field case](https://arxiv.org/pdf/2603.17419) documents nine healthcare-company agents, four high-severity configuration or credential findings, and a layered target architecture using gVisor, a credential proxy, per-agent egress allowlists, and trusted metadata plus untrusted-content labeling. It also exposes brittle prompt controls, exception burden, DNS/CDN maintenance, and a highly privileged audit agent. Use it as a concrete design and residual-risk account, not proof that four layers eliminate a threat class.

## A minimal policy contract

For one application-code workflow, fill this in:

```yaml
generator_identity: repo-scoped, short-lived
read_scope: named repository and approved public sources
write_scope: ephemeral branch only
secrets: none; brokered test credential by exception
network: deny by default; registry proxy allowlist
dependencies: pinned, provenance checked, age policy applied
build: isolated, reproducible where feasible, no deploy credential
acceptance: declared tests + domain review + security checks by risk
artifact: digest bound to source and evidence
deployment: separate principal, staged, reversible
runtime: least privilege, egress/data bounds, monitored
revocation_owner: named role
```

Then attack the contract. Try a prompt injection in a repository document, a nonexistent package, a build script that contacts an undeclared host, a request for a sibling repository, a secret printed to logs, a valid but overbroad infrastructure call, and an artifact swap after approval. A policy is not implemented until denial and recovery are observed.

## Measures and stop rules

Measure unauthorized attempts, false denials, dependency exceptions, secret exposures, provenance gaps, review yield, escaped faults, rollback time, evidence-reconstruction time, and human/compute cost. Track separately by risk class. A low aggregate failure rate can hide one unacceptable red-tier path.

Pause autonomous generation or deployment if:

- identities or artifacts cannot be linked end to end;
- build or agent processes acquire ambient production credentials;
- default-deny egress or resource policy is routinely bypassed;
- acceptance evidence is generated and judged by one correlated loop;
- rollback, revocation, or forensic reconstruction fails;
- operators cannot distinguish current target controls from aspirational design.

Rollback includes revoking identities, quarantining artifacts, stopping deployments, rotating exposed credentials, restoring systems, and reviewing sibling outputs produced under the same compromised assumptions.

## What good operation looks like

Generated application code is permitted to flow quickly because authority is separated from fluency. The producer cannot decide its own privileges or deployment. Build artifacts have traceable origin. Checks make bounded claims. Runtime contains ordinary and adversarial faults. Humans intervene where domain consequence or weak evidence demands it.

The label “untrusted” never graduates into “safe.” It becomes a maintained chain of explicit, revisable decisions.

Podcast hook: CI passed, the image was signed, and the sandbox held—so how did a perfectly authorized API call still cause harm?

Continue reading: [Chapter 53: Delay and screen new dependencies](53-delay-screen-dependencies.md) applies the same trust chain to the moment a generated package name enters the build.
