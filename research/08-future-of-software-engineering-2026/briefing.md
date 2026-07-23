# Evidence-Weighted Briefing

## Verdict

The Thoughtworks retreat correctly locates several real pressure points in
agentic software engineering: trustworthy acceptance, the operating
environment around agents, changing team cognition, modernization, security,
cost, and the scarcity of accountable judgment. The independent evidence does
not support several of its sharpest formulations as general laws.

The useful synthesis is this:

> Agents make candidate production cheaper. They do not make trustworthy
> acceptance, organizational understanding, operational capacity, or
> accountability free.

That shift changes the work. Tests, specifications, policies, observability,
tool boundaries, review, and rollback become part of the production system.
Yet calling all of that “verification” or “the harness” can hide costs and
create false confidence. A passing test may encode a weak oracle; a formal
proof remains conditional on the specification; a human reviewer may anchor
on the model; and a sophisticated harness can overfit, decay, or cost more
than it saves.

The packet therefore rejects two symmetrical mistakes: treating generation
speed as complete delivery productivity, and responding to weak evidence by
pretending agents have produced no useful change. The evidence supports
bounded gains, serious new failure modes, and local experiments with explicit
accounting.

## What the evidence supports

### Trust must be decomposed

Existing tests can overstate benchmark success, generated tests can prefer
convenient assertions, and evaluator or harness changes can materially change
rankings. Formal verification can provide much stronger acceptance for an
encoded property and trusted kernel, but cannot prove unexpressed intent or
environment fidelity. Human code review has bounded historical evidence and
important knowledge effects; no source in this packet shows that it is
universally obsolete.

The operational response is not “add every verifier.” Measure candidate
volume, acceptance latency, independent fault coverage, false acceptance,
triage cost, downstream defects, and total work. Add a layer when it catches
important failures the existing system misses at a tolerable cost.

### Harnesses are operating systems for bounded agency

Repository instructions, tools, runtime state, tests, observability, policies,
and feedback loops can materially change agent performance. A bounded
self-modifying-harness study also shows that validation-gated edits can improve
a benchmark. Its supposedly held-out set was repeatedly consulted for
promotion, however, and the study omits a truly untouched final test, search
cost, failed proposals, maintenance, and independent replication.

Harness work should therefore be treated as a product with an owner,
versioning, evaluation, expiration, pruning, and a measured cost curve—not as
an ever-growing prompt pile.

### Modes of use matter more than slogans about learning

One randomized short-horizon experiment with 52 experienced Python users found
lower immediate unaided comprehension after AI-assisted unfamiliar-library
work. Classroom and workplace studies show changes in help-seeking,
verification, collaboration, and task allocation. They do not establish a
career-scale apprenticeship cliff, durable cognitive decline, or a uniquely
vulnerable seven-to-ten-year cohort.

Pairing, design quorums, explanation, reflective comparison, and declared
non-AI practice are plausible countermeasures that still need evaluation.
Unaided exercises must be formative, consented, accessible, job-relevant, and
separated from covert surveillance or punitive employment decisions.

### Modernization value is bounded but credible

AI can help with discovery, explanation, dependency mapping,
retro-documentation, test assistance, selected translation, and
environment-backed repair. The evidence does not show autonomous replacement
of a large production mainframe with preserved functional and
non-functional behavior.

“Port first, improve second” is a defensible risk-reduction heuristic when the
current behavior is worth preserving and an oracle exists. It is not a
universal law: obsolete behavior, security defects, missing tests, and
architecture constraints may make literal preservation the wrong objective.
Modernization accounting must include discovery, human expertise, parallel
operation, cutover, verification, rework, and realized business value—not
only generated code or elapsed demo time.

### Defense in depth survives audit

Models do hallucinate package names, and some names recur. Laboratory work also
shows that persistent instructions can steer selected models toward a target
package name. Those stages are not the same as malicious registration,
installation, execution, or compromise.

Distinct identity, least privilege, pre-action policy, narrow tools, parameter
validation, secret separation, constrained egress, isolated execution,
provenance, durable logs, revocation, monitoring, and incident response cover
different failure modes. No source quantifies a universal risk reduction for a
color tier, sandbox, or maturity model. A dependency cooldown can reduce
immediate exposure to a fresh release, but fourteen days has no established
universal basis and delay cannot replace source approval, screening, lockfiles,
or containment.

### Human presence and human judgment are different

A controlled COMPAS study found no accuracy benefit from adding the score and
showed strong anchoring when the displayed score was shifted. Organizational
studies identify cyborg, centaur, and abdication patterns, but do not establish
a causal performance hierarchy. A systematic review supplies useful design
dimensions while lacking the quality appraisal required for a pooled claim.

Meaningful judgment requires a named decision, relevant expertise,
information, time, stop or override power, an appeal path, and accountability
after failure. Evaluate a hybrid against both a strong human-only and strong
AI-only workflow. A person clicking approve is not an independent control.

## Important negative findings

The audit did not validate these retreat claims:

- agent review consumes four times the tokens and fixes roughly 90% of its own
  errors;
- an AI-built TypeScript-to-CLR compiler took four days;
- a COBOL compiler passed the relevant NIST suite in three days for about
  $5,000;
- maintenance generally consumes 30–50% of IT spend, or a $100 million program
  was safely reframed as an $8 million proposal over 20% of systems;
- agent-related security incidents rose about twenty-fold;
- an annual token budget was exhausted in three months, or coding-agent spend
  rose ten-fold;
- full-lifecycle productivity is generally 2–3x or 10x;
- a hype reset will arrive in 12–18 months;
- an architecture round trip creates a general 1,400x inference-cost ratio;
- open source is moving from shared code to shared specifications;
- human–AI centaurs generally beat the best human or AI-only alternative;
- visibly human software will command a reliable market premium.

Some numbers resemble results elsewhere, but those results measure different
constructs. Similar digits do not create provenance. The guide keeps these as
anonymous retreat recollections, hypotheses, or omissions rather than
reverse-identifying participants or manufacturing validation.

## A practical operating model

For each agentic workflow, write down:

1. the decision and value being pursued;
2. the generator, tools, data, privileges, and side effects;
3. the acceptance evidence and how independent its failure modes are;
4. the human role, expertise, time, authority, and recourse;
5. total work, including harness construction, verification, exceptions,
   infrastructure, and downstream rework;
6. consequence, reversibility, blast radius, observability, and recovery;
7. the stop condition, rollback path, owner, and review date.

Run a bounded experiment. Compare against the current workflow and, when
feasible, a simpler alternative. Promote autonomy only after evidence on the
actual workload; demote it after incidents, distribution shift, control
failure, or material system change.

## Confidence and limits

Confidence is high in the evidence classifications, exact denominators quoted
from retained studies, and the conclusion that the strongest universal claims
remain unproven. Confidence is medium in cross-source mechanism syntheses such
as review-pressure shifts, harness decay, or mode-dependent learning because
the studies are heterogeneous. Confidence is low in forecasts, market-wide
rates, universal productivity multipliers, and fixed governance thresholds.

The corpus includes peer-reviewed studies, preprints, official standards and
policies, vendor or consultancy reports, practitioner cases, perspectives, and
community discussions. It is current through 23 July 2026. Fast-moving product
prices, policies, and model capabilities must be rechecked before a live
decision.
