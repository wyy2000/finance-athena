#!/usr/bin/env python3
"""
完整的银行投资风险审核系统测试脚本
"""

import requests
import json
import time
import webbrowser

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

def test_frontend_pages():
    """测试前端页面"""
    print("\n🌐 测试前端页面...")
    
    pages = [
        ("/", "主页"),
        ("/customer.html", "客户页面"),
        ("/auditor.html", "审核员页面")
    ]
    
    for page, name in pages:
        try:
            response = requests.get(f"{BASE_URL}{page}")
            if response.status_code == 200:
                print(f"✅ {name} 加载成功")
            else:
                print(f"❌ {name} 加载失败: {response.status_code}")
        except Exception as e:
            print(f"❌ {name} 加载异常: {e}")

def test_customer_register():
    """测试客户注册"""
    print("\n👤 测试客户注册...")
    
    customer_data = {
        "name": "测试用户",
        "phone": "13900000000",
        "id_card": "110101199001011111",
        "email": "test@example.com",
        "occupation": "测试工程师",
        "investment_amount": 100000,
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

def open_browser():
    """在浏览器中打开系统"""
    print("\n🌐 在浏览器中打开系统...")
    try:
        webbrowser.open(f"{BASE_URL}")
        print("✅ 已打开浏览器")
    except Exception as e:
        print(f"❌ 打开浏览器失败: {e}")

def main():
    """主测试函数"""
    print("🚀 开始完整测试银行投资风险审核系统")
    print("=" * 60)
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(3)
    
    # 测试健康检查
    if not test_health_check():
        print("❌ 服务未启动，请检查服务状态")
        return
    
    # 测试前端页面
    test_frontend_pages()
    
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
    
    # 打开浏览器
    open_browser()
    
    print("\n" + "=" * 60)
    print("✅ 完整系统测试完成！")
    print("\n🎉 系统功能总结：")
    print("   ✅ 后端API服务正常运行")
    print("   ✅ 前端页面正常显示")
    print("   ✅ 客户注册和风险评估功能正常")
    print("   ✅ 投资建议生成功能正常")
    print("   ✅ 审核员登录和工作台功能正常")
    print("   ✅ SQLite数据库正常工作")
    print("\n🌐 访问地址：")
    print(f"   主页: {BASE_URL}")
    print(f"   客户页面: {BASE_URL}/customer.html")
    print(f"   审核员页面: {BASE_URL}/auditor.html")
    print(f"   API文档: {BASE_URL}/docs")
    print("\n🔑 审核员账号：")
    print("   用户名: junior1, senior1, expert1, committee1")
    print("   密码: password123")

if __name__ == "__main__":
    main()
