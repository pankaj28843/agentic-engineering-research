# Why Legacy Modernization May Be the Near-Term Value Pool

Greenfield software starts with freedom and uncertainty. Legacy software starts with constraints and evidence. Its code may be difficult, but it often comes with years of behavior, production traffic, batch schedules, support tickets, user habits, and known failure modes. Those artifacts can make a narrow modernization task unusually suitable for agents: the destination is uncertain, but parts of the current system are observable.

That is the case for legacy modernization as a near-term value pool. It is a **selection argument**, not a claim that agents can autonomously replace mainframes. The most defensible opportunities are bounded work in which:

- understanding the existing system is expensive;
- a useful intermediate artifact is easy to name;
- deterministic tools or historical environments can constrain the agent;
- a domain expert can evaluate omissions;
- the organization captures value before a full replacement succeeds.

The [2026 Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) goes further, presenting legacy modernization as a potentially large value pool and including vivid anonymous demonstrations and economics. The report is **retreat synthesis**, not an attributable project record. The audited corpus does not validate the anonymous compiler timelines, cost, suite claims, maintenance-spend range, or portfolio savings. The narrower opportunity survives without them.

## Why legacy can be more constrained than greenfield

“Legacy” does not mean merely old source code. It is a running socio-technical system:

```text
code + data + jobs + integrations + infrastructure
     + operating procedures + tacit rules + users + regulation
```

That complexity makes wholesale migration dangerous. It also creates evidence unavailable to a new product. Existing behavior can be observed, dependencies can be mapped, and proposed artifacts can be compared with a known system. In a greenfield product, an agent can generate quickly while the organization is still discovering what should exist. In a legacy system, some intent is encoded—imperfectly—in what already exists.

This yields a useful asymmetry:

- **Greenfield advantage:** fewer inherited constraints and more design freedom.
- **Legacy advantage:** more observable behavior, accumulated knowledge, and concrete discovery work.
- **Legacy liability:** hidden coupling, obsolete behavior, weak tests, scarce environments, and high consequence of error.

The opportunity is strongest where the advantage is accessible and the liability is bounded. A functioning historical system can be an oracle for selected behavior; it is never a complete specification of what the future system ought to preserve.

## What current practice evidence supports

Thoughtworks practitioners responding to public COBOL claims describe codebase mapping as repeated preprocessing, chunking, local summarization, relationship extraction, and higher-level synthesis, combined with static and dynamic analysis and human interpretation ([“Claude Code and COBOL modernization: What's the reality?”](https://www.thoughtworks.com/insights/articles/claude-code-cobol-modernization-reality)). They identify discovery, planning, tacit constraints, data synchronization, possible dual running, and cutover as separate parts of modernization.

This is **firsthand consultancy practice evidence** and a useful system boundary. The authors explicitly say they have leading indicators rather than final replacement outcomes and that the jury remains out. The source supports “AI can assist costly discovery under scaffolding,” not “AI has made large modernization cheap.”

Microsoft's public work with Bankdata provides a second bounded account. Bankdata has more than 70 million lines of mainframe code, but the authors say only some modules are good replatforming candidates. Their early experiments produced educated guesses and hallucinated output; a small donated module and a two-day hack informed an agentic migration prototype. Excessive context reduced coherence, call-chain mapping reached depth three but not farther, and deterministic tests were described as crucial ([Microsoft DevBlogs](https://devblogs.microsoft.com/all-things-azure/how-we-use-ai-agents-for-cobol-migration-and-mainframe-modernization/)).

This is **vendor-and-collaborator prototype evidence**. It exposes constraints—batch throughput, I/O, JCL orchestration, service levels, context depth—and an inspectable repository lead. It reports no completed enterprise migration, production equivalence, cost, defect rate, or ROI. Its most valuable result may be candidate selection: a large codebase does not imply every module should move.

## Value before replacement

The near-term value pool contains outputs that are useful even if a replacement is postponed:

1. **System inventory and dependency maps.** Locate programs, data stores, job flows, interfaces, and ownership gaps.
2. **Retro-documentation.** Produce reviewable explanations of business terms and control flow.
3. **Business-rule candidates.** Extract rules for domain experts to confirm, reject, and annotate.
4. **Test and environment recovery.** Reconstruct historical builds and expose the behavior a future change must consider.
5. **Compatibility repair.** Adapt bounded components to a modern runtime without redesigning the whole system.
6. **Migration triage.** Identify modules that should remain, wrap, replatform, replace, or retire.

Each item has an independent beneficiary. Operators can use a dependency map; auditors can inspect rule candidates; maintainers can use recovered environments. That gives the work option value: the organization learns before making an irreversible program commitment.

One industrial case makes the boundary concrete. A 2026 ACM workshop paper describes LLM-assisted retro-documentation across five BNP Paribas applications ([paper](https://dl.acm.org/doi/full/10.1145/3786170.3788390)). Its orchestrated pipelines increased a paper-defined functional-vocabulary measure while reported fidelity ranged from 0.74 to 0.95; greater abstraction could reduce fidelity and propagate errors. Evaluation relied largely on an LLM judge with expert review of a curated subset.

This is **single-institution documentation evidence**, not migration evidence. It shows that useful semantic extraction can be evaluated as its own product and that “more business language” can trade off against faithfulness. It does not establish behavioral equivalence, durable savings, or broad expert validation.

## Repository rescue is promising—and narrower than modernization

[RepoRescue](https://arxiv.org/html/2607.01213v1) studied compatibility repair across 193 Python and 122 Java repositories. It recovered a historical environment in which each admitted repository's tests passed, demonstrated failure in a modern environment, and asked agent systems to repair the break. Full-tool Python success for several systems ranged from 36.8% to 51.3%; a five-system union reached 62.7%.

The audit behind the headline is more instructive. Stripping test edits materially reduced apparent success for several systems. Among 34 apparently successful unmaintained-Python rescues, only 22 passed realistic-use scenarios, and only 12 both addressed the compatibility failure and showed no observed regression in targeted bug hunting.

This is **whole-repository benchmark evidence** that environment access enables real bounded repairs and that green tests overstate practical success. It is one trial per condition, uses existing test surfaces, mixes model and framework effects, and studies compatibility rescue—not language replacement, data migration, operations, or business transformation.

The study nevertheless reveals why legacy can be attractive: the historical and modern environments create a before-and-after question that can be executed. A greenfield “is this the right product?” question rarely has such an oracle.

## When legacy is the wrong value pool

The argument fails under several conditions:

- the old behavior is harmful, insecure, illegal, or strategically obsolete;
- the system cannot be reproduced or observed well enough to compare behavior;
- modernization requires synchronized change across data, organization, regulation, and business process;
- the scarce expert becomes a permanent reviewer bottleneck;
- discovery artifacts are not maintained and become a second stale system;
- a vendor's demo drives a rewrite before module-level value is demonstrated;
- the apparent savings exclude dual operation, data reconciliation, incident risk, and decommissioning.

These are **risk mechanisms and practitioner constraints**, not frequency estimates. They explain why a constrained value thesis must include exit conditions.

Community practitioners discussing COBOL repeatedly distinguish source syntax from JCL, databases, interfaces, compliance, operational knowledge, and dialects ([Hacker News discussion](https://news.ycombinator.com/item?id=46678550)). This is **non-representative social evidence**: useful for discovering constraints and conflicting experiences, useless for estimating prevalence or ROI. Some contributors report more value in explanation and rule extraction than autonomous migration, which is consistent with the bounded value pool but does not validate it.

## Exercise: score a modernization wedge

Pick one proposed legacy use case. Score each dimension from 0 to 3:

| Dimension | 0 | 3 |
|---|---|---|
| Bounded output | “Modernize the system” | one named artifact or behavior |
| Observable baseline | behavior cannot be reproduced | stable historical evidence exists |
| Independent checks | agent grades itself | deterministic and expert checks differ from generator |
| Expert availability | no accountable domain owner | reviewer owns semantics and exceptions |
| Intermediate value | only pays after full cutover | artifact is useful immediately |
| Reversibility | early work commits architecture/cutover | work can be discarded or redirected |
| Data/operation scope | opaque, cross-system, regulated | constrained and reproducible |
| Maintenance path | no owner after pilot | artifact and harness have owners |

Do not treat the total as scientific. Use it to expose disagreement. Any zero in observable baseline, expert availability, or intermediate value is a reason to shrink the wedge before funding a large program.

Then define a six-week learning contract:

- one artifact, such as a dependency map for one job family;
- one named consumer who will use it;
- a blinded or independent sample review;
- omission and false-relationship measures;
- human and compute cost;
- a maintenance test two weeks later;
- a stop rule if verification consumes more than the artifact's likely value.

Compare the wedge with a non-AI alternative: conventional static analysis, manual sampling, a purchased tool, or doing nothing. “Agent versus no agent” is not the only decision.

## The defensible value thesis

No audited source demonstrates safe autonomous modernization of a large production mainframe with complete functional and non-functional equivalence. No source establishes durable portfolio ROI. The case that remains is still substantial:

> Agents may create near-term value in legacy estates by lowering the cost of bounded discovery, documentation, test assistance, environment-backed repair, and candidate triage—especially when existing behavior supplies observable constraints and each output has value before full replacement.

That is more conservative than a compiler demo and more useful to a portfolio owner. It turns “modernize everything” into a queue of falsifiable, reversible value wedges.

Podcast hook: What if legacy code is not the worst place for agents, but the best—because the old system leaves behind an executable trail of what “right” used to mean?

Continue reading: [Management interlude — Sequence Discipline Before Scale](05a-management-sequence-discipline.md).
