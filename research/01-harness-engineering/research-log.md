# Research Log: Harness Engineering for Coding Agent Users

Date: 2026-05-06

## Tool preflight

Required tools were available: `cdp`, `jq`, `curl`, `socli`, `docsearch`, `uv`, `gh`, and `python3`.

After the CDP daemon lifecycle guard was added to `AGENTS.md`, unattended daemon lifecycle use is limited to:

```bash
cdp daemon status --json
```

The daemon was green before continuing extraction:

```json
{
  "ok": true,
  "daemon": {
    "state": "running",
    "process_running": true,
    "message": "daemon keepalive process is running"
  }
}
```

## Scratch root

All bulky artifacts for this session were written under:

```text
tmp/research-web-critical/agentic-engineering-harness-engineering/
```

`tmp/` is intentionally gitignored.

## Query batches

### Batch 1

```text
agentic engineering harness engineering coding agents
harness engineering coding agents Martin Fowler
agent harness coding agents long running agents
context engineering coding agents Martin Fowler
Simon Willison agentic engineering patterns
coding agents harness engineering production lessons learned
coding agents failure modes pitfalls context engineering
site:martinfowler.com/articles exploring gen ai coding agents
site:anthropic.com/engineering harness long-running agents
site:stripe.dev/blog coding agents minions
```

Command shape:

```bash
cdp workflow web-research serp \
  --query-file "$ROOT/queries-batch1.txt" \
  --result-pages 3 \
  --serp google \
  --max-candidates 250 \
  --candidate-out "$ROOT/candidates-batch1.json" \
  --out-dir "$ROOT/batch1" \
  --parallel 1 \
  --min-visible-words 50 \
  --min-html-chars 1000 \
  --min-markdown-words 50 \
  --json > "$ROOT/serp-summary-batch1.json"
```

Outcome: `candidate_count=250`, `failure_count=0`.

### Batch 2

```text
agentic engineering criticism pitfalls coding agents
AI coding agents reliability test driven development continuous integration
context rot context engineering coding agents
long running AI agents state verification failure recovery
AI coding agents production incident postmortem lessons learned
agentic coding security prompt injection sandbox permissions
harness engineering OpenAI coding agents
Stripe minions coding agents one shot end to end
architectural fitness function AI coding agents
requisite variety cybernetics software engineering AI agents
```

Outcome: `candidate_count=250`, `failure_count=0`.

### Batch 3

```text
site:news.ycombinator.com coding agents harness engineering agentic engineering
site:github.com awesome harness engineering coding agents
site:github.com agent rules coding agents CLAUDE.md AGENTS.md
site:docs.anthropic.com Claude Code best practices agents.md
site:developers.openai.com codex agents AGENTS.md coding agent guide
site:github.blog copilot coding agent custom instructions AGENTS.md
site:docs.astral.sh uv python project pyproject uv lock
site:chromedevtools.github.io devtools-protocol browser automation docs
site:developer.chrome.com chrome devtools protocol protocol monitor
site:owasp.org AI agent security prompt injection coding agents
```

Outcome: `candidate_count=250`, `failure_count=0`.

## HN and social signals

HN Algolia was queried for multiple terms including:

- `Agentic Engineering Patterns`
- `What is agentic engineering`
- `Effective harnesses for long-running agents`
- `Harness engineering for coding agent users`
- `Context Engineering for Coding Agents`
- `The role of developer skills in agentic coding`
- `Claude Code coding agents`
- `Codex coding agents`

The expanded HN pass found 67 deduplicated story hits. High-signal threads included Simon Willison's Agentic Engineering Patterns, Fowler's role of developer skills article, Anthropic's long-running harness post, Claude/Codex coding-agent tools, and sandboxing discussions.

`socli research "agentic engineering coding agents harness engineering" --since 365d` found 3 high-signal local social hits: one X post about an opinionated development workflow harness, a Reddit Meta-Harness discussion, and a Reddit SlopCodeBench discussion alleging long-horizon degradation in agent-written code.

## Visit list and extraction

A manual visit list of 86 URLs was selected from SERP, HN, socli, docsearch, and user-provided sources. It balanced:

- primary/official sources,
- practitioner guides,
- security guidance,
- community dissent,
- open-source implementation examples,
- docs for repo setup (`uv`, AGENTS.md, CDP).

Initial extraction with `--parallel 6` succeeded for 25 pages and failed for 61 after a daemon/browser connection drop. Two cdp-cli feature requests were filed under `~/feature-requests/cdp-cli/`:

- `20260506-fix-web-research-extract-daemon-disconnect.md`
- `20260506-harden-daemon-recovery-after-research-workflow-drop.md`

After the user confirmed the daemon was green again, failed URLs were retried in 10-URL chunks with `--parallel 2`. All 61 retry URLs succeeded. Final unique extracted source count: 86.

## Docsearch checks

`docsearch` was used for official docs coverage:

- `docsearch find uv`
- `docsearch find chrome`
- `docsearch find devtools`
- `docsearch search uv "pyproject project uv lock sync" --json`
- `docsearch search chrome-devtools-protocol "Page DOM Runtime Network Browser automation protocol" --json`
- `docsearch search chrome-devtools "protocol monitor network recorder performance" --json`

Fetched docs included uv project setup, uv locking/syncing, uv layout, CDP Page/Network domains, and Chrome Protocol Monitor.

## What pages 2-3 changed

Pages 2-3 surfaced important sources that would have been missed by a shallow pass:

- HN discussions around agentic engineering, coding agents, and sandboxing.
- GitHub Blog's `agents.md` guidance and Copilot custom-instruction support.
- OWASP AI Agent Security and prompt-injection guidance.
- Open-source harness lists and AGENTS.md examples.
- Critical/implementation reports on context rot, long-running agents, and code degradation.

## Article-extraction post-processing

The initial packet was too shallow relative to the crawl cost. The theme was upgraded to use clean article snapshots as the writing substrate. Captured CDP `html.json` files remain under `tmp/`, and `article-extractor` post-processing writes source-focused Markdown under `tmp/.../articles/`:

```bash
uv run python scripts/extract_theme_articles.py \
  research/01-harness-engineering \
  --scratch-root tmp/research-web-critical/agentic-engineering-harness-engineering
```

A full post-processing run successfully extracted 86/86 article snapshots to:

```text
tmp/research-web-critical/agentic-engineering-harness-engineering/articles/
```

The durable reader-facing output is now the ~20k-word guide under [guide/00-README.md](guide/00-README.md). Source diagrams used in the guide were copied locally under [assets/](assets/) with credits in [assets/README.md](assets/README.md).

Private book output was verified with:

```bash
uv run python scripts/build_theme_book.py research/01-harness-engineering --formats markdown,epub
```

Outputs:

```text
tmp/books/01-harness-engineering/01-harness-engineering.md
tmp/books/01-harness-engineering/01-harness-engineering.epub
```

## Limitations

- Many source pages are vendor-authored and have incentives to present agentic coding positively.
- Social signals were sparse in local `socli` for this exact phrase; broader related searches should be run in later passes.
- Some pages had heavy JavaScript in the extracted Markdown, but the relevant body text was present for cited claims; article-extraction post-processing is now used to reduce this noise.
- This pass did not deep-read every HN comment thread; HN was used for signal and dissent discovery.
- Google search region/personalization may affect ranking; sources are cited from extracted pages, not snippets.
- The guide is a substantial first book-grade pass, but behaviour harnessing and evaluator calibration deserve deeper future expansion.

## Audit note

The durable packet commits synthesis, source metadata, guide chapters, and credited guide assets. Raw rendered pages and clean article snapshots remain in gitignored `tmp/`.
