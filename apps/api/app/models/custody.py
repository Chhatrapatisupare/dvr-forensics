from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class ChainOfCustodyEvent(Base):
    __tablename__ = "chain_of_custody"

    id = Column(Integer, primary_key=True, autoincrement=True)

    case_id = Column(
        String,
        nullable=False,
        index=True,
    )

    evidence_id = Column(
        String,
        nullable=False,
        index=True,
    )

    action = Column(
        String,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    timestamp = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    previous_hash = Column(
        String(64),
        nullable=True,
    )

    event_hash = Column(
        String(64),
        nullable=False,
    )
