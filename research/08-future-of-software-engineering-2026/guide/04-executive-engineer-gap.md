# The Executive–Engineer Gap

An executive sees a demonstration turn a request into working code in minutes. An engineer sees the missing production data, compatibility edges, security review, rollout path, and pager duty. Both observations can be true. The gap appears when a result at one level is silently promoted into a promise at another.

The useful mental model is an **evidence ladder**:

```text
demo → bounded task → repository change → production workflow
     → project outcome → portfolio economics → organization strategy
```

Every step adds constraints and possible bottlenecks. Evidence can climb the ladder, but it cannot skip rungs without assumptions. A task-time result is not a project schedule; a project schedule is not realized portfolio value.

The [2026 Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) presents an “executive–engineer gap” as a major concern. Participant reflections, including [Ivett Ördög's account](https://www.ivettordog.com/blog/2026-07-05-future-of-software-engineering-retreat-reflections), establish that the gap was salient at the event. Under Chatham House conditions, repeated accounts belong to a **dependent witness network**. They do not measure executive beliefs as a population, compare belief calibration by role, or show that overconfidence caused deployment failures.

The evidence does support a method for finding expectation mismatches before they become plans.

## How a number changes meaning as it travels

Suppose an experiment says an assisted developer completed a documentation task in half the time. In the next presentation, this becomes “developers are twice as productive.” In a budget meeting, it becomes “the program can finish in half the time.” Each translation changes the denominator.

A 2023 [McKinsey developer experiment](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/unleashing-developer-productivity-with-generative-ai) illustrates the first rung. More than 40 developers worked with and without then-current AI tools on code generation, refactoring, and documentation. The reported gains varied: documentation and new-code tasks were close to twice as fast, refactoring took roughly two-thirds of the time, complex tasks gained less than 10%, and junior developers were sometimes slower.

This is **bounded task evidence** from a consultancy's own developers. The captured article does not expose raw data, exact allocation, sequence effects, uncertainty, durable quality, or downstream delivery. The defensible sentence is “assistance changed time on these tasks.” “Software projects are twice as fast” is several unsupported rungs higher.

At the real-repository rung, [METR's 2026 update](https://metr.org/blog/2026-02-24-uplift-update/) is valuable because it reports a failed measurement, not because it supplies the current multiplier. Its randomized design covered 57 experienced open-source developers, 143 repositories, and more than 800 tasks. Yet AI-preferring developers increasingly declined to join, 30–50% of surveyed developers omitted some tasks, concurrent agents complicated time tracking, and compensation and task mix changed. METR therefore called its current signal unreliable.

This is **transparent randomized evidence with compromised participation and measurement**. It teaches executives and engineers the same lesson: adoption changes the population one can observe. A dashboard can become less representative precisely as a tool becomes normal.

## Public narratives can move faster than operating evidence

In February 2026, Anthropic argued that AI could help compress some COBOL-modernization work “from years to quarters” in [a first-party article](https://claude.com/blog/how-ai-helps-break-cost-barrier-cobol-modernization). Reuters then reported [IBM's steep market decline](https://www.reuters.com/business/ibm-posts-steepest-daily-drop-since-2000-after-anthropic-says-ai-can-modernize-2026-02-24/) following the announcement.

These sources establish a **vendor claim and a market reaction**. They do not establish that large mainframe replacements have been completed in quarters. The vendor article describes mapping, side-by-side testing, and human involvement at a high level; it does not provide the portfolio, comparison, defect record, cost accounting, or production outcome needed to validate the horizon. A price movement shows expectations responding, not the technical claim becoming true.

Thoughtworks practitioners answered with a more elaborate workflow: preprocessing, discovery, static and dynamic analysis, tacit constraints, reverse and forward engineering, data synchronization, possible dual running, and cutover ([their March 2026 response](https://www.thoughtworks.com/insights/articles/claude-code-cobol-modernization-reality)). They explicitly said the jury was still out. This is **firsthand consultancy practice evidence with declared uncertainty**, not a completed comparative modernization study. The contrast is useful: a public horizon can be crisp while the implementation denominator remains open.

## Engineers can be miscalibrated too

“Executive overconfidence” is an attractive story because it assigns ignorance upward. It is incomplete.

Engineers may extrapolate from tool fluency, treat a passing suite as business correctness, dismiss strategic value they cannot see, or use complexity as an argument against changing anything. Leaders may have evidence about market timing, opportunity cost, or portfolio constraints that a repository team lacks. Calibration is not a job title.

The more precise failure is **untranslated evidence**:

- the metric lacks a workload and quality denominator;
- the claim's rung is unclear;
- omitted work has no owner;
- uncertainty is stripped from the summary;
- a forecast is reported like an observation;
- a self-selected survey is treated as representative;
- a vendor or consultancy estimate is presented without its incentive and method.

For example, a 2026 scoping review and snowball survey reported frequent AI use and perceived gains among 65 respondents, heavily concentrated in DACH and younger participants, with only 30 professional developers ([arXiv preprint](https://arxiv.org/html/2603.16975v1)). This is **perception evidence from a narrow sample**, not an industry productivity estimate. Its value is understanding reported experience, provided that the sample travels with the number.

## The expectation-translation card

For every number used in an AI investment decision, put this card beside it:

| Field | Required answer |
|---|---|
| Claim | What exactly changed? |
| Evidence class | Experiment, observation, survey, benchmark, case, vendor claim, or forecast? |
| Unit | Person, task, repository, project, portfolio, or organization? |
| Workload | Which tasks, systems, and risk classes? |
| Comparator | Compared with what workflow and tool version? |
| Quality gate | What had to remain correct, safe, maintainable, and operable? |
| Boundary | Are review, tests, integration, release, incidents, and rework included? |
| Uncertainty | Interval, sample variation, selection, and known missing data? |
| Transfer assumption | Why should this result apply one rung higher or in this environment? |
| Owner | Who is accountable if the assumption fails? |

If a field is unknown, write “unknown.” Do not replace it with a plausible number from another study. The retreat's anonymous 2–3x versus 10x claims and a 12–18-month expectation-reset forecast, for example, have no attributable method in the audited corpus. Nearby task results cannot inherit their provenance.

## Exercise: hold a two-altitude review

Choose one planned agentic investment. Run a 60-minute review with the sponsor, an engineer, an operator, a product owner, and the relevant risk owner.

**First 20 minutes: executive altitude**

- Which business outcome should move?
- What is the latest date at which the outcome matters?
- Which capacity will be redeployed if local work becomes faster?
- What downside is unacceptable?
- What evidence would stop or shrink the investment?

**Second 20 minutes: engineering altitude**

- What work unit will change?
- Which environments, permissions, and data are required?
- What acceptance evidence exists, and what is still human judgment?
- Where will review, integration, or release queues grow?
- How is rollback demonstrated?

**Final 20 minutes: translate**

Draw the evidence ladder for the proposed claim. Mark every rung with observed evidence, a testable assumption, or an unknown. Select one short pilot that measures the first unsupported transition. Report both a positive and a negative outcome: time saved *and* rework, throughput *and* escaped defects, adoption *and* non-participation.

This is not a demand for certainty before action. It is a way to buy information at the rung where the decision currently rests.

## What a calibrated leader sounds like

A calibrated claim might be:

> On this selected documentation workflow, with these reviewers and this quality rubric, median elapsed time fell during a six-week pilot. We have not yet shown a release-level effect. The next gate measures review load, omission rate, and reuse by operators.

That statement is less dramatic than “AI doubles productivity,” but more decision-useful. It names the unit, scope, duration, gate, and missing rung.

The chapter's conclusion is therefore narrower than its title. The corpus does not show that executives are generally more overconfident than engineers, or that mental-model gaps dominate model limitations. It shows why task results, perceptions, market reactions, and portfolio promises must remain separate evidence classes. The preventable risk is not optimism. It is an unowned assumption disguised as a measured result.

Podcast hook: How does “this task took half the time” turn into a promise to cut a program in half—and at which rung should someone interrupt the story?

Continue reading: [Chapter 5 — Why Legacy Modernization May Be the Near-Term Value Pool](05-legacy-modernization-value.md).
