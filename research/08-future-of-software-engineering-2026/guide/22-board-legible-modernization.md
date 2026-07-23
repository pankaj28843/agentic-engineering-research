# 22. Make modernization legible to the board

Scoping AI investment against an existing maintenance burden can improve capital allocation, but only if the framing exposes the full transition and outcome ledger. A maintenance-budget denominator makes a proposal easier to discuss; it does not make the proposed savings real.

The [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) says maintenance often consumes 30–50% of large-enterprise IT spend and describes an anonymous case in which a vague request above $100 million became an $8 million proposal for 20% of systems. The audited source set did not locate a primary budget, organization, system inventory, or outcome report behind those figures. They remain anonymous retreat claims, not benchmarks.

What survives scrutiny is the framing mechanism: move the conversation from “fund AI” to “fund a bounded change in a named system population, with a baseline, gates, accountable owners, and measurable value.”

## A plain-language model: denominator, funnel, ledger

A board-legible modernization proposal needs three connected views.

**The denominator** defines the estate. How many systems, users, transactions, operating costs, incidents, and regulatory obligations are in scope? “Twenty percent” is meaningless until the selection rule and value share are known. Twenty percent of applications could represent 2% or 80% of business criticality.

**The funnel** shows why candidates move from discovery to experiment, migration, and retirement. Every stage has an exit criterion and a stop option. This prevents a promising pilot from silently becoming a portfolio mandate.

**The ledger** records all material costs and benefits over time. One-time discovery and migration costs sit beside recurring licenses, inference, support, and observability. Transition costs include dual running, data reconciliation, training, and temporary productivity loss. Benefits appear only when a cost is removed, an outcome improves, or an avoided risk has an agreed valuation.

The model makes AI an instrument within modernization, not the investment thesis itself.

## What the available economic evidence can and cannot say

[McKinsey’s modernization account](https://www.mckinsey.com/capabilities/quantumblack/our-insights/ai-for-it-modernization-faster-cheaper-and-better) describes programs in which generative AI was associated with large estimated reductions in time or cost, including an anonymous transformation initially priced above $100 million. It also offers a useful cost taxonomy: recurring run costs, one-time program costs, transition costs, and the break-even point. But it is consultancy evidence built from anonymous cases without raw data, counterfactuals, quality outcomes, or enough detail to reproduce the estimates. It supports the accounting questions, not the advertised percentage as a planning prior.

The same source warns that simple “code and load” migration can transfer technical debt rather than remove it. That matters financially. A program can appear successful at cutover while its old run cost, fragile operating model, or defect burden survives in a new platform. A board that funds only conversion may purchase a change of location rather than a reduction in liability.

[Thoughtworks’ COBOL modernization analysis](https://www.thoughtworks.com/insights/articles/claude-code-cobol-modernization-reality) similarly expands the boundary beyond generated code. Discovery, undocumented rules, data movement, integration, synchronization, dual running, cutover, operations, and organizational knowledge are all part of the program. The article reports only leading indicators and says the jury is still out on broad outcomes. As consultancy practice evidence, it cannot estimate a portfolio return, but it is strong counterweight to code-only business cases.

Microsoft’s [agent-assisted modernization account](https://devblogs.microsoft.com/all-things-azure/how-we-use-ai-agents-for-cobol-migration-and-mainframe-modernization/) supplies a concrete selection warning. Bankdata’s estate exceeds 70 million lines, yet not every module is an appropriate transformation candidate; batch behavior, I/O, scheduling, and service-level obligations can require redesign. A portfolio denominator should therefore include candidate classes and exclusions, not imply that every legacy line is equivalent inventory.

Repository evidence reinforces the difference between a green technical signal and realized value. [RepoRescue](https://arxiv.org/html/2607.01213v1) showed that agents could restore compatibility in some Python and Java repositories, especially with full environment feedback. Manual audit of apparently successful unmaintained Python projects still found regressions and failures in realistic scenarios. This is not an economic study, but it demonstrates why technical gates must include scenario audit and why “tests passed” cannot be booked as savings.

Cost visibility is itself immature. A [Channel Dive report on a Flexera survey](https://www.channeldive.com/news/flexera-itam-ai-cost-tracking-tokenmaxxing/823709/) says two-thirds of more than 500 IT asset-management respondents lacked accurate visibility into AI usage, only 36% had a complete asset view, and three-fifths reported increased AI overspend. This is secondary trade-press coverage of all enterprise AI, not a software-modernization sample, and the underlying survey method was not available in the audited material. It cannot validate the retreat’s budget figures. It does show why a proposal that omits metering is not board-legible in operation.

A separate [CFO Dive report](https://www.cfodive.com/news/7-10-firms-report-ai-cost-overruns/825961/) summarizes a vendor survey of 300 US executives: 68% reported at least some AI budget overrun, while only 9% said more than three-quarters of initiatives delivered measurable return. Again, this is secondary, vendor-sponsored, broad-AI evidence with limited sampling detail. It is a warning about measurement and selection, not a modernization base rate.

## How a legible frame can still mislead

Attaching an AI program to a large maintenance pool creates a powerful story: even a small percentage improvement looks valuable. That story has at least six failure modes.

1. **Soft denominator:** “maintenance” may combine essential operations, regulatory work, enhancements, vendor contracts, and deferred renewal. Not all of it is removable waste.
2. **Selected numerator:** the easiest pilot systems may be unrepresentative. Extrapolating their result across the estate ignores dependencies and criticality.
3. **Cost transfer:** cloud, model, data, observability, and specialist-review costs replace rather than eliminate legacy costs.
4. **Double running:** the new system starts costing money before the old one can be retired. A delayed retirement moves break-even sharply.
5. **Quality deferral:** defects, missing behavior, or weakened controls arrive after the declared migration milestone.
6. **Option suppression:** a compelling AI story can crowd out simpler retirement, vendor replacement, interface containment, or policy change.

These are reasoned accounting risks supported by the program-boundary evidence; the audited corpus does not provide their population frequency. Boards should ask for them explicitly rather than pretend there is a universal correction factor.

## The modernization investment canvas

Use this canvas for one candidate cohort before approving a portfolio number.

### 1. Define the estate

- Name systems, owners, users, dependencies, criticality, data classes, and current lifecycle state.
- Report both system count and share of business volume or risk.
- Separate **retire**, **contain**, **replace**, **port**, and **redesign** candidates.
- Record why excluded systems are excluded.

### 2. Establish the counterfactual

- What happens if the organization does nothing for 12, 24, and 36 months?
- What are the non-AI alternatives?
- Which current costs are committed, avoidable, or merely allocated?
- What evidence would cause the team to stop?

### 3. Build the full ledger

- One-time: discovery, data cleanup, tool building, validation, remediation, migration, training, and program management.
- Transition: parallel operation, synchronization, reconciliation, incident buffer, and temporary throughput loss.
- Recurring: models, tokens, licenses, infrastructure, security, observability, support, and specialist ownership.
- Risk: expected defect, security, compliance, vendor, schedule, and knowledge-loss exposure.
- Benefit: retired cost, faster lead time, reduced incident loss, enabled revenue, or avoided end-of-life risk—each with an owner and measurement rule.

### 4. Use gated evidence

For each stage—inventory, representative pilot, shadow operation, cohort migration, retirement—write a pass threshold, failure threshold, maximum exposure, decision owner, and evidence artifact. Keep the pilot cohort visible when reporting results. Do not convert model token cost into total program cost or code-generation time into elapsed migration time.

### 5. Report ranges and realization

Show base, adverse, and favorable cases, including delayed retirement. Track forecast against actual cash, risk, and outcomes at each gate. A benefit is “realized” only when the named cost disappears or the named operational outcome changes. Update the business case rather than protecting its opening story.

## Evidence judgment

- **Confidence in the framing:** moderate. A bounded estate, explicit alternatives, staged gates, and a full lifecycle ledger improve accountability by making assumptions inspectable.
- **Confidence in the retreat’s quantities:** low. The 30–50%, $100 million-plus, $8 million, and 20% figures have no auditable primary provenance in the captured evidence.
- **Confidence in large modernization savings:** low to moderate for particular cases, low as a transferable prior. Consultancy cases indicate possibility but lack independent baselines and outcome data.
- **Main counterevidence:** code conversion can preserve debt; candidate modules are selective; passing tests can hide scenario failures; AI cost visibility is often weak.
- **Unresolved question:** which cohort-level measures best predict actual legacy retirement and sustained operating-cost reduction after the parallel-run period?

Board legibility is not a prettier slide. It is the ability to trace a decision from estate denominator, through selection and gates, to cash, risk, and realized outcomes. Scoping against maintenance spend helps only when it makes that chain harder—not easier—to hand-wave.

Podcast hook: The board approves an $8 million modernization story; the detective work begins by asking what “20% of systems” actually contains and which old bill will disappear.

Continue reading: [Chapter 23, “Stories, benchmarks, and executive learning”](23-stories-benchmarks-executive-learning.md), examines how leaders should interpret evidence; [Chapter 20](20-port-first-improve-second.md) owns the migration-sequence claim.
