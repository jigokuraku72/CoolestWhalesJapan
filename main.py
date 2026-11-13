#!/usr/bin/env python3
"""coolest-art-01 entry: "The Whale and the Blue Planet — Ukiyo-e".

Copies the bundled entry.png to the output directory and verifies it.
Stdlib only, no network access.

The output directory is taken from MAKEFUN_OUTPUT_DIR when set,
otherwise it falls back to /output (the grader's Docker container
does not set MAKEFUN_OUTPUT_DIR, so the fallback is required).
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.png")

EXPECTED_SHA256 = "a53e744fb4bc193f468948f03367f25e0c4df1a1167b04de081466cb68f178fe"
EXPECTED_BYTES = 348353
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 683


def jpeg_dimensions(path):
    """Read width/height from a JPEG's SOF marker (stdlib only)."""
    with open(path, "rb") as f:
        data = f.read()
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height = (data[i + 5] << 8) | data[i + 6]
            width = (data[i + 7] << 8) | data[i + 8]
            return width, height
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        length = (data[i + 2] << 8) | data[i + 3]
        i += 2 + length
    return None, None


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    with open(SOURCE, "rb") as f:
        magic = f.read(2)
    if magic != b"\xff\xd8":
        print("source is not a JPEG (bad magic bytes)", file=sys.stderr)
        return 1

    size = os.path.getsize(SOURCE)
    if size != EXPECTED_BYTES:
        print(f"source size mismatch: {size} != {EXPECTED_BYTES}",
              file=sys.stderr)
        return 1
    if sha256_of(SOURCE) != EXPECTED_SHA256:
        print("source sha256 mismatch", file=sys.stderr)
        return 1

    width, height = jpeg_dimensions(SOURCE)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print(f"source dimensions mismatch: {width}x{height} "
              f"!= {EXPECTED_WIDTH}x{EXPECTED_HEIGHT} (image was cropped?)",
              file=sys.stderr)
        return 1
    print(f"source verified: {size} bytes, JPEG magic OK, "
          f"dimensions {width}x{height} (uncropped landscape)")

    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, OUT_PATH)

    out_size = os.path.getsize(OUT_PATH)
    out_sha = sha256_of(OUT_PATH)
    if out_size != EXPECTED_BYTES or out_sha != EXPECTED_SHA256:
        print("output verification failed", file=sys.stderr)
        return 1

    print(f"wrote {OUT_PATH} ({out_size} bytes, sha256 {out_sha[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
