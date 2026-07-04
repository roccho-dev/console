#!/usr/bin/env python3
"""Verify console stays a projection surface, not an authority source."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CONTRACT = ROOT / "docs" / "contracts" / "console-visualization-input.v0.jsonl"
RECEIPT = ROOT / "docs" / "receipts" / "console-readme-projection.receipt.jsonl"

REQUIRED_README_SNIPPETS = [
    "console deploys visualization of externally authoritative state; it does not define that state.",
    "not in the selected real package closure yet",
    "projection only",
    "roccho-dev/adrs",
    "roccho-dev/governance",
    "roccho-dev/ui",
    "roccho-dev/deploy",
    "GitHub Projects",
    "private ADR content",
    "private issue content",
    "secrets",
    "credentials",
    "roccho-dev/adrs#187",
    "roccho-dev/governance#134",
]

FORBIDDEN_AUTHORITY_CLAIMS = [
    "console is the adr authority",
    "console is the work-ledger authority",
    "console is the ui component authority",
    "console is the deployment authority",
    "console is final governance evidence",
    "github projects are required for correctness",
]


def fail(message: str) -> None:
    raise SystemExit(f"console boundary check failed: {message}")


def read_required(path: Path) -> str:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    text = read_required(path)
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"{path.relative_to(ROOT)}:{line_number} is not valid JSON: {exc}")
        if not isinstance(row, dict):
            fail(f"{path.relative_to(ROOT)}:{line_number} must be a JSON object")
        rows.append(row)
    if not rows:
        fail(f"{path.relative_to(ROOT)} has no JSONL rows")
    return rows


def check_readme() -> None:
    readme = read_required(README)
    readme_lower = readme.lower()
    for snippet in REQUIRED_README_SNIPPETS:
        if snippet.lower() not in readme_lower:
            fail(f"README.md missing required boundary snippet: {snippet}")
    for forbidden in FORBIDDEN_AUTHORITY_CLAIMS:
        if forbidden in readme_lower:
            fail(f"README.md contains forbidden authority claim: {forbidden}")


def check_projection_rows(rows: list[dict[str, Any]], path: Path) -> None:
    for index, row in enumerate(rows, start=1):
        if row.get("projection_only") is not True:
            fail(f"{path.relative_to(ROOT)} row {index} must set projection_only=true")
        if row.get("selected_real_package_closure") is True:
            fail(f"{path.relative_to(ROOT)} row {index} must not claim selected real package closure")
        if row.get("public_safe") is False:
            fail(f"{path.relative_to(ROOT)} row {index} must not be explicitly public_unsafe")


def check_receipt(rows: list[dict[str, Any]]) -> None:
    if len(rows) != 1:
        fail("receipt must contain exactly one JSONL row")
    receipt = rows[0]
    expected_claim = "console deploys visualization of externally authoritative state; it does not define that state."
    required_pairs: dict[str, Any] = {
        "record_kind": "non_blocking_projection_receipt",
        "source_repo": "roccho-dev/console",
        "source_issue": 1,
        "adrs_contract_issue": "roccho-dev/adrs#187",
        "governance_observer_issue": "roccho-dev/governance#134",
        "claim": expected_claim,
        "projection_only": True,
        "blocking": False,
        "selected_real_package_closure": False,
        "public_safe": True,
        "sanitized": True,
    }
    for key, expected_value in required_pairs.items():
        if receipt.get(key) != expected_value:
            fail(f"receipt {key} must be {expected_value!r}")
    must_not_claim = set(receipt.get("must_not_claim", []))
    required_forbidden = {
        "adr_authority",
        "work_ledger_authority",
        "ui_component_authority",
        "deployment_authority",
        "closure_certificate_authority",
        "required_github_projects_authority",
        "final_governance_evidence",
    }
    missing = sorted(required_forbidden - must_not_claim)
    if missing:
        fail(f"receipt missing must_not_claim entries: {missing}")


def main() -> None:
    check_readme()
    contract_rows = load_jsonl(CONTRACT)
    receipt_rows = load_jsonl(RECEIPT)
    check_projection_rows(contract_rows, CONTRACT)
    check_projection_rows(receipt_rows, RECEIPT)
    check_receipt(receipt_rows)
    print("console boundary check passed")


if __name__ == "__main__":
    main()
