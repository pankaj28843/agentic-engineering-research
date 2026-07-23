# 32. Reimplementing a contribution’s intent from scratch

Maintainers can sometimes turn a proposed contribution into a fresh issue, specification, and implementation. The audited evidence does not establish that this is a generally safe way to accept AI-assisted ideas, reduce review cost, or separate unprotected intent from protected expression. Passing tests does not prove independence, license compliance, authorship, security, maintainability, or community legitimacy.

The [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) sketches a workflow: extract a pull request’s intent into prose, evaluate the idea, reimplement it from scratch, and credit the contributor. That is a thoughtful hypothesis from an anonymous discussion, not an evaluated clean-room method. Whether it is permissible depends on facts, licenses, jurisdiction, project policy, and process. This chapter is an evidence and workflow analysis, not legal advice.

## A plain-language model: five layers, not one “idea”

A contribution arrives as a bundle:

1. **Intent:** the problem the contributor wants solved and the outcome they value.
2. **Behavior:** inputs, outputs, APIs, compatibility, edge cases, and performance visible to users.
3. **Expression:** source structure, algorithms, names, comments, tests, documentation, and other concrete choices.
4. **Provenance:** who or what produced each artifact, which materials were consulted, what licenses and representations attach, and who can attest to it.
5. **Community relationship:** attribution, consent, communication, trust, review norms, and authority to decide.

Rewriting prose or code may change expression. It does not automatically reset the other layers. A specification can copy distinctive structure; an implementation can be behaviorally compatible yet still provoke dependence or attribution questions; a legally defensible process can still damage community trust. Conversely, visible similarity does not by itself settle legal dependence.

Tests occupy the behavior layer. They can show that selected examples pass. They cannot demonstrate that the specification is complete, the new code was independently created, untested behavior is compatible, ownership is clear, or future maintenance will be affordable.

## Why maintainers are considering new gates

The best quantitative source in this phase, the preprint [*Augmentation with Dilution*](https://arxiv.org/html/2606.26289v1), studied 2,808 repositories detected as adopting coding agents and 8,289 propensity-matched controls, covering 454,977 repository-months. It found no statistically significant change in the absolute number of human contributors, but found lower human-contributor density, a 3.7-point reduction in newcomers’ relative share, and about 5.3% greater review depth after adoption.

These are structural signals, not proof that AI submissions displace people or create 5.3% more maintainer work. “Review depth” is comments per review, not hours or quality, and excludes roughly 268,000 repository-months without review activity. Detection, treatment timing, matching, the public repository sample, unobserved confounding, and preprint status constrain causality and transfer. Still, the study supports asking how intake composition and review patterns change.

The qualitative preprint [*An Endless Stream of AI Slop*](https://assets.empirical-software.engineering/pdf/ieeesw26-ai-slop.pdf) coded expressed perceptions in 15 Reddit and Hacker News threads selected for explicit use of “AI slop.” Participants described review friction, quality degradation, incentives, consequences, and mitigation ideas. The selection term, platforms, small final corpus, and absence of a prevalence design mean this is evidence of concerns people articulate—not the rate or cause of poor contributions.

Projects are responding in different ways. A study of public governance materials from [67 visible open-source projects](https://arxiv.org/html/2603.26487) identified seven concern areas, three interpretive governance orientations, and twelve recurring strategies involving accountability, verification, provenance, incentives, review capacity, and platform controls. Its English-, GitHub-, policy-visible sample and cross-sectional coding do not reveal actual compliance or policy effects. The important result is pluralism: “ban” and “allow” are not the only choices.

## Current policies contradict one universal workflow

An [LLVM community RFC](https://discourse.llvm.org/t/rfc-llvm-ai-tool-policy-human-in-the-loop/89159) proposes that contributors understand, review, explain, revise, and accept responsibility for submitted changes, with disclosure for substantial generated content. The long official discussion records dissent about inclusion, objective criteria, burden, exceptions, and policy lock-in. It is evidence of a live governance choice, not proof of final adoption or benefit.

[QEMU’s current provenance documentation](https://www.qemu.org/docs/master/devel/code-provenance.html) takes a stricter position: it says contributions known or suspected to include or derive from AI-generated content will be declined because contributors must satisfy the project’s Developer Certificate of Origin obligations. Researching APIs or algorithms, debugging, and static analysis sit outside that content restriction; specific exceptions can be proposed. This proves QEMU’s stated posture, not settled law, reliable detection, uniform enforcement, or effectiveness.

GitHub, both a platform owner and AI-tool vendor, describes low-friction submission volume as a [trust and review-capacity problem](https://github.blog/open-source/maintainers/welcome-to-the-eternal-september-of-open-source-heres-what-we-plan-to-do-for-maintainers/). It reports shipped pull-request and interaction controls and calls criteria-based gating and automated triage exploratory. It also acknowledges that restrictions can disproportionately affect good-faith newcomers. The page provides no comparative effect on maintainer time, quality, or contributor retention.

These sources support explicit project policy, contributor accountability, evidence gates, and controlled intake. They do not select intent extraction and reimplementation as the best policy.

## The chardet dispute exposes the unresolved seams

Independent commentary on the [chardet 7.0 rewrite dispute](https://shujisado.org/2026/03/10/can-you-relicense-open-source-by-rewriting-it-with-ai-the-chardet-7-0-dispute/) describes a ground-up, MIT-licensed, API-compatible replacement for an LGPL line and an objection from a person claiming to be the original author. The objection argued, among other things, that access to the old implementation undermined a clean-room theory.

The commentator separates access and dependence, similarity, derivative-work doctrine, process, attribution, and community legitimacy. That separation is the contribution. The author did not perform a full similarity analysis, verify the objector’s identity, or adjudicate the dispute and expressly offers no definitive legal conclusion. It therefore proves neither infringement nor independence.

The case is a counterexample to the idea that “generated from prose” closes provenance. Old-code access, the provenance of the prose and tests, API compatibility, generated and human edits, licenses, identity, and project authority all still matter.

The Linux Foundation’s normative article on [AI licensing](https://www.linuxfoundation.org/blog/the-open-source-legacy-and-ais-licensing-challenge) reinforces the decomposition. It treats code, weights, data or other materials, attribution, downstream rights, and outputs as distinct artifacts. Its proposed framework is not evidence of legal sufficiency, uptake, enforceability, reproducibility, or equal access, but it shows why a code-only record is incomplete.

## A controlled intent-dossier experiment

If a project wants to test the retreat workflow, do it as a bounded governance experiment—not a laundering shortcut.

### 1. Establish authority first

Confirm that project policy permits the experiment. Name the maintainer decision owner and obtain appropriate project and legal guidance for the relevant licenses and jurisdiction. Ask the contributor’s consent to restate and test the idea, define how they will be credited, and preserve their original submission rather than silently replacing it.

### 2. Build an intent dossier

Record the original issue and contribution, contributor statements, tools and models disclosed, source materials consulted, licenses, old-implementation access, dates, and every human or generated transformation. Separate:

- problem and user outcome;
- public interface and compatibility requirements;
- examples and executable tests;
- non-functional and security constraints;
- implementation suggestions that must not masquerade as requirements;
- unknowns and disputed interpretations.

Invite the contributor and domain maintainers to correct the dossier. A prose summary written by the same model from the same code is not automatically independent.

### 3. Decide whether reimplementation is worth doing

Evaluate value, scope, fit, threat model, maintenance ownership, and review capacity before generating code. Compare with reviewing the original, asking the contributor to revise it, implementing manually, postponing, or rejecting. Reimplementation can cost more because maintainers must now review the idea, specification, generated code, provenance, and relationship.

### 4. Define a fresh-build protocol

Choose who may see which artifacts and document that choice. Whether a clean-room-like separation is appropriate is a project-specific legal and governance question; do not attach the label merely because a new model session was opened. Version the specification and tests, record model and prompt provenance, and prohibit unrecorded copying.

### 5. Verify multiple dimensions

Run behavior and compatibility tests, security analysis, dependency and license checks, similarity analysis where appropriate, maintainability review, and an independent provenance review. Inspect untested edge cases and documentation. None of these checks substitutes for the others or guarantees legal safety.

### 6. Make the community decision visible

Publish the rationale, credit, evidence, dissent, exceptions, and maintenance owner that policy allows. Give affected people an appeal or correction route. Stop if authority, provenance, contributor consent, review capacity, or security cannot be resolved.

Measure maintainer hours, contributor experience, defects, review cycles, later maintenance, and disputes against the project’s normal intake path. Without that comparison, “low maintainer cost” remains an assumption.

## Evidence judgment

- **Need for changed intake governance:** moderate evidence that contribution composition, review patterns, and expressed concerns are changing; no ecosystem-wide burden rate.
- **Intent-dossier workflow:** plausible as a controlled project process, but unvalidated.
- **Safe separation of intent and expression:** not established. Behavior, expression, provenance, licensing, and community legitimacy remain intertwined.
- **Reduced maintainer cost:** unsupported. The extra specification, provenance, legal, security, and review work may cost more.
- **Policy choice:** project-specific. Official examples range from proposed human-accountability rules to broad provenance restrictions.

The durable idea is not “regenerate and the problem disappears.” It is “separate the questions, preserve the evidence, and let an accountable community decide.”

Podcast hook: A promising pull request is converted into a clean-looking prose specification and rebuilt overnight. The mystery is whether anything became independent—or whether provenance, expression, and community trust merely changed form.

Continue reading: [Chapter 33, “Will open source shift from code to specs?”](33-open-source-code-to-specs.md), tests the broader ecosystem hypothesis that the reimplementation idea implies.
