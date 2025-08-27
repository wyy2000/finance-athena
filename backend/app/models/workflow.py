from sqlalchemy import Column, Integer, String, DECIMAL, Enum, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class AuditLevel(enum.Enum):
    junior = "junior"
    senior = "senior"
    expert = "expert"
    committee = "committee"

class AuditStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    need_review = "need_review"

class WorkflowStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    rejected = "rejected"

class NotificationType(enum.Enum):
    sms = "sms"
    email = "email"
    system = "system"

class NotificationStatus(enum.Enum):
    pending = "pending"
    sent = "sent"
    failed = "failed"

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    assessment_data = Column(JSON, comment="评估问卷数据")
    risk_score = Column(Integer, nullable=False, comment="风险评分")
    risk_level = Column(String(20), nullable=False)
    assessment_date = Column(DateTime, default=func.now())
    
    customer = relationship("Customer", back_populates="assessments")

class InvestmentAdvice(Base):
    __tablename__ = "investment_advice"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    portfolio_type = Column(String(20), nullable=False)
    expected_return_min = Column(DECIMAL(5, 2), comment="预期最低收益")
    expected_return_max = Column(DECIMAL(5, 2), comment="预期最高收益")
    portfolio_config = Column(JSON, comment="投资组合配置")
    advice_content = Column(Text, comment="投资建议内容")
    created_at = Column(DateTime, default=func.now())
    
    customer = relationship("Customer", back_populates="advice")

class AuditWorkflow(Base):
    __tablename__ = "audit_workflow"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    current_level = Column(Enum(AuditLevel), nullable=False)
    workflow_status = Column(Enum(WorkflowStatus), default=WorkflowStatus.pending)
    assigned_auditor_id = Column(Integer, ForeignKey("auditors.id"), comment="当前审核员ID")
    next_level = Column(Enum(AuditLevel), comment="下一级审核")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    customer = relationship("Customer", back_populates="workflows")
    assigned_auditor = relationship("Auditor")

class AuditRecord(Base):
    __tablename__ = "audit_records"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    auditor_id = Column(Integer, ForeignKey("auditors.id"), nullable=False)
    audit_level = Column(Enum(AuditLevel), nullable=False)
    audit_status = Column(Enum(AuditStatus), nullable=False)
    audit_opinion = Column(Text, comment="审核意见")
    audit_date = Column(DateTime, default=func.now())
    
    customer = relationship("Customer", back_populates="audit_records")
    auditor = relationship("Auditor")

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)
    title = Column(String(200), comment="通知标题")
    content = Column(Text, nullable=False, comment="通知内容")
    status = Column(Enum(NotificationStatus), default=NotificationStatus.pending)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    customer = relationship("Customer", back_populates="notifications")
