#!/usr/bin/env python3
"""Copy entry.png to /output/entry.png byte-for-byte and verify the result."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "entry.png"
DEST_DIR = Path("/output")
DEST = DEST_DIR / "entry.png"


def main():
    data = SOURCE.read_bytes()
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(data)

    written = DEST.read_bytes()
    if written != data:
        raise RuntimeError(
            f"verification failed: {SOURCE} ({len(data)} bytes) != {DEST} ({len(written)} bytes)"
        )

    print(f"wrote {len(data)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
