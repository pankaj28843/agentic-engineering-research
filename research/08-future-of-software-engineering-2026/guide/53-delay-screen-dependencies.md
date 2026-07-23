# 53. Delay and screen new dependencies

> **Report point:** Governance, bullet 53, page 13 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Practice judgment:** A configurable release-age gate can buy observation time, but fourteen days is not evidence-based and age never establishes trust.

Waiting before adopting a newly published dependency is appealing because it is cheap and understandable. If a malicious release is noticed and removed quickly, a project that did not install it avoids exposure. The retreat report suggests a two-week minimum.

The audited evidence supports the mechanism, not that interval. The selected corpus includes a 48-hour product default, seven-day preferences, four- and fourteen-day package-manager examples, and one named incident detected within hours. It does not contain a representative distribution of compromise-detection times, ecosystem-specific optimal windows, or patient-attacker behavior.

Use delay as one filter in a dependency admission system. Do not turn the clock into a certificate.

## Keep the threat chain intact

Agent-generated dependencies create a plausible chain:

```text
nonexistent name → attacker registers it → agent or person selects it
→ package installs → payload executes → useful access exists → harm occurs
```

Evidence at one stage does not establish the next.

A USENIX study route, [*We Have a Package for You!*](https://www.usenix.org/publications/loginonline/we-have-package-you-comprehensive-analysis-package-hallucinations-code), reports roughly 19,000 prompts per model across 16 models for Python and npm, substantial package-name hallucination, and repeatability among some nonexistent names. The rate is bounded by those model versions, prompts, ecosystems, and registry snapshots. It does not measure malicious publication, installation, execution, or compromise.

A separate Rust preprint, [*When LLMs Invent Rust Crates*](https://arxiv.org/html/2606.08444v1), evaluates 14 model variants on 2,794 tasks and reports 10,779 hallucinated recommendations among 48,494 crate recommendations. Its parser can confuse aliases or private crates, and source-level imports are not installations. The studies make name validation necessary; they do not show that slopsquatting compromises are common.

The dependency policy should therefore block nonexistent names before debating age. Once an attacker registers a hallucinated name, existence alone becomes a weak signal.

## Choose a local delay, not a magic number

[StepSecurity’s npm cooldown check](https://www.stepsecurity.io/blog/introducing-the-npm-package-cooldown-check) implements a configurable pull-request check with a 48-hour default and administrator override. [Socket’s description of pnpm minimum release age](https://socket.dev/blog/pnpm-10-16-adds-new-setting-for-delayed-dependency-updates) shows package-manager-level delay with exclusion support. These first-party pages prove implementability. Their intervals and claimed benefits are vendor or product choices, not effect estimates.

[ActiveState’s counterargument](https://www.activestate.com/blog/beyond-dependency-cooldowns/) correctly identifies patient payloads, transitive dependencies, broad version ranges, unauthenticated publishing, agent paths outside governed installers, and emergency updates as residuals. Its own seven-day preference and twelve-hour minimum are also opinions rather than estimates from a representative incident distribution.

One named [September 2025 npm incident analysis](https://www.sygnia.co/threat-reports-and-advisories/npm-supply-chain-attack-september-2025/) reports a malicious version at 13:16 UTC, community suspicion about an hour later, maintainer acknowledgement at 15:15, and npm takedown beginning at 17:17. It involved maintainer phishing and at least 18 packages, not agent hallucination. It demonstrates that observation time can matter; one fast case cannot locate the tail or validate 48 hours, seven days, or fourteen days.

Choose the interval from:

- ecosystem publication and response characteristics you can observe;
- the harm of immediate adoption;
- the cost of delayed security, compatibility, or business fixes;
- whether dependencies are direct, transitive, build-time, or runtime reachable;
- your own detection and emergency-response capability.

Document the rationale and revisit it. Different repositories and dependency classes may need different windows.

Measure age from the exact version’s publication, not from the package’s original creation or the day a pull request happened to open. A mature package can publish a brand-new malicious version; an old lockfile can also resolve a fresh transitive release when version ranges remain broad.

## Build the full admission path

For every proposed new package or version:

1. **Resolve identity.** Confirm exact ecosystem, normalized name, publisher or organization, expected source repository, and package ownership. Reject unresolved or nonexistent names.
2. **Check intent.** Require the proposer to explain why existing code or an approved dependency is insufficient. Generated prose is not approval.
3. **Apply source policy.** Prefer approved registries, namespaces, mirrors, and maintainers. Make typo, ownership-transfer, and look-alike checks explicit.
4. **Apply the age gate.** Enforce the configured minimum against the exact version publication time. Fail closed when metadata is missing.
5. **Inspect provenance and integrity.** Verify available signatures, attestations, source-to-build claims, and expected digests without assuming any one signal is complete.
6. **Analyze content.** Run malware, vulnerability, license, build-script, and policy checks with known limitations.
7. **Review transitive and reachable use.** A vulnerable library that cannot reach a sensitive path differs from an install-time script or widely invoked parser. Preserve the dependency graph and lockfile.
8. **Contain build and runtime.** Use isolated builds, scoped credentials, constrained egress, least-privilege runtime, and monitoring so an admitted defect has bounded consequence.
9. **Record the decision.** Link package, version, purpose, evidence, approver or policy, exception, artifact, and downstream services.

A cooldown without these steps delays both good and bad code indiscriminately. The other controls decide what the extra time is used for.

## Design the emergency path first

Delaying a critical security fix can be more dangerous than accepting a fresh version. Create a narrow exception:

- a named incident or product-risk owner requests it;
- the exact version and urgency are recorded;
- source, publisher, content, provenance, and reachable change receive accelerated review;
- build and runtime privileges are tightened where feasible;
- deployment is staged with enhanced observation;
- rollback or compensating control is prepared;
- the exception expires and receives retrospective review.

Do not encode a permanent exclusion because one package once needed urgency. Exclusions are high-value attacker targets and should be scoped by package, version or condition, repository, owner, and time.

## Pilot the policy

Run the age gate in report-only mode on several repositories for four weeks. Capture proposed dependencies, version ages, direct/transitive status, reason for adoption, security urgency, eventual decision, reviewer effort, and whether external advisories or takedowns appeared during the wait.

Then enforce it on a bounded set while keeping the emergency path available. Measure:

- proposals delayed, blocked, approved, and excepted;
- time-to-merge and time-to-remediate;
- false identity or hallucinated-name findings;
- malicious, vulnerable, abandoned, or policy-incompatible packages found;
- transitive and runtime-reachable exposure;
- bypass through alternative installers, vendoring, generated code, or broad version ranges;
- human effort and exception aging;
- incidents and near misses before and after, with exposure denominators.

Do not claim success from the number of blocked packages. A policy that delays hundreds of harmless updates and detects nothing may still have reduced an unobserved risk, but it has not measured that reduction. Pair operational metrics with adversarial exercises and incident evidence.

## Stop and rollback rules

Revise or suspend the policy if emergency security fixes are dangerously delayed, teams routinely bypass the governed path, metadata is unreliable, false blocks overwhelm review, or the chosen interval provides no decision value relative to its cost. The answer may be a different interval, a different policy per package class, stronger source curation, or more automated screening.

If a dependency is later found malicious or compromised, stop builds and rollout, quarantine relevant artifacts, rotate exposed credentials, identify affected versions and reachable paths, restore from known-good artifacts, and inspect sibling projects. A package older than the threshold receives no presumption of safety.

## What good operation looks like

New dependencies enter through one observable path. Names and owners are resolved, versions are pinned, provenance and content are screened, reachability is understood, build and runtime are constrained, and exceptions are urgent but auditable. The delay is configurable and justified in local terms.

The policy never says “fourteen days makes a package safe.” It says “we will not be the first observer without a reason, and time is only one of the signals we require.”

Podcast hook: If a malicious package patiently waits fifteen days, what exactly did the fourteen-day rule prove?

Continue reading: [Management interlude: The compressed hype cycle](53a-management-compressed-hype-cycle.md) closes the guide by turning this and the other report claims into a repeatable decision posture.
