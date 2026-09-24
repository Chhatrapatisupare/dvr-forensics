from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.custody import ChainOfCustodyEvent


class ChainOfCustodyService:
    """
    Creates and verifies a cryptographically linked
    chain of custody for forensic evidence.
    """

    @staticmethod
    def _canonical_timestamp(timestamp: datetime) -> str:
        """
        Convert timestamps into one deterministic UTC representation.

        SQLite/SQLAlchemy may return datetime values without timezone
        information, so verification must normalize them consistently.
        """

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        timestamp = timestamp.astimezone(timezone.utc)

        return timestamp.isoformat()

    @staticmethod
    def _calculate_event_hash(
        case_id: str,
        evidence_id: str,
        action: str,
        description: str,
        timestamp: str,
        previous_hash: str | None,
    ) -> str:

        payload = {
            "case_id": case_id,
            "evidence_id": evidence_id,
            "action": action,
            "description": description,
            "timestamp": timestamp,
            "previous_hash": previous_hash,
        }

        canonical_data = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        )

        return hashlib.sha256(
            canonical_data.encode("utf-8")
        ).hexdigest()

    def add_event(
        self,
        db: Session,
        case_id: str,
        evidence_id: str,
        action: str,
        description: str,
    ) -> ChainOfCustodyEvent:

        previous_event = (
            db.query(ChainOfCustodyEvent)
            .filter(
                ChainOfCustodyEvent.case_id == case_id,
                ChainOfCustodyEvent.evidence_id == evidence_id,
            )
            .order_by(ChainOfCustodyEvent.id.desc())
            .first()
        )

        previous_hash = (
            previous_event.event_hash
            if previous_event
            else None
        )

        timestamp = datetime.now(timezone.utc)

        canonical_timestamp = self._canonical_timestamp(
            timestamp
        )

        event_hash = self._calculate_event_hash(
            case_id=case_id,
            evidence_id=evidence_id,
            action=action,
            description=description,
            timestamp=canonical_timestamp,
            previous_hash=previous_hash,
        )

        event = ChainOfCustodyEvent(
            case_id=case_id,
            evidence_id=evidence_id,
            action=action,
            description=description,
            timestamp=timestamp,
            previous_hash=previous_hash,
            event_hash=event_hash,
        )

        db.add(event)
        db.commit()
        db.refresh(event)

        return event

    def verify_chain(
        self,
        db: Session,
        case_id: str,
        evidence_id: str,
    ) -> bool:

        events = (
            db.query(ChainOfCustodyEvent)
            .filter(
                ChainOfCustodyEvent.case_id == case_id,
                ChainOfCustodyEvent.evidence_id == evidence_id,
            )
            .order_by(ChainOfCustodyEvent.id.asc())
            .all()
        )

        expected_previous_hash = None

        for event in events:

            canonical_timestamp = self._canonical_timestamp(
                event.timestamp
            )

            expected_hash = self._calculate_event_hash(
                case_id=event.case_id,
                evidence_id=event.evidence_id,
                action=event.action,
                description=event.description,
                timestamp=canonical_timestamp,
                previous_hash=expected_previous_hash,
            )

            if event.previous_hash != expected_previous_hash:
                return False

            if event.event_hash != expected_hash:
                return False

            expected_previous_hash = event.event_hash

        return True
    def get_events(
        self,
        db: Session,
        case_id: str,
        evidence_id: str,
    ) -> list[dict]:

        events = (
            db.query(ChainOfCustodyEvent)
            .filter(
                ChainOfCustodyEvent.case_id == case_id,
                ChainOfCustodyEvent.evidence_id == evidence_id,
            )
            .order_by(ChainOfCustodyEvent.id.asc())
            .all()
        )

        return [
            {
                "id": event.id,
                "action": event.action,
                "description": event.description,
                "timestamp": event.timestamp.isoformat(),
                "previous_hash": event.previous_hash,
                "event_hash": event.event_hash,
            }
            for event in events
        ]
