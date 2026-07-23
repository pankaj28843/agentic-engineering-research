# 17. Design quorums, non-AI drills, and orchestration curricula

> **Report point:** Apprenticeship, bullet 17, page 6 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** The countermeasures have plausible learning mechanisms; their workplace efficacy is unresolved.

If agents take over routine implementation, telling people to “learn to supervise agents” is not enough. Supervision itself depends on judgment: noticing a hidden assumption, recognizing a suspiciously easy answer, choosing evidence, and knowing when to stop. Those abilities were often built through work that now looks delegable.

The retreat proposed design quorums, deliberate non-AI practice, and an orchestration curriculum. Each could preserve opportunities to build judgment. None has been validated as a workplace remedy. The responsible move is to treat them as interventions with explicit mechanisms, ethical boundaries, and delayed learning outcomes—not as traditions to mandate by intuition.

## A plain-language model: protect the learning loop

Skill develops through a loop:

1. **Attempt:** the learner makes a consequential choice rather than watching an answer appear.
2. **Explanation:** they expose the model, assumptions, and uncertainty behind the choice.
3. **Feedback:** a person, test, or real outcome reveals what the model missed.
4. **Revision:** they try again with that discrepancy in mind.
5. **Transfer:** later, they recognize and handle a related problem without copying the earlier solution.

An agent can strengthen any step. It can generate examples, simulate alternatives, give immediate feedback, or help someone explore a codebase. It can also bypass the attempt, compress explanation into acceptance, and make success arrive before the learner has formed a model.

The countermeasure question is therefore not “Was AI allowed?” It is “Which cognitive and social work did the learner actually perform, and did it transfer later?” Task completion, satisfaction, interaction, immediate comprehension, and delayed transfer are separate outcomes.

## The strongest warning is short-horizon

The most direct audited experiment randomized 52 experienced Python users who were unfamiliar with the Trio library. In [How AI Impacts Skill Formation](https://arxiv.org/html/2601.20245v2), 26 participants used a GPT-4o chat assistant and 26 did not; both groups could search the web. They completed two tasks with up to 35 minutes each, followed immediately by an unaided 14-question, 27-point quiz about concepts, code reading, and debugging.

The AI group scored 4.15 points lower, reported as a 17% difference (`d = 0.738`, `p = .01`). Task time did not differ significantly. All AI-assisted participants completed both tasks, while four control participants did not finish the second. That combination is important: completion and immediate understanding can move differently.

The experiment does not show career-scale deskilling. It used one session, one unfamiliar library, an immediate quiz, and no production task, delayed retention measure, human-pair condition, or autonomous coding agent. Exploratory interaction patterns suggested direct delegation might be less conducive to understanding, but the relevant subgroup was only about four people. It supports a learning-risk question and the need to distinguish outcomes, not a universal prescription.

## What interaction studies add

A small controlled student study provides mechanism evidence without a learning result. [The AI pair-programming study](https://www.se.cs.uni-saarland.de/publications/docs/WSD+.pdf) assigned 19 late-bachelor or early-master students to human–human or human–AI work. Researchers annotated about 35 “knowledge-transfer episodes” per human-pair session and 18 per human–AI session. Yet an episode meant that a perceived knowledge gap prompted an attempt to resolve it; it did not show what participants later understood or retained. Conditions differed, prior AI experience was unbalanced, and there was no pre/post assessment.

Two classroom studies show that course design matters. In a 12-week course of 364 students, [Salomon and colleagues](https://www.cs.ubc.ca/~rtholmes/papers/splash_2025_salomon.pdf) observed AI-first help seeking and less peer communication in some interviews, but had no non-AI cohort or objective learning comparison. A [three-cohort introductory programming study](https://arxiv.org/html/2603.22672v1) followed 248 students across successive 2023–2025 offerings and logged 10,632 interactions with a custom GPT. Help-seeking and verification patterns changed while assignment and final performance remained broadly similar. Successive cohorts were not the same people; models, calendar time, and cohort composition changed together, and there was no delayed retention.

Workplace evidence is thinner. [A case study of two established teams](https://scholarspace.manoa.hawaii.edu/bitstreams/4f29b0c8-06ac-4d5d-9fa0-52eb93321eb2/download) observed different AI use in solo and paired sessions, including more human handling of domain questions in pairs. It measured no retained learning. Interviews with [13 generative-AI users](https://arxiv.org/html/2405.01543v1) elicited reports of learning, rubber-ducking, and changed human collaboration, but offered no comparator or objective outcome.

Across these sources, explanation, peer discussion, verification, and use mode are plausible moderators. That is mechanism convergence across unlike studies, not a pooled intervention effect.

## Three candidates, three unproven mechanisms

**A design quorum** brings multiple people into framing, modeling, and acceptance decisions before or around agent execution. Its proposed mechanism is required explanation plus distributed challenge. A quorum can fail if a senior performs the reasoning while juniors merely prompt, if status suppresses disagreement, or if attendance is mistaken for participation.

**A non-AI drill** temporarily removes assistance so a learner can inspect what they can retrieve, explain, or debug unaided. Its mechanism is diagnosis and deliberate practice, not moral purification. It can fail through irrelevant puzzles, anxiety, inaccessible format, hidden scoring, or punitive use. University teaching guidance from the [Duke Center for Teaching and Learning](https://ctl.duke.edu/ai-ethics-learning-toolkit/does-ai-harm-critical-thinking/) offers transparent compare-and-reflect exercises, but reports no measured effect and does not authorize workplace surveillance.

**An orchestration curriculum** teaches problem decomposition, context selection, tool boundaries, evidence choice, verification, escalation, and reflection. Its mechanism is to make supervision knowledge explicit. It can fail if “orchestration” becomes prompt folklore detached from domain expertise, or if learners coordinate work they could not evaluate themselves.

All three should be compared with ordinary mentoring, deliberate practice on real tasks, documentation-first work, and project rotation. A new label is not evidence that the learning design is new or better.

## What would count as success

An intervention should improve a defined capability beyond the immediate exercise and do so at an acceptable human cost. A useful evaluation would include a baseline, a matched or crossover comparison, an immediate task, and a delayed related task that requires transfer rather than recall. It would record who actually explained and decided, not merely who attended, and would examine code or operational outcomes alongside individual understanding.

The study also needs attrition and burden data. If the people most overloaded by a quorum stop participating, the remaining group can appear to improve. If a drill helps confident speakers while disadvantaging someone who needs an accessible format, an average score hides harm. Ordinary mentoring or project rotation is a serious rival: a branded agentic curriculum should beat the support people could have received without it, not just beat no support at all.

No audited study meets that bar in a software workplace. Naming the bar prevents an engaging workshop, a high satisfaction score, or a successful demo from being reported as preserved apprenticeship.

It also prevents a null result from being blamed automatically on learners. The intervention, facilitation, task relevance, access, and opportunity to practise are all part of the causal package.

## Exercise: a consented countermeasure trial

Choose one job-relevant capability, such as explaining a service boundary or diagnosing a failed test. Invite a small group to co-design a four-week formative trial.

- Record a baseline through a declared, accessible task with feedback.
- Specify which loop step the intervention is meant to strengthen.
- Use one candidate intervention and preserve normal mentoring as the comparator.
- Measure immediate performance and a related task after a delay.
- Ask participants about burden, psychological safety, access, and whether the exercise resembled their work.
- Minimize stored data, set a deletion date, and prohibit use in ranking, discipline, hiring, promotion, or compensation.
- Publish a null or harmful result as readily as an improvement.

Do not infer an individual deficit from one task. The trial asks whether the work design creates learning opportunities. [Chapters 48](48-run-design-quorums.md) and [49](49-non-ai-learning-checkpoints.md) own facilitation and assessment details.

## What survives skeptical review

There is bounded evidence that AI-assisted completion can coexist with lower immediate comprehension and that human–AI use changes conversation, help seeking, and verification. There is no matched workplace evidence that design quorums, non-AI drills, or orchestration curricula improve objective learning and delayed retention.

The countermeasures are worth testing because their mechanisms are legible, not because efficacy is settled. Protect attempts, explanations, feedback, revision, and transfer; then measure whether the proposed practice actually carries them.

Podcast hook: If an agent completes the apprenticeship task, which part of the apprentice’s learning loop disappeared—and how could a team restore it without turning work into an exam?

Continue reading: [Chapter 49: Add non-AI learning checkpoints](49-non-ai-learning-checkpoints.md) develops the ethical formative-assessment boundary.
