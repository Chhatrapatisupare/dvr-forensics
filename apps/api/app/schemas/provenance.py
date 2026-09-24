from pydantic import BaseModel


class ProvenanceNode(BaseModel):
    id: str
    type: str
    label: str
    metadata: dict = {}


class ProvenanceEdge(BaseModel):
    source: str
    target: str
    relationship: str


class ProvenanceResponse(BaseModel):
    evidence_id: str
    nodes: list[ProvenanceNode]
    edges: list[ProvenanceEdge]