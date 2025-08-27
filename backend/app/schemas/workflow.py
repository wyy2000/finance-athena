from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ..models.workflow import AuditLevel, AuditStatus

class AuditRequest(BaseModel):
    customer_id: int
    audit_status: AuditStatus
    audit_opinion: Optional[str] = None

class AuditResponse(BaseModel):
    code: int = 200
    message: str
    data: Optional[Dict[str, Any]] = None

class WorkflowResponse(BaseModel):
    code: int = 200
    data: Dict[str, Any]

class PendingItem(BaseModel):
    customer_id: int
    customer_name: str
    application_id: str
    investment_amount: float
    risk_level: str
    submitted_at: str
    priority: str

class WorkflowData(BaseModel):
    pending_count: int
    approved_count: int
    need_review_count: int
    total_investment: float
    pending_list: List[PendingItem]
