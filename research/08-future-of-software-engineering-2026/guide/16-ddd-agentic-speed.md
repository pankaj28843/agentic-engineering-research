# 16. Domain-driven design at agentic speed

> **Report point:** Team design, bullet 16, page 6 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** DDD offers relevant design vocabulary; comparative effectiveness for agentic work is unknown.

When code becomes cheaper to produce, a wrong boundary becomes cheaper to reproduce too. An agent can rapidly spread an ambiguous term, couple two domains, or implement a local assumption in dozens of places. Domain-driven design (DDD) looks attractive because it focuses attention on language, models, and boundaries rather than the volume of code.

That is a plausible fit, not a proven one. The audited corpus contains design principles, participant experiments, and conceptual arguments. It contains no multi-codebase comparison showing that DDD makes agent output more correct, maintainable, navigable, or collectively owned.

## A plain-language model: map, borders, and traffic rules

Think of a software system as a map.

The **map labels** are the terms people use: customer, account, policy, order, entitlement. A ubiquitous language tries to make those labels mean the same thing in conversation, specifications, code, and tests within a domain. The **borders** are bounded contexts: places where a model is internally coherent and where translation is explicit. The **traffic rules** are interfaces and invariants that govern what may cross.

An agent benefits from a legible map because its task context can be narrower and contradictions easier to detect. A human benefits because a proposed change can be discussed in business terms and traced to an accountable boundary. But a beautifully named border can still be wrong. DDD does not discover the domain automatically, and an agent repeating the vocabulary does not demonstrate understanding.

“Agentic speed” adds a feedback concern. Cheap implementation allows more boundary experiments and cheaper reversal, which could reduce the cost of being wrong. It also allows an error to propagate faster. The valuable property is therefore not fixed architecture; it is **inspectable and reversible boundary learning**.

## What the audited sources contribute

The most direct admissible source is [Maintainable Software’s agentic codebase principles](https://maintainable.software/agentic-engineering-part-2-agentic-codebase-principles/). It proposes locality, small blast radius, boundary integrity, navigability, and bounded rebuild/test scope, using domain modules or vertical slices as possible structures. These are concrete properties that can be inspected in a repository. The source is an independent practitioner synthesis, not a comparative study, and it supplies no task set, agent baseline, maintenance horizon, or ownership outcome.

The retreat’s DDD trail is richer conceptually but weaker empirically. [Mathias Verraes](https://verraes.net/2026/07/software-design-in-the-agentic-age/) presents bounded contexts, ubiquitous language, domain models, specifications, deterministic refactoring, and reversibility explicitly as design “bets.” He reports arguments and experiments but provides no shared artifact, comparator, long-run evolution measure, or outcome data. That candour is useful: the source owns a hypothesis rather than disguising it as a result.

[Giles Edwards-Alexander’s retreat notes](https://overwatering.org/blog/2026/07/notes-from-fose-europe/) record recurring domain-model discussion and ask why DDD should work now. [Jimmy Nilsson’s short reflection](https://www.linkedin.com/posts/jimmynilsson_twsoftwaredev26-activity-7478347334784016385-ijb8/) places DDD alongside XP, TDD, BDD, and continuous delivery as enduring fundamentals. [Andrew Harmel-Law](https://www.linkedin.com/pulse/software-engineering-having-raft-moment-andrew-harmel-law-f6mle/) warns that practices often carry reasoning and shared-understanding functions that may be lost when the visible activity changes.

These authors attended overlapping retreat events and share professional networks. Their convergence shows that experienced practitioners found the vocabulary promising; it is not independent replication. Consultancy and design-practice incentives are relevant context.

No selected source isolates DDD from simpler modularity, smaller files, vertical slices, explicit interfaces, architecture decision records, dependency rules, or better tests. A reported improvement after modularization cannot be attributed to DDD if context size, naming, test scope, and dependency structure changed together.

## The strongest hypothesis

DDD may help agentic work through four mechanisms:

1. **Context locality:** a task can bring a coherent slice of model, rules, and examples rather than a whole repository.
2. **Semantic checks:** domain terms and invariants give reviewers something stronger than stylistic consistency to challenge.
3. **Ownership alignment:** a boundary can identify who has authority to accept changes and who bears operational consequences.
4. **Reversibility:** explicit translations and contained dependencies can make a mistaken model cheaper to replace.

Each mechanism can be tested without claiming that the entire DDD repertoire is necessary. A small service with stable concepts may need only clear modules and tests. A complex product with contested language may benefit from event storming, bounded contexts, and explicit translation. The intervention should match the uncertainty.

Agent speed also creates a counterargument: if refactoring and regeneration are cheap, perhaps teams need less up-front boundary design. That can be true when behavior is well specified, coupling is observable, and reversal is safe. It is less convincing where domain errors create legal, financial, safety, or data consequences. Cheap code does not make stakeholder disagreement cheap.

DDD itself can become a cost. Workshops can delay feedback; elaborate aggregates can obscure a simple workflow; ubiquitous language can freeze one group’s interpretation; and context boundaries can mirror the org chart rather than the domain. An agent may amplify that ceremony as readily as it amplifies useful structure.

## What a meaningful comparison would require

Evidence for DDD at agentic speed should compare explicit interventions, not repositories casually labeled “DDD” and “non-DDD.” The same change could be attempted against a baseline structure and against a structure with a defined locality or boundary improvement. Researchers would need to hold the model, prompt strategy, tool permissions, tests, and task stable, then record context gathered, cross-boundary edits, invalid assumptions, review time, defects, and rework.

The maintenance horizon matters more than a single generated patch. A useful study would introduce later requirement changes and operational failures to see whether people and agents can locate the relevant model, predict impact, and reverse a bad decision. Team outcomes would include who can explain and approve the change, not merely token count or compilation success. Multiple domains are necessary because a clear accounting boundary and a contested healthcare concept present different semantic difficulty.

Even that comparison would test selected DDD mechanisms, not the philosophy as a whole. The goal is to learn whether locality, language, and explicit translation add value over simpler rivals—and at what coordination cost.

Evidence should include failure cases selected before the trial. An intervention that helps an agent add a feature may still hinder a cross-context change, a schema migration, or an incident investigation. Reviewers should record where the domain language clarified disagreement and where it merely renamed it. Without those negative cases, a team can attribute any successful patch to DDD and every failure to incomplete adoption, making the hypothesis impossible to falsify.

## Exercise: a boundary falsification card

Choose one proposed or existing boundary and complete this card with a domain expert and an engineer:

- **Claim:** What concept or rule is coherent inside this boundary?
- **Contradiction:** What realistic example would show that the model is wrong?
- **Leak:** Which decision currently requires knowledge from outside the boundary?
- **Translation:** Which term changes meaning as it crosses the border?
- **Evidence:** Which test, production signal, or stakeholder decision would reveal the mistake?
- **Reversal:** What would have to change if the boundary moved tomorrow?
- **Simpler rival:** Could a module, interface, or dependency rule deliver the same benefit with less conceptual machinery?

Ask an agent to implement or explain one bounded change, then inspect context gathered, cross-boundary edits, rejected assumptions, test scope, and human review effort. Do not infer maintainability from a successful first patch. Revisit after a later change, when boundary quality becomes more visible.

This is a local falsification exercise, not evidence that DDD outperforms alternatives.

## What survives skeptical review

DDD contributes a disciplined language for discussing rapidly generated code: models, context, translation, invariants, and ownership. The case is strongest where business meaning is contested and wrong assumptions are consequential. The same desired properties may sometimes be achieved through simpler modular design.

The defensible conclusion is that DDD is an agentic design hypothesis with inspectable mechanisms—not a newly proven best practice. Use agents to make boundary experiments cheaper, and use human domain judgment to decide what those experiments mean.

Success should be claimed only when later changes remain understandable, contained, and reversible—not merely when the first generated implementation compiles.

Podcast hook: If an agent can refactor a system overnight, does that make domain boundaries less important—or merely let a bad boundary spread before breakfast?

Continue reading: [Chapter 45: Preserve spec-pairing](45-preserve-spec-pairing.md) examines how teams can keep shared reasoning around the model while implementation accelerates.
