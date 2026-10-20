"""Tests for update_analyzer.py, run against fake releases in a temp dir.

Standard library only. Run from the repo root:

    python3 -m unittest discover -s .github/scripts -p "test_*.py" -v
"""

import hashlib
import json
import os
import pathlib
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCRIPT = HERE / "update_analyzer.py"
FROZEN_PAGE = REPO / "files/bigfix-relevance-analyzer-playground.html"
ZIP_NAME = "bigfix-relevance-analyzer-analyzer.zip"

sys.path.insert(0, str(HERE))
import update_analyzer  # noqa: E402


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def make_set(version="1.38.1", cores=3, salt=b""):
    """Return {name: bytes} for a split analyzer set, manifest.json included."""
    files = {
        "editor.js": b"window.playgroundEditor = {};\n" + salt,
        "glue.mjs": b"globalThis.__component = {};\n" + salt,
        "index.html": b"<!doctype html><title>analyzer</title>\n" + salt,
    }
    core_entries = []
    for i in range(1, cores + 1):
        name = "analyzer.core.wasm" if i == 1 else "analyzer.core%d.wasm" % i
        path = name + ".gz"
        files[path] = b"\x1f\x8b fake core %d " % i + salt
        core_entries.append(
            {
                "name": name,
                "path": path,
                "encoding": "gzip",
                "size": len(files[path]),
                "sha256": sha256(files[path]),
            }
        )
    core_entries.sort(key=lambda e: e["name"])

    def entry(path):
        return {"path": path, "size": len(files[path]), "sha256": sha256(files[path])}

    manifest = {
        "format": 1,
        "package": "bigfix-relevance-analyzer",
        "version": version,
        "editor": entry("editor.js"),
        "glue": entry("glue.mjs"),
        "cores": core_entries,
    }
    files["manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    return files


def write_zip(path, files, extra=None):
    """Write a flat zip like the producer's: fixed timestamps, manifest last."""
    names = sorted(n for n in files if n != "manifest.json")
    if "manifest.json" in files:
        names.append("manifest.json")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in names:
            zf.writestr(zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0)), files[name])
        for info, data in extra or []:
            zf.writestr(info, data)


class AnalyzerTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp(prefix="update-analyzer-"))
        self.addCleanup(shutil.rmtree, self.tmp)
        # A copy of the site's files/ layout: the frozen page and the
        # published split set side by side.
        self.files = self.tmp / "site/files"
        self.files.mkdir(parents=True)
        self.frozen = self.files / FROZEN_PAGE.name
        shutil.copyfile(FROZEN_PAGE, self.frozen)
        self.frozen_sha = sha256(self.frozen.read_bytes())
        self.dest = self.files / "analyzer"
        self.release = self.tmp / "release"
        self.release.mkdir()
        self.work = self.tmp / "work"

    def tearDown(self):
        # Regression: whatever happened, the frozen single-file page is
        # untouched.
        self.assertEqual(sha256(self.frozen.read_bytes()), self.frozen_sha)

    # helpers

    def publish(self, files):
        self.dest.mkdir(parents=True, exist_ok=True)
        for name, data in files.items():
            (self.dest / name).write_bytes(data)

    def release_with(self, files, listed=True, sums_hash=None, extra=None, sep="  "):
        zip_path = self.release / ZIP_NAME
        write_zip(zip_path, files, extra)
        lines = ["%s  bigfix-relevance-analyzer-playground.html" % ("0" * 64)]
        if listed:
            digest = sums_hash or sha256(zip_path.read_bytes())
            lines.append("%s%s%s" % (digest, sep, ZIP_NAME))
        (self.release / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n")
        return zip_path

    def apply(self, tag=None):
        return update_analyzer.apply_release(
            self.release, self.dest, tag=tag, work_dir=self.work
        )

    def snapshot(self):
        if not self.dest.exists():
            return None
        return {
            p.name: (p.read_bytes(), p.stat().st_mtime_ns)
            for p in sorted(self.dest.iterdir())
        }

    def assert_published(self, files):
        self.assertEqual(sorted(p.name for p in self.dest.iterdir()), sorted(files))
        for name, data in files.items():
            self.assertEqual((self.dest / name).read_bytes(), data, name)

    def assert_rejected(self, pattern, tag=None):
        before = self.snapshot()
        with self.assertRaisesRegex(update_analyzer.ReleaseError, pattern):
            self.apply(tag=tag)
        self.assertEqual(self.snapshot(), before, "published set changed")
        self.assertFalse((self.files / "evil").exists())
        self.assertFalse((self.tmp / "evil").exists())


class NotListedTest(AnalyzerTestCase):
    """Every release up to v1.38.1 has no zip: finish without changes."""

    def test_not_listed_with_nothing_published(self):
        self.release_with(make_set(), listed=False)
        self.assertEqual(self.apply(), "not-listed")
        self.assertFalse(self.dest.exists())

    def test_not_listed_leaves_published_set(self):
        self.publish(make_set("1.38.0"))
        before = self.snapshot()
        self.release_with(make_set(), listed=False)
        self.assertEqual(self.apply(), "not-listed")
        self.assertEqual(self.snapshot(), before)

    def test_not_listed_does_not_need_the_zip(self):
        (self.release / "SHA256SUMS.txt").write_text(
            "%s  bigfix-relevance-analyzer-playground.html\n" % ("0" * 64)
        )
        self.assertEqual(self.apply(), "not-listed")

    def test_is_listed(self):
        self.release_with(make_set(), listed=False)
        self.assertFalse(update_analyzer.is_listed(self.release / "SHA256SUMS.txt"))
        self.release_with(make_set(), listed=True)
        self.assertTrue(update_analyzer.is_listed(self.release / "SHA256SUMS.txt"))

    def test_missing_sums_file_is_an_error(self):
        with self.assertRaises(update_analyzer.ReleaseError):
            self.apply()


class GoodZipTest(AnalyzerTestCase):
    def test_first_publish(self):
        files = make_set()
        self.release_with(files)
        self.assertEqual(self.apply(tag="v1.38.1"), "updated")
        self.assert_published(files)

    def test_binary_mode_marker_in_sums(self):
        files = make_set()
        self.release_with(files, sep=" *")
        self.assertEqual(self.apply(), "updated")
        self.assert_published(files)

    def test_replaces_older_set(self):
        self.publish(make_set("1.38.0", salt=b"old"))
        files = make_set("1.39.0")
        self.release_with(files)
        self.assertEqual(self.apply(tag="1.39.0"), "updated")
        self.assert_published(files)

    def test_rebuild_at_same_version_is_applied(self):
        self.publish(make_set("1.39.0", salt=b"first build"))
        files = make_set("1.39.0", salt=b"second build")
        self.release_with(files)
        self.assertEqual(self.apply(), "updated")
        self.assert_published(files)

    def test_dropped_file_is_deleted(self):
        self.publish(make_set("1.38.0", cores=14))
        files = make_set("1.39.0", cores=13)
        self.release_with(files)
        self.assertEqual(self.apply(), "updated")
        self.assert_published(files)
        self.assertFalse((self.dest / "analyzer.core14.wasm.gz").exists())

    def test_stray_file_is_deleted(self):
        self.publish(make_set())
        (self.dest / "stray.txt").write_text("not in the zip")
        self.release_with(make_set())
        self.assertEqual(self.apply(), "updated")
        self.assert_published(make_set())

    def test_identical_zip_is_unchanged(self):
        files = make_set()
        self.publish(files)
        before = self.snapshot()
        self.release_with(files)
        self.assertEqual(self.apply(), "unchanged")
        self.assertEqual(self.snapshot(), before, "files were rewritten")

    def test_manifest_matches_but_file_differs_is_repaired(self):
        files = make_set()
        self.publish(files)
        (self.dest / "glue.mjs").write_bytes(b"hand edited")
        self.release_with(files)
        self.assertEqual(self.apply(), "updated")
        self.assert_published(files)

    def test_manifest_is_written_last(self):
        self.publish(make_set("1.38.0", salt=b"old"))
        files = make_set("1.39.0")
        self.release_with(files)
        order = []
        real = update_analyzer._install

        def spy(src, dst):
            order.append(pathlib.Path(dst).name)
            return real(src, dst)

        update_analyzer._install = spy
        self.addCleanup(setattr, update_analyzer, "_install", real)
        self.apply()
        self.assertEqual(order[-1], "manifest.json")
        self.assertEqual(sorted(order), sorted(files))


class RejectedZipTest(AnalyzerTestCase):
    def setUp(self):
        super().setUp()
        self.publish(make_set("1.38.0"))

    def test_bad_checksum(self):
        self.release_with(make_set(), sums_hash="f" * 64)
        self.assert_rejected("checksum")

    def test_listed_but_not_downloaded(self):
        self.release_with(make_set())
        (self.release / ZIP_NAME).unlink()
        self.assert_rejected("missing")

    def test_path_traversal(self):
        self.release_with(
            make_set(), extra=[(zipfile.ZipInfo("../evil"), b"x")]
        )
        self.assert_rejected("unsafe")

    def test_subdirectory_entry(self):
        self.release_with(
            make_set(), extra=[(zipfile.ZipInfo("sub/evil"), b"x")]
        )
        self.assert_rejected("unsafe")

    def test_backslash_entry(self):
        self.release_with(
            make_set(), extra=[(zipfile.ZipInfo("..\\evil"), b"x")]
        )
        self.assert_rejected("unsafe")

    def test_absolute_entry(self):
        self.release_with(make_set(), extra=[(zipfile.ZipInfo("/evil"), b"x")])
        self.assert_rejected("unsafe")

    def test_symlink_entry(self):
        info = zipfile.ZipInfo("evil")
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        self.release_with(make_set(), extra=[(info, b"../../etc/passwd")])
        self.assert_rejected("symlink")

    def test_duplicate_entry(self):
        files = make_set()
        self.release_with(
            files, extra=[(zipfile.ZipInfo("glue.mjs"), b"second copy")]
        )
        self.assert_rejected("duplicate")

    def test_no_manifest(self):
        files = make_set()
        del files["manifest.json"]
        self.release_with(files)
        self.assert_rejected("manifest.json")

    def test_unknown_format(self):
        files = make_set()
        manifest = json.loads(files["manifest.json"])
        manifest["format"] = 2
        files["manifest.json"] = json.dumps(manifest).encode()
        self.release_with(files)
        self.assert_rejected("format")

    def test_wrong_package(self):
        files = make_set()
        manifest = json.loads(files["manifest.json"])
        manifest["package"] = "something-else"
        files["manifest.json"] = json.dumps(manifest).encode()
        self.release_with(files)
        self.assert_rejected("package")

    def test_file_does_not_match_manifest(self):
        files = make_set()
        files["analyzer.core2.wasm.gz"] = b"tampered"
        self.release_with(files)
        self.assert_rejected("analyzer.core2.wasm.gz")

    def test_manifest_names_missing_file(self):
        files = make_set()
        del files["glue.mjs"]
        self.release_with(files)
        self.assert_rejected("glue.mjs")

    def test_manifest_path_escapes(self):
        files = make_set()
        manifest = json.loads(files["manifest.json"])
        manifest["glue"]["path"] = "../glue.mjs"
        files["manifest.json"] = json.dumps(manifest).encode()
        self.release_with(files)
        self.assert_rejected("unsafe")

    def test_version_does_not_match_tag(self):
        self.release_with(make_set("1.39.0"))
        self.assert_rejected("version", tag="v1.40.0")


class CommandLineTest(AnalyzerTestCase):
    def run_cli(self, *args):
        out = self.tmp / "github_output"
        env = dict(os.environ, GITHUB_OUTPUT=str(out))
        proc = subprocess.run(
            [sys.executable, "-I", str(SCRIPT)] + [str(a) for a in args],
            env=env,
            capture_output=True,
            text=True,
        )
        outputs = out.read_text() if out.exists() else ""
        return proc, outputs

    def test_listed_command(self):
        self.release_with(make_set(), listed=False)
        proc, outputs = self.run_cli("listed", self.release / "SHA256SUMS.txt")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("listed=false", outputs)
        self.assertIn("not listed", proc.stdout)

        self.release_with(make_set())
        proc, outputs = self.run_cli("listed", self.release / "SHA256SUMS.txt")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("listed=true", outputs)

    def test_apply_command(self):
        self.release_with(make_set())
        proc, outputs = self.run_cli(
            "apply", "--release-dir", self.release, "--dest", self.dest,
            "--tag", "v1.38.1", "--work-dir", self.work,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("status=updated", outputs)
        self.assert_published(make_set())

    def test_apply_command_failure(self):
        self.release_with(make_set(), sums_hash="f" * 64)
        proc, outputs = self.run_cli(
            "apply", "--release-dir", self.release, "--dest", self.dest,
            "--work-dir", self.work,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("::error::", proc.stdout + proc.stderr)
        self.assertNotIn("status=", outputs)


class WorkflowTest(unittest.TestCase):
    """The workflow publishes the split set and leaves the frozen page alone."""

    def setUp(self):
        self.text = (
            REPO / ".github/workflows/update-bigfix-relevance-analyzer-playground.yaml"
        ).read_text(encoding="utf-8")

    def test_calls_the_script(self):
        self.assertIn(".github/scripts/update_analyzer.py", self.text)
        self.assertIn("files/analyzer", self.text)

    def test_never_touches_the_frozen_page(self):
        self.assertNotIn("bigfix-relevance-analyzer-playground.html", self.text)

    def test_runs_the_tests_on_pull_requests(self):
        self.assertIn("python3 -m unittest discover -s .github/scripts", self.text)
        self.assertIn('".github/scripts/**"', self.text)

    def test_verifies_with_sha256sum(self):
        self.assertIn("sha256sum -c --ignore-missing", self.text)


if __name__ == "__main__":
    unittest.main()
