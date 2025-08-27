-- 创建数据库
CREATE DATABASE IF NOT EXISTS finance_athena CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE finance_athena;

-- 创建客户信息表
CREATE TABLE IF NOT EXISTS customers (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    phone VARCHAR(20) NOT NULL UNIQUE COMMENT '手机号',
    id_card VARCHAR(18) NOT NULL UNIQUE COMMENT '身份证号',
    email VARCHAR(100) COMMENT '邮箱',
    occupation VARCHAR(100) COMMENT '职业',
    investment_amount DECIMAL(15,2) COMMENT '投资金额',
    age_range VARCHAR(20) COMMENT '年龄范围',
    income_level VARCHAR(20) COMMENT '收入水平',
    investment_experience VARCHAR(20) COMMENT '投资经验',
    risk_tolerance VARCHAR(20) COMMENT '风险承受能力',
    investment_goal VARCHAR(20) COMMENT '投资目标',
    investment_period VARCHAR(20) COMMENT '投资期限',
    risk_score INT DEFAULT 0 COMMENT '风险评分',
    risk_level ENUM('conservative', 'moderate', 'aggressive') COMMENT '风险等级',
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending' COMMENT '状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建审核员表
CREATE TABLE IF NOT EXISTS auditors (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(50) NOT NULL,
    role ENUM('junior', 'senior', 'expert', 'committee') NOT NULL,
    department VARCHAR(100) COMMENT '部门',
    phone VARCHAR(20) COMMENT '联系电话',
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建风险评估记录表
CREATE TABLE IF NOT EXISTS risk_assessments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT NOT NULL,
    assessment_data JSON COMMENT '评估问卷数据',
    risk_score INT NOT NULL COMMENT '风险评分',
    risk_level ENUM('conservative', 'moderate', 'aggressive') NOT NULL,
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- 创建投资建议表
CREATE TABLE IF NOT EXISTS investment_advice (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT NOT NULL,
    portfolio_type ENUM('conservative', 'moderate', 'aggressive') NOT NULL,
    expected_return_min DECIMAL(5,2) COMMENT '预期最低收益',
    expected_return_max DECIMAL(5,2) COMMENT '预期最高收益',
    portfolio_config JSON COMMENT '投资组合配置',
    advice_content TEXT COMMENT '投资建议内容',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- 创建审核流程表
CREATE TABLE IF NOT EXISTS audit_workflow (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT NOT NULL,
    current_level ENUM('junior', 'senior', 'expert', 'committee') NOT NULL,
    workflow_status ENUM('pending', 'in_progress', 'completed', 'rejected') DEFAULT 'pending',
    assigned_auditor_id BIGINT COMMENT '当前审核员ID',
    next_level ENUM('junior', 'senior', 'expert', 'committee') COMMENT '下一级审核',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (assigned_auditor_id) REFERENCES auditors(id)
);

-- 创建审核记录表
CREATE TABLE IF NOT EXISTS audit_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT NOT NULL,
    auditor_id BIGINT NOT NULL,
    audit_level ENUM('junior', 'senior', 'expert', 'committee') NOT NULL,
    audit_status ENUM('pending', 'approved', 'rejected', 'need_review') NOT NULL,
    audit_opinion TEXT COMMENT '审核意见',
    audit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (auditor_id) REFERENCES auditors(id)
);

-- 创建通知记录表
CREATE TABLE IF NOT EXISTS notifications (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT NOT NULL,
    notification_type ENUM('sms', 'email', 'system') NOT NULL,
    title VARCHAR(200) COMMENT '通知标题',
    content TEXT NOT NULL COMMENT '通知内容',
    status ENUM('pending', 'sent', 'failed') DEFAULT 'pending',
    sent_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- 插入初始审核员数据
INSERT INTO auditors (username, password_hash, name, role, department, phone) VALUES
('junior1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uOeG', '初级审核员1', 'junior', '风险审核部', '13800138001'),
('senior1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uOeG', '中级审核员1', 'senior', '风险审核部', '13800138002'),
('expert1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uOeG', '高级审核员1', 'expert', '风险审核部', '13800138003'),
('committee1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uOeG', '投资委员会1', 'committee', '投资委员会', '13800138004');

-- 密码都是: password123
