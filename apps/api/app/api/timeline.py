from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.evidence import Evidence
from app.schemas.timeline import TimelineEventResponse
from app.services.recording_service import RecordingService
from app.services.timeline_service import TimelineService


router = APIRouter(
    prefix="/api",
    tags=["Timeline"],
)


@router.get(
    "/evidence/{evidence_id}/timeline",
    response_model=list[TimelineEventResponse],
)
def get_timeline(
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
        recordings = RecordingService().list_recordings(
            evidence_path=evidence.source_path,
            evidence_id=evidence.id,
            sha256=evidence.sha256,
            size_bytes=evidence.size_bytes,
        )

        events = TimelineService().build_timeline(
            recordings
        )

        return [
            {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "timestamp": event.timestamp,
                "end_time": event.end_time,
                "camera": event.camera,
                "channel": event.channel,
                "status": event.status,
                "description": event.description,
                "source_recording_id": (
                    event.source_recording_id
                ),
                "duration_seconds": (
                    event.duration_seconds
                ),
            }
            for event in events
        ]

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
