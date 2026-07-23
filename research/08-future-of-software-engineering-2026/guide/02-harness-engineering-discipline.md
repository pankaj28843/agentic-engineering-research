# Harness Engineering as a Discipline

A powerful engine does not make a safe vehicle. The vehicle also needs steering, brakes, instruments, operating limits, maintenance procedures, and a driver who knows what each signal means. In agentic software work, that surrounding control system is the **harness**.

The word is overloaded. At its broadest, a harness can mean everything around a model. For a software team, a useful boundary is narrower:

> A coding-agent harness is the versioned set of instructions, tools, context routes, permissions, environments, checks, runtime policies, and escalation paths that shape an agent's work and expose evidence about its results.

That definition makes harness engineering a discipline rather than a prompt collection. A discipline has named objects, owners, change control, operating feedback, and a way to retire what no longer earns its cost.

The [2026 Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) treats harness engineering as a major emerging responsibility. Fowler's [13 July retreat notes](https://martinfowler.com/fragments/2026-07-13.html) and Kief Morris's [participant account](https://infrastructure-as-code.com/posts/fose-july-2026.html) provide firsthand provenance for that emphasis. These are **practice-witness sources** from an overlapping Chatham House event, not independent proof that a particular harness organization improves delivery.

The more durable case comes from the control problem itself.

## Guides, sensors, and the steering loop

[Birgitta Böckeler's harness-engineering model](https://martinfowler.com/articles/harness-engineering.html) separates two kinds of control:

- **Guides** act before or during generation: repository instructions, examples, architectural rules, approved commands, dependency policies, and task decomposition.
- **Sensors** observe an action or artifact and feed back a corrective signal: compilers, linters, tests, policy checks, runtime probes, and structured review.

Each can also be computational or inferential. A type checker is computational: cheap, repeatable, and narrow. An architectural review by another model is inferential: semantically wider, but variable and harder to calibrate. The categories are a **practitioner taxonomy**, not a comparative experiment. Their value is that they force a team to say what a control can observe.

A guide without a sensor can encode a rule without revealing whether it worked. A sensor without a guide can make the agent repeat a known mistake and rediscover the correction. The steering loop joins them:

```text
intent -> guide -> agent action -> sensor -> evidence -> correction
                    ^                         |
                    +---- harness revision ---+
```

This is why a harness is more than “context.” Context engineering decides what information reaches a model call. Harness engineering also governs actions, permissions, state, evaluation, recovery, and promotion through a lifecycle.

## Why ownership matters

A harness can fail while every individual component appears reasonable.

One team adds a repository instruction. Another changes the build image. Security tightens network policy. A model upgrade changes tool behavior. A generated test encodes an old product assumption. No one owns the composed outcome. The harness has become production infrastructure without production stewardship.

Ownership does not require one central team to control every rule. It requires an accountable contract:

- **Product teams** own domain intent, local acceptance examples, and the decision to ship.
- **Platform teams** own shared execution, identity, observability, safe defaults, and paved paths.
- **Security and risk owners** define constrained actions and exception paths.
- **Model/tool owners** qualify versions and disclose changes in behavior or cost.
- **A named harness steward** owns composition, health, conflict resolution, and retirement for a bounded system.

The exact split is an organizational design hypothesis. No audited study in this corpus compares centralized and federated harness ownership. The important property is traceable accountability at the seams.

## Evidence that the surrounding system matters

The clearest bounded experiment in the local corpus is [Self-Harness](https://arxiv.org/html/2606.09498v1). It held a base model and evaluator fixed while iteratively changing prompts, tools, memory, verification rules, permissions, adapters, and runtime mechanisms. Across three model families on a filtered 64-task subset of Terminal-Bench 2.0, reported held-out pass rates rose from 40.5% to 61.9%, 23.8% to 38.1%, and 42.9% to 57.1%.

This is **preprint benchmark evidence** that changing the surrounding protocol can materially change observed agent performance. It also found different models benefited from different changes: earlier artifact creation, dependency checks, loop stopping, environment preservation, or faster transitions from exploration to testing.

Its limits prevent the larger marketing conclusion. The “held-out” set was consulted during candidate promotion on every iteration, so it functioned as an adaptively reused validation set rather than an untouched final test. The study reports neither full engineering cost nor long-term maintenance, and Terminal-Bench is not a production organization. It does not prove that a self-modifying harness should own itself.

A second bounded result comes from [RepoRescue](https://arxiv.org/html/2607.01213v1). In its Python compatibility benchmark, some systems' apparent successes fell sharply when test-file edits were stripped; blocking test edits during execution changed the repair strategies and outcomes. The paper explicitly treats model plus agent framework as the observed system because context construction, tools, retries, and stopping behavior affect performance. This is **repository-benchmark evidence** that harness permissions can change not just the score but the path an agent takes. It remains one trial per condition and a compatibility-rescue task, not a general harness ROI study.

Conceptual work goes further. The paper [“Code as the Agentic Interface”](https://arxiv.org/html/2605.18747v1) argues that executable, stateful repositories can act as a durable interface for agents when paired with tools, tests, permissions, and observability. That is a **design argument**, not controlled evidence. It is useful precisely because it exposes its conditions: code alone is not a trustworthy interface when goals are ambiguous or sensors are weak.

## A discipline, or temporary scaffolding?

One skeptical possibility is that today's elaborate harnesses compensate for weak models. As models improve, explicit reminders, bespoke wrappers, and recovery tricks may become obsolete. [An O'Reilly practitioner counterargument](https://www.oreilly.com/radar/stop-overengineering-your-agent-harness/) warns that teams can fossilize workarounds after the underlying model no longer needs them.

That is plausible. It does not imply that the discipline disappears. Vehicle engines improved; brakes, instruments, and maintenance did not vanish. The likely split is:

- **ephemeral controls** that patch a model-specific failure;
- **durable controls** that express organizational intent, permissions, interfaces, and independent acceptance evidence.

The discipline earns its keep by distinguishing the two. A harness feature should have a failure it prevents, evidence that it still works, an owner, a cost, and a retirement condition. “We once saw the agent do something odd” is not a perpetual control case.

Harness complexity also creates its own failure modes:

- conflicting instructions and stale context;
- feedback that rewards the metric rather than the intent;
- hidden coupling to a model or tool version;
- slow checks that encourage bypasses;
- state compressed until a critical exception disappears;
- growing control surface that no human can explain;
- self-generated rules validated against the same reused task set.

These are **mechanism risks and practitioner observations**, not measured prevalence. They make harness health an empirical question.

## The minimum harness record

Treat each meaningful control as a small, inspectable product. Record:

| Field | Question |
|---|---|
| Control | What guide, sensor, permission, or recovery action exists? |
| Intended failure | Which concrete failure mode should it reduce? |
| Scope | Which repositories, tasks, models, and risk classes does it govern? |
| Signal | What evidence does it produce, and who can interpret it? |
| Independence | Does it share assumptions, model family, examples, or context with the generator? |
| Cost | What latency, tokens, infrastructure, maintenance, and human attention does it consume? |
| Owner | Who may change it, approve exceptions, and respond when it fails? |
| Version | Which model, tool, environment, and policy version was qualified? |
| Retirement test | What observation would justify deleting or simplifying it? |

This record prevents a common category error: a prompt can be useful without being a policy; a judge can be informative without being an approval authority; a passing test can be evidence without being proof of intent.

## Exercise: run a four-week harness loop

Choose one repository and one recurring task class, such as dependency updates or API endpoint changes. Do not start by installing more controls.

**Week 1 — Baseline.** Record 10–20 executions under the current harness. Cluster only observable failures: missing artifact, violated boundary, stale dependency assumption, test bypass, unrecovered command failure, false completion, or human-discovered semantic defect. Preserve successful traces too.

**Week 2 — One bounded change.** Select the highest-cost recurring failure. Add one guide or sensor. Write down the causal story: “If this signal arrives before completion, the agent can correct this failure.” Keep model, task sampling, and acceptance gate fixed where possible.

**Week 3 — Challenge it.** Run known failures, known passes, and novel cases. Look for regressions, reward gaming, latency, and conflicts. Have a person who did not author the control explain what it accepts and misses.

**Week 4 — Decide.** Keep, revise, or remove the change. Version the decision. If it is model-specific, attach an expiry test to the next model upgrade. If it encodes durable product or safety intent, move it into the owning system's normal change process.

Track end-to-end outcomes, not only pass rate: human intervention, time to accepted change, unique faults caught, false alarms, escaped failures, and maintenance minutes.

## A defensible claim

The available evidence supports this statement:

> For bounded agent workflows, the surrounding execution and feedback system can materially affect observed performance, and teams need explicit stewardship of that system.

It does not yet support these stronger statements:

- harness engineering has a proven universal team structure;
- more harness is always safer;
- a self-improving harness generalizes indefinitely;
- a particular feature remains valuable across model generations;
- harness investment has a known organization-wide return.

The difference matters. A discipline is not a bundle of fashionable components. It is a repeatable way to make assumptions, evidence, costs, and responsibility visible as models and systems change.

Podcast hook: If two teams use the same model but get different results, is the model the product—or is the invisible control system around it the real engineering asset?

Continue reading: [Chapter 3 — The Apprenticeship Cliff](03-apprenticeship-cliff.md).
