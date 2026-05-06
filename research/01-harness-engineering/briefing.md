# Briefing: Harness Engineering for Coding Agent Users

## Verdict

Harness engineering is emerging as the practical discipline for making coding agents useful beyond toy tasks. The most robust pattern across sources is a control loop:

```text
human intent
  -> feedforward guides: AGENTS.md, skills, specs, examples, architecture rules
  -> agent work in a constrained environment
  -> feedback sensors: tests, linters, browser checks, traces, reviewers, evaluators
  -> harness update: encode the lesson in docs, tools, tests, or rules
```

Confidence: **high** for the control-loop framing; **medium** for claims of very large productivity multipliers; **high** that naive autonomy degrades without deterministic verification, sandboxing, and explicit human escalation.

## Claims assessed

### 1. "Agent = model + harness" is useful but too broad unless bounded

LangChain states the broadest definition directly: a raw model becomes an agent when a harness gives it state, tool execution, feedback loops, and enforceable constraints. Its component list includes system prompts, tools, skills, MCPs, filesystem, sandbox, browser, orchestration, handoffs, hooks, compaction, continuation, and lint checks.

Fowler/Thoughtworks narrows that frame for coding-agent users. Built-in product harnesses already exist, but users and teams build an *outer harness* for their repo, workflow, and risk profile. This narrower frame is more useful for this repository because it connects directly to files, tests, source indices, CDP artifacts, and validation commands.

Assessment: **well-supported**. The term is broad, but the bounded coding-agent context prevents it from becoming meaningless.

### 2. Harnesses need both feedforward guides and feedback sensors

Böckeler's core distinction is durable: guides steer before action; sensors observe after action and let agents self-correct. She also separates computational controls (tests, linters, type checks, structural analysis) from inferential controls (LLM review, LLM-as-judge, semantic critique). The important warning is that either half alone fails: feedback-only agents repeat mistakes; feedforward-only agents encode rules without learning whether they worked.

OpenAI and Stripe independently report the same shape in production terms. OpenAI describes a short `AGENTS.md` as a table of contents, a structured in-repo knowledge base, custom linters, structural tests, browser/DOM/screenshot tooling, and observability. Stripe describes minions running in isolated devboxes, using deterministic git/lint/test orchestration around an agent loop, and shifting feedback left with local checks before bounded CI retries.

Assessment: **strongly supported** by multiple independent practitioner accounts, though OpenAI/Stripe are also promoting their own agentic tooling investments.

### 3. Context engineering is the substrate; harness engineering is the control system

Fowler describes context engineering as the means for making guides and sensors available to the agent. Anthropic frames context as a finite attention budget and recommends high-signal minimal context, just-in-time retrieval, compaction, structured note-taking, and sub-agent architectures. This explains why a giant instruction file is an anti-pattern: it consumes attention while degrading navigability and freshness.

OpenAI's in-repository knowledge store reinforces the same lesson: `AGENTS.md` should be a map, not an encyclopedia. Documentation, plans, generated references, quality scores, reliability docs, and security docs become the system of record, with mechanical checks to keep them fresh.

Assessment: **strongly supported**. For this repo, the implementation consequence is: keep `AGENTS.md` short, put durable synthesis in `docs/` and `research/`, and put raw extraction artifacts in gitignored `tmp/`.

### 4. The human role moves from "in the loop" to "on the loop"

Kief Morris argues that humans should focus on building and managing the working loop rather than either leaving agents unsupervised or inspecting every line. The difference is what happens after dissatisfaction: "in the loop" fixes the artifact; "on the loop" changes the harness that produced it.

OpenAI echoes this with "Humans steer. Agents execute." Their reported human work is specifying intent, designing environments, encoding feedback loops, and adding missing capabilities. Simon Willison adds a practical anti-pattern: do not inflict unreviewed agent code on collaborators; the author must validate code, PR descriptions, screenshots, and testing evidence before asking others to review.

Assessment: **well-supported**, with a hard boundary: humans can move up a level only when verification is strong enough for the risk of the change.

### 5. Long-running agents need durable state, clean handoffs, and scoped increments

Anthropic's November 2025 harness used an initializer agent plus coding agents. The initializer creates an `init.sh`, a progress file, an initial git commit, and a structured JSON feature list. Coding agents work one feature at a time, commit progress, update notes, and self-verify with browser automation. Their observed failure modes were one-shotting too much, running out of context with half-implemented work, and declaring the project done too early.

Anthropic's March 2026 follow-up adds stronger skepticism about self-evaluation. Separating generator and evaluator agents, negotiating sprint contracts, and using Playwright-based evaluators improved outcomes but introduced large cost and latency. Later model improvements made some scaffold pieces less load-bearing, which supports a key maintenance principle: re-test which harness parts still matter as models improve.

Assessment: **strongly supported** for long-horizon coding and research; **cost-sensitive** and not automatically worth it for small tasks.

### 6. Behavior harnessing remains the hardest gap

Böckeler calls functional behavior the elephant in the room: AI-generated tests being green is not enough, and manual testing still appears in most high-autonomy workflows. The approved fixtures / approved scenarios pattern offers one mitigation: design domain-readable fixture files that combine input and expected output so humans review fixture diffs rather than complex assertion code.

Anthropic's evaluator-agent work and Stripe's browser/CI loops are credible movement toward behavior harnessing, but both show limits. Anthropic's frontend evaluator required calibration and still missed layout and nested feature issues. Stripe caps CI retries because marginal returns decline.

Assessment: **contested and unsolved**. Behavior harness quality is the main place future research should focus.

### 7. Security is harness design, not model politeness

OWASP's AI Agent Security Cheat Sheet lists prompt injection, tool abuse, data exfiltration, memory poisoning, excessive autonomy, cascading failures, denial of wallet, and supply-chain attacks as core risks. Its recommended controls are least-privilege tools, input validation, memory isolation, explicit human approval for high-risk actions, output validation, monitoring, and secure multi-agent communication.

Arize's production-failure analysis adds operational failure modes: retrieval noise, hallucinated tool arguments, recursive loops, guardrail failures, pre-training bias overriding retrieved context, schema drift, instruction drift, and destructive code generation. Patrick McCanna's Bubblewrap writeup is a practitioner argument for wrapping coding agents in operating-system controls rather than relying on vendor implementation choices.

Stripe's devboxes are a scaled version of the same idea: isolated, pre-warmed environments without production resources or internet access.

Assessment: **strongly supported**. This repo therefore codifies a CDP daemon human-in-the-loop guard in `AGENTS.md`: only `cdp daemon status --json` is allowed unattended; daemon start/restart/keepalive/active-probe require explicit human approval.

### 8. Vendor success stories are real evidence, but not neutral evidence

OpenAI reports a million-line, agent-generated internal product, 1,500 PRs, and roughly one-tenth the time of hand-written code. Stripe reports more than a thousand minion-produced PRs per week. These are important primary sources because they describe real systems with users, CI, dev environments, observability, and failure handling.

But they are not neutral. Both organizations sell or benefit from agentic tooling narratives, and both operate at unusual scale with unusual internal tooling. Their lessons generalize better as patterns than as ROI estimates.

Community signals add skepticism. HN threads around Simon Willison, Fowler, Anthropic, and coding agents show interest but also concern about code review burden, sandboxing, context, and slop. The local socli pass surfaced a Reddit discussion of SlopCodeBench claiming long-horizon agent code degrades across repeated edits and a Meta-Harness discussion arguing that harnesses themselves may need automated improvement loops.

Assessment: **patterns generalize; numbers do not yet generalize**.

## What changed after pages 2-3 of Google results

The first page mostly confirmed the canonical story: Fowler, Simon Willison, Anthropic, LangChain, OpenAI, and Stripe. Pages 2-3 changed the research shape in four ways:

1. Surfaced HN threads and community dissent that made the report more skeptical.
2. Surfaced GitHub and GitHub Blog material about `AGENTS.md`, custom instructions, and agent rule files, which directly informed this repo's setup.
3. Surfaced OWASP and sandboxing/security sources that shifted the repo from "research workflow" toward explicit human-in-the-loop daemon and tool-boundary rules.
4. Surfaced implementation lists and harness repositories, useful as future prior art but too noisy to treat as proof.

## Source signals

- **Primary/official:** Fowler/Thoughtworks, Anthropic Engineering, OpenAI, Stripe, GitHub Blog, OWASP, uv docs, Chrome/CDP docs.
- **Practitioner:** Simon Willison, Addy Osmani, Patrick McCanna, Approved Scenarios pattern.
- **Vendor/practitioner:** LangChain, Arize, Cursor, Parallel.
- **Community:** HN threads and local socli Reddit/X signals.
- **Reference:** Cybernetics and requisite variety background.

## Failure modes to watch

1. **Monolithic AGENTS.md:** too much guidance becomes non-guidance and rots quickly.
2. **Prompt-only governance:** rules without executable checks do not reliably prevent drift.
3. **Feedback-only loops:** agents may repeat the same mistake or spiral through expensive retries.
4. **AI-generated tests as false confidence:** green tests can encode the wrong behavior.
5. **Evaluator leniency:** LLM evaluators need calibration and should be checked against human judgment.
6. **Instruction drift and context rot:** long sessions bury critical constraints unless pinned, compacted, or rediscovered.
7. **Over-permissioned tools:** shell, filesystem, browser, MCP, and network access need least privilege and audit trails.
8. **Vendor-incentive blindness:** productivity claims require triangulation with failure reports and independent evidence.

## Implications for this repository

- `AGENTS.md` is a table of contents and safety contract, not the research corpus.
- `tmp/` is the scratch substrate for CDP and web extraction; durable theme outputs live under `research/`.
- Repo-local skills encode repeatable research workflows and source audits.
- `uv` provides a reproducible validation path without committing bulky artifacts.
- Every theme should include both positive evidence and skeptical counter-evidence.

## Bottom line

Harness engineering is best understood as cybernetic software engineering for coding agents: reduce uncontrolled variety, expose high-signal context, add deterministic sensors where possible, use inferential sensors where necessary, keep humans at the leverage points, and continuously improve the harness when failures repeat.
