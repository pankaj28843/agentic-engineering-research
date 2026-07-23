# 38. Coverage, adversarial probing, then mutation—run it as an experiment

> **Report point:** Playbook, bullet 38, pages 11–12 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Playbook judgment:** Coverage, adversarial probing, and mutation expose different weaknesses. The proposed order is plausible, but no audited Part 1 source proves that it is the most efficient sequence.

Coverage tells us where tests executed. Adversarial probing asks which troublesome inputs or behaviors the test designer may have missed. Mutation asks whether tests notice selected changes to the program. These are not three versions of the same metric.

The tempting sequence is:

```text
coverage map → adversarial probes → mutation challenge
```

It has an intuitive economy. First find untouched regions. Then reason about risky behaviors within and beyond them. Finally spend mutation compute where the test suite is supposed to distinguish correct from incorrect behavior. But intuition is not a comparative result. This playbook makes the ordering itself testable and stops teams from turning a tool sequence into ritual.

## Plain mental model: map, attack plan, fire drill

Coverage is a map showing streets the patrol visited. It does not say whether the patrol noticed a burglary. Adversarial probing is an attack plan based on likely entry points. Mutation is a controlled fire drill: alter the system and see whether the alarm sounds.

A covered line can have no meaningful assertion. An uncovered line can be generated boilerplate or an impossible branch. A property-based test can generate thousands of inputs against the wrong property. A surviving mutant can represent a real oracle gap, an equivalent program, or an irrelevant change. Every signal needs classification.

The outcome of interest is not a high percentage. It is **relevant weaknesses found per unit of total verification effort, without increasing false confidence**.

## Choose a bounded experiment

Select two to six comparable modules or behavior slices that:

- have stable tests and can run reproducibly;
- contain meaningful branches or domain rules;
- can tolerate mutation in an isolated environment;
- have recent defect history, risky boundaries, or upcoming changes;
- have an owner able to judge whether a probe or mutant matters.

Avoid starting with the entire monorepo. Tool setup, generated code, integration dependencies, and equivalent mutants can swamp the learning signal.

Freeze a baseline:

- line and branch coverage, with exclusions visible;
- test runtime, flake rate, and infrastructure cost;
- recent escaped defects and late rework by failure class;
- known fault seeds or historical bug reintroductions;
- reviewer and triage time;
- mutation score if already available, including equivalent/invalid handling;
- a risk inventory independent of coverage.

Do not optimize from coverage alone. The repository-mining study [*Testing with AI Agents*](https://arxiv.org/html/2603.13724) dynamically analyzed only 531 commits across three selected TypeScript projects and found project-specific coverage changes. It measured coverage, not fault detection. Its bounded result is a warning against treating a coverage delta as delivered quality.

## Define the three stages

### Stage 1: use coverage as a locator

Run the existing suite under realistic configurations and collect line, branch, condition, and, where useful, path or state-transition information. Tag:

- unexecuted risk-relevant code;
- executed code with no observable assertion;
- error paths hidden by mocks;
- environment-dependent paths absent from the run;
- generated or defensive code intentionally excluded.

Inspect assertion reach, not just execution reach. A test that calls a payment function and asserts only “no exception” may cover every line without checking the amount, ledger entry, idempotency key, or authorization.

End this stage with hypotheses, not a target percentage: “currency rounding boundaries are exercised but not asserted,” or “timeout compensation is never reached under the current fixture.”

### Stage 2: probe adversarially

Turn the risk hypotheses into counterexamples. Use boundary analysis, state-machine transitions, invalid sequences, concurrency schedules, historical incidents, consumer misuse, and property-based input generation. [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) demonstrates generation over declared domains and shrinking of failures; its documentation does not show that generated cases outperform expert examples or production traces.

For each probe, write:

- the risk or invariant it challenges;
- why the existing suite might miss it;
- the expected decision owner;
- whether the probe reveals a product defect, test defect, ambiguous requirement, or invalid scenario;
- the minimal reproducible case.

Agents can generate probe ideas, but domain owners must reject nonsensical or requirement-leaking cases. Keep a sample of rejected probes and reasons; otherwise prompt changes can inflate “findings” by producing noise.

### Stage 3: mutate selectively

Apply mutation operators to risk-relevant code and to logic whose tests claim strong discrimination. [Stryker](https://stryker-mutator.io/) defines the operational mechanic: modify program behavior and see whether tests kill the mutant. Start with changed lines and high-consequence rules, then expand if the yield justifies it.

Classify every sampled survivor:

- meaningful weak-test signal;
- equivalent behavior;
- irrelevant under the supported contract;
- invalid or uncompilable mutant;
- environmental or tooling failure;
- unresolved.

Do not reward teams for killing equivalent mutants with brittle assertions. Mutation score without a survivor taxonomy invites gaming.

## Compare orderings instead of assuming one

If the modules are sufficiently comparable, rotate the order:

- cohort A: coverage → adversarial → mutation;
- cohort B: mutation → adversarial → coverage inspection;
- cohort C: adversarial → coverage → mutation;
- optional control: existing workflow only.

If sample size is too small for a credible quantitative comparison, run a repeated crossover over several change cycles and treat conclusions as local qualitative evidence. Randomize module assignment where practical. Use the same time budget, fault seeds, tool versions, and classification rubric. Keep evaluators blind to the ordering when judging whether a finding is relevant.

Record incremental yield after each stage:

```text
unique relevant findings
────────────────────────────────────────
engineer + agent + CI + triage effort
```

Also record severe findings separately; one access-control flaw should not be averaged away by twenty style-level mutants.

The closest strong evidence is not an ordering trial. [SWE-ABS](https://arxiv.org/html/2603.00520v1) used issue context, slicing, coverage, generated tests, and mutation to strengthen benchmark suites. It rejected 2,184 of 11,041 patches already accepted by the original tests and changed all 30 agent rankings. But the pipeline had access to gold patches, used LLM filtering, and initially produced 53 wrong or overfit tests among 500 tasks. The result supports the possibility that adversarial strengthening reveals weak acceptance. It does not prove this chapter’s sequence or a production effect size.

## Use a balanced scorecard

Measure at least:

- unique relevant defects, weak tests, and ambiguous requirements found at each stage;
- severe-risk findings;
- overlap between stages;
- false probes, equivalent mutants, and unresolved classifications;
- setup, execution, and human triage time;
- CI latency and compute cost;
- test additions that remain stable after the target change;
- escaped defects and rework in the following observation window;
- developer attempts to game or bypass the metrics.

The Meta practice report on [mutation-based compliance hardening](https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/) describes thousands of mutants, hundreds of tests, equivalence filtering, compute, oracle work, and human acceptance. It is an organization-owned account without an exposed common comparator or fault outcome. Its useful lesson is operational: equivalence and review are first-order costs, not cleanup details.

Generated tests also vary sharply by model. In [*Rethinking the Value of Agent-Generated Tests*](https://arxiv.org/html/2602.07900v1), test-file generation ranged from 0.6% to 98.6% across six models on 500 SWE-bench Verified tasks each, and instruction ablations changed token and tool use much more consistently than solve rate. This does not rank test quality. It shows why an ordering calibrated to one model or prompt should not become permanent policy.

## Stop conditions

Stop or narrow the experiment when:

- mutation runtime or triage breaches the agreed budget without new relevant findings;
- more than the predeclared share of sampled survivors remains unclassified;
- probe generation produces mostly invalid domain cases;
- teams add superficial assertions only to improve coverage or mutation scores;
- flaky infrastructure makes kills and survivors irreproducible;
- the stages repeatedly find the same low-consequence issue;
- high-severity historical faults remain undetected despite improving headline metrics.

An efficient stop rule can be marginal: after two consecutive batches produce no unique actionable findings, pause expansion and review the risk model. Do not set a universal percentage. Different modules and consequences justify different thresholds.

## Rollback and durable outputs

This experiment should not endanger production code. Run mutants in isolated branches or ephemeral environments. Keep tool configuration, generated cases, classification decisions, and baseline reports versioned.

If the sequence underperforms, remove the mandatory gate, restore the prior CI path, and retain only independently valuable tests or probes. Quarantine generated tests whose intent is not understood. Revert metric-based merge requirements before they distort behavior. Preserve historical-fault cases and domain invariants even if the tool that found them is retired.

Recalibrate after major model, test-framework, architecture, or workload changes. A stage that once added unique signal can become redundant; a cheap new operator can make mutation newly worthwhile.

## What survives skeptical review

Coverage, adversarial probing, and mutation answer complementary questions. Using coverage to target reasoning and mutation to challenge assertions is a coherent starting hypothesis. Benchmark and practice evidence show that existing suites can be strengthened and that equivalence, oracle quality, compute, and human review matter.

No audited source demonstrates that this order is optimal, that a higher mutation score reduces production defects, or that generated probes are trustworthy without review. Run the sequence against alternatives, measure incremental findings and total cost, and retain the right to skip a stage whose marginal evidence is poor.

Podcast hook: The dashboard says 95% coverage, the adversary finds the missing boundary in ten minutes, and half the surviving mutants turn out to mean nothing. Which signal should the team buy next?

Continue reading: [Chapter 39, “Measure code review”](39-measure-code-review.md), applies the same outcome-and-cost discipline to human and agent inspection.
