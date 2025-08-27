from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from ..database import Base
import enum

class AuditorRole(enum.Enum):
    junior = "junior"
    senior = "senior"
    expert = "expert"
    committee = "committee"

class AuditorStatus(enum.Enum):
    active = "active"
    inactive = "inactive"

class Auditor(Base):
    __tablename__ = "auditors"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(50), nullable=False)
    role = Column(Enum(AuditorRole), nullable=False)
    department = Column(String(100), comment="部门")
    phone = Column(String(20), comment="联系电话")
    status = Column(Enum(AuditorStatus), default=AuditorStatus.active)
    created_at = Column(DateTime, default=func.now())
