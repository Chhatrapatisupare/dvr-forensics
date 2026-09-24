from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.evidence import Evidence
from app.schemas.recording import RecordingResponse
from app.services.recording_service import RecordingService


router = APIRouter(
    prefix="/api",
    tags=["Recordings"],
)


@router.get(
    "/evidence/{evidence_id}/recordings",
    response_model=list[RecordingResponse],
)
def list_recordings(
    evidence_id: str,
    db: Session = Depends(get_db),
):
    evidence = (
        db.query(Evidence)
        .filter(Evidence.id == evidence_id)
        .first()
    )

    if not evidence:
        raise HTTPException(
            status_code=404,
            detail="Evidence not found",
        )

    try:
        service = RecordingService()

        return service.list_recordings(
            evidence_path=evidence.source_path,
            evidence_id=evidence.id,
            sha256=evidence.sha256,
            size_bytes=evidence.size_bytes,
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )