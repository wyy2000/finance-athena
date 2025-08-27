from typing import Dict, Any
from decimal import Decimal
from ..models.customer import RiskLevel

class InvestmentAdviceService:
    @staticmethod
    def generate_portfolio(risk_level: RiskLevel, investment_amount: float) -> Dict[str, Any]:
        """生成投资组合建议"""
        portfolios = {
            RiskLevel.conservative: {
                "portfolio_type": RiskLevel.conservative.value,
                "expected_return_min": Decimal("4.0"),
                "expected_return_max": Decimal("6.0"),
                "portfolio_config": {
                    "money_fund": 40,
                    "government_bonds": 30,
                    "bank_products": 20,
                    "bond_fund": 10
                },
                "advice_content": "基于您的保守型风险偏好，建议配置低风险投资产品，主要投资于货币基金、国债等稳定收益产品。"
            },
            RiskLevel.moderate: {
                "portfolio_type": RiskLevel.moderate.value,
                "expected_return_min": Decimal("6.0"),
                "expected_return_max": Decimal("10.0"),
                "portfolio_config": {
                    "mixed_fund": 35,
                    "bond_fund": 25,
                    "quality_stocks": 25,
                    "money_fund": 15
                },
                "advice_content": "基于您的稳健型风险偏好，建议配置平衡型投资组合，适度配置股票和基金产品。"
            },
            RiskLevel.aggressive: {
                "portfolio_type": RiskLevel.aggressive.value,
                "expected_return_min": Decimal("10.0"),
                "expected_return_max": Decimal("15.0"),
                "portfolio_config": {
                    "growth_stocks": 50,
                    "tech_fund": 25,
                    "emerging_markets": 15,
                    "bond_fund": 10
                },
                "advice_content": "基于您的激进型风险偏好，建议配置高收益投资组合，主要投资于成长股和科技基金。"
            }
        }
        
        return portfolios.get(risk_level, portfolios[RiskLevel.moderate])
