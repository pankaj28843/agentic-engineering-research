# 10. What the “4×” and “90%” harness claims really show

> **Report point:** Harness engineering, bullet 10, page 5 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** Both headline figures remain unverified retreat recollections; they should generate experiments, not conclusions.

Two numbers in the retreat report are unusually memorable. Agent review was said to use four times as many tokens as code generation, and agents were said to fix roughly 90% of the errors found during refactoring. A number feels firmer than a story. Here, that feeling is misleading.

The source audit could not identify the experiment owner, task set, comparator, denominator, model, harness, time window, or raw runs behind either figure. Several nearby sources contain a “4×,” a token comparison, a self-review estimate, or successful repairs—but each measures a different construct.

The correct interpretation is not that the figures are false. It is that **their truth conditions are unknown**.

## A plain-language model: a number needs a noun

“Four times” is incomplete. Four times what: input tokens, output tokens, price, latency, attempts, or total compute? Compared with what: the first coding pass, a human review, no review, or a different model? “Ninety percent fixed” is equally incomplete. Ninety percent of compiler errors, review findings, test failures, security defects, or all latent faults? Did “fixed” mean a check passed once, the change survived an independent test, or the issue did not recur in production?

A minimally interpretable result has this shape:

```text
outcome = unit + population + intervention + comparator + time window + uncertainty
```

For example: “Across 200 preselected refactoring tasks, the review loop consumed a median of 4.1 times the billed input-plus-output tokens of the initial generation loop, while an independent hidden test set accepted 87% of first-round corrections.” That still would not settle customer value or generalize to another model, but at least it could be audited.

Without those fields, a precise-looking number is an **attributed observation**. It belongs in the research log, not in a business case.

## The nearby “4×” figures are not the same result

[Lilian Weng’s synthesis of harness self-improvement](https://lilianweng.github.io/posts/2026-07-04-harness/) mentions a roughly fourfold result from RE-Bench: at a two-hour horizon, the best agents reportedly achieved around four times the human **score**. Humans surpassed agents at longer horizons. That is a performance comparison, not token consumption, and this packet did not independently audit the underlying RE-Bench experiment for this claim.

A study of agent-generated tests reported a token effect under a prompt ablation, but it was not fourfold. [*Rethinking the Value of Agent-Generated Tests*](https://arxiv.org/html/2602.07900v1) found model-specific changes when an instruction to create tests was removed; the largest nearby result in the audit was a 49% input-token reduction for one model. An ablation of test-generation instructions is not the cost of agent review.

The [Hacker News discussion of a controlled code-cleanliness experiment](https://news.ycombinator.com/item?id=48798815) summarizes 7–8% fewer tokens on cleaner repository variants. The thread also exposes a decisive missing check: the experiment did not test whether agents broke unrelated repository tests. This is a useful falsifier and a route to the primary work, but neither the magnitude nor the outcome matches the retreat claim.

Another [Hacker News harness-engineering discussion](https://news.ycombinator.com/item?id=48416264) includes a commenter’s estimate that self-review could use at least five times as many tokens. It is explicitly an unmeasured community observation. Changing “5× speculation” into support for “4× measured” would be number laundering.

These near matches explain why provenance work matters. Search can easily assemble a convincing chain from unrelated quantities.

## “The agent fixed it” also needs an oracle

The 90% figure has a deeper problem: a fix cannot be evaluated independently of the detector.

If an agent writes code, writes a test, observes the failure, changes the code, and passes its own test, the loop has demonstrated internal consistency. It has not necessarily shown that the original intent was met. The test may encode the same misunderstanding, cover only the convenient path, or reward a shortcut. The [SWE-ABS benchmark-strengthening study](https://arxiv.org/html/2603.00520v1) illustrates the general danger: adversarially strengthened tests rejected 2,184 of 11,041 patches that had passed the original SWE-bench Verified tests, reducing aggregate success by 16.6 points and changing all 30 agent rankings. That is benchmark evidence, not a production estimate, but it establishes that “passed the available tests” can overstate repair success.

The problem appears in ordinary review too. A 2024 [study of security-related code-review concerns](https://link.springer.com/article/10.1007/s10664-024-10496-y) found that fixes were attempted for only about two-fifths of surfaced concerns in OpenSSL and PHP and classified 37% as successfully resolved in each project. Those percentages do not contradict the retreat’s 90%, because the populations and definitions differ. They show why “finding,” “attempting,” and “resolving” must not be collapsed.

No audited source connected the retreat’s 90% to a known set of faults, an independent verifier, or downstream outcomes. It must remain unattributed.

## What the figures may still teach

Weak provenance does not make the retreat observation worthless. It identifies two testable hypotheses.

First, verification may consume more inference than generation. That is plausible when a reviewer rereads the repository, generates counterexamples, runs tools, and iterates on failures. But a larger token bill can mean deeper checking, redundant wandering, poor context design, or a cheaper model doing more work. Cost, latency, energy, and detection value should be recorded separately.

Second, an agent may cheaply repair many faults that a harness makes explicit. Compilers, linters, type checkers, focused tests, and schema validators produce localized feedback. Agents can often act on such feedback. But high correction of **detected, machine-localizable errors** says nothing about undetected domain errors, security assumptions, or operational hazards. It may still be economically valuable; it is simply a narrower claim.

The [Fowler/Böckeler harness-engineering article](https://martinfowler.com/articles/harness-engineering.html) provides the useful architecture: feed-forward context steers the agent, while feedback sensors expose properties of its work. It also warns that tests, coverage, mutation, and manual checks do not automatically establish test quality, and that instructions can conflict or decay. This is practitioner taxonomy, not an experiment validating the two figures.

## A replication card

Before repeating either number internally, write a one-page replication card:

| Field | Required decision |
|---|---|
| Tasks | Sample rule, count, difficulty, language, repository familiarity |
| Baseline | Initial generation only, human review, another model, or existing workflow |
| Token unit | Input, output, cached, reasoning, retries, and billing conversion |
| Review boundary | Which prompts, tools, tests, and reruns count as review |
| Error population | Seeded faults, independent review findings, test failures, or incidents |
| Fix oracle | Hidden tests, mutation survivors, formal property, expert adjudication |
| Independence | Who wrote the oracle, and can generator and judge share the same error? |
| Outcomes | Detection, correct repair, regression, latency, human effort, and cost |
| Uncertainty | Per-task distribution, median, intervals, and failed/aborted runs |
| Stop rule | Fixed budget chosen before results are examined |

Run the experiment on mundane work, not only successful demos. Preserve discarded trajectories and failures. Keep at least one final test set untouched until the workflow is frozen. Report distributions: an average can hide a few enormous review loops or many zero-cost trivial tasks.

Most importantly, do not optimize the ratio itself. “Review tokens ÷ generation tokens” is not a target. A fourfold review bill can be rational for a high-risk change and absurd for a reversible text edit. The decision quantity is something closer to:

```text
incremental trusted defects caught
-----------------------------------
tokens + latency + human triage + maintenance
```

Even that ratio needs severity and false-positive costs.

## What survives skeptical review

The audited evidence does not validate the retreat’s fourfold token ratio or approximately 90% self-fix rate. Nearby numerical results measure scores, prompt ablations, code cleanliness, or informal estimates and cannot substitute for provenance.

What survives is a research agenda: verification cost deserves its own ledger, and correction rates require an independent fault oracle. Treat both headline figures as hypotheses worth reproducing under a declared protocol. Until then, do not use them to forecast budgets, staffing, safety, or productivity.

Podcast hook: How can four times the tokens and ninety percent success add up to no usable evidence?

Continue reading: [Chapter 40: Turn lint feedback into agent instructions](40-lint-to-agent-instructions.md) examines one narrow, measurable feedback loop without inheriting these anonymous ratios.
