from datetime import datetime

from pydantic import BaseModel


class RecordingResponse(BaseModel):
    id: str
    camera: str
    channel: int
    start_time: datetime
    end_time: datetime
    status: str
    format: str
    duration_seconds: float