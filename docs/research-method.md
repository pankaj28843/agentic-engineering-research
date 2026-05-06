# Research Method

The default research posture is skeptical, browser-grounded, and reproducible.

## Source ladder

1. Primary/official sources: docs, specs, engineering blogs by the implementing team, papers.
2. Practitioner reports: production writeups, incident reports, postmortems, detailed implementation blogs.
3. Community signals: HN, Reddit, X/LinkedIn archive, GitHub issues and repositories.
4. SERP snippets: discovery leads only. Do not cite snippets as evidence unless the research question is explicitly about the SERP.

## Deep theme workflow

1. Create a theme slug and scratch root under `tmp/research-web-critical/<slug>/`.
2. Build 2-3 query batches, each with at most 10 Google queries.
3. Run paginated SERP collection with 2-3 result pages per query.
4. Inspect `candidates.tsv` before choosing visit URLs. Pages 2-3 matter because dissent, niche implementation reports, and older foundations often appear there.
5. Add HN and local social signals. Treat social posts as leads unless the linked source is fetched or the thread itself is being analyzed.
6. Extract selected pages as rendered Markdown into `tmp/`.
7. Synthesize claims for and against; label source quality and incentives.
8. Commit only durable outputs: briefing, source index, research log, and machine-readable metadata.

## CDP daemon rule

Only `cdp daemon status --json` is allowed as an unattended daemon lifecycle command. If it is not green/running, ask the user to start or restart the daemon. Do not run daemon start/restart/keepalive/active-probe commands without explicit human approval.

## Google URL hygiene

Google result URLs may contain tracking and encoded metadata parameters such as `ved`, `ei`, `usg`, `sa`, and redirect targets under `url=`, `q=`, or `u=`. Use canonical source URLs from `cdp` candidates or page extraction. Do not preserve Google redirect wrappers or cite protobuf-like tracking parameters as evidence.

## Validation

Run:

```bash
uv run python scripts/validate_research.py
```

The validator checks theme packet completeness, source metadata, local markdown links, and `AGENTS.md` guardrails.
