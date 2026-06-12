#!/usr/bin/env python3
"""Validate the skill suite, repository identity, and cross-file contracts."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "catalog.json"
IDENTITY_PATH = REPO_ROOT / "repository.json"
EVALS_PATH = REPO_ROOT / "evals/cases.json"
FUNCTION_LINE_LIMIT = 45
SKILL_BUDGETS = {
    "wechat-miniapp-delivery": {"words": 2200, "lines": 300},
    "wechat-miniapp-design": {"words": 1500, "lines": 230},
}

VISUAL_CONTRACTS = {
    "skills/wechat-miniapp-delivery/SKILL.md": [
        "Visual Runtime Acceptance QA",
        "visual state matrix",
        "rendered runtime evidence",
    ],
    "skills/wechat-miniapp-delivery/references/json-contracts.md": [
        '"visual_runtime_acceptance"',
        '"owner": "visual_qa"',
        '"visual_runtime_evidence"',
    ],
    "skills/wechat-miniapp-delivery/references/example-handoff-pack.md": [
        "Visual Runtime QA Handoff",
        '"visual_runtime_acceptance"',
        '"visual_runtime_evidence"',
    ],
    "skills/wechat-miniapp-delivery/references/workflow-and-handoffs.md": [
        "Visual runtime acceptance",
        "Visual runtime QA worker",
        "visual state matrix",
    ],
    "skills/wechat-miniapp-delivery/references/tooling-and-risk-checklists.md": [
        "Visual runtime acceptance gate",
        "runtime-ui-quality-gates.md",
        "rendered evidence",
    ],
    "skills/wechat-miniapp-delivery/references/multi-platform-miniapp-patterns.md": [
        "visual runtime acceptance",
    ],
    "skills/wechat-miniapp-delivery/references/qa-and-acceptance-matrix.md": [
        "Visual Runtime Acceptance",
        "visual state matrix",
    ],
}


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)


def load_json(path: Path, validation: Validation) -> object:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        validation.errors.append(f"{path.relative_to(REPO_ROOT)}: {exc}")
        return {}


def parse_frontmatter(path: Path, validation: Validation) -> dict[str, str]:
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    validation.require(match is not None, f"{path.relative_to(REPO_ROOT)}: missing frontmatter")
    if match is None:
        return {}

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip()
    return values


def validate_identity_shape(
    identity: dict[str, object],
    validation: Validation,
) -> str | None:
    repository = identity.get("repository")
    role = identity.get("role")
    upstream = identity.get("upstream")
    default_ref = identity.get("default_ref")
    validation.require(
        isinstance(repository, str)
        and re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository) is not None,
        "repository.json: repository must be owner/name",
    )
    validation.require(role in {"primary", "fork"}, "repository.json: role must be primary or fork")
    validation.require(default_ref == "main", "repository.json: default_ref must be main")
    if role == "primary":
        validation.require(upstream is None, "repository.json: primary repository must not set upstream")
    elif role == "fork":
        validation.require(
            isinstance(upstream, str) and upstream != repository,
            "repository.json: fork must name a different upstream repository",
        )
    return repository if isinstance(repository, str) else None


def referenced_repositories() -> set[str]:
    repositories: set[str] = set()
    for relative in ("README.md", "catalog.json"):
        text = (REPO_ROOT / relative).read_text()
        repositories.update(
            re.findall(
                r"(?:github\.com|raw\.githubusercontent\.com)/"
                r"([A-Za-z0-9_.-]+/wechat-miniapp-delivery)",
                text,
            )
        )
        repositories.update(
            re.findall(r"--repo ([A-Za-z0-9_.-]+/wechat-miniapp-delivery)", text)
        )
    return repositories


def validate_identity_references(repository: str, validation: Validation) -> None:
    installer = (REPO_ROOT / "scripts/install_from_github.py").read_text()
    validation.require(
        f'FALLBACK_REPO = "{repository}"' in installer,
        "scripts/install_from_github.py: FALLBACK_REPO must match repository.json",
    )
    validation.require(
        referenced_repositories() == {repository},
        "README.md and catalog.json must point only to repository.json repository",
    )


def validate_identity(validation: Validation) -> None:
    identity = load_json(IDENTITY_PATH, validation)
    if not isinstance(identity, dict):
        validation.errors.append("repository.json: expected an object")
        return
    repository = validate_identity_shape(identity, validation)
    if repository:
        validate_identity_references(repository, validation)


def validate_markdown_links(skill_root: Path, validation: Validation) -> None:
    for path in skill_root.rglob("*.md"):
        text = path.read_text()
        for target in re.findall(r"\[[^\]]+\]\(([^)#]+)", text):
            if "://" in target or target.startswith("/"):
                continue
            resolved = (path.parent / target).resolve()
            validation.require(
                resolved.is_file(),
                f"{path.relative_to(REPO_ROOT)}: missing link target {target}",
            )


def validate_json_blocks(skill_root: Path, validation: Validation) -> None:
    for path in skill_root.rglob("*.md"):
        for index, block in enumerate(
            re.findall(r"```json\n(.*?)\n```", path.read_text(), re.DOTALL),
            start=1,
        ):
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                validation.errors.append(
                    f"{path.relative_to(REPO_ROOT)}: invalid JSON block {index}: {exc}"
                )


def validate_skill_paths(
    name: str,
    source: str,
    validation: Validation,
) -> tuple[Path, Path] | None:
    skill_root = (REPO_ROOT / source).resolve()
    validation.require(
        skill_root.parent == (REPO_ROOT / "skills").resolve(),
        f"catalog.json: {name} source must be directly under skills/",
    )
    validation.require(skill_root.name == name, f"catalog.json: {name} source folder mismatch")
    skill_md = skill_root / "SKILL.md"
    agent_yaml = skill_root / "agents/openai.yaml"
    validation.require(skill_md.is_file(), f"{source}: missing SKILL.md")
    validation.require(agent_yaml.is_file(), f"{source}: missing agents/openai.yaml")
    return (skill_md, agent_yaml) if skill_md.is_file() else None


def validate_skill_metadata(
    name: str,
    source: str,
    skill_md: Path,
    agent_yaml: Path,
    validation: Validation,
) -> None:
    frontmatter = parse_frontmatter(skill_md, validation)
    validation.require(frontmatter.get("name") == name, f"{source}/SKILL.md: name mismatch")
    validation.require(bool(frontmatter.get("description")), f"{source}: description required")
    validation.require(
        not any(skill_md.parent.rglob("README.md")),
        f"{source}: README.md does not belong inside a skill folder",
    )
    if agent_yaml.is_file():
        validation.require(
            f"${name}" in agent_yaml.read_text(),
            f"{source}/agents/openai.yaml: default prompt must mention ${name}",
        )


def validate_skill_budget(name: str, skill_md: Path, validation: Validation) -> None:
    budget = SKILL_BUDGETS.get(name)
    if not budget:
        return
    text = skill_md.read_text()
    validation.require(
        len(text.split()) <= budget["words"],
        f"{name}/SKILL.md: exceeds {budget['words']} word context budget",
    )
    validation.require(
        len(text.splitlines()) <= budget["lines"],
        f"{name}/SKILL.md: exceeds {budget['lines']} line context budget",
    )


def validate_skill(item: dict[str, object], validation: Validation) -> None:
    name = item.get("name")
    source = item.get("source")
    validation.require(isinstance(name, str), "catalog.json: skill name must be a string")
    validation.require(isinstance(source, str), f"catalog.json: {name} source must be a string")
    if not isinstance(name, str) or not isinstance(source, str):
        return
    paths = validate_skill_paths(name, source, validation)
    if paths is None:
        return
    skill_md, agent_yaml = paths
    validate_skill_metadata(name, source, skill_md, agent_yaml, validation)
    validate_skill_budget(name, skill_md, validation)
    validate_markdown_links(skill_md.parent, validation)
    validate_json_blocks(skill_md.parent, validation)


def validate_catalog(validation: Validation) -> None:
    catalog = load_json(CATALOG_PATH, validation)
    if not isinstance(catalog, dict):
        validation.errors.append("catalog.json: expected an object")
        return
    skills = catalog.get("skills")
    validation.require(isinstance(skills, list) and bool(skills), "catalog.json: skills required")
    if not isinstance(skills, list):
        return

    names: set[str] = set()
    for item in skills:
        validation.require(isinstance(item, dict), "catalog.json: each skill must be an object")
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        validation.require(name not in names, f"catalog.json: duplicate skill {name}")
        if isinstance(name, str):
            names.add(name)
        validate_skill(item, validation)

    ignored = (REPO_ROOT / ".gitignore").read_text().splitlines()
    validation.require(".codex/" in ignored, ".gitignore: .codex/ must be ignored")
    validation.require(".claude/" in ignored, ".gitignore: .claude/ must be ignored")


def validate_visual_contracts(validation: Validation) -> None:
    for relative, markers in VISUAL_CONTRACTS.items():
        path = REPO_ROOT / relative
        validation.require(path.is_file(), f"{relative}: required visual contract file missing")
        if not path.is_file():
            continue
        text = path.read_text()
        for marker in markers:
            validation.require(marker in text, f"{relative}: missing visual contract marker {marker}")


def validate_python(validation: Validation) -> None:
    for path in (REPO_ROOT / "scripts").glob("*.py"):
        try:
            source = path.read_text()
            tree = ast.parse(source)
        except SyntaxError as exc:
            validation.errors.append(f"{path.relative_to(REPO_ROOT)}: {exc}")
            continue
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            lines = (node.end_lineno or node.lineno) - node.lineno + 1
            validation.require(
                lines <= FUNCTION_LINE_LIMIT,
                f"{path.relative_to(REPO_ROOT)}:{node.lineno} "
                f"{node.name} exceeds {FUNCTION_LINE_LIMIT} lines ({lines})",
            )


def validate_evals(validation: Validation) -> None:
    data = load_json(EVALS_PATH, validation)
    validation.require(
        isinstance(data, dict) and isinstance(data.get("cases"), list),
        "evals/cases.json: cases must be a list",
    )
    runner = REPO_ROOT / "scripts/run_skill_evals.py"
    validation.require(runner.is_file(), "scripts/run_skill_evals.py: required")


def validate_openspec(validation: Validation) -> None:
    root = REPO_ROOT / "openspec"
    validation.require(root.is_dir(), "openspec/: repository iteration specs are required")
    change_root = root / "changes"
    specs_root = root / "specs"
    validation.require(
        change_root.is_dir() or specs_root.is_dir(),
        "openspec/: expected changes or archived specs",
    )
    for change in change_root.iterdir() if change_root.is_dir() else []:
        if not change.is_dir() or change.name == "archive":
            continue
        for required in ("proposal.md", "design.md", "tasks.md"):
            validation.require(
                (change / required).is_file(),
                f"openspec/changes/{change.name}: missing {required}",
            )
        validation.require(
            any((change / "specs").glob("*/spec.md")),
            f"openspec/changes/{change.name}: capability specs required",
        )


def main() -> int:
    validation = Validation()
    validate_identity(validation)
    validate_catalog(validation)
    validate_visual_contracts(validation)
    validate_evals(validation)
    validate_openspec(validation)
    validate_python(validation)

    if validation.errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in validation.errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
