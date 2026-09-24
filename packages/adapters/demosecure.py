from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from packages.adapters.base import VendorAdapter


class DemoSecureAdapter(VendorAdapter):
    """
    Working synthetic/reference adapter.

    This adapter is intentionally limited to the deterministic
    DemoSecure fixture generated for development and testing.
    """

    name = "DemoSecure"
    version = "1.0.0"

    MAGIC = "DEMOSECURE-DVR-IMAGE"

    def _read_metadata(self, evidence_path: Path) -> dict[str, Any]:
        if not evidence_path.is_file():
            raise FileNotFoundError(
                f"Evidence file not found: {evidence_path}"
            )

        content = evidence_path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        start_marker = "=== DEMOSECURE FORENSIC FIXTURE ==="
        end_marker = "=== END DEMOSECURE FIXTURE ==="

        if start_marker not in content:
            raise ValueError(
                "DemoSecure fixture header not found."
            )

        start = content.index(start_marker) + len(start_marker)

        if end_marker in content:
            end = content.index(end_marker)
            json_text = content[start:end].strip()
        else:
            json_text = content[start:].strip()

        return json.loads(json_text)

    def detect(self, evidence_path: Path) -> bool:
        if not evidence_path.is_file():
            return False

        with evidence_path.open(
            "rb",
        ) as evidence_file:
            header = evidence_file.read(256)

        return self.MAGIC.encode("utf-8") in header

    def inspect(self, evidence_path: Path) -> dict[str, Any]:
        metadata = self._read_metadata(evidence_path)

        return {
            "vendor": metadata.get("vendor"),
            "model": metadata.get("model"),
            "firmware": metadata.get("firmware"),
            "filesystem": metadata.get("filesystem"),
            "timezone": metadata.get("timezone"),
            "channels": metadata.get("channels"),
        }

    def list_recordings(
        self,
        evidence_path: Path,
    ) -> list[dict[str, Any]]:
        metadata = self._read_metadata(evidence_path)

        recordings = metadata.get("recordings", [])

        normalized = []

        for recording in recordings:
            normalized.append(
                {
                    "id": recording.get("id"),
                    "camera": recording.get("camera"),
                    "channel": recording.get("channel"),
                    "start_time": recording.get("start_time"),
                    "end_time": recording.get("end_time"),
                    "status": recording.get("status"),
                    "format": recording.get("format"),
                    "vendor": self.name,
                }
            )

        return normalized