from pydantic import BaseModel


class RecoveryRequest(BaseModel):
    recording_id: str


class RecoveryResponse(BaseModel):
    id: str
    evidence_id: str
    recording_id: str
    output_path: str
    sha256: str
    size_bytes: int
    status: str
    method: str
    confidence: str

    model_config = {
        "from_attributes": True
    }