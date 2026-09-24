from datetime import datetime

from pydantic import BaseModel


class TimelineEventResponse(BaseModel):
    event_id: str
    event_type: str
    timestamp: datetime
    end_time: datetime | None
    camera: str | None
    channel: int | None
    status: str
    description: str
    source_recording_id: str | None
    duration_seconds: float | None
