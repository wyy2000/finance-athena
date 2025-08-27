#!/usr/bin/env python3
"""
银行投资风险审核系统API测试脚本
"""

import requests
import json
import time

# API基础URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 健康检查通过")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_customer_register():
    """测试客户注册"""
    print("\n👤 测试客户注册...")
    
    customer_data = {
        "name": "张三",
        "phone": "13800138000",
        "id_card": "110101199001011234",
        "email": "zhangsan@example.com",
        "occupation": "工程师",
        "investment_amount": 500000,
        "assessment_data": {
            "age": "31-45岁",
            "income": "30-50万",
            "experience": "3-5年",
            "risk_tolerance": "15-30%",
            "goal": "积极增长",
            "period": "3-5年"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/customers/register",
            json=customer_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 客户注册成功")
            print(f"   客户ID: {result['data']['customer_id']}")
            print(f"   风险评分: {result['data']['risk_score']}")
            print(f"   风险等级: {result['data']['risk_level']}")
            return result['data']['customer_id']
        else:
            print(f"❌ 客户注册失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 客户注册异常: {e}")
        return None

def test_get_customer_advice(customer_id):
    """测试获取客户投资建议"""
    print(f"\n💡 测试获取客户{customer_id}的投资建议...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/customers/{customer_id}/advice")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 获取投资建议成功")
            print(f"   客户姓名: {result['data']['customer_info']['name']}")
            print(f"   投资金额: {result['data']['customer_info']['investment_amount']}")
            print(f"   风险等级: {result['data']['risk_assessment']['risk_level']}")
            print(f"   投资建议: {result['data']['investment_advice']['advice_content'][:50]}...")
            return True
        else:
            print(f"❌ 获取投资建议失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取投资建议异常: {e}")
        return False

def test_auditor_login():
    """测试审核员登录"""
    print("\n🔐 测试审核员登录...")
    
    login_data = {
        "username": "junior1",
        "password": "password123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auditors/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 审核员登录成功")
            print(f"   访问令牌: {result['access_token'][:20]}...")
            return result['access_token']
        else:
            print(f"❌ 审核员登录失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 审核员登录异常: {e}")
        return None

def test_workflow_dashboard(token):
    """测试获取工作台数据"""
    print("\n📊 测试获取工作台数据...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/workflow/workflow", headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 获取工作台数据成功")
            print(f"   待审核数量: {result['data']['pending_count']}")
            print(f"   已通过数量: {result['data']['approved_count']}")
            print(f"   本月投资总额: {result['data']['total_investment']}")
            return True
        else:
            print(f"❌ 获取工作台数据失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取工作台数据异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试银行投资风险审核系统API")
    print("=" * 50)
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(5)
    
    # 测试健康检查
    if not test_health_check():
        print("❌ 服务未启动，请检查Docker容器状态")
        return
    
    # 测试客户注册
    customer_id = test_customer_register()
    if not customer_id:
        print("❌ 客户注册失败，停止测试")
        return
    
    # 测试获取投资建议
    test_get_customer_advice(customer_id)
    
    # 测试审核员登录
    token = test_auditor_login()
    if not token:
        print("❌ 审核员登录失败，停止测试")
        return
    
    # 测试工作台数据
    test_workflow_dashboard(token)
    
    print("\n" + "=" * 50)
    print("✅ API测试完成！")
    print("\n🌐 访问地址：")
    print("   前端页面: http://localhost:8000")
    print("   API文档: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
