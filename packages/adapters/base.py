from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class VendorAdapter(ABC):
    """
    Base interface for all DVR/NVR vendor adapters.

    Each vendor-specific adapter must implement detection
    and metadata/recording parsing.
    """

    name: str = "Unknown"
    version: str = "0.1.0"

    @abstractmethod
    def detect(self, evidence_path: Path) -> bool:
        """
        Determine whether this adapter understands the evidence.
        """
        raise NotImplementedError

    @abstractmethod
    def inspect(self, evidence_path: Path) -> dict[str, Any]:
        """
        Read forensic metadata from the evidence.
        """
        raise NotImplementedError

    @abstractmethod
    def list_recordings(
        self,
        evidence_path: Path,
    ) -> list[dict[str, Any]]:
        """
        Return normalized recording metadata.
        """
        raise NotImplementedError