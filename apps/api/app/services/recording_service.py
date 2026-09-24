from __future__ import annotations

from datetime import datetime
from pathlib import Path

from packages.core.evidence.source import EvidenceSource
from packages.adapters.registry import AdapterRegistry


class RecordingService:
    def list_recordings(
        self,
        evidence_path: str,
        evidence_id: str,
        sha256: str,
        size_bytes: int,
    ):
        path = Path(evidence_path)

        if not path.is_file():
            raise FileNotFoundError(
                f"Evidence file not found: {path}"
            )

        source = EvidenceSource(
            evidence_id=evidence_id,
            path=path,
            sha256=sha256,
            size_bytes=size_bytes,
            source_type="disk_image",
        )

        registry = AdapterRegistry()
        adapter = registry.detect(source.path)

        if adapter is None:
            raise ValueError(
                "No supported vendor adapter detected."
            )

        # VendorAdapter contract expects Path.
        recordings = adapter.list_recordings(source.path)

        result = []

        for recording in recordings:
            start_time = datetime.fromisoformat(
                recording["start_time"].replace("Z", "+00:00")
            )
            end_time = datetime.fromisoformat(
                recording["end_time"].replace("Z", "+00:00")
            )

            result.append(
                {
                    "id": recording["id"],
                    "camera": recording["camera"],
                    "channel": recording["channel"],
                    "start_time": start_time,
                    "end_time": end_time,
                    "status": recording["status"],
                    "format": recording["format"],
                    "duration_seconds": (
                        end_time - start_time
                    ).total_seconds(),
                }
            )

        return result
