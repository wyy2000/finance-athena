from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.workflow import AuditWorkflow, AuditRecord, AuditLevel, WorkflowStatus, AuditStatus
from ..models.auditor import Auditor, AuditorRole

class AuditWorkflowService:
    @staticmethod
    def create_workflow(db: Session, customer_id: int, risk_level: str, investment_amount: float) -> str:
        """创建审核流程"""
        # 根据风险等级和投资金额确定审核流程
        if risk_level == "conservative":
            levels = [AuditLevel.junior]
        elif risk_level == "moderate":
            levels = [AuditLevel.junior, AuditLevel.senior]
            if investment_amount > 1000000:  # 100万以上需要高级审核
                levels.append(AuditLevel.expert)
        else:  # aggressive
            levels = [AuditLevel.junior, AuditLevel.senior, AuditLevel.expert, AuditLevel.committee]
        
        # 创建审核流程记录
        workflow_id = f"WF{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 分配第一个审核员
        first_auditor = AuditWorkflowService.assign_auditor(db, levels[0])
        
        # 创建工作流记录
        workflow = AuditWorkflow(
            customer_id=customer_id,
            current_level=levels[0],
            workflow_status=WorkflowStatus.pending,
            assigned_auditor_id=first_auditor,
            next_level=levels[1] if len(levels) > 1 else None
        )
        
        db.add(workflow)
        db.commit()
        
        return workflow_id
    
    @staticmethod
    def assign_auditor(db: Session, level: AuditLevel) -> Optional[int]:
        """分配审核员"""
        # 根据审核级别分配合适的审核员
        role_mapping = {
            AuditLevel.junior: AuditorRole.junior,
            AuditLevel.senior: AuditorRole.senior,
            AuditLevel.expert: AuditorRole.expert,
            AuditLevel.committee: AuditorRole.committee
        }
        
        auditor = db.query(Auditor).filter(
            Auditor.role == role_mapping[level],
            Auditor.status == "active"
        ).first()
        
        return auditor.id if auditor else None
    
    @staticmethod
    def process_audit(db: Session, workflow_id: int, auditor_id: int, 
                     audit_result: AuditStatus, opinion: str) -> bool:
        """处理审核结果"""
        workflow = db.query(AuditWorkflow).filter(AuditWorkflow.id == workflow_id).first()
        if not workflow:
            return False
        
        # 创建审核记录
        audit_record = AuditRecord(
            customer_id=workflow.customer_id,
            auditor_id=auditor_id,
            audit_level=workflow.current_level,
            audit_status=audit_result,
            audit_opinion=opinion
        )
        db.add(audit_record)
        
        if audit_result == AuditStatus.rejected:
            # 如果拒绝，结束流程
            workflow.workflow_status = WorkflowStatus.rejected
        elif audit_result == AuditStatus.approved:
            if workflow.next_level:
                # 流转到下一级
                next_auditor = AuditWorkflowService.assign_auditor(db, workflow.next_level)
                workflow.current_level = workflow.next_level
                workflow.assigned_auditor_id = next_auditor
                # 这里需要确定下一级，简化处理
                workflow.workflow_status = WorkflowStatus.in_progress
            else:
                # 完成所有审核
                workflow.workflow_status = WorkflowStatus.completed
        
        db.commit()
        return True
    
    @staticmethod
    def get_pending_workflows(db: Session, auditor_id: int) -> List[AuditWorkflow]:
        """获取待审核的工作流"""
        return db.query(AuditWorkflow).filter(
            AuditWorkflow.assigned_auditor_id == auditor_id,
            AuditWorkflow.workflow_status.in_([WorkflowStatus.pending, WorkflowStatus.in_progress])
        ).all()
