from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from decimal import Decimal
from ..models.customer import RiskLevel, CustomerStatus

class AssessmentData(BaseModel):
    age: str
    income: str
    experience: str
    risk_tolerance: str
    goal: str
    period: str

class CustomerCreate(BaseModel):
    name: str
    phone: str
    id_card: str
    email: Optional[str] = None
    occupation: Optional[str] = None
    investment_amount: Decimal
    assessment_data: AssessmentData

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    id_card: str
    email: Optional[str] = None
    occupation: Optional[str] = None
    investment_amount: Decimal
    age_range: Optional[str] = None
    income_level: Optional[str] = None
    investment_experience: Optional[str] = None
    risk_tolerance: Optional[str] = None
    investment_goal: Optional[str] = None
    investment_period: Optional[str] = None
    risk_score: int
    risk_level: Optional[RiskLevel] = None
    status: CustomerStatus
    created_at: str

    class Config:
        from_attributes = True

class CustomerRegisterResponse(BaseModel):
    code: int = 200
    message: str
    data: Dict[str, Any]
