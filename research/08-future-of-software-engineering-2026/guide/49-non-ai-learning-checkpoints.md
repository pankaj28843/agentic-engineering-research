# 49. Add non-AI learning checkpoints

> **Report point:** People and skill formation, bullet 49, page 12 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** A declared formative checkpoint can expose a learner’s own understanding; workplace efficacy and longitudinal benefit are unvalidated.

A non-AI checkpoint is a brief, known-in-advance exercise in which someone recalls, explains, diagnoses, or performs a job-relevant skill without generative assistance. Its legitimate purpose is feedback: help the learner and team see which understanding is available when the tool is absent, wrong, or too slow.

It is not a covert test of loyalty to pre-AI work, a proxy for intelligence, or an instrument for ranking employees. Production software engineering is usually open-book and collaborative. The checkpoint should isolate only a capability that matters under real conditions, then return the person to normal tools with better information.

## A plain-language model: inspect the fallback, not the person

Pilots train with simulators and checklists even though they normally use instruments. The goal is not to prove that instruments are bad. It is to identify what the pilot must notice, decide, and do when automation is misleading or unavailable.

Software teams can use the same logic. A developer may need to:

- explain an authorization boundary before approving generated code;
- predict the consequence of a schema or migration change;
- diagnose a failure from logs when the agent suggests a plausible but wrong cause;
- state an invariant and design a counterexample;
- recover a service using an established runbook.

Those are judgment and recovery capabilities. Asking someone to memorize syntax that is always searchable would measure nostalgia, not resilience.

The checkpoint is valid only if its exercise, conditions, interpretation, and consequences match its stated purpose. “No AI” describes the tool condition; it does not establish that the task measures learning.

## What the evidence permits

The strongest bounded result comes from a randomized [study of 52 experienced Python users](https://arxiv.org/html/2601.20245v2). Participants completed two unfamiliar-library tasks of at most 35 minutes using either an AI chat assistant or conventional web resources, then took an immediate unaided quiz. The AI group scored lower on that comprehension measure; task time did not differ significantly, and all AI participants finished while four control participants did not. The study did not measure delayed retention, workplace performance, autonomous coding agents, or career skill.

A [survey of 319 knowledge workers](https://www.microsoft.com/en-us/research/wp-content/uploads/2025/01/lee_2025_ai_critical_thinking_survey.pdf) analyzed 936 self-reported examples of generative-AI use. It measured perceived critical-thinking enactment and effort, not objective ability or decline. Confidence in AI and confidence in oneself were associated with different reported effort, but the cross-sectional, self-reported design cannot establish causation.

A [three-cohort introductory-programming study](https://arxiv.org/html/2603.22672v1) analyzed 248 students and 10,632 interactions, including 2,782 coded interactions. Assignment performance did not differ significantly under its reported comparison, while help-seeking patterns changed. Successive cohorts and time effects prevent a clean causal conclusion.

Finally, a [19-student pair-programming study](https://www.se.cs.uni-saarland.de/publications/docs/WSD+.pdf) counted attempts to address perceived knowledge gaps, not retained knowledge. Together these sources justify separating completion, perceived effort, observed behavior, immediate comprehension, and delayed transfer. They do not prove a durable workplace learning loss or that checkpoints repair one.

## The ethical gate comes first

Do not run a checkpoint unless all of these conditions hold:

1. **Declared:** people know the purpose, task class, tool conditions, data use, and feedback process in advance.
2. **Participatory:** affected workers help choose relevant competencies and challenge the design.
3. **Formative:** results guide practice and support; they are separate from pay, discipline, promotion, redundancy, and forced ranking.
4. **Job-relevant:** the unaided capability has a credible role in review, recovery, safety, communication, or learning.
5. **Accessible:** accommodations and alternative response modes preserve the construct rather than testing disability, language speed, or test familiarity.
6. **Data-minimized:** collect only what feedback requires, limit access, declare retention, and delete person-level records on schedule.
7. **Contestable:** participants can explain context, challenge scoring, and opt out or use an equivalent alternative without retaliation.
8. **Low stakes:** uncertainty is expected and help follows quickly.

If management wants surprise tests, individual rankings, continuous monitoring, or employment decisions, stop. The selected education and workplace sources do not authorize those uses.

## Select a competency from real work

Begin with a recent incident, review escape, or repeated misunderstanding. Ask:

- What decision did a human need to make?
- What clue or invariant should have been recognized?
- Under what real condition might AI be unavailable or untrustworthy?
- What observable response would demonstrate useful understanding?
- Which reference materials would normally be available?

Write the competency as an action: “Given these logs and the service map, identify the likely violated invariant and choose the next safe diagnostic.” Avoid “understands distributed systems.”

Use three exercise types:

- **Recall:** state a small set of critical invariants or escalation triggers without assistance.
- **Explanation:** explain a design, tradeoff, or generated change in plain language to a collaborator.
- **Application:** diagnose or modify a bounded scenario using allowed non-generative references.

Recall should be the smallest portion. Most professional competence is explanation and application with documentation.

## Compare tool conditions honestly

Use a two-part checkpoint, not an ideological contest.

In **Part A**, allow normal non-generative references—code, documentation, runbooks, logs, and search—while withholding generative assistance for 10 to 20 minutes. Record reasoning, uncertainty, and requested information, not typing speed.

In **Part B**, restore the normal AI tool. Ask the learner to compare its answer with their own, identify what changed, verify one consequential claim, and revise the response. This tests calibration and integration, which are part of contemporary work.

Where useful, add a later transfer sample on a different but structurally similar scenario. Repeating the same question mostly measures memory for the exercise. Space it by days or weeks and keep the burden low.

Do not interpret a lower unaided result as evidence that AI caused the gap. The competency may never have been taught; the task may be inaccessible; anxiety, unfamiliarity, language, or poor instructions may dominate. A baseline before an intervention is better than a one-off diagnosis.

## A four-week pilot

Choose one team and one competency. Co-design two equivalent scenarios with domain experts and an accessibility reviewer. Pilot them with volunteers, including experienced people, to detect ambiguous scoring and hidden knowledge.

At week zero, run the two-part baseline and give private feedback immediately. Offer a learning activity: explanation with a peer, deliberate practice, review of counterexamples, or guided use of the agent. At weeks two and four, use new scenarios that exercise the same underlying decision. Keep ordinary production work and open-book practice unchanged.

Use a simple rubric:

| Dimension | Evidence to look for |
|---|---|
| Model | Names the relevant components, actors, or invariant |
| Evidence | Distinguishes observation from assumption |
| Judgment | Chooses a safe next action and explains the tradeoff |
| Calibration | Marks uncertainty and knows when to escalate |
| Transfer | Applies the reasoning to a changed scenario |

Score descriptions, not people. Two trained reviewers can compare a sample to find rubric ambiguity; inter-reviewer disagreement should trigger rubric repair, not averaging away the problem.

## Metrics and interpretation

Report participation and denominators alongside:

- change in rubric dimensions across equivalent scenarios;
- delayed transfer, not only immediate correction;
- ability to identify and repair a plausible AI error in Part B;
- participant-rated relevance, safety, accessibility, and feedback usefulness;
- time burden and disruption;
- production signals related to the target competency, such as review catches or recovery quality, aggregated cautiously;
- opt-outs, accommodations, contested results, and missing data.

Do not create a single “AI dependency score.” More unaided recall does not necessarily improve production judgment, and a production outcome can change for many reasons. Small voluntary pilots are especially vulnerable to selection effects. Present qualitative counterexamples and alternative explanations.

The decisive comparison is not whether people can reproduce code from memory. It is whether a bounded practice improves a job-relevant decision later without creating surveillance, stigma, or inequity. The current corpus does not answer that longitudinal question.

## Stop and rollback

Stop immediately if results enter performance management, identities leak beyond the agreed feedback circle, participants discover surprise scoring, or accommodations are denied. Delete improperly collected records and notify participants of what happened.

Pause when reviewer agreement is poor, scenarios reward obscure recall, participation drops because people feel unsafe, or repeated scores do not relate to the named work capability. Redesign with worker input before continuing.

Set a pilot stop rule such as: if perceived safety or job relevance declines across two rounds, if the time burden exceeds the agreed budget, or if no delayed transfer signal appears after the learning activity, do not scale. Absence of improvement may mean the exercise or intervention is wrong, not the people.

Rollback means ending the checkpoint schedule, deleting person-level records according to the contract, and returning to ordinary learning support. Preserve only anonymized design lessons that participants agreed could be retained. Substitute less test-like mechanisms—peer explanation, incident rehearsal, guided review, or a team game day—when those fit the competency better.

## The practical checkpoint card

Before any exercise, publish:

- competency and why it matters;
- normal tools and temporarily unavailable tools;
- realistic scenario and allowed references;
- accessibility options;
- descriptive rubric;
- feedback and support offered;
- data owner, access, retention, and deletion date;
- explicit prohibited uses;
- stop and appeal routes.

If that card would make the intervention politically uncomfortable to state plainly, the design is probably unsafe. A checkpoint should increase agency by helping people inspect and strengthen their understanding. It should never become evidence that workers must compete with a tool under artificial conditions.

Podcast hook: Can a ten-minute no-AI exercise reveal a useful fallback skill without becoming a loyalty test for the pre-AI profession?

Continue reading: [Chapter 19: LLM use, critical thinking, and the limits of the evidence](19-llm-critical-thinking.md) separates immediate comprehension, self-report, behavior, and durable skill.
