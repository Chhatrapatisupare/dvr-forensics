from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TimelineEvent:
    event_id: str
    event_type: str
    timestamp: datetime
    end_time: datetime | None
    camera: str | None
    channel: int | None
    status: str
    description: str
    source_recording_id: str | None = None

    @property
    def duration_seconds(self) -> float | None:
        if self.end_time is None:
            return None

        return (self.end_time - self.timestamp).total_seconds()
