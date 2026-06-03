# Guide: OpenAI Harness Engineering

This guide teaches OpenAI-centered harness engineering for practitioners who already know how to run coding agents in tmux, remote shells, persistent goals, and long-running loops. It assumes you can already launch agents. The harder question here is how to shape the repository, app runtime, browser evidence, observability, review process, and cleanup loops so the agent has a real engineering environment instead of a prompt-shaped guess.

The primary source is OpenAI's February 11, 2026 post, [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/). That post reports an internal beta product built with zero manually written code, roughly a million lines, about 1,500 pull requests, per-worktree app instances, Chrome DevTools Protocol access, local observability, a repository knowledge store, custom lints, agent review, autonomy loops, and cleanup work. The guide also uses OpenAI's public [Symphony](https://github.com/openai/symphony) source, official OpenAI Codex docs, requested YouTube capsules, Ryan/X extraction, and official Anthropic comparison pages.

## What You Should Learn

Harness engineering is the discipline of designing the surroundings of an agent. In ordinary software engineering, the codebase, tests, docs, CI, logs, dashboards, browser, issue tracker, and review process are mostly built for humans. In the OpenAI story, those surfaces are redesigned so Codex can inspect them, act on them, and use their output as feedback.

An ELI5 version:

Imagine asking a child to clean a messy room. If the lights are off, the toy boxes are unlabeled, the trash can is hidden, and nobody says what "clean" means, the child guesses. If the room has labels, pictures, bins, a checklist, and a way to know when the job is done, the child can do much more. Harness engineering is turning the software "room" into a labeled, checkable place for Codex.

That analogy is useful, but the practitioner version is sharper: a good harness moves tacit human judgment into executable and inspectable artifacts. A short `AGENTS.md` tells the agent where to start. `docs/` tells it what the system believes. Worktrees isolate concurrent attempts. Browser/CDP evidence lets it see the app. Logs, metrics, and traces let it reason about runtime behavior. Lints and structural tests encode architecture. Review agents and Ralph-style loops turn feedback into iteration. Cleanup agents keep entropy from compounding.

## Chapter Map

- [01 - What OpenAI Means](01-what-openai-means.md): the experiment, the frame, and why this is not just prompting.
- [02 - Legible Apps And Browsers](02-legible-apps-and-browsers.md): per-worktree apps, browser/CDP validation, local observability, and visual evidence.
- [03 - Repository Knowledge](03-repository-knowledge.md): short `AGENTS.md`, system-of-record docs, progressive disclosure, plans, and knowledge drift.
- [04 - Invariants And Lints](04-invariants-and-lints.md): architecture, taste, domain layers, boundary parsing, custom lint messages, and CI.
- [05 - Review And Ralph Loops](05-review-and-ralph-loops.md): agent-to-agent review, pushback, merge philosophy, long loops, and human attention.
- [06 - Symphony Orchestration](06-symphony-orchestration.md): what the public OpenAI Symphony source teaches about scheduling work.
- [07 - Video And Social Evidence](07-video-and-social-evidence.md): transcript-weighted synthesis of the requested videos and X extraction.
- [08 - Replication Playbook](08-replication-playbook.md): Linux/macOS implementation steps for a serious local harness.
- [09 - Capabilities, Costs, And Unknowns](09-capabilities-costs-and-unknowns.md): current official product surfaces, USD 200/month comparison, safety, and open questions.

## How To Read This

Read chapters 01 through 05 if you want the mental model. Read chapter 08 if you want to implement. Read chapter 09 before spending money or increasing autonomy. If you are refreshing the packet later, start from [source-index.md](../source-index.md) and [research-log.md](../research-log.md), not from memory.

The guide uses a strict evidence rule: OpenAI and Anthropic official claims are treated as vendor evidence, public Symphony code as source-code evidence, transcripts as practitioner evidence, X and comments as weak social signal, and search snippets as leads only. Where a claim is an inference, it is labeled as such.

