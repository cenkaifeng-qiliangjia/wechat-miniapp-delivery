#!/usr/bin/env python3
"""Install the skill from the public GitHub repo without cloning it first."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys
import tempfile
import urllib.request
import zipfile

SKILL_NAME = "wechat-miniapp-delivery"
DEFAULT_REPO = "cenkaifeng-qiliangjia/wechat-miniapp-delivery"
DEFAULT_REF = "main"
SKILL_PATH = Path("skills") / SKILL_NAME


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


def install(src: Path, dest_root: Path, force: bool) -> Path:
    dest_root.mkdir(parents=True, exist_ok=True)
    dest_dir = dest_root / SKILL_NAME
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
        src = repo_root / SKILL_PATH
        if not (src / "SKILL.md").is_file():
            print(f"Missing skill path in downloaded repo: {src}", file=sys.stderr)
            return 1
        try:
            for label, dest_root in resolve_targets(args):
                dest_dir = install(src, dest_root, force=args.force)
                print(f"Installed {SKILL_NAME} for {label} at {dest_dir}")
        except (FileExistsError, RuntimeError) as exc:
            print(str(exc), file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
