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


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    data = load_json(CASES_PATH)
    catalog = load_json(REPO_ROOT / "catalog.json")
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        errors.append("evals/cases.json: cases must be a list")
        cases: list[object] = []
    else:
        cases = data["cases"]

    known_skills = {
        item["name"]
        for item in catalog.get("skills", [])
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    identifiers: set[str] = set()
    for raw_case in cases:
        if not isinstance(raw_case, dict):
            errors.append("eval case must be an object")
            continue
        case_id = raw_case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append("eval case id must be a non-empty string")
            continue
        if case_id in identifiers:
            errors.append(f"{case_id}: duplicate id")
        identifiers.add(case_id)

        prompt = raw_case.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"{case_id}: prompt must be a non-empty string")

        expected_skills = raw_case.get("expected_skills")
        if not isinstance(expected_skills, list) or not all(
            isinstance(value, str) for value in expected_skills
        ):
            errors.append(f"{case_id}: expected_skills must be a string list")
            expected_skills = []
        unknown_skills = set(expected_skills) - known_skills
        if unknown_skills:
            errors.append(f"{case_id}: unknown skills {sorted(unknown_skills)}")

        profile = raw_case.get("expected_profile")
        if "wechat-miniapp-delivery" in expected_skills:
            if profile not in SUPPORTED_PROFILES:
                errors.append(f"{case_id}: invalid delivery profile {profile!r}")
        elif profile is not None:
            errors.append(f"{case_id}: profile requires wechat-miniapp-delivery")

        required = raw_case.get("required_concepts")
        forbidden = raw_case.get("forbidden_concepts")
        if not isinstance(required, list) or not all(isinstance(value, str) for value in required):
            errors.append(f"{case_id}: required_concepts must be a string list")
            required = []
        if not isinstance(forbidden, list) or not all(
            isinstance(value, str) for value in forbidden
        ):
            errors.append(f"{case_id}: forbidden_concepts must be a string list")
            forbidden = []

        for concept in required:
            check_marker(case_id, concept, REQUIRED_CONCEPTS, errors)
        for concept in forbidden:
            check_marker(case_id, concept, FORBIDDEN_CONCEPT_GUARDS, errors)

    result = {
        "ok": not errors,
        "cases": len(cases),
        "errors": errors,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        print("Skill behavior evals failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print(f"Skill behavior evals passed: {len(cases)} cases.")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
