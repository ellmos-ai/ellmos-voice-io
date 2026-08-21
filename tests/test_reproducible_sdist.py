import gzip
import hashlib
import io
import tarfile
from pathlib import Path

from tools.normalize_sdist import normalize_sdist


def _write_sdist(path: Path, *, member_mtime: int, gzip_mtime: int) -> None:
    tar_buffer = io.BytesIO()
    payload = b"same package payload"
    with tarfile.open(fileobj=tar_buffer, mode="w") as archive:
        member = tarfile.TarInfo("example-1.0/PKG-INFO")
        member.size = len(payload)
        member.mtime = member_mtime
        archive.addfile(member, io.BytesIO(payload))
    with path.open("wb") as output:
        with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=gzip_mtime) as compressed:
            compressed.write(tar_buffer.getvalue())


def test_normalizer_makes_timestamp_variant_sdists_byte_identical(tmp_path: Path):
    first = tmp_path / "first.tar.gz"
    second = tmp_path / "second.tar.gz"
    _write_sdist(first, member_mtime=100, gzip_mtime=200)
    _write_sdist(second, member_mtime=300, gzip_mtime=400)

    first_digest = normalize_sdist(first, epoch=1_787_270_400)
    second_digest = normalize_sdist(second, epoch=1_787_270_400)

    assert first_digest == second_digest
    assert first.read_bytes() == second.read_bytes()
    assert hashlib.sha256(first.read_bytes()).hexdigest() == first_digest
