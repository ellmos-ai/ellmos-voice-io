#!/usr/bin/env python3
"""Normalize tar.gz metadata so repeated sdist builds become byte-reproducible."""

from __future__ import annotations

import argparse
import copy
import glob
import gzip
import hashlib
import io
import os
import tarfile
import tempfile
from pathlib import Path


def normalized_sdist_bytes(path: Path, epoch: int) -> bytes:
    entries: list[tuple[tarfile.TarInfo, bytes | None]] = []
    with tarfile.open(path, "r:gz") as source:
        for member in source.getmembers():
            payload: bytes | None = None
            if member.isfile():
                extracted = source.extractfile(member)
                if extracted is None:
                    raise RuntimeError(f"could not read archive member: {member.name}")
                payload = extracted.read()
            entries.append((member, payload))

    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w", format=tarfile.PAX_FORMAT) as target:
        for original, payload in entries:
            member = copy.copy(original)
            member.mtime = epoch
            member.uid = 0
            member.gid = 0
            member.uname = ""
            member.gname = ""
            member.pax_headers = {}
            target.addfile(member, io.BytesIO(payload) if payload is not None else None)

    gzip_buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=gzip_buffer, mtime=epoch) as compressed:
        compressed.write(tar_buffer.getvalue())
    return gzip_buffer.getvalue()


def normalize_sdist(path: Path, epoch: int) -> str:
    normalized = normalized_sdist_bytes(path, epoch)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False) as tmp:
        temporary_path = Path(tmp.name)
        tmp.write(normalized)
        tmp.flush()
        os.fsync(tmp.fileno())
    try:
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)
    return hashlib.sha256(normalized).hexdigest()


def _expand_paths(raw_paths: list[str]) -> list[Path]:
    expanded: list[Path] = []
    for raw in raw_paths:
        matches = [Path(match) for match in glob.glob(raw)]
        expanded.extend(matches or [Path(raw)])
    return expanded


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="sdist .tar.gz path(s); shell-style globs are accepted")
    parser.add_argument(
        "--epoch",
        type=int,
        default=int(os.environ.get("SOURCE_DATE_EPOCH", "0")),
        help="canonical Unix timestamp (default: SOURCE_DATE_EPOCH)",
    )
    args = parser.parse_args()
    if args.epoch <= 0:
        parser.error("--epoch or a positive SOURCE_DATE_EPOCH is required")

    paths = _expand_paths(args.paths)
    for path in paths:
        if not path.is_file() or not path.name.endswith(".tar.gz"):
            parser.error(f"not an sdist tar.gz file: {path}")
        digest = normalize_sdist(path, args.epoch)
        print(f"{digest}  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
