# Podcast Evidence Handoff Contract

This contract freezes a published AI-news packet for downstream podcast
production. It transfers evidence and editorial ordering only. Script drafting,
cast and voice selection, TTS, audio processing, filenames, RSS publication,
and human listening approval belong to the downstream audio repository.

## Required input packet

The materializer accepts one complete `publish-ai-news` packet whose frozen
publication window is recorded in `stories.json`. It requires:

- `stories.json` with one publication object and unique story IDs;
- `sources.json` with one record per canonical story source URL;
- exactly one dated guide chapter for every inclusive publication date;
- every dated guide chapter encoded as valid UTF-8;
- every story's canonical source URL to appear in its dated chapter;
- a daily brief for every date; and
- an explicit day note for every zero-story date.

The join is exact. A missing source record, an unused source record, an
out-of-window story, a missing or extra dated chapter, or an unplaceable story
fails materialization. Repair the durable packet rather than guessing in the
audio workflow.

## Determinism and provenance

The caller supplies `--packet-frozen-at` as an observed, timezone-aware
timestamp. The optional `--run-requested-at` is emitted only when an actual
request timestamp is known; otherwise the handoff records it as unobserved.
Both are normalized to UTC.
The publication evidence cutoff and observed request time may not occur after
the packet freeze marker; an impossible chronology fails materialization.

For identical packet bytes and CLI arguments, the JSON output is byte-identical:
keys are sorted, indentation is fixed, ASCII escaping is stable, and no current
clock or absolute packet path enters the payload. The handoff binds
`stories.json`, `sources.json`, and every dated guide chapter by relative path,
byte count, and SHA-256. The CLI prints the output SHA-256 and materialized
counts after an atomic write.

Each `days[]` object also carries `guide_markdown`, the chapter's complete
UTF-8 text decoded directly from its source bytes. The materializer does not
trim, normalize, summarize, or reconstruct that value. Re-encoding it as UTF-8
therefore reproduces the bytes authenticated by the adjacent `guide.sha256`.

The handoff preserves research administration for auditability; it does not
turn that administration into dialogue. Publication-versus-discussion dates,
timezone normalization, inclusion-window decisions, retrieval or extraction
failures, page visibility, and similar process notes stay in provenance and
show notes. `day_notes`, `guide_caveats`, and full guide prose are evidence
inputs, not verbatim spoken requirements. Downstream authors should speak only
the shortest uncertainty that materially changes a claim's credibility, scope,
attribution, chronology, causality, comparison, or interpretation. When useful
substance is supported only as an attributed practitioner report or discussion,
state that substance at its supported scope instead of narrating why another
source was unavailable.

This is an additive field in `publish-ai-news-podcast-handoff/v1`. The schema
identifier remains v1 because no existing field, meaning, or required consumer
behavior changed; consumers that tolerate unknown object fields remain
compatible. New authoring consumers should use `guide_markdown` when they need
the full chapter and use normalized fields only for indexing or validation.

## Downstream guarantees

The versioned JSON payload contains:

- the complete frozen publication metadata;
- all dates in inclusive chronological order;
- each day's title, daily brief, day notes, and typed zero-story gap;
- each day's exact full guide Markdown, including factual exposition, Builder
  impact, caveats, discussion notes, evidence links, and radar prose;
- every story in first-canonical-URL guide order;
- the full story ledger record, canonical URL list, and joined source records;
- exact normalized caveat and discussion prose from full-item guide blocks;
- complete seven-day unions anchored to the publication start; and
- source, story, HN-reference, zero-day, and exact-join validation counts.

A trailing partial week is intentionally not promoted to a weekly union. The
downstream producer may synthesize from the handed-off evidence but must retain
the JSON hash in its own provenance ledger. It must not scrape or reconstruct
this packet independently. No handoff field is automatically listener-facing;
the downstream editorial contract decides what is spoken while preserving the
claim and source boundaries recorded here.

## Command

Run from the research repository root after issue and source validation:

```bash
python3 .agents/skills/publish-ai-news/scripts/materialize_podcast_handoff.py \
  research/<NN-issue-slug> \
  --from <YYYY-MM-DD> \
  --to <YYYY-MM-DD> \
  --packet-frozen-at <timezone-aware-ISO-timestamp> \
  --output tmp/podcast-handoffs/<issue-slug>/podcast-handoff.json
```

Add `--run-requested-at <timezone-aware-ISO-timestamp>` only when that event
was observed. Do not substitute an inferred timestamp.

The handoff is generated scratch state under `tmp/`; the durable packet records
the exact command, output path, hash, and counts in `research-log.md`.
