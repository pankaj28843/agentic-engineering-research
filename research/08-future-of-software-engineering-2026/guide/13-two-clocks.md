# 13. The two clocks of agentic delivery

> **Report point:** Team design, bullet 13, page 5 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** The mechanism is plausible; the system-level effect remains unmeasured.

An agent can produce a plausible patch in minutes while a team still needs days to decide what the patch should mean, discover who must approve it, and establish that it is safe. That contrast motivates a useful hypothesis: agentic delivery runs on two clocks.

The first is the **candidate clock**. It measures how quickly code, tests, documentation, and alternative designs can be proposed. The second is the **commitment clock**. It covers the work required to turn a candidate into an accountable change: clarifying intent, choosing among tradeoffs, validating behavior, integrating with other work, and accepting operational consequences.

This is a model, not a law. Faster candidate production need not make decision latency the bottleneck in every team. The important result of the evidence audit is more modest: generation can relocate effort, and teams need to observe where it went.

## A plain-language model: proposals are not deliveries

Imagine a restaurant kitchen. Buying a machine that can prepare ten possible dishes per minute does not guarantee that ten meals leave the pass. Someone still has to know what was ordered, check allergies, choose the right plate, inspect the result, and coordinate service. If those activities have spare capacity, the machine helps. If they do not, the kitchen accumulates options and rework.

Agentic delivery has the same shape. Candidate output is an arrival stream. Review, specification, integration, and acceptance are constrained services. End-to-end delivery improves only when the whole path can absorb the new arrival rate. Otherwise the visible symptom may be a growing review queue, repeated prompt-and-reject cycles, more context switching, or code that is merged quickly but repaired later.

The two clocks therefore should not be read as “coding no longer matters.” Implementation can remain the constraint when work is novel, tools are unreliable, verification is weak, or changes require difficult debugging. Nor does the model imply that every decision deserves a meeting. A clear, reversible, well-tested change may move through both clocks quickly. The model asks a diagnostic question: **which activity currently limits trusted completion?**

## What the audited evidence actually shows

The strongest empirical anchor is indirect. In a 12-week software-engineering course, [Salomon and colleagues](https://www.cs.ubc.ca/~rtholmes/papers/splash_2025_salomon.pdf) studied 364 third-year students working in pairs; 341 survey responses were valid, and 84% reported using generative AI. Interviews described some students moving earlier into implementation, using AI as a first contact, and validating output retrospectively. This is evidence that workflow order and help-seeking can change. It is not evidence that specification became the universal bottleneck: there was no non-AI cohort, production delivery measure, review-queue telemetry, or objective code-quality outcome.

Industry accounts make the proposed mechanism vivid but do not close that gap. A [Stack Overflow article about decision fatigue](https://stackoverflow.blog/2026/05/21/coding-agents-are-giving-everyone-decision-fatigue/) recounts an engineer generating roughly seven times as much code and needing six reviewers. The article does not provide the underlying queue data, comparison condition, survey instrument, or system boundary. It can support the question “where did the work move?” but not a sevenfold productivity claim or a general queueing result.

A separate [practitioner report about adding AI agents](https://towardsdatascience.com/why-adding-more-ai-agents-made-our-system-slower/) supplies a useful technical counterexample. In the described system, one request could fan out to about 30 downstream calls while a 100-connection limit and event-loop/JSON work constrained throughput. The accompanying simulation was deliberately tuned to expose that mechanism. This shows that concurrency can move a bottleneck to shared resources. It does not show that additional agents generally slow software teams; the system, workload, and human decision process are different.

The retreat witness trail is consistent with a shifted-constraint hypothesis. [Annie Vella](https://annievella.com/posts/finding-comfort-in-the-uncertainty/) describes movement toward a supervisory middle loop, while [Giles Edwards-Alexander](https://overwatering.org/blog/2026/07/notes-from-fose-europe/) contrasts organizations optimized for output with organizations built to learn. These are firsthand interpretations from the same retreat network, not independent outcome studies. Their convergence establishes salience, not prevalence.

The overall evidence class is therefore mixed:

- one bounded classroom study observes changed workflow and collaboration;
- practitioner stories identify plausible review and resource bottlenecks;
- retreat accounts propose an organizational interpretation;
- no selected source jointly measures generation, decision time, validation, rework, defects, and end-to-end delivery in production.

That missing joint measurement matters. Without it, ordinary waiting can be relabeled as a novel “agentic bottleneck,” and local frustration can be mistaken for a general law.

The unit of analysis also changes the story. A developer can finish their part sooner while the change waits longer for another specialty. A team can merge more patches while a product outcome takes longer because it chose the wrong work. An organization can shorten delivery while increasing operational recovery later. A two-clock claim should state whether it concerns an individual task, a team change, a product outcome, or a full service lifecycle; otherwise speed at one level can conceal delay at another.

## Counterexamples that should change the conclusion

There are at least four cases in which the candidate clock may still dominate.

First, an agent may simply be bad at the task. Unfamiliar languages, weak context, subtle concurrency failures, or novel algorithms can make usable generation slow. Second, a team may have unusually strong acceptance machinery: narrow changes, deterministic tests, clear ownership, and reversible deployment can let review keep pace. Third, parallel candidates can be valuable when they explore genuinely different options and the cost of comparison is small. Fourth, a temporary queue may be rational if it buys information before an irreversible choice.

Conversely, a fast merge is not proof that the commitment clock is healthy. Deferred integration bugs, unread changes, and later incident work can hide decision and validation time outside the measured lead time. Any local test must therefore include downstream rework and defects, not just time to merge.

The skeptical conclusion is conditional: **faster implementation exposes another constraint only when candidate production exceeds the team’s capacity to make and validate commitments.** Whether that condition holds is an empirical question for each work system.

## What would raise confidence

A stronger study would follow a varied set of production changes from accepted intent through operation. It would timestamp candidate creation, clarification, review, automated validation, integration, rejection, and recovery; identify whether those activities happened serially or in parallel; and preserve task type, team size, model, tool, and codebase familiarity. It would count accepted changes rather than generated lines and include defects and rework after merge.

The decisive comparison is not “agent users versus non-users” in the abstract. It is whether a defined increase in candidate capacity shortens trusted end-to-end delivery, leaves it unchanged, or moves delay elsewhere. Reviewers’ workload and context switching matter alongside elapsed time: a queue that stays short because six people interrupt other work is not free capacity. Repeated observations before and after a workflow change would still face confounding, but they would be much stronger than a memorable fast patch or a leadership impression.

## Exercise: a one-change clock trace

Choose one ordinary change—not a showcase—and reconstruct its path in a 30-minute team session. This is a diagnostic exercise, not a performance scorecard.

1. Mark when the intent became clear enough to act.
2. Mark when the first plausible candidate appeared.
3. List every wait, rejection, clarification, review, integration step, and later repair.
4. For each interval, ask whether more generation capacity would have shortened it.
5. Name one counterfactual: a case in which implementation would still have been the constraint.
6. Record missing data rather than estimating it from memory.

The output is a hypothesis such as “acceptance criteria, not code generation, dominated this change” or “the agent’s repeated incorrect attempts still dominated.” Do not turn a single trace into a universal rule. Repeat across different task types before changing staffing or process. [Chapter 44](44-instrument-two-clocks.md) owns the fuller instrumentation and operational decision method.

## What survives skeptical review

The two-clock idea is valuable as a falsifiable map. It helps a team distinguish producing options from accepting consequences and prevents candidate volume from masquerading as delivery. The evidence does not yet establish a population effect, a stable ratio between the clocks, or a threshold at which review becomes overwhelmed.

Treat “decision latency is the new bottleneck” as a claim to test, not a diagnosis to announce. A credible result will include cases where the claim fails.

Podcast hook: What happens when a five-minute patch creates a five-day decision—and how would a team know which clock it actually improved?

Continue reading: [Chapter 44: Instrument the two clocks](44-instrument-two-clocks.md) turns this bounded hypothesis into an operational measurement practice.
