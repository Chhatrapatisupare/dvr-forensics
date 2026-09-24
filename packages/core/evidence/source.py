from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class EvidenceSource:
    """
    Represents a forensic evidence source.

    The original evidence is treated as read-only.
    """

    evidence_id: str
    path: Path
    sha256: str
    size_bytes: int
    source_type: str = "disk_image"

    @property
    def exists(self) -> bool:
        return self.path.is_file()

    def verify_size(self) -> bool:
        """
        Verify that the evidence file size has not changed.
        """
        return self.path.stat().st_size == self.size_bytes