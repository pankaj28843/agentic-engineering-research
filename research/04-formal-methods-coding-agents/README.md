# Theme 04: Formal Methods for Coding Agents

This theme studies how formal methods are being paired with LLM coding agents: specifications, model checking, theorem proving, program verification, runtime monitors, and tool-use policies. It focuses on the last six months of visible activity where possible, while using older foundational sources when they define the tools or methods.

## Start with the reader-facing guide

- [guide/00-README.md](guide/00-README.md) — chapter-wise ELI5 guide for developers who know tests and type checkers but are new to formal methods.
- [assets/README.md](assets/README.md) — notes on diagrams and local assets.

## Support files

- [briefing.md](briefing.md) — executive verdict, evidence, counter-evidence, and practical recommendations.
- [source-index.md](source-index.md) — human-readable source catalog with quality labels and artifact paths.
- [research-log.md](research-log.md) — query batches, HN/GitHub/social notes, extraction notes, and limitations.
- [sources.json](sources.json) — machine-readable source metadata.

## One-sentence takeaway

The practical pattern is not “the LLM becomes mathematically trustworthy”; it is “the LLM proposes code, proofs, specs, plans, or tool calls, and independent formal or semi-formal machinery checks, rejects, constrains, or monitors them.”

## Current confidence

High confidence that generate → check → repair loops are real and increasingly useful for Dafny/Lean/TLA+-style work; medium confidence that this will become mainstream in ordinary product code soon; high confidence that wrong specifications, vacuous proofs, and agent/tool boundary mistakes remain the central failure modes.
