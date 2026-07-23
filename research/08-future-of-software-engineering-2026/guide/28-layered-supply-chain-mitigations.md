# 28. Delay, registries, microVMs, and internal zero trust

Dependency-age gates, curated registries, provenance checks, review, scanning, narrow authority, and stronger execution isolation block different stages of a supply-chain attack. They are useful in combination, but the audited corpus cannot assign a risk-reduction percentage to any layer or prove that a two-week delay is optimal.

The [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) proposes roughly fourteen days before adopting new versions, vetted registries, microVMs, and zero-trust treatment of generated code. The practices have credible mechanisms. The interval and effect claims remain anonymous retreat conclusions.

## A plain-language model: interrupt the chain

Defense in depth resembles several doors along a corridor. A package must be selected, resolved, downloaded, built, executed, reach valuable data or credentials, and persist into production. A control is valuable when it interrupts a named transition.

- An **age gate** delays selection of a fresh version.
- A **curated registry or allowlist** constrains where packages come from.
- **Identity, signatures, provenance, lockfiles, and review** make source and change inspectable.
- **Static and malware analysis** look for known or suspicious content.
- **Narrow credentials and egress** reduce what successful code can reach.
- **Sandboxing or microVMs** move the execution boundary and limit host access.
- **Deployment gates and runtime detection** constrain production entry and detect behavior after release.

Layers are not simply additive. They can share blind spots, rely on the same metadata, or be bypassed through one emergency exception. A stack of nominal controls can still have one effective point of failure.

## What a delay really does

StepSecurity documents a configurable [npm package cooldown check](https://www.stepsecurity.io/blog/introducing-the-npm-package-cooldown-check) with a default 48-hour requirement and administrator override. Socket describes pnpm’s configurable [`minimumReleaseAge`](https://socket.dev/blog/pnpm-10-16-adds-new-setting-for-delayed-dependency-updates), along with exclusions and examples of longer configurations. These vendor sources prove implementability. Their defaults and examples are policy choices, not experimentally derived optima.

A named September 2025 npm incident gives one useful timeline. [Sygnia reports](https://www.sygnia.co/threat-reports-and-advisories/npm-supply-chain-attack-september-2025/) that a maintainer phishing compromise led to a malicious release at 13:16 UTC; community suspicion appeared one hour later, the maintainer acknowledged the breach by 15:15, and npm takedown began at 17:17, with cleanup continuing the next day. At least 18 packages were affected. The event was not AI-related or slopsquatting. It shows that a short delay can sometimes allow public response to start; one incident cannot establish the detection-time distribution or its long tail.

ActiveState’s vendor argument, [“A Cooldown Is Not a Sourcing Strategy”](https://www.activestate.com/blog/beyond-dependency-cooldowns/), names patient payloads, transitive dependencies, broad version ranges, weak publisher authentication, bypass paths, and urgent patches as residual risks. Its preferred intervals are opinions rather than outcome evidence, but the critique correctly separates age from trust. A malicious package can wait.

Fourteen days therefore has no general evidentiary basis in this corpus. A local interval should balance immediate-adoption exposure against security-patch delay, operational urgency, ecosystem speed, and the organization’s other controls. It needs an audited emergency path, because exceptions often become the real policy.

## Registries, provenance, and review

The [OpenSSF security guide for AI code-assistant instructions](https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions.html) advises constraining new dependencies, verifying source and reputation, pinning versions, maintaining inventories and SBOMs, using signatures and scanners, avoiding secrets, and retaining human responsibility. This is expert normative guidance, not a controlled efficacy study. Prompt instructions can be ignored and should not be the enforcement boundary.

A curated internal registry can centralize review and block direct resolution from public sources. It does not make mirrored content safe, authenticate every maintainer, expose dormant behavior, or guarantee rapid security updates. Provenance can show who built an artifact and from what inputs without proving those inputs benign. Scanners find only what their rules and analysis can see. Reviewers face time pressure and can be manipulated by plausible generated context.

The registry also becomes a service with its own availability, compromise, freshness, and emergency-publishing risks. Its approval record should identify the artifact digest, source, reviewer, evidence, expiry or re-review trigger, and downstream consumers. Otherwise “internally vetted” can outlive the version, threat model, or evidence that originally justified it.

The [targeted dependency-steering preprint](https://arxiv.org/html/2605.09594) also shows that persistent skill or instruction artifacts can influence package selection. Governance must cover agent configurations, skills, and tool catalogs as supply-chain inputs, not only the final lockfile.

## Isolation and its residual reach

A Docker-authored [comparison of agent sandboxing approaches](https://www.docker.com/blog/comparing-sandboxing-approaches-ai-agents/) distinguishes chroot, containers, Docker-in-Docker, VMs, microVMs, and gVisor by trust boundary, compatibility, startup, resources, and complexity. Its product comparisons and performance tables are not independent benchmarks. The useful point is architectural: shared-kernel containers and hardware-backed or user-space-kernel approaches expose different escape surfaces.

An independent SRE’s [microVM survey](https://emirb.github.io/blog/microvm-2026/) reinforces that VMM choice, device model, density, compatibility, and operating burden differ. It also warns against treating containers as an equivalent isolation boundary. Neither source demonstrates production escape rates. MicroVMs retain VMM and device vulnerabilities, image risk, host integration, networking, credentials, and operational mistakes.

The bounded field case [*Caging the Agents*](https://arxiv.org/pdf/2603.17419) combines gVisor, credential proxying, per-agent egress allowlists, and metadata labeling in a target healthcare-agent architecture. It candidly reports brittle prompt controls, DNS/CDN maintenance, exception burden, and a highly privileged audit-agent paradox. The authors’ claims about coverage and overhead are self-assessed and partly concern a target still being migrated. The case supports layering because isolation alone cannot constrain authorized network or credential use.

## Internal zero trust

[NIST SP 800-207](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf) says network location should not confer implicit trust and calls for per-session, least-privilege decisions using identity, resource state, context, policy, and telemetry. NIST did not evaluate agent-generated code. Applying the architecture inside a generated-code pipeline is an inference: every agent, build, tool call, artifact, and deployment should receive only the authority needed at that moment.

This means a sandboxed process should not inherit broad production credentials. A vetted package should not bypass deployment review. A signed artifact should not obtain unrestricted egress. Detection and revocation remain necessary after preventive gates.

## The control-chain matrix

Build a matrix before purchasing another security product.

Rows are attack stages:

1. suggestion or dependency edit;
2. source selection and resolution;
3. download and build;
4. test execution;
5. deployment;
6. runtime data, credential, and network access;
7. persistence, detection, and response.

For each stage, record:

- preventive control and enforcement owner;
- evidence or detection signal;
- credential, data, and network exposure;
- likely bypass and correlated dependency;
- false-positive and false-negative cost;
- emergency exception and audit trail;
- rollback or containment action;
- current effectiveness evidence: measured locally, vendor-claimed, normative, or unknown.

Then run four tabletop cases:

- a brand-new malicious version discovered quickly;
- a dormant payload in an established package;
- a compromised legitimate maintainer;
- a hallucinated name registered before the agent suggests it again.

Mark which control interrupts each transition. The exercise will usually show that age helps only the first case, curation depends on source review, scanning has detection gaps, and isolation helps only while credentials and egress remain constrained. Test one emergency bypass because that path often collapses several layers at once.

## Evidence judgment

- **Age gates:** mechanistically credible and implementable; no universal optimal interval or measured coverage.
- **Curated sources and provenance:** useful preventive and forensic layers; neither proves benign content.
- **Scanning and review:** necessary evidence inputs with unknown false-positive, false-negative, and labor costs.
- **MicroVMs and gVisor:** stronger or different isolation boundaries than ordinary shared-kernel containers; no absolute safety or comparative incident-rate evidence.
- **Layered bundle:** moderate architectural confidence, unknown production effect size and operational burden.
- **Residual production risk:** packages can be established, patient, transitively reachable, or authorized through exceptions; code can escape the intended risk envelope through credentials, network, deployment, and policy.

Defense in depth earns its name only when every layer owns a different transition and every residual path has an accountable response.

Podcast hook: A two-week timer, a private registry, and a microVM all report green—yet the patient payload reaches production through the emergency lane. The episode maps which door each control actually guards.

Continue reading: [Chapter 27](27-slopsquatting.md) owns the hallucinated-name evidence; Chapter 52 treats generated code as untrusted, and Chapter 53 turns dependency controls into operating practice.
