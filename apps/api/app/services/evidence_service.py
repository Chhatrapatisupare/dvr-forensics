from __future__ import annotations

from pathlib import Path

from packages.adapters.registry import AdapterRegistry
from packages.core.evidence.source import EvidenceSource
from packages.forensics.hashing.sha256 import calculate_sha256


class EvidenceService:
    """
    Coordinates evidence hashing and vendor detection.
    """

    def __init__(self) -> None:
        self.registry = AdapterRegistry()

    def create_source(
        self,
        evidence_id: str,
        evidence_path: str | Path,
    ) -> EvidenceSource:

        path = Path(evidence_path)

        if not path.is_file():
            raise FileNotFoundError(
                f"Evidence file not found: {path}"
            )

        sha256 = calculate_sha256(path)

        return EvidenceSource(
            evidence_id=evidence_id,
            path=path,
            sha256=sha256,
            size_bytes=path.stat().st_size,
        )

    def detect_vendor(
        self,
        source: EvidenceSource,
    ) -> str | None:

        adapter = self.registry.detect(source.path)

        if adapter is None:
            return None

        return adapter.name

    def inspect(
        self,
        source: EvidenceSource,
    ) -> dict:

        adapter = self.registry.detect(source.path)

        if adapter is None:
            raise ValueError(
                "No compatible vendor adapter detected."
            )

        return {
            "adapter": adapter.name,
            "adapter_version": adapter.version,
            "metadata": adapter.inspect(source.path),
            "recordings": adapter.list_recordings(source.path),
        }