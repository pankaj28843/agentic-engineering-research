# 13. How to read and refresh the source set

This research packet is not a timeless verdict. It is a snapshot of several fast-moving surfaces: LiteLLM gateway support, Claude Desktop third-party inference, Anthropic computer-use beta tools, Codex Desktop computer use, and open-source desktop-control runtimes. The source set should be refreshed before any serious implementation decision.

The most important reading habit is to preserve the distinction between source types. Official docs define supported contracts. GitHub issues reveal failures and edge cases. Practitioner writeups show how systems break in the wild. HN threads and social posts reveal interest and skepticism, but they are leads until verified. Local setup inspection explains what this machine is actually running.

## Source quality ladder

Use this ladder when deciding how much weight to give a claim:

1. Official vendor documentation for the exact feature and date.
2. Source code or configuration in the relevant local project.
3. Official repository README or maintained examples.
4. GitHub issues with maintainer responses or reproducible logs.
5. Practitioner writeups with concrete steps, versions, and artifacts.
6. HN/social discussion that links to primary evidence.
7. Search snippets, AI summaries, or secondhand claims.

Search snippets and AI summaries are not durable evidence. They can be used to discover sources, but final claims should cite the page, repository, issue, or local file that actually supports the claim.

The source index for this theme is intentionally mixed. It includes official LiteLLM docs for Claude Desktop/Cowork and Claude Code, Anthropic docs for computer use, OpenAI docs for Codex app computer use, GitHub repositories for open-source runtime comparisons, GitHub issues for failure modes, and practitioner/security writeups such as ZombAIs. That mix is useful only if each source is read in its proper role.

## Read official docs first

Start every refresh with official docs, because they define the intended contract.

For LiteLLM, read the Claude Code and Claude Desktop/Cowork docs first. The Claude Code page explains how Claude Code can use `ANTHROPIC_BASE_URL` and an auth token against LiteLLM ([LiteLLM Claude Code quickstart](https://docs.litellm.ai/docs/tutorials/claude_responses_api)). The Desktop/Cowork page explains Developer Mode, third-party inference settings, gateway URL, virtual key, restart, and dashboard verification ([LiteLLM Claude Desktop integration](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork)). Those docs are the basis for treating Desktop text routing as feasible.

For Anthropic, read the computer-use docs next. They define the beta header, versioned tool types, screenshot/action loop, `tool_result` continuation, and safety guidance ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). If the beta name, tool version, or model support changes, update this guide before running experiments.

For Codex Desktop, read the current Codex app computer-use docs and then compare them with recent GitHub issues. Product docs say what should happen. Issues show what actually fails for users. Keep those two evidence streams separate.

## Verify local setup after reading docs

Official docs say what is supported in general. The local setup says what is true on this machine.

For this project, the local setup inspection found a LiteLLM proxy on `localhost:11435`, direct `chatgpt/` model names, an API key helper pattern, and a patched Anthropic bridge for Claude Code system-message compatibility. Those are local facts, not universal LiteLLM facts.

Before acting on this packet later, re-check the local state:

```text
Claude Code settings still point to LiteLLM:
LiteLLM proxy still listens on expected port:
Configured model aliases still exist:
Target model still uses Responses mode:
Virtual key support available:
Patch set still applied:
Proxy logs available:
```

Do not assume `localhost:11435` is healthy because this guide mentions it. Run the Stage 1 baseline from the checklist. If the baseline fails, stop there.

## GitHub issues are failure evidence, not specs

GitHub issues are valuable because they expose integration pain, but they can be stale, incomplete, or specific to one user's environment. Use them to identify failure classes, not to define product behavior.

For Codex Desktop computer use, issue reports such as `Computer Use plugin unavailable` are useful because they show possible helper/plugin/cache/account-state failures ([openai/codex#18258](https://github.com/openai/codex/issues/18258)). They do not prove that every Codex install will fail. They prove that product-state and helper-state boundaries must be logged.

When reading an issue, extract:

```text
Product version:
OS version:
Region/account state:
Exact error text:
Maintainer response:
Workaround:
Whether the issue is open or closed:
Date of last meaningful update:
```

If the issue is closed, do not assume the failure is gone. Check whether it was fixed, made obsolete, closed as duplicate, or closed without resolution. If the issue is open, do not assume the feature is unusable. It may be a narrow configuration problem.

## Repository READMEs are capability claims

Open-source repositories often describe what the project aims to do, not what is robust in your environment. READMEs are still useful because they reveal architecture and integration style.

For Cua, read for the virtualization and computer-use-agent design direction ([trycua/cua](https://github.com/trycua/cua)). For E2B open-computer-use, read for sandbox/cloud-runtime assumptions ([e2b-dev/open-computer-use](https://github.com/e2b-dev/open-computer-use)). For open-codex-computer-use, read for how community experiments connect Codex-like models to computer-control loops ([iFurySt/open-codex-computer-use](https://github.com/iFurySt/open-codex-computer-use)). For OpenClaw's Peekaboo-style issue, read for Mac-native screenshot/accessibility bridge thinking ([OpenClaw Peekaboo issue](https://github.com/openclaw/openclaw/issues/67776)).

For each repository, refresh:

```text
Last commit date:
Recent release date:
Supported OS:
Supported model providers:
Isolation model:
Logging/replay support:
Permission model:
Known limitations:
```

Do not rank repositories by stars alone. For a computer-use harness, isolation, observability, and stop controls matter more than popularity.

## Practitioner security writeups need careful handling

Security writeups are especially important for computer use because they show adversarial behavior. The ZombAIs article is valuable because it demonstrates how webpage prompt injection can drive a computer-use host into downloading and executing code ([ZombAIs](https://embracethered.com/blog/posts/2024/claude-computer-use-c2-the-zombais/)). The lesson is the threat model, not the exploit recipe.

When refreshing security sources, extract defensive lessons:

```text
What input channel carried hostile instructions:
What action chain occurred:
Which sandbox boundary failed or held:
What human confirmation was absent:
What network/filesystem controls would have helped:
What should be avoided in this lab:
```

Do not reproduce malware, command-and-control behavior, or unauthorized systems. If a security source includes dangerous steps, summarize the risk and mitigation rather than turning it into a runbook.

## HN and social signals are triage, not proof

HN threads can reveal what practitioners are worried about, what they have tried, and which links matter. They are especially useful for finding skepticism and failure stories. But HN comments are not specs.

Use HN/social sources to answer:

```text
Are people actually using this?
What confuses experienced users?
Which failure modes are discussed repeatedly?
Which primary sources do commenters link?
Are there strong dissenting claims worth checking?
```

Then verify against official docs, repositories, issues, or extracted articles. In this packet, HN and social research helped identify practitioner caveats around computer use and product readiness. Durable claims still need primary sources in `source-index.md` and `sources.json`.

If the local `socli` archive is available, prefer it for already-indexed social material because it preserves full local context. If not, HN Algolia can still be used for public HN threads.

## Refresh cadence

The source set should be refreshed at different intervals depending on the decision being made.

Refresh immediately before:

- enabling Claude Desktop/Cowork against the local LiteLLM proxy;
- running the official Anthropic computer-use demo;
- adapting the demo to LiteLLM;
- granting macOS permissions to a desktop product helper;
- choosing an open-source runtime for serious experimentation;
- publishing or sharing conclusions outside the private repo.

For casual reading, a monthly refresh is enough. For implementation work, refresh the exact docs and issues on the day of the experiment.

Fast-moving docs to refresh first:

```text
LiteLLM Claude Desktop/Cowork docs
LiteLLM Claude Code docs
Anthropic computer-use docs
OpenAI Codex app computer-use docs
openai/codex computer-use issues
Anthropic quickstarts computer-use demo README
```

## What to update in this repo

A refresh is not complete until the durable files agree with each other.

Update these files together:

```text
README.md
briefing.md
source-index.md
research-log.md
sources.json
guide/00-README.md
affected guide chapters
```

For example, if Anthropic changes the computer-use beta version, update `sources.json`, the source index, the computer-use contract chapter, the control-demo checklist, and any boundary-debugging labels affected by the new response shape.

If Codex Desktop fixes a plugin failure class, update the Codex comparison chapter and keep the old issue as historical evidence only if it still explains a possible stale-install problem.

If LiteLLM documents computer-use tool support explicitly, that would change the central uncertainty of this packet. Update the briefing verdict and Stage 5 decision rules.

## Keep raw artifacts out of git

The repository policy is clear: raw rendered pages, clean article snapshots, SERP dumps, screenshots, and CDP artifacts belong under `tmp/`, which is gitignored. Durable synthesis belongs in the theme files.

During a refresh, save bulky artifacts under a path like:

```text
tmp/research-web-critical/litellm-claude-computer-use/
```

Commit only:

```text
source summaries
source index entries
structured source metadata
research log notes
guide updates
briefing updates
```

Do not commit screenshots, raw HTML, raw SERP dumps, secret-bearing logs, or full proxy request bodies. If a request/response packet is needed for debugging, redact it and summarize the important boundary facts in the decision log.

## Preserve the experiment separation

The easiest way for this research to go stale is to collapse different products into one claim. Avoid that during every refresh.

Keep these statements separate:

```text
Claude Code can use this local LiteLLM proxy for text/coding requests.
Claude Desktop/Cowork can be configured for third-party inference through LiteLLM.
Anthropic computer use is a beta API/tool-loop contract.
The official computer-use demo can run against real Claude credentials.
The official demo may or may not work through ChatGPT-backed LiteLLM.
Codex Desktop computer use is a separate product path.
Open-source runtimes are harness alternatives, not proof of Desktop support.
```

A new source may strengthen one statement and say nothing about the others. For example, a LiteLLM Desktop/Cowork doc update improves confidence in Desktop text routing, but it does not prove Anthropic computer-use beta tool compatibility through a ChatGPT-backed route.

## Red flags during refresh

Stop and re-evaluate if you find any of these:

```text
Official docs removed third-party inference instructions.
LiteLLM changed endpoint paths or auth behavior.
Anthropic changed beta headers or tool type names.
Computer-use docs added stricter model restrictions.
Codex Desktop changed helper/plugin architecture.
Open-source runtime is archived or unmaintained.
A security source reports a new prompt-injection class relevant to the lab.
Local proxy aliases no longer match the documented route.
```

A red flag does not necessarily invalidate the whole packet. It means the affected decision gate should be rerun and the old conclusion should be marked stale until verified.

## How to write new source notes

When adding a source, capture the source's role:

```text
Title:
URL:
Date accessed:
Publisher/owner:
Source type:
Quality label:
Relevant claim:
What it does not prove:
Related experiment stage:
```

The “what it does not prove” field prevents overclaiming. For example:

```text
Relevant claim: LiteLLM documents Claude Desktop/Cowork third-party inference setup.
What it does not prove: It does not prove Anthropic computer-use beta tools survive a ChatGPT-backed transformation.
```

That discipline is the difference between a useful research packet and a pile of links.

## How to refresh with CDP safely

When browser-grounded research is needed, use the repo's CDP rules. Check daemon health with safe diagnostics. Do not start, stop, restart, repair, keep alive, or actively probe the daemon without explicit human approval in the current turn. Keep Google SERP collection low-parallelism to avoid blocking and to behave like a human-paced search.

A good refresh pattern is:

1. Build fewer than ten focused queries.
2. Run SERP collection at low parallelism.
3. Inspect candidates before extraction.
4. Extract only selected pages.
5. Read page content, not snippets.
6. Summarize durable findings.
7. Update source metadata.
8. Validate the repo.

If CDP is unhealthy and the research question requires rendered pages, stop and ask the human to fix or approve the browser state. Do not silently downgrade to snippet-only research for a critical claim.

## Refresh output checklist

A good refresh leaves this behind:

```text
Updated source-index entry for every new durable source.
Updated sources.json with URL, title, type, quality, and notes.
Research-log entry explaining what was searched and why.
Guide changes only where conclusions changed.
No secrets in committed files.
No raw tmp artifacts staged.
Validation passing.
```

If validation fails because the guide has too few words, missing links, broken local links, invalid source JSON, or trailing whitespace, fix the durable files rather than weakening validation. The validation script encodes the repository's research quality floor.

## Refresh scenarios

Different changes require different refresh depth. Do not run the same heavy research workflow for every small update.

If the question is whether Claude Desktop text routing still works through LiteLLM, refresh only the Desktop/Cowork docs, local proxy settings, virtual-key behavior, and LiteLLM logs. The test should still be a tiny text prompt and dashboard verification. Computer-use sources are background context, not the main evidence.

If the question is whether Anthropic computer use changed, refresh the Anthropic computer-use docs, the Quickstarts demo repository, SDK examples, and any release notes around beta tool versions. The important fields are model support, beta header name, tool type name, tool schema, stop reasons, and how screenshots/tool results are represented. A change in any of those fields affects the control run and the proxy-adapted run.

If the question is whether the ChatGPT-backed LiteLLM route can carry computer use, refresh LiteLLM's Anthropic gateway docs, provider transformation behavior, open issues about tool use, and the local patch set. Then run a boundary packet. Do not infer compatibility from Desktop text routing alone.

If the question is whether Codex Desktop computer use is ready to compare, refresh product docs and recent `openai/codex` issues. Focus on helper availability, plugin registration, account/region state, permission prompts, and whether the issue reports match the user's OS and app version. Product readiness can change quickly, so old issue reports should be treated as historical failure classes unless they are still active.

If the question is which open-source runtime deserves a trial, refresh repository health and architecture. The right source is not just the README; inspect recent commits, issues, releases, and whether the project documents isolation and replay. A runtime that can complete a flashy browser task but cannot record actions or isolate secrets is not a good fit for this lab.

If the question is security, refresh threat-model sources and official safety guidance. Prioritize recent prompt-injection reports, sandbox recommendations, and examples where computer-use agents crossed from reading content into taking harmful actions. Translate those sources into stop conditions and harness constraints, not into exploit steps.

## Source conflict handling

Conflicts are normal. A vendor doc may say a feature is supported, while GitHub issues show users failing to enable it. A README may advertise a runtime as local-first, while issues reveal that important paths require cloud services. A practitioner writeup may claim a feature is unsafe, while official docs describe mitigations.

Handle conflicts explicitly:

```text
Claim:
Source supporting it:
Source contradicting or limiting it:
Likely scope of each source:
Experiment that would resolve it:
Current decision:
```

Do not delete the weaker source just because it is inconvenient. Instead, downgrade its scope. For example, an old Codex helper issue might no longer describe the current app, but it still justifies logging helper state during the experiment. An older Anthropic computer-use blog post might use a prior tool version, but it can still explain the loop concept if the version caveat is clear.

When a conflict affects an experiment gate, choose the safer interpretation until tested. If one source says a route should work and another shows a plausible failure mode, the checklist should include a step that detects the failure mode.

## Evidence-to-action mapping

Every durable finding should map to an action. Otherwise the guide becomes an annotated bibliography instead of an experiment plan.

Examples:

```text
Evidence: LiteLLM Desktop docs require a virtual key.
Action: Do not paste a broad master key into Desktop.

Evidence: Anthropic computer use returns tool_use/tool_result loops.
Action: Validate at least one full action/result/follow-up cycle.

Evidence: ZombAIs shows webpage prompt injection can lead to harmful actions.
Action: Use local or allowlisted pages first, block downloads, require confirmation.

Evidence: Codex issues mention plugin/helper unavailable states.
Action: Record app version, helper state, permission grants, and exact error text.

Evidence: Open-source runtimes vary in isolation and replay.
Action: Compare harness controls, not only model/provider support.
```

This mapping should be preserved during refreshes. If a new source does not change any action, it may belong in scratch notes rather than durable guide text.

## Archiving stale conclusions

When a conclusion changes, preserve enough history to understand why. Do not leave stale text in place as if it were current.

Use this pattern:

```text
Old conclusion:
New conclusion:
Source that changed it:
Date changed:
Experiment stages affected:
```

For small changes, update the affected chapter and add a research-log entry. For major changes, update the briefing and source index as well. If an entire path becomes irrelevant, keep a short historical note and mark the old evidence as superseded in prose.

A likely future example is explicit LiteLLM support for Anthropic computer-use tools. If LiteLLM adds documented support, this packet's Stage 5 uncertainty should be rewritten. The old warning should not disappear entirely; it should become historical context explaining why the boundary test exists.

Another likely example is Codex Desktop helper maturity. If plugin-unavailable issues are resolved across releases, the Codex chapter should stop presenting them as current blockers and instead keep them as setup checks.

## Review questions before commit

Before committing a refresh, ask these questions:

```text
Did every new claim get a source?
Did every source get a quality label?
Did any source change an experiment gate?
Did any old conclusion become stale?
Did I separate text routing from computer-use tool loops?
Did I separate product desktop automation from API contracts?
Did I keep raw artifacts and screenshots out of git?
Did validation pass?
```

If the answer is no, keep editing. The value of this repository is not that it has many links; it is that a future run can be executed safely and interpreted precisely.

## Minimum evidence before changing verdicts

Do not change the packet's verdict from “unproven” to “supported” on documentation alone. A support verdict for a route requires a successful experiment record, a named model/alias, observed logs, and a clear boundary classification. Documentation can justify trying a route; only a run can prove that this local route works.

The same standard applies to failures. A single product issue or failed local run should not become a global “does not work” claim. It should become a scoped failure with date, version, route, and observed boundary.

## The refresh takeaway

This packet should stay useful because it is structured around contracts and boundaries, not around one-time hype. Refresh official docs for contracts, local files for actual configuration, GitHub issues for failure classes, repositories for implementation options, and practitioner sources for security lessons. Then update the durable synthesis so the next experiment starts from evidence instead of memory.
