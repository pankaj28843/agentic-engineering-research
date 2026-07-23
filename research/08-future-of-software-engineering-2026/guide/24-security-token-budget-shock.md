# 24. Security incidents and token-budget shock

The retreat anecdotes are credible warning signals, but the audited evidence cannot show that agent-related security incidents rose twentyfold or that coding-agent token budgets generally exhausted annual allocations in three months. The organizations, baselines, incident definitions, exposure counts, and billing records behind those claims are unavailable.

The [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) attributes both observations to unnamed participants. That provenance is appropriate for surfacing an emerging risk under Chatham House rules. It is insufficient for estimating trend, prevalence, or cause. Management should respond by installing denominators and controls, not by repeating the multipliers as an industry rate.

## A plain-language model: counts need exposure

Raw incident counts behave like road-accident counts. If ten times as many vehicles are travelling, more accidents can occur even if each trip is safer. Better detection and reporting can also raise the count without changing underlying risk.

For agents, a minimally useful incident rate is:

> confirmed incidents / defined unit of agent exposure

The exposure might be active users, agent sessions, tool calls, autonomous runs, generated changes merged, production actions, or hours operating with a given permission tier. No single denominator fits every event, but one must be named.

Spend has a similar decomposition:

> spend = workload × calls per workload × tokens per call × unit price + tool, infrastructure, and review overhead

A larger bill may come from successful adoption, longer contexts, runaway retries, expensive model choice, duplicated agents, uncached prompts, price change, weak caps, or unowned experimentation. “Token budget shock” describes the outcome, not the mechanism.

The two ledgers should connect. A policy that reduces spend by truncating context may increase faulty actions and review. A security control that adds repeated scans or model calls may increase cost while lowering risk. Optimizing either number alone can be misleading.

## What independent evidence was found

The closest cost evidence concerns enterprise AI broadly, not coding-agent token budgets.

A [Channel Dive article summarizing a Flexera survey](https://www.channeldive.com/news/flexera-itam-ai-cost-tracking-tokenmaxxing/823709/) reports more than 500 IT asset-management respondents. Two-thirds allegedly lacked accurate visibility into AI usage, only 36% had a complete view of AI assets, and three-fifths reported increased AI overspend. The article also relays an Uber budget anecdote involving four months, not the retreat’s unnamed three-month coding-token claim. Because this is secondary trade-press reporting, the underlying sampling and questionnaire were not available in the audited corpus. It supports a visibility problem, not a precise software-engineering rate.

A [CFO Dive article](https://www.cfodive.com/news/7-10-firms-report-ai-cost-overruns/825961/) reports a vendor survey of 300 US executives in which 68% said AI initiatives ran over budget at least sometimes, 33% said mostly or always, and 9% said more than three-quarters of initiatives showed measurable return. This is also secondary, vendor-sponsored evidence with limited method detail, covering all AI initiatives. It cannot tell whether token unit cost, unplanned usage, weak budgeting, or conventional program overruns caused the responses.

A self-selected [Pragmatic Engineer survey of more than 900 respondents](https://newsletter.pragmaticengineer.com/p/the-impact-of-ai-on-software-engineers-2026) found reported coding-tool costs, usage limits, and a minority who regarded the tools as below value. These are perceptions and individual reports, not audited company billing or a representative incidence estimate.

The corpus contained **no independent population study of agent-related security incidents** with stable definitions and exposure denominators. That absence is the central result, not a reason to substitute adjacent numbers.

[World Wide Technology’s enterprise guidance](https://www.wwt.com/wwt-research/how-to-securely-implement-ai-coding-assistants-across-the-enterprise) identifies plausible control surfaces: vendor vetting, access controls, data and secret handling, logs, code scanning, SAST/DAST, penetration testing, prompt and provenance retention, CI/CD gates, monitoring, training, and tracking acceptance and failure trends. It is practitioner guidance, not evidence that those controls reduce incidents by a measured amount.

This leaves a clear evidence classification:

- The retreat’s “20x” and “annual budget in three months” statements are **anonymous observations**.
- Broad-AI surveys provide **limited secondary evidence** that cost visibility and budget control are common concerns.
- Security guidance provides **mechanism and control evidence**, not prevalence or effectiveness estimates.
- Industry-wide coding-agent incident and token-spend trends remain **open questions**.

## Definitions before dashboards

An organization cannot measure a security trend until it defines what counts. At minimum, separate:

- **Data events:** sensitive context sent, retained, exposed, or used outside policy.
- **Secret events:** credentials generated, logged, committed, disclosed, or misused.
- **Code events:** vulnerable or policy-violating output merged or deployed.
- **Dependency events:** unapproved, malicious, vulnerable, or hallucinated packages introduced.
- **Action events:** an agent changes infrastructure, data, permissions, or external systems improperly.
- **Privilege events:** the agent or integration obtains broader access than intended.
- **Governance events:** an unregistered model, tool, account, or workflow bypasses required controls.

Record near misses separately from confirmed incidents, and severity separately from count. A blocked secret commit is evidence that exposure occurred and a control worked; counting it as equivalent to a production breach makes both safety and trend analysis worse.

Every record needs event time, detection source, agent and tool version, permission tier, affected asset, exposure unit, severity, containment time, root-cause class, and owner. Retain enough provenance to reproduce the causal chain without retaining sensitive prompts indiscriminately.

## The paired warning-signal ledger

Use a weekly or monthly table with security and economics on the same row for each workflow.

### Exposure columns

- Active users and sessions.
- Agent runs and tool calls by permission tier.
- Generated changes proposed, merged, and deployed.
- Production or external actions.
- Workload category and criticality.

### Security columns

- Near misses, confirmed incidents, and severity-weighted loss.
- Rate per relevant exposure unit.
- Detection channel and median detection/containment time.
- Control stage that stopped the event.
- Recurrence by root cause.

### Economics columns

- Input, output, cached, and reasoning tokens where available.
- Calls, retries, aborted loops, and tool round trips per completed task.
- Model and current unit price.
- Infrastructure, scanning, observability, and human-review cost.
- Cost per accepted change or completed workflow—not merely per call.
- Budget owner, cap, forecast, and variance explanation.

### Interpretation columns

- Adoption or workload change.
- Model, price, policy, or permission change.
- Known measurement or reporting change.
- Expected benefit and quality result.
- Corrective action and review date.

Run a simple reconciliation exercise on the largest weekly variance. Decompose it into volume, calls per task, tokens per call, price, and overhead. Then examine incident-rate changes using the same workload and permission cohorts. If the organization cannot perform this decomposition, it knows that the budget alarm is real but not yet what to fix.

## Counterexamples and boundary conditions

Rising raw incidents can be a good sign if reporting and detection improve faster than exposure. Falling counts can be dangerous if teams move work into unobserved tools. A budget exhausted early can reflect a wildly successful product, an unrealistic initial allocation, or uncontrolled retry loops. Conversely, staying within budget can result from discouraging valuable use.

Unit prices may fall while total spending rises because contexts, users, and agent autonomy grow. Security rates may fall while maximum possible loss rises because tools receive stronger permissions. Average cost can hide a few runaway workflows, and average incident severity can hide a catastrophic tail.

These alternatives are not excuses for inaction. They are why management needs cohort-level denominators, distributions, and named owners before turning an anecdote into policy.

## Evidence judgment

- **Retreat multipliers:** unverified and not generalizable from the material available.
- **Cost-control concern:** low-to-moderate confidence; several broad-AI surveys point toward weak visibility and overruns, but all have important scope and method limits.
- **Security trend:** unknown. No audited independent incidence dataset with consistent definitions and exposure was found.
- **Control mechanisms:** moderate practice confidence that access, logging, provenance, testing, scanning, and monitored release address plausible failure paths; outcome effectiveness was not measured here.
- **Unresolved question:** which exposure unit and incident taxonomy allow meaningful cross-organization comparison without encouraging under-reporting?

The responsible response to a shocking multiplier is a measurement upgrade. Preserve the story as a lead, name its limitations, and build the ledger that can tell volume growth from price change, better detection from greater risk, and useful adoption from uncontrolled operation.

Podcast hook: A board hears that incidents rose twentyfold and the annual token budget vanished by spring. The investigation begins with the missing denominators—and discovers four very different possible stories.

Continue reading: [Chapter 25a, “Manage the story, not just the metric”](25a-management-story.md), explains how to govern such warning narratives; Chapter 31a turns the spend ledger into an accountability cadence.
