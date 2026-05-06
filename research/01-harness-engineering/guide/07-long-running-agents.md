# Chapter 07 — Long-running agents

**You'll learn:** why long-running agents fail across context windows, how Anthropic's initializer/coding-agent pattern works, and which durable artifacts let agents resume without guessing.

Source jumps: Anthropic's [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), Anthropic's [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps), LangChain's [long horizon autonomous execution](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness), and OpenAI's [six-hour Codex runs](https://openai.com/index/harness-engineering/).

## The shift-worker problem

Anthropic explains long-running agent work with a useful analogy: imagine a software project staffed by engineers working in shifts, where each new engineer arrives with no memory of the previous shift. That is what happens when a task spans multiple context windows. Each new session starts with limited memory, imperfect compaction, and no lived experience of the previous attempts.

This matters because complex coding tasks can take hours or days. The agent may need to build several features, run the app, fix bugs, write tests, update docs, and recover from mistakes. If all state lives in the chat transcript, the task becomes fragile. The transcript fills, compaction loses nuance, and the next agent has to infer what happened from half-finished files.

Anthropic observed two major failure modes when asking Claude to build a production-quality web app from a high-level prompt like “build a clone of claude.ai.” First, the agent tried to do too much at once, ran out of context mid-implementation, and left half-implemented undocumented work. Second, later sessions saw partial progress and prematurely declared the project done.

Those are not just model failures. They are harness failures: the environment did not force incremental progress, durable handoff, or clear completion criteria.

## Anthropic's two-part solution

Anthropic's public solution has two roles:

1. **Initializer agent:** the first session sets up the environment.
2. **Coding agent:** every later session makes incremental progress and leaves structured updates.

The initializer creates artifacts future agents need:

- `init.sh` to start the development server or run setup.
- `claude-progress.txt` to log what agents have done.
- An initial git commit showing the starting state.
- A structured feature list expanding the user's prompt into end-to-end requirements.

The coding agent starts by getting bearings, reading progress notes, reading the feature list, inspecting git history, running the app, and verifying basic functionality. Then it chooses one not-yet-passing feature, implements it, tests it, commits progress, and updates the progress file.

This is harness engineering because the harness changes the shape of work. It does not ask the model to “be more careful.” It gives the model durable rails.

## The feature list as anti-one-shot control

The most interesting artifact is the structured feature list. In Anthropic's clone example, the initializer created over 200 features. Each feature had a description, steps, and a `passes` field initially set to false. Later agents were instructed to change only the pass status after careful testing, not rewrite or remove tests.

A simplified version:

```json
{
  "category": "functional",
  "description": "New chat button creates a fresh conversation",
  "steps": [
    "Navigate to main interface",
    "Click the New Chat button",
    "Verify a new conversation is created",
    "Check that chat area shows welcome state",
    "Verify conversation appears in sidebar"
  ],
  "passes": false
}
```

This fights two failures at once. It prevents one-shotting because the agent has a list of small user-visible behaviours. It prevents premature victory because many features remain explicitly failing until tested. Anthropic found JSON worked better than Markdown because the model was less likely to casually rewrite it.

The broader lesson is not “always use JSON.” The lesson is: long tasks need a durable, reviewable representation of remaining work.

## Clean state and git commits

Anthropic defines a clean state as code appropriate for merging to main: no major bugs, orderly, documented, and easy for the next developer to continue. Asking the agent to leave a clean state is not enough; the harness backs it with git commits and progress notes.

Git commits do several jobs:

- Mark a known working point.
- Let later agents inspect what changed.
- Allow rollback when a change goes bad.
- Provide a compact history outside the chat transcript.
- Encourage smaller increments.

Progress notes do a different job. They tell the next session what was attempted, what worked, what remains, and any caveats. Without them, a fresh agent wastes time rediscovering state or accidentally building on a broken assumption.

This pattern is useful beyond autonomous app building. Any multi-session research or refactoring task benefits from a plan file, progress log, and commit discipline.

## Testing like a human user

Anthropic observed that Claude often marked features complete without proper end-to-end testing. It might run unit tests or curl a development server but miss that the feature did not work as a user would experience it. Explicit prompting to use browser automation tools and test as a human user dramatically improved performance.

That detail connects directly to behaviour harnessing. Code-level tests are not enough for many features. The agent needs tools that expose the product surface: browser automation, screenshots, DOM inspection, console logs, and possibly visual comparison. OpenAI's Codex harness makes the same move with Chrome DevTools Protocol. Stripe's minions focus more on developer tooling and CI, but the principle is similar: use the same tools humans use, exposed in agent-legible ways.

Browser testing still has limits. Anthropic notes issues like browser-native alert modals that Puppeteer MCP could not see. Vision can miss layout problems. Automated flows may not cover weird interactions. So browser tools reduce supervision but do not eliminate it.

## The “getting up to speed” ritual

Anthropic gives a concrete session-start ritual:

```text
1. Run pwd to see the working directory.
2. Read progress notes.
3. Read feature list.
4. Inspect recent git log.
5. Read init.sh.
6. Start the app.
7. Verify basic functionality before new work.
8. Choose one not-yet-done feature.
```

This ritual looks almost too basic, but it matters. Agents are prone to local optimism. They may start coding before verifying that the app is already broken. If they build on a broken state, they make the problem worse. A harness should force a baseline check before new work.

For this research repo, the equivalent ritual is: read `AGENTS.md`, inspect the theme README, read source metadata, regenerate article snapshots if needed, update the chapter plan, write one coherent increment, run validation, and leave research-log notes. Long-running research has the same handoff problem as long-running coding.

## Continuation loops and the danger of “done”

LangChain discusses continuation patterns such as “Ralph loops,” where the harness intercepts an agent's attempt to stop and reinjects the original goal in a fresh context. OpenAI mentions a Ralph Wiggum Loop for PR completion: Codex reviews its own changes, requests additional reviews, responds to feedback, and iterates until reviewers are satisfied.

Continuation is powerful but risky. If the completion criteria are vague, the agent may loop wastefully. If the goal is too broad, it may keep generating low-value work. If there is no budget, costs can explode. If sensors are weak, it may converge on green but wrong.

The safe version combines continuation with:

- Clear completion criteria.
- Small increments.
- Durable state.
- Bounded retries.
- Escalation to humans when judgement is required.
- Evidence of verification.

Stripe's at-most-two CI rounds are a good example of bounded continuation. Anthropic's one-feature-at-a-time instruction is another.

## Single agent or multi-agent?

Anthropic lists an open question: does a single general-purpose coding agent perform best across contexts, or do specialized agents improve outcomes? Testing agent, QA agent, cleanup agent, architecture reviewer, and product-sense reviewer are plausible roles. OpenAI already uses agent-to-agent review and cleanup tasks. Many frameworks advertise multi-agent systems.

The harness lesson is to specialize only when specialization changes behaviour. A “reviewer agent” is useful if it has different instructions, tools, model, context, or authority than the coding agent. If it is just the same model saying “looks good,” it adds cost without control.

A practical split:

- Planner: decomposes work and updates plan.
- Implementer: edits code.
- Verifier: runs tests and browser checks.
- Reviewer: critiques diff against standards.
- Janitor: scans for drift and stale docs.
- Human: decides ambiguous trade-offs and risk.

Each role needs clear inputs and outputs. Otherwise multi-agent becomes multi-confusion.

## Long-running harness checklist

For any long task, ask:

1. What file records the goal and acceptance criteria?
2. What file records progress and decisions?
3. What command restores the working environment?
4. What test proves the baseline is not already broken?
5. How does the agent choose the next small increment?
6. What must be true before the agent marks an item done?
7. How often does it commit?
8. How does it recover from a bad change?
9. What budget caps retries?
10. When does it escalate to a human?

If these answers are missing, long-running autonomy will be fragile.

## Chapter takeaways

- Long-running agents fail when state lives only in the context window.
- Anthropic's initializer/coding-agent pattern uses durable files, feature lists, progress notes, git commits, and browser verification.
- One-feature-at-a-time work fights one-shotting and premature completion.
- Browser automation improves behaviour checks but has limits.
- Continuation loops need budgets, evidence, and human escalation.

**Next:** [Chapter 08 — Production case studies](08-production-case-studies.md).
