from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models.auditor import Auditor
from ..models.workflow import AuditWorkflow, AuditRecord, WorkflowStatus, AuditStatus
from ..models.customer import Customer, CustomerStatus
from ..schemas.workflow import AuditRequest, AuditResponse, WorkflowResponse
from ..services.audit_workflow import AuditWorkflowService
from ..utils.auth import get_current_auditor
from ..utils.notification import NotificationService

router = APIRouter(prefix="/api/v1/workflow", tags=["workflow"])

@router.get("/workflow", response_model=WorkflowResponse)
async def get_workflow_dashboard(
    current_auditor: Auditor = Depends(get_current_auditor),
    db: Session = Depends(get_db)
):
    """获取审核工作台数据"""
    # 统计待审核数量
    pending_count = db.query(AuditWorkflow).filter(
        AuditWorkflow.assigned_auditor_id == current_auditor.id,
        AuditWorkflow.workflow_status.in_([WorkflowStatus.pending, WorkflowStatus.in_progress])
    ).count()
    
    # 统计已通过数量
    approved_count = db.query(AuditRecord).filter(
        AuditRecord.auditor_id == current_auditor.id,
        AuditRecord.audit_status == AuditStatus.approved
    ).count()
    
    # 统计需复审数量
    need_review_count = db.query(AuditRecord).filter(
        AuditRecord.auditor_id == current_auditor.id,
        AuditRecord.audit_status == AuditStatus.need_review
    ).count()
    
    # 计算本月投资总额
    total_investment = db.query(func.sum(Customer.investment_amount)).filter(
        Customer.status == CustomerStatus.approved
    ).scalar() or 0
    
    # 获取待审核列表
    pending_workflows = AuditWorkflowService.get_pending_workflows(db, current_auditor.id)
    pending_list = []
    
    for workflow in pending_workflows:
        customer = db.query(Customer).filter(Customer.id == workflow.customer_id).first()
        if customer:
            pending_list.append({
                "customer_id": customer.id,
                "customer_name": customer.name,
                "application_id": f"RA-{customer.id:03d}",
                "investment_amount": float(customer.investment_amount),
                "risk_level": customer.risk_level.value if customer.risk_level else "unknown",
                "submitted_at": customer.created_at.isoformat(),
                "priority": "high" if float(customer.investment_amount) > 1000000 else "normal"
            })
    
    return WorkflowResponse(
        data={
            "pending_count": pending_count,
            "approved_count": approved_count,
            "need_review_count": need_review_count,
            "total_investment": float(total_investment),
            "pending_list": pending_list
        }
    )

@router.post("/audit", response_model=AuditResponse)
async def submit_audit(
    audit_request: AuditRequest,
    current_auditor: Auditor = Depends(get_current_auditor),
    db: Session = Depends(get_db)
):
    """提交审核结果"""
    try:
        # 查找对应的工作流
        workflow = db.query(AuditWorkflow).filter(
            AuditWorkflow.customer_id == audit_request.customer_id,
            AuditWorkflow.assigned_auditor_id == current_auditor.id,
            AuditWorkflow.workflow_status.in_([WorkflowStatus.pending, WorkflowStatus.in_progress])
        ).first()
        
        if not workflow:
            raise HTTPException(status_code=404, detail="未找到对应的审核任务")
        
        # 处理审核结果
        success = AuditWorkflowService.process_audit(
            db, 
            workflow.id, 
            current_auditor.id, 
            audit_request.audit_status, 
            audit_request.audit_opinion or ""
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="审核处理失败")
        
        # 如果审核完成，更新客户状态并发送通知
        if workflow.workflow_status == WorkflowStatus.completed:
            customer = db.query(Customer).filter(Customer.id == audit_request.customer_id).first()
            if customer:
                customer.status = CustomerStatus.approved
                db.commit()
                
                # 发送通知
                NotificationService.send_audit_completion_notification(
                    db, customer.id, customer.name, "approved"
                )
        elif workflow.workflow_status == WorkflowStatus.rejected:
            customer = db.query(Customer).filter(Customer.id == audit_request.customer_id).first()
            if customer:
                customer.status = CustomerStatus.rejected
                db.commit()
                
                # 发送通知
                NotificationService.send_audit_completion_notification(
                    db, customer.id, customer.name, "rejected"
                )
        
        return AuditResponse(
            message="审核提交成功",
            data={"workflow_id": workflow.id}
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
