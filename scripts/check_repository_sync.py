#!/usr/bin/env python3
"""Compare a primary repository and fork while allowing repository identity differences."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {".git", ".codex", ".claude", "__pycache__"}
IDENTITY_AWARE_FILES = {
    Path("README.md"),
    Path("catalog.json"),
    Path("scripts/install_from_github.py"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare this repository with another checkout of its primary or fork."
    )
    parser.add_argument("--other", required=True, help="Path to the other repository checkout")
    return parser.parse_args()


def load_identity(root: Path) -> dict[str, object]:
    path = root / "repository.json"
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"{path}: expected an object")
    return value


def validate_relationship(left: dict[str, object], right: dict[str, object]) -> None:
    identities = {str(left.get("role")): left, str(right.get("role")): right}
    if set(identities) != {"primary", "fork"}:
        raise RuntimeError("Expected one primary repository and one fork repository.")

    primary = identities["primary"]
    fork = identities["fork"]
    if fork.get("upstream") != primary.get("repository"):
        raise RuntimeError("Fork upstream must match the primary repository.")
    if primary.get("upstream") is not None:
        raise RuntimeError("Primary repository must not declare an upstream.")
    if primary.get("default_ref") != fork.get("default_ref"):
        raise RuntimeError("Primary and fork default refs must match.")


def tracked_files(root: Path) -> set[Path]:
    files: set[Path] = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        if path.is_file() and path.suffix != ".pyc":
            files.add(relative)
    return files


def normalized_content(root: Path, relative: Path, identity: dict[str, object]) -> bytes:
    content = (root / relative).read_bytes()
    if relative not in IDENTITY_AWARE_FILES:
        return content

    repository = identity.get("repository")
    if not isinstance(repository, str):
        raise RuntimeError(f"{root / 'repository.json'}: repository must be a string")
    return content.replace(repository.encode(), b"<repository>")


def main() -> int:
    args = parse_args()
    other_root = Path(args.other).expanduser().resolve()
    if not other_root.is_dir():
        print(f"Other repository does not exist: {other_root}", file=sys.stderr)
        return 1

    try:
        left_identity = load_identity(REPO_ROOT)
        right_identity = load_identity(other_root)
        validate_relationship(left_identity, right_identity)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    left_files = tracked_files(REPO_ROOT) - {Path("repository.json")}
    right_files = tracked_files(other_root) - {Path("repository.json")}
    errors: list[str] = []
    for relative in sorted(left_files | right_files):
        if relative not in left_files:
            errors.append(f"missing from current repository: {relative}")
            continue
        if relative not in right_files:
            errors.append(f"missing from other repository: {relative}")
            continue
        if normalized_content(REPO_ROOT, relative, left_identity) != normalized_content(
            other_root, relative, right_identity
        ):
            errors.append(f"content differs: {relative}")

    if errors:
        print("Repository sync check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Repository sync check passed; only repository identity differs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
