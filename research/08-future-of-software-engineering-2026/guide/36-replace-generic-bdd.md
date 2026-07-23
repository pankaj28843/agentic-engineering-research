# 36. Replace generic BDD only when a narrower test surface wins

> **Report point:** Playbook, bullet 36, pages 11–12 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Playbook judgment:** Replace a layered BDD surface only after a purpose-built approval rig proves easier to review and at least as good at finding relevant faults. Coexistence is a valid result.

Generic behavior-driven development can create a useful common language. It can also grow into a stack of feature prose, regular-expression steps, fixtures, page objects, mocks, and helper libraries through which nobody can see the real oracle. The mistake is to turn that observation into “BDD is obsolete.”

This playbook treats replacement as a local selection problem. The candidate is not “all BDD.” It is one behavior slice whose current test surface is costly to understand or change. The challenger is not free-form agent judgment. It is a small, executable, versioned, reviewable approval rig: a domain-specific interface that accepts meaningful inputs, observes meaningful outputs, and makes differences inspectable.

No audited source compares a generic BDD stack with such a rig across representative production systems. The retreat’s approval-rig example is a practitioner lead, not a measured winner. The process below is therefore an experiment with a reversible migration, not a universal retirement program.

## Plain mental model: shorten the distance to the oracle

A test has two jobs:

1. arrange and exercise behavior;
2. decide whether the observed result is acceptable.

Layers are useful when they hide irrelevant machinery. They are harmful when they hide the decision. A reader should be able to trace:

```text
domain example → system action → observed result → approval rule
```

If “Given an eligible account” expands through five step files, a global fixture, three mocks, and an assertion helper that accepts any 2xx response, the English is readable but the acceptance rule is not. A purpose-built surface might instead expose `quoteRenewal(customer, date)` and compare a normalized result with an approved domain record. That is better only if the normalization, fixtures, side effects, and approval policy are themselves visible.

The target is not fewer files. It is **less interpretive distance with no loss of fault detection**.

## Gate 1: select a real candidate

Choose one bounded behavior family, not an entire repository. Require at least two of these observed symptoms over a recent window:

- routine behavior changes require edits across multiple generic step or fixture layers;
- step reuse couples unrelated scenarios, so changing one domain concept breaks another;
- reviewers cannot identify the decisive assertion without executing or debugging the suite;
- failures point to framework plumbing rather than the violated domain expectation;
- agent-generated changes copy existing steps but weaken, duplicate, or bypass the oracle;
- test runtime, flakiness, or fixture construction delays feedback enough to change developer behavior;
- defect or incident analysis shows that the feature prose passed while a relevant condition was never asserted.

Do not select a suite merely because it uses Gherkin, has many files, or feels old. Keep BDD when the scenarios are actively used with nontechnical stakeholders, the mapping from prose to executable rule is direct, failures are diagnostic, and maintenance is proportionate. The custom surface must solve a demonstrated problem, not satisfy an architectural taste.

Name a migration owner, a domain approver, and a maintainer for the proposed rig. If nobody will own normalization rules, example data, tool upgrades, and disputed approvals, stop before building it.

## Gate 2: write the comparison contract

Before implementation, freeze a baseline and a decision card. Sample recent changes and record:

- median engineer time from requested behavior change to trustworthy green result;
- reviewer time to explain what the test actually approves;
- flaky or non-diagnostic failures per run;
- escaped defects and late rework plausibly inside the selected behavior boundary;
- suite runtime and infrastructure cost;
- files or abstraction layers changed per domain change;
- false alarms and waived failures;
- known blind spots, including security, concurrency, performance, and downstream side effects.

The baseline will be noisy. Use medians, distributions, and concrete cases rather than one aggregate “test productivity” score. Do not count steps deleted as value.

Define the challenger’s contract in domain terms. It should state its input schema, controllable environment, observed outputs and side effects, normalization rules, permitted nondeterminism, approval storage, reviewer workflow, and evidence retained after a run. Make an explicit list of what it does **not** prove.

The [Fowler/Böckeler harness model](https://martinfowler.com/articles/harness-engineering.html) is useful here: feed-forward guidance and feedback sensors are different parts of the steering loop, and maintainability, architecture, behavior, and human operability all matter. It is practitioner taxonomy, not evidence that more harness is automatically better.

## Build a shadow rig, not a big-bang replacement

Implement the smallest vertical slice that can run beside the existing suite.

1. **Choose representative cases.** Include ordinary paths, boundary cases, one historically troublesome case, and at least one invalid input. Trace each case to a requirement, production observation, incident, or named domain decision.
2. **Expose domain-shaped operations.** Hide transport and setup only where those details are irrelevant. Preserve a route to inspect the raw request, response, events, database effects, and logs.
3. **Make approval explicit.** Store a structured expected result or executable invariant. Require a human-readable diff for changes. Never let “update all snapshots” be the normal resolution path.
4. **Control nondeterminism.** Freeze clocks and seeds where valid; otherwise specify tolerances and explain why. Redact secrets without erasing fields whose shape matters.
5. **Run old and new in parallel.** Neither surface becomes authoritative during the observation window. Classify disagreements instead of immediately teaching one to mimic the other.
6. **Preserve traceability.** Map every retired scenario to a challenger case, an intentionally dropped assertion, or an explicit gap with an owner.

Property-based and mutation tools can challenge the new oracle. [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) shows the mechanics of generating inputs from declared domains and shrinking failures; [Stryker](https://stryker-mutator.io/) shows the mechanics of altering code and asking whether tests detect the change. Their documentation does not establish delivered-quality improvement. Use them as probes, not badges.

## Challenge both surfaces

Run an oracle workshop before choosing a winner. Ask domain experts and engineers to introduce or identify plausible faults: swapped boundaries, omitted side effects, stale defaults, authorization mistakes, partial updates, incorrect error mapping, and concurrency hazards. Seed only safe faults in a controlled branch or environment.

For every probe, record whether the legacy BDD surface catches it, the approval rig catches it, both catch it, or neither does. Investigate survivors. A surviving mutant can be a weak test, an equivalent change, an irrelevant difference, or an invalid mutant; raw mutation score is not truth.

The strongest warning comes from a benchmark, not from BDD research. [SWE-ABS](https://arxiv.org/html/2603.00520v1) strengthened tests for patches that had already passed SWE-bench Verified and rejected 2,184 of 11,041 of them. Yet 53 of 500 initially generated test additions were themselves wrong or overfit and needed correction. The bounded lesson is double-sided: fixed suites can be weak, and new tests can be wrong. A challenger must be reviewed adversarially rather than trusted because it is custom.

## Decide with a balanced scorecard

Promote the new surface only if it meets all safety floors and shows a meaningful local advantage.

**Safety floors**

- no unexplained loss of requirement or scenario coverage;
- no increase in severe seeded-fault survivors;
- raw effects and approval differences remain inspectable;
- false approvals and flaky failures stay within the predeclared tolerance;
- an accountable maintainer accepts the ongoing work;
- the old path can still run during the rollback window.

**Possible advantages**

- lower time to make and review a representative behavior change;
- fewer framework-layer edits;
- faster, more diagnostic feedback;
- more unique relevant faults found;
- lower triage and fixture-maintenance effort;
- clearer participation by the actual domain decision-makers.

Use a decision table rather than a single score:

| Result | Action |
|---|---|
| New surface improves clarity and detection at tolerable cost | Migrate the bounded slice |
| New surface is clearer but misses distinct legacy faults | Keep both while strengthening it |
| Each surface finds valuable unique faults | Deliberate coexistence |
| New surface mainly duplicates the old one | Stop expansion |
| New surface is harder to maintain or approve safely | Roll back |

## Stop conditions and rollback

Pause migration when reviewers cannot explain an approval diff, unclassified disagreements accumulate, sensitive production data is copied without a lawful handling path, the rig normalizes away meaningful behavior, or maintenance work exceeds the agreed budget for two consecutive review periods. Stop immediately if it approves a seeded high-consequence fault that the old suite catches.

Rollback should be designed before deletion:

- keep the legacy scenarios runnable and pin their dependencies through the observation window;
- migrate in small commits with a scenario-to-rig manifest;
- retain the last approved artifacts and tool version;
- route production releases back to the old gate with one configuration change;
- restore ownership and triage expectations, not only files;
- open a short failure review that distinguishes a bad interface, bad oracle, bad data, and bad rollout.

After a successful window, archive rather than silently erase the old scenarios. Record why each was retired and which evidence replaced it. If the approval rig later becomes a new opaque framework, reapply the same selection test.

## What this playbook does not claim

It does not show that custom test surfaces are cheaper in general, that BDD prose has no collaborative value, or that mutation and property testing guarantee a strong oracle. A small stable domain may benefit from a tailored rig; a cross-organizational protocol may benefit from durable shared scenarios. A bespoke interface can also become undocumented infrastructure whose only expert leaves.

The trustworthy outcome is narrower: one team can compare two review surfaces on the same behavior, preserve traceability, challenge both with plausible faults, and reverse the migration. Replacement is earned by evidence. Coexistence and retention remain legitimate findings.

Podcast hook: A beautifully readable scenario can still hide a useless assertion. Follow one team as it shortens the path from business example to executable approval—and discovers a reason to keep part of the old suite.

Continue reading: [Chapter 37, “Default to three-tier verification”](37-default-three-tier-verification.md), turns a single approval surface into a migration-wide decision framework.
