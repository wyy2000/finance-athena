from typing import Dict, Any
from ..models.customer import RiskLevel
from ..schemas.customer import AssessmentData

class RiskAssessmentService:
    @staticmethod
    def calculate_risk_score(assessment_data: AssessmentData) -> int:
        """计算风险评分"""
        score = 50  # 基础分
        
        # 年龄影响
        age_scores = {
            "18-30岁": 15,
            "31-45岁": 10,
            "46-60岁": 5,
            "60岁以上": -10
        }
        score += age_scores.get(assessment_data.age, 0)
        
        # 收入影响
        income_scores = {
            "50万以上": 15,
            "30-50万": 10,
            "10-30万": 5,
            "10万以下": 0
        }
        score += income_scores.get(assessment_data.income, 0)
        
        # 投资经验影响
        experience_scores = {
            "5年以上": 15,
            "3-5年": 10,
            "1-3年": 5,
            "无经验": 0
        }
        score += experience_scores.get(assessment_data.experience, 0)
        
        # 风险承受能力影响
        tolerance_scores = {
            "30%以上": 20,
            "15-30%": 10,
            "5-15%": 5,
            "5%以内": -10
        }
        score += tolerance_scores.get(assessment_data.risk_tolerance, 0)
        
        # 投资目标影响
        goal_scores = {
            "追求高收益": 15,
            "积极增长": 10,
            "稳健增值": 5,
            "资产保值": -5
        }
        score += goal_scores.get(assessment_data.goal, 0)
        
        # 投资期限影响
        period_scores = {
            "5年以上": 10,
            "3-5年": 5,
            "1-3年": 0,
            "1年以内": -10
        }
        score += period_scores.get(assessment_data.period, 0)
        
        return max(0, min(100, score))
    
    @staticmethod
    def determine_risk_level(score: int) -> RiskLevel:
        """确定风险等级"""
        if score < 40:
            return RiskLevel.conservative
        elif score < 70:
            return RiskLevel.moderate
        else:
            return RiskLevel.aggressive
