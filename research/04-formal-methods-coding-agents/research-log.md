# Research Log: Formal Methods for Coding Agents

## Task framing

User requested an in-depth, publishable, ELI5-style guide on formal methods in terms of coding agents, including how people have used the idea in the last six months. The work was treated as a durable repository theme, not a chat-only answer.

## CDP and tool preflight

- Confirmed required tools were available: `cdp`, `jq`, `curl`, `gh`, `socli`, and `docsearch`.
- Ran the only unattended daemon lifecycle check allowed by this repository:

```bash
cdp daemon status --json
```

The daemon reported `ok: true` and `health.state: healthy`, so browser-grounded workflows continued.

## Query batches

Scratch root: `tmp/research-web-critical/formal-methods-coding-agents/`

### Batch 1

```text
formal methods coding agents LLM agents 2026
formal methods for coding agents verification agents
LLM assisted formal verification Dafny Lean coding agents 2026
DafnyBench LLM verification hints Dafny
dafny annotator LLM Dafny annotations
Lean theorem proving LLM agent Prover Agent COPRA
runtime verification LLM agents tool use policy SMT
formal verification tool using LLM agents policy
site:arxiv.org LLM agents formal verification runtime constraints
site:news.ycombinator.com formal methods LLM agents
```

Command:

```bash
cdp workflow web-research serp \
  --query-file tmp/research-web-critical/formal-methods-coding-agents/queries-batch1.txt \
  --result-pages 3 \
  --serp google \
  --max-candidates 250 \
  --candidate-out tmp/research-web-critical/formal-methods-coding-agents/candidates-batch1.json \
  --out-dir tmp/research-web-critical/formal-methods-coding-agents/batch1 \
  --parallel 1 \
  --min-visible-words 50 \
  --min-html-chars 1000 \
  --min-markdown-words 50 \
  --json > tmp/research-web-critical/formal-methods-coding-agents/serp-summary-batch1.json
```

Result: 250 candidates, 0 failures.

### Batch 2

```text
last 6 months formal methods LLM coding agents
2026 LLM program verification Dafny agents
2025 formal methods LLM agents survey
AgentGuard runtime verification AI agents
solver-aided verification tool-using LLM agents
data over-exposure LLM agents data flow analysis
model checking AI agent workflows TLA+ LLM agents
autoformalization LLM formal specification 2026
LLM theorem proving Lean agent 2026
GitHub formal methods coding agents Dafny Lean TLA+ LLM
```

Result: 250 candidates, 0 failures.

### Official/source-definition batch

```text
NASA formal methods mathematically rigorous techniques specification design verification
TLA+ TLC model checker TLAPS official
Dafny verification-aware programming language static verifier official
Lean theorem prover dependent type theory official
SPARK formal verification Ada official
```

Result: 100 candidates, 0 failures.

## What pages 2-3 changed

The top results emphasized DafnyBench, DafnyPro, and broad formal-verification/AI narratives. Later pages and targeted queries surfaced a second, more agent-specific layer:

- runtime verification and dynamic assurance for agents (`AgentGuard`),
- privacy/data-flow analysis across agent tools (`AgentRaft`),
- LTL over memory/tool/MCP/human boundaries (`AgentVerify`),
- verified self-evolving agents (`SEVerA`),
- HN skepticism about overclaiming guarantees,
- open-source guard tools for coding-agent runtimes.

That shifted the synthesis from “LLMs can help theorem proving” toward “the practical coding-agent opportunity is to formalize the outer loop and tool boundary.”

## HN pass

Used HN Algolia over the last six months with keywords:

```text
formal methods LLM
formal verification LLM
Dafny LLM
Lean theorem prover LLM
formal methods coding agents
TLA+ LLM
agent verification
runtime verification AI agents
```

High-signal HN threads:

- `48065254` — [Can LLMs model real-world systems in TLA+?](https://news.ycombinator.com/item?id=48065254), 122 points, 32 comments.
- `46411539` — [Designing Predictable LLM-Verifier Systems for Formal Method Guarantee](https://news.ycombinator.com/item?id=46411539), 59 points, 13 comments.
- `47047027` — [Lean 4: How the theorem prover works and why it's the new competitive edge in AI](https://news.ycombinator.com/item?id=47047027), 145 points in the fetched item.
- `46790127` — browser-agent verification layer discussion; useful adjacent signal for post-condition-gated agents.

HN takeaways:

- Practitioners like the proof-checking direction but warn that generated specs can be hard to validate.
- Theorem provers are often explained as “proof-checking compilers,” not as larger test suites.
- Some claims about LLM-verifier convergence were criticized as mathematically thin or dependent on unrealistic assumptions.

## Social archive pass

`socli research "formal methods LLM coding agents" --since 180d` returned no candidates. Broader social searches around “formal verification,” “Dafny,” “Lean theorem prover,” “TLA+,” and “model checking” produced mostly low-confidence or adjacent agent-security items rather than focused formal-methods adoption signals. The report therefore treats HN as the stronger community signal.

## GitHub pass

Used `gh --help`, `gh search repos --help`, `gh search code --help`, and `gh search issues --help` before relying on GitHub CLI behavior.

Focused repository reads:

- `sun-wendy/DafnyBench` — 64 stars, 11 forks, Dafny, updated 2026-05-16.
- `metareflection/dafny-annotator` — 20 stars, 4 forks, Python, updated 2026-04-02.
- `Beneficial-AI-Foundation/dafny-autopilot` — 14 stars, 1 fork, TypeScript, updated 2026-01-18.
- `trishullab/copra` — 72 stars, 12 forks, Python, updated 2026-04-29.
- `kAIto47802/Prover-Agent` — 24 stars, 1 fork, Python, updated 2026-05-15.
- `GoPlusSecurity/agentguard` — 403 stars, 60 forks, TypeScript, updated 2026-05-15.
- `RaghavRoy145/autocomplete-and-verify` — 0 stars, Emacs Lisp, updated 2025-05-09.

GitHub takeaway: repos show real prototypes and tools, but star counts are modest except GoPlus AgentGuard. This is still early-adopter territory.

## Docsearch pass

`docsearch find "Dafny"`, `docsearch find "Lean theorem prover"`, and `docsearch find "TLA+"` did not return useful tenants for this topic, so official web docs were extracted through CDP instead.

## Extraction

Selected 41 URLs into `tmp/research-web-critical/formal-methods-coding-agents/visit-urls.txt`, then extracted with:

```bash
cdp workflow web-research extract \
  --url-file tmp/research-web-critical/formal-methods-coding-agents/visit-urls.txt \
  --max-pages 100 \
  --parallel 4 \
  --selector body \
  --out-dir tmp/research-web-critical/formal-methods-coding-agents/pages \
  --min-visible-words 50 \
  --min-html-chars 1000 \
  --min-markdown-words 50 \
  --json > tmp/research-web-critical/formal-methods-coding-agents/extract-summary.json
```

Result: 41 extracted pages, 0 failures. One ACM Queue page had a low visible-word warning and was not used as a core evidence source.

Then post-processed article snapshots with:

```bash
uv run python scripts/extract_theme_articles.py \
  research/04-formal-methods-coding-agents \
  --scratch-root tmp/research-web-critical/formal-methods-coding-agents
```

Result: 36/36 source snapshots extracted to `tmp/research-web-critical/formal-methods-coding-agents/articles/`.

## Limitations

- Google results are time-, region-, and browser-state dependent.
- arXiv HTML sometimes contains conversion artifacts; claims were checked against extracted abstracts and body text where possible.
- Some 2026 agent-verification work is preprint-only or workshop-listed; it is labeled accordingly.
- This research did not run Dafny, Lean, TLA+, TLC, or AgentGuard locally. It studied published sources and open-source project metadata.
- “Last six months” is emphasized, but older sources are included when foundational: NASA’s definition, official language/tool docs, DafnyBench, dafny-annotator, and COPRA.

## Validation

Repository validation command run after authoring:

```bash
uv run python scripts/validate_research.py
```

Result: `Validated 4 research theme(s).`

## Source audit note

- Source mix: 5 official, 5 primary, 12 paper, 1 preprint, 7 open-source, 3 practitioner, and 3 community records in `sources.json`.
- Guide depth: 14 guide files and about 19.7k words, with inline external source links throughout.
- CDP hygiene: research log records only `cdp daemon status --json` as the daemon lifecycle check; no unattended start/restart/keepalive/active-browser-probe commands.
- Source hygiene: selected URLs are canonical source URLs, not Google redirect wrappers; Google snippets were used only for source discovery.
- Article extraction: `scripts/extract_theme_articles.py` produced 36/36 article snapshots under `tmp/`, which remains uncommitted scratch space.
