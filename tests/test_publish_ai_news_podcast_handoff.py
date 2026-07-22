from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "skills"
    / "publish-ai-news"
    / "scripts"
    / "materialize_podcast_handoff.py"
)
SPEC = importlib.util.spec_from_file_location("materialize_podcast_handoff", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PodcastHandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.packet = Path(self.temporary.name) / "07-test-issue"
        (self.packet / "guide").mkdir(parents=True)
        self.write_packet()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_packet(self) -> None:
        primary = "https://example.com/release"
        hn_primary = "https://news.ycombinator.com/item?id=123"
        hn_radar = "https://news.ycombinator.com/item?id=456"
        ledger = {
            "publication": {
                "title": "Test issue",
                "timezone": "Europe/Copenhagen",
                "from": "2026-07-01",
                "to": "2026-07-07",
                "evidence_cutoff_at": "2026-07-08T00:01:00+02:00",
                "rubric_version": "test-v1",
                "partial": False,
            },
            "stories": [
                {
                    "id": "release",
                    "edition_date": "2026-07-01",
                    "title": "A release",
                    "placement": "lead",
                    "material_delta": "A release changed the deployment boundary.",
                    "confidence": "B",
                    "discussion_intensity": 2,
                    "source_urls": [primary, hn_primary],
                },
                {
                    "id": "radar",
                    "edition_date": "2026-07-01",
                    "title": "A radar item",
                    "placement": "radar",
                    "material_delta": "A discussion exposed a follow-up question.",
                    "confidence": "C",
                    "discussion_intensity": 1,
                    "source_urls": [hn_radar],
                },
            ],
        }
        sources = [
            {"url": primary, "title": "Release", "quality": "primary", "role": "fact"},
            {
                "url": hn_primary,
                "title": "Release discussion",
                "quality": "community",
                "role": "interpretation",
            },
            {
                "url": hn_radar,
                "title": "Radar discussion",
                "quality": "community",
                "role": "lead",
            },
        ]
        (self.packet / "stories.json").write_text(
            json.dumps(ledger, indent=2), encoding="utf-8"
        )
        (self.packet / "sources.json").write_text(
            json.dumps(sources, indent=2), encoding="utf-8"
        )

        first = f"""# 2026-07-01, Wednesday: Release boundary moves

<div class="daily-brief" markdown="1">

**Daily brief:** One bounded release changed a deployment choice, while a
community thread raised a separate question worth watching.

</div>

<article class="lead-story" markdown="1">

## A release changes deployment choices

The primary artifact records a bounded release.

The factual record reports a 3\u00d7 throughput change under the named fixture.

<div class="impact" markdown="1">

**Builder impact:** Preserve the measured fixture and deployment boundary when
turning this result into an engineering decision.

</div>

<div class="caveat" markdown="1">

**Caveat:** Production reproduction remains unavailable.

</div>

<div class="discussion" markdown="1">

**Discussion:** Practitioners compared `staging` failure modes.

</div>

<div class="evidence" markdown="1">

*Evidence:* [Primary: release]({primary}) · [HN: discussion]({hn_primary})

</div>

</article>

## On the radar

- [A separate question]({hn_radar}) remains open because the participant report
  does not establish whether the behavior reproduces outside its test harness.
"""
        (self.packet / "guide" / "02-2026-07-01.md").write_text(first, encoding="utf-8")
        start = date(2026, 7, 2)
        for offset in range(6):
            day = start + timedelta(days=offset)
            chapter = f"""# {day.isoformat()}, {day.strftime("%A")}: No retained story

<div class="daily-brief" markdown="1">

**Daily brief:** No candidate cleared the frozen evidence and relevance rules.

</div>

<div class="day-note" markdown="1">

**Day note:** The evidence review retained no publishable story for this date.

</div>
"""
            (
                self.packet / "guide" / f"{offset + 3:02d}-{day.isoformat()}.md"
            ).write_text(chapter, encoding="utf-8")

    def build(self) -> dict[str, object]:
        return MODULE.build_handoff(
            self.packet,
            packet_frozen_at="2026-07-22T17:00:00+02:00",
            run_requested_at="2026-07-22T14:30:00Z",
            start_override="2026-07-01",
            end_override="2026-07-07",
        )

    def test_materializes_exact_order_notes_joins_and_week(self) -> None:
        payload = self.build()
        self.assertEqual(MODULE.SCHEMA_VERSION, payload["schema_version"])
        self.assertEqual(
            "2026-07-22T15:00:00Z", payload["timeline"]["packet_frozen"]["at"]
        )
        self.assertEqual(7, payload["validation"]["day_count"])
        self.assertEqual(2, payload["validation"]["story_count"])
        self.assertEqual(3, payload["validation"]["canonical_source_record_count"])
        self.assertEqual(2, payload["validation"]["hn_source_reference_count"])
        self.assertEqual(
            ["release", "radar"], payload["days"][0]["guide_order_story_ids"]
        )
        self.assertEqual(
            ["Production reproduction remains unavailable."],
            payload["days"][0]["stories"][0]["guide_caveats"],
        )
        self.assertEqual(
            ["Practitioners compared staging failure modes."],
            payload["days"][0]["stories"][0]["guide_discussion_notes"],
        )
        self.assertEqual(
            "zero-retained-stories", payload["days"][1]["zero_story_gap"]["kind"]
        )
        self.assertEqual(1, len(payload["weekly_unions"]))
        self.assertEqual(
            ["release", "radar"], payload["weekly_unions"][0]["ordered_story_ids"]
        )

    def test_serialization_is_byte_stable_and_has_no_absolute_packet_path(self) -> None:
        first = MODULE.serialize_handoff(self.build())
        second = MODULE.serialize_handoff(self.build())
        self.assertEqual(first, second)
        self.assertNotIn(str(self.packet).encode(), first)
        self.assertIn(b'"path": "guide/02-2026-07-01.md"', first)

        output = Path(self.temporary.name) / "handoff.json"
        summary = MODULE.write_handoff(self.build(), output)
        self.assertEqual(hashlib.sha256(first).hexdigest(), summary["sha256"])
        self.assertEqual(first, output.read_bytes())

    def test_full_guide_markdown_survives_serialization_exactly(self) -> None:
        guide_path = self.packet / "guide" / "02-2026-07-01.md"
        expected = guide_path.read_bytes().decode("utf-8")

        serialized = MODULE.serialize_handoff(self.build())
        restored = json.loads(serialized)
        actual = restored["days"][0]["guide_markdown"]

        self.assertEqual(expected, actual)
        self.assertIn(
            "The factual record reports a 3\u00d7 throughput change under the named fixture.",
            actual,
        )
        self.assertIn(
            "**Builder impact:** Preserve the measured fixture and deployment boundary",
            actual,
        )
        self.assertIn(
            "## On the radar\n\n- [A separate question]",
            actual,
        )
        self.assertTrue(actual.endswith("outside its test harness.\n"))

    def test_rejects_unused_source_record(self) -> None:
        path = self.packet / "sources.json"
        sources = json.loads(path.read_text(encoding="utf-8"))
        sources.append(
            {
                "url": "https://example.net/unused",
                "title": "Unused",
                "quality": "primary",
                "role": "none",
            }
        )
        path.write_text(json.dumps(sources), encoding="utf-8")
        with self.assertRaisesRegex(MODULE.HandoffError, "source join is not exact"):
            self.build()

    def test_rejects_story_not_locatable_in_its_guide(self) -> None:
        path = self.packet / "guide" / "02-2026-07-01.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "https://news.ycombinator.com/item?id=456",
                "https://example.net/missing",
            ),
            encoding="utf-8",
        )
        with self.assertRaises(MODULE.HandoffError):
            self.build()

    def test_rejects_non_radar_story_without_article(self) -> None:
        path = self.packet / "guide" / "02-2026-07-01.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace('<article class="lead-story" markdown="1">', "")
        text = text.replace("</article>", "", 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(MODULE.HandoffError, "has no matching article"):
            self.build()

    def test_rejects_unobserved_timezone_for_frozen_marker(self) -> None:
        with self.assertRaisesRegex(MODULE.HandoffError, "include a UTC offset"):
            MODULE.build_handoff(
                self.packet,
                packet_frozen_at="2026-07-22T17:00:00",
            )

    def test_rejects_impossible_timeline_order(self) -> None:
        with self.assertRaisesRegex(MODULE.HandoffError, "evidence cutoff is after"):
            MODULE.build_handoff(
                self.packet,
                packet_frozen_at="2026-07-07T20:00:00Z",
            )
        with self.assertRaisesRegex(MODULE.HandoffError, "request timestamp is after"):
            MODULE.build_handoff(
                self.packet,
                packet_frozen_at="2026-07-22T15:00:00Z",
                run_requested_at="2026-07-22T15:00:01Z",
            )

    def test_rejects_malformed_or_duplicate_story_source_urls(self) -> None:
        path = self.packet / "stories.json"
        ledger = json.loads(path.read_text(encoding="utf-8"))
        ledger["stories"][0]["source_urls"] = ["https://example.com/release", 42]
        path.write_text(json.dumps(ledger), encoding="utf-8")
        with self.assertRaisesRegex(MODULE.HandoffError, "invalid source URL"):
            self.build()

        self.write_packet()
        ledger = json.loads(path.read_text(encoding="utf-8"))
        ledger["stories"][0]["source_urls"] = [
            "https://example.com/release",
            "https://example.com/release",
        ]
        path.write_text(json.dumps(ledger), encoding="utf-8")
        with self.assertRaisesRegex(MODULE.HandoffError, "duplicate source URLs"):
            self.build()


if __name__ == "__main__":
    unittest.main()
