# 25a. Manage the story, not just the metric

**Management interlude — not a report bullet**

*Part 3 source: “Manage the story, not just the metric,” page 14 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf).*

Boards do not make decisions from metrics alone. They interpret metrics through a causal story: what changed, why it matters, who can act, and what happens next. Management’s job is not to suppress that narrative instinct. It is to make the story auditable.

This interlude synthesizes the expectation gap in [Chapter 04](04-executive-engineer-gap.md), investment framing in [Chapter 22](22-board-legible-modernization.md), evidence translation in [Chapter 23](23-stories-benchmarks-executive-learning.md), and lifecycle measurement in [Chapter 25](25-productivity-hype-bubble.md). It introduces no new productivity estimate.

## The claim stack

Most board stories contain five layers, even when they appear as one sentence:

1. **Observation:** a demo succeeded, a metric moved, or an incident occurred.
2. **Mechanism:** the agent generated, searched, reviewed, acted, or failed in a particular way.
3. **Estimate:** the observed effect is quantified for a defined population and boundary.
4. **Forecast:** the estimate is projected across teams, systems, or time.
5. **Decision:** the organization funds, restricts, expands, or stops something.

Each layer needs its own evidence. A vivid observation can establish possibility. It cannot silently become a population estimate. A measured local effect cannot become a portfolio forecast without selection and transfer assumptions. A forecast does not determine a decision until cost, risk, alternatives, and reversibility are considered.

Write the layers as separate sentences in every board paper. Label each one **observed**, **measured**, **inferred**, **forecast**, or **recommended**. The visible seams prevent confidence from leaking upward.

## Curate for truth, not only impact

The retreat is right that a concrete story can make an invisible engineering problem legible. It also warns that repeatable success anecdotes can oversell capability. Both dynamics are visible in the public evidence. Reuters recorded a major [market reaction to Anthropic’s COBOL modernization announcement](https://www.reuters.com/business/ibm-posts-steepest-daily-drop-since-2000-after-anthropic-says-ai-can-modernize-2026-02-24/); the reaction does not independently verify the capability claim.

The management answer is **paired storytelling**:

- Put the successful demo beside a failed or bounded case.
- State what was selected, rehearsed, retried, or excluded.
- Follow the visible output through review, integration, operation, and maintenance.
- Attach a base rate when one exists; say “no suitable base rate” when it does not.
- Name the counterfactual: current practice and the best non-AI alternative.
- State which decision the story can and cannot support.

A security incident without exposure can motivate investigation but not establish a trend. A token bill without workload, calls, retries, and price decomposition cannot identify the remedy. A fast coding task without a lifecycle boundary cannot become a delivery forecast. The board should see those missing fields, not an invented placeholder.

## Make fact-checking a management process

Fact-checking should occur before a claim enters the recurring management narrative, not as a forensic exercise after a failed investment.

For every material AI claim, assign a named **claim owner** who is different from the program sponsor where practical. The owner maintains:

- exact wording and decision purpose;
- original source and date;
- evidence class and independence;
- population, task, baseline, denominator, and quality gate;
- local applicability and known exclusions;
- counterevidence and alternative explanations;
- forecast assumptions;
- expiry or review date;
- observed outcome after the decision.

Use original studies and records, not slide citations, search snippets, or repeated vendor summaries. If the source is an anonymous retreat account, label it an anonymous lead. If it is a consultancy case without raw data, retain that limitation. If a study’s authors later weaken their conclusion—as METR did when [later participation and task-selection changes damaged validity](https://metr.org/blog/2026-02-24-uplift-update/)—update the board narrative rather than preserving the earlier headline.

## A 45-minute story review

Choose one claim that will influence funding or policy.

**Minutes 0–10: Decompose.** Write its observation, mechanism, estimate, forecast, and decision layers. Highlight any missing layer.

**Minutes 10–20: Audit.** Open the original source. Record evidence class, denominator, comparison, quality boundary, uncertainty, conflicts, and omitted lifecycle work.

**Minutes 20–30: Pair.** Add the strongest failure case, boundary condition, or alternative explanation. If no counterevidence is available, record that as a research gap.

**Minutes 30–40: Decide reversibly.** Define the smallest decision the evidence supports, maximum exposure, stage gate, stop condition, and next measurement.

**Minutes 40–45: Assign memory.** Name the claim owner, outcome owner, review date, and repository location for the evidence packet.

The meeting output is a one-page claim stack, not another dashboard. Repeat it when the model, workflow, price, population, or risk tier changes.

## What management should hear

A good story does not end with “AI worked” or “AI failed.” It sounds like this:

> In this defined workflow, under these conditions, we observed this result. The likely mechanism is this. The evidence does not cover these systems or outcomes. We will make this bounded, reversible decision, monitor these leading and outcome measures, and revisit it on this date.

That language may feel less exciting than a universal multiplier. It is more useful because it preserves the route from evidence to action.

Management should also ask whose story is missing. Successful users are more visible than non-adopters; central platform teams see aggregate usage but not every review burden; engineers see failure detail but may not see balance-sheet effects; vendors see adoption through their own instruments. A board narrative should name these viewpoints and the incentive attached to each.

## Evidence boundary

There is moderate support for the need to distinguish stories, benchmark contracts, and local outcomes. Empirical studies in Chapter 23 demonstrate how conclusions move when task selection, environment, oracle, or audit changes. There is no audited causal evidence that this specific governance routine improves board decisions. Treat it as a testable management control: retain the claims, decisions, and later outcomes, then inspect whether calibration improves.

The principle is simple: metrics need narrative to become decisions, and narratives need provenance to remain honest.

Podcast hook: A five-layer board story starts with one impressive demo and ends with a portfolio bet. The tension comes from stopping confidence at every seam until the evidence earns the next layer.

Continue reading: [Chapter 22](22-board-legible-modernization.md) supplies the investment ledger; [Chapter 23](23-stories-benchmarks-executive-learning.md) supplies the evidence card; [Chapter 25](25-productivity-hype-bubble.md) supplies the measurement boundary.
