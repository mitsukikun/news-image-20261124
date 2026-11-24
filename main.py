#!/usr/bin/env python3
"""Publish the news-image-20261124 front page.

Copies the shipped picture (entry.png, JPEG bytes under a .png name)
into the output directory and verifies it before reporting success.

Pure standard library only; no network, no timestamps, no randomness,
so two runs write byte-identical output.

Usage:
    python3 main.py
    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import struct
import sys

PICTURE_NAME = "entry.png"
MAX_BYTES = 1024 * 1024          # 1 MiB cap from the competition
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def fail(message):
    print("FAIL: " + message, file=sys.stderr)
    raise SystemExit(1)


def read_picture(path):
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except OSError as exc:
        fail("cannot read %s: %s" % (path, exc))


def jpeg_dimensions(data):
    """Return (width, height) from the first JPEG frame header (SOF0/1/2).

    Walks the marker segments: each segment is 0xFF, marker byte, then a
    2-byte big-endian length (length includes its own two bytes).
    """
    if len(data) < 4 or data[0:2] != b"\xff\xd8":
        return None
    pos = 2
    while pos + 9 <= len(data):
        if data[pos] != 0xFF:
            pos += 1
            continue
        marker = data[pos + 1]
        if marker in (0xC0, 0xC1, 0xC2):  # baseline / extended / progressive
            height = struct.unpack(">H", data[pos + 5:pos + 7])[0]
            width = struct.unpack(">H", data[pos + 7:pos + 9])[0]
            return (width, height)
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if pos + 4 > len(data):
            return None
        length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if length < 2:
            return None
        pos += 2 + length
    return None


def check_picture(data, path):
    if not data:
        fail("%s is empty" % path)
    if len(data) > MAX_BYTES:
        fail("%s is %d bytes, over the %d-byte cap" % (path, len(data), MAX_BYTES))
    if data[0:2] != b"\xff\xd8":
        fail("%s has no JPEG start-of-image marker" % path)
    if data[-2:] != b"\xff\xd9":
        fail("%s has no JPEG end-of-image marker" % path)
    size = jpeg_dimensions(data)
    if size is None:
        fail("%s has no readable JPEG frame header" % path)
    if size != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail("%s is %dx%d, expected %dx%d"
             % (path, size[0], size[1], EXPECTED_WIDTH, EXPECTED_HEIGHT))
    return size


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, PICTURE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dest_path = os.path.join(out_dir, PICTURE_NAME)

    data = read_picture(source_path)
    width, height = check_picture(data, source_path)
    digest = hashlib.sha256(data).hexdigest()

    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        fail("cannot create output directory %s: %s" % (out_dir, exc))
    try:
        with open(dest_path, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        fail("cannot write %s: %s" % (dest_path, exc))

    written = read_picture(dest_path)
    if written != data:
        fail("output %s differs from shipped %s" % (dest_path, source_path))
    # Re-validate the file that actually landed on disk, so a truncated
    # or corrupted write is caught even if the bytes happened to match
    # in memory.
    check_picture(written, dest_path)
    if hashlib.sha256(written).hexdigest() != digest:
        fail("output sha256 mismatch for %s" % dest_path)

    print("OK: %s" % dest_path)
    print("bytes: %d" % len(data))
    print("sha256: %s" % digest)
    print("dimensions: %dx%d" % (width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
