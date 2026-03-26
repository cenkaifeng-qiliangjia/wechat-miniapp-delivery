#!/usr/bin/env python3
"""Sync the canonical skill into Codex and Claude repo-local mirrors."""

from __future__ import annotations

from pathlib import Path
import shutil
import sys

SKILL_NAME = "wechat-miniapp-delivery"
REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = REPO_ROOT / "skills" / SKILL_NAME
TARGET_DIRS = [
    REPO_ROOT / ".codex" / "skills" / SKILL_NAME,
    REPO_ROOT / ".claude" / "skills" / SKILL_NAME,
]


def reset_copy(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest)


def main() -> int:
    skill_md = SOURCE_DIR / "SKILL.md"
    if not skill_md.is_file():
        print(f"Missing canonical SKILL.md: {skill_md}", file=sys.stderr)
        return 1

    for target in TARGET_DIRS:
        reset_copy(SOURCE_DIR, target)
        print(f"Synced {SOURCE_DIR} -> {target}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
