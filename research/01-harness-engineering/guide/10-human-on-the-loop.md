# Chapter 10 — Human on the loop

**You'll learn:** why harness engineering changes the human role, what “on the loop” means, and how to avoid both blind autonomy and line-by-line micromanagement.

Source jumps: Böckeler's [The role of the human](https://martinfowler.com/articles/harness-engineering.html#TheRoleOfTheHuman), Fowler/Thoughtworks [Humans and Agents in Software Engineering Loops](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html), OpenAI's [Humans steer. Agents execute](https://openai.com/index/harness-engineering/), and Simon Willison's [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/).

## The false choice

People often frame coding agents as a choice between two bad extremes:

1. Let the agent run unsupervised and hope.
2. Inspect every generated line as if it were written by a careless intern.

Harness engineering offers a third posture. The human does not disappear, and the human does not review by brute force forever. The human steers the loop: specify intent, shape the environment, design feedback, inspect evidence, decide trade-offs, and update the harness when failures repeat.

Kief Morris's “on the loop” framing, echoed in the Thoughtworks material, is useful. “In the loop” means the human intervenes inside each work item. “On the loop” means the human manages the system that produces work items. If an agent makes the same mistake repeatedly, an in-the-loop human fixes the artifact again. An on-the-loop human changes the harness so the mistake becomes less likely or easier to catch.

## What humans bring that agents do not

Böckeler's main article is strong here. Human developers carry an implicit harness inside themselves. We know conventions. We feel the cognitive pain of complexity. We know our name is on the commit. We have social accountability. We understand which technical debt is tolerated for business reasons. We can sense that technically correct code may be wrong for the team.

A coding agent has none of that by default. It has no aesthetic disgust at a 300-line function. It does not know which convention is load-bearing and which is accidental. It does not know the organization's current priorities unless the harness exposes them. It may produce code that is locally plausible and globally misaligned.

Harnesses try to externalize part of human experience: rules, examples, tests, architecture boundaries, product specs, review checklists, quality scores, and escalation paths. But this can only go so far. Some judgement remains human.

## Steering work, not typing work

OpenAI's statement “Humans steer. Agents execute.” can sound like marketing, but the concrete work they describe is real engineering:

- Translate user feedback into acceptance criteria.
- Prioritize work.
- Design environments.
- Encode feedback loops.
- Add missing tools and guardrails.
- Capture human taste into docs or linters.
- Decide where constraints matter and where local autonomy is okay.
- Validate outcomes.

This is not less engineering. It is engineering at a different layer. A developer may type fewer implementation lines but spend more time designing the system that makes implementation reliable.

Stripe's minions preserve human review for PRs. OpenAI says humans may review PRs but pushed much review effort toward agent-to-agent checks. The right balance depends on risk, verification, team maturity, and failure cost. A payments system and a personal toy app should not have the same autonomy level.

## Evidence changes review

A human reviewing agent output should not be asked to reconstruct everything from scratch. The harness should produce an evidence bundle:

- The original task/spec.
- The plan or feature item chosen.
- The diff.
- Commands run and outputs.
- Browser screenshots or videos for UI changes.
- Test/lint/typecheck results.
- Known risks or skipped checks.
- Source links for research claims.
- Any human approvals requested.

Simon Willison's patterns are useful here. In [linear walkthroughs](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/), he asks agents to generate structured explanations with actual snippets pulled by tools, reducing hallucinated explanation risk. In his broader [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/), he repeatedly emphasizes using agents to create better understanding, tests, and review artifacts. The point is not only to produce code faster. It is to produce artifacts that make human judgement cheaper and better.

This guide itself follows that principle: every chapter has source jumps so you can inspect the original article behind the synthesis.

## The harness update loop

The human-on-the-loop move is clearest after a failure.

Suppose a reviewer sees an agent PR that adds a workaround instead of diagnosing the root cause. The weak response is to comment “please don't do this” and move on. The harness response asks:

- Was the task too vague?
- Did the agent lack debugging instructions?
- Did it skip reading logs?
- Is there a test that would force root-cause correctness?
- Should a reviewer skill flag brute-force fixes?
- Should docs explain the subsystem's intended design?
- Did the error message mislead the agent?

Then the team improves a guide or sensor. Over time, repeated review comments become durable controls.

This is a ratchet. Each real failure should leave the harness slightly better. Not every weird one-off deserves a rule. But repeated failures should not remain tribal knowledge.

## Avoiding harness bloat

There is a danger: if every failure becomes another paragraph in `AGENTS.md`, the harness becomes sludge. OpenAI's giant `AGENTS.md` failure is the warning. Humans on the loop must also prune.

Good pruning questions:

- Is this rule still needed with current models?
- Is it repeated enough to justify permanent guidance?
- Can a deterministic check replace prose?
- Can the rule move to a task-specific skill instead of always-loaded context?
- Is the source still true?
- Does this conflict with another rule?
- Is this preference or a real invariant?

Harness engineering is not accumulating instructions. It is maintaining a coherent control system.

## Skills as human leverage

Böckeler's context memo describes skills as lazy-loaded packages of guidance, instructions, docs, and scripts. Skills are a way to preserve human expertise without stuffing it into every session. A security review skill can include the exact scan commands and threat model checklist. A refactoring skill can include project-specific patterns. A browser verification skill can explain how to capture screenshots and console logs.

The best skills are written from repeated practice. They answer: “When a human expert does this task well, what steps, checks, and judgement points do they use?” They should include commands and failure handling, not just vague advice.

This repo's local skills need to evolve the same way. The original `theme-deep-research` skill produced a short briefing and source index. The new expectation is a book-grade ELI5 guide. That is a harness update caused by a real failure: the output did not justify the research cost.

## Human responsibility remains

A subtle trap is using harness language to dodge responsibility. “The agent wrote it” is not an excuse. If a human asks an agent to produce a PR and merges it, the human and team own the result. Willison has warned against dumping unreviewed AI slop onto collaborators. The person using the agent should validate the artifact, not outsource review burden to others.

Harnesses reduce the amount of manual inspection needed for low-risk, well-sensed work. They do not remove accountability. The more autonomy you grant, the stronger your evidence, rollback, audit, and approval paths must be.

## A personal workflow for being on the loop

For an individual developer using coding agents:

1. Start with a clear task and acceptance criteria.
2. Ask the agent to plan before editing.
3. Keep tasks small enough to review.
4. Require tests or evidence before “done.”
5. Review the diff and generated evidence.
6. Note repeated failures.
7. Promote repeated failures into docs, tests, hooks, or skills.
8. Remove obsolete guidance.
9. Never ask teammates to review unvalidated agent output.
10. Keep a log of harness improvements.

For a team, add ownership, CI integration, risk classification, and periodic harness audits.

## Chapter takeaways

- “On the loop” means managing the system that produces work, not inspecting every line forever.
- Humans bring judgement, taste, accountability, organizational memory, and trade-off awareness.
- Good harnesses convert human judgement into guides, sensors, skills, checks, and evidence bundles.
- Harness bloat is real; prune and prefer executable checks over prose where possible.
- Humans remain responsible for agent-produced artifacts.

**Next:** [Chapter 11 — Build your first harness](11-build-your-first-harness.md).
