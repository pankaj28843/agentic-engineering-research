# Chapter 06 — Maintainability, architecture, and behaviour harnesses

**You'll learn:** the three harness categories in the Fowler article, why maintainability is easiest, why architecture fitness is promising, and why functional behaviour remains the hardest gap.

Source jumps: Böckeler's [regulation categories](https://martinfowler.com/articles/harness-engineering.html#RegulationCategories), Thoughtworks' [Architectural fitness function](https://www.thoughtworks.com/en-de/radar/techniques/architectural-fitness-function), the [approved fixtures](https://lexler.github.io/augmented-coding-patterns/patterns/approved-fixtures/) pattern, and OpenAI's [architecture enforcement](https://openai.com/index/harness-engineering/).

![Fowler harness types diagram showing maintainability, architecture fitness, and behaviour as separate regulation dimensions.](../assets/fowler/harness-types.png)

Image credit: Birgitta Böckeler, [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html). Local copy documented in [assets/README.md](../assets/README.md).

## Harnesses regulate different things

Böckeler describes the agent harness as a cybernetic governor: it combines feedforward and feedback to regulate the codebase toward a desired state. But “desired state” is not one thing. You might want the code to be maintainable, the architecture to stay coherent, and the application to behave correctly for users. Those are related but different.

She names three useful categories:

1. **Maintainability harness** — regulates internal code quality.
2. **Architecture fitness harness** — regulates architectural characteristics.
3. **Behaviour harness** — regulates functional behaviour from the user's point of view.

This categorization matters because each category has different harnessability. Some code qualities are easy to sense with existing tools. Some architectural qualities can be turned into structural rules. Functional behaviour often requires domain judgement and remains much harder.

## Maintainability harness: easiest, not easy

Maintainability includes duplicate code, complexity, test coverage, style, naming, file size, dependency hygiene, dead code, and local readability. This is the easiest category because software teams already have many computational sensors:

- Formatters.
- Linters.
- Type checkers.
- Complexity metrics.
- Test coverage.
- Dependency scanners.
- Dead code detectors.
- Static analysis.
- Code search rules.

For coding agents, these tools become more valuable. Agents can produce a lot of code quickly, including repetitive or over-complicated code. A human reviewer does not want to say “this file is too big” one hundred times. A file-size lint can say it every time, cheaply and consistently.

OpenAI's Codex team reports enforcing structured logging, naming conventions, schema/type naming, file size limits, platform reliability requirements, and dependency directions with custom lints. They also run recurring cleanup agents to scan for drift and open refactoring PRs. This is a maintainability harness in production form.

But maintainability is not fully solved. Böckeler notes that LLMs can partially address semantic problems such as semantically duplicate code, redundant tests, brute-force fixes, or over-engineered solutions, but this is expensive and probabilistic. Some high-impact problems remain difficult: misdiagnosing the issue, adding unnecessary features, or misunderstanding instructions. A maintainability harness reduces toil; it does not remove judgement.

## Architecture fitness harness: making “good architecture” executable

Architecture fitness functions come from evolutionary architecture. Thoughtworks' [Radar entry](https://www.thoughtworks.com/en-de/radar/techniques/architectural-fitness-function) defines a fitness function as an objective integrity assessment of architectural characteristics, potentially using unit tests, metrics, monitors, and other verification criteria. In plain English: if architecture says “services must not depend on UI,” a fitness function checks that rule continuously.

For agents, architecture fitness functions are powerful because agents are pattern machines. If the repo contains drift, the agent may copy the drift. If boundaries are implicit, the agent may cross them. If the architecture is executable, the agent gets feedback early.

Examples:

- Dependency direction rules: domain cannot import infrastructure; service cannot import UI.
- Layer rules: Types → Config → Repo → Service → Runtime → UI, with only allowed edges.
- Performance fitness: a critical path must stay under a latency threshold.
- Observability fitness: new service code must emit structured logs with required fields.
- Security fitness: routes touching PII must pass authorization middleware.
- Data boundary fitness: external inputs must be parsed at boundaries.

OpenAI's architecture model is a vivid case. Each business domain has fixed layers and validated dependency directions. Cross-cutting concerns enter through explicit providers. The team says this kind of rigidity might normally be postponed until an organization has hundreds of engineers, but with agents it becomes an early prerequisite. The constraints allow speed without decay.

## Behaviour harness: the elephant in the room

The behaviour harness asks: does the application do what users need? This is the hardest category because the agent can generate both the code and the tests. If the agent misunderstands the requirement, it may write tests that confirm the misunderstanding. Green tests become false confidence.

Böckeler describes the current common pattern for high-autonomy coding agents:

- Feedforward: a functional specification, from a short prompt to multi-file specs.
- Feedback: check that the AI-generated test suite is green, maybe has coverage, maybe survives mutation testing, and then combine with manual testing.

Her judgement is blunt: too much faith in AI-generated tests is not good enough yet.

Anthropic's long-running agent article shows a partial mitigation for web apps: explicitly prompt the agent to test as a human user would using browser automation tools. Their Claude app clone improved when Claude used Puppeteer MCP to test end-to-end features, take screenshots, and identify bugs that were not obvious from code alone. But limitations remained: browser automation and model vision can miss some bugs, such as browser-native alert modals.

## Approved fixtures as a behaviour bridge

The [approved fixtures](https://lexler.github.io/augmented-coding-patterns/patterns/approved-fixtures/) pattern is useful because it changes what humans review. Instead of asking humans to inspect complicated assertion code, you design fixtures that show input and expected output in a domain-readable format. The test runner reads fixtures, executes code, regenerates actual output, and validation becomes a diff review.

For example, a checkout fixture can show:

```markdown
## Input
User: premium_member
Cart: laptop + mouse
Discount code: SAVE20

## Service Calls
POST /inventory/reserve -> 200 reservation_id
GET /pricing/calculate -> subtotal, discount, total
POST /payment/process -> transaction_id

## Output
Order: confirmed
Total: $1000
Email sent: order_confirmation
```

A human can review that diff more easily than generated test code. The pattern works especially well when the domain has an intuitive representation: visual algorithms, call sequences, transformations, refactorings, generated documents, or structured business flows.

It is not a wholesale answer. Some behaviours are hard to fixture. Some require real external systems, accessibility judgement, human taste, or product sense. But approved fixtures show the kind of direction behaviour harnessing needs: make expected behaviour inspectable at the right level of abstraction.

## Harnessability: not every codebase is equal

Böckeler introduces “harnessability”: how amenable a codebase is to being governed by guides and sensors. A strongly typed language gives a free type-checking sensor. Clear module boundaries make architecture rules possible. Frameworks that abstract complexity reduce what the agent has to reason about. Boring, stable technologies are often more legible to agents.

Legacy systems with high entropy are harder. If there are no clear boundaries, no reliable tests, no standard way to run the app, and no trustworthy docs, the harness is most needed where it is hardest to build. This is a painful but important point. Harness engineering is not just “add agents.” It may require paying down technical debt so the environment becomes legible enough for agents and humans.

OpenAI draws a similar conclusion with “agent legibility.” The team favored dependencies and abstractions Codex could reason about in-repo. Sometimes it was cheaper to reimplement a subset of functionality than to depend on opaque upstream behaviour. That trade-off would be questionable in a human-only team, but it can make sense if agent legibility is a primary goal.

## Harness templates and topologies

Böckeler speculates that harness templates may become the next service templates. Many enterprises already have common service topologies: CRUD business service, event processor, data dashboard, internal tool. A harness template would bundle guides and sensors for a topology: architecture docs, scaffolding scripts, lint rules, tests, observability conventions, security defaults, and workflow skills.

![Fowler harness template diagram showing topology-specific bundles of guides and sensors.](../assets/fowler/harness-templates.png)

Image credit: Birgitta Böckeler, [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html).

This is attractive because it reduces variety. If every service is a snowflake, the harness must model endless possibilities. If services follow a few topologies, the harness can be stronger. But service templates already have versioning and synchronization problems: teams fork them and drift from upstream improvements. Harness templates would inherit that problem, with the added difficulty that some controls are nondeterministic and harder to test.

## A maturity path

A realistic harness maturity path looks like this:

1. **Make the repo runnable.** One command to install, one command to test, one command to lint.
2. **Write a short map.** `AGENTS.md` points to docs and commands.
3. **Add maintainability sensors.** Format, type, lint, test, coverage, dependency checks.
4. **Add architecture sensors.** Import rules, package boundaries, schema boundary checks.
5. **Add behaviour evidence.** Browser smoke tests, approved fixtures, user-path checks.
6. **Add continuous sensors.** Drift detection, stale docs, dead code, runtime anomalies.
7. **Template what repeats.** Promote repeated service shapes into harness templates.

Do not start by designing a grand harness for everything. Start where repeated failures are most expensive.

## Chapter takeaways

- Maintainability harnesses are easiest because many computational tools already exist.
- Architecture fitness harnesses turn architectural intent into executable checks.
- Behaviour harnessing is the hardest unsolved area because generated tests can encode generated misunderstandings.
- Approved fixtures help by making expected behaviour reviewable as domain-readable diffs.
- Harnessability depends on codebase structure, technology choices, tests, docs, and ambient affordances.

**Next:** [Chapter 07 — Long-running agents](07-long-running-agents.md).
