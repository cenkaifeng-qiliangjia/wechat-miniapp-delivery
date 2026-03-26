#!/usr/bin/env python3
"""Install the canonical skill from a local clone into agent skill directories."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys

SKILL_NAME = "wechat-miniapp-delivery"
REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = REPO_ROOT / "skills" / SKILL_NAME


def codex_root() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return codex_home / "skills"


def claude_root() -> Path:
    return Path.home() / ".claude" / "skills"


def install(src: Path, dest_root: Path, force: bool) -> Path:
    dest_root.mkdir(parents=True, exist_ok=True)
    dest_dir = dest_root / SKILL_NAME
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not (SOURCE_DIR / "SKILL.md").is_file():
        print(f"Missing canonical skill at {SOURCE_DIR}", file=sys.stderr)
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
        for label, dest_root in targets:
            dest_dir = install(SOURCE_DIR, dest_root, force=args.force)
            print(f"Installed {SKILL_NAME} for {label} at {dest_dir}")
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
