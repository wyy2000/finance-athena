#!/usr/bin/env python3
"""
银行投资风险审核系统 - 数据库查看器
用于快速查看数据库中的相关信息
"""

import sqlite3
import os
import sys
from datetime import datetime

class DatabaseViewer:
    def __init__(self, db_path="finance_athena.db"):
        """初始化数据库连接"""
        self.db_path = db_path
        if not os.path.exists(db_path):
            print(f"❌ 数据库文件 {db_path} 不存在")
            print("请确保在正确的目录下运行此脚本")
            sys.exit(1)
        
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # 使结果可以通过列名访问
        self.cursor = self.conn.cursor()
    
    def execute_query(self, query, params=None):
        """执行查询并返回结果"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ 查询执行失败: {e}")
            return []
    
    def print_table(self, title, data, max_width=80):
        """格式化打印表格"""
        if not data:
            print(f"📋 {title}: 无数据")
            return
        
        print(f"\n{'='*max_width}")
        print(f"📋 {title}")
        print(f"{'='*max_width}")
        
        # 获取列名
        columns = data[0].keys()
        
        # 计算每列的最大宽度
        col_widths = {}
        for col in columns:
            col_widths[col] = len(str(col))
            for row in data:
                col_widths[col] = max(col_widths[col], len(str(row[col])))
        
        # 打印表头
        header = " | ".join(str(col).ljust(col_widths[col]) for col in columns)
        print(header)
        print("-" * len(header))
        
        # 打印数据行
        for row in data:
            row_str = " | ".join(str(row[col]).ljust(col_widths[col]) for col in columns)
            print(row_str)
        
        print(f"{'='*max_width}")
        print(f"总计: {len(data)} 条记录")
    
    def view_customers(self):
        """查看所有客户信息"""
        query = """
        SELECT 
            id as '客户ID',
            name as '姓名',
            phone as '手机号',
            investment_amount as '投资金额',
            risk_score as '风险评分',
            risk_level as '风险等级',
            status as '状态',
            created_at as '创建时间'
        FROM customers 
        ORDER BY created_at DESC
        """
        data = self.execute_query(query)
        self.print_table("客户信息", data)
    
    def view_risk_assessments(self):
        """查看风险评估记录"""
        query = """
        SELECT 
            ra.id as '评估ID',
            ra.customer_id as '客户ID',
            c.name as '客户姓名',
            ra.risk_score as '风险评分',
            ra.risk_level as '风险等级',
            ra.assessment_date as '评估时间'
        FROM risk_assessments ra
        JOIN customers c ON ra.customer_id = c.id
        ORDER BY ra.assessment_date DESC
        """
        data = self.execute_query(query)
        self.print_table("风险评估记录", data)
    
    def view_investment_advice(self):
        """查看投资建议"""
        query = """
        SELECT 
            ia.id as '建议ID',
            ia.customer_id as '客户ID',
            c.name as '客户姓名',
            ia.portfolio_type as '投资组合类型',
            ia.expected_return_min as '预期最低收益',
            ia.expected_return_max as '预期最高收益',
            ia.created_at as '创建时间'
        FROM investment_advice ia
        JOIN customers c ON ia.customer_id = c.id
        ORDER BY ia.created_at DESC
        """
        data = self.execute_query(query)
        self.print_table("投资建议", data)
    
    def view_auditors(self):
        """查看审核员信息"""
        query = """
        SELECT 
            id as '审核员ID',
            username as '用户名',
            name as '姓名',
            role as '角色',
            department as '部门',
            phone as '电话',
            status as '状态',
            created_at as '创建时间'
        FROM auditors
        ORDER BY id
        """
        data = self.execute_query(query)
        self.print_table("审核员信息", data)
    
    def view_audit_workflow(self):
        """查看审核流程"""
        query = """
        SELECT 
            aw.id as '流程ID',
            aw.customer_id as '客户ID',
            c.name as '客户姓名',
            aw.current_level as '当前审核级别',
            aw.workflow_status as '流程状态',
            a.name as '审核员姓名',
            aw.next_level as '下一级审核',
            aw.created_at as '创建时间'
        FROM audit_workflow aw
        JOIN customers c ON aw.customer_id = c.id
        LEFT JOIN auditors a ON aw.assigned_auditor_id = a.id
        ORDER BY aw.created_at DESC
        """
        data = self.execute_query(query)
        self.print_table("审核流程", data)
    
    def view_audit_records(self):
        """查看审核记录"""
        query = """
        SELECT 
            ar.id as '审核记录ID',
            ar.customer_id as '客户ID',
            c.name as '客户姓名',
            a.name as '审核员姓名',
            ar.audit_level as '审核级别',
            ar.audit_status as '审核状态',
            ar.audit_opinion as '审核意见',
            ar.audit_date as '审核时间'
        FROM audit_records ar
        JOIN customers c ON ar.customer_id = c.id
        JOIN auditors a ON ar.auditor_id = a.id
        ORDER BY ar.audit_date DESC
        """
        data = self.execute_query(query)
        self.print_table("审核记录", data)
    
    def view_statistics(self):
        """查看统计信息"""
        print("\n" + "="*80)
        print("📊 系统统计信息")
        print("="*80)
        
        # 客户统计
        query = """
        SELECT 
            COUNT(*) as '总客户数',
            COUNT(CASE WHEN status = 'pending' THEN 1 END) as '待审核客户数',
            COUNT(CASE WHEN status = 'approved' THEN 1 END) as '已通过客户数',
            COUNT(CASE WHEN status = 'rejected' THEN 1 END) as '已拒绝客户数',
            SUM(investment_amount) as '总投资金额',
            AVG(risk_score) as '平均风险评分'
        FROM customers
        """
        data = self.execute_query(query)
        if data:
            row = data[0]
            print(f"👥 客户统计:")
            print(f"   总客户数: {row['总客户数']}")
            print(f"   待审核: {row['待审核客户数']}")
            print(f"   已通过: {row['已通过客户数']}")
            print(f"   已拒绝: {row['已拒绝客户数']}")
            print(f"   总投资金额: {row['总投资金额']:,.2f} 元")
            print(f"   平均风险评分: {row['平均风险评分']:.1f}")
        
        # 风险等级分布
        query = """
        SELECT 
            risk_level as '风险等级',
            COUNT(*) as '客户数量'
        FROM customers 
        WHERE risk_level IS NOT NULL
        GROUP BY risk_level
        ORDER BY COUNT(*) DESC
        """
        data = self.execute_query(query)
        if data:
            print(f"\n📈 风险等级分布:")
            for row in data:
                print(f"   {row['风险等级']}: {row['客户数量']} 人")
        
        # 审核员工作量
        query = """
        SELECT 
            a.name as '审核员姓名',
            a.role as '角色',
            COUNT(ar.id) as '审核记录数',
            COUNT(CASE WHEN ar.audit_status = 'approved' THEN 1 END) as '通过数',
            COUNT(CASE WHEN ar.audit_status = 'rejected' THEN 1 END) as '拒绝数'
        FROM auditors a
        LEFT JOIN audit_records ar ON a.id = ar.auditor_id
        GROUP BY a.id, a.name, a.role
        ORDER BY COUNT(ar.id) DESC
        """
        data = self.execute_query(query)
        if data:
            print(f"\n👨‍💼 审核员工作量:")
            for row in data:
                print(f"   {row['审核员姓名']} ({row['角色']}): {row['审核记录数']} 条记录")
    
    def view_customer_detail(self, customer_id):
        """查看特定客户的详细信息"""
        print(f"\n{'='*80}")
        print(f"👤 客户详细信息 (ID: {customer_id})")
        print(f"{'='*80}")
        
        # 客户基本信息
        query = "SELECT * FROM customers WHERE id = ?"
        data = self.execute_query(query, (customer_id,))
        if data:
            customer = data[0]
            print(f"📋 基本信息:")
            print(f"   姓名: {customer['name']}")
            print(f"   手机号: {customer['phone']}")
            print(f"   投资金额: {customer['investment_amount']:,.2f} 元")
            print(f"   风险评分: {customer['risk_score']}")
            print(f"   风险等级: {customer['risk_level']}")
            print(f"   状态: {customer['status']}")
            print(f"   创建时间: {customer['created_at']}")
        
        # 风险评估
        query = "SELECT * FROM risk_assessments WHERE customer_id = ?"
        data = self.execute_query(query, (customer_id,))
        if data:
            assessment = data[0]
            print(f"\n📊 风险评估:")
            print(f"   风险评分: {assessment['risk_score']}")
            print(f"   风险等级: {assessment['risk_level']}")
            print(f"   评估时间: {assessment['assessment_date']}")
        
        # 投资建议
        query = "SELECT * FROM investment_advice WHERE customer_id = ?"
        data = self.execute_query(query, (customer_id,))
        if data:
            advice = data[0]
            print(f"\n💡 投资建议:")
            print(f"   投资组合类型: {advice['portfolio_type']}")
            print(f"   预期收益: {advice['expected_return_min']}% - {advice['expected_return_max']}%")
            print(f"   建议内容: {advice['advice_content']}")
        
        # 审核流程
        query = """
        SELECT 
            aw.*,
            c.name as customer_name,
            a.name as auditor_name
        FROM audit_workflow aw
        JOIN customers c ON aw.customer_id = c.id
        LEFT JOIN auditors a ON aw.assigned_auditor_id = a.id
        WHERE aw.customer_id = ?
        """
        data = self.execute_query(query, (customer_id,))
        if data:
            workflow = data[0]
            print(f"\n🔄 审核流程:")
            print(f"   当前审核级别: {workflow['current_level']}")
            print(f"   流程状态: {workflow['workflow_status']}")
            print(f"   分配审核员: {workflow['auditor_name'] or '未分配'}")
            print(f"   下一级审核: {workflow['next_level'] or '无'}")
        
        # 审核记录
        query = """
        SELECT 
            ar.*,
            a.name as auditor_name
        FROM audit_records ar
        JOIN auditors a ON ar.auditor_id = a.id
        WHERE ar.customer_id = ?
        ORDER BY ar.audit_date DESC
        """
        data = self.execute_query(query, (customer_id,))
        if data:
            print(f"\n📝 审核记录:")
            for record in data:
                print(f"   {record['audit_date']} - {record['auditor_name']} ({record['audit_level']}): {record['audit_status']}")
                if record['audit_opinion']:
                    print(f"     意见: {record['audit_opinion']}")
    
    def show_menu(self):
        """显示菜单"""
        print("\n" + "="*80)
        print("🏦 银行投资风险审核系统 - 数据库查看器")
        print("="*80)
        print("1. 查看所有客户信息")
        print("2. 查看风险评估记录")
        print("3. 查看投资建议")
        print("4. 查看审核员信息")
        print("5. 查看审核流程")
        print("6. 查看审核记录")
        print("7. 查看系统统计信息")
        print("8. 查看特定客户详细信息")
        print("0. 退出")
        print("="*80)
    
    def run(self):
        """运行数据库查看器"""
        while True:
            self.show_menu()
            choice = input("请选择功能 (0-8): ").strip()
            
            if choice == '0':
                print("👋 再见！")
                break
            elif choice == '1':
                self.view_customers()
            elif choice == '2':
                self.view_risk_assessments()
            elif choice == '3':
                self.view_investment_advice()
            elif choice == '4':
                self.view_auditors()
            elif choice == '5':
                self.view_audit_workflow()
            elif choice == '6':
                self.view_audit_records()
            elif choice == '7':
                self.view_statistics()
            elif choice == '8':
                customer_id = input("请输入客户ID: ").strip()
                try:
                    self.view_customer_detail(int(customer_id))
                except ValueError:
                    print("❌ 请输入有效的客户ID")
            else:
                print("❌ 无效选择，请重新输入")
            
            input("\n按回车键继续...")

def main():
    """主函数"""
    print("🚀 启动数据库查看器...")
    
    # 查找数据库文件
    db_paths = [
        "finance_athena.db",
        "backend/finance_athena.db",
        "../backend/finance_athena.db"
    ]
    
    db_path = None
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("❌ 未找到数据库文件")
        print("请确保在正确的目录下运行此脚本")
        return
    
    print(f"📁 使用数据库: {db_path}")
    
    viewer = DatabaseViewer(db_path)
    viewer.run()
    viewer.conn.close()

if __name__ == "__main__":
    main()
