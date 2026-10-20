#!/usr/bin/env python3
"""Build a fake bigfix-relevance-analyzer release for testing update_analyzer.py.

Used by the tests and by the workflow's pull_request dry run, which needs a
release with the split set zip to exercise download/verify/unpack. Standard
library only. The file contents are placeholders, not a working analyzer.

    fake_release.py OUT_DIR [--version 0.0.0]
        Writes OUT_DIR/bigfix-relevance-analyzer-analyzer.zip and an
        OUT_DIR/SHA256SUMS.txt in the real release format ("<hash>  ./<name>").
"""

import argparse
import hashlib
import json
import pathlib
import sys
import zipfile

ZIP_NAME = "bigfix-relevance-analyzer-analyzer.zip"


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
    files["manifest.json"] = encode_manifest(manifest)
    return files


def encode_manifest(manifest):
    return (json.dumps(manifest, indent=2) + "\n").encode()


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


def write_release(out_dir, files, listed=True, sums_hash=None, extra=None,
                  prefix="./", sep="  "):
    """Write the zip and SHA256SUMS.txt into out_dir; return the zip's path.

    The real release lists assets as "<hash>  ./<name>" (the producer runs
    `sha256sum ./*`), so prefix defaults to "./".
    """
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / ZIP_NAME
    write_zip(zip_path, files, extra)
    lines = ["%s  %sbigfix-relevance-analyzer-playground.html" % ("0" * 64, prefix)]
    if listed:
        digest = sums_hash or sha256(zip_path.read_bytes())
        lines.append("%s%s%s%s" % (digest, sep, prefix, ZIP_NAME))
    (out_dir / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n")
    return zip_path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("out_dir", type=pathlib.Path)
    parser.add_argument("--version", default="0.0.0")
    args = parser.parse_args(argv)
    write_release(args.out_dir, make_set(args.version))
    print("wrote a fake %s release into %s" % (args.version, args.out_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
