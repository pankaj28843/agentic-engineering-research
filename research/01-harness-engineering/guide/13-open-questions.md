# Chapter 13 — Open questions and research agenda

**You'll learn:** which parts of harness engineering are well supported, which are still contested, and what future research should investigate before teams over-automate.

Source jumps: Böckeler's [open questions](https://martinfowler.com/articles/harness-engineering.html#AStartingPoint-AndOpenQuestions), Anthropic's [future work](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), OpenAI's [what we're still learning](https://openai.com/index/harness-engineering/), Arize's [failure analysis](https://arize.com/blog/common-ai-agent-failures/), and OWASP's [agent security risks](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html).

## What is well supported

After reading the source set, several claims are strong.

First, “model plus harness” is a useful frame. LangChain, Fowler/Thoughtworks, OpenAI, Stripe, Anthropic, HumanLayer, and practitioner sources all converge on the idea that the system around the model matters enormously. They use different language, but the pattern is consistent: tools, state, context, feedback, constraints, and human escalation shape outcomes.

Second, guides and sensors are a durable vocabulary. The feedforward/feedback distinction explains why prompt-only governance fails and why test-only correction is wasteful. The computational/inferential axis explains where deterministic tools and LLM judgement each belong.

Third, context engineering is foundational. Multiple sources warn against giant always-loaded context and endorse progressive disclosure, repo-local knowledge, durable state, and just-in-time retrieval.

Fourth, security boundaries must be engineered outside the model. OWASP, Stripe, OpenAI, Arize, and sandboxing practitioners all point toward least privilege, isolation, validation, monitoring, and approval.

Fifth, long-running agents need durable handoff artifacts. Anthropic's progress files, feature lists, git commits, and baseline tests are concrete and plausible.

## What is still weak or contested

The hardest unresolved area is functional behaviour harnessing. Maintainability can lean on existing static analysis. Architecture can lean on fitness functions. Behaviour often depends on whether generated tests actually encode the user's intent. Böckeler calls this the elephant in the room, and the source set does not solve it.

LLM evaluators are promising but not enough. Anthropic's evaluator-agent work improved some outcomes but required calibration and still missed issues. Arize recommends LLM-as-judge checks for contradictions between answers and retrieved text, but those checks are still probabilistic. If an LLM wrote the feature, an LLM wrote the tests, and an LLM judged the result, the harness needs calibration against human judgement.

Productivity economics are also contested. OpenAI's one-tenth time estimate and Stripe's thousand-plus minion PRs per week are important reports, but they come from organizations with strong incentives and unusual infrastructure. They show possibility, not baseline expectation.

Finally, harness maintenance is unsolved. As guides, sensors, skills, docs, hooks, and evaluators grow, how do teams keep them coherent? How do they detect contradictions? How do they know whether a sensor never fires because quality is high or because detection is weak? Böckeler explicitly asks for ways to evaluate harness coverage and quality, analogous to code coverage and mutation testing for tests.

## Behaviour harness research questions

Important questions:

1. When do approved fixtures work best, and when do they fail?
2. How can generated tests be audited without reading every assertion?
3. Can mutation testing reveal AI-written tests that assert the wrong behaviour?
4. How do browser automation, screenshots, DOM snapshots, and visual diffing complement each other?
5. How should LLM evaluators be calibrated against human judgement?
6. Can user analytics or production traces become safe behaviour sensors?
7. How do we express product taste as evidence rather than vague prose?
8. What is the minimum human manual testing needed at each autonomy level?

This is where future themes should spend serious time.

## Harness coverage research questions

A test suite has coverage metrics, flawed but useful. A harness needs something similar.

Possible dimensions:

- **Guide coverage:** which repeated failure modes have feedforward guidance?
- **Sensor coverage:** which critical invariants are checked computationally or inferentially?
- **Timing coverage:** are cheap checks left enough? Are expensive checks budgeted?
- **Risk coverage:** which high-risk actions have approval gates?
- **Context coverage:** can the agent discover the relevant source of truth?
- **Drift coverage:** are docs, tests, dependencies, and architecture monitored over time?
- **Behaviour coverage:** which user journeys have executable evidence?
- **Escalation coverage:** does the agent know when to stop and ask?

A practical harness audit could map known failure modes to controls:

```text
Failure mode                  Guide?   Sensor?   Timing   Owner
wrong package manager          yes      no        start    platform
forbidden import direction     yes      yes       local    architecture
UI fix not browser-tested      yes      partial   pre-PR   frontend
agent reads secrets            yes      yes       always   security
research summary too shallow   yes      yes       validate research
```

This repo's validator is moving in that direction by checking for guide files and minimum depth. That is primitive, but it encodes the lesson that shallow briefings are not acceptable final artifacts.

## Security research questions

OWASP gives a broad map, but coding-agent-specific security still needs field data.

Questions:

1. Which permission prompts actually stop bad outcomes, and which create approval fatigue?
2. How should MCP tools be scoped and audited in real developer environments?
3. What is the best sandbox boundary for local coding agents: container, VM, Bubblewrap, devbox, remote environment?
4. How can memory poisoning be detected in repo-local docs and vector stores?
5. What observability signals predict denial-of-wallet loops?
6. How should agents handle secrets needed for tests without seeing production credentials?
7. Can tool descriptions themselves become injection surfaces?
8. How do multi-agent systems prevent cascading compromise?

The safe default is to assume model-level safety is insufficient and design tool-level boundaries.

## Model improvement versus harness improvement

A recurring question is whether harness engineering will become less important as models improve. LangChain argues some harness responsibilities may be absorbed into future models: planning, self-verification, and long-horizon coherence may improve natively. Anthropic's later work suggests some scaffold pieces become less load-bearing as models change.

But this does not make harnesses disappear. Even a brilliant human developer needs a build system, tests, docs, permissions, observability, and deployment controls. Better models may reduce some compensating scaffolding, but local context, risk boundaries, business rules, and verification will remain system concerns.

The research habit should be: periodically retest which harness parts still pay rent. Do not keep a rule forever because an older model needed it. Do not remove a deterministic safety boundary because a newer model seems nicer.

## What future themes should do differently

This repository's first pass captured many sources but produced a shallow briefing. The corrected methodology should be:

1. Crawl broadly and keep raw artifacts in `tmp/`.
2. Post-process captured HTML with article extraction into clean article snapshots.
3. Read the clean article snapshots as the synthesis substrate.
4. Write a chapter-wise ELI5 guide with inline source links.
5. Include local source images when they are educational, with credits.
6. Keep the briefing as summary, not main output.
7. Build optional EPUB/Markdown reading artifacts.
8. Validate guide depth and links.
9. Record limitations and open questions.

The core project goal is not “collect research.” It is “turn fast-moving agentic engineering material into durable, personalized reading material.”

## Chapter takeaways

- Harness engineering is well supported as a frame, but behaviour verification and harness quality metrics remain open.
- Vendor case studies prove patterns more than economics.
- Future work should focus on behaviour harnesses, evaluator calibration, security boundaries, harness coverage, and maintenance.
- Better models will change harness design but not eliminate the need for local controls.
- This repo's methodology must prioritize meaty ELI5 deep dives over short summaries.

**Next:** [Chapter 14 — Two-sentence summary](14-two-sentence-summary.md).
