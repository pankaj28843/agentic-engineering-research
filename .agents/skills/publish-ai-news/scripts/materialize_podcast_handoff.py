#!/usr/bin/env python3
"""Materialize a deterministic podcast evidence handoff from a news packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "publish-ai-news-podcast-handoff/v1"
DATED_GUIDE_RE = re.compile(r"^\d{2}-(\d{4}-\d{2}-\d{2})\.md$")
HEADING_RE = re.compile(r"^# (\d{4}-\d{2}-\d{2}), ([A-Za-z]+): (.+)$", re.MULTILINE)
ARTICLE_RE = re.compile(r"<article(?:\s[^>]*)?>(.*?)</article>", re.DOTALL)
HN_ITEM_RE = re.compile(r"^https://news\.ycombinator\.com/item\?id=\d+$")


class HandoffError(ValueError):
    """Raised when packet evidence cannot be joined without interpretation."""


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HandoffError(f"cannot read {path}: {exc}") from exc


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def file_binding(path: Path, relative_to: Path) -> dict[str, Any]:
    content = path.read_bytes()
    return {
        "path": path.relative_to(relative_to).as_posix(),
        "sha256": sha256_bytes(content),
        "byte_count": len(content),
    }


def read_utf8_exact(path: Path) -> str:
    try:
        return path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HandoffError(f"{path}: dated guide must be valid UTF-8: {exc}") from exc


def parse_date(value: str, label: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise HandoffError(f"{label} must be an ISO date: {value!r}") from exc


def normalize_timestamp(value: str, label: str) -> str:
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise HandoffError(f"{label} must be an ISO timestamp: {value!r}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise HandoffError(f"{label} must include a UTC offset: {value!r}")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def timestamp_value(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def inclusive_dates(start: date, end: date) -> list[date]:
    if start > end:
        raise HandoffError(f"from date {start} is after to date {end}")
    return [start + timedelta(days=offset) for offset in range((end - start).days + 1)]


def clean_markdown_text(value: str, label: str | None = None) -> str:
    text = value.strip()
    if label:
        text = re.sub(rf"^\*\*{re.escape(label)}:\*\*\s*", "", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"</?[^>]+>", " ", text)
    text = text.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", text).strip()


def extract_div_blocks(markdown: str, class_name: str, label: str) -> list[str]:
    pattern = re.compile(
        rf'<div class="{re.escape(class_name)}"[^>]*>(.*?)</div>', re.DOTALL
    )
    return [
        clean_markdown_text(match.group(1), label)
        for match in pattern.finditer(markdown)
    ]


def validate_publication(
    publication: Any, start_override: str | None, end_override: str | None
) -> tuple[date, date]:
    if not isinstance(publication, dict):
        raise HandoffError("stories.json publication must be an object")
    required = (
        "title",
        "timezone",
        "from",
        "to",
        "evidence_cutoff_at",
        "rubric_version",
    )
    missing = [field for field in required if not publication.get(field)]
    if missing:
        raise HandoffError(f"stories.json publication is missing: {', '.join(missing)}")
    if (start_override is None) != (end_override is None):
        raise HandoffError("supply both --from and --to, or neither")

    publication_start = parse_date(str(publication["from"]), "publication.from")
    publication_end = parse_date(str(publication["to"]), "publication.to")
    start = (
        parse_date(start_override, "--from") if start_override else publication_start
    )
    end = parse_date(end_override, "--to") if end_override else publication_end
    if start != publication_start or end != publication_end:
        raise HandoffError(
            "requested window must exactly match the frozen publication window "
            f"{publication_start} through {publication_end}"
        )
    inclusive_dates(start, end)
    return start, end


def index_sources(raw_sources: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(raw_sources, list):
        raise HandoffError("sources.json must contain a list")
    sources: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(raw_sources, 1):
        if not isinstance(record, dict):
            raise HandoffError(f"sources.json record {index} is not an object")
        url = record.get("url")
        if not isinstance(url, str) or not url.startswith(("https://", "http://")):
            raise HandoffError(f"sources.json record {index} has an invalid URL")
        if url in sources:
            raise HandoffError(f"sources.json contains duplicate URL: {url}")
        sources[url] = deepcopy(record)
    return sources


def index_stories(raw_stories: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_stories, list):
        raise HandoffError("stories.json stories must contain a list")
    seen: set[str] = set()
    stories: list[dict[str, Any]] = []
    for index, story in enumerate(raw_stories, 1):
        if not isinstance(story, dict):
            raise HandoffError(f"stories.json story {index} is not an object")
        story_id = story.get("id")
        if not isinstance(story_id, str) or not story_id:
            raise HandoffError(f"stories.json story {index} has no id")
        if story_id in seen:
            raise HandoffError(f"stories.json contains duplicate story id: {story_id}")
        seen.add(story_id)
        source_urls = story.get("source_urls")
        if not isinstance(source_urls, list) or not source_urls:
            raise HandoffError(f"story {story_id} has no source_urls")
        if any(
            not isinstance(url, str) or not url.startswith(("https://", "http://"))
            for url in source_urls
        ):
            raise HandoffError(f"story {story_id} has an invalid source URL")
        if len(source_urls) != len(set(source_urls)):
            raise HandoffError(f"story {story_id} has duplicate source URLs")
        stories.append(deepcopy(story))
    return stories


def dated_guide_files(guide_root: Path) -> dict[date, Path]:
    result: dict[date, Path] = {}
    for path in sorted(guide_root.glob("*.md")):
        match = DATED_GUIDE_RE.match(path.name)
        if not match:
            continue
        chapter_date = parse_date(match.group(1), f"guide filename {path.name}")
        if chapter_date in result:
            raise HandoffError(f"duplicate dated guide chapter for {chapter_date}")
        result[chapter_date] = path
    return result


def story_article_notes(
    markdown: str, stories: list[dict[str, Any]], guide_path: Path
) -> tuple[dict[str, list[str]], dict[str, list[str]], set[str]]:
    caveats = {story["id"]: [] for story in stories}
    discussions = {story["id"]: [] for story in stories}
    article_story_ids: set[str] = set()
    for article_match in ARTICLE_RE.finditer(markdown):
        article = article_match.group(1)
        candidates = [
            story
            for story in stories
            if any(url in article for url in story["source_urls"])
        ]
        if len(candidates) != 1:
            candidate_ids = [story["id"] for story in candidates]
            raise HandoffError(
                f"{guide_path}: article must join exactly one story, found {candidate_ids}"
            )
        story_id = candidates[0]["id"]
        if story_id in article_story_ids:
            raise HandoffError(
                f"{guide_path}: story {story_id} appears in multiple articles"
            )
        article_story_ids.add(story_id)
        caveats[story_id].extend(extract_div_blocks(article, "caveat", "Caveat"))
        discussions[story_id].extend(
            extract_div_blocks(article, "discussion", "Discussion")
        )
    return caveats, discussions, article_story_ids


def materialize_day(
    chapter_date: date,
    guide_path: Path,
    packet_root: Path,
    day_stories: list[dict[str, Any]],
    source_by_url: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    markdown = read_utf8_exact(guide_path)
    heading = HEADING_RE.search(markdown)
    if not heading:
        raise HandoffError(f"{guide_path}: missing dated H1")
    if parse_date(heading.group(1), f"{guide_path} heading") != chapter_date:
        raise HandoffError(f"{guide_path}: heading date does not match filename")
    if heading.group(2) != chapter_date.strftime("%A"):
        raise HandoffError(f"{guide_path}: heading weekday is incorrect")

    daily_briefs = extract_div_blocks(markdown, "daily-brief", "Daily brief")
    if len(daily_briefs) != 1 or not daily_briefs[0]:
        raise HandoffError(f"{guide_path}: expected one non-empty daily brief")
    day_notes = extract_div_blocks(markdown, "day-note", "Day note")
    caveats, discussions, article_story_ids = story_article_notes(
        markdown, day_stories, guide_path
    )

    positioned: list[tuple[int, dict[str, Any]]] = []
    for story in day_stories:
        if story.get("placement") != "radar" and story["id"] not in article_story_ids:
            raise HandoffError(
                f"{guide_path}: non-radar story {story['id']} has no matching article"
            )
        positions = [markdown.find(url) for url in story["source_urls"]]
        positions = [position for position in positions if position >= 0]
        if not positions:
            raise HandoffError(
                f"{guide_path}: story {story['id']} has no canonical source URL in the chapter"
            )
        positioned.append((min(positions), story))
    positioned.sort(key=lambda pair: pair[0])
    if len({position for position, _ in positioned}) != len(positioned):
        raise HandoffError(f"{guide_path}: story guide order is ambiguous")

    ordered_stories: list[dict[str, Any]] = []
    for guide_order, (_, story) in enumerate(positioned, 1):
        source_records: list[dict[str, Any]] = []
        for url in story["source_urls"]:
            record = source_by_url.get(url)
            if record is None:
                raise HandoffError(
                    f"story {story['id']} references uncataloged source: {url}"
                )
            source_records.append(deepcopy(record))
        handoff_story = deepcopy(story)
        handoff_story["guide_order"] = guide_order
        handoff_story["canonical_urls"] = list(story["source_urls"])
        handoff_story["canonical_source_records"] = source_records
        handoff_story["guide_caveats"] = caveats[story["id"]]
        handoff_story["guide_discussion_notes"] = discussions[story["id"]]
        ordered_stories.append(handoff_story)

    zero_story_gap: dict[str, str] | None = None
    if not ordered_stories:
        if not day_notes:
            raise HandoffError(
                f"{guide_path}: zero-story day requires an explicit day note"
            )
        zero_story_gap = {
            "kind": "zero-retained-stories",
            "reason": " ".join(day_notes),
        }

    return {
        "date": chapter_date.isoformat(),
        "weekday": chapter_date.strftime("%A"),
        "chapter_title": heading.group(3).strip(),
        "guide": file_binding(guide_path, packet_root),
        "guide_markdown": markdown,
        "daily_brief": daily_briefs[0],
        "day_notes": day_notes,
        "zero_story_gap": zero_story_gap,
        "story_count": len(ordered_stories),
        "guide_order_story_ids": [story["id"] for story in ordered_stories],
        "stories": ordered_stories,
    }


def materialize_weekly_unions(days: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unions: list[dict[str, Any]] = []
    for start_index in range(0, len(days), 7):
        chunk = days[start_index : start_index + 7]
        if len(chunk) < 7:
            continue
        dates = [parse_date(day["date"], "day date") for day in chunk]
        if dates != inclusive_dates(dates[0], dates[-1]):
            raise HandoffError("weekly union contains a non-contiguous date range")

        ordered_stories = [story for day in chunk for story in day["stories"]]
        ordered_urls: list[str] = []
        seen_urls: set[str] = set()
        for story in ordered_stories:
            for url in story["canonical_urls"]:
                if url not in seen_urls:
                    seen_urls.add(url)
                    ordered_urls.append(url)
        unions.append(
            {
                "from": chunk[0]["date"],
                "to": chunk[-1]["date"],
                "dates": [day["date"] for day in chunk],
                "ordered_guide_paths": [day["guide"]["path"] for day in chunk],
                "ordered_story_ids": [story["id"] for story in ordered_stories],
                "ordered_canonical_urls": ordered_urls,
                "zero_story_dates": [
                    day["date"] for day in chunk if day["story_count"] == 0
                ],
                "story_count": len(ordered_stories),
                "unique_source_count": len(ordered_urls),
            }
        )
    return unions


def build_handoff(
    packet_root: Path,
    *,
    packet_frozen_at: str,
    run_requested_at: str | None = None,
    start_override: str | None = None,
    end_override: str | None = None,
) -> dict[str, Any]:
    packet_root = packet_root.resolve()
    stories_path = packet_root / "stories.json"
    sources_path = packet_root / "sources.json"
    guide_root = packet_root / "guide"
    ledger = load_json(stories_path)
    if not isinstance(ledger, dict):
        raise HandoffError("stories.json root must be an object")
    publication = ledger.get("publication")
    start, end = validate_publication(publication, start_override, end_override)
    sources = index_sources(load_json(sources_path))
    stories = index_stories(ledger.get("stories"))
    frozen_at = normalize_timestamp(packet_frozen_at, "--packet-frozen-at")
    requested_at = (
        normalize_timestamp(run_requested_at, "--run-requested-at")
        if run_requested_at
        else None
    )
    evidence_cutoff_at = normalize_timestamp(
        str(publication["evidence_cutoff_at"]), "publication.evidence_cutoff_at"
    )
    if timestamp_value(evidence_cutoff_at) > timestamp_value(frozen_at):
        raise HandoffError(
            "publication evidence cutoff is after the packet freeze marker"
        )
    if requested_at and timestamp_value(requested_at) > timestamp_value(frozen_at):
        raise HandoffError("run request timestamp is after the packet freeze marker")

    expected_dates = inclusive_dates(start, end)
    expected_date_set = set(expected_dates)
    guides = dated_guide_files(guide_root)
    if set(guides) != expected_date_set:
        missing = sorted(expected_date_set - set(guides))
        extra = sorted(set(guides) - expected_date_set)
        raise HandoffError(
            f"dated guide window mismatch; missing={missing}, extra={extra}"
        )

    stories_by_date: dict[date, list[dict[str, Any]]] = {
        day: [] for day in expected_dates
    }
    for story in stories:
        edition_date = parse_date(
            str(story.get("edition_date")), f"story {story['id']} date"
        )
        if edition_date not in expected_date_set:
            raise HandoffError(f"story {story['id']} is outside the publication window")
        stories_by_date[edition_date].append(story)

    days = [
        materialize_day(day, guides[day], packet_root, stories_by_date[day], sources)
        for day in expected_dates
    ]
    ordered_ids = [story["id"] for day in days for story in day["stories"]]
    ledger_ids = [story["id"] for story in stories]
    if set(ordered_ids) != set(ledger_ids) or len(ordered_ids) != len(ledger_ids):
        raise HandoffError("guide order does not cover each ledger story exactly once")

    referenced_urls = [url for story in stories for url in story["source_urls"]]
    referenced_set = set(referenced_urls)
    missing_urls = sorted(referenced_set - set(sources))
    unused_urls = sorted(set(sources) - referenced_set)
    if missing_urls or unused_urls:
        raise HandoffError(
            f"source join is not exact; missing={missing_urls}, unused={unused_urls}"
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "timeline": {
            "run_requested": {
                "at": requested_at,
                "observation": "provided" if requested_at else "unobserved",
            },
            "packet_frozen": {"at": frozen_at, "observation": "provided"},
        },
        "packet": {
            "slug": packet_root.name,
            "publication": deepcopy(publication),
            "stories": file_binding(stories_path, packet_root),
            "sources": file_binding(sources_path, packet_root),
            "dated_guides": [
                file_binding(guides[day], packet_root) for day in expected_dates
            ],
        },
        "ordering_rule": (
            "inclusive publication date, then first canonical story URL occurrence "
            "in the corresponding dated guide chapter"
        ),
        "days": days,
        "weekly_unions": materialize_weekly_unions(days),
        "validation": {
            "day_count": len(days),
            "story_count": len(stories),
            "zero_story_dates": [
                day["date"] for day in days if day["story_count"] == 0
            ],
            "canonical_source_record_count": len(sources),
            "story_source_reference_count": len(referenced_urls),
            "unique_story_source_url_count": len(referenced_set),
            "hn_source_reference_count": sum(
                bool(HN_ITEM_RE.match(url)) for url in referenced_urls
            ),
            "missing_source_urls": missing_urls,
            "unused_source_urls": unused_urls,
            "guide_order_story_ids_are_complete": True,
        },
    }


def serialize_handoff(payload: dict[str, Any]) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def write_handoff(payload: dict[str, Any], output: Path) -> dict[str, Any]:
    content = serialize_handoff(payload)
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(content)
    try:
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    return {
        "output": str(output),
        "sha256": sha256_bytes(content),
        "byte_count": len(content),
        "day_count": payload["validation"]["day_count"],
        "story_count": payload["validation"]["story_count"],
        "canonical_source_record_count": payload["validation"][
            "canonical_source_record_count"
        ],
        "story_source_reference_count": payload["validation"][
            "story_source_reference_count"
        ],
        "weekly_union_count": len(payload["weekly_unions"]),
        "zero_story_dates": payload["validation"]["zero_story_dates"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "packet", type=Path, help="research packet containing stories.json"
    )
    parser.add_argument("--from", dest="start")
    parser.add_argument("--to", dest="end")
    parser.add_argument("--packet-frozen-at", required=True)
    parser.add_argument("--run-requested-at")
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = build_handoff(
            args.packet,
            packet_frozen_at=args.packet_frozen_at,
            run_requested_at=args.run_requested_at,
            start_override=args.start,
            end_override=args.end,
        )
        summary = write_handoff(payload, args.output)
    except (HandoffError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
