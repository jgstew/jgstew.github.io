#!/usr/bin/env python3
"""Publish the bigfix-relevance-analyzer split set into files/analyzer/.

Called by .github/workflows/update-bigfix-relevance-analyzer-playground.yaml.
Standard library only, so it runs on a bare runner and locally.

The release contract is tools/playground-wasm/SPLIT_ANALYZER.md in
jgstew/bigfix-relevance-analyzer: a release attaches
bigfix-relevance-analyzer-analyzer.zip, a flat zip of manifest.json, editor.js,
glue.mjs, analyzer.core*.wasm.gz and index.html, listed in SHA256SUMS.txt.

    update_analyzer.py listed RELEASE_DIR/SHA256SUMS.txt
        Is the zip in this release? Sets the step output listed=true|false.

    update_analyzer.py apply --release-dir DIR --dest files/analyzer [--tag vX.Y.Z]
        Verify the zip and publish it into DEST. Sets the step output
        status=not-listed|unchanged|updated. Any problem is an error (exit 1)
        and leaves DEST as it was.
"""

import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import stat
import sys
import tempfile
import zipfile

ZIP_NAME = "bigfix-relevance-analyzer-analyzer.zip"
SUMS_NAME = "SHA256SUMS.txt"
MANIFEST = "manifest.json"
PACKAGE = "bigfix-relevance-analyzer"
# The whole set is about 9 MiB today; refuse anything absurdly larger.
MAX_TOTAL_BYTES = 256 * 1024 * 1024
# Bare file names only: no "/", "\", "..", leading dot, or other surprises.
SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class ReleaseError(Exception):
    """The release cannot be published; DEST is left untouched."""


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def _check_name(name, what):
    if not SAFE_NAME.match(name) or ".." in name:
        raise ReleaseError("unsafe %s %r: must be a bare file name" % (what, name))


def read_sums(sums_path):
    """Return {file name: sha256} from a sha256sum-style checksum file."""
    sums_path = pathlib.Path(sums_path)
    if not sums_path.is_file():
        raise ReleaseError("missing %s" % sums_path)
    sums = {}
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([0-9a-fA-F]{64}) [ *](.+)$", line.strip())
        if m:
            sums[m.group(2)] = m.group(1).lower()
    return sums


def is_listed(sums_path):
    return ZIP_NAME in read_sums(sums_path)


def read_zip(zip_path):
    """Return {name: bytes} for a flat zip, rejecting anything unsafe."""
    try:
        zf = zipfile.ZipFile(zip_path)
    except zipfile.BadZipFile as e:
        raise ReleaseError("%s is not a valid zip: %s" % (zip_path.name, e))
    with zf:
        infos = zf.infolist()
        total = 0
        seen = set()
        for info in infos:
            _check_name(info.filename, "zip entry")
            if info.is_dir():
                raise ReleaseError("unsafe zip entry %r: directory" % info.filename)
            if stat.S_ISLNK(info.external_attr >> 16):
                raise ReleaseError("zip entry %r is a symlink" % info.filename)
            if info.filename in seen:
                raise ReleaseError("duplicate zip entry %r" % info.filename)
            seen.add(info.filename)
            total += info.file_size
        if total > MAX_TOTAL_BYTES:
            raise ReleaseError("zip is too large when unpacked (%d bytes)" % total)
        try:
            return {info.filename: zf.read(info) for info in infos}
        except (zipfile.BadZipFile, OSError) as e:
            raise ReleaseError("cannot read %s: %s" % (zip_path.name, e))


def check_manifest(files, tag=None):
    """Validate manifest.json against the unpacked files (SPLIT_ANALYZER.md)."""
    if MANIFEST not in files:
        raise ReleaseError("zip has no %s" % MANIFEST)
    try:
        manifest = json.loads(files[MANIFEST].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as e:
        raise ReleaseError("%s is not valid JSON: %s" % (MANIFEST, e))
    if not isinstance(manifest, dict) or manifest.get("format") != 1:
        raise ReleaseError("unknown %s format: %r" % (MANIFEST, manifest.get("format")
                                                     if isinstance(manifest, dict)
                                                     else manifest))
    if manifest.get("package") != PACKAGE:
        raise ReleaseError("unexpected package %r" % manifest.get("package"))
    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        raise ReleaseError("%s has no version" % MANIFEST)
    if tag and version != (tag[1:] if tag.startswith("v") else tag):
        raise ReleaseError("manifest version %s does not match tag %s" % (version, tag))

    entries = [manifest.get("editor"), manifest.get("glue")]
    cores = manifest.get("cores")
    if not isinstance(cores, list) or not cores:
        raise ReleaseError("%s has no cores" % MANIFEST)
    entries.extend(cores)
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise ReleaseError("malformed %s entry: %r" % (MANIFEST, entry))
        path = entry["path"]
        _check_name(path, "manifest path")
        if path not in files:
            raise ReleaseError("%s names %s, which the zip does not have"
                               % (MANIFEST, path))
        data = files[path]
        if entry.get("size") != len(data) or entry.get("sha256") != _sha256(data):
            raise ReleaseError("%s does not match its size/sha256 in %s"
                               % (path, MANIFEST))
    return version


def _install(src, dst):
    """Copy src to dst atomically (write a temp file beside dst, then rename)."""
    tmp = dst.with_name("." + dst.name + ".tmp")
    shutil.copyfile(src, tmp)
    os.replace(tmp, dst)


def _published_matches(dest, files):
    if not (dest / MANIFEST).is_file():
        return False
    if (dest / MANIFEST).read_bytes() != files[MANIFEST]:
        return False
    # The manifest matches. Also confirm the folder holds exactly these bytes,
    # so a hand-edited or partly written folder gets repaired.
    if sorted(p.name for p in dest.iterdir()) != sorted(files):
        return False
    return all((dest / name).read_bytes() == data for name, data in files.items())


def apply_release(release_dir, dest, tag=None, work_dir=None):
    """Publish the release's split set into dest.

    Returns "not-listed", "unchanged" or "updated". Raises ReleaseError, with
    dest untouched, if anything about the release is wrong.
    """
    release_dir = pathlib.Path(release_dir)
    dest = pathlib.Path(dest)
    sums = read_sums(release_dir / SUMS_NAME)
    if ZIP_NAME not in sums:
        return "not-listed"

    zip_path = release_dir / ZIP_NAME
    if not zip_path.is_file():
        raise ReleaseError("%s is listed in %s but missing" % (ZIP_NAME, SUMS_NAME))
    if _sha256(zip_path.read_bytes()) != sums[ZIP_NAME]:
        raise ReleaseError("%s checksum does not match %s" % (ZIP_NAME, SUMS_NAME))

    files = read_zip(zip_path)
    check_manifest(files, tag)
    if dest.is_dir() and _published_matches(dest, files):
        return "unchanged"

    # Everything is validated; only now touch dest. Stage the files on disk,
    # then follow the producer's order: remove the old manifest first, write
    # every other file, remove files the new set no longer has, and write the
    # new manifest last, so a reader never sees a manifest naming missing files.
    if work_dir is not None:
        pathlib.Path(work_dir).mkdir(parents=True, exist_ok=True)
    staging = pathlib.Path(tempfile.mkdtemp(prefix="analyzer-", dir=work_dir))
    try:
        for name, data in files.items():
            (staging / name).write_bytes(data)
        dest.mkdir(parents=True, exist_ok=True)
        if (dest / MANIFEST).exists():
            (dest / MANIFEST).unlink()
        for name in sorted(files):
            if name != MANIFEST:
                _install(staging / name, dest / name)
        for path in sorted(dest.iterdir()):
            if path.name in files:
                continue
            if path.is_dir() and not path.is_symlink():
                print("::warning::leaving unexpected directory %s" % path)
            else:
                path.unlink()
        _install(staging / MANIFEST, dest / MANIFEST)
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return "updated"


def _set_output(key, value):
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write("%s=%s\n" % (key, value))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p_listed = sub.add_parser("listed", help="is the zip listed in SHA256SUMS.txt?")
    p_listed.add_argument("sums", type=pathlib.Path)
    p_apply = sub.add_parser("apply", help="verify and publish the zip")
    p_apply.add_argument("--release-dir", type=pathlib.Path, required=True)
    p_apply.add_argument("--dest", type=pathlib.Path, required=True)
    p_apply.add_argument("--tag", default=None)
    p_apply.add_argument("--work-dir", type=pathlib.Path, default=None)
    args = parser.parse_args(argv)

    try:
        if args.command == "listed":
            listed = is_listed(args.sums)
            if listed:
                print("%s is listed in %s" % (ZIP_NAME, args.sums.name))
            else:
                print("::notice::%s is not listed in %s: this release has no "
                      "split analyzer set, nothing to publish"
                      % (ZIP_NAME, args.sums.name))
            _set_output("listed", "true" if listed else "false")
        else:
            status = apply_release(args.release_dir, args.dest, args.tag,
                                   args.work_dir)
            messages = {
                "not-listed": "::notice::%s is not in this release; nothing to do"
                % ZIP_NAME,
                "unchanged": "%s already matches this release; nothing to do"
                % args.dest,
                "updated": "published the split analyzer set into %s" % args.dest,
            }
            print(messages[status])
            _set_output("status", status)
    except ReleaseError as e:
        print("::error::%s" % e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
