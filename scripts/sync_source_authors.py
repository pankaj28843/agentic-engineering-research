#!/usr/bin/env python3
"""Reconcile source-index author/organization cells into sources.json."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID_RE = re.compile(r"^`([^`]+)`$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("theme_dir", type=Path)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if sources.json is not already synchronized; do not write.",
    )
    return parser.parse_args()


def author_map(source_index: Path) -> dict[str, str]:
    authors: dict[str, str] = {}
    for line_no, line in enumerate(
        source_index.read_text(encoding="utf-8").splitlines(),
        1,
    ):
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 5:
            raise SystemExit(
                f"{source_index}:{line_no}: expected five source-table cells"
            )
        match = SOURCE_ID_RE.fullmatch(cells[0])
        if match is None:
            raise SystemExit(f"{source_index}:{line_no}: invalid source ID cell")
        author = cells[2]
        if not author or author == "—":
            raise SystemExit(f"{source_index}:{line_no}: missing author/organization")
        source_id = match.group(1)
        if source_id in authors:
            raise SystemExit(f"{source_index}:{line_no}: duplicate source ID {source_id}")
        authors[source_id] = author
    if not authors:
        raise SystemExit(f"{source_index}: no source rows found")
    return authors


def synchronized_records(
    records: list[object],
    authors: dict[str, str],
    sources_path: Path,
) -> list[dict[str, object]]:
    synchronized: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for record_no, raw in enumerate(records, 1):
        if not isinstance(raw, dict):
            raise SystemExit(f"{sources_path}: record {record_no} is not an object")
        source_ids = raw.get("source_ids")
        if not isinstance(source_ids, list) or not source_ids:
            raise SystemExit(f"{sources_path}: record {record_no} has no source_ids")
        matched_authors: set[str] = set()
        for source_id in source_ids:
            if not isinstance(source_id, str) or source_id not in authors:
                raise SystemExit(
                    f"{sources_path}: record {record_no} has uncataloged source ID "
                    f"{source_id!r}"
                )
            seen_ids.add(source_id)
            matched_authors.add(authors[source_id])
        if len(matched_authors) != 1:
            raise SystemExit(
                f"{sources_path}: record {record_no} combines differing authors: "
                f"{sorted(matched_authors)}"
            )
        author = matched_authors.pop()
        rebuilt: dict[str, object] = {}
        inserted = False
        for key, value in raw.items():
            if key == "author_or_organization":
                continue
            rebuilt[key] = value
            if key == "title":
                rebuilt["author_or_organization"] = author
                inserted = True
        if not inserted:
            rebuilt["author_or_organization"] = author
        synchronized.append(rebuilt)

    unused = sorted(set(authors) - seen_ids)
    if unused:
        raise SystemExit(
            f"{sources_path}: source-index IDs missing from JSON: {', '.join(unused)}"
        )
    return synchronized


def main() -> int:
    args = parse_args()
    theme = args.theme_dir.expanduser().resolve()
    source_index = theme / "source-index.md"
    sources_path = theme / "sources.json"
    authors = author_map(source_index)
    current = json.loads(sources_path.read_text(encoding="utf-8"))
    if not isinstance(current, list):
        raise SystemExit(f"{sources_path}: expected a JSON array")
    synchronized = synchronized_records(current, authors, sources_path)
    expected = json.dumps(synchronized, ensure_ascii=False, indent=2) + "\n"
    actual = sources_path.read_text(encoding="utf-8")
    if args.check:
        if actual != expected:
            raise SystemExit(f"{sources_path}: author metadata is not synchronized")
        print(f"Checked {len(synchronized)} source record(s).")
        return 0
    sources_path.write_text(expected, encoding="utf-8")
    print(f"Synchronized {len(synchronized)} source record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
