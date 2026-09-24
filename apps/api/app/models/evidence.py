from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String, primary_key=True)

    case_id = Column(
        String,
        nullable=False,
        index=True,
    )

    filename = Column(
        String,
        nullable=False,
    )

    source_path = Column(
        String,
        nullable=False,
    )

    source_type = Column(
        String,
        nullable=False,
        default="disk_image",
    )

    size_bytes = Column(
        Integer,
        nullable=False,
    )

    sha256 = Column(
        String(64),
        nullable=False,
    )

    status = Column(
        String,
        nullable=False,
        default="IMPORTED",
    )

    vendor = Column(
        String,
        nullable=True,
    )

    imported_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
