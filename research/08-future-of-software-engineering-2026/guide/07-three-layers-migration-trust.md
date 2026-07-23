# Three Layers of Migration Trust

A migration can compile, pass its tests, and still be wrong. It can preserve every observed behavior and still preserve a security flaw that should have been removed. “Equivalent” is not one property; it is a collection of claims about selected behavior, inputs, state, timing, failure, and operations.

The [2026 Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) proposes a memorable three-layer pattern:

1. characterization tests;
2. symbolic execution;
3. production back-testing.

The pattern is useful because its layers ask different questions. The report calls the approach rigorous and novel, but it provides no named implementation, workload, incremental coverage result, operating cost, or failure analysis. It is **anonymous retreat practice evidence**, not validation of a standard stack.

Treat the three layers as a hypothesis for combining different kinds of evidence, not a recipe whose ingredients guarantee trust.

## Layer 1: characterization tests

Characterization tests record what the current system does for selected cases. They are especially valuable when written requirements are incomplete. The old system becomes a reference implementation:

```text
historical input + historical state
             ↓
        old-system output
             ↓
      executable expectation
```

What this layer can establish:

- selected examples still produce selected observable results;
- known edge cases and past incidents do not regress;
- the new system disagrees with the old one in a reproducible way.

What it cannot establish:

- unobserved inputs or paths are equivalent;
- hidden side effects match;
- performance and failure behavior are acceptable;
- old behavior is desirable;
- the fixtures represent future production.

[RepoRescue](https://arxiv.org/html/2607.01213v1) demonstrates this boundary at repository scale. Its benchmark admitted repositories only after their original tests passed in a recovered historical environment and failed in a modern one. Agent systems then tried to restore compatibility. Among 34 unmaintained Python repositories that appeared to pass the original suite after repair, only 22 passed realistic-use scenarios; targeted bug hunting found five rescue-caused regressions, leaving 12 with both a meaningful compatibility patch and no observed regression.

This is **whole-repository benchmark evidence** that a historical executable baseline is powerful and incomplete. It studies compatibility rescue, uses one trial per system and condition, and remains bounded by existing tests and added scenarios. It supports additional layers; it does not prescribe which.

## Layer 2: symbolic execution and formal checks

Examples sample behavior. Symbolic execution reasons over classes of inputs and paths by representing values symbolically and collecting path conditions. Related formal techniques ask a prover or solver to establish a property for all states inside a model.

What this layer can establish:

- an encoded invariant holds across explored or proven paths;
- arithmetic, bounds, state, or control-flow properties follow from stated assumptions;
- a counterexample exists within the model when a property fails.

What it cannot establish:

- the property is the right expression of business intent;
- external services, concurrency, time, data quality, and infrastructure match the model;
- path exploration is computationally feasible;
- unmodeled behavior is safe.

[AutoRocq](https://arxiv.org/html/2511.17330v3) is an instructive bounded result. An LLM agent proposes and refines tactics using feedback from the Rocq theorem prover; the final proof is accepted by the deterministic proof kernel. It proved 824 of 1,717 mathematical lemmas and 198 of 641 program-verification lemmas derived from 131 deterministic small C programs.

This is **formal-method empirical evidence** that probabilistic search can produce kernel-checked proofs for encoded obligations. The program set is small and deterministic; only 30.9% of the program-verification lemmas were solved. A successful proof establishes its stated property, not complete program correctness, production equivalence, or the cost-effectiveness of formalizing a legacy estate.

Symbolic execution may be infeasible on path-rich, concurrent, reflective, or environment-heavy systems. In those cases, bounded model checking, property tests, static analysis, or formal checks around a critical core may supply more value than pretending to verify the whole program.

## Layer 3: production back-testing

Production back-testing runs the candidate against recorded or shadowed real workloads and compares selected observations with the current system. It is not the same as sending uncontrolled writes to production. A careful form may replay sanitized traffic, mirror read-only requests, run a batch in parallel, or compare reports before cutover.

What this layer can establish:

- behavior on the observed workload and environment;
- differences in outputs, latency, resource use, and selected side effects;
- unexpected cases missing from hand-authored fixtures;
- operational effects visible only under realistic volume or data shape.

What it cannot establish:

- behavior on rare future inputs absent from the replay;
- equivalence when nondeterminism makes exact comparison meaningless;
- safety of irreversible external effects;
- permission to retain or replay sensitive data;
- correctness of shared downstream dependencies.

Thoughtworks practitioners describe data synchronization, possible dual running, and cutover as distinct modernization concerns ([practice account](https://www.thoughtworks.com/insights/articles/claude-code-cobol-modernization-reality)). This is **consultancy workflow evidence**, not a measured back-testing result. It supports the operational boundary: source translation is only one part of a system migration.

## The value comes from disagreement

Three green layers are comforting, but disagreement is more informative:

- Characterization passes; proof fails: the examples did not cover an invariant violation.
- Proof passes; replay fails: the model omitted an environmental interaction.
- Replay passes; characterization fails: production traffic did not exercise a known contractual edge.
- All pass; expert rejects: the stack faithfully preserved behavior that policy requires changing.

The layers are not independent merely because their names differ. If characterization fixtures and production replay use the same sampled traffic, they may share blind spots. If the agent writes the migration and formal property from one summary, the proof can perfectly certify the misunderstanding. If old and new systems call the same faulty service, differential comparison can agree on a shared failure.

The architecture should therefore record **evidence lineage**: who selected the cases, where properties came from, which data populates replay, and which assumptions are shared.

## Counterevidence from confident self-review

A short-snippet modernization study provides a useful warning. [“Articulate but Wrong”](https://arxiv.org/html/2605.21537v1) tested 60 Python 2 snippets of at most ten lines across 11 models and three prompt conditions, producing 1,980 modernization calls. A type-strict external oracle found 39.7% aggregate semantic drift in the semantic-hazard group versus 7.0% in benign controls. Same-model textual self-review missed 83 of 262 drifted outputs, or 31.7%.

This is **reproducible snippet-benchmark evidence**. It does not represent repository migration, independent-model review, or tool-backed agents. Its lesson is narrower: an articulate explanation by the generating model is not behavioral evidence. The verifier must interact with the property, environment, or system, not merely ask the candidate to reassure itself.

## Exercise: design an evidence matrix

Select one migration slice, such as one batch job, API method, or compatibility repair. List the claims that matter:

| Claim | Characterization | Formal/symbolic | Back-test/replay | Residual owner |
|---|---|---|---|---|
| functional output | named examples | invariant or relation | observed workload diff | domain expert |
| state mutation | before/after fixture | transition property | shadow-state comparison | data owner |
| failure behavior | known fault cases | no forbidden state | injected/replayed failures | operator |
| performance | threshold examples | usually limited | latency/resource distribution | SRE |
| security/policy | known abuse cases | access invariant | monitored shadow traffic | security/risk |
| intentional change | old/new expected difference | new property | observed impact | product owner |

For every occupied cell, record:

- the oracle and its owner;
- the environment and data;
- false-positive and false-negative risks;
- whether the evidence shares inputs, author, model, or assumptions with another cell;
- the authority a pass grants;
- the cost and runtime frequency.

Then create one known-bad migration for each layer. If a layer does not fail, narrow its claim or strengthen it. Rehearse a disagreement and decide who resolves it before the real migration.

Finally, keep an **intentional-difference ledger**. Not every old/new mismatch is a defect. Mark the policy, security, performance, or product reason for each accepted divergence. A migration that preserves everything may be as wrong as one that preserves too little.

## A layered claim, not layered certainty

The corpus supports the components separately: historical tests and environment checks expose bounded compatibility evidence; kernel-checked proofs establish encoded properties; realistic-use scenarios catch failures behind green suites; workflow accounts show why data and operation must enter the migration boundary.

It does not establish the exact three-layer stack as a superior default, its unique incremental coverage, or its economic feasibility. High-assurance work should compose techniques according to the claim and risk, sometimes using all three, sometimes applying formal analysis to one core and replay elsewhere, and sometimes stopping because no faithful oracle exists.

Trust does not come from the number of layers. It comes from knowing which proposition each layer supports, which errors it can independently expose, and who owns the remaining uncertainty.

Podcast hook: If tests, a proof, and a production replay all say “green,” what could still be wrong—and did the three checks inherit the same misunderstanding?

Continue reading: [Chapter 8 — Hybrid Evals and Councils of Judges](08-hybrid-evals-council-judges.md).
