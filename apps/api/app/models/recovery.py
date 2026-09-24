from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class RecoveryArtifactRecord(Base):
    __tablename__ = "recovery_artifacts"

    id = Column(String, primary_key=True)
    evidence_id = Column(String, nullable=False, index=True)
    recording_id = Column(String, nullable=False, index=True)
    output_path = Column(String, nullable=False)
    sha256 = Column(String(64), nullable=False)
    size_bytes = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    method = Column(String, nullable=False)
    confidence = Column(String, nullable=False)
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )