# 35. Keeping human judgment in the loop

> **Report point:** Conspicuously human, bullet 35, page 10 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** Meaningful judgment can be operationalized; no universal human-in-the-loop advantage or optimal task allocation has been established.

A person clicking “approve” is not the same as human judgment. They may lack relevant expertise, receive an opaque recommendation, have seconds to respond, and face pressure never to stop the system. The interface contains a human; the decision does not.

As implementation becomes highly automated, the governing question is not which lines of code a person must type. It is which **decisions** need accountable human authority, what that authority requires, and whether automation sometimes produces a better result than a ceremonial review.

## A plain-language model: seven conditions for judgment

Human judgment is meaningful only when seven conditions are visible:

1. **Decision:** the choice reserved for a person is named precisely.
2. **Owner:** someone has legitimate authority and accepts responsibility for it.
3. **Expertise:** the owner can interpret the domain, evidence, and likely failure modes.
4. **Information and time:** they receive enough context and attention to reason rather than rubber-stamp.
5. **Power:** they can stop, override, request more evidence, or choose a different path.
6. **Recourse:** affected people can contest the decision and exceptions have an appeal route.
7. **Learning:** failures and disagreements change future policy, tools, or allocation.

This model turns “keep a human in the loop” into an auditable organizational claim. If any condition is absent, the loop may provide reassurance, labor, or liability transfer without judgment.

## Human presence can make a system worse

Two controlled experiments reported in [ACM Queue](https://queue.acm.org/detail.cfm?id=3363293) directly challenge the assumption that a hybrid must be safer. In the first, 225 US Mechanical Turk participants—75 per condition—judged 40 filtered Broward County profiles. Accuracy was 54.2% with profiles alone, 51.0% with profiles plus a COMPAS score, and 53.5% with the score plus a warning; neither comparison reported here was statistically significant. COMPAS alone scored 65.0%.

The second experiment shifted displayed COMPAS scores by plus or minus three. Mean human ratings moved from 3.88 to 5.96, a 42.3% difference (`p < .0001`), demonstrating anchoring. The captured article did not state that experiment’s sample size. Participants were novices making repeated, low-stakes simulated judgments, not experts shipping software, and the second result measured anchoring rather than accuracy or fairness.

Even with those limits, the finding is important: showing a person a machine output can pull the person toward it, and a warning does not guarantee independent evaluation. Human review must be compared with strong AI-only and human-only baselines on the same task. It cannot be presumed beneficial.

## “Centaur” describes a pattern, not a performance result

The [Cyborgs, Centaurs and Self-Automators](https://www.hbs.edu/ris/Publication%20Files/26-036_e7d0e59a-904c-49f1-b610-56eb2bdfe6f9.pdf) working paper studied 244 junior BCG consultants completing one fictional investment task with a custom GPT-4 interface in April 2023. Researchers analyzed 4,975 prompt-response interactions and 237 follow-up interviews. They identified fused or “cyborg,” directed or “centaur,” and abdicated or “self-automator” patterns.

The paper reports 146 fused, 34 directed, and 63 abdicated participants; those counts total 243 despite the stated sample of 244, and displayed percentages total 101%. The modes were observed, not randomized. Claims about which mode was more correct or persuasive were not accompanied by group outcomes, tests, intervals, or enough rater detail in the audited text. There was no human-only or AI-only arm and no longitudinal skill measure.

The study is valuable because it shows materially different ways people allocate work to the same tool. It cannot establish that centaurs generally outperform, that one style causes better judgment, or that a short 2023 consultant task transfers to software engineering.

## Framework evidence defines a better comparison

The ICML position paper [Centaur Evaluations](https://digitaleconomy.stanford.edu/app/uploads/2025/06/CentaurEvaluations.pdf) proposes specifying the distribution of humans, interface, outcome and process scores, human time, and compute, then varying human time and compute rather than benchmarking a model alone. It is an evaluation contract, not an experiment. The authors acknowledge task dependence, noisy and expensive studies, fairness failures, cases where AI alone beats a hybrid, and the disappearance of the chess-centaur advantage.

A 2026 [systematic review of human-in-the-loop AI](https://www.mdpi.com/1099-4300/28/4/377) offers a three-dimensional taxonomy: where the human sits in the lifecycle, the granularity of interaction, and its timing. It maps evaluation across task effectiveness, human factors, interaction quality, governance, and lifecycle robustness. Crucially, it warns that a person can become a scapegoat or rubber stamp without information, time, expertise, and override authority.

The review describes a 134-source English-language corpus but does not publish reproducible queries, full flow counts, reviewer agreement, extraction data, quality appraisal, or risk-of-bias assessment. There is no pooled effect. It supports vocabulary and design questions, not the claim that human involvement improves outcomes.

The 2026 [PNAS Nexus perspective on human–AI teaming](https://academic.oup.com/pnasnexus/article/5/3/pgag030/8490283) adds explicit goals, role partitioning, audit trails, uncertainty, escalation, disagreement procedures, circuit breakers, recourse, fallbacks, and joint process/outcome evaluation. Its evidence base is acknowledged to be dominated by laboratories, small deployments, and prototypes. These are responsible design propositions, not measured software effects.

## Which decisions should remain visibly human?

The evidence does not produce a universal list. A defensible allocation starts with consequence and legitimacy.

Humans should visibly own the **ends**: whose needs count, which tradeoffs are acceptable, and what harms the organization refuses to optimize away. They should retain accountable authority over **high-consequence commitments** that are difficult to reverse, especially where affected people cannot consent or recover easily. They should own **exceptions and recourse**, because applying a general rule to an unusual case often requires values and context absent from the rule. They should also decide whether the available evidence is sufficient to increase autonomy and whether an incident requires stopping or rolling back the system.

That does not mean a person must manually inspect every low-risk implementation detail. Automation may improve consistency, accessibility, attention to known rules, and detection of patterns humans miss. Human judgment can introduce fatigue, bias, politics, and delay. In a reversible, observable task with a strong verifier, AI-only execution plus human policy ownership may be better than per-change approval.

The allocation must therefore be local and revisable. Consequence, reversibility, uncertainty, data sensitivity, privilege, blast radius, observability, recovery evidence, and system maturity all matter. A fixed “human always reviews code” rule can be both too weak for value-laden decisions and needlessly expensive for well-constrained ones.

An official [LLVM community RFC on AI-tool use](https://discourse.llvm.org/t/rfc-llvm-ai-tool-policy-human-in-the-loop/89159) illustrates the governance choice. It proposes that contributors understand, review, explain, revise, and take responsibility for submitted changes, while the discussion preserves disagreement about inclusion, objective evidence, exceptions, and policy lock-in. The RFC establishes a live proposal and dissent, not adoption or effectiveness. Comprehension and accountability are decision criteria; a “human-reviewed” label alone is not evidence that they were met.

Allocation also has distributional consequences. Moving people only to exception handling can leave them with rare, stressful cases and too little routine practice to stay calibrated. Keeping routine decisions human can impose needless delay on those awaiting service. Workload, skill retention, and who bears failure must sit beside average accuracy.

## Exercise: the judgment-rights card

For one automated workflow, complete a card for the highest-consequence decision:

- What exact choice is being made, and who is affected?
- Who owns the choice before and after failure?
- What expertise and information does that person need?
- How much time do they actually receive?
- Can they stop, override, defer, or demand new evidence?
- How can an affected person appeal?
- What is the strong human-only baseline? The strong AI-only baseline?
- Which outcome, severity, workload, distributional effect, and recovery measure will compare all three?
- When will the allocation be reconsidered?

Observe a real decision. If the owner cannot explain the evidence, exercise authority, or change the system after failure, redesign the loop before adding another approval box.

## What survives skeptical review

Meaningful human judgment is an institutional capability made of authority, expertise, information, time, recourse, accountability, and learning. Human presence alone can add no value or negative value, and hybrid performance is task-dependent.

Keep people visibly responsible for goals, consequential and hard-to-reverse tradeoffs, exceptions, recourse, and changes to the autonomy boundary. Automate where evidence shows a constrained system is safer or more effective. Then compare the actual human-only, AI-only, and hybrid workflows rather than treating “human in the loop” as the conclusion.

Podcast hook: If the reviewer has twenty seconds, no appeal path, and no power to stop deployment, is the human in the loop—or merely on the liability form?

Continue reading: [Management interlude 35a: Protect differentiated human value deliberately](35a-management-human-value.md) turns judgment, shared reasoning, and careful design into portfolio decisions.
