#!/usr/bin/env python3
"""Generate optional repo-local mirrors for one or more canonical skills."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "catalog.json"


def load_catalog() -> list[dict[str, object]]:
    data = json.loads(CATALOG_PATH.read_text())
    return data["skills"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate repo-local skill mirrors.")
    parser.add_argument(
        "--skill",
        action="append",
        help="Generate mirrors only for the named skill. Repeat to select multiple skills. Defaults to the whole suite.",
    )
    return parser.parse_args()


def select_skills(requested: list[str] | None) -> list[dict[str, object]]:
    skills = load_catalog()
    if not requested:
        return skills

    lookup = {item["name"]: item for item in skills}
    selected: list[dict[str, object]] = []
    for name in requested:
        if name not in lookup:
            raise RuntimeError(f"Unknown skill: {name}")
        selected.append(lookup[name])
    return selected


def reset_copy(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest)


def main() -> int:
    args = parse_args()
    try:
        selected_skills = select_skills(args.skill)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    for skill in selected_skills:
        source_dir = REPO_ROOT / str(skill["source"])
        skill_md = source_dir / "SKILL.md"
        if not skill_md.is_file():
            print(f"Missing canonical SKILL.md: {skill_md}", file=sys.stderr)
            return 1
        for target in skill["generated_mirrors"]:
            target_path = REPO_ROOT / str(target)
            reset_copy(source_dir, target_path)
            print(f"Generated mirror {source_dir} -> {target_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
