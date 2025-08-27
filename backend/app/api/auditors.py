from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.auditor import Auditor
from ..schemas.auditor import AuditorLogin, TokenResponse
from ..utils.auth import authenticate_auditor, create_access_token, get_current_auditor
from datetime import timedelta

router = APIRouter(prefix="/api/v1/auditors", tags=["auditors"])

@router.post("/login", response_model=TokenResponse)
async def login_auditor(
    auditor_data: AuditorLogin,
    db: Session = Depends(get_db)
):
    """审核员登录"""
    auditor = authenticate_auditor(db, auditor_data.username, auditor_data.password)
    if not auditor:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": auditor.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def get_current_auditor_info(current_auditor: Auditor = Depends(get_current_auditor)):
    """获取当前审核员信息"""
    return {
        "id": current_auditor.id,
        "username": current_auditor.username,
        "name": current_auditor.name,
        "role": current_auditor.role.value,
        "department": current_auditor.department,
        "phone": current_auditor.phone
    }
