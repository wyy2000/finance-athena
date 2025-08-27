#!/usr/bin/env python3
"""
SQLite数据库初始化脚本
"""

import sqlite3
import os
from pathlib import Path

def init_sqlite_db():
    """初始化SQLite数据库"""
    db_path = Path("finance_athena.db")
    
    # 如果数据库文件已存在，删除它
    if db_path.exists():
        os.remove(db_path)
        print("🗑️ 删除现有数据库文件")
    
    # 创建数据库连接
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔨 创建数据库表...")
    
    # 创建客户信息表
    cursor.execute('''
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE,
        id_card VARCHAR(18) NOT NULL UNIQUE,
        email VARCHAR(100),
        occupation VARCHAR(100),
        investment_amount DECIMAL(15,2),
        age_range VARCHAR(20),
        income_level VARCHAR(20),
        investment_experience VARCHAR(20),
        risk_tolerance VARCHAR(20),
        investment_goal VARCHAR(20),
        investment_period VARCHAR(20),
        risk_score INTEGER DEFAULT 0,
        risk_level VARCHAR(20),
        status VARCHAR(20) DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建审核员表
    cursor.execute('''
    CREATE TABLE auditors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        name VARCHAR(50) NOT NULL,
        role VARCHAR(20) NOT NULL,
        department VARCHAR(100),
        phone VARCHAR(20),
        status VARCHAR(20) DEFAULT 'active',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建风险评估记录表
    cursor.execute('''
    CREATE TABLE risk_assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        assessment_data TEXT,
        risk_score INTEGER NOT NULL,
        risk_level VARCHAR(20) NOT NULL,
        assessment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
    ''')
    
    # 创建投资建议表
    cursor.execute('''
    CREATE TABLE investment_advice (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        portfolio_type VARCHAR(20) NOT NULL,
        expected_return_min DECIMAL(5,2),
        expected_return_max DECIMAL(5,2),
        portfolio_config TEXT,
        advice_content TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
    ''')
    
    # 创建审核流程表
    cursor.execute('''
    CREATE TABLE audit_workflow (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        current_level VARCHAR(20) NOT NULL,
        workflow_status VARCHAR(20) DEFAULT 'pending',
        assigned_auditor_id INTEGER,
        next_level VARCHAR(20),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (assigned_auditor_id) REFERENCES auditors(id)
    )
    ''')
    
    # 创建审核记录表
    cursor.execute('''
    CREATE TABLE audit_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        auditor_id INTEGER NOT NULL,
        audit_level VARCHAR(20) NOT NULL,
        audit_status VARCHAR(20) NOT NULL,
        audit_opinion TEXT,
        audit_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (auditor_id) REFERENCES auditors(id)
    )
    ''')
    
    # 创建通知记录表
    cursor.execute('''
    CREATE TABLE notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        notification_type VARCHAR(20) NOT NULL,
        title VARCHAR(200),
        content TEXT NOT NULL,
        status VARCHAR(20) DEFAULT 'pending',
        sent_at DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
    ''')
    
    # 插入初始审核员数据
    print("👥 插入初始审核员数据...")
    cursor.execute('''
    INSERT INTO auditors (username, password_hash, name, role, department, phone) VALUES
    ('junior1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uOeG', '初级审核员1', 'junior', '风险审核部', '13800138001'),
    ('senior1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uOeG', '中级审核员1', 'senior', '风险审核部', '13800138002'),
    ('expert1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uOeG', '高级审核员1', 'expert', '风险审核部', '13800138003'),
    ('committee1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uOeG', '投资委员会1', 'committee', '投资委员会', '13800138004')
    ''')
    
    # 提交更改
    conn.commit()
    conn.close()
    
    print("✅ SQLite数据库初始化完成！")
    print(f"📁 数据库文件: {db_path.absolute()}")

if __name__ == "__main__":
    init_sqlite_db()
