from pydantic import BaseModel
from typing import Optional


class StartVerificationRequest(BaseModel):
    phone_number: str
    payload: Optional[str]


class StartVerificationResponse(BaseModel):
    status: str
    request_id: Optional[str]


class VerifyRequest(BaseModel):
    phone_number: str
    code: str


class SimpleResponse(BaseModel):
    status: str
    message: str | None = None


