from datetime import datetime
from sqlalchemy.orm import Session
from ..models.workflow import Notification, NotificationType, NotificationStatus

class NotificationService:
    @staticmethod
    def create_notification(
        db: Session,
        customer_id: int,
        notification_type: NotificationType,
        title: str,
        content: str
    ) -> Notification:
        """创建通知"""
        notification = Notification(
            customer_id=customer_id,
            notification_type=notification_type,
            title=title,
            content=content,
            status=NotificationStatus.pending
        )
        db.add(notification)
        db.commit()
        return notification
    
    @staticmethod
    def send_audit_completion_notification(db: Session, customer_id: int, customer_name: str, status: str):
        """发送审核完成通知"""
        if status == "approved":
            title = "投资风险评估审核通过"
            content = f"尊敬的{customer_name}，您的投资风险评估已审核通过，请登录系统查看投资建议。"
        else:
            title = "投资风险评估审核结果"
            content = f"尊敬的{customer_name}，您的投资风险评估审核未通过，请联系客服了解详情。"
        
        return NotificationService.create_notification(
            db, customer_id, NotificationType.sms, title, content
        )
    
    @staticmethod
    def get_customer_notifications(db: Session, customer_id: int, limit: int = 10):
        """获取客户的通知历史"""
        notifications = db.query(Notification).filter(
            Notification.customer_id == customer_id
        ).order_by(Notification.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": n.id,
                "title": n.title,
                "content": n.content,
                "notification_type": n.notification_type.value,
                "status": n.status.value,
                "created_at": n.created_at.isoformat(),
                "sent_at": n.sent_at.isoformat() if n.sent_at else None
            }
            for n in notifications
        ]
    
    @staticmethod
    def mark_notification_as_read(db: Session, notification_id: int, customer_id: int):
        """标记通知为已读"""
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.customer_id == customer_id
        ).first()
        
        if notification:
            notification.status = NotificationStatus.sent
            db.commit()
            return True
        return False
