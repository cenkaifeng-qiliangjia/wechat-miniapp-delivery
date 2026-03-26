#!/usr/bin/env python3
"""Install one or more canonical skills from a local clone into agent skill directories."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "catalog.json"


def codex_root() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return codex_home / "skills"


def claude_root() -> Path:
    return Path.home() / ".claude" / "skills"


def load_catalog() -> list[dict[str, object]]:
    data = json.loads(CATALOG_PATH.read_text())
    return data["skills"]


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


def install(src: Path, dest_root: Path, skill_name: str, force: bool) -> Path:
    dest_root.mkdir(parents=True, exist_ok=True)
    dest_dir = dest_root / skill_name
    if dest_dir.exists():
        if not force:
            raise FileExistsError(f"Destination already exists: {dest_dir}")
        shutil.rmtree(dest_dir)
    shutil.copytree(src, dest_dir)
    return dest_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install the local skill clone.")
    parser.add_argument(
        "--target",
        choices=["codex", "claude", "openclaw", "all"],
        default="all",
        help="Install target. 'all' installs Codex and Claude defaults.",
    )
    parser.add_argument(
        "--dest",
        help="Destination skills root for a single target. Required for openclaw.",
    )
    parser.add_argument(
        "--openclaw-dest",
        help="Optional OpenClaw skills root used together with --target all.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing destination skill directory.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        help="Install only the named skill. Repeat to install multiple skills. Defaults to the whole suite.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        selected_skills = select_skills(args.skill)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    targets: list[tuple[str, Path]] = []
    if args.target == "codex":
        targets.append(("codex", Path(args.dest) if args.dest else codex_root()))
    elif args.target == "claude":
        targets.append(("claude", Path(args.dest) if args.dest else claude_root()))
    elif args.target == "openclaw":
        if not args.dest:
            print(
                "For openclaw installs, pass --dest pointing to a workspace skills directory.",
                file=sys.stderr,
            )
            return 1
        targets.append(("openclaw", Path(args.dest)))
    else:
        targets.extend([("codex", codex_root()), ("claude", claude_root())])
        if args.openclaw_dest:
            targets.append(("openclaw", Path(args.openclaw_dest)))

    try:
        for skill in selected_skills:
            skill_name = str(skill["name"])
            source_dir = REPO_ROOT / str(skill["source"])
            if not (source_dir / "SKILL.md").is_file():
                print(f"Missing canonical skill at {source_dir}", file=sys.stderr)
                return 1
            for label, dest_root in targets:
                dest_dir = install(source_dir, dest_root, skill_name, force=args.force)
                print(f"Installed {skill_name} for {label} at {dest_dir}")
    except (FileExistsError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
