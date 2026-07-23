# 19. Does LLM use erode critical thinking?

> **Report point:** Apprenticeship, bullet 19, page 6 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** Some bounded tasks show different comprehension and thinking behavior; general cognitive decline and workplace transfer are unproven.

“LLMs reduce critical thinking” compresses several different claims into one alarming sentence. A person can finish a task, report little mental effort, fail an immediate comprehension quiz, forget material later, or struggle to transfer a concept to a new setting. Those outcomes are not interchangeable.

The student and worker research in the audited corpus raises a credible concern about how assistance changes activity. It does not establish that LLM use causes a general erosion of cognition. The studies differ in population, exposure, task, measurement, and horizon; some produce a counter-signal rather than a simple decline.

## A plain-language model: the learning-outcome ladder

Think of six rungs:

1. **Completion:** Did the person produce an acceptable answer or artifact?
2. **Behavior:** What did they ask, check, discuss, or delegate while working?
3. **Perceived effort:** Did they feel that they analyzed, evaluated, or created?
4. **Immediate comprehension:** Can they explain or debug the material without assistance now?
5. **Retention:** Can they still do so after time has passed?
6. **Transfer:** Can they apply the underlying judgment to a meaningfully different problem?

Evidence on a lower rung cannot silently climb to a higher one. A course grade is not delayed retention. A prompt log is not knowledge gained. Self-reported effort is not objective skill. An immediate quiz is not career development. Even “critical thinking” can refer to different activities—analysis, evaluation, synthesis, verification, or stewardship—depending on the instrument.

This ladder also prevents an opposite mistake: successful completion does not prove preserved understanding.

## The most direct experiment

[How AI Impacts Skill Formation](https://arxiv.org/html/2601.20245v2) randomized 52 crowd workers who used Python at least weekly and had more than one year of experience. All were unfamiliar with the Trio library. Twenty-six used a GPT-4o chat assistant supplied with task context; 26 did not. Both groups could use web search. After a warm-up and two tasks of up to 35 minutes each, participants completed an unaided 14-question, 27-point conceptual, code-reading, and debugging quiz.

The AI group scored 4.15 points lower, which the authors describe as a 17% score difference (`d = 0.738`, `p = .01`). A warm-up-controlled model was similar (`d = 0.725`, `p = .016`). Task time did not differ significantly. All treatment participants completed both tasks, while four control participants did not complete the second.

This is a randomized short-horizon result separating completion from immediate comprehension. It deserves attention. Its boundaries are equally important: one unfamiliar Python library, one session, no code-writing assessment, no delayed test, no production setting, no human-pair comparator, and no autonomous agent. Most participants had at least four years of programming experience, but that does not make it a tenure study. The paper’s exploratory behavioral subgroups were tiny and cannot establish that one interaction style causes the score difference.

The precise conclusion is that, in this setting, AI-assisted completion coexisted with lower immediate unaided comprehension. “LLMs deskill developers” goes far beyond the design.

## A survey measures perception, not decline

The [CHI 2025 critical-thinking study](https://www.microsoft.com/en-us/research/wp-content/uploads/2025/01/lee_2025_ai_critical_thinking_survey.pdf) surveyed 319 Prolific participants who used generative AI at least weekly for work and retained 936 first-hand task examples. Participants were young and technology-skewed: 71.79% were 18–34, 59 reported computer or mathematical work, and 309 used ChatGPT.

Participants reported critical-thinking enactment in 555 of 936 examples. Mixed-effects models found that higher confidence in AI was associated with less perceived critical-thinking enactment (`β = -0.69`, `p < .001`), while self-confidence was associated with more. Qualitative responses described verification, integration, and stewardship as places where thinking moved.

This was cross-sectional self-report from people already using the tools. Confidence was not randomized, expertise was self-described, and the study did not measure correctness, objective cognition, skill loss, or retention. It would be wrong to subtract 555 from 936 and claim the remainder involved “no critical thinking.” The unit was a reported example and the construct was perceived enactment.

The study supports a redistribution hypothesis: as trust, task, and context vary, workers perceive their thinking work differently. It does not show that confidence caused decline.

## Classroom evidence supplies counter-signals

In [Three Years with Classroom AI in Introductory Programming](https://arxiv.org/html/2603.22672v1), three successive Japanese university cohorts totaled 248 students, mostly first-year programming beginners. Across 14 lessons and 57 exercises, a custom GPT logged 10,632 interactions. Researchers manually coded a stratified sample of 2,782 and observed changing help-seeking and verification patterns. Assignment scores did not differ significantly across cohorts (`H = 3.23`, `p = .357`), and final performance was broadly similar.

This is not individual longitudinal evidence. Cohort composition, model capability, peer behavior, and calendar time changed together; retries and outside help were possible; no delayed workplace transfer was tested. Still, broadly similar course outcomes complicate a universal decline story.

The [Microsoft New Future of Work Report 2025](https://www.microsoft.com/en-us/research/wp-content/uploads/2025/12/New-Future-Of-Work-Report-2025.pdf) maps a similarly heterogeneous research landscape across learning, trust, labor, and teaming. It mixes peer-reviewed studies, preprints, working papers, internal research, surveys, and perspective, so it is a secondary route rather than one experiment. Its value here is the warning that tool use, verification, skill, hiring, and team outcomes are different constructs. Any numerical finding must be traced to its underlying study and retain that study’s population and design.

One selected article titled “Cognitive Offloading in Student–AI Collaboration” was excluded from the audit because the captured page contained only a browser-verification shell. Its title and discovery metadata are not evidence. That exclusion illustrates the standard required here: an intuitively relevant study cannot enter the conclusion until its population, task, comparator, measures, and limitations can be read.

No result here is a replication of another. The unfamiliar-library experiment, worker survey, introductory course, and software-engineering course operationalize different constructs in different populations. Agreement would not create one pooled effect, and apparent disagreement need not be a contradiction. A claim about cognition should travel with its rung on the outcome ladder, or it will acquire certainty as it moves from paper to presentation to policy.

## How LLMs might help thinking

Automation can reduce unproductive search, offer alternative explanations, expose counterarguments, and let a learner rehearse questions privately. It can also free attention for evaluation and integration. The worker survey’s verification and stewardship themes and the classroom study’s later verification patterns are compatible with that possibility, though neither proves a benefit.

The likely moderator is use mode plus task design. Directly delegating a problem that was meant to build a mental model is different from using an LLM to critique a model the learner first articulated. A strong result on one task may come with a learning cost; on another, assistance may make a previously inaccessible learning opportunity possible. Accessibility, language, prior expertise, time pressure, and feedback quality can change the tradeoff.

## Exercise: audit a cognition claim

For any study—or an internal learning claim—fill out this card:

- **Population:** Who participated, and how were they recruited?
- **Task:** Was it a quiz, course, synthetic problem, or production decision?
- **Exposure:** Which model, interface, duration, and allowed alternatives?
- **Comparator:** What did the other group receive?
- **Construct:** Completion, behavior, perceived effort, comprehension, retention, or transfer?
- **Timing:** Immediate or delayed?
- **Quantity:** What count, effect, uncertainty, and missing denominator?
- **Rivals:** Prior expertise, motivation, tool access, cohort change, or task selection?
- **Transfer boundary:** What must be true before applying it to software work?

If a team adds an unaided check, declare it in advance, make it job-relevant and accessible, provide feedback, minimize stored data, and separate it from ranking and employment decisions. The goal is for learners to inspect understanding, not for employers to create covert surveillance. [Chapter 49](49-non-ai-learning-checkpoints.md) owns checkpoint design.

## What survives skeptical review

One randomized unfamiliar-library experiment found lower immediate unaided comprehension with AI assistance. A worker survey found associations in perceived thinking, and classroom studies observed changed help seeking with bounded and mixed performance results. No source establishes durable cognitive decline, career-scale deskilling, or transfer to agentic software workplaces.

The right question is not whether an LLM was present. It is which kind of thinking the task required, which activity the tool displaced or enabled, and what the person could understand and transfer later.

Podcast hook: When an AI-assisted learner finishes faster but understands less immediately, is that deskilling—or a task-design warning whose long-term meaning is still unknown?

Continue reading: [Chapter 49: Add non-AI learning checkpoints](49-non-ai-learning-checkpoints.md) shows how to test retained understanding without surveillance or nostalgia.
