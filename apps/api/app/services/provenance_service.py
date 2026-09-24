from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.evidence import Evidence
from app.models.recovery import RecoveryArtifactRecord
from app.services.recording_service import RecordingService


class ProvenanceService:

    def build_graph(
        self,
        db: Session,
        evidence_id: str,
    ) -> dict:

        evidence = (
            db.query(Evidence)
            .filter(Evidence.id == evidence_id)
            .first()
        )

        if evidence is None:
            raise ValueError("Evidence not found.")

        nodes = []
        edges = []

        # -------------------------------------------------
        # Evidence node
        # -------------------------------------------------

        nodes.append(
            {
                "id": evidence.id,
                "type": "evidence",
                "label": evidence.filename,
                "metadata": {
                    "sha256": evidence.sha256,
                    "size_bytes": evidence.size_bytes,
                    "vendor": evidence.vendor,
                    "status": evidence.status,
                },
            }
        )

        # -------------------------------------------------
        # Recording nodes
        # -------------------------------------------------

        recordings = RecordingService().list_recordings(
            evidence_path=evidence.source_path,
            evidence_id=evidence.id,
            sha256=evidence.sha256,
            size_bytes=evidence.size_bytes,
        )

        recording_ids = set()

        for recording in recordings:

            recording_id = recording["id"]
            recording_ids.add(recording_id)

            nodes.append(
                {
                    "id": recording_id,
                    "type": "recording",
                    "label": (
                        f'{recording["camera"]} / '
                        f'{recording_id}'
                    ),
                    "metadata": {
                        "camera": recording["camera"],
                        "channel": recording["channel"],
                        "start_time": recording["start_time"].isoformat(),
                        "end_time": recording["end_time"].isoformat(),
                        "status": recording["status"],
                        "format": recording["format"],
                        "duration_seconds": (
                            recording["duration_seconds"]
                        ),
                    },
                }
            )

            edges.append(
                {
                    "source": evidence.id,
                    "target": recording_id,
                    "relationship": "CONTAINS",
                }
            )

        # -------------------------------------------------
        # Recovery artifact nodes
        # -------------------------------------------------

        artifacts = (
            db.query(RecoveryArtifactRecord)
            .filter(
                RecoveryArtifactRecord.evidence_id == evidence_id
            )
            .all()
        )

        for artifact in artifacts:

            nodes.append(
                {
                    "id": artifact.id,
                    "type": "artifact",
                    "label": artifact.output_path,
                    "metadata": {
                        "recording_id": artifact.recording_id,
                        "sha256": artifact.sha256,
                        "size_bytes": artifact.size_bytes,
                        "status": artifact.status,
                        "method": artifact.method,
                        "confidence": artifact.confidence,
                        "created_at": (
                            artifact.created_at.isoformat()
                            if artifact.created_at
                            else None
                        ),
                    },
                }
            )

            if artifact.recording_id in recording_ids:
                edges.append(
                    {
                        "source": artifact.recording_id,
                        "target": artifact.id,
                        "relationship": "RECOVERED_AS",
                    }
                )

        return {
            "evidence_id": evidence_id,
            "nodes": nodes,
            "edges": edges,
        }