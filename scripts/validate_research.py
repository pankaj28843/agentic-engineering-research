#!/usr/bin/env python3
"""Validate the durable research repository structure."""

from __future__ import annotations

import ast
import json
import re
import sys
from collections.abc import Mapping
from decimal import Decimal, DecimalException, ROUND_HALF_EVEN
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_ROOT = ROOT / "research"
REQUIRED_THEME_FILES = (
    "README.md",
    "briefing.md",
    "source-index.md",
    "research-log.md",
)
MIN_GUIDE_CHAPTERS = 8
MIN_GUIDE_WORDS = 18_000


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_agents() -> None:
    agents = ROOT / "AGENTS.md"
    if not agents.exists():
        fail("AGENTS.md is missing")
    text = agents.read_text(encoding="utf-8")
    required = [
        "cdp daemon status --json",
        "Do **not** run `cdp daemon start`",
        "Do **not** run `cdp daemon restart`",
        "cdp --browser-mode headed",
        "including Hacker News",
        "podcast handoff",
        "tmp/",
    ]
    for needle in required:
        if needle not in text:
            fail(f"AGENTS.md is missing required instruction: {needle}")


def validate_skill_browser_examples() -> None:
    skills = (
        ROOT / ".agents/skills/theme-deep-research/SKILL.md",
        ROOT / ".agents/skills/publish-ai-news/SKILL.md",
    )
    for skill in skills:
        if not skill.exists():
            fail(f"browser-facing skill is missing: {skill}")
        text = skill.read_text(encoding="utf-8")
        if "cdp --browser-mode headed workflow" not in text:
            fail(f"{skill}: missing headed CDP workflow examples")
        for line_no, line in enumerate(text.splitlines(), 1):
            command = line.lstrip()
            if re.match(r"(?:curl|wget|http|https|xh)\s", command):
                fail(f"{skill}:{line_no}: direct HTTP example bypasses headed CDP")
            if command.startswith("cdp workflow "):
                fail(
                    f"{skill}:{line_no}: CDP workflow example is not explicitly headed"
                )


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+(?:[-']\w+)?\b", text))


def validate_theme_guide(theme_dir: Path) -> None:
    guide_dir = theme_dir / "guide"
    if not guide_dir.exists():
        fail(f"{theme_dir}: missing guide/ directory for ELI5 deep-dive chapters")
    index = guide_dir / "00-README.md"
    if not index.exists():
        fail(f"{theme_dir}: missing guide/00-README.md")
    chapters = sorted(path for path in guide_dir.glob("*.md") if path.is_file())
    if len(chapters) < MIN_GUIDE_CHAPTERS:
        fail(
            f"{theme_dir}: expected at least {MIN_GUIDE_CHAPTERS} guide chapters, found {len(chapters)}"
        )
    total_words = sum(word_count(path.read_text(encoding="utf-8")) for path in chapters)
    if total_words < MIN_GUIDE_WORDS:
        fail(
            f"{theme_dir}: guide is too thin ({total_words} words < {MIN_GUIDE_WORDS})"
        )
    guide_text = "\n".join(path.read_text(encoding="utf-8") for path in chapters)
    if "https://" not in guide_text:
        fail(f"{theme_dir}: guide must include inline external source links")


def load_json_object(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path}: invalid JSON: {exc}")
    if not isinstance(value, dict):
        fail(f"{path}: expected one JSON object")
    return value


def load_jsonl_objects(path: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"{path}:{line_no}: invalid JSONL record: {exc}")
        if not isinstance(record, dict):
            fail(f"{path}:{line_no}: expected a JSON object")
        records.append(record)
    if not records:
        fail(f"{path}: expected at least one JSONL record")
    return records


def _decimal_fixture_value(value: object, *, name: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (Decimal, int, float, str)):
        raise ValueError(f"{name} must be a finite decimal value")
    try:
        decimal_value = Decimal(str(value))
    except DecimalException as exc:
        raise ValueError(f"{name} must be a finite decimal value") from exc
    if not decimal_value.is_finite():
        raise ValueError(f"{name} must be a finite decimal value")
    return decimal_value


def evaluate_decimal_formula(
    formula: object, identifiers: Mapping[str, object]
) -> Decimal:
    """Evaluate a fixture formula without executing Python code."""

    if not isinstance(formula, str) or not formula.strip():
        raise ValueError("formula must be a non-empty string")
    if len(formula) > 1_000:
        raise ValueError("formula is too long")
    try:
        tree = ast.parse(formula, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"invalid formula syntax: {exc.msg}") from exc
    if sum(1 for _ in ast.walk(tree)) > 128:
        raise ValueError("formula has too many syntax nodes")

    def evaluate(node: ast.AST) -> Decimal:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Name):
            if node.id not in identifiers:
                raise ValueError(f"undefined identifier: {node.id}")
            return _decimal_fixture_value(identifiers[node.id], name=node.id)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(
                node.value, (int, float)
            ):
                raise ValueError(
                    f"unsupported syntax: {type(node).__name__}"
                )
            literal = ast.get_source_segment(formula, node)
            if literal is None:
                raise ValueError("invalid decimal literal")
            try:
                value = Decimal(literal.replace("_", ""))
            except DecimalException as exc:
                raise ValueError(f"invalid decimal literal: {literal}") from exc
            if not value.is_finite():
                raise ValueError(f"decimal literal must be finite: {literal}")
            return value
        if isinstance(node, ast.UnaryOp):
            operand = evaluate(node.operand)
            if isinstance(node.op, ast.UAdd):
                return operand
            if isinstance(node.op, ast.USub):
                return -operand
            raise ValueError(f"unsupported syntax: {type(node.op).__name__}")
        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)
            try:
                if isinstance(node.op, ast.Add):
                    return left + right
                if isinstance(node.op, ast.Sub):
                    return left - right
                if isinstance(node.op, ast.Mult):
                    return left * right
                if isinstance(node.op, ast.Div):
                    return left / right
            except (DecimalException, ZeroDivisionError) as exc:
                raise ValueError(f"invalid decimal arithmetic: {exc}") from exc
            raise ValueError(f"unsupported syntax: {type(node.op).__name__}")
        raise ValueError(f"unsupported syntax: {type(node).__name__}")

    result = evaluate(tree)
    if not result.is_finite():
        raise ValueError("formula result must be finite")
    return result


def validate_json_schema_contract(
    *,
    schema: dict[str, object],
    valid_instance: dict[str, object],
    invalid_cases: list[dict[str, object]],
    fixture: Path,
) -> None:
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        fail(f"{fixture}: invalid Draft 2020-12 decision schema: {exc.message}")

    validator = Draft202012Validator(schema)
    valid_errors = sorted(
        validator.iter_errors(valid_instance),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    if valid_errors:
        fail(
            f"{fixture}: valid decision does not satisfy its schema: "
            f"{valid_errors[0].message}"
        )

    if len(invalid_cases) < 4:
        fail(f"{fixture}: expected at least four negative schema cases")
    for record in invalid_cases:
        case_id = record.get("invalid_case_id")
        instance = record.get("instance")
        expected_keywords = record.get("expected_keywords")
        if (
            not isinstance(case_id, str)
            or not isinstance(instance, dict)
            or not isinstance(expected_keywords, list)
            or not expected_keywords
            or not all(isinstance(keyword, str) for keyword in expected_keywords)
        ):
            fail(f"{fixture}: malformed negative schema case: {case_id!r}")
        errors = sorted(
            validator.iter_errors(instance),
            key=lambda error: (list(error.absolute_path), error.message),
        )
        if not errors:
            fail(f"{fixture}: negative schema case unexpectedly validates: {case_id}")
        evidence = "\n".join(
            " ".join(
                (
                    str(error.validator),
                    error.message,
                    "/".join(str(part) for part in error.absolute_path),
                    "/".join(str(part) for part in error.absolute_schema_path),
                )
            )
            for error in errors
        ).lower()
        missing = [
            keyword for keyword in expected_keywords if keyword.lower() not in evidence
        ]
        if missing:
            fail(
                f"{fixture}: negative schema case {case_id} did not produce "
                f"expected evidence: {', '.join(missing)}"
            )


def validate_capstone_v2(theme_dir: Path) -> None:
    fixture = theme_dir / "guide" / "fixtures" / "capstone-v2"
    if not fixture.exists():
        return

    manifest_path = fixture / "manifest.json"
    manifest = load_json_object(manifest_path)
    if manifest.get("fixture_id") != "capstone-v2":
        fail(f"{manifest_path}: fixture_id must be capstone-v2")
    if manifest.get("deterministic") is not True:
        fail(f"{manifest_path}: deterministic must be true")

    referenced: list[str] = []
    for key in (
        "engine",
        "faults",
        "evaluation_cases",
        "gates",
        "pricing",
        "egress_policy",
        "expected_events",
        "golden_ledger",
        "decision_schema",
        "decision_valid_example",
        "decision_invalid_cases",
    ):
        value = manifest.get(key)
        if not isinstance(value, str):
            fail(f"{manifest_path}: {key} must name one file")
        referenced.append(value)
    workloads = manifest.get("workloads")
    if not isinstance(workloads, list) or not all(
        isinstance(item, str) for item in workloads
    ):
        fail(f"{manifest_path}: workloads must be a list of file names")
    referenced.extend(workloads)
    for rel in referenced:
        if not (fixture / rel).is_file():
            fail(f"{manifest_path}: referenced fixture file is missing: {rel}")

    engine = load_json_object(fixture / str(manifest["engine"]))
    clock = engine.get("clock")
    service = engine.get("service_model")
    capacity = engine.get("capacity")
    if not isinstance(clock, dict) or clock.get("tick_ms") != 100:
        fail(f"{fixture / str(manifest['engine'])}: expected a 100 ms virtual tick")
    if not isinstance(service, dict) or service.get("prefill_tokens_per_tick") != 1000:
        fail(f"{fixture / str(manifest['engine'])}: unexpected service model")
    if not isinstance(capacity, dict) or capacity.get("model_slots") != 3:
        fail(f"{fixture / str(manifest['engine'])}: expected three model slots")

    mixed = load_jsonl_objects(fixture / "workloads" / "mixed.jsonl")
    request_ids = [record.get("request_id") for record in mixed]
    expected_request_ids = [
        "r-01",
        "r-02",
        "r-03",
        "r-04-01",
        "r-04-02",
        "r-04-03",
        "r-04-04",
        "r-04-05",
        "r-04-06",
        "r-05",
        "r-06",
    ]
    if request_ids != expected_request_ids:
        fail(f"{fixture}: mixed workload IDs/order differ from capstone-v2")
    if any("repeat" in record for record in mixed):
        fail(f"{fixture}: mixed workload must expand repeated requests")
    load_jsonl_objects(fixture / "workloads" / "south-baseline.jsonl")
    load_jsonl_objects(fixture / str(manifest["faults"]))

    cases = load_jsonl_objects(fixture / str(manifest["evaluation_cases"]))
    case_ids = [record.get("case_id") for record in cases]
    expected_case_ids = [
        "e-01",
        "e-02",
        "e-03",
        "e-04",
        "e-05",
        "e-06",
        "e-07",
        "e-08",
        "e-09a",
        "e-09b",
        "e-10",
    ]
    if case_ids != expected_case_ids:
        fail(f"{fixture}: evaluation cases must retain all eleven canonical IDs")

    gates = load_json_object(fixture / str(manifest["gates"]))
    core = gates.get("core")
    live_stretch = gates.get("live_stretch")
    if not isinstance(core, dict) or "p95" in json.dumps(core).lower():
        fail(f"{fixture}: deterministic core must use exact values/maxima, not p95")
    if not isinstance(live_stretch, dict):
        fail(f"{fixture}: missing live_stretch gates")
    p95_policy = live_stretch.get("p95_policy")
    if (
        not isinstance(p95_policy, dict)
        or p95_policy.get("minimum_sample_size", 0) < 20
        or p95_policy.get("algorithm") != "nearest_rank"
    ):
        fail(f"{fixture}: live p95 needs n>=20 and nearest_rank")
    evaluation_gate = core.get("evaluation")
    if (
        not isinstance(evaluation_gate, dict)
        or evaluation_gate.get("required_case_ids") != expected_case_ids
    ):
        fail(f"{fixture}: gate case IDs do not reconcile with evaluation cases")

    schema = load_json_object(fixture / str(manifest["decision_schema"]))
    if "2020-12" not in str(schema.get("$schema")):
        fail(f"{fixture}: decision schema must declare Draft 2020-12")
    if schema.get("additionalProperties") is not False:
        fail(f"{fixture}: decision schema must reject undeclared properties")
    valid_decision = load_json_object(fixture / str(manifest["decision_valid_example"]))
    invalid_decisions = load_jsonl_objects(
        fixture / str(manifest["decision_invalid_cases"])
    )
    validate_json_schema_contract(
        schema=schema,
        valid_instance=valid_decision,
        invalid_cases=invalid_decisions,
        fixture=fixture,
    )

    pricing_path = fixture / str(manifest["pricing"])
    pricing = load_json_object(pricing_path)
    rates = pricing.get("rates")
    worked = pricing.get("worked_case")
    if not isinstance(rates, dict) or not isinstance(worked, dict):
        fail(f"{fixture}: pricing rates and worked_case are required")
    cost_gate = core.get("cost")
    if (
        not isinstance(cost_gate, dict)
        or cost_gate.get("case_id") != worked.get("case_id")
    ):
        fail(f"{fixture}: cost gate and worked price must name the same case")

    worked_identifiers = (
        "input_tokens",
        "output_tokens",
        "write_tool_attempts",
    )
    rate_identifiers = (
        "input_usd_per_million_tokens",
        "output_usd_per_million_tokens",
        "write_tool_attempt_usd",
    )
    missing_identifiers = [
        name
        for name in worked_identifiers
        if name not in worked
    ] + [
        name
        for name in rate_identifiers
        if name not in rates
    ]
    if missing_identifiers:
        fail(
            f"{pricing_path}: missing canonical cost identifiers: "
            f"{', '.join(missing_identifiers)}"
        )

    try:
        cost_identifiers = {
            name: _decimal_fixture_value(worked[name], name=name)
            for name in worked_identifiers
        }
        cost_identifiers.update(
            {
                name: _decimal_fixture_value(rates[name], name=name)
                for name in rate_identifiers
            }
        )
        amount = (
            cost_identifiers["input_tokens"]
            * cost_identifiers["input_usd_per_million_tokens"]
            / Decimal(1_000_000)
            + cost_identifiers["output_tokens"]
            * cost_identifiers["output_usd_per_million_tokens"]
            / Decimal(1_000_000)
            + cost_identifiers["write_tool_attempts"]
            * cost_identifiers["write_tool_attempt_usd"]
        ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_EVEN)
        formula_amounts = {
            "pricing formula": evaluate_decimal_formula(
                pricing.get("formula"), worked
            ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_EVEN),
            "worked calculation": evaluate_decimal_formula(
                worked.get("calculation"), {}
            ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_EVEN),
            "cost gate formula": evaluate_decimal_formula(
                cost_gate.get("formula"), cost_identifiers
            ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_EVEN),
        }
        expected_amounts = {
            "cost gate expected_usd": _decimal_fixture_value(
                cost_gate.get("expected_usd"), name="expected_usd"
            ),
            "worked expected_amount_usd": _decimal_fixture_value(
                worked.get("expected_amount_usd"), name="expected_amount_usd"
            ),
        }
    except ValueError as exc:
        fail(f"{fixture}: invalid cost contract: {exc}")

    fixture_amount = Decimal("0.0042")
    reconciled_amounts = {
        "canonical calculation": amount,
        **formula_amounts,
        **expected_amounts,
    }
    mismatched_amounts = [
        f"{name}={value}"
        for name, value in reconciled_amounts.items()
        if value != fixture_amount
    ]
    if mismatched_amounts:
        fail(
            f"{fixture}: cost contract must reconcile exactly to 0.0042: "
            f"{', '.join(mismatched_amounts)}"
        )

    egress = load_json_object(fixture / str(manifest["egress_policy"]))
    proof = egress.get("case_e03_expected_proof")
    if not isinstance(proof, dict) or any(
        proof.get(key) != 0
        for key in ("adapter_invocations", "sink_records", "sink_bytes")
    ):
        fail(f"{fixture}: e-03 must carry a zero-invocation/zero-byte egress proof")

    events = load_jsonl_objects(fixture / str(manifest["expected_events"]))
    if [event.get("sequence") for event in events] != list(range(1, len(events) + 1)):
        fail(f"{fixture}: expected event sequence must be contiguous")
    if not any(
        event.get("case_id") == "e-09a"
        and event.get("event") == "authorization_decision"
        and event.get("effects") == 0
        for event in events
    ):
        fail(f"{fixture}: e-09a stale-authority proof is missing")
    if not any(
        event.get("case_id") == "e-09b"
        and event.get("event") == "effect_reconciled"
        and event.get("adapter_effect_count") == 1
        for event in events
    ):
        fail(f"{fixture}: e-09b acknowledgement-loss reconciliation is missing")

    ledger = load_jsonl_objects(fixture / str(manifest["golden_ledger"]))
    e09b = next((row for row in ledger if row.get("case_id") == "e-09b"), None)
    try:
        ledger_amount = (
            _decimal_fixture_value(e09b.get("amount_usd"), name="amount_usd")
            if e09b is not None
            else None
        )
        ledger_formula_amount = (
            evaluate_decimal_formula(e09b.get("formula"), {}).quantize(
                Decimal("0.0001"), rounding=ROUND_HALF_EVEN
            )
            if e09b is not None
            else None
        )
    except ValueError as exc:
        fail(f"{fixture}: invalid e-09b golden-ledger cost: {exc}")
    if (
        e09b is None
        or ledger_amount != fixture_amount
        or ledger_amount != amount
        or ledger_formula_amount != fixture_amount
        or e09b.get("adapter_effect_count") != 1
    ):
        fail(f"{fixture}: e-09b golden ledger does not reconcile")


def validate_theme(theme_dir: Path) -> None:
    for name in REQUIRED_THEME_FILES:
        path = theme_dir / name
        if not path.exists():
            fail(f"{theme_dir}: missing {name}")
        if not path.read_text(encoding="utf-8").strip():
            fail(f"{path}: file is empty")

    validate_theme_guide(theme_dir)
    validate_capstone_v2(theme_dir)

    sources_json = theme_dir / "sources.json"
    if not sources_json.exists():
        fail(f"{theme_dir}: missing sources.json")
    data = json.loads(sources_json.read_text(encoding="utf-8"))
    if not isinstance(data, list) or len(data) < 10:
        fail(f"{sources_json}: expected at least 10 source records")
    records_use_author_metadata = any(
        isinstance(item, dict) and "author_or_organization" in item for item in data
    )
    seen: set[str] = set()
    for idx, item in enumerate(data, 1):
        if not isinstance(item, dict):
            fail(f"{sources_json}: item {idx} is not an object")
        url = item.get("url")
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            fail(f"{sources_json}: item {idx} has invalid url")
        netloc = urlparse(url).netloc
        if not netloc or "." not in netloc:
            fail(f"{sources_json}: item {idx} url has invalid host: {url}")
        if url in seen:
            fail(f"{sources_json}: duplicate url: {url}")
        seen.add(url)
        if not item.get("quality"):
            fail(f"{sources_json}: item {idx} missing quality label")
        if records_use_author_metadata and not item.get("author_or_organization"):
            fail(
                f"{sources_json}: item {idx} missing author_or_organization "
                "while the catalog uses author metadata"
            )


def validate_markdown_hygiene() -> None:
    for path in ROOT.rglob("*.md"):
        if ".venv" in path.parts or ".git" in path.parts or "tmp" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                fail(f"{path}:{line_no}: trailing whitespace")
        # Catch common broken local links early. External links are source data and are not fetched.
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = (path.parent / target.split("#", 1)[0]).resolve()
            if target.split("#", 1)[0] and not target_path.exists():
                fail(f"{path}: broken local link: {target}")


def main() -> None:
    validate_agents()
    validate_skill_browser_examples()
    if not RESEARCH_ROOT.exists():
        fail("research/ directory is missing")
    themes = [p for p in sorted(RESEARCH_ROOT.iterdir()) if p.is_dir()]
    if not themes:
        fail("research/ contains no theme directories")
    for theme in themes:
        validate_theme(theme)
    validate_markdown_hygiene()
    print(f"Validated {len(themes)} research theme(s).")


if __name__ == "__main__":
    main()
