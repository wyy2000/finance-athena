from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.customer import Customer, CustomerStatus
from ..models.workflow import RiskAssessment, InvestmentAdvice
from ..schemas.customer import CustomerCreate, CustomerRegisterResponse, CustomerResponse
from ..services.risk_assessment import RiskAssessmentService
from ..services.investment_advice import InvestmentAdviceService
from ..services.audit_workflow import AuditWorkflowService

router = APIRouter(prefix="/api/v1/customers", tags=["customers"])

@router.post("/register", response_model=CustomerRegisterResponse)
async def register_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    """客户注册和风险评估"""
    try:
        # 检查手机号是否已存在
        existing_customer = db.query(Customer).filter(Customer.phone == customer_data.phone).first()
        if existing_customer:
            raise HTTPException(status_code=400, detail="手机号已存在")
        
        # 检查身份证号是否已存在
        existing_customer = db.query(Customer).filter(Customer.id_card == customer_data.id_card).first()
        if existing_customer:
            raise HTTPException(status_code=400, detail="身份证号已存在")
        
        # 计算风险评分
        risk_score = RiskAssessmentService.calculate_risk_score(customer_data.assessment_data)
        risk_level = RiskAssessmentService.determine_risk_level(risk_score)
        
        # 创建客户记录
        customer = Customer(
            name=customer_data.name,
            phone=customer_data.phone,
            id_card=customer_data.id_card,
            email=customer_data.email,
            occupation=customer_data.occupation,
            investment_amount=customer_data.investment_amount,
            age_range=customer_data.assessment_data.age,
            income_level=customer_data.assessment_data.income,
            investment_experience=customer_data.assessment_data.experience,
            risk_tolerance=customer_data.assessment_data.risk_tolerance,
            investment_goal=customer_data.assessment_data.goal,
            investment_period=customer_data.assessment_data.period,
            risk_score=risk_score,
            risk_level=risk_level,
            status=CustomerStatus.pending
        )
        
        db.add(customer)
        db.flush()  # 获取ID但不提交
        
        # 创建风险评估记录
        assessment = RiskAssessment(
            customer_id=customer.id,
            assessment_data=customer_data.assessment_data.dict(),
            risk_score=risk_score,
            risk_level=risk_level.value
        )
        db.add(assessment)
        
        # 生成投资建议
        portfolio_data = InvestmentAdviceService.generate_portfolio(
            risk_level, 
            float(customer_data.investment_amount)
        )
        
        advice = InvestmentAdvice(
            customer_id=customer.id,
            portfolio_type=risk_level.value,
            expected_return_min=portfolio_data["expected_return_min"],
            expected_return_max=portfolio_data["expected_return_max"],
            portfolio_config=portfolio_data["portfolio_config"],
            advice_content=portfolio_data["advice_content"]
        )
        db.add(advice)
        
        # 创建审核流程
        workflow_id = AuditWorkflowService.create_workflow(
            db, 
            customer.id, 
            risk_level.value, 
            float(customer_data.investment_amount)
        )
        
        db.commit()
        
        return CustomerRegisterResponse(
            message="注册成功",
            data={
                "customer_id": customer.id,
                "risk_score": risk_score,
                "risk_level": risk_level.value,
                "workflow_id": workflow_id
            }
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """获取客户信息"""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    
    return customer

@router.get("/{customer_id}/advice")
async def get_customer_advice(customer_id: int, db: Session = Depends(get_db)):
    """获取客户投资建议"""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    
    assessment = db.query(RiskAssessment).filter(RiskAssessment.customer_id == customer_id).first()
    advice = db.query(InvestmentAdvice).filter(InvestmentAdvice.customer_id == customer_id).first()
    
    return {
        "code": 200,
        "data": {
            "customer_info": {
                "id": customer.id,
                "name": customer.name,
                "phone": customer.phone,
                "investment_amount": float(customer.investment_amount),
                "risk_level": customer.risk_level.value if customer.risk_level else None,
                "status": customer.status.value
            },
            "risk_assessment": {
                "risk_score": assessment.risk_score if assessment else None,
                "risk_level": assessment.risk_level if assessment else None
            },
            "investment_advice": {
                "portfolio_type": advice.portfolio_type if advice else None,
                "expected_return": f"{advice.expected_return_min}%-{advice.expected_return_max}%" if advice else None,
                "portfolio_config": advice.portfolio_config if advice else None,
                "advice_content": advice.advice_content if advice else None
            },
            "audit_status": customer.status.value
        }
    }
