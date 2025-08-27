-- 银行投资风险审核系统 - 数据库查询脚本
-- 用于快速查看数据库中的相关信息

-- ========================================
-- 1. 查看所有客户信息
-- ========================================
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
ORDER BY created_at DESC;

-- ========================================
-- 2. 查看风险评估记录
-- ========================================
SELECT 
    ra.id as '评估ID',
    ra.customer_id as '客户ID',
    c.name as '客户姓名',
    ra.risk_score as '风险评分',
    ra.risk_level as '风险等级',
    ra.assessment_date as '评估时间',
    ra.assessment_data as '评估数据'
FROM risk_assessments ra
JOIN customers c ON ra.customer_id = c.id
ORDER BY ra.assessment_date DESC;

-- ========================================
-- 3. 查看投资建议
-- ========================================
SELECT 
    ia.id as '建议ID',
    ia.customer_id as '客户ID',
    c.name as '客户姓名',
    ia.portfolio_type as '投资组合类型',
    ia.expected_return_min as '预期最低收益',
    ia.expected_return_max as '预期最高收益',
    ia.advice_content as '投资建议',
    ia.created_at as '创建时间'
FROM investment_advice ia
JOIN customers c ON ia.customer_id = c.id
ORDER BY ia.created_at DESC;

-- ========================================
-- 4. 查看审核员信息
-- ========================================
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
ORDER BY id;

-- ========================================
-- 5. 查看审核流程
-- ========================================
SELECT 
    aw.id as '流程ID',
    aw.customer_id as '客户ID',
    c.name as '客户姓名',
    aw.current_level as '当前审核级别',
    aw.workflow_status as '流程状态',
    aw.assigned_auditor_id as '分配审核员ID',
    a.name as '审核员姓名',
    aw.next_level as '下一级审核',
    aw.created_at as '创建时间',
    aw.updated_at as '更新时间'
FROM audit_workflow aw
JOIN customers c ON aw.customer_id = c.id
LEFT JOIN auditors a ON aw.assigned_auditor_id = a.id
ORDER BY aw.created_at DESC;

-- ========================================
-- 6. 查看审核记录
-- ========================================
SELECT 
    ar.id as '审核记录ID',
    ar.customer_id as '客户ID',
    c.name as '客户姓名',
    ar.auditor_id as '审核员ID',
    a.name as '审核员姓名',
    ar.audit_level as '审核级别',
    ar.audit_status as '审核状态',
    ar.audit_opinion as '审核意见',
    ar.audit_date as '审核时间'
FROM audit_records ar
JOIN customers c ON ar.customer_id = c.id
JOIN auditors a ON ar.auditor_id = a.id
ORDER BY ar.audit_date DESC;

-- ========================================
-- 7. 查看通知记录
-- ========================================
SELECT 
    n.id as '通知ID',
    n.customer_id as '客户ID',
    c.name as '客户姓名',
    n.notification_type as '通知类型',
    n.title as '通知标题',
    n.content as '通知内容',
    n.status as '状态',
    n.sent_at as '发送时间',
    n.created_at as '创建时间'
FROM notifications n
JOIN customers c ON n.customer_id = c.id
ORDER BY n.created_at DESC;

-- ========================================
-- 8. 统计信息查询
-- ========================================

-- 8.1 客户统计
SELECT 
    COUNT(*) as '总客户数',
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as '待审核客户数',
    COUNT(CASE WHEN status = 'approved' THEN 1 END) as '已通过客户数',
    COUNT(CASE WHEN status = 'rejected' THEN 1 END) as '已拒绝客户数',
    SUM(investment_amount) as '总投资金额',
    AVG(risk_score) as '平均风险评分'
FROM customers;

-- 8.2 风险等级分布
SELECT 
    risk_level as '风险等级',
    COUNT(*) as '客户数量',
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 2) as '占比(%)'
FROM customers 
WHERE risk_level IS NOT NULL
GROUP BY risk_level
ORDER BY COUNT(*) DESC;

-- 8.3 审核员工作量统计
SELECT 
    a.name as '审核员姓名',
    a.role as '角色',
    COUNT(ar.id) as '审核记录数',
    COUNT(CASE WHEN ar.audit_status = 'approved' THEN 1 END) as '通过数',
    COUNT(CASE WHEN ar.audit_status = 'rejected' THEN 1 END) as '拒绝数',
    COUNT(CASE WHEN ar.audit_status = 'need_review' THEN 1 END) as '需复审数'
FROM auditors a
LEFT JOIN audit_records ar ON a.id = ar.auditor_id
GROUP BY a.id, a.name, a.role
ORDER BY COUNT(ar.id) DESC;

-- 8.4 待审核工作流统计
SELECT 
    aw.current_level as '当前审核级别',
    COUNT(*) as '待审核数量',
    SUM(c.investment_amount) as '待审核投资总额'
FROM audit_workflow aw
JOIN customers c ON aw.customer_id = c.id
WHERE aw.workflow_status IN ('pending', 'in_progress')
GROUP BY aw.current_level
ORDER BY COUNT(*) DESC;

-- ========================================
-- 9. 特定客户完整信息查询
-- ========================================
-- 使用方法：将下面的 customer_id 替换为实际的客户ID

-- 9.1 客户基本信息
SELECT * FROM customers WHERE id = 1;

-- 9.2 客户风险评估
SELECT * FROM risk_assessments WHERE customer_id = 1;

-- 9.3 客户投资建议
SELECT * FROM investment_advice WHERE customer_id = 1;

-- 9.4 客户审核流程
SELECT 
    aw.*,
    c.name as customer_name,
    a.name as auditor_name
FROM audit_workflow aw
JOIN customers c ON aw.customer_id = c.id
LEFT JOIN auditors a ON aw.assigned_auditor_id = a.id
WHERE aw.customer_id = 1;

-- 9.5 客户审核记录
SELECT 
    ar.*,
    c.name as customer_name,
    a.name as auditor_name
FROM audit_records ar
JOIN customers c ON ar.customer_id = c.id
JOIN auditors a ON ar.auditor_id = a.id
WHERE ar.customer_id = 1
ORDER BY ar.audit_date DESC;

-- 9.6 客户通知记录
SELECT 
    n.*,
    c.name as customer_name
FROM notifications n
JOIN customers c ON n.customer_id = c.id
WHERE n.customer_id = 1
ORDER BY n.created_at DESC;

-- ========================================
-- 10. 数据清理和维护查询
-- ========================================

-- 10.1 查找重复的手机号
SELECT phone, COUNT(*) as count
FROM customers 
GROUP BY phone 
HAVING COUNT(*) > 1;

-- 10.2 查找重复的身份证号
SELECT id_card, COUNT(*) as count
FROM customers 
GROUP BY id_card 
HAVING COUNT(*) > 1;

-- 10.3 查找孤立的审核记录（没有对应客户）
SELECT ar.* 
FROM audit_records ar
LEFT JOIN customers c ON ar.customer_id = c.id
WHERE c.id IS NULL;

-- 10.4 查找孤立的投资建议（没有对应客户）
SELECT ia.* 
FROM investment_advice ia
LEFT JOIN customers c ON ia.customer_id = c.id
WHERE c.id IS NULL;

-- ========================================
-- 11. 性能优化查询
-- ========================================

-- 11.1 查看表大小
SELECT 
    name as '表名',
    sql as '建表语句'
FROM sqlite_master 
WHERE type='table' 
ORDER BY name;

-- 11.2 查看索引
SELECT 
    name as '索引名',
    tbl_name as '表名',
    sql as '索引定义'
FROM sqlite_master 
WHERE type='index' 
ORDER BY tbl_name, name;

-- ========================================
-- 使用说明：
-- 1. 在SQLite命令行中执行：.read database/queries.sql
-- 2. 或者在Python中使用：
--    import sqlite3
--    conn = sqlite3.connect('finance_athena.db')
--    with open('database/queries.sql', 'r') as f:
--        sql = f.read()
--    conn.executescript(sql)
-- ========================================
