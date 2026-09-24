from pydantic import BaseModel


class EvidenceImportRequest(BaseModel):
    evidence_path: str


class EvidenceResponse(BaseModel):
    id: str
    case_id: str
    filename: str
    source_path: str
    source_type: str
    size_bytes: int
    sha256: str
    status: str
    vendor: str | None

    model_config = {
        "from_attributes": True
    }
