# 6. Router Families: Rules, Predictors, and Bounded Learning

## ELI5 hook

A taxi dispatcher can use a rule (“wheelchair trips go to vans”), a weather
forecast (“send more cars before the rain”), a learned estimate (“this street
usually takes twelve minutes”), or an experiment (“try a new neighborhood and
see”). These tools answer different questions. None should be allowed to
ignore a passenger's destination, accessibility requirement, or payment
authority.

LLM router families differ in the same way. The algorithm can estimate
difficulty or preference inside an eligible route set. It must not become the
authority that defines eligibility. Start with the least complex family that
can satisfy the measured requirement.

## Mechanism: what each family knows

**Rules** use explicit features and thresholds: task type, context length,
language, consequence, time of day, or queue state. They are easy to audit and
often strong when the workload has clear categories. Their weakness is brittle
boundaries and maintenance when the distribution changes.

**Complexity classifiers** predict a task stratum or a route class from the
request envelope and redacted content. They are useful when a human-readable
rule cannot express the boundary. The output must be a fixed enum. Training
labels inherit the mistakes and selection effects of the policy that collected
them. Permit an explicit abstain result when the evidence cannot support a
choice; the deterministic decoder must reject any enum outside the eligible set.

**Per-route quality/cost predictors** estimate whether a candidate will pass,
how much work it will consume, or how long it will take. They can support a
Pareto choice, but the prediction interval matters. A small apparent cost
difference is not a reason to switch when the quality estimate is uncertain.

**Pairwise preference routers** learn which of two endpoints is more likely to
win for a prompt. Research systems such as [RouteLLM](https://arxiv.org/html/2406.18665)
make this pattern concrete on preference data. The measured question is
whether that preference signal transfers to the enterprise acceptance rubric,
price snapshot, and context construction.

**Contextual bandits** trade exploration for exploitation. They can learn
changing route performance, but exploration consumes budget and can expose
users to lower-quality routes. Exploration must be bounded, logged, and
restricted to candidates already permitted by `R1`. Offline policy evaluation
and a holdout reduce, but do not eliminate, counterfactual uncertainty.

In the proposed safe starting scope, exploration belongs only in approved
readonly lanes. The classification call itself must also be eligible: sending
restricted features to an unapproved region breaches the boundary before any
worker is selected. A bandit's desire for information never qualifies an
undeclared provider.

**Hybrid policies** often work best: deterministic hard rules, a small
classifier for an uncertain stratum, and a deterministic scorer. The more
adaptive the family, the more important signed policy versions, drift alarms,
label review, and rollback become. A route policy also changes the labels it
will later learn from: easy requests may be overrepresented in the cheap lane,
while hard requests are escalated and receive more human attention.

## Worked example: three months of changing traffic

Consider an **illustrative** multilingual support queue. In month one, 70% of
requests are short, one-language summaries; 20% are policy lookups; 10% are
long mixed-language cases. A rule routes by context length and language. It
meets the proposed acceptance floor for the first two groups but abstains on
the long tail.

In month two, a product launch makes mixed-language requests 35% of traffic.
A supervised classifier trained on month one routes many of them to the
efficient model because length and language tokens look familiar. Acceptance
falls in the long-tail stratum. The right correction is not to let the
classifier choose a new provider. Add held-out month-two examples, a feature
for evidence ambiguity if it is trusted, an abstention threshold, and a
minimum acceptance floor. Keep the rule-based safety envelope.

In month three, the enterprise runs a small bandit experiment among two
already-approved readonly routes for low-consequence requests. Ten percent of
eligible traffic is exploration; high-consequence and residency-restricted
requests are excluded. The bandit cannot change the route set, budget ceiling,
or authority. Its reward is cost per accepted outcome with an acceptance-rate
floor, not raw thumbs-up or token savings. A separate holdout evaluates whether
the observed improvement survives the route policy's own feedback loop.

The point is not that the bandit is superior. The point is that each family
has a different information requirement and risk. A rule may beat a learned
router when the category is legible and labels are sparse. A learned family
may be useful only where its extra information changes the Pareto choice.

For this illustrative queue, evidence ambiguity is useful only if it predicts
whether the efficient route will preserve the policy exception and changes a
measured choice. Compare the resulting route mix and accepted outcomes against
the original language-and-context-length rule on held-out requests. A longer
explanation for an unchanged choice buys no demonstrated routing benefit.

## Failure drill: learning from its own blind spot

In this illustrative failure drill, the classifier sends uncertain cases to
the cheapest route. Those cases get
fewer human labels because the product displays a generic answer and users
leave. The training set now contains confident cheap-route outcomes, not the
hard cases that should define the boundary. Offline accuracy rises while real
quality falls.

Break the loop with a fixed holdout, stratified sampling, explicit exploration
within safe lanes, and human labels on abstentions and escalations. Track the
coverage of every stratum. Compare the learned policy to a content-free fixed
baseline. If the policy cannot estimate quality for a protected stratum, keep
the deterministic or capable route. Route learning is optional; the policy
boundary is not.

The [OpenAI harness engineering account](https://openai.com/index/harness-engineering/)
and [Martin Fowler's independent discussion](https://martinfowler.com/articles/harness-engineering.html)
are useful for a related lesson: the environment, repository context, and
feedback surface shape agent performance. A router trained around one harness
or context construction should not be treated as a provider-neutral law.

Treat that environment as part of the qualified route: retrieval corpus,
context builder, region, cache scope, output schema, tool permission,
validator, feedback loop, and acceptance rubric. Changing one can make the old
quality estimate inapplicable even if the model pin is unchanged. Re-evaluate
the affected contract rather than assuming the predictor learned a permanent
property of the model.

## Reader exercises

1. Pick three workloads and select rules, a classifier, a predictor, or a
   bounded bandit for each. Explain what new information the choice buys.
2. Design an exploration budget that cannot broaden policy eligibility. State
   which strata are excluded and what stops the experiment.
3. Draw the label-feedback loop from route choice to outcome to training set.
   Mark where selection bias, judge bias, and missing human labels enter.
4. Define a drift alarm using acceptance, abstention, route mix, and feature
   distributions. Choose the owner who can roll back the policy.

## Data and governance for learned routers

The hardest part of a learned router is often the label pipeline. A label such
as “the capable model won” can mean a human preferred its prose, a validator
passed its fields, a user clicked a button, or an evaluator scored it higher.
These are different targets. Name the outcome and keep the label source. A
router trained on a mixed label silently learns a mixture of product taste,
judge behavior, and operational availability.

Build a route-outcome table with request stratum, eligible set, chosen enum,
features available before dispatch, route version, acceptance result, rework,
latency, cost, and censoring reason. A request whose cheap answer was never
reviewed is not the same as a request whose answer was reviewed and passed. A
request that was blocked by `R1` has no counterfactual worker outcome. Keep
those distinctions in training and evaluation.

Guard against leakage. Features such as validator failure, final human edit,
or provider response tokens are available after the choice and cannot be used
as pre-dispatch features. A proxy feature such as route-specific latency can
also leak the outcome if it is measured after selection. Freeze the feature
schema and run a temporal holdout so a model cannot memorize a provider alias
or a prompt template that changes next month.

Govern the learned policy as a release artifact. Store training data lineage,
label rubric, feature schema, model pin, route enum version, exploration
budget, acceptance floor, and rollback target. Monitor feature drift, route
mix, abstentions, protected-stratum acceptance, and disagreement with the
fixed baseline. When the policy is uncertain, it should abstain or use a
deterministic rule rather than exploit a confidence score that no one has
calibrated.

The feedback loop also changes the business. Sending more work to a local
route may justify capacity investment; sending more to a managed route may
change invoice tiers; routing uncertain work to humans may increase label
quality but reduce apparent automation. Include these second-order effects in
the evaluation plan. A policy is part of the system it measures.

## When not to learn

Learning is a poor first choice when a rule is clear, the protected stratum is
small, the labels arrive late, or the cost of one exploration mistake is high.
It is also a poor choice when the router's predicted difference is smaller
than price and latency noise. A deterministic route table can be more honest
and more stable while the team collects evidence.

Use learning when it answers a decision that the rule cannot: a measurable
complexity boundary, a stable preference among eligible routes, or a changing
capacity pattern. Prove that its output changes route mix or accepted cost
against the rule baseline. If it only produces a more elaborate explanation,
keep the rule and save the model call.

A learned router needs a retirement rule. If drift makes it uncertain,
disagreement with the fixed baseline grows, protected-stratum acceptance
falls below its floor, or labels stop arriving, freeze exploration and return
to a declared fixed policy. Keep the model and data artifacts so the cause can
be investigated;
retirement is not deletion. Reintroduce learning only after recalibration and
another replay.

## Checkpoint

Choose a learned family only when it observes a signal that changes a measured
decision. Record the labels, features available before dispatch, holdout,
exploration limit, and retirement rule. Keep eligibility deterministic even if
the choice is learned. The reader's artifact is a router-family decision that
states why a rule is insufficient and what evidence would make the team return
to a simpler rule.

## Source slot

Use [RouteLLM](https://arxiv.org/html/2406.18665), [FrugalGPT](https://arxiv.org/html/2305.05176),
and the recent research records S02–S04 and S58–S62 in the [source catalog](../sources.json)
for bounded algorithm evidence. Use [OpenAI harness engineering](https://openai.com/index/harness-engineering/)
and [Fowler](https://martinfowler.com/articles/harness-engineering.html) for
environment and feedback-loop practice. The family-selection guidance is a
proposal; it needs an enterprise holdout and rollback test.
