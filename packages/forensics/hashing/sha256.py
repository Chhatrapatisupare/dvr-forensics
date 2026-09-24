from __future__ import annotations

import hashlib
from pathlib import Path


def calculate_sha256(
    file_path: str | Path,
    chunk_size: int = 1024 * 1024,
) -> str:
    """
    Calculate the SHA-256 hash of a file.

    The file is opened in binary read-only mode and processed
    in chunks so large evidence files do not need to fit in RAM.
    """
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Evidence file not found: {path}")

    digest = hashlib.sha256()

    with path.open("rb") as evidence_file:
        while chunk := evidence_file.read(chunk_size):
            digest.update(chunk)

    return digest.hexdigest()