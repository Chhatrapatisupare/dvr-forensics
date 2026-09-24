from pydantic import BaseModel, ConfigDict


class EvidenceResponse(BaseModel):
    """
    Public API representation of a forensic evidence item.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    case_id: str
    filename: str
    source_path: str
    source_type: str
    size_bytes: int
    sha256: str
    status: str
    vendor: str | None = None


class EvidenceImportRequest(BaseModel):
    """
    Request payload for importing a disk image or evidence file.
    """

    evidence_path: str


class EvidenceCreate(BaseModel):
    """
    Request schema for registering new evidence.
    """

    filename: str
    source_path: str
    source_type: str
    size_bytes: int
    sha256: str
    vendor: str | None = None


class EvidenceSummary(BaseModel):
    """
    Lightweight evidence information for dashboard/list views.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    source_type: str
    size_bytes: int
    sha256: str
    status: str
    vendor: str | None = None