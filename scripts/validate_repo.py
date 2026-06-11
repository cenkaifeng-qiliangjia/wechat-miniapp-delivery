#!/usr/bin/env python3
"""Validate the skill suite, repository identity, and cross-file contracts."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "catalog.json"
IDENTITY_PATH = REPO_ROOT / "repository.json"

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


def validate_identity(validation: Validation) -> dict[str, object]:
    identity = load_json(IDENTITY_PATH, validation)
    if not isinstance(identity, dict):
        validation.errors.append("repository.json: expected an object")
        return {}

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
    else:
        validation.require(
            isinstance(upstream, str) and upstream != repository,
            "repository.json: fork must name a different upstream repository",
        )

    if isinstance(repository, str):
        installer = (REPO_ROOT / "scripts/install_from_github.py").read_text()
        validation.require(
            f'FALLBACK_REPO = "{repository}"' in installer,
            "scripts/install_from_github.py: FALLBACK_REPO must match repository.json",
        )

        referenced_repositories: set[str] = set()
        for relative in ("README.md", "catalog.json"):
            text = (REPO_ROOT / relative).read_text()
            referenced_repositories.update(
                re.findall(
                    r"(?:github\.com|raw\.githubusercontent\.com)/"
                    r"([A-Za-z0-9_.-]+/wechat-miniapp-delivery)",
                    text,
                )
            )
            referenced_repositories.update(
                re.findall(r"--repo ([A-Za-z0-9_.-]+/wechat-miniapp-delivery)", text)
            )
        validation.require(
            referenced_repositories == {repository},
            "README.md and catalog.json must point only to the repository declared in repository.json",
        )

    return identity


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


def validate_skill(item: dict[str, object], validation: Validation) -> None:
    name = item.get("name")
    source = item.get("source")
    validation.require(isinstance(name, str), "catalog.json: skill name must be a string")
    validation.require(isinstance(source, str), f"catalog.json: {name} source must be a string")
    if not isinstance(name, str) or not isinstance(source, str):
        return

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
    if not skill_md.is_file():
        return

    frontmatter = parse_frontmatter(skill_md, validation)
    validation.require(frontmatter.get("name") == name, f"{source}/SKILL.md: name mismatch")
    validation.require(
        bool(frontmatter.get("description")),
        f"{source}/SKILL.md: description is required",
    )
    validation.require(
        len(skill_md.read_text().splitlines()) < 500,
        f"{source}/SKILL.md: keep the main skill under 500 lines",
    )
    validation.require(
        not any(skill_root.rglob("README.md")),
        f"{source}: README.md does not belong inside a skill folder",
    )

    if agent_yaml.is_file():
        validation.require(
            f"${name}" in agent_yaml.read_text(),
            f"{source}/agents/openai.yaml: default prompt must mention ${name}",
        )

    validate_markdown_links(skill_root, validation)
    validate_json_blocks(skill_root, validation)


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
            compile(path.read_text(), str(path), "exec")
        except SyntaxError as exc:
            validation.errors.append(f"{path.relative_to(REPO_ROOT)}: {exc}")


def main() -> int:
    validation = Validation()
    validate_identity(validation)
    validate_catalog(validation)
    validate_visual_contracts(validation)
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
