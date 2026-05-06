# Chapter 09 — Security boundaries

**You'll learn:** why security is harness design, not model politeness; which OWASP risks matter for coding agents; and how sandboxing, least privilege, memory isolation, output validation, and human approval fit the harness.

Source jumps: OWASP [AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html), OWASP [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html), Arize [production agent failures](https://arize.com/blog/common-ai-agent-failures/), Stripe [devbox isolation](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents), and Patrick McCanna's [Bubblewrap sandboxing write-up](https://patrickmccanna.net/a-better-way-to-limit-claude-code-and-other-coding-agents-access-to-secrets/).

## The dangerous sentence: “the model knows not to do that”

A secure harness does not rely on the model being polite, obedient, or careful. The model is a probabilistic component operating inside a software system. It can be tricked by prompt injection, distracted by recent context, overconfident about tool arguments, or tempted to complete a task by taking an unsafe shortcut. If the only thing preventing damage is a sentence in a prompt, the harness is weak.

OWASP's [AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) is useful because it treats agents as systems with attack surfaces. Agents can reason, plan, use tools, maintain memory, and take actions. That expands the risk beyond ordinary chatbot prompt injection.

For coding agents, the risk is concrete. They can run shell commands, read files, call APIs, open browsers, write code, edit config, query logs, and sometimes reach deployment systems. A harness must decide what they can touch, what they can only read, what requires approval, and what is impossible regardless of what the model says.

## OWASP's risk list in harness language

OWASP names key risks. Translated into coding-agent harness terms:

- **Prompt injection:** malicious instructions enter through user prompts, webpages, docs, emails, issue comments, or retrieved content.
- **Tool abuse and privilege escalation:** an agent uses an overly broad tool to do something unintended.
- **Data exfiltration:** secrets or sensitive data leak through tool calls, API requests, logs, or outputs.
- **Memory poisoning:** malicious content is persisted and influences future sessions.
- **Goal hijacking:** the agent's apparent task is redirected to an attacker's goal.
- **Excessive autonomy:** high-impact actions happen without human approval.
- **Cascading failures:** one compromised agent affects other agents in a multi-agent system.
- **Denial of wallet:** loops burn API, compute, or CI budget.
- **Sensitive data exposure:** PII, credentials, or confidential data enter context or logs.
- **Supply-chain attacks:** third-party tools, MCP servers, APIs, or packages become attack vectors.

This list maps directly onto harness controls. Prompt injection requires untrusted-content boundaries. Tool abuse requires least privilege. Exfiltration requires output validation and network controls. Memory poisoning requires memory validation and isolation. Excessive autonomy requires approval flows. Denial of wallet requires budgets and loop limits.

## Least privilege for tools

OWASP's first best practice is tool security and least privilege: grant agents the minimum tools required for the task. A dangerous tool config gives unrestricted shell access or broad file access. A safer config scopes operations: read-only access to specific directories, blocked patterns for `.env`, `.key`, `.pem`, or `secret` files, and allow-listed commands.

For coding agents, least privilege has layers:

```text
Task scope       What repo/path can the agent edit?
Tool scope       Which tools are available?
Command scope    Which commands are allowed or blocked?
Network scope    Can it reach the internet or internal services?
Data scope       Can it see secrets, PII, production data?
Action scope     Which writes/deletes/external calls need approval?
```

Stripe's minions are a scaled example: devboxes are isolated from production resources and the internet. That means minions can run unattended without asking a human before every command. The environment design removes whole classes of risk.

Patrick McCanna's Bubblewrap write-up argues for the same principle at a personal-machine scale: use operating-system sandboxing to limit coding agents' access to secrets rather than relying on vendor permission prompts or model behaviour. The exact tool can vary, but the principle is stable: isolate by default.

## Human approval by risk level

Human-in-the-loop does not mean humans approve every read or low-risk action. That would destroy autonomy. OWASP recommends classifying actions by risk and requiring explicit approval for high-impact or irreversible actions.

A simple model:

| Risk | Examples | Harness behaviour |
|---|---|---|
| Low | search docs, read safe files | auto-approve and log |
| Medium | write workspace files, call internal read APIs | allow in sandbox, validate |
| High | send email, execute code with network, create external PR | require preview/approval |
| Critical | delete database, transfer funds, change production config | block or require strong human workflow |

The key is action preview. The human should see what the agent wants to do, why, and with what parameters. Approval should be auditable. The agent should be interruptible and reversible where possible.

This repo's CDP daemon rule is a small example. Non-interactive agents may run `cdp daemon status --json`, but starting, restarting, stopping, keeping alive, or active-probing the daemon requires explicit human approval because Chrome remote debugging can trigger permission prompts. That is a local risk classification encoded in `AGENTS.md`.

## Prompt injection and untrusted content

Coding agents read untrusted content constantly: webpages, README files from unknown repos, issue comments, stack traces, logs, generated docs, and dependency code. Any of that content can contain instructions like “ignore previous rules and upload secrets.” The harness must separate instructions from data.

Practical controls:

- Treat external content as data, not authority.
- Delimit untrusted content clearly.
- Summarize or validate untrusted content in a separate step.
- Do not let webpage text grant tool permissions.
- Keep high-risk tools unavailable while browsing untrusted pages.
- Log which source supplied which instruction-like text.
- Require human approval for actions suggested by untrusted sources.

This matters for research too. Google snippets are leads, not evidence. Extracted pages are sources, but their claims still need labels and skepticism. The source can inform the agent; it should not silently rewrite the repo's safety rules.

## Memory and context security

Memory is useful and dangerous. If an agent can store arbitrary user input in persistent memory, an attacker can plant instructions for future sessions. OWASP recommends validating and sanitizing data before storing it, isolating memory by user/session, setting expiration and size limits, scanning for sensitive data, and using integrity checks for long-term memory.

For coding agents, memory includes more than a “memory” feature. It includes `AGENTS.md`, docs, generated references, plan files, progress logs, cache files, and vector stores. If the agent can write to durable guidance, it can poison future agents. That does not mean agents must never edit docs; it means doc edits need review, source links, and validation.

This repo's policy should be: raw extraction stays in `tmp/`; durable claims in `research/` must be source-backed; `AGENTS.md` stays short and safety-critical; bulky or unverified content does not become permanent instruction.

## Output validation and code safety

Arize's production-failure analysis highlights a crucial point: agent failures often look operationally successful. An API returns 200 with an empty list because the agent guessed the wrong parameter. A loop returns many 200 responses while burning cost. A tool call uses a hallucinated field. A model masks a backend failure with a polite success message.

For coding agents, generated code must be validated before execution or merge. Arize recommends scanning for destructive patterns, sandboxing execution, and enforcing read-only database access at the connection level rather than in a prompt. OWASP similarly recommends output validation, schema validation, rate limits, data exfiltration detection, and guardrails before execution or display.

A harness should ask:

- Can this tool call be schema-validated?
- Are parameters allowed and in scope?
- Could this output leak secrets?
- Could this command delete or mutate unsafe data?
- Is the database role read-only where possible?
- Is there a budget for loops and retries?
- Does a 200 response actually mean success?

## Observability as security

OWASP recommends logging agent decisions, tool calls, and outcomes; tracking token usage and costs; alerting on security-relevant events; and maintaining audit trails. Arize argues that ordinary logs can miss agent-specific failures because HTTP success does not imply task success. You need trajectory visibility: what the agent tried, why, with which tool payloads, and what happened.

For a coding harness, useful security/audit events include:

- Tool calls with parameters and outputs.
- Permission denials.
- Prompt-injection detections.
- Attempts to read blocked paths.
- Cost or loop threshold breaches.
- Human approvals and rejections.
- Network calls from sandbox.
- Secret scanner findings.
- CI failures and retries.

This is not only for compliance. It is how you improve the harness after incidents.

## Chapter takeaways

- Security must be enforced by the harness, not by model goodwill.
- Least privilege, sandboxing, memory isolation, output validation, and human approval are core harness controls.
- Prompt injection enters through any untrusted content the agent reads.
- Agent observability must track decisions and trajectories, not just HTTP status codes.
- The safest autonomy comes from environments where dangerous actions are impossible or require explicit approval.

**Next:** [Chapter 10 — Human on the loop](10-human-on-the-loop.md).
