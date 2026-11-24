#!/usr/bin/env python3
"""news-image-20261124 entry (Python 3.13, standard library only).

The entry image is the pre-rendered entry.png beside this file (drawn by
draw.py). This program only copies it to the output directory and verifies
the copy is byte-identical to the source, so two runs always write the
same bytes. It renders nothing.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dst = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(src):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)

    if os.path.getsize(dst) == 0:
        print("error: copied entry.png is empty", file=sys.stderr)
        return 1
    if _sha256(src) != _sha256(dst):
        print("error: copied entry.png differs from the source", file=sys.stderr)
        return 1

    print("wrote", dst, "(" + _sha256(dst)[:12] + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
