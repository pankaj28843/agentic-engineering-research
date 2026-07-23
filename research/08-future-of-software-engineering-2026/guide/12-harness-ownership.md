# 12. Who owns the harness?

> **Report point:** Harness engineering, bullet 12, page 5 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** Harnesses need explicit shared stewardship and product accountability; no audited study establishes one universally superior ownership model.

A shared agent harness can quickly become infrastructure. It assembles context, exposes tools, grants permissions, records traces, runs evaluators, and teaches agents local conventions. If every product team builds its own, the organization duplicates risk and effort. If a central group owns everything, it may recreate the detached operations silo that platform engineering was meant to avoid.

The retreat report favors a platform-shaped answer. The evidence audit supports the need for ownership but not a single org chart. The selected sources identify maintenance, versioning, model specificity, stale instructions, weak evaluators, safety boundaries, and pruning as real concerns. None compares centralized, federated, enabling-team, and product-owned harnesses on common outcomes.

The responsible conclusion is a design principle: **centralize reusable mechanisms and guardrails; keep intent, acceptance, and operational consequences with the teams whose systems are changed.**

## A plain-language model: mechanism, policy, and use

“The harness” sounds like one product, but it contains at least three ownership domains.

**Mechanism** is how the system works: tool protocols, context assembly, trace storage, sandboxing, authentication, evaluation runners, version distribution, and rollback. These components often benefit from specialist engineering and shared investment.

**Policy** defines what the mechanism permits: data boundaries, risk tiers, approval requirements, retention, model eligibility, and organization-wide prohibited actions. Security, legal, architecture, and platform stakeholders may share authority here.

**Use** is the situated work: repository instructions, domain vocabulary, task acceptance criteria, local tools, exceptions, and responsibility for what reaches production. Product teams hold the knowledge and consequences.

Confusing these domains produces two familiar failures. A central platform may encode generic rules that are safe but useless, then become a ticket queue for every local change. Or product teams may copy a powerful harness without maintaining its security controls, evidence, or upgrade path.

Ownership is therefore a set of decision rights, not a directory name.

## What the source base supports

The [Fowler/Böckeler account of harness engineering](https://martinfowler.com/articles/harness-engineering.html) describes a steering loop with feed-forward context and feedback sensors. It explicitly raises construction and maintenance work, conflicting instructions, legacy-system difficulty, contribution, and versioning. The article is a practitioner synthesis without a comparative study, but it establishes the scope of the stewardship problem: a harness is not a prompt file that can be “owned” once and forgotten.

[*Self-Harness*](https://arxiv.org/html/2606.09498v1) adds empirical evidence that useful harness changes can be model-specific. Three model families improved differently on a filtered Terminal-Bench task set after validation-gated changes. The result does not determine an organization design, but it warns against assuming one universal configuration. Someone must know which model, repository, evaluator, and evidence a rule targets.

[The Verification Horizon](https://arxiv.org/html/2606.26300v1) shows why evaluator ownership is consequential. Model and prompt choices changed rankings and agreement; some long-horizon evaluator outputs could not be parsed; proxy optimization required continued verifier evolution. A team that owns only the generation layer cannot outsource truth to a platform score without understanding its validity.

The [code-as-harness survey](https://arxiv.org/html/2605.18747v1) treats executable interfaces as inspectable coordination and state, while acknowledging permission, stale-context, authority, oracle, mutation, and safety limits. This supports narrow interfaces and explicit controls as architecture concerns. It does not show that a central team operates them better.

Finally, [Lilian Weng’s synthesis](https://lilianweng.github.io/posts/2026-07-04-harness/) identifies evaluator ambiguity, memory lifecycle, reward hacking, diversity collapse, and short-horizon optimization. These risks cross team boundaries, but their manifestations are local. Shared expertise helps; local observation remains indispensable.

The evidence thus establishes the **work of ownership**, not its ideal allocation.

## Compare four models without pretending one won

In a **central platform model**, one team publishes the harness, tools, and policies. This can improve consistency, security review, observability, and upgrade leverage. It can also create slow queues, generic abstractions, and incentives to maximize adoption rather than outcomes.

In an **enabling-team model**, specialists temporarily help product teams build capability and then reduce dependence. This can transfer knowledge and reveal local constraints. It may struggle to maintain durable shared infrastructure or serve many teams simultaneously.

In a **federated model**, a small core owns protocols and guardrails while product representatives own domain packages and participate in governance. This aligns reuse with local knowledge, but decision latency, incompatible variants, and diffuse accountability can grow.

In a **product-owned model**, each team controls its complete harness. Feedback is fast and responsibility is clear. Duplication, inconsistent safety, inaccessible traces, and upgrade fragmentation are the obvious costs.

These are archetypes. A real organization can assign mechanisms centrally, policies jointly, and local use to products. That hybrid is often attractive, but it is still a hypothesis that must be judged against local flow, risk, and capability.

## Apply the dependency rule

Domain-driven design offers a useful structural test. High-level domain intent should not depend on the private details of a vendor model or browser session. Product-specific acceptance should call stable capabilities—“validate this payment contract,” “open this approved rendered page,” “check this migration invariant”—rather than reaching into generic automation internals.

Conversely, the platform should not contain every team’s domain decisions. It can provide a schema for a narrow tool, enforce permissions, record provenance, and expose versioning. The product-owned adapter supplies the domain semantics. This creates a deep module: a small, stable interface hides complicated extraction, browser, model, or evaluator behavior.

The boundary makes change safer. A platform can improve an arXiv extractor or trace store without rewriting research workflows. A product team can strengthen a payment invariant without forking the harness runtime. Ownership follows the abstraction: the group with the knowledge and ability to verify a decision owns that layer.

## An ownership matrix

Use a decision-rights matrix before arguing about team topology:

| Asset or decision | Accountable owner | Required contributors | Promotion evidence |
|---|---|---|---|
| Tool protocol and runtime | Platform/core | Product integrators, security | Compatibility, isolation, rollback |
| Credentials and permissions | Security/platform | Product data owner | Least privilege, audit, abuse tests |
| Shared evaluator framework | Verification/core | Domain experts | Calibration, hidden faults, cost |
| Organization policy | Named governance body | Legal, security, engineering | Risk rationale, exception process |
| Repository instructions | Product team | Platform adviser | Local task outcomes, regression test |
| Domain acceptance criteria | Product owner/engineers | Operators, users, risk owner | Executable examples and expert review |
| Memory or skill package | Named maintainer | Users across adopting teams | Version, provenance, expiry date |
| Production release | Owning service team | Required approvers by risk | System-specific acceptance and rollback |

Every row needs a named human role or team, even when an agent proposes changes. “The community owns it” and “the platform owns it” are not enough unless contribution, adjudication, incident response, and retirement rights are explicit.

## Exercise: trace one shared rule

Choose a harness rule used by at least two teams. Reconstruct:

1. who first proposed it and from which failure;
2. which repositories, models, and tool versions it was tested against;
3. who can change, approve, override, and retire it;
4. which team is paged if it causes a production failure;
5. what evidence would show that it has become stale;
6. whether a local team can inspect and safely escape it.

If any answer is “nobody” or “everyone,” assign a temporary accountable owner and an expiry date. If the rule contains domain intent, move that portion toward the product. If it implements a reusable mechanism, hide it behind a stable interface. If it is a risk control, make bypass visible and governed rather than impossible to discuss.

Track two kinds of service-level objective. The platform needs reliability and response measures: tool availability, upgrade success, incident recovery, and request latency. Product teams need outcome measures: accepted changes, false refusals, escaped faults, rework, and local maintenance. A platform can meet its uptime target while making delivery worse; a product can ship quickly while externalizing security risk. Both views are required.

[Chapter 42](42-govern-prune-shared-skills.md) owns the contribution, versioning, pruning, and retirement lifecycle. This chapter owns the prior boundary: no lifecycle works if decision rights and consequences are detached.

## What would raise confidence

A useful comparative study would follow multiple organizations or internal teams using different ownership allocations. It would measure harness change lead time, reuse, duplicated effort, security exceptions, evaluator validity, incident response, model-upgrade cost, product outcomes, and team autonomy over a meaningful period. Team selection and system risk would need careful adjustment; a platform is often introduced where complexity is already high.

Qualitative evidence would also matter. Which knowledge gets lost at handoffs? Can product engineers explain platform decisions? Can platform engineers observe local failures? Does contribution produce real shared stewardship or merely a central backlog? No selected source answers these questions comparatively.

## What survives skeptical review

Harness infrastructure requires explicit stewardship because its instructions, tools, evaluators, permissions, state, and model assumptions change. Shared investment is justified for reusable mechanisms and organization-wide controls. Product teams must retain ownership of domain intent, acceptance, and operational consequences.

That is an architectural boundary, not proof that a platform team is always best. Choose and revise the ownership model using visible decision rights, evidence, flow, and incidents. A harness that everyone uses but nobody can safely change is not a platform; it is an inherited dependency.

Podcast hook: When a shared agent rule breaks one product to help another, who gets to decide whether it learned or regressed?

Continue reading: [Chapter 42: Govern and prune shared skills](42-govern-prune-shared-skills.md) turns the ownership matrix into a contribution and retirement process.
