from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String, Text

from app.database import Base


class ForensicCase(Base):
    __tablename__ = "cases"

    id = Column(String, primary_key=True)
    case_number = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    status = Column(
        String,
        nullable=False,
        default="OPEN",
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
