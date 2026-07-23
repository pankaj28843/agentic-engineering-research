# 37. Default to three-tier verification—then justify every tier

> **Report point:** Playbook, bullet 37, pages 11–12 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Playbook judgment:** Characterization, symbolic verification, and back-testing form a useful migration checklist, not a validated universal sequence. Each tier needs an applicability gate, an independent oracle, and an explicit skip record.

A migration team needs more than a green inherited test suite. It also needs more than a proof of a narrow property or a successful replay of yesterday’s traffic. Each answers a different question:

- **Characterization:** what did the old system observably do for selected cases?
- **Symbolic verification:** what must be true for all states covered by an encoded model?
- **Back-testing:** what happens when the candidate meets historical workload, data shape, and operating conditions?

Calling these “three tiers” is a useful default because it forces three conversations. It is not evidence that every migration needs all three, that they must run in that order, or that together they establish correctness. The audited corpus contains evidence for individual components, but no selected source compares or validates this exact stack.

## Plain mental model: three flashlights, three blind spots

Imagine inspecting a bridge at night. One flashlight illuminates the path people used yesterday. Another illuminates the engineering constraints encoded in a model. The third illuminates how the bridge behaves under recorded traffic. Overlapping light increases confidence, but darkness remains outside every beam.

Characterization can faithfully preserve an old bug. A proof can establish the wrong property. A replay can omit the rare event that matters most. The tiers are strongest when their failure modes differ and their evidence lineage is visible.

The default decision record should therefore say:

```text
tier → question → oracle owner → sampled domain → blind spots → result → skip/exception
```

Do not collapse the result to “three-tier verification passed.”

## Start with an applicability canvas

Apply the canvas to one migration slice: a protocol endpoint, batch job, calculation, parser, or state transition. Do not start at whole-system scale.

### Characterization gate

Use characterization when the old implementation can run, its observable outputs matter, and representative inputs can be assembled safely. Ask:

- Can the old and new systems receive semantically identical inputs?
- Which outputs, errors, events, state changes, and timing tolerances are observable?
- Are old results authoritative, merely informative, or known to contain defects?
- Can nondeterminism, external dependencies, and clocks be controlled or normalized?
- Who may approve an intentional difference?

Skip or narrow this tier when the old system is unavailable, unsafe to execute, legally unusable, corrupted, or so poorly observed that its output would create false confidence. Record the substitute: a protocol specification, independently curated examples, domain reconstruction, or consumer contract.

### Symbolic gate

Use symbolic or formal techniques when an important property can be expressed precisely and the analyzed state space is tractable enough to justify the effort. Candidates include arithmetic safety, state-machine transitions, access-control invariants, protocol conformance, memory safety for a bounded component, and conservation rules.

Ask:

- What property is encoded, in what language, against which abstraction?
- Which assumptions, environment models, loop bounds, and unsupported features constrain it?
- Is the checker or proof kernel independent of the generating model?
- Would a proof failure be diagnosable and actionable?
- Is the consequence high enough to pay the formalization cost?

Skip formalization for a slice when the property is mostly subjective, the environment dominates behavior, the abstraction would erase the relevant risk, or nobody can maintain the model. “Hard to formalize” is not automatically a skip for a safety-critical invariant; it can be a signal to reduce scope.

### Back-test gate

Use back-testing when historical traces or datasets represent meaningful operating conditions and can be handled lawfully. Ask:

- What population and time window produced the data?
- Were rare failures, peak periods, schema changes, and downstream effects retained?
- How will secrets and personal data be minimized, transformed, or kept in place?
- Can the candidate run without reproducing harmful side effects?
- Which distribution shifts make the replay stale?

Skip or use synthetic replay when consent, contracts, retention, privacy, or security prohibit reuse; when history encodes harmful bias that should not become an oracle; or when the migration creates a genuinely new behavior with no historical analogue. A skipped replay requires another environment-fidelity argument, not an empty checkbox.

## Build the evidence lineage before running tools

Create a small manifest for every test, property, and trace cohort:

- source and collection date;
- behavior or risk represented;
- transformation, redaction, or normalization applied;
- expected result and approving role;
- known exclusions;
- tool, model, and environment version;
- retention and access policy;
- relation to the other tiers.

This prevents false independence. Three tiers derived from the same old test fixture may produce three agreeing answers while sharing one misunderstanding. A characterization example copied into a formal property and used to select replay traces is one lineage, not three.

The migration evidence supports this caution. [RepoRescue](https://arxiv.org/html/2607.01213v1) evaluated compatibility repairs across 193 Python and 122 Java repositories. In a closer audit of 34 apparently successful unmaintained Python repairs, 22 survived a more realistic scenario, and only 12 were meaningful compatibility patches with no observed regression. Original tests and environment access were useful, but success under the first oracle did not settle realistic behavior.

## Run a staged pilot

The operational order below is a diagnostic convenience, not a law.

1. **Freeze the migration slice.** Name observable boundaries, risk, rollback, and intentional non-goals.
2. **Characterize selected behavior.** Capture ordinary, boundary, invalid, and historically troublesome cases. Classify known defects as preserve temporarily, quarantine, fix during migration, or retire.
3. **Extract candidate invariants.** Do not infer them from outputs alone. Review them with domain and operational owners.
4. **Apply the narrowest formal method that fits.** A model checker, symbolic executor, refinement type, proof assistant, or exhaustive finite-state test may qualify. Record assumptions and unmodeled behavior.
5. **Back-test in a side-effect-safe environment.** Replay cohorts by time, customer or data shape, peak load, and failure history. Compare both functional results and operational signals.
6. **Reconcile disagreements.** Never automatically vote. A proof and old output can disagree because the old system violates a desired invariant; replay and characterization can disagree because normalization hid state.
7. **Canary the candidate.** The three tiers precede production exposure; they do not replace staged rollout, observability, and rollback.

Formal evidence has a precise boundary. [AutoRocq](https://arxiv.org/html/2511.17330v3) produced kernel-accepted proofs for 824 of 1,717 mathematical lemmas and 198 of 641 lemmas derived from small deterministic C programs. That is strong acceptance relative to the encoded property. It does not prove requirement completeness, environment fidelity, or suitability for large interactive systems.

Translation evidence supplies a different warning. [*Articulate but Wrong*](https://arxiv.org/html/2605.21537v1) tested 11 models on 60 tiny Python 2 snippets across 1,980 calls. Semantic drift was much more frequent for semantic-hazard transformations, and same-model self-review missed 83 of 262 drift cases. The tasks are too small and artificial for an enterprise failure rate, but they show why fluent explanations and same-model checking are weak substitutes for independent behavior evidence.

## Define minimum evidence and legitimate skips

Make the default demanding but not ceremonial:

| Tier status | Minimum record |
|---|---|
| Applied and passed | Scope, oracle, result, blind spots, tool/data version |
| Applied and failed | Counterexample, disposition, owner, rerun condition |
| Partially applied | Covered subset, uncovered subset, reason |
| Skipped as inapplicable | Technical reason and alternative evidence |
| Skipped by constraint | Privacy, cost, time, or tooling constraint plus risk acceptance |
| Deferred | Owner, date, deployment limitation until completion |

A team may skip symbolic proof for a presentation-layer migration with no tractable high-consequence invariant. It should not skip characterization merely because writing fixtures is tedious. A replay of personal data may be prohibited even when valuable. The skip decision belongs to the named risk owner, not to the agent generating the port.

## Measure the stack, not just the candidate

For each tier, measure:

- setup and maintenance effort;
- execution latency and infrastructure cost;
- unique relevant faults or disagreements found;
- false alarms and invalid counterexamples;
- time from finding to verified resolution;
- coverage of named risks, not only lines or branches;
- overlap and shared lineage with other tiers;
- escaped defects and rework during the canary and observation window.

Track **cost per unique actionable finding** and **severe-risk coverage** separately. A cheap tier that finds only duplicates may still be useful as fast feedback. An expensive proof may be justified for one catastrophic invariant. No scalar score should erase consequence.

The [Thoughtworks modernization account](https://www.thoughtworks.com/insights/articles/claude-code-cobol-modernization-reality) emphasizes discovery, static and dynamic analysis, tacit constraints, data migration, synchronization, dual running, and cutover. It is consultancy practice evidence, not a trial of this stack. Its main contribution is to remind us that verification work extends beyond translated code.

## Stop, rollback, and refresh

Stop promotion when:

- two tiers agree only because they share the same unreviewed oracle;
- unexplained differences exceed the predeclared threshold;
- a high-consequence invariant cannot be encoded or otherwise checked;
- replay data handling violates its approved purpose or access boundary;
- the formal model omits the mechanism behind the named risk;
- triage cost grows without unique findings;
- canary signals move outside the rollback envelope.

Rollback the migration slice, not the evidence. Route traffic to the old implementation, retain the candidate and counterexamples, revoke replay-data access that is no longer needed, and pin the verifier versions required to reproduce decisions. If the old system is itself unsafe, rollback may mean a safe degraded mode or quarantined adapter rather than full restoration.

Refresh characterization cases after intentional behavior changes, properties after design changes, and replay cohorts after material distribution shifts. Give each evidence artifact an owner and review-by date. A three-tier stack with stale tiers is three kinds of historical reassurance.

## What survives skeptical review

The three questions are durable: what was observed, what must always hold inside a model, and what happens under representative conditions? Their combination makes blind spots discussable and disagreements diagnostic.

What remains unproven is the exact stack as a universal default, its ordering, and its cost-effectiveness. Some slices need all three; some need one strong tier plus different controls; some cannot safely use the old system as an oracle. The playbook’s discipline is to make application, omission, lineage, and residual risk explicit before a migration earns trust.

Podcast hook: Three green lights illuminate three different parts of a migration—and still leave one critical behavior in the dark.

Continue reading: [Chapter 38, “Coverage, adversarial probing, then mutation”](38-coverage-adversarial-mutation.md), tests whether a proposed verification order finds weak tests efficiently.
