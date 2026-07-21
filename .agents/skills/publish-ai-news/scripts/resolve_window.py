#!/usr/bin/env python3
"""Resolve explicit or cadence-based news windows with UTC day boundaries."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cadence", required=True, choices=("daily", "weekly", "monthly"))
    parser.add_argument("--from", dest="from_date", type=date.fromisoformat)
    parser.add_argument("--to", dest="to_date", type=date.fromisoformat)
    parser.add_argument("--timezone", required=True)
    parser.add_argument("--allow-partial", action="store_true")
    parser.add_argument(
        "--now",
        help="Optional aware ISO timestamp for deterministic validation; defaults to now.",
    )
    return parser.parse_args()


def parse_now(value: str | None, zone: ZoneInfo) -> datetime:
    if value is None:
        return datetime.now(zone)
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("--now must include a UTC offset or Z")
    return parsed.astimezone(zone)


def default_window(cadence: str, today: date) -> tuple[date, date]:
    if cadence == "daily":
        previous = today - timedelta(days=1)
        return previous, previous
    if cadence == "weekly":
        current_monday = today - timedelta(days=today.weekday())
        end = current_monday - timedelta(days=1)
        return end - timedelta(days=6), end
    first_of_month = today.replace(day=1)
    end = first_of_month - timedelta(days=1)
    return end.replace(day=1), end


def resolve(args: argparse.Namespace) -> dict[str, object]:
    try:
        zone = ZoneInfo(args.timezone)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"unknown timezone: {args.timezone}") from exc

    if (args.from_date is None) != (args.to_date is None):
        raise ValueError("--from and --to must be supplied together")

    now = parse_now(args.now, zone)
    if args.from_date is None:
        start, end = default_window(args.cadence, now.date())
    else:
        start, end = args.from_date, args.to_date

    if end < start:
        raise ValueError("--to precedes --from")
    if end >= now.date() and not args.allow_partial:
        raise ValueError("window includes the current or a future local day; pass --allow-partial explicitly")

    days = []
    cursor = start
    while cursor <= end:
        local_start = datetime.combine(cursor, time.min, zone)
        local_end = datetime.combine(cursor + timedelta(days=1), time.min, zone)
        days.append(
            {
                "date": cursor.isoformat(),
                "weekday": cursor.strftime("%A"),
                "local_start": local_start.isoformat(),
                "local_end_exclusive": local_end.isoformat(),
                "utc_start": local_start.astimezone(timezone.utc).isoformat(),
                "utc_end_exclusive": local_end.astimezone(timezone.utc).isoformat(),
                "utc_start_epoch": int(local_start.timestamp()),
                "utc_end_epoch": int(local_end.timestamp()),
            }
        )
        cursor += timedelta(days=1)

    return {
        "cadence": args.cadence,
        "timezone": str(zone),
        "from": start.isoformat(),
        "to": end.isoformat(),
        "partial": end >= now.date(),
        "resolved_at": now.isoformat(),
        "days": days,
    }


def main() -> None:
    args = parse_args()
    try:
        result = resolve(args)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
