# 42. Govern and prune shared skills as versioned products

> **Report point:** Playbook, bullet 42, pages 11–12 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Playbook judgment:** Shared agent skills need owners, compatibility evidence, discoverability, deprecation, and retirement. No audited study establishes the best ownership model or pruning cadence.

A shared skill is a reusable procedure that packages instructions, tool contracts, examples, and verification for a class of work. It may teach an agent how to migrate a database, publish documentation, repair a dependency, or audit a repository. Reuse can save effort and spread good practice. It can also spread a stale assumption or unsafe workaround to every adopter at once.

Treat the skill as a product dependency, not a clever prompt. It needs a named population, stable interface, tests, versions, support, telemetry appropriate to its risk, and an end-of-life path.

## Plain mental model: a skill is a maintained bridge

The skill bridges a user’s intent and a changing combination of model, repository, tool, and policy:

```text
intent → skill contract → model and tools → evidence → user outcome
```

Every endpoint moves. Models internalize formerly explicit behavior. Tool schemas change. Repository conventions diverge. Policies tighten. A bridge that worked last quarter may now add latency, hide a better native capability, or direct the agent to an obsolete path.

Governance should make two decisions easy:

1. whether a team can safely adopt a skill;
2. whether the organization can confidently change or remove it.

## Choose ownership by consequence and knowledge

Use one of three patterns deliberately:

- **Central ownership:** a platform team owns broad mechanical skills and organization-wide controls. This favors consistency and upgrade leverage but risks generic abstractions and slow queues.
- **Federated ownership:** a core team owns format, runtime, and policy while domain maintainers own content packages. This preserves local knowledge but requires real contribution and adjudication mechanisms.
- **Product ownership:** one product team owns a skill tightly coupled to its domain and operations. This shortens feedback but can create forks and duplicated controls.

A hybrid is usually necessary. The platform can own packaging, signing, retrieval, isolation, and compatibility tooling. Security owns mandatory control intent. Product teams own domain acceptance and consequences. The accountable maintainer for each skill must still be one named role or team.

The [Fowler/Böckeler harness article](https://martinfowler.com/articles/harness-engineering.html) identifies instruction conflict, maintenance, contribution, versioning, and legacy-system difficulty as real practitioner concerns. It does not compare ownership structures. Choose topology from local flow and risk, then measure it.

## Define the skill contract

Every catalog entry should expose:

- purpose, intended users, and supported task classes;
- non-goals and prohibited uses;
- required tools, permissions, data, and network access;
- inputs, outputs, side effects, and artifacts;
- verification steps and evidence retained;
- supported repositories, languages, models, and harness versions;
- failure and escalation behavior;
- owner, support route, version, provenance, license, and review date;
- rollback and deprecation status.

Keep the description small enough for accurate discovery. A skill that claims “handle all cloud tasks” cannot make permissions, outcomes, or evaluation reviewable. Split broad capabilities along consequence and reversible task boundaries.

Do not call a document a skill merely because an agent can read it. Reusable execution needs an observable contract. Conversely, not every useful instruction deserves packaging. A single repository rule can remain local until repeated adoption and maintenance justify sharing.

## Use a staged lifecycle

### 1. Proposal

Require a real recurring need, named adopters, an owner, and examples of current failure or duplicated work. Record why a repository-local instruction or ordinary tool is insufficient. Reject proposals whose primary goal is catalog growth.

### 2. Qualification

Run:

- **with/without tests** on matched tasks;
- **correctness and regression checks** independent of the skill’s own output;
- **compatibility tests** across every claimed model, tool, and repository class;
- **permission and denial tests**;
- **adversarial cases** for ambiguous inputs, prompt injection, stale examples, and partial tool failure;
- **cost accounting** for tokens, calls, latency, CI, and human review.

Use an untouched release set if the skill was iteratively tuned. One passing demo is not qualification.

[*Self-Harness*](https://arxiv.org/html/2606.09498v1) found different validation-gated improvements for three model families on 64 filtered terminal tasks. Its held-out split was adaptively reused for promotion, and it did not measure long-run maintenance or production safety. The bounded lesson for skills is model specificity: compatibility must be tested, not inferred from shared natural language.

### 3. Limited release

Publish to named pilot teams with a pinned version. Make activation explicit. Capture task success, refusals, overrides, cost, incidents, and support demand without collecting unrelated private content. Provide a one-step return to the prior workflow.

### 4. General availability

Require stable evidence, documented support, discoverability, version policy, and upgrade tooling. Mark the supported matrix visibly. General availability should mean “the owner will maintain this contract,” not “works everywhere.”

### 5. Deprecation and retirement

Deprecate when native model or tool capability removes the benefit, the underlying workflow disappears, risk exceeds value, compatibility fragments, support ends, or a replacement has better evidence. Publish dates, migration guidance, pinned fallback, and exception handling. Retire credentials and catalog discovery as well as files.

## Make discovery evidence-aware

Catalog search should return the smallest relevant set using task, repository, risk, and required capability. Show:

- why the skill matched;
- owner and maturity;
- last evaluation date;
- supported model/tool matrix;
- permissions and side effects;
- alternatives and deprecation notice.

Do not preload every skill schema or description. Context cost and ambiguous selection grow with the catalog. Track false selection, missed selection, and users bypassing discovery. Allow a human to choose no skill.

A skill may be discoverable but not invocable because the current identity lacks authority. Keep discovery, authorization, and execution separate. Natural-language relevance never grants credentials.

## Govern versions and forks

Use immutable releases and semantic meaning that fits the contract:

- patch: clarification or compatible repair;
- minor: new optional capability or supported target;
- major: changed behavior, permissions, outputs, or migration requirements.

Pin production workflows. Test upgrades against real adopter scenarios before changing the default. Record which version produced each consequential artifact.

Forks are signals. A domain-specific fork may be correct; a dozen near-identical forks may reveal a missing extension point. Require fork provenance, owner, divergence reason, upstream relationship, and review date. Do not force unsafe convergence merely to reduce counts.

Create a small governance forum for shared or high-risk skills. It approves major releases, privilege changes, and retirement disputes. Routine domain content remains with its owner. Publish decision records so “platform policy” is inspectable.

## Measure value and burden

Track per skill:

- successful independently accepted tasks;
- unique failure classes prevented or resolved;
- regressions, incidents, and unsafe attempted actions;
- false refusals and escalation quality;
- tokens, calls, latency, and human time;
- adoption, repeat use, abandonment, and support tickets;
- compatibility failures by model and tool version;
- forks and unresolved divergence;
- time to repair a broken release;
- age since last meaningful evaluation;
- performance against the no-skill condition.

Do not optimize installs or invocations. A mandatory skill can have 100% adoption and negative value. Sample users and nonusers, and preserve change mix when comparing them.

The [code-as-harness survey](https://arxiv.org/html/2605.18747v1) frames executable interfaces as persistent and inspectable while acknowledging stale context, permission conflicts, oracle weakness, mutation overfit, and safety. It is a narrative systems survey, not governance evidence. Its boundary is useful: inspectability helps only if someone maintains the inspected contract.

## Pruning review

At each review date, run four questions:

1. Does the failure or need still exist?
2. Does the skill still outperform the simpler workflow?
3. Does it remain safe and compatible on current models and tools?
4. Is its total benefit greater than catalog, context, support, and exception cost?

Possible decisions are renew, narrow, split, merge, deprecate, or retire. “No recent incident” is insufficient if nobody uses the skill. “Many users” is insufficient if native capability now performs as well.

[Lilian Weng’s harness synthesis](https://lilianweng.github.io/posts/2026-07-04-harness/) highlights evaluator ambiguity, memory lifecycle, reward hacking, diversity loss, and short-horizon optimization. It is a conceptual literature essay whose quantitative examples require primary-source verification. Use it to design falsifiers, not to claim that shared skills self-improve.

The practitioner countercase [*Stop Overengineering Your Agent Harness*](https://www.oreilly.com/radar/stop-overengineering-your-agent-harness/) argues that harness features should address observed failures and can expire as models improve. It supplies no retirement cadence. This playbook operationalizes the testable part: maintain a no-skill comparator and require renewal evidence.

## Stop conditions and rollback

Freeze distribution when provenance is missing, permissions exceed the declared contract, a severe regression appears, the supported matrix is false, or no accountable owner responds. Suspend automatic upgrades when adopter outcomes diverge materially.

Rollback by repointing invocations to the pinned prior version or disabling discovery, revoking changed credentials, restoring the previous workflow, and retaining evidence. Notify known adopters with the affected versions and safe alternative. For a harmful skill, remove invocation authority immediately; preserving an archive for forensics does not mean leaving it callable.

## What survives skeptical review

Shared skills create a plausible economy of reusable know-how, but the corpus contains no comparison of central, federated, and product ownership; no validated compatibility standard; and no evidence-based retirement interval. Model improvement can make a skill obsolete, while domain complexity can make it more valuable.

The durable practice is explicit lifecycle governance: narrow contracts, named owners, matched with/without evaluation, supported matrices, evidence-aware discovery, immutable versions, controlled forks, expiry, and reversible retirement. A healthy catalog is not the largest one. It is the one whose remaining entries can still justify their existence.

Podcast hook: The organization’s most popular agent skill works on yesterday’s model, fails on today’s tool, and has three owners who all thought someone else would retire it.

Continue reading: [Chapter 43, “Replace broad infrastructure tools”](43-narrow-infrastructure-tools.md), applies the same narrow-contract discipline to high-consequence cloud operations.
