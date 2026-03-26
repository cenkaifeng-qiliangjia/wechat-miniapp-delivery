#!/usr/bin/env python3
"""Install one or more skills from the public GitHub repo without cloning it first."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import urllib.request
import zipfile

DEFAULT_REPO = "cenkaifeng-qiliangjia/wechat-miniapp-delivery"
DEFAULT_REF = "main"


def codex_root() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return codex_home / "skills"


def claude_root() -> Path:
    return Path.home() / ".claude" / "skills"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install the skill from GitHub.")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="owner/repo")
    parser.add_argument("--ref", default=DEFAULT_REF, help="Git ref to download")
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


def download_repo(repo: str, ref: str, tmp_dir: Path) -> Path:
    owner, repo_name = repo.split("/", 1)
    zip_url = f"https://codeload.github.com/{owner}/{repo_name}/zip/{ref}"
    zip_path = tmp_dir / "repo.zip"
    with urllib.request.urlopen(zip_url) as response, zip_path.open("wb") as file_handle:
        file_handle.write(response.read())
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(tmp_dir)
        top_levels = {Path(name).parts[0] for name in archive.namelist() if name}
    if len(top_levels) != 1:
        raise RuntimeError("Unexpected GitHub archive layout.")
    return tmp_dir / next(iter(top_levels))


def load_catalog(repo_root: Path) -> list[dict[str, object]]:
    data = json.loads((repo_root / "catalog.json").read_text())
    return data["skills"]


def select_skills(repo_root: Path, requested: list[str] | None) -> list[dict[str, object]]:
    skills = load_catalog(repo_root)
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


def resolve_targets(args: argparse.Namespace) -> list[tuple[str, Path]]:
    if args.target == "codex":
        return [("codex", Path(args.dest) if args.dest else codex_root())]
    if args.target == "claude":
        return [("claude", Path(args.dest) if args.dest else claude_root())]
    if args.target == "openclaw":
        if not args.dest:
            raise RuntimeError(
                "For openclaw installs, pass --dest pointing to a workspace skills directory."
            )
        return [("openclaw", Path(args.dest))]

    targets = [("codex", codex_root()), ("claude", claude_root())]
    if args.openclaw_dest:
        targets.append(("openclaw", Path(args.openclaw_dest)))
    return targets


def main() -> int:
    args = parse_args()
    with tempfile.TemporaryDirectory(prefix="miniapp-skill-install-") as tmp:
        repo_root = download_repo(args.repo, args.ref, Path(tmp))
        try:
            selected_skills = select_skills(repo_root, args.skill)
            for skill in selected_skills:
                skill_name = str(skill["name"])
                src = repo_root / str(skill["source"])
                if not (src / "SKILL.md").is_file():
                    print(f"Missing skill path in downloaded repo: {src}", file=sys.stderr)
                    return 1
                for label, dest_root in resolve_targets(args):
                    dest_dir = install(src, dest_root, skill_name, force=args.force)
                    print(f"Installed {skill_name} for {label} at {dest_dir}")
        except (FileExistsError, RuntimeError) as exc:
            print(str(exc), file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
