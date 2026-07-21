# Editorial Contract Reference

Read this reference before candidate adjudication and manuscript writing.

## Candidate Snapshot

Never edit a scored candidate in place. Write a new snapshot when evidence or
the takeaway changes. Preserve:

- candidate, cluster, continuation, duplicate, and overlap identities;
- canonical takeaway and exact material delta;
- event, publication, discussion, retrieval, evidence-cutoff, and edition dates;
- raw timestamps, timezones, normalized UTC, date rule, alternatives, and
  uncertainty;
- source URL, author/organization, type, independence, access state, content hash
  or artifact path, relied-upon claim, and exactly one evidence role;
- rubric version, scorer/time, component anchors/reasons, confidence, discussion
  observations, overlap adjustment, final score, and threshold;
- selected, radar, excluded, deferred, or merged status, including overrides and
  displaced candidates.

Use `unknown`, `not_found`, `not_applicable`, and `not_checked` precisely.

## Relevance

| Component | Weight | Anchors |
|---|---:|---|
| Engineering consequence | 35 | 0 none; 10 local optional change; 20 material decision for one group; 30 production/cross-team significance; 35 severe or irreversible consequence |
| Catch-up dependency | 20 | 0 isolated; 10 improves later understanding; 20 required for a later high-relevance story |
| Material novelty or correction | 20 | 0 repetition; 10 meaningful increment; 15 new capability, economics, failure, or policy; 20 reverses a takeaway |
| Durability | 15 | 0 engagement-only; 5 days; 10 months; 15 persistent assumption, dependency, risk, or cost |
| Breadth | 10 | 0 no defined audience; 5 one engineering constituency; 10 multiple constituencies or a shared dependency |

Interpolate only between adjacent anchors and write the reason. Apply zero to
minus 15 only to duplicated content, naming the overlap. Weak evidence, hype,
and popularity do not use that adjustment.

Placement thresholds:

- `75-100`: lead-eligible;
- `60-74`: full-item eligible;
- `45-59`: radar or documented full-item override;
- below `45`: exclude unless correcting the publication or closing a major
  incident.

Thresholds never create a daily quota.

## Confidence And Discussion

Confidence is separate from relevance:

- `A`: primary evidence plus independent reproduction, direct operational
  evidence, or an authoritative correction;
- `B`: primary evidence plus credible independent analysis or multiple
  attributable practitioner reports;
- `C`: one inspectable first-party artifact with limited corroboration, or
  multiple credible reports without the primary artifact;
- `D`: discovery-only, anonymous, inaccessible, materially conflicting, or
  claim-only.

Grade D cannot support an unqualified factual item. A vendor-claim-only candidate
cannot lead without material independent or practitioner substantiation.

Discussion intensity is `0-5`: none located; one substantive contribution;
several on one platform; substantive attention across two communities;
sustained cross-community follow-up/correction; or exceptional sustained
technical depth. Raw popularity does not qualify. Discussion may break a close
tie but adds no relevance points.

## Machine-Readable Story Ledger

Persist selected lead, secondary, and radar placements in `stories.json`. The
root contains `publication` and `stories`. Publication records the title,
timezone, inclusive `from` and `to` dates, `evidence_cutoff_at`, and
`rubric_version`. Every story records:

- unique `id`, `edition_date`, `title`, `placement`, and `material_delta`;
- `confidence`, `discussion_intensity`, and the selected `date_rule` number;
- `continuation_of` as an earlier story ID or `null`;
- `relevance` with all six components and their arithmetic `total`;
- a non-empty list of canonical `source_urls`;
- `override_reason` when a sub-threshold secondary is deliberately retained.

The bundled issue validator checks this shape, scoring bounds and arithmetic,
date-window membership, continuation direction, thresholds, IDs, and URLs.

## Edition Dates

Assign the first applicable rule:

1. First inspectable correction, invalidation, or reversal.
2. Incident onset, material escalation, substantive restoration, or a
   causal/preventive postmortem delta.
3. In-window event date when the takeaway was already supportable.
4. Earliest qualifying in-window publication when the event is unknown or out
   of window.
5. First new in-window production, economic, security, or operational
   consequence of an older event.
6. First date cumulative evidence for a slow burn crosses the threshold.
7. Earliest defensible editorial fallback, with alternatives and uncertainty.

Tie-break by earliest fully supportable takeaway, earliest inspectable source
timestamp, then earliest UTC timestamp. Later knowledge creates a continuation
snapshot; it does not rewrite an earlier date.

## Durable Packet

```text
research/<NN-issue-slug>/
  README.md
  briefing.md
  publication-spec.md
  design-audit.md
  source-index.md
  research-log.md
  sources.json
  newspaper.css
  guide/00-README.md
  guide/01-period-map.md
  guide/<ordered-date-files>.md
  guide/<final-methodology-file>.md
```

The period map is required for weekly, monthly, and custom ranges longer than
seven days. It contains five to eight arcs and no more than five standalone
dates, introducing no facts absent from the daily chapters.

## Daily Chapter

Begin with ISO date, weekday, and a literal three-to-seven-word theme. Then use:

- a 25-45 word daily brief;
- zero or one lead, only at relevance 75 or above;
- zero to three secondaries;
- zero to three 18-35 word radar notes;
- an optional whole-day note for continuation, access, or evidence conditions.

Do not render empty sections. Every full item has a factual headline, one
integrated factual account, exactly one bold `Builder impact:` sentence,
optional caveat/discussion lines only when material, and two to four descriptive
evidence links or an explicit missing state. Limit the whole day to 800 words.
Quiet days may be shorter or have no lead.

Write from extracted source pages rather than the SERP. Label vendor claims,
counter-evidence, access limits, and inferences at the sentence where they
matter. Keep bulky browser artifacts under `tmp/` and canonical metadata in
`sources.json`.

## Protected Content And Overflow

Protect the factual proposition, builder impact, claim state, material
correction/uncertainty, only primary proof, necessary independent support,
explicit missing-evidence state, and continuation history.

For a three-page day: remove redundancy; tighten the daily brief; remove
duplicate links; compress background; reduce impact to one consequence; merge
overlapping qualifications; cut low-continuity radar; remove the lowest-priority
secondary; tighten the lead; remove another secondary; then demote a lead that
no longer merits its slot. If protected content still spills, revise the
publication-wide contract and rerun every fixture. Never shrink one day's type.
