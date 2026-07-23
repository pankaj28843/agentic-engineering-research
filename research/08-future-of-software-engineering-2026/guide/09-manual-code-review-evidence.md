# 09. Does manual code review work?

> **Report point:** Verification, bullet 09, page 4 of the [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
> **Evidence judgment:** Human review can surface consequential concerns, but its causal effect, ideal scope, and advantage over agent review remain unmeasured.

The retreat discussion reached an uncomfortable question: if nobody in the room could immediately cite evidence that manual code review works, why preserve it as a default? That is a good challenge. It is not, by itself, evidence that review is useless.

The audited literature supports a bounded answer. Human review has found security concerns in real projects, and some review characteristics are associated with later software quality. But reviewing a change does not guarantee that a concern is correct, fixed, or even acted on. Historical studies do not tell us whether a present-day human, an agent, a hybrid pair, or a stronger automated check is the best reviewer for a given change.

The useful question is therefore not “review or no review?” It is: **which failure are we trying to catch, what independent signal could catch it, and what happens after the signal fires?**

## A plain-language model: detection is only one link

Think of review as a five-link chain:

```text
change → inspection → concern → decision → verified resolution
```

Each link can fail. A reviewer can miss a defect. A comment can identify a preference rather than a defect. A valid concern can be ignored. A proposed fix can be wrong. The corrected patch can introduce another fault.

That is why “the pull request was reviewed” is a process fact, not a quality outcome. Review can also perform functions that defect counts do not capture: communicating intent, challenging architecture, enforcing policy, spreading knowledge, and assigning accountability. Those outcomes must be named separately. A study about security comments cannot establish knowledge transfer; a survey about confidence cannot establish fewer production defects.

Automated checks have their own boundary. A type checker, property test, security scanner, or proof tool can examine more cases consistently than a tired person, but only within its encoded model. A human may notice a mistaken requirement or dangerous interaction outside that model. Conversely, a human rereading routine formatting or dependency rules is often a weak and expensive substitute for deterministic automation.

## What direct evidence survives the audit

The clearest recent study in this packet examined security-related review concerns in OpenSSL and PHP. [Charoenwet and colleagues](https://link.springer.com/article/10.1007/s10664-024-10496-y) mapped 135,560 review comments toward 40 weakness categories and manually coded 6,146 comments. Their final data included 188 concerns in 164 OpenSSL pull requests and 123 concerns in 100 PHP pull requests. Fixes were attempted for only 39% and 41% of concerns, and the authors classified 37% as successfully resolved in each project. Some changes with unresolved concerns were still merged.

This establishes something important but narrow: human review in two mature C/C++ projects surfaced security-relevant concerns, yet detection did not ensure resolution. The comments were concerns, not a gold-standard set of confirmed vulnerabilities, and the design does not reveal what would have happened without review. It cannot give us a “review effectiveness percentage” or show that a person beat an agent.

An older observational study connects review practice to later defects. [McIntosh and colleagues](https://rebels.cs.uwaterloo.ca/papers/emse2016_mcintosh.pdf) modeled post-release defect fixes for Qt 5.0, Qt 5.1, VTK 5.10, and ITK 4.3. Review coverage was high in three releases—about 96% to 98%—but near-complete coverage did not eliminate defect-prone components. Coverage was a statistically significant predictor in only two of the four systems; participation and expertise also varied in their associations.

That inconsistency is a result, not an inconvenience. It suggests that the existence of a review gate is too coarse a variable. Who participates, what they inspect, the size and comprehensibility of the change, available automation, and project context may matter. The study used historical open-source releases and component-level observational models. It does not identify the causal benefit of adding review, nor does it transfer automatically to agent-generated patches in 2026.

Together, the two studies support three restrained claims:

- review can expose issues that matter;
- review coverage alone is not a sufficient quality guarantee;
- finding a concern and producing a verified correction are different outcomes.

They do not establish mandatory review of every change as the optimal policy.

## The displacement claim has not been tested

A 2026 position paper argues that coding agents will supersede human reviewers. [*The End of Code Review*](https://arxiv.org/html/2606.13175v1) is useful because it states the provocative hypothesis plainly. It offers no new matched experiment: no common change set reviewed by humans and agents, no hidden-fault outcome, no downstream defect window, and no total-cost comparison. Its premises also acknowledge prompt injection, correlated blind spots, architecture, accountability, and high-risk oversight.

Capability on repair benchmarks is not a review comparison. An agent that can solve a task after being told a failure is present has not thereby shown that it can discover unknown faults in an ordinary change. Likewise, an agent-generated review comment is not an outcome unless its correctness, novelty, actionability, and resolution are assessed.

Practitioner reports of review pressure are leads, not effect estimates. The [Stack Overflow account of decision fatigue](https://stackoverflow.blog/2026/05/21/coding-agents-are-giving-everyone-decision-fatigue/) describes higher code output and substantial reviewer effort, but provides no matched baseline or defect data. The [Hacker News discussion of an agent-first project](https://news.ycombinator.com/item?id=48416264) reports extensive human steering and discarded runs. Both make review cost worth measuring. Neither proves that the cost is wasted or that agent review would remove it.

## Separate four review outcomes

A credible comparison should keep at least four outcomes apart:

1. **Detection:** Did the reviewer identify a real, previously unknown problem?
2. **Resolution:** Was the problem corrected without introducing another one?
3. **Prevention:** Did the process reduce later incidents, defects, or rework?
4. **Coordination:** Did relevant people gain the explanation or authority needed to operate the result?

Comment count is not detection. Acceptance rate is not correctness. Time to merge is not prevention. Attendance is not learning.

The comparator also matters. A human review might look weak against a property test targeted at a known invariant and strong against a generic language-model critique. Pairing during design could prevent an error before a pull request exists. Mutation testing might expose a weak test suite more reliably than another pass over the diff. The right study compares plausible alternatives for the same failure class, rather than treating “review” as one indivisible intervention.

## When manual review is a poor default

Manual review is especially questionable when a deterministic rule already exists. Formatting, forbidden imports, dependency direction, schema compatibility, generated-file drift, and many security policies belong in executable checks. Asking people to catch these repeatedly creates inconsistent enforcement and consumes attention that could be used on intent and risk.

Huge diffs are another weak setting. Neither a human nor a model can preserve reliable context indefinitely. Splitting the change, generating semantic summaries, testing contracts, or reviewing the design before generation may improve the inspection problem more than adding reviewers.

Low-risk and reversible changes may not justify synchronous human approval if independent checks and rapid rollback are strong. At the other extreme, a high-risk change should not depend on an unaided generalist reading a diff. It may need domain experts, explicit threat analysis, formalized invariants, staged exposure, and operational observation.

The counterexample cuts both ways: replacing all human review with an agent merely changes the reviewer. If the generator and reviewer share training, prompts, assumptions, or context, they can miss the same defect. Multiple fluent comments do not create an independent oracle.

## Exercise: build a review outcome ledger

For the next 20 nontrivial changes, record a small ledger. Do not use it to rank individuals.

| Field | Question |
|---|---|
| Risk class | What harm could this change cause, and how reversible is it? |
| Concern source | Human, agent, static check, test, incident history, or other? |
| Concern class | Correctness, security, operability, architecture, policy, or style? |
| Validity | Was the concern confirmed, rejected, or left uncertain? |
| Novelty | Would another existing check already have caught it? |
| Resolution | Was it fixed, accepted as risk, deferred, or ignored? |
| Verification | What independent evidence showed the resolution worked? |
| Downstream result | Rework, escaped defect, incident, or no observed problem? |
| Effort | Reviewer time, author time, tool cost, and waiting time? |

After 20 changes, look for a migration opportunity. Repeated deterministic findings should become automation. High-value domain concerns should shape reviewer assignment or earlier design work. Low-yield, high-effort gates should be narrowed experimentally—not removed on intuition alone. Keep a holdout or staged comparison so that fewer comments do not masquerade as better quality.

[Chapter 39](39-measure-code-review.md) develops the measurement design and Goodhart safeguards. This chapter’s conclusion is deliberately prior to that playbook: the current evidence warrants selective, outcome-oriented review, not faith in a ceremony and not faith in its abolition.

## What survives skeptical review

Manual code review has bounded empirical value: it can surface consequential concerns and its participation patterns can relate to software quality. The same evidence shows incomplete follow-through, inconsistent associations, and residual defects despite broad coverage.

No audited source establishes a current causal advantage for human review over agent review, or the reverse. Until comparable outcome data exists, allocate review by risk and failure mode, automate deterministic checks, and measure the entire path from concern to verified resolution.

Podcast hook: A reviewer found the flaw—but the patch still shipped. At which link did “code review works” stop being true?

Continue reading: [Chapter 39: Measure code review](39-measure-code-review.md) turns detection, resolution, prevention, coordination, and cost into a practical comparison.
