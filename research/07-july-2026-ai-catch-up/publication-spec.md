# Publication Specification

Status: frozen before phase-two reporting on 21 July 2026.

## Reader contract

The reader is an AI-engineering practitioner returning after missing 1-21 July
2026. The edition supports a 10-15 minute scan of the period map, date headings,
daily briefs, and builder-impact lines, followed by a 45-75 minute evidence-led
catch-up through item prose and deep links.

The daily chronology is the reporting spine. A one-page **Period Map** precedes
it and lists five to eight consequential arcs, each with a takeaway and linked
material dates, plus no more than five standalone dates. It adds navigation,
not new reporting.

## Daily information architecture

Every date begins on a new page and conditionally renders only sections with
content:

1. ISO date, weekday, and a literal three-to-seven-word theme.
2. A 25-45 word **Daily brief** naming the principal material delta, one
   additional consequential delta when present, and any period-arc continuation.
3. Zero or one lead. A lead requires a relevance score of at least 75.
4. Zero to three secondary items under **What else mattered**.
5. Zero to three 18-35 word notes under **On the radar**.
6. An optional **Day note** only for a continuation, access failure, or evidence
   condition applying to the whole chapter.

Every full item contains a factual headline, an integrated factual account,
exactly one bold **Builder impact:** sentence, optional **Caveat:** and
**Discussion:** lines when material, and one evidence line. The evidence line
contains two to four descriptive links or an explicit missing state. Its labels
are limited to `Primary`, `Independent`, `Data`, `Code`, `HN`, and `Social`.

Do not render empty headings, signal badges, or a separate "What happened"
label. Missing evidence uses explicit text such as `Independent evidence not
found` or `Primary source inaccessible`.

| Slot | Preferred | Hard ceiling |
|---|---:|---:|
| Daily brief | 25-38 words | 45 words |
| Lead account | 90-135 words | 150 words |
| Secondary account | 55-90 words | 105 words |
| Builder impact | 12-28 words | 32 words |
| Caveat or discussion line | 10-30 words | 35 words |
| Radar item | 18-30 words | 35 words |
| Full-item evidence links | 2-4 | 4 |
| Full items, including lead | 0-4 | 4 |
| Radar items | 0-3 | 3 |
| Whole day | 500-700 words | 800 words and two A4 pages |

There is no minimum story or word quota. Quiet days stay quiet.

## Deterministic story dates

Each candidate records a `story_takeaway` and the exact `material_delta` being
reported. The edition date is the first applicable rule:

1. First inspectable evidence of a correction, invalidation, or reversal.
2. Incident onset, material escalation, substantive restoration, or a
   postmortem that changes causal or preventive understanding.
3. In-window event date when the reported consequence was already supportable.
4. Earliest qualifying in-window publication when the event is unknown or
   outside the window.
5. First stored date of a new in-window production, economic, security, or
   operational consequence of an older event.
6. Earliest date when cumulative evidence for a slow burn crosses the inclusion
   threshold.
7. Earliest defensible in-window editorial fallback, with rejected alternatives
   and uncertainty recorded.

Ties resolve to the earliest date when the takeaway was fully supportable, then
the earliest inspectable source timestamp, then the earliest UTC timestamp.
The ledger preserves raw timestamp and timezone, normalized UTC, event,
publication, discussion, and retrieval times, the selected rule, alternatives,
and uncertainty. A later chapter exists only for a material new delta and links
back through `continuation_of`; later knowledge is never imported into an
earlier-dated item.

## Selection relevance

Popularity, confidence, and relevance are separate outputs.

| Component | Weight | Anchors |
|---|---:|---|
| Engineering consequence | 35 | 0 none; 10 local optional change; 20 material decision for a defined group; 30 production or cross-team significance; 35 severe or irreversible consequence |
| Catch-up dependency | 20 | 0 isolated; 10 improves later understanding; 20 required for a later high-relevance story |
| Material novelty or correction | 20 | 0 repetition; 10 meaningful increment; 15 new capability, economics, failure, or policy; 20 reverses a prior takeaway |
| Durability | 15 | 0 engagement-only; 5 days; 10 months; 15 persistent assumption, dependency, risk, or cost |
| Breadth | 10 | 0 no defined audience; 5 one engineering constituency; 10 multiple constituencies or a shared dependency |

Interpolate only between adjacent anchors and record why. Apply a zero to minus
15 content-overlap adjustment only to a duplicated takeaway and name the
overlapping candidate. Weak evidence, hype, and popularity do not use this
adjustment.

- `75-100`: lead-eligible.
- `60-74`: full-item eligible.
- `45-59`: radar or documented full-item override.
- Below `45`: excluded unless correcting this publication or closing a major
  incident.

Scores rank candidates but never force a daily quota.

## Evidence confidence and discussion

Confidence controls wording and safeguards rather than relevance points:

- `A`: primary evidence plus independent reproduction, direct operational
  evidence, or an authoritative correction.
- `B`: primary evidence plus credible independent analysis or multiple
  attributable practitioner reports.
- `C`: one inspectable first-party artifact with limited corroboration, or
  multiple credible reports without the primary artifact.
- `D`: discovery-only, anonymous, inaccessible, materially conflicting, or
  claim-only.

Confidence D cannot support an unqualified factual item. A vendor-claim-only
candidate cannot be a lead without material independent or practitioner
substantiation.

Discussion intensity ranges from zero (none located) to five (exceptional,
sustained technical depth). Raw popularity cannot qualify. Discussion may break
a tie between similarly relevant candidates but contributes no relevance
points. Each source observation has one scoring role: an HN thread may qualify
interpretation or discussion, but it cannot also prove the event without a
distinct inspectable fact.

## Source and audit contract

The evidence order is original artifact; independent reporting or technical
analysis; HN or attributable practitioner correction; attributable social
signal; then discovery-only SERP and external-agent leads.

Every considered candidate has an immutable scored snapshot containing its
identity, canonical takeaway, material delta, relationships, timestamps,
evidence cutoff, source provenance and content hash, relied-upon claim,
independence, rubric version, component anchors, confidence, discussion
observations, final score, threshold, status, override, and displaced candidate.
The ledger distinguishes `unknown`, `not_found`, `not_applicable`, and
`not_checked`. Later evidence creates a new snapshot rather than silently
changing an earlier one.

## Headed discovery contract

All live discovery and extraction uses headed CDP. Google runs against Google
only, with no fallback, `--parallel 1`, batches of at most ten queries, and two
or three result pages. Exact dates are supplied as a tab-separated query and
Google `tbs` value:

```text
AI LLM agents<TAB>cdr:1,cd_min:07/01/2026,cd_max:07/01/2026
```

Google dates and snippets are discovery hints, never proof. The researcher
inspects candidate ledgers before choosing canonical sources, extracts rendered
pages with headed CDP, and checks page-quality artifacts.

HN discovery uses bounded dates, canonical item pages, and linked original
sources read through headed CDP. Broad `AI` token matching is not a relevance
filter. Local social archives are gap aids only when they contain the reporting
window. External agents can challenge the method or propose leads but cannot
satisfy a source requirement.

## Podcast evidence handoff

After publication acceptance, the dated issue may feed downstream audio only
through the versioned `publish-ai-news-podcast-handoff/v1` evidence handoff.
Materialization must bind `stories.json`, `sources.json`, and all 21 dated guide
chapters by SHA-256; preserve guide order, daily briefs, caveats, discussion
notes, and typed zero-story gaps; join every canonical source record exactly;
and emit complete seven-day unions anchored to July 1. Missing or unused source
records, missing dates, unplaceable stories, and inferred timestamps fail the
handoff rather than being repaired downstream.

The current handoff was frozen at `2026-07-22T15:16:59Z` with SHA-256
`2ade3b81aaf3f2387101bd03bf0fdf3de285a7468cbcf0cf77f6f44bd07e4d6d`.
It contains 21 days, 56 stories, 101 canonical sources, 102 story-source
references, 43 HN references, three complete weekly unions, and the explicit
July 10 zero-story gap. The run-requested time was not observed and remains
typed as unobserved. This post-publication transfer does not revise the frozen
editorial rubric and does not define script, cast, TTS, audio, RSS, filename, or
human-review policy.

## A4 design brief

The design is a quiet, high-density broadsheet for practitioners. Date, delta,
impact, and evidence form one scan path.

- A4 portrait with 20 mm top, 16 mm side, and 22 mm bottom page margins; center
  the body at a 166 mm maximum measure for 22 mm effective side gutters.
- Body type at least 10.5 pt and line height at least 1.45.
- A single roughly 80-100-character reading measure; no dense multi-column body
  copy.
- White paper, near-black ink, one dark-red accent, and neutral rules.
- Grayscale-safe hierarchy; no cards, badges, gradients, shadows, or ornamental
  imagery.
- Descriptive clickable links, with a source ledger for print parity.
- A continuation footer on page one of a two-page day and repeated date running
  head on page two where the renderer supports it.
- Headings remain with at least two following lines. Impact, caveat, discussion,
  and evidence lines do not strand alone at the top of a page.

## Overflow and acceptance

If a day reaches three pages, remove redundancy, tighten the daily brief,
remove redundant links, compress background, reduce impact to one consequence,
merge overlapping qualifications, and cut low-continuity radar or secondary
items in that order. Protect the proposition, builder impact, claim state,
material correction, only primary proof, necessary independent support,
explicit missing-evidence states, and continuation history. Never shrink one
day's typography.

Acceptance requires Markdown lint, repository validation, independent rendering
of every date within one or two A4 pages, assembly in date order, all dates
exactly once as chapter headings, no duplicated chapters or blank pages,
preserved links, and visual inspection of the cover, period map, densest day,
quietest day, every two-page boundary, and final page. Repeated date text is
allowed only in an intentional continuation running head.
