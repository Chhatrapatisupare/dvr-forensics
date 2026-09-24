from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.evidence import Evidence
from app.models.recovery import RecoveryArtifactRecord
from app.schemas.recovery import RecoveryRequest, RecoveryResponse
from app.services.custody_service import ChainOfCustodyService
from app.services.recovery_service import RecoveryService
from app.services.recording_service import RecordingService


router = APIRouter(
    prefix="/api",
    tags=["Recovery"],
)


@router.post(
    "/evidence/{evidence_id}/recover",
    response_model=RecoveryResponse,
)
def recover_recording(
    evidence_id: str,
    request: RecoveryRequest,
    db: Session = Depends(get_db),
):
    evidence = (
        db.query(Evidence)
        .filter(Evidence.id == evidence_id)
        .first()
    )

    if evidence is None:
        raise HTTPException(
            status_code=404,
            detail="Evidence not found.",
        )

    recordings = RecordingService().list_recordings(
        evidence_path=evidence.source_path,
        evidence_id=evidence.id,
        sha256=evidence.sha256,
        size_bytes=evidence.size_bytes,
    )

    recording = next(
        (
            item
            for item in recordings
            if item["id"] == request.recording_id
        ),
        None,
    )

    if recording is None:
        raise HTTPException(
            status_code=404,
            detail="Recording not found.",
        )

    if recording["status"] != "recovered":
        raise HTTPException(
            status_code=400,
            detail=(
                "This recording is not marked as recoverable "
                "in the DemoSecure fixture."
            ),
        )

    # Return the existing artifact instead of creating duplicates.
    existing = (
        db.query(RecoveryArtifactRecord)
        .filter(
            RecoveryArtifactRecord.evidence_id == evidence_id,
            RecoveryArtifactRecord.recording_id == request.recording_id,
        )
        .first()
    )

    if existing is not None:
        return existing

    output_directory = (
        Path(request.output_directory)
        if request.output_directory
        else Path("artifacts") / "recovered"
    )

    artifact = RecoveryService().recover_recording(
        evidence_id=evidence.id,
        evidence_path=evidence.source_path,
        recording_id=request.recording_id,
        output_directory=output_directory,
    )

    record = RecoveryArtifactRecord(
        id=artifact.artifact_id,
        evidence_id=artifact.evidence_id,
        recording_id=artifact.recording_id,
        output_path=artifact.output_path,
        sha256=artifact.sha256,
        size_bytes=artifact.size_bytes,
        status=artifact.status,
        method=artifact.method,
        confidence=artifact.confidence,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    ChainOfCustodyService().add_event(
        db=db,
        case_id=evidence.case_id,
        evidence_id=evidence.id,
        action="RECOVERED",
        description=(
            f"Synthetic recovery artifact created: "
            f"{artifact.artifact_id}; "
            f"SHA-256: {artifact.sha256}"
        ),
    )

    return record


@router.get(
    "/evidence/{evidence_id}/recovery-artifacts",
    response_model=list[RecoveryResponse],
)
def list_recovery_artifacts(
    evidence_id: str,
    db: Session = Depends(get_db),
):
    evidence = (
        db.query(Evidence)
        .filter(Evidence.id == evidence_id)
        .first()
    )

    if evidence is None:
        raise HTTPException(
            status_code=404,
            detail="Evidence not found.",
        )

    return (
        db.query(RecoveryArtifactRecord)
        .filter(
            RecoveryArtifactRecord.evidence_id == evidence_id
        )
        .order_by(RecoveryArtifactRecord.created_at.asc())
        .all()
    )