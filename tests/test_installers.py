from __future__ import annotations

import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import zipfile

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    path = REPO_ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(name.removesuffix(".py"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


REMOTE = load_script("install_from_github.py")
LOCAL = load_script("install_skill.py")


def archive_bytes(entries: dict[str, str]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, content in entries.items():
            archive.writestr(name, content)
    return buffer.getvalue()


class RemoteInputTests(unittest.TestCase):
    def test_repository_and_ref_validation(self) -> None:
        self.assertEqual(
            REMOTE.validate_repository_ref("owner/repo", "refs/tags/v1.2.3"),
            ("owner/repo", "refs/tags/v1.2.3"),
        )
        for repo in ("https://github.com/owner/repo", "../repo", "owner/repo/extra"):
            with self.subTest(repo=repo), self.assertRaises(RuntimeError):
                REMOTE.validate_repository_ref(repo, "main")
        for ref in ("", "../main", "/main", "main/", "main?x=1"):
            with self.subTest(ref=ref), self.assertRaises(RuntimeError):
                REMOTE.validate_repository_ref("owner/repo", ref)

    def test_safe_extract_rejects_unsafe_paths(self) -> None:
        for member in ("../outside.txt", "/absolute.txt", "repo-main\\outside.txt"):
            with self.subTest(member=member), tempfile.TemporaryDirectory() as tmp:
                archive_path = Path(tmp) / "bad.zip"
                archive_path.write_bytes(archive_bytes({member: "bad"}))
                with zipfile.ZipFile(archive_path) as archive:
                    with self.assertRaises(RuntimeError):
                        REMOTE.safe_extract(archive, Path(tmp) / "extract")
                self.assertFalse((Path(tmp).parent / "outside.txt").exists())

    def test_safe_extract_rejects_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            archive_path = Path(tmp) / "symlink.zip"
            info = zipfile.ZipInfo("repo-main/link")
            info.create_system = 3
            info.external_attr = 0o120777 << 16
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr(info, "../outside")
            with zipfile.ZipFile(archive_path) as archive:
                with self.assertRaises(RuntimeError):
                    REMOTE.safe_extract(archive, Path(tmp) / "extract")

    def test_download_uses_timeout_and_extracts_one_root(self) -> None:
        payload = archive_bytes({"repo-main/catalog.json": "{}", "repo-main/file.txt": "ok"})
        with tempfile.TemporaryDirectory() as tmp:
            response = io.BytesIO(payload)
            with mock.patch.object(REMOTE.urllib.request, "urlopen", return_value=response) as urlopen:
                root = REMOTE.download_repo("owner/repo", "main", Path(tmp), timeout=7.5)
            self.assertEqual(root.name, "repo-main")
            self.assertEqual((root / "file.txt").read_text(), "ok")
            urlopen.assert_called_once_with(
                "https://codeload.github.com/owner/repo/zip/main",
                timeout=7.5,
            )


class AtomicInstallTests(unittest.TestCase):
    def make_source(self, root: Path, value: str) -> Path:
        source = root / "source"
        source.mkdir()
        (source / "SKILL.md").write_text(value)
        return source

    def test_force_replaces_existing_skill(self) -> None:
        for installer in (REMOTE, LOCAL):
            with self.subTest(installer=installer.__name__), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                source = self.make_source(root, "new")
                destination_root = root / "dest"
                existing = destination_root / "demo-skill"
                existing.mkdir(parents=True)
                (existing / "SKILL.md").write_text("old")

                result = installer.install(source, destination_root, "demo-skill", force=True)

                self.assertEqual((result / "SKILL.md").read_text(), "new")
                self.assertEqual(list(destination_root.glob(".demo-skill.*")), [])

    def test_force_restores_existing_skill_when_swap_fails(self) -> None:
        for installer in (REMOTE, LOCAL):
            with self.subTest(installer=installer.__name__), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                source = self.make_source(root, "new")
                destination_root = root / "dest"
                existing = destination_root / "demo-skill"
                existing.mkdir(parents=True)
                (existing / "SKILL.md").write_text("old")
                original_rename = Path.rename

                def fail_staging_swap(path: Path, target: Path):
                    if ".stage-" in path.name:
                        raise OSError("simulated swap failure")
                    return original_rename(path, target)

                with mock.patch.object(Path, "rename", new=fail_staging_swap):
                    with self.assertRaises(OSError):
                        installer.install(source, destination_root, "demo-skill", force=True)

                self.assertEqual((existing / "SKILL.md").read_text(), "old")
                self.assertEqual(list(destination_root.glob(".demo-skill.*")), [])


if __name__ == "__main__":
    unittest.main()
