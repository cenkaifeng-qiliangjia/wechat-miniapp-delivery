#!/usr/bin/env python3
"""Validate declarative skill behavior contracts without model credentials."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = REPO_ROOT / "evals/cases.json"
SUPPORTED_PROFILES = {"quick", "standard", "release-critical"}

REQUIRED_CONCEPTS = {
    "profile-selection": (
        "skills/wechat-miniapp-delivery/SKILL.md",
        "Select A Delivery Profile",
    ),
    "focused-validation": (
        "skills/wechat-miniapp-delivery/SKILL.md",
        "focused static, unit, or runtime validation",
    ),
    "standard-coordination": (
        "skills/wechat-miniapp-delivery/SKILL.md",
        "scoped plan and acceptance dimensions",
    ),
    "release-gates": (
        "skills/wechat-miniapp-delivery/SKILL.md",
        "full plan, environment doctor, preflight, risk register, and ownership",
    ),
    "release-evidence": (
        "skills/wechat-miniapp-delivery/SKILL.md",
        "Never claim preview, upload, deploy, or publish success without evidence",
    ),
    "downgrade-blocker": (
        "skills/wechat-miniapp-delivery/SKILL.md",
        "explicit blocker list",
    ),
    "api-contract-testing": (
        "skills/wechat-miniapp-delivery/SKILL.md",
        "API Contract Test",
    ),
    "shared-button-reset": (
        "skills/wechat-miniapp-design/SKILL.md",
        "Reset native button defaults in one shared class",
    ),
    "vertical-centering": (
        "skills/wechat-miniapp-design/SKILL.md",
        "display: flex",
    ),
    "layout-stability": (
        "skills/wechat-miniapp-design/SKILL.md",
        "Reserve layout space",
    ),
    "native-layering": (
        "skills/wechat-miniapp-design/SKILL.md",
        "hide or unmount any native surface",
    ),
    "rendered-evidence": (
        "skills/wechat-miniapp-design/SKILL.md",
        "Static CSS review alone is not acceptance evidence",
    ),
    "existing-design-system": (
        "skills/wechat-miniapp-design/SKILL.md",
        "Reuse The Existing Design System First",
    ),
    "configuration-aware-units": (
        "skills/wechat-miniapp-design/SKILL.md",
        "Do not assume `px` converts to `rpx`",
    ),
    "progressive-context-loading": (
        "skills/wechat-miniapp-delivery/SKILL.md",
        "Use progressive context loading",
    ),
}

FORBIDDEN_CONCEPT_GUARDS = {
    "full-role-ceremony": (
        "skills/wechat-miniapp-delivery/SKILL.md",
        "Do not create a full PM task graph",
    ),
    "unverified-release-claim": (
        "skills/wechat-miniapp-delivery/SKILL.md",
        "Never claim preview, upload, deploy, or publish success without evidence",
    ),
    "force-token-migration": (
        "skills/wechat-miniapp-design/SKILL.md",
        "Do not force a token migration",
    ),
}

REFERENCE_PATHS = {
    "runtime-ui-quality-gates": (
        "wechat-miniapp-design",
        "skills/wechat-miniapp-design/references/runtime-ui-quality-gates.md",
    ),
    "workflow-and-handoffs": (
        "wechat-miniapp-delivery",
        "skills/wechat-miniapp-delivery/references/workflow-and-handoffs.md",
    ),
    "tooling-and-risk-checklists": (
        "wechat-miniapp-delivery",
        "skills/wechat-miniapp-delivery/references/tooling-and-risk-checklists.md",
    ),
    "json-contracts": (
        "wechat-miniapp-delivery",
        "skills/wechat-miniapp-delivery/references/json-contracts.md",
    ),
    "developer-test-obligations": (
        "wechat-miniapp-delivery",
        "skills/wechat-miniapp-delivery/references/developer-test-obligations.md",
    ),
    "design-system-bootstrap": (
        "wechat-miniapp-design",
        "skills/wechat-miniapp-design/references/design-system-bootstrap.md",
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run deterministic skill behavior evals.")
    parser.add_argument("--json", action="store_true", help="Print a JSON result.")
    return parser.parse_args()


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{path}: {exc}") from exc


def check_marker(
    case_id: str,
    concept: str,
    registry: dict[str, tuple[str, str]],
    errors: list[str],
) -> None:
    contract = registry.get(concept)
    if contract is None:
        errors.append(f"{case_id}: unknown concept {concept}")
        return
    relative, marker = contract
    path = REPO_ROOT / relative
    if not path.is_file() or marker not in path.read_text():
        errors.append(f"{case_id}: concept {concept} is not enforced by {relative}")


def string_list(
    case_id: str,
    field: str,
    value: object,
    errors: list[str],
) -> list[str]:
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    errors.append(f"{case_id}: {field} must be a string list")
    return []


def validate_references(
    case_id: str,
    references: list[str],
    expected_skills: list[str],
    errors: list[str],
    require_skill: bool,
) -> None:
    for reference in references:
        contract = REFERENCE_PATHS.get(reference)
        if contract is None:
            errors.append(f"{case_id}: unknown reference {reference}")
            continue
        skill_name, relative = contract
        if require_skill and skill_name not in expected_skills:
            errors.append(f"{case_id}: reference {reference} requires {skill_name}")
        path = REPO_ROOT / relative
        if not path.is_file():
            errors.append(f"{case_id}: missing reference file {relative}")
        if require_skill:
            route = f"references/{path.name}"
            skill_entry = REPO_ROOT / "skills" / skill_name / "SKILL.md"
            if route not in skill_entry.read_text():
                errors.append(f"{case_id}: {skill_name} does not route to {route}")


def validate_case(
    raw_case: object,
    known_skills: set[str],
    identifiers: set[str],
    errors: list[str],
) -> None:
    if not isinstance(raw_case, dict):
        errors.append("eval case must be an object")
        return
    case_id = raw_case.get("id")
    if not isinstance(case_id, str) or not case_id:
        errors.append("eval case id must be a non-empty string")
        return
    if case_id in identifiers:
        errors.append(f"{case_id}: duplicate id")
    identifiers.add(case_id)

    if not isinstance(raw_case.get("prompt"), str) or not raw_case["prompt"].strip():
        errors.append(f"{case_id}: prompt must be a non-empty string")
    expected_skills = string_list(
        case_id, "expected_skills", raw_case.get("expected_skills"), errors
    )
    unknown_skills = set(expected_skills) - known_skills
    if unknown_skills:
        errors.append(f"{case_id}: unknown skills {sorted(unknown_skills)}")
    validate_profile(case_id, raw_case.get("expected_profile"), expected_skills, errors)
    validate_case_contracts(case_id, raw_case, expected_skills, errors)


def validate_profile(
    case_id: str,
    profile: object,
    expected_skills: list[str],
    errors: list[str],
) -> None:
    if "wechat-miniapp-delivery" in expected_skills:
        if profile not in SUPPORTED_PROFILES:
            errors.append(f"{case_id}: invalid delivery profile {profile!r}")
    elif profile is not None:
        errors.append(f"{case_id}: profile requires wechat-miniapp-delivery")


def validate_case_contracts(
    case_id: str,
    raw_case: dict[str, object],
    expected_skills: list[str],
    errors: list[str],
) -> None:
    required = string_list(
        case_id, "required_concepts", raw_case.get("required_concepts"), errors
    )
    forbidden = string_list(
        case_id, "forbidden_concepts", raw_case.get("forbidden_concepts"), errors
    )
    required_refs = string_list(
        case_id, "required_references", raw_case.get("required_references", []), errors
    )
    forbidden_refs = string_list(
        case_id, "forbidden_references", raw_case.get("forbidden_references", []), errors
    )
    for concept in required:
        check_marker(case_id, concept, REQUIRED_CONCEPTS, errors)
    for concept in forbidden:
        check_marker(case_id, concept, FORBIDDEN_CONCEPT_GUARDS, errors)
    validate_references(case_id, required_refs, expected_skills, errors, require_skill=True)
    validate_references(case_id, forbidden_refs, expected_skills, errors, require_skill=False)
    overlap = set(required_refs) & set(forbidden_refs)
    if overlap:
        errors.append(f"{case_id}: references cannot be both required and forbidden {sorted(overlap)}")


def load_cases(errors: list[str]) -> list[object]:
    data = load_json(CASES_PATH)
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        errors.append("evals/cases.json: cases must be a list")
        return []
    return data["cases"]


def known_skill_names() -> set[str]:
    catalog = load_json(REPO_ROOT / "catalog.json")
    if not isinstance(catalog, dict):
        return set()
    skills = catalog.get("skills", [])
    if not isinstance(skills, list):
        return set()
    return {
        item["name"]
        for item in skills
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }


def run_evals() -> dict[str, object]:
    errors: list[str] = []
    cases = load_cases(errors)
    known_skills = {
        name for name in known_skill_names()
    }
    identifiers: set[str] = set()
    for raw_case in cases:
        validate_case(raw_case, known_skills, identifiers, errors)
    return {
        "ok": not errors,
        "cases": len(cases),
        "errors": errors,
    }


def report_result(result: dict[str, object], as_json: bool) -> None:
    errors = result["errors"]
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        print("Skill behavior evals failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print(f"Skill behavior evals passed: {result['cases']} cases.")


def main() -> int:
    args = parse_args()
    result = run_evals()
    report_result(result, args.json)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
