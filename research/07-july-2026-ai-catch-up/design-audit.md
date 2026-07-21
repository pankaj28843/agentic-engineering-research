# UI Design Brief: July 2026 Catch-Up Edition

## Design thesis

Make consequence, date, and evidence faster to scan than reputation or hype: a
quiet practitioner broadsheet whose hierarchy remains intact on screen, on an
A4 printout, and in grayscale.

## Product fit

The primary job is reorientation after a three-week absence. The reader needs
to learn which assumptions changed, which stories connect, and which source to
open next. The design therefore privileges four things in this order: date and
daily delta, factual headline, builder impact, and evidence. Methodology and
discussion strength remain available without competing for first attention.

The edition has two reading paths. The scan path uses the period map, daily
briefs, headlines, and bold builder-impact sentences. The evidence path follows
the factual accounts and descriptive links. A page fails when either path
requires decoding decorative labels, jumping between columns, or reading raw
URLs.

## UX priorities

1. Make a missed three-week period understandable without reading every item.
2. Keep evidence adjacent to the claim it supports and visibly distinguish
   unavailable evidence from an omitted citation.
3. Fit every date into one or two A4 pages without per-day type changes or
   hidden overflow.
4. Let quiet days remain sparse rather than disguising them with layout filler.

## Tokens and visual language

| Token | Value or rule | Reason |
|---|---|---|
| Mood | Restrained technical broadsheet | Signals editorial judgment rather than marketing |
| Paper | White | Maximizes print predictability and contrast |
| Ink | Near-black `#181817` | Softer than process black while retaining legibility |
| Accent | Dark red `#7a1f27` | One non-vendor color for rules and links |
| Muted ink | Neutral gray `#5d5b57` | Separates metadata without relying on hue |
| Rules | Neutral gray `#b8b4ad` | Builds hierarchy without cards or shaded panels |
| Body | 10.5 pt minimum, 1.45 line height | Keeps dense reporting readable on A4 |
| Measure | 118 mm maximum, roughly 55-72 characters | Supports sustained reading without columns |
| Shape | Square edges, thin rules, no shadows | Preserves an editorial rather than app-dashboard character |
| Imagery | None unless an evidence-bearing diagram earns space | Avoids atmosphere competing with reporting |
| Motion | Not applicable to the PDF | No animated behavior to explain or disable |

The hierarchy uses type size, weight, spacing, rule weight, and explicit labels.
Color is never the only carrier of state. The accent must be replaceable by
black without erasing the distinction between date, headline, impact, and
evidence.

## Layout rules

| Surface | Rule | Narrow or print behavior | Failure state |
|---|---|---|---|
| Cover | Literal title, window, and purpose; no decorative hero | One A4 page at final size | Title wraps awkwardly or hides the reporting window |
| Period map | Five to eight arcs and at most five standalone dates | One A4 page; shorten copy before reducing type | Map spills or introduces facts absent from daily chapters |
| Daily opener | ISO date, weekday, short theme, then daily brief | Every date begins on a new page | Date is stranded or mistaken for an item heading |
| Full item | Headline, account, impact, optional qualification, evidence | Keep impact and evidence blocks intact where possible | Metadata strands at the top of a page |
| Radar | Compact prose separated by a neutral rule | Remains one column | Radar becomes visually equal to a lead |
| Links | Descriptive anchor text, underlined | Clickable in PDF and understandable in extracted text | Raw URL, "click here," or color-only affordance |
| Overflow | Apply the editorial cut hierarchy | One or two pages per date | Per-day font, margin, scale, or tracking override |

The PDF is the primary viewport. Desktop and mobile PDF readers may zoom or
reflow controls around it, but the publication itself does not adopt responsive
web columns. The acceptance viewports are the physical A4 page and rasterized
A4 pages at a legible inspection resolution.

## Accessibility requirements

- [x] Body text remains at least 10.5 pt with line height at least 1.45.
- [x] Reading order in extracted PDF text matches the visible one-column order.
- [x] Heading levels are semantic and sequential within each chapter.
- [x] Every link uses source-descriptive text and remains clickable after PDF
  generation.
- [x] Information encoded with the dark-red accent is also encoded through
  weight, rule, placement, or label.
- [x] Grayscale rasterization preserves lead, secondary, radar, impact, and
  evidence hierarchy.
- [x] No page is blank, clipped, or dominated by accidental whitespace.
- [x] Headings retain at least two following lines; evidence and qualification
  blocks are not stranded at a page top.

## Anti-patterns to avoid

- Cards, pills, badges, gradients, shadows, ornamental dividers, and decorative
  charts.
- Two-column body copy that speeds scanning but weakens deep reading.
- Visible relevance or discussion scores that turn editorial judgment into a
  gamified leaderboard.
- Uniform visual weight for primary evidence, community discussion, and social
  signal.
- Filling quiet dates to achieve false visual symmetry.
- Repeated QR codes or printed raw URLs that consume the daily page budget.

## Implementation handoff

The initial rules live in [newspaper.css](newspaper.css). The renderer must
append this stylesheet after its built-in theme, retain A4 geometry, and reject
missing stylesheet inputs before mutating source or output files.

Validation has three layers:

1. Mechanical checks: A4 dimensions, one-to-two pages per date, nonblank pages,
   required date text, link annotations, and extracted reading order.
2. Raster review: cover, period map, densest and quietest dates, every two-page
   boundary, and final page.
3. Progressive visual reasoning: inspect the smallest useful previews first,
   select suspicious tiles from a contact sheet, and escalate only those areas
   needed to decide a concrete rework.

The final stylesheet passed all three layers on 22 July 2026. The fixture set
contains 21 independently rendered A4 chapters: 11 use one page and 10 use two,
with no blank or clipped pages. The 63-page assembled PDF preserves date order
and all 101 canonical source links. Progressive grayscale review covered the
cover, one-page period map, quiet July 10 chapter, dense July 15 break, both
July 21 pages, every generated page through blank-tile checks, and the final
page. The PDF remains untagged, so semantic accessibility depends on the source
Markdown and correct extracted reading order rather than a tagged PDF tree.
