"""Tests for update_analyzer.py, run against fake releases in a temp dir.

Standard library only. Run from the repo root:

    python3 -m unittest discover -s .github/scripts -p "test_*.py" -v
"""

import json
import os
import re
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
FAKE_RELEASE = HERE / "fake_release.py"
FROZEN_PAGE = REPO / "files/bigfix-relevance-analyzer-playground.html"
ZIP_NAME = "bigfix-relevance-analyzer-analyzer.zip"

sys.path.insert(0, str(HERE))
import update_analyzer  # noqa: E402
from fake_release import (  # noqa: E402
    encode_manifest,
    make_set,
    sha256,
    write_release,
)


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

    def release_with(self, files, **kwargs):
        return write_release(self.release, files, **kwargs)

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

    def test_real_release_sums_format(self):
        # v1.38.1's SHA256SUMS.txt, verbatim apart from the hashes elided.
        sums = self.release / "SHA256SUMS.txt"
        sums.write_text(
            "%s  ./bigfix-relevance-analyzer-playground.html\n"
            "%s  ./bigfix-relevance-developer.vsix\n" % ("a" * 64, "b" * 64)
        )
        self.assertFalse(update_analyzer.is_listed(sums))
        sums.write_text("%s  ./%s\n" % ("c" * 64, ZIP_NAME))
        self.assertTrue(update_analyzer.is_listed(sums))

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

    def test_bare_name_in_sums(self):
        files = make_set()
        self.release_with(files, prefix="")
        self.assertEqual(self.apply(), "updated")
        self.assert_published(files)

    def test_dot_slash_name_in_sums(self):
        files = make_set()
        self.release_with(files, prefix="./")
        self.assertEqual(self.apply(), "updated")
        self.assert_published(files)

    def test_optional_raw_core_fields_accepted(self):
        files = make_set()
        manifest = json.loads(files["manifest.json"])
        for core in manifest["cores"]:
            core["raw_size"] = 1234
            core["raw_sha256"] = "d" * 64
        files["manifest.json"] = encode_manifest(manifest)
        self.release_with(files)
        self.assertEqual(self.apply(), "updated")
        self.assert_published(files)

    def test_unknown_extra_keys_accepted(self):
        files = make_set()
        manifest = json.loads(files["manifest.json"])
        manifest["built_by"] = "a future producer"
        manifest["glue"]["note"] = "extra"
        manifest["cores"][0]["note"] = "extra"
        files["manifest.json"] = encode_manifest(manifest)
        self.release_with(files)
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

    def test_write_failure_is_reported(self):
        self.publish(make_set("1.38.0", salt=b"old"))
        self.release_with(make_set("1.39.0"))
        real = update_analyzer._install
        calls = []

        def failing(src, dst):
            calls.append(dst)
            if len(calls) == 2:
                raise OSError(28, "No space left on device")
            return real(src, dst)

        update_analyzer._install = failing
        self.addCleanup(setattr, update_analyzer, "_install", real)
        with self.assertRaisesRegex(update_analyzer.ReleaseError, "partly written"):
            self.apply()


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

    def edit_manifest(self, change):
        files = make_set()
        manifest = json.loads(files["manifest.json"])
        change(manifest)
        files["manifest.json"] = encode_manifest(manifest)
        return files

    def test_entry_not_in_manifest(self):
        self.release_with(make_set(), extra=[(zipfile.ZipInfo("extra.js"), b"x")])
        self.assert_rejected("not named in manifest.json")

    def test_core_name_does_not_match_path(self):
        def change(m):
            m["cores"][1]["name"] = "analyzer.core9.wasm"
        self.release_with(self.edit_manifest(change))
        self.assert_rejected("core")

    def test_core_name_is_not_a_core(self):
        files = make_set()
        manifest = json.loads(files["manifest.json"])
        files["evil.wasm.gz"] = files["analyzer.core2.wasm.gz"]
        manifest["cores"][1]["name"] = "evil.wasm"
        manifest["cores"][1]["path"] = "evil.wasm.gz"
        del files["analyzer.core2.wasm.gz"]
        files["manifest.json"] = encode_manifest(manifest)
        self.release_with(files)
        self.assert_rejected("core name")

    def test_core_encoding_not_gzip(self):
        def change(m):
            m["cores"][0]["encoding"] = "br"
        self.release_with(self.edit_manifest(change))
        self.assert_rejected("encoding")

    def test_bad_raw_sha256(self):
        def change(m):
            m["cores"][0]["raw_sha256"] = "not hex"
        self.release_with(self.edit_manifest(change))
        self.assert_rejected("raw_sha256")

    def test_bad_raw_size(self):
        for bad in (-1, "12", 1.5, True):
            with self.subTest(raw_size=bad):
                def change(m):
                    m["cores"][0]["raw_size"] = bad
                self.release_with(self.edit_manifest(change))
                self.assert_rejected("raw_size")

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


class FakeReleaseTest(AnalyzerTestCase):
    """fake_release.py builds what the workflow's PR dry run unpacks."""

    def test_fake_release_round_trip(self):
        proc = subprocess.run(
            [sys.executable, "-I", str(FAKE_RELEASE), str(self.release),
             "--version", "0.0.0"],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        sums = (self.release / "SHA256SUMS.txt").read_text()
        self.assertIn("  ./%s\n" % ZIP_NAME, sums)
        self.assertEqual(self.apply(tag="v0.0.0"), "updated")
        self.assertEqual(self.apply(tag="v0.0.0"), "unchanged")


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
        # It is named only as a pull_request path, so PRs that change it run
        # the pin test.
        lines = [
            line.strip()
            for line in self.text.splitlines()
            if "bigfix-relevance-analyzer-playground.html" in line
        ]
        self.assertEqual(lines, ['- "files/bigfix-relevance-analyzer-playground.html"'])

    def test_pull_request_dry_run_exercises_unpack(self):
        self.assertIn("python3 -I .github/scripts/fake_release.py", self.text)
        dry_run = self.text[self.text.index("fake_release.py"):]
        self.assertIn("sha256sum -c --ignore-missing", dry_run)
        self.assertIn("update_analyzer.py apply", dry_run)
        self.assertIn("status=unchanged", dry_run)

    def test_pull_requests_do_not_share_the_publish_queue(self):
        self.assertIn(
            "group: update-playground-${{ github.event_name == 'pull_request'"
            " && github.ref || 'publish' }}",
            self.text,
        )

    def test_release_without_sums_is_a_no_op(self):
        # v0.1.0 to v0.5.1 have no SHA256SUMS.txt.
        self.assertIn("has no SHA256SUMS.txt", self.text)

    def test_version_input_pattern(self):
        m = re.search(r"grep -Eq '([^']+)'", self.text)
        self.assertIsNotNone(m)
        pattern = re.compile(m.group(1))
        for good in ("1.38.1", "v1.38.1", "1.0.0b1", "1.0.0rc1", "1.0.0-rc.1",
                     "2.0.0.post1"):
            self.assertTrue(pattern.match(good), good)
        for bad in ("1.0", "latest", "1.0.0;rm -rf /", "../1.0.0", "1.0.0 x", ""):
            self.assertFalse(pattern.match(bad), bad)

    def test_runs_the_tests_on_pull_requests(self):
        self.assertIn("python3 -m unittest discover -s .github/scripts", self.text)
        self.assertIn('".github/scripts/**"', self.text)

    def test_verifies_with_sha256sum(self):
        self.assertIn("sha256sum -c --ignore-missing", self.text)


if __name__ == "__main__":
    unittest.main()
