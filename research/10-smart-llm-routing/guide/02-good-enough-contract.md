# 2. Good Enough Is a Contract

## ELI5 hook

A courier company does not grade every parcel with one question called
“quality.” A birthday card, a refrigerator, and a prescription have different
acceptable conditions. The card may need to arrive today. The refrigerator
must arrive upright and undamaged. The prescription needs identity and chain
of-custody checks. A route is good only when it meets the contract for the
parcel in front of it.

LLM quality works the same way. A global model leaderboard is a useful signal,
but it cannot replace the acceptance contract for a particular workload. A
short summary, a policy answer, a code patch, and a tool proposal have
different failure costs. “Good enough” must name the task, the consequence,
the evidence, the allowed uncertainty, and the decision that follows a miss.

## Mechanism: capability, quality, preference

Build a request vector before choosing a model:

```text
workload class, consequence, sensitivity, residency
context length and freshness, language, tool/schema needs
deadline and latency budget, acceptance test, retry/escalation budget
```

Use three separate words:

- **Capability** means the route contract says the worker can attempt the task:
  it supports the required context shape, language, output schema, tools,
  region, and authority boundary. Capability is an eligibility question.
- **Quality** means an instance of the route is likely to pass the acceptance
  test for this stratum. Quality is an empirical probability or a measured
  score with uncertainty, not a model's self-confidence.
- **Preference** chooses among eligible routes that meet the quality floor,
  balancing cost, latency, capacity, and user experience.

Confusing the three creates unsafe policies. A cheap route may be capable of
producing JSON but poor at preserving a legal exception. A benchmark may show
high average quality while a protected multilingual stratum fails. A route
may be preferred because it is cheap only after hard gates and quality floors
have been applied.

Create strata that change the decision. Useful dimensions include consequence,
data class, language, context length, tool use, freshness, and whether a human
can cheaply review the result. Avoid a taxonomy so fine that no stratum has
enough observations to calibrate. Record an explicit `abstain` label: the
system did not have enough evidence to accept or safely escalate.

Acceptance can combine deterministic and human signals:

```text
accepted = schema_valid
        ∧ required_evidence_present
        ∧ domain_invariants_pass
        ∧ policy_and_authority_pass
        ∧ human_approval_if_required
```

An LLM judge may assist with a semantic rubric, but the judge is another
measurement instrument that needs calibration and holdouts. [Mastra's agent
evaluation discussion](https://mastra.ai/articles/ai-agent-evaluation) is a
practitioner source for making evaluation an explicit engineering surface.
[SWE-bench](https://www.swebench.com/) and the [Aider leaderboard](https://aider.chat/docs/leaderboards/)
show why a coding benchmark must be read with its task and scoring context;
they are not a universal ordering for every coding journey.

## Worked example: three request strata

These labels are **illustrative**. A generic enterprise has a document-help
assistant with three strata.

| Stratum | Contract | Allowed route set | Pass, abstain, fail |
|---|---|---|---|
| Routine summary | preserve named facts, cite the supplied document, no external action | deterministic extract; efficient readonly; capable readonly | pass when fields and citation checks hold; abstain when source is incomplete; fail on invented facts |
| Multilingual policy lookup | answer in requested language, preserve exception and effective date, identify missing jurisdiction | efficient readonly; capable readonly; human review on high consequence | pass with evidence and exception checks; abstain on conflicting sources; fail on unsupported certainty |
| Account-state proposal | normalize an intended change, list impact, never execute without approval | capable proposal route only; deterministic tool and human gate | pass only when schema, auth, exact digest, and approval hold; otherwise blocked or denied |

The third row is not “harder text” alone. It has a different authority contract.
The route set is narrowed before any model-mediated complexity estimate. A
model can propose a normalized action, but deterministic code checks tenant,
actor, resource, policy, and approval. The model never becomes the authority
because it received a high score.

For a small evaluation sample, collect a result per request rather than one
average. Suppose the routine stratum has 60 examples, multilingual has 25,
and proposals have 15. The policy might require at least 95% acceptance for
routine summaries, 90% for multilingual lookup with an abstention ceiling,
and zero unauthorized side effects for proposals. These are **proposed example
floors**, not universal targets. A lower-consequence route cannot compensate
for an authority failure in a higher-consequence stratum.

## Failure drill: the hidden denominator

The monthly report says acceptance rose from 88% to 91%. Investigation shows
that the router began abstaining on long multilingual requests and returning
“please contact support.” Routine summaries improved, so the aggregate looked
better. The protected stratum lost access and its denominator shrank.

Repair the report by publishing, per stratum: traffic volume, attempted count,
accepted count, abstained count, failed count, escalations, human rework,
latency tails, and route mix. Set a minimum traffic and acceptance floor for
each protected stratum. If a stratum is too small for a reliable estimate,
label it unknown and keep the safer route. Do not let a global score hide a
local regression.

The same discipline applies to model capabilities. A provider page can
document a feature; it cannot prove the feature behaves correctly with this
prompt, region, tenant, or tool contract. Current provider pages in the [source
index](../source-index.md) are evidence for documented facts, while the
acceptance taxonomy remains an enterprise proposal to be measured.

## Reader exercises

1. Choose one workflow and write a five-line acceptance rubric. Include one
   deterministic invariant, one evidence requirement, one abstention rule,
   and one human boundary.
2. Make a four-by-four matrix with consequence on one axis and uncertainty on
   the other. Put a route set in every cell and explain why the cells differ.
3. Mark each label in your rubric as deterministic, human-calibrated, judge-
   assisted, or unmeasured. Remove any route choice that depends on an
   unmeasured label.
4. Split one aggregate quality metric into three strata. Identify the hidden
   denominator that would make an improvement misleading.

## Calibrating the contract over time

An acceptance contract is a measurement instrument, and instruments drift.
New document templates change what “preserve the named facts” means. A policy
owner may tighten an exception. A language mix may change after a product
launch. A judge may become more generous after a rubric rewrite. Version the
rubric and the dataset together so an apparent quality change has a traceable
cause.

Keep a small calibration set with examples at the boundaries: answers that
barely pass, answers that are fluent but wrong, incomplete evidence, conflicting
jurisdictions, and requests that must abstain. Have domain reviewers label the
set independently, discuss disagreements, and freeze the adjudicated result.
Use it to check deterministic validators and semantic judges before a route
policy changes. Do not silently relabel old outcomes because the new route
would otherwise look worse.

The contract should specify what happens after a miss. A routine summary might
permit one no-side-effect repair. A restricted policy lookup might require a
human review. A high-consequence proposal might be blocked until an owner
clarifies scope. “Try a stronger model” is one possible transition, not the
definition of quality. The transition itself consumes budget and can increase
exposure, so it belongs in the acceptance map.

A useful quality table includes more than a pass percentage:

| Field | Why it matters |
|---|---|
| attempted | reveals whether the policy avoided hard cases by abstaining |
| accepted | supplies the business numerator |
| abstained or blocked | exposes uncertainty and policy coverage |
| false acceptance | measures unsafe or wrong work that slipped through |
| false rejection | measures useful work sent to repair or humans |
| review time | connects quality to accepted-outcome economics |
| slice and version | makes the result reproducible |

Calibrate thresholds on future-like examples. If reviewers label only the
answers shown to users, the dataset misses requests blocked before generation.
Sample those requests deliberately. If one route receives more human review,
its quality estimate may look worse simply because its uncertain cases were
examined. Report review intensity and label source alongside the score.

The contract can improve without becoming vague. A change from “answer the
question” to “answer using the current approved source, cite the section, and
name uncertainty when two sources conflict” is more testable. A change from
“high quality” to “the capable model feels better” is less testable. Every
route choice should point to the clause it is expected to satisfy.

## Acceptance is an outcome, not a tone

Readers often begin with a style rubric because style is visible. Add outcome
evidence beside it. A summary is accepted when the named facts survive and the
source is current. A policy lookup is accepted when the exception and date are
preserved. A proposal is accepted only when a trusted system confirms scope
and a human or approved policy authorizes the exact action. Pleasant prose is
one feature of the experience, not its completion condition.

Write abstention as a product behavior. It may ask for a missing document,
show a qualified uncertainty statement, or transfer to a human. Measure the
user's completion after that transfer. If an abstention is always counted as
a failure, the router may learn to overstate certainty; if it is always
counted as success, the product may stop serving the hard cases. The contract
must say which outcome the user can rely on.

Review the taxonomy with domain owners before training a router. A technical
team can detect malformed fields but may miss a jurisdictional exception. A
domain reviewer can label the exception but may not know whether the route
actually had the required source. Keep both evidence types in the record.

## Checkpoint

Before assigning a route, ask whether the contract can distinguish a pass from
a polished miss. If it cannot, the quality estimate is not ready to guide
cost optimization. Make the smallest useful taxonomy, collect boundary cases,
and state who adjudicates disagreement. A quality floor is meaningful only
when coverage and abstention remain visible. The reader's artifact at this
point is a strata matrix that a domain owner can sign and an evaluator can
replay.

## Source slot

Use [RouteLLM](https://arxiv.org/html/2406.18665) and the routing papers in
[the source catalog](../sources.json) for bounded model-selection evidence.
Use [Mastra's evaluation article](https://mastra.ai/articles/ai-agent-evaluation),
[SWE-bench](https://www.swebench.com/), and [Aider](https://aider.chat/docs/leaderboards/)
for task-specific evaluation context. The chapter's floors, labels, and route
envelopes are proposals; they become claims only after a stratified dataset,
calibrated rubric, and replay evidence exist.
