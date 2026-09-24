from __future__ import annotations

import hashlib
import shutil
from pathlib import Path
from uuid import uuid4

from packages.core.evidence.recovery import RecoveryArtifact


class RecoveryService:
    """
    Synthetic/demo recovery engine.

    This implementation never modifies the original evidence.
    It creates a separate artifact representing a recovered
    recording from the deterministic DemoSecure fixture.
    """

    def recover_recording(
        self,
        evidence_id: str,
        evidence_path: str,
        recording_id: str,
        output_directory: str | Path,
    ) -> RecoveryArtifact:

        source = Path(evidence_path)

        if not source.is_file():
            raise FileNotFoundError(
                f"Evidence file not found: {source}"
            )

        output_dir = Path(output_directory)
        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        artifact_id = (
            f"ARTIFACT-{uuid4().hex[:12].upper()}"
        )

        output_path = (
            output_dir
            / f"{recording_id}_recovered.txt"
        )

        # Synthetic recovery artifact.
        # The original evidence is opened read-only and copied
        # into a separate derived artifact.
        source_bytes = source.read_bytes()

        recovered_marker = (
            f"\n\n"
            f"=== SYNTHETIC RECOVERY ===\n"
            f"Recording: {recording_id}\n"
            f"Evidence: {evidence_id}\n"
            f"Method: DemoSecure synthetic recovery\n"
            f"=== END SYNTHETIC RECOVERY ===\n"
        ).encode("utf-8")

        output_path.write_bytes(
            source_bytes + recovered_marker
        )

        digest = hashlib.sha256()

        with output_path.open("rb") as artifact_file:
            while chunk := artifact_file.read(
                1024 * 1024
            ):
                digest.update(chunk)

        return RecoveryArtifact(
            artifact_id=artifact_id,
            evidence_id=evidence_id,
            recording_id=recording_id,
            output_path=str(
                output_path.resolve()
            ),
            sha256=digest.hexdigest(),
            size_bytes=output_path.stat().st_size,
            status="RECOVERED",
            method="DemoSecure synthetic recovery",
            confidence="DEMO",
        )
