# Daily Chapter Template

Use only sections that contain evidence-backed material. Replace every bracketed
field and delete instructional comments before publication.

```markdown
# YYYY-MM-DD, Weekday: Three-to-Seven-Word Theme

<div class="daily-brief" markdown="1">

**Daily brief:** [25-45 words naming the principal delta, one additional delta
when material, and a continuation arc when present.]

</div>

<article class="lead-story" markdown="1">

## [Factual lead headline]

[Integrated factual account, 90-150 words. State attribution and any
interpretation-changing uncertainty in the prose.]

<div class="impact" markdown="1">

**Builder impact:** [One concrete consequence, 12-32 words.]

</div>

<div class="caveat" markdown="1">

**Caveat:** [Only when material, 10-35 words.]

</div>

<div class="discussion" markdown="1">

**Discussion:** [Only when substantive evidence changes interpretation, 10-35
words.]

</div>

<div class="evidence" markdown="1">

*Evidence:* [Primary: descriptive source](https://example.com) · [Independent:
descriptive source](https://example.org) · [HN: substantive
thread](https://news.ycombinator.com/item?id=NNN)

</div>

</article>

## What else mattered

<article markdown="1">

### [Factual secondary headline]

[Integrated account, 55-105 words.]

<div class="impact" markdown="1">

**Builder impact:** [One concrete consequence, 12-32 words.]

</div>

<div class="evidence" markdown="1">

*Evidence:* [Primary: descriptive source](https://example.com) · Independent
evidence not found · [HN: substantive
thread](https://news.ycombinator.com/item?id=NNN)

</div>

</article>

## On the radar

<div class="radar" markdown="1">

- **[Literal label]:** [18-35 words; include a descriptive source link in the
  sentence.]

</div>

<div class="day-note" markdown="1">

**Day note:** [Only for a continuation, access failure, or evidence condition
that applies to the whole chapter.]

</div>
```

There is at most one `lead-story`. Delete `What else mattered`, `On the radar`,
and `Day note` when empty. Every full item gets exactly one builder-impact line
and one evidence block. Evidence labels are limited to `Primary`, `Independent`,
`Data`, `Code`, `HN`, and `Social`; an explicit missing state is plain text, not
a dead link.
