#!/usr/bin/env python3
"""Install one or more skills from the public GitHub repo without cloning it first."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import uuid
import zipfile

FALLBACK_REPO = "cenkaifeng-qiliangjia/wechat-miniapp-delivery"
DEFAULT_REF = "main"
DEFAULT_TIMEOUT_SECONDS = 30.0
REPOSITORY_PATTERN = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
REF_PATTERN = re.compile(r"[A-Za-z0-9._/-]+")


def repo_from_checkout() -> str | None:
    script_path = Path(__file__)
    if not script_path.is_file():
        return None

    repo_root = script_path.resolve().parents[1]
    if not (repo_root / "catalog.json").is_file():
        return None

    remote_name = "origin"
    try:
        upstream = subprocess.run(
            [
                "git",
                "-C",
                str(repo_root),
                "rev-parse",
                "--abbrev-ref",
                "--symbolic-full-name",
                "@{upstream}",
            ],
            capture_output=True,
            check=False,
            text=True,
        )
        if upstream.returncode == 0 and "/" in upstream.stdout:
            remote_name = upstream.stdout.strip().split("/", 1)[0]
        result = subprocess.run(
            ["git", "-C", str(repo_root), "remote", "get-url", remote_name],
            capture_output=True,
            check=False,
            text=True,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None

    remote = result.stdout.strip()
    match = re.match(
        r"^(?:https://|ssh://git@|git@)(?P<host>[^/:]+)(?:/|:)(?P<repo>[^/]+/[^/]+?)(?:\.git)?$",
        remote,
    )
    if match and "github" in match.group("host").lower():
        return match.group("repo")
    return None


def default_repo() -> str:
    return repo_from_checkout() or FALLBACK_REPO


def codex_root() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return codex_home / "skills"


def claude_root() -> Path:
    return Path.home() / ".claude" / "skills"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install the skill from GitHub.")
    parser.add_argument(
        "--repo",
        default=default_repo(),
        help="GitHub owner/repo. Defaults to this checkout's origin or this script's repository.",
    )
    parser.add_argument("--ref", default=DEFAULT_REF, help="Git ref to download")
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="GitHub download timeout in seconds.",
    )
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


def validate_repository_ref(repo: str, ref: str) -> tuple[str, str]:
    if REPOSITORY_PATTERN.fullmatch(repo) is None or ".." in repo:
        raise RuntimeError("Invalid --repo. Expected GitHub owner/repo.")
    if (
        not ref
        or REF_PATTERN.fullmatch(ref) is None
        or ref.startswith("/")
        or ref.endswith("/")
        or ".." in PurePosixPath(ref).parts
    ):
        raise RuntimeError("Invalid --ref. Use a branch, tag, or commit name.")
    return repo, ref


def safe_extract(archive: zipfile.ZipFile, dest: Path) -> str:
    top_levels: set[str] = set()
    dest_resolved = dest.resolve()
    for info in archive.infolist():
        if "\\" in info.filename:
            raise RuntimeError(f"Unsafe archive path: {info.filename}")
        member = PurePosixPath(info.filename)
        if not member.parts:
            continue
        if member.is_absolute() or ".." in member.parts:
            raise RuntimeError(f"Unsafe archive path: {info.filename}")
        if stat.S_ISLNK(info.external_attr >> 16):
            raise RuntimeError(f"Archive symlinks are not allowed: {info.filename}")

        target = dest.joinpath(*member.parts).resolve()
        if target != dest_resolved and dest_resolved not in target.parents:
            raise RuntimeError(f"Unsafe archive path: {info.filename}")
        top_levels.add(member.parts[0])

    if len(top_levels) != 1:
        raise RuntimeError("Unexpected GitHub archive layout.")
    archive.extractall(dest)
    return next(iter(top_levels))


def download_repo(repo: str, ref: str, tmp_dir: Path, timeout: float) -> Path:
    owner, repo_name = repo.split("/", 1)
    zip_url = f"https://codeload.github.com/{owner}/{repo_name}/zip/{ref}"
    zip_path = tmp_dir / "repo.zip"
    try:
        with urllib.request.urlopen(zip_url, timeout=timeout) as response:
            with zip_path.open("wb") as file_handle:
                shutil.copyfileobj(response, file_handle)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"GitHub download failed with HTTP {exc.code}.") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"GitHub download failed: {exc}") from exc

    try:
        with zipfile.ZipFile(zip_path) as archive:
            top_level = safe_extract(archive, tmp_dir)
    except zipfile.BadZipFile as exc:
        raise RuntimeError("GitHub returned an invalid ZIP archive.") from exc
    return tmp_dir / top_level


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

    staging = dest_root / f".{skill_name}.stage-{uuid.uuid4().hex}"
    backup = dest_root / f".{skill_name}.backup-{uuid.uuid4().hex}"
    moved_existing = False
    try:
        shutil.copytree(src, staging)
        if dest_dir.exists():
            dest_dir.rename(backup)
            moved_existing = True
        try:
            staging.rename(dest_dir)
        except OSError:
            if moved_existing and backup.exists() and not dest_dir.exists():
                backup.rename(dest_dir)
            raise
        if backup.exists():
            shutil.rmtree(backup, ignore_errors=True)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        if moved_existing and backup.exists() and not dest_dir.exists():
            backup.rename(dest_dir)
        raise
    return dest_dir


def validate_selected_skills(
    repo_root: Path,
    selected_skills: list[dict[str, object]],
) -> list[tuple[str, Path]]:
    validated: list[tuple[str, Path]] = []
    root = repo_root.resolve()
    for skill in selected_skills:
        skill_name = skill.get("name")
        source = skill.get("source")
        if not isinstance(skill_name, str) or re.fullmatch(r"[a-z0-9-]+", skill_name) is None:
            raise RuntimeError(f"Invalid skill name in catalog: {skill_name!r}")
        if not isinstance(source, str):
            raise RuntimeError(f"Invalid source for skill {skill_name}.")
        src = (repo_root / source).resolve()
        if root not in src.parents or not (src / "SKILL.md").is_file():
            raise RuntimeError(f"Missing or unsafe skill path in downloaded repo: {source}")
        validated.append((skill_name, src))
    return validated


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
    try:
        if args.timeout <= 0:
            raise RuntimeError("--timeout must be greater than zero.")
        repo, ref = validate_repository_ref(args.repo, args.ref)
        targets = resolve_targets(args)
        with tempfile.TemporaryDirectory(prefix="miniapp-skill-install-") as tmp:
            repo_root = download_repo(repo, ref, Path(tmp), args.timeout)
            selected_skills = select_skills(repo_root, args.skill)
            validated_skills = validate_selected_skills(repo_root, selected_skills)
            for skill_name, src in validated_skills:
                for label, dest_root in targets:
                    dest_dir = install(src, dest_root, skill_name, force=args.force)
                    print(f"Installed {skill_name} for {label} at {dest_dir}")
    except (FileExistsError, OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
