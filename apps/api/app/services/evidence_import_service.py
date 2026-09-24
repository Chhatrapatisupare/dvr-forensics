from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.evidence import Evidence
from app.services.custody_service import ChainOfCustodyService
from app.services.evidence_service import EvidenceService
from packages.core.evidence.source import EvidenceSource
from packages.forensics.hashing.sha256 import calculate_sha256


class EvidenceImportService:

    def __init__(self):
        self.custody_service = ChainOfCustodyService()
        self.evidence_service = EvidenceService()

    def import_evidence(
        self,
        db: Session,
        case_id: str,
        evidence_path: str | Path,
    ) -> Evidence:

        path = Path(evidence_path)

        if not path.is_file():
            raise FileNotFoundError(
                f"Evidence file not found: {path}"
            )

        evidence_id = f"EVIDENCE-{uuid4().hex[:12].upper()}"

        # ---------------------------------------------------------
        # 1. Calculate SHA-256 without modifying the source
        # ---------------------------------------------------------
        sha256 = calculate_sha256(path)

        size_bytes = path.stat().st_size

        # ---------------------------------------------------------
        # 2. Build the core EvidenceSource object
        # ---------------------------------------------------------
        source = EvidenceSource(
            evidence_id=evidence_id,
            path=path,
            sha256=sha256,
            size_bytes=size_bytes,
            source_type="disk_image",
        )

        # ---------------------------------------------------------
        # 3. Create database evidence record
        # ---------------------------------------------------------
        evidence = Evidence(
            id=evidence_id,
            case_id=case_id,
            filename=path.name,
            source_path=str(path.resolve()),
            source_type="disk_image",
            size_bytes=size_bytes,
            sha256=sha256,
            status="HASHED",
        )

        db.add(evidence)
        db.commit()
        db.refresh(evidence)

        # ---------------------------------------------------------
        # 4. Chain of custody: IMPORTED
        # ---------------------------------------------------------
        self.custody_service.add_event(
            db=db,
            case_id=case_id,
            evidence_id=evidence_id,
            action="IMPORTED",
            description=(
                f"Evidence image imported: {path.name}. "
                "Original source was opened read-only."
            ),
        )

        # ---------------------------------------------------------
        # 5. Chain of custody: HASHED
        # ---------------------------------------------------------
        self.custody_service.add_event(
            db=db,
            case_id=case_id,
            evidence_id=evidence_id,
            action="HASHED",
            description=f"SHA-256 calculated: {sha256}",
        )

        # ---------------------------------------------------------
        # 6. Detect vendor through AdapterRegistry
        # ---------------------------------------------------------
        vendor = self.evidence_service.detect_vendor(source)

        if vendor:
            evidence.vendor = vendor
            evidence.status = "DETECTED"

            db.commit()
            db.refresh(evidence)

            # -----------------------------------------------------
            # 7. Chain of custody: DETECTED
            # -----------------------------------------------------
            self.custody_service.add_event(
                db=db,
                case_id=case_id,
                evidence_id=evidence_id,
                action="DETECTED",
                description=(
                    f"Vendor adapter detected: {vendor}"
                ),
            )

        return evidence
