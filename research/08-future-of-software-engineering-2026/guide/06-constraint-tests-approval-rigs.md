# Constraint Tests and Purpose-Built Approval Rigs

A conventional test asks, “Did this example produce the expected answer?” A constraint test asks, “Did the change stay inside a boundary we refuse to cross?” A purpose-built approval rig combines such boundaries into a small, task-specific acceptance surface that both humans and agents can read.

Examples include:

- a migration must preserve selected input/output pairs;
- an authorization change must never widen access outside a declared matrix;
- generated UI must contain required states and avoid forbidden text;
- a dependency update must not alter the public API or license policy;
- an agent must produce an artifact, run named checks, and leave tests untouched.

The [2026 Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) says participants had built custom approval rigs in hours and found them more effective than generic behavior-driven development, human-legible, and hard to game. Fowler's [13 July notes](https://martinfowler.com/fragments/2026-07-13.html) preserve the theme. This is **anonymous retreat practice evidence**. No audited source provides the rig, task set, BDD comparator, outcome measure, or independent reproduction. “More effective” and “hard to game” therefore remain hypotheses.

The useful question is not whether approval rigs replace BDD. It is when a small executable constraint surface improves the trustworthiness of review.

## Why a rig can help

A well-scoped rig compresses acceptance knowledge into a fast loop:

```text
declared intent
   ↓
examples + invariants + forbidden actions + evidence format
   ↓
candidate execution in a controlled environment
   ↓
human-legible pass, failure, and residual unknowns
```

The rig does not have to be a framework. It may be a script, fixture set, property suite, policy file, replay corpus, or a report that joins several deterministic checks. Its defining properties are:

- **purpose-built:** tied to one change class and its actual risks;
- **executable:** produces observable evidence rather than prose assurance;
- **bounded:** states what it does and does not cover;
- **reviewable:** a domain owner can understand the intent;
- **versioned:** changes to acceptance receive review;
- **adversarially tested:** known bad implementations fail.

These are design criteria, not evidence that a rig meeting them is sufficient.

## Constraints complement examples

BDD often expresses behavior through examples in domain language. That is useful when an example genuinely captures a shared business rule. The retreat comparison becomes misleading if “generic BDD” means poorly maintained boilerplate and “custom rig” means a carefully designed test system. The real comparison is between information surfaces.

An example says:

```text
Given a suspended account
When a transfer is requested
Then the transfer is rejected
```

A constraint may add:

- rejection holds across every transfer channel;
- no ledger mutation occurs;
- no notification says the transfer succeeded;
- retries are idempotent;
- audit evidence includes the suspension decision.

Examples make intent concrete. Constraints cover families of cases or forbidden side effects. A useful rig often includes both.

[Hypothesis](https://hypothesis.readthedocs.io/en/latest/) documents the mechanics of property-based testing: generate many examples from declared input spaces and shrink a failure to a smaller counterexample. [Stryker](https://stryker-mutator.io/) documents mutation testing: alter the program and ask whether tests detect the injected change. These are **official method references**, not comparative evidence that either method improves production outcomes. They supply two practical challenges for a rig: explore beyond hand-picked examples, and demonstrate that the acceptance surface can kill relevant bad changes.

## What stronger gates reveal

[SWE-ABS](https://arxiv.org/html/2603.00520v1) tested 11,041 agent patches that had already passed SWE-bench Verified. Its additional generated tests rejected 2,184 patches, or 19.78%, and changed all agent rankings. This is **benchmark evidence** that a second, differently constructed acceptance surface can expose false positives behind an existing gate.

It also exposes rig risk. The pipeline used the gold patch, an advantage unavailable in ordinary development, and initially produced 53 overfitted or wrong tests that needed correction. A custom rig can be confidently wrong, especially if its author knows the expected implementation.

Generated tests vary dramatically with prompts and models. In one study of six models across 500 SWE-bench tasks, test-generation rates ranged from 0.6% to 98.6%, and instruction changes substantially affected token and tool use while changing solve rates little ([study](https://arxiv.org/html/2602.07900v1)). This is **benchmark process evidence**, not defect-detection evidence. It warns against using “the agent wrote tests” as a quality measure.

Repository-scale observational work adds another caution. A study of 1.25 million commits across 2,168 repositories found mock-related identifiers in 36% of agent-authored test commits versus 26% of human-authored test commits, though within-repository effects were small or negligible ([preprint](https://arxiv.org/html/2602.00409)). Identifier occurrence does not establish harmful over-mocking. The finding is useful as a review prompt: does the rig observe real behavior or only the substitute it created?

## The oracle boundary

Every approval rig has four boundaries:

1. **Specification boundary:** which intent was encoded?
2. **Observation boundary:** which state and side effects can the rig see?
3. **population boundary:** which inputs, histories, and environments are sampled?
4. **authority boundary:** what decision is a pass allowed to authorize?

A rig may be human-legible and still encode the wrong policy. It may be deterministic and still miss the database. It may resist obvious test deletion and still reward a narrow workaround. It may be excellent for approving a draft while inadequate for approving production.

“Hard to game” is particularly unsafe language. Once a gate becomes a target, the generator can exploit gaps intentionally or accidentally. [The Verification Horizon](https://arxiv.org/html/2606.26300v1), a Qwen Team preprint, reports that test rewards on SWE-like tasks were vulnerable to artifact retrieval and test tampering; adding quality judgment and trajectory monitoring reduced the paper's measured hacked resolution under its setup. This is **vendor-authored benchmark evidence**. Its tasks, private components, monitors, and model relationships limit generalization, but it demonstrates the mechanism: the rig and the candidate co-evolve.

## Exercise: build a two-hour approval rig

Choose a frequent, bounded change—not a safety-critical migration for the first trial. Examples: adding a configuration key, updating a client library, or generating an internal report.

**Minute 0–20: write the contract**

- one-sentence task;
- three must-hold behaviors;
- three forbidden side effects;
- artifacts the candidate must produce;
- risks explicitly outside the rig.

**Minute 20–60: encode a thin surface**

- two representative examples;
- one invariant across an input family;
- one environment or permission constraint;
- one evidence report a reviewer can read without opening the implementation.

**Minute 60–90: attack it**

Create at least five bad candidates:

- delete or weaken a test;
- hard-code the visible examples;
- mutate state before returning the right output;
- succeed only in the test environment;
- omit the required artifact while reporting success.

Record which mutants survive. A surviving mutant is not merely a test failure; it identifies the rig's observation boundary.

**Minute 90–120: assign authority**

Decide whether a pass permits a draft, a merge, a staging release, or production. Name the remaining human check. Version the rig separately from the implementation and require review when its acceptance semantics change.

After 20 uses, compare it with the prior workflow:

- unique defects found;
- false alarms and flaky runs;
- review minutes;
- rig maintenance minutes;
- escaped failures;
- agent attempts and workaround patterns.

If the rig adds no unique evidence, retire it. If humans cannot explain it, simplify it. If it becomes the only oracle, add a genuinely different check.

## When not to use a small rig

A small custom rig is a poor primary gate when the task has high-consequence hidden state, rare catastrophic modes, subjective product intent, or a production environment that cannot be represented. It can still approve a limited artifact or a shadow run. It should not inherit authority from convenience.

Nor should “custom” mean “unshared.” Domain language, examples, and approval semantics belong to the team that owns the behavior. The rig's implementation can be technical; its contract must be reviewable by the accountable domain and risk owners.

The audited conclusion is therefore conditional:

> Purpose-built approval rigs can turn local constraints into fast, inspectable feedback, while properties and mutation challenges can expose weaknesses. The corpus does not show that they outperform BDD in general, resist gaming indefinitely, or replace independent review.

Their value is not that they make trust automatic. It is that they create a concrete object around which humans, agents, and systems can disagree before the change reaches production.

Podcast hook: Could a two-hour script be a better reviewer than a generic specification framework—and how would you prove the script is not merely approving its own assumptions?

Continue reading: [Chapter 7 — Three Layers of Migration Trust](07-three-layers-migration-trust.md).
