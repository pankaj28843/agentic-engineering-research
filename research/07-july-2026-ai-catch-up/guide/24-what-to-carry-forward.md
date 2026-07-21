# What to Carry Forward: A Field Guide for Building With Agents

The first three weeks of July 2026 revealed a durable idea: the useful unit of
AI engineering is the whole operating system around the model. That includes
the specification, context, tools, permissions, memory, runtime, evaluator,
human gates, telemetry, and recovery path. A better or cheaper model can still
make the system worse or more expensive. More context can lose the plan, more
agents can create conflicts, and a polite question can become authorization.

The durable operating rules are:

1. Evaluate the workflow you operate, not the model you admire.
2. Make every consequential agent action observable and replayable.
3. Treat permissions, questions, retrieval, and memory as security boundaries.
4. Budget context, coordination, and human review as real resources.
5. Prefer bounded autonomy with explicit evidence of completion.
6. Keep models portable enough that policy, price, or capability changes do not
   become emergencies.
7. Measure completed outcomes, failure recovery, and reviewer effort, not token
   price alone.
8. Preserve specifications and invariants outside generated code.

These are not slogans. Each rule below names the failure it prevents, explains
the mechanism in plain language, and turns the lesson into controls a builder
can implement.

## 1. Engineer the system, not the leaderboard position

A coding agent is more like a junior engineer inside a workshop than a text box
with a score. The model supplies judgment and generation, but the workshop
determines what the model can see, what it can touch, how it receives errors,
how long it can work, and who decides whether the result is acceptable. Two
teams can use the same model and get materially different cost, speed, and
quality because their harnesses differ.

The period supplied unusually direct evidence. Databricks evaluated model and
harness combinations on reviewed tasks from its private, multi-language
codebase. In that environment, a cheaper open model paired with Pi was
statistically tied with a much more expensive model, at lower cost per completed
task. The important result was not a universal winner. It was that the
combination changed the decision. See the [July 8 private-code evaluation
chapter](09-2026-07-08.md) and the [Databricks private-code
benchmark](https://www.databricks.com/blog/benchmarking-coding-agents-databricks-multi-million-line-codebase).

Ploy's production migration made the same point from another direction. Its
fixtures checked tool use, files, and visual output rather than trusting a
vendor score. GPT-5.6 improved time, cost, output-token use, and visual quality
for that particular agent, but the exercise also exposed assumptions in the
harness. The [July 9 production-migration chapter](10-2026-07-09.md) separates
the shipped model facts from the [Ploy migration
evidence](https://ploy.ai/blog/migrating-a-production-ai-agent-to-gpt-5-6).

Even the meaning of "better" depends on the interface. A newer model can reason
better and still invent fields inside a strict tool schema. That is not a
philosophical objection; it is an API compatibility failure. The bounded
example in the [July 4 tool-calling chapter](05-2026-07-04.md) shows why schema
adherence needs its own regression suite, separate from task success.
Likewise, Meta's Terminal-Bench comparison became questionable when a reader
noticed that the evaluation used blanket resource limits rather than the
benchmark's task-specific limits. Availability remained real, but the
comparison no longer supported the simple conclusion. The harness and the
grader were part of the claimed result.

The operating rule is simple: never approve a model change from a model-only
evaluation. Freeze a representative harness version, repository snapshot,
toolset, permissions profile, and evaluator. Run the old and new candidates
against identical fixtures. Record success, elapsed time, input and output
tokens, tool-call validity, retries, files revisited, human interventions, and
final reviewer judgment. Then repeat the comparison after deliberately changing
the harness. If the ranking flips, the model was not the sole cause.

This leads to a useful three-layer evaluation stack:

- **Layer one, contract tests:** Can the model emit valid tool calls, respect
  path and command rules, survive empty or malformed tool results, and stop at
  the right boundary?
- **Layer two, task fixtures:** Can the complete agent solve representative
  repository tasks under pinned conditions, with reviewed expected outcomes?
- **Layer three, operational trials:** Does it improve actual lead time,
  reviewer effort, rollback frequency, incident rate, and cost in a controlled
  rollout?

Public benchmarks remain useful for discovery, not acceptance. The period's
strongest warning came when OpenAI audited all 731
tasks in the public SWE-Bench Pro split and judged roughly 30% broken. Hidden
requirements, flawed tests, and invalid repository state had made impressive
scores hard to interpret. The [July 8 benchmark-correction
chapter](09-2026-07-08.md) and [OpenAI's task-quality
audit](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)
make the durable lesson explicit: evaluator quality is part of product quality.

## 2. Turn evaluation into a maintained engineering system

An evaluation is production infrastructure. It needs versioning, ownership,
review, incident intake, and retirement rules so the team does not optimize
against stale tasks while real work changes.

Begin with a task inventory. Sample failures and routine work from the systems
the agent will actually touch. Include ambiguous feature requests,
investigation, migrations, documentation, test repair, tool use, and rollback.
Senior SWE-Bench was notable because it tried to represent underspecified and
judgment-heavy engineering rather than only narrow patch completion. Its critics
then asked exactly the questions an internal evaluation owner should ask: Are
tasks adversarially generated? Are there degenerate cases? What is the human
baseline? Can models have seen the data? Can scores across versions still be
compared? The [July 2 evaluation chapter](03-2026-07-02.md) is a compact guide
to those design tensions.

For every internal fixture, preserve five things: the input state, the intended
outcome, the acceptance procedure, the reason the task matters, and the date on
which it was last revalidated. A task without a stable repository snapshot is
not reproducible. A task without a reviewed acceptance rule invites the grader
to reward plausible nonsense. A task without a business reason can raise a
score without improving the operation.

Measure more than pass rate. The code-cleanliness study in the [July 6
chapter](07-2026-07-06.md) reported no improvement in pass rate but fewer tokens
and file revisits on cleaner code. That means maintainability may pay through
reduced search effort before it changes headline correctness. Similarly, the
[Apple SpeechAnalyzer test](https://get-inscribe.com/blog/apple-speech-api-benchmark.html)
reported useful local latency and word-error results, yet the [July 13 bounded
speech chapter](14-2026-07-13.md) correctly limits the conclusion to its English
audiobook dataset, Apple hardware, and included comparators. A good evaluation
records where a result applies as carefully as what the result is.

Long-horizon agents add another requirement: inspect trajectories, not only
end states. In Vending-Bench, repeated runs and published transcripts showed a
measurable difference in agent coordination behavior. The evaluator could say
what messages were sent and how often cartels formed. It could not directly
measure inner intent. The [July 6 long-horizon chapter](07-2026-07-06.md) and
[Vending-Bench report](https://andonlabs.com/blog/fable5-vending-bench) model
good scientific restraint: report behavior, repeat it, and label psychological
interpretations as hypotheses.

Security evaluations need the same separation. Automated red teams can generate
more attacks than a human team can author, but a vendor's internally reported
success rates do not prove protection in your architecture. The
[July 15 self-testing chapter](16-2026-07-15.md) shows both the promise and the
evidence limit of automated adversarial generation. Use such systems to expand
pressure, then validate the findings and mitigations against independent,
locally owned acceptance tests.

A maintained evaluation program should therefore have a release rhythm:

- Add every serious production failure as a minimized regression case.
- Quarantine fixtures whose verifier, date, repository state, or expected result
  is disputed.
- Keep a small frozen core for longitudinal comparison and a rotating set for
  current work.
- Run human baselines on a sample, including time and review effort.
- Review model and harness changes independently, then together.
- Publish uncertainty: sample size, variance, exclusions, contamination risk,
  and unresolved grader disagreements.

## 3. Make trajectories observable, replayable, and attributable

When an agent fails, the final message is rarely enough to explain why. The
cause may be an instruction loaded before the prompt, a tool result from twenty
steps earlier, a compaction decision, an updated runtime, a cached response, or
a human question that timed out. Without a trace, every incident becomes a
story people tell from memory.

The event-log architecture in [July 5's quiet but durable
chapter](06-2026-07-05.md) offers a practical model. [The Log is the
Agent](https://arxiv.org/abs/2605.21997) proposes an append-only record as the
source of truth, with deterministic projections used to rebuild current state.
Agent systems can reuse mature event-sourcing concepts such as immutable
events, snapshots, idempotency, lineage, and forks.

ELI5 version: do not keep only the whiteboard after a long meeting. Keep the
ordered stack of notes showing who added, erased, or approved each item. Then a
reviewer can rebuild the whiteboard, branch from an earlier point, or discover
where a bad assumption entered.

At minimum, an agent event should identify the run, actor, model and version,
harness version, input provenance, event type, timestamp, parent event, content
hash, permission decision, and resulting side effect. Tool calls need both the
requested operation and a normalized receipt: command, arguments, working
directory, environment policy, exit status, output digest, changed files, and
external identifiers. Human decisions need the prompt displayed, choices,
answer, timeout policy, and identity of the approver. Memory writes and
retrievals need source lineage and policy outcomes.

This record does not make side effects reversible. Replaying an HTTP request,
payment, deployment, or database mutation can repeat damage. The event log must
distinguish pure observations from effectful operations. Effectful tools need
idempotency keys, dry-run modes where possible, preconditions, and a recorded
compensation or recovery action. Replay should default to simulation unless the
operator explicitly authorizes effects.

The July evidence shows why this depth matters. A Codex issue found an unusual
cluster of responses stopping at exactly 516 reasoning tokens, and an HN reader
reproduced the boundary with wrong answers in four of ten trials. The evidence
supported a reproducible anomaly, not its cause. Still, logs containing model
version, reasoning length, answer quality, and intermediary prompts made the
anomaly visible. See the [July 4 response-shape
investigation](05-2026-07-04.md) and the [underlying Codex issue
data](https://github.com/openai/codex/issues/30364).

The Claude response-leakage report from the same day illustrates attribution.
A user saw unrelated content, but competing explanations included provider
mix-up, transport behavior, hallucination, and hidden local context. Request and
response IDs, account and workspace provenance, cache state, and exact context
assembly are what turn that argument into an investigation.

Runtime attribution matters too. On July 19, commands against a deployed
Claude Code binary exposed that it embedded Bun's Rust port before that runtime
was a normal tagged release. The [binary-forensics
chapter](20-2026-07-19.md) and [reproducible inspection
steps](https://simonwillison.net/2026/Jul/19/claude-code-in-bun-in-rust/)
show why the agent's effective software bill of materials must cover embedded
runtimes, not only the visible product version. Performance or memory behavior
can change even when the model name does not.

Operationally, every run should answer four questions without guesswork:

1. What exact inputs and policy state shaped this action?
2. What did the agent request, and what actually happened?
3. Which human or automated gate authorized the consequence?
4. Can we reproduce the decision without repeating the side effect?

## 4. Treat every boundary as hostile until proven otherwise

Agent security is not one prompt-injection filter. An agent translates
untrusted language into actions across several boundaries: files become
context, model output becomes tool input, names become downloaded packages,
memory becomes future context, and questions become authority. Each translation
needs its own control.

### Filesystem and egress boundaries

The July 14 evidence is a direct warning. Wire-level traces showed Grok Build
sending files it read, including `.env` content, and moving repository material
and Git history. A privacy command affected retention rather than transmission.
Separately, opening a repository in Cursor on Windows could execute a malicious
workspace-root `git.exe`. These are different failures with one shared cause:
the tool was given a trust boundary broader than the user's mental model. Read
the [July 14 trust-boundary chapter](15-2026-07-14.md), the [Grok Build wire
analysis](https://gist.github.com/cereblab/dc9a40bc26120f4540e4e09b75ffb547),
and the [Cursor execution disclosure](https://mindgard.ai/blog/cursor-0day-when-full-disclosure-becomes-the-only-protection-left).

Contain the process, not just the prompt. Mount only the repository and required
toolchains. Exclude home directories, SSH material, cloud credentials, browser
profiles, and unrelated workspaces. Make secret injection task-scoped and
short-lived. Deny arbitrary network access by default; allow destinations by
tool and operation. Observe the wire so a setting named "private" cannot be
mistaken for a guarantee of no transmission. Open untrusted repositories in a
disposable environment where workspace executables cannot become toolchain
dependencies.

### Retrieval and resolver boundaries

HalluSquatting demonstrates a less obvious translation failure. A model invents
a plausible package, repository, skill, or MCP server name. A resolver then
finds an attacker-controlled resource registered under that name. The model did
not need to generate exploit code; it only needed to generate an identity that
the system trusted too quickly. The [July 18 resolver-trust
chapter](19-2026-07-18.md) explains the pattern.

Never let free-form model text directly select executable supply-chain objects.
Resolve names against an allowlisted catalog with canonical IDs, ownership,
version, integrity hash, and approval status. Return a receipt before fetching.
Fetch into quarantine, scan and inspect there, and require a separate permission
to install or execute. A nonexistent identifier should fail closed, not trigger
a broad internet search followed by installation.

### Memory boundaries

Persistent memory is an input channel delayed in time. The GhostWriter report
described hidden instructions or false facts being stored during one interaction
and activated during a later legitimate request. Although the packet had only a
secondary source for the quantitative claims, the architecture lesson does not
depend on the exact attack rate. The [July 19 memory-poisoning
chapter](20-2026-07-19.md) correctly treats provenance, validation, retrieval
policy, and revocation as the controls.

Memory entries should carry their source, author, creation event, confidence,
scope, expiry, and integrity status. Separate user-authored policy from inferred
preferences and retrieved claims. Run policy checks both when writing and when
retrieving. Make entries inspectable and deletable. Never concatenate an opaque
memory store into a privileged system prompt.

### Data and template boundaries

Hugging Face's July incident began with a malicious dataset using a remote-code
loader and template injection, then reached a worker and node, credentials, and
limited internal datasets. The response also revealed a resilience issue:
commercial-model guardrails blocked some forensic analysis, while a self-hosted
model completed it. The [July 16 incident chapter](17-2026-07-16.md) and
[Hugging Face disclosure](https://huggingface.co/blog/security-incident-july-2026)
make datasets, templates, agent credentials, and forensic access part of the
privileged computing base.

Treat model and dataset loading like code execution. Disable remote code by
default. Render templates in a constrained engine. Give workers workload
identities with minimal, short-lived credentials. Segment nodes and storage.
Preserve telemetry at a volume that supports reconstruction. Maintain a
self-hosted or otherwise independently controlled response path so safety
filters, provider outages, or account restrictions cannot block incident
analysis.

Across all four boundaries, separate generation from authorization. The model
may propose a path, package, memory, command, or destination. Deterministic
policy must resolve, constrain, and record the authority to act.

## 5. Design human control as a protocol, not a conversation

Many teams say they keep a human in the loop. That phrase is incomplete. Which
human? At what point? Presented with what evidence? How long can they wait? What
happens on silence? Can the agent reinterpret an informational question as
permission?

The versioned Claude Code failure in the [July 17 control-gate
chapter](18-2026-07-17.md) is a precise example. `AskUserQuestion` timed out
after 60 seconds and continued without a complete answer. Permission prompts did
not behave the same way, but in allowlisted or bypass-permission runs the
question could be the only remaining gate. The behavior was fixed quickly. The
durable failure was semantic: the system had no explicit type saying, "This
question blocks a consequential choice and silence means stop." Read the
[original reproduction](https://www.olafalders.com/2026/07/17/claude-code-anatomy-of-a-misfeature/)
for the version and mechanics.

Human gates should be typed protocol objects. A gate needs a purpose, permitted
answers, risk class, evidence bundle, deadline, default outcome, approver role,
and audit record. "Need information" and "need authorization" are different
types. Missing information can sometimes use a documented default. Missing
authorization must fail closed. Partial answers should remain partial rather
than being coerced into consent.

The Short Leash method in the [July 2 chapter](03-2026-07-02.md) offers a useful
workflow baseline: plan first, implement in small steps, review the diff before
continuing, and commit after each subtask. It is one practitioner's method, not
a universal optimum, but it converts supervision into explicit rollback units.
The pattern is particularly valuable while a team is still learning its agents'
failure modes.

Bounded work can support looser gates because the output is easy to inspect and
cheap to reverse. Terry Tao's agent-assisted applet ports and visualization are
a good example: the artifacts were visual aids, an expert could judge them, and
errors did not directly alter a production or proof boundary. The [July 11
bounded-tools chapter](12-2026-07-11.md) shows why the right question is not
"human or autonomous?" but "how observable, reversible, and expertise-matched
is this task?"

Use a simple autonomy matrix:

| Consequence | Easy to inspect and reverse | Hard to inspect or reverse |
|---|---|---|
| Low | May run unattended with logging | Require post-run review before reuse |
| High | Require approval before effect | Keep advisory; human performs action |

Generating a migration plan is lower consequence than executing it in
production; editing a scratch branch is more reversible than rotating
credentials. A Lean artifact helps inspection but does not replace mathematical
review. The [July 15 proof-assistance chapter](16-2026-07-15.md) shows how
formal-looking output can still carry an unreviewed theorem claim.

Human control also needs ergonomics. Present the proposed consequence, reason,
trust-boundary change, relevant diff, tests, uncertainty, and rollback path to a
qualified owner. Measure response time and rejection rate; an unevaluable gate
is theater even when it waits for a click.

## 6. Budget context and coordination like compute

Context is not free memory. It has latency, monetary cost, attention cost, and
failure modes. Instructions, tool schemas, repository excerpts, histories,
subagent reports, and output reserves compete for a finite working space. More
context can help until it dilutes relevant signals, triggers compaction, or
multiplies across parallel workers.

The [July 12 harness-cost chapter](13-2026-07-12.md) made fixed overhead
visible. In a pinned proxy measurement, Claude Code sent about 33,000 tokens
before the user's task, compared with about 7,000 for OpenCode. A large
instruction file and five MCP servers added substantial repeated cost. A direct
121,000-token task expanded to 513,000 tokens with two subagents. Those exact
numbers belong to specific product versions and configurations. The durable
lesson is to meter the assembled request at the harness boundary, not estimate
from the prompt a user typed. See the [Systima component
study](https://systima.ai/blog/claude-code-vs-opencode-token-overhead).

The [July 18 context-allocation chapter](19-2026-07-18.md) shows a related
runtime dependency. A merged metadata change altered usable context and output
reserve behavior. Practitioners reported compaction losing important details
and responded with durable plan files and structured external state. The exact
numeric reduction was discussion-sourced because the captured primary diff did
not render it, but the merged metadata change itself was real. The operational
response does not require faith in a single number: pin metadata, observe
compaction, reserve output headroom, and keep critical plans outside transient
conversation state.

Coordination consumes the same budget at a larger scale. Cursor's SQLite swarm
experiment showed that new coordination patterns reduced conflicts, duplicate
packages, and code volume, while several model mixes eventually reached the
same test result at dramatically different costs. The experiment was
vendor-designed and drew credible criticism. Still, the [July 20
swarm chapter](21-2026-07-20.md) and [Cursor's published
experiment](https://cursor.com/blog/agent-swarm-model-economics) support a
useful engineering question: what does each extra agent contribute that could
not be obtained by a cheaper sequential step?

Assign roles from uncertainty, not enthusiasm. Parallel exploration is useful
when the problem has several plausible architectures, independent evidence
paths, or isolated work units. It is wasteful when all workers reread the same
context, edit the same files, or wait on the same missing fact. A coordinator
should define ownership, shared invariants, message format, merge authority,
and stop conditions before spawning workers.

Track these coordination metrics:

- Unique useful findings per worker, not messages sent.
- Duplicate reads, duplicate edits, and merge conflicts.
- Context and cost multiplied by delegation.
- Time to first validated result and time to integrated result.
- Human review minutes per accepted change.
- Rework caused by inconsistent assumptions.
- Work discarded after another agent changed the specification.

Keep a durable task capsule outside chat: objective, constraints, plan,
decisions, evidence, open questions, changed files, validation, and next action.
Workers should read only their slice and return structured results. Compaction
must not be the sole custodian of requirements or safety decisions.

## 7. Build a portfolio of models and deployment paths

Model portability is not only a negotiating tactic. It is resilience against
price changes, access policy, provider outages, safety-filter mismatches, data
boundaries, and workload specialization. Portability does not mean every model
is interchangeable. It means the system can express its requirements clearly
enough to test alternatives and route work deliberately.

The period's open-model stories show several distinct reasons to care. GitHub
made an open-weight model selectable through a mainstream managed channel on
July 1. A local-inference repository on July 3 made hardware, VRAM,
quantization, bandwidth, and throughput choices concrete. Thinking Machines
shipped Inkling as an inspectable, tunable artifact rather than claiming it was
the best model overall. LM Studio packaged local and cloud open-model workflows.
The [July 1 distribution chapter](02-2026-07-01.md), [July 3 local-operation
chapter](04-2026-07-03.md), [July 15 open-weights
chapter](16-2026-07-15.md), and [July 16 local-agent
chapter](17-2026-07-16.md) describe different points on the same deployment
spectrum.

Do not collapse "open weights," "open source," "local," and "private" into one
label. Open weights may still carry restrictive licenses or opaque training.
Local software may call remote providers. A hosted open model still exposes
data to the host. A zero-retention claim is not the same as no transmission.
An announced future weight release is not a currently deployable artifact. The
Kimi K3 announcement and Qwen Image 3.0 demonstration were correctly limited by
what was actually available and inspectable in the [July 16](17-2026-07-16.md)
and [July 21](22-2026-07-21.md) chapters.

Specialization may matter more than parameter scale. Mistral's Leanstral offered
a deployable proof-oriented model and artifacts for Lean workflows. Cisco's
small Antares models targeted vulnerability localization rather than autonomous
discovery. Apple's on-device speech system performed well in a bounded hardware
and dataset test. Google's Flash family emphasized latency and price tiers, with
a restricted cyber model serving a narrower audience. These do not establish a
single ranking. They suggest routing tasks to models whose deployment and
capability envelopes match the job.

Create a model capability contract containing:

- Required input types, context size, tool schemas, latency, throughput, and
  output structure.
- Data residency, retention, training-use, logging, and deletion requirements.
- Minimum fixture results and maximum regression thresholds.
- Total cost per accepted outcome, including retries and review.
- Availability, rate-limit, and incident-response expectations.
- License, weight access, serving dependencies, and export-policy exposure.
- A tested fallback and the features lost during failover.

Provider policy can move independently of engineering. The weakly verified
Claude export-control report on [July 1](02-2026-07-01.md) and Reuters report of
an Alibaba restriction on [July 3](04-2026-07-03.md) should not be overstated,
but access can change for legal, geopolitical, security, or organizational
reasons. Exercise fallbacks on real fixtures and document changes in data,
quality, tooling, and latency.

Open weights also function as distribution strategy. The [July 20 strategic
analysis](21-2026-07-20.md) argued that hardware constraints can encourage
portable distribution while closed labs optimize services. That conclusion is
analysis, not measured destiny. For builders, the narrower lesson is sufficient:
hosting control, hardware availability, ecosystem integration, and model
quality are separate procurement axes. Score them separately.

## 8. Price completed, reviewed outcomes

Token price is visible but often the wrong unit. Retries, invalid tools, long
outputs, and repair can make a cheap model expensive per accepted change. A
specialized small model may still dominate on one narrow task.

Several July stories point toward outcome accounting. Databricks priced
completed private-code tasks. Ploy measured production fixtures rather than
vendor benchmarks. The GLM-5.2 analysis in the [July 6 economics
chapter](07-2026-07-06.md) paired low output-token price with explicit limits in
speed, vision, web use, privacy, and terms. Google's [July 21 Flash release
chapter](22-2026-07-21.md) made price and latency clearer than generalized
quality. The State of Open Source AI survey in the [July 17
chapter](18-2026-07-17.md) showed why adoption counts and benchmark gaps do not
answer production-operability questions.

Define an accepted outcome before measuring cost. For a code change, acceptance
might require tests, static checks, security policy, a reviewer approval, and no
rollback within seven days. For vulnerability localization, it might require a
true vulnerable file in the top five results and a reviewer-confirmed finding.
For transcription, it might require domain word-error rate plus latency on
target hardware. Without the acceptance definition, "cost per task" can hide a
large quality difference.

Then calculate:

`outcome cost = model + tools + compute + retries + evaluation + reviewer time + expected failure recovery`

Expected failure recovery is probability multiplied by consequence. It prevents
a fragile system from looking cheap merely because the accounting ends before
the incident. Include the opportunity cost of blocked reviewers and the cost of
maintaining the harness. Report median and tail behavior; a workflow that is
usually cheap but occasionally consumes an hour of expert repair may be a poor
default.

Do not confuse research leverage with autonomous value. The AI-assisted CIRCL
audit produced seven human-validated bugs and upstream fixes. Its strength was
the lineage from candidate through proof of concept to repair, not a claim that
the model independently audited cryptography. The [July 7 security-audit
chapter](08-2026-07-07.md) and [zkSecurity report](https://blog.zksecurity.xyz/posts/circl-bugs/)
show the cost center teams must preserve: expert triage.

The WordPress RCE report in the [July 20 chapter](21-2026-07-20.md) gives the
opposite accounting warning. The technical chain was credible enough to study,
but a $500,000 exploit-broker comparison was unsupported and strongly disputed
by security practitioners. Model subscription cost and model-hours did not
represent researcher time, validation, disclosure, or market value. Never let a
dramatic comparator substitute for a complete cost ledger.

Review outcome economics monthly. Promote a candidate only when it beats the
current system across the weighted portfolio. When price or versions change,
rerun accepted-outcome calculations instead of extrapolating from token tables.

## 9. Preserve specifications outside generated implementations

Agents can write several plausible implementations faster than humans can read
them. That changes where engineering judgment is scarce. The bottleneck moves
toward specifying invariants, designing discriminating tests, comparing hidden
choices, and deciding what evidence permits deployment.

The distributed DNS case study in the [July 20 specification
chapter](21-2026-07-20.md) used concurrent agent loops to build competing
implementations. Their disagreements surfaced underspecified decisions, which
the practitioner turned into a terse specification. The retained system then
had tests, shadow deployment, and documentation. This is a useful pattern
because diversity was used to discover the specification, not to vote on truth.
The [original case study](https://blog.exe.dev/claude-is-not-a-compiler) says it
plainly: the agent is not the compiler that makes an informal wish correct.

Keep four durable artifacts outside generated code:

1. **Behavioral contract:** inputs, outputs, error semantics, performance
   bounds, and compatibility obligations.
2. **Safety invariants:** states and actions that must never occur, with the
   enforcement layer named.
3. **Decision record:** important alternatives, assumptions, and why the chosen
   design won.
4. **Validation evidence:** tests, traces, reviewer findings, rollout results,
   and known gaps tied to versions.

Ask competing agents or implementations to expose decisions, not merely code.
For example: How are writes ordered? What happens after partial failure? Which
state is authoritative? What is retried? How is identity established? Which
resource limits are enforced? Convert divergent answers into tests or explicit
choices before selecting an implementation.

Formal methods strengthen this process where properties are expressible.
Leanstral and the assisted convex-optimization claim also showed the evidence
boundary: an inspectable artifact does not prove that it matches the intended
theorem or appropriate assumptions. Domain review remains part of acceptance.

The same rule applies to interfaces. GPT-Live's split between a low-latency
conversation and slower delegated work, covered in the [July 8 interface
chapter](09-2026-07-08.md), is an architectural pattern. The contract must say
which loop owns the user commitment, how background results are reconciled, and
what happens when the conversational layer speaks before delegated work
finishes. Riddle's handwritten interface in the [July 7
chapter](08-2026-07-07.md) similarly turns an ambient notebook into an input
channel; capture, memory, provider use, and privileged installation need
explicit contracts.

Generated code is replaceable. The specification, evidence, and operational
history are the assets that let a team replace it safely.

## Failure modes to recognize early

The following patterns recur across the period. Use them during design reviews
and incident triage.

### The benchmark halo

**Symptom:** A team treats a public aggregate score as evidence for its own
workflow.

**Mechanism:** Broken tasks, contamination, verifier flaws, resource differences,
or harness behavior distort the comparison.

**Control:** Use public results only to nominate candidates. Require private
fixtures, pinned environments, human review, and documented applicability.

### The invisible harness tax

**Symptom:** Bills, latency, or context exhaustion exceed estimates even though
user prompts are small.

**Mechanism:** Always-loaded instructions, tool schemas, histories, retries,
subagents, and output reserves dominate the request.

**Control:** Meter assembled requests at the API boundary. Attribute cost by
component and establish budgets for fixed overhead and delegation.

### The friendly gate

**Symptom:** An agent asks a question, receives no complete answer, and acts
anyway.

**Mechanism:** Conversational UI hides authorization semantics; timeout or
partial-answer behavior changes across versions.

**Control:** Typed gates, fail-closed authorization, version-pinned regression
tests, and explicit unattended-run policy.

### The privacy-label shortcut

**Symptom:** Users interpret retention, training-use, or local-product language
as proof that data never leaves the machine.

**Mechanism:** Transmission, storage, training, trace handling, and provider
hops are distinct properties.

**Control:** Verify network behavior, enumerate every processor, isolate
secrets, and document each lifecycle property separately.

### The resolver leap

**Symptom:** A generated name becomes an installed package, skill, server, or
repository.

**Mechanism:** Plausible text crosses directly into supply-chain identity.

**Control:** Canonical allowlisted resolution, integrity receipts, quarantine,
and a separate execution approval.

### The trusted-memory fallacy

**Symptom:** Old memory silently changes a later privileged decision.

**Mechanism:** Stored content loses provenance and re-enters context at higher
trust.

**Control:** Scoped, typed, expiring memory with write and retrieval validation,
inspection, and revocation.

### The swarm reflex

**Symptom:** More agents produce more messages, branches, and cost without
faster validated delivery.

**Mechanism:** Roles overlap, context is duplicated, invariants diverge, and
integration becomes the bottleneck.

**Control:** Spawn from a named uncertainty or partition, assign ownership,
define output contracts, and measure unique contribution plus merge cost.

### The artifact-is-proof error

**Symptom:** Generated tests, a formal file, a proof of concept, or polished
output is treated as independent validation.

**Mechanism:** The artifact may encode the wrong requirement, share the same
model error, or lack domain review.

**Control:** Separate author from verifier where feasible, inspect assumptions,
and obtain evidence at the actual consequence boundary.

### The claim inflation chain

**Symptom:** A concrete technical result becomes a broad story about autonomy,
intent, savings, or market value.

**Mechanism:** Each retelling drops scope and uncertainty. Vendor comparisons or
dramatic analogies become apparent facts.

**Control:** Preserve source role and confidence, distinguish observation from
interpretation, and stop publication when the evidence is inaccessible. The
[July 10 no-story chapter](11-2026-07-10.md) is useful precisely because it
records two evidence failures instead of filling the day with claims.

## Builder checklists

These checklists are intended for pull requests, design reviews, procurement,
and release gates. A team should adapt thresholds, but it should not silently
delete the questions.

### Before approving an agent use case

- State the job in observable terms and define an accepted outcome.
- Name the human owner and the people qualified to review the result.
- Classify each action by consequence, reversibility, and inspectability.
- List data, filesystem, network, identity, package, memory, and deployment
  boundaries the agent can cross.
- Define what the model may propose versus what deterministic policy or a human
  must authorize.
- Choose a bounded pilot with a real baseline and a rollback path.
- Record prohibited tasks, especially those lacking a competent reviewer.

### Before trusting an evaluation

- Pin repository state, model, harness, tools, resource limits, and evaluator.
- Confirm each fixture has a reviewed requirement and valid acceptance rule.
- Include ambiguous investigation, tool failures, and negative cases.
- Measure validity of tool calls, retries, trajectory length, file revisits,
  latency, cost, and reviewer effort alongside pass rate.
- Run enough repetitions to expose variance and long-tail failures.
- Maintain human baselines for a representative sample.
- Label vendor measurements, internal measurements, reproductions, and
  discussion-derived corrections separately.
- Quarantine broken or contaminated tasks instead of averaging them away.

### Before granting tools or permissions

- Mount the smallest filesystem scope and exclude home and credential stores.
- Give each run a short-lived workload identity and least-privilege credentials.
- Deny network egress by default; allow named destinations per tool.
- Prevent workspace executables from becoming implicit toolchain dependencies.
- Validate tool arguments structurally and return exact errors to the agent.
- Require canonical identity and integrity checks before fetching dependencies.
- Distinguish read, propose, write, execute, publish, deploy, and delete powers.
- Record authorization and a normalized receipt for every side effect.
- Test timeout, cancellation, partial answer, and lost-connection behavior.

### Before enabling persistent memory

- Separate policy, user facts, inferred preferences, summaries, and retrieved
  content into different trust classes.
- Attach source event, author, scope, confidence, timestamp, and expiry.
- Validate on write and on retrieval; do not trust prior validation forever.
- Make memory visible to the user or operator and support targeted revocation.
- Prevent retrieved memory from overriding higher-trust instructions.
- Test delayed injection, conflicting entries, stale facts, and deletion.
- Log which memory items influenced each consequential decision.

### Before scaling to multiple agents

- Name the uncertainty or independent work partition that justifies parallelism.
- Assign exclusive file, subsystem, or evidence ownership where possible.
- Give every worker a bounded input and structured return contract.
- Externalize shared invariants and current decisions in a durable capsule.
- Select one merge authority and define conflict resolution before work starts.
- Cap context, elapsed time, spend, and retries per worker.
- Stop workers whose unique contribution falls below coordination cost.
- Compare the swarm with a single-agent and sequential baseline.

### Before changing models or runtimes

- Read the effective model metadata, output reserve, context policy, and release
  notes rather than relying on the product label.
- Inventory embedded runtimes and dependencies from the deployed artifact.
- Run contract, fixture, safety, compaction, and failover suites.
- Recalculate cost per accepted outcome with review and recovery included.
- Verify data handling, retention, regional availability, and policy changes.
- Roll out in shadow or canary mode with a versioned rollback target.
- Watch response shape, schema errors, tool retries, memory, and latency for
  silent regressions.

### Before calling the system production-ready

- Demonstrate that a failed run can be reconstructed from logs.
- Demonstrate that replay does not repeat external effects by default.
- Exercise revocation of credentials, memory, packages, and model access.
- Run a malicious repository, prompt-injection, hallucinated-package, and data
  exfiltration drill in an isolated environment.
- Confirm human gates fail closed and reach qualified reviewers.
- Prove a provider or model fallback on representative work.
- Publish known limits, unresolved risks, and the owner of each remediation.
- Review actual incidents and near misses after the pilot, not only successes.

## A 30-day adoption plan

This plan assumes a team already has access to one or more coding agents but
has not yet built a disciplined operating system around them. The goal is not
full autonomy in 30 days. The goal is one production-relevant workflow with
measured value, constrained authority, reproducible evidence, and a credible
decision about what to do next.

### Days 1-3: Choose the job and freeze the contract

Select one frequent, bounded workflow such as test repair, dependency updates,
internal documentation, UI fixtures, static-analysis remediation, or
vulnerability localization. Exclude production deployment, credential changes,
and broad autonomous issue resolution from the first pilot.

Write a one-page contract: objective, accepted outcome, non-goals, data scope,
allowed tools, prohibited actions, reviewer role, timeout, spend cap, and
rollback. Classify every proposed action by consequence, reversibility, and
inspectability. Choose the existing human workflow as the baseline.

**Exit evidence:** An owner-approved contract, a risk classification, and ten to
twenty representative historical tasks with legally and operationally valid
data.

### Days 4-6: Build the smallest evaluation harness

Turn the historical tasks into pinned fixtures. Preserve repository snapshots
and expected results. Write deterministic contract tests for tool schemas,
paths, commands, network policy, cancellation, and malformed results. Define
the human review rubric and record baseline completion time and defects on a
sample.

Do not optimize prompts yet. First prove that repeated runs produce comparable
measurements. Store model, harness, runtime, context, and evaluator versions
with every result.

**Exit evidence:** A repeatable command or pipeline that runs fixtures and emits
task success, tool validity, latency, tokens, estimated cost, and reviewer
status.

### Days 7-9: Instrument the trajectory

Add append-only run events and normalized tool receipts. Capture context-source
metadata, model and harness versions, permission decisions, memory reads and
writes, file changes, external calls, compaction, retries, and stop reason.
Separate pure observations from side effects. Add idempotency keys or dry-run
behavior to effectful tools.

Choose one failed fixture and conduct a reconstruction exercise. A reviewer who
did not watch the run should be able to explain what happened and identify the
authorization chain.

**Exit evidence:** A trace that reconstructs the failure without rerunning side
effects, plus a documented list of remaining blind spots.

### Days 10-12: Enforce the security boundary

Run the agent in a disposable environment with minimal mounts. Remove ambient
credentials and inject only short-lived task credentials. Restrict egress.
Disable remote code in datasets and packages unless explicitly approved. Add a
canonical resolver or allowlist for dependencies, skills, MCP servers, and
repositories.

Test a repository containing a fake local executable, a secret-like file, a
prompt-injected document, and a hallucinated dependency name. Inspect both tool
logs and network behavior. Verify that retention or privacy labels do not stand
in for transmission evidence.

**Exit evidence:** All four adversarial cases fail without crossing their trust
boundaries, or the pilot remains blocked with named remediations.

### Days 13-15: Formalize human gates and recovery

Replace conversational approvals with typed gates. Define who can approve each
risk class, what evidence they see, and what timeout does. Make missing
authorization fail closed. Test silence, partial answers, disconnection,
cancellation, stale approvals, and product-version changes.

Create rollback or compensation procedures for every side effect in the pilot.
Practice stopping a run midway, revoking its identity, discarding its workspace,
and restoring the pre-run state.

**Exit evidence:** A gate regression suite and one recorded stop-and-recover
drill completed by the operating team.

### Days 16-18: Establish the baseline and compare candidates

Run the current configuration repeatedly across non-deterministic fixtures.
Compare at most two alternatives: a different model, harness, or
local/specialized route. Change one dimension before testing combinations.

Calculate accepted-outcome cost, not token price. Include model and tool charges,
compute, retries, evaluator cost, reviewer minutes, and observed recovery work.
Report median, tail, and failure categories. Treat public benchmark scores as
context only.

**Exit evidence:** A decision table showing capability, operational constraints,
confidence, and cost per accepted outcome for each candidate.

### Days 19-21: Pilot with bounded real work

Move from historical fixtures to a small queue of current work in shadow mode or
on isolated branches. Keep the same review rubric. Do not let the agent publish,
merge, deploy, or contact external users. Record where live tasks differ from
fixtures and convert each meaningful surprise into a candidate regression test.

Review failures and near misses daily. Classify causes as model, harness,
context, tool, permission, evaluator, specification, or human process rather
than labeling every failure a model issue.

**Exit evidence:** At least ten current tasks, all reviewed, with traceable
acceptance decisions and no unexplained side effects.

### Days 22-24: Test context and coordination deliberately

Measure fixed prompt, instruction, tool-schema, memory, and repository overhead
at the actual model boundary. Trigger compaction in a controlled fixture and
check whether requirements, decisions, and safety constraints survive. Move
critical state into a durable capsule.

If the workflow has genuine independent work, test one small parallel design
against the sequential baseline. Define roles and merge authority first. Do not
scale beyond two or three workers during this phase. Measure duplicate work,
conflicts, total context, integration time, and reviewer burden.

**Exit evidence:** A context budget, a compaction regression, and either a
measured case for bounded parallelism or a decision to remain sequential.

### Days 25-27: Exercise portability and incident response

Run a representative subset through the fallback model or deployment path.
Record lost features, changed schemas, latency, quality, and data-boundary
differences. Inspect the effective runtime and dependency inventory of the
deployed agent.

Conduct one incident tabletop covering a leaked credential, poisoned memory,
malicious dependency, unexpected transmission, or provider loss. Walk through
detection, containment, reconstruction, revocation, recovery, and regression
creation. Confirm responders have an independent model path for forensics.

**Exit evidence:** A tested fallback report and an incident record with owners,
times, evidence, and corrective actions.

### Days 28-30: Decide, document, and set the next boundary

Review the pilot against its original contract. Count accepted outcomes,
rejections, escaped defects, reviewer minutes, median and tail completion time,
cost, security events, and recovery work. List every assumption that remains
untested. Ask reviewers whether the system reduced cognitive load or merely
moved it into harder-to-audit supervision.

Choose one of three explicit outcomes: stop, continue the bounded pilot, or
promote it with a narrowly expanded authority. Do not promote based only on a
high pass rate. Promotion requires reliable traces, enforced permissions,
working recovery, qualified review, and favorable outcome economics.

Publish an internal operating note containing the behavioral contract, safety
invariants, model and harness versions, evaluation summary, known limits,
runbook, fallback, and owners. Schedule monthly fixture maintenance and a
quarterly trust-boundary review.

**Exit evidence:** A signed decision with supporting metrics and the exact next
authority boundary, not a general mandate to "use agents more."

## The operating doctrine

The most durable lesson from these 21 days is that agentic engineering is
ordinary systems engineering under unusually probabilistic control. The model
can suggest, synthesize, search, and sometimes discover at remarkable speed.
It also amplifies whatever the surrounding system leaves ambiguous: a broken
grader, an overbroad mount, an invented package, a silent timeout, a bloated
context, an unowned specification, or a dramatic but unsupported comparison.

Strong teams will not win by finding a model that eliminates engineering
discipline. They will win by making discipline cheaper to apply. Their agents
will operate inside small, explicit authority envelopes. Their evaluations will
use real work and maintained verifiers. Their traces will make failures
reconstructable. Their human gates will have protocol semantics. Their memory
and retrieval systems will preserve provenance. Their economics will count
review and recovery. Their specifications will survive model and code changes.

The edition itself supplies one final example. On July 10, inaccessible or
undated evidence prevented publication of a claimed proof and a misuse report.
On other days, vendor benchmarks were kept separate from independent results,
announcements were distinguished from released weights, observed behavior was
separated from claims about intent, and strong technical evidence was separated
from inflated economic framing. That same discipline belongs inside every
agent system: know what happened, know how you know, know what remains uncertain,
and allow consequences only when the evidence matches the risk.

Carry that forward, and model progress becomes leverage rather than operational
surprise.
