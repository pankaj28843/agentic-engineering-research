from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / ".agents/skills/publish-ai-news/scripts/validate_issue.py"
SPEC = importlib.util.spec_from_file_location("validate_issue", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def chapter(*, weekday: str = "Wednesday", extra: str = "") -> str:
    brief = "A consequential release changed the default deployment path while a measured evaluation exposed a practical limit, giving builders one verified capability and one explicit reason to retain their existing safeguards today."
    impact = "Pin the new dependency in a staging branch and rerun the production evaluation before changing the default route."
    return f'''# 2026-07-01, {weekday}: Models Meet Production Reality

<div class="daily-brief" markdown="1">

**Daily brief:** {brief}

</div>

<article class="lead-story" markdown="1">

## A release changes deployment choices

The primary artifact documents a bounded change and the independent analysis checks its operational consequences without extending the claim beyond the captured evidence.

<div class="impact" markdown="1">

**Builder impact:** {impact}

</div>

<div class="evidence" markdown="1">

*Evidence:* [Primary: release notes](https://example.com/release) · [Independent: evaluation](https://example.org/evaluation)

</div>

</article>
{extra}
'''


class ValidateIssueTests(unittest.TestCase):
    def write(self, text: str) -> Path:
        root = Path(tempfile.mkdtemp())
        path = root / "02-2026-07-01.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_valid_chapter_passes(self) -> None:
        path = self.write(chapter())
        result = MODULE.validate_chapter(path, date(2026, 7, 1), 800)
        self.assertEqual([], result["errors"])

    def test_colon_inside_link_title_is_not_an_evidence_label(self) -> None:
        path = self.write(
            chapter().replace(
                "[Primary: release notes]",
                "[Primary: Better Models: Worse Tools]",
            )
        )
        result = MODULE.validate_chapter(path, date(2026, 7, 1), 800)
        self.assertEqual([], result["errors"])

    def test_rejects_wrong_weekday_and_missing_impact(self) -> None:
        path = self.write(chapter(weekday="Tuesday").replace("**Builder impact:**", "**Consequence:**"))
        result = MODULE.validate_chapter(path, date(2026, 7, 1), 800)
        self.assertTrue(any("weekday" in error for error in result["errors"]))
        self.assertTrue(any("builder impact" in error for error in result["errors"]))

    def test_rejects_single_link_without_missing_state(self) -> None:
        path = self.write(chapter().replace(" · [Independent: evaluation](https://example.org/evaluation)", ""))
        result = MODULE.validate_chapter(path, date(2026, 7, 1), 800)
        self.assertTrue(any("evidence has 1 links" in error for error in result["errors"]))

    def test_rejects_empty_conditional_heading(self) -> None:
        path = self.write(chapter(extra="\n## What else mattered\n"))
        result = MODULE.validate_chapter(path, date(2026, 7, 1), 800)
        self.assertTrue(any("What else mattered heading is empty" in error for error in result["errors"]))

    def story_payload(self) -> dict[str, object]:
        return {
            "publication": {
                "title": "July issue",
                "timezone": "Europe/Copenhagen",
                "from": "2026-07-01",
                "to": "2026-07-02",
                "evidence_cutoff_at": "2026-07-03T00:01:00+02:00",
                "rubric_version": "1",
            },
            "stories": [
                {
                    "id": "2026-07-01-release",
                    "edition_date": "2026-07-01",
                    "title": "Release",
                    "placement": "lead",
                    "material_delta": "A dated release changed an inspectable capability.",
                    "confidence": "B",
                    "discussion_intensity": 2,
                    "date_rule": 4,
                    "continuation_of": None,
                    "relevance": {
                        "consequence": 28,
                        "catch_up_dependency": 18,
                        "novelty_or_correction": 17,
                        "durability": 13,
                        "breadth": 8,
                        "overlap_adjustment": 0,
                        "total": 84,
                    },
                    "source_urls": ["https://example.com/release"],
                },
                {
                    "id": "2026-07-02-release-update",
                    "edition_date": "2026-07-02",
                    "title": "Release update",
                    "placement": "secondary",
                    "material_delta": "An operational consequence changed the earlier release takeaway.",
                    "confidence": "A",
                    "discussion_intensity": 1,
                    "date_rule": 5,
                    "continuation_of": "2026-07-01-release",
                    "relevance": {
                        "consequence": 22,
                        "catch_up_dependency": 16,
                        "novelty_or_correction": 12,
                        "durability": 10,
                        "breadth": 6,
                        "overlap_adjustment": 0,
                        "total": 66,
                    },
                    "source_urls": ["https://example.org/operation"],
                },
            ],
        }

    def write_stories(self, payload: dict[str, object]) -> Path:
        root = Path(tempfile.mkdtemp())
        path = root / "stories.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_valid_story_data_passes(self) -> None:
        path = self.write_stories(self.story_payload())
        result = MODULE.validate_story_data(path, date(2026, 7, 1), date(2026, 7, 2))
        self.assertEqual([], result["errors"])

    def test_rejects_bad_score_and_forward_continuation(self) -> None:
        payload = self.story_payload()
        stories = payload["stories"]
        assert isinstance(stories, list)
        stories[0]["continuation_of"] = "2026-07-02-release-update"
        stories[0]["relevance"]["total"] = 99
        path = self.write_stories(payload)
        result = MODULE.validate_story_data(path, date(2026, 7, 1), date(2026, 7, 2))
        self.assertTrue(any("component sum" in error for error in result["errors"]))
        self.assertTrue(any("earlier edition date" in error for error in result["errors"]))

    def test_rejects_tracking_source_url(self) -> None:
        payload = self.story_payload()
        stories = payload["stories"]
        assert isinstance(stories, list)
        stories[0]["source_urls"] = ["https://example.com/release?utm_source=feed"]
        path = self.write_stories(payload)
        result = MODULE.validate_story_data(path, date(2026, 7, 1), date(2026, 7, 2))
        self.assertTrue(any("tracking parameters" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
