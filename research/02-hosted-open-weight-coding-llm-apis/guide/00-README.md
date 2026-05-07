# Guide: Hosted Open-Weight Coding LLM APIs

This is a living guide for a practical question: **Can hosted open-weight coding models replace or reduce Claude Opus / GPT-5.5 usage for a week of real development work without becoming unsafe, unreliable, or deceptively expensive?**

The guide is intentionally written for a hands-on coding-agent user. It assumes you are comfortable with API keys, a terminal coding agent, and running tests, but it does not assume you already know the current model/provider market.

## Reading path

1. [Quick verdict and the one-week plan](01-quick-verdict.md)
2. [What “open weight” buys you, and what it does not](02-open-weight-does-not-mean-risk-free.md)
3. [The model shortlist: Qwen, Kimi, DeepSeek, Llama, and baselines](03-model-shortlist.md)
4. [Price and actual context matrix](04-price-context-matrix.md)
5. [Provider safety, privacy, and reliability](05-provider-safety-reliability.md)
6. [Benchmarks, HN, GitHub, and practitioner signal](06-benchmarks-social-github-signal.md)
7. [A one-week evaluation protocol you can actually run](07-one-week-evaluation-protocol.md)
8. [Coding-agent setup patterns and gotchas](08-coding-agent-setup.md)
9. [Refresh playbook for keeping this guide alive](09-refresh-playbook.md)

## Current short answer

Start with **OpenRouter** as the minimal provider interface, but do not use it naively. Use OpenRouter because its model pages and API expose price/context metadata for Qwen, Kimi, DeepSeek, Llama, Opus, and GPT-5.5 in one place, because it supports provider routing, and because its privacy docs say prompts/responses are not stored unless you opt into logging or product improvement ([OpenRouter data collection](https://openrouter.ai/docs/guides/privacy/data-collection)). Then tighten it: set a small credit balance, enable ZDR/provider policy controls, and pin or prefer providers with zero-retention policies for sensitive code. Keep **DeepInfra direct** as the privacy-simple backup, because its docs say inference inputs and outputs are not stored to disk, are held only in memory during inference, and are not used for training except when routing to Google/Anthropic models ([DeepInfra data privacy](https://docs.deepinfra.com/account/data-privacy)).

Do **not** treat “open weight” as a blanket green light for private repositories. DeepSeek direct pricing is extremely attractive, and the current DeepSeek API docs advertise 1M context for V4 Flash/Pro at very low per-million-token rates ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)), but DeepSeek’s own privacy policy says user inputs may be collected, retained, used to improve/train technology, and processed/stored in the People’s Republic of China ([DeepSeek privacy policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)). Use it for synthetic, public, or redacted tasks unless your risk tolerance explicitly permits otherwise.

## Baseline framing

The meaningful comparison is not “Can an open model beat Opus on one benchmark?” The meaningful comparison is:

- Can it solve your repository’s issues with fewer human repairs?
- Does it preserve architectural intent and test discipline?
- Does it work inside your coding-agent harness without tool-call/schema drift?
- How much does it cost for real prompts, not marketing prompts?
- Does the provider retain, train on, or route your code to a jurisdiction you cannot accept?
- Does it fail gracefully when context is long, tools error, or the task requires multiple iterations?

That is why this guide pairs price tables with a week-long evaluation protocol. Prices and context windows are only the first filter.

## Source stance

Google SERP snippets were used only for discovery. Claims in this guide are grounded in extracted pages, provider docs, official model pages, benchmark pages, GitHub repositories, HN threads, and local `socli` signals recorded in [research-log.md](../research-log.md). Vendor benchmark claims are labeled as vendor claims unless corroborated by independent benchmarks or hands-on practitioner reports.
