# 40. Turn lint findings into agent instructions—selectively

> **Report point:** Playbook, bullet 40, pages 11–12 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Playbook judgment:** A deterministic diagnostic can become useful repair guidance when it explains a stable local rule and preserves the checker as the oracle. No audited study shows that this transformation generally improves independent outcomes.

A linter already tells an agent that something is wrong. Why add instructions?

Because a terse diagnostic can identify a symptom without explaining the repository’s intended repair. “Forbidden dependency” may not name the supported adapter. “Cyclomatic complexity exceeded” may invite cosmetic extraction rather than a coherent domain boundary. “Do not use raw SQL” may leave the agent guessing which query abstraction preserves transactions and observability.

But the opposite failure is equally common: every lint result becomes prose in a giant instruction file. Rules conflict, context grows, models change, and the agent learns to satisfy local style while weakening behavior. This playbook treats lint-to-instruction conversion as a controlled comparison among three conditions, with the deterministic check remaining authoritative.

## Plain mental model: alarm, repair card, inspection

The linter is an alarm. A repair instruction is the card beside the alarm explaining the local response. Tests and review inspect whether the response actually worked.

```text
diagnostic → bounded repair guidance → code change → original check
           → independent correctness and regression checks
```

The guidance must not replace the diagnostic. If prose and checker disagree, the executable rule wins until its owner changes it. The guidance should reduce search and wrong repairs, not broaden the agent’s authority.

## Select rules worth translating

Start from recent lint failures, repair attempts, and review comments. Choose a small rule family only when:

- the rule is deterministic and has a stable identifier;
- failures recur often enough to justify maintenance;
- the correct repair depends on repository-specific structure or policy;
- agents commonly silence, suppress, or cosmetically satisfy the rule;
- a safe preferred pattern and verification command can be stated;
- a named owner can update both rule and guidance.

Do not add guidance for a self-explanatory formatter error, a one-off migration, a disputed style preference, or a diagnostic whose false-positive rate is not understood. Fix the rule before teaching a workaround. If the right response requires product judgment, tell the agent to escalate rather than encode an invented default.

The [Fowler/Böckeler harness account](https://martinfowler.com/articles/harness-engineering.html) distinguishes feed-forward guidance from feedback sensors and warns about conflicting instructions and maintenance. It is useful architecture vocabulary, not comparative evidence that prose improves repair.

## Write a repair contract, not a slogan

For each selected rule, create a compact, versioned card:

| Field | Content |
|---|---|
| Rule ID | Exact deterministic diagnostic |
| Intent | Failure or architectural property the rule protects |
| Scope | Paths, languages, and task types where it applies |
| Preferred repair | Small ordered recipe or named abstraction |
| Forbidden shortcuts | Suppression, broad exception, mock, cast, or bypass to avoid |
| Evidence | Commands and independent checks required |
| Examples | One compliant and one deceptive near-miss |
| Escalation | When the recipe is unsafe or inapplicable |
| Owner and expiry | Maintainer, version, review date |

Keep the card near the owning code or rule, and retrieve it by rule ID only after the diagnostic occurs. Do not preload the entire catalog into every task. Link to a reusable helper rather than restating its implementation.

A good instruction says:

> `ARCH-014` means domain code imported an infrastructure client. Move the call behind the existing `PaymentGateway` port in this module; do not add a local interface or suppress the rule. Run the architecture test, unit tests for the domain service, and the contract test for the adapter. Escalate if the needed operation is absent from the port.

A bad instruction says:

> Follow clean architecture and fix all lint errors.

The first narrows search and names verification. The second adds tokens and invites interpretation.

## Design the three-arm comparison

Use comparable tasks that naturally trigger the selected rules. Include historical failures, seeded safe examples, and ordinary repository changes. Predeclare exclusions and success criteria.

Assign tasks, ideally randomly or by balanced rotation, to:

- **No added help:** ordinary repository context and the diagnostic;
- **Raw diagnostic:** exact rule ID, location, and linter text surfaced prominently;
- **Repair guidance:** the same diagnostic plus the rule card.

The first two arms may coincide if diagnostics are always visible; keep them separate only when the harness previously hid or truncated feedback. Use the same model, effort, tool permissions, task statement, and retry budget. Repeat across more than one model family if the instruction is meant to be shared.

Do not let the guidance arm receive extra hidden examples, human hints, or time. Reviewers assessing correctness should not know the arm when practical.

## Measure correctness before compliance

Record:

1. **Task correctness:** independent acceptance tests and domain review, not the linter alone.
2. **Rule resolution:** diagnostic cleared without suppression or configuration weakening.
3. **Repair quality:** the underlying smell or policy breach is genuinely removed.
4. **Regression:** unrelated tests, architecture checks, performance, security, and supported behavior.
5. **Effort:** input/output tokens, tool calls, retries, wall time, CI time, and human triage.
6. **Maintainability:** change size, duplication, new abstractions, reviewer comprehension, and later edits.
7. **Failure mode:** ignored diagnostic, literal but wrong fix, workaround, over-broad refactor, escalation, or false positive.

Keep task success and rule compliance separate. A model can clear a complexity threshold by scattering methods while making the system harder to understand. It can remove a forbidden import and quietly duplicate network code. Those are regressions even when the linter is green.

Model behavior is sensitive to instructions. [*Rethinking the Value of Agent-Generated Tests*](https://arxiv.org/html/2602.07900v1) changed test-writing instructions across six-model benchmark runs and observed substantial model-specific changes in test creation, tool calls, and tokens, while most task outcomes stayed stable. This is not a lint study. It supports only the need to test instruction effects per model and to measure cost independently from outcome.

## Challenge the instruction

Before promotion, give the card adversarial cases:

- the preferred abstraction lacks the needed capability;
- obeying the rule would change public behavior;
- two rules recommend conflicting structures;
- the diagnostic is a false positive;
- generated code or a vendored directory is in scope accidentally;
- a suppression is actually the documented exception path;
- the “correct” example is stale after an API change.

The desired response may be a structured escalation, not an automatic fix. Measure whether the agent recognizes the boundary. An instruction that works only on the happy-path example is a memorized patch, not reusable guidance.

Also run the full relevant suite. A community discussion of a code-cleanliness experiment identified an important missing outcome: hidden task tests did not check unrelated repository regressions. The [captured Hacker News thread](https://news.ycombinator.com/item?id=48798815) is only a lead to the primary experiment, and its token figures are not evidence for this playbook. Its falsifier is durable: local success can coexist with damage elsewhere.

## Promotion and placement

Promote a rule card only if, across the declared sample:

- correctness does not regress;
- deceptive compliance and suppressions decrease;
- independent reviewers judge repairs at least as maintainable;
- total effort or time improves enough to repay card maintenance;
- the effect is not confined to one memorized task;
- at least one intended model benefits and other supported models do not materially regress.

Choose placement by reuse:

- repository-local card for domain or architecture rules;
- language/tool package for stable organization-wide mechanics;
- runtime retrieval keyed by diagnostic for large catalogs;
- no instruction when the raw diagnostic already performs as well.

Version the card with the linter rule. A rule change without a guidance review should fail the catalog’s maintenance check, not the product build.

## Stop, rollback, and prune

Stop expanding when cards increase token load without better independent outcomes, models follow examples too literally, conflicts rise, false-positive workarounds accumulate, or owners cannot keep cards synchronized. Pause a specific card after a major model, framework, or architecture change until it is recalibrated.

Rollback is straightforward:

- disable retrieval of the card while leaving the linter active;
- restore the raw diagnostic condition;
- remove any merge requirement tied to guidance compliance;
- retain failed-task traces and classification;
- revert unsafe repair templates;
- keep independently valuable tests added during evaluation.

Give every card an expiry date. The practitioner counterargument in [*Stop Overengineering Your Agent Harness*](https://www.oreilly.com/radar/stop-overengineering-your-agent-harness/) is that harness features should answer observed failures and may expire as models improve. That is attributed advice without controlled outcomes, but it supplies a useful pruning hypothesis: regularly re-run the raw-diagnostic arm. If the card no longer adds value, retire it.

## Evidence boundary

No audited source directly compares no guidance, raw lint diagnostics, and repository-specific repair cards on matched tasks with correctness, regressions, tokens, and maintainability. The proposed experiment is new work. It should not inherit credibility from anonymous harness anecdotes or from unrelated token results.

The defensible pattern is narrow: retain deterministic enforcement, retrieve guidance only for recurring local repair ambiguity, test it against simpler conditions, and remove it when the marginal benefit disappears. A growing instruction catalog is not evidence of a learning organization; a shrinking catalog can be.

Podcast hook: The agent clears every lint error, the architecture gets worse, and the instruction that caused it looks perfectly reasonable. How do we test the repair advice itself?

Continue reading: [Chapter 41, “Operationalize the learn loop”](41-operationalize-learn-loop.md), generalizes a single rule card into a controlled process for proposing harness changes from failures.
