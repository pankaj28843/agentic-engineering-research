from __future__ import annotations

import importlib.util
import unittest
from argparse import Namespace
from datetime import date
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "skills"
    / "publish-ai-news"
    / "scripts"
    / "resolve_window.py"
)
SPEC = importlib.util.spec_from_file_location("resolve_window", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def args(**overrides: object) -> Namespace:
    values = {
        "cadence": "daily",
        "from_date": None,
        "to_date": None,
        "timezone": "Europe/Copenhagen",
        "allow_partial": False,
        "now": "2026-07-21T12:00:00+02:00",
    }
    values.update(overrides)
    return Namespace(**values)


class ResolveWindowTests(unittest.TestCase):
    def test_daily_defaults_to_previous_completed_day(self) -> None:
        result = MODULE.resolve(args())
        self.assertEqual((result["from"], result["to"]), ("2026-07-20", "2026-07-20"))

    def test_weekly_defaults_to_previous_iso_week(self) -> None:
        result = MODULE.resolve(args(cadence="weekly"))
        self.assertEqual((result["from"], result["to"]), ("2026-07-13", "2026-07-19"))

    def test_monthly_defaults_to_previous_calendar_month(self) -> None:
        result = MODULE.resolve(args(cadence="monthly"))
        self.assertEqual((result["from"], result["to"]), ("2026-06-01", "2026-06-30"))

    def test_explicit_range_preserves_dst_aware_utc_boundaries(self) -> None:
        result = MODULE.resolve(
            args(
                from_date=date(2026, 3, 29),
                to_date=date(2026, 3, 29),
                now="2026-04-01T12:00:00+02:00",
            )
        )
        day = result["days"][0]
        self.assertEqual(day["utc_start"], "2026-03-28T23:00:00+00:00")
        self.assertEqual(day["utc_end_exclusive"], "2026-03-29T22:00:00+00:00")

    def test_requires_both_explicit_bounds(self) -> None:
        with self.assertRaisesRegex(ValueError, "supplied together"):
            MODULE.resolve(args(from_date=date(2026, 7, 1)))

    def test_rejects_current_day_without_partial_intent(self) -> None:
        with self.assertRaisesRegex(ValueError, "current or a future"):
            MODULE.resolve(
                args(from_date=date(2026, 7, 21), to_date=date(2026, 7, 21))
            )

    def test_allows_labeled_partial_window(self) -> None:
        result = MODULE.resolve(
            args(
                from_date=date(2026, 7, 21),
                to_date=date(2026, 7, 21),
                allow_partial=True,
            )
        )
        self.assertTrue(result["partial"])


if __name__ == "__main__":
    unittest.main()
