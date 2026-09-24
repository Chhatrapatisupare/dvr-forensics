from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RecoveryArtifact:
    artifact_id: str
    evidence_id: str
    recording_id: str
    output_path: str
    sha256: str
    size_bytes: int
    status: str
    method: str
    confidence: str
