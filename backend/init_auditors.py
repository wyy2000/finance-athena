#!/usr/bin/env python3
"""
初始化审核员数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.auditor import Auditor, AuditorRole, AuditorStatus
from app.utils.auth import get_password_hash

def init_auditors():
    """初始化审核员数据"""
    db = SessionLocal()
    
    try:
        # 检查是否已有审核员
        existing_auditor = db.query(Auditor).first()
        if existing_auditor:
            print("✅ 审核员数据已存在")
            return
        
        # 创建审核员
        auditors = [
            {
                "username": "junior1",
                "password": "password123",
                "name": "初级审核员1",
                "role": AuditorRole.junior,
                "department": "风险审核部",
                "phone": "13800138001"
            },
            {
                "username": "senior1", 
                "password": "password123",
                "name": "中级审核员1",
                "role": AuditorRole.senior,
                "department": "风险审核部", 
                "phone": "13800138002"
            },
            {
                "username": "expert1",
                "password": "password123", 
                "name": "高级审核员1",
                "role": AuditorRole.expert,
                "department": "风险审核部",
                "phone": "13800138003"
            },
            {
                "username": "committee1",
                "password": "password123",
                "name": "投资委员会1", 
                "role": AuditorRole.committee,
                "department": "投资委员会",
                "phone": "13800138004"
            }
        ]
        
        for auditor_data in auditors:
            auditor = Auditor(
                username=auditor_data["username"],
                password_hash=get_password_hash(auditor_data["password"]),
                name=auditor_data["name"],
                role=auditor_data["role"],
                department=auditor_data["department"],
                phone=auditor_data["phone"],
                status=AuditorStatus.active
            )
            db.add(auditor)
        
        db.commit()
        print("✅ 审核员数据初始化完成")
        print("👥 创建的审核员账号：")
        for auditor_data in auditors:
            print(f"   用户名: {auditor_data['username']}, 密码: {auditor_data['password']}")
            
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_auditors()
