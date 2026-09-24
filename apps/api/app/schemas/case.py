from pydantic import BaseModel


class CaseCreate(BaseModel):
    case_number: str
    title: str
    description: str | None = None


class CaseResponse(BaseModel):
    id: str
    case_number: str
    title: str
    description: str | None
    status: str

    model_config = {
        "from_attributes": True
    }
