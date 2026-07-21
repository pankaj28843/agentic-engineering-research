#!/usr/bin/env python3
"""Validate dated Markdown chapters against the publish-ai-news contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import parse_qs, urlparse

DATE_HEADING = re.compile(
    r"^# (?P<date>\d{4}-\d{2}-\d{2}), (?P<weekday>[A-Za-z]+): (?P<theme>.+)$",
    re.MULTILINE,
)
LINK = re.compile(r"\[[^]]+\]\(https?://[^)]+\)")
WORD = re.compile(r"\b\w+(?:[-']\w+)?\b")
TRACKING_PARAMS = {"ei", "gclid", "usg", "utm_campaign", "utm_content", "utm_medium", "utm_source", "ved"}


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid ISO date: {value}") from exc


def dates_between(start: date, end: date) -> list[date]:
    if end < start:
        raise ValueError("--to must not precede --from")
    return [start + timedelta(days=offset) for offset in range((end - start).days + 1)]


def prose_word_count(markdown: str) -> int:
    text = re.sub(r"```.*?```", " ", markdown, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(
        r"\[([^]]+)\]\(https?://[^)]+\)",
        lambda match: match.group(1),
        text,
    )
    return len(WORD.findall(text))


def inner_blocks(markdown: str, class_name: str) -> list[str]:
    pattern = re.compile(
        rf'<div class="{re.escape(class_name)}" markdown="1">\s*(.*?)\s*</div>',
        re.DOTALL,
    )
    return pattern.findall(markdown)


def validate_chapter(path: Path, expected: date, max_words: int) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    heading = DATE_HEADING.search(text)
    if not heading:
        errors.append("missing canonical date heading")
    else:
        if heading.group("date") != expected.isoformat():
            errors.append(f"heading date is {heading.group('date')}, expected {expected.isoformat()}")
        if heading.group("weekday") != expected.strftime("%A"):
            errors.append(f"weekday is {heading.group('weekday')}, expected {expected.strftime('%A')}")
        theme_words = WORD.findall(heading.group("theme"))
        if not 3 <= len(theme_words) <= 7:
            errors.append(f"theme has {len(theme_words)} words, expected 3-7")

    briefs = inner_blocks(text, "daily-brief")
    if len(briefs) != 1:
        errors.append(f"found {len(briefs)} daily briefs, expected 1")
    elif not briefs[0].lstrip().startswith("**Daily brief:**"):
        errors.append("daily brief is missing its literal label")
    else:
        brief_words = prose_word_count(briefs[0].split("**Daily brief:**", 1)[1])
        if not 25 <= brief_words <= 45:
            errors.append(f"daily brief has {brief_words} words, expected 25-45")

    lead_count = text.count('class="lead-story"')
    if lead_count > 1:
        errors.append(f"found {lead_count} lead stories, expected at most 1")

    articles = re.findall(r"<article(?: [^>]*)?>\s*(.*?)\s*</article>", text, re.DOTALL)
    if len(articles) > 4:
        errors.append(f"found {len(articles)} full items, expected at most 4")
    for index, article in enumerate(articles, 1):
        impacts = inner_blocks(article, "impact")
        if len(impacts) != 1 or "**Builder impact:**" not in impacts[0]:
            errors.append(f"item {index} must contain exactly one labeled builder impact")
        elif not 12 <= prose_word_count(impacts[0].split("**Builder impact:**", 1)[1]) <= 32:
            errors.append(f"item {index} builder impact must contain 12-32 words")
        evidence = inner_blocks(article, "evidence")
        if len(evidence) != 1 or "*Evidence:*" not in evidence[0]:
            errors.append(f"item {index} must contain exactly one labeled evidence block")
            continue
        link_count = len(LINK.findall(evidence[0]))
        missing_state = bool(re.search(r"\b(?:not found|inaccessible|not available)\b", evidence[0], re.I))
        if link_count > 4 or (link_count < 2 and not missing_state):
            errors.append(f"item {index} evidence has {link_count} links and no qualifying missing state")
        labels = re.findall(r"\[([A-Z][A-Za-z]+):", evidence[0].replace("*Evidence:*", ""))
        invalid = sorted(set(labels) - {"Primary", "Independent", "Data", "Code", "HN", "Social"})
        if invalid:
            errors.append(f"item {index} uses invalid evidence labels: {', '.join(invalid)}")

    radar_sections = re.findall(r"## On the radar\s+(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if radar_sections:
        radar_count = len(re.findall(r"^- ", radar_sections[0], re.MULTILINE))
        if radar_count == 0:
            errors.append("On the radar heading is empty")
        elif radar_count > 3:
            errors.append(f"found {radar_count} radar items, expected at most 3")
    if "## What else mattered" in text:
        section = text.split("## What else mattered", 1)[1].split("\n## ", 1)[0]
        if "<article" not in section:
            errors.append("What else mattered heading is empty")

    words = prose_word_count(text)
    if words > max_words:
        errors.append(f"chapter has {words} prose words, maximum is {max_words}")
    return {"date": expected.isoformat(), "file": str(path), "words": words, "errors": errors}


def validate_story_data(path: Path, start: date, end: date) -> dict[str, object]:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"file": str(path), "stories": 0, "errors": [f"cannot read valid JSON: {exc}"]}

    if not isinstance(payload, dict):
        return {"file": str(path), "stories": 0, "errors": ["root must be an object"]}
    publication = payload.get("publication")
    if not isinstance(publication, dict):
        errors.append("publication must be an object")
    else:
        if publication.get("from") != start.isoformat():
            errors.append(f"publication.from must be {start.isoformat()}")
        if publication.get("to") != end.isoformat():
            errors.append(f"publication.to must be {end.isoformat()}")
        for field in ("title", "timezone", "evidence_cutoff_at", "rubric_version"):
            if not isinstance(publication.get(field), str) or not publication[field].strip():
                errors.append(f"publication.{field} must be a non-empty string")

    stories = payload.get("stories")
    if not isinstance(stories, list):
        return {"file": str(path), "stories": 0, "errors": errors + ["stories must be an array"]}

    ids: set[str] = set()
    dated_ids: dict[str, date] = {}
    continuations: list[tuple[int, str, date]] = []
    components = {
        "consequence": (0, 35),
        "catch_up_dependency": (0, 20),
        "novelty_or_correction": (0, 20),
        "durability": (0, 15),
        "breadth": (0, 10),
        "overlap_adjustment": (-15, 0),
    }
    for index, story in enumerate(stories, 1):
        prefix = f"story {index}"
        if not isinstance(story, dict):
            errors.append(f"{prefix} must be an object")
            continue
        story_id = story.get("id")
        if not isinstance(story_id, str) or not story_id.strip():
            errors.append(f"{prefix}.id must be a non-empty string")
        elif story_id in ids:
            errors.append(f"{prefix}.id is duplicated: {story_id}")
        else:
            ids.add(story_id)
        try:
            edition_date = date.fromisoformat(story.get("edition_date", ""))
        except (TypeError, ValueError):
            errors.append(f"{prefix}.edition_date must be an ISO date")
            edition_date = start
        else:
            if not start <= edition_date <= end:
                errors.append(f"{prefix}.edition_date is outside the publication window")
            if isinstance(story_id, str):
                dated_ids[story_id] = edition_date
        for field in ("title", "material_delta"):
            if not isinstance(story.get(field), str) or not story[field].strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")
        placement = story.get("placement")
        if placement not in {"lead", "secondary", "radar"}:
            errors.append(f"{prefix}.placement must be lead, secondary, or radar")
        if story.get("confidence") not in {"A", "B", "C", "D"}:
            errors.append(f"{prefix}.confidence must be A, B, C, or D")
        discussion = story.get("discussion_intensity")
        if not isinstance(discussion, int) or isinstance(discussion, bool) or not 0 <= discussion <= 5:
            errors.append(f"{prefix}.discussion_intensity must be an integer from 0 to 5")
        date_rule = story.get("date_rule")
        if not isinstance(date_rule, int) or isinstance(date_rule, bool) or not 1 <= date_rule <= 7:
            errors.append(f"{prefix}.date_rule must be an integer from 1 to 7")

        relevance = story.get("relevance")
        component_total = 0
        if not isinstance(relevance, dict):
            errors.append(f"{prefix}.relevance must be an object")
        else:
            for field, (minimum, maximum) in components.items():
                value = relevance.get(field)
                if not isinstance(value, int) or isinstance(value, bool) or not minimum <= value <= maximum:
                    errors.append(f"{prefix}.relevance.{field} must be an integer from {minimum} to {maximum}")
                else:
                    component_total += value
            total = relevance.get("total")
            if not isinstance(total, int) or isinstance(total, bool):
                errors.append(f"{prefix}.relevance.total must be an integer")
            elif total != component_total:
                errors.append(f"{prefix}.relevance.total is {total}, expected component sum {component_total}")
            elif placement == "lead" and total < 75:
                errors.append(f"{prefix} is a lead below the 75-point threshold")
            elif placement == "secondary" and total < 60 and not story.get("override_reason"):
                errors.append(f"{prefix} is a secondary below 60 without override_reason")

        source_urls = story.get("source_urls")
        if not isinstance(source_urls, list) or not source_urls:
            errors.append(f"{prefix}.source_urls must be a non-empty array")
        else:
            if len(source_urls) != len(set(source_urls)):
                errors.append(f"{prefix}.source_urls contains duplicates")
            for url in source_urls:
                parsed = urlparse(url) if isinstance(url, str) else None
                if parsed is None or parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    errors.append(f"{prefix}.source_urls contains an invalid URL")
                    break
                if parsed.netloc.lower().endswith("google.com") and parsed.path == "/url":
                    errors.append(f"{prefix}.source_urls contains a Google redirect wrapper")
                    break
                tracking = sorted(TRACKING_PARAMS & set(parse_qs(parsed.query)))
                if tracking:
                    errors.append(f"{prefix}.source_urls contains tracking parameters: {', '.join(tracking)}")
                    break

        continuation = story.get("continuation_of")
        if continuation is not None:
            if not isinstance(continuation, str) or not continuation:
                errors.append(f"{prefix}.continuation_of must be null or a non-empty story id")
            else:
                continuations.append((index, continuation, edition_date))

    for index, parent_id, child_date in continuations:
        if parent_id not in dated_ids:
            errors.append(f"story {index}.continuation_of references unknown id: {parent_id}")
        elif dated_ids[parent_id] >= child_date:
            errors.append(f"story {index}.continuation_of must reference an earlier edition date")
    return {"file": str(path), "stories": len(stories), "errors": errors}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("guide_dir", type=Path)
    parser.add_argument("--from", dest="start", type=parse_date, required=True)
    parser.add_argument("--to", dest="end", type=parse_date, required=True)
    parser.add_argument("--max-words", type=int, default=800)
    parser.add_argument("--stories", type=Path, help="Optional machine-readable story ledger")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.max_words < 1:
        raise SystemExit("--max-words must be positive")
    try:
        expected_dates = dates_between(args.start, args.end)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    results: list[dict[str, object]] = []
    seen_paths: set[Path] = set()
    for expected in expected_dates:
        matches = sorted(args.guide_dir.glob(f"*-{expected.isoformat()}.md"))
        if len(matches) != 1:
            results.append({
                "date": expected.isoformat(),
                "file": None,
                "words": 0,
                "errors": [f"found {len(matches)} matching chapter files, expected 1"],
            })
            continue
        seen_paths.add(matches[0])
        results.append(validate_chapter(matches[0], expected, args.max_words))

    dated_files = set(args.guide_dir.glob("*-????-??-??.md"))
    for extra in sorted(dated_files - seen_paths):
        results.append({"date": None, "file": str(extra), "words": 0, "errors": ["dated chapter is outside the requested window"]})

    story_data = validate_story_data(args.stories, args.start, args.end) if args.stories else None
    error_count = sum(len(result["errors"]) for result in results)
    if story_data:
        error_count += len(story_data["errors"])
    payload = {
        "ok": error_count == 0,
        "days": len(expected_dates),
        "errors": error_count,
        "results": results,
        "story_data": story_data,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for result in results:
            for error in result["errors"]:
                print(f"ERROR: {result['date'] or result['file']}: {error}", file=sys.stderr)
        if story_data:
            for error in story_data["errors"]:
                print(f"ERROR: {story_data['file']}: {error}", file=sys.stderr)
        print(f"Validated {len(expected_dates)} day(s); {error_count} error(s).")
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
