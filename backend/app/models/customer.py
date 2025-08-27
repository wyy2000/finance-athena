from sqlalchemy import Column, Integer, String, DECIMAL, Enum, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class RiskLevel(enum.Enum):
    conservative = "conservative"
    moderate = "moderate"
    aggressive = "aggressive"

class CustomerStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, comment="姓名")
    phone = Column(String(20), nullable=False, unique=True, comment="手机号")
    id_card = Column(String(18), nullable=False, unique=True, comment="身份证号")
    email = Column(String(100), comment="邮箱")
    occupation = Column(String(100), comment="职业")
    investment_amount = Column(DECIMAL(15, 2), comment="投资金额")
    age_range = Column(String(20), comment="年龄范围")
    income_level = Column(String(20), comment="收入水平")
    investment_experience = Column(String(20), comment="投资经验")
    risk_tolerance = Column(String(20), comment="风险承受能力")
    investment_goal = Column(String(20), comment="投资目标")
    investment_period = Column(String(20), comment="投资期限")
    risk_score = Column(Integer, default=0, comment="风险评分")
    risk_level = Column(Enum(RiskLevel), comment="风险等级")
    status = Column(Enum(CustomerStatus), default=CustomerStatus.pending, comment="状态")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    assessments = relationship("RiskAssessment", back_populates="customer")
    advice = relationship("InvestmentAdvice", back_populates="customer")
    workflows = relationship("AuditWorkflow", back_populates="customer")
    audit_records = relationship("AuditRecord", back_populates="customer")
    notifications = relationship("Notification", back_populates="customer")
