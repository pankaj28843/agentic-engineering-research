from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_research.py"
CAPSTONE = (
    ROOT
    / "research"
    / "09-production-llm-systems-engineering"
    / "guide"
    / "fixtures"
    / "capstone-v2"
)
SPEC = importlib.util.spec_from_file_location("validate_research", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["decision"],
    "properties": {"decision": {"enum": ["accept", "reject"]}},
}


class ValidateJSONSchemaContractTests(unittest.TestCase):
    def test_accepts_valid_positive_and_invalid_negative(self) -> None:
        MODULE.validate_json_schema_contract(
            schema=SCHEMA,
            valid_instance={"decision": "accept"},
            invalid_cases=[
                {
                    "invalid_case_id": f"bad-{index}",
                    "instance": {"decision": "unknown"},
                    "expected_keywords": ["enum", "decision"],
                }
                for index in range(4)
            ],
            fixture=Path("fixture"),
        )

    def test_rejects_malformed_positive(self) -> None:
        with self.assertRaises(SystemExit):
            MODULE.validate_json_schema_contract(
                schema=SCHEMA,
                valid_instance={"decision": "unknown"},
                invalid_cases=[],
                fixture=Path("fixture"),
            )

    def test_rejects_negative_case_that_validates(self) -> None:
        with self.assertRaises(SystemExit):
            MODULE.validate_json_schema_contract(
                schema=SCHEMA,
                valid_instance={"decision": "accept"},
                invalid_cases=[
                    {
                        "invalid_case_id": f"not-negative-{index}",
                        "instance": {"decision": "accept"},
                        "expected_keywords": ["enum"],
                    }
                    for index in range(4)
                ],
                fixture=Path("fixture"),
            )


class ActualCapstoneDecisionSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = json.loads(
            (CAPSTONE / "schemas" / "decision.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.valid_instance = json.loads(
            (CAPSTONE / "schemas" / "decision.valid.json").read_text(
                encoding="utf-8"
            )
        )
        self.validator = Draft202012Validator(self.schema)

    def test_real_valid_example_is_clean(self) -> None:
        errors = sorted(
            self.validator.iter_errors(self.valid_instance),
            key=lambda error: (list(error.absolute_path), error.message),
        )

        self.assertEqual([], [error.message for error in errors])

    def test_real_schema_rejects_empty_citations_at_the_exact_path(self) -> None:
        citations_schema = self.schema["properties"]["citations"]
        self.assertEqual(1, citations_schema.get("minItems"))

        empty_citations = dict(self.valid_instance)
        empty_citations["citations"] = []
        errors = [
            error
            for error in self.validator.iter_errors(empty_citations)
            if error.validator == "minItems"
        ]

        self.assertEqual([["citations"]], [list(error.absolute_path) for error in errors])
        self.assertEqual(
            [["properties", "citations", "minItems"]],
            [list(error.absolute_schema_path) for error in errors],
        )

    def test_real_negative_fixture_covers_empty_citations(self) -> None:
        records = [
            json.loads(line)
            for line in (
                CAPSTONE / "schemas" / "decision.invalid-cases.jsonl"
            ).read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        empty_case = next(
            (
                record
                for record in records
                if record["invalid_case_id"] == "schema-invalid-empty-citations"
            ),
            None,
        )

        self.assertIsNotNone(empty_case)
        assert empty_case is not None
        errors = [
            error
            for error in self.validator.iter_errors(empty_case["instance"])
            if error.validator == "minItems"
        ]
        self.assertEqual([["citations"]], [list(error.absolute_path) for error in errors])


class DecimalFormulaEvaluationTests(unittest.TestCase):
    def test_actual_cost_contract_reconciles_to_exact_fixture_amount(self) -> None:
        gates = json.loads((CAPSTONE / "gates.json").read_text(encoding="utf-8"))
        pricing = json.loads((CAPSTONE / "pricing.json").read_text(encoding="utf-8"))
        worked = pricing["worked_case"]
        identifiers = {
            "input_tokens": worked["input_tokens"],
            "output_tokens": worked["output_tokens"],
            "write_tool_attempts": worked["write_tool_attempts"],
            **pricing["rates"],
        }

        computed = MODULE.evaluate_decimal_formula(
            gates["core"]["cost"]["formula"], identifiers
        ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_EVEN)
        ledger_rows = [
            json.loads(line)
            for line in (CAPSTONE / "golden-ledger.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ]
        ledger_e09b = next(
            row for row in ledger_rows if row.get("case_id") == "e-09b"
        )

        self.assertEqual(Decimal("0.0042"), computed)
        self.assertEqual(
            {
                Decimal(str(gates["core"]["cost"]["expected_usd"])),
                Decimal(str(worked["expected_amount_usd"])),
                Decimal(str(ledger_e09b["amount_usd"])),
            },
            {Decimal("0.0042")},
        )

    def test_rejects_undefined_formula_identifier(self) -> None:
        with self.assertRaisesRegex(ValueError, "undefined identifier: missing_rate"):
            MODULE.evaluate_decimal_formula(
                "input_tokens * missing_rate",
                {"input_tokens": 550},
            )

    def test_rejects_unsafe_formula_syntax(self) -> None:
        unsafe_formulas = (
            "__import__('os').system('id')",
            "input_tokens ** 2",
            "rates['input']",
        )

        for formula in unsafe_formulas:
            with self.subTest(formula=formula):
                with self.assertRaisesRegex(ValueError, "unsupported syntax"):
                    MODULE.evaluate_decimal_formula(
                        formula,
                        {"input_tokens": 550},
                    )


if __name__ == "__main__":
    unittest.main()
