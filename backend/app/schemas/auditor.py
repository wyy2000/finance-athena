from pydantic import BaseModel
from typing import Optional
from ..models.auditor import AuditorRole

class AuditorLogin(BaseModel):
    username: str
    password: str

class AuditorResponse(BaseModel):
    id: int
    username: str
    name: str
    role: AuditorRole
    department: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
