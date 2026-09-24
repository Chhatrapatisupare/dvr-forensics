from __future__ import annotations

from datetime import datetime, timezone

from packages.core.timeline.event import TimelineEvent


class TimelineService:
    """
    Converts normalized recording metadata into a
    chronological forensic timeline.

    All timeline timestamps are normalized to UTC.
    """

    @staticmethod
    def _to_utc(value: datetime | str) -> datetime:
        if isinstance(value, str):
            value = datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )

        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)

    def build_timeline(
        self,
        recordings: list[dict],
    ) -> list[TimelineEvent]:

        events: list[TimelineEvent] = []

        for recording in recordings:
            start_time = self._to_utc(
                recording["start_time"]
            )

            end_time = self._to_utc(
                recording["end_time"]
            )

            status = recording.get(
                "status",
                "unverified",
            )

            event = TimelineEvent(
                event_id=f"TIMELINE-{recording['id']}",
                event_type="RECORDING",
                timestamp=start_time,
                end_time=end_time,
                camera=recording.get("camera"),
                channel=recording.get("channel"),
                status=status,
                description=(
                    f"Recording {recording['id']} "
                    f"from {recording.get('camera')} "
                    f"channel {recording.get('channel')}"
                ),
                source_recording_id=recording["id"],
            )

            events.append(event)

        events.sort(
            key=lambda event: event.timestamp
        )

        return events
