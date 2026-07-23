# 14. Superpowered silos versus spec-pairing teams

> **Report point:** Team design, bullet 14, page 6 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** AI use changes interaction patterns; effects on ownership, inclusion, and team outcomes remain open.

An individual engineer with an agent can appear spectacularly productive. That person may explore, implement, and test a change without waiting for a colleague. Yet local speed can coexist with a weaker team: fewer shared explanations, more private context, concentrated decision authority, and code that only its producer can confidently change.

The alternative proposed at the retreat was not necessarily to pair on every keystroke. It was to pair on the **specification and reasoning** while letting agents perform more implementation. That proposal is plausible, but the evidence does not show that “spec-pairing” reliably prevents silos. The honest conclusion is that AI changes where collaboration happens, so teams must inspect whether the functions once carried by pairing still occur.

## A plain-language model: output, reasoning, and ownership

Team coherence has at least three surfaces.

The **output surface** is what gets produced: patches, tests, diagrams, and documents. The **reasoning surface** contains the intent, constraints, rejected options, and uncertainties behind those artifacts. The **ownership surface** answers who can explain, challenge, operate, and safely modify the result later.

Agent tools can expand the output surface while shrinking the other two. A private conversation between one engineer and an agent may contain substantial reasoning, but it is not automatically legible to the team. Sharing the final patch does not transmit the decision process. Conversely, a team can preserve shared reasoning without preserving an old ceremony exactly. A design conversation, written decision record, joint acceptance example, or rotating reviewer might carry the same function.

That distinction matters because “pairing” is a visible practice, while explanation, challenge, and distributed authority are its possible mechanisms. Preserving the label without those mechanisms would protect a ceremony, not team coherence.

## What changed in observed work

Several bounded studies show that the choice of interlocutor changes.

In 13 interviews with generative-AI users across heterogeneous software-related roles, [Barke and colleagues](https://arxiv.org/html/2405.01543v1) found reports of AI as a rubber duck, iterative correction, collaborative prompt refinement, and less reliance on human pairing in some situations. Recruitment selected people already using the tools, and the study measured no team performance, retained knowledge, or ownership. It supports redistribution of conversation, not a causal silo effect.

A richer workplace case observed two established teams at Sparebank1 Utvikling. The [HICSS study](https://scholarspace.manoa.hawaii.edu/bitstreams/4f29b0c8-06ac-4d5d-9fa0-52eb93321eb2/download) covered 28 people, including 15 developers, and 49 programming sessions across 25 observation days. AI appeared in all 16 solo sessions, 29 of 31 physical-pair sessions, and one of two remote-pair sessions. Pair work involved less direct AI interaction; humans tended to handle domain questions while AI handled more technical ones, and participants sometimes verified or rejected AI suggestions.

That is useful observational evidence about task allocation. It does not show that pairing preserved learning or system ownership. Pairing already existed, sessions were not randomly assigned, task mixes differed, and there was no objective learning, quality, or delivery outcome. A small self-estimated time-saving result lacked a reported denominator and should not carry the argument.

Classroom evidence points in a similar but equally bounded direction. In a 12-week course with 364 students working in pairs, [Salomon and colleagues](https://www.cs.ubc.ca/~rtholmes/papers/splash_2025_salomon.pdf) recorded AI-first help seeking and reduced peer communication in some interviews alongside high perceived usefulness. There was no non-AI cohort and no objective collaboration outcome. Positive experience and reduced peer contact can coexist; neither tells us whether the team learned.

Finally, a controlled laboratory study assigned 19 advanced computer-science students to six human–human sessions or seven human–AI sessions. The [study of “knowledge-transfer episodes”](https://www.se.cs.uni-saarland.de/publications/docs/WSD+.pdf) annotated 210 episodes in human pairs and 126 in human–AI work—about 35 versus 18 per session. But an episode meant a perceived knowledge gap and an attempt to address it. It was not a test of knowledge gained, remembered, or transferred. Conditions also differed: human pairs conversed naturally, while AI participants thought aloud, and prior AI experience was unbalanced.

Together, these studies justify saying that human–human and human–AI work exhibit different conversational patterns. They do not justify saying that human pairs transfer twice as much knowledge, that agent use destroys collective ownership, or that spec-pairing fixes either problem.

## The credible mechanism—and its alternatives

Spec-pairing could help because it makes intent contestable before implementation becomes cheap and plentiful. Two people can expose ambiguous terms, surface domain knowledge, and negotiate acceptance criteria. If the implementation then arrives quickly, both retain a route back to the decision.

But other mechanisms might perform the same job. A team could rotate the person who frames the problem, require a short explanation from someone other than the author, review executable examples together, or make rejected alternatives visible. Conventional pairing itself is not flawless: the laboratory study observed more side discussion and occasions when human pairs lost track. It can exclude people through scheduling, dominance, language, accessibility, or time-zone constraints. A new asynchronous practice may sometimes distribute understanding better.

There is also a counterexample to the silo story: an agent can expand access to explanation. It can help someone prepare questions before a team discussion or offer low-stakes rehearsal. The [13-interview study](https://arxiv.org/html/2405.01543v1) includes accounts of AI acting as a rubber duck and enabling iterative correction. Those adoption-selected self-reports establish neither benefit nor prevalence, but they complicate the assumption that an AI interlocutor must isolate its user.

The question is therefore functional: after the tool changes, who can explain the decision, who had a meaningful chance to challenge it, and who can act when the original author is absent?

## Do not collapse the outcomes

A defensible local comparison keeps at least four outcomes separate. **Contact** asks whether colleagues interacted. **Explanation** asks whether reasons and uncertainty became visible. **Learning** requires an assessment of what someone can later understand or do. **Ownership** asks whether authority and operational capacity are distributed beyond the original producer. More messages can increase contact without improving any of the others; a quiet written review can sometimes transfer more reasoning than a long call.

The relevant cost also includes coordination time, interruptions, accessibility, and delayed rework. A pairing intervention that spreads understanding but makes participation impossible across time zones is not an uncomplicated success. A solo-agent workflow that ships quickly but leaves one person permanently on call is not either. Measuring each construct prevents “team coherence” from becoming an attractive label attached to whichever practice leaders already prefer.

A longitudinal test should sample these outcomes after the author rotates away or an incident occurs. That is when apparent shared ownership becomes observable rather than aspirational.

## Exercise: sample the shared reasoning, not the ceremony

Select one recently completed change and invite three people: its author, someone who reviewed it, and someone likely to operate or modify it. Give each person five quiet minutes to write:

- the user or system outcome the change was meant to produce;
- the most important constraint and rejected alternative;
- the evidence that made the change acceptable;
- the first action to take if it fails.

Compare the answers without scoring individuals. Large differences are a signal to investigate the work system, not proof that someone is deficient. Then identify which activity—pair conversation, issue text, agent transcript, decision note, review, or operational handoff—actually carried shared understanding. Preserve or redesign that function in one subsequent change and sample again.

This exercise does not establish learning or ownership. It makes those claims testable and can reveal whether a supposedly collaborative ritual leaves knowledge concentrated. [Chapter 45](45-preserve-spec-pairing.md) owns the fuller practice design, including roles, inclusion, and measures.

## What survives skeptical review

AI use can alter who asks whom, when peers speak, and whether domain and technical questions go to different partners. That claim has bounded qualitative and observational support. The downstream effects on inclusion, durable learning, code quality, and collective ownership have not been established.

“Superpowered silo” is a risk pattern, not a diagnosis of every highly productive individual. “Spec-pairing” is a candidate response, not a proven cure. Preserve the social functions—explanation, challenge, shared decisions, and recoverable ownership—and test which practice carries them in your context.

Podcast hook: If the team sees only the patch while one engineer and an agent saw the reasoning, who really owns the change?

Continue reading: [Chapter 45: Preserve spec-pairing](45-preserve-spec-pairing.md) develops the practice while keeping learning and ownership as outcomes to measure.
