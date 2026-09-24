from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Recording:
    id: str
    camera: str
    channel: int
    start_time: datetime
    end_time: datetime
    status: str
    format: str

    @property
    def duration_seconds(self) -> float:
        return (self.end_time - self.start_time).total_seconds()